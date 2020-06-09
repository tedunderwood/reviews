import random, os, sys
from collections import Counter

import string, csv
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from scipy.spatial.distance import cosine

# GET METADATA

# It would probably be simpler if I had written this to use a pandas dataframe,
# but I didn't; I'm using aligned numpy vectors. The reasons lie in the possibility
# of overlapping genre assignments in the LoC version of this code.

genredocs = dict()
genredates = dict()
genreauthors = dict()

allnonrandom = set()

genre_assigns = dict()

meta = pd.read_csv('genremetadata4kirkus.tsv', sep = '\t', index_col = 'docid', dtype = {'Dominant_Topic': object})

allgenres = list(set(meta['Dominant_Topic']))

for g in allgenres:
    df = meta.loc[meta['Dominant_Topic'] == g, : ]
    genredocs[g] = np.array(df.index.tolist())
    genredates[g] = np.array(df['date'])
    genreauthors[g] = np.array(df['author'])

    for d in genredocs[g]:
        genre_assigns[d] = g

allnonrandom = set(meta.index.tolist())

for g in allgenres:
    docsnotinthisgenre = list(allnonrandom - set(genredocs[g]))
    genredocs['not' + g] = np.array(docsnotinthisgenre)
    genreauthors['not' + g] = np.array(meta.loc[docsnotinthisgenre, 'author'])
    genredates['not' + g] = np.array(meta.loc[docsnotinthisgenre, 'date'])

# the random genre

rand_df = pd.read_csv('randommetadata4kirkus.tsv', sep = '\t', index_col = 'docid')
genredocs['random'] = np.array(rand_df.index.tolist())
genreauthors['random'] = np.array(rand_df['author'].tolist())
genredates['random'] = np.array(rand_df['date'].tolist())

alldocids = set(genredocs['random']).union(allnonrandom)

# LOAD tfidf vectors

tfidf_vectors = dict()

# The first column is docid, the rest are floats
# for a particular word, scaled by idf.

havevectors = set()

with open('tfidf_matrix_4kirkus.tsv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        if fields[0] == 'docid':
            continue   # that's the header
        thevector = np.array([float(x) for x in fields[1:]])
        docid = fields[0]
        if docid not in alldocids:
            print('special')
            docid = docid.replace('uc1.b', 'uc1.$b')
            if docid not in alldocids:
                print('docid error')
        tfidf_vectors[docid] = thevector
        havevectors.add(docid)

# ACTUAL MEASUREMENT

# Our process is as follows:

# select a docid randomly from the allnonrandom list
# get a genre assignment randomly from its list of genres
# select a docid from that genre list, masked by date
# measure in-genre distance
# select a docid from the random list, masked by date
# also one from the nonrandom list, masked by date
# measure both outgenre distances
# record this comparison

def get_doc_in_date_range(author, date, genre):
    global genredocs, genredates, genreauthors

    # let's select a docid that is no more than ten years earlier, no
    # more than ten years later, and *not* our original docid

    # returns the match, and the date of the selected docid

    mask = (genredates[genre] > (date - 10)) & (genredates[genre] < (date + 10)) & (genreauthors[genre] != author)

    candidates = genredocs[genre][mask]

    if len(candidates) < 1:
        return 'no match', 0, 'anonymous'
    else:
        match = random.sample(list(candidates), 1)[0]
        index = np.where(genredocs[genre] == match)
        newdate = genredates[genre][index][0]
        newauthor = genreauthors[genre][index][0]
        return match, newdate, newauthor

def get_doc_with_date_match(author, date, genre):
    global genredocs, genredates, all_genre_assigns

    # let's select a docid that exactly matches the
    # date of the original docid

    mask = (genredates[genre] == date) & (genreauthors[genre] != author)

    candidates = genredocs[genre][mask]

    if len(candidates) < 1:
        return 'no match'
    else:
        match = random.sample(list(candidates), 1)[0]
        return match

def measure_cosine(docA, docB):
    global tfidf_vectors

    assert docA != docB

    return cosine(tfidf_vectors[docA], tfidf_vectors[docB])

def get_othergenredoc(genretoavoid, author, date):

    othermatch = get_doc_with_date_match(author, date, 'not' + genretoavoid)

    return othermatch

failures = 0

results = list()

for i in range(10000):

    if i % 100 == 1:
        print(i)

    firstdoc = random.sample(allnonrandom, 1)[0]

    genre = genre_assigns[firstdoc]
    firstdate = genredates[genre][genredocs[genre] == firstdoc][0]
    firstauthor = genreauthors[genre][genredocs[genre] == firstdoc][0]

    genrematch, genrematchdate, matchauthor = get_doc_in_date_range(firstauthor, firstdate, genre)

    if genrematch == 'no match':
        failures += 1
        continue

    datediff = abs(firstdate - genrematchdate)
    meandate = (firstdate + genrematchdate) / 2

    if firstdoc not in havevectors or genrematch not in havevectors:
        failures += 1
        continue

    in_genre_dist = measure_cosine(firstdoc, genrematch)

    fullyrandommatchA = get_doc_with_date_match(firstauthor, genrematchdate, 'random')
    fullyrandommatchB = get_doc_with_date_match(matchauthor, firstdate, 'random')

    othergenrematchA = get_othergenredoc(genre, firstauthor, genrematchdate)
    othergenrematchB = get_othergenredoc(genre, matchauthor, firstdate)

    if fullyrandommatchA == 'no match' or fullyrandommatchB == 'no match':
        failures += 1
        continue
    elif othergenrematchA == 'no match' or othergenrematchB == 'no match':
        failures += 1
        continue
    elif fullyrandommatchA not in havevectors or fullyrandommatchB not in havevectors or othergenrematchA not in havevectors or othergenrematchB not in havevectors:
        failures += 1
        continue

    fully_random_dist_A = measure_cosine(firstdoc, fullyrandommatchA)
    fully_random_dist_B = measure_cosine(genrematch, fullyrandommatchB)

    fully_random_dist = (fully_random_dist_A + fully_random_dist_B) / 2

    other_genre_dist_A = measure_cosine(firstdoc, othergenrematchA)
    other_genre_dist_B = measure_cosine(genrematch, othergenrematchB)

    other_genre_dist = (other_genre_dist_A + other_genre_dist_B) / 2

    result = [genre, firstdoc, firstdate, genrematchdate, datediff, meandate, in_genre_dist, fully_random_dist, other_genre_dist, fully_random_dist - in_genre_dist, other_genre_dist - in_genre_dist]
    results.append(result)

with open('kirkus_results.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('genre\tfirstdoc\tfirstdate\tmatchdate\tdatediff\tmeandate\tingenredist\tfullrandomdist\tothergenredist\tfullrandomdiff\tothergenrediff\n')
    for res in results:
        f.write('\t'.join([str(x) for x in res]) + '\n')

import ast, random, os, sys
from collections import Counter

import string, csv
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from scipy.spatial.distance import cosine

# GET METADATA

# Because a volume can have more than one genre, the metadata for this
# experiment is not a table of rows uniquely identified by docid.

# Instead, each row records an *assignment* of a docid to a genre,
# and there can be multiple rows for a single volume/docid.

# We also have "date" recorded in each row, because we are often going
# to want to select volumes from a subset of a category limited by date.
# We could build pandas dataframes to do that, but it seems simpler just
# to use a numpy mask

# We'll create a dictionary genreframes that has a separate key for each genre;
# the value for each genre will be a pandas dataframe. We can easily limit this
# by date.

genredocs = dict()
genredates = dict()
genreauthors = dict()
allgenres = ['allnonrandom']

genredocs['allnonrandom'] = list()
genredates['allnonrandom'] = list()
genreauthors['allnonrandom'] = list()

# Now, the question is, how should we sample volumes? Many volumes
# may be in more than one category. If we test in-genre distance for
# every category they're a member of, volumes with multiple assignments
# may be overrepresented.

# So we are instead going to sample from a list of volumes,
# and then secondarily select from within the list of non-random
# genres for that volume. To do that we'll create the following dictionary:

all_genre_assigns = dict()

with open('genre_assignments_4loc.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        g = row['genre']
        if g not in genredocs:
            genredocs[g] = []
            genredates[g] = []
            genreauthors[g] = []
            allgenres.append(g)

        docid = row['docid']
        genredocs[g].append(docid)
        genredates[g].append(int(row['date']))
        genreauthors[g].append(row['author'])

        if g != 'random':
            if docid not in genredocs['allnonrandom']:
                genredocs['allnonrandom'].append(docid)
                genredates['allnonrandom'].append(int(row['date']))
                genreauthors['allnonrandom'].append(row['author'])
            if docid not in all_genre_assigns:
                all_genre_assigns[docid] = []
            all_genre_assigns[docid].append(g)

for g in allgenres:
    genredates[g] = np.array(genredates[g])
    genredocs[g] = np.array(genredocs[g])
    genreauthors[g] = np.array(genreauthors[g])
    # that will allow us to mask

# LOAD tfidf vectors

tfidf_vectors = dict()

# The first column is docid, the rest are floats
# for a particular word, scaled by idf.

with open('tfidf_matrix_4loc.tsv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        if fields[0] == 'docid':
            continue   # that's the header
        thevector = np.array([float(x) for x in fields[1:]])
        docid = fields[0]
        tfidf_vectors[docid] = thevector

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
        return 'no match', 0, 'ge'
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

    for i in range(5):
        othermatch = get_doc_with_date_match(author, date, 'allnonrandom')
        genresofmatch = all_genre_assigns[othermatch]
        if len(genresofmatch) == 1 and genresofmatch[0] == genre:
            avoidthis = True
        else:
            avoidthis = False

        if not avoidthis:
            return othermatch

    return 'no match'

failures = 0

results = list()

for i in range(10000):

    if i % 100 == 1:
        print(i)

    firstdoc = random.sample(list(genredocs['allnonrandom']), 1)[0]

    genre = random.sample(all_genre_assigns[firstdoc], 1)[0]
    firstdate = genredates[genre][genredocs[genre] == firstdoc][0]
    firstauthor = genreauthors[genre][genredocs[genre] == firstdoc][0]

    genrematch, genrematchdate, matchauthor = get_doc_in_date_range(firstauthor, firstdate, genre)

    if genrematch == 'no match':
        failures += 1
        continue

    datediff = abs(firstdate - genrematchdate)
    meandate = (firstdate + genrematchdate) / 2

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

    fully_random_dist_A = measure_cosine(firstdoc, fullyrandommatchA)
    fully_random_dist_B = measure_cosine(genrematch, fullyrandommatchB)

    fully_random_dist = (fully_random_dist_A + fully_random_dist_B) / 2

    other_genre_dist_A = measure_cosine(firstdoc, othergenrematchA)
    other_genre_dist_B = measure_cosine(genrematch, othergenrematchB)

    other_genre_dist = (other_genre_dist_A + other_genre_dist_B) / 2

    result = [genre, firstdoc, firstdate, genrematchdate, datediff, meandate, in_genre_dist, fully_random_dist, other_genre_dist, fully_random_dist - in_genre_dist, other_genre_dist - in_genre_dist]
    results.append(result)

with open('loc_results.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('genre\tfirstdoc\tfirstdate\tmatchdate\tdatediff\tmeandate\tingenredist\tfullrandomdist\tothergenredist\tfullrandomdiff\tothergenrediff\n')
    for res in results:
        f.write('\t'.join([str(x) for x in res]) + '\n')

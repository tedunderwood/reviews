import pandas as pd
import random

# We start by identifying the topics that have been flagged as
# identifying genres or genre-like groupings. This draws on work
# by Peizhen Wu and Ted Underwood.

topics = pd.read_csv('genre_80_mallet_categories_for_20c_exp.csv')
genretopics = topics.dropna(subset = ['possible_genres'])
genretopics = genretopics['Topic_Num'].tolist()
print(genretopics)

# Now we want to select the volumes associated with each topic;
# this draws on the topic model of Kirkus Reviews created by
# Yuerong Hu.

# We will also select 1000 random volumes from the whole dataset
# to permit a fully-random contrast set as well as an other-
# genres contrast set.

meta = pd.read_csv('kirkusreviews_topicinfo_added.tsv', sep = '\t')

topicdictionary = dict()

for g in genretopics:
    selected = meta.loc[meta['Dominant_Topic'] == g, :]
    topicdictionary[g] = selected['docid'].tolist()

# We will also select 1000 random volumes from the whole dataset
# to permit a fully-random contrast set as well as an other-
# genres contrast set.

allvols = set(meta['docid'])
topicdictionary['random'] = random.sample(allvols, 1000)

# Let's print a short metadata table containing all the metadata we'll need for the
# next step

allselected = list()

for k, v in topicdictionary.items():
    print(k, len(v))
    allselected.extend(v)

allselected = list(set(allselected))

meta.set_index('docid', inplace = True)

outmeta = meta.loc[allselected, ['Dominant_Topic', 'author', 'orig_title', 'Topic_Perc_Contrib']]

def lower_and_trim(author):
    return author.lower().strip('1234567890 ,.()[]\t\n"')

outmeta = outmeta.assign(author = outmeta.author.map(lower_and_trim))

outmeta.to_csv('mallet80metadata4experiment.tsv', sep = '\t', index_label = 'docid')

# make paths to these volumes

import SonicScrewdriver as utils
import os

missing = set()
idmapper = dict()

for anid in allselected:

    path, postfix = utils.pairtreepath(anid, '/Volumes/TARDIS/work/ef/fic/')
    totalpath = path + postfix + '/' + utils.clean_pairtree(anid) + '.json.bz2'

    if not os.path.isfile(totalpath):
        if '$' in anid:
            newid = anid.replace('uc1.b', 'uc1.$b')
        else:
            newid = anid.replace('uc1.$b', 'uc1.b')

        path, postfix = utils.pairtreepath(newid, '/Volumes/TARDIS/work/ef/fic/')
        totalpath = path + postfix + '/' + utils.clean_pairtree(newid) + '.json.bz2'
        if os.path.isfile(totalpath):
            idmapper[anid] = totalpath
        else:
            missing.add(anid)
    else:
        idmapper[anid] = totalpath

print("Found: ", len(idmapper))
print("Missing: ", len(missing))
print()

from collections import Counter

import csv
import numpy as np
from collections import Counter

# BUILD TRANSLATORS.

# We want to translate ocr errors and American spellings
# to the correct British spelling when possible.

translator = dict()

with open('../../bpo/gethathimatches/CorrectionRules.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

with open('../../bpo/gethathimatches/VariantSpellings.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

print('Translators built.')

paths = list(set(idmapper.values()))

# The following code is borrowed from Yuerong Hu, and also uses HTRC Feature Reader, by
# Peter Organisciak.

from htrc_features import FeatureReader

def get_token_counts(vol,hat,tail):
    df_tl = vol.tokenlist().reset_index()# convert to dataframe
    df_tl = df_tl[df_tl['section']=='body']#get rid of header and footer; keep only body
    page_count=df_tl['page'].tolist()[-1]# get total page number
    page_hat=round(page_count*hat)# find the 15% page
    page_tail=page_count-round(page_count*tail)# find the "counter-5%" page
    df_tl=df_tl[df_tl['page'].between(page_hat, page_tail, inclusive=False)] # locate the pages in between
    series_tl=df_tl.groupby(["token"]).size()# group the tokens across pages
    new_df_tl = series_tl.to_frame().reset_index() # convert to df
    return new_df_tl

docfreqs = Counter()
termfreqs = dict()
ctr = 0

fr = FeatureReader(paths)
for vol in fr.volumes():
    ctr += 1
    if ctr % 100 == 1:
        print(ctr)

    output = get_token_counts(vol,0.15,0.05)
    docid = str(vol.id)

    thesewords = Counter()

    for row in output.itertuples(index = False):
        if pd.isnull(row[0]):
            continue
        word = row[0].lower().strip('.",')

            # we're lowercasing everything and also
            # stripping certain kinds of punctuation that
            # may be glued to the word without really
            # changing its meaning

        if len(word) < 2 and not word.isalpha():
            continue

            # we don't want to include punctuation marks in our vocabulary

        if word in translator:
            word = translator[word]

            # we correct ocr errors and convert to British spelling

        thesewords[word] = int(row[1])      # the raw count of this token in this document

    # increment document frequencies

    for w, count in thesewords.items():
        docfreqs[w] += 1
        # note that these are document frequencies, so only increment by 1
        # not by the term frequency (count) in the document

    # also create a dictionary entry in termfreqs, where the key is
    # a docid, and the value is a Counter of term frequencies

    termfreqs[docid] = thesewords

# MAKE VOCABULARY OF 2500 MOST COMMON WORDS

vocab = docfreqs.most_common(2500)

with open('kirkus_vocabulary.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('word\tdocfreq\n')
    for word, docfreq in vocab:
        f.write(word + '\t' + str(docfreq) + '\n')

vocabwords = [x[0] for x in vocab]
docvector = np.array([x[1] for x in vocab])

# MAKE A MATRIX OF TF-IDF VALUES

dictforpandas = dict()

for docid, wordfreqs in termfreqs.items():
    termvector = np.zeros(2500)
    for idx, word in enumerate(vocabwords):
        if word in wordfreqs:
            termvector[idx] = wordfreqs[word]

    termvector = termvector / docvector
    dictforpandas[docid] = termvector

outdf = pd.DataFrame.from_dict(dictforpandas, orient = 'index', columns = vocabwords)
outdf.to_csv('tfidf_matrix_4kirkus.tsv', sep = '\t', index_label = 'docid')


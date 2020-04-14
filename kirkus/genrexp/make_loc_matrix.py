# make_loc_matrix

# We're preparing to measure
# cosine distances on genre categories inferred from
# Library of Congress genre/form/subject headings.

# This part of the code is purely data preparation:
# it infers a vocabulary of the top 2500 words,
# calculates inverse document frequencies for that vocabulary,
# and saves a matrix where rows are docids, columns are
# vocabulary words, and cells are tf-idf scores for the words.

import pandas as pd
import os, glob
from collections import Counter

import csv
import numpy as np

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

# Now get the token frequencies for individual docids,
# using data created by Yuerong Hu.

rootpath = '/Volumes/T5/genrexp2_token_counts/'

filepaths = glob.glob(rootpath + '*.csv')

docfreqs = Counter()
termfreqs = dict()

for path in filepaths:
    # we're iterating through separate files for eachdocid

    df = pd.read_csv(path, index_col = 0)

    thesewords = Counter()

    # .itertuples() gives relatively fast iteration through Pandas DataFrames

    for row in df.itertuples(index = False):
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

    docid = path.split('/')[-1].replace('.csv', '')

    termfreqs[docid] = thesewords

# MAKE VOCABULARY OF 2500 MOST COMMON WORDS

vocab = docfreqs.most_common(2500)

with open('loc_vocabulary.tsv', mode = 'w', encoding = 'utf-8') as f:
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
outdf.to_csv('tfidf_matrix_4loc.tsv', sep = '\t', index_label = 'docid')




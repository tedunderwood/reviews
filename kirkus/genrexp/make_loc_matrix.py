# make_loc_matrix

# Cosine distances on genre categories inferred from
# Library of Congress genre/form/subject headings.

# This part of the code is purely data preparation:
# it infers a vocabulary of the top 2500 words,
# calculates inverse document frequencies for that vocabulary,
# and saves a matrix where rows are docids and columns are
# vocabulary words.

import pandas as pd
import os, glob
from collections import Counter

import csv
import numpy as np

# BUILD TRANSLATORS.

punctuationstring = string.punctuation + '—‘’“”'
punctzapper = str.maketrans(punctuationstring, ' ' * len(punctuationstring))

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

# if os.path.exists('vocabulary.tsv'):
#     havevocab = True
#     vocab = dict()
#     with open('vocabulary.tsv', encoding = 'utf-8') as f:
#         for line in f[1:]                      # skip header
#             fields = line.strip().split('\t')
#             vocab[fields[0]] = int(fields[1])

# else:
#     havevocab = False

rootpath = '/Volumes/T5/genrexp2_token_counts/'

filepaths = glob.glob(rootpath + '*.csv')

docfreqs = Counter()
termfreqs = dict()

for path in filepaths:
    df = pd.read_csv(path, index_col = 0)
    thesewords = Counter()
    for row in df.itertuples(index = False):
        if pd.isnull(row[0]):
            continue
        word = row[0].lower().strip('.",') # the last strip shouldn't be necessary
                                         # but in practice there are stray double
                                         # quotes that can prove problematic

            # lowercase everything

        if len(word) < 2 and not word.isalpha():
            continue

            # we don't want to include punctuation marks in our vocabulary

        if word in translator:
            word = translator[word]

            # we correct ocr errors and convert to British spelling

        thesewords[word] = int(row[1])      # the raw count of this token in this document

    for w, count in thesewords.items():
        docfreqs[w] += 1
        # note that these are document frequencies, so only increment by 1
        # not by the term frequency (count) in the document

    docid = path.split('/')[-1].replace('.csv', '')

    termfreqs[docid] = thesewords

vocab = docfreqs.most_common(2500)

with open('vocabulary.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('word\tdocfreq\n')
    for word, docfreq in vocab:
        f.write(word + '\t' + str(docfreq) + '\n')

vocabwords = [x[0] for x in vocab]
docvector = np.array([x[1] for x in vocab])

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




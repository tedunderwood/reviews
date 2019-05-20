# concatenate_results.py

# Gathers the reviews that made it through the Fiction Filter,
# adds back in some divided reviews, and organizes the metadata

import os, csv, sys


import pandas as pd
import numpy as np
from collections import Counter

# This script turns paired text and metadata files into a feature matrix
# that can be used to train a model of "reviews-of-fiction," excluding
# reviews of nonfiction that tend to be mixed in.

infiles = ['tedreviewtexts0to100.txt', 'jessicareviewtexts100to200.txt',
'jessicareviewtexts200to300.txt','jessicareviewtexts300to400.txt',
'tedreviewtexts400to500.txt', 'tedreviewtexts500to600.txt']

metafiles = ['tedreviewmeta0to100.tsv', 'jessicareviewmeta100to200.tsv', 'jessicareviews200to300.tsv',
'jessicareviews300to400.tsv', 'tedreviews400to500.tsv', 'tedreviews500to600.tsv']

# So, I readily admit that the next section of code is a mess.
# It parses the text file,with sections of metadata and text delimited
# by lines of equals-signs and lines of hyphens.

# It's not the best-structured data in the world; I was compromising
# btw human readability and computer readability. So parsing it becomes
# a bit of a tangle.

seqstokeep = set()
tdf = pd.read_csv('trainingdata.tsv', sep = '\t')
for idx, row in tdf.iterrows():
    if row.genrecode == 'y':
        seqstokeep.add(str(row.sequenceID))

genredict = dict()

metaroot = '../processedmeta/'
textroot = '../processedtexts/'

toadd = dict()

for mf in metafiles:
    metadf = pd.read_csv(metaroot + mf, sep = '\t', dtype = {'RecordID': str, 'seq': str})
    for idx, row in metadf.iterrows():

        isfic = row.isfiction
        if not pd.isnull(isfic) and isfic == 'y' and not pd.isnull(row.howpositive):
            if row.seq in seqstokeep:
                toadd[row.RecordID] = str(row.seq)
                if not '-' in row.seq:
                    genredict[row.RecordID] = isfic

        elif not pd.isnull(isfic) and isfic == 'n':
            genredict[row.RecordID] = isfic

resultroot = '../filtered/'

gotright = 0
gotwrong = 0

found = set()

totakeout = set()

for decade in range(1800, 1940, 10):
    with open(resultroot + 'reviews' + str(decade) + '.txt', mode = 'r') as f:
        for line in f:
            fields = line.split('\t')
            recid = fields[0]
            found.add(recid)
            if recid in toadd:
                toadd.pop(recid)
            if recid in genredict and genredict[recid] == 'y':
                gotright += 1
            elif recid in genredict and genredict[recid] == 'n':
                gotwrong += 1
                print(recid)
                totakeout.add(recid)

missing = 0
print(gotwrong / (gotright + gotwrong))
print()
for key, value in genredict.items():
    if value == 'y' and not key in found:
        missing += 1
print(missing)
print(len(toadd))

toadd = set(toadd.values())
additionalreviews = dict()

texted = 0

def parsefile(path, additionalreviews, texted):

    seq = ''
    record = ''
    valid = True

    with open(path, encoding = 'utf-8') as f:
        meta = False
        for line in f:
            if line.startswith('====='):

                meta = True
                seq = ''
                record = ''

            elif line.startswith('-----'):
                meta = False

            elif meta and len(seq) < 1:
                fields = line.strip().split()
                seq = fields[0]
                record = fields[1]

            elif not meta and len(line) > 1:
                texted += 1
                if seq in toadd:
                    if record in additionalreviews:
                        print('bloop')
                        additionalreviews[record] = additionalreviews[record] + ' ' + line.strip()
                    else:
                        additionalreviews[record] = line.strip()


    return additionalreviews, texted

# HERE IS WHERE WE ACTUALLY START PARSING.
# sorry, this code is a mess

for textfile in infiles:
    additionalreviews, texted = parsefile(textroot + textfile, additionalreviews, texted)

print(texted)

for decade in range(1800, 1940, 10):
    copied = []
    with open(resultroot + 'reviews' + str(decade) + '.txt', mode = 'r') as f:
        for line in f:
            fields = line.split('\t')
            recid = fields[0]
            if not recid in totakeout:
                copied.append(line)

    with open(resultroot + 'all_fic_reviews.txt', mode = 'a', encoding = 'utf-8') as f:
        for line in copied:
            f.write(line)

with open(resultroot + 'all_fic_reviews.txt', mode = 'a', encoding = 'utf-8') as f:
    for key, value in additionalreviews.items():
        outline = str(key) + '\t1.0\t' + value + '\n' 
        f.write(outline)





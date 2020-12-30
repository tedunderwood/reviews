# -*- coding: utf-8 -*-
# publisherfinder.py

import glob, sys, csv, re
from collections import Counter

anynumregex = re.compile('\S{0,3}\d\S{0,3}')

args = sys.argv

year = args[1]

import read_pubnames

all_reviewwords, reviewdict = read_pubnames.get_names('brd_pubs_indexed1930s.tsv')

all_review_codes = set([x.replace('.', '') for x in reviewdict.keys()])
all_review_codes.add('summary')

publishers = []

with open('30spublishers.txt', encoding = 'utf-8') as f:
    for line in f:
        publishers.append(line.strip())

targetpaths = glob.glob('/media/secure_volume/brd/output/' +year + '*.tsv')

if len(targetpaths) > 0:
    targetpath = targetpaths[0]

newpublishers = Counter()
newreviews = Counter()

with open(targetpath, encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:

        publishwords = row['publisher'].split()

        for w in publishwords:
            w = w.strip('.,[]()')
            if len(w) < 3:
                continue
            elif anynumregex.fullmatch(w):
                continue
            else:
                newpublishers[w] +=1

        review = row['publication']

        newreviews[review] += 1


with open('newpublishers.tsv', mode = 'w', encoding = 'utf-8') as f:
    for k, v in newpublishers.most_common(1000):

        if k in publishers:
            continue
        else:
            f.write(k +'\t' + str(v) + '\n')

with open('oldpublishers.tsv', mode = 'w', encoding = 'utf-8') as f:
    for p in publishers:
        if p in newpublishers:
            f.write(p + '\t' + str(newpublishers[p]) + '\n')
        else:
            f.write(p + '\t0\n')

with open('newreviews.tsv', mode = 'w', encoding = 'utf-8') as f:
    for k, v in newreviews.most_common(1000):
        if k in all_review_codes:
            continue
        else:
            f.write(k +'\t' + str(v) + '\n')

with open('oldreviews.tsv', mode = 'w', encoding = 'utf-8') as f:
    for r in all_review_codes:
        r1 = r.replace('.', '')
        totalcount = newreviews[r] + newreviews[r1]
        f.write(r + '\t' + str(totalcount) + '\n')














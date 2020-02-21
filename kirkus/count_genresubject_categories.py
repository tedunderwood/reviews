import pandas as pd
from collections import Counter

allcats = Counter()

datesets = dict()
for period in ['pre1955', '1955-1980', 'post1980']:
    datesets[period] = Counter()

meta = pd.read_csv('kirkus_htrc_merged.csv', low_memory = False)

for idx, row in meta.iterrows():
    if not pd.isnull(row['subjects']):
        subjects = row['subjects'].split('|')
    else:
        subjects = list()

    if not pd.isnull(row['genres']):
        genres = row['genres'].split('|')
    else:
        genres = list()

    if not pd.isnull(row['latestcomp']):
        date = int(row['latestcomp'])
    else:
        date = 0

    if date < 1900:
        continue
    elif date < 1955:
        period = 'pre1955'
    elif date < 1981:
        period = '1955-1980'
    else:
        period = 'post1980'

    for g in genres:
        allcats[g] += 1
        datesets[period][g] += 1

    for s in subjects:
        allcats[s] += 1
        datesets[period][s] += 1

commoncats = [x[0] for x in allcats.most_common(1000)]

with open('common_headings.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('category\talloccurences\tpre1955\t1955-1980\tpost1980\n')
    for c in commoncats:
        outrow = c + '\t' + str(allcats[c]) + '\t' + str(datesets['pre1955'][c]) + '\t' + str(datesets['1955-1980'][c]) + '\t' + str(datesets['post1980'][c]) + '\n'
        f.write(outrow)





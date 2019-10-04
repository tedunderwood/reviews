# create_genres2.py

# this is a second round of genre-creation
# bringing us to a full complement

import pandas as pd
import ast, random
from collections import Counter

books = pd.read_csv('grouped_books.tsv', sep = '\t')

cats = Counter()

allwars = set()

indices = dict()

the_categories = ['britain', 'northamerica', 'englishfiction', 'stories', 'biography', 'random']

for tc in the_categories:
    indices[tc] = set()

the_qualifications = {'britain': {'scotland', 'ireland', 'england', 'great britain',
    'london', 'british'},
    'northamerica': {'american fiction', 'new york', 'indians of north america',
    'frontier and pioneer life', 'african americans', 'massachusetts', 'michigan',
    'united states', 'new england', 'western stories'},
    'random': {}, 'stories': {'short stories'},
    'biography': {'containsbiogmaterial', 'biography', 'autobiography', 'isbiographical'},
    'englishfiction': {'english fiction'}}

for idx, row in books.iterrows():
    if not pd.isnull(row['genres']):
        g = ast.literal_eval(row['genres'])
        g = set([x.lower() for x in g])
    else:
        g = set()

    if not pd.isnull(row['subjects']):
        s = ast.literal_eval(row['subjects'])
        s = set([x.lower() for x in s])
    else:
        s = set()

    storiesalready = False

    for category, quals in the_qualifications.items():
        for q in quals:
            if q in g or q in s:
                indices[category].add(idx)
                cats[category] += 1
                if category == 'stories':
                    storiesalready = True
                break

    if not storiesalready and ('stories' in row['title'].lower()):
        indices['stories'].add(idx)
        cats['stories'] += 1

indices['random'] = random.sample(books.index.tolist(), 200)
cats['random'] = 200

print(cats)

for i, tc in enumerate(the_categories):
    for tc2 in the_categories[i + 1 : ]:
        tcm = indices[tc]
        tcm2 = indices[tc2]
        jaccard = len(tcm.intersection(tcm2)) / len(tcm.union(tcm2))
        jaccard = int(jaccard * 1000) / 1000
        print(tc, tc2, jaccard)

for tc in the_categories:
    thisset = indices[tc]
    k = 200
    if len(thisset) < k:
        k = len(thisset)

    chosen = random.sample(thisset, k)
    chosendf = books.loc[chosen, : ]
    chosendf = chosendf.assign(is_fic = [''] * k)

    chosendf.to_csv('../genremeta/' + tc + '.tsv', index = False, sep = '\t')


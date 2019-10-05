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

the_categories = ['britain', 'northamerica', 'englishfiction', 'stories', 'biography', 'random',
    'history', 'novel', 'romance', 'juvenile', 'folklore', 'social', 'war', 'unmarked']

for tc in the_categories:
    indices[tc] = set()

categories_found = pd.read_csv('common_book_genres.tsv', sep = '\t')

allwars = set()
for c in categories_found['category']:
    if 'war ' in c or ' war' in c or ' wars' in c or 'revolution' in c:
        allwars.add(c)

the_qualifications = {'britain': {'scotland', 'ireland', 'england', 'great britain',
    'london', 'british'},
    'northamerica': {'american fiction', 'new york', 'indians of north america',
    'frontier and pioneer life', 'african americans', 'massachusetts', 'michigan',
    'united states', 'new england', 'western stories'},
    'random': {}, 'stories': {'short stories'},
    'biography': {'containsbiogmaterial', 'biography', 'autobiography', 'isbiographical'},
    'englishfiction': {'english fiction'},
    'history': {'history', 'historical fiction'},
    'folklore': {'legends', 'folklore', 'fairy tales', 'folktales', 'folk tales', 'folk-lore, irish', 'folk-lore, bengali', 'tales', 'mythology', 'mythology, norse', 'mythology, celtic', 'mythology, slavic'},
    'romance': {},
    'novel': {},
    'juvenile': {'juvenile fiction', 'juvenile audience', 'juvenile literature'},
    'social': {'social life and customs', 'social conditions', 'social problems', 'social classes',
        'manners and customs'},
    'war': allwars,
    'unmarked': {}
    }

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
    folklorealready = False

    for category, quals in the_qualifications.items():
        for q in quals:
            if q in g or q in s:
                indices[category].add(idx)
                cats[category] += 1
                if category == 'stories':
                    storiesalready = True
                elif category == 'folklore':
                    folklorealready = True
                break

    titlegroup = False

    if not storiesalready and ('stories' in row['title'].lower()):
        indices['stories'].add(idx)
        cats['stories'] += 1
        titlegroup = True

    if 'a novel' in row['title'].lower():
        cats['novel'] += 1
        indices['novel'].add(idx)
        titlegroup = True

    if 'a romance' in row['title'].lower() or 'the romance' in row['title'].lower():
        cats['romance'] += 1
        indices['romance'].add(idx)
        titlegroup = True

    if 'legends' in row['title'].lower() or 'folktales' in row['title'].lower() or 'folk tales' in row['title'].lower():
        indices['folklore'].add(idx)
        cats['folklore'] += 1
        titlegroup = True

    if len(g) < 1 and len(s) < 1 and not titlegroup:
        cats['unmarked'] += 1
        indices['unmarked'].add(idx)

allbooks = set(books.index.tolist())

outrows = []

for tc in the_categories:
    thisset = allbooks - indices[tc]
    # we subtract the set to get the contrast set

    k = 200
    if len(thisset) < k:
        k = len(thisset)

    outrow = tc + '\t' + str(len(indices[tc])) + '\t' + str(len(thisset)) + '\n'

    chosen = random.sample(thisset, k)
    chosendf = books.loc[chosen, : ]
    chosendf = chosendf.assign(is_fic = [''] * k)

    chosendf.to_csv('../genremeta/' + tc + '_contrast.tsv', index = False, sep = '\t')

    outrows.append(outrow)

with open('../genremeta/contrast_sizes.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('category\tsize\tcontrastsize\n')
    for row in outrows:
        f.write(row)

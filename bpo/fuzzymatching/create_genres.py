import pandas as pd
import ast, random
from collections import Counter

books = pd.read_csv('grouped_books.tsv', sep = '\t')

cats = Counter()

allwars = set()

indices = dict()

the_categories = ['history', 'novel', 'romance', 'juvenile', 'folklore', 'social', 'war', 'unmarked']

for tc in the_categories:
    indices[tc] = set()

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

    if 'history' in g or 'history' in s or 'historical fiction' in s or 'historical fiction' in g:
        cats['history'] += 1
        indices['history'].add(idx)

    if 'a romance' in row['title'].lower() or 'the romance' in row['title'].lower():
        cats['romance'] += 1
        indices['romance'].add(idx)

    if 'a novel' in row['title'].lower():
        cats['novel'] += 1
        indices['novel'].add(idx)

    if 'legends' in g or 'legends' in s or 'folklore' in g or 'folklore' in s or 'fairy tales' in g or 'fairy tales' in s or 'folktales' in g or 'folk tales' in s or 'Folk-lore, Irish' in s or 'Folk-lore, Bengali' in s or 'folk tales' in row['title'].lower() or 'folktales' in row['title'].lower() or 'tales' in s or 'tales' in g or 'mythology, norse' in s or 'mythology' in s or 'mythology, celtic' in s or 'mythology, slavic' in s or 'legends' in row['title'].lower():
        cats['folklore'] += 1
        indices['folklore'].add(idx)

    if 'juvenile fiction' in g or 'juvenile fiction' in s or 'juvenile audience' in g or 'juvenile audience' in s or 'juvenile literature' in g or 'juvenile literature' in s:
        cats['juvenile'] += 1
        indices['juvenile'].add(idx)

    if 'social life and customs' in g or 'social life and customs' in s or 'social conditions' in s or 'social problems' in s or 'social classes' in s or 'manners and customs' in s:
        cats['social'] += 1
        indices['social'].add(idx)

    war = False
    for category in s.union(g):
        if 'war ' in category or ' war' in category or ' wars' in category or 'revolution' in category:
            war = True
            allwars.add(category)

    if war:
        cats['war'] += 1
        indices['war'].add(idx)

    if len(s) < 1 and len(g) < 1 and not ('a novel' in row['title'].lower()) and not ('a romance' in row['title'].lower()):
        cats['unmarked'] += 1
        indices['unmarked'].add(idx)

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

    chosendf.to_csv('genremeta/' + tc + '.tsv', index = False, sep = '\t')


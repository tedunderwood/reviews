import pandas as pd
import ast, random
from collections import Counter

books = pd.read_csv('grouped_books.tsv', sep = '\t')

cats = Counter()

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

    for cat in g:
        cats[cat] += 1

    for cat in s:
        cats[cat] += 1

with open('common_book_genres.tsv', mode = 'w', encoding = 'utf-8') as f:
    for cat, ct in cats.most_common():
        f.write(cat + '\t' + str(ct) + '\n')


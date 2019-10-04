import pandas as pd
from collections import Counter
from difflib import SequenceMatcher

meta = pd.read_csv('unifiedmatches.tsv', sep = '\t')

def get_ratio(stringA, stringB):

    m = SequenceMatcher(None, stringA, stringB)

    thefilter = m.real_quick_ratio()

    if thefilter < 0.7:
        return thefilter

    else:
        return m.ratio()

bookids = dict()
bookctr = 0
matchedindexes = dict()

# meta = meta.iloc[0: 2000, : ]

def returninitial(author):
    return author[0]

meta = meta.assign(authorinitial = meta.author.map(returninitial))

metagroups = meta.groupby(['authorinitial'])

for initial, initgroup in metagroups:
    initgroup = initgroup.sort_index()

    for ir in initgroup.itertuples():

        idx1 = ir.Index
        title1 = ir.title
        author1 = ir.author

        print(idx1)

        # if pd.isnull(title1) or pd.isnull(author1):
            # continue

        for ir2 in initgroup.itertuples():

            idx2 = ir2.Index

            if idx2 in matchedindexes:
                continue

            if idx2 < idx1:
                continue

            title2 = ir2.title
            author2 = ir2.author

            # if pd.isnull(title2) or pd.isnull(author2):
                # continue

            if (title1[0] != title2[0]) and (author1[0] != author2[0]):
                continue

            titleratio = get_ratio(title1, title2)

            if titleratio < 0.8:
                continue

            authorratio = get_ratio(author1, author2)

            if authorratio < 0.8:
                continue

            if authorratio + titleratio < 1.88:
                continue
            else:
                if idx1 in matchedindexes:
                    bookid = matchedindexes[idx1]
                elif idx2 in matchedindexes:
                    bookid = matchedindexes[idx2]
                else:
                    bookid = 'B' + str(bookctr)
                    bookctr += 1
                    bookids[bookid] = set()

                matchedindexes[idx1] = bookid
                matchedindexes[idx2] = bookid
                bookids[bookid].add(idx1)
                bookids[bookid].add(idx2)

def map2bookids(idx):
    global matchedindexes
    if idx not in matchedindexes:
        return ''
    else:
        return matchedindexes[idx]

meta = meta.assign(bookid = meta.index.map(map2bookids))

meta = meta.sort_values(by = 'bookid')

meta.to_csv('grouped_matches.tsv', index = False, sep = '\t')


import pandas as pd
from collections import Counter

def count_genres(stringseq, genrectr):
    for field in stringseq:
        if not pd.isnull(field):
            genres = field.split('|')
            for g in genres:
                genrectr[g] += 1

acc = pd.read_csv('927accurateMatchingOutput.csv')

acc = acc.loc[ : , ['id', 'author', 'title', 'docid', 'genres', 'subjects']]
acc = acc.dropna(subset = ['author', 'title'])

colmap = {'id': 'bpoid', 'docid': 'htrcid'}

acc = acc.rename(columns = colmap)

fuzz = pd.read_csv('927fuzzyMatchingOutput.csv')

# we're going to drop rows that don't have an author or title
# these matches are unreliable

fuzz = fuzz.dropna(subset = ['bpoauthor', 'bpotitle', 'htrcauthor', 'htrctitle'])

titlemeta = pd.read_csv('../noveltmmeta/metadata/titlemeta.tsv', sep = '\t', index_col = 'docid')

def map2subjects(astring):
    global titlemeta
    if astring in titlemeta.index:
        return titlemeta.at(astring, 'subjects')
    else:
        return ''

subjects = fuzz.index.map(map2subjects)

fuzz = fuzz.assign(subjects = subjects)

fuzz = fuzz.loc[ : , ['htrcauthor', 'htrctitle', 'bpoId', 'htrcDocid', 'htrtGenre', 'subjects']]

colmap = {'htrctitle': 'title', 'htrcauthor': 'author', 'bpoId': 'bpoid', 'htrcDocid': 'htrcid', 'htrtGenre': 'genres'}

fuzz = fuzz.rename(columns = colmap)

unifiedmatches = pd.concat([acc, fuzz])

unifiedmatches = unifiedmatches.to_csv('unifiedmatches.tsv', index = False, sep = '\t')

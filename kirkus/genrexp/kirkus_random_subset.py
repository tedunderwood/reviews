# create random subset

import pandas as pd
import random

# We start by identifying the topics that have been flagged as
# identifying genres or genre-like groupings. This draws on work
# by Peizhen Wu and Ted Underwood.

topics = pd.read_csv('genre_80_mallet_categories_for_20c_exp.csv')
genretopics = topics.dropna(subset = ['possible_genres'])
genretopics = genretopics['Topic_Num'].tolist()
print(genretopics)

meta = pd.read_csv('metadata4kirkus.tsv', sep = '\t')

genrerows = meta.loc[meta['Dominant_Topic'].isin(genretopics), : ]
genredocs = list(set(genrerows['docid'].tolist()))

alldocs = meta['docid'].tolist()

randomdocs = set(alldocs) - set(genredocs)

print(len(randomdocs))

randomdocs = list(randomdocs)
randomdocs.extend(random.sample(genredocs, 1000 - len(randomdocs)))

meta.set_index('docid', inplace = True)

genredf = meta.loc[genredocs, : ]
genredf = genredf.loc[~genredf.index.duplicated(keep='first')]
randomdf = meta.loc[randomdocs, : ]

genredf.to_csv('genremetadata4kirkus.tsv', sep = '\t', index_label = 'docid')
randomdf.to_csv('randommetadata4kirkus.tsv', sep = '\t', index_label = 'docid')

import glob
import pandas as pd

alldec = 0
samples = []

for decade in range(1800, 1920, 10):

    df = pd.read_csv('matched_reviews_' + str(decade) + '.tsv', sep = '\t')
    thegood = sum(df.matchquality > 2.1)
    theall = len(df)

    print(decade, theall, thegood)
    alldec = alldec + thegood
    gooddf = df.loc[df.matchquality > 2.1, : ]
    thissample = gooddf.sample(90)
    samples.append(thissample)

print()
print(alldec)

samples = pd.concat(samples, axis = 0)

# New columns

# isfiction
# singlework
# actualtitle
# actualauthor
# howpositive (nan)
# genresnamed

reviews = pd.read_csv('allreviews.tsv', sep = '\t', low_memory = False)

takefromreview = ['RecordID', 'RecordTitle', 'PathID', 'Title', 'AlphaPubDate', 'PubYear']

columns = dict()
for t in takefromreview:
    columns[t] = []

for decade in range(1800, 1920, 10):
    df = reviews.loc[(reviews.PubYear >= decade) & (reviews.PubYear < decade + 10), :]
    sampledf = df.sample(10)
    for idx, row in sampledf.iterrows():
        for t in takefromreview:
            columns[t].append(row[t])

rawdf = pd.DataFrame.from_dict(columns)

samples = pd.concat([samples, rawdf], axis = 0)
samples = samples.sample(frac=1).reset_index(drop = True)

samples = samples.assign(isfiction = '')
samples = samples.assign(singlework = '')
samples = samples.assign(actualtitle = '')
samples = samples.assign(actualauthor = '')
samples = samples.assign(howpositive = '')
samples = samples.assign(genresnamed = '')
samples = samples.assign(comments = '')

samples.to_csv('bpometa/selectedrows.tsv', sep = '\t', index_label = 'seq')

for i in range(0, len(samples), 100):
    df = samples.iloc[i : i + 100, : ]
    df.to_csv('bpometa/reviews' + str(i) + 'to' + str(i + 100) + '.tsv',
        sep = '\t', index_label = 'seq')





import pandas as pd
import numpy as np

publishers = ['Appleton', 'Baker', 'Barnes', 'Benziger', 'Bobbs', "Brentano's", 'Cassell', 'Century', 'Collier-Fox', 'Crowell', 'Ditson', 'Dodd', 'Doran', 'Doubleday', 'Dutton', 'Elder', 'Estes', 'Ginn', 'Goodspeed', 'Harper', 'Heath', 'Holt', 'Houghton', 'Knopf', 'Lane', 'Lippincott', 'Little', 'Liveright', 'Longmans', 'Macmillan', 'McBride', 'McClure', 'McGraw', 'Moffat', 'Oxford', 'Page', 'Pott', 'Putnam', 'Scribner', 'Simmons', 'Stokes', 'Walton', 'Warne', 'Wessels', 'Wilde', 'Wiley', 'Winston', 'Yale']

pubdata = dict()

df = pd.read_csv('pairedvoloutfile.tsv', sep = '\t')

for idx, row in df.iterrows():
    found = False
    for p in publishers:
        if not pd.isnull(row['publisher']) and p in row['publisher']:
            if p not in pubdata:
                pubdata[p] = dict()
                pubdata[p]['sentiment'] = []
                pubdata[p]['wordcount'] = []
                pubdata[p]['price'] = []
                pubdata[p]['numreviews'] = []
            pubdata[p]['sentiment'].append(row['avgsent'])
            if row['price'] > 0:
                pubdata[p]['price'].append(row['price'])
            pubdata[p]['wordcount'].append(row['wordcount'])
            pubdata[p]['numreviews'].append(row['numreviews'])

with open('publishers.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('publisher\twordcount\tprice\tsentiment\tnumreviews\tnumbooks\n')
    for p, data in pubdata.items():
        sentiment = np.mean(np.array(data['sentiment']))
        wordcount = np.mean(np.array(data['wordcount']))
        price = np.mean(np.array(data['price']))
        numreviews = np.mean(data['numreviews'])
        numbooks = len(data['numreviews'])

        f.write(p + '\t' + str(wordcount) + '\t' + str(price) + '\t' + str(sentiment) + '\t' + str(numreviews) + '\t' + str(numbooks) + '\n')


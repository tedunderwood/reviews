# Experiment 1

import ast, string, csv
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

# Get stopwords

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

translator = dict()

punctuationstring = string.punctuation + '—‘’“”'

punctzapper = str.maketrans(punctuationstring, ' ' * len(punctuationstring))

with open('../../gethathimatches/CorrectionRules.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

with open('../../gethathimatches/VariantSpellings.txt', encoding = 'utf-8') as f:
    reader = csv.reader(f, delimiter = '\t')
    for row in reader:
        if len(row) < 2:
            continue
        translator[row[0]] = row[1]

print('Translators built.')

bpodict = dict()

with open('../../filtered/all_fic_reviews.txt', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        bpoid = int(fields[0])

        cleaned_text = fields[2].translate(punctzapper)

        acceptedwords = []

        words = word_tokenize(cleaned_text)
        for w in words:
            w = w.lower()

            if w in stop_words or len(w) < 2:
                continue
            elif w in translator:
                w = translator[w]

            acceptedwords.append(w)

        bpodict[bpoid] = acceptedwords

print('BPO dictionary built.')

lengths = []
for k, v in bpodict.items():
    lengths.append(len(v))
print("Mean bpodict len, ", np.mean(lengths))

def get_htrctext(stringset):
    global stop_words

    htrcids = ast.literal_eval(stringset)

    alltokens = []

    for h in htrcids:
        outpath = '/Volumes/TARDIS/work/ef/bpoexp/' + h + '.txt'
        with open(outpath) as f:
            thisdoc = f.read()

        tokens = word_tokenize(thisdoc)
        for t in tokens:
            if t not in stop_words:
                alltokens.append(t)

    the_text = ' '.join(alltokens)

    return the_text

def get_bpotext(stringset):

    global bpodict

    bpoids = ast.literal_eval(stringset)

    alltokens = []

    for b in bpoids:
        alltokens.extend(bpodict[b])

    the_text = ' '.join(alltokens)

    return the_text

# Load word-vector model

from pyemd import emd
from gensim.models import KeyedVectors
# from sklearn.metrics import euclidean_distances

wv = KeyedVectors.load_word2vec_format(
        "/Users/tunder/data/word2vec/GoogleNews-vectors-negative300.bin.gz",
        binary=True)

print('Word-vector model loaded.')

wv.init_sims(replace=True)

print('Word-vector model normalized.')

meta = pd.read_csv('../meta/grouped_books.tsv', sep = '\t')

outrows = []

htrc_distances = []
bpo_distances = []

for i in range(100):
    print(i)

    tworows = meta.sample(n = 2, replace = False)

    indices = tworows.index.tolist()

    voltexts = dict()
    for j in indices:
        voltexts[j] = dict()

        voltexts[j]['bpo'] = get_bpotext(tworows.loc[j, 'bpoids'])
        voltexts[j]['htrc'] = get_htrctext(tworows.loc[j, 'htrcids'])

    bpodist = wv.wmdistance(voltexts[indices[0]]['bpo'], voltexts[indices[1]]['bpo'])
    htrcdist = wv.wmdistance(voltexts[indices[0]]['htrc'], voltexts[indices[1]]['htrc'])

    # meandate = np.mean(tworows[''])

    outrow = str(bpodist) + '\t' + str(htrcdist) + '\n'

    outrows.append(outrow)

    htrc_distances.append(htrcdist)
    bpo_distances.append(bpodist)

print(pearsonr(htrc_distances, bpo_distances))

with open('initial_test.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('bpo_distance\thtrc_distance\n')
    for row in outrows:
        f.write(row)


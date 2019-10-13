# Experiment 2b

import pandas as pd
import ast, random
from collections import Counter

# create categories

books = pd.read_csv('../meta/datedbooks.tsv', sep = '\t', index_col = 'bookid')

books_in_cat = dict()

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

    gs = g.union(s)
    for cat in gs:
        if cat not in books_in_cat:
            books_in_cat[cat] = set()
        books_in_cat[cat].add(idx)

books_by_date = dict()

date_groups = books.groupby('pubdate')

for date, group in date_groups:
    books_by_date[date] = group.index.tolist()

genrecategories = []

with open('../meta/genre_categories_for_exp2.tsv', encoding = 'utf-8') as f:
    for line in f:
        if '(' in line:
            continue
        fields = line.split('\t')
        genrecategories.append([x.strip('"\n') for x in fields if len(x) > 2])

genrebooks = dict()

for genregroup in genrecategories:
    newbookset = set()
    for gen in genregroup:
        for book in books_in_cat[gen]:
            newbookset.add(book)

    genrebooks[genregroup[0]] = list(newbookset)
    print(genregroup[0], len(newbookset))
print()

import string, csv
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
        inpath = '/Volumes/TARDIS/work/ef/bpoexp/' + h + '.txt'
        try:
            with open(inpath) as f:
                thisdoc = f.read()
        except:
            print('File error:', h)
            thisdoc = ''

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

wv_exists = 'wv' in locals() or 'wv' in globals()

if not wv_exists:

    wv = KeyedVectors.load_word2vec_format(
            "/Users/tunder/data/word2vec/GoogleNews-vectors-negative300.bin.gz",
            binary=True)

    print('Word-vector model loaded.')

    wv.init_sims(replace=True)

    print('Word-vector model normalized.')

else:
    print('Using existing wv.')

def get_two_distances(id1, id2):
    global wv, books

    bpo1 = get_bpotext(books.at[id1, 'bpoids'])
    bpo2 = get_bpotext(books.at[id2, 'bpoids'])
    htrc1 = get_htrctext(books.at[id1, 'htrcids'])
    htrc2 = get_htrctext(books.at[id2, 'htrcids'])

    if len(bpo1) > 10 and len(bpo2) > 10:
        bpodist = wv.wmdistance(bpo1, bpo2)
    else:
        bpodist = -1000

    if len(htrc1) > 10 and len(htrc2) > 10:
        htrcdist = wv.wmdistance(htrc1, htrc2)
    else:
        htrcdist = -1000

    return bpodist, htrcdist, np.mean([len(bpo1), len(bpo2)]), np.mean([len(htrc1), len(htrc2)])

ctr = 0

with open('exp2bprime.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('category\tbook1\tbook2\tdate1\tdate2\trandombpo\tingroupbpo\tbpodiff\trandomhtrc\tingrouphtrc\thtrcdiff\tleninbpo\tleninhtrc\tlenrandbpo\tlenrandtrc\n')

bpo_distances = []
htrc_distances= []
categories_used = []
categories_to_use = []

for cat, booklist in genrebooks.items():

    pairstouse = []

    for idx, b1 in enumerate(booklist):
        for b2 in booklist[idx + 1 : ]:

            if books.at[b1, 'author'] == books.at[b2, 'author']:
                continue
            else:
                pairstouse.append((b1, b2))

    if len(pairstouse) > 100:
        pairstouse = random.sample(pairstouse, 100)

    print(cat, len(pairstouse))

    these_bpos = []
    these_htrcs = []

    for b1, b2 in pairstouse:

        date1 = books.at[b1, 'pubdate']
        date2 = books.at[b2, 'pubdate']

        in_bpo, in_htrc, len_in_bpo, len_in_htrc = get_two_distances(b1, b2)

        randidx1 = random.sample(books_by_date[date1], 1)[0]
        randidx2 = random.sample(books_by_date[date2], 1)[0]

        if books.at[randidx1, 'author'] == books.at[randidx2, 'author']:
            continue

        rand_bpo1, rand_htrc1, len_rand_bpo1, len_rand_htrc1 = get_two_distances(randidx1, b2)

        if in_bpo < -100 or in_htrc < -100 or rand_bpo1 < -100 or rand_htrc1 < -100:
            continue

        rand_bpo2, rand_htrc2, len_rand_bpo2, len_rand_htrc2 = get_two_distances(b1, randidx2)

        if rand_bpo2 < -100 or rand_htrc2 < -100:
            continue

        rand_bpo = np.mean([rand_bpo1, rand_bpo2])
        rand_htrc = np.mean([rand_htrc1, rand_htrc2])
        len_rand_bpo = np.mean([len_rand_bpo1, len_rand_bpo2])
        len_rand_htrc = np.mean([len_rand_htrc1, len_rand_htrc2])

        with open('exp2bprime.tsv', mode = 'a', encoding = 'utf-8') as f:
            f.write('\t'.join([str(x) for x in [cat, b1, b2, date1, date2, rand_bpo, in_bpo, rand_bpo-in_bpo, rand_htrc, in_htrc, rand_htrc-in_htrc, len_in_bpo, len_in_htrc, len_rand_bpo, len_rand_htrc]]) + '\n')

        these_htrcs.append(rand_htrc - in_htrc)
        these_bpos.append(rand_bpo - in_bpo)

    bpo_distances.append(np.mean(these_bpos))
    htrc_distances.append(np.mean(these_htrcs))
    print(np.median(these_bpos), np.median(these_htrcs))

print()
print(pearsonr(bpo_distances, htrc_distances))















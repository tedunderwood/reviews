# Experiment 2cprime

# cosine distances on subject categories

import pandas as pd
import ast, random, os
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

import string, csv
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from scipy.spatial.distance import cosine

# create categories

books = pd.read_csv('../meta/datedbooks.tsv', sep = '\t', index_col = 'bookid')

books_in_cat = dict()

if os.path.exists('reviewvectors.tsv'):
    havedocs = True
else:
    havedocs = False

punctuationstring = string.punctuation + '—‘’“”'
punctzapper = str.maketrans(punctuationstring, ' ' * len(punctuationstring))

translator = dict()

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

def get_htrctext(stringset):

    htrcids = ast.literal_eval(stringset)

    tokens = []

    for h in htrcids:
        inpath = '/Volumes/TARDIS/work/ef/bpoexp/' + h + '.txt'
        if os.path.exists(inpath):
            with open(inpath) as f:
                thisdoc = f.read()
        else:
            print('File error:', h, htrcids)
            thisdoc = ''

        thisdoc = thisdoc.translate(punctzapper)
        words = word_tokenize(thisdoc)

        for w in words:
            if len(w) < 2:
                continue
            w = w.lower()

            if w in translator:
                w = translator[w]
                if w in translator:
                    w = translator[w]

            tokens.append(w)

    return tokens

bpodict = dict()
bpodocfreqs = Counter()

with open('../../filtered/all_fic_reviews.txt', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        bpoid = int(fields[0])

        cleaned_text = fields[2].translate(punctzapper)

        acceptedwords = []

        words = word_tokenize(cleaned_text)
        for w in words:
            if len(w) < 2:
                continue
            w = w.lower()

            if w in translator:
                w = translator[w]
                if w in translator:
                    w = translator[w]

            acceptedwords.append(w)

        bpodict[bpoid] = acceptedwords
        for w in set(acceptedwords):
            bpodocfreqs[w] += 1

print('BPO dictionary built.')

def get_bpotext(stringset):

    global bpodict

    bpoids = ast.literal_eval(stringset)

    alltokens = []

    for b in bpoids:
        alltokens.extend(bpodict[b])

    the_text = ' '.join(alltokens)

    return the_text

booktexts = []
reviewtexts = []
docfreqs = Counter()
bookids = []

ctr = 0

for idx, row in books.iterrows():
    ctr += 1
    if ctr % 10 == 1:
        print(ctr)

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

    if not havedocs:
        tokens = get_htrctext(row['htrcids'])
        for t in set(tokens):
            docfreqs[t] += 1
        booktext = ' '.join(tokens)
        reviewtext = get_bpotext(row['bpoids'])

        if len(booktext) > 10 and len(reviewtext) > 5:
            booktexts.append(booktext)
            reviewtexts.append(reviewtext)
            bookids.append(idx)

lexicon = docfreqs.most_common(2500)

with open('docfreqs.tsv', mode = 'w', encoding = 'utf-8') as f:
    for word, freq in lexicon:
        f.write(str(word) + '\t' + str(freq) + '\n')

vocab = [x[0] for x in lexicon]
idf = 1 / np.array([x[1] for x in lexicon])

sparse_matrix = CountVectorizer(strip_accents = 'ascii', vocabulary = vocab).fit_transform(booktexts)

# we don't really have to name the columns, but we do need to transform
# the sparse matrix to a normal one
termdoc = pd.DataFrame(sparse_matrix.toarray())

# normalize termdoc
rowsums = termdoc.sum(axis=1)
termdoc = termdoc.div(rowsums, axis = 0)

del(sparse_matrix)
del(booktexts)

book_vectors = dict()

for idx, bookid in enumerate(bookids):
    book_vectors[bookid] = termdoc.iloc[idx, : ] * idf

print('Have bookvectors.')

bpolexicon = bpodocfreqs.most_common(2500)

with open('bpodocfreqs.tsv', mode = 'w', encoding = 'utf-8') as f:
    for word, freq in lexicon:
        f.write(str(word) + '\t' + str(freq) + '\n')

bpovocab = [x[0] for x in bpolexicon]
bpoidf = 1 / np.array([x[1] for x in bpolexicon])

sparse_matrix = CountVectorizer(strip_accents = 'ascii', vocabulary = bpovocab).fit_transform(reviewtexts)

# we don't really have to name the columns, but we do need to transform
# the sparse matrix to a normal one
termdoc = pd.DataFrame(sparse_matrix.toarray())

# normalize termdoc
rowsums = termdoc.sum(axis=1)
termdoc = termdoc.div(rowsums, axis = 0)

del(sparse_matrix)

review_vectors = dict()

assert len(bookids) == len(reviewtexts)
del(reviewtexts)

for idx, bookid in enumerate(bookids):
    review_vectors[bookid] = termdoc.iloc[idx, : ] * bpoidf

print("Have reviewvectors.")

def write_vectors(vectordict, path, vocab):
    with open(path, mode = 'w', encoding = 'utf-8') as f:
        header = 'bookid\t' + '\t'.join(vocab) + '\n'
        f.write(header)
        for k, v in vectordict.items():
            f.write(k + '\t' + '\t'.join([str(x) for x in v]) + '\n')

write_vectors(book_vectors, 'bookvectors.tsv', vocab)
write_vectors(review_vectors, 'reviewvectors.tsv', bpovocab)

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

def get_two_distances(id1, id2):
    global review_vectors, book_vectors

    bpodist = cosine(review_vectors[id1], review_vectors[id2])
    htrcdist = cosine(book_vectors[id1], book_vectors[id2])

    return bpodist, htrcdist

ctr = 0

with open('exp2cprime.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('category\tbook1\tbook2\tdate1\tdate2\trandombpo\tingroupbpo\tbpodiff\trandomhtrc\tingrouphtrc\thtrcdiff\n')

def get_date_match(date):
    global books_by_date, book_vectors

    randidx = random.sample(books_by_date[date1], 1)[0]

    if randidx not in book_vectors:
        randidx = random.sample(books_by_date[date + 1], 1)[0]
        if randidx not in book_vectors:
            randidx = random.sample(books_by_date[date - 1], 1)[0]

    return randidx

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
            elif b1 not in book_vectors or b2 not in book_vectors:
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

        in_bpo, in_htrc = get_two_distances(b1, b2)

        randidx1 = get_date_match(date1)
        randidx2 = get_date_match(date2)

        rand_bpo1, rand_htrc1 = get_two_distances(randidx1, b2)

        if in_bpo < -100 or in_htrc < -100 or rand_bpo1 < -100 or rand_htrc1 < -100:
            continue

        rand_bpo2, rand_htrc2 = get_two_distances(b1, randidx2)

        if rand_bpo2 < -100 or rand_htrc2 < -100:
            continue

        rand_bpo = np.mean([rand_bpo1, rand_bpo2])
        rand_htrc = np.mean([rand_htrc1, rand_htrc2])

        with open('exp2cprime.tsv', mode = 'a', encoding = 'utf-8') as f:
            f.write('\t'.join([str(x) for x in [cat, b1, b2, date1, date2, rand_bpo, in_bpo, rand_bpo - in_bpo, rand_htrc, in_htrc, rand_htrc - in_htrc]]) + '\n')

        these_htrcs.append(rand_htrc - in_htrc)
        these_bpos.append(rand_bpo - in_bpo)

    bpo_distances.append(np.mean(these_bpos))
    htrc_distances.append(np.mean(these_htrcs))
    print(np.mean(these_bpos), np.mean(these_htrcs))

print()
print(pearsonr(bpo_distances, htrc_distances))















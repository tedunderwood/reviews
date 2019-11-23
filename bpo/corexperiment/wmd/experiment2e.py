# Experiment 2e

# A version of experiment 2c (using cosine distance)
# that tests distance on disjoint groups of books.
# That is, different sets of books are used to test
# distance for the reviews and for the books themselves.
#
# This is arguably not necessary, since we aren't
# necessarily claiming that the genre categories assigned
# by librarians define *stable* objects; we could take them in this
# experiment merely as arbitrary samples, and still use those samples
# to confirm that variation in book-similarity tends to correlate
# with variation in review-similarity.

# But it may become more interesting if we also know that this variation
# is not random, but explained by the genre categorization.

# This script is based on experiment2cprime1.

import pandas as pd
import ast, random, os
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler

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

ctr = 0

for idx, row in books.iterrows():
    ctr += 1
    if not havedocs and ctr % 10 == 1:
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

def get_vectors(apath):
    adict = dict()
    with open(apath, encoding = 'utf-8') as f:
        reader = csv.reader(f, delimiter = '\t')
        for row in reader:
            if row[0] != 'bookid' and not pd.isnull(row[1]):
                adict[row[0]] = np.array([float(x) for x in row[1:]])
                if pd.isnull(adict[row[0]][0]):
                    adict.pop(row[0])
            elif row[0] == 'bookid':
                colnames = row

    return adict, colnames

def transformadict(adict):
    df = pd.DataFrame.from_dict(adict, orient='index')
    matrix = StandardScaler().fit_transform(df)
    indices = df.index.tolist()
    for i in range(matrix.shape[0]):
        adict[indices[i]] = matrix[i, : ]
    return adict

book_vectors, bookcolnames = get_vectors('bookvectors.tsv')
review_vectors, reviewcolnames = get_vectors('reviewvectors.tsv')

book_vectors = transformadict(book_vectors)
review_vectors = transformadict(review_vectors)

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

# Now let's split the books into two disjoint sets,
# one for which we will make book text comparisons
# and one for which we will make review text comparisons.

booktextsbygenre = dict()
reviewtextsbygenre = dict()

def partition(lst, n):
    '''Credit where due:
    this is from https://stackoverflow.com/questions/3352737/how-to-randomly-partition-a-list-into-n-nearly-equal-parts
    '''

    division = len(lst) / float(n)
    return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n)]

for key, value in genrebooks.items():
    thesebooks = list(value)
    random.shuffle(thesebooks)
    partitions = partition(thesebooks, 2)
    booktextsbygenre[key] = partitions[0]
    reviewtextsbygenre[key] = partitions[1]


def get_two_distances(id1, id2, masked_word, reviewcolnames, bookcolnames):
    global review_vectors, book_vectors

    rev1 = np.array(review_vectors[id1])
    rev2 = np.array(review_vectors[id2])

    if masked_word in reviewcolnames:
        idx = reviewcolnames.index(masked_word)
        rev1[idx] = 0
        rev2[idx] = 0

    book1 = book_vectors[id1]
    book2 = book_vectors[id2]

    if masked_word in bookcolnames:
        idx = bookcolnames.index(masked_word)
        book1[idx] = 0
        book2[idx] = 0

    bpodist = cosine(rev1, rev2)
    htrcdist = cosine(book1, book2)

    return bpodist, htrcdist

ctr = 0

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

# First book distances.

bookresults = dict()

for cat, booklist in booktextsbygenre.items():

    bookresults[cat] = []

    if cat == 'stories':
            masked_word = 'stories'
    elif cat == 'romance':
        masked_word = 'novel'
    elif cat == 'novel':
        masked_word = 'novel'
    else:
        masked_word = 'antidisestablishmentarianism'

    # in certain cases, where a category was selected by recognizing
    # words in the title, it would give the category an unfair
    # advantage to allow that word in as a feature; it's almost
    # guaranteed to be present, e.g. in the review

    pairstouse = []

    for idx, b1 in enumerate(booklist):
        for b2 in booklist[idx + 1 : ]:

            if books.at[b1, 'author'] == books.at[b2, 'author']:
                continue
            elif b1 not in book_vectors or b2 not in book_vectors:
                continue
            else:
                pairstouse.append((b1, b2))

    if len(pairstouse) > 200:
        pairstouse = random.sample(pairstouse, 200)

    print(cat, len(pairstouse))

    these_bpos = []
    these_htrcs = []

    for b1, b2 in pairstouse:

        date1 = books.at[b1, 'pubdate']
        date2 = books.at[b2, 'pubdate']

        in_bpo, in_htrc = get_two_distances(b1, b2, masked_word, reviewcolnames, bookcolnames)

        randidx1 = get_date_match(date1)
        randidx2 = get_date_match(date2)

        rand_bpo1, rand_htrc1 = get_two_distances(randidx1, b2, masked_word, reviewcolnames, bookcolnames)

        if in_bpo < -100 or in_htrc < -100 or rand_bpo1 < -100 or rand_htrc1 < -100:
            continue

        rand_bpo2, rand_htrc2 = get_two_distances(b1, randidx2, masked_word, reviewcolnames, bookcolnames)

        if rand_bpo2 < -100 or rand_htrc2 < -100:
            continue

        rand_bpo = np.mean([rand_bpo1, rand_bpo2])
        rand_htrc = np.mean([rand_htrc1, rand_htrc2])

        rowdict = dict()
        rowdict['comparisontype'] = 'booktext'
        bpodiff = rand_bpo - in_bpo
        htrcdiff = rand_htrc - in_htrc
        for varname in ['cat', 'b1', 'b2', 'date1', 'date2', 'rand_bpo', 'in_bpo',
            'bpodiff', 'rand_htrc', 'in_htrc', 'htrcdiff']:
            rowdict[varname] = locals()[varname]

        bookresults[cat].append(rowdict)
        these_htrcs.append(htrcdiff)
        these_bpos.append(bpodiff)

    print(np.mean(these_bpos), np.mean(these_htrcs))

reviewresults = dict()

for cat, booklist in reviewtextsbygenre.items():

    reviewresults[cat] = []

    if cat == 'stories':
            masked_word = 'stories'
    elif cat == 'romance':
        masked_word = 'novel'
    elif cat == 'novel':
        masked_word = 'novel'
    else:
        masked_word = 'antidisestablishmentarianism'

    # in certain cases, where a category was selected by recognizing
    # words in the title, it would give the category an unfair
    # advantage to allow that word in as a feature; it's almost
    # guaranteed to be present, e.g. in the review

    pairstouse = []

    for idx, b1 in enumerate(booklist):
        for b2 in booklist[idx + 1 : ]:

            if books.at[b1, 'author'] == books.at[b2, 'author']:
                continue
            elif b1 not in book_vectors or b2 not in book_vectors:
                continue
            else:
                pairstouse.append((b1, b2))

    if len(pairstouse) > 200:
        pairstouse = random.sample(pairstouse, 200)

    print(cat, len(pairstouse))

    these_bpos = []
    these_htrcs = []

    for b1, b2 in pairstouse:

        date1 = books.at[b1, 'pubdate']
        date2 = books.at[b2, 'pubdate']

        in_bpo, in_htrc = get_two_distances(b1, b2, masked_word, reviewcolnames, bookcolnames)

        randidx1 = get_date_match(date1)
        randidx2 = get_date_match(date2)

        rand_bpo1, rand_htrc1 = get_two_distances(randidx1, b2, masked_word, reviewcolnames, bookcolnames)

        if in_bpo < -100 or in_htrc < -100 or rand_bpo1 < -100 or rand_htrc1 < -100:
            continue

        rand_bpo2, rand_htrc2 = get_two_distances(b1, randidx2, masked_word, reviewcolnames, bookcolnames)

        if rand_bpo2 < -100 or rand_htrc2 < -100:
            continue

        rand_bpo = np.mean([rand_bpo1, rand_bpo2])
        rand_htrc = np.mean([rand_htrc1, rand_htrc2])

        rowdict = dict()
        rowdict['comparisontype'] = 'reviewtext'
        bpodiff = rand_bpo - in_bpo
        htrcdiff = rand_htrc - in_htrc
        for varname in ['cat', 'b1', 'b2', 'date1', 'date2', 'rand_bpo', 'in_bpo',
            'bpodiff', 'rand_htrc', 'in_htrc', 'htrcdiff']:
            rowdict[varname] = locals()[varname]

        reviewresults[cat].append(rowdict)
        these_htrcs.append(htrcdiff)
        these_bpos.append(bpodiff)

    print(np.mean(these_bpos), np.mean(these_htrcs))

print()
print('Writing to file.')

with open('../results/splitcomparisons.tsv', mode = 'w', encoding = 'utf-8') as f:
    fields = ['comparisontype', 'cat', 'b1', 'b2', 'date1', 'date2', 'rand_bpo', 'in_bpo',
            'bpodiff', 'rand_htrc', 'in_htrc', 'htrcdiff']
    scribe = csv.DictWriter(f, fieldnames = fields, delimiter = '\t')
    scribe.writeheader()
    for key, value in bookresults.items():
        for row in value:
            scribe.writerow(row)
    for key, value in reviewresults.items():
        for row in value:
            scribe.writerow(row)



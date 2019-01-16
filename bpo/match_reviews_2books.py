# match reviews to books

# This is code for a fuzzy-matching problem of a particularly
# messy kind. Book review titles may mention the author as
# well as the title, but they may also omit words, mention
# the price, etc.

# Instead of doing fuzzy matching on the string as a whole,
# we are well advised to break it into pieces.

import os, csv
import pandas as pd
from collections import Counter
from difflib import SequenceMatcher

commonwords = {'the', 'an', 'of', 'to', 'be', 'in', 'and', 'book', 'review', 'that',
'or', 'for', 'how', 'why', 'it', 'not', 'on', 'with','as', 'you', 'do'}
takefromreview = ['RecordID', 'RecordTitle', 'PathID', 'Title', 'AlphaPubDate', 'PubYear']

fields = ['RecordID', 'RecordTitle', 'PathID', 'Title', 'AlphaPubDate', 'PubYear',
'bookauthor', 'booktitle', 'bookdate', 'matchquality']

def stripword(word):
    word = word.replace("&apos;", "'")
    return word.strip('()[]{}.,/')

def reduce2tokens(astring):
    if len(astring) < 1:
        return set()

    astring = astring.lower()
    words = astring.split()
    if len(words) > 8:
        words = words [0:8]

    cleanwords = set()

    for w in words:
        cleanwords.add(stripword(w))

    return cleanwords

def addifexists(index, word, number):
    if word not in index:
        index[word] = set()
    index[word].add(number)

books = pd.read_csv('../../noveltmmeta/metadata/titlemeta.tsv', sep = '\t', low_memory = False)

reviews = pd.read_csv('allreviews.tsv', sep = '\t', low_memory = False)

for decade in range(1800, 1940, 10):

    print(decade)

    index = dict()
    wordsperdoc = Counter()

    bookset = books.loc[(books.inferreddate > decade - 20) & (books.inferreddate < decade + 30), : ]

    for i, row in bookset.iterrows():
        idx = row.name
        if pd.isnull(row['shorttitle']):
            continue

        title = row['shorttitle']
        words = reduce2tokens(title)
        for w in words:
            if len(w) > 1 and w not in commonwords:
                addifexists(index, w, idx)
                wordsperdoc[idx] += 1

        if not pd.isnull(row['author']):
            lastname = row['author'].split()[0]
            lastname = stripword(lastname.lower())

            if len(lastname) > 1 and lastname not in commonwords:
                addifexists(index, lastname, idx)
                wordsperdoc[idx] += 1

    reviewset = reviews.loc[(reviews.PubYear >= decade) & (reviews.PubYear < decade + 10), : ]

    found = []

    for idx, row in reviewset.iterrows():
        title = row['RecordTitle']
        reviewyear = int(row['PubYear'])

        matchtitle = stripword(title.lower())

        if len(matchtitle) > 25:
            matchtitle = matchtitle[0: 25]

        words = reduce2tokens(title)

        count = Counter()
        idf = Counter()

        for w in words:
            if w in index:
                for doc in index[w]:
                    count[doc] += 1
                    basis = len(index[w]) + 2
                    if len(w) < 6:
                        basis = basis + 1
                    idf[doc] += 1 / basis

        matches = []

        for doc, ct in count.items():
            ratiofound = ct / (wordsperdoc[doc] + 2)
            matchquality = ratiofound + idf[doc] + (ct * 0.05)

            if matchquality < 0.25:
                continue

            booktitle = stripword(bookset.loc[doc, 'shorttitle'].lower())

            if len(booktitle) > 25:
                booktitle = booktitle[0: 25]

            booktitle = booktitle.replace('a novel', '')
            matchtitle = matchtitle.replace('a novel', '')
            m = SequenceMatcher(None, booktitle, matchtitle)
            fuzzymatch = m.ratio()
            if fuzzymatch > 0.66:
                minlen = min(len(booktitle), len(matchtitle))
                lenratio = minlen / 25
                augment = (fuzzymatch ** 2) + (fuzzymatch * lenratio)
                matchquality = matchquality + augment
                if booktitle == matchtitle:
                    matchquality += 0.11

            bookyear = int(bookset.loc[doc, 'inferreddate'])

            gap = bookyear - reviewyear
            if gap < 3 and gap > -3:
                matchquality += 0.1
            elif gap > 10 or gap < -10:
                matchquality -= 0.1
                if gap > 15 or gap < -15:
                    matchquality -= 0.15

            matches.append((matchquality, doc))

        matches.sort(reverse = True)

        if len(matches) > 0 and matches[0][0] > 0.7:

            matchquality, thematch = matches[0]
            matchrow = dict()

            for field in takefromreview:
                matchrow[field] = row[field]

            bookrow = bookset.loc[thematch, : ]
            matchrow['bookauthor'] = bookrow['author']
            matchrow['booktitle'] = bookrow['shorttitle']
            matchrow['bookdate'] = bookrow['inferreddate']
            matchrow['matchquality'] = matchquality

            found.append((matchquality, matchrow))

    found.sort(reverse = True, key = lambda x: x[0])


    with open('matched_reviews_' + str(decade) + '.tsv', mode = 'w', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, delimiter = '\t', fieldnames = fields)
        writer.writeheader()
        for quality, row in found:
            writer.writerow(row)













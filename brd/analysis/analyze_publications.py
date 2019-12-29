# -*- coding: utf-8 -*-
# select_fiction_reviews.py
# Ted Underwood, Dec 2019

# This script does a complicated join on two sets of files:

# a) the original reviews scraped from BRD, which are structured
# with one line for each ~review~
# and
# b) the files produced by pair_index_with_reviews.py, which
# have one line for each ~book~, but only fiction books,
# and also some summary data at the book level, like mean sentiment

# we want to get all the lines from (a) that match auth-title pairs
# in (b), and add summary data from (b). We don't add the
# headings, unfortunately, because we're not allowed to export them.

import pandas as pd
import numpy as np
import csv, re
from difflib import SequenceMatcher

wordcountregex = re.compile('\d*0w[.]?')

def get_ratio(stringA, stringB):

    m = SequenceMatcher(None, stringA, stringB)

    thefilter = m.real_quick_ratio()
    if thefilter < 0.5:
        return thefilter

    else:
        return m.ratio()

def makeint(wordcount):
    wordcount = wordcount[ : -1]
    try:
        intwords = int(wordcount)
    except:
        intwords = 50
    return intwords

# triplets2process = []

# with open('pairing_meta.tsv', encoding = 'utf-8') as f:
#     reader = csv.DictReader(f, delimiter = '\t')
#     for row in reader:
#         triplets2process.append(row)

triplets2process = [{'indexpath': '/Users/tunder/Dropbox/python/reviews/brd/data/volume14 extract.txt',
    'reviewpath': '/Users/tunder/Dropbox/python/reviews/output/brd_quotes.tsv',
    'outfilename': 'pairedvoloutfile.tsv'}]

for triplet in triplets2process:
    # reviewsfile = triplet['reviewsname']
    # reviewspath = '/media/secure_volume/brd/output/' + reviewsfile

    # bookfile = triplet['outfilename']  # it was the 'outfile' for the other script!
    # bookpath = '/media/secure_volume/brd/paired/' + bookfile + '.tsv'

    # if bookfile.endswith('1914') or bookfile.endswith('1915'):
    #     continue
    #     # those don't actually exist!
    # else:
    #     print(bookfile)

    reviewspath = triplet['reviewpath']
    bookpath = triplet['outfilename']

    reviews = pd.read_csv(reviewspath, sep = '\t')

    books = pd.read_csv(bookpath, sep = '\t', engine='python', quoting=csv.QUOTE_NONE, index_col = 'index')

    list_of_dfs = []

    for idx, row in books.iterrows():

        auth = row['author']
        title = row['title']

        thisdf = reviews.loc[(reviews['booktitle'] == title) & (reviews['bookauthor'] == auth), : ]

        thisdf = thisdf.assign(wordcount = row['wordcount'])
        thisdf = thisdf.assign(avgsentiment = row['avgsent'])
        thisdf = thisdf.assign(bookindex = idx)
        thisdf = thisdf.assign(numreviewswithsent = row['numreviewswithsent'])
        thisdf = thisdf.assign(numreviewsofbk = row['numallreviews'])
        thisdf = thisdf.assign(authtitlefromindex = row['target'])
        thisdf = thisdf.assign(matchcloseness = row['closeness'])
        list_of_dfs.append(thisdf)

    selected = pd.concat(list_of_dfs)

    outname = 'localfiction.tsv'

    selected.to_csv(outname, sep = '\t', index = False)

    pubframe = pd.read_csv('brd_pubs_indexed.tsv', sep = '\t')

    pubs = [x.strip('.') for x in pubframe['code']]
    pubs.extend(['summary', 'Boston Transcript', 'A L A Bkl', 'The Times [London] Lit Sup', 'New Repub', 'Cleveland', 'Wis Lib Bul', 'Pittsburgh', 'Survey'])

    wordcounts = dict()
    sentiments = dict()

    bookrange = list(books.index)
    bookmatrix = dict()

    for p in pubs:
        wordcounts[p] = []
        sentiments[p] = []
        bookmatrix[p] = np.zeros(len(bookrange))

    bookmatrix['sentiment'] = np.zeros(len(bookrange))
    bookmatrix['price'] = np.zeros(len(bookrange))

    sentcats = dict()
    for i in range(1, 5):
        sentcats[i] = []

    missingpubs = []

    for idx, row in selected.iterrows():
        thispub = row['publication']
        if pd.isnull(thispub):
            continue
        themax = 0
        winner = 'other'
        for p in pubs:
            ratio = get_ratio(p, thispub)
            if ratio > themax and ratio > 0.5:
                themax = ratio
                winner = p

        if winner == 'other':
            missingpubs.append(thispub)
            winner = 'summary'

        if not pd.isnull(row.citation):
            citationparts = row.citation.split()
            if len(citationparts) > 0 and wordcountregex.fullmatch(citationparts[-1]):
                thesewords = makeint(citationparts[-1])
                if thesewords < 3000:
                    wcount = thesewords
                else:
                    wcount = 3000
                    # we impose a cap on super-long reviews because I'm skeptical
            else:
                wcount = float('nan')

        if not pd.isnull(wcount):
            idx = row['bookindex']
            matrix_index = bookrange.index(idx)
            bookmatrix[winner][matrix_index] = wcount
            bookmatrix['sentiment'][matrix_index] = row['avgsentiment']
            bookmatrix['price'][matrix_index] = row['price']
            if bookmatrix['price'][matrix_index] > 5:
                bookmatrix['price'][matrix_index] = 5

        if pd.isnull(row.sentiment):
            thissent = float('NaN')
        elif row.sentiment == '+' or row.sentiment == '+ +' or row.sentiment == '+ + +':
            thissent = 4
        elif row.sentiment == '+ -':
            thissent = 3
        elif row.sentiment == '- +':
            thissent = 2
        elif row.sentiment == '-' or row.sentiment == '- -':
            thissent = 1

        wordcounts[winner].append(wcount)
        sentiments[winner].append(thissent)

        if not pd.isnull(thissent) and not pd.isnull(wcount):
            sentcats[thissent].append(wcount)

    with open('publicationstats.tsv', mode = 'w', encoding = 'utf-8') as f:
        f.write('pubname\twcount\tavgsent\tnumrevs\n')

    for p in pubs:
        if len(sentiments[p]) < 2 or p == 'summary':
            continue
        print(p)
        wcount = round(np.nanmean(wordcounts[p]), 1)
        print(wcount)
        avgsent = round(np.nanmean(sentiments[p]), 3)
        print(avgsent)
        numrevs = len(sentiments[p])
        print(numrevs)
        print()
        with open('publicationstats.tsv', mode = 'a', encoding = 'utf-8') as f:
            f.write(p + '\t' + str(wcount) + '\t' + str(avgsent) + '\t' + str(numrevs) + '\n')

    with open('sentcats.tsv', mode = 'w', encoding = 'utf-8') as f:
        f.write('sent\twcount\n')
        for i in range(1, 5):
            for w in sentcats[i]:
                f.write(str(i) + '\t' + str(w) + '\n')

    bigpubs = ['sentiment', 'price']

    for p in pubs:
        if sum(bookmatrix[p]) > 4000:
            bigpubs.append(p)

    with open('bookmatrix.tsv', mode = 'w', encoding = 'utf-8') as f:
        f.write('\t'.join([x.replace(' ', '').replace('.', '') for x in bigpubs]) + '\n')
        for i in range(len(bookrange)):
            outlist = [str(bookmatrix[x][i]) for x in bigpubs]
            outrow = '\t'.join(outlist) + '\n'
            f.write(outrow)












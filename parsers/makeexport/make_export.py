# -*- coding: utf-8 -*-
# make_export.py
# Ted Underwood, Jan 2021

# This script does a complicated join on two sets of files:

# a) the original reviews scraped from BRD, which are structured
# with one line for each ~review~
# and
# b) the files produced by pair_index_with_reviews.py, which
# have one line for each ~book~,
# and also some summary data at the book level, like mean sentiment

# we want to get all the lines from (a) that match auth-title pairs
# in (b), and add summary data from (b). We don't add the
# headings, unfortunately, because we're not allowed to export them.

import pandas as pd
import csv, sys

metafile = sys.argv[1]

triplets2process = []

with open(metafile, encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        triplets2process.append(row)

# triplets2process = [{'indexpath': '/Users/tunder/Dropbox/python/reviews/brd/data/volume14 extract.txt',
#     'reviewpath': '/Users/tunder/Dropbox/python/reviews/output/brd_quotes.tsv',
#     'outfilename': 'pairedvoloutfile.tsv'}]

for triplet in triplets2process:
    reviewsfile = triplet['reviewsname']
    reviewspath = '/media/secure_volume/brd/output/' + reviewsfile

    bookfile = triplet['outfilename']  # it was the 'outfile' for the other script!
    bookpath = '/media/secure_volume/brd/paired/' + bookfile + '.tsv'

    if bookfile.endswith('1914') or bookfile.endswith('1915'):
        continue
        # those don't actually exist!
    else:
        print(bookfile)

    # reviewspath = triplet['reviewpath']
    # bookpath = triplet['outfilename']

    reviews = pd.read_csv(reviewspath, sep = '\t')

    books = pd.read_csv(bookpath, sep = '\t', engine='python', quoting=csv.QUOTE_NONE, index_col = 'index')

    list_of_dfs = []

    for idx, row in books.iterrows():

        auth = row['author']
        title = row['title']

        thisdf = reviews.loc[(reviews['booktitle'] == title) & (reviews['bookauthor'] == auth), : ]

        # thisdf = thisdf.assign(wordcount = row['wordcount'])
        thisdf = thisdf.assign(avgsentiment = row['avgsent'])
        thisdf = thisdf.assign(avgsentwmissing = row['avgsentwmissing'])
        thisdf = thisdf.assign(bookindex = idx)
        thisdf = thisdf.assign(numreviewswithsent = row['numreviewswithsent'])
        thisdf = thisdf.assign(numreviewsofbk = row['numallreviews'])
        thisdf = thisdf.assign(authtitlefromindex = row['target'])
        thisdf = thisdf.assign(matchcloseness = row['closeness'])

        for idx2, row2 in thisdf.iterrows():
            thisreview = row2['quote']
            allowedwords = []
            if not pd.isnull(thisreview):
                words = thisreview.split()
            else:
                words = []

            for w in words:
                if w == '<endsubj>':
                    allowedwords = []
                    # we don't take any words that might be part of a subject
                    # heading; this is achieved by clearing the counter whenever
                    # we get to the end of a line marked as part of a subject heading;
                    # these will always be the first words in the review
                else:
                    allowedwords.append(w.strip('. ,"'))

            allowedwords = sorted(allowedwords, key =str.casefold)  # goodbye sequential order

            wordbag = ' '.join(allowedwords)

            thisdf.at[idx2, 'quote'] = wordbag

        thisdf.drop(['sentiment'], axis = 1, inplace = True)

        list_of_dfs.append(thisdf)

    selected = pd.concat(list_of_dfs)

    outname = bookpath.replace('pairedvol', 'nonconsumptive')

    selected.to_csv(outname, sep = '\t', index = False)










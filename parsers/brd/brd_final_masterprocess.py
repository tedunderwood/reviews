# brd_final_masterprocess.py

import os, sys, csv

quotefieldnames = ['bookauthor', 'booktitle', 'brdpage', 'price', 'publisher', 'publication',
                'sentiment', 'citation', 'quote']

import brd_bookmaker as bookmaker
import brd_quotationmaker as quotationmaker
import brd_extract_pagelist as extractor
import hyphenjoiner


# I may eventually set up this loop to do multiple volumes
# in one run. At present, we're just doing a single volume.
# I'm also making a point of clearly labeling the parts
# so this will be intelligible for readers.

year = '1918'
suffix = '30112013681652'
startpage = 9

year_suffix_startpage = [(year, suffix, startpage)]

outfile = '/media/secure_volume/brd/output/' + year + '_' + suffix + '.tsv'

for year, vol, startpage in year_suffix_startpage:
    pagelist = extractor.extract(vol, startpage)
    books, author_errors = bookmaker.get_books(pagelist)
    quotations = quotationmaker.divide_into_quotations(books)

    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, delimiter = '\t', fieldnames = quotefieldnames)
        writer.writeheader()

        for quote in quotations:

            c = dict()
            book = quote.book

            c['bookauthor'] = book.author
            c['booktitle'] = book.title
            c['brdpage'] = book.pagenum
            c['price'] = book.price
            c['publisher'] = book.publisher
            c['publication'] = quote.publication
            c['sentiment'] = quote.sentiment
            c['citation'] = quote.citation
            c['quote'] = hyphenjoiner.join_hyphens(quote.thequote)

            writer.writerow(c)

        print(author_errors)

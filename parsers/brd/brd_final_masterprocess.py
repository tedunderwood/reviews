# brd_final_masterprocess.py

import os, sys, csv

outfile = '/media/secure_volume/brd/output/' + sys.argv[1]
quotefieldnames = ['bookauthor', 'booktitle', 'brdpage', 'price', 'publisher', 'publication',
                'sentiment', 'citation', 'quote']

if not os.path.isfile(outfile):
    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        f.write('\t'.join(quotefieldnames) + '\n')

import brd_bookmaker as bookmaker
import brd_quotationmaker as quotationmaker
import brd_extract_pagelist as extractor

vols2parse = [('39015078260935', 9)]

for vol, startpage in vols2parse:
    pagelist = extractor.extract(vol, startpage)
    books, author_errors = bookmaker.get_books(pagelist)
    quotations = quotationmaker.divide_into_quotations(books)

    with open(outquotes, mode = 'w', encoding = 'utf-8') as f:
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
            c['quote'] = quote.thequote

            writer.writerow(c)

        print(author_errors)

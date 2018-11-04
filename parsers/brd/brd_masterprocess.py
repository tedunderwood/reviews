# brd_masterprocess.py

import os, sys, csv

outfile = '/media/secure_volume/brd/output/' + sys.argv[1]
fieldnames = ['bookauthor', 'booktitle', 'brdpage', 'price', 'publication', 
                'sentiment', 'citation', 'quote']

if not os.path.isfile(outfile):
    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        f.write('\t'.join(fieldnames) + '\n')

import brd_bookmaker as bookmaker
import brd_quotationmaker as quotationmaker
import brd_extract_pagelist as extractor

vols2parse = [('39015078260935', 9)]

for vol, startpage in vols2parse:
    pagelist = extractor.extract(vol, startpage)
    books, author_errors = bookmaker.get_books(pagelist)
    quotations = quotationmaker.divide_into_quotations(books)

    with open(outfile, mode = 'a', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, delimiter = '\t', fieldnames = fieldnames)

        for quote in quotations:

            c = dict()
            book = quote.book

            c['bookauthor'] = book.author
            c['booktitle'] = book.title
            c['brdpage'] = book.pagenum
            c['price'] = book.price
            c['publication'] = quote.publication
            c['sentiment'] = quote.sentiment
            c['citation'] = quote.citation
            c['quote'] = quote.thequote

            writer.writerow(c)

        print(author_errors)








# brd_local_masterprocess.py

# Differs from the main brd_masterprocess by
# writing to a different outfile.

import os, sys, csv

outquotes = '/Users/tunder/Dropbox/python/reviews/output/brd_quotes.tsv'
outbooks = '/Users/tunder/Dropbox/python/reviews/output/brd_books.tsv'
quotefieldnames = ['bookauthor', 'booktitle', 'brdpage', 'price', 'publication',
                'sentiment', 'citation', 'quote']
bookfieldnames = ['bookauthor', 'booktitle', 'brdpage', 'price', 'publisher', 'reviewlines']

import brd_bookmaker as bookmaker
import brd_quotationmaker as quotationmaker
import brd_extract_local_pagelist as extractor

# vols2parse = [('39015078260935', 9)]
vols2parse = [('uiug.30112013681652', 8)]

for vol, startpage in vols2parse:
    pagelist = extractor.extract(vol, startpage)
    books, author_errors = bookmaker.get_books(pagelist)

    with open(outbooks, mode = 'w', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, delimiter = '\t', fieldnames = bookfieldnames)
        writer.writeheader()

        for book in books:

            c = dict()

            c['bookauthor'] = book.author
            c['booktitle'] = book.title
            c['brdpage'] = book.pagenum
            c['price'] = book.price
            c['publisher'] = book.publisher
            c['reviewlines'] = '\n | '.join(book.reviewlines)

            writer.writerow(c)

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
            c['publication'] = quote.publication
            c['sentiment'] = quote.sentiment
            c['citation'] = quote.citation
            c['quote'] = quote.thequote

            writer.writerow(c)

        print(author_errors)








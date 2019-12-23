# brd_final_masterprocess.py

import os, sys, csv

quotefieldnames = ['bookauthor', 'booktitle', 'brdpage', 'price', 'publisher', 'publication',
                'sentiment', 'citation', 'quote']

import brd_bookmaker as bookmaker
import brd_quotationmaker as quotationmaker
import extract_1920s_pagelist as extractor
import hyphenjoiner

quartets = []

with open('/media/secure_volume/brd/meta/1920sfiles.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        quartet = (row['year'], row['idsuffix'], int(row['start']), int(row['stop']))
        quartets.append(quartet)

for year, vol, startpage, endpage in quartets:
    print(year, vol, startpage, endpage)
    outfile = '/media/secure_volume/brd/output/' + year + '_' + vol + '.tsv'
    pagelist = extractor.extract(vol, startpage, endpage)
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

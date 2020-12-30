#!/usr/bin/env python

# 30smaster.py

import os, sys, csv

publishers = ['Liverlght', 'Appleton', 'Baker', 'Barnes', 'Benziger', 'Bobbs', "Brentano's", 'Cassell', 'Century', 'Collier-Fox', 'Crowell', 'Ditson', 'Dodd', 'Doran', 'Doubleday', 'Dutton', 'Elder', 'Estes', 'Ginn', 'Goodspeed', 'Harper', 'Heath', 'Holt', 'Houghton', 'Knopf', 'Lane', 'Lippincott', 'Little', 'Liveright', 'Longmans', 'Macmillan', 'McBride', 'McClure', 'McGraw', 'Moffat', 'Oxford', 'Page', 'Pott', 'Putnam', 'Scribner', 'Simmons', 'Stokes', 'Viking', 'Walton', 'Warne', 'Wessels', 'Wilde', 'Wiley', 'Winston', 'Yale']

quotefieldnames = ['bookauthor', 'booktitle', 'brdpage', 'price', 'publisher', 'publication',
                'sentiment', 'citation', 'quote']

import brd1930s_bookmaker as bookmaker
import brd_quotationmaker as quotationmaker
import extract_pagelist as extractor
import hyphenjoiner

quartets = []

with open('/media/secure_volume/brd/meta/1930sfiles.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        quartet = (row['year'], row['idsuffix'], int(row['start']), int(row['stop']))
        quartets.append(quartet)

for year, vol, startpage, endpage in quartets:
    print(year, vol, startpage, endpage)
    outfile = '/media/secure_volume/brd/output/' + year + '_' + vol + '.tsv'
    pagelist = extractor.extract(vol, startpage, endpage)
    books, author_errors = bookmaker.get_books(pagelist, publishers)
    quotations = quotationmaker.divide_into_quotations(books, publishers)

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

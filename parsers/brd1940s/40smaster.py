#!/usr/bin/env python

# 40smaster.py

import os, sys, csv

publishers = []

with open('40spublishers.txt', encoding = 'utf-8') as f:
    for line in f:
        publishers.append(line.strip())

quotefieldnames = ['bookauthor', 'booktitle', 'brdpage', 'price', 'publisher', 'publication',
                'sentiment', 'citation', 'quote']

import brd1940s_bookmaker as bookmaker
import brd1940s_quotationmaker as quotationmaker
import extract_pagelist as extractor
import hyphenjoiner

quartets = []

with open('/media/secure_volume/brd/meta/1940sfiles.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        quartet = (row['year'], row['idsuffix'], int(row['start']), int(row['stop']))
        quartets.append(quartet)

for year, vol, startpage, endpage in quartets:
    outfile = '/media/secure_volume/brd/output/' + year + '_' + vol + '.tsv'
    pagelist = extractor.extract(vol, startpage, endpage)
    books, author_errors = bookmaker.get_books(pagelist, publishers)
    print(year, vol, startpage, endpage, len(books))
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

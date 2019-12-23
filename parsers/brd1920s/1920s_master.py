# brd_final_masterprocess.py

import os, sys, csv

quotefieldnames = ['bookauthor', 'booktitle', 'brdpage', 'price', 'publisher', 'publication',
                'sentiment', 'citation', 'quote']

import brd_bookmaker as bookmaker
import brd_quotationmaker as quotationmaker
import brd_extract_pagelist as extractor
import hyphenjoiner


# The commented and uncommented sections below toggle to
# move this from multiple-volume to single-volume processing.

# year = '1917'
# suffix = '39015078261040'
# startpage = 9

# year_suffix_startpage = [(year, suffix, startpage)]

# with open('/media/secure_volume/brd/output/processed_files.tsv', mode = 'a', encoding = 'utf-8') as f:
#     for y, v, s in year_suffix_startpage:
#         f.write(y + '\t' + v + '\t' + str(s) + '\n')

bookdict = dict()

with open('/media/secure_volume/brd/output/processed_files.tsv', encoding = 'utf-8') as f:
    for line in f:
        fields = line.strip().split('\t')
        triplet = (fields[0], fields[1], int(fields[2]))
        bookdict[fields[1]] = triplet

year_suffix_startpage = []

for k, v in bookdict.items():
    year_suffix_startpage.append(v)

for year, vol, startpage in year_suffix_startpage:
    print(year, vol, startpage)
    outfile = '/media/secure_volume/brd/output/' + year + '_' + vol + '.tsv'
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

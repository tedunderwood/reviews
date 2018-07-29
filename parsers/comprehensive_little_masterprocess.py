# comprehensive_little_masterprocess.py

import os, sys

outfile = sys.argv[1]
fieldnames = ['articleauth', 'byorabout', 'genre', 'year', 'journal', 'subject']

if not os.path.isfile(outfile):
    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        f.write('\t'.join(fieldnames) + '\n')

import comprehensive_little_authormaker as authormaker
import comprehensive_little_citationmaker as citationmaker
import extract_pagelist as extractor

vols2parse = ['39015019184806']

for vol in vols2parse:
    pagelist = extractor.extract(vol)
    authors, author_names = authormaker.get_authors(pagelist)

    with open('authorlist.txt', mode = 'a', encoding = 'utf-8') as f:
        for auth in author_names:
            f.write(auth + '\n')

    citations = citationmaker.authors_to_citations(authors)

    with open(outfile, mode = 'a', encoding = 'utf-8') as f:
        writer = DictWriter(f, delimiter = '\t', fieldnames = fieldnames)

        for cite in citations:

            c = dict()
            c['articleauth'] = cite.attributes['author_name']
            c['byorabout'] = cite.attributes['group_tag']

            if 'date' in cite.attributes:
                c['year'] = cite.attributes['date']
            else:
                c['year'] = float('nan')

            c['genre'] = cite.get_part('genre')
            c['journal'] = cite.get_part('journal')
            c['subject'] = cite.get_part('subject')

            # the get_part() method has a failsafe of
            # returning an empty string if the part
            # doesn't exist.

            writer.writerow(c)








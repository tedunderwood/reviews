#!/usr/bin/env python

# clm_master.py

import os, sys, csv, re

import extract_clm_pagelist as extractor

from difflib import SequenceMatcher

def strings_similar(a, b):
    matcher = SequenceMatcher(None, a, b)
    ratio = matcher.ratio()
    if ratio > .81:
        return True
    else:

workoptions = ['BY', 'ABOUT']
yearregex = re.compile('.{0,1}\d{2}\)')

clm_volumes = ['39015079928167', '39015079928159', '39015079928183',
        '39015079928142', '39015019184806', '39015079928175',
        '39015079928209', '39015079928191']

def starts_uppercase(astring):
    if len(astring) < 1:
        return False
    elif len(astring) > 4:
        sample = astring[0: 4]
    else:
        sample = astring

    if sample.is_upper():
        return True


for vol in clm_volumes:
    outfile = '/media/secure_volume/clm/output/' + vol + '.tsv'
    pagelist = extractor.extract(vol, 0, 2500)

    results = []
    
    startedyet = False
    author = 'Not An Author'
    outoforder = False
    byorabout = 'BY'
    yearsforauth = dict()
    for option in workoptions:
        yearsforauth[option] = []

    for page in pagelist:
        for line in page:
            if not startedyet:
                if line.startswith('VOLUM') or line.startwith('WORKS'):
                    startedyet = True
            elif not starts_uppercase(line):
                words = line.strip().split():
                for word in line:
                    if hyphenregex.fullmatch(word):
                        year = int(word[-3: -1])
                        yearsforauth[byorabout].append(year)
            else:
                if strings_similar(line, 'LITTLE MAGAZINE INDEX'):
                    continue
                elif strings_similar(line, 'WORKS BY'):
                    byorabout = 'BY'
                elif strings_similar(line, 'WORKS ABOUT'):
                    byorabout = 'ABOUT'
                else:
                    results.append((author, outoforder, yearsforauth))
                    if line < author:
                        outoforder = True
                    else:
                        outoforder = False
                    author = line
                    yearsforauth = dict()
                    for option in workoptions:
                        yearsforauth[option] = []

    results.append((author, outoforder, yearsforauth))

    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        f.write('author\toutoforder\tbyorabout\tyearlist\n')
        for auth, outoforder, yearsforauth in results:
            f.write(auth + '\t' + str(outoforder) + '\t' + 'BY\t' + ' '.join([str(x) for x in yearsforauth['BY']]) + '\n')
            f.write(auth + '\t' + str(outoforder) + '\t' + 'ABOUT\t' + ' '.join([str(x) for x in yearsforauth['ABOUT']]) + '\n')








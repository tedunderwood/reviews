#!/usr/bin/env python

# clm_master.py

import os, sys, csv, re

import extract_pagelist as extractor

from difflib import SequenceMatcher

def strings_similar(a, b, caplength):

    if len(a) > caplength:
        a = a[0: caplength]
    if len(b) > caplength:
        b = b[0: caplength]

    matcher = SequenceMatcher(None, a, b)
    ratio = matcher.ratio()
    if ratio > .80:
        return True
    else:
        return False

workoptions = ['BY', 'ABOUT']
yearregex = re.compile('.{0,1}\d{2}\)')

clm_volumes = ['39015079928167', '39015079928159', '39015079928183',
        '39015079928142', '39015019184806', '39015079928175',
        '39015079928209', '39015079928191']

def starts_uppercase(astring):
    if len(astring) < 6:
        return False
    elif len(astring) > 8:
        sample = astring[0: 8]
    else:
        sample = astring

    if not sample.isupper():
        return False

    lettercount = 0
    for letter in sample:
        if letter.isalpha():
            lettercount += 1

    if lettercount >= 5:
        return True
    else:
        return False

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

    wordsthatfail = 0
    wordsthatfit = 0

    for page in pagelist:
        for line in page:

            if not startedyet:
                if line.startswith('VOLUM') or line.startswith('WORKS'):
                    startedyet = True
            elif starts_uppercase(line):
                if strings_similar(line, 'LITTLE MAGAZINE INDEX', 22):
                    continue
                elif strings_similar(line, 'MAGAZINES INDEXED', 22):
                    continue
                elif strings_similar(line, 'WORKS BY', 9):
                    byorabout = 'BY'
                elif strings_similar(line, 'WORKS ABOUT', 12):
                    byorabout = 'ABOUT'
                else:
                    results.append((author, outoforder, yearsforauth))
                    if line < author:
                        outoforder = True
                    else:
                        outoforder = False
                    if len(line) > 50:
                        line = line[0: 50]
                    line = line.replace('\t', ' ')
                    author = line
                    yearsforauth = dict()
                    for option in workoptions:
                        yearsforauth[option] = []
                    byorabout = 'BY'
            
            line = line.replace(')', ') ')  # these two replace operations
            line = line.replace("'", " '")  # ensure '39) is surrounded by spaces
            words = line.strip().split()
            for word in words:
                if yearregex.fullmatch(word):
                    year = int(word[-3: -1])
                    yearsforauth[byorabout].append(year)
                    wordsthatfit += 1
                else:
                    wordsthatfail += 1

    results.append((author, outoforder, yearsforauth))

    print(wordsthatfit, wordsthatfail)

    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        f.write('author\toutoforder\tbyorabout\tyearlist\n')
        for auth, outoforder, yearsforauth in results:
            if len(yearsforauth['BY']) < 1 and len(yearsforauth['ABOUT']) < 1:
                continue
            f.write(auth + '\t' + str(outoforder) + '\t' + 'BY\t' + ' '.join([str(x) for x in yearsforauth['BY']]) + '\n')
            f.write(auth + '\t' + str(outoforder) + '\t' + 'ABOUT\t' + ' '.join([str(x) for x in yearsforauth['ABOUT']]) + '\n')








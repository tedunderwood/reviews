#!/usr/bin/env python

# clm_master.py

import os, sys, csv, re

import extract_pagelist as extractor

from difflib import SequenceMatcher

import pandas as pd

titles = pd.read_csv('titlewords.tsv', sep ='\t')

authorset = [x.upper() for x in titles.author]

initialdict = dict()

for auth in authorset:
    initial = auth[0]
    if initial not in initialdict:
        initialdict[initial] = []
    initialdict[initial].append(auth)


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
    outfile = '/media/secure_volume/clm/output/titlematch' + vol + '.tsv'
    pagelist = extractor.extract(vol, 0, 2500)

    results = []
    
    startedyet = False
    author = 'Not An Author'
    titledict = dict()
    outoforder = False
    byorabout = 'BY'
    yearsforauth = dict()
    for option in workoptions:
        yearsforauth[option] = []

    wordsthatfail = 0
    wordsthatfit = 0
    publicationyearmatch = 0

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
                elif strings_similar(line, 'WORKS ABOUT', 12):
                    byorabout = 'ABOUT'
                elif strings_similar(line, 'WORKS BY', 9):
                    byorabout = 'BY'
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

                    initial = author[0]
                    if initial in initialdict:
                        authcandidates = initialdict[initial]
                        maxmatch = 0
                        for auth in authcandidates:
                            matcher = SequenceMatcher(None, author, auth)
                            thematchratio = matcher.ratio()
                            if thematchratio > 0.8 and thematchratio > maxmatch:
                                authmatch = auth
                                maxmatch = thematchratio
                        if maxmatch > 0:
                            books = titles.loc[titles.author == authmatch.lower(), : ]
                            # print(authmatch, len(books))
                            titledict = dict()
                            for idx, row in books.iterrows():
                                words = row.titlewords.split()
                                date = int(row.date)
                                for w in words:
                                    w = w.strip('",[]')
                                    if w == 'novel' or w == 'stories':
                                        continue
                                    titledict[w] = date
                                print(authmatch, len(titledict))
                        else:
                            titledict = dict()
                            publicationyearmatch = 0
                    else:
                        titledict = dict()
                        publicationyearmatch = 0
            
            line = line.replace(')', ') ')  # these two replace operations
            line = line.replace("'", " '")  # ensure '39) is surrounded by spaces
            words = line.strip().split()
            for word in words:
                wordlow = word.lower().strip(':;,.()[]')
                if wordlow in titledict:
                    publicationyearmatch = titledict[wordlow]
                    print(word, publicationyearmatch)
                if yearregex.fullmatch(word):
                    year = int(word[-3: -1])
                    if publicationyearmatch > 0:
                        yearsforauth[byorabout].append(str(year) + '--' + str(publicationyearmatch))
                    wordsthatfit += 1
                    publicationyearmatch = 0
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







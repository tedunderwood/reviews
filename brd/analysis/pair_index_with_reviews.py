# -*- coding: utf-8 -*-
# pair_index_with_reviews.py
# Ted Underwood, Dec 2019

# This script reads the authors and titles from the BRD index of fiction
# (parsed by Wenyi Shang) and pairs them with review metadata
# (parsed by Ted Underwood) in order to create a table of books confirmed
# as fiction, along with aggregated metadata about those books
# (for instance, the price, the number of reviews, the average wordcount
# of reviews, and the average sentiment as reported by BRD).

# I'm just going to say up front that the particular thresholds and
# formulae used here are super ad hoc and hacky.

import pandas as pd
import numpy as np
import re, math, csv
from difflib import SequenceMatcher

wordcountregex = re.compile('\d*0w[.]?')

# we read a list of files to process from disk
# each row of this file contains three data elements:
#
# * an 'indexpath' that provides the complete file path
# to an index file
#
# * a 'reviewsname' that names an extracted .tsv with
# per-review data; these are expected to all be in the
# same folder
#
# * an 'outfilename' under which the results will be saved

triplets2process = []

with open('pairing_meta.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        triplets2process.append(row)

def get_ratio(stringA, stringB):

    '''
    A generic function to get fuzzy similarity between two strings.
    '''

    m = SequenceMatcher(None, stringA, stringB)

    thefilter = m.real_quick_ratio()

    if thefilter < 0.5:
        return thefilter

    else:
        return m.ratio()

def get_title_ratio(stringA, stringB):

    '''
    When searching for the similarity between two titles, we use this modified version,
    which gives a boost to the similarity when it applies to two long strings, but also
    permits relatively high similarity in cases where one string is much longer than
    the other and only the overlapping starts are similar. This is useful because there
    are often variant fiction titles like

    Shane
    and
    Shane: A Story of the American West.
    '''

    origA = stringA
    origB = stringB

    minlen = min(len(stringA), len(stringB))

    if minlen > 3:
        stringA = stringA[0: minlen]
        stringB = stringB[0: minlen]

    if minlen < 20:
        lendiscount = 1.2 - (((20 - minlen) ** 1.1) / 100)
    else:
        lendiscount = 1.2

    m = SequenceMatcher(None, stringA, stringB)

    thefilter = m.real_quick_ratio()
    if thefilter < 0.6:
        return thefilter * lendiscount

    else:
        primarymatch = m.ratio() * lendiscount
        m2 = SequenceMatcher(None, origA, origB)
        secondarymatch = m2.ratio()

        return max(primarymatch, secondarymatch)

def onlyalpha(astring):
    alphapart = ''
    for character in astring:
        if character.isalpha():
            alphapart = alphapart + character
    return alphapart

def name_to_initial(authname):
    if pd.isnull(authname):
        return('0')
    else:
        return authname.lower()[0]

def makeint(wordcount):
    wordcount = wordcount[ : -1]
    try:
        intwords = int(wordcount)
    except:
        intwords = 10
    return intwords

def specialsplit(author):
    '''
    The goal here is basically to split an author name into parts,
    using punctuation to divide parts, but stripping it. Probably a
    simpler, more pythonic solution could be written.
    '''

    thispart = []
    allnames = []

    for idx, character in enumerate(author):
        if character == '.' or character == ',' or character == ':' or character == '(' or character == ')' or character == ' ':
            if len(thispart) > 0:
                thisname = ''.join(thispart)
                allnames.append(thisname)
                thispart = []
        else:
            thispart.append(character)

    if len(thispart) > 0:
        thisname = ''.join(thispart)
        allnames.append(thisname)

    return allnames

for triplet in triplets2process:

    indexpath = row['indexpath']

    reviewsname = row['reviewsname']
    reviewspath = '/media/secure_volume/brd/output/' + reviewsname

    outfilename = row['outfilename']
    outfilepath = '/media/secure_volume/brd/paired/' + outfilename

    year = outfilename[-4: ]

    bookdata = dict()
    bookmeta = dict()

    print(outfilename)

    # first open the index/"extract" file
    # to create a list of author-title combos
    # confirmed as fiction

    fic_authors = dict()

    numindexlines = 0

    with open(indexpath, encoding = 'utf-8') as f:
        for indexlinenum, line in enumerate(f):
            if line.startswith('<\h'):
                continue
            else:
                line = line.strip('\n.')
                fields = line.split('$')
                author = fields[0]
                title = fields[1].lower()

                authnames = specialsplit(author)
                if len(authnames) > 1:
                    lastname = authnames[0].lower()
                    initials = ''.join([onlyalpha(x[0].lower()) for x in authnames[1:]])
                else:
                    lastname = author.lower()

            theinitial = lastname[0]
            if theinitial not in fic_authors:
                fic_authors[theinitial] = []

            fic_authors[theinitial].append((lastname, initials, title, indexlinenum))
            numindexlines += 1

    reviews = pd.read_csv(reviewspath, sep = '\t')

    reviews = reviews.assign(initial = reviews.bookauthor.map(name_to_initial))

    initialgroups = reviews.groupby('initial')

    initialdict = dict()

    for initial, df in initialgroups:
        initialdict[initial] = df

    del initialgroups

    matchedindexes = []
    notfound = []

    previousreviews = dict()
    previousindexlines = dict()
    dislodgedindexlines = []

    for init, auth_titles in fic_authors.items():

        df = initialdict[init]

        for lastname, first_initials, title, indexlinenum in auth_titles:

            closestreviewidx = -1
            maxcloseness = 0
            nextcloseness = 0
            nextreviewidx = -1
            besttitleratio = 0

            if len(lastname) < 3 or len(title) < 3:
                continue

            for reviewidx, row in df.iterrows():
                bookauthor = row['bookauthor'].strip('.,')
                booktitle = row['booktitle']

                if pd.isnull(bookauthor) or pd.isnull(booktitle):
                    continue
                elif len(bookauthor) < 5 or len(booktitle) < 4:
                    continue
                else:
                    booktitle = booktitle.lower().replace('— ', '').replace('- ', '')

                authnames = specialsplit(bookauthor)
                book_initials = ''
                if len(authnames) > 1:
                    book_last = authnames[0].lower().replace('- ', '').replace('— ', '')
                    for name in authnames[1:]:
                        if len(name) > 0:
                            book_initials = book_initials + name[0].lower()
                else:
                    book_last = bookauthor.lower()

                lastratio = get_ratio(lastname, book_last)

                if lastratio > 0.5:
                    initialratio = get_ratio(first_initials, book_initials)

                    minlen = min(len(first_initials), len(book_initials))

                    if initialratio < 0.5 and minlen > 0 and first_initials[0] == book_initials[0]:
                        initialratio = 0.5
                    elif minlen == 0:
                        initialratio = 0.25

                    titleratio = get_title_ratio(title.replace('- ', ''), booktitle)

                    overallmatch = (lastratio + (initialratio * .45)) * ((titleratio + .08) ** 1.5)

                    if reviewidx in previousreviews:
                        prevclose, prevmatch = previousreviews[reviewidx]
                    else:
                        prevclose = 0

                    if overallmatch > maxcloseness and overallmatch > prevclose:

                        maxcloseness = overallmatch
                        closestreviewidx = reviewidx
                        besttitleratio = titleratio

            if maxcloseness > 0.77:

                if closestreviewidx in previousreviews:
                    # we made a mistake with our first assignment
                    # let's assign this index line to its next best match

                    prevclose, prevmatch = previousreviews[closestreviewidx]
                    dislodgedindexlines.append((prevmatch, closestreviewidx))
                    removeindex = year + '+' + str(prevmatch)
                    bookmeta.pop(removeindex)

                previousreviews[closestreviewidx] = maxcloseness, indexlinenum

                masterindex = year + '+' + str(indexlinenum)
                bookmeta[masterindex] = dict()
                bookmeta[masterindex]['closeness'] = maxcloseness
                bookmeta[masterindex]['target'] = lastname + ' + ' + first_initials + ' + ' + title
            else:
                if closestreviewidx < 0:
                    matchtitle = 'no title found'
                else:
                    matchtitle = reviews.loc[closestreviewidx, 'booktitle']

                notfound.append((lastname, first_initials, title, maxcloseness, matchtitle))

    allsentiments = []

    matchedindexes = list(previousreviews.keys())

    for idx in matchedindexes:
        author = reviews.loc[idx, 'bookauthor']
        title = reviews.loc[idx, 'booktitle']
        publisher = reviews.loc[idx, 'publisher']

        matchingrows = reviews.loc[(reviews.bookauthor == author) & (reviews.booktitle == title),  : ]
        # print(author, title, matchingrows.shape)

        sentiments = []
        wordcount = 0
        price = 0

        for idx2, row in matchingrows.iterrows():
            if row.price > 0:
                price = row.price

            if not pd.isnull(row.citation):
                citationparts = row.citation.split()
                if len(citationparts) > 0 and wordcountregex.fullmatch(citationparts[-1]):
                    thesewords = makeint(citationparts[-1])
                    if thesewords < 3000:
                        wordcount += thesewords
                    else:
                        wordcount += 3000
                        # we impose a cap on super-long reviews because I'm skeptical
                else:
                    wordcount += 10

            if pd.isnull(row.sentiment):
                thissent = float('NaN')
            elif row.sentiment == '+' or row.sentiment == '+ +' or row.sentiment == '+ + +':
                thissent = 4
            elif row.sentiment == '+ -':
                thissent = 3
            elif row.sentiment == '- +':
                thissent = 2
            elif row.sentiment == '-' or row.sentiment == '- -':
                thissent = 1

            allsentiments.append(thissent)
            sentiments.append(thissent)

        closeness, indexlinenum = previousreviews[idx]
        masterindex = year + '+' + str(indexlinenum)
        bookdata[masterindex] = [author, title, price, wordcount, idx2, publisher, sentiments]

    average_sentiment = np.nanmean(allsentiments)

    for idx, data in bookdata.items():
        sentiments = data[6]
        sentcount = np.count_nonzero(~np.isnan(sentiments))
        sentiments = [average_sentiment if math.isnan(x) else x for x in sentiments]
        sentiment = np.mean(sentiments)
        data[6] = sentiment
        data.append(sentcount) # number of non-NaN reviews
        data.append(len(sentiments)) # total number of reviews

    with open(outfilepath + '.tsv', mode = 'w', encoding = 'utf-8') as f:
        f.write('index\tauthor\ttitle\tprice\twordcount\trows\tpublisher\tavgsent\tnumreviewswithsent\tnumallreviews\tcloseness\ttarget\n')
        for idx, data in bookdata.items():
            outrow = [idx]
            outrow.extend([str(x) for x in data])
            outrow.extend([str(bookmeta[idx]['closeness']), bookmeta[idx]['target']])
            f.write('\t'.join(outrow) + '\n')


    notfound = sorted(notfound, key = lambda x: x[3])

    percentfound = len(bookdata) / numindexlines

    percentfound = round(percentfound, 2)

    print('Index lines: ' + str(numindexlines) + '\t Found: ' + str(len(bookdata)))
    print('Not found: ' + str(len(notfound)) + '\t Percent found: ' + str(percentfound))
    print()





















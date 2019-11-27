import pandas as pd
import numpy as np
import re, math
from difflib import SequenceMatcher

wordcountregex = re.compile('\d*0w[.]?')

# extract_files = ['../data/volume8 extract.txt', '../data/volume9 extract.txt',
#     '../data/volume10 extract.txt', '../data/volume11 extract.txt',
#     '../data/volume12 extract.txt', '../data/volume13 extract.txt']

# review_files = ['/media/secure_volume/brd/output/1912_39015078260992.tsv',
# '/media/secure_volume/brd/output/1913_33433082016522.tsv',
# '/media/secure_volume/brd/output/1914_32106019850293.tsv',
# '/media/secure_volume/brd/output/1915_30112013681629.tsv',
# '/media/secure_volume/brd/output/1916_33433082016555.tsv',
# '/media/secure_volume/brd/output/1917_39015078261040.tsv']

extract_files = ['../data/volume14 extract.txt']
review_files = ['/Users/tunder/Dropbox/python/reviews/output/brd_quotes.tsv']

def get_ratio(stringA, stringB):

    m = SequenceMatcher(None, stringA, stringB)

    thefilter = m.real_quick_ratio()
    if thefilter < 0.7:
        return thefilter

    else:
        return m.ratio()

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
    firstpart = []

    for idx, character in enumerate(author):
        if character == '.' or character == ',' or character == ':':
            lastname = ''.join(firstpart)
            firstname = author[idx: ]
            return[lastname, firstname]
        else:
            firstpart.append(character)

    return author


yearctr = 0
bookdata = dict()
bookmeta = dict()

for ef, rf in zip(extract_files, review_files):

    yearctr += 1

    fic_authors = dict()

    with open(ef, encoding = 'utf-8') as f:
        for line in f:
            if line.startswith('<\h'):
                continue
            else:
                line = line.strip('\n.')
                fields = line.split('$')
                author = fields[0]
                title = fields[1]

                authnames = specialsplit(author)
                if len(authnames) > 1:
                    lastname = authnames[0].lower()
                    initials = onlyalpha(authnames[1].lower())
                else:
                    lastname = author.lower()

            theinitial = lastname[0]
            if theinitial not in fic_authors:
                fic_authors[theinitial] = []

            fic_authors[theinitial].append((lastname, initials, title))

    reviews = pd.read_csv(rf, sep = '\t')

    reviews = reviews.assign(initial = reviews.bookauthor.map(name_to_initial))

    initialgroups = reviews.groupby('initial')

    initialdict = dict()

    for initial, df in initialgroups:
        initialdict[initial] = df

    del initialgroups

    matchedindexes = []

    for init, auth_titles in fic_authors.items():

        df = initialdict[init]

        for lastname, first_initials, title in auth_titles:

            closestmatch = -1
            closeness = 0

            if len(lastname) < 3 or len(title) < 3:
                continue

            for idx, row in df.iterrows():
                bookauthor = row['bookauthor']
                booktitle = row['booktitle']

                if pd.isnull(bookauthor) or pd.isnull(booktitle):
                    continue
                if len(bookauthor) < 5 or len(booktitle) < 4:
                    continue

                authnames = specialsplit(bookauthor)
                book_initials = ''
                if len(authnames) > 1:
                    book_last = authnames[0].lower()
                    for name in authnames[1:]:
                        if len(name) > 0:
                            book_initials = book_initials + name[0].lower()
                else:
                    book_last = bookauthor.lower()

                lastratio = get_ratio(lastname, book_last)

                if lastratio > 0.75:
                    initialratio = get_ratio(first_initials, book_initials)
                    titleratio = get_ratio(title, booktitle.lower())

                    overallmatch = (lastratio + (initialratio * .25)) * titleratio

                    if overallmatch > closeness:
                        closeness = overallmatch
                        closestmatch = idx

            if closeness > 0.5:
                matchedindexes.append(closestmatch)
                masterindex = str(yearctr) + '+' + str(closestmatch)
                bookmeta[masterindex] = dict()
                bookmeta[masterindex]['closeness'] = closeness
                bookmeta[masterindex]['target'] = lastname + ' + ' + first_initials + ' + ' + title

    allsentiments = []

    for idx in matchedindexes:
        author = reviews.loc[idx, 'bookauthor']
        title = reviews.loc[idx, 'booktitle']

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

        masterindex = str(yearctr) + '+' + str(idx)
        bookdata[masterindex] = [author, title, price, wordcount, idx2, sentiments]


    average_sentiment = np.nanmean(allsentiments)

    for idx, data in bookdata.items():
        sentiments = data[5]
        sentiments = [average_sentiment if math.isnan(x) else x for x in sentiments]
        sentiment = np.mean(sentiments)
        data[5] = sentiment

with open('outdata.tsv', mode = 'w', encoding = 'utf-8') as f:
    f.write('index\tauthor\ttitle\tprice\twordcount\trows\tavgsent\tcloseness\ttarget\n')
    for idx, data in bookdata.items():
        outrow = [idx]
        outrow.extend([str(x) for x in data])
        outrow.extend([str(bookmeta[idx]['closeness']), bookmeta[idx]['target']])
        f.write('\t'.join(outrow) + '\n')
























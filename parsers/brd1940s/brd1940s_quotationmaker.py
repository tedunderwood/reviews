# brd_quotationmaker.py

# This module accepts a list of Book objects,
# and divides them into Quotations.

# As often with Python, it may make sense to start reading from the
# bottom of the script, and move up.

import lexparse, re
import read_pubnames
from difflib import SequenceMatcher

def match_strings(stringA, stringB):
    m = SequenceMatcher(None, stringA, stringB)
    match = m.quick_ratio()

    if match > 0.7:
        match = m.ratio()

    return match

class Quotation:

    # A quotation combines book information with information
    # about the reviewing publication, and review sentiment
    # (when available). There's also a citation (which may include
    # volume, date, page number and so on, but is not parsed at
    # this stage). Finally, of course, there's the quotation from
    # the review.

    def __init__(self, book, review, sentiment, cite, thequote):

        self.book = book
        self.publication = review
        self.sentiment = sentiment
        self.citation = cite
        self.thequote = thequote

def divide_into_quotations(booklist, publishers):

    all_reviewwords, reviewdict = read_pubnames.get_names('brd_pubs_indexed1940s.tsv')

    with open('allreviewwords.txt', mode = 'w', encoding = 'utf-8') as f:
        for w in all_reviewwords:
            f.write(w + '\n')

    reviewnames = set(reviewdict.keys())

    lexical_patterns = [('numeric', '.?[0-9]{1,7}.?[0-9]*[,.:=]?'), \
    ('reviewword', all_reviewwords),
    ('openparen', '\(.*'),
    ('closeparen', '.*\)'),
    ('fullstop', '.*\.'),
    ('commastop', '.*\,'),
    ('startdash', '—.*'),
    ('numeric', {'I:', 'II:', 'III:', 'IV:'}),
    ('titlecase', '[A-Z].*'),
    ('monthabbrev', {'Ja', 'F', 'Mr', 'Ap', 'My', 'Je', 'Jl', 'Ag', 'S', 'O', 'N', 'D'}),
    ('lineendingyear', '[\'"•■]\d+'),
    ('volandpgrange', '[0-9]+[:][0-9-]+'),
    ('somenumeric', '.?.?[0-9]{1,7}.?.?[0-9]*.?'),
    ('allcaps', '[A-Z\'\,]+'),
    ('dollarprice', '.*\$.?.?[0-9]{1,7}.?[0-9]*[,.:=]?'),
    ('centprice', '.?.?[0-9]{1,7}.?[0-9]*c+[,.:=]?'),
    ('hyphennumber', '[0-9]{1,3}[-—~]+[0-9]{3,7}[,.:=)]?'),
    ('openquote', '[\"\'“‘]+\S*'),
    ('plusorminus', '[\+\-\—]+'),
    ('reviewword', all_reviewwords),
    ('wordcount', '\d*0w[.]?'),
    ('OCRwordcount', '\S*Ow[.]?')
    ]

    wordcountregex = re.compile('\d*0w[.]?')
    ocrwordcountregex = re.compile('\S*Ow[.]?')

    rule_list = lexparse.patterns2rules(lexical_patterns)
    allquotes = []

    plusmisreads = {'-4-', '4-', '1-', '-1-', '4—', '1—', '-|-',
        '-l-', '-)-', '—|—', '-I-', '-(-', '-f'}

    monthnames = {'Ja', 'F', 'Mr', 'Ap', 'My', 'Je', 'Jl', 'Ag', 'S' , 'O', 'D'}

    for book in booklist:
        lines = book.reviewlines

        accumulated = []
        citationcount = 0

        addtonext = ''
        skipnext = False

        for linecount, line in enumerate(lines):

            # We keep track of linecount because there are
            # characteristic kinds of noise early on, when trailing lines
            # of a citation get treated as part of the review.

            if len(addtonext) > 0:
                line = addtonext + ' ' + line
                addtonext = ''

            if skipnext:
                skipnext = False
                continue

            tokens = line.strip().split()
            if len(tokens) < 1:
                continue

            taglist = lexparse.apply_rule_list(rule_list, tokens)

            # in the first two lines we often have fragments
            # left over from the book bibliographical entry

            if linecount <= 3:
                trailingbibline = False

                for tags in taglist.tagseq:
                    if 'hyphennumber' in tags or 'dollarprice' in tags or 'centprice' in tags:
                        trailingbibline = True

                if trailingbibline:

                    # get the existing publisher to see if it makes more sense
                    # fused with something in this trailing line

                    existingpubparts = book.publisher.split()
                    if len(existingpubparts) > 0:
                        existingpub = existingpubparts[-1].strip('-')
                    else:
                        existingpub = 'not a publisher'

                    tokenssofar = []
                    for l in accumulated:
                        tokenssofar.extend(l.strip().split())
                    tokenssofar.extend(tokens)

                    tokenssofar = [x.strip('.,[]()-') for x in tokenssofar]

                    for tok in tokenssofar:
                        if tok in publishers:
                            book.publisher = tok

                        rejoined = existingpub + tok
                        if rejoined in publishers:
                            book.publisher = book.publisher.strip('-') + tok

                    line = line + ' <endsubj>'
                    accumulated.append(line)
                    continue

            # Sometimes a book is followed by a summary that
            # is not attributed to any particular review.
            # The only way I have to identify this is,
            # that a) this is the first sequence of lines and
            # b) the next line opens with a quotation mark,
            # and there has been no other citation info provided
            # yet.

            if citationcount == 0 and len(accumulated) > 3:
                if 'openquote' in taglist.tagseq[0]:
                    sentiment = ''
                    review = 'summary'
                    cite = 'summary'
                    citationcount += 1
                    quote = Quotation(book, review, sentiment, cite, accumulated)
                    allquotes.append(quote)
                    accumulated = []
                    accumulated.append(line)
                    # this line (opening with a quote) will be part of the next quotation
                    matched = True
                    continue

            numberwords = 0
            reviewwords = 0
            plusyet = False
            totalclues = 0

            for word, tags in zip(taglist.stringseq, taglist.tagseq):
                if 'reviewword' in tags:
                    reviewwords += 1
                    totalclues += 1

                elif 'plusorminus' in tags and not plusyet:
                    reviewwords += 0.5
                    totalclues += 1
                    plusyet = True

                elif word in monthnames:
                    totalclues += 1

                elif 'somenumeric' in tags and not '-' in word and not ',' in word:
                    numberwords += 1
                    totalclues += 1
                    if word.endswith('w'):
                        totalclues += 1
                        reviewwords += 0.5
                    elif ':' in word:
                        totalclues += 1
                        reviewwords += 0.5
                    elif word.startswith('p'):
                        totalclues += 1
                        reviewwords += 0.5

            if numberwords > 0 and reviewwords > 0.9 and totalclues > 3:
                sentimentbits = []

                numericyet = False
                publisherbits = []
                citationbits = []

                nextwordctr = 0

                for word, tags in zip(taglist.stringseq, taglist.tagseq):

                    nextwordctr += 1

                    if not numericyet and word == '+':
                        sentimentbits.append('+')
                        continue
                    if not numericyet and word in plusmisreads:
                        # e.g. '4-' is a fairly common ocr misread for +
                        sentimentbits.append('+')
                        continue
                    if not numericyet and (word == '-' or word == '—' or word == '—-'):
                        sentimentbits.append('-')
                        continue
                    if not numericyet and (word == '=-' or word == '--' or word == '-—'):
                        sentimentbits.append('-')
                        continue
                    if not numericyet and (word == '==' or word == '=--' or word == '—-'):
                        sentimentbits.append('-')
                        continue
                    if not numericyet and (word == '+-' or word == '+—' or word == '+='):
                        sentimentbits.append('+')
                        sentimentbits.append('-')
                        continue
                    if not numericyet and (word == '-+' or word == "—+" or word == '=+'):
                        sentimentbits.append('-')
                        sentimentbits.append('+')
                        continue
                    if not numericyet and (word == '++-' or word == '++—' or word == "++="):
                        sentimentbits.append('+')
                        sentimentbits.append('+')
                        continue
                        sentimentbits.append('-')
                    if not numericyet and (word == '++'):
                        sentimentbits.append('+')
                        sentimentbits.append('+')
                        continue
                    if not numericyet and (word == '+++'):
                        sentimentbits.append('+')
                        sentimentbits.append('+')
                        sentimentbits.append('+')
                        continue
                    if not numericyet and nextwordctr == 1 and word == "H":
                        # this is a weird but common misread; however, it's risky
                        # enough that we should only do it in first position
                        sentimentbits.append('+')
                        sentimentbits.append('-')
                        continue

                    if 'somenumeric' in tags:
                        numericyet = True

                    if not numericyet:
                        publisherbits.append(word)
                    else:
                        citationbits.append(word)

                    if numericyet and ('wordcount' in tags or 'OCRwordcount' in tags) and (nextwordctr < len(taglist.stringseq)):
                        addtonext = ' '.join(taglist.stringseq[nextwordctr : ])
                        break

                # if this line doesn't end with a word count, and the next one does?
                # probably a continuation

                if len(citationbits) > 0 and not wordcountregex.fullmatch(citationbits[-1]) and not ocrwordcountregex.fullmatch(citationbits[-1]):
                    if linecount < (len(lines) - 1):
                        wordsinnextline = lines[linecount + 1].strip().split()
                        if len(wordsinnextline) > 0 and len(wordsinnextline) < 3 and wordcountregex.fullmatch(wordsinnextline[-1]):
                            citationbits.extend(wordsinnextline)
                            skipnext = True

                sentiment = ' '.join(sentimentbits)
                review = ' '.join(publisherbits)
                cite = ' '.join(citationbits)
                citationcount += 1

                quote = Quotation(book, review, sentiment, cite, accumulated)
                allquotes.append(quote)
                accumulated = []

            else:
                # odds of review 1 or less
                accumulated.append(line)

    return allquotes















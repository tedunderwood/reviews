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

def divide_into_quotations(booklist):

    all_reviewwords, reviewdict = read_pubnames.get_names('brd_pubs_indexed.tsv')
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
    ('wordcount', '\d*0w[.]?')
    ]

    wordcountregex = re.compile(lexical_patterns['\d*0w[.]?'])

    rule_list = lexparse.patterns2rules(lexical_patterns)
    allquotes = []

    trailingbibs = []

    plusmisreads = {'-4-', '4-', '1-', '-1-', '4—', '1—', '-|-',
        '-l-', '-)-', '—|—', '-I-', '-(-', '-f'}

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



            # Most of the reviews in BRD are followed by a separate
            # citation line like this:

            # + Boston Transcript p6 O 9 '20 340w

            # That's easy to parse! Beautiful. Most of the code below
            # will be devoted to that ordinary case.

            # But the last line of the *first* review,
            # which is just summarizing the book as a whole,
            # often looks like this:

            # to Lloyd's register."—-N Y P I. New Tech Bits

            # That's a trickier situation and requires special care.

            # if "—" in line:
            #     parts = line.split('—')
            #     possiblename = parts[-1]
            #     if len(possiblename) > 3:
            #         matched = False

            #         for review in reviewnames:
            #             match = match_strings(possiblename, review)
            #             if match > 0.9:
            #                 accumulated.append(parts[0])
            #                 # add the part before the review name
            #                 sentiment = ''
            #                 cite = ''
            #                 citationcount += 1
            #                 quote = Quotation(book, reviewdict[review], sentiment, cite, accumulated)
            #                 allquotes.append(quote)
            #                 accumulated = []
            #                 matched = True
            #                 break

            #         if matched:
            #             continue

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
                    for oldline in accumulated:
                        trailingbibs.append(oldline)
                    accumulated = []
                    trailingbibs.append(line)
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

            oddsofreview = 0
            reviewwordyet = False

            for word, tags in zip(taglist.stringseq, taglist.tagseq):
                if 'reviewword' in tags and not reviewwordyet:
                    oddsofreview += 1
                    reviewwordyet = True
                if 'plusorminus' in tags:
                    oddsofreview += 1
                if 'somenumeric' in tags and not '-' in word and not ',' in word:
                    oddsofreview += 1

            if (oddsofreview > 1 and linecount > 1) or oddsofreview > 2:
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

                    if numericyet and 'wordcount' in tags and (nextwordctr < len(taglist.stringseq)):
                        addtonext = ' '.join(taglist.stringseq[nextwordctr : ])
                        break


                # if this line doesn't end with a word count, and the next one does?
                # probably a continuation

                if len(citationbits) > 0 and not wordcountregex.fullmatch(citationbits[-1]):
                    if linecount < (len(lines) - 1):
                        wordsinnextline = lines[linecount + 1].strip().split()
                        if len(wordsinnextline) > 0 and wordcountregex.fullmatch(wordsinnextline[-1]):
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

    print(trailingbibs)

    return allquotes















# -*- coding: utf-8 -*-
# brd_bookmaker.py

# Extracts Book objects from the Book Review Digest.

# The general strategy is to loop through pages, looking for citations:
# groups of lines that

#    1) Begin with a capitalized word, followed by a comma,
#    2) and end with a "price," which might involve patterns
#       like $1.50 or 50c. or £2

# Once we find citations, we turn the lines between citations into
# Book objects.

import os, sys, re
from difflib import SequenceMatcher
import lexparse

valid_prices = {"81": 1.00, "81.50": 1.50, "81.25": 1.25, "81": 1.0, "82": 2.0, "83": 3.0, "81.75": 1.75, "82.50": 2.50, "81.35": 1.35, '81.85': 1.85, '81.95': 1.95, '81.45': 1.45, '83.50': 3.50, '85': 5.0, '84': 4.0}

hyphenregex = re.compile('.?[0-9]{1,2}[-—~]+[0-9]{3,7}.?')

def match_strings(stringA, stringB):
    m = SequenceMatcher(None, stringA, stringB)

    match = m.quick_ratio()

    if match > 0.7:
        match = m.ratio()

    return match

def percent_upper(astring):
    uppercount = 0
    for character in astring:
        if character.isupper():
            uppercount += 1
    denom = len(astring)
    if denom < 1:
        denom = 1
    return uppercount / denom

def aggressivepricetranslate(astring):
    astring = astring.replace('I', '1').replace('O', '0')
    if len(astring) > 1 and astring[0] == 'J':
        astring = astring[1:]
    return pricetranslate(astring)

def pricetranslate(astring):
    digits = ''
    decimalused = False

    for char in astring:
        if char.isdigit():
            digits = digits + char
        elif char == '.' and not decimalused:
            digits = digits + char
            decimalused = True
        elif char == 'i' and not decimalused:
            digits = digits + '1'
        elif char == 'c' and len(digits) > 1:
            digits = '0.' + digits
        else:
            continue

    if len(digits) > 0:
        try:
            price = float(digits)
        except:
            price = 0.0
    else:
        price = 0.0

    if price > 49 and len(digits) > 1 and '.' in digits and (digits[0] == '5' or digits[0] == '8'):
        try:
            price = float(digits[1:])
        except:
            price = 0.0

    if price > 99:
        price = 0.0

    return price

def numcaps(word):
    capcount = 0
    for char in word:
        if char.isupper():
            capcount += 1
        elif not char.isalpha():
            capcount += 1
    return capcount

class Book:

    # A Book possesses a Citation and
    # a sequence of lines associated
    # with reviews.

    def __init__(self, cite, linelist):

        self.thecitation = cite
        self.reviewlines = linelist
        self.author = cite.author
        self.title = cite.title
        self.price = cite.price
        self.publisher = cite.publisher
        self.pagenum = cite.pagenum

        # Note that we give the book a pagenumber corresponding to the page
        # where its citation ended.

class Citation:

    # A Citation should have an author and a title.
    # It may also have a price, and a publisher.
    # The publisher is liable to be everything
    # after the title that isn't a number.

    # The "pagenum" of the citation is the page of
    # BRD where the citation occurred (specifically,
    # the page where it ends.)

    def __init__(self, linelist, rule_list, textpage):
        self.pagenum = textpage

        alltuples = []
        for line in linelist:
            tokens = line.strip().split()
            if len(tokens) < 1:
                continue

            taglist = lexparse.apply_rule_list(rule_list, tokens)
            for astring, tags in zip(taglist.stringseq, taglist.tagseq):
                alltuples.append((astring, tags))

        titlestart = False
        titledone = False
        authordone = False
        authorstop = False
        dollarpricefound = False

        # The underlying logic here is elegant. We take words up to the first
        # full stop as the "author." From there to the next full stop is
        # the "title." Except, well, in cases of initials.
        # Since "Adams, B. V." has two periods, the rule is that we need
        # a non-fullstopped word or a word of more than three characters to trigger
        # 'title."

        # To implement that we need two flags:
        #   authorstop -- we have reached a full stop
        #   authordone -- we also hit a subsequent word that lacks a period
        #                 or is more than three chars long

        title = []
        author = []
        price = 0
        publisher = []
        tokenssincenumpages = 3

        for word, tags in alltuples:

            tokenssincenumpages += 1

            if authorstop and not authordone:
                if word.startswith('eds.') or word.startswith('pseud.'):
                    author.append(word)
                elif len(word) > 1 and numcaps(word) / len(word) < 1:
                    authordone = True
                    if word[0].isupper():
                        titlestart = True
                        title.append(word)
                else:
                    author.append(word)

            elif not authordone:
                author.append(word)
                if 'fullstop' in tags:
                    authorstop = True
                elif len(word) > 1 and numcaps(word) / len(word) < 0.6:
                    authorstop = True

            elif not titledone:

                if word[0].isupper():
                    titlestart = True

                if titlestart and 'fullstop' in tags:
                    titledone = True

                if titlestart and 'dollarprice' in tags and not 'numpages' in tags:
                    price = pricetranslate(word)
                    if '$' in word:
                        dollarpricefound = True
                    titledone = True

                if titlestart and 'numpages' in tags:
                    titledone = True
                    publisher.append(word)
                    tokenssincenumpages = 0

                else:
                    title.append(word)

            else:
                if titlestart and 'numpages' in tags:
                    publisher.append(word)
                    tokenssincenumpages = 0

                elif tokenssincenumpages < 3 and 'somenumeric' in tags:
                    if '$' in word:
                        dollarpricefound = True
                    price = aggressivepricetranslate(word)

                elif 'dollarprice' in tags:
                    tryprice = pricetranslate(word)
                    if not dollarpricefound:
                        price = tryprice
                    if '$' in word:
                        dollarpricefound = True
                elif 'centprice' in tags and not dollarpricefound:
                    price = pricetranslate(word)
                elif word.strip("'‘’*t") in valid_prices and not dollarpricefound:
                    price = valid_prices[word.strip("'‘’*t")]
                else:
                    publisher.append(word)

        self.author = ' '.join(author)
        self.title = ' '.join(title)
        self.publisher = ' '.join(publisher)
        self.price = price

def get_books(pagelist, publishers):

    lexical_patterns = [('numeric', '.?[0-9]{1,7}.?[0-9]*[,.:=]?'), \
    ('genreword', {'reviewed', 'by', 'review.', 'review', 'by,',
        'article.', 'article', 'article-non', 'lit.', 'non-lit.',
        'poem.', 'fict.', 'fiction', 'fict', 'fiction.', 'poem'}),
    ('openparen', '\(.*'),
    ('closeparen', '.*\)'),
    ('fullstop', '\S+[\.\?!]'),
    ('commastop', '.*\,'),
    ('startdash', '—.*'),
    ('numeric', {'I:', 'II:', 'III:', 'IV:'}),
    ('titlecase', '[A-Z].*'),
    ('monthabbrev', {'Ja', 'F', 'Mr', 'Ap', 'My', 'Je', 'Jl', 'Ag', 'S', 'O', 'N', 'D'}),
    ('lineendingyear', '[\'"•■]\d+'),
    ('volandpgrange', '[0-9]+[:][0-9-]+'),
    ('somenumeric', '.?.?.?[0-9]{1,7}.?.?[0-9]*.?'),
    ('allcaps', '[[A-Z\'\,\‘\.\-:;]*[A-Z]{2,}[A-Z\'\,\‘\.\:;]*'),
    ('dollarprice', '.{0,2}[$\"\'\“].?.?[0-9]{1,7}.?[0-9]*[,.:=]?'),
    ('centprice', '.?.?[0-9]{1,7}.?[0-9]*c+[,.:=]?'),
    ('hyphennumber', '.?[0-9]{1,2}[-—~]+[0-9]{3,7}.?'),
    ('openquote', '[\"\'“‘]+\S*'),
    ('deweydecimal', '[0-9]{3}[.][0-9-]+'),
    ('numpages', '\d{2,5}p')
    ]

    rule_list = lexparse.patterns2rules(lexical_patterns)

    # Our strategy is to find pairs of lines that bookend a citation. A
    # citation and the lines that follow it (before the next citation)
    # is going to count as an Author.

    # A citation starts with a line whose first word is either capitalized and
    # followed by a comma, or all uppercase and longer than three characters.
    # It should be alphabetically later than the last author-name. Exceptions
    # are flagged.

    # A citation ends with a line (up to five lines later) that contains
    # $ + number or number + c, or number containing a hyphen, or that ends
    # with a publisher.

    # We create a list of author_names as well as a list of Author objects.

    author_errors = []
    books = []

    # We keep track of the last author name we've seen; it's going to be
    # the name that governs the lines we are currently examining.

    last_author_name = ''

    textpage = 1

    reviewlines = []
    citation_started = False
    citation_finished = False

    citationlines = []
    governing_citation = Citation(['Anonymous. My book. $1.00. Macmillan.'], rule_list, textpage)
    aligned = 0

    for pagenum, page in enumerate(pagelist):

        for linenum, line in enumerate(page):

            line = line.strip()

            this_line_is_new_citation = False

            # Line numbers are only relevant in guiding us to ignore the running header,
            # and to update the page number. This will be imperfect, because OCR,
            # but that's okay. If we get four successive pages that increment each
            # other as they should (10, 11, 12, 13, ...), we say that enough have been aligned to
            # override checking and just keep adding one per page.

            if aligned >= 4 and linenum == 0:
                textpage += 1

            if linenum < 4:
                thematch = match_strings('BOOK REVIEW DIGEST', line)
                if thematch > 0.8 and len(line) > 7:
                    wordsinline = line.split()
                    if len(wordsinline) > 3 and wordsinline[0].isdigit():
                        pagenum = int(wordsinline[0])
                    elif len(wordsinline) > 3 and wordsinline[-1].isdigit():
                        pagenum = int(wordsinline[-1])

                    if textpage + 1 == pagenum:
                        aligned += 1
                        textpage = pagenum
                    elif pagenum < 20:
                        textpage = pagenum

                    continue
                    # skip this line

                if len(line) > 15:
                    thetail = line[-11: ]
                    thematch = match_strings('—Continued.', thetail)
                    if thematch > 0.75:
                        continue

                if line.isdigit() and aligned < 4:
                    try:
                        newtextpage = int(line)
                        if textpage + 1 == newtextpage:
                            aligned += 1
                        else:
                            aligned = 0
                        textpage = newtextpage
                    except:
                        textpage += 1

                elif len(line) > 12 and line[-2: ].isdigit() and aligned < 4:
                    words = line.split()
                    if words[-1].isdigit():
                        pagenumpart = words[-1]
                        try:
                            newtextpage = int(pagenumpart)
                            if textpage + 1 == newtextpage:
                                aligned += 1
                            else:
                                aligned = 0
                            textpage = newtextpage
                        except:
                            textpage += 1

                elif len(line) > 12 and line[0: 2].isdigit() and aligned < 4:
                    words = line.split()
                    if words[0].isdigit():
                        pagenumpart = words[0]
                        try:
                            newtextpage = int(pagenumpart)
                            if textpage + 1 == newtextpage:
                                aligned += 1
                            else:
                                aligned = 0
                            textpage = newtextpage
                        except:
                            textpage += 1

            if line.startswith('Figures in parenth'):
                continue

            tokens = line.split()
            if len(tokens) < 1:
                continue

            # There are things that look like the beginning of a citation but
            # are actually cross-references

            if "See" in line:
                skepticalofcitestart = True
            else:
                skepticalofcitestart = False

            nextline = linenum + 1

            if nextline < len(page) and "See" in page[nextline]:
                skepticalofcitestart = True

            cannotcitestart = False

            if skepticalofcitestart and linenum + 5 < len(page):
                for lookforward in range(1, 5):
                    futureline = page[linenum + lookforward]
                    if percent_upper(futureline) > .3:
                        cannotcitestart = True

            taglist = lexparse.apply_rule_list(rule_list, tokens)

            firstword = taglist.stringseq[0]
            firsttagset = taglist.tagseq[0]

            cluescitationahead = 0

            distancetolook = 6

            if (len(page) - linenum) < distancetolook:
                distancetolook = len(page) - linenum

            if 'allcaps' in firsttagset and len(firstword) > 2 and distancetolook > 1:
                for lookforward in range(1, distancetolook):
                    futureline = page[linenum + lookforward]
                    if '$' in futureline or "ed." in futureline:
                        cluescitationahead += 1
                    if cluescitationahead > 0:
                        futuretokens = futureline.split()
                        for t in futuretokens:
                            if hyphenregex.fullmatch(t):
                                cluescitationahead += 1

            if not citation_started and not cannotcitestart:

                allcapcount = 0
                for tags in taglist.tagseq:
                    if 'allcaps' in tags:
                        allcapcount += 1

                lineuppercasepct = percent_upper(line)

                if (allcapcount > 0 and lineuppercasepct > 0.1 and len(line) > 9) or (lineuppercasepct > 0.6 and len(line) > 9) or (allcapcount > 0 and cluescitationahead > 0 and len(line) > 9):

                    percentageupper = percent_upper(firstword)
                    if len(line) > 15:
                        pctupin15 = percent_upper(line[0: 15])
                    else:
                        pctupin15 = 0

                    if 'allcaps' in firsttagset and len(firstword) > 2 and cluescitationahead > 0:
                        this_line_is_new_citation = True
                    elif lineuppercasepct > 0.72 and len(line) > 14:
                        this_line_is_new_citation = True
                    elif pctupin15 > .35 and ('$' in line or cluescitationahead > 1) and len(reviewlines) > 3:
                        this_line_is_new_citation = True
                    elif percentageupper > 0.7 and len(firstword) > 4 and allcapcount > 2:
                        this_line_is_new_citation = True
                    elif pctupin15 > 0.65:
                        this_line_is_new_citation = True
                    else:
                        reviewlines.append(line)

                else:
                    reviewlines.append(line)

                if this_line_is_new_citation:
                    # a new citation has begun
                    citation_finished = False

                    citationlines = []

                    for string, tags in zip(taglist.stringseq, taglist.tagseq):
                        if 'dollarprice' in tags or 'centprice' in tags:
                            # note that our conditions for ending a citation with the first
                            # line are more stringent than they will be from the second onward
                            citation_finished = True
                            break

            elif not citation_started and cannotcitestart:
                reviewlines.append(line)

            else:
                # if a citation has been started, let's see if we should end it

                for string, tags in zip(taglist.stringseq, taglist.tagseq):
                    if 'dollarprice' in tags or 'centprice' in tags or 'hyphennumber' in tags or 'deweydecimal' in tags:
                        # more conditions can end a citation now
                        citation_finished = True
                        break

                if len(taglist.stringseq) > 1 and taglist.stringseq[-1].strip('.') in publishers:
                    # sometimes there's no price and the publisher's name is the only clue
                    # that the citation is finished
                    citation_finished = True

                if len(citationlines) > 2 and len(taglist.tagseq) > 1 and 'somenumeric' in taglist.tagseq[0]:
                    try:
                        deweydecimal = float(taglist.stringseq[0])
                        if deweydecimal > 99:
                            citation_finished = True
                    except:
                        pass

            if this_line_is_new_citation or citation_started:
                citationlines.append(line)
                citation_started = True
                this_line_is_new_citation = False

            if citation_finished:
                # we have concluded a new citation
                # first, make the last citation into a book:

                thisbook = Book(governing_citation, reviewlines)
                books.append(thisbook)

                # initialize reviewlines, and create a new citation
                reviewlines = []
                citation_started = False
                citation_finished = False
                # we finished that citation, started a new one

                governing_citation = Citation(citationlines, rule_list, textpage)
                citationlines = []

                new_author = governing_citation.author
                if new_author < last_author_name:
                    author_errors.append((textpage, last_author_name, new_author))
                last_author_name = new_author

            elif len(citationlines) > 8:
                # this is too many lines, and we were probably in error to have
                # started the citation, so put those lines back in reviewlines.
                # This is esp. likely to happen at the top of a page, when
                # an entry is "continued."

                reviewlines.extend(citationlines)
                citationlines = []
                citation_started = False

            elif len(citationlines) > 2:
                lineuppercasepct = percent_upper(line)
                lastuppercasepct = percent_upper(citationlines[-2])

                if lineuppercasepct > .45 and cluescitationahead > 0 and len(line) > 12 and lastuppercasepct < .45:
                    # we started a citation in error two or more lines back; this is the actual
                    # citation start
                    # notice that we check the pct uppercase of last line to make sure this isn't
                    # just a long multiline author name!

                    # discarded = citationlines[0: -1]
                    # for d in discarded:
                    #     print(d)
                    citationlines = [citationlines[-1]]

    return books, author_errors


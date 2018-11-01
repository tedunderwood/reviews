# brd_bookmaker.py

# Extracts Book objects from the Book Review Digest.

# The general strategy is to loop through pages, looking for citations:
# groups of lines that

#    1) Begin with a capitalized word, followed by a comma,
#    2) and end with a "price," which might involve patterns
#       like $1.50 or 50c. or £2

# Once we find citations, we turn the lines between citations into
# Book objects.

import os, sys
from difflib import SequenceMatcher
import lexparse

def match_strings(stringA, stringB):
    m = SequenceMatcher(None, stringA, stringB)
    match = m.quick_ratio()

    if match > 0.7:
        match = m.ratio()

    return match

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

    return price

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

        titledone = False
        authordone = False
        authorstop = False

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

        for word, tags in alltuples:

            if authorstop and not authordone:
                if len(word) > 3:
                    authordone = True
                elif 'fullstop' not in tags:
                    authordone = True

            if not authordone:
                author.append(word)
                if 'fullstop' in tags:
                    authorstop = True
                if authorstop and len(word) > 2:
                    authordone = True
                    # because that wasn't an initial

            elif not titledone:
                title.append(word)
                if 'fullstop' in tags:
                    titledone = True

            else:
                if 'dollarprice' in tags:
                    price = pricetranslate(word)
                elif 'centprice' in tags:
                    price = pricetranslate(word)
                else:
                    publisher.append(word)

        self.author = ' '.join(author)
        self.title = ' '.join(title)
        self.publisher = ' '.join(publisher)
        self.price = price

def get_books(pagelist):
    global publishers

    lexical_patterns = [('numeric', '.?[0-9]{1,7}.?[0-9]*[,.:=]?'), \
    ('genreword', {'reviewed', 'by', 'review.', 'review', 'by,',
        'article.', 'article', 'article-non', 'lit.', 'non-lit.',
        'poem.', 'fict.', 'fiction', 'fict', 'fiction.', 'poem'}),
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
    ('hyphennumber', '[0-9]*[-—]+[0-9]*[,.:=]?'),
    ('openquote', '[\"\'“‘]+\S*')
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
    citationlines = []
    governing_citation = Citation(['Anonymous. My book. $1.00. Macmillan.'], rule_list, textpage)
    aligned = 0

    for pagenum, page in enumerate(pagelist):

        for linenum, line in enumerate(page):

            # Line numbers are only relevant in guiding us to ignore the running header,
            # and to update the page number. This will be imperfect, because OCR,
            # but that's okay. If we get four successive pages that increment each
            # other as they should (10, 11, 12, 13, ...), we say that enough have been aligned to
            # override checking and just keep adding one per page.

            if aligned >= 4 and linenum == 0:
                textpage += 1

            if linenum < 4:
                thematch = match_strings('BOOK REVIEW DIGEST', line)
                if thematch > 0.8:
                    continue
                    # skip this line

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

            tokens = line.strip().split()
            if len(tokens) < 1:
                continue

            taglist = lexparse.apply_rule_list(rule_list, tokens)

            if not citation_started:
                firstword = taglist.stringseq[0]
                firsttagset = taglist.tagseq[0]
                if 'titlecase' in firsttagset and 'commastop' in firsttagset:
                    citation_started = True
                elif 'allcaps' in firsttagset and len(firstword) > 3:
                    citation_started = True
                else:
                    reviewlines.append(line)

                if citation_started:
                    # a new citation has begun
                    citationlines = []
                    citationlines.append(line)

            else:
                # if a citation has been started, let's see if we should end it

                for string, tags in zip(taglist.stringseq, taglist.tagseq):
                    if 'dollarprice' in tags or 'centprice' in tags or 'hyphennumber' in tags:
                        # we have concluded a new citation
                        # so first, make the last citation into a book:

                        thisbook = Book(governing_citation, reviewlines)
                        books.append(thisbook)

                        # initialize reviewlines, and create a new citation
                        reviewlines = []
                        citationlines.append(line)
                        citation_started = False
                        # we finished that citation

                        governing_citation = Citation(citationlines, rule_list, textpage)
                        citationlines = []

                        new_author = governing_citation.author
                        if new_author < last_author_name:
                            author_errors.append((textpage, last_author_name, new_author))
                        last_author_name = new_author

                        # we ended the accumulation of lines, and formed a new
                        # governing_citation, so

                        break

                if len(citationlines) > 5:
                    # this is too many lines, and we were probably in error to have
                    # started the citation, so put those lines back in reviewlines.
                    # This is esp. likely to happen at the top of a page, when
                    # an entry is "continued."

                    reviewlines.extend(citationlines)
                    citationlines = []
                    citation_started = False


                if citation_started:
                    # we didn't find any reason to end the citation
                    citationlines.append(line)


    return books, author_errors


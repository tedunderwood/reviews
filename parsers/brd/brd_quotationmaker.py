# brd_quotationmaker.py

# This module accepts a list of Book objects,
# and divides them into Quotations.

# As often with Python, it may make sense to start reading from the
# bottom of the script, and move up.

import lexparse
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
    # (when available).

    def __init__(self, book, review, sentiment, thequote):

        self.attributes = dict()
        self.attributes['group_tag'] = group_tag
        self.attributes['author_name'] = author_name
        self.tagseq = []
        self.stringseq = []

        for astring, tagset in tuples:
            self.tagseq.append(tagset)
            self.stringseq.append(astring)

        self.parts = dict()
        self.length = len(self.stringseq)

    def is_assigned_to_part(self, index):
        for partname, part in self.parts.items():
            if index >= part['startposition'] and index < part['endposition']:
                return partname

        # or, if no part matched
        return False

    def add_attribute(self, attribute_name, attribute_value):
        ''' This is extremely simple. Attributes are just
        basically a dictionary possessed by the Citation.'''

        self.attributes[attribute_name] = attribute_value

    def add_part(self, partname, start, end):

        # First we check for a couple of odd possibilities; they're not
        # exactly fatal errors, and might be things I want to permit, but
        # I haven't planned to do them and I want to know if they're
        # happening by accident.

        # a) reassigning a part
        if partname in self.parts:
            print('You reassigned an existing part name.')

        # b) creating a part that contains tokens already assigned to another
        overlap = False
        for i in range(start, end):
            if self.is_assigned_to_part(i):
                overlap = True
                break
        if overlap:
            print('You created two overlapping parts.')
            print(self.stringseq)

        # c) fatal errors
        if start > end:
            print('Part start > end: ' + str(start) + "  " + str(end))
            print(partname)
            print(self.stringseq)
            sys.exit(0)

        if start < 0 or end > self.length:
            print('Index error in citation: ' + str(start) + "  " + str(end))
            print(self.length)
            print(self.stringseq)
            print(partname)

            sys.exit(0)

        # Done with error checking. Do the job

        self.parts[partname] = dict()
        self.parts[partname]['startposition'] = start
        self.parts[partname]['endposition'] = end

        stringvalue = ' '.join(self.stringseq[start: end])
        self.parts[partname]['stringvalue'] = stringvalue

    def get_part(self, partname):
        if partname not in self.parts:
            return ''
        else:
            return self.parts[partname]['stringvalue']

    def hastag(self, index, tagtocheck):

        if index < 0 or index > (self.length - 1):
            # index error, technically, but
            # this class is written to tolerate
            # index error
            return False
        elif tagtocheck in self.tagseq[index]:
            return True
        else:
            return False

    def is_in_part(self, index, part):
        if part not in self.parts:
            return False
        else:
            start = self.parts[part]['startposition']
            end = self.parts[part]['endposition']
            if index >= start and index < end:
                return True
            else:
                return False

    def locs_between(self, part1, part2):
        '''
        Returns the start (inclusive) and end (exclusive)
        for the range of positions between part1 and part2,
        assuming both parts present and part1 precedes
        part 2 without overlap.
        '''

        if part1 not in self.parts:
            return 0, 0
        elif part2 not in self.parts:
            return 0, 0
        else:
            end1 = self.parts[part1]['endposition']
            start2 = self.parts[part2]['startposition']
            if end1 > start2:
                return 0, 0
            else:
                return end1, start2

    def startloc(self, part):
        if part not in self.parts:
            return 0
        else:
            return self.parts[part]['startposition']

    def unassigned_intro(self):
        '''
        Starts at zero and keeps counting until it
        reaches a position assigned to a part.
        '''

        for i in range(self.length):
            if self.is_assigned_to_part(i):
                break

        return i

    def enumerate_reversed_tags(self):

        for idx in reversed(range(len(self.tagseq))):
            yield idx, self.tagseq[idx]

def writegroup(taggedlist):
    ''' Was used for debugging,
    now deactivated.'''
    outlines = []
    for astring, tags in zip(taggedlist.stringseq, taggedlist.tagseq):
        outlines.append(astring)
        if 'EOL' in tags:
            outlines.append('>\n')

    with open('taggedlists.txt', mode = 'a', encoding = 'utf-8') as f:
        f.write(' '.join(outlines))
        f.write('\nNEW LIST\n')


def divide_into_quotations(booklist):
    lexical_patterns = [('numeric', '.?[0-9]{1,7}.?[0-9]*[,.:=]?'), \
    ('reviewword', reviewwords),
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
    ('openquote', '[\"\'“‘]+\S*)'),
    ('plusorminus', '[\+\-\—]+')
    ]

    for book in booklist:
        lines = book.reviewlines

        allquotes = []
        accumulated = []
        citationcount = 0

        for line in lines:
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

            if "—" in line:
                parts = line.split('—')
                possiblename = parts[-1]
                if len(possiblename) > 3:
                    matched = False

                    for review in reviewnames:
                        match = match_strings(possiblename, review)
                        if match > 0.9:
                            accumulated.append(parts[0])
                            # add the part before the review name
                            sentiment = ''
                            cite = ''
                            citationcount += 1
                            quote = Quotation(book, review, sentiment, cite, accumulated)
                            allquotes.append(quote)
                            accumulated = []
                            matched = True
                            break

                    if matched:
                        continue


            tokens = line.strip().split()
            if len(tokens) < 1:
                continue

            taglist = lexparse.apply_rule_list(rule_list, tokens)

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
                if 'somenumeric' in tags:
                    oddsofreview += 1

            if oddsofreview > 1:
                sentimentbits = []

                numericyet = False
                publisherbits = []
                citationbits = []

                for word, tags in zip(taglist.stringseq, taglist.tagseq):
                    if word == '+':
                        sentimentbits.append('+')
                        continue
                    if word == '-' or word == '—' or word == '—-':
                        sentimentbits.append('-')
                        continue
                    if word == '+-' or word == '+—':
                        sentimentbits.append('+')
                        sentimentbits.append('-')
                        continue
                    if word == '-+' or word == "—+":
                        sentimentbits.append('-')
                        sentimentbits.append('+')
                        continue

                    if 'somenumeric' in tags:
                        numericyet = True

                    if not numericyet:
                        publisherbits.append(word)
                    else:
                        citationbits.append(word)

                sentiment = ' '.join(sentimentbits)
                review = ' '.join(publisherbits)
                cite = ' '.join(citationbits)
                citationcount += 1

                quote = Quotation(book, review, sentiment, cite, accumulated)
                accumulated = []

            else:
                # odds of review 1 or less
                accumulated.append(line)


    return allquotes















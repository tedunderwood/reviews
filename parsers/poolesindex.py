#!/usr/bin/python

# poolesindex.py

# index-specific rules and functions
# for parsing Poole's Index to Periodical
# Literature

# lexical rules are 2-tuples, where the
# first element is a tag, and the second is
# a pattern; patterns can be either regexen,
# or sets of matching strings

import re, sys, csv, glob
import lexparse

from difflib import SequenceMatcher

# Let's read in abbreviations. We need a list of
# full journal names, but also a list of all the tokens
# that could appear in a name. In both cases, we want to
# permit easy errors like dropping a period.

all_journal_tokens = set()
all_journal_titles = set()

with open('../pooles/abbreviations.tsv', encoding = 'utf-8') as f:
    reader = csv.DictReader(f, delimiter = '\t')
    for row in reader:
        abbrev = row['abbreviation']
        all_journal_titles.add(abbrev)
        all_journal_titles.add(abbrev.replace('.', ''))
        all_journal_titles.add(abbrev + ',')
        tokens = abbrev.split()
        for t in tokens:
            all_journal_tokens.add(t)
            all_journal_tokens.add(t.replace('.', ''))

lexical_patterns = [('numeric', '.?[0-9]{1,7}.?[0-9]*[,.:=]?'), \
    ('samearticle', {'Same', 'art.', 'same', 'art', 'Snme', 'Art.'}), \
    ('newseries', {'n.s.', 'n.', 's.', 'n', 's'}), \
    ('openparen', '\(.*'),
    ('closeparen', '.*\)'),
    ('fullstop', '.*\.'),
    ('startdash', '—.*'),
    ('numeric', {'I:', 'II:', 'III:', 'IV:'}),
    ('titlecase', '[A-Z].*')]

class Citation:

    # A list of strings, paired with lexical tags, that can
    # also acquire named parts.

    # A "part" is a consecutive sequence of strings in the
    # list of strings. Known part names:
    #    'volandpgnums'
    #    'reviewauthor'
    #    'journal'
    #    'title'

    # It is initialized with a TaggedList from lexparse module.

    def __init__(self, tagged):

        self.stringseq = tagged.stringseq
        self.tagseq = tagged.tagseq

        self.length = len(self.stringseq)

        self.parts = dict()
        self.subjects = dict()

        # defining zero will come in handy later

    def is_assigned_to_part(self, index):
        for partname, part in self.parts.items():
            if index >= part['startposition'] and index < part['endposition']:
                return partname

        # or, if no part matched
        return False

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

    def set_subject(self, division, label):
        '''
        defines the subject of the article,
        could be either main or subhed
        '''

        self.subjects[division] = label

    def get_subject(self, division):
        if division != 'main' and division != 'subhed':
            print('Illegal division name: ' + division)
            sys.exit(0)
        else:
            return self.subjects[division]

    def get_outrow(self):
        outrow = dict()
        outrow['mainhed'] = self.subjects['main']
        outrow['subhed'] = self.subjects['subhed']
        if 'author' in self.parts:
            outrow['author'] = self.parts['author']['stringvalue']
        else:
            outrow['author'] = ''

        if 'journalname' in self.parts:
            outrow['journalname'] = self.parts['journalname']['stringvalue']
        else:
            outrow['journalname'] = ''

        if 'volandpgnums' in self.parts:
            outrow['volandpg'] = self.parts['volandpgnums']['stringvalue']
        else:
            outrow['volandpg'] = ''

        outrow['fullcite'] = self.stringseq

        return outrow

def divide_into_citations(page):
    '''
    Given a tagged page, go through the whole sequence
    dividing it into citations. We rely on the Poole's convention
    that each citation ends with a pair of numbers. However, since
    there are various exceptions to that rule, we need to be a little
    cautious. For instance, this is a well-formed Poole's citation:

    Same art. Chr. Lit. 11: 105 a, 129 a.

    I don't know what those a's are telling us. But clearly our confidence
    that numeric/alpha boundaries correspond to citation boundaries needs
    to be qualified. One number is enough to flag the beginning of a numeric
    section. But you need more than one alphabetic token, or a capitalized token,
    to signal the start of an alphabetic sequence. And alphabetic tokens that
    are fullstopped should go with the previous citation if not capitalized
    and the preceding number was not fullstopped.
    '''

    # The logic is, iterate through the sequence, finding pairs of
    # alphabetic-sequence followed by numeric-sequence. We'll record
    # start and end points as we hit them. When they don't exist yet,
    # they are None.

    # Initial conditions:

    alphabet_start = 0
    alphabet_end = None
    numeric_start = None
    numeric_end = None

    citation_list = []

    for i in range(page.length):

        end_of_citation = False

        if i == page.length - 1:
            if not alphabet_end:
                alphabet_end = i
            if not numeric_start:
                numeric_start = i
            if not numeric_end:
                numeric_end = i

            end_of_citation = True

        elif not alphabet_end:
            if not page.hastag(i, 'numeric'):
                pass
                # we are in the middle of an alphabetic sequence
                # everything good
            elif page.hastag(i, 'numeric') and page.hastag(i, 'closeparen'):
                pass
                # numbers inside parentheses are often dates
            else:
                # we are in an alphabetic sequence and just reached
                # a numeric token

                alphabet_end = i + 1
                numeric_start = i + 1
                # python logic, sequences are start-inclusive, end-exclusive

        elif alphabet_end and page.hastag(i, 'numeric'):
            # we are in a numeric sequence and this is a number
            # there is no problem, all is well with the world
            pass

        else:
            # We are in a numeric sequence and this is not a number.
            # Has the numeric sequence ended yet?
            # One non-numeric token is not enough to trigger this

            if page.hastag(i, 'titlecase') or page.hastag(i, 'startdash'):
                end_of_citation = True

            elif page.hastag(i - 1, 'fullstop'):
                end_of_citation = True
                # the previous token was fullstopped so
                # it was probably the end

            elif page.hastag(i, 'fullstop') and page.hastag(i - 1, 'numeric'):
                # this is a non-numeric token but it is full stopped and the previous
                # token was numeric and not stopped, so we're going to count this
                # as part of the numeric sequence.
                pass

            elif not page.hastag(i + 1, 'numeric'):
                end_of_citation = True
                # This token is not numeric, neither is the next one,
                # so probably the numeric section is over
            else:
                # the next token is numeric, so relax, we're still in a numeric
                # sequence
                pass

        if end_of_citation:

            numeric_end = i
            if alphabet_start == numeric_end:
                continue

            next_cite = Citation(page.subdivide(alphabet_start, numeric_end))

            relative_num_start = (numeric_start - alphabet_start) - 1
            relative_num_end = numeric_end - alphabet_start

            next_cite.add_part('volandpgnums', relative_num_start, relative_num_end)
            citation_list.append(next_cite)

            alphabet_start = i
            alphabet_end = None
            numeric_start = None
            numeric_end = None

    return citation_list

def parse_citation(cite, startinitial, endinitial):
    '''
    For each citation, this identifies author and journal parts.
    '''

    authorflag = False
    authend = 0

    for i in range(cite.length):
        if cite.hastag(i, 'openparen'):
            authorflag = True
            authstart = i

        if cite.hastag(i, 'closeparen'):
            authend = i + 1
            break
            # Note the effect of this break. It means that if there are two
            # parenthetical passages in a citation, we only take the *first*
            # one as the author. That's an intended effect. Parentheses can
            # also occur within journal names.

    if authorflag and authend > 0:
        cite.add_part('author', authstart, authend)

    if authorflag:
        # Everything between the author and the vol number is the journal title.

        journalstart, journalend = cite.locs_between('author', 'volandpgnums')
        if journalend > journalstart:
            cite.add_part('journalname', journalstart, journalend)

    else:
        # we're going to look for a journal title
        # by moving backward in the citation,
        # being increasingly skeptical
        startnumeric = cite.startloc('volandpgnums')
        beforenumeric = startnumeric - 1
        if beforenumeric < 0:
            pass
        else:
            maxreach = startnumeric - 6
            if maxreach < -1:
                maxreach = -1

            titleparts = []
            idx = -2
            for idx in range(beforenumeric, maxreach, -1):
                if idx == beforenumeric:
                    titleparts.append(cite.stringseq[idx])
                elif idx == (beforenumeric - 1):
                    possible = cite.stringseq[idx]
                    if possible in all_journal_tokens:
                        titleparts.append(possible)
                    else:
                        break
                else:
                    possible = cite.stringseq[idx]
                    possible_title = possible + ' ' + ' '.join(list(reversed(titleparts)))
                    if possible_title in all_journal_titles:
                        titleparts.append(possible)
                    elif possible_title.strip('. ns,') in all_journal_titles:
                        titleparts.append(possible)
                    else:
                        break

            if idx >= -1 and beforenumeric > idx:
                cite.add_part('journalname', idx + 1, beforenumeric + 1)

    ## Okay, now we have tagged all parts. Things not yet
    ## tagged are the intro.

    endofintro = cite.unassigned_intro()
    cite.add_part('intro', 0, endofintro)

    apparent_header = cite.get_part('intro')
    if len(apparent_header) > 0:
        thisinitial = apparent_header[0].lower()
    else:
        thisinitial = '.'

    matcher = SequenceMatcher(None, apparent_header, 'Same art.')
    is_same_article = matcher.ratio()

    if cite.hastag(0, 'startdash'):
        cite.set_subject('main', '<headless 1>')
        cite.set_subject('subhed', apparent_header)
    elif cite.hastag(0, 'openparen'):
        cite.set_subject('main', '<headless 2>')
        cite.set_subject('subhed', apparent_header)
    elif cite.hastag(0, 'samearticle') and cite.hastag(1, 'samearticle'):
        cite.set_subject('main', '<headless 3>')
        cite.set_subject('subhed', apparent_header)
    elif thisinitial < startinitial or thisinitial > endinitial:
        cite.set_subject('main', '<headless 4>')
        cite.set_subject('subhed', apparent_header)
    elif is_same_article > 0.85:
        cite.set_subject('main', '<headless 5>')
        cite.set_subject('subhed', apparent_header)
    else:
        cite.set_subject('main', apparent_header)
        cite.set_subject('subhed', apparent_header)

    # no return needed because citations are mutable and have been mutated

def get_citations(page, rule_list, start_headword, end_headword):
    print()
    print('Next page.')
    tagged_page = lexparse.apply_rule_list(rule_list, page)
    citation_list = divide_into_citations(tagged_page)

    if len(start_headword) < 1:
        startinitial = 'a'
    else:
        startinitial = start_headword[0].lower()

    if len(end_headword) < 1:
        endinitial = 'z'
    else:
        endinitial = end_headword[0].lower()

    for cite in citation_list:
        parse_citation(cite, startinitial, endinitial)

    return citation_list

## MAIN

paths = glob.glob('../pooles/poolesclean*txt')

citations = []
start_headword = ''
end_headword = ''

rule_list = lexparse.patterns2rules(lexical_patterns)

for p in paths:
    with open(p, encoding = 'utf-8') as f:
        filelines = f.readlines()
        page = []
        for fl in filelines:
            fl = fl.replace('.—', '. —')
            fl = fl.replace('—', '— ')
            fl = fl.replace(',', ', ')
            # The point of doing that is to make
            # sure citations get cleanly separated.
            # They often begin with a dash.

            tokens = fl.strip().split()
            if len(tokens) < 1 and len(page) > 0:
                # this is a pagebreak
                citations.extend(get_citations(page, rule_list, start_headword, end_headword))
                page = []
            elif tokens[0] == 'Page' and tokens[1].isnumeric():
                if len(page) > 0:
                    citations.extend(get_citations(page, rule_list, start_headword, end_headword))
                    page = []
                else:
                    pass
            elif len(tokens) < 3:
                page.extend(tokens)
            elif tokens[0].isupper() and (len(tokens[0]) > 2 or tokens[2].isupper()):
                start_headword = tokens[0]
                end_headword = tokens[2]
                page.extend(tokens[3: ])
            else:
                page.extend(tokens)

        if len(page) > 0:
            citations.extend(get_citations(page, rule_list, start_headword, end_headword))

    # Now we assign main subjects.

    current_header = ''
    for cite in citations:
        main_subject = cite.get_subject('main')
        if main_subject.startswith('<head'):
            cite.set_subject('main', current_header)
        else:
            current_header = main_subject

    outpath = p.replace('clean', 'results').replace('.txt', '.tsv')
    columns = ['mainhed', 'subhed', 'author', 'journalname', 'volandpg', 'fullcite']
    with open(outpath, mode = 'w', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, delimiter = '\t', fieldnames = columns)
        writer.writeheader()
        for cite in citations:
            outrow = cite.get_outrow()
            writer.writerow(outrow)






















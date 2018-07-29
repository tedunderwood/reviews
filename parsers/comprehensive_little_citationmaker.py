# comprehensive_little_citationmaker.py

# This module accepts a list of Author objects,
# and divides them into Citations. Then it parses
# the citations.

# Right now I've written code that divides the Authors into Citations.
# I haven't yet written code that parses each Citation into parts.

# As often with Python, it may make sense to start reading from the
# bottom of the script, and move up.

import os, sys
from difflib import SequenceMatcher

class Citation:

    # a citation has an author_name,
    # it has a group_tag such as 'WORKS ABOUT' or 'WORKS BY'
    # and it has a sequence of strings and tagsets

    # as it is parsed, it may also acquire "parts," which
    # are dictionary entries associated with a "partname,"
    # a "startposition" within the citation, and and
    # "endposition" inside the citation.

    def __init__(self, tuples, group_tag, author_name):

        self.group_tag = group_tag
        self.author_name = author_name
        self.tagseq = []
        self.stringseq = []

        for astring, tagset in tuples:
            self.tagseq.append(tagset)
            self.stringseq.append(astring)

        self.parts = dict()

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

def divide_into_citations(tagged_group, group_tag, author_name):

    # we look for a sequence of three triggers to
    # divide citations:
    #   1) an open parenthesis
    #   2) a close parenthesis.
    #   3) a token that contains
    #      digits, ended with an EOL.
    #
    # e.g  (Ap '61) 341-42.

    #   These triggers can be separated by one token
    #   (to allow for ocr errors and odd formats)
    #   but more than one token of separation resets
    #   the counter. It is possible, after all, that
    #   pairs of parentheses will occur within titles, and
    #   we don't want these to falsely trigger division.

    citation_list = []

    tuples_for_next_citation = []
    parenopened = False
    parenclosed = False
    interruptions = 0

    for string, tags in zip(tagged_group.stringseq, tagged_group.tagseq):
        tuples_for_next_citation.append((string, tags))

        if parenclosed and 'EOL' in tags and 'somenumeric' in tags:
            next_citation = Citation(tuples_for_next_citation, group_tag, author_name)
            citation_list.append(next_citation)
            tuples_for_next_citation = []

        elif parenopened and 'closeparen' in tags:
            parenclosed = True
            interruptions = 0

        elif 'openparen' in tags:
            parenopened = True
            if 'closeparen' in tags:
                parenclosed = True
                # it's possible for both to happen at once, like
                # ('44)
            interruptions = 0

        else:
            interruptions += 1
            if interruptions > 1:
                parenopened = False
                parenclosed = False

    if len(tuples_for_next_citation) > 0:
        next_citation = Citation(tuples_for_next_citation, group_tag, author_name)
        citation_list.append(next_citation)

    return citation_list

def subdivide_author(auth, rule_list):
    ''' This function accepts an Author, which contains a list of lines
    paired with group_tags to identify "WORKS BY" or "WORKS ABOUT." *Every* line in a
    WORKS ABOUT section is expected to bear the tag "about."

    First this function turns the lines
    into TaggedLists (a class from the lexparse module.)

    Then it iterates through tuples of the form
            (TaggedList, group_tag)

    and aggregates them into Citations.
    '''

    author_name = auth.name
    rawlines = auth.get_lines()

    last_tag = 'match-any'

    citation_list = []

    tokenchunk = []

    for line, group_tag in rawlines:
        tokens = line.strip().split()

        # what to do with the tokens depends on
        # where we are in a tag sequence

        if last_tag == 'match-any':
            # turn them into a new TaggedList (the first for this author)
            tagged_group = lexparse.apply_rule_list(rule_list, tokens)
            last_tag = group_tag

        elif group_tag == last_tag:
            # group_tag remains the same (WORKS ABOUT or WORKS BY)
            # so just extend the group

            new_group = lexparse.apply_rule_list(rule_list, tokens)
            tagged_group.extend(new_group)

        else:
            # there has been a shift of tag so let's divide the
            # groups

            new_citations = divide_into_citations(tagged_group, last_tag, author_name)
            citation_list.extend(new_citations)

            # and create a new tagged_group
            tagged_group = lexparse.apply_rule_list(rule_list, tokens)

    # when we're done, since there's not a next tag to trigger the
    # division of tagged_group, we have to do it explicitly

    if len(tagged_group) > 0:
        new_citations = divide_into_citations(tagged_group, last_tag, author_name)
        citation_list.extend(new_citations)

    return citation_list

def authors_to_citations(author_list):

    lexical_patterns = [('numeric', '.?[0-9]{1,7}.?[0-9]*[,.:=]?'), \
    ('samearticle', {'Same', 'art.', 'same', 'art', 'Snme', 'Art.'}), \
    ('newseries', {'n.s.', 'n.', 's.', 'n', 's'}), \
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
    ('somenumeric', '\S?\d+\S?'),
    ('allcaps', '[A-Z\']+')
    ]

    rule_list = lexparse.patterns2rules(lexical_patterns)

    for auth in author_list:
        citation_list = subdivide_author(auth, rule_list)

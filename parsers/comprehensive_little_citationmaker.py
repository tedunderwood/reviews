# comprehensive_little_citationmaker.py

# This module accepts a list of Author objects,
# and divides them into Citations. Then it parses
# the citations.

# Right now I've written code that divides the Authors into Citations.
# I haven't yet written code that parses each Citation into parts.

# As often with Python, it may make sense to start reading from the
# bottom of the script, and move up.

import lexparse

class Citation:

    # A citation, like a TaggedList, is basically a sequence of
    # strings paired with an equal-length sequence of tagsets.

    # In addition, a citation can have "parts" and attributes.

    # Parts are subsets of the sequence, represented as
    # dictionary entries associated with a "partname,"
    # a "startposition" within the citation, and an
    # "endposition" inside the citation. Parts also have
    # a 'stringvalue' which is simply the string version of
    # the whole subsequence.

    # Attributes are possessed globally by the citation as a whole.
    # In the *Comprehensive Index to English-Language Little Magazines,*
    # citations always have

    # an author_name: the author entry under which this was found, and

    # a group_tag: which will be "by" if this occurred in WORKS BY, or
    #              "about" if it occurred in WORKS ABOUT.

    # Citations *may* also have a date: the year of publication, if we can
    # infer it.

    def __init__(self, tuples, group_tag, author_name):

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


def divide_into_citations(tagged_group, group_tag, author_name):

    # we look for a sequence of three triggers to
    # divide citations:
    #   1) an open parenthesis
    #   2) a close parenthesis with some numbers attached.
    #   3) a token that contains
    #      digits, ended with a period and/or an EOL.
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

    # writegroup(tagged_group)
    # was used for debugging, now deactivated

    for string, tags in zip(tagged_group.stringseq, tagged_group.tagseq):
        tuples_for_next_citation.append((string, tags))

        if parenclosed and ('fullstop' in tags or 'EOL' in tags) and 'somenumeric' in tags:
            next_citation = Citation(tuples_for_next_citation, group_tag, author_name)
            citation_list.append(next_citation)
            tuples_for_next_citation = []
            parenopened = False
            parenclosed = False
            interruptions = 0
            print('trigger3')

        elif parenopened and 'closeparen' in tags and 'somenumeric' in tags:
            parenclosed = True
            interruptions = 0

        elif 'openparen' in tags:
            parenopened = True
            if 'closeparen' in tags and 'somenumeric' in tags:
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
    print(author_name)
    rawlines = auth.get_lines()

    last_tag = 'match-any'

    citation_list = []

    tokenchunk = []

    tagged_group = 'not yet used'

    for line, group_tag in rawlines:
        tokens = line.strip().split()
        if len(tokens) < 1:
            continue
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
            # and make this tag into the last_tag
            last_tag = group_tag


    # when we're done, since there's not a next tag to trigger the
    # division of tagged_group, we have to do it explicitly

    if type(tagged_group) != str:
        # slightly cheesy way of confirming that it's a TaggedList
        new_citations = divide_into_citations(tagged_group, last_tag, author_name)
        citation_list.extend(new_citations)

    return citation_list

def assign_date(cite):
    ''' In the Comprehensive Index, dates are contained within parentheses
    near the end of the citation.

    So our strategy is going to be to iterate through the citation *starting
    at the end and proceeding in reverse.* We will tag the first closeparen-openparen
    pair we find as the "date-parenthesis." Then, if possible, we will extract
    a year from that citation part.'''

    parenbegun = False
    parenfinished = False

    for index, taglist in cite.enumerate_reversed_tags():

        if 'closeparen' in taglist:
            parenbegun = True
            endposition = index

        if parenbegun and 'openparen' in taglist:
            startposition = index
            parenfinished = True
            break

    if parenfinished:
        cite.add_part('date-parenthesis', startposition, endposition + 1)
        # +1 for the usual Python reason that sequences are start-inclusive
        # and end-exclusive

        last_string = cite.stringseq[endposition]
        number_part = last_string.strip("[]()'")
        try:
            year2digit = int(number_part)
        except:
            year2digit = -1

        if year2digit >= 0 and year2digit < 100:
            date = 1900 + year2digit
            cite.add_attribute('date', date)

def assign_genre(cite):
    ''' Citations in the Comprehensive Index tend to contain a one- or
    two-word phrase defining the "genre" of the piece. Common options
    include 'article.', 'poem.', 'fict.', or 'reviewed by'.

    We want to find this phrase, both in order to identify book reviews
    and in order to identify journal names, which tend to occupy the
    space between the 'genre' and the 'date-parenthesis.'

    We iterate from the end, in reverse order, because we are less likely
    to hit misleading false positives that way. E.g. "reviewed" could
    occur in a title, but it won't occur at the end of a citation.
    '''

    genrebegun = False
    startposition = 0

    for index, taglist in cite.enumerate_reversed_tags():

        if not genrebegun and 'genreword' in taglist:
            genrebegun = True
            endposition = index
        elif 'genreword' in taglist:
            continue
        elif genrebegun and not 'genreword' in taglist:
            # we've reached the end of the genre section
            startposition = index + 1
            break
        else:
            continue

    if genrebegun:
        cite.add_part('genre', startposition, endposition + 1)

def assign_journal(cite):
    '''
    Right now this works very simply. We're going to assume that
    everything between the "genre" phrase and the "date-parenthesis"
    is the journal name. In reality, that won't be true. Often we have
    a situation like

    reviewed by Edwin R. Murrow. Brit. Review, vol. 10 (My '61)

    In that situation the genre phrase is "reviewed by." The space
    between genre phrase and date-parenthesis includes the reviewer's
    name as well as the journal name.

    But the only way we're going to be able to separate reviewers' names
    from journal names is to start by getting a lot of these phrases and
    then identifying the parts at the end that remain the same -- e.g.
    "Brit Review."
    '''

    if 'genre' in cite.parts and 'date-parenthesis' in cite.parts:
        startjournal, endjournal = cite.locs_between('genre', 'date-parenthesis')

        if startjournal > 0 and endjournal > startjournal:
            cite.add_part('journal', startjournal, endjournal)

def assign_subject(cite):
    ''' Our heuristic is that everything before the first string
    identified as another part == 'subject'. Usually this will mean
    everything before the 'genre'.
    '''

    startsubject = 0
    endsubject = cite.unassigned_intro()

    cite.add_part('subject', startsubject, endsubject)

def parse_parts(citation_list):

    for cite in citation_list:

        assign_date(cite)
        assign_genre(cite)
        assign_journal(cite)
        assign_subject(cite)

def authors_to_citations(author_list):

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
    ('somenumeric', '.?[0-9]{1,7}.?.?[0-9]*.?'),
    ('allcaps', '[A-Z\']+')
    ]

    rule_list = lexparse.patterns2rules(lexical_patterns)

    all_parsed_citations = []

    for auth in author_list:
        citation_list = subdivide_author(auth, rule_list)
        parse_parts(citation_list)
        all_parsed_citations.extend(citation_list)

    return all_parsed_citations


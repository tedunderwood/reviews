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

citation_discourse = {'the', 'an', 'in', 'of', 'our', 'for', 'poem', 'review', 'with',
'by', 'is', 'as', 'this', 'is', 'her', 'his', 'new', 'its', 'no', 'one', 'that', 'or', 'if'}

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
    ('commastop', '.*\,'),
    ('startdash', '—.*'),
    ('numeric', {'I:', 'II:', 'III:', 'IV:'}),
    ('titlecase', '[A-Z].*'),
    ('monthabbrev', {'Ja', 'F', 'Mr', 'Ap', 'My', 'Je', 'Jl', 'Ag', 'S', 'O', 'N', 'D'}),
    ('lineendingyear', '[\'"•■]\d+'),
    ('volandpgrange', '[0-9]+[:][0-9-]+')
    ('allcaps', '[A-Z\']+')
    ]

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

def parse_chunk(chunk):
    '''
    Given a chunk of tagged lines, this divides them into citations.
    '''
    citations = []

    tag, entryline = chunk[0]
    the_entry = ' '.join(entryline.stringseq)

    holding = []

    for idx in range(1, len(chunk)):
        tag, line = chunk[idx]
        if tag == 'endcitation':
            holding.append(line)
            citations.append(parse_citation(holding, the_entry))
            holding = []
        else:
            holding.append(line)





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

def is_header(tl):
    '''Accepts a TaggedList (tl) and
    characterizes it as potentially a header.'''

    linelen = tl.length
    if linelen == 1 and tl.hastag(0, 'numeric'):
        return True
    else:
        isheader = True
        for i in range(linelen):
            if not tl.hastag(i, 'allcaps'):
                isheader = False
        return isheader

def is_citation_end(tl):
    linelen = tl.length
    lastidx = linelen - 1
    if lastidx < 0:
        return False
    else:
        if tl.hastag(lastidx, 'lineendingyear'):
            return True
        else:
            return False

def has_citation(tl):
    global all_journal_tokens

    linelen = tl.length
    if linelen < 1:
        return False

    hascitation = False
    suspicious = 0
    for i in range(linelen):
        if tl.hastag(i, 'volandpgrange'):
            hascitation = True
            break
        elif tl.hastag(i, 'numeric'):
            suspicious += 1
        elif tl.hastag(i, 'monthabbrev'):
            suspicious += 0.5
        elif tl.stringseq[i] in all_journal_tokens:
            suspicious += 0.5

    if suspicious > 2 or (suspicious / linelen) > 0.5:
        return True
    else:
        return False

def is_entry(tl):
    global citation_discourse

    linelen = tl.length
    if linelen < 1:
        return False

    suspicious = 0
    if tl.hastag(0, 'commastop'):
        suspicious += 1
    if tl.hastag(linelen - 1, 'closeparen'):
        suspicious += 1
    if tl.stringseq[linelen-1].endswith('ontinued'):
        suspicious += 1

    for i in range(linelen):
        if tl.hastag(i, 'titlecase') or tl.hastag(i, 'openparen'):
            suspicious += 1
        elif tl.stringseq[i] in citation_discourse:
            suspicious -= 1
        elif tl.hastag(i, 'numeric'):
            suspicious -= 1

    if suspicious >= linelen:
        return True
    else:
        return False

## MAIN


rule_list = lexparse.patterns2rules(lexical_patterns)

def parse_pages(pagefiles, rule_list, prev_entry = 'A'):

    for p in pagefiles:
        ## first read in a page and tag all the strings in each line

        with open(p, encoding = 'utf-8') as f:
            filelines = f.readlines()
            tagged_page = []

            for fl in filelines:
                tokens = fl.strip().split()
                if len(tokens) < 1:
                    continue
                else:
                    tagged_line = lexparse.apply_rule_list(rule_list, tokens)
                    tagged_page.append(tagged_line)

        ## now identify the lines themselves as entries or as citations

        linetuples = []
        for index, line in enumerate(tagged_page):
            if index < 2 and is_header(line):
                linetag = 'header'
            elif is_citation_end(line):
                linetag = 'citationend'
            elif has_citation(line):
                linetag = 'citationpart'
            elif is_entry(line):
                linetag = 'entry'
            elif is_all_text(line):
                linetag = 'alltext'
            else:
                linetag = 'ambiguous'

            linetuples.append((linetag, line))


        # Now we organize lines into groups that share an entry.
        # First, use alphabetical sequence to confirm entries. We're going create
        # a list of lines that we think are entries.

        entrypoints = []

        # We're going to rely on the variable prev_entry, inerited from
        # the previous page, to make sure
        # that entries are in alphabetical order. But we also need a
        # way to correct errors if we get off.

        lowerthanprev = 0
        allentries = 1
        # note a bit of additive smoothing
        firstonpage = 'Aa'

        for ltuple in linetuples:
            tag, line = ltuple
            if tag == 'entry':
                firstword = line.stringseq[0]

                if firstonpage == 'Aa':
                    firstonpage = firstword
                    # 'Aa' is just a flag that we haven't taken the firstonpage yet

                allentries += 1
                if firstword < prev_entry:
                    lowerthanprev += 1

        if (lowerthanprev / allentries) > 0.5:
            prev_entry = firstonpage

            # If more than half the entries on the page begin with a word
            # alphabetically earlier than prev_entry, we have gotten out of
            # order, and the prev_entry needs to be reset to the first on page.

        for idx, ltuple in enumerate(linetuples):
            tag, line = ltuple
            firstword = line.stringseq[0]
            if tag == 'entry' and firstword >= prev_entry:
                entrypoints.append(idx)
                prev_entry = firstword
            elif tag == 'alltext' and line.stringseq[0] >= prev_entry:
                for idx2 in range(idx +1, len(linetuples)):
                    tag2, line2 = linetuples[idx2]
                    if tag2 == 'entry' and line2.stringseq[0] >= firstword:
                        entrypoints.append(idx)
                        prev_entry = firstword
                        break
                    elif tag2 == 'entry':
                        break
            else:
                continue

        # okay, now we have a list of lines that we think are entries.
        # we can use that to create chunks of lines that share the same
        # entry

        chunks = []
        for idx, entrypoint in enumerate(entrypoints):
            linenum = entrypoint
            if idx + 1 >= len(entrypoints):
                chunks.append((entrypoint, len(linetuples)))
            else:
                for idx2 in range(idx + 1, len(entrypoints)):
                    linenum2 = entrypoints[idx2]
                    if linenum2 = linenum + 1:
                        # sequential entries should be kept together
                        linenum = linenum2
                    else:
                        # aha, a break
                        chunks.append((entrypoint, linenum2))
                        break

        citations = []
        for chunktuple in chunks:
            startline, stopline = chunktuple
            new_chunk = linetuples[startline: stopline]
            new_citations = parse_chunk(new_chunk)
            citations.extend(new_citations)







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






















# comprehensive_little_citationmaker.py

# This module accepts a list of Author objects,
# and divides them into Citations. Then it parses
# the citations.

import os, sys
from difflib import SequenceMatcher

def subdivide_author(auth, rule_list):
    ''' This function accepts an Author, which contains a list of lines
    paired with tags like "by" or "about." First it turns those lines
    into TaggedLists (a class from the lexparse module.)

    Then it iterates through tuples of the form
            (TaggedList, linetag)

    and aggregates them into Citations.
    '''
    rawlines = auth.get_lines()

    tagged_lines = []

    for line, linetag in rawlines:
        tokens = line.strip().split()

        if len(tokens) < 1:
            continue

        tagged_line = lexparse.apply_rule_list(rule_list, tokens)
        tagged_lines.append((tagged_line, linetag))





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
    ('volandpgrange', '[0-9]+[:][0-9-]+')
    ('allcaps', '[A-Z\']+')
    ]

    rule_list = lexparse.patterns2rules(lexical_patterns)

    for auth in author_list:
        citation_list = subdivide_author(auth, rule_list)

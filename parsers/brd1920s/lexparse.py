import re

# the lex modules contains functions that
# compile lexical rules, paired with tags,
# and then search a list of strings, assigning
# lexical tags to all strings matching
# each tag

# the tagged list can then be passed to
# yacc, which divides it into citations
# and parses the citations

class LexicalRule:
    # An object that, most crucially, has a method
    # *characterizes()* capable of identifying strings that
    # fit the rule

    def __init__(self, tag, pattern):
        '''
        The pattern determines whether strings match the rule;
        if they do, they get tagged with the tag.
        '''

        self.tag = tag

        # Patterns come in two forms. Either they're a regex string
        # or they're a set of possible examples.

        if type(pattern) == set:
            self.matchset = pattern
            self.ruletype = 'set'

        elif type(pattern) == str:
            self.matchset = set()
            self.matchregex = re.compile(pattern)
            self.ruletype = 'regex'

    def characterizes(self, astring):

        if self.ruletype == 'regex':
            if self.matchregex.fullmatch(astring):
                return True
            else:
                return False

        if self.ruletype == 'set':
            if astring in self.matchset:
                return True
            else:
                return False

class TaggedList:
    # Essentially a sequence of strings, where each string
    # is paired with a set of tags. Associated behavior includes
    # ability to divide itself into pieces, and report tags.

    def __init__(self, stringseq, tagseq):

        assert len(stringseq) == len(tagseq)

        if len(stringseq) < 1:
            print('error: empty TaggedList')
            # we cannot have empty TaggedLists
        assert type(stringseq[0]) == str
        assert type(tagseq[0]) == set

        self.stringseq = stringseq
        self.tagseq = tagseq
        self.length = len(stringseq)

    def subdivide(self, start, stop):
        if start < 0 or start >= stop:
            print('error: attempt to create TaggedList with illegal start ' + str(start))
            print('and stop: ' + str(stop))
            return None
        elif stop > len(self.stringseq):
            print('error: TaggedList stop index beyond object limit, at ' + str(stop))
            return None
            # those are error conditions

        return TaggedList(self.stringseq[start: stop], self.tagseq[start: stop])

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

    def extend(self, other_tagged_list):

        for idx, tag in enumerate(other_tagged_list.tagseq):
            self.tagseq.append(tag)
            matching_string = other_tagged_list.stringseq[idx]
            self.stringseq.append(matching_string)

        self.length = len(self.stringseq)


def patterns2rules(patterntuple_list):
    '''
    Converts a list of patterntuples to a list of
    LexicalRules, where a patterntuple is a 2-tuple
    of the form:
    (tag, pattern)
    and "pattern" is either a string that creates
    a regex, or a set of strings.
    '''

    rule_list = []

    for patterntuple in patterntuple_list:
        tag, pattern = patterntuple
        newrule = LexicalRule(tag, pattern)
        rule_list.append(newrule)

    return rule_list

def apply_rule_list(rule_list, string_list):
    '''
    Very simply iterates through a list of strings, trying
    each of the lexical rules in its rule_list parameter,
    creating set of the tags corresponding to
    all the rules that characterize each string, and
    saving those sets in a list which then is paired with
    the strings to create a TaggedList.
    '''

    tag_list = []

    for astring in string_list:
        tagsforthisstring = set()
        for lexrule in rule_list:
            if lexrule.characterizes(astring):
                tagsforthisstring.add(lexrule.tag)

        tag_list.append(tagsforthisstring)

    # the last string in a string_list
    # is always tagged end-of-line

    if len(tag_list) > 0:
        tag_list[-1].add('EOL')

    marked_up = TaggedList(string_list, tag_list)

    return marked_up





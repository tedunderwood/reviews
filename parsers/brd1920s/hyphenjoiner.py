# hyphenjoiner.py

lexicon = set()
with open('../brd/SlimDictionary.txt', encoding = 'utf-8') as f:
    for line in f:
        lexicon.add(line.strip())

def join_hyphens(listoflines):

    listlen = len(listoflines)
    listofwords = []

    for idx, line in enumerate(listoflines):
        newlist = line.split()

        if len(listofwords) > 0 and len(line) > 0:
            lastword = listofwords[-1]
            if lastword.endswith('-') or lastword.endswith('—'):
                if lastword[0].isupper():
                    titlecase = True
                else:
                    titlecase = False

                firstword = newlist[0].lower().strip('.?,!;:)“("')
                lastword = lastword[0:-1].lower().strip('.?,;:!)“("')

                possiblematch = lastword + firstword
                if possiblematch in lexicon:
                    listofwords.pop(-1)
                    newlist.pop(0)
                    listofwords.append(possiblematch)

        listofwords.extend(newlist)

    return ' '.join(listofwords)



import pandas as pd
import numpy as np
from collections import Counter

# This script turns paired text and metadata files into a feature matrix
# that can be used to train a model of "reviews-of-fiction," excluding
# reviews of nonfiction that tend to be mixed in.

infiles = ['tedreviewtexts0to100.txt', 'jessicareviewtexts100to200.txt',
'jessicareviewtexts200to300.txt','jessicareviewtexts300to400.txt',
'tedreviewtexts400to500.txt', 'tedreviewtexts500to600.txt']

metafiles = ['tedreviewmeta0to100.tsv', 'jessicareviewmeta100to200.tsv', 'jessicareviews200to300.tsv',
'jessicareviews300to400.tsv', 'tedreviews400to500.tsv', 'tedreviews500to600.tsv']

# Create a translator that zaps punctuation, turning it into spaces.
# This is a crude approach to tokenizing, but it's esp useful with
# this data because hyphenation is in practice wonky. (Words are
# in particular often glued together with question marks.)

delchars = ''.join(c for c in map(chr, range(256)) if not c.isalpha())
spaces = ' ' * len(delchars)
punct2space = str.maketrans(delchars, spaces)

# THE FOLLOWING SECTION LOADS A LOT OF RULE FILES.
# It's more verbose than necessary because this is old code.
# If you don't want to be bored, skip down to line 89.

rulepath = '/Users/tunder/Dropbox/DataMunging/rulesets/'
delim = '\t'

romannumerals = set()
with open(rulepath + 'romannumerals.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

for line in filelines:
    line = line.rstrip()
    romannumerals.add(line)

lexicon = dict()

with open(rulepath + 'MainDictionary.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

for line in filelines:
    line = line.rstrip()
    fields = line.split(delim)
    englflag = int(fields[1])
    lexicon[fields[0]] = englflag

personalnames = set()
with open(rulepath + 'PersonalNames.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

for line in filelines:
    line = line.rstrip()
    line = line.lower()
    personalnames.add(line)

placenames = set()
with open(rulepath + 'PlaceNames.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

for line in filelines:
    line = line.rstrip()
    line = line.lower()
    placenames.add(line)

correctionrules = dict()

with open(rulepath + 'CorrectionRules.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

for line in filelines:
    line = line.rstrip()
    fields = line.split(delim)
    correctionrules[fields[0]] = fields[1]

variants = dict()
with open(rulepath + 'VariantSpellings.txt', encoding = 'utf-8') as file:
    filelines = file.readlines()

for line in filelines:
    line = line.rstrip()
    fields = line.split(delim)
    variants[fields[0]] = fields[1]

# Create a dictionary of "match quality" codes. These reflect
# the closeness of match between title-author in the review
# metadata and in our HathiTrust fiction database. Poor matches
# can signal that a book isn't actually fiction.

# When we sweep a net through BPO we're going to reject everything
# below matchquality 2.1, but there are a few ringers with lower
# match quality in the training database. It's okay if we give the
# fiction model a slightly exaggerated bias against poor match quality,
# because ultimately we want reviews of fiction that are also correctly
# matched.

matchquality = dict()
for decade in range(1800, 1940, 10):
    df = pd.read_csv('meta/matched_reviews_' + str(decade) + '.tsv', sep = '\t')
    for idx, row in df.iterrows():
        matchquality[str(row.RecordID)] = float(row.matchquality)

def checkEqual3(lst):
   return lst[1:] == lst[:-1]

def line2words(line):
    global punct2space, romannumerals, lexicon, personalnames, placenames, correctionrules, variants

    if pd.isnull(line):
        return []
    line = line.strip().translate(punct2space).lower()
    words = line.split()
    outwords = []
    for w in words:
        if w in romannumerals:
            w = '#romannumeral'
        elif w in personalnames:
            w = '#personalname'
        elif w in placenames:
            w = '#placename'
        elif w.isdigit():
            w = '#arabicnumeral'

        if w in correctionrules:
            w = correctionrules[w]

        if w in variants:
            w = variants[w]

        if w not in lexicon and not w.startswith('#') and len(w) > 1:
            w = '#notenglishword'

        outwords.append(w)

    return outwords

# So, I readily admit that the next section of code is a mess.
# It parses the text file,with sections of metadata and text delimited
# by lines of equals-signs and lines of hyphens.

# It's not the best-structured data in the world; I was compromising
# btw human readability and computer readability. So parsing it becomes
# a bit of a tangle.


genredict = dict()

def parsefile(path, metafile, seqdict):

    global genredict

    metadf = pd.read_csv('processedmeta/' + metafile, sep = '\t', dtype = {'seq': str})
    metadf.set_index('seq', inplace=True)

    grouped = metadf.groupby('RecordID')
    for rec, df in grouped:
        if not checkEqual3(list(df.isfiction)):
            print('Inconsistent: ', rec)

    seq = ''
    record = ''
    valid = True

    with open(path, encoding = 'utf-8') as f:
        meta = False
        for line in f:
            if line.startswith('====='):
                if len(seq) > 1:
                    seqdict[seq] = (valid, checkrecord, thistext)
                meta = True
                seq = ''
                record = ''

            elif line.startswith('-----'):
                meta = False
                thistext = Counter()
                words = line2words(thistitle)
                for w in words:
                    thistext[w] += 1

            elif meta and len(seq) < 1:
                fields = line.strip().split()
                seq = fields[0]
                record = fields[1]
                if seq not in metadf.index:
                    print(seq, record)
                    valid = False
                else:
                    checkrecord = metadf.loc[seq, 'RecordID']
                    thistitle = metadf.loc[seq, 'RecordTitle']
                    genre = metadf.loc[seq, 'isfiction']
                    year = metadf.loc[seq, 'PubYear']
                    genredict[seq] = genre
                    if pd.isnull(year) or int(year) < 1830:
                        genredict[seq] = 'dirty'

                    truthvalues = pd.isnull(checkrecord)
                    if type(truthvalues) == bool and truthvalues:
                        print('null')
                        valid = False
                    else:
                        checkrecord = str(checkrecord)
                        if record != checkrecord:
                            print('False match', checkrecord)
                            valid = False
                        else:
                            valid = True

            elif not meta and len(line) > 1:
                words = line2words(line)
                for w in words:
                    thistext[w] += 1

    return seqdict

# HERE IS WHERE WE ACTUALLY START PARSING.
# sorry, this code is a mess

root = 'processedtexts/'

seqdict = dict()

for textfile, metafile in zip(infiles, metafiles):
    seqdict = parsefile(root + textfile, metafile, seqdict)

allwords = Counter()

print()
print('Summary:')
for seq, v in seqdict.items():
    if genredict[seq] != 'y' and genredict[seq] != 'n':
        continue

    valid, recordid, text = v
    if not valid:
        print(len(text))
    else:
        for word, count in text.items():
            allwords[word] += 1

allwords['voyages'] += 380
allwords['tale'] += 380
allwords['tales'] += 380
allwords['novels'] += 380
allwords['letters'] += 380
allwords['novel'] += 120
allwords['hero'] += 100
allwords['characters'] += 100

# Okay, here are some really baroque details.

# BROADLY, we're going to use 400 features, which are
# the 400 most common words in the dataset. BROADLY.

# In practice, we group a bunch of features into
# hashtagged collective features, like #placename,
# based on a gazetteer of places. I know this strategy
# is not perfect (we don't have all places).

# More importantly, we count #rarewords that aren't in
# the 400 most frequent. We also include #matchquality as
# a feature (see above).

# These last two features are not in the tokenized
# text at all, or in the vocab we get by counting
# most_common features in it. So we create two separate
# columns for them at the start of the matrix. And
# instead of actually taking the 400 most common words,
# we take the most common 398.

wordsequence = dict()
header = ['#matchquality', '#rareword']

vocab = allwords.most_common(398)

idx = 2
for word, count in vocab:
    wordsequence[word] = idx
    idx += 1
    header.append(word)

header = '\t'.join(header)

outlines = []

textlens = []
errors = 0
leftout = 0

# We identify the column of the matrix that records
# words not found at all in our dictionary of English
# words. When this number is high, it tends to indicate
# severe OCR problems. We're going to set a 2% cap on it.

notenglishidx = wordsequence['#notenglishword']

for seq, value in seqdict.items():
    valid, recordid, text = value
    if valid and len(text) >= 40:
        textlens.append(len(text))
        wordcounts = np.zeros(400)
        for word, count in text.items():
            if word in wordsequence:
                idx = wordsequence[word]
            else:
                idx = 1
                # that's the moment where we pour all
                # words not in the top 398 into the
                # #rareword column.

            wordcounts[idx] = wordcounts[idx] + 1

        wordcounts = wordcounts / np.sum(wordcounts)

        if wordcounts[notenglishidx] > 0.02:
            continue

        if recordid in matchquality:
            wordcounts[0] = matchquality[recordid]
        else:
            print("Missing quality: ", seq, recordid)
            wordcounts[0] = 2.0
            errors += 1

            # What's happening here is that we're hitting some ringers
            # not in our database of matchqualities. But match quality
            # for these reviews is probably quite low. We make a
            # reasonable estimate.

        genre = genredict[seq]
        if genre == 'y' or genre == 'n':
            outline = seq + '\t' + genre + '\t' + '\t'.join([str(x) for x in wordcounts]) + '\n'
            outlines.append(outline)
        else:
            leftout += 1

with open('fictionfilter/trainingdata.tsv', mode = 'w', encoding = 'utf-8') as f:
    header = 'sequenceID\tgenrecode\t' + header + '\n'
    f.write(header)
    for o in outlines:
        f.write(o)
print()
print(errors)










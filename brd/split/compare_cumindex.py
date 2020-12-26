# compares the cumulative index to the previous four years and
# identifies books that are only in the fifth year

# in the process, identifies records from earlier years
# that are filed under a heading not attested in the
# cumulative index

import sys, os
from difflib import SequenceMatcher

args = sys.argv

year = int(args[1])

def get_authtitle(line):
    lineparts = line.split('$')

    author = lineparts[0]
    title = lineparts[1]

    return author, title

def get_metadata(path):
    with open(path, encoding = 'utf-8') as f:
        filelines = f.readlines()

    heading = 'no heading'

    metadata = []

    for line in filelines:

        line = line.strip()


        if line.startswith('**'):
            continue
        elif len(line) < 3:
            continue
        elif line.startswith('<') and line.endswith('>'):
            line = line.replace('"', '').replace("'", ''). replace('”', '').replace('>', '')
            heading = ' '.join(line.split(' ')[1: ])
        elif '$' in line:
            author, title = get_authtitle(line)
            metadata.append((author, title, heading))
        else:
            print(line)

    return metadata

def find_match(auth, title, tomatch):

    bestmatch = ''
    maxmatch = 0

    for auth2, title2, heading in tomatch:

        authmatcher = SequenceMatcher(None, auth, auth2)
        authmatch = authmatcher.ratio()

        titlematcher = SequenceMatcher(None, title, title2)
        titlematch = titlematcher.ratio()

        minlen = min(len(title), len(title2))
        if minlen < 8:
            titlematch = titlematch * .95
        if minlen > 16:
            titlematch = titlematch * 1.05

        totalmatch = authmatch * titlematch

        if totalmatch > maxmatch:
            maxmatch = totalmatch
            bestmatch = (auth2, title2, heading)

    return bestmatch, maxmatch

def do_headings_match(headingstring, heading):
    headings2 = headingstring.split('|')
    headingsmatch = False

    if len(headingstring) > 11:
        headingstring = headingstring[0: 11]

    for h2 in headings2:

        if len(h2) > 11:
            h2 = h2[0: 11]

        matcher = SequenceMatcher(None, heading, h2)
        heading_match = matcher.ratio()

        if heading_match > .7:
            headingsmatch = True
            break

    return headingsmatch

indexpath = '/media/secure_volume/brd/output_index/volume' + str(year) + ' extract.txt'

indexmeta = get_metadata(indexpath)

indexbyauth = dict()
indexbytitle = dict()

uniqueindex = 0

for auth, title, heading in indexmeta:

    if len(auth) > 0:
        authinitial = auth[0]
    else:
        authinital = 'x'

    if len(title) > 0:
        titleinitial = title[0]
    else:
        titleinitial = 'x'

    if authinitial not in indexbyauth:
        indexbyauth[authinitial] = dict()
    if titleinitial not in indexbytitle:
        indexbytitle[titleinitial] = dict()
    if titleinitial not in indexbyauth[authinitial]:
        indexbyauth[authinitial][titleinitial] = []
    if authinitial not in indexbytitle[titleinitial]:
        indexbytitle[titleinitial][authinitial] = []

    alreadyhave = indexbyauth[authinitial][titleinitial]

    bestmatch, maxmatch = find_match(auth, title, alreadyhave)
    if maxmatch > 0.6:
        matchindex = alreadyhave.index(bestmatch)
        a2, b2, h2 = alreadyhave[matchindex]
        if '|' not in h2:
            h2 = h2 + '|' + str(uniqueindex)
            uniqueindex += 1
        h3 = h2 + '|' + heading
        alreadyhave[matchindex] = (a2, b2, h3)
        alreadyhave.append((auth, title, h3))
    else:
        indexbyauth[authinitial][titleinitial].append((auth, title, heading))

    alreadyhave = indexbytitle[titleinitial][authinitial]

    bestmatch, maxmatch = find_match(auth, title, alreadyhave)
    if maxmatch > 0.6:
        matchindex = alreadyhave.index(bestmatch)
        a2, b2, h2 = alreadyhave[matchindex]
        h3 = h2 + '|' + heading
        alreadyhave[matchindex] = (a2, b2, h3)
        alreadyhave.append((auth, title, h3))
    else:
        indexbytitle[titleinitial][authinitial].append((auth, title, heading))

foundindices = set()
discrepancies = []

for y in range(year - 4, year):
    print()
    print(y)

    path = '/media/secure_volume/brd/output_index/volume' + str(y) + ' extract.txt'

    meta = get_metadata(path)
    print("titles in this year", len(meta))
    found = []
    unfound = []
    headingmatched = 0
    headingdiscrep = 0

    for auth, title, heading in meta:

        if len(auth) > 0:
            authinit = auth[0]
        else:
            authinit = 'x'

        if len(title) > 0:
            titleinit = title[0]
        else:
            titleinit = 'x'

        success = False

        if authinit in indexbyauth:
            authmatches = indexbyauth[authinit]
            if titleinit in authmatches:
                mostlikely = authmatches[titleinit]

                match, maximum = find_match(auth, title, mostlikely)

                if maximum > 0.45:
                    found.append(((auth, title, heading), match))
                    auth2, title2, headings2 = match

                    headingsmatch = do_headings_match(headings2, heading)

                    if headingsmatch:
                        headingmatched += 1
                    else:
                        headingdiscrep += 1
                        cumheadings = headings2.split('|')
                        cumheadings = ' + '.join([x for x in cumheadings if not x.isdigit()])
                        discrepancies.append([str(y), auth, title, heading, auth2, title2, cumheadings])

                    success = True
                    mostlikely.pop(mostlikely.index(match))

                else:

                    for initial, triples in authmatches.items():
                        match, maximum = find_match(auth, title, triples)
                        if maximum > 0.45:
                            success = True
                            found.append(((auth, title, heading), match))
                            triples.pop(triples.index(match))

                            auth2, title2, headings2 = match
                            headingsmatch = do_headings_match(headings2, heading)

                            if headingsmatch:
                                headingmatched += 1
                            else:
                                headingdiscrep += 1
                                cumheadings = headings2.split('|')
                                cumheadings = ' + '.join([x for x in cumheadings if not x.isdigit()])
                                discrepancies.append([str(y), auth, title, heading, auth2, title2, cumheadings])

                            break

            else:

                for initial, triples in authmatches.items():
                    match, maximum = find_match(auth, title, triples)
                    if maximum > 0.45:
                        success = True
                        found.append(((auth, title, heading), match))
                        triples.pop(triples.index(match))

                        auth2, title2, headings2 = match
                        headingsmatch = do_headings_match(headings2, heading)

                        if headingsmatch:
                            headingmatched += 1
                        else:
                            headingdiscrep += 1
                            cumheadings = headings2.split('|')
                            cumheadings = ' + '.join([x for x in cumheadings if not x.isdigit()])
                            discrepancies.append([str(y), auth, title, heading, auth2, title2, cumheadings])

                        break

        if not success:
            unfound.append((auth, title, heading))

    print('Found: ', len(found))
    print('matched headings', headingmatched)
    print('discrepant ', headingdiscrep)
    print('unfound: ', len(unfound))

    for a, b in found:
        a, t, h = a
        elements = h.split('|')
        for e in elements:
            if e.isdigit():
                foundindices.add(e)

headingdict = dict()
headinglist = []

count = 0
for k, v in indexbyauth.items():
    for k2, v2 in v.items():
        for a, t, h in v2:
            elements = h.split('|')
            toremove = False
            for e in elements:
                if e in foundindices:
                    toremove = True
                if e.isdigit():
                    foundindices.add(e)

            if not toremove:
                count += 1
                for e in elements:
                    if e.isdigit():
                        continue
                    elif e not in headingdict:
                        headingdict[e] = []
                        headinglist.append(e)
                    headingdict[e].append((a, t))

print('Unmatched in cum index: ', count)

headinglist.sort()

outfolder = '/media/secure_volume/brd/split/'

unmatchedlines = []

for heading in headinglist:
    unmatchedlines.append('<\\heading ' + heading + '>\n')
    for a, t in headingdict[heading]:
        unmatchedlines.append(a + ' <:> ' + t + '\n')

numlines = len(unmatchedlines)
fileindex = 0

for floor in range(0, numlines, 56):
    filename = outfolder + 'uml' + str(fileindex) + '.txt'
    fileindex += 1

    with open(filename, mode = 'w', encoding = 'utf-8') as f:
        f.write('\n')
        for l in unmatchedlines[floor: floor + 56]:
            outline = '  ' + l
            f.write(outline)

discreplines = []
for row in discrepancies:
    discreplines.append(' > '.join(row) + '\n')

numlines = len(discreplines)
fileindex = 0

for floor in range(0, numlines, 56):
    filename = outfolder + 'dcl' + str(fileindex) + '.txt'
    fileindex += 1

    with open(filename, mode = 'w', encoding = 'utf-8') as f:
        f.write('\n')
        for l in discreplines[floor: floor + 56]:
            outline = '  ' + l
            f.write(outline)


















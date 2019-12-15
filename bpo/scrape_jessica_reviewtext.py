import xml.etree.ElementTree as ET
import os, csv, sys, re
from zipfile import ZipFile
import pandas as pd

wanted = ['RecordID', 'RecordTitle', 'Title',
     'AlphaPubDate', 'SubjectTerms', 'Volume', 'Issue',
     'StartPage', 'EndPage']

def get_texts(zf, seqrecords):
    print(pathid)
    global wanted
    wantset = set(wanted)

    files = zf.namelist()
    allrecords = []
    errorlist = []

    for seq, record in seqrecords:
        f = str(record) + '.xml'
        if f not in files:
            errorlist.append(f)
            continue

        record = dict()
        record['SubjectTerms'] = []
        record['seq'] = seq

        try:
            data = zf.read(f)
            root = ET.fromstring(data)
        except:
            errorlist.append(f)
            continue

        for child in root:
            tag = child.tag
            if tag in wantset and not tag in record:
                record[tag] = child.text
            elif tag in wantset:
                record[tag] = record[tag] + '|' + child.text
            elif tag == 'Publication':
                for grandchild in child:
                    record[grandchild.tag] = grandchild.text
            elif tag == 'FullText':
                record['reviewtext'] = child.text
            elif tag == 'Terms':
                for grandchild in child:
                    FTname = 'ds'
                    for ggc in grandchild:
                        if ggc.tag == 'FlexTermValue' and FTname == 'ds':
                            record['SubjectTerms'].append(ggc.text)

        if len(record['SubjectTerms']) > 0:
            record['SubjectTerms'] = '|'.join(record['SubjectTerms'])
        else:
            record['SubjectTerms'] = ''

        allrecords.append(record)

    return allrecords, errorlist

## MAIN EXECUTION BEGINS HERE

sourcedir = '/projects/ischoolichass/ichass/usesofscale/tardis/BPO/'
sources = [x for x in os.listdir(sourcedir) if x.endswith('.zip')]

args = sys.argv

jess = pd.read_csv('jessica_articles.tsv', sep = '\t')

magazinegroups = jess.group_by('Title')

for name, groupdf in magazinegroups:
    print(name)

index = int(args[1])

magazinename, toget = magazinegroups[index]
bypath = toget.groupby('PathID')

filename = magazinename.lower().replace(' ', '')
if len(filename) > 20:
    filename = filename[0 : 20]

outfile = 'jessica/' + filename + '.txt'

recordsfromallpaths = []

for pathid, group in bypath:

    path = 'StanfordBP_' + pathid + '.zip'

    zf = ZipFile(sourcedir + path)

    records, errorlist = get_texts(zf, list(group['RecordID']))

    for rec in records:
        recordsfromallpaths.append(rec)

with open(outfile, mode = 'w', encoding = 'utf-8') as f:

    for rec in recordsfromallpaths:
        for t in wanted:
            if t not in rec:
                rec[t] = ''

        f.write('<' + ' | '.join(rec['RecordID'], rec['RecordTitle']]) + '>\n')
        fulltext = rec['reviewtext'].replace("&apos;", "'").replace('&quot;', '"')
        fulltext = fulltext.replace('&amp;', '&').replace('&pound;', '£').replace('&lt;', '<').replace('&gt;', '>')
        f.write(fulltext + '\n')



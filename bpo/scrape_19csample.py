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

infile = args[1]
outfile = args[2]

toget = pd.read_csv(infile, sep = '\t', index_col = 'seq')
bypath = toget.groupby('PathID')

recordsfromallpaths = []

for pathid, group in bypath:
    seqtuples = []
    for seq, row in group.iterrows():
        seqtuples.append((seq, row['RecordID']))

    path = 'StanfordBP_' + pathid + '.zip'

    zf = ZipFile(sourcedir + path)

    records, errorlist = get_texts(zf, seqtuples)

    for rec in records:
        seq = rec['seq']
        recordsfromallpaths.append((seq, rec))

recordsfromallpaths.sort(key = lambda x: x[0])

with open(outfile, mode = 'w', encoding = 'utf-8') as f:

    for seq, rec in recordsfromallpaths:

        fulltext = rec['reviewtext'].replace("&apos;", "'").replace('&quot;', '"')
        fulltext = fulltext.replace('&amp;', '&').replace('&pound;', '£').replace('&lt;', '<').replace('&gt;', '>')
        fulltext = fulltext.replace('\n', '  ').replace('\t', ' ')
        f.write(str(seq) + '\t' + fulltext + '\n')



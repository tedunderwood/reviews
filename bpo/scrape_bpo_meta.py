import xml.etree.ElementTree as ET
import os, csv
from zipfile import ZipFile

wanted = ['RecordID', 'RecordTitle', 'DateTimeStamp', 'PathID', 'PublicationID', 'Title', 'Qualifier', 'Publisher',
     'AlphaPubDate', 'NumericPubDate', 'SourceType', 'SubjectTerms', 'OtherTerms', 'ObjectType', 'LanguageCode', 
     'Volume', 'Issue', 'StartPage', 'EndPage']

def get_table(zf, pathid):
    print(pathid)
    global wanted
    wantset = set(wanted)

    files = zf.namelist()
    allrecords = []
    errorlist = []

    for f in files:

        record = dict()
        record['SubjectTerms'] = []
        record['OtherTerms'] = []
        record['PathID'] = pathid

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
            elif tag == 'Terms':
                for grandchild in child:
                    FTname = 'ds'
                    for ggc in grandchild:
                        if ggc.tag == 'FlexTermValue' and FTname == 'ds':
                            record['SubjectTerms'].append(ggc.text)
                        elif ggc.tag == 'FlexTermName' and ggc.text == 'DerivedSubject':
                            FTname = 'ds'
                        elif ggc.tag == 'FlexTermName':
                            FTname = 'other'
                        elif ggc.tag == 'FlexTermValue' and FTname != 'ds':
                            record['OtherTerms'].append(ggc.text)

        if len(record['SubjectTerms']) > 0:
            record['SubjectTerms'] = '|'.join(record['SubjectTerms'])
        else:
            record['SubjectTerms'] = ''

        if len(record['OtherTerms']) > 0:
            record['OtherTerms'] = '|'.join(record['OtherTerms'])
        else:
            record['OtherTerms'] = ''

        allrecords.append(record)

    return allrecords, errorlist

sourcedir = '/projects/ischoolichass/ichass/usesofscale/tardis/BPO/'
sources = [x for x in os.listdir(sourcedir) if x.endswith('.zip')]

processed = 0

for source in sources:
    
    pathid = source.replace('StanfordBP_', '').replace('.zip', '')
    outfile = '../meta/' + pathid + '.tsv'

    if os.path.isfile(outfile):
        continue

    zf = ZipFile(sourcedir + source)
    
    allrecords, errorlist = get_table(zf, pathid)

    with open(outfile, mode = 'w', encoding = 'utf-8') as f:
        writer = csv.DictWriter(f, fieldnames = wanted, delimiter = '\t')
        writer.writeheader()
        for rec in allrecords:
            writer.writerow(rec)

    errorpath = '../meta/errorlist.txt'
    with open(errorpath, mode = 'a', encoding = 'utf-8') as f:
        for anid in errorlist:
            f.write(anid + '\n')

    processed += 1
    if processed > 25000:
        break


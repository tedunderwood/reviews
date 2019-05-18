# filter_bpo_for_fiction.py

# Sweeps through BPO, applying a model to see if a review
# is likely a review of a work of fiction.

import xml.etree.ElementTree as ET
import os, csv, sys, re 
from zipfile import ZipFile
import pickle
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

with open('model/fictionreview_scaler.pkl', mode = 'rb') as f:
	scaler = pickle.load(f)

with open('model/fictionreview_model.pkl', mode = 'rb') as f:
	model = pickle.load(f)

# read the vocabulary to create
# both a "vocab" set of all words we didn't consider
# rarewords, and a "leximap" dict of words actually
# used in the model

with open('model/fictionreview_vocab.txt', mode = 'r', encoding = 'utf-8') as f:
	leximap = dict()
	vocab = set()
	for idx, line in enumerate(f):
		word = line.strip()
		if idx < 210:
			vocab.add(word)
			leximap[word] = idx

reg_constant = .0265
numfeatures = 210

# these constants are copied directly from makemodel.ipynb
# where the model is trained

delchars = ''.join(c for c in map(chr, range(256)) if not c.isalpha())
spaces = ' ' * len(delchars)
punct2space = str.maketrans(delchars, spaces)

rulepath = '/projects/ischoolichass/ichass/usesofscale/rules/'
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

def words2vec(words, vocab, leximap, numfeatures):
	vector = np.zeros(numfeatures)
	for w in words:
		if w not in vocab:
			w = '#rareword'
			# which is, itself, in the lexicon!
		idx = leximap[w]
		vector[idx] += 1

	vector = vector / np.sum(vector)

	return vector

wanted = ['RecordID', 'RecordTitle', 'Title', 
	 'AlphaPubDate', 'SubjectTerms', 'Volume', 'Issue', 
	 'StartPage', 'EndPage']

def get_texts(zf, recordIDs):
	print(pathid)
	global wanted
	wantset = set(wanted)

	files = zf.namelist()
	allrecords = []
	errorlist = []

	for record in recordIDs:
		f = str(record) + '.xml'
		if f not in files:
			errorlist.append(f)
			continue

		record = dict()
		record['SubjectTerms'] = []

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

toget = pd.read_csv(infile, sep = '\t')
meandate = np.mean(toget.PubYear)
bypath = toget.groupby('PathID')

suspicious = {'CHRISTMAS', 'BOOKS.', 'NOVELS', 'OF', 'OP', 'WEEK.'}

recordsfromallpaths = []
athenaeumcollectives = []
pubdates = dict()

recordsconsidered = 0

for pathid, group in bypath:
	recordIDs = []
	for seq, row in group.iterrows():
		recordIDs.append(row['RecordID'])
		pubdates[str(row['RecordID'])] = str(row['PubYear'])

	path = 'StanfordBP_' + pathid + '.zip'

	zf = ZipFile(sourcedir + path)

	records, errorlist = get_texts(zf, recordIDs)

	probs = []

	for rec in records:
		recordsconsidered += 1

		if 'reviewtext' in rec:
			words = line2words(rec['reviewtext'])
		else: 
			continue

		if 'RecordTitle' in rec:
			words.extend(line2words(rec['RecordTitle']))
		if len(words) <= 30:
			continue

		vector = words2vec(words, vocab, leximap, 210)
		scaled = scaler.transform(vector.reshape(1, -1))
		prob = model.predict_proba(scaled)[0][1]

		probs.append(prob)

		if prob < 0.5:
			continue

		if 'Title' in rec and rec['Title'] == 'The Athenaeum':
			if meandate > 1870 and meandate < 1890:
				reviewtext = rec['reviewtext']
				textlen = len(reviewtext)
				cap = min(textlen, 300)
				checktext = rec['ReviewTitle'] + ' ' + reviewtext[0: cap]
				words2check = set(checktext.split())
				suspects = len(suspicious.intersection(words2check))
				if checktext.count('(') > 1:
					suspects += checktext.count('(')
				if len(suspects) > 1:
					athenaeumcollectives.append(rec)
					continue

		# okay, it survived filtering
		
		recordsfromallpaths.append(rec)

print()
print(len(recordsfromallpaths) / recordsconsidered)

def writerecord(rec, file):
	global pubdates

	outtext = rec['reviewtext'].replace("&apos;", "'").replace('&quot;', '"').replace('\t', ' ')
	outtext = outtext.replace('&amp;', '&').replace('&pound;', '£').replace('&lt;', '<').replace('&gt;', '>')
	pubdate = pubdates[rec['RecordID']]
	file.write(str(rec['RecordID']) + '\t' + str(pubdate) + '\t' + outtext + '\n')


with open(outfile, mode = 'a', encoding = 'utf-8') as f:

	for rec in recordsfromallpaths:
		for t in wanted:
			if t not in rec:
				rec[t] = ''

		writerecord(rec, f)

with open('athenaeumcollectives.txt', mode = 'a', encoding = 'utf-8') as f:

	for rec in athenaeumcollectives:
		for t in wanted:
			if t not in rec:
				rec[t] = ''

		writerecord(rec, f)




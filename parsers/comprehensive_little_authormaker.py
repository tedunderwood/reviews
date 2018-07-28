# comprehensive_little_authormaker.py

# Extracts author objects from the Comprehensive
# Index to Little Magazines.

import os, sys
import extract_pagelist
from difflib import SequenceMatcher

templates = {'LITTLE MAGAZINE INDEX', 'WORKS BY', 'WORKS ABOUT'}

def match_strings(stringa, stringb):
	m = SequenceMatcher(None, stringA, stringB)
	match = m.quick_ratio()

	if match > 0.7:
		match = m.ratio()

	return match

def get_authors(pagelist):
	global templates

	authors = []

	thisauthor = ''

	# Our initial strategy is to find uppercase lines that don't fit any of
	# the templates listed above in "templates." By process of elimination,
	# those are the names of authors.

	for page in pagelist:
		for linenum, line in enumerate(page):

			if line.isupper():
				upperpct = 1
				digitpct = 0
			elif len(line) == 0:
				upperpct = 0
				digitpct = 0
			else:
				upper = 0
				lower = 0
				digits = 0

				for char in line:
					if char.isupper():
						upper += 1
					elif char.isalpha():
						lower += 1
					elif char.isdigit():
						digits += 1

				upperpct = upper / (upper + lower + 0.1)
				digitpct = digits / (len(line) + 0.1)

			if upperpct < 0.9:
				continue
				# lowercase lines are not authors
			elif digitpct > .95 and linenum < 2:
				continue
				# this is a page number on the top of the page
			elif line in templates:
				# this is a line like "WORKS BY"
				continue
			else:
				for t in templates:
					match = match_strings(line, t)
					if match > 0.88:
						continue

			# If flow reaches this point, all the reasons to ignore this line
			# have been exhausted. We infer that it's an author name!

			authors.append(line)

	return authors

vols2parse = ['39015019184806']

for vol in vols2parse:
	pagelist = extract_pagelist.extract(vol)
	authors = get_authors(pagelist)
	with open('authorlist.txt', mode = 'w', encoding = 'utf-8') as f:
		for auth in authors:
			f.write(auth + '\n')


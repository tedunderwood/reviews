# read_pubnames.py

import csv

def get_names(path):

	pubwords = set()
	pubnames = dict()

	with open(path, mode = 'r', encoding = 'utf-8') as f:
		reader = csv.DictReader(f, delimiter = '\t')
		for row in reader:
			code = row['code']
			words = code.split()
			for w in words:
				pubwords.add(w)
				pubwords.add(w.strip('.'))
				pubwords.add(w.lower())
			name = row['fullname']
			pubnames[code] = name

	not_allowed = ['a', 'an', 'am', 'to', 'the', 'of']
	for n in not_allowed:
		if n in pubwords:
			print(n)
			pubwords.remove(n)

	return pubwords, pubnames

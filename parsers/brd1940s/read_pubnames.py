## read_pubnames.py

import csv

not_allowed = ['a', 'an', 'to', 'the', 'of', 'and', 'am', 'A.', '&']

def get_names(path):

	pubwords = {'kirkus', 'york', 'times', 'chicago', 'tribune', 'yorker'}
	pubnames = dict()

	with open(path, mode = 'r', encoding = 'utf-8') as f:
		reader = csv.DictReader(f, delimiter = '\t')
		for row in reader:
			code = row['code']
			words = code.split()
			for w in words:
				if w not in not_allowed:
					pubwords.add(w)
					pubwords.add(w.strip('.'))
			name = row['fullname']
			pubnames[code] = name

	return pubwords, pubnames

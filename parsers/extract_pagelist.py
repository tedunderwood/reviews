# extract_pagelist.py

# This opens a zipfile and reads all the pages;
# it returns a list of pages, where each page is 
# a list of lines.

# To specify a zipfile, the function extract()
# requires a "suffix": this is the part of the
# volume id after the first period.

from zipfile import ZipFile
import os, sys

def extract(suffix):
	datadir = '/media/secure_volume/volsinuse/'
	zippath = datadir + suffix + '.zip'

	pages = []

	with ZipFile(zippath) as z:
		pageinfo = z.infolist()

		pagetuples = []
		for p in pageinfo:
			print(p.filename)
			sequence = p.filename.split('/')[-1].replace('.txt', '')
			try:
				sequence = int(sequence)
			except:
				print(sequence)
			pagetuples.append((sequence, p.filename))

		pagetuples.sort()

		for sequence, filename in pagetuples:
			pg = str(z.read(filename), 'utf-8')
			lines = pg.split('\n')
			pages.append(lines)

	return pages

if __name__ == "__main__":
	suffix = sys.argv[1]
	pages = extract(suffix)
	print(pages[10: 12])




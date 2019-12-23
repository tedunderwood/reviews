# extract_pagelist.py

# This opens a zipfile and reads all the pages;
# it returns a list of pages, where each page is
# a list of lines.

# To specify a zipfile, the function extract()
# requires a "suffix": this is the part of the
# volume id after the first period.

from zipfile import ZipFile
import os, sys

def extract(suffix, startpage):
	''' Reads pages in the zipfile named by suffix.
	First it sorts the pages to put them in integer order.
	It only reads pages after startpage.
	'''

	datadir = '/media/secure_volume/brd/'
	zippath = datadir + suffix + '.zip'

	pages = []

	with ZipFile(zippath) as z:
		pageinfo = z.infolist()

		pagetuples = []

		for p in pageinfo:
			sequence = p.filename.split('/')[-1].replace('.txt', '')
			if '_' in sequence:
				sequence = sequence.split('_')[-1]
			try:
				sequence = int(sequence)
			except:
				print('non-integer filename: ', sequence)
			pagetuples.append((sequence, p.filename))

		pagetuples.sort()

		for sequence, filename in pagetuples:
			if sequence < startpage:
				continue

			pg = str(z.read(filename), 'utf-8')
			lines = pg.split('\n')
			pages.append(lines)

	return pages

if __name__ == "__main__":
	suffix = sys.argv[1]
	pages = extract(suffix)
	print(pages[10: 12])




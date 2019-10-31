# bred_extract_local_pagelist.py

# This opens a zipfile and reads all the pages;
# it returns a list of pages, where each page is
# a list of lines.

# To specify a zipfile, the function extract()
# requires a "suffix": this is the part of the
# volume id after the first period.

# This differs from brd_extract_pagelist mainly in
# expecting a local folder.



import os, sys

def extract(volumeID, startpage):
	''' Reads pages in the zipfile named by suffix.
	First it sorts the pages to put them in integer order.
	It only reads pages after startpage.
	'''

	datadir = '/Users/tunder/Dropbox/python/reviews/gethathi/'
	volfolder = os.path.join(datadir, volumeID)

	pages = []

	pagetuples = []

	files = os.listdir(volfolder)

	for filename in files:
		sequence = filename.replace('.txt', '')
		try:
			sequence = int(sequence)
			pagetuples.append((sequence, filename))
		except:
			print('non-integer filename: ', sequence)

	pagetuples.sort()

	for sequence, filename in pagetuples:
		if sequence < startpage:
			continue

		with open(os.path.join(volfolder, filename), encoding = 'utf-8') as f:
			lines = f.readlines()
		pages.append(lines)

	return pages

if __name__ == "__main__":
	suffix = sys.argv[1]
	pages = extract(suffix)
	print(pages[10: 12])




# comprehensive_little_authormaker.py

# Extracts Author objects from the Comprehensive
# Index to Little Magazines.

# The general strategy is to loop through pages, looking for author names--
# in other words, lines that are

#    1) mostly uppercase
#    2) but don't match the "templates" listed below (e.g. "WORKS ABOUT")

# Because texts can have OCR errors we use *fuzzy* matching to assess (2).
# Once we find author names, we turn the lines between author names
# into Author objects.

import os, sys
import extract_pagelist
from difflib import SequenceMatcher

templates = {'LITTLE MAGAZINE INDEX', 'WORKS BY', 'WORKS ABOUT'}

def match_strings(stringA, stringB):
	m = SequenceMatcher(None, stringA, stringB)
	match = m.quick_ratio()

	if match > 0.7:
		match = m.ratio()

	return match

class Author:

    # An Author is a creature that possesses a name and a sequence of
    # tagged lines. Each of the lines may be tagged "about" or "by," if it
    # appeared in a WORKS ABOUT or WORKS BY section. But lines are also
    # permitted to possess blank tags.

    def __init__(self, authorname, linelist):

    	self.name = authorname

    	current_tag = ''
    	self.tagged_lines = []

    	for line in linelist:
    		bymatch = match_strings(line, 'WORKS BY')
    		aboutmatch = match_strings(line, 'WORKS ABOUT')
    		if bymatch > 0.9:
    			current_tag = 'by'
    			continue
    			# notice that the line WORKS BY itself is not preserved
    		elif aboutmatch > 0.9:
    			current_tag = 'about'
    			continue
    		else:
    			linetuple = (line, current_tag)
    			self.tagged_lines.append(linetuple)

    def get_lines(self):
    	return list(self.tagged_lines)

    	# I'm providing a method that returns a deep copy,
    	# to insulate the object from accidental changes.


def get_authors(pagelist):
	global templates

	# Our initial strategy is to find uppercase lines that don't fit any of
	# the templates listed above in "templates." By process of elimination,
	# those are the names of authors.

	# We create a list of author_names as well as a list of Author objects.

	author_names = []
	authors = []

	# We keep track of the last author name we've seen; it's going to be
	# the name that governs the lines we are currently examining.

	last_author_name = ''
	last_auth_lines = []

	for page in pagelist:
		for linenum, line in enumerate(page):

			# First we assess the percentage of characters that are uppercase,
			# and the percentage that are digits.

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

				upperpct = upper / (len(line) + 0.1)
				digitpct = digits / (len(line) + 0.1)

			# Now that we have those percentages, we

			if upperpct < 0.9:
				last_auth_lines.append(line)
				continue
				# lowercase lines are not authors
				# but should be appended to these_lines

			elif digitpct > .95 and linenum < 2:
				continue
				# this is a page number on the top of the page
				# ignore it

			elif line in templates:
				# this is a line like "WORKS BY"
				# save it unless it's the book title

				if line != 'LITTLE MAGAZINE INDEX':
					last_auth_lines.append(line)
				continue

			else:
				# maybe we need fuzzy matching?
				matched = False
				for t in templates:
					match = match_strings(line, t)
					if match > 0.85:
						if t != 'LITTLE MAGAZINE INDEX':
							last_auth_lines.append(line)
						matched = True
						break

				if matched:
					continue

			# If flow reaches this point, all the reasons to ignore this line
			# have been exhausted. We infer that it's an author name!

			# We create a new Author object using the last name and the
			# lines we've been gathering.

			lastauth = Author(last_author_name, last_auth_lines)
			authors.append(lastauth)

			# Create a new blank list of lines.
			last_auth_lines = []

			# The next Author will use this name.
			last_author_name = line
			author_names.append(line)

	return authors, author_names


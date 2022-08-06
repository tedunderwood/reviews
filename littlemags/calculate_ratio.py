# calculate ratio

import glob
import pandas as pd

filelist = glob.glob('/media/secure_volume/clm/output/titlematch*')

hits = dict()
totals = dict()


for afilepath in filelist:
	alternate = afilepath.replace('titlematch', '')

	allyears = pd.read_csv(alternate, sep = '\t')
	matched = pd.read_csv(afilepath, sep = '\t')

	authors = set([str(x) for x in matched.author])

	for auth in authors:
		df = matched.loc[matched.author == auth, : ]
		pubyrs = set()
		for years in df.yearlist:
			if pd.isnull(years):
				continue
			combos = years.split()
			for c in combos:
				yr, pubyr = c.split('--')
				yr = int(yr)
				if yr < 80:
					yr = yr + 1900
				else:
					yr = yr + 1900
				pubyr = int(pubyr)
				pubyrs.add(pubyr)
				gap = yr - pubyr
				if gap not in hits:
					hits[gap] = 0
				hits[gap] += 1

		df = matched.loc[matched.author == auth, : ]
		for yearstring in df.yearlist:
			if pd.isnull(yearstring):
				continue
			years = [int(x) for x in yearstring.split()]
			for yr in years:
				if yr < 80:
					yr = yr + 1900
				else:
					yr = yr + 1900

				for py in pubyrs:
					gap = yr - py
					if gap not in totals:
						totals[gap] = 0
					totals[gap] += 1

	print(len(hits), len(totals))


for gap in [-5, 15]:
	print(gap, round((hits[gap] * 100)/totals[gap]), 6)






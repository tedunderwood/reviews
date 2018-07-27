import pandas as pd
import os

have = 0
knownmissing = 0
unknownmissing = 0

missing = set()
with open('/media/secure_volume/volumes_not_available') as f:
	for line in f:
		zipfile = line.strip().split('/')[0].replace('.zip', '')
		missing.add(zipfile)

meta = pd.read_csv('/home/dcuser/reviews/metadata/volmeta.csv')

datapath = '/media/secure_volume/voids-6775/'

for anid in meta.docid:
	parts = anid.split('.', 1)
	if len(parts) != 2:
		print(parts, 'error')
		continue
	else:
		suffix = parts[1]

	checkpath = datapath + suffix + '/' + suffix + '.zip'

	if os.path.isfile():
		have += 1
	else:
		if suffix in missing:
			knownmissing += 1
		else:
			unknownmissing += 1

print("Files we have: ", have)
print("Files known missing: ", knownmissing)

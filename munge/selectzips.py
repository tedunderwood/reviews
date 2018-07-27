import pandas as pd
import os, shutil

titles2get = {'comprehensivelittle', 'brd', 'rpgl'}

meta = pd.read_csv('/home/dcuser/reviews/metadata/volmeta.csv')

datapath = '/media/secure_volume/voids-6775/'

destpath = '/media/secure_volume/volsinuse/'

for idx, row in meta.iterrows():

	anid = row['volid']
	filename = row['filename']

	parts = anid.split('.', 1)
	suffix = parts[1]

	checkpath = datapath + suffix
	if os.path.isdir(checkpath):
		continue

	if filename not in titles2get:
		shutil.rmtree(checkpath)

	else:
		source = checkpath + '/' + suffix + '.zip'
		destination = destpath + suffix + '.zip'
		shutil.move(source, destination)

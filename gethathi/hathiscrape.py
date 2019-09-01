from hathitrust_api import DataAPI
import pandas as pd 
import codecs, time, os, random

# meta = pd.read_csv('manual.tsv', sep = '\t')

data_api = DataAPI("546686df08", "fbda40a272c61f76a40d3c80ee2e")

hathi_ids = ['uiug.30112013681652', 'uiug.30112013681678', 'uiug.30112013682262']


for anid in hathi_ids:
	
	cleanid = anid.replace('/', '+').replace(':', '=')
	if os.path.isdir(cleanid):
		pagesalready = set([int(x.replace('.txt', '')) for x in os.listdir(cleanid)])
	else:
		os.mkdir(cleanid)
		pagesalready = set()

	finished = False

	print(anid)
	for i in range(1, 1000):
		pagename = i - 1

		# note that the API starts counting at 1 but we start counting at zero
		# I *think* this is right

		if pagename in pagesalready:
			print(pagename, end = '*')
			continue

		try:
			text = data_api.getpageocr(anid, i)
			text = codecs.decode(text, 'utf-8')
			print(pagename, end = ' ')
			with open(cleanid + '/' + str(pagename) + '.txt', mode = 'w', encoding = 'utf-8') as f:
				f.write(text)
			
		except Exception as inst:
			print(type(inst))
			print(inst.args)
			if inst.args[0].startswith('404'):
				finished = True
			break
		time.sleep(1.15)

	if finished:
		print()
		print('totalpages: ' + str(pagename))
		print()
				
	else:
		time.sleep(10)
		print('failed: ' + str(pagename))
		print()
		




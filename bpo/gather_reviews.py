import os, csv

tables = ['../meta/' + x for x in os.listdir('../meta') if x.endswith('.tsv')]

rows = []

for t in tables:
	print(t)	
	with open(t, encoding = 'utf-8') as f:
		reader = csv.DictReader(f, delimiter = '\t')
		fieldnames = reader.fieldnames
		for row in reader:
			if row['ObjectType'] == 'Review' and 'LITERATURE' in row['SubjectTerms']:
				row.pop('DateTimeStamp')
				row.pop('LanguageCode')
				row.pop('OtherTerms')
				row['PubYear'] = row['NumericPubDate'][0:4]
				rows.append(row)

fieldnames.remove('DateTimeStamp')
fieldnames.remove('LanguageCode')
fieldnames.remove('OtherTerms')
fieldnames.append('PubYear')

with open('allreviews.tsv', mode = 'w', encoding = 'utf-8') as f:
	writer = csv.DictWriter(f, fieldnames = fieldnames, delimiter = '\t')
	writer.writeheader()
	for row in rows:
		writer.writerow(row)

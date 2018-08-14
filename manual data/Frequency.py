import csv

with open('vol1citations.tsv) as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row in reader:
    print(row)
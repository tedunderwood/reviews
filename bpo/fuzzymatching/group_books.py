import pandas as pd

meta = pd.read_csv('grouped_matches.tsv', sep = '\t')

grouped = meta.groupby('bookid')

authors = []
titles = []
bpoids = []
htrcids = []
subjects = []
genres = []
books = []

def string_equiv(aset):
    if len(aset) > 0:
        return(str(aset))
    else:
        return ''

for bookid, bookgroup in grouped:

    hid = set()
    bid = set()
    sset = set()
    gset = set()

    for idx, row in bookgroup.iterrows():

        if not pd.isnull(row['subjects']):
            subj = set(row['subjects'].split('|'))
        else:
            subj = set()

        if not pd.isnull(row['genres']):
            genr = set(row['genres'].split('|'))
        else:
            genr = set()

        hid.add(row['htrcid'])
        bid.add(row['bpoid'])

        for s in subj:
            if s == 'Fiction' or s == 'NotFiction' or s == 'UnknownGenre':
                continue
            if s == 'fast' or s == 'Sir':
                continue
            else:
                sset.add(s)

        for g in genr:
            if g == 'Fiction' or g == 'NotFiction' or g == 'UnknownGenre':
                continue
            if g == 'fast' or g == 'Sir':
                continue
            else:
                gset.add(g)

    author = row['author']
    title = row['title']

    if "waverly novels" in title.lower():
        continue
    else:
        authors.append(author)
        titles.append(title)
        books.append(bookid)
        bpoids.append(str(bid))
        htrcids.append(str(hid))
        genres.append(string_equiv(gset))
        subjects.append(string_equiv(sset))

new_df = pd.DataFrame({'bookid': books, 'author': authors, 'title': titles,
    'subjects': subjects, 'genres': genres, 'bpoids': bpoids, 'htrcids': htrcids})

new_df.to_csv('grouped_books.tsv', sep = '\t', index = False)

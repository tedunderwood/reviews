with open('../copydata/extract17dollar.txt', encoding = 'utf-8') as f:
    filelines = f.readlines()

with open('../copydata/extract17.txt', mode = 'w', encoding = 'utf-8') as f:
    for line in filelines:
        f.write(line.replace('$', ' <:> '))


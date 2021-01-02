import glob

filelist = glob.glob('../copydata/*.txt')

for filename in filelist:
    with open(filename, encoding = 'utf-8') as f:
        lines = f.readlines()

    with open(filename, mode = 'w', encoding = 'utf-8') as f:
        for l in lines:
            if not l == '\n':
                f.write(l)

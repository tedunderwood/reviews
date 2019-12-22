import sys

args = sys.argv

infile = '/media/secure_volume/brd/output_index/volume' + str(args[1]) + ' ' + str(args[2]) + '.txt'

outfolder = '/media/secure_volume/brd/split/'

with open(infile, encoding = 'utf-8') as f:
    lines = f.readlines()

numlines = len(lines)

fileindex = 0

for floor in range(0, numlines, 50):
    filename = outfolder + 's' + str(fileindex) + '.txt'
    fileindex += 1

    with open(filename, mode = 'w', encoding = 'utf-8') as f:
        f.write('\n')
        for l in lines[floor: floor + 50]:
            outline = ' ' + l.replace('$', ' <:> ')
            f.write(outline)

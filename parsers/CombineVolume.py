import os
import os.path
#applied to Comprehensive index to English-language little magazines volume 1-8
#combine txt files of one volume together
dirRoot='/media/secure_volume/voids-6775/39015019184806/39015019184806'
k=open("volume1.txt",'a')
for parent,dirnames,filenames in os.walk(dirRoot):
    for filepath in filenames:
        txtPath=os.path.join(parent,filepath)
        f=open(txtPath)
        k.write(f.read())
k.close()

dirRoot='/media/secure_volume/voids-6775/39015079928209/39015079928209'
k=open("volume2.txt",'a')
for parent,dirnames,filenames in os.walk(dirRoot):
    for filepath in filenames:
        txtPath=os.path.join(parent,filepath)
        f=open(txtPath)
        k.write(f.read())
k.close()

dirRoot='/media/secure_volume/voids-6775/39015079928191/39015079928191'
k=open("volume3.txt",'a')
for parent,dirnames,filenames in os.walk(dirRoot):
    for filepath in filenames:
        txtPath=os.path.join(parent,filepath)
        f=open(txtPath)
        k.write(f.read())
k.close()

dirRoot='/media/secure_volume/voids-6775/9015079928183/9015079928183'
k=open("volume4.txt",'a')
for parent,dirnames,filenames in os.walk(dirRoot):
    for filepath in filenames:
        txtPath=os.path.join(parent,filepath)
        f=open(txtPath)
        k.write(f.read())
k.close()

dirRoot='/media/secure_volume/voids-6775/39015079928175/39015079928175'
k=open("volume5.txt",'a')
for parent,dirnames,filenames in os.walk(dirRoot):
    for filepath in filenames:
        txtPath=os.path.join(parent,filepath)
        f=open(txtPath)
        k.write(f.read())
k.close()

dirRoot='/media/secure_volume/voids-6775/39015079928167/39015079928167'
k=open("volume6.txt",'a')
for parent,dirnames,filenames in os.walk(dirRoot):
    for filepath in filenames:
        txtPath=os.path.join(parent,filepath)
        f=open(txtPath)
        k.write(f.read())
k.close()

dirRoot='/media/secure_volume/voids-6775/39015079928159/39015079928159'
k=open("volume7.txt",'a')
for parent,dirnames,filenames in os.walk(dirRoot):
    for filepath in filenames:
        txtPath=os.path.join(parent,filepath)
        f=open(txtPath)
        k.write(f.read())
k.close()

dirRoot='/media/secure_volume/voids-6775/39015079928142/39015079928142'
k=open("volume8.txt",'a')
for parent,dirnames,filenames in os.walk(dirRoot):
    for filepath in filenames:
        txtPath=os.path.join(parent,filepath)
        f=open(txtPath)
        k.write(f.read())
k.close()


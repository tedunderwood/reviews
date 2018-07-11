import os
import os.path
dirRoot='/media/secure_volume/voids-6775/39015019184806/39015019184806'
k=open("volume1.txt",'a')
for parent,dirnames,filenames in os.walk(dirRoot):
    for filepath in filenames:
        txtPath=os.path.join(parent,filepath)
        f=open(txtPath)
        k.write(f.read())
k.close()


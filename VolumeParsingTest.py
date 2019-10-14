import re

def main():
    filein = open('volume1.txt', 'r',encoding='utf-8')
  # fileout=open('parsedVolume1.txt','w')
    text = filein.read()
    list_str = re.split(r"WORK BY|WORK ABOUT", text)
    for index in range(len(list_str)):
        fileout=open("./split_content/text%d" % index,'w',encoding='utf-8')
        fileout.write(list_str[index])
if __name__=='__main__':
    main()

import pprint
f= open('JournaltextList.txt')
content = f.read().split()
#print(content)
frequency={}
for word in content:
    if word not in frequency:
        frequency[word]=1
    else:
        frequency[word]+=1
#print(frequency)
new=sorted(frequency.items(),key=lambda item:item[1])
pp=pprint.PrettyPrinter(indent=4)
pp.pprint(new)
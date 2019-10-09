#coding:utf-8
import re
import sys
import os
#Overall Strategy:
#1.Parse the text into mutiple textual pieces of Author's name,"WORK BY" and "WORK ABOUT"
#2.Search for "review by" records within the "WORK ABOUT" sections
#3.

f=open('test.txt', 'r',encoding='utf-8')
line=f.readlines()
f1=open('new1.txt','w+')#collect Author's name,"WORK BY" and "WORK ABOUT"pieces
f2=open('new2.txt','w')#collect "review by" records



#1 First Version Done
#Parsing: get Author's name,"WORK BY" and "WORK ABOUT"pieces
try:
    for i in range(0,len(line)):
        if re.match(r"WORK BY|WORK ABOUT",line[i]):
            print("writing", i)
            f1.write(line[i])
            print(line[i])#WORK BY/ABOUT
            #Locate the line of "WORK BY" to identify the author's name(in the line above "WORK BY")
            #Locate the line of "WORK ABOUT" to find the start point of a section which might contains "review by" records.
            print(line[i-1])#Author's name/the last line of the "WORK BY" section
            ######To be done: how to find the end point of the "WORK ABOUT" section
        else:
            pass
except IndexError:
            print("pass")


line1=f1.readline()
flag=0


#2 To be done
#Selecting: try to find all the "review by" records in the "WORK ABOUT" sections.
# To be testing: WORK ABOUT\n[\w\W]*?review by[\w\W]*?\n\n
# an example of a "review by" record:
# The Function of Socialization in Social Evolution, review by, James G. Stevens. Sewanee. vol. 25 no. 2(Apirl’17) 253
try:
    for i in range(0,len(line1)):
        if re.match(r'WORK ABOUT\n[\w\W]*?review by[\w\W]*?\n\n',line[i-1]):
           flag+=1
#        if flag>3:
#          del line[i+1]
        else:
           continue
    else:
         f2.write(line[i])
except IndexError:
    print ("pass")
#print(flag)

#try:
#os.remove('new1.txt' )
#except WindowsError:
#  pass

#3 To be done
#Matching：connect the extracted "review by" record(s) with the corresponding author


f.close()
f2.close()

print("finish")




import os
import re
import numpy as np
from hathitrust_api import DataAPI
import pandas as pd
import codecs, time, os, random
np.set_printoptions(threshold=np.inf)
def get_directory(dir): # get all documents' directories in the folder
    lists = os.listdir(dir)  # traverse all subfolders in the folder
    volumenumber = len(lists)
    volumelist = list(range(volumenumber))
    pagenumber = list(range(volumenumber))
    path = list(range(volumenumber))
    for i in list(range(volumenumber)):
        volumelist[i] = os.path.join(dir, lists[i])  # concatenate rootdir and this specific volume
        volumepage = os.listdir(volumelist[i])  # traverse all txts in the volume subfolder
        pagenumber[i] = len(volumepage)
        path[i] = list(range(pagenumber[i]))
        volumepage.sort(key=lambda x: int(
            x[:-4]))  # sort the arrangement of the volumepages, from 0, 1, 10, 11, 100... to 0, 1, 2, 3, 4...
        for j in list(range(pagenumber[i])):
            path[i][j] = os.path.join(volumelist[i],
                                      volumepage[j])  # concatenate volume directory and this specific page
    return volumenumber, pagenumber, path
def read(x): # read the document
    f=open(x,'r', encoding='UTF-8')
    r=f.read()
    return r
def main():
    volumenumber = get_directory(r'D:\DH collaborative\book review\Library')[0]
    pagenumber = get_directory(r'D:\DH collaborative\book review\Library')[1]
    path= get_directory(r'D:\DH collaborative\book review\Library')[2]
    print(path)
    textlist=list(range(volumenumber))
    index_startpage=list(range(volumenumber))
    index_endpage=list(range(volumenumber))
    #a list of texts that wrongly attributed to headings. Keep updating
    wrong_headings=['Brgggn, A. Wind between the','Underngian. F. B. On a passing','Richardson, H: H. Fortunes of','Military servitude and','Humphrey, Z. Home','Mr','States in war-time','Strange story of William','Son of', 'Island of', 'Nathan. it', 'Adventures in','When the king losses his', 'Short stories from','Famous detective']
    headings_with_subheading=['European war','Historical novels','Locality, Novels of','Legends and folktale']
    # a list of subheadings, ususally name of places. Keep updating
    subheadings=['Balkan', 'Itoumunian','New Mexico', 'Philippine Islands', 'Imeden', 'Syracuse','Algeria', 'Baltimore', 'BroOklyn', 'Detroit', 'Hawaiian Islands', 'Long Island', 'Heeico', 'Michigan','Flem\xef\xac\x82h','Prussia','Austria', 'Balkans', 'Hungary', 'Poland','Asiatic Turkey', 'Austrla-Hungary', 'Brazll', 'Richard', 'Georgla', 'Great Lakes', 'Clammer and', 'Newport', 'South Sea Islands', 'Turkey','Bohemia', 'Portugal', 'Rome under Nero','Labrador', 'Latin Amerth', 'Malay peninsula', 'North Carolina', 'South America', 'South Sea islands', 'Sweden','Afrtoa', 'Arabian coast', 'Asia Minor', 'Constantinople', 'Cuba', 'Greece','Untted smm','Early Christiane', 'Netherlands', 'Palestine','New Memo','Bohemian','Greek', 'Hebrew', 'Norwegian', 'Polish', 'Portuguese','Yiddish','Germany', 'Great Britain', 'United States','Babylon', 'Crimean war', 'Denmark', 'England','France', 'Iceland', 'India', 'Napoleonic era', 'Rome', 'Russia', 'Scotland', 'Spain','Alaska', 'Australia', 'Bahama islands', 'California', 'Canada', 'Chile', 'Egypt', 'Georgia', 'Holland', 'Indiana', 'Ireland', 'Japan', 'Kansas', 'Kentucky', 'Lorraine', 'Missouri', 'Nebraska', 'New England', 'New Orleans', 'Oregon', 'Pennsylvania', 'Philadelphia', 'South A lrlca', 'Venice', 'Wales', 'West Virginia', 'Wisconsin','Danish', 'Dutch', 'French', 'German', 'Italian', 'Japanese', 'Russian', 'Sanskrit', 'Spanish', 'Swedish','Belgium','Cnnurla', 'Cape Colony', 'Emmi', 'Italy', 'Jerusalem', 'Middle ages','Flemish', 'Irish','Adirondacks', 'Africa', 'Arizona', 'Armenia', 'Boston', 'Email', 'Cape Cod', 'Chicago', 'China', 'Connecticut', 'Far East', 'Florida', 'Louisiana', 'Mexico', 'Minnesota', 'Mississippi river', 'New chlmul', 'Ohio', 'Paris', 'Philippine islandn', 'San Francisco', 'South Africa', 'South Carolina', 'South seas', 'Switzerland', 'Virginia']
    subheadings=sorted(list(set(subheadings)))
    print(subheadings)
    # a list of headings that follows the fiction section. Need to add manually each time
    nextheadings=['Fiddier\'s luck. _ Schauﬂ\'ler, R. H. (.11 \'20)','Field ambulance sketches. (N \'19','Field book of insects. Lutz. . E.','Fielchrtlips for the cotton-belt. Morgan. J. O.','Fifth wheel. Prouty, 0. H. (Ap \'16)','Fifteens thousand miles by stage. Strahorn, C.','Fifty years in Oregon. Geer, T. T. (Jl. \'12.)','Field-days in California. Torrey. B. (Ap \'18)','Fiddling girl. Cam bell, D. R. (Jl \'14)','Fidelity. Glaspell, S. (My \'15)'] #to be changed
    nextheadings=sorted(list(set(nextheadings)))
    print(nextheadings)
    pattern1 = re.compile("[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[,.:]*\s[A-Z]*\s*[A-Za-z01][,.:]+\s") # regular author name, "0" for mistakenly recognized "O", "1" for mistankenly recognized "l", "a-z" for initials for wrongly recognized capitla letters
    pattern1_1= re.compile("[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[-][A-Z][a-zé§¢ﬂﬁ]+[']*[a-zé§¢ﬂﬁ]*[,.:]*\s[A-Z]*\s*[A-Za-z01][,.:]+\s") # names like "Kaye-Smith"
    pattern1_2=re.compile("[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[A-Z][a-zé§¢ﬂﬁ]+[']*[a-zé§¢ﬂﬁ]*[,.:]*\s[A-Z]*\s*[A-Za-z01][,.:]+\s") # names like "McArthur"
    pattern1_3=re.compile("[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[,.:]*\spseud.") # names with only a family name and with pseud.
    pattern1_4 = re.compile("[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[,.:]*\sSir\s[A-Za-z01][,.:]+\s")  # names with "Sir"
    pattern1_5=re.compile("[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*\s[A-Z][a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[,.:]*\s[A-Z]*\s*[A-Za-z01][,.:]+\s") # family names with two words "Du Puy"
    pattern2 = re.compile("[A-Z][a-z]+")
    pattern2_1=re.compile(" [A-Z][a-z]+")
    pattern2_2 = re.compile("[.:]\s[A-Z][a-z]+")
    for i in list(range(volumenumber)): # read all documents in all volumes
        bookcount = 0
        textlist[i]=list(range(pagenumber[i]))
        flag = 0
        count=-1
        for j in list(range(pagenumber[i])): # read all pages (seperate txt files)
            textlist[i][j]=read(path[i][j])
        for j in list(range(pagenumber[i])):  # get the start and end page number of the index. Note that modification may need, since there may be other OCR errors and inconsitency among years
            if textlist[i][j][:34].lower()=='subject, title and pseudonym index' or textlist[i][j][:23].lower()=='subject and title index': # case insensitive, and two different index titles
                print('Volume number %d: the index begins at page %d' %(i+6,j+1)) # output is added by 1 to be consistent with the book-no page 0 there
                index_startpage[i]=j
                flag=1
                for k in range(j,pagenumber[i]):
                    if textlist[i][k][:23].lower()=='directory of publishers' or len(textlist[i][k])==0: # case insensitive, and two different possible type of page after index: another directory, or empty
                        print('Volume number %d: the index ends at page %d' % (i+6, k))  # no 1 added, since that page is no longer index
                        index_endpage[i] = k
                        break
                break
        if flag==1: # if the volume has an index, do the following steps
            text=[]
            fiction_headings=[] # to store the headings
            fiction_books=[] # to store the lines under the heading
            for j in list(range(index_startpage[i], index_endpage[i])):
                bookcount+=textlist[i][j].count('(') # how many books are there in the index in total
                linenum=textlist[i][j].count('\n')+1
                line=list(range(linenum))
                line[0:linenum]=textlist[i][j].split('\n') # split each page by line
                line=line[:-1]
                for k in list(range(linenum-1)):
                    #print line[k]
                    #words=line[k].split()
                    #length=len(words)
                    #for m in range(length):
                    #    if(len(words[m]) == 2):
                    #        if words[m][0]>='A' and words[m][0]<='Z' and words[m][1]=='.':
                    #            bookcount+=1
                    if(line[k]!=''):
                        text.append(line[k])
            linelength=len(text)
            #print linelength
            if i>=6: # for well-organized fiction indexes
                for j in list(range(linelength)): # begin to generate a list of headings within fiction
                    if (text[j] == "FICTION" ):
                        bookcount_fiction=0
                        for k in list(range(1, linelength - j)):
                            if (text[j + k] in nextheadings): # if fiction section ends
                                break
                            if '(' in text[j+k]:
                                bookcount_fiction+=1
                            if len(text[j + k]) > 1 and len(text[k + j]) <= 30 and '(' not in text[
                                k + j] and '\'' not in text[
                                k + j]:  # must be at least 2 characters, no more than 25 characters (avoiding titles not finished in a line to be included, not including '(' to avoid OCR error) # next line beginning with non-characterized character
                                if (text[k + j][0] >= 'A' and text[k + j][0] <= 'Z' and text[k + j][1] >= 'a' and
                                        text[k + j][1] <= 'z' and (
                                                text[k + j][-1] >= 'a' and text[k + j][-1] <= 'z' or text[
                                            k + j] == ':')):  # first character A-Z, second a-z (avoiding "BOOK REVIEW DIGEST"), last a-z or 0-9 (eg "Adams, Henry, 1838-1918")
                                    if (len(text[k+j]) >= 4): # Sometimes a heading contains no books, but direct to "See other sections"
                                        if (text[k+j][:4] in ['See ','Sec ','Sac ']):
                                            continue
                                    if len(text[j + k]) >=9: # not "xxx-Continued"
                                        if(text[j+k][-9:] in ['Continued','Continucd']):
                                            continue
                                    if (text[k+j] in subheadings or text[k+j] in wrong_headings): # For wrong headings, ignore them
                                        continue
                                    fiction_headings.append(text[k + j]) # Otherwise, add that heading into the list
                                    fiction_books.append([]) # add an empty list to the booklist, to match the headinglist
                                    count += 1 # to count the number of lists in the booklist
                                    # if (len(fiction_headings[-1]) >= 4):  # find next headings
                                    #    if (fiction_headings[-1] == 'Finance'):
                                    #        print text[j+k-25:j+k]
                                    # if len(fiction_headings) >= 2 and fiction_headings[-1] < fiction_headings[-2]: # find abnormal circumstances
                                    #    print fiction_headings[-1]
                                    #    print fiction_headings
                            if (text[j + k] in fiction_headings): # begin to add lines to book list, skip the lines that already in heading list
                                continue
                            elif(count>=0): # if there is already a list in the book list (which means there is already list in headings)
                                fiction_books[count].append(text[j + k]) # add texts into the booklist
                        length=len(fiction_headings)
                        fiction_authors = []  # to store the names of authors
                        fiction_titles = []  # to store the names of titles
                        fiction_time = []  # to store the time of books
                        dictionary=[] # generate a dictionary
                        for k in list(range(length)): # make the four lists have k lists in each
                            fiction_authors.append([])
                            fiction_titles.append([])
                            fiction_time.append([])
                            dictionary.append([])
                        if (length > 0):
                            for k in list(range(length)):
                                #print(fiction_headings[k], fiction_books[k]) # print headings and all the content of each heading
                                count = -1
                                for m in list(range(len(fiction_books[k]))):
                                    #print fiction_books[k][m]
                                    if ((re.match(pattern1, fiction_books[k][m]) != None) or (re.match(pattern1_3,fiction_books[k][m])!=None)): # if the line matches with the regular pattern of "author"
                                        if(re.search(pattern2, fiction_books[k][m][1:])!=None): # the line must contains contents other than author information
                                            flag = re.search(pattern2, fiction_books[k][m][1:]).start() # find where author ends and title starts
                                            fiction_authors[k].append(fiction_books[k][m][:flag])
                                            fiction_titles[k].append(fiction_books[k][m][flag + 1:])
                                            fiction_time[k].append([])
                                            count += 1
                                    elif ((re.match(pattern1_1, fiction_books[k][m]) != None) or (re.match(pattern1_2, fiction_books[k][m]) != None)): # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                        if (re.search(pattern2_1, fiction_books[k][m][1:]) != None):  # a new pattern to match this case, begin with space, then [A-Z][a-z]+, for titles
                                            flag = re.search(pattern2_1,fiction_books[k][m][1:]).start()  # find where author ends and title starts
                                            fiction_authors[k].append(fiction_books[k][m][:flag+1])
                                            fiction_titles[k].append(fiction_books[k][m][flag + 2:])
                                            fiction_time[k].append([])
                                            count += 1
                                    elif ((re.match(pattern1_4, fiction_books[k][m]) != None) or (re.match(pattern1_5, fiction_books[k][m]) != None)):  # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                        if (re.search(pattern2_2, fiction_books[k][m][1:]) != None):  # a new pattern to match this case, begin with comma or colon, then space, then [A-Z][a-z]+, for titles
                                            flag = re.search(pattern2_2, fiction_books[k][m][1:]).start()  # find where author ends and title starts
                                            fiction_authors[k].append(fiction_books[k][m][:flag + 2])
                                            fiction_titles[k].append(fiction_books[k][m][flag + 3:])
                                            fiction_time[k].append([])
                                            count += 1
                                    elif fiction_books[k][m - 1][-1] == '-': # if not matches with the pattern of "author", if last line ends with run-on line signals
                                        if count != -1: # avoid index out of range
                                            fiction_titles[k][count] = fiction_titles[k][count][:-1] + fiction_books[k][m] # deal with run-on lines
                                        else:
                                            continue
                                    else:
                                        if count!=-1: # if not matches with the pattern of "author", and last line not ends with run-on line signal
                                            fiction_titles[k][count] = fiction_titles[k][count] + ' ' + fiction_books[k][m] # deal with regular lines
                                        else:
                                            continue
                                for m in list(range(len(fiction_titles[k]))):
                                    for n in list(range(len(fiction_titles[k][m]))):
                                        if (fiction_titles[k][m][n] == '('): # separate title and time, find where time starts
                                            fiction_time[k][m] = fiction_titles[k][m][n:]
                                            for t in range(len(fiction_time[k][m])): # find where time ends
                                                if(fiction_time[k][m][t]==')'):
                                                    fiction_time[k][m]=fiction_time[k][m][:t+1]
                                                    break
                                            for l in range(n): # find where title ends
                                                if (fiction_titles[k][m][n - l] >= 'a' and fiction_titles[k][m][
                                                    n - l] <= 'z'):
                                                    fiction_titles[k][m] = fiction_titles[k][m][:n - l + 1]
                                                    break
                                            break
                                print(fiction_authors[k])
                                print(fiction_titles[k])
                                print(fiction_time[k])
                                dictionary[k] = dict(zip(fiction_authors[k], fiction_titles[k])) # zip to dictionary
                                print(dictionary[k])
                                #print(fiction_headings[k],'~',len(dictionary[k])) # print number of each genre
                        print(bookcount_fiction)
            else: # for early versions of indexes
                for j in range(linelength):
                    if (text[j] == "Fiction." or text[j]=='Fiction'):
                        bookcount_fiction = 0
                        for k in list(range(1, linelength - j)): # begin to generate a list of headings within fiction
                            if (text[j+k] in nextheadings): # if fiction section ends
                                break
                            if '(' in text[j+k]:
                                bookcount_fiction+=1
                            if len(text[j + k]) > 1 and len(text[k + j]) <= 30 and '(' not in text[
                                k + j] and '\'' not in text[
                                k + j]:  # must be at least 2 characters, no more than 30 characters (avoiding titles not finished in a line to be included, not including '(' to avoid OCR error) # next line beginning with non-characterized character
                                if (text[k + j][0] >= 'A' and text[k + j][0] <= 'Z' and text[k + j][1] >= 'a' and
                                        text[k + j][1] <= 'z' and (
                                                text[k + j][-1] >= 'a' and text[k + j][-1] <= 'z' or text[
                                            k + j] == ':')):  # first character A-Z, second a-z (avoiding "BOOK REVIEW DIGEST"), last a-z or 0-9 (eg "Adams, Henry, 1838-1918")
                                    fiction_headings.append(text[k + j])# add that heading into the list
                                    fiction_books.append([]) # add an empty list to the booklist, to match the headinglist
                                    count+=1 # to count the number of lists in the booklist
                            if (text[j+k] in fiction_headings): # begin to add lines to book list, skip the lines that already in heading list
                                continue
                            elif(count>=0): # if there is already a list in the book list (which means there is already list in headings)
                                fiction_books[count].append(text[j+k])
                            else: # if no headings at all, just add the books under the fiction_books list (this is not possible in well-organized latter versions)
                                fiction_books.append(text[j+k])
                        length=len(fiction_headings)
                        fiction_authors = []  # to store the names of authors
                        fiction_titles = []  # to store the names of titles
                        fiction_time=[] # to store the time of books
                        dictionary=[]
                        for k in list(range(length)): # similar to the operations above
                            fiction_authors.append([])
                            fiction_titles.append([])
                            fiction_time.append([])
                            dictionary.append([])
                        count=-1
                        if(length>0):
                            for k in list(range(length)):
                                for m in list(range(len(fiction_books[k]))):
                                    if ((re.match(pattern1, fiction_books[k][m]) != None) or (re.match(pattern1_3,fiction_books[k][m])!=None)): # if the line matches with the regular pattern of "author"
                                        flag=re.search(pattern2,fiction_books[k][m][1:]).start()
                                        fiction_authors[k].append(fiction_books[k][m][:flag])
                                        fiction_titles[k].append(fiction_books[k][m][flag+1:])
                                        fiction_time[k].append([])
                                        count += 1
                                    elif ((re.match(pattern1_1, fiction_books[k][m]) != None) or (re.match(pattern1_2,fiction_books[k][ m]) != None)):  # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                        if (re.search(pattern2_1, fiction_books[k][m][1:]) != None):  # a new pattern to match this case, begin with space, then [A-Z][a-z]+, for titles
                                            flag = re.search(pattern2_1,fiction_books[k][m][1:]).start()  # find where author ends and title starts
                                            fiction_authors[k].append(fiction_books[k][m][:flag+1])
                                            fiction_titles[k].append(fiction_books[k][m][flag + 2:])
                                            fiction_time[k].append([])
                                            count += 1
                                    elif ((re.match(pattern1_4, fiction_books[k][m]) != None) or (re.match(pattern1_5, fiction_books[k][m]) != None)):  # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                        if (re.search(pattern2_2, fiction_books[k][m][1:]) != None):  # a new pattern to match this case, begin with comma or colon, then space, then [A-Z][a-z]+, for titles
                                            flag = re.search(pattern2_2, fiction_books[k][m][1:]).start()  # find where author ends and title starts
                                            fiction_authors[k].append(fiction_books[k][m][:flag + 2])
                                            fiction_titles[k].append(fiction_books[k][m][flag + 3:])
                                            fiction_time[k].append([])
                                            count += 1
                                    elif (fiction_books[k][m - 1][-1] == '-'):
                                        fiction_titles[k][count] = fiction_titles[k][count][:-1] + fiction_books[k][m]
                                    else:
                                        fiction_titles[k][count] = fiction_titles[k][count] + ' ' + fiction_books[k][m]
                                for m in list(range(len(fiction_titles[k]))):
                                    for n in list(range(len(fiction_titles[k][m]))):
                                        if (fiction_titles[k][m][n] == '('):
                                            fiction_time[k][m] = fiction_titles[k][m][n:]
                                            for t in range(len(fiction_time[k][m])): # find where time ends
                                                if(fiction_time[k][m][t]==')'):
                                                    fiction_time[k][m]=fiction_time[k][m][:t+1]
                                                    break
                                            for l in list(range(n)):
                                                if (fiction_titles[k][m][n - l] >= 'a' and fiction_titles[k][m][
                                                    n - l] <= 'z'):
                                                    fiction_titles[k][m] = fiction_titles[k][m][:n - l + 1]
                                                    break
                                            break
                                print(fiction_headings[k],fiction_books[k])
                            print(fiction_authors[k])
                            print(fiction_titles[k])
                            print(fiction_time[k])
                            dictionary[k] = dict(zip(fiction_authors[k], fiction_titles[k]))
                            print(dictionary[k])
                            print(bookcount_fiction)
                        else:
                            length2=len(fiction_books)
                            for m in list(range(length2)):
                                if ((re.match(pattern1, fiction_books[m]) != None) or (re.match(pattern1_3,fiction_books[m])!=None)): # if the line matches with the regular pattern of "author"
                                    flag = re.search(pattern2, fiction_books[m][1:]).start()
                                    fiction_authors.append(fiction_books[m][:flag])
                                    fiction_titles.append(fiction_books[m][flag+1:])
                                    fiction_time.append([])
                                    count+=1
                                elif ((re.match(pattern1_1, fiction_books[m]) != None) or (re.match(pattern1_2,fiction_books[m]) != None)):  # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                    if (re.search(pattern2_1, fiction_books[m][1:]) != None):  # a new pattern to match this case, begin with space, then [A-Z][a-z]+, for titles
                                        flag = re.search(pattern2_1, fiction_books[m][
                                                                   1:]).start()  # find where author ends and title starts
                                        fiction_authors.append(fiction_books[m][:flag + 1])
                                        fiction_titles.append(fiction_books[m][flag + 2:])
                                        fiction_time.append([])
                                        count += 1
                                elif ((re.match(pattern1_4, fiction_books[m]) != None) or (re.match(pattern1_5, fiction_books[m]) != None)):  # if the line matches with the pattern of "author" with dash (e.g. "Kaye-Smith") or with a prefix (e.g. "McArthur")
                                    if (re.search(pattern2_2, fiction_books[m][1:]) != None):  # a new pattern to match this case, begin with comma or colon, then space, then [A-Z][a-z]+, for titles
                                        flag = re.search(pattern2_2, fiction_books[m][1:]).start()  # find where author ends and title starts
                                        fiction_authors.append(fiction_books[m][:flag + 2])
                                        fiction_titles.append(fiction_books[m][flag + 3:])
                                        fiction_time.append([])
                                        count += 1
                                elif(fiction_books[m-1][-1]=='-'):
                                    fiction_titles[count]=fiction_titles[count][:-1]+fiction_books[m]
                                else:
                                    fiction_titles[count] = fiction_titles[count] +' '+fiction_books[m]
                            for m in list(range(len(fiction_titles))):
                                for n in list(range(len(fiction_titles[m]))):
                                    if(fiction_titles[m][n]=='('):
                                        fiction_time[m]=fiction_titles[m][n:]
                                        for t in range(len(fiction_time[m])):  # find where time ends
                                            if (fiction_time[m][t] == ')'):
                                                fiction_time[m] = fiction_time[m][:t + 1]
                                                break
                                        for l in range(n):
                                            if(fiction_titles[m][n-l]>='a' and fiction_titles[m][n-l]<='z'):
                                                fiction_titles[m] = fiction_titles[m][:n-l+1]
                                                break
                                        break
                            print(fiction_books)
                            print(fiction_authors)
                            print(fiction_titles)
                            print(fiction_time)
                            dictionary=dict(zip(fiction_authors,fiction_titles))
                            print(dictionary)
                            print(bookcount_fiction)
        print(bookcount)
        if flag==0: # if the volume doesn't have an index, print it out and end
            print('Volume number %d: no index found in this volume' %(i+3))
            index_startpage[i]='N/A'
            index_endpage[i] = 'N/A'
        #print bookcount
    #print textlist[3][638]
if __name__ == '__main__':
    main()
import re
TEXT='W‘liliamson, C: N'
pattern1 = re.compile("[A-Z]['‘]*[a-zé§¢ﬂﬁ]+['‘]*[a-zé§¢ﬂﬁ]*[,.:]*\s[A-Z]*\s*[A-Za-z01][,.:]+\s")
pattern2 = re.compile("[A-Z][a-z]+")
if ((re.match(pattern1, TEXT) != None) or (re.match(pattern1,TEXT)!=None)):
    print('arsenal')
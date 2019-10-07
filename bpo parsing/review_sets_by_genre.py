import pandas as pd
import ast

colnames=['id', 'score','review']
data=pd.read_csv('/Users/hu/Desktop/BPO2019fall/bpo parsing/all_fic_reviews.txt',sep='\t',names=colnames, header=None)


r_bpoid_list=[]
r_review_list=[]

df=pd.read_csv('/Users/hu/Desktop/BPO2019fall/bpo parsing/genremeta/biography.tsv',sep='\t')
#print(df.columns) #'author', 'bookid', 'bpoids', 'genres', 'htrcids', 'subjects', 'title','is_fic', 'pubdate'
bpo_handle=df['bpoids'].tolist()
r_bookid_list=df['bookid'].tolist()
set_bpo_handle=[]
for item in bpo_handle:
    #print(type(item)): str
    idset = ast.literal_eval(item)
    #print(type(idset))# to set
    set_bpo_handle.append(idset)

print(len(set_bpo_handle))

list_bpo_handle=[]
for m in set_bpo_handle:
    for n in m:
        #print(type(n))
        list_bpo_handle.append(str(n))
print(len(list_bpo_handle))

for row in data.itertuples():
    #print(type(row.id)):str
    if row.id in list_bpo_handle:
        string=row.review
        r_bpoid_list.append(row.id)
        r_review_list.append(string)
    else:
        pass
print(len(r_review_list),len(r_bpoid_list))


selected= pd.DataFrame(list(zip(r_bpoid_list, r_review_list)),
               columns =['selected_id', 'selected_review'])
#counter=0
final_bpoid_list=[]
final_string_list=[]
for set in set_bpo_handle:
    #print(set)
    #counter=counter+1
    #print(counter)
    final_string = ""
    bpo_id_set = []
    for single in set:
        for row in selected.itertuples():
            if row.selected_id != str(single):
                pass
            else:
                bpo_id_set.append(row.selected_id)
                string=str(row.selected_review)
                #print("h1",len(string))
                final_string=final_string+string
                #print("h2", len(final_string))
    final_string_list.append(final_string)
    final_bpoid_list.append(bpo_id_set)


print(len(final_string_list),len(final_bpoid_list))
output= pd.DataFrame(list(zip(r_bookid_list,final_bpoid_list, final_string_list)),
               columns =['bookid','selected_id', 'selected_review'])
output.to_csv('output.csv')



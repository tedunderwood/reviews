import os
import pandas as pd
import ast
import string as st

#two flles for all genremeta files
colnames=['id', 'score','review']
data=pd.read_csv('all_fic_reviews.txt',sep='\t',names=colnames, header=None)
colnames2=['before', 'after']
replacement_dict=pd.read_csv('Replacement_dict.csv',sep=',',names=colnames2, header=None)
words2r=replacement_dict['before'].tolist()
words2s=replacement_dict['after'].tolist()
#print(len(words2r),len(words2s))

#functions for all
def remove_punctuation(text):
    no_punct="".join([c for c in text if c not in st.punctuation])
    return no_punct

def replace_words(text):
    for i in range(len(words2r)):
        text=text.replace(str(words2r[i]), str(words2s[i]))
    return text


def genremeta_processor(filename):
    #load file
    print(filename)
    df = pd.read_csv(filename, sep='\t')
    # print(df.columns) #'author', 'bookid', 'bpoids', 'genres', 'htrcids', 'subjects', 'title','is_fic', 'pubdate'
    bpo_handle = df['bpoids'].tolist()
    r_bookid_list = df['bookid'].tolist()
    #r_bookid_list = df['bookid'].tolist()
    #get set of bpoids
    set_bpo_handle = []
    for item in bpo_handle:
        # print(type(item)): str
        idset = ast.literal_eval(item)
        # print(type(idset))# to set
        set_bpo_handle.append(idset)
    #get list of bpoids
    list_bpo_handle = []
    for m in set_bpo_handle:
        for n in m:
            # print(type(n))
            list_bpo_handle.append(str(n))
    print("set count:",len(set_bpo_handle),"list count:",len(list_bpo_handle))

    #preprocess the review texts
    r_bpoid_list = []
    r_review_list = []
    for row in data.itertuples():
        # print(type(row.id)):str
        if row.id in list_bpo_handle:
            text = row.review
            #lowercase
            text = text.lower()
            #replace words
            text = replace_words(text)
            #remove punctuations
            string = remove_punctuation(text)
            # print(string)
            r_bpoid_list.append(row.id)
            r_review_list.append(string)
        else:
            pass
    print(len(r_review_list), len(r_bpoid_list))

    selected = pd.DataFrame(list(zip(r_bpoid_list, r_review_list)),
                            columns=['selected_id', 'selected_review'])
    genre_tag=filename.rstrip('.tsv').lstrip('./testdata/')
    genre_tag_list = [genre_tag for i in range(len(r_review_list))]
    final_bpoid_list = []
    final_string_list = []
    for set in set_bpo_handle:
        # print(set)
        # counter=counter+1
        # print(counter)
        final_string = ""
        bpo_id_set = []
        for single in set:
            for row in selected.itertuples():
                if row.selected_id != str(single):
                    pass
                else:
                    bpo_id_set.append(row.selected_id)
                    string = str(row.selected_review)
                    # print("h1",len(string))
                    final_string = final_string + string
                    # print("h2", len(final_string))
        final_string_list.append(final_string)
        final_bpoid_list.append(bpo_id_set)

    print(len(final_string_list),len(final_bpoid_list))
    output = pd.DataFrame(list(zip(r_bookid_list,final_bpoid_list, final_string_list,genre_tag_list)),
                          columns=['bookid', 'selected_id', 'selected_review', 'genre'])
    return output

if __name__ == '__main__':
    # Load the genremeta files
    filenames = []
    directory = os.walk("./genremeta")
    for path, dir_list, file_list in directory:
        for file_name in file_list:
            print(file_name)
            if str(file_name)=='contrast_sizes.tsv':
                print("here we ignore this file: ",file_name)
            else:
                if file_name[-3:] == 'tsv':
                    filenames.append(file_name)
                    file = os.path.join(path, file_name)
                else:
                    print("File format wrong: ",file_name)
                    # raise TypeError("File format wrong")
    print(filenames)
    for filename in filenames:
        filepath = './genremeta/' + filename
        output = genremeta_processor(filepath)
        output_filename = filename.rstrip('.tsv') + "_output.tsv"
        print(output_filename)
        path = '/Users/hu/Desktop/BPO2019fall/parsingBPO/bpo parsing/results'
        output_file = os.path.join(path, output_filename)
        output.to_csv(output_file, index=False)

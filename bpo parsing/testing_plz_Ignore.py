import string as st
import pandas as pd
import os
from nltk.tokenize import word_tokenize
from collections import Counter
#tokenize and word count
string = "hey you are great great great"
tokens = word_tokenize(string)
print(tokens)
print(string.split())
total_token = len(tokens)
print(len(string.split()), total_token)

    # review_length.append(total_token)
    # token_counts = Counter(tokens).most_common()  # a list
    # token_counts_output.append(token_counts)
    # norm_list_per_review = []
    # for cp in token_counts:
    #     # print(cp[1])
    #     norm_value = float(cp[1] / total_token)
    #     norm_list = [cp[0], norm_value]
    #     norm_list_per_review.append(norm_list)
    # token_norm_output.append(norm_list_per_review)

# for a in token_counts_output:
#     print(a)
# for b in token_norm_output:
#     print(b)
# add new list to df




# str = "This &is [an] example? √¶ra's ,√¶sthetics erarie,eyrie √¶ra's,airy{of} string. with.? punctuation!!!!" # Sample string
# str=str.lower()
# print(str)
# list1=["√¶sthetics"]
# list2=['era']
# # print(str.replace(list1[0], list2[0]))
# import os
# filenames = []
# directory = os.walk("./testdata")
# for path, dir_list, file_list in directory:
#     print(path,)
#     for file_name in file_list:
#         file = os.path.join(path, file_name)
#         if file_name[-3:] == 'tsv':
#             filenames.append(file_name)
#         else:
#             raise TypeError("File format wrong")
# print(filenames)
#
# for filename in filenames:
#     filepath = './testdata' + filename
#     filepath
# # output = analyze_sculptures(block_filenames, shape_filenames)
# # print(output)


# list1=['hi','hi','hi']
# list2=['de','de','de']
# output = pd.DataFrame(list(zip(list1,list2)),columns=['1', '2'])
# fliename='biography.tsv'
# output_filename = fliename.rstrip('.tsv') + "_output.tsv"
# print(output_filename)
# path='/Users/hu/Desktop/BPO2019fall/parsingBPO/bpo parsing/results'
# print('hi')
# output_file = os.path.join(path,output_filename)
# print('hi2')
# output.to_csv(output_file, index=False)

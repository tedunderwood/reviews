import os
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
#word_tokenize accepts a string as an input, not a file.
#stop_words = set(stopwords.words('english'))

def token_norm(df):
    token_counts_output = []
    review_length = []
    token_norm_output = []

    for row in df.itertuples():
        token_count = []
        string = row.selected_review
        tokens = word_tokenize(string)
        total_token = len(string.split())
        review_length.append(total_token)
        token_counts = Counter(tokens).most_common()  # a list
        token_counts_output.append(token_counts)
        norm_list_per_review = []
        for cp in token_counts:
            # print(cp[1])
            norm_value = float(cp[1] / total_token)
            norm_list = [cp[0], norm_value]
            norm_list_per_review.append(norm_list)
        token_norm_output.append(norm_list_per_review)
    print(len(token_counts_output), len(review_length), len(token_norm_output))
    # for a in token_counts_output:
    #     print(a)
    # for b in token_norm_output:
    #     print(b)
    # add new list to df
    df['length'] = review_length
    df['token_counts'] = token_counts_output
    df['norm_token_counts'] = token_norm_output
    return df

if __name__ == '__main__':
    # Load the genremeta files
    filenames = []
    directory = os.walk("./results")
    for path, dir_list, file_list in directory:
        for file_name in file_list:
            print(file_name)
            if file_name[-3:] == 'tsv':
                filenames.append(file_name)
                file = os.path.join(path, file_name)
            else:
                print("File format wrong: ",file_name)
                # raise TypeError("File format wrong")
    print(filenames)
    for filename in filenames:
        filepath = './results/' + filename
        df=pd.read_csv(filepath)
        output = token_norm(df)
        output_filename = filename.rstrip('.tsv') + "_final.tsv"
        print(output_filename)
        path = '/Users/hu/Desktop/BPO2019fall/parsingBPO/bpo parsing/final_results'
        output_file = os.path.join(path, output_filename)
        output.to_csv(output_file, index=False)





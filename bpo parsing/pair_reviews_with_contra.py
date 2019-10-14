import pandas as pd
import os

def get_df(filename):
    df = pd.read_csv(filename)
    print(df.head())
    return df

df_list=[]
if __name__ == '__main__':
    filenames = []
    directory = os.walk("./results")
    for path, dir_list, file_list in directory:
        for file_name in file_list:
            if file_name[-3:] == 'tsv':
                filenames.append(file_name)
                file = os.path.join(path, file_name)
            else:
                # print("File format wrong: ",file_name)
                pass
                # raise TypeError("File format wrong")
        #print(filenames)
        for filename in filenames:
            filepath = './results/' + filename
            output = get_df(filepath)
            df_list.append(pd)
    print(len(df_list))

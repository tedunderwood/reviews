import pandas as pd
import os
def resample(filename):
    df = pd.read_csv(filename)
    # Randomly sample 70% of your dataframe
    # df_percent = df.sample(frac=0.7)
    # Randomly sample 7 elements from your dataframe
    df_subset = df.sample(n=135)
    df_subset.to_csv('demo_sample.csv')
    return df_subset


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
        print(filenames)
        for filename in filenames:
            filepath = './results/' + filename
            output = resample(filepath)
            output_filename = filename.rstrip('.tsv') + "_sample.tsv"
            print(output_filename)
            path = '/Users/hu/Desktop/BPO2019fall/parsingBPO/bpo parsing/samples135'
            output_file = os.path.join(path, output_filename)
            output.to_csv(output_file, index=False)
            print("done")

import pandas as pd
import string as st
df=pd.read_csv('/Users/hu/Desktop/BPO2019fall/parsingBPO/bpo parsing/output_sample_biography.csv')
#print(df.head())
#print(df['selected_review'])

text=df['selected_review'][3]


def remove_punctuation(string):
    no_punct="".join([c for c in text if c not in st.punctuation])
    return no_punct

text2=remove_punctuation(text)
print(text2)
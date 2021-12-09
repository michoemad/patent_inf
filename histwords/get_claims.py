PATH = "sunny-victor-323903-99ca9a609b49.json"
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH
from google.cloud import bigquery
import pandas as pd
import numpy as np
from representations.sequentialembedding import SequentialEmbedding
import viz.common as common
import nltk


nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('averaged_perceptron_tagger')


def get_decade(year,limit=9999999):
    project_id = 'sunny-victor-323903'
    client = bigquery.Client(project=project_id)
    dataset_id = "patents"
    df = client.query('''
    SELECT A.patent_id FROM 
    `patents-public-data.patentsview.application` AS A

    WHERE SUBSTR(A.date , 1, 4) >= "%d" AND
    SUBSTR(A.date , 1, 4) <= "%d"
    ORDER BY RAND()
    LIMIT %d
    ''' % (year,year+10,limit))
    df = df.to_dataframe()
    vals = df.to_numpy().astype(str)

    vals = "("+ np.array2string(vals,separator=",",formatter={'int':lambda x: int(x)}).replace("[","").replace("]","")  +")"
    # print(vals)
    df = client.query('''
    SELECT patent_id,text FROM
    `sunny-victor-323903.patents.claims_%d` 

    WHERE patent_id IN %s
    ''' % (year%100,vals))

    df = df.to_dataframe()
    # df.to_csv("temp.csv")
    # df = df.astype(str)
    df.text.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
    df['text'] = df['text'].str.encode('utf-8')
    df = df[["patent_id","text"]]
    # df = df.set_index('patent_id', append=True).swaplevel(0,1)
    df["text"] = df.groupby(['patent_id'])['text'].transform(lambda x: ' '.join(x))
    df = df.drop_duplicates()
    # Now we get the patents from the dataset
    return df


def embed_sample(df,year):
    # Now we simply apply either max or average aggregation to each claim
    seq_embeddings = SequentialEmbedding.load("eng-all", range(1970,2000,10))
    # Clean
    # df["text"]=df["text"].apply(common.full_clean)
    # 2 modes of word-diff
    # df["scores_avg"]=df["text"].apply(common.words_diff_avg,args=(year,year+10,seq_embeddings))
    df["scores_min"]=df["text"].apply(common.words_diff_min,args=(year,year+10,seq_embeddings))
    # Keep the OG patents as stock
    return df

import ast
def get_word_scores(df,year):
  # Now we simply apply either max or average aggregation to each claim
  seq_embeddings = SequentialEmbedding.load("eng-all", range(1970,2000,10))
  words = dict()
  arr = df["text"].to_numpy()
  big = []
  words = dict()
  for x in arr:
    x= ast.literal_eval(x)
    big.extend(x)
  big = pd.unique(big)
  for y in big:
    words[y]=common.words_diff_min(y,year,year+10,seq_embeddings)
  return words


seq_embeddings = SequentialEmbedding.load("eng-all", range(1970,2000,10))
inf = pd.read_csv("Results\coha\infringements.csv",index_col="patent_id")
ans = []
for _,x in inf.iterrows():
  if(int(x["date"]) == 1990):
    ans.append(-1)
    continue
  ans.append(common.words_diff_min(x["text"],int(x["date"]),int(x["date"])+10,seq_embeddings))
# print(ans)
inf["score_min"] = ans
inf.to_csv("infringements.csv")
# for year in range(1970,2000,10):
  # df = pd.read_csv("sample_claims_%d.csv"%year)
  # words = get_word_scores(df,year)
  # df_word = pd.DataFrame.from_dict(words,orient="index")
  # df_word.to_csv("sample_words_%d.csv"%year)
# year=1980
# df=get_decade(year,limit=1000)
# df.to_csv("sample_claims_%d.csv"%year)

# year=1970
# df=get_decade(year,limit=1000)
# df.to_csv("sample_claims_%d.csv"%year)
# df = embed_sample(df,year)

# for year in range(1970,1991,10):
#   df = pd.read_csv("sample_claims_%d.csv"%year)
#   df["text"]=df["text"].apply(common.full_clean)
#   df.to_csv("sample_claims_%d.csv"%year)
  # df = embed_sample(df,year)
  # df.loc[:,["patent_id","scores_min"]].to_csv("sample_scores_%d.csv"%(year))

# a = "Hi abdo salar"
# print(set(a.split()))

def get_single_patent(pub_no,table_id,column):
    project_id = 'sunny-victor-323903'
    client = bigquery.Client(project=project_id)
    dataset_id = "patents"
    df = client.query('''
      SELECT
        publication_number,%s
      FROM
        `%s.%s`
      WHERE publication_number=%d
      LIMIT %d
    ''' % (column,dataset_id,table_id,pub_no))
    return df

def get_min_year(year,table_id):
    project_id = 'sunny-victor-323903'
    client = bigquery.Client(project=project_id)
    dataset_id = "patents"
    df = client.query('''
      SELECT
        MIN(GRANT_DATE)
      FROM
        `%s.%s`
    ''' % (dataset_id,table_id))
    return df

"""
We need a testbench that takes some patent and computes the average semantic change in the claims text..
We should have two variations (max and avg)
We then use these numbers on patents related to infringements and on random samples
"""

# Testing, try one patent first then make the code bigger
# get_single_patent(4845481)
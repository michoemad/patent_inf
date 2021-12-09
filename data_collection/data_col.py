
from google.cloud import bigquery
import os
import pandas as pd
import numpy as np

class data_col:
  # On init, change the project_id
  def __init__(self,project_id):
    JSON_FILE = "careful-lock-334103-b2599c42ca05.json"
    tpath = os.path.dirname(os.path.realpath(__file__))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(tpath,JSON_FILE)
    self.project_id = project_id
    self.client = bigquery.Client(project=project_id)

  # this function will take a table and columsn and return them in a df
  # tname is assumed to be anything
  # cols is an iterable of col names
  # args is for extra statemtns we want to add to the query
  def get_table(self,tname,cols,args=""):
    cols = ",".join(cols) if type(cols)!=str else cols
    df = self.client.query('''
    SELECT %s FROM
    `%s` 
    %s
    ''' % (cols,tname,args))
    df = df.to_dataframe()
    return df
  
  def run_query(self,query):
    df = self.client.query(query)
    return df.to_dataframe()

  # gets decade from the big patentsview dataset
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

import os,sys
tpath = os.path.dirname(os.path.realpath(__file__))
# mpath = os.path.abspath(os.path.join(tpath, "../"))
tpath = os.path.abspath(os.path.join(tpath, "../histwords"))
sys.path.append(tpath)
# sys.path.append(mpath)
import representations.embedding
import data_col as data_col
import data_clean as data_clean
import pandas as pd
# data = data_col.data_col("careful-lock-334103")
# df = data.get_table("careful-lock-334103.patents.claims_70",["patent_id","text"],"LIMIT 1000")
# df.set_index("patent_id",inplace=True)
# df.to_csv("test.csv")

# Assume we have a df of texts and we want to clean it

# 1) rean clean on text
# 2) split to get arrays
df = pd.read_csv("../test.csv",index_col="patent_id")
data_clean.clean_df_split(df,"text")
df.to_csv("../test.csv",index=True)

# print(df["text"])
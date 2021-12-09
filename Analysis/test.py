import pandas as pd
import os,sys
import scores
from scores import SequentialEmbedding
import ast
import numpy as np
# tpath = os.path.dirname(os.path.realpath(__file__))
# tpath = os.path.abspath(os.path.join(tpath, "../histwords"))
# sys.path.append(tpath)
# print(sys.path)
# df = pd.read_csv("../test.csv",index_col="patent_id")
# df["text"] = df["text"].apply(ast.literal_eval)
# df.to_pickle("pick.csv")

# Let's always save in pickle
df = pd.read_pickle("pick.csv")

df = df.iloc[:5]

embeds = SequentialEmbedding.load("../histwords/eng-all",range(1970,2000,10))
score = scores.Scores(embeds)
df["years"] = np.random.randint(0,3,size=len(df))*10+1970
df["text"] = df["text"].apply(np.unique)
# print(test)
# score.get_semantic_shift_multi(test,1970,1990,3)
# vals = score.get_semantic_df(df,"text","years",1990,3)

text_year = df.loc[:,("text","years")].to_numpy()
# text_year = np.stack(text_year)
# print(text_year[:,1])
# test = lambda x: 
# test(text_year)
# print(text_year[:,0][0])
vec = lambda x,y: score.get_semantic_shift_multi(x[:5],y,1990,3)
vec = np.vectorize(vec)
vals = vec(text_year[:,0],text_year[:,1])
df["scores"]=vals
# text_year = np.apply_over_axes(vec,text_year,axes=[0,1])
# print(vec)
# df["scores"] = vals
# df["scores"] = df.apply(lambda x: score.get_semantic_shift_m,lti(x["text"],1970,1990,3),axis=1)
# print(df)

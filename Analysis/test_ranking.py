import ranking
import imports
import pandas as pd
import sys,os
import numpy as np
tpath = os.path.dirname(os.path.realpath(__file__))
tpath = os.path.abspath(os.path.join(tpath, "../histwords"))

sys.path.append(tpath)
from representations.sequentialembedding import SequentialEmbedding

df = pd.read_pickle("pick.csv")
# df = df.iloc[:50]
embeds = SequentialEmbedding.load("../histwords/eng-all",range(1970,2000,10))
df["text"] = df["text"].apply(np.unique)
df["years"] = np.random.randint(0,3,size=len(df))*10+1970

# text_year = df.loc[:,("text","years")].to_numpy()
vec = lambda x,y: ranking.rank_words_sort(x,y,1990,3)
df["text"] = df.apply(lambda x: ranking.rank_words_sort(x["text"],x["years"],1990,embeds),axis=1)
print(df)
# vec = np.vectorize(vec)
# vec(text_year[:,0],text_year[:,1])
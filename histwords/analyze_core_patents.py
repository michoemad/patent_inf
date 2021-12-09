import glob
from viz import common
import pandas as pd
from representations.sequentialembedding import SequentialEmbedding
# df = pd.DataFrame.from_dict(D,columns=["text"],orient="index")


EMBEDS = "eng-all"
seq_embeddings = SequentialEmbedding.load(EMBEDS, range(1970,2000,10))
Dates = {}
Dates[1990]= [5224216,6054561]
Dates[1980]= [4751578]
Dates[1970]=[4342854]

# for key,val in Dates.items():
#     Dates[key] = map(lambda x: str(x),val)
fname = "Results\eng-all\samples\infringements_lite.csv"
df = pd.read_csv(fname,index_col="patent_id")

# df = df[["text"]]
# print(df)
# Sort first 

# df.loc[Dates[1990],"text"] = df.loc[Dates[1990]]["text"].apply(common.sort_words,args=(1990,2000,seq_embeddings))
df.loc[Dates[1980],"text"] = df.loc[Dates[1980]]["text"].apply(common.sort_words,args=(1980,1990,seq_embeddings))
df.loc[Dates[1970],"text"] = df.loc[Dates[1970]]["text"].apply(common.sort_words,args=(1970,1980,seq_embeddings))

# print(df)
# for k in range(3,12,2):
#     st = "top_{}_score".format(k)
#     df.loc[:,st]=0 
#     df.loc[Dates[1990],st] = df.loc[Dates[1990]]["text"].apply(common.words_diff_k,args=(1990,2000,seq_embeddings,k))
#     df.loc[Dates[1980],st] = df.loc[Dates[1980]]["text"].apply(common.words_diff_k,args=(1980,1990,seq_embeddings,k))
#     df.loc[Dates[1970],st] = df.loc[Dates[1970]]["text"].apply(common.words_diff_k,args=(1970,1980,seq_embeddings,k))


# df.loc[:,"score_max"]=0 
# df.loc[Dates[1990],"score_max"] = df.loc[Dates[1990]]["text"].apply(common.words_diff_max,args=(1990,2000,seq_embeddings))
# df.loc[Dates[1980],"score_max"] = df.loc[Dates[1980]]["text"].apply(common.words_diff_max,args=(1980,1990,seq_embeddings))
# df.loc[Dates[1970],"score_max"] = df.loc[Dates[1970]]["text"].apply(common.words_diff_max,args=(1970,1980,seq_embeddings))

df.to_csv(fname)

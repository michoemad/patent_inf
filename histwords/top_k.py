import pandas as pd
from viz import common
from representations.sequentialembedding import SequentialEmbedding
import os

# This module is for computing the top k classes of a given document


# Assumes input is a df with a column called text holding the worcs
def sort_words(year,embeds,df):
    df["text"] = df["text"].apply(common.sort_words,args=(year,year+10,embeds))
    return df


# Set vars
year = 1970
EMBEDS = "eng-all"
flag_dir = "eng-all"
BASE_DIR = "Results\{}\samples".format(flag_dir)
CLAIMS_DIR = "Results\samples"
# Load stuff
seq_embeddings = SequentialEmbedding.load(EMBEDS, range(1970,2000,10))
fname = os.path.join(CLAIMS_DIR,"sample_claims_{}.csv".format(year))
df = pd.read_csv(fname,index_col="patent_id")

# operations
df = sort_words(year,seq_embeddings,df)
df.to_csv(os.path.join(BASE_DIR,"sample_sorted_{}.csv".format(year)))
# # geneate scores based on k
# try k (3,11,2)

# store top 10 words for now
# f = pd.read_csv("Results\eng-all\samples\sample_sorted_{}.csv".format(year),index_col="patent_id")

for k in range(3,11,2):
    df["score"] = df["text"].apply(common.words_diff_k,args=(year,year+10,seq_embeddings,k))
    df.to_csv(os.path.join(BASE_DIR,"sample_scores_k={}_{}.csv".format(flag_dir,k,year)),columns=["score"])
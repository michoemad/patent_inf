
# 1) Imprort data
# 2) run cleaning on the correct columns + splitting
# 3) sort words
# 4) get scores from sorted wrods
# 5) aggregate results 
import os,sys
import pandas as pd

# def add_paths():
tpath = os.path.dirname(os.path.realpath(__file__))
hpath = os.path.abspath(os.path.join(tpath, "../"))
apath = os.path.abspath(os.path.join(tpath, "../histwords"))
# dpath = os.path.abspath(os.path.join(tpath, "../data_collection"))
sys.path.append(hpath)
sys.path.append(apath)
import helpers
import data_collection.data_clean as data_clean
import Analysis.ranking as ranking
import Analysis.scores as scores
from representations.sequentialembedding import SequentialEmbedding
# Will do this for both embeddings
# Embedding data
EMBED = "eng-all"
EMBED_PATH = "../histwords"
START_YEAR = 1960
END_YEAR = 1990 #inclusive
DATES = range(START_YEAR,END_YEAR+10,10)

DATA_PATH = "../Data"
embeds = SequentialEmbedding.load(os.path.join(EMBED_PATH,EMBED),DATES)
# # Load data and clean
def load_and_clean(fname,index_colname,text_colname,date_colname):
    df = pd.read_csv(fname,index_col=index_colname)
    data_clean.clean_df_split(df,text_colname)
    data_clean.remove_duplicates(df,text_colname)
    df[date_colname] = df[date_colname]//(10**4)
    return df
    
# Now that we have clean and duplicate free text
def rank_words(df,text_colname,date_colname,end_year,embeds):
    ranking.rank_words_df(df,text_colname,date_colname,end_year,embeds)

# Returns array with all scores with the same df order
def gen_scores(df,text_colname,date_colname,end_year,k,embeds):
    # Now we get score of top k
    scorer = scores.Scores(embeds)
    # Adds a "score" column to the pasesd in df
    return scorer.get_semantic_df(df,text_colname,date_colname,end_year,k)

def approximate_decade(df,date_colname):
    df[date_colname] = df[date_colname] - df[date_colname]%10

# Let colnames = [text_colname,index_colname,date_colname,new_col,class_colname]
def run_experiment(fname,colnames,k,save_checkpoint=False):
    text_colname,index_colname,date_colname,new_col,class_colname = colnames
    df = load_and_clean(fname,index_colname,text_colname,date_colname)
    # checkpoint
    if (save_checkpoint):
        df.to_csv(fname.split(".")[0]+"_clean.csv")
    # Remove irrelevant times
    df = df[df[date_colname]<END_YEAR+10]
    approximate_decade(df,date_colname)
    rank_words(df,text_colname,date_colname,END_YEAR,embeds)
    if (save_checkpoint):
        df.to_csv(fname.split(".")[0]+"_ranked.csv")
    vals = gen_scores(df,text_colname,date_colname,END_YEAR,k,embeds)
    df[new_col]=vals
    fin = df.groupby(class_colname)[[new_col]].agg("mean")
    return fin

if __name__ =="__main__":
    # df.to_pickle("temp.csv")
    # df = pd.read_pickle("temp.csv")
    fin = run_experiment("../Data/all_cats.csv",
    # Let colnames = [text_colname,index_colname,date_colname,new_col,class_colname]
    colnames=["claims","patent_id","filing_date","scores","subclass_id"],
    k=5,save_checkpoint=True)
    print(fin)
    # print(df["claims"])
    # Aggregate step

    # print(fin)
    # # Save our results
    fin.to_csv("../Data/all_cats_processed.csv")


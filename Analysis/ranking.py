import imports
import numpy as np
# Here we establish functions for ranking words over time and doing so in bulk

def word_diff(word,year,end_year,seq_embeddings):
    # fiction_embeddings = SequentialEmbedding.load("eng-all", (year,end_year))
    x=seq_embeddings.get_embed(year).represent(word)
    y=seq_embeddings.get_embed(end_year).represent(word)
    return x.dot(y)

def is_zero(word,embeds,year,end_year):
    x=embeds.get_embed(year).represent(word)
    y=embeds.get_embed(end_year).represent(word)
    if ((np.all(x==0) or np.all(y==0))):
        return False
    return True

# rank a list by their words, ascending -> first k words are the most changing
# words is a numpy array for efficiency
def rank_words_sort(words,year,end_year,embeds):
    words = filter(lambda x: is_zero(x,embeds,year,end_year),words)
    ans = sorted(words,key=lambda x: word_diff(x,year,end_year,embeds))
    return ans

# rank a list by their words, ascending -> first k words are the most changing
# words is a numpy array for efficiency
def rank_words_df(df,text_colname,year_colname,end_year,embeds):
    df[text_colname] = df.apply(lambda x: rank_words_sort(x[text_colname],x[year_colname],end_year,embeds),axis=1)
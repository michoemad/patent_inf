
import os,sys
tpath = os.path.dirname(os.path.realpath(__file__))
tpath = os.path.abspath(os.path.join(tpath, "../histwords"))

sys.path.append(tpath)

from representations.sequentialembedding import SequentialEmbedding
import numpy as np
class Scores:
    # Assume embeds are loaded outside for simplicity
    def __init__(self,embeds):
        self.embeds = embeds
        self.cache = dict()
    # for one word and a given year, returns a list of NN
    def get_NN(self,word,year):
        NN= self.embeds.get_embed(year).closest(word,year)
        if (NN[0][0]==0):
            return []
        return NN
    # For many words
    def get_NN_multi(self,words,year):
        res = []
        for word in words:
            res.append(self.get_NN(word,year))
        return res
    # for a given word, year compute its semantic score
    # n is number of neighbors to fetch
    # Remember, the higher the score, the more change has occured

    # We def need memoization :)
    def get_semantic_shift(self,word,init_year,final_year,n):
        if ((word,init_year) in self.cache.keys()):
            return self.cache[(word,init_year)]
        x=self.embeds.get_embed(init_year).represent(word)
        y=self.embeds.get_embed(final_year).represent(word)
        if ((np.all(x==0) or np.all(y==0))):
            return np.nan
        NN1 = self.embeds.get_embed(init_year).closest(word,n=n)
        NN2 = self.embeds.get_embed(final_year).closest(word,n=n)
        NN1 = set(NN1)
        NN2 = set(NN2)

        size_intersection = float(len(NN1.intersection(NN2)))
        size_union = len(NN1)+len(NN2)-size_intersection
        score = 1.0 - (size_intersection/size_union)
        self.cache[(word,init_year)]=score
        return score
    
    # Do the same given a list of words
    def get_semantic_shift_multi(self,words,init_year,final_year,n):
        # Given a list of words, get the average semantic score
        # print(init_year)
        # print(words,init_year,final_year)
        score = 0
        vec = lambda x: self.get_semantic_shift(x,init_year,final_year,n)
        vec = np.vectorize(vec)
        words = np.array(words,dtype=str)
        # print(words,init_year)
        res = vec(words)
        # print(res[~np.isnan(res)])
        scores = np.mean(res[~np.isnan(res)])
        return scores
    
    # Returns a series with scores for each entry in a df
    # Apply on top k words
    def get_semantic_df(self,df,text_col,years_col,final_year,k):
        text_year = df.loc[:,(text_col,years_col)].to_numpy()
        vec = lambda x,y: self.get_semantic_shift_multi(x[:k],y,final_year,k)
        vec = np.vectorize(vec)
        vals = vec(text_year[:,0],text_year[:,1])
        return vals
        # df["scores"]=vals
        # return df.apply(lambda x:
        # self.get_semantic_shift_multi(x[text_col],x[years_col],final_year,n),axis=1)
    
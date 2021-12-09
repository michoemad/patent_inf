# Clean claim text and make a set of words
# from typing import Dict
import nltk
from itertools import chain
from nltk.corpus import wordnet
from nltk.corpus import verbnet, stopwords
from nltk.stem import WordNetLemmatizer
from viz.scripts.closest_over_time_chain import get_closest_time

import collections
import csv
import argparse
import pandas as pd
import viz.common as common
import numpy as np
import glob
import os,re
from representations.sequentialembedding import SequentialEmbedding
import operator
# OUT_DIR=""
def word_diff(words,year,end_year):
    fiction_embeddings = SequentialEmbedding.load("eng-all", (year,end_year))
    scores = dict()
    for word in words:
        x=fiction_embeddings.get_embed(year).represent(word)
        y=fiction_embeddings.get_embed(end_year).represent(word)
        if (not (np.all(x==0) or np.all(y==0))):
            scores[word]=x.dot(y)
    scores = sorted(scores.items(), key=operator.itemgetter(1))
    return scores


def write_results(F,fname):
    with open(fname + '.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in F:
            writer.writerow([key, value])


def get_NN_word(word,year,n):
    F = embeds.get_embed(year).closest(word,n)
    # M = sorted(F.items(),key=lambda x: x[1])
    # print(F)
    if(F[0][0]==0):
        return
    write_results(F,"Results/eng-all/words/%s_%d"%(word,year))

def read_csv(fname):
    res = []
    with open(fname, 'r') as csv_file:  
        reader = csv.reader(csv_file)
        for val,key in reader:
            res.append(key)
    return res

## Combine files
def combine_files(word):
    dic = dict()
    for year in range(1970,2001,10):
        fname = "Results/coha/words/%s_%d.csv"%(word,year)
        if (os.path.exists(fname)):
            dic[year]=read_csv(fname)
    return dic
words = ["peripheral", "diskette", "disk","signal","ram","mixer","solid polymer", "polypropylene",
"monoclonal","antibody"]
# for word in words:
#     # read_csv("Results/eng-all/words_nn/%s_%d.csv"%(word,year))
#     dic = combine_files(word)
#     write_results(dic.items(),"Results/coha/words/%s_all"%word)


# for word in words:
#     for year in range(1970,2000,10):
#         get_NN_word(word,year,10)

# Now draw:
words = "coha-word"
embeds = SequentialEmbedding.load(words, range(1840,2000,10))
# for word in words:
get_closest_time("port",words,embeds)
get_closest_time("io",words,embeds)
get_closest_time("flash",words,embeds)
get_closest_time("connect",words,embeds)

# | Patent ID | Words | Year |
# | --- | --- | --- |
# | US5224216A | peripheral, diskette, disk | 1991 |
# | US4751578A | Signal, RAM, mixer | 1985 |
# | US4342854A | Solid polymer, polypropylene | 1971 |
# | US6054561A | monoclonal, antibody | 1995 |
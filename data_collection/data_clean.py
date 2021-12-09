# Clean claim text and make a set of words
# from typing import Dict
# CLAIM_DIR = "claims/"
import nltk
from nltk.corpus import verbnet, stopwords,wordnet
from nltk.stem import WordNetLemmatizer
import argparse
# import pandas as pd
import numpy as np
import glob
import os,re
from representations.sequentialembedding import SequentialEmbedding
import operator
import collections

from itertools import chain

claim_dates = {"io":1990,"dna":1980,"floor":1980,"antigen":1990}

cached = stopwords.words("english")
punctuation = [".", ",", "'", "\"", ":", ";", "?", "(", ")", "[", "]"]

def remove_stopwords(in_str):
    return " ".join([x for x in in_str.split() if x not in cached]) 

def remove_unwanted_chars(text):
    # text = text.encode('ascii',errors='ignore') # Remove non-ascii
    no_brackets = re.sub("([\(\[]).*?([\)\]])", "", text)
    # no_digits = re.sub("\d+\.*\d*%*", "", no_brackets)
    no_newlines = re.sub("\n|\t", "", no_brackets)
    no_newlines = re.sub(r'[^A-Za-z0-9\- ]+', '', no_newlines)
    no_punc = "".join([ch for ch in no_newlines if ch not in punctuation])
    return no_punc.lower()

tag_dict = {"J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV}
def lemma(text,lemmatizer):
    # nltk.pos_tag(nltk.word_tokenize(texts))
    res = []
    for y in nltk.pos_tag(nltk.word_tokenize(text)):
        lem = lemmatizer.lemmatize(y[0],pos=tag_dict.get(y[1][0], wordnet.NOUN))
        res.append(lem)
    return " ".join(res)

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
    # print(fiction_embeddings.get_subembeds(["gay","lesbian"]).embeds[1960].represent("gay"))

# This function is for cleaning normal text, not vectorized
def clean_text(text):
    lemmatizer = WordNetLemmatizer()
    clean = lemma(remove_stopwords(remove_unwanted_chars(text)),lemmatizer)
    return clean

# Given a df and a colname, clean the colname and split the text
def clean_df_split(df,colname):
    df[colname]=df[colname].apply(clean_text)
    df[colname] = df[colname].str.split()

def remove_duplicates(df,colname):
    df[colname] = df[colname].apply(np.unique)

# sub = "io"
# year,end_year = claim_dates[sub],claim_dates[sub]+10
# # year,end_year = 1980,2000

# fname="claim_"+sub
# claim = open(os.path.join(CLAIM_DIR,fname+".txt"),"r")
# claim_text = claim.read()

# Clean claim text and make a set of words
# from typing import Dict
import nltk
from itertools import chain
from nltk.corpus import wordnet
from nltk.corpus import verbnet, stopwords
from nltk.stem import WordNetLemmatizer
import collections

import argparse
# import pandas as pd
import numpy as np
import glob
import os,re
from representations.sequentialembedding import SequentialEmbedding
import operator


CLAIM_DIR = "claims/"

claim_dates = {"io":1990,"dna":1980,"floor":1980,"antigen":1990}

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('averaged_perceptron_tagger')
cached = stopwords.words("english")
punctuation = [".", ",", "'", "\"", ":", ";", "?", "(", ")", "[", "]"]

def remove_stopwords(in_str):
    return " ".join([x for x in in_str.split() if x not in cached]) 

def remove_unwanted_chars(text):
    no_brackets = re.sub("([\(\[]).*?([\)\]])", "", text)
    # no_digits = re.sub("\d+\.*\d*%*", "", no_brackets)
    no_newlines = re.sub("\n|\t", "", no_brackets)
    # no_newlines = re.sub(r'[^A-Za-z0-9 ]+', '', no_newlines)
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

sub = "io"
year,end_year = claim_dates[sub],claim_dates[sub]+10
# year,end_year = 1980,2000

fname="claim_"+sub
claim = open(os.path.join(CLAIM_DIR,fname+".txt"),"r")
claim_text = claim.read()
lemmatizer = WordNetLemmatizer()

clean = lemma(remove_stopwords(remove_unwanted_chars(claim_text)),lemmatizer)
clean = clean.split(" ")
import csv
scores = word_diff(set(clean),year,end_year)
# to_csv
with open(os.path.join(CLAIM_DIR,fname+"_"+str(year)+"-"+str(end_year) + '.csv'), 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in scores:
       writer.writerow([key, value])
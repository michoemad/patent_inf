
import os,sys
import ast
import pandas as pd


tpath = os.path.dirname(os.path.realpath(__file__))
tpath = os.path.abspath(os.path.join(tpath, "../histwords"))

sys.path.append(tpath)
from representations.sequentialembedding import SequentialEmbedding

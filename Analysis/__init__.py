__author__ = 'User'
import os,sys
tpath = os.path.dirname(os.path.realpath(__file__))
dpath = os.path.abspath(os.path.join(tpath, "../data_collection"))
tpath = os.path.abspath(os.path.join(tpath, "../histwords"))

sys.path.append(dpath)
sys.path.append(tpath)

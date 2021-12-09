import pandas as pd
import numpy as np
from scipy import stats
from representations.sequentialembedding import SequentialEmbedding
from top_k import BASE_DIR
# Assumes we are given two dfs and we do the normal t-test
from viz import common
import os
# get_mean, get_variance, plug the formula, t-table from scipy
def two_test(sample1,sample2):
    mean1 = sample1.mean()
    mean2= sample2.mean()
    var1 = sample1.var()
    var2 = sample2.var()
    t = (mean1-mean2)/np.sqrt((var1/len(sample1)) + (var2/len(sample2)))
    t=np.abs(t)
    dof = min(len(sample1),len(sample2))-1
    t_ = stats.t.ppf(1-0.05, dof)
    print("Value of t is %.2f and t_ is %.2f"%(t,t_))

def one_test(sample,popmean):
    # t,p = stats.ttest_1samp(sample,popmean,alternative="less")
    mean = sample.mean()
    var = sample.var()
    # print(mean,var,popmean)
    t= (popmean-mean)/((np.sqrt(var/len(sample))))
    pval = stats.t.sf(np.abs(t), len(sample)-1)  # two-sided pvalue = Prob(abs(t)>tt)
    print("Value of t is %.2f and p is %f"%(t,pval))


Dates = {}
Dates[1990]= [5224216,6054561]
Dates[1980]= [4751578]
Dates[1970]=[4342854]

words = {1990:["peripheral","diskette","disk","port","io"],
        1980: ["signal","ram","mixer"],
        1970:["solid polymer","polypropylene"]}
# inf.loc[Dates[1980]].hist(column="score_max")
# import matplotlib.pyplot as plt
# plt.savefig("inf_80_max.png")

# inf.loc[Dates[1990]].hist(column="score_max")
# import matplotlib.pyplot as plt
# plt.savefig("inf_90_max.png")

flag_dir = "coha"
EMBED = "coha-word"
BASE_DIR = "Results\{}\samples".format(flag_dir)

inf = pd.read_csv("Results\{}\samples\infringements_lite.csv".format(flag_dir),index_col="patent_id")


results = dict()
for patents in Dates.values():
    for patent in patents:
        results[patent] = []

def inf_one_test():
    # Go through each year and compute the p and t
    # append to dframe
    for year in [1970,1980,1990]:
        for k in range(3,11,2):
            sample = pd.read_csv("Results\{}\samples\sample_scores_k={}_{}.csv".format(flag_dir,k,year),index_col="patent_id")
            for patent in Dates[year]:
                # print("Patent: %d"%(patent))
                (t,p ) = stats.ttest_1samp(sample.loc[:,"score"].to_numpy(),inf.loc[patent,"top_{}_score".format(k)])
                results[patent] = results[patent] + [(t,p)]


inf_one_test()
cols = ["top_"+str(i) for i in range(3,11,2)]
df = pd.DataFrame.from_dict(results,orient="index",columns=cols)
df.to_csv(os.path.join(BASE_DIR,"ttest_results.csv"))

# print(results)
# stats.ttest_1samp()
# word t-test
# for word in words[1970]:
#     val = common.words_diff_min(word,1970,1980,seq_embeddings)
#     one_test(sample_70.iloc[:,1].to_numpy(),val)


# sample_80.hist(column="scores_max",bins=100)
# import matplotlib.pyplot as plt
# plt.savefig("80_max.png")
# # # print(inf)
# def compare_year(inf,sample,year):
#     print(year)
#     # Compare Avg
#     sample1 = inf.loc[:,"score_avg"]
#     sample2=  sample["scores_avg"]
#     print("Avg:")
#     two_test(sample1,sample2)
#     # # Compare Max
#     sample1 = inf.loc[:,"score_max"]
#     sample2=  sample["scores_max"]
#     print("Max:")
#     two_test(sample1,sample2)

# compare_year(inf,sample_70,1970)
# compare_year(inf,sample_80,1980)
# compare_year(inf,sample_90,1990)
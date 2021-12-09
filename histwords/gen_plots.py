from top_k import BASE_DIR
from viz.scripts.multiple_years import multiple_years
from viz.scripts.closest_over_time_chain import get_closest_time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# give nan array of vals make a histo
def create_histo(vals):
        plt.hist(vals, bins=80)  # density=False would make counts
        plt.ylabel('Probability')
        plt.xlabel('Scores')

FLAG = "eng-all"

BASE_DIR = "Results\{}\samples".format(FLAG)
HIST_DIR = "Results\{}\histograms".format(FLAG)


Dates = {}
Dates[1990]= [5224216,6054561]
Dates[1980]= [4751578]
Dates[1970]=[4342854]

def make_all_histos():
        for year in range(1970,1991,10):
                for k in range(3,11,2):
                        # for k in range(3,11,2):
                        fname = os.path.join(BASE_DIR,"sample_scores_k={}_{}.csv".format(k,year))
                        df = pd.read_csv(fname,index_col="patent_id")
                        plt.clf()
                        plt.hist(df["score"].to_numpy(), bins=80)  # density=False would make counts
                        plt.ylabel('Probability')
                        plt.xlabel('K={} Scores'.format(k))
                        plt.savefig(os.path.join(HIST_DIR,"hist_k={}_{}.png".format(k,year)))

# for a given year and directory, plot the inf vs all patents
def super_impose(year):
        df_inf = pd.read_csv(os.path.join(BASE_DIR,"infringements_lite.csv"),index_col="patent_id")
        # For a given year and for all k
        for k in range(3,11,2):
                fname = os.path.join(BASE_DIR,"sample_scores_k={}_{}.csv".format(k,year))
                df_k = pd.read_csv(fname,index_col="patent_id")
                create_histo(df_k.loc[:,"score"].to_numpy())
                for patent in Dates[year]:
                        x = df_inf.loc[patent,"top_{}_score".format(k)]
                        plt.axvline(x,color="r",label="{}".format(patent))
                plt.legend()
                # plt.show()
                plt.savefig(os.path.join(HIST_DIR,"hist_imp_k={}_{}".format(k,year)))
                plt.clf()

                # break


super_impose(1980)
super_impose(1970)
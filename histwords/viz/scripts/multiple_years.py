import helpers
import sys


"""
Let's examine the closest neighbors for a word over time
"""

import numpy as np
import matplotlib.pyplot as plt


# We accept a list of words from command line
# to generate graphs for.
def multiple_years(word1,*YEARS):
    # print(word1,YEARS)
    embeddings = helpers.load_embeddings()
    all_lookups = {}
    all_sims = {}
    # wordchain = "_".join(WORDS)
    # Lookups contains string of wordyear and their embedding
    helpers.clear_figure()
    time_sims, lookups, nearests, sims = helpers.get_time_sims(embeddings, word1)

    all_lookups.update(lookups)
    all_sims.update(sims)


    words = all_lookups.keys()
    values = [ all_lookups[word] for word in words ]
    fitted = helpers.fit_tsne(values)
    # print(fitted)
    # draw the words onto the graph
    cmap = helpers.get_cmap(len(time_sims))
    # print(words)
    # TODO: split the annotations up
    # annotations = helpers.plot_words(WORDS, words, fitted, cmap, all_sims)
    for year in YEARS:
        annotations = helpers.plot_words_year(word1,words,fitted,all_sims,year)
        helpers.savefig("%s_%s_chain.png" % (word1,year))
    # plt.show()
    # if annotations:
    #     helpers.plot_annotations(annotations)

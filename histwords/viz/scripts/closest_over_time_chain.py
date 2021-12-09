import helpers
import sys


"""
Let's examine the closest neighbors for a word over time
"""

import numpy as np
import matplotlib.pyplot as plt


# We accept a list of words from command line
# to generate graphs for.

# WORDS = helpers.get_words()


def get_closest_time(word1,output,embeddings):
    # embeddings = helpers.load_embeddings()
    all_lookups = {}
    all_sims = {}
    # WORDS.sort()
    # wordchain = "_".join(WORDS)
    # Lookups contains string of wordyear and their embedding
    helpers.clear_figure()
    time_sims, lookups, nearests, sims = helpers.get_time_sims(embeddings, word1)

    all_lookups.update(lookups)
    all_sims.update(sims)


    words = all_lookups.keys()
    values = [ all_lookups[word] for word in words ]
    fitted = helpers.fit_tsne(values)
    if (fitted is None):
        return
    # draw the words onto the graph
    cmap = helpers.get_cmap(len(time_sims))

    # TODO: split the annotations up
    annotations = helpers.plot_words(word1, words, fitted, cmap, all_sims)
    if annotations:
        helpers.plot_annotations(annotations)

    helpers.savefig("%s_%s_chain.png" %(output,word1))

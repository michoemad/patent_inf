from representations.sequentialembedding import SequentialEmbedding
from viz import common
"""
Example showing how to load a series of historical embeddings and compute similarities over time.
Warning that loading all the embeddings into main memory can take a lot of RAM
"""

seq_embeds = SequentialEmbedding.load("eng-all",range(1980,2000,10))

print(common.word_diff("controllable",1980,1990,seq_embeds))
# if __name__ == "__main__":
#     fiction_embeddings = SequentialEmbedding.load("eng-fiction-all_sgns", range(1950, 1970, 10))
#     # print(fiction_embeddings.get_embed(1951).represent("gay")) # gets the vector!
#     # Get diff year
#     print(fiction_embeddings.get_subembeds(["gay","lesbian"]).embeds[1960].represent("gay"))
#     # time_sims = fiction_embeddings.get_time_sims("lesbian", "gay")   
    # print "Similarity between gay and lesbian drastically increases from 1950s to the 1990s:"
    # for year, sim in time_sims.iteritems():
    #     print "{year:d}, cosine similarity={sim:0.2f}".format(year=year,sim=sim)


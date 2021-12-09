import pandas as pd

# Break a big CSV into little classes

df = pd.read_csv("all_cats.csv",index_col="patent_id")

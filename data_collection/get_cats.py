import data_col

import pandas as pd
from google.cloud import bigquery

collector = data_col.data_col("careful-lock-334103")

# cats is a list of ints
def get_cats(cats,collector):
    table_name = "patents-public-data.patentsview.uspc"
    cats = list(map(lambda x: '"'+str(x)+'"',cats))

    query1 = """SELECT mainclass_id,subclass_id,patent_id FROM `%s`
    WHERE mainclass_id IN (%s)
    AND LENGTH(mainclass_id)=3
    """%(table_name,",".join(cats))
    df = collector.run_query(query1)
    return df

# table1 has patents, table2 has dates
def join_dates(table1,collector,new_table):
    job_config = bigquery.QueryJobConfig(destination=collector.project_id+"."+new_table)
    query = """SELECT A.*,B.filing_date FROM `%s` AS A
    INNER JOIN `patents-public-data.uspto_oce_pair.application_data` AS B
    ON A.patent_id = B.patent_number"""%(collector.project_id+"."+table1)
    collector.client.query(query,job_config=job_config)

# might need to split categories?
df = collector.run_query("SELECT * FROM `careful-lock-334103.patents.all_cats_claims`")
df.set_index("patent_id")
df.to_csv("all_cats.csv")

# join_dates("patents.other_cats",collector,"patents.other_cats_dates")
# df.to_gbq(u"patents.other_cats")
# df2 = pd.read_csv("uspc_700.csv",index_col="patent_id")
# df  = df.append(df2)
# print(df)
# df = collector.run_query(query1)
# df.to_pickle("res1.csv")
# print(df)
# df = pd.read_csv("uspc_700.csv",index_col="patent_id")
# print(len(df[df["filing_date"]<"2000"])) #156,747
# #116
# print(len(df[df["filing_date"]<"1990"]))
# # df = pd.read_pickle("res1.csv")
# # df.to_csv("")
# # print(df)
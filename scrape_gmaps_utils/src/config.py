import pandas as pd
from ...pipeline_utils import sql_engine

# Mengambil nama universitas dari hasil scraping web QS dan THE
db_engine = sql_engine()
df = pd.read_sql_query('SELECT * FROM temp_merged_df_1_2_3_4', con = db_engine)
KEYWORDS = df['University'].tolist() 

# Melakukan query rating google maps dari setiap nama universitas
queries = [
    {"keyword": keyword, "max_results": 1} for keyword in KEYWORDS
]

number_of_scrapers = 16
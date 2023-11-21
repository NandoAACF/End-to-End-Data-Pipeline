import pandas as pd

file_path = 'src/final_all_data.csv'

# Mengambil nama universitas dari hasil scraping web QS dan THE
df = pd.read_csv(file_path)
KEYWORDS = df['University'].tolist() 

# Melakukan query rating google maps dari setiap nama universitas
queries = [
    {"keyword": keyword, "max_results": 1} for keyword in KEYWORDS
]

number_of_scrapers = 16
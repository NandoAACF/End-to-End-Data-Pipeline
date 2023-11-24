import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine

def get_json(url, headers=None):
    if headers is None:
        headers = {}
    
    res = requests.get(url, headers=headers).json()
    rows = res['data']
    return rows



def scrape_json_qs(url, numOfUniv):
    rows = get_json(url)
    
    data = []
    
    id = 0
    for i in range(0, numOfUniv):
        id += 1
        rank = rows[i]['rank_display']
        univ_name = rows[i]['title'].split('class="uni-link"')[1].split('>')[1].split('<')[0]
        score_univ = rows[i]['score']
        country = rows[i]['country']
        city = rows[i]['city']
        region = rows[i]['region']
        data.append([id, rank, univ_name, score_univ, country, city, region])
    
    df1 = pd.DataFrame(data, columns=['Id', 'Rank', 'University', 'Score', 'Country', 'City', 'Region'])

    return df1



def load(df, fileName):
    return df.to_csv(fileName, index=False)



def extract(pathFile):
    return pd.read_csv(pathFile)



def get_every_url(url, numOfUniv):
    rows = get_json(url)
    urls = []

    for i in range(0, numOfUniv):
        partial_univ_url = rows[i]['title'].split('" class="uni-link"')[0].split('href="')[1]
        univ_url = 'https://www.topuniversities.com' + partial_univ_url
        urls.append((univ_url))
    
    return urls



def get_soup(urls):
    page = requests.get(urls)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup



def get_univ_rank(soup):
    try:
        univ_rank = soup.findAll('div', attrs={'class':'latest_rank'})[0].get_text()
    except:
        univ_rank = 0
    return univ_rank



def get_univ_name(soup):
    univ_name = soup.find('h1', attrs={'class':'text-white'}).get_text()
    return univ_name



def no_value(i, univ_name, univ_rank):
    return [
        {
            'Id': i+1,
            'Ranking': univ_rank,
            'University Name': univ_name,
        }
    ]



def scrape_page(soup, i):
    univ_name = get_univ_name(soup)
    univ_rank = get_univ_rank(soup)

    data = []

    try:
        no_row = soup.findAll('div', attrs = {'class':'univ-subsection-full-width'})
        # Cek apakah ada keterangan info TOEFL, IELTS, dll
        if len(no_row) > 0:
            for j in range(0, len(no_row)):
                # Ada 3 pilihan status, yaitu bachelor, master, dan general
                # Kita akan menggunakan yang statusnya bachelor
                status = soup.findAll('div', attrs = {'class':'univ-subsection-full-width'})[j].find('h4', attrs = {'class':'univ-subsection-full-width-title'}).get_text()
                # Jika status bachelor
                if status == 'Bachelor':
                    new_no = j
                    all_subject = soup.findAll('div', attrs = {'class':'univ-subsection-full-width'})[new_no].findAll('div', attrs = {'class':'univ-subsection-full-width-value bottom-div'})
                    label = []
                    value = []
                    for k in range(0, len(all_subject)):
                        label.append(all_subject[k].find('label').get_text()) 
                        value.append(all_subject[k].find('div').get_text())
                    while len(label) < 10:
                        label.append('')
                        value.append('')
                    data.append(
                        {
                            'Id': i+1,
                            'Ranking': univ_rank,
                            'University Name': univ_name,
                            label[0]: value[0],
                            label[1]: value[1],
                            label[2]: value[2],
                            label[3]: value[3],
                            label[4]: value[4],
                            label[5]: value[5],
                            label[6]: value[6],
                            label[7]: value[7],
                            label[8]: value[8],
                            label[9]: value[9]
                        }
                    )
                    return data
                
                else:
                    if status != 'General' or 'Master':
                        pass
                    else:
                        data = no_value(i, univ_name, univ_rank)

    except:
        data = no_value(i, univ_name, univ_rank)
        return data

    else:
        data = no_value(i, univ_name, univ_rank)
        return data



def scrape_all_pages_qs(url, numOfUniv):
    urls = get_every_url(url, numOfUniv)

    all_data = []

    for i in range(0, len(urls)):
        print(f'Getting data from {urls[i]} ({i})')
        soup = get_soup(urls[i])
        data = scrape_page(soup, i)
        all_data.extend(data)

    df2 = pd.DataFrame(all_data)

    return df2



def merge_qs(df1, df2):
    temp_merged_df = df1.merge(df2, on='Id', how='inner')
    return temp_merged_df



def transform_and_merge_qs(df1, df2):
    temp_merged_df = merge_qs(df1, df2)

    temp_merged_df.drop(['Id', 'University Name', 'Rank', 'Unnamed: 5'], axis=1, inplace=True)

    null_percentages = (temp_merged_df.isnull().sum()*100/temp_merged_df.shape[0]).sort_values(ascending=False)
    columns_to_drop = null_percentages[null_percentages > 58].index
    temp_merged_df.drop(columns_to_drop, axis=1, inplace=True)

    temp_merged_df['University'] = temp_merged_df['University'].str.replace(r'\([^)]*\)', '').str.strip()
    
    temp_merged_df['Ranking'] = temp_merged_df['Ranking'].str.replace(r'[^0-9]', '')
    temp_merged_df.rename(columns={'Ranking': 'Rank'}, inplace=True)


    temp_merged_df['IELTS'] = temp_merged_df['IELTS'].str.rstrip('+')
    temp_merged_df['TOEFL'] = temp_merged_df['TOEFL'].str.rstrip('+')

    temp_merged_df['IELTS'].replace('', np.nan, inplace=True)
    temp_merged_df['IELTS'].replace('0', np.nan, inplace=True)
    temp_merged_df['TOEFL'].replace('0', np.nan, inplace=True)

    temp_merged_df['Rank'] = temp_merged_df['Rank'].astype('int64')
    temp_merged_df['Score'] = temp_merged_df['Score'].astype('float64')
    temp_merged_df['IELTS'] = temp_merged_df['IELTS'].astype('float64')
    temp_merged_df['TOEFL'] = temp_merged_df['TOEFL'].astype('float64')

    temp_merged_df['TOEFL'].loc[temp_merged_df['TOEFL'] > 200] = np.nan

    temp_merged_df['Rank'].replace(0, method='ffill', inplace=True)

    rank_column = temp_merged_df.pop('Rank')
    temp_merged_df.insert(0, 'Rank', rank_column)

    return temp_merged_df



def scrape_json_the(url, headers, numOfUniv):
    rows = get_json(url, headers)
    
    data = []

    for i in range(0, numOfUniv):
        name = rows[i]['name']
        num_students = rows[i]['stats_number_students']
        inter_students = rows[i]['stats_pc_intl_students']
        gender_ratio = rows[i]['stats_female_male_ratio']
        subjects = rows[i]['subjects_offered']
        data.append([name, num_students, inter_students, gender_ratio, subjects])

    df3 = pd.DataFrame(data, columns=['University', 'Total Students', 'International Students', 'Gender Ratio', 'Subjects'])

    return df3



def transform_the(df3):
    df3['Total Students'] = pd.to_numeric(df3['Total Students'].str.replace(',', ''), errors='coerce')
    df3['International Students'] = pd.to_numeric(df3['International Students'].str.replace('%', ''), errors='coerce') / 100
    df3[['Male Ratio', 'Female Ratio']] = df3['Gender Ratio'].str.split(':', expand=True).astype(float)
    df3['Subjects Count'] = df3['Subjects'].fillna('').str.split(',').apply(lambda x: len(x) if x != [''] else 0)

    df3.drop(['Gender Ratio'], axis=1, inplace=True)
    df3.drop(['Subjects'], axis=1, inplace=True)

    return df3



def merge_all(temp_merged_df, df_new):
    merged_all_df = pd.merge(temp_merged_df, df_new, on='University', how='left')
    return merged_all_df



def transform_cwur(df4):
    df4['University'] = df4['University'].str.split('\n').str[0].apply(lambda x: x.strip())
    df4['Alumni Employability Rank'].loc[df4['Alumni Employability Rank'] == '-'] = np.nan
    df4['Alumni Employability Rank'] = df4['Alumni Employability Rank'].astype('Int64')
    return df4



def transform_gmaps(df5):
    df5 = df5.rename(columns={'keyword': 'University', 'rating':'Rating', 'reviews':'Total Reviews'})
    return df5



def sql_engine():
    return create_engine('postgresql://postgres:Planify123Junpro@20.24.68.238/rekdatuniv')



def load_to_sql(df, tableName, db_engine):
    return df.to_sql(name = tableName, con = db_engine, if_exists='replace', index=False)



def unit_test(df):
    assert df.shape[0] == 500, "Total number of rows should be 500"
    assert isinstance(df, pd.DataFrame), "Output should be a dataframe"
    assert df['Rank'].isnull().sum() == 0, "There should be no null values in the Rank column"
    assert df['University'].isnull().sum() == 0, "There should be no null values in the University column"
    assert (df.isnull().sum() / len(df) * 100).max() < 300, "There should be no columns with null values more than 60% of the total rows"
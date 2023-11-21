import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import text

from pipeline_utils import sql_engine

@st.cache_data
def get_data():
    # Mengambil data dari database SQL
    db_engine = sql_engine()
    conn = db_engine.connect()
    query = text('SELECT * FROM all_data')
    df = pd.read_sql_query(query, con = conn)

    return df

df = get_data()

def show_insight():

    st.title('Top 500 World Universities Insight')

    # Question
    st.markdown("### **Region, negara, dan kota apa yang paling banyak memiliki universitas terbaik?**")
    region_counts = df['Region'].value_counts()

    plt.figure(figsize=(10, 5))
    sns.barplot(x=region_counts.values, y=region_counts.index, palette='viridis')

    for index, value in enumerate(region_counts.values):
        plt.text(value, index, str(value), va='center')

    plt.title('Number of Universities per Region')

    st.pyplot(plt)
    
    st.write('Tampak bahwa hampir separuh dari 500 universitas terbaik di dunia berada di Eropa. Amerika Utara dan Asia juga memiliki jumlah universitas terbaik yang tidak jauh berbeda. Sementara itu, Afrika hanya memiliki 7 universitas terbaik.')


    country_counts = df['Country'].value_counts()[:10]

    plt.figure(figsize=(10, 5))
    sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis')

    for index, value in enumerate(country_counts.values):
        plt.text(value, index, str(value), va='center')

    plt.title('Top 10 Countries with the Most Best Universities')

    st.pyplot(plt)

    st.write('US merupakan negara yang memiliki paling banyak universitas terbaik, yaitu sebanyak 82 universitas dan jumlahnya berbeda sangat signifikan dibanding negara lainnya, diikuti oleh Inggris dan Jerman.')


    city_counts = df['City'].value_counts()[:10]

    plt.figure(figsize=(10, 5))
    sns.barplot(x=city_counts.values, y=city_counts.index, palette='viridis')

    for index, value in enumerate(city_counts.values):
        plt.text(value, index, str(value), va='center')

    plt.title('Top 10 Cities with the Most Best Universities')

    st.pyplot(plt)

    st.write('London merupakan kota yang memiliki paling banyak universitas terbaik, yaitu sebanyak 9 universitas.')



    # Question
    st.markdown("### **Apakah ada korelasi antara skor TOEFL dan IELTS terhadap ranking universitas?**")

    # fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # sns.scatterplot(x='Rank', y='TOEFL', data=df, ax=axes[0])
    # axes[0].invert_xaxis()
    # sns.regplot(x='Rank', y='TOEFL', data=df, scatter=False, ax=axes[0], color='darkblue')
    # axes[0].set_title('TOEFL Scores vs. Rankings of Top 500 Universities')
    # axes[0].set_xlabel('University Rank')
    # axes[0].set_ylabel('TOEFL Score')

    # sns.scatterplot(x='Rank', y='IELTS', data=df, ax=axes[1])
    # axes[1].invert_xaxis()
    # sns.regplot(x='Rank', y='IELTS', data=df, scatter=False, ax=axes[1], color='darkblue')
    # axes[1].set_title('IELTS Scores vs. Rankings of Top 500 Universities')
    # axes[1].set_xlabel('University Rank')
    # axes[1].set_ylabel('IELTS Score')

    # plt.tight_layout()

    # st.pyplot(plt)


    df['Rank Bins'] = pd.cut(df['Rank'], bins=range(1, df['Rank'].max() + 50, 50), right=False)

    rank_bins_mean = df.groupby('Rank Bins')['TOEFL'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x='Rank Bins', y='TOEFL', ci=None, palette='viridis')

    for p in ax.patches:
        value = round(p.get_height(), 1)
        ax.annotate(f'{value}', (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black')

    plt.xticks(rotation=45)

    plt.title('Rank Bins vs TOEFL')
    plt.xlabel('Rank Bins')
    plt.ylabel('TOEFL')
    st.pyplot(plt)


    df['Rank Bins'] = pd.cut(df['Rank'], bins=range(1, df['Rank'].max() + 50, 50), right=False)

    rank_bins_mean = df.groupby('Rank Bins')['IELTS'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x='Rank Bins', y='IELTS', ci=None, palette='viridis')

    for p in ax.patches:
        value = round(p.get_height(), 1)
        ax.annotate(f'{value}', (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black')    

    plt.xticks(rotation=45)

    plt.title('Rank Bins vs IELTS')
    plt.xlabel('Rank Bins')
    plt.ylabel('IELTS')
    st.pyplot(plt)


    st.write('Tampak bahwa semakin tinggi peringkat universitas, skor TOEFL dan IELTS mahasiswa yang diterima pun juga semakin tinggi, walaupun korelasinya tidak terlalu kuat. Hal ini masuk akal karena biasanya universitas yang bagus memiliki syarat lebih ketat daripada universitas lain.')

    st.write('Rata-rata skor TOEFL mahasiswa top 50 universitas terbaik adalah 93 dan skor IETLS nya 6.6')
    st.write('Setidaknya harus memiliki skor TOEFL di atas 80 dan skor IELTS di atas 6.0 supaya bisa diterima di top 300 universitas terbaik di dunia.')



    # Question
    st.markdown("### **Apakah ranking universitas berpengaruh terhadap jumlah mahasiswa asing?**")

    df['Rank Bins'] = pd.cut(df['Rank'], bins=range(1, df['Rank'].max() + 50, 50), right=False)

    rank_bins_mean = df.groupby('Rank Bins')['International Students'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(data=df, x='Rank Bins', y='International Students', ci=None, palette='viridis')

    plt.plot(rank_bins_mean['Rank Bins'].astype(str), rank_bins_mean['International Students'], color='red', marker='o')

    plt.xticks(rotation=45)

    plt.title('Rank Bins vs International Students with Trend Line')
    plt.xlabel('Rank Bins')
    plt.ylabel('International Students')
    st.pyplot(plt)

    st.write('Tampak jelas bahwa semakin tinggi peringkat universitas, maka jumlah mahasiswa asingnya juga semakin banyak. Hal ini masuk akal karena universitas yang memiliki peringkat tinggi biasanya lebih terkenal dan memiliki kualitas pendidikan yang baik sehingga banyak mahasiswa asing yang tertarik untuk belajar di sana.')


    # Question
    st.markdown("### **Bagaimana distribusi jumlah mahasiswa di universitas top 500?**")

    plt.figure(figsize=(8, 5))
    sns.histplot(df['Total Students'], bins=20, kde=True, palette='viridis', color='purple')
    plt.title('Distribusi Jumlah Mahasiswa di Top 500 Universitas')
    plt.xlabel('Total Students')
    plt.ylabel('Frequency')
    st.pyplot(plt)

    st.write('Tampak bahwa distribusi jumlah mahasiswa di universitas top 500 memiliki skewness positif, yang berarti bahwa pusat distribusinya cenderung condong ke kiri. Sebagian besar universitas top 500 memiliki 10000 - 30000 mahasiswa. Sedangkan, mahasiswa terbanyak pada universitas top 500 hampir mencapai 80000 mahasiswa.')


    # Question
    st.markdown("### **Bagaimana relasi antara jumlah mahasiswa dengan ranking dari universitas?**")

    df['Rank Bins'] = pd.cut(df['Rank'], bins=range(1, df['Rank'].max() + 50, 50), right=False)

    rank_bins_mean = df.groupby('Rank Bins')['Total Students'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(data=df, x='Rank Bins', y='Total Students', ci=None, palette='viridis')

    plt.plot(rank_bins_mean['Rank Bins'].astype(str), rank_bins_mean['Total Students'], color='red', marker='o')

    plt.xticks(rotation=45)

    plt.title('Rank Bins vs Total Students with Trend Line')
    plt.xlabel('Rank Bins')
    plt.ylabel('Total Students')
    st.pyplot(plt)

    st.write('Tampak trend bahwa semakin tinggi peringkat universitas, maka rata-rata jumlah mahasiswanya pun relatif semakin banyak.')


    # Question
    st.markdown("### **Bagaimana persebaran mahasiswa laki-laki dan perempuan pada universitas top 500 di dunia?**")

    male_percentage = df['Male Ratio'].mean()
    female_percentage = df['Female Ratio'].mean()

    labels = ['Male', 'Female']
    sizes = [male_percentage, female_percentage]
    colors = ['lightblue', 'lightcoral']

    plt.figure(figsize=(4, 4))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    st.pyplot(plt)

    st.write('Tampak bahwa persentase mahasiswa laki-laki dan perempuan di universitas top 500 di dunia tidak jauh berbeda, yaitu sekitar 51% laki-laki dan 49% perempuan.')


    # Question
    st.markdown("### **Bagaimana persebaran mahasiswa laki-laki dan perempuan berdasarkan negara?**")

    df_copy = df.copy()
    df_copy = df.loc[df['Male Ratio'].notnull()]
    df_copy = df.loc[df['Female Ratio'].notnull()]

    mean_ratios_by_region = df_copy.groupby('Region').agg({
        'Male Ratio': 'mean',
        'Female Ratio': 'mean'
    }).reset_index()

    mean_ratios_melted = mean_ratios_by_region.melt(id_vars='Region', value_vars=['Male Ratio', 'Female Ratio'], 
                                                    var_name='Gender', value_name='Mean Ratio')

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=mean_ratios_melted, x='Region', y='Mean Ratio', hue='Gender', palette='viridis')

    for p in ax.patches:
        value = round(p.get_height(), 1)
        ax.annotate(f'{value}', (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black')

    plt.title('Mean Male and Female Ratios by Region')
    plt.xlabel('Region')
    plt.ylabel('Mean Ratio')
    st.pyplot(plt)

    st.write('Tampak jelas bahwa mahasiswa universitas top 500 di Asia didominasi oleh perempuan, sedangkan di benua lain didominasi oleh laki-laki.')


    # Question
    st.markdown("### **Apakah universitas yang peringkatnya tinggi memiliki jumlah prodi lebih banyak?**")

    df['Rank Bins'] = pd.cut(df['Rank'], bins=range(1, df['Rank'].max() + 50, 50), right=False)

    rank_bins_mean = df.groupby('Rank Bins')['Subjects Count'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(data=df, x='Rank Bins', y='Subjects Count', ci=None, palette='viridis')

    plt.plot(rank_bins_mean['Rank Bins'].astype(str), rank_bins_mean['Subjects Count'], color='red', marker='o')

    plt.xticks(rotation=45)

    plt.title('Rank Bins vs Subjects Count with Trend Line')
    plt.xlabel('Rank Bins')
    plt.ylabel('Subjects Count')
    st.pyplot(plt) 

    st.write('Korelasi antara peringkat universitas dan jumlah program studi tidak terlalu jelas, namun universitas top 50 memiliki rata-rata jumlah program studi yang lebih tinggi dibanding peringkat di bawahnya.')


    # Question
    st.markdown("### **Berapa minimal skor akreditasi yang harus didapat oleh universitas agar masuk ke daftar top 100 dan top 500 universitas?**")
    plt.figure(figsize=(6, 6))
    scatterplot = sns.scatterplot(x='Rank', y='Score', data=df, s=100, color='green')

    plt.title('University Score vs. Rank')
    plt.xlabel('Rank')
    plt.ylabel('Score')

    plt.grid(True)
    st.pyplot(plt) 

    st.write('Skor akreditasi universitas top 100 ada di atas 60, sedangkan skor akreditasi universitas top 500 ada di atas 23. Artinya, setidaknya suatu universitas harus mendapatkan skor akreditasi di atas 60 supaya bisa masuk daftar top 100 universitas terbaik di dunia.')


    # Question
    st.markdown("### **Region apa yang memiliki rata-rata skor akreditasi tertinggi?**")
    mean_score_by_region = df.groupby('Region')['Score'].mean().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='Score', y='Region', data=mean_score_by_region, palette='viridis')

    for index, value in enumerate(mean_score_by_region['Score']):
        plt.text(value, index, f'{value:.1f}', va='center')

    plt.title('Mean University Score by Region')
    plt.xlabel('Mean Score')
    plt.ylabel('Region')
    st.pyplot(plt) 

    st.write('Universitas di North America memiliki rata-rata skor akreditasi tertinggi, sedangkan rata-rata skor akreditasi universitas di Africa paling rendah. Hal ini masuk akal karena pendidikan di Afrika belum sebaik di benua lainnya.')


    # Question
    st.markdown("### **Apa saja universitas di Indonesia yang masuk ke daftar top 500?**")
    indonesia_universities = df[df['Country'] == 'Indonesia']

    indonesia_universities_sorted = indonesia_universities.sort_values('Rank')

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=indonesia_universities_sorted, x='University', y='Rank', palette='viridis')

    for p in ax.patches:
        value = int(p.get_height())
        ax.annotate(f'{value}', (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black')

    plt.title('Indonesian Universities by Rank')
    plt.xticks(rotation=8)
    plt.xlabel('University Name')
    plt.ylabel('Rank')
    st.pyplot(plt) 

    st.write('Terdapat 5 universitas di Indonesia yang masuk ke daftar top 500, yaitu Universitas Indonesia, Universitas Gadjah Mada, Institut Teknologi Bandung, Universitas Airlangga, dan Institut Pertanian Bogor.')
    st.write('Peringkat tertinggi dipegang oleh Universitas Indonesia, yaitu peringkat 237.')


    # Question
    st.markdown("### **Benua dan negara apa yang mahasiswanya memiliki skor TOEFL dan IELTS tertinggi?**")
    df_copy = df.copy()
    df_copy = df.loc[df['TOEFL'].notnull()]
    mean_TOEFL_by_region = df_copy.groupby('Region')['TOEFL'].mean().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='TOEFL', y='Region', data=mean_TOEFL_by_region, palette='viridis')

    for index, value in enumerate(mean_TOEFL_by_region['TOEFL']):
        plt.text(value, index, f'{value:.1f}', va='center')

    plt.title('Mean University TOEFL by Region')
    plt.xlabel('Mean TOEFL')
    plt.ylabel('Region')
    st.pyplot(plt) 

    mean_IELTS_by_region = df.groupby('Region')['IELTS'].mean().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='IELTS', y='Region', data=mean_IELTS_by_region, palette='viridis')

    for index, value in enumerate(mean_IELTS_by_region['IELTS']):
        plt.text(value, index, f'{value:.1f}', va='center')

    plt.title('Mean University IELTS by Region')
    plt.xlabel('Mean IELTS')
    plt.ylabel('Region')
    st.pyplot(plt) 

    st.write('Mahasiswa di North America memiliki rata-rata skor TOEFL dan IELTS tertinggi, sedangkan mahasiswa di Africa memiliki rata-rata skor TOEFL dan IELTS terendah. Tampak perbedaan yang cukup signifikan antara skor TOEFL di North America dan Africa. Skor TOEFL di North America hampir 2 kali lipat lebih tinggi daripada skor di Africa')
    st.write('FYI: Skor rata-rata TOEFL iBT adalah 84 dan skor rata-rata IELTS adalah 6.0. Artinya mahasiswa di Afrika memiliki skor TOEFL yang masih cukup jauh di bawah rata-rata dunia.')


    # Question
    st.markdown("### **Benua apa yang memiliki rata-rata mahasiswa asing terbanyak?**")
    
    df_copy = df.copy()
    df_copy = df_copy.loc[df_copy['Region'] != 'Latin America']
    mean_International_Students_by_region = df_copy.groupby('Region')['International Students'].mean().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='International Students', y='Region', data=mean_International_Students_by_region, palette='viridis')

    for index, value in enumerate(mean_International_Students_by_region['International Students']):
        plt.text(value, index, f'{value:.2f}', va='center')

    plt.title('Mean University International Students by Region')
    plt.xlabel('Mean International Students')
    plt.ylabel('Region')
    st.pyplot(plt) 

    st.write('Oceania memiliki rata-rata jumlah mahasiswa asing terbanyak, sedangkan Afrika memiliki rata-rata jumlah mahasiswa asing terendah dengan perbedaan yang sangat signifikan dibanding Oceania (2,5 kali lipatnya). Hal ini masuk akal karena Oceania memiliki banyak negara yang terkenal akan kualitas pendidikannya, seperti Australia dan New Zealand. Sementara itu, Afrika memiliki banyak negara yang masih berkembang sehingga mungkin kurang menarik minat mahasiswa asing.')


    # Question
    st.markdown("### **Bagaimana distribusi peringkat employability alumni pada universitas top 500?**")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Alumni Employability Rank'], bins=30, kde=True, palette='viridis', color='purple')
    plt.title('Distribution of Alumni Employability Rank')
    plt.xlabel('Alumni Employability Rank')
    plt.ylabel('Frequency')
    st.pyplot(plt)

    st.write('Tampak bahwa distribusi peringkat employability alumni pada universitas top 500 memiliki skewness positif, yang berarti bahwa pusat distribusinya cenderung condong ke kiri. Hal ini menunjukkan bahwa lulusan universitas terbaik memiliki kemudahan dalam mencari kerja.')


    # Question
    st.markdown("### **Bagaimana korelasi antara peringkat employability alumni dengan peringkat universitas?**")
    plt.figure(figsize=(6, 6))
    scatterplot = sns.scatterplot(x='Rank', y='Alumni Employability Rank', data=df, palette='viridis')

    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    sns.regplot(x='Rank', y='Alumni Employability Rank', data=df, scatter=False, ax=scatterplot.axes, color='darkblue')

    plt.title('University Rank vs Alumni Employability Rank')
    plt.xlabel('University Rank')
    plt.ylabel('Alumni Employability Rank')
    st.pyplot(plt)

    st.write('Tampak bahwa semakin tinggi peringkat universitas, maka peringkat employability alumni pun juga semakin tinggi. Hal ini masuk akal karena perusahaan akan mencari kandidat yang lulus dari universitas terbaik.')


    # Question
    st.markdown("### **Negara apa yang memiliki rata-rata peringkat employability alumni tertinggi?**")
    mean_employability_by_rank = df.groupby('Region')['Alumni Employability Rank'].mean().sort_values(ascending=True).reset_index()
    mean_employability_by_rank = mean_employability_by_rank[mean_employability_by_rank['Region'] != 'Latin America']

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='Alumni Employability Rank', y='Region', data=mean_employability_by_rank, palette='viridis')

    for index, value in enumerate(mean_employability_by_rank['Alumni Employability Rank']):
        plt.text(value, index, f'{value:.0f}', va='center')

    plt.title('Mean University Alumni Employability Rank by Region')
    plt.xlabel('Mean Alumni Employability Rank')
    plt.ylabel('Region')
    st.pyplot(plt)

    st.write('Mahasiswa lulusan Oceania justru memiliki peringkat employability alumni yang paling rendah, sedangkan mahasiswa lulusan Amerika Utara memiliki peringkat employability alumni yang paling tinggi.')


    # Question
    st.markdown("### **Apakah universitas yang memiliki peringkat tinggi juga memiliki rating google maps yang lebih tinggi?**")
    df['Rank Bins'] = pd.cut(df['Rank'], bins=range(1, df['Rank'].max() + 50, 50), right=False)

    rank_bins_mean = df.groupby('Rank Bins')['Rating'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(data=df, x='Rank Bins', y='Rating', ci=None, palette='viridis')

    plt.plot(rank_bins_mean['Rank Bins'].astype(str), rank_bins_mean['Rating'], color='red', marker='o')

    plt.xticks(rotation=45)

    plt.title('Rank Bins vs Rating with Trend Line')
    plt.xlabel('Rank Bins')
    plt.ylabel('Rating')
    st.pyplot(plt)

    st.write('Tidak. Rating universitas di Google Maps tidak berkorelasi dengan peringkat universitas. Hal tersebut masuk akal karena rating universitas di Google Maps bukan acuan untuk menentukan kualitas pendidikan di universitas tersebut. Rating universitas di Google Maps hanya berdasarkan pengalaman orang-orang yang pernah mengunjungi universitas tersebut.')


    # Question
    st.markdown("### **Bagaimana korelasi antara peringkat universitas dengan jumlah review di google maps?**")
    plt.figure(figsize=(5, 5))
    scatterplot = sns.scatterplot(x='Rank', y='Total Reviews', data=df)

    plt.gca().invert_xaxis()

    sns.regplot(x='Rank', y='Total Reviews', data=df, scatter=False, ax=scatterplot.axes, color='darkblue')

    plt.title('Total Reviews Scores vs. Rankings of Top 500 Universities')
    plt.xlabel('University Rank')
    plt.ylabel('Total Reviews Score')
    st.pyplot(plt)

    st.write('Semakin tinggi peringkat universitas, maka jumlah review di Google Maps pun juga semakin banyak. Hal ini masuk akal karena universitas yang memiliki peringkat tinggi biasanya lebih terkenal dan banyak orang yang sudah mengunjungi universitas tersebut.')


    # Kesimpulan
    st.markdown("### **Kesimpulan**")
    st.write('- Sebagian besar universitas terbaik di dunia berada di Eropa')
    st.write('- Semakin tinggi peringkat universitas, maka skor TOEFL dan IETLS mahasiswa yang diterima pun juga semakin tinggi.')
    st.write('- Rata-rata skor TOEFL mahasiswa top 300 universitas terbaik adalah di atas 80 dan skor IETLS nya di atas 6.0')
    st.write('- Semakin tinggi peringkat universitas, maka jumlah mahasiswa asingnya juga semakin banyak.')
    st.write('- Sebagian besar universitas terbaik memiliki 10000 - 30000 mahasiswa')
    st.write('- Universitas terbaik di Asia didominasi oleh perempuan, sedangkan di benua lain didominasi oleh laki-laki.')
    st.write('- Top 100 universitas memiliki skor akreditasi di atas 60')
    st.write('- Amerika Utara memiliki rata-rata skor akreditas tertinggi, sedangkan Afrika yang terendah')
    st.write('- Universitas di Indonesia yang masuk daftar top 500 adalah Universitas Indonesia, Universitas Gadjah Mada, Institut Teknologi Bandung, Universitas Airlangga, dan Institut Pertanian Bogor.')
    st.write('- Skor TOEFL mahasiswa di Amerika Utara hampir 2 kali lipat lebih tinggi daripada Afrika.')
    st.write('- Mahasiswa asing terbanyak ada di Oceania dan yang paling sedikit ada di Africa')
    st.write('- Semakin tinggi peringkat universitas, maka lulusannya semakin mudah mencari pekerjaan')
    st.write('- Mahasiswa lulusan Amerika Utara memiliki peringkat employability terbaik.')
    st.write('- Tidak ada korelasi antara rating universitas di Google Maps dengan peringkat universitas tersebut.')
    st.write('- Semakin tinggi peringkat universitas, maka rata-rata jumlah review di Google Maps pun juga semakin banyak.')
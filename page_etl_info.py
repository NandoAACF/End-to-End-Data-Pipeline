import streamlit as st

def show_etl_info():
    st.markdown("# ETL Pipeline Information")
    st.write('Info: Semua fungsi untuk kebutuhan ETL disimpan di pipeline_utils.py dan dipanggil pada MainNotebook.ipynb')
    st.image('images/pipeline.png')

    st.markdown("## Extract")
    st.write('Mengekstrak masing-masing kelima sumber tersebut')
    st.markdown('#### **Scrape API JSON Web Top Universities QS (Sumber 1):**')
    st.image('images/1.png')
    st.write('- Kami memanfaatkan API dari web ini supaya bisa mengambil feature-feature yang diperlukan')
    st.write('- Mendapatkan data dari API menggunakan library Requests')
    st.write('- API JSON tersebut memuat semua daftar universitas berdasarkan akreditasi QS.')
    st.write('- Maka, kita akan me-looping 500 baris dari JSON untuk mendapatkan feature tersebut')
    st.write('- Kemudian, kita append setiap hasil looping ke dalam list.')
    st.write('- Setelah semua looping selesai, kita ubah list tersebut menjadi sebuah dataframe')

    st.markdown('#### **Scrape API JSON Web Top Universities THE (Sumber 2):**')
    st.image('images/2.png')
    st.write('- Scraping dengan cara mengidentifikasi tag HTML-nya')
    st.write('- Memanfaatkan BeautifulSoup agar bisa mengambil value dari dalam tag HTML-nya.')
    st.write('- Kita akan mengambil value skor TOEFL dan IELTS dari setiap page')
    st.write('- Scrape sumber kedua ini memakan waktu cukup lama karena kita harus melakukan langkah di atas sebanyak 500 kali untuk setiap halaman')

    st.markdown('#### **Scrape API JSON Web Times Higher Education (Sumber 3):**')
    st.image('images/3.png')
    st.write('- Kami mendapatkan API JSON-nya dengan cara melakukan inspect network pada page tersebut')
    st.write('- Logikanya: page tersebut mengambil data dari API sehingga kita bisa menangkap API yang diambil dengan cara inspeksi bagian traffic networknya.')
    st.write('- Menggunakan library Requests untuk get data dari API tersebut.')
    st.write('- Kita bisa mengambil value dari setiap feature yang kita inginkan dengan cara menspesfikkan key nya.')
    st.write('- Looping langkah tersebut untuk 500 universitas.')
    st.write('- Kemudian, kita append setiap hasil looping ke dalam list.')
    st.write('- Setelah semua looping selesai, kita ubah list tersebut menjadi sebuah dataframe.')

    st.markdown('#### **Scrape API JSON Web CWUR (Sumber 4):**')
    st.write('- Scraping pada page CWUR memanfaatkan library Scrapy')
    st.write('- Kita mengidentifikasi CSS Selector yang memuat value Alumni Employability Rank agar bisa diekstrak')
    st.image('images/4.png')
    st.write('- Pencet tombol copy selector pada tag HTML yang kita inginkan supaya kita bisa mendapatkan selector yang akan diidentifikasi oleh Scrapy.')

    st.markdown('#### **Scrape Google Maps to get Rating and Total Reviews (Sumber 5)**')
    st.write('- Scraping rating dan total review pada google maps menggunakan library Selenium.')
    st.write('- Selenium digunakan untuk menjalankan browser dan melakukan beberapa tahapan, seperti membuka Google Maps dan melakukan scraping pada halaman-halaman tersebut.')
    st.write('- Mengkonfigurasikan list universitas yang didapat dari web QS sebagai keywords pada google maps.')
    st.image('images/5_1.png')
    st.write('- Membuka google maps dengan link berdasarkan keywords yang sudah ditentukan.')
    st.image('images/5_2.png')
    st.write('- Fungsi yang akan mengambil nilai rating dan jumlah review pada setiap page google maps yang dikunjungi.')
    st.image('images/5_3.png')
    st.write('- Hasil scraping akan disimpan ke dalam bentuk file json dan csv.')
    st.image('images/5_4.png')

    st.markdown("## Transform")
    st.markdown('#### **Transformasi sumber 1 dan sumber 2**')
    code = '''def transform_and_merge_qs(df1, df2):
    temp_merged_df = merge_qs(df1, df2)

    temp_merged_df.drop(['Id', 'University Name', 'Rank', 'Unnamed: 5'], axis=1, 
			inplace=True)

    null_percentages = ((temp_merged_df.isnull().sum()*100/temp_merged_df.shape[0])
			.sort_values(ascending=False))
    columns_to_drop = null_percentages[null_percentages > 58].index
    temp_merged_df.drop(columns_to_drop, axis=1, inplace=True)

    temp_merged_df['University'] = (temp_merged_df['University'].str
			.replace(r'\([^)]*\)', '').str.strip())
    
    temp_merged_df['Ranking'] = (temp_merged_df['Ranking'].str
			.replace(r'[^0-9]', ''))
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

    return temp_merged_df'''
    st.code(code, language='python')
    st.write('- Menghilangkan singkatan universitas')
    st.write('- Menghilangkan tanda ‘#’ dan ‘=‘ pada kolom Rank')
    st.write('- Menghilangkan tanda ‘+’ pada kolom TOEFL dan IELTS')
    st.write('- Mengganti nilai 0 pada kolom TOEFL dan IELTS menjadi null supaya tidak mengganggu hasil EDA')
    st.write('- Mengubah tipe data kolom Rank, Score, TOEFL, IELTS menjadi numerik')
    st.write('- Mengubah outlier pada kolom TOEFL menjadi null')
    st.write('- Mengganti nilai 0 pada rank dengan cara forward fill')

    st.markdown('#### **Transformasi sumber 3**')
    code = '''def transform_the(df3):
    df3['Total Students'] = pd.to_numeric(df3['Total Students'].str
			.replace(',', ''), errors='coerce')
    df3['International Students'] = pd.to_numeric(df3['International Students']
			.str.replace('%', ''), errors='coerce') / 100
    df3[['Male Ratio', 'Female Ratio']] = (df3['Gender Ratio'].str
			.split(':', expand=True).astype(float))
    df3['Subjects Count'] = (df3['Subjects'].fillna('').str.split(',')
			.apply(lambda x: len(x) if x != [''] else 0))

    df3.drop(['Gender Ratio'], axis=1, inplace=True)
    df3.drop(['Subjects'], axis=1, inplace=True)

    return df3'''
    st.code(code, language='python')
    st.write('- Mengubah tipe data kolom Total Students menjadi numerik')
    st.write('- Mengubah tipe data kolom International Students dari persentase menjadi decimal')
    st.write('- Split kolom Gender Ratio menjadi 2 kolom, yaitu Male Ratio dan Female Ratio.')
    st.write('- Membuat kolom Subject Count untuk menghitung jumlah mata kuliah setiap universitas berdasarkan kolom Subjects')
    st.write('- Drop kolom Gender Ratio dan Subjects karena sudah tidak dibutuhkan')

    st.markdown('#### **Transformasi sumber 4**')
    code = '''def transform_cwur(df4):
    df4['University'] = (df4['University'].str.split('\n').str[0]
			.apply(lambda x: x.strip()))
    df4['Alumni Employability Rank'].loc[df4['Alumni Employability Rank'] == '-'] \
			= np.nan
    df4['Alumni Employability Rank'] = df4['Alumni Employability Rank']
			.astype('Int64')
    return df4'''
    st.code(code, language='python')
    st.write('- Menghilangkan backtick n dan whitespace pada kolom nama University')
    st.write('- Mengubah nilai employability rank yang “-” menjadi nan')
    st.write('- Mengubah tipe data kolom Alumni Employability Rank menjadi tipe data Integer')

    st.markdown('#### **Transformasi sumber 5**')
    code = '''def transform_gmaps(df5):
    df5 = df5.rename(columns={'keyword': 'University', 'rating':'Rating', 
			'reviews':'Total Reviews'})
    return df5'''
    st.code(code, language='python')
    st.write('- Mengubah nama kolom agar menjadi lebih informatif')

    st.markdown("## Load")
    st.write('- Hasil integrasi kelima dataframe tersebut disimpan ke PostgreSQL')
    st.image('images/vm.png')
    st.write('- Menggunakan Azure Virtual Machine dalam membuat database PostgreSQL')
    st.write('- Tujuannya supaya bisa diakses oleh berbagai orang dengan mudah')
    st.write('- Spesifikasi virtual machine yang kami gunakan adalah Standard B1s yang memiliki 1 vcpu dan 1 GiB memory')
    st.write('- Sistem operasi yang kami gunakan pada VM adalah Linux Ubuntu 20.04')
    st.image('images/sqlengine.png')
    st.write('- Memanfaatkan sqlalchemy untuk melakukan koneksi ke database PostgreSQL')
    st.write('- Membuat fungsi load_to_sql untuk menyimpan dataframe ke sebuah tabel di PostgreSQL')
    st.write('- Contoh hasil query SELECT * from all_data pada database PostgreSQL kami di VM.')
    st.image('images/query.png')

    st.markdown("## Unit Test")
    st.write('- Kami menerapkan unit test setelah melakukan setiap transformasi untuk memastikan bahwa tidak ada kesalahan')
    code = '''def unit_test(df):
    assert df.shape[0] == 500, "Total number of rows should be 500"
    assert isinstance(df, pd.DataFrame), "Output should be a dataframe"
    assert df['Rank'].isnull().sum() == 0, "There should be no null values in the Rank column"
    assert df['University'].isnull().sum() == 0, "There should be no null values in the University column"
    assert (df.isnull().sum() / len(df) * 100).max() < 300, "There should be no columns with null values more than 60% of the total rows"'''
    st.code(code, language='python')
    st.write('- Jumlah baris harus ada 500 karena kita menganalisis 500 universitas terbaik di dunia')
    st.write('- Output harus dalam bentuk dataframe')
    st.write('- Tidak boleh ada null values di kolom Rank karena ini kolom yang sangat penting')
    st.write('- Tidak boleh ada null values di kolom University karena kolom ini yang digunakan sebagai key untuk integrasi dataframe')
    st.write('- Tidak boleh ada kolom yang memiliki persentase null values lebih dari 60% karena insight-nya akan menjadi kurang valid')
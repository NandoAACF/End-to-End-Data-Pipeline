import streamlit as st
from page_insight import show_insight
from page_etl_info import show_etl_info

page = st.sidebar.radio("Choose Option", ("Insight", "ETL Pipeline Information"))

if page == 'Insight':
    show_insight()
elif page == 'ETL Pipeline Information':
    show_etl_info()
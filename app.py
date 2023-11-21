import streamlit as st
from page_insight import show_insight

page = st.sidebar.radio("Choose Option", ("Insight", "ETL Pipeline Information"))

if page == 'Insight':
    show_insight()
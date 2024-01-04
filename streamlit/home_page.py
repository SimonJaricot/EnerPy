import streamlit as st
from functions import read_markdown_file

def app():
    st.markdown(read_markdown_file('home_page.md'), unsafe_allow_html=True)
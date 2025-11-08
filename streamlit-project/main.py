import streamlit as st
import pandas as pd 
import numpy as np
import pdfplumber


st.title("Resume optimizer")

file = st.file_uploader("Select a resume" , type=["pdf"])
if(file is not None):
    markdown_content = ""
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
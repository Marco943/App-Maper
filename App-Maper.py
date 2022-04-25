import streamlit as st, pandas as pd, fitz, PyPDF2
from pdfminer.high_level import extract_text

cabecalho = st.container()
corpo = st.container()

with cabecalho:
    st.header('App Maper - Extração de dados')

with corpo:
    arquivos = st.file_uploader('Carregar o Maper em PDF', accept_multiple_files=True)

    with st.expander('PyMuPDF (fitz)'):
        for arquivo in arquivos:
            doc = fitz.open(arquivo)
            st.write(doc[0].get_text())

    with st.expander('PyPDF2'):
        for arquivo in arquivos:
            doc = PyPDF2.PdfFileReader(arquivo)
            st.write(doc.getPage(0).extractText())

    with st.expander('pdfminer'):
        for arquivo in arquivos:
            doc = arquivo
            st.write(extract_text(doc))
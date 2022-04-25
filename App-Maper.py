import streamlit as st, pandas as pd, PyPDF2

cabecalho = st.container()
corpo = st.container()

with cabecalho:
    st.header('App Maper - Extração de dados')

@st.experimental_memo
def extrair_dados_lideranca(relatorio):
    arquivo = PyPDF2.PdfFileReader(relatorio)
    txt = arquivo.getPage(0).extractText()+ arquivo.getPage(1).extractText()
    txt = txt.replace('€','').replace(' \n','\n').replace('\n\n','\n')

    nome = re.findall(r'NOME:\n(.*)\n', txt)[0]
    cargo = re.findall(r'CARGO:\n(.*)\n', txt)[0]

    resposta = {'Nome': [nome], 'Cargo': [cargo]}

    competencias = re.findall(r'\n\d\d?\s-\s(.*)\n', txt) # Pega um trecho que contém 'espaço hífen espaço' e que tem um ou dois dígitos antes
    notas = re.findall(r'\n(\d\d?)\n(?:\d\d?\s-|página|Página)', txt) # Pega o número de um dígito (\d) que está depois de um parágrafo (\n) e antes de: Um texto que começa com um ou dois números, tem um espaço e um hífen; um texto 'página'; um texto 'Página'

    for i in range(len(competencias)):
        resposta[competencias[i]] = notas[i]

    resposta = pd.DataFrame.from_dict(resposta)
    return resposta

with corpo:
    arquivos = st.file_uploader('Carregar o Maper em PDF', accept_multiple_files=True)
    if len(arquivos) != 0:
        st.write('Carrege algum relatório de Maper de liderança')
    else:
        with st.expander('PyPDF2'):
            df = []
            for arquivo in arquivos:
                df.append(extrair_dados_lideranca(arquivo))
            df = pd.concat(df)
            st.dataframe(df)

        st.download_button(
            label = 'Baixar em formato CSV',
            data = df.to_csv().encode('utf-8'),
            file_name = 'Maper.csv',
            mime = 'text/csv'
        )

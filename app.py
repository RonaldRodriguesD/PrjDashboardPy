import streamlit as st
import pandas as pd

# Configuraçoes da página
st.set_page_config(page_title="Dashboard Netflix - Fatec", layout="wide")
st.title("📊 Análise de Dados Netflix")
st.markdown("Dashboard desenvolvido por Ronald R. Dantas, para a disciplina de Mineração de Dados.")

# 1 - Carregar os dados
url = 'https://raw.githubusercontent.com/profzappa/profGit/refs/heads/master/netflix_titles.csv'

@st.cache_data # Cache para não baixar o arquivo novamente
def load_data():
    data = pd.read_csv(url)
    data['type'] = data['type'].replace({'Movie': 'Filme', 'TV Show': 'Série'})
    return data

df = load_data()

# 2 - Sidebar / Filtros
st.sidebar.header("Filtros")
tipo_filtro = st.sidebar.multiselect("Selecione o Tipo:", options=df['type'].unique(), default=df['type'].unique())
df_filtrado = df[df['type'].isin(tipo_filtro)]

# 3 - Layout do Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Total de Títulos", len(df_filtrado))
col2.metric("País Principal", df_filtrado['country'].mode()[0])
col3.metric("Ano mais comum", int(df_filtrado['release_year'].mode()[0]))

# 4 - Gráficos
st.subheader("Distribuição por Tipo")
st.bar_chart(df_filtrado['type'].value_counts())
st.subheader("Top 10 Países com mais produções")
st.bar_chart(df_filtrado['country'].value_counts().head(10))

# 5 - Tabela de Dados
if st.checkbox("Mostrar base de dados"):
    st.write(df_filtrado)
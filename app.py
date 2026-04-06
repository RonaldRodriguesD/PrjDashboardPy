import streamlit as st
import pandas as pd

st.set_page_config(page_title="Netflix Data Mining - Fatec", layout="wide")

@st.cache_data
def load_and_clean_data():
    # 1. Lendo a base
    url = 'https://raw.githubusercontent.com/profzappa/profGit/refs/heads/master/netflix_titles.csv'
    df = pd.read_csv(url)

    # 2. Traduzir os nomes das colunas
    colunas_traduzidas = {
        'show_id': 'ID', 'type': 'Tipo', 'title': 'Título',
        'director': 'Diretor', 'cast': 'Elenco', 'country': 'País',
        'date_added': 'Data de Adição', 'release_year': 'Ano de Lançamento',
        'rating': 'Classificação', 'duration': 'Duração',
        'listed_in': 'Gêneros', 'description': 'Descrição'
    }
    df.rename(columns=colunas_traduzidas, inplace=True)

    # 3. Traduzir categorias
    df['Tipo'] = df['Tipo'].replace({'Movie': 'Filme', 'TV Show': 'Série'})
    
    # 4. Tratar valores nulos
    df['País'] = df['País'].fillna('Não Identificado')
    df['Diretor'] = df['Diretor'].fillna('Ninguém listado')
    
    return df

# Carregando os dados já tratados
df = load_and_clean_data()

st.title("📊 Análise Exploratória: Netflix")
st.markdown(f"**Cientista de Dados:** {st.sidebar.text_input('Nome do Aluno', 'Ronald R. Dantas')}")

# Filtro lateral por Tipo
tipos_selecionados = st.sidebar.multiselect(
    "Filtrar por Tipo:", 
    options=df['Tipo'].unique(), 
    default=df['Tipo'].unique()
)
df_filtrado = df[df['Tipo'].isin(tipos_selecionados)]

# Exibindo os 10 gêneros mais recorrentes
st.subheader("Top 10 Gêneros Mais Recorrentes")
top_generos = df_filtrado['Gêneros'].value_counts().head(10)
st.bar_chart(top_generos)

# Exibindo os 10 países
st.subheader("Top 10 Países na Base")
st.write(df_filtrado['País'].value_counts().head(10))

# Estatísticas Descritivas
if st.checkbox("Ver Estatísticas Descritivas"):
    st.write(df_filtrado.describe())
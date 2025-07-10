import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard Ensino Médio - Paraíba",
    page_icon="📊",
    layout="wide"
)

# --- Carregamento e Preparação dos Dados ---
# Usamos o cache para otimizar o carregamento dos dados
@st.cache_data
def carregar_dados():
    # COLOQUE A URL QUE VOCÊ COPIOU DO GITHUB RAW AQUI
    url_do_csv = 'https://raw.githubusercontent.com/severino-neto/dashboard-PBEMStats/refs/heads/main/PB_EnsinoMedio_Stats.csv'
    df = pd.read_csv(url_do_csv)
    
    # Limpeza de nomes de colunas (exemplo)
    df.rename(columns={
        'ESCOLAS_COM_TABLET_PARA _ALUNOS(%)': 'ESCOLAS_COM_TABLET_PARA_ALUNOS(%)'
    }, inplace=True)

    # Cálculo da média geral do ENEM (não presente originalmente)
    enem_subjects = ['MEDIA_GERAL_CN', 'MEDIA_GERAL_CH', 'MEDIA_GERAL_LC', 'MEDIA_GERAL_MT', 'MEDIA_GERAL_REDACAO']
    df['MEDIA_ENEM_GERAL'] = df[enem_subjects].mean(axis=1)
    
    return df

df = carregar_dados()

# --- Barra Lateral de Filtros (Sidebar) ---
st.sidebar.header("Filtros Interativos")

# Filtro por Ano
anos_disponiveis = sorted(df['ANO'].unique())
ano_selecionado = st.sidebar.multiselect(
    'Selecione o Ano:',
    options=anos_disponiveis,
    default=anos_disponiveis  # Padrão: todos os anos selecionados
)

# Filtro por Município
municipios_disponiveis = sorted(df['NOME_MUNICIPIO'].unique())
municipio_selecionado = st.sidebar.multiselect(
    'Selecione o Município:',
    options=municipios_disponiveis,
    default=[] # Padrão: Nenhum para não poluir o gráfico inicial
)

# Filtro por Dependência Administrativa
deps_disponiveis = sorted(df['DEPENDENCIA_ADM'].unique())
dep_selecionada = st.sidebar.multiselect(
    'Selecione a Dependência Administrativa:',
    options=deps_disponiveis,
    default=deps_disponiveis
)

# Aplicar filtros ao DataFrame
if not ano_selecionado:
    ano_selecionado = anos_disponiveis
if not dep_selecionada:
    dep_selecionada = deps_disponiveis

df_filtrado = df[
    (df['ANO'].isin(ano_selecionado)) &
    (df['DEPENDENCIA_ADM'].isin(dep_selecionada))
]

# Se um ou mais municípios forem selecionados, aplica o filtro
if municipio_selecionado:
    df_filtrado = df_filtrado[df_filtrado['NOME_MUNICIPIO'].isin(municipio_selecionado)]


# --- Layout Principal do Dashboard ---
st.title("📊 Dashboard Interativo do Ensino Médio na Paraíba")
st.markdown("Use os filtros na barra lateral para explorar os dados de desempenho, infraestrutura e socioeconômicos.")

# --- KPIs Principais ---
st.markdown("### Métricas Gerais")
col1, col2, col3 = st.columns(3)
media_enem_geral_filtrada = df_filtrado['MEDIA_ENEM_GERAL'].mean()
total_escolas_filtrado = df_filtrado['TOTAL_DE_ESCOLAS_POR_DEPENDENCIA'].sum()
num_municipios_filtrado = df_filtrado['NOME_MUNICIPIO'].nunique()

col1.metric("Média Geral no ENEM", f"{media_enem_geral_filtrada:.2f}")
col2.metric("Total de Escolas", f"{total_escolas_filtrado:,}".replace(",", "."))
col3.metric("Nº de Municípios", num_municipios_filtrado)

st.markdown("---")


# --- Visualizações Interativas ---
st.markdown("### Análises Visuais")

# Gráfico 1: Evolução Temporal da Média do ENEM
st.markdown("#### Evolução da Média Geral do ENEM por Ano")
df_evolucao = df_filtrado.groupby('ANO')['MEDIA_ENEM_GERAL'].mean().reset_index()
fig_evolucao = px.line(
    df_evolucao,
    x='ANO',
    y='MEDIA_ENEM_GERAL',
    markers=True,
    title='Média Geral do ENEM ao Longo dos Anos',
    labels={'MEDIA_ENEM_GERAL': 'Média Geral', 'ANO': 'Ano'}
)
fig_evolucao.update_layout(xaxis_dtick=1) # Forçar a exibição de todos os anos
st.plotly_chart(fig_evolucao, use_container_width=True)


# Gráfico 2: Ranking de Municípios
st.markdown("#### Ranking de Municípios por Média no ENEM")
df_ranking = df_filtrado.groupby('NOME_MUNICIPIO')['MEDIA_ENEM_GERAL'].mean().nlargest(15).sort_values(ascending=True).reset_index()
fig_ranking = px.bar(
    df_ranking,
    x='MEDIA_ENEM_GERAL',
    y='NOME_MUNICIPIO',
    orientation='h',
    title='Top 15 Municípios por Média Geral no ENEM',
    labels={'MEDIA_ENEM_GERAL': 'Média Geral', 'NOME_MUNICIPIO': 'Município'}
)
st.plotly_chart(fig_ranking, use_container_width=True)


# Gráfico 3: Análise de Correlação Interativa
st.markdown("#### Análise de Correlação Interativa")
st.write("Selecione duas variáveis para visualizar a correlação entre elas.")

col_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
col_numericas.remove('ANO') # Remover ano das opções de correlação
col_numericas.remove('COD_MUNICIPIO')

col_x = st.selectbox("Selecione a variável do Eixo X", options=col_numericas, index=col_numericas.index('PIB_PER_CAPITA'))
col_y = st.selectbox("Selecione a variável do Eixo Y", options=col_numericas, index=col_numericas.index('MEDIA_ENEM_GERAL'))

fig_corr = px.scatter(
    df_filtrado,
    x=col_x,
    y=col_y,
    color='DEPENDENCIA_ADM',
    hover_name='NOME_MUNICIPIO',
    title=f'Correlação entre {col_x} e {col_y}',
    labels={col_x: col_x.replace("_", " ").title(), col_y: col_y.replace("_", " ").title()}
)
st.plotly_chart(fig_corr, use_container_width=True)


# --- Tabela de Dados ---
st.markdown("---")
st.markdown("### Tabela de Dados Filtrados")
st.write("Visualize os dados brutos com os filtros aplicados. Você pode ordenar clicando no cabeçalho das colunas.")
st.dataframe(df_filtrado)
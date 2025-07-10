import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback, dash_table
import numpy as np

# Carregar os dados
df = pd.read_csv('PB_EnsinoMedio_Stats.csv')

# Limpeza e preparação dos dados
def prepare_data(df):
    # Converter colunas numéricas
    numeric_columns = [
        'MEDIA_GERAL_CN', 'MEDIA_GERAL_CH', 'MEDIA_GERAL_LC', 'MEDIA_GERAL_MT', 'MEDIA_GERAL_REDACAO',
        'MEDIA_CN_F', 'MEDIA_CH_F', 'MEDIA_LC_F', 'MEDIA_MT_F', 'MEDIA_REDACAO_F',
        'MEDIA_CN_M', 'MEDIA_CH_M', 'MEDIA_LC_M', 'MEDIA_MT_M', 'MEDIA_REDACAO_M',
        'TAXA_APROVACAO_3S', 'NOTA_SAEB_MT', 'NOTA_SAEB_LC', 'IDEB',
        'PIB_MUNICIPIO', 'PIB_PER_CAPITA', 'VALOR_ADM_PUBLICA'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Mapear dependência administrativa
    dependencia_map = {
        1: 'Federal',
        2: 'Estadual', 
        3: 'Municipal',
        4: 'Privada'
    }
    df['DEPENDENCIA_NOME'] = df['DEPENDENCIA_ADM'].map(dependencia_map)
    
    return df

df = prepare_data(df)

# Configuração do app Dash
app = dash.Dash(__name__)
app.title = "Dashboard - Ensino Médio PB"

# Layout do dashboard
app.layout = html.Div([
    html.Div([
        html.H1("Dashboard - Ensino Médio da Paraíba", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
        html.P("Análise interativa dos dados educacionais dos municípios paraibanos (2017-2023)",
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '16px'})
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa'}),
    
    # Filtros
    html.Div([
        html.Div([
            html.Label("Ano:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='ano-dropdown',
                options=[{'label': str(ano), 'value': ano} for ano in sorted(df['ANO'].unique())],
                value=df['ANO'].max(),
                style={'marginBottom': '15px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label("Dependência:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='dependencia-dropdown',
                options=[{'label': 'Todas', 'value': 'todas'}] + 
                        [{'label': dep, 'value': dep} for dep in df['DEPENDENCIA_NOME'].dropna().unique()],
                value='todas',
                style={'marginBottom': '15px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%', 'verticalAlign': 'top'}),
        
        html.Div([
            html.Label("Municípios:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='municipio-dropdown',
                options=[{'label': 'Todos', 'value': 'todos'}] + 
                        [{'label': mun, 'value': mun} for mun in sorted(df['NOME_MUNICIPIO'].unique())],
                value=['Campina Grande', 'João Pessoa', 'Cajazeiras'],
                multi=True,
                style={'marginBottom': '15px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'margin': '20px', 'borderRadius': '10px'}),
    
    # Estatísticas resumo
    html.Div(id='stats-cards', style={'margin': '20px'}),
    
    # Gráficos principais
    html.Div([
        # Primeira linha de gráficos
        html.Div([
            dcc.Graph(id='media-areas-graph')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='comparacao-genero-graph')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Segunda linha de gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='pib-desempenho-graph')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='ideb-aprovacao-graph')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Terceira linha - Infraestrutura
    html.Div([
        dcc.Graph(id='infraestrutura-graph')
    ], style={'padding': '10px', 'margin': '20px'}),
    
    # Tabela de ranking
    html.Div([
        html.H3("Top 10 Municípios por Desempenho", style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.Div(id='ranking-table')
    ], style={'padding': '20px', 'margin': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
    
], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ffffff'})

# Callbacks para interatividade
@app.callback(
    [Output('stats-cards', 'children'),
     Output('media-areas-graph', 'figure'),
     Output('comparacao-genero-graph', 'figure'),
     Output('pib-desempenho-graph', 'figure'),
     Output('ideb-aprovacao-graph', 'figure'),
     Output('infraestrutura-graph', 'figure'),
     Output('ranking-table', 'children')],
    [Input('ano-dropdown', 'value'),
     Input('dependencia-dropdown', 'value'),
     Input('municipio-dropdown', 'value')]
)
def update_dashboard(ano_selecionado, dependencia_selecionada, municipios_selecionados):
    # Filtrar dados
    df_filtered = df[df['ANO'] == ano_selecionado].copy()
    
    if dependencia_selecionada != 'todas':
        df_filtered = df_filtered[df_filtered['DEPENDENCIA_NOME'] == dependencia_selecionada]
    
    if municipios_selecionados and 'todos' not in municipios_selecionados:
        if isinstance(municipios_selecionados, str):
            municipios_selecionados = [municipios_selecionados]
        df_filtered = df_filtered[df_filtered['NOME_MUNICIPIO'].isin(municipios_selecionados)]
    
    # Cards de estatísticas
    total_municipios = df_filtered['NOME_MUNICIPIO'].nunique()
    media_geral = df_filtered[['MEDIA_GERAL_CN', 'MEDIA_GERAL_CH', 'MEDIA_GERAL_LC', 'MEDIA_GERAL_MT', 'MEDIA_GERAL_REDACAO']].mean().mean()
    taxa_aprovacao_media = df_filtered['TAXA_APROVACAO_3S'].mean()
    ideb_medio = df_filtered['IDEB'].mean()
    
    stats_cards = html.Div([
        html.Div([
            html.H4(f"{total_municipios}", style={'color': '#3498db', 'margin': '0'}),
            html.P("Municípios", style={'margin': '0'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px', 'width': '22%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.H4(f"{media_geral:.1f}" if not pd.isna(media_geral) else "N/A", style={'color': '#e74c3c', 'margin': '0'}),
            html.P("Média Geral ENEM", style={'margin': '0'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px', 'width': '22%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.H4(f"{taxa_aprovacao_media:.1f}%" if not pd.isna(taxa_aprovacao_media) else "N/A", style={'color': '#27ae60', 'margin': '0'}),
            html.P("Taxa de Aprovação", style={'margin': '0'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px', 'width': '22%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.H4(f"{ideb_medio:.1f}" if not pd.isna(ideb_medio) else "N/A", style={'color': '#f39c12', 'margin': '0'}),
            html.P("IDEB Médio", style={'margin': '0'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px', 'width': '22%', 'display': 'inline-block', 'margin': '1%'})
    ])
    
    # Gráfico 1: Médias por área de conhecimento
    areas = ['MEDIA_GERAL_CN', 'MEDIA_GERAL_CH', 'MEDIA_GERAL_LC', 'MEDIA_GERAL_MT', 'MEDIA_GERAL_REDACAO']
    area_names = ['Ciências da Natureza', 'Ciências Humanas', 'Linguagens e Códigos', 'Matemática', 'Redação']
    
    medias_por_area = []
    for area in areas:
        media = df_filtered[area].mean()
        medias_por_area.append(media)
    
    fig1 = px.bar(
        x=area_names, 
        y=medias_por_area,
        title="Médias por Área de Conhecimento (ENEM)",
        labels={'x': 'Área de Conhecimento', 'y': 'Média'},
        color=medias_por_area,
        color_continuous_scale='viridis'
    )
    fig1.update_layout(showlegend=False, height=400)
    
    # Gráfico 2: Comparação por gênero
    if len(df_filtered) > 0:
        genero_data = []
        for area, area_name in zip(areas, area_names):
            area_f = area.replace('GERAL', 'F')
            area_m = area.replace('GERAL', 'M')
            
            if area_f in df_filtered.columns and area_m in df_filtered.columns:
                media_f = df_filtered[area_f].mean()
                media_m = df_filtered[area_m].mean()
                
                genero_data.extend([
                    {'Área': area_name, 'Gênero': 'Feminino', 'Média': media_f},
                    {'Área': area_name, 'Gênero': 'Masculino', 'Média': media_m}
                ])
        
        df_genero = pd.DataFrame(genero_data)
        fig2 = px.bar(
            df_genero, 
            x='Área', 
            y='Média', 
            color='Gênero',
            title="Comparação de Desempenho por Gênero",
            barmode='group',
            color_discrete_map={'Feminino': '#e74c3c', 'Masculino': '#3498db'}
        )
        fig2.update_layout(height=400)
    else:
        fig2 = px.bar(title="Dados insuficientes para comparação por gênero")
    
    # Gráfico 3: PIB vs Desempenho
    if len(df_filtered) > 0 and 'PIB_PER_CAPITA' in df_filtered.columns:
        df_filtered['MEDIA_GERAL'] = df_filtered[areas].mean(axis=1)
        fig3 = px.scatter(
            df_filtered,
            x='PIB_PER_CAPITA',
            y='MEDIA_GERAL',
            hover_data=['NOME_MUNICIPIO', 'DEPENDENCIA_NOME'],
            title="PIB per Capita vs Desempenho Médio",
            labels={'PIB_PER_CAPITA': 'PIB per Capita (R$)', 'MEDIA_GERAL': 'Média Geral ENEM'},
            color='DEPENDENCIA_NOME'
        )
        fig3.update_layout(height=400)
    else:
        fig3 = px.scatter(title="Dados insuficientes para análise PIB vs Desempenho")
    
    # Gráfico 4: IDEB vs Taxa de Aprovação
    if len(df_filtered) > 0 and 'IDEB' in df_filtered.columns and 'TAXA_APROVACAO_3S' in df_filtered.columns:
        fig4 = px.scatter(
            df_filtered,
            x='IDEB',
            y='TAXA_APROVACAO_3S',
            hover_data=['NOME_MUNICIPIO', 'DEPENDENCIA_NOME'],
            title="IDEB vs Taxa de Aprovação",
            labels={'IDEB': 'IDEB', 'TAXA_APROVACAO_3S': 'Taxa de Aprovação 3ª Série (%)'},
            color='DEPENDENCIA_NOME'
        )
        fig4.update_layout(height=400)
    else:
        fig4 = px.scatter(title="Dados insuficientes para análise IDEB vs Taxa de Aprovação")
    
    # Gráfico 5: Infraestrutura
    infra_cols = ['ACESSO_A_INTERNET(%)', 'ESCOLAS_COM_LABORATÓRIO_DE_INFORMÁTICA(%)', 
                  'ESCOLAS_COM_DESKTOP_PARA_ALUNOS(%)', 'ESCOLAS_COM_TABLET_PARA _ALUNOS(%)']
    infra_names = ['Acesso à Internet', 'Laboratório de Informática', 'Desktop para Alunos', 'Tablet para Alunos']
    
    if len(df_filtered) > 0:
        infra_data = []
        for col, name in zip(infra_cols, infra_names):
            if col in df_filtered.columns:
                media = df_filtered[col].mean()
                infra_data.append({'Infraestrutura': name, 'Porcentagem': media})
        
        df_infra = pd.DataFrame(infra_data)
        fig5 = px.bar(
            df_infra,
            x='Infraestrutura',
            y='Porcentagem',
            title="Infraestrutura Tecnológica das Escolas (%)",
            color='Porcentagem',
            color_continuous_scale='blues'
        )
        fig5.update_layout(showlegend=False, height=400)
    else:
        fig5 = px.bar(title="Dados insuficientes para análise de infraestrutura")
    
    # Tabela de ranking
    if len(df_filtered) > 0:
        df_ranking = df_filtered.copy()
        df_ranking['MEDIA_GERAL'] = df_ranking[areas].mean(axis=1)
        df_ranking = df_ranking.sort_values('MEDIA_GERAL', ascending=False).head(10)
        
        ranking_data = []
        for i, (_, row) in enumerate(df_ranking.iterrows()):
            ranking_data.append({
                'Posição': i+1,
                'Município': row['NOME_MUNICIPIO'],
                'Dependência': row['DEPENDENCIA_NOME'],
                'Média Geral': f"{row['MEDIA_GERAL']:.2f}" if not pd.isna(row['MEDIA_GERAL']) else "N/A",
                'IDEB': f"{row['IDEB']:.1f}" if not pd.isna(row['IDEB']) else "N/A",
                'Taxa Aprovação': f"{row['TAXA_APROVACAO_3S']:.1f}%" if not pd.isna(row['TAXA_APROVACAO_3S']) else "N/A"
            })
        
        ranking_table = dash_table.DataTable(
            data=ranking_data,
            columns=[{"name": col, "id": col} for col in ranking_data[0].keys()],
            style_cell={'textAlign': 'center', 'padding': '10px'},
            style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {
                    'if': {'row_index': 0},
                    'backgroundColor': '#f1c40f',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                {
                    'if': {'row_index': 1},
                    'backgroundColor': '#bdc3c7',
                    'color': 'black'
                },
                {
                    'if': {'row_index': 2},
                    'backgroundColor': '#e67e22',
                    'color': 'white'
                }
            ]
        )
    else:
        ranking_table = html.P("Nenhum dado disponível para o ranking.")
    
    return stats_cards, fig1, fig2, fig3, fig4, fig5, ranking_table

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)


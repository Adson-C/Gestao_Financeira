import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO


# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        html.Legend("Tabela de despesas"),
        html.Div(id="tabela-despesas", className="dbc"),
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph', style={"margin-right": "20px"}),
        ], width=9),
        
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Despesas"),
                    html.Legend("R$ -", id="valor_despesa_card", style={'font-size': '60px'}),
                    html.H6("Total de despesas"),
                ], style={'text-align': 'center', 'padding-top': '30px'}))
        ], width=3),
    ]),
], style={"padding": "10px"})


# =========  Callbacks  =========== #
# Tabela
@app.callback(
     Output("tabela-despesas", "children"),
     [Input("store-despesas", "data"),
      Input("dropdown-despesa", "value"),
      Input("store-filtros-despesas", "data")],  # Adicionado para filtrar com base nas categorias selecionadas
)
def imprimir_tabela(data, categorias_selecionadas, stored_filters):
    df = pd.DataFrame(data)
    
    # Verificar se o dataframe está vazio ou não tem as colunas necessárias
    if df.empty or not all(col in df.columns for col in ['Categoria', 'Data', 'Efetuado', 'Fixo']):
        # Retornar uma tabela vazia
        return dash_table.DataTable(
            id='datatable-interactivity',
            columns=[{"name": i, "id": i} for i in ['Data', 'Valor', 'Categoria', 'Descrição', 'Fixo', 'Efetuado']],
            data=[],
            filter_action="native",
            sort_action="native",
            sort_mode="single",
            page_action="native",
            page_current=0,
            page_size=10,
        )
    
    # Se categorias_selecionadas for None, usar stored_filters
    if categorias_selecionadas is None and stored_filters:
        categorias_selecionadas = stored_filters
    
    # Filtrar por categorias se houver seleção
    if categorias_selecionadas:
        df = df[df['Categoria'].isin(categorias_selecionadas)]
    
    # Converter para datetime e depois para date
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    # Filtrar valores nulos após conversão
    df = df.dropna(subset=['Data'])
    df['Data'] = df['Data'].dt.date

    # Converter os valores booleanos para strings
    df.loc[df['Efetuado'] == 0, 'Efetuado'] = 'Não'
    df.loc[df['Efetuado'] == 1, 'Efetuado'] = 'Sim'

    df.loc[df['Fixo'] == 0, 'Fixo'] = 'Não'
    df.loc[df['Fixo'] == 1, 'Fixo'] = 'Sim'

    df = df.fillna('-')

    df = df.sort_values(by='Data', ascending=False)

    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixo" or i == "Efetuado"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],

        data=df.to_dict('records'),
        filter_action="native",    
        sort_action="native",       
        sort_mode="single",  
        selected_columns=[],        
        selected_rows=[],          
        page_action="native",      
        page_current=0,             
        page_size=10,                        
    ),

    return tabela

# Bar Graph - Modificado para filtrar por categorias            
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('store-despesas', 'data'),
     Input("dropdown-despesa", "value"),
     Input("store-filtros-despesas", "data"),
     Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def bar_chart(data, categorias_selecionadas, stored_filters, theme):
    df = pd.DataFrame(data)
    
    # Verificar se o dataframe está vazio ou não tem as colunas necessárias
    if df.empty or 'Categoria' not in df.columns or 'Valor' not in df.columns:
        # Criar uma figura vazia
        fig = px.bar(
            pd.DataFrame({'Categoria': ['Sem dados'], 'Valor': [0]}),
            x='Categoria',
            y='Valor',
            title="Despesas Gerais"
        )
        fig.update_layout(template=template_from_url(theme))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig
    
    # Se categorias_selecionadas for None, usar stored_filters
    if categorias_selecionadas is None and stored_filters:
        categorias_selecionadas = stored_filters
    
    # Filtrar por categorias se houver seleção
    if categorias_selecionadas:
        df = df[df['Categoria'].isin(categorias_selecionadas)]
        
    df_grouped = df.groupby("Categoria").sum()[["Valor"]].reset_index()
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title="Despesas Gerais")
    graph.update_layout(template=template_from_url(theme))
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return graph

# Simple card - Modificado para filtrar por categorias
@app.callback(
    Output('valor_despesa_card', 'children'),
    [Input('store-despesas', 'data'),
     Input("dropdown-despesa", "value"),
     Input("store-filtros-despesas", "data")]
)
def display_desp(data, categorias_selecionadas, stored_filters):
    df = pd.DataFrame(data)
    
    # Verificar se o dataframe está vazio ou não tem a coluna necessária
    if df.empty or 'Categoria' not in df.columns or 'Valor' not in df.columns:
        return "R$ 0.00"
    
    # Se categorias_selecionadas for None, usar stored_filters
    if categorias_selecionadas is None and stored_filters:
        categorias_selecionadas = stored_filters
    
    # Filtrar por categorias se houver seleção
    if categorias_selecionadas:
        df = df[df['Categoria'].isin(categorias_selecionadas)]
    
    valor = df['Valor'].sum()
    
    return f"R$ {valor:.2f}"
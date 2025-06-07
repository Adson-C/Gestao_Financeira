from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
# from globals import *

from app import app
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO


# Card icon style
card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
    }

graph_margin = dict(l=25, r=25, t=25, b=0)


# =========  Layout  =========== #
layout = dbc.Col([
        dbc.Row([
            # Saldo Total
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Saldo"),
                        html.H5("R$ -", id="p-saldo-dashboards", style={}),
                    ], style={'padding-left': '20px', 'padding-top': '10px'}),
                    dbc.Card(
                        html.Div(className='fa fa-university', style=card_icon),
                        color='warning',
                        style={'maxWidth': 75, 'height': 100, 'margin-left': '-10'},
                    ),
                ])
            ], width=4),  # Responsivo com breakpoints para diferentes tamanhos de tela  xs=12, sm=6, md=4
            # Receitas
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Receita"),
                        html.H5("R$ -", id="p-receita-dashboards", style={}),
                    ], style={'padding-left': '20px', 'padding-top': '10px'}),
                    dbc.Card(
                        html.Div(className='fa fa-smile-o', style=card_icon),
                        color='success',
                         style={'maxWidth': 75, 'height': 100, 'margin-left': '-10'},
                    ),
                ])
            ], width=4),  # Responsivo xs=12, sm=6, md=4
            # Despesas
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Despesa"),
                        html.H5("R$ -", id="p-despesa-dashboards", style={}),
                    ], style={'padding-left': '20px', 'padding-top': '10px'}),
                    dbc.Card(
                        html.Div(className='fa fa-meh-o', style=card_icon),
                        color='danger',
                         style={'maxWidth': 75, 'height': 100, 'margin-left': '-10'},
                    ),
                ])
            ], width=4),  # Responsivo xs=12, sm=6, md=4
        ], style={'margin': '10px'}),
        # Filtro de Análise lançamentos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Legend("Filtrar lançamentos", className="card-title"),
                    html.Label('Categorias das receitas'),
                    html.Div(
                        dcc.Dropdown(
                        id="dropdown-receita",
                        clearable=False,
                        style={'width': '100%'},
                        persistence=True,
                        persistence_type="session",
                        multi=True)
                ),
                html.Label('Categorias das despesas', style={'margin-top': '10px'}),
                    dcc.Dropdown(
                        id="dropdown-despesa",
                        clearable=False,
                        style={'width': '100%'},
                        persistence=True,
                        persistence_type="session",
                        multi=True
                    ),
                # Filtro de Análise Periódo
                html.Legend("Período de Análise", style={'margin-top': '10px'}),
                dcc.DatePickerRange(
                    month_format="Do MMM, YY",
                    end_date_placeholder_text="Data...",
                    start_date=datetime(2024, 4, 1).date(),
                    end_date=datetime.today() + timedelta(days=31),
                    updatemode="singledate",
                    id="date-picker-config",
                    style={'z-index': '100'}),
                
                ],style={'height': '100%', 'padding': '20px'})
            ], width=4), # responsivoxs=12, sm=12, md=4)
            # Graficos 1
            dbc.Col(
                dbc.Card(dcc.Graph(id="graph1"), style={'height': '100%', 'padding': '10px'}), width=8),
        ], style={'margin': '10px'}),

        dbc.Row([
            # Grafico 2 3 4
            dbc.Col(dbc.Card(dcc.Graph(id="graph2"), style={'padding': '10px'}),  width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph3"), style={'padding': '10px'}),  width=3),
            dbc.Col(dbc.Card(dcc.Graph(id="graph4"), style={'padding': '10px'}),  width=3),
        ])
    ])

# =========  Callbacks  =========== #
# Receitas - Modificado para filtrar com base nas categorias selecionadas
@app.callback([Output("dropdown-receita", "options"),
              Output("dropdown-receita", "value"),
              Output("p-receita-dashboards", "children")],
              [Input("store-receitas", "data"),
               Input("dropdown-receita", "value"),
               Input("store-filtros-receitas", "data")])
def populate_dropdown_receita(data, selected_categories, stored_filters):
    df = pd.DataFrame(data)
    
    # Verificar se o dataframe está vazio ou não tem a coluna Categoria
    if df.empty or 'Categoria' not in df.columns:
        return [], [], "R$ 0.00"
    
    # Opções para o dropdown
    options = [{"label": x, "value": x} for x in df['Categoria'].unique() if pd.notna(x)]
    
    # Valores padrão para o dropdown (todas as categorias)
    if selected_categories is None:
        # Se houver filtros armazenados, use-os
        if stored_filters:
            selected_categories = stored_filters
        else:
            selected_categories = [x for x in df['Categoria'].unique() if pd.notna(x)]
    
    # Calcular o valor total com base nas categorias selecionadas
    if selected_categories:
        filtered_df = df[df['Categoria'].isin(selected_categories)]
        valor = filtered_df['Valor'].sum()
    else:
        valor = 0
    
    return options, selected_categories, f"R$ {valor:.2f}"

# Despesas - Modificado para filtrar com base nas categorias selecionadas
@app.callback([Output("dropdown-despesa", "options"),
              Output("dropdown-despesa", "value"),
              Output("p-despesa-dashboards", "children")],
              [Input("store-despesas", "data"),
               Input("dropdown-despesa", "value"),
               Input("store-filtros-despesas", "data")])
def populate_dropdown_despesa(data, selected_categories, stored_filters):
    df = pd.DataFrame(data)
    
    # Verificar se o dataframe está vazio ou não tem a coluna Categoria
    if df.empty or 'Categoria' not in df.columns:
        return [], [], "R$ 0.00"
    
    # Opções para o dropdown
    options = [{"label": x, "value": x} for x in df['Categoria'].unique() if pd.notna(x)]
    
    # Valores padrão para o dropdown (todas as categorias)
    if selected_categories is None:
        # Se houver filtros armazenados, use-os
        if stored_filters:
            selected_categories = stored_filters
        else:
            selected_categories = [x for x in df['Categoria'].unique() if pd.notna(x)]
    
    # Calcular o valor total com base nas categorias selecionadas
    if selected_categories:
        filtered_df = df[df['Categoria'].isin(selected_categories)]
        valor = filtered_df['Valor'].sum()
    else:
        valor = 0
    
    return options, selected_categories, f"R$ {valor:.2f}"

# Saldos total - Modificado para considerar apenas as categorias selecionadas
@app.callback(
    Output("p-saldo-dashboards", "children"),
    [Input("store-receitas", "data"),
     Input("store-despesas", "data"),
     Input("dropdown-receita", "value"),
     Input("dropdown-despesa", "value")])
def saldo_total(receitas, despesas, receitas_selecionadas, despesas_selecionadas):
    df_receitas = pd.DataFrame(receitas)
    df_despesas = pd.DataFrame(despesas)
    
    # Filtrar pelas categorias selecionadas
    if receitas_selecionadas and 'Categoria' in df_receitas.columns and not df_receitas.empty:
        df_receitas_filtrado = df_receitas[df_receitas["Categoria"].isin(receitas_selecionadas)]
        valor_receitas = df_receitas_filtrado["Valor"].sum()
    else:
        valor_receitas = 0
    
    if despesas_selecionadas and 'Categoria' in df_despesas.columns and not df_despesas.empty:
        df_despesas_filtrado = df_despesas[df_despesas["Categoria"].isin(despesas_selecionadas)]
        valor_despesas = df_despesas_filtrado["Valor"].sum()
    else:
        valor_despesas = 0
    
    # Calcular o saldo
    saldo = valor_receitas - valor_despesas
    
    return f'R$ {saldo:.2f}'

# =========  Callbacks  =========== #
# Graficos 1
@app.callback(
    Output("graph1", "figure"),
    [
        Input("store-receitas", "data"),
        Input("store-despesas", "data"),
        Input("dropdown-despesa", "value"),
        Input("dropdown-receita", "value"),
        Input(ThemeChangerAIO.ids.radio("theme"), "value")
    ],
)
def create_graph1(receita_data, despesa_data, despesa, receita, theme):
    df_ds = pd.DataFrame(despesa_data)
    df_rc = pd.DataFrame(receita_data)
    
    # Certifique-se de que os dataframes têm as colunas necessárias
    required_columns = ['Data', 'Valor', 'Categoria']
    
    if not all(col in df_ds.columns for col in required_columns) or df_ds.empty:
        df_ds = pd.DataFrame(columns=required_columns)
        df_ds['Data'] = pd.to_datetime([])
        df_ds['Valor'] = []
        df_ds['Categoria'] = []
    else:
        df_ds['Data'] = pd.to_datetime(df_ds['Data'], errors='coerce')
        df_ds = df_ds.sort_values(by='Data', ascending=True)
    
    if not all(col in df_rc.columns for col in required_columns) or df_rc.empty:
        df_rc = pd.DataFrame(columns=required_columns)
        df_rc['Data'] = pd.to_datetime([])
        df_rc['Valor'] = []
        df_rc['Categoria'] = []
    else:
        df_rc['Data'] = pd.to_datetime(df_rc['Data'], errors='coerce')
        df_rc = df_rc.sort_values(by='Data', ascending=True)
    
    # Filtrar pelos valores selecionados
    if despesa and not df_ds.empty:
        df_ds = df_ds[df_ds['Categoria'].isin(despesa)]
    else:
        df_ds = df_ds[df_ds['Categoria'] == "nenhuma_categoria"]  # Para não mostrar nada
    
    if receita and not df_rc.empty:
        df_rc = df_rc[df_rc['Categoria'].isin(receita)]
    else:
        df_rc = df_rc[df_rc['Categoria'] == "nenhuma_categoria"]  # Para não mostrar nada
    
    dfs = [df_ds, df_rc]

    for df in dfs:
        if not df.empty and 'Valor' in df.columns:
            df['Acumulado'] = df['Valor'].cumsum()
            if 'Data' in df.columns:
                df['Mes'] = df['Data'].dt.month
        
    df_receitas_mes = df_rc.groupby("Mes")["Valor"].sum() if not df_rc.empty and 'Mes' in df_rc.columns else pd.Series(dtype='float64')
    df_despesas_mes = df_ds.groupby("Mes")["Valor"].sum() if not df_ds.empty and 'Mes' in df_ds.columns else pd.Series(dtype='float64')
    
    # Criar o df_saldo_mes com base nos dados filtrados
    meses_combinados = set(df_receitas_mes.index).union(set(df_despesas_mes.index))
    df_saldo_mes = pd.DataFrame(index=sorted(meses_combinados), columns=["Valor"])
    
    for mes in meses_combinados:
        receita_valor = df_receitas_mes.get(mes, 0)
        despesa_valor = df_despesas_mes.get(mes, 0)
        df_saldo_mes.loc[mes, "Valor"] = receita_valor - despesa_valor
    
    df_saldo_mes = df_saldo_mes.reset_index()
    df_saldo_mes.columns = ["Mes", "Valor"]
    
    # Calcular acumulado
    if not df_saldo_mes.empty:
        df_saldo_mes['Acumulado'] = df_saldo_mes['Valor'].cumsum()
        df_saldo_mes['Mes'] = df_saldo_mes['Mes'].apply(lambda x: calendar.month_abbr[x] if 1 <= x <= 12 else str(x))

    fig = go.Figure()
    
    # Adicionar as linhas no gráfico
    if not df_rc.empty and 'Data' in df_rc.columns and 'Acumulado' in df_rc.columns:
        fig.add_trace(go.Scatter(name='Receitas', x=df_rc['Data'], y=df_rc['Acumulado'], fill='tonextx', mode='lines'))
    
    if not df_ds.empty and 'Data' in df_ds.columns and 'Acumulado' in df_ds.columns:
        fig.add_trace(go.Scatter(name='Despesas', x=df_ds['Data'], y=df_ds['Acumulado'], fill='tonexty', mode='lines'))
    
    if not df_saldo_mes.empty and 'Acumulado' in df_saldo_mes.columns:
        fig.add_trace(go.Scatter(name='Saldo Mensal', x=df_saldo_mes['Mes'], y=df_saldo_mes['Acumulado'], mode='lines'))

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# =========  Callbacks  =========== #
# Graficos 2 Filtro de Análise lançamentos
@app.callback(
    Output("graph2", "figure"),
    
    [Input("store-receitas", "data"),
    Input("store-despesas", "data"),
    Input("dropdown-despesa", "value"),
    Input("dropdown-receita", "value"),
    Input("date-picker-config", "start_date"),
    Input("date-picker-config", "end_date"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def graph2_show(data_receita, data_despesa, despesa, receita, start_date, end_date, theme):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)

    # Verificar se os dataframes têm as colunas necessárias
    if 'Categoria' not in df_rc.columns or df_rc.empty:
        df_rc = pd.DataFrame(columns=['Data', 'Valor', 'Categoria', 'Output'])
        df_rc['Data'] = pd.to_datetime([])
    else:
        df_rc['Output'] = 'Receitas'
        df_rc["Data"] = pd.to_datetime(df_rc["Data"], errors='coerce')
    
    if 'Categoria' not in df_ds.columns or df_ds.empty:
        df_ds = pd.DataFrame(columns=['Data', 'Valor', 'Categoria', 'Output'])
        df_ds['Data'] = pd.to_datetime([])
    else:
        df_ds['Output'] = 'Despesas'
        df_ds["Data"] = pd.to_datetime(df_ds["Data"], errors='coerce')

    df_final = pd.concat([df_ds, df_rc])
    
    # Certificar-se de que as datas são datetime
    if start_date is not None and end_date is not None:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df_final = df_final[(df_final["Data"] >= start_date) & (df_final["Data"] <= end_date)]
    
    # Filtrar pelas categorias selecionadas
    categorias_filtro = []
    if receita:
        categorias_filtro.extend(receita)
    if despesa:
        categorias_filtro.extend(despesa)
    
    if categorias_filtro:
        df_final = df_final[df_final["Categoria"].isin(categorias_filtro)]

    # grafico 2
    fig = px.bar(df_final, x="Data", y="Valor", color="Output", barmode="group")
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

# =========  Callbacks  =========== #
# Graficos 3
@app.callback(
    Output("graph3", "figure"),
    
    [Input("store-receitas", "data"),
     Input("dropdown-receita", "value"),
     Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_receita3(data_receita, receita, theme):
    df = pd.DataFrame(data_receita)
    
    # Verificar se o dataframe tem as colunas necessárias
    if 'Categoria' not in df.columns or 'Valor' not in df.columns or df.empty:
        # Criar um dataframe vazio com as colunas necessárias
        df = pd.DataFrame({'Categoria': ['Sem dados'], 'Valor': [0]})
    
    # Filtrar pelos valores selecionados
    if receita:
        df = df[df['Categoria'].isin(receita)]
    else:
        df = df[df['Categoria'] == "nenhuma_categoria"]  # Para não mostrar nada

    # grafico 3
    fig = px.pie(df, values=df['Valor'], names=df['Categoria'], hole=.2)
    fig.update_layout(title={"text": "Receitas"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

# =========  Callbacks  =========== #
# Graficos 4
@app.callback(
    Output("graph4", "figure"),
    
    [Input("store-despesas", "data"),
     Input("dropdown-despesa", "value"),
     Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_receita4(data_despesa, despesa, theme):
    df = pd.DataFrame(data_despesa)
    
    # Verificar se o dataframe tem as colunas necessárias
    if 'Categoria' not in df.columns or 'Valor' not in df.columns or df.empty:
        # Criar um dataframe vazio com as colunas necessárias
        df = pd.DataFrame({'Categoria': ['Sem dados'], 'Valor': [0]})
    
    # Filtrar pelos valores selecionados
    if despesa:
        df = df[df["Categoria"].isin(despesa)]
    else:
        df = df[df["Categoria"] == "nenhuma_categoria"]  # Para não mostrar nada

    # grafico 4
    fig = px.pie(df, values=df['Valor'], names=df['Categoria'], hole=.2)
    fig.update_layout(title={"text": "Despesas"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig
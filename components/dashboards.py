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
# Receitas
@app.callback([Output("dropdown-receita", "options"),
              Output("dropdown-receita", "value"),
              Output("p-receita-dashboards", "children")],
              Input("store-receitas", "data"))
def populate_dropdown_receita(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df['Categoria'].unique().tolist()
    
    return [([{"label": x, "value": x} for x in df['Categoria'].unique()]), val, f"R$ {valor}"]

# =========  Callbacks  =========== #
# Despesas
@app.callback([Output("dropdown-despesa", "options"),
              Output("dropdown-despesa", "value"),
              Output("p-despesa-dashboards", "children")],
              Input("store-despesas", "data"))
def populate_dropdown_despesa(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df['Categoria'].unique().tolist()
    
    return [([{"label": x, "value": x} for x in df['Categoria'].unique()]), val, f"R$ {valor}"]


# =========  Callbacks  =========== #
# Saldos total
@app.callback(
    Output("p-saldo-dashboards", "children"),
    Input("store-receitas", "data"),
    Input("store-despesas", "data"))
def saldo_total(receitas, despesas):
    df_receitas = pd.DataFrame(receitas)
    df_despesas = pd.DataFrame(despesas)
    valor = df_receitas["Valor"].sum() - df_despesas["Valor"].sum()
    return f'R$ {valor}'

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
    df_ds = pd.DataFrame(despesa_data).sort_values(by='Data', ascending=True)
    df_rc = pd.DataFrame(receita_data).sort_values(by='Data', ascending=True)
    
    dfs = [df_ds, df_rc]

    for df in dfs:
        df['Acumulado'] = df['Valor'].cumsum()
        df['Data'] = pd.to_datetime(df['Data'])
        df['Mes'] = df['Data'].apply(lambda x: x.month)
        
    df_receitas_mes = df_rc.groupby("Mes")["Valor"].sum()
    df_despesas_mes = df_ds.groupby("Mes")["Valor"].sum()
    df_saldo_mes = df_receitas_mes - df_despesas_mes
    df_saldo_mes.to_frame()
    df_saldo_mes = df_saldo_mes.reset_index()
    df_saldo_mes['Acumulado'] = df_saldo_mes['Valor'].cumsum()
    df_saldo_mes['Mes'] = df['Mes'].apply(lambda x: calendar.month_abbr[x])

    df_ds = df_ds[df_ds['Categoria'].isin(despesa)]
    df_rc = df_rc[df_rc['Categoria'].isin(receita)]

    fig = go.Figure()
    
    # fig.add_trace(go.Scatter(name='Despesas', x=df_ds['Data'], y=df_ds['Acumulo'], fill='tonexty', mode='lines'))
    fig.add_trace(go.Scatter(name='Receitas', x=df_rc['Data'], y=df_rc['Acumulado'], fill='tonextx', mode='lines'))
    # fig.add_trace(go.Scatter(name='Saldo Mensal', x=df_saldo_mes['Mes'], y=df_saldo_mes['Acumulado'], mode='lines'))

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
def grah2_show(data_receita, data_despesa, despesa, receita, start_date, end_date, theme):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)

    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat([df_ds, df_rc])
    df_final["Data"] = pd.to_datetime(df_final["Data"])

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_final = df_final[(df_final["Data"] >= start_date) & (df_final["Data"] <= end_date)]
    df_final = df_final[(df_final["Categoria"].isin(receita)) | (df_final["Categoria"].isin(despesa))]

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
    df = df[(df['Categoria'].isin(receita))]

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
def pie_receita4(data_despesa, despesa,theme):
    df = pd.DataFrame(data_despesa)
    df = df[(df["Categoria"].isin(despesa))]

    # grafico 4
    fig = px.pie(df, values=df['Valor'], names=df['Categoria'], hole=.2)
    fig.update_layout(title={"text": "Despesas"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

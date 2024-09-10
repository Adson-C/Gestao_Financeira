from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_templates as dbc
import pandas as pd
import plotly.express as px

from app import *

from components import sidebar, dashboards, extratos

# variaveis globais
from globals import *


# DataFrames and Dcc.Store

df_receitas = pd.read_csv("df_receitas.csv", index_col=0, parse_dates=True)
df_receitas_aux = df_receitas.to_dict()

df_despesas = pd.read_csv("df_despesas.csv", index_col=0, parse_dates=True)
df_despesas_aux = df_despesas.to_dict()

list_receitas = pd.read_csv('df_cat_receita.csv', index_col=0)
list_receitas_aux = list_receitas.to_dict()

list_despesas = pd.read_csv('df_cat_despesa.csv', index_col=0)
list_despesas_aux = list_despesas.to_dict()

# =========  Layout  =========== #
content = html.Div(id="page-content")


app.layout = dbc.Container(children=[
     # Stores the URL cache
    dcc.Store(id="store-receitas", data=df_receitas.to_dict()),
    dcc.Store(id="store-despesas", data=df_despesas.to_dict()),
    dcc.Store(id="store-cat-receitas", data=df_cat_receita.to_dict()),
    dcc.Store(id="store-cat-despesas", data=df_cat_despesa.to_dict()),
    dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            sidebar.layout

        ], md=2),

        dbc.Col([
            content
        ], md=10),
    ])
    
], fluid=True,)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/" or pathname == "/dashboards":
        return dashboards.layout
    if pathname == "/extratos":
        return extratos.layout
    else:
        return html.P("404: Not found", className="p-3")

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)
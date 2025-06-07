from dash import html, dcc
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *

from components import sidebar, dashboards, extratos

# DataFrames and Dcc.Store
try:
    df_receitas = pd.read_csv("df_receitas.csv", index_col=0)
    # Converter a coluna Data para datetime com formato específico
    df_receitas["Data"] = pd.to_datetime(df_receitas["Data"], format='%Y-%m-%d', errors='coerce')
    df_receitas_aux = df_receitas.to_dict()
except FileNotFoundError:
    # Se o arquivo não existir, criar um dataframe vazio
    df_receitas = pd.DataFrame({
        'Valor': [], 
        'Efetuado': [],
        'Fixo': [],
        'Data': [],
        'Categoria': [],
        'Descricão': [],
    })
    df_receitas_aux = df_receitas.to_dict()

try:
    df_despesas = pd.read_csv("df_despesas.csv", index_col=0)
    # Converter a coluna Data para datetime com formato específico
    df_despesas["Data"] = pd.to_datetime(df_despesas["Data"], format='%Y-%m-%d', errors='coerce')
    df_despesas_aux = df_despesas.to_dict()
except FileNotFoundError:
    # Se o arquivo não existir, criar um dataframe vazio
    df_despesas = pd.DataFrame({
        'Valor': [], 
        'Efetuado': [],
        'Fixo': [],
        'Data': [],
        'Categoria': [],
        'Descricão': [],
    })
    df_despesas_aux = df_despesas.to_dict()

try:
    list_receitas = pd.read_csv('df_cat_receita.csv', index_col=0)
    list_receitas_aux = list_receitas.to_dict()
except FileNotFoundError:
    # Se o arquivo não existir, criar categorias padrão
    list_receitas = pd.DataFrame({'Categoria': ['Salário', 'Vale', 'VR alimentação']})
    list_receitas.to_csv('df_cat_receita.csv')
    list_receitas_aux = list_receitas.to_dict()

try:
    list_despesas = pd.read_csv('df_cat_despesa.csv', index_col=0)
    list_despesas_aux = list_despesas.to_dict()
except FileNotFoundError:
    # Se o arquivo não existir, criar categorias padrão
    list_despesas = pd.DataFrame({'Categoria': ['Compras Mês', 'Estacionamento', 'Gasolina', 'Internet', 'Luz', 'Saúde']})
    list_despesas.to_csv('df_cat_despesa.csv')
    list_despesas_aux = list_despesas.to_dict()

# =========  Layout  =========== #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
     # Stores the URL cache
    dcc.Store(id="store-receitas", data=df_receitas_aux),
    dcc.Store(id="store-despesas", data=df_despesas_aux),
    dcc.Store(id="store-cat-receitas", data=list_receitas_aux),
    dcc.Store(id="store-cat-despesas", data=list_despesas_aux),
    # Stores para filtros selecionados (adicionados para manter o estado entre navegações)
    dcc.Store(id="store-filtros-receitas", data=[]),
    dcc.Store(id="store-filtros-despesas", data=[]),
    
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

# Callback para sincronizar os filtros entre páginas
@app.callback(
    [Output("store-filtros-receitas", "data"),
     Output("store-filtros-despesas", "data")],
    [Input("dropdown-receita", "value"),
     Input("dropdown-despesa", "value")],
    [State("store-filtros-receitas", "data"),
     State("store-filtros-despesas", "data")]
)
def sync_filters(dropdown_receita, dropdown_despesa, filtros_receitas, filtros_despesas):
    # Determinar qual input disparou o callback
    ctx = dash.callback_context
    
    # Se nenhum callback foi disparado ainda, retorne os valores atuais
    if not ctx.triggered:
        return filtros_receitas, filtros_despesas
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Atualizar os filtros apropriados
    if trigger_id == "dropdown-receita" and dropdown_receita is not None:
        filtros_receitas = dropdown_receita
    elif trigger_id == "dropdown-despesa" and dropdown_despesa is not None:
        filtros_despesas = dropdown_despesa
        
    return filtros_receitas, filtros_despesas

# Callback para limpar campos do modal ao abrir para nova entrada
@app.callback(
    [Output("txt-receita", "value", allow_duplicate=True),
     Output("valor_receita", "value", allow_duplicate=True),
     Output("data_receita", "date", allow_duplicate=True),
     Output("switches-input-receita", "value", allow_duplicate=True),
     Output("select_receita", "value", allow_duplicate=True)],
    [Input("open-novo-receita", "n_clicks")],
    prevent_initial_call=True
)
def clear_receita_modal(n_clicks):
    if n_clicks:
        from datetime import datetime
        from globals import cat_receita
        return "", "", datetime.today().date(), [1], cat_receita[0] if cat_receita else ""
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

@app.callback(
    [Output("txt_despesa", "value", allow_duplicate=True),
     Output("valor_despesa", "value", allow_duplicate=True),
     Output("data_despesa", "date", allow_duplicate=True),
     Output("switches-input-despesa", "value", allow_duplicate=True),
     Output("select_despesa", "value", allow_duplicate=True)],
    [Input("open-novo-despesa", "n_clicks")],
    prevent_initial_call=True
)
def clear_despesa_modal(n_clicks):
    if n_clicks:
        from datetime import datetime
        from globals import cat_despesa
        return "", "", datetime.today().date(), [1], cat_despesa[0] if cat_despesa else ""
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)
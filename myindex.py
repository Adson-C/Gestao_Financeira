from dash import html, dcc
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import requests
import base64
import io

from app import *
import os

from components import sidebar, dashboards, extratos

# ===== FUNÇÃO PARA CARREGAR DADOS DO GITHUB OU LOCAL =====
def carregar_dados_github_ou_local(filename, estrutura_padrao):
    """Carrega dados do GitHub se possível, senão do arquivo local"""
    
    # Tentar carregar do GitHub primeiro
    token = os.environ.get('GITHUB_TOKEN')
    owner = os.environ.get('REPO_OWNER') 
    repo = os.environ.get('REPO_NAME')
    
    if all([token, owner, repo]):
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filename}"
            headers = {'Authorization': f'token {token}'}
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                content = base64.b64decode(response.json()['content']).decode()
                df = pd.read_csv(io.StringIO(content), index_col=0)
                print(f"✅ {filename} carregado do GitHub")
                return df
                
        except Exception as e:
            print(f"⚠️ Erro ao carregar {filename} do GitHub: {e}")
    
    # Fallback: carregar arquivo local
    try:
        df = pd.read_csv(filename, index_col=0)
        # Limpar dados inconsistentes
        if 'Categoria' in df.columns:
            df = df.dropna(subset=['Categoria'])  # Remove linhas sem categoria
        print(f"📁 {filename} carregado localmente")
        return df
    except FileNotFoundError:
        print(f"📄 Criando {filename} novo")
        df = pd.DataFrame(estrutura_padrao)
        df.to_csv(filename)
        return df

# ===== ESTRUTURAS PADRÃO =====
estrutura_receitas = {
    'Valor': [], 
    'Efetuado': [],
    'Fixo': [],
    'Data': [],
    'Categoria': [],
    'Descricão': [],
}

estrutura_categorias = {
    'Categoria': []
}

# ===== CARREGAR DADOS (SUBSTITUINDO A SEÇÃO ATUAL) =====

# Carregar dados das receitas
df_receitas = carregar_dados_github_ou_local("df_receitas.csv", estrutura_receitas)
if 'Data' in df_receitas.columns and not df_receitas.empty:
    df_receitas["Data"] = pd.to_datetime(df_receitas["Data"], format='%Y-%m-%d', errors='coerce')
df_receitas_aux = df_receitas.to_dict()

# Carregar dados das despesas  
df_despesas = carregar_dados_github_ou_local("df_despesas.csv", estrutura_receitas)
if 'Data' in df_despesas.columns and not df_despesas.empty:
    df_despesas["Data"] = pd.to_datetime(df_despesas["Data"], format='%Y-%m-%d', errors='coerce')
df_despesas_aux = df_despesas.to_dict()

# Carregar categorias de receitas
list_receitas = carregar_dados_github_ou_local('df_cat_receita.csv', estrutura_categorias)
if list_receitas.empty:
    list_receitas = pd.DataFrame({'Categoria': ['Salário', 'Vale', 'VR alimentação']})
    list_receitas.to_csv('df_cat_receita.csv')
list_receitas_aux = list_receitas.to_dict()

# Carregar categorias de despesas
list_despesas = carregar_dados_github_ou_local('df_cat_despesa.csv', estrutura_categorias)
if list_despesas.empty:
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
    port = int(os.environ.get('PORT', 8051))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run_server(host='0.0.0.0', port=port, debug=debug)
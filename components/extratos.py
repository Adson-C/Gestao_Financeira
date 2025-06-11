import dash
from dash.dependencies import Input, Output, State
from dash import dash_table, callback_context
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime
from github_storage import github_storage

from app import app
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO


# =========  Layout  =========== #
layout = dbc.Col([
    # Seção de Despesas
    dbc.Row([
        html.H3("💸 Tabela de Despesas", style={'color': '#dc3545', 'margin-bottom': '20px'}),
        html.Div(id="tabela-despesas", className="dbc"),
    ], style={'margin-bottom': '30px'}),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph'),
        ], width=9),
        
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("💸 Total Despesas", style={'color': '#dc3545'}),
                    html.H2("R$ 0,00", id="valor_despesa_card", style={'color': '#dc3545'}),
                    html.P("Valor total gasto"),
                ])
            )
        ], width=3),
    ], style={'margin-bottom': '50px'}),
    
    # Separador
    html.Hr(style={'margin': '50px 0', 'border': '2px solid #ddd'}),
    
    # Seção de Receitas
    dbc.Row([
        html.H3("💰 Tabela de Receitas", style={'color': '#28a745', 'margin-bottom': '20px'}),
        html.Div(id="tabela-receitas", className="dbc"),
    ], style={'margin-bottom': '30px'}),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-receitas'),
        ], width=9),
        
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("💰 Total Receitas", style={'color': '#28a745'}),
                    html.H2("R$ 0,00", id="valor_receita_card", style={'color': '#28a745'}),
                    html.P("Valor total recebido"),
                ])
            )
        ], width=3),
    ]),
], style={"padding": "20px"})


# =========  Callbacks para Tabelas  =========== #
# Tabela de Despesas
@app.callback(
    Output("tabela-despesas", "children"),
    [Input("store-despesas", "data")],
)
def imprimir_tabela_despesas(data):
    df = pd.DataFrame(data)
    
    # Verificar se o dataframe está vazio
    if df.empty:
        return html.Div([
            dash_table.DataTable(
                id='datatable-despesas',
                columns=[
                    {"name": "Data", "id": "Data"},
                    {"name": "Valor", "id": "Valor"},
                    {"name": "Categoria", "id": "Categoria"},
                    {"name": "Descrição", "id": "Descricao"},
                    {"name": "Fixo", "id": "Fixo"},
                    {"name": "Efetuado", "id": "Efetuado"}
                ],
                data=[],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#dc3545', 'color': 'white', 'fontWeight': 'bold'},
            ),
            html.Hr(),
            dbc.Alert("📝 Nenhuma despesa encontrada. Adicione despesas usando o botão '- Despesa' no menu lateral.", 
                     color="info", style={'margin-top': '20px'})
        ])
    
    # Processar dados
    df_display = df.copy()
    
    if 'Data' in df_display.columns:
        df_display['Data'] = pd.to_datetime(df_display['Data'], errors='coerce')
        df_display = df_display.dropna(subset=['Data'])
        df_display['Data'] = df_display['Data'].dt.strftime('%d/%m/%Y')
    
    # Converter valores booleanos
    if 'Efetuado' in df_display.columns:
        df_display['Efetuado'] = df_display['Efetuado'].replace({0: 'Não', 1: 'Sim'})
    if 'Fixo' in df_display.columns:
        df_display['Fixo'] = df_display['Fixo'].replace({0: 'Não', 1: 'Sim'})
    
    df_display = df_display.fillna('-')
    df_display = df_display.reset_index(drop=True)
    
    tabela = dash_table.DataTable(
        id='datatable-despesas',
        columns=[{"name": col, "id": col} for col in df_display.columns],
        data=df_display.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        page_action="native",
        page_current=0,
        page_size=10,
        row_selectable="single",
        selected_rows=[],
        style_cell={'textAlign': 'left', 'padding': '12px', 'fontSize': '14px'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': '#dc3545',
            'fontWeight': 'bold',
            'color': 'white',
            'fontSize': '16px'
        }
    )
    
    # Botões de ação
    botoes = html.Div([
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    "✏️ Editar Selecionado", 
                    id="btn-editar-despesa", 
                    color="warning", 
                    disabled=True,
                    size="lg",
                    style={'margin-right': '10px'}
                ),
                dbc.Button(
                    "🗑️ Excluir Selecionado", 
                    id="btn-excluir-despesa", 
                    color="danger", 
                    disabled=True,
                    size="lg"
                ),
            ])
        ], style={"margin-top": "15px"}),
        html.Div(id="feedback-despesa", style={'margin-top': '10px'})
    ])

    return html.Div([tabela, botoes])

# Tabela de Receitas
@app.callback(
    Output("tabela-receitas", "children"),
    [Input("store-receitas", "data")],
)
def imprimir_tabela_receitas(data):
    df = pd.DataFrame(data)
    
    # Verificar se o dataframe está vazio
    if df.empty:
        return html.Div([
            dash_table.DataTable(
                id='datatable-receitas',
                columns=[
                    {"name": "Data", "id": "Data"},
                    {"name": "Valor", "id": "Valor"},
                    {"name": "Categoria", "id": "Categoria"},
                    {"name": "Descrição", "id": "Descricao"},
                    {"name": "Fixo", "id": "Fixo"},
                    {"name": "Efetuado", "id": "Efetuado"}
                ],
                data=[],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#28a745', 'color': 'white', 'fontWeight': 'bold'},
            ),
            html.Hr(),
            dbc.Alert("💰 Nenhuma receita encontrada. Adicione receitas usando o botão '+ Receita' no menu lateral.", 
                     color="info", style={'margin-top': '20px'})
        ])
    
    # Processar dados
    df_display = df.copy()
    
    if 'Data' in df_display.columns:
        df_display['Data'] = pd.to_datetime(df_display['Data'], errors='coerce')
        df_display = df_display.dropna(subset=['Data'])
        df_display['Data'] = df_display['Data'].dt.strftime('%d/%m/%Y')
    
    # Converter valores booleanos
    if 'Efetuado' in df_display.columns:
        df_display['Efetuado'] = df_display['Efetuado'].replace({0: 'Não', 1: 'Sim'})
    if 'Fixo' in df_display.columns:
        df_display['Fixo'] = df_display['Fixo'].replace({0: 'Não', 1: 'Sim'})
    
    df_display = df_display.fillna('-')
    df_display = df_display.reset_index(drop=True)
    
    tabela = dash_table.DataTable(
        id='datatable-receitas',
        columns=[{"name": col, "id": col} for col in df_display.columns],
        data=df_display.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        page_action="native",
        page_current=0,
        page_size=10,
        row_selectable="single",
        selected_rows=[],
        style_cell={'textAlign': 'left', 'padding': '12px', 'fontSize': '14px'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': '#28a745',
            'fontWeight': 'bold',
            'color': 'white',
            'fontSize': '16px'
        }
    )
    
    # Botões de ação
    botoes = html.Div([
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    "✏️ Editar Selecionado", 
                    id="btn-editar-receita", 
                    color="warning", 
                    disabled=True,
                    size="lg",
                    style={'margin-right': '10px'}
                ),
                dbc.Button(
                    "🗑️ Excluir Selecionado", 
                    id="btn-excluir-receita", 
                    color="danger", 
                    disabled=True,
                    size="lg"
                ),
            ])
        ], style={"margin-top": "15px"}),
        html.Div(id="feedback-receita", style={'margin-top': '10px'})
    ])

    return html.Div([tabela, botoes])

# =========  Callbacks para Habilitar/Desabilitar Botões  =========== #
@app.callback(
    [Output("btn-editar-despesa", "disabled"),
     Output("btn-excluir-despesa", "disabled"),
     Output("feedback-despesa", "children")],
    [Input("datatable-despesas", "selected_rows")]
)
def toggle_buttons_despesa(selected_rows):
    if selected_rows and len(selected_rows) > 0:
        feedback = dbc.Alert(f"✅ Linha {selected_rows[0] + 1} selecionada. Use os botões acima para editar ou excluir.", color="success")
        return False, False, feedback
    return True, True, ""

@app.callback(
    [Output("btn-editar-receita", "disabled"),
     Output("btn-excluir-receita", "disabled"),
     Output("feedback-receita", "children")],
    [Input("datatable-receitas", "selected_rows")]
)
def toggle_buttons_receita(selected_rows):
    if selected_rows and len(selected_rows) > 0:
        feedback = dbc.Alert(f"✅ Linha {selected_rows[0] + 1} selecionada. Use os botões acima para editar ou excluir.", color="success")
        return False, False, feedback
    return True, True, ""

# =========  Callbacks para Edição  =========== #
# Callback para editar despesa
@app.callback(
    [Output("store-edit-mode-despesa", "data", allow_duplicate=True),
     Output("modal-novo-despesa", "is_open", allow_duplicate=True),
     Output("txt_despesa", "value", allow_duplicate=True),
     Output("valor_despesa", "value", allow_duplicate=True),
     Output("data_despesa", "date", allow_duplicate=True),
     Output("switches-input-despesa", "value", allow_duplicate=True),
     Output("select_despesa", "value", allow_duplicate=True)],
    [Input("btn-editar-despesa", "n_clicks")],
    [State("datatable-despesas", "selected_rows"),
     State("store-despesas", "data")],
    prevent_initial_call=True
)
def editar_despesa(n_clicks, selected_rows, store_data):
    if not n_clicks or not selected_rows:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    try:
        selected_idx = selected_rows[0]
        df = pd.DataFrame(store_data)
        
        if selected_idx >= len(df):
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        row_data = df.iloc[selected_idx]
        
        # Preparar valores para o modal
        switches_value = []
        if row_data.get('Efetuado', 0) == 1:
            switches_value.append(1)
        if row_data.get('Fixo', 0) == 1:
            switches_value.append(2)
        
        try:
            data_valor = pd.to_datetime(row_data['Data']).date()
        except:
            data_valor = datetime.today().date()
        
        edit_data = {"edit_mode": True, "edit_index": selected_idx}
        
        return (edit_data, True, 
                str(row_data.get('Descricão', '')), 
                str(row_data.get('Valor', '')), 
                data_valor, 
                switches_value, 
                str(row_data.get('Categoria', '')))
                
    except Exception as e:
        print(f"Erro ao editar despesa: {e}")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Callback para editar receita
@app.callback(
    [Output("store-edit-mode-receita", "data", allow_duplicate=True),
     Output("modal-novo-receita", "is_open", allow_duplicate=True),
     Output("txt-receita", "value", allow_duplicate=True),
     Output("valor_receita", "value", allow_duplicate=True),
     Output("data_receita", "date", allow_duplicate=True),
     Output("switches-input-receita", "value", allow_duplicate=True),
     Output("select_receita", "value", allow_duplicate=True)],
    [Input("btn-editar-receita", "n_clicks")],
    [State("datatable-receitas", "selected_rows"),
     State("store-receitas", "data")],
    prevent_initial_call=True
)
def editar_receita(n_clicks, selected_rows, store_data):
    if not n_clicks or not selected_rows:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    try:
        selected_idx = selected_rows[0]
        df = pd.DataFrame(store_data)
        
        if selected_idx >= len(df):
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        row_data = df.iloc[selected_idx]
        
        # Preparar valores para o modal
        switches_value = []
        if row_data.get('Efetuado', 0) == 1:
            switches_value.append(1)
        if row_data.get('Fixo', 0) == 1:
            switches_value.append(2)
        
        try:
            data_valor = pd.to_datetime(row_data['Data']).date()
        except:
            data_valor = datetime.today().date()
        
        edit_data = {"edit_mode": True, "edit_index": selected_idx}
        
        return (edit_data, True, 
                str(row_data.get('Descricão', '')), 
                str(row_data.get('Valor', '')), 
                data_valor, 
                switches_value, 
                str(row_data.get('Categoria', '')))
                
    except Exception as e:
        print(f"Erro ao editar receita: {e}")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

# =========  Callbacks para Exclusão  =========== #
# Callback para excluir despesa
@app.callback(
    Output("store-despesas", "data", allow_duplicate=True),
    [Input("btn-excluir-despesa", "n_clicks")],
    [State("datatable-despesas", "selected_rows"),
     State("store-despesas", "data")],
    prevent_initial_call=True
)
def excluir_despesa(n_clicks, selected_rows, store_data):
    if not n_clicks or not selected_rows:
        return dash.no_update
    
    try:
        selected_idx = selected_rows[0]
        df = pd.DataFrame(store_data)
        
        if selected_idx < len(df):
            df = df.drop(df.index[selected_idx]).reset_index(drop=True)
            
            # 🚀 NOVA LINHA: Salvar no GitHub automaticamente
            github_storage.salvar_despesas(df)
            
            return df.to_dict()
    except Exception as e:
        print(f"Erro ao excluir despesa: {e}")
    
    return dash.no_update

# Modificar callback de excluir receita (linha ~230):
@app.callback(
    Output("store-receitas", "data", allow_duplicate=True),
    [Input("btn-excluir-receita", "n_clicks")],
    [State("datatable-receitas", "selected_rows"),
     State("store-receitas", "data")],
    prevent_initial_call=True
)
def excluir_receita(n_clicks, selected_rows, store_data):
    if not n_clicks or not selected_rows:
        return dash.no_update
    
    try:
        selected_idx = selected_rows[0]
        df = pd.DataFrame(store_data)
        
        if selected_idx < len(df):
            df = df.drop(df.index[selected_idx]).reset_index(drop=True)
            
            # 🚀 NOVA LINHA: Salvar no GitHub automaticamente
            github_storage.salvar_receitas(df)
            
            return df.to_dict()
    except Exception as e:
        print(f"Erro ao excluir receita: {e}")
    
    return dash.no_update

# =========  Callbacks para Gráficos  =========== #
# Gráfico de Despesas
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('store-despesas', 'data'),
     Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def bar_chart_despesas(data, theme):
    df = pd.DataFrame(data)
    
    if df.empty or 'Categoria' not in df.columns or 'Valor' not in df.columns:
        fig = px.bar(
            pd.DataFrame({'Categoria': ['Sem dados'], 'Valor': [0]}),
            x='Categoria',
            y='Valor',
            title="📊 Despesas por Categoria"
        )
        fig.update_traces(marker_color='#dc3545')
        fig.update_layout(template=template_from_url(theme))
        return fig
    
    # Garantir que os valores sejam numéricos
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
    df = df.dropna(subset=['Valor'])
    
    # Agrupar e somar os valores
    df_grouped = df.groupby("Categoria")["Valor"].sum().reset_index()
    df_grouped = df_grouped.sort_values('Valor', ascending=False)
    
    fig = px.bar(
        df_grouped, 
        x='Categoria', 
        y='Valor', 
        title="📊 Despesas por Categoria"
    )
    
    fig.update_traces(marker_color='#dc3545', text=df_grouped['Valor'], texttemplate='R$ %{text:,.0f}', textposition='outside')
    fig.update_layout(template=template_from_url(theme))
    
    return fig

# Gráfico de Receitas
@app.callback(
    Output('bar-graph-receitas', 'figure'),
    [Input('store-receitas', 'data'),
     Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def bar_chart_receitas(data, theme):
    df = pd.DataFrame(data)
    
    if df.empty or 'Categoria' not in df.columns or 'Valor' not in df.columns:
        fig = px.bar(
            pd.DataFrame({'Categoria': ['Sem dados'], 'Valor': [0]}),
            x='Categoria',
            y='Valor',
            title="📊 Receitas por Categoria"
        )
        fig.update_traces(marker_color='#28a745')
        fig.update_layout(template=template_from_url(theme))
        return fig
    
    # Garantir que os valores sejam numéricos
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
    df = df.dropna(subset=['Valor'])
    
    # Agrupar e somar os valores
    df_grouped = df.groupby("Categoria")["Valor"].sum().reset_index()
    df_grouped = df_grouped.sort_values('Valor', ascending=False)
    
    fig = px.bar(
        df_grouped, 
        x='Categoria', 
        y='Valor', 
        title="📊 Receitas por Categoria"
    )
    
    fig.update_traces(marker_color='#28a745', text=df_grouped['Valor'], texttemplate='R$ %{text:,.0f}', textposition='outside')
    fig.update_layout(template=template_from_url(theme))
    
    return fig

# =========  Callbacks para Cards de Valores  =========== #
# Card de valor total das despesas
@app.callback(
    Output('valor_despesa_card', 'children'),
    [Input('store-despesas', 'data')]
)
def display_valor_despesas(data):
    df = pd.DataFrame(data)
    
    if df.empty or 'Valor' not in df.columns:
        return "R$ 0,00"
    
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
    df = df.dropna(subset=['Valor'])
    
    valor = df['Valor'].sum()
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Card de valor total das receitas
@app.callback(
    Output('valor_receita_card', 'children'),
    [Input('store-receitas', 'data')]
)
def display_valor_receitas(data):
    df = pd.DataFrame(data)
    
    if df.empty or 'Valor' not in df.columns:
        return "R$ 0,00"
    
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
    df = df.dropna(subset=['Valor'])
    
    valor = df['Valor'].sum()
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
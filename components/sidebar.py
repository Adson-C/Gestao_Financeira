import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

from globals import *
from dash_bootstrap_templates import ThemeChangerAIO


# =========  Layout  =========== #
layout = dbc.Col([
               html.H2("Controle Financeiro", className="text-primary"),
               html.P("By: Adson Sá", className="text-info"),
               html.Hr(),
               
                # Button de perfil =============================================
                dbc.Button(id='btn_avatar',
                    children=[
                        html.Img(src='/assets/img_hom.png', id='avatar_change', alt='Avatar', className='perfil_avatar')
                    ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
                
                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("Selecionar Perfil")),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_hom.png", className='perfil_avatar', top=True),
                                    dbc.CardBody([
                                        html.H4("Perfil Homem", className="card-title"),
                                        html.P(
                                            "Um Card com exemplo do perfil Homem. Texto para preencher o espaço",
                                            className="card-text",
                                        ),
                                        dbc.Button("Acessar", color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_fem2.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Perfil Mulher", className="card-title"),
                                        html.P(
                                            "Um Card com exemplo do perfil Mulher. Texto para preencher o espaço",
                                            className="card-text",
                                        ),
                                        dbc.Button("Acessar", color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                        ], style={"padding": "5px"}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_home.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Perfil Casa", className="card-title"),
                                        html.P(
                                            "Um Card com exemplo do perfil Casa. Texto para preencher o espaço",
                                            className="card-text",
                                        ),
                                        dbc.Button("Acessar",  color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_plus.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Adicionar Novo Perfil", className="card-title"),
                                        html.P(
                                            "Esse projeto é um protótipo, o botão de adicionar um novo perfil esta desativado momentaneamente!",
                                            className="card-text",
                                        ),
                                        dbc.Button("Adicionar", color="success"),
                                    ]),
                                ]),
                            ], width=6),
                        ], style={"padding": "5px"}),
                    ]),
                ],
                style={"background-color": "rgba(0, 0, 0, 0.5)"},
                id="modal-perfil",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True
                ),
                
                # Button de novo =============================================
                dbc.Row([
                    dbc.Col([
                        dbc.Button(color='success', id='open-novo-receita', children=['+ Receita'])
                    ], width=6),
                    dbc.Col([
                        dbc.Button(color='danger', id='open-novo-despesa', children=['- Despesa'])
                    ], width=6)
                ]),
                
                # Stores para controlar modo de edição
                dcc.Store(id="store-edit-mode-receita", data={"edit_mode": False, "edit_index": None}),
                dcc.Store(id="store-edit-mode-despesa", data={"edit_mode": False, "edit_index": None}),
                
                 # Modal Receita =============================================
                dbc.Modal([
                    dbc.ModalHeader([
                        dbc.ModalTitle(id="modal-title-receita", children="Adicionar Receita")
                    ]),
                    dbc.ModalBody([
                        dbc.Row([
                        # Receita ==================
                            dbc.Col([
                                dbc.Label("Descrição: "),
                                dbc.Input(placeholder="Ex.: dividendo da bolsa, herança....", id="txt-receita"),
                        ], width=6),
                           dbc.Col([
                               dbc.Label("Valor: "),
                               dbc.Input(placeholder="R$ 100.00", id="valor_receita", value=""),
                           ], width=6)
                        ]),
                        dbc.Row([
                        # Data ====================
                            dbc.Col([
                                dbc.Label("Data: "),
                                dcc.DatePickerSingle(
                                    id='data_receita',
                                    min_date_allowed=date(2020, 1, 1),
                                    max_date_allowed=date(2030, 12, 31),
                                    date=datetime.today(),
                                    style={'width': '100%'}
                                ),
                            ], width=4),
                            # Extras =================
                            dbc.Col([
                                dbc.Label("Extras"),
                                dbc.Checklist(
                                    options=[{"label": "Foi recebida", "value": 1},
                                        {"label": "Receita Recorrente", "value": 2}],
                                    value=[1],
                                    id="switches-input-receita",
                                    switch=True),
                            ], width=4),
                            # Categotia ===============
                            dbc.Col([
                                html.Label("Categoria da receita: "),
                                dbc.Select(id="select_receita",options=[{'label': i, 'value': i} for i in cat_receita],value=cat_receita[0])
                            ], width=4),
                            
                        ], style={'margin-top': '25px'}),
                        
                        dbc.Row([
                            dbc.Accordion([
                            # Adcionar/Remover Categorias ===============
                                dbc.AccordionItem(children=[
                                    dbc.Row([
                                        # Adcionar Categorias ===============
                                        dbc.Col([
                                                html.Legend("Adicionar categoria", style={'color': 'green'}),
                                                dbc.Input(type="text", placeholder="Nova categoria...", id="input-add-receita", value=""),
                                                html.Br(),
                                                dbc.Button("Adicionar", className="btn btn-success", id="add-category-receita", style={"margin-top": "20px"}),
                                                html.Br(),
                                                html.Div(id="category-div-add-receita", style={}),
                                            ], width=6),
                                        # Remover Categorias ===============
                                        dbc.Col([
                                            html.Legend("Excluir categoria : ", style={'color': 'red'}),
                                            dbc.Checklist(
                                                id="checklist-selected-style-receita",
                                                options=[{'label': i, 'value': i} for i in cat_receita],
                                                value=[],
                                                label_checked_style={'color': 'red'},
                                                input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},
                                            ),
                                            dbc.Button("Remover", color="warning", id="remover-category-receita", style={'margin-top': '20px'}),
                                        ], width=6),
                                        # Salvar =============
                                    ])
                                ], title='Adcionar/Remover Categorias'),
                            ], flush=True, start_collapsed=True, id="accordion-receita"),

                            html.Div(id="id_teste_receita", style={'padding-top': '20px'}),
                            dbc.ModalFooter([
                                dbc.Button("Salvar", id='salvar_receita', color="success"),
                                dbc.Button("Cancelar", id='cancelar_receita', color="secondary", style={"margin-left": "10px"}),
                                dbc.Popover(dbc.PopoverBody("Receita salva"), target="salvar_receita", placement="left", trigger="click"),
                            ])
                    ], style={'margin-top': '25px'})
                    ])
                ], style={'background-color': 'rgba(17, 140, 79, 0.5)'},
                id="modal-novo-receita",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True),
                
                # Modal Despesa =============================================
                dbc.Modal([
                    dbc.ModalHeader([
                        dbc.ModalTitle(id="modal-title-despesa", children="Adicionar Despesa")
                    ]),
                    dbc.ModalBody([
                        dbc.Row([
                            # Despesa =================
                            dbc.Col([
                                dbc.Label("Descrição: "),
                                dbc.Input(placeholder="Ex.: Gasolina, Luz, estacionamento....", id="txt_despesa"),
                        ], width=6),
                           dbc.Col([
                               dbc.Label("Valor: "),
                               dbc.Input(placeholder="R$ 100.00", id="valor_despesa", value=""),
                           ], width=6),
                        ]),
                        dbc.Row([
                            # Data =================
                            dbc.Col([
                                dbc.Label("Data: "),
                                dcc.DatePickerSingle(
                                    id='data_despesa',
                                    min_date_allowed=date(2020, 1, 1),
                                    max_date_allowed=date(2030, 12, 31),
                                    date=datetime.today(),
                                    style={'width': '100%'}
                                ),
                            ], width=4),
                            # Extras =================
                            dbc.Col([
                            dbc.Label("Opções Extras"),
                            dbc.Checklist(
                                options=[{"label": "Foi recebida", "value": 1},
                                    {"label": "despesa Recorrente", "value": 2}],
                                value=[1],
                                id="switches-input-despesa",
                                switch=True),
                        ], width=4),
                            # Categotia ===============
                            dbc.Col([
                                html.Label("Categoria da despesa: "),
                                dbc.Select(
                                    id="select_despesa",
                                    options=[{'label': i, 'value': i} for i in cat_despesa],
                                    value=cat_despesa[0])
                            ], width=4)
                        ], style={'margin-top': '25px'}),
                        dbc.Row([
                            dbc.Accordion([
                                dbc.AccordionItem(children=[
                                    dbc.Row([
                                        # Accordion Item add depesas ===============
                                        dbc.Col([
                                            html.Legend("Adcionar despesa: ", style={'color': 'green'}),
                                            dbc.Input(type="text", placeholder="Nova despesa...", id="input-add-despesa", value=""),
                                            html.Br(),
                                            dbc.Button("Adicionar", className="btn btn-success", id="add-category-despesa", style={'margin-top': '20px'}),
                                            html.Br(),
                                            html.Div(id="category-div-add-despesa", style={}),
                                        ], width=6),
                                        # Remover Categorias ===============
                                        dbc.Col([
                                            html.Legend("Excluir categoria : ", style={'color': 'red'}),
                                            dbc.Checklist(
                                                id="chicklist-category-despesa",
                                                options=[{'label': i, 'value': i} for i in cat_despesa],
                                                value=[],
                                                label_checked_style={'color': 'red'},
                                                input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},
                                            ),
                                            dbc.Button("Remover", color="warning", id="remover-category-despesa", style={'margin-top': '20px'})
                                        ], width=6),
                                        
                                    ])
                                    # Adcionar/Remover Categorias
                                ], title='Adcionar/Remover Categorias'),
                            ], flush=True, start_collapsed=True, id="accordion-despesa"),

                            html.Div(id="id_teste_depesa", style={'padding-top': '20px'}),
                            dbc.ModalFooter([
                                dbc.Button("Salvar", id='salvar_despesa', color="success"),
                                dbc.Button("Cancelar", id='cancelar_despesa', color="secondary", style={"margin-left": "10px"}),
                                dbc.Popover(dbc.PopoverBody("Despesa salva"), target="salvar_despesa", placement="left", trigger="click"),
                            ])
                        ], style={'margin-top': '25px'})
                    ])
                ], style={'background-color': 'rgba(17, 140, 79, 0.5)'},
                id="modal-novo-despesa",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True),
                
                # Seção NAV =============================================
               html.Hr(),
               dbc.Nav([
                dbc.NavLink("Dashboards", href="/dashboards", active="exact"),
                dbc.NavLink("Extratos", href="/extratos", active="exact"),
            ], vertical=True, pills=True, id="nav-buttons", style={'margin-bottom': '50px'}),
        ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.QUARTZ})

          ], id="sidebar_completa")

# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    [Output("modal-novo-receita", "is_open"),
     Output("store-edit-mode-receita", "data")],
    [Input("open-novo-receita", "n_clicks"),
     Input("cancelar_receita", "n_clicks")],
    [State("modal-novo-receita", "is_open"),
     State("store-edit-mode-receita", "data")]
)
def toggle_modal_receita(n1, n_cancel, is_open, edit_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, edit_data
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "open-novo-receita" and n1:
        # Resetar para modo de criação
        return True, {"edit_mode": False, "edit_index": None}
    elif trigger_id == "cancelar_receita" and n_cancel:
        return False, {"edit_mode": False, "edit_index": None}
    
    return is_open, edit_data

# Pop-up despesa
@app.callback(
    [Output("modal-novo-despesa", "is_open"),
     Output("store-edit-mode-despesa", "data")],
    [Input("open-novo-despesa", "n_clicks"),
     Input("cancelar_despesa", "n_clicks")],
    [State("modal-novo-despesa", "is_open"),
     State("store-edit-mode-despesa", "data")]
)
def toggle_modal_despesa(n1, n_cancel, is_open, edit_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, edit_data
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "open-novo-despesa" and n1:
        # Resetar para modo de criação
        return True, {"edit_mode": False, "edit_index": None}
    elif trigger_id == "cancelar_despesa" and n_cancel:
        return False, {"edit_mode": False, "edit_index": None}
    
    return is_open, edit_data

# Pop-up perfis
@app.callback(
    Output("modal-perfil", "is_open"),
    Input("btn_avatar", "n_clicks"),
    State("modal-perfil", "is_open")
)
def toggle_modal_pefil(n1, is_open):
    if n1:
        return not is_open

# Callback para atualizar título do modal receita
@app.callback(
    Output("modal-title-receita", "children"),
    Input("store-edit-mode-receita", "data")
)
def update_modal_title_receita(edit_data):
    if edit_data["edit_mode"]:
        return "Editar Receita"
    return "Adicionar Receita"

# Callback para atualizar título do modal despesa
@app.callback(
    Output("modal-title-despesa", "children"),
    Input("store-edit-mode-despesa", "data")
)
def update_modal_title_despesa(edit_data):
    if edit_data["edit_mode"]:
        return "Editar Despesa"
    return "Adicionar Despesa"

# =========  Callbacks  =========== 
# Salvar/Editar receita
@app.callback(
    [Output("store-receitas", "data"),
     Output("modal-novo-receita", "is_open", allow_duplicate=True)],
    Input("salvar_receita", "n_clicks"),
    [
        State("txt-receita", "value"),
        State("valor_receita", "value"),
        State("data_receita", "date"),
        State("switches-input-receita", "value"),
        State("select_receita", "value"),
        State("store-receitas", "data"),
        State("store-edit-mode-receita", "data"),
    ],
    prevent_initial_call=True
)
def salvar_form_receita(n_clicks, descricao, valor, date, switches, categoria, dict_receitas, edit_data):
    if not n_clicks or not valor or valor == '':
        return dict_receitas, True

    df_receitas = pd.DataFrame(dict_receitas)
    
    valor = round(float(valor), 2)
    date = pd.to_datetime(date).date()
    categoria = categoria[0] if type(categoria) == list else categoria
    recebido = 1 if 1 in switches else 0
    fixo = 1 if 2 in switches else 0

    if edit_data["edit_mode"] and edit_data["edit_index"] is not None:
        # Modo edição - atualizar linha existente
        idx = edit_data["edit_index"]
        if idx < len(df_receitas):
            df_receitas.loc[idx] = [valor, recebido, fixo, date, categoria, descricao]
    else:
        # Modo criação - adicionar nova linha
        df_receitas.loc[df_receitas.shape[0]] = [valor, recebido, fixo, date, categoria, descricao]
    
    df_receitas.to_csv("df_receitas.csv")
    data_return = df_receitas.to_dict()
    
    return data_return, False

# Salvar/Editar despesa
@app.callback(
    [Output("store-despesas", "data"),
     Output("modal-novo-despesa", "is_open", allow_duplicate=True)],
    Input("salvar_despesa", "n_clicks"),
    [
        State("txt_despesa", "value"),
        State("valor_despesa", "value"),
        State("data_despesa", "date"),
        State("switches-input-despesa", "value"),
        State("select_despesa", "value"),
        State("store-despesas", "data"),
        State("store-edit-mode-despesa", "data"),
    ],
    prevent_initial_call=True
)
def salvar_form_despesa(n_clicks, descricao, valor, date, switches, categoria, dict_despesas, edit_data):
    if not n_clicks or not valor or valor == '':
        return dict_despesas, True

    df_despesas = pd.DataFrame(dict_despesas)
    
    valor = round(float(valor), 2)
    date = pd.to_datetime(date).date()
    categoria = categoria[0] if type(categoria) is list else categoria
    recebido = 1 if 1 in switches else 0
    fixo = 1 if 2 in switches else 0

    if edit_data["edit_mode"] and edit_data["edit_index"] is not None:
        # Modo edição - atualizar linha existente
        idx = edit_data["edit_index"]
        if idx < len(df_despesas):
            df_despesas.loc[idx] = [valor, recebido, fixo, date, categoria, descricao]
    else:
        # Modo criação - adicionar nova linha
        df_despesas.loc[df_despesas.shape[0]] = [valor, recebido, fixo, date, categoria, descricao]
    
    df_despesas.to_csv("df_despesas.csv")
    data_return = df_despesas.to_dict()
    
    return data_return, False

# =========  Callbacks  =========== #
# Remover/add Categorias Despesas
@app.callback(
    [
        Output("category-div-add-despesa", "children"),
        Output("category-div-add-despesa", "style"),
        Output("select_despesa", "options"),
        Output("chicklist-category-despesa", "options"),
        Output("chicklist-category-despesa", "value"),
        Output("store-cat-despesas", "data")
    ],
    [
        Input("add-category-despesa", "n_clicks"),
        Input("remover-category-despesa", "n_clicks")
    ],
    [
        State("input-add-despesa", "value"),
        State("chicklist-category-despesa", "value"),
        State("store-cat-despesas", "data")
    ]
)
def add_category(n, n2, txt, check_delete, data):
    cat_despesa = list(data["Categoria"].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == "" or txt == None:
            txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
            style1 = {'color': 'red'}

        else:
            cat_despesa = cat_despesa + [txt] if txt not in cat_despesa else cat_despesa
            txt1 = f'A categoria {txt} foi adicionada com sucesso!'
            style1 = {'color': 'green'}
    
    if n2:
        if len(check_delete) > 0:
            cat_despesa = [i for i in cat_despesa if i not in check_delete]  
    
    opt_despesa = [{"label": i, "value": i} for i in cat_despesa]
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_cat_despesa.to_csv("df_cat_despesa.csv")
    data_return = df_cat_despesa.to_dict()

    return [txt1, style1, opt_despesa, opt_despesa, [], data_return]

# =========  Callbacks  =========== #
# Remover/add Categorias receita
@app.callback(
    [
        Output("category-div-add-receita", "children"),
        Output("category-div-add-receita", "style"),
        Output("select_receita", "options"),
        Output("checklist-selected-style-receita", "options"),
        Output("checklist-selected-style-receita", "value"),
        Output("store-cat-receitas", "data")
    ],
    [
        Input("add-category-receita", "n_clicks"),
        Input("remover-category-receita", "n_clicks")
    ],
    [
        State("input-add-receita", "value"),
        State("checklist-selected-style-receita", "value"),
        State("store-cat-receitas", "data")
    ]
)
def add_categoryrce(n, n2, txt, check_delete, data):
    cat_receita = list(data["Categoria"].values())

    txt1 = []
    style1 = {}

    if n:
        if txt == "" or txt == None:
            txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
            style1 = {'color': 'red'}

    if n and not(txt == "" or txt == None):
        cat_receita = cat_receita + [txt] if txt not in cat_receita else cat_receita
        txt1 = f'A categoria {txt} foi adicionada com sucesso!'
        style1 = {'color': 'green'}
    
    if n2:
        if check_delete == []:
            pass
        else:
            cat_receita = [i for i in cat_receita if i not in check_delete]  
    
    opt_receita = [{"label": i, "value": i} for i in cat_receita]
    df_cat_receita = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_receita.to_csv("df_cat_receita.csv")
    data_return = df_cat_receita.to_dict()

    return [txt1, style1, opt_receita, opt_receita, [], data_return]
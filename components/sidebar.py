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


# =========  Layout  =========== #
layout = dbc.Col([
               html.H1("Controle Financeiro", className="text-primary"),
               html.P("By: Adson Sá", className="text-info"),
               html.Hr(),
               
                # Button de perfil =============================================
                dbc.Button(id='btn_avatar',
                    children=[
                        html.Img(src='/assets/img_hom.png', id='avatar_change', alt='Avatar', className='perfil_avatar')
                    ], style={'background-color': 'transparent', 'border-color': 'transparent'}),
                
                # Button de novo =============================================
                dbc.Row([
                    dbc.Col([
                        dbc.Button(color='success', id='open-novo-receita', children=['+ Receita'])
                    ], width=6),
                    dbc.Col([
                        dbc.Button(color='danger', id='open-novo-despesa', children=['- Despesa'])
                    ], width=6)
                ]),
                
                 # Modal Receita =============================================
                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("Adicionar Receita")),
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
                                dbc.Label("Extras: "),
                                dbc.Checklist(
                                    options=[],
                                    value=[],
                                    id="switches-input-receita",
                                    switch=True
                                )
                            ], width=4),
                            # Categotia ===============
                            dbc.Col([
                                html.Label("Categoria da receita: "),
                                dbc.Select(id="select_receita",
                                           options=[], 
                                           value=[])
                            ], width=4),
                            
                        ], style={'margin-top': '25px'}),
                        
                        dbc.Row([
                            dbc.Accordion([
                            # Adcionar/Remover Categorias ===============
                                dbc.AccordionItem(children=[
                                    dbc.Row([
                                        # Adcionar Categorias ===============
                                        dbc.Col([
                                            html.Legend("Adcionar categoria: ", style={'color': 'green'}),
                                            dbc.Input(type="text", placeholder="Nova categoria...", id="input-add-receita", value=""), 
                                            html.Br(),
                                            dbc.Button("Adicionar", className="btn btn-success", id="add-category-receita", style={'margin-top': '20px'}),
                                            html.Br(),
                                            html.Div(id="category-div-receita", style={}),
                                        ], width=6),
                                        # Remover Categorias ===============
                                        dbc.Col([
                                            html.Legend("Excluir categoria : ", style={'color': 'red'}),
                                            dbc.Checklist(
                                                id="checkbox-category-receita",
                                                options=[],
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
                                dbc.Button("Adicionar", id='salvar-receita', color="success"),
                                dbc.Popover(dbc.PopoverBody("Receita salva"), target="salvar-receita", placement="left", trigger="click"),
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
                    dbc.ModalHeader(dbc.ModalTitle("Adicionar Despesa")),
                    dbc.ModalBody([
                        dbc.Row([
                            # Despesa =================
                            dbc.Col([
                                dbc.Label("Descrição: "),
                                dbc.Input(placeholder="Ex.: Gasolina, Luz, estacionamento....", id="txt-depesa"),
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
                                dbc.Label("Extras: "),
                                dbc.Checklist(
                                    options=[],
                                    value=[],
                                    id="switches-input-despesa",
                                    switch=True
                                )
                            ], width=4),
                            # Categotia ===============
                            dbc.Col([
                                html.Label("Categoria da despesa: "),
                                dbc.Select(options=[], id="select_despesa", value=[])
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
                                            html.Div(id="category-div-despesa", style={}),
                                        ], width=6),
                                        # Remover Categorias ===============
                                        dbc.Col([
                                            html.Legend("Excluir categoria : ", style={'color': 'red'}),
                                            dbc.Checklist(
                                                id="checkbox-category-despesa",
                                                options=[],
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
                                dbc.Button("Adicionar", id='salvar-despesa', color="success"),
                                dbc.Popover(dbc.PopoverBody("Receita salva"), target="salvar-despesa", placement="left", trigger="click"),
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

          ], id="sidebar_completa")


# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output("modal-novo-receita", "is_open"),
    Input("open-novo-receita", "n_clicks"),
    State("modal-novo-receita", "is_open"),
)
def toggle_modal_novo_receita(n1, is_open):
    if n1:
        return not is_open

# =========  Callbacks  =========== #
# Pop-up despesa
@app.callback(
    Output("modal-novo-despesa", "is_open"),
    Input("open-novo-despesa", "n_clicks"),
    State("modal-novo-despesa", "is_open"),
)
def toggle_modal_novo_despesa(n1, is_open):
    if n1:
        return not is_open
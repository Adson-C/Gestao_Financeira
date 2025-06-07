import dash
import dash_bootstrap_components as dbc

# Inicialização do aplicativo
app = dash.Dash(__name__, suppress_callback_exceptions=True, 
                external_stylesheets=[dbc.themes.QUARTZ],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

server = app.server
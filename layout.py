from dash import html, dcc
import dash_bootstrap_components as dbc
from pages.navbar import create_navbar

def create_layout():
    return html.Div([
        create_navbar(),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

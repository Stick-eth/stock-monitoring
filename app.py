from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

from pages.home import home_layout
from pages.stocks import stocks_layout
from pages.about import about_layout
  
# Initialisation de l'application Dash avec Bootstrap et suppression des exceptions
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title= "DataStick - Stock Analysis", suppress_callback_exceptions=True)

# Application du layout principal
app.layout = create_layout()

# Callback pour le routage entre les pages
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/stocks':
        return stocks_layout()
    elif pathname == '/about':
        return about_layout()
    else:
        return home_layout()

# Enregistrement des callbacks
register_callbacks(app)

# Lancer le serveur
if __name__ == '__main__':
    app.run_server(debug=True)

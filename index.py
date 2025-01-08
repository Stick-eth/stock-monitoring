from dash import Dash, html, Input, Output, dcc, _dash_renderer
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks
from pages.home import home_layout
from pages.stocks import stocks_layout
from pages.about import about_layout
from pages.stocks_list import stocks_list_layout
import dash_mantine_components as dmc
import warnings

_dash_renderer._set_react_version("18.2.0")
# Initialisation de l'application Dash
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.CERULEAN],
    title="DataStick - Stock Analysis",
    suppress_callback_exceptions=True,
)
app._favicon = "assets/favicon.ico"

# Définir le layout principal
app.layout = dmc.MantineProvider(create_layout())

# Callback pour gérer le routage entre les pages
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    if pathname.startswith("/stocks/"):
        # Extraire le ticker depuis l'URL
        parts = pathname.split("/stocks/")
        ticker = parts[-1] if len(parts) > 1 else None
        # Si aucun ticker n'est spécifié, afficher une liste de tickers
        if not ticker:
            return stocks_list_layout()
        # Sinon, charger le layout des stocks avec le ticker spécifié
        return stocks_layout(ticker=ticker)
    elif pathname == "/about":
        return about_layout()
    else:
        return home_layout()

# Enregistrer les callbacks
register_callbacks(app)

# Exécution locale
if __name__ == "__main__":
    warnings.filterwarnings(
        "ignore", message="The 'unit' keyword in TimedeltaIndex construction is deprecated"
    )
    app.run_server(debug=True)

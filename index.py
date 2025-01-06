from dash import Dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks
from pages.home import home_layout
from pages.stocks import stocks_layout
from pages.about import about_layout
from pages.navbar import create_navbar
from pages.stocks_list import stocks_list_layout

import warnings

# Initialisation de l'application Dash
class MainApplication:
    def __init__(self):
        self.__app = Dash(
            __name__,
            external_stylesheets=[dbc.themes.DARKLY],
            title="DataStick - Stock Analysis",
            suppress_callback_exceptions=True,
        )
        self.__app._favicon = "assets/favicon.ico"
        self.set_layout()
        register_callbacks(self.__app)

    @property
    def app(self):
        return self.__app

    def set_layout(self):
        """Définit le layout principal."""
        self.app.layout = html.Div([
            create_navbar(),
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content"),
        ])

        # Callback pour gérer le routage entre les pages
        @self.app.callback(
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


Application = MainApplication()
app = Application.app.server  # L'objet Flask attendu par Vercel

# Exécution locale
if __name__ == "__main__":
    warnings.filterwarnings(
        "ignore", message="The 'unit' keyword in TimedeltaIndex construction is deprecated"
    )
    Application.app.run_server(debug=True)

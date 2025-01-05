from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks
from pages.home import home_layout
from pages.stocks import stocks_layout
from pages.about import about_layout
import warnings

# Initialisation de l'application Dash
class MainApplication:
    def __init__(self):
        self.__app = Dash(
            __name__,
            external_stylesheets=[dbc.themes.CERULEAN],
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
        self.app.layout = create_layout()

        # Callback pour gérer le routage entre les pages
        @self.app.callback(
            Output("page-content", "children"),
            Input("url", "pathname"),
        )
        def display_page(pathname):
            if pathname == "/stocks":
                return stocks_layout()
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

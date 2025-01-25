from dash import Dash, html, Input, Output, dcc, _dash_renderer, clientside_callback
import dash_bootstrap_components as dbc
from pages.layout import create_layout
from callbacks.stocks_callbacks import register_stocks_callbacks
from pages.home import home_layout
from pages.stocks import stocks_layout
from pages.about import about_layout
from pages.stocks_list import stocks_list_layout
from pages.login import login_layout
from pages.profile import profile_layout
from pages.privacypolicy import privacy_policy_layout
from pages.portfolio_overview import portfolio_overview_layout
from components.utils.ip_access import add_ip_to_atlas
import dash_mantine_components as dmc
from dash_bootstrap_templates import load_figure_template
import warnings
from components.utils.cache_config import cache
import requests
import os
from flask import Flask, session, redirect, request, url_for
from urllib.parse import urlencode, urlparse, parse_qs

# Mettre à jour la version de React pour éviter les avertissements
_dash_renderer._set_react_version("18.2.0")

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Récupération des paramètres OAuth Google
GOOGLE_AUTH_CLIENT_ID = os.getenv("GOOGLE_AUTH_CLIENT_ID")
GOOGLE_AUTH_CLIENT_SECRET = os.getenv("GOOGLE_AUTH_CLIENT_SECRET")
GOOGLE_AUTH_REDIRECT_URI = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
GOOGLE_AUTH_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_AUTH_USERINFO_URI = "https://www.googleapis.com/oauth2/v3/userinfo"

# Initialisation de l'application Flask et Dash
server = Flask(__name__)
server.secret_key = os.getenv("SECRET_KEY", "ajoutezmonlinkedin")  # Nécessaire pour les sessions Flask
app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.LUMEN, dbc.icons.FONT_AWESOME] + dmc.styles.ALL ,
    title="DataStick - Financial Tool",
    suppress_callback_exceptions=True,
)
app._favicon = "assets/favicon.ico"

def build_google_oauth_url():
    """
    Construit l'URL d'authentification Google.
    """
    params = {
        "client_id": GOOGLE_AUTH_CLIENT_ID,
        "redirect_uri": GOOGLE_AUTH_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "include_granted_scopes": "true",
        "prompt": "consent"
    }
    return f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"

def exchange_code_for_token(auth_code):
    """
    Échange le 'code' contre un token d'accès et un refresh_token si présent.
    """
    data = {
        "code": auth_code,
        "client_id": GOOGLE_AUTH_CLIENT_ID,
        "client_secret": GOOGLE_AUTH_CLIENT_SECRET,
        "redirect_uri": GOOGLE_AUTH_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(GOOGLE_AUTH_TOKEN_URI, data=data)
    response.raise_for_status()
    return response.json()

def get_user_info(access_token):
    """
    Récupère les informations de l'utilisateur depuis l'API Google.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(GOOGLE_AUTH_USERINFO_URI, headers=headers)
    response.raise_for_status()
    return response.json()

@server.route("/login/callback")
def google_auth_callback():
    """
    Cette route est appelée par Google après l'authentification.
    Récupère le paramètre 'code', échange contre un token et stocke les informations utilisateur dans la session Flask.
    """
    code = request.args.get("code")
    if not code:
        return "Erreur : pas de code renvoyé par Google.", 400

    try:
        # Échanger le code contre un token
        token_info = exchange_code_for_token(code)

        # Récupérer les informations utilisateur
        if token_info.get("access_token"):
            user_info = get_user_info(token_info["access_token"])
            session["user_name"] = user_info.get("name", "Unknown")
            session["user_email"] = user_info.get("email", "Unknown")

            print("User info:", session["user_name"], session["user_email"])

        # Rediriger vers la page principale
        return redirect(request.host_url)

    except Exception as e:
        return f"Une erreur s'est produite lors de l'échange du code : {e}", 500

# Définir le layout principal
app.layout = dmc.MantineProvider([create_layout()])

# Initialisation du cache
cache.init_app(app.server)

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark"); 
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)

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
    elif pathname == "/login":
        return login_layout()
    elif pathname == "/logout":
        session.clear()
        return home_layout()
    elif pathname == "/profile":
        return profile_layout()
    elif pathname == "/privacy":
        return privacy_policy_layout()
    elif pathname == "/portfolio/overview":
        return portfolio_overview_layout()
    else:
        return home_layout()

# Enregistrer les callbacks
register_stocks_callbacks(app)

# Ajouter l'adresse IP à la liste d'accès de MongoDB Atlas
add_ip_to_atlas()

# Exécution locale
if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="The 'unit' keyword in TimedeltaIndex construction is deprecated")
    app.run_server(debug=True)

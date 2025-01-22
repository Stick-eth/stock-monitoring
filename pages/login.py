from dash import html, dcc
import dash_bootstrap_components as dbc
from urllib.parse import urlencode
import dotenv
import os
from flask import session

dotenv.load_dotenv()

# Récupération des variables d'environnement
GOOGLE_AUTH_CLIENT_ID = os.getenv("GOOGLE_AUTH_CLIENT_ID")
GOOGLE_AUTH_SCOPE = os.getenv("GOOGLE_AUTH_SCOPE")
GOOGLE_AUTH_URL = os.getenv("GOOGLE_AUTH_URL")
GOOGLE_AUTH_REDIRECT_URI = os.getenv("GOOGLE_AUTH_REDIRECT_URI")

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
    url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    return url

# Contenu de l'onglet Login (authentification normale cachée)
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(id="hidden-login-section", style={"display": "none"}, children=[
                dbc.Label("Username or Email", html_for="login-username"),
                dbc.Input(type="text", id="login-username", placeholder="Enter your username or email", className="mb-3"),
                dbc.Label("Password", html_for="login-password"),
                dbc.Input(type="password", id="login-password", placeholder="Enter your password", className="mb-3"),
                dbc.Button("Login", id="login-button", color="primary", className="mb-3"),
            ]),
            html.Div("Classic login coming soon ! 🚧", style={"textAlign": "center", "margin": "10px 0", "color": "gray"}),
            html.Div("SO", style={"textAlign": "center", "margin": "10px 0", "color": "gray"}),
            html.A(
                dbc.Button(
                    "Login with Google",
                    id="google-login-button",
                    color="danger",
                    className="mb-3",
                    style={"width": "100%"}
                ),
                href=build_google_oauth_url()
            ),
        ]
    ),
    className="mt-3",
)

# Contenu de l'onglet Create Account (inscription cachée)
tab2_content = dbc.Card(
    dbc.CardBody(
        html.Div(id="hidden-signup-section", style={"display": "none"}, children=[
            dbc.Label("Username", html_for="signup-username"),
            dbc.Input(type="text", id="signup-username", placeholder="Choose a username", className="mb-3"),
            dbc.Label("Email", html_for="signup-email"),
            dbc.Input(type="email", id="signup-email", placeholder="Enter your email", className="mb-3"),
            dbc.Label("Password", html_for="signup-password"),
            dbc.Input(type="password", id="signup-password", placeholder="Create a password", className="mb-3"),
            dbc.Button("Create Account", id="signup-button", color="success", className="mb-3"),
        ])
    ),
    className="mt-3",
)

# Ensemble des onglets
tabs = dbc.Tabs([
    dbc.Tab(tab1_content, label="Login"),
])

def login_layout():
    """Layout pour la page de connexion et de création de compte."""
    user_name = session.get("user_name")
    user_email = session.get("user_email")

    if user_name and user_email:
        return dcc.Location(pathname="/profile", id="redirect-to-profile")
    else:
        return html.Div([
            dbc.Container(
                [
                    html.H2("Welcome to DataStick", className="text-center mt-4 mb-4"),
                    tabs
                ],
                style={"maxWidth": "500px", "marginTop": "50px"}
            )
        ])

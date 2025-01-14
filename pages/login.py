from dash import html, dcc
import dash_bootstrap_components as dbc

# Contenu de l'onglet Login
tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div([
                dbc.Label("Username or Email", html_for="login-username"),
                dbc.Input(type="text", id="login-username", placeholder="Enter your username or email", className="mb-3"),
                dbc.Label("Password", html_for="login-password"),
                dbc.Input(type="password", id="login-password", placeholder="Enter your password", className="mb-3"),
                dbc.Button("Login", id="login-button", color="primary", className="mb-3"),
                html.Div("OR", style={"textAlign": "center", "margin": "10px 0", "color": "gray"}),
                dbc.Button(
                    "Login with Google", id="google-login-button", color="danger", className="mb-3",
                    style={"width": "100%"}
                ),
            ])
        ]
    ),
    className="mt-3",
)

# Contenu de l'onglet Create Account
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div([
                dbc.Label("Username", html_for="signup-username"),
                dbc.Input(type="text", id="signup-username", placeholder="Choose a username", className="mb-3"),
                dbc.Label("Email", html_for="signup-email"),
                dbc.Input(type="email", id="signup-email", placeholder="Enter your email", className="mb-3"),
                dbc.Label("Password", html_for="signup-password"),
                dbc.Input(type="password", id="signup-password", placeholder="Create a password", className="mb-3"),
                dbc.Button("Create Account", id="signup-button", color="success", className="mb-3"),
            ])
        ]
    ),
    className="mt-3",
)

# Configuration des onglets
tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Login"),
        dbc.Tab(tab2_content, label="Create Account"),
    ]
)

# Layout principal
def login_layout():
    """Layout pour la page de connexion et de création de compte."""
    return html.Div([
        dbc.Container(
            [
                html.H2("Welcome to DataStick", className="text-center mt-4 mb-4"),
                tabs
            ],
            style={"maxWidth": "500px", "marginTop": "50px"}
        )
    ])

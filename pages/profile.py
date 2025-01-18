from dash import html, dcc
import dash_bootstrap_components as dbc
from flask import session

def profile_layout():
    """
    Layout pour la page de profil utilisateur :
      - Affiche le nom et l'email depuis la session
      - Un bouton "Logout" qui redirige vers /logout
    """

    # Vérifier si l'utilisateur est connecté
    # (c'est-à-dire si user_name et user_email existent et ne sont pas vides)
    if not session.get("user_name") or not session.get("user_email"):
        # Si l'utilisateur n'est pas connecté, on le redirige vers la page de login
        return dcc.Location(pathname="/login", id="redirect-to-login")

    user_name = session["user_name"]
    user_email = session["user_email"]

    return html.Div([
        dbc.Container([
            # Titre
            html.H2("Mon profil", className="text-center mt-4 mb-4"),

            # Affichage des informations utilisateur
            dbc.Card([
                dbc.CardBody([
                    html.H4("Informations du compte", className="card-title"),
                    html.P(f"Nom : {user_name}", className="card-text"),
                    html.P(f"Email : {user_email}", className="card-text"),
                ])
            ], className="mb-3"),

            # Bouton logout (redirection vers /logout)
            html.Div([
                html.A(
                    dbc.Button("Se déconnecter", color="danger"),
                    href="/logout"  # Vous devez avoir une route Flask ou Dash qui gère la déconnexion
                )
            ], style={"textAlign": "center"})
        ], style={"maxWidth": "500px", "marginTop": "50px"})
    ])

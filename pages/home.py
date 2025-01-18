from dash import html
from flask import session, request

def home_layout():
    """Layout de la page d'accueil."""
    # Vérifier si la session contient les informations de l'utilisateur avant de les récupérer
    if "user_name" in session and "user_email" in session:
        user_name = session["user_name"]
    else:
        user_name = ""
    
    if user_name == "":
        title = "Bienvenue sur DataStick !"
    else:
        title = f"Bienvenue sur DataStick, {user_name}"

    # Mettre le nom de l'utilisateur dans le message de bienvenue "Bienvenue sur DataStick, {user_name}"
    return html.Div([
        html.H1(title, style={'textAlign': 'center'}),
        html.P("Utilisez cette application pour surveiller et analyser les actions financières.", style={'textAlign': 'center'}),
    ])

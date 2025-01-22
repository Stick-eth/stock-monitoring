from dash import html
import dash_bootstrap_components as dbc
from flask import session
from model.user_favorite import get_favorite_tickers
from model.tickers_list import get_specific_tickers

def home_layout():
    """Layout de la page d'accueil."""
    # Vérifier si la session contient les informations de l'utilisateur avant de les récupérer
    if "user_name" in session and "user_email" in session:
        user_name = session["user_name"]
        user_email = session["user_email"]

        # Récupérer les tickers favoris de l'utilisateur
        favorite_tickers = get_favorite_tickers(user_email)
        favorite_tickers_info = get_specific_tickers(favorite_tickers)
    else:
        user_name = ""
        favorite_tickers_info = []

    # Définir le titre
    title = f"Welcome to DataStick, {user_name}" if user_name else "Welcome to DataStick !"

    # Création de la grille horizontale avec les cartes Bootstrap pour les tickers favoris
    if favorite_tickers_info:
        cards = [
            dbc.Card(
                dbc.CardBody([
                    html.H4(ticker["symbol"], className="card-title", style={"marginBottom": "5px"}),
                    html.P(ticker["name"], className="card-text", style={"marginBottom": "5px"}),
                    html.P(f"Market Cap: {ticker['market_cap']}", className="card-text", style={"fontSize": "0.9em"})
                ]),
                style={"width": "18rem", "margin": "10px"},
                className="shadow-sm"
            ) for ticker in favorite_tickers_info
        ]

        grid = dbc.Row(
            [dbc.Col(card, width="auto") for card in cards],
            className="g-3",
            justify="start",
            style={"marginTop": "20px"}
        )
    else:
        grid = html.P("You don't have any favorite tickers yet.", style={"textAlign": "center", "marginTop": "20px"})

    # Retourner le layout complet
    return html.Div([
        html.H1(title, style={'textAlign': 'center'}),
        html.P("Here are your favorite tickers:", style={'textAlign': 'center'}),
        grid
    ])

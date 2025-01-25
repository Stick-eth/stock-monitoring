from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
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
    title = f"Hi {user_name}! 👋" if user_name else "Welcome to DataStick !"

    # Création du carrousel avec un affichage horizontal forcé
    if favorite_tickers_info:
        grid = html.Div([html.P("Here are your favorite tickers:", style={'textAlign': 'center'}),dmc.Carousel(
            children=[
                dmc.CarouselSlide(
                    html.Div([
                        html.Div([
                            html.A(
                                href=f"/stocks/{ticker['symbol']}",
                                children=[
                                    html.P(ticker["symbol"], style={"fontWeight": "bold", "fontSize": "1.2em", "marginRight": "5px", "marginBottom": "0"}),
                                    html.P(ticker["name"], style={"fontSize": "1em", "opacity": "0.8", "marginTop": "0"})
                                ],
                                style={"textDecoration": "none", "color": "inherit"}
                            ),
                        ], style={"marginBottom": "8px"}),

                        html.P(f"Market Cap: {ticker['market_cap']}", 
                            style={"fontSize": "0.8em", "marginTop": "5px", "opacity": "0.6"})
                    ], 
                    
                    )  # Style individuel de chaque carte
                ) for ticker in favorite_tickers_info
            ],
            id="carousel-size",
            withIndicators=False,
            withControls=False,
            autoScroll=True,
            height=200,
            skipSnaps=True,
            slideSize='20%',
            slideGap={"base": 0, "sm": "md"},
            loop=True,
            align="start",
            style={"margin": "20px auto", "width": "90%"}
        )])
    else:
        grid = html.P("")

    # Retourner le layout complet
    return html.Div([
        #gap just to make the layout look better
        html.P(title, style={'textAlign': 'center', 'marginTop': '20px','fontWeight':'bold','fontSize':'1.5em',}),
        grid,
    ])

from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from components.tickers_list import get_tickers

# Charger les tickers une seule fois pour éviter de recalculer à chaque interaction
ALL_TICKERS = get_tickers()  # Liste de dictionnaires [{'symbol': 'AAPL', 'name': 'Apple Inc', 'market_cap': '3.83 Trillion'}]

def stocks_list_layout():
    """Retourne le layout de la page listant les stocks avec une mise à jour en temps réel."""
    return html.Div([
        html.H1("💻 Stock Screener", style={'textAlign': 'center', 'marginTop': '20px'}),
        html.P("Recherchez une entreprise ou sélectionnez un ticker pour voir ses détails.", 
               style={'textAlign': 'center', 'marginTop': '10px'}),

        # Barre de recherche
        html.Div([
            dbc.Input(
                id="stock-search",
                type="text",
                placeholder="Rechercher un ticker...",
                style={'width': '50%', 'margin': '10px auto', 'textAlign': 'center'}
            )
        ], style={'textAlign': 'center'}),

        # Liste des tickers filtrés dynamiquement
        html.Div(id="filtered-ticker-list", style={'textAlign': 'center', 'marginTop': '20px'})
    ])

# Callback pour filtrer dynamiquement la liste des tickers en fonction de la recherche en temps réel
@callback(
    Output("filtered-ticker-list", "children"),
    Input("stock-search", "value")  # 🔹 Mise à jour instantanée dès qu'on tape
)
def update_ticker_list(search_value):
    search_value = (search_value or "").strip().lower()  # Normalisation pour éviter les erreurs de casse

    if not search_value:
        filtered_tickers = ALL_TICKERS[:50]  # Afficher un nombre limité de tickers si aucun filtre
    else:
        filtered_tickers = [
            ticker for ticker in ALL_TICKERS 
            if search_value in ticker["symbol"].lower() or search_value in ticker["name"].lower()
        ]

    if not filtered_tickers:
        return html.P("Aucun résultat trouvé.", style={"color": "red", "marginTop": "10px"})

    return html.Div([
        html.Div([
            dcc.Link(
                f"{ticker['symbol']} - {ticker['name']} | Market Cap: {ticker['market_cap']}",
                href=f"/stocks/{ticker['symbol']}",
                style={
                    'margin': '5px', 'padding': '10px', 'borderBottom': '1px solid #ddd', 
                    'display': 'block', 'fontSize': '18px', 'color': 'black', 'textDecoration': 'none'
                }
            )
        ], style={
            'padding': '5px', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9', 'marginBottom': '5px'
        }) for ticker in filtered_tickers
    ])

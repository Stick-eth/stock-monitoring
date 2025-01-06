from dash import html, dcc
from components.tickers_list import get_tickers

def stocks_list_layout():
    """Retourne le layout de la page Stocks."""
    return html.Div([
        html.H1("💻", style={'textAlign': 'center', 'marginTop': '20px'}),
        html.P("Sélectionnez un ticker pour voir les détails de l'entreprise.", style={'textAlign': 'center', 'marginTop': '20px'}),
        # Afficher en ligne la liste des tickers et un bouton à coté pour voir les détails qui redirige vers la page des stocks (/stocks/ticker)
        html.Div([
            html.Div([
                dcc.Link(
                    f"{ticker}",
                    href=f"/stocks/{ticker}",
                    style={'margin': '5px', 'padding': '5px', 'border': '1px solid #ccc', 'borderRadius': '5px', 'display': 'inline-block'}
                )
            ]) for ticker in get_tickers()
        ], style={'textAlign': 'center', 'marginTop': '20px'})

    ])
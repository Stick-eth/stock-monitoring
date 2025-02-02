from dash import html

import dash_bootstrap_components as dbc
def portfolio_overview_layout():
    """Retourne le layout de la page Portfolio Overview, pour l'instant vide."""
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H1("Portfolio Overview"),
                html.P("This page will display an overview of the user's portfolio."),
                html.P("(For now, it is empty ! 🚧)")
            ])
        ])
    ], className="container", style={"marginTop": "20px", "textAlign": "center"})
    
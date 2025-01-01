from dash import html


def home_layout():
    """Layout de la page d'accueil."""
    return html.Div([
        html.H1("Bienvenue sur DataStick", style={'textAlign': 'center'}),
        html.P("Utilisez cette application pour surveiller et analyser les actions financières.", style={'textAlign': 'center'}),
    ])

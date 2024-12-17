from dash import html

def home_layout():
    """Layout de la page d'accueil."""
    return html.Div([
        html.H1("Bienvenue sur Stock Monitoring", style={'textAlign': 'center', 'marginTop': '50px'}),
        html.P("Utilisez cette application pour surveiller et analyser les actions financières.", style={'textAlign': 'center'}),
    ])

from dash import dcc, html

def create_layout():
    """Retourne le layout de l'application."""
    return html.Div([
        html.H1("Analyse Financière des Tickers", style={'textAlign': 'center', 'marginTop': '20px'}),

        # Sélecteur de ticker
        dcc.Dropdown(
            id='ticker-dropdown',
            options=[{'label': ticker, 'value': ticker} for ticker in ['MA', 'V', 'MSFT', 'AAPL', 'TSLA']],
            value='AAPL',
            style={'width': '50%', 'margin': '20px auto'}
        ),

        # Graphiques financiers
        dcc.Graph(id='revenue-net-income-graph', style={'width': '60%', 'margin': '20px auto'}),
        dcc.Graph(id='price-graph', style={'width': '60%', 'margin': '20px auto'}),

        # Liste scrollable des insiders
        html.Div(id='insider-list', style={
            'width': '80%', 'height': '300px', 'overflowY': 'scroll',
            'border': '1px solid #ccc', 'margin': '20px auto', 'padding': '10px'
        }),

        html.Footer([
            html.P("Made by stick", style={'textAlign': 'center'})
        ])
    ])

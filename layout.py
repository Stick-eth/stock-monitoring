from dash import dcc, html
from components.tickers_list import get_tickers
from data_loader import DATA_DIRS


no_interaction = {
        'scrollZoom': False,         # Désactive le zoom avec la molette
        'doubleClick': False,        # Désactive le zoom avec double-clic
        'showTips': True,            # Affiche les tooltips au survol
        'displayModeBar': False,      # Cache la barre d'outils
        'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
        
    }

def create_layout():
    """Retourne le layout de l'application."""
    return html.Div([
        html.H1("Analyse Financière des Tickers", style={'textAlign': 'center', 'marginTop': '20px'}),

        # Sélecteur de ticker
        dcc.Dropdown(
            id='ticker-dropdown',
            options=[{'label': ticker, 'value': ticker} for ticker in get_tickers(DATA_DIRS)],
            value='AAPL',
            style={'width': '50%', 'margin': '20px auto'}
        ),

        # Graphiques financiers pour CA et Croissance du CA côte à côte
        html.Div([
            dcc.Graph(id='revenue-net-income-graph', style={'width': '48%', 'display': 'inline-block'},config=no_interaction),
            dcc.Graph(id='growth-graph', style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'},config=no_interaction)
        ], style={'display': 'flex', 'justify-content': 'center', 'marginTop': '20px'}),

        # Graphique des prix
        html.Div([
            dcc.Graph(id='price-graph', style={'width': '60%', 'margin': '20px auto'},config=no_interaction)
        ]),

        # Liste scrollable des insiders
        html.Div(id='insider-list', style={
            'width': '80%', 'height': '300px', 'overflowY': 'scroll',
            'border': '1px solid #ccc', 'margin': '20px auto', 'padding': '10px'
        }),

        html.Footer([
            html.P("Aniss SEJEAN", style={'textAlign': 'center'})
        ])
    ])


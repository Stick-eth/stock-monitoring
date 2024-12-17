from dash import html, dcc
from components.tickers_list import get_tickers
from data_loader import DATA_DIRS

# Configuration pour désactiver certaines interactions
no_interaction = {
    'scrollZoom': False,
    'doubleClick': False,
    'showTips': True,
    'displayModeBar': False,
    'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
}

def stocks_layout():
    """Retourne le layout de la page Stocks."""
    return html.Div([
        html.H1("Analyse Financière des Tickers", style={'textAlign': 'center', 'marginTop': '20px'}),

        # Sélecteur de ticker
        dcc.Dropdown(
            id='ticker-dropdown',
            options=[{'label': ticker, 'value': ticker} for ticker in get_tickers(DATA_DIRS)],
            value='AAPL',
            style={'width': '50%', 'margin': '20px auto'}
        ),

        # Graphiques financiers
        html.Div([
            dcc.Graph(id='revenue-net-income-graph', style={'width': '48%', 'display': 'inline-block'}, config=no_interaction),
            dcc.Graph(id='growth-graph', style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'}, config=no_interaction)
        ], style={'display': 'flex', 'justify-content': 'center', 'marginTop': '20px'}),

        html.Div([
            dcc.Graph(id='price-graph', style={'width': '60%', 'margin': '20px auto'}, config=no_interaction),
            dcc.Graph(id='fcf-op-graph', style={'width': '60%', 'margin': '20px auto'}, config=no_interaction)
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
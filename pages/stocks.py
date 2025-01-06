from dash import html, dcc
from components.tickers_list import get_tickers
from data_loader import DATA_DIRS

# Configuration pour désactiver certaines interactions
no_interaction = {
    'scrollZoom': False,
    'showTips': True,
    'displayModeBar': False,
    'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
}

def stocks_layout(ticker=None):
    """Retourne le layout de la page Stocks."""
    tickers = get_tickers()

    # Vérifier si le ticker est valide
    if ticker and ticker not in tickers:
        return html.Div([
            html.H1("💻 Stock Screener", style={'textAlign': 'center', 'marginTop': '20px'}),
            html.P(f"Le ticker '{ticker}' est invalide. Veuillez sélectionner un ticker valide.",
                   style={'textAlign': 'center', 'color': 'red', 'marginTop': '20px'}),
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

    return html.Div([
        html.H1(f"💻 Stock Screener", style={'textAlign': 'center', 'marginTop': '20px'}),

        # Conteneur pour le company-overview et le price-graph côte à côte
        html.Div([
            html.Div(
                id='company-overview', 
                style={'width': '60%', 'padding': '20px', 'boxSizing': 'border-box'}
            ),
            html.Div(
                dcc.Graph(id='price-graph', config=no_interaction),
                style={'padding': '20px', 'boxSizing': 'border-box', 'width': '40%'}
            )
        ], style={'width': '85%', 'margin': '20px auto', 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start'}),

        # Description de l'entreprise
        html.Div(id='company-description', style={'width': '80%', 'margin': '20px auto', 'color': 'rgb(80, 77, 113)'}),

        # Graphiques financiers
        html.Div([
            dcc.Graph(id='revenue-net-income-graph', style={'width': '48%', 'display': 'inline-block'}, config=no_interaction),
            dcc.Graph(id='growth-graph', style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'}, config=no_interaction)
        ], style={'display': 'flex', 'marginTop': '20px'}),

        # Autres graphiques
        html.Div([
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

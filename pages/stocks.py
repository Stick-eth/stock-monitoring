from dash import html, dcc
from components.tickers_list import get_tickers
from model.data_loader import DATA_DIRS
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


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
    tickers = [ticker['symbol'] for ticker in tickers]

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
        dmc.LoadingOverlay(
                    visible=True,
                    id="loading-overlay",
                    zIndex=10,
                    loaderProps={
                        "variant": "custom",
                        "children": dmc.Image(
                            h=150,
                            radius="md",
                            src="/assets/loading.gif",
                            style={
                                "objectFit": "contain",  # Empêche le GIF d'être coupé
                                "width": "100%",        # S'assure que le GIF occupe tout l'espace horizontal
                                "height": "100%",       # S'assure que le GIF occupe tout l'espace vertical
                                "display": "block",     # Évite les marges automatiques indésirables
                            },
                        ),
                    },
                    overlayProps={
                        "radius": "sm",
                        "blur": 2,
                        "style": {
                            "display": "flex",           # Permet un centrage avec flexbox
                            "alignItems": "center",      # Centre verticalement
                            "justifyContent": "center",  # Centre horizontalement
                            "position": "fixed",         # Assure une position absolue pleine page
                            "top": 0,
                            "left": 0,
                            "width": "100%",
                            "height": "100%",
                            "overflow": "hidden",        # Empêche tout dépassement
                        },
                    },
                    transitionProps={ "transition": 'fade', "duration": 1000 }
                ),
      
                html.Div([
                    html.Div(
                        id='company-overview'
                    ),
                        dcc.Graph(id='price-graph',style={'display': 'inline-block', 'marginLeft': '4%'}, config=no_interaction),
                ], style={
                    'display': 'flex',
                    'flexWrap': 'wrap',  # Permet de basculer les éléments sur une nouvelle ligne
                    'marginTop': '20px'
                },className="responsive-div"),

                # Graphiques financiers
                html.Div([
                    dcc.Graph(id='revenue-net-income-graph', style={'display': 'inline-block'}, config=no_interaction),
                    dcc.Graph(id='growth-graph', style={'display': 'inline-block', 'marginLeft': '4%'}, config=no_interaction)
                ], style={
                    'display': 'flex',
                    'flexWrap': 'wrap',  # Permet de basculer les éléments sur une nouvelle ligne
                    'marginTop': '20px'
                },className="responsive-div"),

                # Autres graphiques
                html.Div([
                    dcc.Graph(id='fcf-op-graph', style={'display': 'inline-block'}, config=no_interaction),
                    dcc.Graph(id='roce-graph', style={'display': 'inline-block', 'marginLeft': '4%'}, config=no_interaction)
                ], style={
                    'display': 'flex',
                    'flexWrap': 'wrap',  # Permet de basculer les éléments sur une nouvelle ligne
                    'marginTop': '20px'
                },className="responsive-div"),

                # Liste scrollable des insiders
                html.H6("Transactions d'Insiders", style={'textAlign': 'center', 'marginTop': '20px'}),
                html.Div(id='insider-list', style={
                    'width': '50%',
                    'height': '350px',
                    'overflowY': 'scroll',
                    'border': '1px solid #ccc',
                    'margin': '20px auto',
                    'padding': '10px'
                }),

                # Description de l'entreprise
                html.Div(id='company-description', style={
                    'width': '80%',
                    'margin': '20px auto',
                    'color': 'rgb(80, 77, 113)'
                }),
                # Bouton TradingView
                html.Div(id='tradingview-button', style={'textAlign': 'center'}),

                # Footer
                html.Footer([
                    html.P("Aniss SEJEAN", style={'textAlign': 'center'})
                ])
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px'})

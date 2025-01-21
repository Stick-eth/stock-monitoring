import threading
from dash import html, dcc, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
from model.tickers_list import get_tickers
from model.add_stock import get_ticker
from flask import session
import os
import dash

ALL_TICKERS = get_tickers()

def stocks_list_layout():
    user_email = session.get("user_email", "")
    admin = user_email == os.getenv("ADMIN_EMAIL")

    layout_children = [
        html.H1("💻 Stock Screener", style={'textAlign': 'center', 'marginTop': '20px'}),
        html.P("Recherchez une entreprise ou sélectionnez un ticker pour voir ses détails.", 
               style={'textAlign': 'center', 'marginTop': '10px'}),

        html.Div([
            dbc.Input(
                id="stock-search",
                type="text",
                placeholder="Rechercher un ticker...",
                style={'width': '50%', 'margin': '10px', 'display': 'inline-block'}
            ),
            dbc.Button("+", id="add-ticker-btn", color="primary", outline=True, className="ms-2", 
                       style={"display": "inline-block" if admin else "none"})
        ], style={'textAlign': 'center'}),

        html.Div(id="filtered-ticker-list", style={'textAlign': 'center', 'marginTop': '20px'}),
        dcc.Store(id="ticker-add-status", data=None),
        html.Div(id="add-ticker-status-message")
    ]

    layout_children.append(
        dbc.Modal(
            [
                dbc.ModalHeader("Ajouter un Ticker"),
                dbc.ModalBody([
                    dbc.Label("Nom du Ticker"),
                    dbc.Input(id="new-ticker-input", type="text", placeholder="Ex: AAPL"),
                    html.Br(),
                    dbc.Checkbox(id="force-toggle", label="Forcer l'ajout"),
                ]),
                dbc.ModalFooter([
                    dbc.Button("Annuler", id="close-modal-btn", color="secondary"),
                    # Ajout de `disabled=False` pour permettre la gestion en callback
                    dbc.Button("Ajouter", id="confirm-add-ticker-btn", color="primary", n_clicks=0, disabled=False),
                ]),
            ],
            id="add-ticker-modal",
            is_open=False,
            centered=True
        )
    )
    if not admin:
        layout_children[-1].style = {"display": "none"}

    return html.Div(layout_children)

@callback(
    Output("filtered-ticker-list", "children"),
    Input("stock-search", "value")
)
def update_ticker_list(search_value):
    search_value = (search_value or "").strip().lower()
    if not search_value:
        filtered_tickers = ALL_TICKERS[:50]
    else:
        filtered_tickers = [
            t for t in ALL_TICKERS 
            if search_value in t["symbol"].lower() or search_value in t["name"].lower()
        ]
    if not filtered_tickers:
        return html.P("Aucun résultat trouvé.", style={"color": "red", "marginTop": "10px"})
    
    return html.Div(
        style={'maxWidth': '700px', 'margin': '0 auto'},
        children=[
            dbc.Button(
                html.Div([
                    # Ligne 1 : Nom (gauche, en gras) + Market Cap (droite)
                    html.Div([
                        html.Div(
                            ticker['name'],
                            style={'fontWeight': 'bold', 'fontSize': '1rem', 'display': 'inline-block'}
                        ),
                        html.Div(
                            f"Market Cap: {ticker['market_cap']}",
                            style={'fontSize': '0.9rem', 'color': '#555', 'float': 'right'}
                        ),
                    ], style={'marginBottom': '5px', 'overflow': 'hidden'}),

                    # Ligne 2 : Symbole (en plus petit)
                    html.Div(
                        ticker['symbol'],
                        style={'fontSize': '0.85rem', 'color': '#666'}
                    )
                ]),
                href=f"/stocks/{ticker['symbol']}",
                color="white",               # Couleur de fond Bootstrap
                className="w-100 border border-1 shadow-sm text-start mb-2",
                style={
                    'padding': '10px',
                    'textDecoration': 'none'
                }
            )
            for ticker in filtered_tickers
        ]
    )



def threaded_get_ticker(ticker, force, store_component):
    """Exécute get_ticker dans un thread et met à jour l'état après exécution."""
    try:
        result = get_ticker(ticker, force)
        store_component.data = {"success": result, "ticker": ticker}
    except Exception as e:
        store_component.data = {"success": False, "error": str(e)}

@callback(
    [
        Output("add-ticker-modal", "is_open"),
        Output("ticker-add-status", "data"), 
        # On gère le disabled du bouton "Ajouter"
        Output("confirm-add-ticker-btn", "disabled")
    ],
    [
        Input("add-ticker-btn", "n_clicks"), 
        Input("close-modal-btn", "n_clicks"), 
        Input("confirm-add-ticker-btn", "n_clicks")
    ],
    [
        State("new-ticker-input", "value"), 
        State("force-toggle", "value"), 
        State("add-ticker-modal", "is_open"),
        State("ticker-add-status", "data")
    ]
)
def handle_modal_and_add_ticker(open_clicks, close_clicks, confirm_clicks, new_ticker, force, is_open, status_data):
    trigger_id = ctx.triggered_id

    if trigger_id == "add-ticker-btn":
        # Ouvre la modal et réactive le bouton au cas où il était désactivé
        return True, dash.no_update, False

    elif trigger_id == "close-modal-btn":
        # Ferme la modal et réactive le bouton pour la prochaine ouverture
        return False, dash.no_update, False

    elif trigger_id == "confirm-add-ticker-btn" and new_ticker:
        # Désactive le bouton "Ajouter" juste avant de lancer le thread
        # (pour éviter que l'utilisateur ne reclique immédiatement)
        thread = threading.Thread(
            target=threaded_get_ticker,
            args=(new_ticker.strip().upper(), force, dash.callback_context)
        )
        thread.start()
        # On ferme la modal et on remet le store à None
        # Le bouton est désactivé (True) tant que la modal est fermée
        return False, None, True

    return is_open, status_data, dash.no_update

@callback(
    Output("add-ticker-status-message", "children"),
    Input("ticker-add-status", "data")
)
def display_status_message(status_data):
    if not status_data:
        return dash.no_update
    if status_data.get("success"):
        return dbc.Alert(
            f"Le ticker {status_data['ticker']} a été ajouté avec succès !", 
            color="success", 
            dismissable=True
        )
    else:
        return dbc.Alert(
            f"Erreur lors de l'ajout : {status_data.get('error', 'Inconnu')}", 
            color="danger", 
            dismissable=True
        )

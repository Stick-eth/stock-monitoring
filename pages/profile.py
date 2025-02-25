from dash import html, dcc, callback, Input, Output, State, MATCH, ALL, ctx
import dash_bootstrap_components as dbc
from flask import session
from model.user_score import update_scores, get_scores, clear_scores

CRITERES = {
    "CAGR": "Compound annual growth rate",
    "Beta": "Beta",
    "P/E Ratio": "Price-to-earnings ratio",
    "EPS": "Earnings per share",
    "Dividend Yield": "Dividend yield"
}
    

def profile_layout():
    """Layout principal de la page de profil."""
    if not session.get("user_name") or not session.get("user_email"):
        return dcc.Location(pathname="/login", id="redirect-to-login")

    user_name = session["user_name"]
    user_email = session["user_email"]

    # Conteneur "read-only" pour l'affichage des critères
    read_only_criteria_list = dbc.ListGroup([], id="read-only-criteria-container", className="mb-3")

    return html.Div([
        dbc.Container([
            dcc.Location(id="redirect-refresh", refresh=True),
            html.H2("My profile", className="text-center mt-4 mb-4"),
            
            dbc.Card([
                dbc.CardBody([
                    html.H4("Account informations", className="card-title"),
                    html.P(f"Name : {user_name}", className="card-text"),
                    html.P(f"Email : {user_email}", className="card-text"),
                ])
            ], className="mb-3"),
            
            html.Div([
                html.A(
                    dbc.Button("Log out", color="danger"),
                    href="/logout"
                )
            ], style={"textAlign": "center"}),

            html.Hr(),
            html.H4("My criteria", className="text-center mt-4 mb-4"),

            # Liste en lecture seule
            read_only_criteria_list,

            # Bouton pour ouvrir le modal d'édition
            dbc.Button("Edit", id="open-edit-modal", color="primary", className="mt-3"),

        ], style={"maxWidth": "600px", "marginTop": "50px"}),

        # ------------- MODAL D'ÉDITION -------------
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Modifier mes critères")),
            dbc.ModalBody([
                # Liste des critères éditables
                dbc.ListGroup([], id="criteria-container", className="mb-3"),

                # On n'a plus besoin du bouton "Charger" vu qu'on charge automatiquement
                dbc.Button("+ Add a criteria", id="add-criteria", color="primary", className="mt-2"),
                html.Hr(),
                dbc.Button("Save", id="save-criteria", color="success"),
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-edit-modal", color="secondary")
            )
        ], id="edit-criteria-modal", is_open=False),
        dcc.Location(id="redirect-after-save", refresh=True)

    ])


# -------------------------------------------------------------------
# Callbacks
# -------------------------------------------------------------------

@callback(
    Output("edit-criteria-modal", "is_open"),
    [Input("open-edit-modal", "n_clicks"),
     Input("close-edit-modal", "n_clicks")],
    [State("edit-criteria-modal", "is_open")]
)
def toggle_modal(open_click, close_click, is_open):
    """Ouvre/Ferme le modal d'édition."""
    if open_click or close_click:
        return not is_open
    return is_open


@callback(
    Output("read-only-criteria-container", "children"),
    Input("edit-criteria-modal", "is_open"),
    prevent_initial_call=True
)
def update_read_only_criteria(is_open):
    """
    À chaque fermeture du modal, on recharge la liste en lecture seule depuis la DB.
    On suppose que l'utilisateur peut avoir modifié les critères, donc on se met à jour.
    """
    # Si le modal vient juste de s'ouvrir => on ne fait rien
    if is_open:
        return []

    user_email = session.get("user_email")
    if not user_email:
        return []

    stored_scores = get_scores(user_email)
    unique_criteria = set()
    items = []
    for score in stored_scores:
        criterion, values = list(score.items())[0]
        if criterion in unique_criteria:
            continue
        unique_criteria.add(criterion)
        items.append(create_read_only_item(criterion, values[0], values[1]))
    return items


@callback(
    # On autorise plusieurs triggers sur le même Output (ajout/suppression & chargement)
    Output("criteria-container", "children"),
    Input("edit-criteria-modal", "is_open"),  # pour charger auto quand on ouvre
    Input("add-criteria", "n_clicks"),        # pour ajouter
    Input({"type": "remove-criteria", "index": ALL}, "n_clicks"),  # pour retirer
    State("criteria-container", "children"),
    prevent_initial_call=True
)
def modify_criteria(is_open, add_clicks, remove_clicks, children):
    """
    Gère la liste des critères dans le modal (édition).
    - Au moment où le modal s'ouvre (is_open=True), on charge les critères depuis la DB.
    - On peut ensuite ajouter ou supprimer des critères dans la liste.
    """
    triggered_id = ctx.triggered_id
    user_email = session.get("user_email")

    # Si le callback est déclenché par l'ouverture du modal => on recharge depuis la DB
    if triggered_id == "edit-criteria-modal" and is_open and user_email:
        stored_scores = get_scores(user_email)
        unique_criteria = set()
        new_children = []
        for i, score in enumerate(stored_scores):
            criterion, values = list(score.items())[0]
            if criterion in unique_criteria:
                continue
            unique_criteria.add(criterion)
            new_children.append(create_criteria_item(i, criterion, values[0], values[1]))
        return new_children

    # Si on a cliqué sur "Ajouter un critère"
    elif triggered_id == "add-criteria":
        new_index = len(children)
        children.append(create_criteria_item(new_index, "", "", ""))
        return children

    # Si on a cliqué sur "remove-criteria"
    elif isinstance(triggered_id, dict) and triggered_id.get("type") == "remove-criteria":
        index_to_remove = triggered_id["index"]
        return [
            child for child in children
            if child["props"]["id"]["index"] != index_to_remove
        ]

    # Sinon on ne met rien à jour
    return children


@callback(
    Output({"type": "criteria-dropdown", "index": ALL}, "options"),
    Input({"type": "criteria-dropdown", "index": ALL}, "value"),
)
def update_dropdown_options(selected_values):
    """Empêche la sélection en double du même critère dans le Dropdown."""
    available_criteria = list(CRITERES.keys())
    updated_options = []

    for selected_value in selected_values:
        # Autorise la sélection "courante" ou celles qui ne sont pas déjà prises
        options = [
            {"label": c, "value": c}
            for c in available_criteria
            if c not in selected_values or c == selected_value
        ]
        updated_options.append(options)

    return updated_options


@callback(
    Output("redirect-after-save", "href"),  # Ajout d'un Output pour rediriger
    Input("save-criteria", "n_clicks"),
    State({"type": "criteria-dropdown", "index": ALL}, "value"),
    State({"type": "criteria-min", "index": ALL}, "value"),
    State({"type": "criteria-max", "index": ALL}, "value"),
    prevent_initial_call=True
)
def save_criteria(n_clicks, criteria_values, min_values, max_values):
    """Sauvegarde dans la DB les critères actuellement affichés dans le modal, puis recharge la page."""
    user_email = session.get("user_email")
    db_result = []
    
    if not user_email:
        return "/profile"  # Redirection après tentative de sauvegarde sans utilisateur

    if criteria_values:
        for i in range(len(criteria_values)):
            if criteria_values[i]:
                min_val = min_values[i] if min_values[i] else None
                max_val = max_values[i] if max_values[i] else None
                db_min_val = min_val if min_val is not None else 0
                db_max_val = max_val if max_val is not None else 0
                db_result.append({criteria_values[i]: [db_min_val, db_max_val]})

        update_scores(user_email, db_result)
    else:
        # Si aucun critère, on vide la DB
        clear_scores(user_email)

    return "/profile"  # Redirection vers la même page pour actualiser


# -------------------------------------------------------------------
# Fonctions utilitaires
# -------------------------------------------------------------------

def create_read_only_item(criterion, min_val, max_val):
    """Crée un item en lecture seule pour le container principal."""
    return dbc.ListGroupItem([
        dbc.Row([
            dbc.Col(html.B(criterion), width=4),
            dbc.Col(f"Min: {min_val}", width=3),
            dbc.Col(f"Max: {max_val}", width=3),
        ], className="align-items-center")
    ], className="mb-1")


def create_criteria_item(index, criterion, min_val, max_val):
    """Crée un item éditable pour le modal."""
    return dbc.ListGroupItem([
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    options=[{"label": c, "value": c} for c in CRITERES.keys()],
                    value=criterion,
                    id={"type": "criteria-dropdown", "index": index},
                    style={"width": "100%"}
                ), width=4
            ),
            dbc.Col(
                dbc.Input(
                    type="number", value=min_val,
                    placeholder="Min",
                    id={"type": "criteria-min", "index": index},
                    style={"width": "100%"}
                ), width=3
            ),
            dbc.Col(
                dbc.Input(
                    type="number", value=max_val,
                    placeholder="Max",
                    id={"type": "criteria-max", "index": index},
                    style={"width": "100%"}
                ), width=3
            ),
            dbc.Col(
                dbc.Button(
                    "✕",
                    id={"type": "remove-criteria", "index": index},
                    color="danger",
                    size="sm"
                ), width=1
            )
        ], className="align-items-center")
    ], id={"type": "criteria-item", "index": index})


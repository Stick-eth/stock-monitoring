from dash import html, dcc, callback, Input, Output, State, MATCH, ALL, ctx
import dash_bootstrap_components as dbc
import json
from flask import session

# Liste des critères prédéfinis avec descriptions attendues
CRITERES = {
    "Critère 1": "Valeur attendue en %",
    "Critère 2": "Nombre d'unités",
    "Critère 3": "Taux de croissance",
    "Critère 4": "Montant en euros",
    "Critère 5": "Valeur normalisée"
}

def profile_layout():
    if not session.get("user_name") or not session.get("user_email"):
        return dcc.Location(pathname="/login", id="redirect-to-login")

    user_name = session["user_name"]
    user_email = session["user_email"]

    return html.Div([
        dbc.Container([
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
            html.H4("Paramètres personnalisés"),
            
            dbc.ListGroup(id="criteria-container", className="mb-3"),
            
            dbc.Button("+ Ajouter un critère", id="add-criteria", color="primary", className="mt-2"),
            
            dbc.Button("Sauvegarder", id="save-criteria", color="success", className="mt-2 ml-2"),
            
            html.Pre(id="output-json", className="mt-3 p-2 border")
        ], style={"maxWidth": "600px", "marginTop": "50px"})
    ])

@callback(
    Output("criteria-container", "children"),
    Input("add-criteria", "n_clicks"),
    Input({"type": "remove-criteria", "index": ALL}, "n_clicks"),
    State("criteria-container", "children"),
    prevent_initial_call=True
)
def modify_criteria(add_clicks, remove_clicks, children):
    if children is None:
        children = []
    
    triggered_id = ctx.triggered_id
    
    if triggered_id == "add-criteria" and len(children) < 10:
        index = len(children)
        
        criteria_row = dbc.ListGroupItem([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        options=[{"label": c, "value": c} for c in CRITERES.keys()],
                        id={"type": "criteria-dropdown", "index": index},
                        placeholder="Sélectionner un critère",
                        style={"width": "100%"}
                    ), width=3
                ),
                dbc.Col(
                    dcc.Input(
                        type="number", id={"type": "criteria-min", "index": index},
                        placeholder="Min", style={"width": "100%"}
                    ), width=2
                ),
                dbc.Col(
                    dcc.Input(
                        type="number", id={"type": "criteria-max", "index": index},
                        placeholder="Max", style={"width": "100%"}
                    ), width=2
                ),
                dbc.Col(
                    html.Small(
                        id={"type": "criteria-description", "index": index},
                        children="",
                        className="text-muted"
                    ), width=3
                ),
                dbc.Col(
                    dbc.Button("✕", id={"type": "remove-criteria", "index": index}, color="danger", size="sm"),
                    width=1
                )
            ], className="align-items-center")
        ])
        children.append(criteria_row)
    
    elif isinstance(triggered_id, dict) and triggered_id.get("type") == "remove-criteria":
        index_to_remove = triggered_id["index"]
        children = [child for i, child in enumerate(children) if i != index_to_remove]
    
    return children

@callback(
    Output({"type": "criteria-description", "index": MATCH}, "children"),
    Input({"type": "criteria-dropdown", "index": MATCH}, "value"),
    prevent_initial_call=True
)
def update_description(selected_criteria):
    return CRITERES.get(selected_criteria, "")

@callback(
    Output("output-json", "children"),
    Input("save-criteria", "n_clicks"),
    State({"type": "criteria-dropdown", "index": ALL}, "value"),
    State({"type": "criteria-min", "index": ALL}, "value"),
    State({"type": "criteria-max", "index": ALL}, "value"),
    prevent_initial_call=True
)
def save_criteria(n_clicks, criteria_values, min_values, max_values):
    result = []
    if criteria_values:
        for i in range(len(criteria_values)):
            if criteria_values[i]:
                min_val = min_values[i] if min_values[i] is not None else 0
                max_val = max_values[i] if max_values[i] is not None else 0
                result.append({criteria_values[i]: [min_val, max_val]})
    
    return json.dumps(result, indent=2, ensure_ascii=False)

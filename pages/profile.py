from dash import html, dcc, callback, Input, Output, State, MATCH, ALL, ctx
import dash_bootstrap_components as dbc
import json
from flask import session
from model.user_score import update_scores, get_scores, clear_scores

# Liste des critères prédéfinis
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
            
            dbc.Button("Charger", id="load-criteria", color="secondary", className="mt-2"),
            
            dbc.Button("+ Ajouter un critère", id="add-criteria", color="primary", className="mt-2 ml-2"),
            
            dbc.Button("Sauvegarder", id="save-criteria", color="success", className="mt-2 ml-2"),
            
            html.Pre(id="output-json", className="mt-3 p-2 border")
        ], style={"maxWidth": "600px", "marginTop": "50px"})
    ])

@callback(
    Output("criteria-container", "children"),
    Input("load-criteria", "n_clicks"),
    Input({"type": "remove-criteria", "index": ALL}, "n_clicks"),
    State("criteria-container", "children"),
    prevent_initial_call=True
)
def modify_criteria(load_clicks, remove_clicks, children):
    user_email = session.get("user_email")
    triggered_id = ctx.triggered_id
    
    if triggered_id == "load-criteria" and user_email:
        children = []
        stored_scores = get_scores(user_email)
        unique_criteria = set()
        for i, score in enumerate(stored_scores):
            criterion, values = list(score.items())[0]
            if criterion in unique_criteria:
                continue  # Ignore duplicate criteria
            unique_criteria.add(criterion)
            children.append(dbc.ListGroupItem([
                dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        options=[{"label": c, "value": c} for c in CRITERES.keys()],
                        value=criterion,
                        id={"type": "criteria-dropdown", "index": i},
                        style={"width": "100%"}
                    ), width=4),
                    dbc.Col(dcc.Input(
                        type="number", value=values[0], id={"type": "criteria-min", "index": i},
                        style={"width": "100%"}
                    ), width=3),
                    dbc.Col(dcc.Input(
                        type="number", value=values[1], id={"type": "criteria-max", "index": i},
                        style={"width": "100%"}
                    ), width=3),
                    dbc.Col(dbc.Button("✕", id={"type": "remove-criteria", "index": i}, color="danger", size="sm"), width=1)
                ], className="align-items-center")
            ]))
        return children
    
    elif isinstance(triggered_id, dict) and triggered_id.get("type") == "remove-criteria":
        index_to_remove = triggered_id["index"]
        children = [child for i, child in enumerate(children) if i != index_to_remove]
    
    return children

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
    user_email = session.get("user_email")
    
    if criteria_values and user_email:
        for i in range(len(criteria_values)):
            if criteria_values[i]:
                min_val = min_values[i] if min_values[i] is not None else 0
                max_val = max_values[i] if max_values[i] is not None else 0
                result.append({criteria_values[i]: [min_val, max_val]})
        
        # Enregistrer les données en BDD
        update_scores(user_email, result)
    
    return json.dumps(result, indent=2, ensure_ascii=False)

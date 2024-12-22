from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import json



def create_description_company(data_overview):
    """Crée un composant affichant la description de l'entreprise."""
    try:    
        # Si les données sont manquantes, on remplace par "N/A" au lieu de stopper l'affichage.
        description = data_overview.get("Description", "N/A")
        return html.Div([
            # Premier container
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H5("Description de l'entreprise"),
                        html.P(description)
                    ]), className="d-flex align-items-center justify-content-center"),
                ])
            ])
        ])
    except Exception as e:
        print(f"Erreur lors de la création de la description de l'entreprise : {e}")
        return html.P("Erreur lors de la création de la description de l'entreprise.")
    
    

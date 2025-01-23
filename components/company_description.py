from dash import html
import dash_bootstrap_components as dbc

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
                        html.P(description)
                    ]), className="d-flex align-items-center justify-content-center"),
                ])
            ])
        ])
    except Exception as e:
        print(f"Error in create description company: {e}")
        return html.P("An error occured while trying to display the company description.")
    
    

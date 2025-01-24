from dash import html
import dash_bootstrap_components as dbc
from components.utils.overview_utils import *

def create_company_header(data_overview):
    """Crée un composant affichant la description de l'entreprise."""
    try:    
        # Récupération des données avec valeurs par défaut
        name = data_overview.get("Name", "N/A") if data_overview else "N/A"
        sector = data_overview.get("Sector", "N/A") if data_overview else "N/A"
        industry = data_overview.get("Industry", "N/A") if data_overview else "N/A"
        description = data_overview.get("Description", "N/A") if data_overview else "N/A"
        ticker = data_overview.get("Symbol", "N/A") if data_overview else "N/A"

        # Ajout de l'emoji, si possible, sinon 📈
        emoji = get_emoji_by_ticker(ticker) 
        if emoji == "":
            emoji = "📈"

        name = f"{emoji} {name}"

        return dbc.Stack([
                    html.H2(name, className="company-name"),
                    html.H6("Company Description", className="company-description-title", style={'marginTop': '0.5rem','fontweight': 'bold'}),
                    html.P(description, className="company-description", style={'width': '90%', 'fontSize': '0.9rem', 'opacity': '0.6'}), 

                ])
    
    except Exception as e:
        print(f"Error in create description company: {e}")
        return html.P("An error occurred while trying to display the company description.")

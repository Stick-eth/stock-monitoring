
from dash import html
import dash_bootstrap_components as dbc

def create_tradingview_button(data_overview):
    """Crée un composant affichant la description de l'entreprise."""
    try:    
        exchange = data_overview.get("Exchange", "N/A")
        symbol = data_overview.get("Symbol", "N/A")
        # Lien exemple : https://www.tradingview.com/chart/gE4RreoN/?symbol={exchange}%3A{symbol}
        link = f"https://www.tradingview.com/chart/gE4RreoN/?symbol={exchange}%3A{symbol}"
        # Retourner un bouton couleur secondaire avec le lien TradingView 
        return html.Div([
            dbc.Button("See on TradingView", color="primary", href=link, target="_blank", style={"width": "100%"})
        ])
    except Exception as e:
        return dbc.Button("Open TradingView", color="primary", href="https://www.tradingview.com/", target="_blank")
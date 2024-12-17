from dash import html

def create_insider_list(data):
    """Crée une liste scrollable des transactions d'insiders."""
    if not data:
        return html.P("Aucune transaction d'insiders disponible.")

    max_items = 50
    items = []
    for tx in data[:max_items]:
        items.append(html.Div([
            html.P(f"{tx['Insider']} - {tx['Start Date']}", style={'fontWeight': 'bold'}),
            html.P(f"Position : {tx['Position']} | Actions : {tx['Shares']} | Valeur : {tx['Value']}"),
            html.Hr()
        ]))
    return items

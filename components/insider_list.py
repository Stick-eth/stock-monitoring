from dash import html

def create_insider_list(data):
    """Crée une liste scrollable des transactions d'insiders avec coloration basée sur les mots-clés."""
    if not data:
        return html.P("Aucune transaction d'insiders disponible.")

    max_items = 50
    items = []

    for tx in data[:max_items]:
        # Récupérer le champ 'Text' ou indiquer "Détail non spécifié" si vide
        text = tx.get('Text', '').strip()
        if not text:
            text = "Détail non spécifié"

        # Détecter les mots-clés dans le champ 'Text'
        background_color = '#FFFFFF'  # Couleur par défaut (blanc)

        if 'Sale' in text:
            background_color = '#FFCCCC' # Rouge clair pour les ventes
        elif any(keyword in text for keyword in ['Award', 'Grant', 'Conversion','Gift']):
            background_color = '#CCFFCC'  # Vert clair pour les attributions et conversions

        # Créer l'élément de la liste avec le style approprié
        item = html.Div([
            html.P(f"{tx['Insider']} - {tx['Start Date']}", style={'fontWeight': 'bold'}),
            html.P(f"Position : {tx['Position']} | Actions : {tx['Shares']} | Valeur : {tx['Value']}"),
            html.P(f"Détail : {text}"),
            html.Hr(style={'margin': '10px 0'})
        ], style={'backgroundColor': background_color, 'padding': '10px', 'marginBottom': '10px', 'borderRadius': '5px'})

        items.append(item)

    return items

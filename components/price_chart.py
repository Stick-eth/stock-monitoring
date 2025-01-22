import plotly.graph_objs as go
from datetime import datetime
from components.utils.common_layout import apply_common_layout

def create_price_chart(data):
    try:
        """Crée un graphique des prix sans pandas."""
        if not data:
            return go.Figure()

        # Convertir les données en listes
        dates = [datetime.strptime(entry["Date"], "%Y-%m-%d %H:%M:%S%z") for entry in data]
        closes = [float(entry["Close"]) for entry in data]

        # Calcul du prix le plus haut (ATH)
        ath = max(closes)

        # Créer le graphique
        fig = go.Figure()

        # Ajouter la ligne de l'ATH
        fig.add_trace(go.Scatter(
            x=[min(dates), max(dates)],
            y=[ath, ath],
            mode='lines',
            name="ATH",
            line=dict(color='green', dash='dash', width=2),
            opacity=0.5,
            text=[f"ATH: {ath:.2f}"]
        ))

        # Ajouter le prix de clôture
        fig.add_trace(go.Scatter(
            x=dates,
            y=[round(close, 2) for close in closes],
            mode='lines',
            name="USD",
            line=dict(color='rgb(182, 174, 255)'),
            fill='tozeroy',
            fillcolor='rgba(0, 0, 0, 0)'
        ))

        # Mettre à jour la mise en page
        fig = apply_common_layout(
            fig,
            title="Price",
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False
        )
        
        fig.update_layout(
            yaxis=dict( showticklabels=False, showline=False),
            xaxis=dict(color='rgb(90, 86, 126)', showline=True, linecolor='rgb(53, 51, 75)')
        )

        return fig

    except Exception as e:
        print(f"Error creating price chart: {e}")
        return go.Figure().update_layout(title="An error occurred while creating the chart.")

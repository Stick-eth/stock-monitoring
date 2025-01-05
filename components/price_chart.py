import plotly.graph_objs as go
from datetime import datetime

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
            name="Prix de Clôture",
            line=dict(color='rgb(107, 102, 153)'),
            fill='tozeroy',
            fillcolor='rgba(167, 163, 194, 0.3)'
        ))

        # Mettre à jour la mise en page
        fig.update_layout(
            title="Prix de l'Action",
            xaxis_title="Date",
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(showticklabels=False, autorange=True, type='log'),
            xaxis=dict(showgrid=False, autorange=True),
            margin=dict(t=40),
            showlegend=False
        )

        return fig

    except Exception as e:
        print(f"Erreur lors de la création du graphique des prix : {e}")
        return go.Figure().update_layout(title="Graphique non disponible")

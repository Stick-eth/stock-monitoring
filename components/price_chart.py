import plotly.graph_objs as go
import pandas as pd

def create_price_chart(data):
    try:
        """Crée un graphique des prix."""
        if not data:
            return go.Figure()

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"], utc=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode='lines', name="Prix de Clôture"))

        fig.layout.yaxis.fixedrange = True

        fig.update_layout(
            title="Prix de l'Action",
            xaxis_title="Date",
            yaxis_title="Prix",
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(showticklabels=False)
        )
        return fig
    except Exception as e:
        print(f"Erreur lors de la création du graphique des prix : {e}")
        return go.Figure().update_layout(title="Graphique non disponible")

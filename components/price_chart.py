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
        fig.layout.yaxis.fixedrange = True
        ath = df["Close"].max()
        fig.add_trace(go.Scatter(x=[df["Date"].min(), df["Date"].max()], y=[ath, ath], mode='lines', name="ATH", line=dict(color='green', dash='dash', width=2), opacity=0.5, text=[f"ATH: {ath:.2f}"]))
        fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"].apply(lambda x: round(x, 2)), mode='lines', name="Prix de Clôture", line=dict(color='rgb(107, 102, 153)'), fill='tozeroy', fillcolor='rgba(167, 163, 194, 0.3)'))
        fig.update_layout(
            title="Prix de l'Action",
            xaxis_title="Date",
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(showticklabels=False, autorange=True,type='log'),
            xaxis=dict(showgrid=False, autorange=True),
            margin=dict(t=40),
            showlegend=False  # Ensure legends are displayed
        )
        return fig
    except Exception as e:
        print(f"Erreur lors de la création du graphique des prix : {e}")
        return go.Figure().update_layout(title="Graphique non disponible")

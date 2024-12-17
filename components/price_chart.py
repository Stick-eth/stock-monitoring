import plotly.graph_objs as go
import pandas as pd

def create_price_chart(data):
    """Crée un graphique des prix."""
    if not data:
        return go.Figure()

    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"], utc=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode='lines', name="Prix de Clôture"))

    fig.update_layout(
        title="Prix de l'Action",
        xaxis_title="Date",
        yaxis_title="Prix"
    )
    return fig

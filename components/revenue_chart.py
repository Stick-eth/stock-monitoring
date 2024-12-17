import plotly.graph_objs as go
import pandas as pd

def create_revenue_chart(data):
    """Crée un graphique combiné pour le CA et Bénéfice Net."""
    if not data:
        return go.Figure()

    df = pd.DataFrame(data.get("annualReports", []))
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], utc=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["fiscalDateEnding"], y=df["totalRevenue"].astype(float), name="Chiffre d'Affaires"))
    fig.add_trace(go.Bar(x=df["fiscalDateEnding"], y=df["netIncome"].astype(float), name="Bénéfice Net"))

    fig.update_layout(
        title="Chiffre d'Affaires et Bénéfice Net",
        xaxis_title="Date",
        yaxis_title="Valeur",
        barmode="group"  # Barres côte-à-côte
    )
    return fig

import plotly.graph_objs as go
import pandas as pd

def create_revenue_chart(data):
    try :
        """Crée un graphique combiné pour le CA et Bénéfice Net."""
        if not data:
            return go.Figure()

        df = pd.DataFrame(data.get("annualReports", []))
        df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], utc=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["fiscalDateEnding"], y=df["totalRevenue"].astype(float) / 1e9, name="Chiffre d'Affaires", hovertemplate='Chiffre d\'Affaires : $%{y:.2f} milliards<extra></extra>'))
        fig.add_trace(go.Bar(x=df["fiscalDateEnding"], y=df["netIncome"].astype(float) / 1e9, name="Bénéfice Net", hovertemplate='Bénéfice Net : $%{y:.2f} milliards<extra></extra>'))

        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True

        fig.data[0].marker.color = 'rgb(107, 102, 153)'  # Change the color of the first bar (Chiffre d'Affaires)
        
        # Change the color of the second bar (Bénéfice Net) based on its value
        net_income_colors = ['rgb(167, 163, 194)' if val >= 0 else 'red' for val in df["netIncome"].astype(float)]
        fig.data[1].marker.color = net_income_colors
        fig.data[1].marker.color = 'rgb(167, 163, 194)'  # Change the color of the second bar (Bénéfice Net)
        
        fig.update_layout(
            title="Chiffre d'Affaires et Bénéfice Net",
            xaxis_title="Date",
            yaxis_title="Valeur",
            barmode="group",  # Barres côte-à-côte
            legend=dict(
                orientation="h",
                y=-0.2,  # Place la légende sous le graphique
                x=0.5,
                xanchor="center"
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(showticklabels=False),
            hovermode="x unified"
        )
        return fig

    except Exception as e:
        print(f"Erreur lors de la création du graphique du CA et Bénéfice Net : {e}")
        return go.Figure().update_layout(title="Graphique non disponible")
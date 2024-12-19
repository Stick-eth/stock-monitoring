import plotly.graph_objs as go
import pandas as pd
import numpy as np

def create_growth_chart(data):
    try:
        """Crée un graphique de croissance annuelle pour le CA et le Bénéfice Net."""
        if not data:
            return go.Figure()

        # Convertir les données en DataFrame
        df = pd.DataFrame(data.get("annualReports", []))
        df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], utc=True)
        df.sort_values("fiscalDateEnding", inplace=True)

        # Convertir les colonnes en float
        df["totalRevenue"] = df["totalRevenue"].astype(float)
        df["netIncome"] = df["netIncome"].astype(float)

        # Fonction pour calculer la croissance relative en évitant les explosions de pourcentage
        def relative_growth(current, previous):
            if previous == 0 or pd.isna(previous):
                return np.nan  # Évite les divisions par zéro
            return ((current - previous) / abs(previous)) * 100

        # Appliquer la fonction de croissance pour le chiffre d'affaires
        df["RevenueGrowth"] = df["totalRevenue"].combine(df["totalRevenue"].shift(1), relative_growth)

        # Appliquer la fonction de croissance pour le bénéfice net
        df["NetIncomeGrowth"] = df["netIncome"].combine(df["netIncome"].shift(1), relative_growth)

        # Plafonner les valeurs extrêmes pour éviter les graphiques illisibles
        df["RevenueGrowthClamped"] = df["RevenueGrowth"].clip(-100, 100)
        df["NetIncomeGrowthClamped"] = df["NetIncomeGrowth"].clip(-100, 100)

        # Créer le graphique
        fig = go.Figure()
        # Ajouter la croissance du CA
        fig.add_trace(go.Bar(
            x=df["fiscalDateEnding"],
            y=df["RevenueGrowth"],
            name="Croissance du Chiffre d'Affaires",
            marker_color=["green" if v > 0 else "red" for v in df["RevenueGrowth"]],
            hovertemplate='Croissance CA : %{y:.2f}%<extra></extra>'
        ))

        # Ajouter la croissance du bénéfice net
        fig.add_trace(go.Bar(
            x=df["fiscalDateEnding"],
            y=df["NetIncomeGrowth"],
            name="Croissance du Bénéfice Net",
            marker_color=["#66CC66" if v > 0 else "#FF6347" for v in df["NetIncomeGrowth"]],
            hovertemplate='Croissance  :Bénéf. Net %{y:.2f}%<extra></extra>'
        ))

        # Fixer les plages des axes pour éviter le zoom
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True

        # Personnaliser le graphique
        fig.update_layout(
            title="Croissance Chiffre d'Affaires & Bénéfice Net",
            barmode="group",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                y=-0.2,
                x=0.5,
                xanchor="center"
            ),
            showlegend=False,  # Retire la légende
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(showticklabels=False)
        )

        return fig

    except Exception as e:
        print(f"Erreur lors de la création du graphique de croissance : {e}")
        return go.Figure().update_layout(title="Graphique non disponible")
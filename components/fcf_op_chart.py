import plotly.graph_objs as go
import pandas as pd

def create_fcf_op_chart(data_income, data_cashflow):
    """Crée un graphique combiné pour le Free Cash Flow (FCF) et les Bénéfices Opérationnels."""

    try:
        if not data_income or not data_cashflow:
            return go.Figure().update_layout(title="Données non disponibles")

        # Convertir les données en DataFrame
        df_income = pd.DataFrame(data_income.get("annualReports", []))
        df_cashflow = pd.DataFrame(data_cashflow.get("annualReports", []))

        # Convertir les dates en datetime
        df_income["fiscalDateEnding"] = pd.to_datetime(df_income["fiscalDateEnding"], utc=True)
        df_cashflow["fiscalDateEnding"] = pd.to_datetime(df_cashflow["fiscalDateEnding"], utc=True)

        # Convertir les champs nécessaires en float
        df_cashflow["operatingCashflow"] = df_cashflow["operatingCashflow"].astype(float)
        df_cashflow["capitalExpenditures"] = df_cashflow["capitalExpenditures"].astype(float)
        df_income["operatingIncome"] = df_income["operatingIncome"].astype(float)

        # Fusionner les DataFrames sur la colonne "fiscalDateEnding"
        df = pd.merge(df_income, df_cashflow, on="fiscalDateEnding", suffixes=('_income', '_cashflow'))

        # Calculer le Free Cash Flow (FCF)
        df["FCF"] = df["operatingCashflow"] - df["capitalExpenditures"]

        # Créer le graphique
        fig = go.Figure()

        # Ajouter le Free Cash Flow (FCF)
        fig.add_trace(go.Bar(
            x=df["fiscalDateEnding"],
            y=df["FCF"] / 1e9,
            name="Free Cash Flow",
            marker_color='rgb(167, 163, 194)',
            hovertemplate='Free Cash Flow : $%{y:.2f} milliards<extra></extra>'
        ))

        # Ajouter les Bénéfices Opérationnels
        fig.add_trace(go.Bar(
            x=df["fiscalDateEnding"],
            y=df["operatingIncome"] / 1e9,
            name="Bénéfices Opérationnels",
            marker_color='rgb(107, 102, 153)',
            hovertemplate='Bénéfices Opérationnels : $%{y:.2f} milliards<extra></extra>'
        ))

        # Fixer les plages des axes pour éviter le zoom
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True

        # Mettre à jour la mise en page
        fig.update_layout(
            title="Free Cash Flow et Bénéfices Opérationnels",
            barmode="group",  # Barres côte-à-côte
            showlegend=False,  # Retire la légende
            yaxis=dict(showticklabels=False),  # Retire l'échelle de l'axe y
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )

        return fig

    except Exception as e:
        print(f"Erreur lors de la création du graphique FCF/Opérationnel : {e}")
        return go.Figure().update_layout(title="Graphique non disponible")

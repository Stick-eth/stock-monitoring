import plotly.graph_objs as go
import pandas as pd
import numpy as np

def create_fcf_op_chart(data_income, data_balance):
    try:
        """Crée un graphique combiné pour le Free Cash Flow (FCF) et les Bénéfices Opérationnels."""
        if not data_income or not data_balance:
            return go.Figure()

        # Convertir les données en DataFrame
        df_income = pd.DataFrame(data_income.get("annualReports", []))
        df_balance = pd.DataFrame(data_balance.get("annualReports", []))
        df_income["fiscalDateEnding"] = pd.to_datetime(df_income["fiscalDateEnding"], utc=True)
        df_balance["fiscalDateEnding"] = pd.to_datetime(df_balance["fiscalDateEnding"], utc=True)

        # Extraire les champs nécessaires
        df_income["netIncome"] = df_income["netIncome"].astype(float)
        df_income["depreciationAndAmortization"] = df_income["depreciationAndAmortization"].astype(float)
        df_income["operatingIncome"] = df_income["operatingIncome"].astype(float)
        df_balance["propertyPlantEquipment"] = df_balance["propertyPlantEquipment"].astype(float)

        # Fusionner les DataFrames sur la colonne "fiscalDateEnding"
        df = pd.merge(df_income, df_balance, on="fiscalDateEnding", suffixes=('_income', '_balance'))

        # Calculer le Free Cash Flow (FCF)
        df["FCF"] = df["netIncome"] + df["depreciationAndAmortization"] - df["propertyPlantEquipment"]

        # Créer le graphique
        fig = go.Figure()

        # Ajouter le Free Cash Flow (FCF)
        fig.add_trace(go.Bar(
            x=df["fiscalDateEnding"],
            y=df["FCF"] / 1e9,
            name="Free Cash Flow",
            marker_color='rgb(107, 142, 35)',
            hovertemplate='Free Cash Flow : $%{y:.2f} milliards<extra></extra>'
        ))

        # Ajouter les Bénéfices Opérationnels
        fig.add_trace(go.Bar(
            x=df["fiscalDateEnding"],
            y=df["operatingIncome"] / 1e9,
            name="Bénéfices Opérationnels",
            marker_color='rgb(70, 130, 180)',
            hovertemplate='Bénéfices Opérationnels : $%{y:.2f} milliards<extra></extra>'
        ))

        # Fixer les plages des axes pour éviter le zoom
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True

        # Mettre à jour la mise en page
        fig.update_layout(
            title="Free Cash Flow et Bénéfices Opérationnels",
            xaxis_title="Date",
            yaxis_title="Montant (en milliards de $)",
            barmode="group",  # Barres côte-à-côte
            legend=dict(
                orientation="h",
                y=-0.2,  # Place la légende sous le graphique
                x=0.5,
                xanchor="center"
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )

        return fig
    
    except Exception as e:
        print(f"Erreur lors de la création du graphique FCF/Opérationnel : {e}")
        return go.Figure().update_layout(title="Graphique non disponible")


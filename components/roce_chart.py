import plotly.graph_objs as go
from datetime import datetime

def create_roce_chart(data_income_statement, data_balance_sheet):
    try:
        """Crée un graphique de l'évolution du ROCE."""
        # Vérification des données
        if not data_income_statement or "annualReports" not in data_income_statement:
            return go.Figure().update_layout(title="Données non disponibles (Income Statement)")
        if not data_balance_sheet or "annualReports" not in data_balance_sheet:
            return go.Figure().update_layout(title="Données non disponibles (Balance Sheet)")

        # Extraire les rapports
        income_reports = data_income_statement["annualReports"]
        balance_reports = data_balance_sheet["annualReports"]

        # Extraire les colonnes nécessaires
        fiscal_dates = [report.get("fiscalDateEnding") for report in income_reports]
        ebits = [float(report.get("ebit", 0)) for report in income_reports]
        total_assets = [float(report.get("totalAssets", 0)) for report in balance_reports]
        current_liabilities = [float(report.get("totalCurrentLiabilities", 0)) for report in balance_reports]

        # Convertir les dates en format datetime
        fiscal_dates = [datetime.strptime(date, "%Y-%m-%d") for date in fiscal_dates]

        # Calculer le ROCE pour chaque année
        roces = []
        for ebit, assets, liabilities in zip(ebits, total_assets, current_liabilities):
            if assets - liabilities > 0:  # Éviter les divisions par zéro ou négatives
                roce = (ebit / (assets - liabilities)) * 100
            else:
                roce = None  # Indiquer les données manquantes ou non valides
            roces.append(roce)

        # Créer le graphique
        fig = go.Figure()

        # Ajouter les barres pour le ROCE
        fig.add_trace(go.Bar(
            x=fiscal_dates,
            y=[value if value is not None else 0 for value in roces],  # Remplacer None par 0 pour l'affichage
            name="ROCE (%)",
            hovertemplate='ROCE : %{y:.2f}%<extra></extra>',
            marker_color=['rgb(107, 142, 35)' if value and value >= 0 else 'red' for value in roces]  # Vert si positif, rouge si négatif ou nul
        ))

        # Mettre à jour la mise en page
        fig.update_layout(
            title="Évolution du ROCE",
            xaxis_title="Date",
            yaxis_title="ROCE (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified",
            yaxis=dict(showgrid=True),
            xaxis=dict(showgrid=True),
            legend=dict(
                orientation="h",
                y=-0.2,
                x=0.5,
                xanchor="center"
            )
        )

        return fig

    except Exception as e:
        print(f"Erreur lors de la création du graphique ROCE : {e}")
        return go.Figure().update_layout(title="Graphique non disponible")

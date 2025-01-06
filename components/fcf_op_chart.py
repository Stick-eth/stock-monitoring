import plotly.graph_objs as go
from components.utils.common_layout import apply_common_layout
from datetime import datetime

def create_fcf_op_chart(data_income, data_cashflow):
    """Crée un graphique combiné pour le Free Cash Flow (FCF) et les Bénéfices Opérationnels sans pandas."""
    try:
        if not data_income or not data_cashflow:
            return go.Figure().update_layout(title="Données non disponibles")

        # Extraire et convertir les données nécessaires
        income_reports = data_income.get("annualReports", [])
        cashflow_reports = data_cashflow.get("annualReports", [])

        # Préparer les données pour fusion par date
        income_data = {
            datetime.strptime(report["fiscalDateEnding"], "%Y-%m-%d"): float(report["operatingIncome"])
            for report in income_reports
            if "fiscalDateEnding" in report and "operatingIncome" in report
        }

        cashflow_data = {
            datetime.strptime(report["fiscalDateEnding"], "%Y-%m-%d"): (
                float(report["operatingCashflow"]),
                float(report["capitalExpenditures"])
            )
            for report in cashflow_reports
            if "fiscalDateEnding" in report and "operatingCashflow" in report and "capitalExpenditures" in report
        }

        # Fusionner les données sur la base des dates
        combined_data = []
        for date, operating_income in income_data.items():
            if date in cashflow_data:
                operating_cashflow, capital_expenditures = cashflow_data[date]
                fcf = operating_cashflow - capital_expenditures
                combined_data.append({
                    "date": date,
                    "operating_income": operating_income,
                    "fcf": fcf
                })

        # Trier les données par date
        combined_data.sort(key=lambda x: x["date"])

        # Extraire les données triées pour le graphique
        dates = [item["date"] for item in combined_data]
        fcf_values = [item["fcf"] / 1e9 for item in combined_data]
        operating_income_values = [item["operating_income"] / 1e9 for item in combined_data]

        # Créer le graphique
        fig = go.Figure()

        # Ajouter le Free Cash Flow (FCF)
        fig.add_trace(go.Bar(
            x=dates,
            y=fcf_values,
            name="Free Cash Flow",
            marker_color='rgb(167, 163, 194)',
            hovertemplate='Free Cash Flow : $%{y:.2f} milliards<extra></extra>'
        ))

        # Ajouter les Bénéfices Opérationnels
        fig.add_trace(go.Bar(
            x=dates,
            y=operating_income_values,
            name="Bénéfices Opérationnels",
            marker_color='rgb(107, 102, 153)',
            hovertemplate='Bénéfices Opérationnels : $%{y:.2f} milliards<extra></extra>'
        ))

        # Fixer les plages des axes pour éviter le zoom
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True

        fig = apply_common_layout(
            fig
        )
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

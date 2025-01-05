import plotly.graph_objs as go
from datetime import datetime

def create_revenue_chart(data):
    try:
        """Crée un graphique combiné pour le Chiffre d'Affaires (CA) et le Bénéfice Net sans pandas."""
        if not data or "annualReports" not in data:
            return go.Figure()

        # Extraire les données nécessaires depuis "annualReports"
        reports = data["annualReports"]

        # Extraire les colonnes nécessaires
        fiscal_dates = [report.get("fiscalDateEnding") for report in reports]
        total_revenues = [float(report.get("totalRevenue", 0)) for report in reports]
        net_incomes = [float(report.get("netIncome", 0)) for report in reports]

        # Convertir les dates en format datetime
        fiscal_dates = [datetime.strptime(date, "%Y-%m-%d") for date in fiscal_dates]

        # Créer le graphique
        fig = go.Figure()

        # Ajouter les barres pour le Chiffre d'Affaires
        fig.add_trace(go.Bar(
            x=fiscal_dates,
            y=[revenue / 1e9 for revenue in total_revenues],  # Convertir en milliards
            name="Chiffre d'Affaires",
            hovertemplate='Chiffre d\'Affaires : $%{y:.2f} milliards<extra></extra>',
            marker_color='rgb(107, 102, 153)'  # Couleur pour le Chiffre d'Affaires
        ))

        # Ajouter les barres pour le Bénéfice Net
        fig.add_trace(go.Bar(
            x=fiscal_dates,
            y=[income / 1e9 for income in net_incomes],  # Convertir en milliards
            name="Bénéfice Net",
            hovertemplate='Bénéfice Net : $%{y:.2f} milliards<extra></extra>',
            marker_color=['rgb(167, 163, 194)' if val >= 0 else 'red' for val in net_incomes]  # Couleur basée sur la valeur
        ))

        # Fixer les plages des axes pour éviter le zoom
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True

        # Mettre à jour la mise en page
        fig.update_layout(
            title="Chiffre d'Affaires et Bénéfice Net",
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

import plotly.graph_objs as go
from components.utils.common_layout import apply_common_layout


def create_growth_chart(data):
    try:
        """Crée un graphique de croissance annuelle pour le CA et le Bénéfice Net sans utiliser pandas."""
        if not data or "annualReports" not in data:
            return go.Figure().update_layout(title="Chart data not available")

        # Extraire les rapports annuels et les trier par date
        annual_reports = data["annualReports"]
        sorted_reports = sorted(annual_reports, key=lambda x: x.get("fiscalDateEnding"))

        # Extraire les données nécessaires
        fiscal_dates = [report.get("fiscalDateEnding") for report in sorted_reports]
        total_revenues = [float(report.get("totalRevenue", 0)) for report in sorted_reports]
        net_incomes = [float(report.get("netIncome", 0)) for report in sorted_reports]

        # Fonction pour calculer la croissance relative
        def relative_growth(current, previous):
            if previous == 0 or previous is None:
                return None  # Évite les divisions par zéro ou les valeurs manquantes
            return ((current - previous) / abs(previous)) * 100

        # Calculer les croissances pour le chiffre d'affaires et le bénéfice net
        revenue_growth = [
            relative_growth(total_revenues[i], total_revenues[i - 1]) if i > 0 else None
            for i in range(len(total_revenues))
        ]
        net_income_growth = [
            relative_growth(net_incomes[i], net_incomes[i - 1]) if i > 0 else None
            for i in range(len(net_incomes))
        ]

        # Créer le graphique
        fig = go.Figure()

        # Ajouter la croissance du CA
        fig.add_trace(go.Bar(
            x=fiscal_dates,
            y=revenue_growth,
            name="Total Revenue Growth",
            marker_color=["green" if v is not None and v > 0 else "red" for v in revenue_growth],
            hovertemplate='Revenue Growth : %{y:.2f}%<extra></extra>',
            marker_line_color='rgba(0,0,0,0)'
        ))

        # Ajouter la croissance du bénéfice net
        fig.add_trace(go.Bar(
            x=fiscal_dates,
            y=net_income_growth,
            name="Net Income Growth",
            marker_color=["#66CC66" if v is not None and v > 0 else "#FF6347" for v in net_income_growth],
            hovertemplate='Net Income Growth : %{y:.2f}%<extra></extra>',
            marker_line_color='rgba(0,0,0,0)'
        ))

        # Fixer les plages des axes pour éviter le zoom
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True

        fig = apply_common_layout(
            fig
        )

        # Personnaliser le graphique
        fig.update_layout(
            title="Annual Growth Chart",
            barmode="group",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                y=-0.2,
                x=0.5,
                xanchor="center"
            ),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(showticklabels=True, title="Growth (%)"),
            xaxis=dict(title="Date")
        )

        return fig

    except Exception as e:
        print(f"Error creating growth chart: {e}")
        return go.Figure().update_layout(title="An error occurred while creating the chart.")

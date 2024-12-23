import plotly.graph_objs as go

def create_growth_chart(data):
    try:
        """Crée un graphique de croissance annuelle pour le CA et le Bénéfice Net sans utiliser pandas."""
        if not data or "annualReports" not in data:
            return go.Figure()

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
            name="Croissance du Chiffre d'Affaires",
            marker_color=["green" if v is not None and v > 0 else "red" for v in revenue_growth],
            hovertemplate='Croissance CA : %{y:.2f}%<extra></extra>'
        ))

        # Ajouter la croissance du bénéfice net
        fig.add_trace(go.Bar(
            x=fiscal_dates,
            y=net_income_growth,
            name="Croissance du Bénéfice Net",
            marker_color=["#66CC66" if v is not None and v > 0 else "#FF6347" for v in net_income_growth],
            hovertemplate='Croissance Bénéf. Net : %{y:.2f}%<extra></extra>'
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
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(showticklabels=True, title="Croissance (%)"),
            xaxis=dict(title="Date")
        )

        return fig

    except Exception as e:
        print(f"Erreur lors de la création du graphique de croissance : {e}")
        return go.Figure().update_layout(title="Graphique non disponible")

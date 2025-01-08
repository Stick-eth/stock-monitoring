from dash.dependencies import Input, Output
from data_loader import load_data
from components.revenue_chart import create_revenue_chart
from components.price_chart import create_price_chart
from components.insider_list import create_insider_list
from components.revenue_growth import create_growth_chart
from components.fcf_op_chart import create_fcf_op_chart
from components.company_overview import create_company_overview
from components.company_description import create_description_company
from components.roce_chart import create_roce_chart

def register_callbacks(app):
    """Enregistre les callbacks Dash pour l'application."""
    @app.callback(
        [Output('revenue-net-income-graph', 'figure'),
         Output('price-graph', 'figure'),
         Output('growth-graph', 'figure'),
         Output('insider-list', 'children'),
         Output('fcf-op-graph', 'figure'),
         Output('company-overview', 'children'),
         Output('company-description', 'children'),
         Output('roce-graph', 'figure'),
         Output("loading-overlay", "visible")],
        [Input('url', 'pathname')]
    )
    def update_data(pathname):
        # Extraire le ticker depuis l'URL
        if pathname.startswith("/stocks/"):
            ticker = pathname.split("/stocks/")[-1]
        else:
            return (None, None, None, None, None, None, None, None ,False)

        # Charger les données pour le ticker si ce n'est pas un point
        if ticker != ".":
            data = load_data(ticker)
        else:
            return (None, None, None, None, None, None, None, None, False)

        # Générer les composants avec les données
        revenue_chart = create_revenue_chart(data.get("INCOME_STATEMENT"))
        price_chart = create_price_chart(data.get("PRICES"))
        growth_chart = create_growth_chart(data.get("INCOME_STATEMENT"))
        insider_list = create_insider_list(data.get("INSIDERS_TX"))
        fcf_op_chart = create_fcf_op_chart(data.get("INCOME_STATEMENT"), data.get("CASH_FLOW"))
        company_overview = create_company_overview(data.get("OVERVIEW"), data.get("INCOME_STATEMENT"), data.get("CASH_FLOW"), data.get("EARNINGS"))
        company_description = create_description_company(data.get("OVERVIEW"))
        roce_chart = create_roce_chart(data.get("INCOME_STATEMENT"),data.get("BALANCE_SHEET"))
        return (
            revenue_chart,
            price_chart,
            growth_chart,
            insider_list,
            fcf_op_chart,
            company_overview,
            company_description,
            roce_chart,
            False
        )

from dash.dependencies import Input, Output
from data_loader import load_data
from components.revenue_chart import create_revenue_chart
from components.price_chart import create_price_chart
from components.insider_list import create_insider_list
from components.revenue_growth import create_growth_chart
from components.fcf_op_chart import create_fcf_op_chart

def register_callbacks(app):
    """Enregistre les callbacks Dash pour l'application."""
    @app.callback(
        [Output('revenue-net-income-graph', 'figure'),
         Output('price-graph', 'figure'),
         Output('growth-graph', 'figure'),
         Output('insider-list', 'children'),
         Output('fcf-op-graph', 'figure')],
        Input('ticker-dropdown', 'value'),
    )
    def update_data(selected_ticker):
        data = load_data(selected_ticker)
        return (
            create_revenue_chart(data.get("INCOME_STATEMENT")),
            create_price_chart(data.get("PRICES")),
            create_growth_chart(data.get("INCOME_STATEMENT")),
            create_insider_list(data.get("INSIDERS_TX")),
            create_fcf_op_chart(data.get("INCOME_STATEMENT"), data.get("BALANCE_SHEET"))
        )

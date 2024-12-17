from dash.dependencies import Input, Output
from data_loader import load_data
from components.revenue_chart import create_revenue_chart
from components.price_chart import create_price_chart
from components.insider_list import create_insider_list

def register_callbacks(app):
    """Enregistre les callbacks Dash pour l'application."""
    @app.callback(
        [Output('revenue-net-income-graph', 'figure'),
         Output('price-graph', 'figure'),
         Output('insider-list', 'children')],
        Input('ticker-dropdown', 'value')
    )
    def update_data(selected_ticker):
        data = load_data(selected_ticker)
        return (
            create_revenue_chart(data.get("INCOME_STATEMENT")),
            create_price_chart(data.get("PRICES")),
            create_insider_list(data.get("INSIDERS_TX"))
        )

import os
import json
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
from datetime import datetime

# Initialisation de l'application Dash
app = Dash(__name__)

# Liste des tickers prédéfinis
TICKERS = ['MA', 'V', 'MSFT', 'AAPL', 'TSLA', 'ACN', 'SPGI', 'COST', 'BKNG']

BALANCE_SHEET_DIR = "./data/BALANCE_SHEET"
INCOME_STATEMENT_DIR = "./data/INCOME_STATEMENT"
OVERVIEW_DIR = "./data/OVERVIEW"
PRICES_DIR = "./data/PRICES"
INSIDER_TX_DIR = "./data/INSIDERS_TX"

# Fonction pour charger les données à partir des fichiers JSON
def load_data(ticker):
    try:
        with open(os.path.join(BALANCE_SHEET_DIR, f"{ticker}.json")) as f:
            balance_sheet_data = json.load(f)

        with open(os.path.join(INCOME_STATEMENT_DIR, f"{ticker}.json")) as f:
            income_statement_data = json.load(f)

        with open(os.path.join(OVERVIEW_DIR, f"{ticker}.json")) as f:
            overview_data = json.load(f)

        with open(os.path.join(PRICES_DIR, f"{ticker}.json")) as f:
            prices_data = json.load(f)

        with open(os.path.join(INSIDER_TX_DIR, f"{ticker}.json")) as f:
            insiders_data = json.load(f)

        return balance_sheet_data, income_statement_data, overview_data, prices_data, insiders_data

    except Exception as e:
        print(f"Erreur de chargement pour {ticker} : {e}")
        return None, None, None, None, None

# Fonction pour transformer les données du compte de résultat en DataFrame
def parse_income_statement(data):
    reports = data.get("annualReports", [])
    if not reports:
        return pd.DataFrame()

    df = pd.DataFrame(reports)
    if 'fiscalDateEnding' not in df.columns:
        print("La colonne 'fiscalDateEnding' est manquante dans les données du compte de résultat.")
        return pd.DataFrame()

    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], utc=True)
    df.set_index("fiscalDateEnding", inplace=True)
    return df

# Fonction pour transformer les prix en DataFrame
def parse_prices(data):
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"], utc=True)
    df.set_index("Date", inplace=True)
    return df

# Layout de l'application
app.layout = html.Div([
    # Titre principal
    html.H1("Analyse Financière des Tickers", style={'textAlign': 'center', 'marginTop': '20px'}),

    # Sélecteur de ticker
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in TICKERS],
        value=TICKERS[0],
        style={'width': '50%', 'margin': '20px auto'}
    ),

        # Graphique des prix
    html.Div([
        dcc.Graph(id='price-graph', style={'width': '60%', 'margin': '20px auto'}),
        dcc.Graph(id='revenue-graph', style={'width': '48%', 'display': 'inline-block'}),
    ],style={'display': 'flex', 'justify-content': 'center', 'marginTop': '20px'}),

    # Graphiques financiers
    html.Div([
        dcc.Graph(id='net-income-graph', style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'}),
        html.Div([
        html.H3("Transactions d'Insiders", style={'textAlign': 'center'}),
        html.Div(
            id='insider-list',
            style={
                'width': '80%',
                'height': '300px',
                'overflowY': 'scroll',
                'border': '1px solid #ccc',
                'margin': '20px auto',
                'padding': '10px'
            }
        ),
    ])
    ], style={'display': 'flex', 'justify-content': 'center', 'marginTop': '20px'}),

    # Liste scrollable des transactions d'insiders
    

    # Footer
    html.Footer([
        html.P(f"Date : {datetime.now().strftime('%Y-%m-%d')}", style={'textAlign': 'center', 'margin': '10px 0'}),
        html.P("Made by stick", style={'textAlign': 'center', 'margin': '0 0 20px 0'})
    ])
])

# Callback pour mettre à jour les graphiques en fonction du ticker sélectionné
@app.callback(
    [Output('revenue-graph', 'figure'),
     Output('net-income-graph', 'figure'),
     Output('price-graph', 'figure')],
    [Input('ticker-dropdown', 'value')]
)
def update_graphs(selected_ticker):
    _, income_statement_data, _, prices_data, _ = load_data(selected_ticker)

    # Initialiser des figures vides par défaut
    revenue_fig = go.Figure()
    net_income_fig = go.Figure()
    price_fig = go.Figure()

    # Graphique du chiffre d'affaires et du bénéfice net
    if income_statement_data:
        income_df = parse_income_statement(income_statement_data)
        if not income_df.empty:
            revenue_fig.add_trace(go.Scatter(
                x=income_df.index,
                y=income_df["totalRevenue"].astype(float),
                mode='lines+markers',
                name='Chiffre d\'affaires'
            ))
            revenue_fig.update_layout(
                title=f"Chiffre d'Affaires de {selected_ticker}",
                xaxis_title='Date',
                yaxis_title='Chiffre d\'Affaires'
            )

            net_income_fig.add_trace(go.Scatter(
                x=income_df.index,
                y=income_df["netIncome"].astype(float),
                mode='lines+markers',
                name='Bénéfice Net'
            ))
            net_income_fig.update_layout(
                title=f"Bénéfice Net de {selected_ticker}",
                xaxis_title='Date',
                yaxis_title='Bénéfice Net'
            )

    # Graphique des prix
    if prices_data:
        prices_df = parse_prices(prices_data)
        if not prices_df.empty:
            price_fig.add_trace(go.Scatter(
                x=prices_df.index,
                y=prices_df["Close"],
                mode='lines',
                name='Prix de clôture'
            ))
            price_fig.update_layout(
                title=f"Prix de l'Action de {selected_ticker}",
                xaxis_title='Date',
                yaxis_title='Prix de clôture'
            )

    return revenue_fig, net_income_fig, price_fig

# Callback pour mettre à jour la liste des transactions d'insiders
@app.callback(
    Output('insider-list', 'children'),
    [Input('ticker-dropdown', 'value')]
)
def update_insider_list(selected_ticker):
    _, _, _, _, insiders_data = load_data(selected_ticker)

    if not insiders_data:
        return html.P("Aucune transaction d'insiders disponible.")

    # Limite le nombre d'éléments affichés à 50
    max_items = 50
    items = []

    for tx in insiders_data[:max_items]:
        item = html.Div([
            html.P(f"{tx['Insider']} - {tx['Start Date']}", style={'fontWeight': 'bold'}),
            html.P(f"Position : {tx['Position']}"),
            html.P(f"Nombre d'actions : {tx['Shares']}"),
            html.P(f"Valeur : {tx['Value']}"),
            html.P(f"Détail : {tx['Text']}"),
            html.Hr(style={'margin': '10px 0'})
        ])
        items.append(item)

    return items

# Lancer le serveur
if __name__ == '__main__':
    app.run_server(debug=True)

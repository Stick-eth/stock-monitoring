from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

def create_company_overview(data_overview, data_income, data_cashflow, data_earnings):
    """Crée un composant affichant les données principales de l'entreprise dans une grille."""

    if not data_overview or not data_income or not data_cashflow or not data_earnings:
        return html.Div("Données insuffisantes", style={'textAlign': 'center', 'marginTop': '20px'})

    # Extraire les informations nécessaires
    name = data_overview.get("Name", "N/A")
    ticker = data_overview.get("Symbol", "N/A")
    dividend_yield = data_overview.get("DividendYield", "N/A")
    pe_ratio = data_overview.get("PERatio", "N/A")
    beta = data_overview.get("Beta", "N/A")
    latest_quarter = data_overview.get("LatestQuarter", "N/A")

    # EPS depuis les données EARNINGS
    earnings = data_earnings.get("annualEarnings", [])
    latest_eps = earnings[0].get("reportedEPS", "N/A") if earnings else "N/A"

    # Convertir le rendement des dividendes en pourcentage
    try:
        dividend_yield = f"{float(dividend_yield) * 100:.2f}%" if dividend_yield != "N/A" else "N/A"
    except ValueError:
        dividend_yield = "N/A"

    # Convertir les données en DataFrame
    df_income = pd.DataFrame(data_income.get("annualReports", []))
    df_cashflow = pd.DataFrame(data_cashflow.get("annualReports", []))

    # Convertir les champs nécessaires en float
    df_income["totalRevenue"] = pd.to_numeric(df_income["totalRevenue"], errors='coerce')
    df_cashflow["operatingCashflow"] = pd.to_numeric(df_cashflow["operatingCashflow"], errors='coerce')

    # Croissance du Chiffre d'Affaires
    revenue_growth_str = "N/A"
    if len(df_income["totalRevenue"].dropna()) >= 2:
        try:
            revenue_growth = ((df_income["totalRevenue"].iloc[-1] - df_income["totalRevenue"].iloc[-2]) /
                              df_income["totalRevenue"].iloc[-2]) * 100
            revenue_growth_str = f"{revenue_growth:.2f}%"
        except ZeroDivisionError:
            revenue_growth_str = "N/A"


    # Créer une grille avec Dash Bootstrap Components
    return dbc.Container([
        html.H3(f"Informations Principales - {name} ({ticker})", className="text-center my-4"),
        dbc.Row([
            dbc.Col(html.Div([
                html.H6("Nom de l'Entreprise"),
                html.P(name, className="fw-bold")
            ]), width=4),
            dbc.Col(html.Div([
                html.H6("Ticker"),
                html.P(ticker, className="fw-bold")
            ]), width=2),
            dbc.Col(html.Div([
                html.H6("Rendement des Dividendes"),
                html.P(dividend_yield, className="fw-bold")
            ]), width=3),
            dbc.Col(html.Div([
                html.H6("PER (Price-to-Earnings Ratio)"),
                html.P(pe_ratio, className="fw-bold")
            ]), width=3),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(html.Div([
                html.H6("Beta"),
                html.P(beta, className="fw-bold")
            ]), width=2),
            dbc.Col(html.Div([
                html.H6("Dernier Trimestre"),
                html.P(latest_quarter, className="fw-bold")
            ]), width=4),
            dbc.Col(html.Div([
                html.H6("Bénéfice par Action (EPS)"),
                html.P(latest_eps, className="fw-bold")
            ]), width=3),
            dbc.Col(html.Div([
                html.H6("Croissance du Chiffre d'Affaires"),
                html.P(revenue_growth_str, className="fw-bold")
            ]), width=3),
        ])
    ], className="border rounded p-4 shadow-sm bg-light")

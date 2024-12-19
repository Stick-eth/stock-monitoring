from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import json
from components.utils.overview_utils import *


def create_company_overview(data_overview, data_income, data_cashflow, data_earnings):
    """Crée un composant affichant les données principales de l'entreprise dans une grille avec tooltips,
    même si certaines données sont manquantes."""

    try:
        # Si les données sont manquantes, on remplace par "N/A" au lieu de stopper l'affichage.
        name, ticker, dividend_yield, pe_ratio, beta, sector, industry, country, exchange, capitalization = extract_company_data(data_overview)

        # Récupération du prix actuel et du prix il y a un an
        try:
            last_prices = fetch_last_price(ticker)
            current_price = last_prices[0] if len(last_prices) > 0 else None
            last_price_year_ago = last_prices[1] if len(last_prices) > 1 else None
        except:
            current_price = None
            last_price_year_ago = None

        # Calcul du badge de la variation en pourcentage
        current_price, variation, price_badge_color = calculate_price_variation(current_price, last_price_year_ago)
    
        # Charger les emojis
        emoji = get_emoji_by_ticker(ticker)

        # Dernier EPS depuis data_earnings
        latest_eps = get_latest_eps(data_earnings)

        # Conversion en DataFrame avec vérification
        df_income = pd.DataFrame(data_income.get("annualReports", [])) if data_income else pd.DataFrame()
        df_cashflow = pd.DataFrame(data_cashflow.get("annualReports", [])) if data_cashflow else pd.DataFrame()

        if "totalRevenue" in df_income.columns:
            df_income["totalRevenue"] = pd.to_numeric(df_income["totalRevenue"], errors='coerce')
        if "operatingCashflow" in df_cashflow.columns:
            df_cashflow["operatingCashflow"] = pd.to_numeric(df_cashflow["operatingCashflow"], errors='coerce')

        return html.Div([
            # Premier container
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H4(emoji if emoji else "📈", style={'fontSize': '2.5rem'}),
                        html.H5(name),
                        html.P((ticker if ticker != "N/A" else "") + (" - " + exchange if exchange != "N/A" else ""))
                    ]), className="d-flex align-items-center justify-content-center"),

                    dbc.Col(html.Div([
                        html.H6("Secteur", id="tooltip-sector", style={'textTransform': 'none'}),
                        html.P(sector if sector != "N/A" else "", className=" mb-0")
                    ]), className="d-flex align-items-center justify-content-center"),

                    dbc.Col(html.Div([
                        html.H6("Industrie", id="tooltip-industry", style={'textTransform': 'none'}),
                        html.P(industry if industry != "N/A" else "", className="mb-0")
                    ]), className="d-flex align-items-center justify-content-center"),

                    dbc.Col(html.Div([
                        html.H6("Pays", id="tooltip-country", style={'textTransform': 'none'}),
                        html.P(country if country != "N/A" else "", className="mb-0")
                    ]), className="d-flex align-items-center justify-content-center"),

                    dbc.Col(html.Div([
                        html.H6("Prix", style={'textTransform': 'none'}),
                        html.P(f"{current_price:.2f}$",  style={'fontSize': '1.5rem'}, className="fw-bold mb-0"),
                        dbc.Badge(f"{variation:.2f}%", color=price_badge_color, className="mt-2")
                    ]), className="d-flex align-items-center justify-content-center")
                ], className="bg-light border rounded p-2 shadow-sm mb-2 mt-4"),
            ], fluid=True, className="text-center", style={'marginleft': 'auto', 'marginright': 'auto'}),

            # Deuxième container
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H6("Capitalisation Boursière", style={'textTransform': 'none'}),
                        html.P(format_market_cap(capitalization) if format_market_cap(capitalization) != "N/A" else "", className="fw-bold mb-0")
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.H6("PER (Price-to-Earnings Ratio)", id="tooltip-pe-ratio", style={'textTransform': 'none'}),
                        html.P(pe_ratio if pe_ratio != "N/A" else "", className="fw-bold mb-0"),
                        dbc.Badge("< 30", color=get_pe_ratio_badge_color(pe_ratio))
                    ]), className="d-flex align-items-center justify-content-center"),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(html.Div([
                        html.H6("Beta", id="tooltip-beta", style={'textTransform': 'none'}),
                        html.P(beta if beta != "N/A" else "", className="fw-bold mb-0"),
                        dbc.Badge("> 1", color=get_beta_badge_color(beta))
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.H6("Bénéfice par Action (EPS)", id="tooltip-eps", style={'textTransform': 'none'}),
                        html.P(latest_eps if latest_eps != "N/A" else "", className="fw-bold mb-0")
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.H6("Rendement des Dividendes", id="tooltip-dividend-yield", style={'textTransform': 'none'}),
                        html.P(dividend_to_percent(dividend_yield) if dividend_to_percent(dividend_yield) != "N/A" else "", className="fw-bold mb-0"),
                        dbc.Badge("< 2%", color=get_dividend_yield_badge_color(dividend_yield))
                    ]), className="d-flex align-items-center justify-content-center")
                ])
            ], fluid=True, className="border rounded p-4 shadow-sm bg-light", style={'marginleft': 'auto', 'marginright': 'auto'}),

            # Tooltips
            dbc.Tooltip("Le secteur d'activité de l'entreprise. Ex : Technologie, Santé, Finance.", 
                        target="tooltip-sector", placement="top"),
            dbc.Tooltip("L'industrie précise au sein du secteur. Ex : Logiciels, Biotechnologie.", 
                        target="tooltip-industry", placement="top"),
            dbc.Tooltip("Le pays où l'entreprise est basée, ce qui peut influencer les régulations et le marché.", 
                        target="tooltip-country", placement="top"),
            dbc.Tooltip("Pourcentage des profits distribués aux actionnaires sous forme de dividendes. Un rendement élevé est souvent attractif pour les investisseurs.", 
                        target="tooltip-dividend-yield", placement="right"),
            dbc.Tooltip("Le ratio entre le prix de l'action et le bénéfice par action. Un PER faible peut indiquer que l'action est sous-évaluée.", 
                        target="tooltip-pe-ratio", placement="right"),
            dbc.Tooltip("Mesure de la volatilité de l'action par rapport au marché. Un Beta supérieur à 1 signifie plus de risque, mais aussi plus de potentiel de gain.", 
                        target="tooltip-beta", placement="bottom"),
            dbc.Tooltip("Le bénéfice net divisé par le nombre d'actions. Plus l'EPS est élevé, plus l'entreprise est rentable.", 
                        target="tooltip-eps", placement="bottom"),
            dbc.Tooltip("Le pourcentage d'augmentation des ventes sur une période donnée. Une croissance positive indique une entreprise en expansion.", 
                        target="tooltip-revenue-growth", placement="bottom"),
        ])
    except Exception as e:
        print(f"Erreur de création de l'aperçu de l'entreprise : {e}")
        return html.Div("Erreur de création de l'aperçu de l'entreprise", style={'textAlign': 'center', 'marginTop': '20px'})


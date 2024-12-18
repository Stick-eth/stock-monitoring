from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import json
from data.fetch_stock_last_price import fetch_last_price

def create_company_overview(data_overview, data_income, data_cashflow, data_earnings):
    """Crée un composant affichant les données principales de l'entreprise dans une grille avec tooltips,
    même si certaines données sont manquantes."""

    try:
        # Si les données sont manquantes, on remplace par "N/A" au lieu de stopper l'affichage.
        name = data_overview.get("Name", "N/A") if data_overview else "N/A"
        ticker = data_overview.get("Symbol", "N/A") if data_overview else "N/A"
        dividend_yield = data_overview.get("DividendYield", "N/A") if data_overview else "N/A"
        pe_ratio = data_overview.get("PERatio", "N/A") if data_overview else "N/A"
        beta = data_overview.get("Beta", "N/A") if data_overview else "N/A"
        sector = data_overview.get("Sector", "N/A") if data_overview else "N/A"
        industry = data_overview.get("Industry", "N/A") if data_overview else "N/A"
        country = data_overview.get("Country", "N/A") if data_overview else "N/A"
        exchange = data_overview.get("Exchange", "N/A") if data_overview else "N/A"
        capitalization = data_overview.get("MarketCapitalization", "N/A") if data_overview else "N/A"

        # Remplace le pays si USA
        if country == "USA":
            country = "United States 🦅"

        # Récupération du prix et de la variation
        try:
            last_prices = fetch_last_price(ticker)
            current_price = last_prices[0] if len(last_prices) > 0 else None
            last_price_year_ago = last_prices[1] if len(last_prices) > 1 else None
        except:
            current_price = None
            last_price_year_ago = None

        # Calcul de la variation en pourcentage
        if current_price is not None and last_price_year_ago is not None and last_price_year_ago != 0:
            variation = ((current_price - last_price_year_ago) / last_price_year_ago) * 100
            badge_color = "success" if variation >= 0 else "danger"
        else:
            variation = 0
            badge_color = "secondary"
            if current_price is None:
                current_price = 0.0

        # Convertir la capitalisation si disponible
        if capitalization not in ["N/A", None, ""]:
            try:
                cap_val = float(capitalization)
                if cap_val >= 1_000_000_000_000:
                    capitalization = f"{cap_val / 1_000_000_000_000:.2f} Trillion"
                elif cap_val >= 1_000_000_000:
                    capitalization = f"{cap_val / 1_000_000_000:.2f} Billion"
                else:
                    capitalization = f"{cap_val / 1_000_000:.2f} Million"
            except:
                capitalization = "N/A"
        else:
            capitalization = "N/A"

        # Charger les emojis
        try:
            with open("assets/emojis.json") as f:
                emojis = json.load(f)
                emoji = emojis.get(ticker, "")
        except FileNotFoundError:
            emoji = ""

        # EPS depuis data_earnings
        if data_earnings and "annualEarnings" in data_earnings and data_earnings["annualEarnings"]:
            latest_eps = data_earnings["annualEarnings"][0].get("reportedEPS", "N/A")
        else:
            latest_eps = "N/A"

        # Convertir rendement dividendes en %
        if dividend_yield not in ["N/A", None, ""]:
            try:
                dividend_yield = f"{float(dividend_yield) * 100:.2f}%"
            except:
                dividend_yield = "N/A"
        else:
            dividend_yield = "N/A"

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
                        html.P(sector if sector != "N/A" else "")
                    ]), className="d-flex align-items-center justify-content-center"),

                    dbc.Col(html.Div([
                        html.H6("Industrie", id="tooltip-industry", style={'textTransform': 'none'}),
                        html.P(industry if industry != "N/A" else "")
                    ]), className="d-flex align-items-center justify-content-center"),

                    dbc.Col(html.Div([
                        html.H6("Pays", id="tooltip-country", style={'textTransform': 'none'}),
                        html.P(country if country != "N/A" else "")
                    ]), className="d-flex align-items-center justify-content-center"),

                    dbc.Col(html.Div([
                        html.H6("Prix", style={'textTransform': 'none'}),
                        html.P(f"{current_price:.2f}$",  style={'fontSize': '1.5rem'}),
                        dbc.Badge(f"{variation:.2f}%", color=badge_color, className="mt-2")
                    ]), className="d-flex align-items-center justify-content-center")
                ], className="bg-light border rounded p-2 shadow-sm mb-2 mt-4"),
            ], fluid=True, className="text-center", style={'marginleft': 'auto', 'marginright': 'auto'}),

            # Deuxième container
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H6("Capitalisation Boursière", style={'textTransform': 'none'}),
                        html.P(capitalization if capitalization != "N/A" else "", className="fw-bold")
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.H6("Rendement des Dividendes", id="tooltip-dividend-yield", style={'textTransform': 'none'}),
                        html.P(dividend_yield if dividend_yield != "N/A" else "", className="fw-bold")
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.H6("PER (Price-to-Earnings Ratio)", id="tooltip-pe-ratio", style={'textTransform': 'none'}),
                        html.P(pe_ratio if pe_ratio != "N/A" else "", className="fw-bold")
                    ]), className="d-flex align-items-center justify-content-center"),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(html.Div([
                        html.H6("Beta", id="tooltip-beta", style={'textTransform': 'none'}),
                        html.P(beta if beta != "N/A" else "", className="fw-bold")
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.H6("Bénéfice par Action (EPS)", id="tooltip-eps", style={'textTransform': 'none'}),
                        html.P(latest_eps if latest_eps != "N/A" else "", className="fw-bold")
                    ]), className="d-flex align-items-center justify-content-center"),
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

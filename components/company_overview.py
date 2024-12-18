from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import json

def create_company_overview(data_overview, data_income, data_cashflow, data_earnings):
    """Crée un composant affichant les données principales de l'entreprise dans une grille avec tooltips."""

    try:
        if not data_overview or not data_income or not data_cashflow or not data_earnings:
            return html.Div("Données insuffisantes", style={'textAlign': 'center', 'marginTop': '20px'})

        # Extraire les informations nécessaires
        name = data_overview.get("Name", "N/A")
        ticker = data_overview.get("Symbol", "N/A")
        dividend_yield = data_overview.get("DividendYield", "N/A")
        pe_ratio = data_overview.get("PERatio", "N/A")
        beta = data_overview.get("Beta", "N/A")
        sector = data_overview.get("Sector", "N/A")
        industry = data_overview.get("Industry", "N/A")
        country = data_overview.get("Country", "N/A")
        exchange = data_overview.get("Exchange", "N/A")
        capitalization = data_overview.get("MarketCapitalization", "N/A") + " USD"
        #convertir la capitalisation boursière en milliards si elle est supérieure à 1 milliard sinon en trillions si elle est supérieure à 1 trillion sinon en millons
        if capitalization != "N/A":
            capitalization = float(capitalization.replace(" USD", ""))
            if capitalization >= 1_000_000_000_000:
                capitalization = f"{capitalization / 1_000_000_000_000:.2f} Trillion"
            elif capitalization >= 1_000_000_000:
                capitalization = f"{capitalization / 1_000_000_000:.2f} Billion"
            else:
                capitalization = f"{capitalization / 1_000_000:.2f} Million"

        # Chercher dans assets/emojis.json s'il y a un emoji pour le ticker de l'entreprise (possible de ne pas trouver)
        try:
            with open("assets/emojis.json") as f:
                emojis = json.load(f)
                emoji = emojis.get(ticker, "")
        except FileNotFoundError:
            emoji = ""

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


        # Créer une grille avec Dash Bootstrap Components et des tooltips
        return html.Div([
            # Premier container pour les informations principales : Nom, Ticker, Secteur, Industrie, Country, Exchange
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H1(emoji if emoji else "📈", style={'fontSize': '2.5rem'})
                    ]), width=12),
                    dbc.Col(html.Div([
                        html.H2(name),
                        html.P(ticker + " - " + exchange)
                    ]), width=4),
                    dbc.Col(html.Div([
                        html.H6("Secteur", id="tooltip-sector",style={'textTransform': 'none'}),
                        html.P(sector)
                    ])),
                    dbc.Col(html.Div([
                        html.H6("Industrie", id="tooltip-industry",style={'textTransform': 'none'}),
                        html.P(industry)
                    ])),
                    dbc.Col(html.Div([
                        html.H6("Pays", id="tooltip-country",style={'textTransform': 'none'}),
                        html.P(country)
                    ])),
                ], className="bg-light border rounded p-4 shadow-sm mb-4")
            ], fluid=True),

            # Deuxième container pour l'aperçu de l'entreprise
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H6("Capitalisation Boursière", style={'textTransform': 'none'}),
                        html.P(capitalization, className="fw-bold")
                    ]), width=3),
                    dbc.Col(html.Div([
                        html.H6("Rendement des Dividendes", id="tooltip-dividend-yield",style={'textTransform': 'none'}),
                        html.P(dividend_yield, className="fw-bold")
                    ]), width=3),
                    dbc.Col(html.Div([
                        html.H6("PER (Price-to-Earnings Ratio)", id="tooltip-pe-ratio",style={'textTransform': 'none'}),
                        html.P(pe_ratio, className="fw-bold")
                    ]), width=3),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(html.Div([
                        html.H6("Beta", id="tooltip-beta",style={'textTransform': 'none'}),
                        html.P(beta, className="fw-bold")
                    ]), width=4),
                    dbc.Col(html.Div([
                        html.H6("Bénéfice par Action (EPS)", id="tooltip-eps",style={'textTransform': 'none'}),
                        html.P(latest_eps, className="fw-bold")
                    ]), width=4),
                ])
            ], className="border rounded p-4 shadow-sm bg-light"),

            # Ajout des tooltips
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

from dash import html,dcc
import dash_bootstrap_components as dbc
from components.utils.overview_utils import *
from components.utils.stock_score import *

def create_company_overview(data_overview, data_income, data_cashflow, data_earnings):
    """Crée un composant affichant les données principales de l'entreprise dans une grille avec tooltips,
    même si certaines données sont manquantes, sans pandas."""

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

        # Calculer les CAGR du chiffre d'affaires et du bénéfice net
        cagr_ca = calculate_cagr_key(data_income, key="totalRevenue")
        cagr_benefice_net = calculate_cagr_key(data_income, key="netIncome")

        # Score de l'entreprise
        score = calculate_stock_score(cagr_ca, beta, pe_ratio, latest_eps, dividend_yield)

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
                        html.H6("Prix", id="tooltip-price", style={'textTransform': 'none'}),
                        html.P(f"{current_price:.2f}$",  style={'fontSize': '1.5rem'}, className="fw-bold mb-0"),
                        dbc.Badge(f"1Y: {variation:.2f}%", color=price_badge_color, className="mt-2")
                    ]), className="d-flex align-items-center justify-content-center")
                ], className="bg-light border rounded p-2 shadow-sm mb-2 mt-4"),
            ], fluid=True, className="text-center", style={'marginleft': 'auto', 'marginright': 'auto'}),

            # Deuxième container
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.P("MarketCap", id="tooltip-market-cap", style={'textTransform': 'none', 'color': 'rgb(127, 121, 178)'}, className="fw-bold mb-0"),
                        html.H5(format_market_cap(capitalization) if format_market_cap(capitalization) != "N/A" else "", className="fw-bold mb-0"),
                        # Ajouter un badge pour la capitalisation boursière get_market_cap_badge_info(capitalization), retourn  un tuple (text,color)
                        dbc.Badge(get_marketcap_badge_info(capitalization)[0], color=get_marketcap_badge_info(capitalization)[1])
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.P("CAGR CA (5Y)", id="tooltip-cagr-ca", style={'textTransform': 'none', 'color': 'rgb(127, 121, 178)'},className="fw-bold mb-0"),
                        html.H5(cagr_ca, className="fw-bold mb-0"),
                        dbc.Badge("> 5%", color=get_cagr_ca_badge_color(cagr_ca))
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.P("CAGR B. net", id="tooltip-cagr-net-income", style={'textTransform': 'none', 'color': 'rgb(127, 121, 178)'},className="fw-bold mb-0"),
                        html.H5(cagr_benefice_net, className="fw-bold mb-0"),
                        dbc.Badge("> 0%", color="secondary")
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.P("P/E Ratio", id="tooltip-pe-ratio", style={'textTransform': 'none', 'color': 'rgb(127, 121, 178)'},className="fw-bold mb-0"),
                        html.H5(pe_ratio if pe_ratio != "N/A" else "", className="fw-bold mb-0"),
                        dbc.Badge("< 30", color=get_pe_ratio_badge_color(pe_ratio))
                    ]), className="d-flex align-items-center justify-content-center"),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(html.Div([
                        html.H6("Beta", id="tooltip-beta", style={'textTransform': 'none', 'color': 'rgb(127, 121, 178)'},className="fw-bold mb-0"),
                        html.P(beta if beta != "N/A" else "", className="fw-bold mb-0"),
                        dbc.Badge("> 1", color=get_beta_badge_color(beta))
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.H6("EPS", id="tooltip-eps", style={'textTransform': 'none', 'color': 'rgb(127, 121, 178)'},className="fw-bold mb-0"),
                        html.P(latest_eps if latest_eps != "N/A" else "", className="fw-bold mb-0"),
                        dbc.Badge("> 1", color=get_eps_badge_color(latest_eps))
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div([
                        html.H6("Dividendes", id="tooltip-dividend-yield", style={'textTransform': 'none', 'color': 'rgb(127, 121, 178)'},className="fw-bold mb-0"),
                        html.P(dividend_to_percent(dividend_yield) if dividend_to_percent(dividend_yield) != "N/A" else "", className="fw-bold mb-0"),
                        dbc.Badge("< 2%", color=get_dividend_yield_badge_color(dividend_yield))
                    ]), className="d-flex align-items-center justify-content-center"),
                    dbc.Col(html.Div(
                        [
                            html.H6(
                                "Score",  # Le label en plus petit
                                style={"fontSize": "1rem", "marginTop": "5px", "textAlign": "center", 'color': 'rgb(127, 121, 178)'}  # Taille réduite et centré
                            ),
                            dbc.Badge(
                                f"{score}",  # Le score en grand
                                color=get_score_badge_color(score),
                                className="fw-bold", id="tooltip-score",
                                style={"fontSize": "1.5rem", "padding": "10px 20px"}  # Grande taille pour le score
                            )
                        ],
                        style={"textAlign": "center"}  # Centrer le tout
                    )
                    )
                ]),
            ], fluid=True, className="border rounded p-4 shadow-sm bg-light mb-4", style={'marginleft': 'auto', 'marginright': 'auto'}),

            # Tooltips
            dbc.Tooltip("Le secteur d'activité de l'entreprise.", target="tooltip-sector", placement="top"),
            dbc.Tooltip("L'industrie précise au sein du secteur.", target="tooltip-industry", placement="top"),
            dbc.Tooltip("Le pays où l'entreprise est basée.", target="tooltip-country", placement="top"),
            dbc.Tooltip("Pourcentage des profits distribués sous forme de dividendes.", target="tooltip-dividend-yield", placement="right"),
            dbc.Tooltip("Le ratio entre le prix de l'action et le bénéfice par action.", target="tooltip-pe-ratio", placement="right"),
            dbc.Tooltip("Mesure de la volatilité de l'action par rapport au marché.", target="tooltip-beta", placement="bottom"),
            dbc.Tooltip(
                dcc.Markdown(
                    """
                    L'EPS mesure le bénéfice net par action en USD d'une entreprise.
                    - **Technologie** : >10  
                    - **Énergie** : >10  
                    - **Conso.Disc.** : 5-15  
                    - **Industrie** : 5-15 
                    - **Finance** : 8-15  
                    - **Santé** : 5-10
                    """
                ),
                target="tooltip-eps",
                placement="bottom",
            ),
            dbc.Tooltip("Le taux de croissance annuel composé du chiffre d'affaires.", target="tooltip-cagr-ca", placement="top"),
            dbc.Tooltip("Le taux de croissance annuel composé du bénéfice net.", target="tooltip-cagr-net-income", placement="top"),
            dbc.Tooltip("le nombre total d'actions multiplié par le prix de l'action, indiquant la taille de l'entreprise.", target="tooltip-market-cap", placement="top"),
            dbc.Tooltip("Le prix actuel de l'action.", target="tooltip-price", placement="top"),
            dbc.Tooltip(dcc.Markdown(
                    """
                    ### Score éxperimental
                    -----------------
                    Ce score est donné à titre indicatif. 
                    Il est calculé en fonction de plusieurs critères et se calcule sur 10.
                    """
                ), target="tooltip-score", placement="top"),
        ])
    except Exception as e:
        print(f"Erreur de création de l'aperçu de l'entreprise : {e}")
        return html.Div("Erreur de création de l'aperçu de l'entreprise", style={'textAlign': 'center', 'marginTop': '20px'})

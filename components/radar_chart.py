from dash import html,dcc
import dash_bootstrap_components as dbc
from components.utils.overview_utils import *
from components.utils.stock_score import *


def create_radar_chart(data_overview, data_income, data_earnings):
    """Crée un graphique radar pour les scores des actions."""
    try:
        # Si les données sont manquantes, on remplace par "N/A" au lieu de stopper l'affichage.
        name,dividend_yield,pe_ratio,beta,exchange,capitalization = extract_company_score_data(data_overview)

        # Dernier EPS depuis data_earnings
        latest_eps = get_latest_eps(data_earnings)

        # Calculer les CAGR du chiffre d'affaires et du bénéfice net
        cagr_ca = calculate_cagr_key(data_income, key="totalRevenue")

        # Score de l'entreprise
        score = calculate_stock_score(cagr_ca, beta, pe_ratio, latest_eps, dividend_yield, True)

        return score
    except Exception as e:
        print(f"Error in create company overview: {e}")
        return [{}]

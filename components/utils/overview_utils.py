import json

# Fonction pour obtenir la couleur du badge pour le EPS (Vert si supérieur à 10; sinon gris)
def get_eps_badge_color(eps):
    try:
        eps_value = float(eps) if eps != "N/A" else 0
        eps_badge_color = "success" if eps_value > 10 else "secondary"
    except ValueError:
        eps_badge_color = "secondary"
    return eps_badge_color

# Fonction pour obtenir la couleur du badge pour le CAGR CA (Vert si supérieur à 5%, rouge si inférieur à 1%)
def get_cagr_ca_badge_color(cagr_ca):
    try:
        cagr_ca_value = float(cagr_ca.replace("%", "")) if cagr_ca != "N/A" else 0
        if cagr_ca_value > 5:
            cagr_ca_badge_color = "success"
        elif cagr_ca_value < 1:
            cagr_ca_badge_color = "danger"
        else:
            cagr_ca_badge_color = "secondary"
    except ValueError:
        cagr_ca_badge_color = "secondary"
    return cagr_ca_badge_color

# Fonction pour obtenir la couleur du badge pour le PER (Orange si inférieur à 20, vert si entre 20 et 30, rouge si supérieur à 30)
def get_pe_ratio_badge_color(pe_ratio):
    try:
        pe_ratio_value = float(pe_ratio) if pe_ratio != "N/A" else 0
        if pe_ratio_value < 20:
            pe_ratio_badge_color = "warning"
        elif pe_ratio_value > 30:
            pe_ratio_badge_color = "danger"
        else:
            pe_ratio_badge_color = "success"
    except ValueError:
        pe_ratio_badge_color = "secondary"
    return pe_ratio_badge_color

# Fonction pour obtenir la couleur du badge pour le dividende
def get_dividend_yield_badge_color(dividend_yield):
    if dividend_yield not in ["N/A", None, ""]:
        try:
            dividend_yield_value = float(dividend_yield.replace("%", "")) / 100
            if dividend_yield_value < 0.01:
                dividend_yield_badge_color = "success"
            elif dividend_yield_value > 0.02:
                dividend_yield_badge_color = "danger"
            else:
                dividend_yield_badge_color = "secondary"
        except ValueError:
            dividend_yield_badge_color = "secondary"
    else:
        dividend_yield_badge_color = "secondary"
    return dividend_yield_badge_color

# Fonction pour obtenir la couleur du badge pour le beta
def get_beta_badge_color(beta):
    try:
        beta_badge_color = "success" if beta != "N/A" and float(beta) > 1 else "secondary"
    except (ValueError, TypeError):
        beta_badge_color = "secondary"
    return beta_badge_color

# Fonction pour récuperer le prix de clôture d'un ticker
def fetch_last_price(ticker: str):
    from datetime import datetime, timedelta
    import yfinance as yf
    """
    Récupère le dernier prix de clôture et le prix de clôture il y a un an pour un ticker donné.
    """
    if not isinstance(ticker, str):
        raise ValueError("Le ticker doit être une chaîne de caractères.")

    try:
        # Récupération des données pour le dernier jour
        ticker_data = yf.Ticker(ticker)
        data = ticker_data.history(period='1d')
        
        # Vérification que les données ne sont pas vides
        if not data.empty:
            last_close_price = data['Close'].values[-1]
        else:
            raise ValueError(f"Aucune donnée disponible pour le ticker '{ticker}'.")
        
        # Déterminer la plage de temps pour l'année précédente
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Récupération des données pour l'année précédente
        data_year_ago = ticker_data.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        
        # Vérification que les données pour l'année précédente ne sont pas vides
        if not data_year_ago.empty:
            close_price_year_ago = data_year_ago['Close'].values[0]
        else:
            raise ValueError(f"Aucune donnée disponible pour le ticker '{ticker}' il y a un an.")

        return last_close_price, close_price_year_ago

    except Exception as e:
        print(f"Erreur lors de la récupération des prix pour le ticker '{ticker}': {e}")
        return 0, 0

# Fonction pour extraire les données principales de l'entreprise
def extract_company_data(data_overview):
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
    dividend_yield = data_overview.get("DividendYield", "N/A") if data_overview else "N/A"

    # essayer de ne garder que les 16 premiers caractères de l'industrie
    if len(industry) > 16:
        industry = industry[:16] + "..."
    if len(sector) > 16:
        sector = sector[:16] + "..."
    if len(name) > 16:
        name = name[:16] + "..."
        # Remplace le pays si USA
    if country == "USA":
        country = "USA 🦅"
    return name,ticker,dividend_yield,pe_ratio,beta,sector,industry,country,exchange,capitalization

# Fonction pour calculer la variation du prix
def calculate_price_variation(current_price, last_price_year_ago):
    if current_price is not None and last_price_year_ago is not None and last_price_year_ago != 0:
        variation = ((current_price - last_price_year_ago) / last_price_year_ago) * 100
        price_badge_color = "success" if variation >= 0 else "secondary"
    else:
        variation = 0
        price_badge_color = "secondary"
        if current_price is None:
            current_price = 0.0
    return current_price,variation,price_badge_color

# Fonction pour obtenir le dernier EPS
def get_latest_eps(data_earnings):
    if data_earnings and "annualEarnings" in data_earnings and data_earnings["annualEarnings"]:
        latest_eps = data_earnings["annualEarnings"][0].get("reportedEPS", "N/A")
    else:
        latest_eps = "N/A"
    return latest_eps

# Fonction pour obtenir l'emoji d'un ticker
def get_emoji_by_ticker(ticker):
    try:
        with open("assets/emojis.json") as f:
            emojis = json.load(f)
            emoji = emojis.get(ticker, "")
    except FileNotFoundError:
        emoji = ""
    return emoji

# Fonction pour formater la capitalisation boursière
def format_market_cap(capitalization):
    if capitalization not in ["N/A", None, ""]:
        try:
            cap_val = float(capitalization)
            if cap_val >= 1_000_000_000_000:
                capitalization = f"{cap_val / 1_000_000_000_000:.2f} T"
            elif cap_val >= 1_000_000_000:
                capitalization = f"{cap_val / 1_000_000_000:.2f} B"
            else:
                capitalization = f"{cap_val / 1_000_000:.2f} M"
        except:
            capitalization = "N/A"
    else:
        capitalization = "N/A"
    return capitalization

# Fonction pour convertir le dividende en pourcentage
def dividend_to_percent(dividend_yield):
    if dividend_yield not in ["N/A", None, ""]:
        try:
            dividend_yield = f"{float(dividend_yield) * 100:.2f}%"
        except:
            dividend_yield = "N/A"
    else:
        dividend_yield = "N/A"
    return dividend_yield

def calculate_cagr_key(data, key):
    """
    Calcule le CAGR (Compound Annual Growth Rate) pour une clé spécifique dans les données.
    
    Arguments :
    - data : dictionnaire contenant les rapports annuels.
    - key : clé pour laquelle calculer le CAGR (par exemple "totalRevenue" ou "netIncome").
    
    Retourne :
    - CAGR en pourcentage sous forme de chaîne ou "N/A" si les données sont insuffisantes.
    """
    try:
        # Extraire les valeurs de la clé spécifiée
        annual_reports = data.get("annualReports", [])
        values = [
            float(report.get(key, 0)) for report in annual_reports if key in report and report.get(key, None) is not None
        ]

        # Vérifier qu'il y a au moins deux valeurs pour calculer le CAGR
        if len(values) >= 2:
            start_value = values[-1]  # Première année (la plus ancienne)
            end_value = values[0]    # Dernière année (la plus récente)
            n_years = len(values) - 1

            if start_value > 0:  # Éviter les divisions par zéro
                cagr = ((end_value / start_value) ** (1 / n_years) - 1) * 100
                return f"{cagr:.2f}%"
        
        # Retourner "N/A" si les données sont insuffisantes ou invalide
        return "N/A"
    except Exception as e:
        print(f"Erreur lors du calcul du CAGR pour la clé {key} : {e}")
        return "N/A"

# Fonction pour obtenir la couleur du badge pour la capitalisation boursière 
def get_marketcap_badge_info(capitalization):
    # retourner le type de taille de la capitalisation boursière (small, medium, large) en fonction de la valeur ainsi qu'une couleur associée
    try:
        cap_val = float(capitalization)
        if cap_val < 1_000_000_000:
            marketcap_type = "Small-cap"
            marketcap_badge_color = "success"
        elif cap_val < 10_000_000_000:
            marketcap_type = "Mid-cap"
            marketcap_badge_color = "warning"
        elif cap_val >= 1_000_000_000_000:
            marketcap_type = "Mega-cap 🚀"
            marketcap_badge_color = "secondary"
        else:
            marketcap_type = "Large-cap"
            marketcap_badge_color = "secondary"
    except:
        marketcap_type = "N/A"
        marketcap_badge_color = "secondary"
    return marketcap_type, marketcap_badge_color


def get_score_badge_color(score):
    # > 8 : vert foncé, 6-8 : vert clair, 4-6 : jaune, 2-4 : orange, < 2 : rouge
    try:
        score_value = float(score)
        if score_value > 8:
            score_badge_color = "success"
        elif score_value > 6:
            score_badge_color = "info"
        elif score_value > 4:
            score_badge_color = "warning"
        elif score_value > 2:
            score_badge_color = "danger"
        else:
            score_badge_color = "secondary"
    except:
        score_badge_color = "secondary"
    return score_badge_color


def extract_company_score_data(data_overview):
    name = data_overview.get("Name", "N/A") if data_overview else "N/A"
    dividend_yield = data_overview.get("DividendYield", "N/A") if data_overview else "N/A"
    pe_ratio = data_overview.get("PERatio", "N/A") if data_overview else "N/A"
    beta = data_overview.get("Beta", "N/A") if data_overview else "N/A"
    exchange = data_overview.get("Exchange", "N/A") if data_overview else "N/A"
    capitalization = data_overview.get("MarketCapitalization", "N/A") if data_overview else "N/A"


    return name,dividend_yield,pe_ratio,beta,exchange,capitalization

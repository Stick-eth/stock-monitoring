
import json

# Fonction pour calculer le CAGR (Compound Annual Growth Rate) du chiffre d'affaires et du bénéfice net
def calculate_cagr(data, period=5):
    import pandas as pd
    """Calcule le CAGR du chiffre d'affaires et du bénéfice net sur une période donnée.

    Paramètres :
    - data : dict contenant les rapports financiers avec "totalRevenue" et "netIncome".
    - period : nombre d'années pour le calcul du CAGR (par défaut : 5).

    Retourne :
    - Un dictionnaire avec les CAGR pour le CA et le bénéfice net.
    """
    try:
        if not data:
            return {"CAGR_CA": "N/A", "CAGR_Benefice": "N/A"}

        # Convertir les données en DataFrame
        df = pd.DataFrame(data.get("annualReports", []))
        df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], utc=True)
        df["totalRevenue"] = pd.to_numeric(df["totalRevenue"], errors='coerce')
        df["netIncome"] = pd.to_numeric(df["netIncome"], errors='coerce')

        # Trier par date décroissante pour s'assurer que les dernières années sont en haut
        df.sort_values("fiscalDateEnding", ascending=False, inplace=True)

        # Sélectionner les données sur la période spécifiée
        if len(df) < period:
            return ["N/A","N/A"]
        
        # Valeurs initiales et finales
        revenue_initial = df["totalRevenue"].iloc[period - 1]
        revenue_final = df["totalRevenue"].iloc[0]

        net_income_initial = df["netIncome"].iloc[period - 1]
        net_income_final = df["netIncome"].iloc[0]

        # Calcul du CAGR pour le CA
        if revenue_initial > 0 and revenue_final > 0:
            cagr_revenue = ((revenue_final / revenue_initial) ** (1 / period) - 1) * 100
        else:
            cagr_revenue = "N/A"

        # Calcul du CAGR pour le bénéfice net
        if net_income_initial > 0 and net_income_final > 0:
            cagr_net_income = ((net_income_final / net_income_initial) ** (1 / period) - 1) * 100
        else:
            cagr_net_income = "N/A"
        cagr_ca = f"{cagr_revenue:.2f}%" if cagr_revenue != "N/A" else "N/A"
        cagr_benefice = f"{cagr_net_income:.2f}%" if cagr_net_income != "N/A" else "N/A"

        return [cagr_ca,cagr_benefice]        
    except Exception as e:
        print(f"Erreur lors du calcul du CAGR : {e}")
        return ["N/A","N/A"]

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
    import pandas as pd
    import yfinance as yf
    if not isinstance(ticker, str):
        raise ValueError("Le ticker doit être une chaîne de caractères.")
    try:
        # Récupération des données pour le dernier jour
        data = yf.Ticker(ticker).history(period='1d')
        
        # Vérification que le DataFrame n'est pas vide
        if data.empty:
            raise ValueError(f"Aucune donnée disponible pour le ticker '{ticker}'.")
        
        # Récupération des données pour l'année précédente
        data_year_ago = yf.Ticker(ticker).history(start=(pd.Timestamp.now() - pd.to_timedelta(365, unit='d')).strftime('%Y-%m-%d'), end=pd.Timestamp.now().strftime('%Y-%m-%d'))
        
        # Vérification que le DataFrame n'est pas vide
        if data_year_ago.empty:
            raise ValueError(f"Aucune donnée disponible pour le ticker '{ticker}' il y a un an.")
        
        # Retourne le dernier prix de clôture et le prix de clôture un an plus tôt
        return data['Close'].iloc[-1], data_year_ago['Close'].iloc[0]
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
        # Remplace le pays si USA
    if country == "USA":
        country = "United States 🦅"
    return name,ticker,dividend_yield,pe_ratio,beta,sector,industry,country,exchange,capitalization

# Fonction pour calculer la variation du prix
def calculate_price_variation(current_price, last_price_year_ago):
    if current_price is not None and last_price_year_ago is not None and last_price_year_ago != 0:
        variation = ((current_price - last_price_year_ago) / last_price_year_ago) * 100
        price_badge_color = "success" if variation >= 0 else "danger"
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
                capitalization = f"{cap_val / 1_000_000_000_000:.2f} Trillion"
            elif cap_val >= 1_000_000_000:
                capitalization = f"{cap_val / 1_000_000_000:.2f} Billion"
            else:
                capitalization = f"{cap_val / 1_000_000:.2f} Million"
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





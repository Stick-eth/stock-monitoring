import yfinance as yf
from datetime import datetime, timedelta

def fetch_last_price(ticker: str):
    """
    Récupère le dernier prix de clôture et le prix de clôture il y a un an pour un ticker donné.

    :param ticker: Le symbole de l'action (par exemple 'AAPL').
    :return: Tuple contenant le dernier prix de clôture et le prix de clôture un an plus tôt.
    """
    if not isinstance(ticker, str):
        raise ValueError("Le ticker doit être une chaîne de caractères.")
    
    # Récupération des données pour le dernier jour
    ticker_data = yf.Ticker(ticker)
    data = ticker_data.history(period='1d')
    
    # Vérification que les données ne sont pas vides
    if data.empty:
        raise ValueError(f"Aucune donnée disponible pour le ticker '{ticker}'.")
    
    # Dernier prix de clôture
    last_close_price = data['Close'].iloc[-1]

    # Définir la plage de dates pour il y a un an
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Récupération des données pour l'année précédente
    data_year_ago = ticker_data.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    
    # Vérification que les données pour l'année précédente ne sont pas vides
    if data_year_ago.empty:
        raise ValueError(f"Aucune donnée disponible pour le ticker '{ticker}' il y a un an.")
    
    # Prix de clôture un an plus tôt
    price_year_ago = data_year_ago['Close'].iloc[0]

    return last_close_price, price_year_ago

import pandas as pd
import yfinance as yf

def fetch_last_price(ticker: str):
    if not isinstance(ticker, str):
        raise ValueError("Le ticker doit être une chaîne de caractères.")
    
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

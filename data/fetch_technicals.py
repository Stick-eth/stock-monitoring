import yfinance as yf
import os
import json
import pandas as pd

# Liste des tickers
tickers = ['MA', 'V', 'MSFT', 'AAPL', 'TSLA', 'ACN', 'SPGI', 'COST', 'BKNG']

# Chemin du dossier principal (le script se trouve déjà dans 'data')
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Sous-dossiers pour les types de données
SUBFOLDERS = {
    'prices': 'PRICES',
    'insider_transactions': 'INSIDERS_TX'
}

# Fonction pour créer les sous-dossiers
def create_directories():
    for folder in SUBFOLDERS.values():
        os.makedirs(os.path.join(DATA_DIR, folder), exist_ok=True)

# Fonction pour sauvegarder les données en JSON
def save_to_json(data, folder, ticker):
    file_path = os.path.join(DATA_DIR, folder, f"{ticker}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"{ticker} {folder} saved to {file_path}")

# Fonction pour récupérer et sauvegarder l'historique complet des prix
def fetch_prices(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="max")  # Récupérer l'historique complet des prix
        hist.reset_index(inplace=True)
        # Convertir les Timestamps en chaînes de caractères
        hist['Date'] = hist['Date'].astype(str)
        # Convertir les colonnes numériques en type 'object' avant de remplacer les NaN
        for col in hist.columns:
            if hist[col].dtype in ['float64', 'int64']:
                hist[col] = hist[col].astype(object)
        # Remplacer les NaN par "NaN"
        hist.fillna("NaN", inplace=True)
        data = hist.to_dict(orient="records")
        save_to_json(data, SUBFOLDERS['prices'], ticker)
    except Exception as e:
        print(f"Error fetching prices for {ticker}: {e}")

# Fonction pour récupérer et sauvegarder les transactions d'initiés
def fetch_insider_transactions(ticker):
    try:
        stock = yf.Ticker(ticker)
        insider = stock.insider_transactions

        if insider is not None and not insider.empty:
            # Convertir toutes les colonnes de type Timestamp en chaînes de caractères
            for col in insider.select_dtypes(include=['datetime64']).columns:
                insider[col] = insider[col].astype(str)
            # Convertir les colonnes numériques en type 'object' avant de remplacer les NaN
            for col in insider.columns:
                if insider[col].dtype in ['float64', 'int64']:
                    insider[col] = insider[col].astype(object)
            # Remplacer les NaN par "NaN"
            insider.fillna("NaN", inplace=True)
            data = insider.to_dict(orient="records")
        else:
            data = []

        save_to_json(data, SUBFOLDERS['insider_transactions'], ticker)

    except Exception as e:
        print(f"Error fetching insider transactions for {ticker}: {e}")

# Fonction principale pour récupérer toutes les données
def fetch_all_data():
    create_directories()
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        fetch_prices(ticker)
        fetch_insider_transactions(ticker)

# Exécution du script
if __name__ == "__main__":
    fetch_all_data()

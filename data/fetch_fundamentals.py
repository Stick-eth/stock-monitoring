import requests
import os
from dotenv import load_dotenv

# Charger les variables depuis le fichier .env
load_dotenv()

# Configuration
api_key = os.getenv("API_KEY")
tickers = ['MA', 'V', 'MSFT', 'AAPL', 'TSLA', 'ACN', 'SPGI', 'COST', 'BKNG']
functions = ['BALANCE_SHEET', 'INCOME_STATEMENT', 'OVERVIEW']

# Chemin du dossier principal (le script se trouve déjà dans 'data')
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def get_data(ticker, function):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données pour {ticker} ({function}): {e}")
        return None

# Boucle pour récupérer les données
for ticker in tickers:
    for function in functions:
        data = get_data(ticker, function)
        if data:
            # Créer le dossier si nécessaire
            function_dir = os.path.join(DATA_DIR, function)
            os.makedirs(function_dir, exist_ok=True)
            
            # Écrire les données dans un fichier JSON
            file_path = os.path.join(function_dir, f"{ticker}.json")
            with open(file_path, 'w') as f:
                f.write(data)
            print(f'{ticker} {function} done')

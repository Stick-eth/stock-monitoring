import requests
import os
from dotenv import load_dotenv

# Charger les variables depuis le fichier .env
load_dotenv()

# Configuration
api_key = os.getenv("API_KEY")
tickers = ['MA', 'V', 'MSFT', 'AAPL', 'TSLA', 'ACN', 'SPGI', 'COST', 'BKNG']
functions = ['BALANCE_SHEET', 'INCOME_STATEMENT', 'OVERVIEW']

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
            os.makedirs(f'./data', exist_ok=True)
            os.makedirs(f'./data/{function}', exist_ok=True)
            # Écrire les données dans un fichier JSON
            with open(f'./data/{function}/{ticker}.json', 'w') as f:
                f.write(data)
            print(f'{ticker} {function} done')
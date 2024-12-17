import os
import json

# Dossiers des fichiers JSON
DATA_DIRS = {
    "BALANCE_SHEET": "./data/BALANCE_SHEET",
    "INCOME_STATEMENT": "./data/INCOME_STATEMENT",
    "OVERVIEW": "./data/OVERVIEW",
    "PRICES": "./data/PRICES",
    "INSIDERS_TX": "./data/INSIDERS_TX"
}

def load_data(ticker):
    """Charge les données JSON d'un ticker."""
    try:
        data = {}
        for key, dir_path in DATA_DIRS.items():
            with open(os.path.join(dir_path, f"{ticker}.json")) as f:
                data[key] = json.load(f)
        return data
    except Exception as e:
        print(f"Erreur de chargement pour {ticker} : {e}")
        return {}

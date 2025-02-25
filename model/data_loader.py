import os
from dotenv import load_dotenv
from pymongo import MongoClient
from components.utils.cache_config import cache
import time

DATA_DIRS = {
    "BALANCE_SHEET": "./data/BALANCE_SHEET",
    "INCOME_STATEMENT": "./data/INCOME_STATEMENT",
    "OVERVIEW": "./data/OVERVIEW",
    "PRICES": "./data/PRICES",
    "INSIDERS_TX": "./data/INSIDERS_TX",
    "CASH_FLOW": "./data/CASH_FLOW",
    "EARNINGS": "./data/EARNINGS",
    "DIVIDENDS": "./data/DIVIDENDS",
}

@cache.memoize(timeout=86400)
def load_data(ticker):
    time.sleep(0.15) # DDOS protection du pauvre
    """
    Charge les données d'un ticker depuis MongoDB (ou depuis les fichiers, selon l'implémentation).
    Retourne un dict ayant les mêmes clés que DATA_DIRS.
    Ignore le ticker s'il est None, 'N/A' ou vide.
    """
    # Si le ticker est None, 'N/A' ou vide, on ne fait rien :
    if not ticker or ticker.strip().upper() == 'N/A':
        print(f"load_data: Ticker invalide '{ticker}'. Aucune donnée ne sera chargée.")
        return {}

    # -- Connexion Mongo : vous pouvez garder la logique existante. --
    try:
        load_dotenv()
        MONGO_URI = os.getenv("MONGO_URI")
        DB_STOCKS = os.getenv("DB_NAME_STOCKS")

        client = MongoClient(MONGO_URI)
        db = client[DB_STOCKS]

        data = {}
        for key in DATA_DIRS:
            doc = db[ticker].find_one({"function": key})
            if doc and "data" in doc:
                data[key] = doc["data"]
            else:
                data[key] = {}
        return data

    except Exception as e:
        print(f"Erreur de chargement pour {ticker} : {e}")
        return {}

import os
import json
import requests
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient

# Chargement des variables d'environnement
load_dotenv()

# Variables d'environnement
API_KEY = os.getenv("API_KEY")      # Clé AlphaVantage
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Fonctions pour Alpha Vantage
AV_FUNCTIONS = [
    'BALANCE_SHEET',
    'INCOME_STATEMENT',
    'OVERVIEW',
    'CASH_FLOW',
    'DIVIDENDS',
    'EARNINGS'
]

################################
#           UTILS MONGO
################################

def last_fetch_date(ticker, function_name):
    """
    Récupère la date du dernier fetch pour un ticker et une fonction donnés,
    ou None s'il n'y a pas encore de document correspondant en base.
    """
    collection = db[ticker]
    doc = collection.find_one(
        {"function": function_name},
        sort=[("fetched_at", -1)]  # Le plus récent en premier
    )
    if doc and "fetched_at" in doc:
        return doc["fetched_at"]
    return None

def needs_fetch(ticker, function_name, force=False):
    """
    Détermine s'il faut refaire la récupération des données pour un ticker/fonction.
    - force=True : on ignore la règle des 30 jours
    - sinon, on compare la date du dernier fetch avec 30 jours
    """
    if force:
        return True
    fetched_at = last_fetch_date(ticker, function_name)
    if not fetched_at:
        return True
    now = datetime.utcnow()
    delta = now - fetched_at
    return delta > timedelta(days=30)

def save_data_to_mongo(ticker, function_name, data):
    """
    Insère/Met à jour les données dans MongoDB dans la collection du ticker.
    Supprime l'ancien document correspondant à (function_name) avant l'insertion.
    
    Document inséré :
    {
       "function": <function_name>,
       "data": <data>,
       "fetched_at": <datetime.utcnow()>
    }
    """
    collection = db[ticker]
    collection.delete_many({"function": function_name})
    document = {
        "function": function_name,
        "data": data,
        "fetched_at": datetime.utcnow()
    }
    result = collection.insert_one(document)
    print(f"✓ Insertion réussie pour {ticker} ({function_name}), ID : {result.inserted_id}")

################################
#        ALPHA VANTAGE
################################

def get_data_from_alpha_vantage(ticker, function_name):
    """
    Récupère les données brutes depuis l'API Alpha Vantage pour un ticker et une fonction donnés.
    Retourne la chaîne JSON brute si tout se passe bien, None sinon.
    """
    url = (
        f'https://www.alphavantage.co/query?function={function_name}'
        f'&symbol={ticker}&apikey={API_KEY}'
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text  # Données brutes (JSON sous forme de chaîne)
    except requests.exceptions.RequestException as e:
        print(f"[AlphaVantage] Erreur lors de la récupération de {ticker} ({function_name}) : {e}")
        return None
    
def fetch_alpha_vantage(ticker, force=False):
    for fn in AV_FUNCTIONS:
        if needs_fetch(ticker, fn, force):
            raw_data = get_data_from_alpha_vantage(ticker, fn)
            if raw_data:
                try:
                    json_data = json.loads(raw_data)
                except json.JSONDecodeError as e:
                    print(f"Impossible de parser en JSON pour {ticker} ({fn}) : {e}")
                    continue

                # Vérification : si l’API signale une limite ou renvoie un message d’erreur,
                # on détecte généralement "Note" ou "Information" dans la réponse
                if "Note" in json_data or "Information" in json_data:
                    print(
                        f"[AlphaVantage] Limite atteinte ou aucune donnée pour {ticker} ({fn}) : "
                        f"{json_data.get('Note') or json_data.get('Information')}"
                    )
                    # Ne pas sauvegarder
                    continue
               
                # Sinon on sauvegarde
                save_data_to_mongo(ticker, fn, json_data)
            else:
                print(f"[AlphaVantage] Aucune donnée brute récupérée pour {ticker} ({fn}).")
        else:
            print(f"[AlphaVantage] Pas de fetch (dernier <30j) pour {ticker} ({fn}).")



################################
#        YAHOO FINANCE
################################

def fetch_prices(ticker):
    """
    Récupère l'historique complet des prix sur Yahoo Finance (yfinance)
    et ne conserve que la Date et le Close.
    Retourne une liste de dictionnaires (records).
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="max")
        hist.reset_index(inplace=True)

        # Ne garder que 'Date' et 'Close'
        hist = hist[['Date', 'Close']]

        # Convertir Date en string
        hist['Date'] = hist['Date'].astype(str)

        # Convertir 'Close' en object pour pouvoir remplacer NaN par "NaN"
        hist['Close'] = hist['Close'].astype(object)
        hist.fillna("NaN", inplace=True)

        data = hist.to_dict(orient="records")
        return data
    except Exception as e:
        print(f"[YahooFinance] Erreur fetch_prices pour {ticker} : {e}")
        return []

def fetch_insider_transactions(ticker):
    """
    Récupère les transactions d'initiés sur Yahoo Finance via yfinance.
    Retourne une liste de dictionnaires (records).
    """
    try:
        stock = yf.Ticker(ticker)
        insider = stock.insider_transactions

        if insider is not None and not insider.empty:
            # Convertir les dates en string
            for col in insider.select_dtypes(include=['datetime64']).columns:
                insider[col] = insider[col].astype(str)

            # Convertir les colonnes numériques en 'object' et remplacer NaN
            for col in insider.columns:
                if insider[col].dtype in ['float64', 'int64']:
                    insider[col] = insider[col].astype(object)
            insider.fillna("NaN", inplace=True)

            data = insider.to_dict(orient="records")
        else:
            data = []
        return data

    except Exception as e:
        print(f"[YahooFinance] Erreur fetch_insider_transactions pour {ticker} : {e}")
        return []

def fetch_yahoo_finance(ticker, force=False):
    """
    Récupère les données Yahoo Finance (PRICES, INSIDERS_TX) pour le ticker,
    si besoin (ou si force=True).
    """
    # PRICES
    if needs_fetch(ticker, "PRICES", force):
        prices_data = fetch_prices(ticker)
        if prices_data:
            save_data_to_mongo(ticker, "PRICES", prices_data)
        else:
            print(f"[YahooFinance] Aucune donnée de prix pour {ticker}")
    else:
        print(f"[YahooFinance] Pas de fetch (dernier <30j) pour {ticker} (PRICES).")

    # INSIDERS_TX
    if needs_fetch(ticker, "INSIDERS_TX", force):
        insider_data = fetch_insider_transactions(ticker)
        if insider_data:
            save_data_to_mongo(ticker, "INSIDERS_TX", insider_data)
        else:
            print(f"[YahooFinance] Aucune transaction d'initiés pour {ticker}")
    else:
        print(f"[YahooFinance] Pas de fetch (dernier <30j) pour {ticker} (INSIDERS_TX).")

################################
#        FONCTION PRINCIPALE
################################

def get_ticker(ticker, force=False):
    """
    Récupère les données d'Alpha Vantage (fonctions financières) et de YahooFinance
    (PRICES, INSIDERS_TX) pour le ticker donné.
    
    :param ticker: Symbole à récupérer (ex: "AAPL")
    :param force: Si True, force la récupération même si <30j depuis le dernier fetch
    """
    try :
        # 1) Alpha Vantage
        fetch_alpha_vantage(ticker, force=force)
        # 2) Yahoo Finance
        fetch_yahoo_finance(ticker, force=force)
        return True
    except Exception as e:
        print(f"Erreur dans get_ticker({ticker}): {e}")
        return False


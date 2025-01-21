import os
from dotenv import load_dotenv
from pymongo import MongoClient

def format_market_cap(value):
    """Formate la capitalisation boursière en milliards/trillions."""
    try:
        value = float(value)
        if value >= 1e12:
            return f"{value / 1e12:.2f} T"
        elif value >= 1e9:
            return f"{value / 1e9:.2f} B"
        elif value >= 1e6:
            return f"{value / 1e6:.2f} M"
        return f"{value:.0f}"
    except (ValueError, TypeError):
        return "N/A"

def get_tickers(limit=100):
    """
    Retourne une liste de tickers avec leur nom et capitalisation boursière,
    limitant le nombre de résultats affichés.
    """
    try:
        load_dotenv()
        MONGO_URI = os.getenv("MONGO_URI")
        DB_NAME = os.getenv("DB_NAME_STOCKS")

        if not MONGO_URI or not DB_NAME:
            print("Erreur: MONGO_URI ou DB_NAME non défini dans le .env.")
            return []

        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]

        # Rechercher uniquement les documents "OVERVIEW"
        overview_docs = db.list_collection_names()
        tickers_info = []

        for ticker in overview_docs:
            doc = db[ticker].find_one({"function": "OVERVIEW"})
            if doc and "data" in doc:
                name = doc["data"].get("Name", "Unknown")
                market_cap = format_market_cap(doc["data"].get("MarketCapitalization", "N/A"))

                tickers_info.append({"symbol": ticker, "name": name, "market_cap": market_cap})

            # Limiter le nombre de résultats
            if len(tickers_info) >= limit:
                break

        return tickers_info

    except Exception as e:
        print(f"Erreur dans get_tickers: {e}")
        return []

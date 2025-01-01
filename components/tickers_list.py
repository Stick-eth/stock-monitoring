import os
from dotenv import load_dotenv
from pymongo import MongoClient

def get_tickers(DATA_DIRS):
    """
    Retourne la liste des tickers pour lesquels il existe au moins un document en base.
    On ignore 'DATA_DIRS' car on ne se base plus sur les fichiers locaux, mais sur MongoDB.
    """
    try:
        load_dotenv()
        MONGO_URI = os.getenv("MONGO_URI")
        DB_NAME = os.getenv("DB_NAME")

        if not MONGO_URI or not DB_NAME:
            print("Erreur: MONGO_URI ou DB_NAME non défini dans le .env.")
            return []

        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]

        # Récupère la liste de toutes les collections (chaque collection = un ticker)
        collections = db.list_collection_names()

        tickers = set()
        for col_name in collections:
            # Vérifier si la collection a au moins un document
            # count_documents({}) donne le nombre total de documents
            if db[col_name].count_documents({}) > 0:
                tickers.add(col_name)

        # Retourne la liste triée des tickers trouvés
        return sorted(tickers)

    except Exception as e:
        print(f"Erreur dans get_tickers: {e}")
        return []

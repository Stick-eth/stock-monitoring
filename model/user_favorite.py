import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Charger les variables d'environnement
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_USERS = os.getenv("DB_NAME_USERS")

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_USERS]
users_collection = db["users"]  # Collection pour stocker les favoris

def add_favorite_tickers(email, tickers):
    """
    Ajoute un ou plusieurs tickers à la liste des favoris d'un utilisateur.
    Si l'utilisateur n'existe pas encore, il est créé.
    """
    if not email or not tickers:
        return False  # Vérification des entrées

    tickers = set(tickers)  # Éviter les doublons
    user = users_collection.find_one({"email": email})

    if user:
        updated_tickers = list(set(user.get("favorites", []) + list(tickers)))
        users_collection.update_one({"email": email}, {"$set": {"favorites": updated_tickers}})
    else:
        users_collection.insert_one({"email": email, "favorites": list(tickers)})

    return True

def remove_favorite_tickers(email, tickers):
    """
    Supprime un ou plusieurs tickers des favoris d'un utilisateur.
    """
    if not email or not tickers:
        return False

    user = users_collection.find_one({"email": email})

    if user:
        updated_tickers = [t for t in user.get("favorites", []) if t not in tickers]
        users_collection.update_one({"email": email}, {"$set": {"favorites": updated_tickers}})
        return True

    return False

def get_favorite_tickers(email):
    """
    Récupère la liste des tickers favoris d'un utilisateur.
    """
    if not email:
        return []

    user = users_collection.find_one({"email": email})
    return user.get("favorites", []) if user else []


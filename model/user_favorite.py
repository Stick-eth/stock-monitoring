import os
from dotenv import load_dotenv
from pymongo import MongoClient, errors

# Charger les variables d'environnement
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_USERS = os.getenv("DB_NAME_USERS")

# Connexion MongoDB
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Timeout pour éviter les blocages
    db = client[DB_USERS]
    users_collection = db["users"]  # Collection pour stocker les favoris
except errors.ConnectionFailure:
    print("❌ ERREUR: Impossible de se connecter à MongoDB.")

def add_favorite_ticker(email, ticker):
    """
    Ajoute un ticker à la liste des favoris d'un utilisateur.
    Si l'utilisateur n'existe pas encore, il est créé.
    """
    try:
        if not email or not ticker:
            return False  # Vérification des entrées

        user = users_collection.find_one({"email": email})

        if user:
            updated_tickers = list(set(user.get("favorites", []) + [ticker]))
            users_collection.update_one({"email": email}, {"$set": {"favorites": updated_tickers}})
        else:
            users_collection.insert_one({"email": email, "favorites": [ticker]})

        return True
    except Exception as e:
        print(f"❌ ERREUR lors de l'ajout du ticker pour {email}: {e}")
        return False

def remove_favorite_ticker(email, ticker):
    """
    Supprime un ticker des favoris d'un utilisateur.
    """
    try:
        if not email or not ticker:
            return False

        user = users_collection.find_one({"email": email})

        if user:
            updated_tickers = [t for t in user.get("favorites", []) if t != ticker]
            users_collection.update_one({"email": email}, {"$set": {"favorites": updated_tickers}})
            return True

        return False
    except Exception as e:
        print(f"❌ ERREUR lors de la suppression du ticker pour {email}: {e}")
        return False

def get_favorite_tickers(email):
    """
    Récupère la liste des tickers favoris d'un utilisateur.
    """
    try:
        if not email:
            return []

        user = users_collection.find_one({"email": email})
        return user.get("favorites", []) if user else []
    except Exception as e:
        print(f"❌ ERREUR lors de la récupération des tickers pour {email}: {e}")
        return []

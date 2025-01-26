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
    users_collection = db["users"]  # Collection pour stocker les favoris et scores
except errors.ConnectionFailure:
    print("❌ ERREUR: Impossible de se connecter à MongoDB.")


def update_scores(email, new_scores):
    """
    Met à jour complètement la liste des scores d'un utilisateur.
    - Si l'utilisateur n'existe pas, il est créé avec ces scores.
    - Remplace complètement les scores existants par ceux fournis.
    
    new_scores doit être une **liste** de dictionnaires.
    """
    try:
        if not email or not isinstance(new_scores, list):
            return False  # Vérification des entrées

        # Vérifier si l'utilisateur existe
        user = users_collection.find_one({"email": email})

        if user:
            # Mise à jour complète des scores
            users_collection.update_one({"email": email}, {"$set": {"scores": new_scores}})
        else:
            # Créer un nouvel utilisateur avec ces scores
            users_collection.insert_one({"email": email, "scores": new_scores})

        return True
    except Exception as e:
        print(f"❌ ERREUR lors de la mise à jour des scores pour {email}: {e}")
        return False


def get_scores(email):
    """
    Récupère la liste complète des scores d'un utilisateur.
    """
    try:
        if not email:
            return []

        user = users_collection.find_one({"email": email})
        return user.get("scores", []) if user else []
    except Exception as e:
        print(f"❌ ERREUR lors de la récupération des scores pour {email}: {e}")
        return []


def clear_scores(email):
    """
    Supprime tous les scores d'un utilisateur.
    """
    try:
        if not email:
            return False

        user = users_collection.find_one({"email": email})

        if user:
            users_collection.update_one({"email": email}, {"$set": {"scores": []}})
            return True

        return False
    except Exception as e:
        print(f"❌ ERREUR lors de la suppression des scores pour {email}: {e}")
        return False

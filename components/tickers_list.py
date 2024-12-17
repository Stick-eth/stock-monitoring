# creer une fonction qui a pour but de retourner une liste de tickers
# Pour cela, chercher les fichiers JSON. Remonter dans le dossier puis aller dans le dossier data et ensuite dans chaque dossier présent se trouvent des fichiers JSON avec le nom des tickers (attentions aux doublons)
import os

def get_tickers(DATA_DIRS):
    """Retourne une liste de tickers basée sur les fichiers JSON disponibles."""
    tickers = set()
    for dir_path in DATA_DIRS.values():
        for file_name in os.listdir(dir_path):
            if file_name.endswith('.json'):
                tickers.add(file_name.split('.')[0])
    return sorted(list(tickers))

from dash import Dash, html
from layout import create_layout
from callbacks import register_callbacks

# Initialisation de l'application Dash
app = Dash(__name__)

# Application du layout
app.layout = create_layout()

# Enregistrement des callbacks
register_callbacks(app)

# Lancer le serveur
if __name__ == '__main__':
    app.run_server(debug=True)

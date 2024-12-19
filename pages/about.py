from dash import html

def about_layout():
    """Layout de la page à propos.
    Contenu : Titre, Description, Crédits.
    Centré verticalement et horizontalement.
    """
    return html.Div([
        html.H1("À Propos", style={'textAlign': 'center', 'marginTop': '20px'}),

        html.Div([
            html.P(
                "📊DataStick est une application web dédiée à l'analyse financière des entreprises cotées en bourse. "
                "Conçue pour offrir une interface simple et intuitive, elle permet de visualiser efficacement les données financières "
                "comme le feraient des solutions de screening coûteuses."
            ),
            html.P(
                "L'idée de DataStick m'est venue après avoir constaté que les outils d'analyse d'actions disponibles sur le marché "
                "sont souvent proposés à des prix exorbitants, atteignant plusieurs centaines d'euros par an. 🫣"
            ),
            html.P(
                "Je développe donc cet outil petit à petit sur mon temps libre, afin de m'en servir pour mes propres analyses et de les partager. "
                "Je suis convaincu que l'accès à l'information ne devrait pas coûter un bras."
            ),
            html.P(
                "👋 D'ailleurs moi c'est Aniss, étudiant en ingénierie informatique et passionné par la finance / big data. ",
                "J'espère que DataStick vous sera utile et vous permettra de prendre des décisions d'investissement éclairées."
            ),
            html.P(
                "Pour suivre l'évolution du projet, consultez le dépôt GitHub :"
            ),
            html.A(
                "https://github.com/Stick-eth/stock-monitoring",
                href="https://github.com/Stick-eth/stock-monitoring",
                style={'display': 'block', 'textAlign': 'center', 'marginTop': '10px'}
            )
        ], style={'width': '60%', 'margin': '20px auto', 'lineHeight': '1.6'}),
    ])

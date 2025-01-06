def apply_common_layout(fig, title=None, xaxis_title=None, yaxis_title=None, showlegend=False, hovermode="x unified"):
    """
    Applique un layout commun à un graphique Plotly.
    
    :param fig: L'objet Figure Plotly à modifier.
    :param title: Titre du graphique (str).
    :param xaxis_title: Titre de l'axe X (str).
    :param yaxis_title: Titre de l'axe Y (str).
    :param showlegend: Booléen pour afficher la légende.
    :param hovermode: Mode de survol (str).
    :return: L'objet Figure modifié.
    :param : exponentiel
    """
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        hovermode=hovermode,
        plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Papier transparent
        xaxis=dict(showgrid=False, autorange=True, color='rgb(90, 86, 126)', showline=True, linecolor='rgb(53, 51, 75)'),  # Pas de grille sur X
        yaxis=dict(showgrid=False, autorange=True),  # Pas de grille sur Y
        margin=dict(t=40),  # Marges supérieures
        showlegend=showlegend  # Afficher ou non la légende
    )
    return fig

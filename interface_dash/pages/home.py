# pages/home.py

import dash
from dash import html

dash.register_page(__name__, path='/', name="Accueil")

layout = html.Div([
    html.H2("Bienvenue sur l’interface de maintenance prédictive 🚀"),
    html.P("Utilisez le menu en haut pour naviguer entre les différentes fonctionnalités."),
])

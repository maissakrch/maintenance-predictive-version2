# interface_dash/app.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Initialisation de l'app avec gestion automatique des pages
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True
)

server = app.server

# Layout principal
app.layout = dbc.Container([
    html.H1("🛠️ Interface Maintenance Prédictive", className="mt-4"),
    
    dbc.Nav([
        dbc.NavLink("🏠 Accueil", href="/", active="exact"),
        dbc.NavLink("📊 Visualisation des données", href="/visualisation", active="exact"),
        dbc.NavLink("🔍 Prédiction", href="/predict", active="exact"),
        # Ajoute ici d'autres NavLink plus tard
    ], pills=True, className="mb-4"),

    dash.page_container
], fluid=True)

# Exécution
if __name__ == '__main__':
    app.run(debug=True)

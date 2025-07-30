# interface_dash/pages/comparison.py

import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/comparison", name="📈 Comparaison des modèles")

# Chargement des résultats
df = pd.read_csv("../results/model_comparison.csv")
df = df.rename(columns={"Unnamed: 0": "Model"})
fig = px.bar(df, x='Model', y='RMSE', color='Model', title="Comparaison des performances (RMSE)")

layout = html.Div([
    html.H2("📈 Comparaison des performances des modèles"),
    dcc.Graph(figure=fig)
])

# interface_dash/pages/shap.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/shap", name="Explicabilité SHAP")

# Lecture des fichiers SHAP
shap_values = pd.read_csv("results/shap_values.csv")
feature_names = pd.read_csv("results/feature_names.csv")

# Moyenne absolue des valeurs SHAP par feature
shap_values_mean = shap_values.abs().mean().values
feature_names_list = feature_names.columns.tolist()
df_shap = pd.DataFrame({
    "Feature": feature_names_list,
    "Importance": shap_values_mean
}).sort_values(by="Importance", ascending=False)

fig = px.bar(df_shap, x="Importance", y="Feature", orientation="h", title="Importance des variables (SHAP)")

layout = html.Div([
    html.H2("🧠 Explicabilité du modèle - SHAP"),
    html.P("Visualisation de l’impact de chaque capteur sur les prédictions du modèle."),
    dcc.Graph(figure=fig)
])

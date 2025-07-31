# interface_dash/pages/shap.py

import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/shap", name="Explicabilité (SHAP)")

def layout():
    try:
        df = pd.read_csv("../results/shap_values.csv")
        feature_names = pd.read_csv("../results/feature_names.csv").columns.tolist()

        df_mean = df.abs().mean().sort_values(ascending=False)
        fig = px.bar(
            x=df_mean.values[:10],
            y=df_mean.index[:10],
            orientation='h',
            labels={'x': 'Valeur moyenne SHAP', 'y': 'Feature'},
            title="Top 10 des variables influentes (SHAP)"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))

        return html.Div([
            html.H2("🧠 Explicabilité avec SHAP"),
            dcc.Graph(figure=fig)
        ])
    except Exception as e:
        return html.Div([
            html.H2("🧠 Explicabilité avec SHAP"),
            html.P(f"Erreur : {e}"),
            html.P("Assure-toi que les fichiers SHAP ont bien été générés.")
        ])

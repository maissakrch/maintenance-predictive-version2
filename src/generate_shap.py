import shap
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

# Chargement du pipeline complet
pipeline = joblib.load("models/random_forest_rul.pkl")

# Séparation des étapes
scaler = pipeline.named_steps["scaler"]
model = pipeline.named_steps["model"]

# Chargement des données
df = pd.read_csv("data/processed/cleaned_train.csv")
X = df.drop(columns=["unit", "cycle", "RUL", "max_cycle"])

# Standardisation
X_scaled = scaler.transform(X)

# SHAP avec modèle seul
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_scaled)

# Graphique résumé
plt.figure()
shap.summary_plot(shap_values, X, show=False)
plt.tight_layout()
os.makedirs("results", exist_ok=True)
plt.savefig("results/shap_summary_plot.png")

# Sauvegardes
pd.DataFrame(shap_values, columns=X.columns).to_csv("results/shap_values.csv", index=False)
pd.DataFrame({"feature_names": X.columns}).to_csv("results/feature_names.csv", index=False)

print("✅ SHAP values exportées avec succès.")

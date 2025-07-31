import pandas as pd
import numpy as np
import os
import joblib
import logging
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Configuration du logging
logging.basicConfig(
    filename="logs/train_models.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Chargement des données
data_path = "data/processed/cleaned_train.csv"
df = pd.read_csv(data_path)

# Préparation des features et cible
X = df.drop(columns=["RUL", "unit", "cycle", "max_cycle"], errors='ignore')
y = df["RUL"]

# Préparation du pipeline
scaler = StandardScaler()

# Dictionnaire pour stocker les résultats
results = []

# Modèle 1 : Random Forest
rf_pipeline = Pipeline([
    ("scaler", scaler),
    ("model", RandomForestRegressor(n_estimators=100, random_state=42))
])

rf_pipeline.fit(X, y)
y_pred_rf = rf_pipeline.predict(X)

mse_rf = mean_squared_error(y, y_pred_rf)
r2_rf = r2_score(y, y_pred_rf)
joblib.dump(rf_pipeline, "models/random_forest_rul.pkl")

results.append({
    "model": "RandomForest",
    "mse": mse_rf,
    "r2_score": r2_rf
})

logging.info(f"Random Forest trained - MSE: {mse_rf}, R2: {r2_rf}")

# Modèle 2 : XGBoost
xgb_pipeline = Pipeline([
    ("scaler", scaler),
    ("model", XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42))
])

xgb_pipeline.fit(X, y)
y_pred_xgb = xgb_pipeline.predict(X)

mse_xgb = mean_squared_error(y, y_pred_xgb)
r2_xgb = r2_score(y, y_pred_xgb)
joblib.dump(xgb_pipeline, "models/xgboost_rul.pkl")

results.append({
    "model": "XGBoost",
    "mse": mse_xgb,
    "r2_score": r2_xgb
})

logging.info(f"XGBoost trained - MSE: {mse_xgb}, R2: {r2_xgb}")

# Sauvegarde des résultats
results_df = pd.DataFrame(results)
os.makedirs("results", exist_ok=True)
results_df.to_csv("results/model_scores.csv", index=False)

print("✅ Modèles entraînés et sauvegardés avec succès.")

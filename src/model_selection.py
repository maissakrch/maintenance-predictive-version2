import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import numpy as np

# Charger les données de test (features + cible)
df = pd.read_csv("data/processed/cleaned_train.csv")
X = df.drop(columns=["RUL"])
y = df["RUL"]

# Charger les modèles
rf_model = joblib.load("models/random_forest_rul.pkl")
xgb_model = joblib.load("models/xgboost_rul.pkl")

# Prédictions
rf_preds = rf_model.predict(X)
xgb_preds = xgb_model.predict(X)

# Calcul des métriques
def evaluate_model(y_true, y_pred):
    return {
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "MAE": mean_absolute_error(y_true, y_pred),
        "R2": r2_score(y_true, y_pred)
    }

rf_metrics = evaluate_model(y, rf_preds)
xgb_metrics = evaluate_model(y, xgb_preds)

# Résumé en DataFrame
results = pd.DataFrame([rf_metrics, xgb_metrics], index=["Random Forest", "XGBoost"])
results.to_csv("results/model_comparison.csv")
print(results)

# Visualisation
results.plot(kind="bar", figsize=(10,6), colormap="Set2", legend=True)
plt.title("Comparaison des modèles")
plt.ylabel("Score")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("results/model_comparison.png")
plt.show()

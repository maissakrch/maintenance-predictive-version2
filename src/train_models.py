import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

# Charger les données nettoyées
df = pd.read_csv("data/processed/cleaned_train.csv")
X = df.drop(columns=["RUL"])
y = df["RUL"]

# Séparer en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
joblib.dump(rf, "models/random_forest_rul.pkl")
print("✅ Modèle Random Forest enregistré.")

# Entraîner XGBoost
xgb = XGBRegressor(n_estimators=100, random_state=42)
xgb.fit(X_train, y_train)
joblib.dump(xgb, "models/xgboost_rul.pkl")
print("✅ Modèle XGBoost enregistré.")


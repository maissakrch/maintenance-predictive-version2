from flask import Flask, request, jsonify
import pandas as pd
import joblib
import traceback

app = Flask(__name__)

# Chargement des modèles
rf_model = joblib.load("models/random_forest_rul.pkl")
xgb_model = joblib.load("models/xgboost_rul.pkl")

# Ajoute cette ligne après le chargement du modèle
expected_features = rf_model.feature_names_in_






@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame(data)

        # On ignore les colonnes non apprises
        for col in ['unit', 'cycle', 'max_cycle', 'RUL']:
            df = df.drop(columns=col, errors='ignore')

        # Juste avant la prédiction, filtre les colonnes
        df = df[[col for col in expected_features if col in df.columns]]

        # Prédictions
        prediction_rf = rf_model.predict(df)
        prediction_xgb = xgb_model.predict(df)

        return jsonify({
            "predictions": {
                "RandomForest": prediction_rf.tolist(),
                "XGBoost": prediction_xgb.tolist()
            }
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 400

if __name__ == '__main__':
    app.run(debug=True)

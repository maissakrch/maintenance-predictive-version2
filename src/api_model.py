from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Chargement du modèle Random Forest
model = joblib.load("models/random_forest_rul.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame(data)
        prediction = model.predict(df)
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

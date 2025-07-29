from flask import Flask, jsonify, request
import sqlite3
import pandas as pd

app = Flask(__name__)

DATABASE_PATH = "data/processed/maintenance.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # pour un accès facile via nom de colonne
    return conn

@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur l'API de maintenance prédictive !"})

@app.route('/data', methods=['GET'])
def get_all_data():
    limit = request.args.get('limit', default=100, type=int)
    try:
        conn = get_db_connection()
        query = f"SELECT * FROM moteurs LIMIT {limit}"
        df = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data/<int:unit_id>', methods=['GET'])
def get_data_by_unit(unit_id):
    try:
        conn = get_db_connection()
        query = f"SELECT * FROM moteurs WHERE unit = {unit_id}"
        df = pd.read_sql(query, conn)
        conn.close()
        if df.empty:
            return jsonify({"error": f"Aucune donnée trouvée pour le moteur {unit_id}."}), 404
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/meta', methods=['GET'])
def get_meta():
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM moteurs", conn)
        conn.close()
        metadata = {
            "colonnes": df.columns.tolist(),
            "types": df.dtypes.apply(lambda x: str(x)).to_dict(),
            "nb_lignes": len(df)
        }
        return jsonify(metadata)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

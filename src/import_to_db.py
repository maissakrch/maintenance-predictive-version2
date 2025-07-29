import pandas as pd
import sqlite3
import os

# Charger les données nettoyées
csv_path = os.path.join("data", "processed", "cleaned_train.csv")
df = pd.read_csv(csv_path)

# Connexion à la base de données SQLite (création automatique)
conn = sqlite3.connect("data/processed/maintenance.db")

# Importation dans une table nommée "moteurs"
df.to_sql("moteurs", conn, if_exists="replace", index=False)

print("✅ Données importées dans la base SQLite.")
conn.close()

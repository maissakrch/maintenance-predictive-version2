import pandas as pd
import sqlite3
import os

# Chemins
data_path = os.path.join("data", "processed", "cleaned_train.csv")
db_path = os.path.join("data", "processed", "maintenance.db")

# Charger les données nettoyées
df = pd.read_csv(data_path)

# Connexion à SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Création de la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS engine_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit INTEGER,
    cycle INTEGER,
    RUL INTEGER,
    max_cycle INTEGER,
    op_setting_1 REAL,
    op_setting_2 REAL,
    op_setting_3 REAL,
    sensor_2 REAL,
    sensor_3 REAL,
    sensor_4 REAL,
    sensor_7 REAL,
    sensor_8 REAL,
    sensor_9 REAL,
    sensor_11 REAL,
    sensor_12 REAL,
    sensor_13 REAL,
    sensor_14 REAL,
    sensor_15 REAL,
    sensor_17 REAL,
    sensor_20 REAL,
    sensor_21 REAL
)
''')

import hashlib

# Anonymiser les ID moteurs (simulé RGPD)
df['unit'] = df['unit'].apply(lambda x: int(hashlib.sha256(str(x).encode()).hexdigest(), 16) % 100000)


# Insertion dans la BDD
df.to_sql('engine_data', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print("✅ Base de données SQLite créée avec succès :", db_path)

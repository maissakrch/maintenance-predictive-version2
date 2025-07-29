import pandas as pd
import os

# Charger le dataset brut
input_path = os.path.join("data", "interim", "extracted_train.csv")
df = pd.read_csv(input_path)

# Supprimer les colonnes constantes ou inutiles
cols_to_drop = ['sensor_1', 'sensor_5', 'sensor_6', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']
df.drop(columns=cols_to_drop, inplace=True)

# Ajouter max_cycle et RUL
df['max_cycle'] = df.groupby('unit')['cycle'].transform('max')
df['RUL'] = df['max_cycle'] - df['cycle']

# Réordonner les colonnes pour plus de clarté
ordered_cols = ['unit', 'cycle', 'RUL', 'max_cycle'] + [col for col in df.columns if col not in ['unit', 'cycle', 'RUL', 'max_cycle']]
df = df[ordered_cols]

# Créer le dossier processed si nécessaire
output_dir = os.path.join("data", "processed")
os.makedirs(output_dir, exist_ok=True)

# Sauvegarder
output_path = os.path.join(output_dir, "cleaned_train.csv")
df.to_csv(output_path, index=False)

print("✅ Dataset nettoyé et sauvegardé dans", output_path)

import pandas as pd
import os

def load_cmaps_data(filepath):
    # Lire le fichier texte brut
    df = pd.read_csv(filepath, sep=" ", header=None)
    df = df.drop(columns=[26, 27])  # Supprimer colonnes vides

    # Définir les noms de colonnes
    columns = ['unit', 'cycle'] + \
              [f'op_setting_{i}' for i in range(1, 4)] + \
              [f'sensor_{i}' for i in range(1, 22)]
    df.columns = columns
    return df

if __name__ == "__main__":
    input_path = os.path.join("data", "raw", "train_FD001.txt")
    output_path = os.path.join("data", "interim", "extracted_train.csv")

    df = load_cmaps_data(input_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Données extraites et sauvegardées dans {output_path}")

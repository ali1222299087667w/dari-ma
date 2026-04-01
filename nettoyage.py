import pandas as pd

df = pd.read_csv("data/annonces_propres.csv")
print("Avant nettoyage :", df.shape)

# 1. Supprimer colonnes inutiles
df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0", "desc", "address"])

# 2. Renommer les colonnes
df = df.rename(columns={
    "new_price": "prix",
    "salles de bains": "salles_bains",
    "Nighberd": "quartier",
    "City": "ville",
    "Type": "type_bien",
    "floor": "etage"
})

# 3. Convertir Yes/No en 1/0
for col in ["ascenseur", "terrasse", "parking"]:
    df[col] = df[col].map({"Yes": 1, "No": 0})

# 4. Supprimer lignes manquantes
df = df.dropna(subset=["prix", "surface", "ville"])

# 5. Supprimer valeurs aberrantes
df = df[df["prix"] > 100000]
df = df[df["prix"] < 50000000]
df = df[df["surface"] > 10]
df = df[df["surface"] < 2000]

df = df.reset_index(drop=True)
print("Après nettoyage :", df.shape)
print(df.head())

df.to_csv("data/annonces_propres.csv", index=False)
print("Fichier sauvegardé !")
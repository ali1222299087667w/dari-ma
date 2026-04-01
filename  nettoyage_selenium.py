import pandas as pd
import re

df = pd.read_csv("data/annonces_selenium.csv")
print("Avant nettoyage :", df.shape)

# 1. Supprimer les prix non numériques
df = df[~df["prix"].str.contains("Projet|consulter|partir", na=True)]
df = df[df["prix"].notna()]

# 2. Nettoyer le prix
def nettoyer_prix(p):
    try:
        p = re.sub(r"[^\d]", "", str(p))
        return int(p)
    except:
        return None

df["prix"] = df["prix"].apply(nettoyer_prix)
df = df.dropna(subset=["prix"])

# 3. Nettoyer la surface
def nettoyer_surface(s):
    try:
        match = re.search(r"(\d+)", str(s))
        return int(match.group(1)) if match else None
    except:
        return None

df["surface"] = df["surface"].apply(nettoyer_surface)

# 4. Utiliser ville_scrape comme ville fiable
df["ville"] = df["ville_scrape"].str.capitalize()

# 5. Garder seulement les vraies villes
villes_valides = ["Casablanca", "Rabat", "Marrakech", "Tanger"]
df = df[df["ville"].isin(villes_valides)]

# 6. Supprimer valeurs aberrantes
df = df[df["prix"] > 100000]
df = df[df["prix"] < 50000000]
df = df[df["surface"] > 10]
df = df[df["surface"] < 2000]

df = df.dropna(subset=["prix", "surface", "ville"])
df = df.reset_index(drop=True)

print("Après nettoyage :", df.shape)
print(df[["prix", "surface", "ville"]].head(10))
print("\nVilles :", df["ville"].value_counts())

df.to_csv("data/annonces_propres_selenium.csv", index=False)
print("\nFichier sauvegardé !")
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/annonces_propres.csv")

# 1. Statistiques générales
print("=== Statistiques ===")
print(df[["prix", "surface", "chambres"]].describe())

# 2. Graphe 1 — Distribution des prix
plt.figure(figsize=(10, 4))
df["prix"].hist(bins=50, color="#7F77DD")
plt.title("Distribution des prix")
plt.xlabel("Prix (DH)")
plt.ylabel("Nombre d'annonces")
plt.tight_layout()
plt.savefig("data/distribution_prix.png")
plt.close()
print("Graphe 1 sauvegardé")

# 3. Graphe 2 — Prix moyen par ville
plt.figure(figsize=(10, 4))
df.groupby("ville")["prix"].mean().sort_values().plot(kind="barh", color="#1D9E75")
plt.title("Prix moyen par ville")
plt.xlabel("Prix moyen (DH)")
plt.tight_layout()
plt.savefig("data/prix_par_ville.png")
plt.close()
print("Graphe 2 sauvegardé")

# 4. Graphe 3 — Prix vs Surface
plt.figure(figsize=(8, 5))
plt.scatter(df["surface"], df["prix"], alpha=0.3, color="#D85A30")
plt.title("Prix vs Surface")
plt.xlabel("Surface (m²)")
plt.ylabel("Prix (DH)")
plt.tight_layout()
plt.savefig("data/prix_vs_surface.png")
plt.close()
print("Graphe 3 sauvegardé")

print("\nEDA terminée ! Ouvre le dossier data/ pour voir les graphes.")
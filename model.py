import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_squared_error
from xgboost import XGBRegressor
import numpy as np
import pickle
import os

# 1. Chargement
df = pd.read_csv("data/annonces_propres_selenium.csv")
print("Données chargées :", df.shape)

# 2. Feature engineering — prix moyen au m² par ville
prix_m2_ville = df.groupby("ville")["prix"].mean() / df.groupby("ville")["surface"].mean()
df["prix_m2_ville"] = df["ville"].map(prix_m2_ville)

# 3. Ratio surface / moyenne ville
surface_moy_ville = df.groupby("ville")["surface"].mean()
df["surface_ratio"] = df["surface"] / df["ville"].map(surface_moy_ville)

# 4. Encoder la ville
le_ville = LabelEncoder()
df["ville_encoded"] = le_ville.fit_transform(df["ville"].astype(str))

# 5. Features enrichies
features = ["surface", "ville_encoded", "prix_m2_ville", "surface_ratio"]
target = "prix"

df_model = df[features + [target]].dropna()
print("Lignes disponibles :", df_model.shape)

# 6. Split
X = df_model[features]
y = df_model[target]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Train : {X_train.shape[0]} | Test : {X_test.shape[0]}")

# 7. Entraîner
model = XGBRegressor(n_estimators=300, learning_rate=0.05, random_state=42)
model.fit(X_train, y_train)
print("Modèle entraîné !")

# 8. Évaluation
y_pred = model.predict(X_test)
r2   = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"\n=== Résultats ===")
print(f"R²   : {r2:.3f}")
print(f"RMSE : {rmse:,.0f} DH")

# 9. Sauvegarder
os.makedirs("model", exist_ok=True)
with open("model/xgboost_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("model/label_encoders.pkl", "wb") as f:
    pickle.dump({
        "ville": le_ville,
        "prix_m2_ville": prix_m2_ville,
        "surface_moy_ville": surface_moy_ville
    }, f)
print("\nModèle sauvegardé !")
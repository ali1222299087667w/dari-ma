from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

annonces = []

villes = [
    "casablanca",
    "rabat",
    "marrakech",
    "tanger",
    "fes"
]

for ville in villes:
    print(f"\n=== Scraping {ville} ===")
    for page in range(1, 11):  # 10 pages par ville
        try:
            url = f"https://www.mubawab.ma/fr/ct/{ville}/immobilier-a-vendre:p:{page}"
            print(f"Page {page}...")
            driver.get(url)
            time.sleep(5)

            items = driver.find_elements(By.CLASS_NAME, "listingBox")
            print(f"  → {len(items)} annonces")

            if len(items) == 0:
                break

            for item in items:
                try:
                    prix  = item.find_element(By.CLASS_NAME, "priceTag").text.strip()
                    titre = item.find_element(By.TAG_NAME, "h2").text.strip()
                    lignes = item.text.split("\n")
                    lieu = lignes[1] if len(lignes) > 1 else ville
                    surface = ""
                    for ligne in lignes:
                        if "m²" in ligne:
                            surface = ligne.strip()
                            break
                    annonces.append({
                        "prix": prix,
                        "titre": titre,
                        "lieu": lieu,
                        "surface": surface,
                        "ville_scrape": ville
                    })
                except:
                    pass

            df = pd.DataFrame(annonces)
            os.makedirs("data", exist_ok=True)
            df.to_csv("data/annonces_selenium.csv", index=False)
            print(f"  Total cumulé : {len(annonces)} annonces")

        except Exception as e:
            print(f"  Erreur, on continue...")
            time.sleep(5)
            continue

driver.quit()
print(f"\nTerminé ! {len(annonces)} annonces collectées")
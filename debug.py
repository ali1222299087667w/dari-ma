from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.mubawab.ma/fr/ct/casablanca/immobilier-a-vendre:p:1")
time.sleep(5)

items = driver.find_elements(By.CLASS_NAME, "listingBox")
print(f"{len(items)} annonces trouvées")

if items:
    item = items[0]
    # Tester chaque élément séparément
    try:
        prix = item.find_element(By.CLASS_NAME, "priceTag").text.strip()
        print(f"Prix : {prix}")
    except Exception as e:
        print(f"Prix introuvable : {e}")

    try:
        titre = item.find_element(By.TAG_NAME, "h2").text.strip()
        print(f"Titre : {titre}")
    except Exception as e:
        print(f"Titre introuvable : {e}")

    try:
        lieu = item.find_element(By.CLASS_NAME, "listingH2").text.strip()
        print(f"Lieu : {lieu}")
    except Exception as e:
        print(f"Lieu introuvable : {e}")

    # Afficher tout le texte de l'annonce
    print(f"\nTexte complet :\n{item.text[:500]}")

driver.quit()
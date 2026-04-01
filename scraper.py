import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def scraper_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

toutes_annonces = []

for page in range(1, 6):  # 5 pages pour tester
    url = f"https://www.avito.ma/fr/maroc/immobilier--%C3%A0_vendre?o={page}"
    print(f"Scraping page {page}...")
    soup = scraper_page(url)

    items = soup.find_all("article")
    print(f"  → {len(items)} annonces trouvées")

    for item in items:
        try:
            prix = item.find("p", class_="sc-1x0vz2r-0").text.strip()
            titre = item.find("p", class_="sc-1nre5ec-1").text.strip()
            lieu = item.find("p", class_="sc-1nre5ec-2").text.strip()
            toutes_annonces.append({
                "prix": prix,
                "titre": titre,
                "lieu": lieu
            })
        except:
            pass

    time.sleep(2)

print(f"\nTotal : {len(toutes_annonces)} annonces collectées")

os.makedirs("data", exist_ok=True)
df = pd.DataFrame(toutes_annonces)
df.to_csv("data/annonces_brutes.csv", index=False)
print("Fichier sauvegardé !")
print(df.head())
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

catalog = []

cards = soup.find_all("a")

for card in cards:
    href = card.get("href")
    text = card.get_text(strip=True)

    if href and "/products/" in href and text:
        item = {
            "name": text,
            "url": href if href.startswith("http") else f"https://www.shl.com{href}",
            "description": text,
            "test_type": "Unknown"
        }

        if item not in catalog:
            catalog.append(item)

with open("catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print(f"Saved {len(catalog)} assessments")

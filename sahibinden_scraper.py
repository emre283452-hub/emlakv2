import requests
from bs4 import BeautifulSoup
import json

def fetch_listings(city="istanbul", district="kadikoy", page=1):
    url = f"https://www.sahibinden.com/satilik-daire/{city}-{district}?pagingOffset={(page-1)*20}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("tr.searchResultsItem")
    listings = []
    for row in rows:
        try:
            title = row.select_one(".searchResultsTitleValue").get_text(strip=True)
            price_text = row.select_one(".searchResultsPriceValue").get_text(strip=True)
            price = (
                price_text.replace("TL", "")
                .replace(".", "")
                .replace(" ", "")
                .replace(",", "")
            )
            price = int(price) if price.isdigit() else None
            location = row.select_one(".searchResultsLocationValue").get_text(strip=True)
            details = row.select_one(".searchResultsAttributeValue")
            if details:
                details = details.get_text(strip=True)
            else:
                details = ""
            listings.append({
                "title": title,
                "price": price,
                "location": location,
                "details": details
            })
        except Exception:
            continue
    return listings

# Bu kodu ekle: Çıktıyı dosyaya yaz
if __name__ == "__main__":
    data = fetch_listings()
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
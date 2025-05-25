import requests
from bs4 import BeautifulSoup
import json

def scrape_livescore():
    url = "https://www.livescore.com/en/football/live/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ خطا در دریافت داده‌ها: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        matches = []

        match_blocks = soup.find_all("div", class_="match-row__data")
        for block in match_blocks:
            try:
                teams = block.find_all("div", class_="match-row__team-name")
                time = block.find("div", class_="match-row__time")
                league_block = block.find_previous("div", class_="match-row__competition")

                home = teams[0].text.strip() if teams else ""
                away = teams[1].text.strip() if len(teams) > 1 else ""
                match_time = time.text.strip() if time else "زمان نامشخص"
                league = league_block.text.strip() if league_block else "لیگ نامشخص"

                matches.append({
                    "home": home,
                    "away": away,
                    "time": match_time,
                    "league": league,
                    "country": "LiveScore"
                })
            except:
                continue

        with open("matches.json", "w", encoding="utf-8") as f:
            json.dump(matches, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(matches)} بازی ذخیره شد.")

    except Exception as e:
        print(f"❌ خطای کلی در scraper: {e}")

if __name__ == "__main__":
    scrape_livescore()

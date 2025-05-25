import requests
import json
from datetime import date

def scrape_sportsdb_fixtures():
    try:
        today = str(date.today())
        url = f"https://www.thesportsdb.com/api/v1/json/1/eventsday.php?d={today}&s=Soccer"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"خطا در دریافت داده‌ها: {response.status_code}")
            return []

        data = response.json()
        matches = []

        if not data.get("events"):
            print("هیچ رویدادی پیدا نشد.")
            return []

        for event in data["events"]:
            home = event.get("strHomeTeam", "")
            away = event.get("strAwayTeam", "")
            time = event.get("strTime", "")
            league = event.get("strLeague", "")
            country = event.get("strCountry", "")
            matches.append({
                "home": home,
                "away": away,
                "time": time,
                "league": league,
                "country": country
            })

        with open("matches.json", "w", encoding="utf-8") as f:
            json.dump(matches, f, ensure_ascii=False, indent=2)

        print(f"✅ {len(matches)} بازی ذخیره شد.")
        return matches

    except Exception as e:
        print("❌ خطا در scraper:", str(e))
        return []

if __name__ == "__main__":
    scrape_sportsdb_fixtures()

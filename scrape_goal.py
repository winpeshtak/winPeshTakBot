
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_goal_fixtures():
    url = "https://www.goal.com/en/fixtures"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"❌ خطا در دریافت داده‌ها از goal.com: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    matches = []

    containers = soup.find_all("div", class_="match-main-data")
    for match in containers:
        try:
            time = match.find("div", class_="match-status").text.strip()
            teams = match.find_all("span", class_="team-name")
            home = teams[0].text.strip()
            away = teams[1].text.strip()
            matches.append({
                "home": home,
                "away": away,
                "time": time
            })
        except Exception:
            continue

    with open("matches.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)

    return matches

# برای تست مستقیم:
if __name__ == "__main__":
    result = scrape_goal_fixtures()
    if isinstance(result, list):
        for m in result:
            print(f"{m['time']} | {m['home']} vs {m['away']}")
    else:
        print(result)

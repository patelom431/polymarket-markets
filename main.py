import requests
import csv
from datetime import datetime, timezone

max_pages = 50
start_cursor = "Mjk1MDA="
next_cursor = start_cursor
data_list = []

allowed_tags = ["Crypto", "Memecoins", "Politics", "Geopolitics", "Foreign Policy", "Breaking News", "Elon Musk", "Twitter", "Tech", "Business", "AI"]
disallowed_tags = ["German Election"]

for i in range(max_pages):
    print("Fetching page with next_cursor", next_cursor)
    req = requests.get("https://clob.polymarket.com/markets?next_cursor=" + next_cursor)
    json = req.json()

    if "data" not in json:
        break

    data = json["data"]
    data_list.extend(data)
    next = json.get("next_cursor")

    if not next or next == next_cursor:
        break

    next_cursor = next

#writer = csv.writer(sys.stdout)
writer = csv.writer(open("markets.csv", "w", newline="", encoding="utf-8"))
writer.writerow(["question", "market_slug", "end_date", "outcomes", "tags", "description"])

sorted_data = [market for market in data_list if market.get("end_date_iso")]
sorted_data.sort(key=lambda x: x["end_date_iso"])

now = datetime.now(timezone.utc)

for market in sorted_data:
    if not market["active"]:
        continue
    if market["closed"]:
        continue
    if market["archived"]:
        continue
    if datetime.fromisoformat(market["end_date_iso"]) < now:
        continue

    if not any(tag in market["tags"] for tag in allowed_tags):
        continue
    if any(tag in market["tags"] for tag in disallowed_tags):
        continue

    outcomes = "[" + ", ".join(token["outcome"] for token in market["tokens"]) + "]"
    tags = "[" + ", ".join(market["tags"]) + "]"
    description = " ".join(market.get("description", "").split())

    writer.writerow([
        market["question"],
        market.get("market_slug", ""),
        market.get("end_date_iso", ""),
        outcomes,
        tags,
        description
    ])
import requests
import csv

max_pages = 5
start_cursor = "Mjk1MDA="
next_cursor = start_cursor
data_list = []

for i in range(max_pages):
    print("Fetching page with next_cursor", next_cursor)
    req = requests.get("https://clob.polymarket.com/markets?next_cursor=" + next_cursor)
    json_data = req.json()

    if "data" not in json_data:
        break

    data = json_data["data"]
    data_list.extend(data)
    nc = json_data.get("next_cursor")

    if not nc or nc == next_cursor:
        break

    next_cursor = nc

#writer = csv.writer(sys.stdout)
writer = csv.writer(open("markets.csv", "w", newline="", encoding="utf-8"))

writer.writerow(["question", "market_slug", "end_date", "outcomes", "tags"])

for market in data_list:
    if not market["active"]:
        continue
    if market["closed"]:
        continue
    if market["archived"]:
        continue
    if "Politics" not in market["tags"]:
        continue

    outcomes_str = "[" + ", ".join(token["outcome"] for token in market["tokens"]) + "]"
    tags_str = "[" + ", ".join(market["tags"]) + "]"

    writer.writerow([
        market["question"],
        market.get("market_slug", ""),
        market.get("end_date_iso", ""),
        outcomes_str,
        tags_str
    ])
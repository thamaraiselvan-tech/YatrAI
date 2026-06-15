import json

with open('../chennai_trichy_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for city_key, city in data["cities"].items():
    print(f"\n==================== {city_key.upper()} ====================")
    for cat, routes in city["routes"].items():
        print(f"\n--- Category: {cat} ---")
        for r in routes:
            print(f"Route: {r['route_id']} | No: {r['route_number']} | Name: {r['name']} | Op: {r['operator']} | Type: {r['type']} | AC: {r['ac']} | Stops: {len(r['stops'])}")

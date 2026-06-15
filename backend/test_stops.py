import json

with open('../chennai_trichy_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

stops = {}
for city_key, city in data["cities"].items():
    for cat, routes in city["routes"].items():
        for r in routes:
            for s in r["stops"]:
                name = s["name"]
                if name not in stops:
                    stops[name] = (s["lat"], s["lng"])

print(f"Total unique stops: {len(stops)}")
for name, coords in sorted(stops.items()):
    print(f"  {repr(name)}: {coords}")

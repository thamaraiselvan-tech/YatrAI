"""
YatrAI Transit Dataset Test Suite
Chennai + Tiruchirappalli — Full Route Coverage
Run: python3 test_routes.py
"""

import json
import math
import sys
from collections import defaultdict

DATASET_PATH = "chennai_trichy_dataset.json"
PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
WARN = "\033[93m⚠\033[0m"
HEAD = "\033[94m"
RESET = "\033[0m"

results = {"pass": 0, "fail": 0, "warn": 0}

def ok(msg):
    results["pass"] += 1
    print(f"  {PASS} {msg}")

def fail(msg):
    results["fail"] += 1
    print(f"  {FAIL} {msg}")

def warn(msg):
    results["warn"] += 1
    print(f"  {WARN} {msg}")

def section(title):
    print(f"\n{HEAD}{'═'*60}")
    print(f"  {title}")
    print(f"{'═'*60}{RESET}")

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# ─────────────────────────────────────────────────────────────
# Load dataset
# ─────────────────────────────────────────────────────────────
section("LOADING DATASET")
try:
    with open(DATASET_PATH) as f:
        data = json.load(f)
    ok(f"Dataset loaded: {DATASET_PATH}")
except Exception as e:
    fail(f"Failed to load dataset: {e}")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# TEST 1 — Metadata
# ─────────────────────────────────────────────────────────────
section("TEST 1 · METADATA VALIDATION")
meta = data.get("metadata", {})
for field in ["version", "generated", "cities", "operators", "total_routes"]:
    if meta.get(field):
        ok(f"metadata.{field} = {meta[field]}")
    else:
        fail(f"metadata.{field} missing")

# ─────────────────────────────────────────────────────────────
# TEST 2 — City structure
# ─────────────────────────────────────────────────────────────
section("TEST 2 · CITY STRUCTURE")
for city_key in ["chennai", "tiruchirappalli"]:
    city = data["cities"].get(city_key)
    if city:
        ok(f"City '{city['name']}' exists")
        for field in ["name", "state", "center", "major_hubs", "routes"]:
            if field in city:
                ok(f"  {city_key}.{field} present")
            else:
                fail(f"  {city_key}.{field} MISSING")
    else:
        fail(f"City '{city_key}' not found")

# ─────────────────────────────────────────────────────────────
# TEST 3 — Route coverage count
# ─────────────────────────────────────────────────────────────
section("TEST 3 · ROUTE COVERAGE COUNT")

all_routes = {}
for city_key, city in data["cities"].items():
    for category, routes in city["routes"].items():
        for route in routes:
            rid = route["route_id"]
            all_routes[rid] = route

total = len(all_routes)
ok(f"Total routes in dataset: {total}")

# per city
for city_key, city in data["cities"].items():
    count = sum(len(v) for v in city["routes"].values())
    ok(f"  {city['name']}: {count} routes")
    for cat, routes in city["routes"].items():
        ok(f"    [{cat}]: {len(routes)} routes")

# ─────────────────────────────────────────────────────────────
# TEST 4 — Schema validation per route
# ─────────────────────────────────────────────────────────────
section("TEST 4 · SCHEMA VALIDATION (every route)")
required_fields = ["route_id", "route_number", "name", "operator", "type",
                   "distance_km", "duration_min", "frequency_min",
                   "first_bus", "last_bus", "fare_min", "fare_max", "ac", "stops"]

schema_errors = 0
for rid, route in all_routes.items():
    for field in required_fields:
        if field not in route:
            fail(f"  {rid}: missing '{field}'")
            schema_errors += 1
    if len(route.get("stops", [])) < 2:
        fail(f"  {rid}: needs at least 2 stops")
        schema_errors += 1

if schema_errors == 0:
    ok(f"All {total} routes pass schema validation")
else:
    fail(f"{schema_errors} schema errors found")

# ─────────────────────────────────────────────────────────────
# TEST 5 — Stop coordinate validation
# ─────────────────────────────────────────────────────────────
section("TEST 5 · STOP COORDINATE VALIDATION")
coord_errors = 0
for rid, route in all_routes.items():
    for stop in route["stops"]:
        lat, lng = stop.get("lat", 0), stop.get("lng", 0)
        # Chennai bounding box: lat 12.6–13.3, lng 79.9–80.5
        # Trichy bounding box: lat 10.5–11.0, lng 78.4–79.0
        # Inter-district routes can go wider
        if route["type"] in ("express", "semi_express") and route.get("distance_km", 0) > 50:
            in_tn = 8.0 < lat < 14.0 and 76.0 < lng < 81.0
        else:
            in_tn = 8.0 < lat < 14.0 and 76.0 < lng < 81.0
        if not in_tn:
            fail(f"  {rid} > '{stop['name']}': coord ({lat},{lng}) out of Tamil Nadu")
            coord_errors += 1

if coord_errors == 0:
    ok(f"All stop coordinates within Tamil Nadu bounds")
else:
    fail(f"{coord_errors} coordinate errors")

# ─────────────────────────────────────────────────────────────
# TEST 6 — Stop sequence integrity
# ─────────────────────────────────────────────────────────────
section("TEST 6 · STOP SEQUENCE INTEGRITY")
seq_errors = 0
for rid, route in all_routes.items():
    seqs = [s["seq"] for s in route["stops"]]
    expected = list(range(1, len(seqs) + 1))
    if seqs != expected:
        fail(f"  {rid}: stop seq {seqs} expected {expected}")
        seq_errors += 1
if seq_errors == 0:
    ok("All routes have contiguous stop sequences starting from 1")

# ─────────────────────────────────────────────────────────────
# TEST 7 — Fare logic
# ─────────────────────────────────────────────────────────────
section("TEST 7 · FARE LOGIC")
fare_errors = 0
for rid, route in all_routes.items():
    if route["fare_min"] > route["fare_max"]:
        fail(f"  {rid}: fare_min ({route['fare_min']}) > fare_max ({route['fare_max']})")
        fare_errors += 1
    if route["fare_min"] < 5:
        warn(f"  {rid}: fare_min={route['fare_min']} (suspiciously low)")
    if route["fare_max"] > 500:
        warn(f"  {rid}: fare_max={route['fare_max']} (suspiciously high)")
if fare_errors == 0:
    ok("fare_min ≤ fare_max for all routes")

# ─────────────────────────────────────────────────────────────
# TEST 8 — Time logic
# ─────────────────────────────────────────────────────────────
section("TEST 8 · OPERATING HOURS")
time_errors = 0
for rid, route in all_routes.items():
    fb = route["first_bus"]
    lb = route["last_bus"]
    # basic HH:MM format check
    for t, label in [(fb, "first_bus"), (lb, "last_bus")]:
        parts = t.split(":")
        if len(parts) != 2:
            fail(f"  {rid}: invalid {label} format '{t}'")
            time_errors += 1
        else:
            h, m = int(parts[0]), int(parts[1])
            if not (0 <= h <= 23 and 0 <= m <= 59):
                fail(f"  {rid}: {label}='{t}' out of range")
                time_errors += 1
    if route["frequency_min"] <= 0:
        fail(f"  {rid}: frequency_min must be > 0")
        time_errors += 1
if time_errors == 0:
    ok("All time fields valid (HH:MM, frequency > 0)")

# ─────────────────────────────────────────────────────────────
# TEST 9 — Operator coverage
# ─────────────────────────────────────────────────────────────
section("TEST 9 · OPERATOR COVERAGE")
operators = defaultdict(list)
for rid, route in all_routes.items():
    operators[route["operator"]].append(rid)
for op, rids in sorted(operators.items()):
    ok(f"  {op}: {len(rids)} routes")

# ─────────────────────────────────────────────────────────────
# TEST 10 — Route type coverage
# ─────────────────────────────────────────────────────────────
section("TEST 10 · ROUTE TYPE COVERAGE")
types = defaultdict(int)
for route in all_routes.values():
    types[route["type"]] += 1
for t, count in sorted(types.items()):
    ok(f"  {t}: {count} routes")

expected_types = ["ordinary", "express", "metro", "suburban_rail", "mrts",
                  "ac_volvo", "feeder", "semi_express", "circular"]
for et in expected_types:
    if et in types:
        ok(f"  Type '{et}' present ✓")
    else:
        warn(f"  Type '{et}' not present in dataset")

# ─────────────────────────────────────────────────────────────
# TEST 11 — Hub connectivity check
# ─────────────────────────────────────────────────────────────
section("TEST 11 · MAJOR HUB CONNECTIVITY")
def routes_through(stop_name_substr, city_routes):
    matched = []
    for routes in city_routes.values():
        for route in routes:
            for stop in route["stops"]:
                if stop_name_substr.lower() in stop["name"].lower():
                    matched.append(route["route_id"])
                    break
    return matched

# Chennai hubs
chennai_routes = data["cities"]["chennai"]["routes"]
for hub in ["Broadway", "Koyambedu", "Chennai Central", "Tambaram", "Guindy", "Airport"]:
    routes_via = routes_through(hub, chennai_routes)
    if routes_via:
        ok(f"  Chennai '{hub}': {len(routes_via)} routes {routes_via[:3]}{'...' if len(routes_via)>3 else ''}")
    else:
        fail(f"  Chennai '{hub}': NO routes pass through!")

# Trichy hubs
trichy_routes = data["cities"]["tiruchirappalli"]["routes"]
for hub in ["Central Bus Stand", "Chathiram", "Srirangam", "Airport", "NIT"]:
    routes_via = routes_through(hub, trichy_routes)
    if routes_via:
        ok(f"  Trichy '{hub}': {len(routes_via)} routes {routes_via[:3]}{'...' if len(routes_via)>3 else ''}")
    else:
        warn(f"  Trichy '{hub}': only partial match")

# ─────────────────────────────────────────────────────────────
# TEST 12 — Route planner simulation (YatrAI core API test)
# ─────────────────────────────────────────────────────────────
section("TEST 12 · ROUTE PLANNER API SIMULATION")

def find_routes(from_stop: str, to_stop: str, city_key: str) -> list:
    """Simulate YatrAI's findRoutes API"""
    city = data["cities"].get(city_key, {})
    results_list = []
    for category, routes in city.get("routes", {}).items():
        for route in routes:
            stop_names = [s["name"].lower() for s in route["stops"]]
            from_idx = next((i for i, n in enumerate(stop_names) if from_stop.lower() in n), -1)
            to_idx = next((i for i, n in enumerate(stop_names) if to_stop.lower() in n), -1)
            if from_idx >= 0 and to_idx >= 0 and from_idx < to_idx:
                stops_on_route = route["stops"][from_idx:to_idx+1]
                # calc approx distance between matched stops
                d = haversine(
                    stops_on_route[0]["lat"], stops_on_route[0]["lng"],
                    stops_on_route[-1]["lat"], stops_on_route[-1]["lng"]
                )
                results_list.append({
                    "route_id": route["route_id"],
                    "route_number": route["route_number"],
                    "name": route["name"],
                    "operator": route["operator"],
                    "type": route["type"],
                    "boarding": stops_on_route[0]["name"],
                    "alighting": stops_on_route[-1]["name"],
                    "intermediate_stops": len(stops_on_route) - 2,
                    "estimated_distance_km": round(d, 2),
                    "frequency_min": route["frequency_min"],
                    "fare_range": f"₹{route['fare_min']}–₹{route['fare_max']}",
                    "ac": route["ac"]
                })
    return sorted(results_list, key=lambda x: x["frequency_min"])

# Chennai test queries
queries_chennai = [
    ("Broadway", "Thiruvanmiyur"),
    ("Koyambedu", "Airport"),
    ("Central", "Tambaram"),
    ("Egmore", "Velachery"),
    ("Koyambedu", "Sholinganallur"),
    ("Chennai Central", "Avadi"),
    ("Broadway", "Porur"),
]
print(f"\n  Chennai Route Planner:")
for src, dst in queries_chennai:
    found = find_routes(src, dst, "chennai")
    if found:
        r = found[0]
        ok(f"  {src} → {dst}: {r['route_number']} ({r['operator']}, every {r['frequency_min']}min, {r['fare_range']})")
    else:
        fail(f"  {src} → {dst}: NO ROUTE FOUND")

# Trichy test queries
queries_trichy = [
    ("Central Bus Stand", "Srirangam"),
    ("Chathiram", "Kailasapuram"),
    ("Central Bus Stand", "Airport"),
    ("Chathiram", "NIT"),
    ("Trichy Junction", "Thuvakudi"),
    ("Chathiram", "Samayapuram"),
    ("Central Bus Stand", "Lalgudi"),
]
print(f"\n  Trichy Route Planner:")
for src, dst in queries_trichy:
    found = find_routes(src, dst, "tiruchirappalli")
    if found:
        r = found[0]
        ok(f"  {src} → {dst}: {r['route_number']} ({r['operator']}, every {r['frequency_min']}min, {r['fare_range']})")
    else:
        fail(f"  {src} → {dst}: NO ROUTE FOUND")

# ─────────────────────────────────────────────────────────────
# TEST 13 — Nearest-stop lookup simulation
# ─────────────────────────────────────────────────────────────
section("TEST 13 · NEAREST STOP LOOKUP (GPS simulation)")

def nearest_stops(user_lat, user_lng, city_key, top_n=5):
    city = data["cities"].get(city_key, {})
    seen = {}
    for routes in city.get("routes", {}).values():
        for route in routes:
            for stop in route["stops"]:
                key = stop["name"]
                d = haversine(user_lat, user_lng, stop["lat"], stop["lng"])
                if key not in seen or seen[key]["dist"] > d:
                    seen[key] = {"name": stop["name"], "dist": round(d, 3),
                                 "lat": stop["lat"], "lng": stop["lng"],
                                 "route": route["route_id"]}
    return sorted(seen.values(), key=lambda x: x["dist"])[:top_n]

# Test: user at Anna Nagar, Chennai
test_cases = [
    (13.0850, 80.2101, "chennai", "Anna Nagar Chennai"),
    (13.0694, 80.1948, "chennai", "Koyambedu CMBT"),
    (10.8048, 78.6921, "tiruchirappalli", "Trichy CBS"),
    (10.7936, 78.7198, "tiruchirappalli", "Thillai Nagar"),
]
for lat, lng, city_key, label in test_cases:
    stops = nearest_stops(lat, lng, city_key)
    if stops:
        top = stops[0]
        ok(f"  Nearest to '{label}': '{top['name']}' ({top['dist']}km via {top['route']})")
        for s in stops[1:3]:
            print(f"      → {s['name']} ({s['dist']}km)")
    else:
        fail(f"  No stops found near '{label}'")

# ─────────────────────────────────────────────────────────────
# TEST 14 — Inter-city query (Trichy → Chennai)
# ─────────────────────────────────────────────────────────────
section("TEST 14 · INTER-CITY ROUTE QUERIES")

def find_inter_city(from_city_key, to_city_key):
    found = []
    for city_key in [from_city_key, to_city_key]:
        city = data["cities"].get(city_key, {})
        for cat, routes in city.get("routes", {}).items():
            for route in routes:
                cities_in_stops = set()
                for stop in route["stops"]:
                    lat, lng = stop["lat"], stop["lng"]
                    # rough bounding box detection
                    if 12.5 < lat < 13.4 and 79.8 < lng < 80.5:
                        cities_in_stops.add("chennai")
                    if 10.5 < lat < 11.1 and 78.4 < lng < 79.1:
                        cities_in_stops.add("tiruchirappalli")
                if from_city_key in cities_in_stops and to_city_key in cities_in_stops:
                    found.append(route)
    return found

routes = find_inter_city("tiruchirappalli", "chennai")
if routes:
    ok(f"Trichy ↔ Chennai inter-city routes: {len(routes)}")
    for r in routes:
        ok(f"  {r['route_number']}: {r['name']} ({r['fare_range'] if 'fare_range' in r else str(r['fare_min'])+'–'+str(r['fare_max'])})")
else:
    fail("No inter-city routes found between Trichy and Chennai")

# ─────────────────────────────────────────────────────────────
# TEST 15 — Frequency / wait time ranking
# ─────────────────────────────────────────────────────────────
section("TEST 15 · FREQUENCY RANKING (Best frequency routes)")

print(f"\n  Chennai — Top 5 most frequent:")
chn_routes = [r for cat in data["cities"]["chennai"]["routes"].values() for r in cat]
for r in sorted(chn_routes, key=lambda x: x["frequency_min"])[:5]:
    ok(f"    {r['route_number']} ({r['name'][:40]}): every {r['frequency_min']}min")

print(f"\n  Trichy — Top 5 most frequent:")
trc_routes = [r for cat in data["cities"]["tiruchirappalli"]["routes"].values() for r in cat]
for r in sorted(trc_routes, key=lambda x: x["frequency_min"])[:5]:
    ok(f"    {r['route_number']} ({r['name'][:40]}): every {r['frequency_min']}min")

# ─────────────────────────────────────────────────────────────
# TEST 16 — AC Route detection
# ─────────────────────────────────────────────────────────────
section("TEST 16 · AC ROUTE DETECTION")
ac_routes = [r for r in all_routes.values() if r.get("ac") is True]
non_ac    = [r for r in all_routes.values() if r.get("ac") is False]
ok(f"AC routes: {len(ac_routes)} — {[r['route_number'] for r in ac_routes]}")
ok(f"Non-AC routes: {len(non_ac)}")

# ─────────────────────────────────────────────────────────────
# TEST 17 — Multi-stop route (longest routes)
# ─────────────────────────────────────────────────────────────
section("TEST 17 · LONGEST ROUTES (by distance)")
sorted_dist = sorted(all_routes.values(), key=lambda x: x.get("distance_km", 0), reverse=True)
for r in sorted_dist[:8]:
    ok(f"  {r['route_id']}: {r['distance_km']}km — {r['name']}")

# ─────────────────────────────────────────────────────────────
# TEST 18 — Last-mile connectivity simulation
# ─────────────────────────────────────────────────────────────
section("TEST 18 · LAST-MILE CONNECTIVITY (airport links)")

airports = {
    "chennai": {"lat": 12.9941, "lng": 80.1709},
    "tiruchirappalli": {"lat": 10.7654, "lng": 78.7094},
}
for city_key, apt in airports.items():
    city = data["cities"][city_key]
    city_name = city["name"]
    stops = nearest_stops(apt["lat"], apt["lng"], city_key, top_n=3)
    if stops:
        ok(f"  {city_name} Airport — nearest transit stops:")
        for s in stops:
            print(f"      → {s['name']} ({s['dist']} km, {s['route']})")
    else:
        fail(f"  No transit near {city_name} airport")

# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
section("TEST SUMMARY")
total_tests = results["pass"] + results["fail"] + results["warn"]
print(f"\n  Total checks : {total_tests}")
print(f"  {PASS} Passed      : {results['pass']}")
print(f"  {FAIL} Failed      : {results['fail']}")
print(f"  {WARN} Warnings    : {results['warn']}")
print(f"\n  Routes in dataset   : {len(all_routes)}")
print(f"  Cities covered      : Chennai, Tiruchirappalli")
print(f"  Transport modes     : City Bus, AC Volvo, Metro (CMRL),")
print(f"                        MRTS, Suburban Rail, Feeder,")
print(f"                        Inter-district Express")
print()

if results["fail"] == 0:
    print(f"\033[92m  ✓ ALL TESTS PASSED — Dataset ready for YatrAI\033[0m\n")
else:
    print(f"\033[91m  ✗ {results['fail']} FAILURES — Fix before deploying\033[0m\n")

sys.exit(0 if results["fail"] == 0 else 1)

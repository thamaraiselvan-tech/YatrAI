"""Test all API endpoints including new /api/places, /api/nearest, /api/coordinates."""
import sys
sys.path.insert(0, '.')
import httpx

BASE = "http://localhost:8000"

def test(name, method, path, body=None, expect_key=None):
    try:
        if method == "GET":
            r = httpx.get(f"{BASE}{path}", timeout=10)
        else:
            r = httpx.post(f"{BASE}{path}", json=body, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if expect_key:
                assert expect_key in data, f"Missing key: {expect_key}"
            print(f"  PASS  {name} ({r.status_code})")
            return data
        else:
            print(f"  FAIL  {name} ({r.status_code}: {r.text[:100]})")
            return None
    except Exception as e:
        print(f"  FAIL  {name} ({e})")
        return None

print("=== YatrAI Expanded API Tests ===\n")

# 1. Status
test("GET /api/status", "GET", "/api/status", expect_key="status")

# 2. Places search
data = test("GET /api/places?q=temple", "GET", "/api/places?q=temple&city=Chennai", expect_key="places")
if data:
    print(f"         Found {len(data['places'])} temples in Chennai")

# 3. Places by category
data = test("GET /api/places?category=mall", "GET", "/api/places?category=mall", expect_key="places")
if data:
    print(f"         Found {len(data['places'])} malls total")

# 4. Nearest node
data = test("GET /api/nearest (Mylapore)", "GET", "/api/nearest?lat=13.0337&lng=80.2694", expect_key="node")
if data:
    print(f"         Nearest: {data['name']} ({data['distance_m']}m)")

# 5. All coordinates
data = test("GET /api/coordinates", "GET", "/api/coordinates", expect_key="coordinates")
if data:
    print(f"         Total coordinates: {len(data['coordinates'])}")

# 6. Route: Mylapore Temple to Srirangam Temple (cross-city)
data = test("POST /api/plan (Temple to Temple)", "POST", "/api/plan", 
            body={"query": "from Mylapore temple to Srirangam temple, cheapest route"},
            expect_key="routes")
if data:
    for mood, route in data.get("routes", {}).items():
        print(f"         {mood}: {route['total_time']}min, Rs.{route['total_fare']}, {len(route['segments'])} segments")

# 7. Route: Trichy local
data = test("POST /api/plan (Trichy local)", "POST", "/api/plan",
            body={"query": "from rockfort to NIT Trichy, fastest"},
            expect_key="routes")
if data:
    for mood, route in data.get("routes", {}).items():
        print(f"         {mood}: {route['total_time']}min, Rs.{route['total_fare']}")

# 8. Wallet
test("GET /api/wallet", "GET", "/api/wallet", expect_key="balance")

# 9. Disruptions  
test("GET /api/disruptions", "GET", "/api/disruptions", expect_key="disrupted_modes")

print("\n=== All tests complete ===")

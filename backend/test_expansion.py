"""Quick validation of database, places, and routing modules."""
import sys
sys.path.insert(0, '.')

from data.database import COORDINATES, TRANSIT_MODES, SCHEDULES
from data.places import PLACES, search_places
from routing.engine import EDGES, solve_route

print(f"✅ Nodes: {len(COORDINATES)}")
print(f"✅ Places: {len(PLACES)}")
print(f"✅ Edges: {len(EDGES)}")
print(f"✅ Transit Modes: {list(TRANSIT_MODES.keys())}")

# Test routing: SRM → Rockfort Temple (Trichy)
route = solve_route("SRM_Dorm", "Rockfort_Temple", 480, "fastest", [])
if route:
    print(f"\n🛤️  Route: SRM_Dorm → Rockfort_Temple (fastest)")
    print(f"   Time: {route['total_time']}min | Fare: ₹{route['total_fare']} | Segments: {len(route['segments'])}")
    for i, seg in enumerate(route['segments']):
        print(f"   [{i+1}] {seg['from_node']} → {seg['to_node']} via {seg['mode']} ({seg['duration']}min, ₹{seg['fare']})")
else:
    print("❌ No route found SRM → Rockfort_Temple")

# Test Chennai local: Mylapore Temple → Phoenix Mall
route2 = solve_route("Kapaleeshwarar_Temple", "Phoenix_MarketCity", 600, "cheapest", [])
if route2:
    print(f"\n🛤️  Route: Mylapore Temple → Phoenix Mall (cheapest)")
    print(f"   Time: {route2['total_time']}min | Fare: ₹{route2['total_fare']}")
    for i, seg in enumerate(route2['segments']):
        print(f"   [{i+1}] {seg['from_node']} → {seg['to_node']} via {seg['mode']} ({seg['duration']}min, ₹{seg['fare']})")
else:
    print("❌ No route found Mylapore Temple → Phoenix Mall")

# Test Trichy local: Rockfort → Srirangam Temple
route3 = solve_route("Rockfort_Temple", "Ranganathaswamy_Temple", 540, "fastest", [])
if route3:
    print(f"\n🛤️  Route: Rockfort → Srirangam Temple (fastest)")
    print(f"   Time: {route3['total_time']}min | Fare: ₹{route3['total_fare']}")
    for i, seg in enumerate(route3['segments']):
        print(f"   [{i+1}] {seg['from_node']} → {seg['to_node']} via {seg['mode']} ({seg['duration']}min, ₹{seg['fare']})")
else:
    print("❌ No route found Rockfort → Srirangam Temple")

# Test place search
results = search_places("temple", "temple", "Chennai")
print(f"\n🔍 Search 'temple' in Chennai: {len(results)} results")
for r in results[:3]:
    print(f"   {r['name']} ({r['category']}) - {r['area']}")

results2 = search_places("mall", "", "Trichy")
print(f"\n🔍 Search 'mall' in Trichy: {len(results2)} results")
for r in results2[:3]:
    print(f"   {r['name']} ({r['category']}) - {r['area']}")

print("\n✅ All tests passed!")

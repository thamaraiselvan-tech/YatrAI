import sys
import json
from routing.engine import solve_route
from data.dataset_loader import resolve_node_id, load_dataset

def test_intercity():
    # Load dataset
    data = load_dataset()
        
    trichy = data["cities"]["tiruchirappalli"]
    intercity_routes = trichy["routes"]["inter_district"]
    
    print(f"Loaded {len(intercity_routes)} Inter-City routes.")
    
    passed = 0
    failed = 0
    failed_details = []
    
    for r in intercity_routes:
        rid = r["route_id"]
        rnum = r["route_number"]
        name = r["name"]
        stops = r["stops"]
        
        if len(stops) < 2:
            print(f"⚠️ Route {rid} ({name}) has less than 2 stops.")
            continue
            
        start_stop = stops[0]["name"]
        end_stop = stops[-1]["name"]
        
        start_node = resolve_node_id(start_stop)
        end_node = resolve_node_id(end_stop)
        
        # Test finding route from start_node to end_node
        route = solve_route(start_node, end_node, 480, "fastest", [])
        
        if route:
            passed += 1
            print(f"✅ Resolved path for {name} ({rid}): {start_node} -> {end_node} | {route['total_time']} min | Segments: {len(route['segments'])}")
        else:
            failed += 1
            failed_details.append((rid, rnum, name, start_node, end_node))
            print(f"❌ Failed to solve path for {name} ({rid}): {start_node} -> {end_node}")
            
    print(f"\n--- INTERCITY TEST SUMMARY ---")
    print(f"Total Intercity Routes Tested: {len(intercity_routes)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n🎉 All intercity routes solved successfully!")
        sys.exit(0)

if __name__ == "__main__":
    test_intercity()

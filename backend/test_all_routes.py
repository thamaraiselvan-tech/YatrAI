import sys
import json
from routing.engine import solve_route
from data.dataset_loader import resolve_node_id, load_dataset

def test_all():
    # Load dataset
    data = load_dataset()
        
    trichy = data["cities"]["tiruchirappalli"]
    
    all_trichy_routes = []
    for category, routes in trichy["routes"].items():
        for r in routes:
            all_trichy_routes.append(r)
            
    print(f"Loaded {len(all_trichy_routes)} Trichy routes.")
    
    passed = 0
    failed = 0
    failed_details = []
    
    for r in all_trichy_routes:
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
        
        # Test finding route from start_node to end_node at 8:00 AM (480 minutes)
        # Using "fastest" mood
        route = solve_route(start_node, end_node, 480, "fastest", [])
        
        if route:
            passed += 1
        else:
            failed += 1
            failed_details.append((rid, rnum, name, start_node, end_node))
            print(f"❌ Route {rid} ({rnum}) failed to solve: {start_node} -> {end_node}")
            
    print(f"\n--- TEST SUMMARY ---")
    print(f"Total Routes Tested: {len(all_trichy_routes)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed Routes List:")
        for fd in failed_details:
            print(f"- {fd[0]} ({fd[1]}): {fd[2]} [From: {fd[3]} -> To: {fd[4]}]")
        sys.exit(1)
    else:
        print("\n🎉 All Trichy routes verified successfully!")
        sys.exit(0)

if __name__ == "__main__":
    test_all()

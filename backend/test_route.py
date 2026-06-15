from routing.engine import solve_route
r = solve_route("SRM_Dorm", "Chennai_Central", 480, "fastest", [])
if r:
    print(f"Route found! Time: {r['total_time']}min, Fare: Rs{r['total_fare']}, Segments: {len(r['segments'])}")
    for s in r['segments']:
        print(f"  {s['from_node']} -> {s['to_node']} via {s['mode']} ({s['duration']}min, Rs{s['fare']})")
else:
    print("No route found")

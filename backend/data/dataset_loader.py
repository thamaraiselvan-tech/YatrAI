import os
import json
import math
from typing import Dict, Tuple, List, Any

# Map of raw stop names in JSON to database node IDs to prevent duplicates and keep compatibility
NODE_MAP = {
    "Chennai Central": "Chennai_Central",
    "Egmore": "Chennai_Egmore",
    "Chennai Beach": "Chennai_Beach",
    "Chennai Fort": "Chennai_Fort",
    "Koyambedu CMBT": "Koyambedu_CMBT",
    "Koyambedu CMBT Chennai": "Koyambedu_CMBT",
    "CMBT / Koyambedu": "Koyambedu_CMBT",
    "Koyambedu": "Koyambedu_CMBT",
    "Tambaram": "Tambaram_Station",
    "Guindy": "Guindy_Station",
    "Guindy Metro": "Guindy_Metro",
    "St. Thomas Mount": "St_Thomas_Mount",
    "St. Thomas Mount Metro": "St_Thomas_Mount",
    "Kattankulathur": "Kattankulathur_Station",
    "Potheri": "Potheri_Station",
    "Central Bus Stand": "Central_Bus_Stand_Trichy",
    "Central Bus Stand Trichy": "Central_Bus_Stand_Trichy",
    "Chathiram": "Chattram_Bus_Stand",
    "Chathiram Bus Stand": "Chattram_Bus_Stand",
    "Srirangam": "Srirangam_Station",
    "Srirangam Bus Stand": "Srirangam_Station",
    "Trichy Junction": "Trichy_Junction",
    "Trichy Airport": "Trichy_Airport",
    "Chennai Airport": "Airport",
    "Chennai Airport T1": "Airport",
    "Chennai Airport T2": "Airport",
    "NIT Trichy / Kattur": "NIT_Trichy",
    "Kattur / NIT Trichy": "NIT_Trichy",
    "T.Nagar": "T_Nagar",
    "AG-DMS": "AG_DMS",
    "BHEL Trichy": "BHEL_Township",
    "BHEL": "BHEL_Township",
    "Golden Rock": "Golden_Rock",
    "Ponmalai": "Golden_Rock",
}

def resolve_node_id(stop_name: str) -> str:
    """Resolve a raw stop name to a standard database node ID."""
    name = stop_name.strip()
    if name in NODE_MAP:
        return NODE_MAP[name]
    
    # Generic normalization: remove special characters, replace spaces/dashes with underscores
    clean = name.replace(" ", "_").replace("'", "").replace(".", "").replace("-", "_").replace("(", "").replace(")", "")
    return clean

def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Calculate the haversine distance in km between two (lat, lon) points."""
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return 6371.0 * c

def load_dataset() -> Dict[str, Any]:
    """Search for and load the chennai_trichy_dataset.json file."""
    paths = [
        "chennai_trichy_dataset.json",
        "../chennai_trichy_dataset.json",
        "../../chennai_trichy_dataset.json",
        os.path.join(os.path.dirname(__file__), "..", "chennai_trichy_dataset.json"),
        os.path.join(os.path.dirname(__file__), "..", "..", "chennai_trichy_dataset.json"),
        os.path.join(os.path.dirname(__file__), "chennai_trichy_dataset.json"),
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError("Could not locate chennai_trichy_dataset.json")

def parse_time_to_min(time_str: str) -> int:
    """Convert 'HH:MM' string to minutes from midnight."""
    parts = time_str.split(":")
    if len(parts) != 2:
        return 480  # fallback: 8:00 AM
    return int(parts[0]) * 60 + int(parts[1])

def get_backend_transit_mode(category: str, operator: str, route_type: str) -> str:
    """Map route properties from the dataset to backend transit modes."""
    op = operator.upper()
    rt = route_type.lower()
    cat = category.lower()

    if cat == "metro" or rt == "metro":
        return "Metro"
    if cat in ("suburban_rail", "mrts") or rt in ("suburban_rail", "mrts"):
        return "Suburban_Train"
    if cat == "inter_district" or (op == "TNSTC" and rt == "express"):
        return "SETC_Bus"
    if op == "MTC":
        return "MTC_Bus"
    if op in ("TNSTC CITY BUS", "CITY BUS TRICHY") or cat == "city_bus":
        return "Town_Bus"
    if op == "SOUTHERN RAILWAY" and rt != "suburban_rail":
        return "Intercity_Train"
    
    return "MTC_Bus"

def get_friendly_line_name(category: str, operator: str, route_number: str, route_type: str) -> str:
    """Format a clean, user-friendly line name for displaying/routing."""
    op = operator.upper()
    rt = route_type.lower()
    cat = category.lower()
    num = route_number

    if cat == "metro":
        return f"CMRL {num}"
    if cat == "suburban_rail":
        return f"Suburban Rail {num}"
    if cat == "mrts":
        return f"MRTS {num}"
    if op == "MTC" and rt == "ac_volvo":
        return f"AC Volvo {num}"
    if op == "MTC":
        return f"Bus {num}"
    if op in ("TNSTC", "TNSTC CITY BUS", "CITY BUS TRICHY"):
        if cat == "inter_district" or rt == "express":
            return f"Express Bus {num}"
        return f"Town Bus {num}"
    
    return f"{operator} {num}"

def load_and_merge_data(
    base_coordinates: Dict[str, Tuple[float, float]],
    base_places: Dict[str, Dict[str, Any]],
    base_schedules: Dict[str, Dict[str, List[int]]],
    base_edges: List[Tuple[str, str, str, str, float]]
) -> Tuple[
    Dict[str, Tuple[float, float]],
    Dict[str, Dict[str, Any]],
    Dict[str, Dict[str, List[int]]],
    List[Tuple[str, str, str, str, float]]
]:
    """
    Parse the chennai_trichy_dataset.json and merge it with our hardcoded database.
    Dynamically generates edges and schedules.
    """
    try:
        data = load_dataset()
    except Exception as e:
        print(f"[Warning] Failed to load dataset: {e}. Using base database.")
        return base_coordinates, base_places, base_schedules, base_edges

    # 1. Clone base structures
    merged_coordinates = dict(base_coordinates)
    merged_places = dict(base_places)
    merged_schedules = dict(base_schedules)
    
    # Store route edges in a set to avoid duplicate route lines
    edges_set = set()
    for edge in base_edges:
        u, v, mode, line, dist = edge
        # Normalize order to avoid duplicates (bidirectional representation)
        key = (min(u, v), max(u, v), mode, line)
        edges_set.add((u, v, mode, line, dist))

    # 2. Iterate through cities and routes in JSON
    for city_key, city in data["cities"].items():
        city_name = "Chennai" if city_key == "chennai" else "Trichy"
        
        for cat_key, routes in city.get("routes", {}).items():
            for r in routes:
                route_id = r["route_id"]
                route_number = r["route_number"]
                route_name = r["name"]
                operator = r["operator"]
                route_type = r["type"]
                stops = r.get("stops", [])

                if len(stops) < 2:
                    continue

                mode = get_backend_transit_mode(cat_key, operator, route_type)
                line_name = get_friendly_line_name(cat_key, operator, route_number, route_type)

                # Process schedules
                first_min = parse_time_to_min(r.get("first_bus", "05:00"))
                last_min = parse_time_to_min(r.get("last_bus", "22:00"))
                freq = r.get("frequency_min", 15)
                if freq <= 0:
                    freq = 15
                
                departures = list(range(first_min, last_min + 1, freq))
                
                # Determine schedule mode key
                if mode == "MTC_Bus":
                    sched_key = line_name.replace(" ", "_")
                else:
                    sched_key = mode
                
                if sched_key not in merged_schedules:
                    merged_schedules[sched_key] = {}

                # Resolve and register all stops in coordinates and places
                resolved_stops = []
                for s in stops:
                    stop_name = s["name"]
                    node_id = resolve_node_id(stop_name)
                    lat, lng = s["lat"], s["lng"]
                    
                    # Update coordinates
                    if node_id not in merged_coordinates:
                        merged_coordinates[node_id] = (lat, lng)
                    
                    # Update places
                    if node_id not in merged_places:
                        merged_places[node_id] = {
                            "name": stop_name,
                            "tamil_name": "", # can be populated later
                            "category": "station",
                            "sub_category": "bus_stand" if "bus" in mode.lower() else ("metro" if mode == "Metro" else "railway"),
                            "city": city_name,
                            "area": city_name,
                            "tags": [mode.lower(), cat_key.lower()],
                        }
                    
                    resolved_stops.append(node_id)
                    
                    # Save schedule departures for this stop
                    if node_id not in merged_schedules[sched_key]:
                        merged_schedules[sched_key][node_id] = departures
                    else:
                        # Merge and keep departures unique and sorted
                        merged_deps = sorted(list(set(merged_schedules[sched_key][node_id] + departures)))
                        merged_schedules[sched_key][node_id] = merged_deps

                # Generate route edges between consecutive stops
                for i in range(len(resolved_stops) - 1):
                    u = resolved_stops[i]
                    v = resolved_stops[i+1]
                    if u == v:
                        continue
                    
                    coord_u = merged_coordinates[u]
                    coord_v = merged_coordinates[v]
                    dist = round(haversine_distance(coord_u, coord_v), 3)
                    if dist <= 0:
                        dist = 0.1
                    
                    edges_set.add((u, v, mode, line_name, dist))

    # 3. Dynamically add walk, rapido, and auto edges between all close node pairs
    # Compute all coordinates list to build distance matrix
    nodes = list(merged_coordinates.keys())
    coords = [merged_coordinates[n] for n in nodes]
    
    # Store existing connections in a fast-lookup dict to avoid adding walk/bike edges if direct transit already exists
    transit_connections = {}
    for edge in edges_set:
        u, v, mode, line, dist = edge
        key = (min(u, v), max(u, v))
        if key not in transit_connections:
            transit_connections[key] = set()
        transit_connections[key].add(mode)

    # Thresholds: walk <= 1.2 km, bike/auto <= 8.0 km
    for i in range(len(nodes)):
        node_i = nodes[i]
        coord_i = coords[i]
        
        for j in range(i + 1, len(nodes)):
            node_j = nodes[j]
            coord_j = coords[j]
            
            # Simple bounding box check before heavy haversine calculation
            if abs(coord_i[0] - coord_j[0]) > 0.1 or abs(coord_i[1] - coord_j[1]) > 0.1:
                continue
                
            dist = haversine_distance(coord_i, coord_j)
            
            # Walk edge (up to 1.2km)
            if dist <= 1.2:
                key = (min(node_i, node_j), max(node_i, node_j))
                # Add Walk edge if it doesn't exist yet
                if "Walk" not in transit_connections.get(key, set()):
                    edges_set.add((node_i, node_j, "Walk", "Walk", round(dist, 3)))
            
            # Bike and Auto edges (up to 8.0km)
            if dist <= 8.0:
                key = (min(node_i, node_j), max(node_i, node_j))
                modes = transit_connections.get(key, set())
                
                if "Rapido_Bike" not in modes:
                    edges_set.add((node_i, node_j, "Rapido_Bike", "Rapido Bike", round(dist, 3)))
                if "Ola_Auto" not in modes:
                    edges_set.add((node_i, node_j, "Ola_Auto", "Ola Auto", round(dist, 3)))

    return merged_coordinates, merged_places, merged_schedules, list(edges_set)

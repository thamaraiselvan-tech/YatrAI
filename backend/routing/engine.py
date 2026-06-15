import heapq
from typing import List, Dict, Any, Tuple, Optional
from data.database import COORDINATES, TRANSIT_MODES, SCHEDULES, haversine_distance, get_traffic_factor, get_next_departure

# ══════════════════════════════════════════════════════════════════════════════
# 400+ EDGES — Complete Chennai & Trichy Transit Network
# Format: (from_node, to_node, mode, line_name, distance_km)
# ══════════════════════════════════════════════════════════════════════════════
EDGES = [

    # ═══════════════════════════════════════════════════════════════════════════
    # SRM CAMPUS ORIGIN CONNECTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    ("SRM_Dorm",        "Potheri_Station",       "Walk",       "Walk to Potheri",           0.2),
    ("SRM_Main_Gate",   "Potheri_Station",       "Walk",       "Walk to Potheri",           0.3),
    ("SRM_Tech_Park",   "Potheri_Station",       "Walk",       "Walk to Potheri",           0.4),
    ("SRM_Dorm",        "Potheri_Station",       "Rapido_Bike","Rapido Bike",               0.2),
    ("SRM_Dorm",        "Kattankulathur_Station","Walk",       "Walk to Kattankulathur",    1.2),
    ("SRM_Dorm",        "Kattankulathur_Station","Rapido_Bike","Rapido Bike",               1.2),
    ("SRM_Dorm",        "Kilambakkam_KCBT",      "MTC_Bus",    "Bus 500C",                  6.0),
    ("SRM_Dorm",        "Kilambakkam_KCBT",      "Rapido_Bike","Rapido Bike",               6.0),
    ("SRM_Dorm",        "GST_Paranur_Toll",      "Rapido_Bike","Rapido Bike",               4.2),
    ("SRM_Main_Gate",   "Kattankulathur_Station","Rapido_Bike","Rapido Bike",               1.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # SOUTHERN RAILWAY — CHENGALPATTU–POTHERI–TAMBARAM LINE
    # ═══════════════════════════════════════════════════════════════════════════
    ("Chengalpattu",          "Singaperumal_Koil",    "Suburban_Train","Suburban Rail",  6.0),
    ("Singaperumal_Koil",     "Maraimalai_Nagar",     "Suburban_Train","Suburban Rail",  3.5),
    ("Maraimalai_Nagar",      "Guduvanchery",         "Suburban_Train","Suburban Rail",  4.0),
    ("Guduvanchery",          "Urapakkam",            "Suburban_Train","Suburban Rail",  4.0),
    ("Urapakkam",             "Vandalur",             "Suburban_Train","Suburban Rail",  3.5),
    ("Vandalur",              "Perungalathur",        "Suburban_Train","Suburban Rail",  3.0),
    ("Perungalathur",         "Sembakkam",            "Suburban_Train","Suburban Rail",  2.5),
    ("Sembakkam",             "Potheri_Station",      "Suburban_Train","Suburban Rail",  2.0),
    ("Potheri_Station",       "Kattankulathur_Station","Suburban_Train","Suburban Rail", 1.8),
    ("Kattankulathur_Station","Chrompet",             "Suburban_Train","Suburban Rail",  4.5),
    ("Chrompet",              "Pallavaram",           "Suburban_Train","Suburban Rail",  2.5),
    ("Pallavaram",            "Tambaram_Station",     "Suburban_Train","Suburban Rail",  3.0),

    # ─ GST Road Bus Parallel (Potheri ↔ Tambaram) ───────────────────────────
    ("Potheri_Station",       "Tambaram_Station",     "MTC_Bus",   "Bus 500C",         12.0),
    ("Potheri_Station",       "Tambaram_Station",     "Rapido_Bike","Rapido Bike",      12.0),
    ("Potheri_Station",       "Tambaram_Station",     "Ola_Auto",  "Ola Auto",         12.0),
    ("Kattankulathur_Station","Tambaram_Station",     "MTC_Bus",   "Bus 500C",         10.5),
    ("Kattankulathur_Station","Tambaram_Station",     "Rapido_Bike","Rapido Bike",      10.5),
    ("Tambaram_Station",      "Kilambakkam_KCBT",     "MTC_Bus",   "Bus 500C",          8.0),
    ("Tambaram_Station",      "Kilambakkam_KCBT",     "Rapido_Bike","Rapido Bike",       8.0),
    ("Potheri_Station",       "Kilambakkam_KCBT",     "MTC_Bus",   "Bus 500C",          6.0),
    ("Perungalathur",         "Kilambakkam_KCBT",     "MTC_Bus",   "Bus 502",           3.5),
    ("Vandalur",              "Kilambakkam_KCBT",     "Rapido_Bike","Rapido Bike",       3.5),

    # ─ GST Road Express Buses ────────────────────────────────────────────────
    ("Koyambedu_CMBT",        "Tambaram_Station",     "MTC_Bus",   "Bus 502",          25.0),
    ("Koyambedu_CMBT",        "Kilambakkam_KCBT",     "MTC_Bus",   "Bus 500C",         32.0),
    ("Koyambedu_CMBT",        "Vandalur",             "MTC_Bus",   "Bus 500",          22.0),
    ("Koyambedu_CMBT",        "GST_Paranur_Toll",     "MTC_Bus",   "Bus 502A",         28.0),
    ("Tambaram_Station",      "Tambaram_West",        "Walk",      "Walk to West",      0.8),
    ("Tambaram_Station",      "Tambaram_West",        "Rapido_Bike","Rapido Bike",       0.8),

    # ═══════════════════════════════════════════════════════════════════════════
    # SOUTHERN RAILWAY — TAMBARAM → GUINDY → CENTRAL (Main South Corridor)
    # ═══════════════════════════════════════════════════════════════════════════
    ("Tambaram_Station",  "Chrompet",         "Suburban_Train","Suburban Rail",   4.0),
    ("Chrompet",          "Pallavaram",        "Suburban_Train","Suburban Rail",   2.5),
    ("Pallavaram",        "St_Thomas_Mount",   "Suburban_Train","Suburban Rail",   4.5),
    ("St_Thomas_Mount",   "Guindy_Station",    "Suburban_Train","Suburban Rail",   3.0),
    ("Guindy_Station",    "Saidapet",          "Suburban_Train","Suburban Rail",   2.0),
    ("Saidapet",          "Mambalam",          "Suburban_Train","Suburban Rail",   2.5),
    ("Mambalam",          "Kodambakkam",       "Suburban_Train","Suburban Rail",   2.0),
    ("Kodambakkam",       "Nungambakkam",      "Suburban_Train","Suburban Rail",   1.8),
    ("Nungambakkam",      "Chetpet",           "Suburban_Train","Suburban Rail",   1.5),
    ("Chetpet",           "Chennai_Egmore",    "Suburban_Train","Suburban Rail",   2.0),
    ("Chennai_Egmore",    "Park_Town",         "Suburban_Train","Suburban Rail",   1.5),
    ("Park_Town",         "Chennai_Fort",      "Suburban_Train","Suburban Rail",   1.0),
    ("Chennai_Fort",      "Chennai_Beach",     "Suburban_Train","Suburban Rail",   1.5),
    ("Chennai_Egmore",    "Chennai_Central",   "Suburban_Train","Suburban Rail",   2.5),
    ("Guindy_Station",    "Chennai_Central",   "Suburban_Train","Suburban Rail",  14.0),
    ("Tambaram_Station",  "Chennai_Central",   "Suburban_Train","Suburban Rail",  27.0),

    # ─ Parallel Bus (Tambaram ↔ Central via Mount) ───────────────────────────
    ("Tambaram_Station",  "Guindy_Station",    "MTC_Bus",   "Bus 21",           13.0),
    ("Tambaram_Station",  "Guindy_Station",    "Rapido_Bike","Rapido Bike",      13.0),
    ("Tambaram_Station",  "Guindy_Station",    "Ola_Auto",  "Ola Auto",         13.0),
    ("Guindy_Station",    "Chennai_Central",   "MTC_Bus",   "Bus 21G",          14.0),
    ("Guindy_Station",    "Chennai_Egmore",    "MTC_Bus",   "Bus 21G",          10.0),
    ("Tambaram_Station",  "Chennai_Egmore",    "MTC_Bus",   "Bus 21D",          26.0),
    ("Pallavaram",        "Guindy_Station",    "MTC_Bus",   "Bus 21",            8.5),
    ("Chrompet",          "Guindy_Station",    "MTC_Bus",   "Bus 21",           10.5),
    ("Chrompet",          "Guindy_Station",    "Rapido_Bike","Rapido Bike",      10.5),
    ("Saidapet",          "Chennai_Central",   "MTC_Bus",   "Bus 5",             8.5),
    ("Saidapet",          "Chennai_Central",   "Rapido_Bike","Rapido Bike",       8.5),

    # ═══════════════════════════════════════════════════════════════════════════
    # CMRL METRO — BLUE LINE (Airport ↔ Chennai Central ↔ Wimco Nagar)
    # ═══════════════════════════════════════════════════════════════════════════
    ("Airport",          "Meenambakkam",      "Metro","CMRL Blue Line",  2.0),
    ("Meenambakkam",     "Nanganallur_Road",  "Metro","CMRL Blue Line",  1.8),
    ("Nanganallur_Road", "Alandur",           "Metro","CMRL Blue Line",  2.0),
    ("Alandur",          "St_Thomas_Mount",   "Metro","CMRL Blue Line",  2.5),
    ("St_Thomas_Mount",  "Guindy_Station",    "Metro","CMRL Blue Line",  2.0),
    ("Guindy_Station",   "Ekkatuthangal",     "Metro","CMRL Blue Line",  1.5),
    ("Ekkatuthangal",    "Little_Mount",      "Metro","CMRL Blue Line",  1.5),
    ("Little_Mount",     "Saidapet",          "Metro","CMRL Blue Line",  1.8),
    ("Saidapet",         "Nandanam",          "Metro","CMRL Blue Line",  2.0),
    ("Nandanam",         "Teynampet",         "Metro","CMRL Blue Line",  1.5),
    ("Teynampet",        "AG_DMS",            "Metro","CMRL Blue Line",  1.5),
    ("AG_DMS",           "Thousand_Lights",   "Metro","CMRL Blue Line",  1.2),
    ("Thousand_Lights",  "LIC",               "Metro","CMRL Blue Line",  1.2),
    ("LIC",              "Chennai_Egmore",    "Metro","CMRL Blue Line",  1.5),
    ("Chennai_Egmore",   "Chennai_Central",   "Metro","CMRL Blue Line",  2.0),
    ("Chennai_Central",  "High_Court",        "Metro","CMRL Blue Line",  1.2),
    ("High_Court",       "Mannadi",           "Metro","CMRL Blue Line",  1.0),
    ("Mannadi",          "Washermenpet",      "Metro","CMRL Blue Line",  2.0),
    ("Washermenpet",     "Tondiarpet",        "Metro","CMRL Blue Line",  2.5),
    ("Tondiarpet",       "Tiruvottiyur",      "Metro","CMRL Blue Line",  3.5),
    ("Tiruvottiyur",     "Wimco_Nagar",       "Metro","CMRL Blue Line",  2.5),

    # Express Metro shortcuts
    ("Airport",          "Guindy_Station",    "Metro","CMRL Blue Line",  8.0),
    ("Airport",          "Chennai_Central",   "Metro","CMRL Blue Line", 21.0),
    ("Guindy_Station",   "Chennai_Central",   "Metro","CMRL Blue Line", 14.0),
    ("Chennai_Central",  "Wimco_Nagar",       "Metro","CMRL Blue Line", 18.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # CMRL METRO — GREEN LINE (CMBT ↔ Vadapalani ↔ Alandur)
    # ═══════════════════════════════════════════════════════════════════════════
    ("Koyambedu_CMBT",   "Arumbakkam",        "Metro","CMRL Green Line", 1.5),
    ("Arumbakkam",       "Vadapalani",        "Metro","CMRL Green Line", 2.0),
    ("Vadapalani",       "Ashok_Nagar",       "Metro","CMRL Green Line", 1.5),
    ("Ashok_Nagar",      "Ekkatuthangal",     "Metro","CMRL Green Line", 1.2),
    ("Ekkatuthangal",    "Alandur",           "Metro","CMRL Green Line", 1.5),
    ("Koyambedu_CMBT",   "Guindy_Station",    "Metro","CMRL Green Line",10.0),

    # ─ Metro Walk Transfers ───────────────────────────────────────────────────
    ("Guindy_Station",   "OMR_Tidel_Park",    "Walk","Guindy Skywalk Link",  0.5),
    ("Velachery",        "OMR_Tidel_Park",    "Walk","Velachery Skywalk Link",1.5),
    ("Adyar",            "OMR_Tidel_Park",    "Walk","Adyar Bridge Walk",    2.0),
    ("Chennai_Central",  "Chennai_Egmore",    "Walk","Central–Egmore Walk",  1.2),
    ("Alandur",          "St_Thomas_Mount",   "Walk","Alandur Walk",         0.8),
    ("Saidapet",         "Little_Mount",      "Walk","Saidapet–Little Mount", 0.8),

    # ═══════════════════════════════════════════════════════════════════════════
    # SOUTHERN RAILWAY — NORTHERN LINE (Beach → Central → Perambur → Avadi)
    # ═══════════════════════════════════════════════════════════════════════════
    ("Chennai_Beach",    "Chennai_Fort",      "Suburban_Train","Suburban Rail",  1.5),
    ("Chennai_Fort",     "Basin_Bridge",      "Suburban_Train","Suburban Rail",  1.8),
    ("Basin_Bridge",     "Perambur",          "Suburban_Train","Suburban Rail",  2.5),
    ("Perambur",         "Vyasarpadi",        "Suburban_Train","Suburban Rail",  1.5),
    ("Vyasarpadi",       "Villivakkam",       "Suburban_Train","Suburban Rail",  2.0),
    ("Villivakkam",      "Korattur",          "Suburban_Train","Suburban Rail",  2.5),
    ("Korattur",         "Ambattur",          "Suburban_Train","Suburban Rail",  3.0),
    ("Ambattur",         "Pattabiram",        "Suburban_Train","Suburban Rail",  4.0),
    ("Pattabiram",       "Avadi",             "Suburban_Train","Suburban Rail",  4.0),
    ("Avadi",            "Arakkonam",         "Suburban_Train","Suburban Rail", 55.0),
    ("Avadi",            "Tiruttani",         "Suburban_Train","Suburban Rail", 85.0),
    ("Perambur",         "Kolathur",          "Suburban_Train","Suburban Rail",  2.8),
    ("Kolathur",         "Madhavaram",        "Suburban_Train","Suburban Rail",  3.2),
    ("Madhavaram",       "Tiruvottiyur",      "Suburban_Train","Suburban Rail",  4.5),
    ("Tiruvottiyur",     "Ennore",            "Suburban_Train","Suburban Rail",  6.0),
    ("Ennore",           "Wimco_Nagar",       "Suburban_Train","Suburban Rail",  3.5),

    # ─ North Bus Corridor ─────────────────────────────────────────────────────
    ("Broadway_Terminal", "Tiruvottiyur",     "MTC_Bus","Bus 1",            16.0),
    ("Broadway_Terminal", "Wimco_Nagar",      "MTC_Bus","Bus 1A",           22.0),
    ("Broadway_Terminal", "Perambur",         "MTC_Bus","Bus 20A",           6.0),
    ("Broadway_Terminal", "Madhavaram",       "MTC_Bus","Bus 20A",          12.0),
    ("Perambur",          "Kolathur",         "MTC_Bus","Bus 20A",           3.5),
    ("Perambur",          "Ambattur",         "MTC_Bus","Bus 29C",          10.0),

    # ─ Northwest Bus Corridor ─────────────────────────────────────────────────
    ("Broadway_Terminal", "Ambattur",         "MTC_Bus","Bus 70",           18.0),
    ("Broadway_Terminal", "Avadi",            "MTC_Bus","Bus 70G",          28.0),
    ("Broadway_Terminal", "Pattabiram",       "MTC_Bus","Bus 71",           22.0),
    ("Broadway_Terminal", "Poonamallee",      "MTC_Bus","Bus 10A",          25.0),
    ("Broadway_Terminal", "Porur",            "MTC_Bus","Bus 10",           22.0),
    ("Koyambedu_CMBT",   "Ambattur",         "MTC_Bus","Bus 29C",          12.0),
    ("Koyambedu_CMBT",   "Avadi",            "MTC_Bus","Bus 70G",          18.0),
    ("Koyambedu_CMBT",   "Poonamallee",      "MTC_Bus","Bus 10A",          15.0),
    ("Koyambedu_CMBT",   "Porur",            "MTC_Bus","Bus 10",           12.0),
    ("Ambattur",          "Ambattur_Industrial","Walk", "Walk to OTA Gate",  0.8),
    ("Ambattur",          "Pattabiram",       "MTC_Bus","Bus 71",           10.0),
    ("Avadi",             "Poonamallee",      "MTC_Bus","Bus 10A",          12.0),
    ("Poonamallee",       "Porur",            "MTC_Bus","Bus 10",            8.0),
    ("Porur",             "Valasaravakkam",   "MTC_Bus","Bus 10",            3.5),
    ("Valasaravakkam",    "Koyambedu_CMBT",   "MTC_Bus","Bus 10",            6.0),
    ("Maduravoyal",       "Koyambedu_CMBT",   "MTC_Bus","Bus 29C",           6.5),
    ("Mogappair",         "Koyambedu_CMBT",   "MTC_Bus","Bus 27B",           5.0),
    ("Mogappair",         "Ambattur",         "MTC_Bus","Bus 70G",           6.5),
    ("Anna_Nagar_Tower",  "Koyambedu_CMBT",   "MTC_Bus","Bus 27B",           3.5),
    ("Anna_Nagar_Tower",  "T_Nagar",          "MTC_Bus","Bus 27B",           7.0),
    ("Anna_Nagar_East",   "Arumbakkam",       "Metro",  "CMRL Green Line",   2.5),
    ("Anna_Nagar_East",   "Thirumangalam_Metro","Metro","CMRL Green Line",   1.8),
    ("Thirumangalam_Metro","Koyambedu_CMBT",  "Metro",  "CMRL Green Line",   2.5),

    # ═══════════════════════════════════════════════════════════════════════════
    # CENTRAL CHENNAI — T. NAGAR / VADAPALANI / KILPAUK NETWORK
    # ═══════════════════════════════════════════════════════════════════════════
    ("T_Nagar",           "Guindy_Station",   "MTC_Bus","Bus 21G",           5.0),
    ("T_Nagar",           "Chennai_Central",  "MTC_Bus","Bus 5",             8.0),
    ("T_Nagar",           "Chennai_Egmore",   "MTC_Bus","Bus 5C",            6.5),
    ("T_Nagar",           "Koyambedu_CMBT",   "MTC_Bus","Bus 27B",           6.5),
    ("T_Nagar",           "Vadapalani",       "MTC_Bus","Bus 56",            3.5),
    ("T_Nagar",           "Velachery",        "MTC_Bus","Bus 56",            6.0),
    ("T_Nagar",           "Chennai_Central",  "Metro",  "CMRL Blue Line",    9.0),
    ("T_Nagar",           "Saidapet",         "Walk",   "T.Nagar–Saidapet",  1.8),
    ("Kilpauk",           "Chennai_Egmore",   "Walk",   "Kilpauk–Egmore",    1.5),
    ("Kilpauk",           "Perambur",         "Walk",   "Kilpauk–Perambur",  2.5),
    ("Kilpauk",           "Anna_Nagar_Tower", "MTC_Bus","Bus 27B",           3.5),
    ("Nandanam",          "T_Nagar",          "Walk",   "Nandanam–TNagar",   1.0),
    ("Vadapalani",        "T_Nagar",          "MTC_Bus","Bus 56",            3.5),
    ("Vadapalani",        "Koyambedu_CMBT",   "Metro",  "CMRL Green Line",   3.5),
    ("Vadapalani",        "Porur",            "MTC_Bus","Bus 10",            5.5),
    ("Ashok_Nagar",       "Guindy_Station",   "Walk",   "Ashok Nagar Walk",  1.2),

    # ═══════════════════════════════════════════════════════════════════════════
    # AIRPORT / ALANDUR INTERCHANGE
    # ═══════════════════════════════════════════════════════════════════════════
    ("Airport",           "Meenambakkam",     "Walk",      "Terminal Walk",    1.0),
    ("Airport",           "Alandur",          "Rapido_Bike","Rapido Bike",      4.5),
    ("Airport",           "Koyambedu_CMBT",   "MTC_Bus",   "Bus 43",          14.0),
    ("Airport",           "Chennai_Central",  "MTC_Bus",   "Bus 43",          21.0),
    ("Airport",           "T_Nagar",          "Rapido_Bike","Rapido Bike",      8.0),
    ("Alandur",           "Guindy_Station",   "Walk",      "Alandur–Guindy",   1.5),
    ("Alandur",           "Koyambedu_CMBT",   "Metro",     "CMRL Green Line", 11.0),
    ("Meenambakkam",      "Pallavaram",       "Rapido_Bike","Rapido Bike",      4.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # OMR / IT CORRIDOR (Old Mahabalipuram Road)
    # ═══════════════════════════════════════════════════════════════════════════
    ("OMR_Tidel_Park",    "Perungudi",        "MTC_Bus","Bus 102",            3.5),
    ("Perungudi",         "Thoraipakkam",     "MTC_Bus","Bus 102",            3.5),
    ("Thoraipakkam",      "Karapakkam",       "MTC_Bus","Bus 102",            3.5),
    ("Karapakkam",        "OMR_Sholinganallur","MTC_Bus","Bus 102",           3.5),
    ("OMR_Sholinganallur","Navallur",         "MTC_Bus","Bus 570A",           6.0),
    ("Navallur",          "Siruseri_IT",      "MTC_Bus","Bus 574",            3.5),
    ("Siruseri_IT",       "Kelambakkam",      "MTC_Bus","Bus 574",            5.0),
    ("Kelambakkam",       "Thiruporur",       "MTC_Bus","Bus 508",            8.0),

    # ─ OMR Express Services ────────────────────────────────────────────────────
    ("Chennai_Central",   "OMR_Tidel_Park",   "MTC_Bus","Bus 102",           14.0),
    ("Chennai_Central",   "OMR_Sholinganallur","MTC_Bus","Bus 102",          25.0),
    ("Koyambedu_CMBT",    "OMR_Sholinganallur","MTC_Bus","Bus 570",          28.0),
    ("Broadway_Terminal", "OMR_Sholinganallur","MTC_Bus","Bus 570A",         24.0),
    ("Koyambedu_CMBT",    "Siruseri_IT",      "MTC_Bus","Bus 574",           32.0),
    ("Broadway_Terminal", "Kelambakkam",      "MTC_Bus","Bus 576",           38.0),
    ("Tambaram_Station",  "OMR_Sholinganallur","MTC_Bus","Bus 119",          15.0),
    ("Tambaram_Station",  "Kelambakkam",      "MTC_Bus","Bus 119A",          20.0),

    # ─ OMR Rapido / Auto ──────────────────────────────────────────────────────
    ("OMR_Tidel_Park",    "Perungudi",        "Rapido_Bike","Rapido Bike",     3.5),
    ("OMR_Tidel_Park",    "OMR_Sholinganallur","Rapido_Bike","Rapido Bike",   11.0),
    ("OMR_Sholinganallur","Siruseri_IT",      "Rapido_Bike","Rapido Bike",     8.5),
    ("Siruseri_IT",       "Kelambakkam",      "Rapido_Bike","Rapido Bike",     5.0),
    ("Guindy_Station",    "OMR_Tidel_Park",   "MTC_Bus","Bus 102",            6.0),
    ("Guindy_Station",    "OMR_Tidel_Park",   "Rapido_Bike","Rapido Bike",    6.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # ECR CORRIDOR (East Coast Road)
    # ═══════════════════════════════════════════════════════════════════════════
    ("Adyar",             "Besant_Nagar",     "MTC_Bus","Bus 51",             3.0),
    ("Besant_Nagar",      "Thiruvanmiyur",    "MTC_Bus","Bus 52",             2.5),
    ("Thiruvanmiyur",     "Indira_Nagar",     "Walk",   "Thiruvanmiyur Walk", 1.0),
    ("Thiruvanmiyur",     "Neelankarai",      "MTC_Bus","Bus 47",             4.0),
    ("Neelankarai",       "Palavakkam",       "MTC_Bus","Bus 47",             3.5),
    ("Palavakkam",        "Injambakkam",      "MTC_Bus","Bus 47A",            3.0),
    ("Injambakkam",       "OMR_Sholinganallur","MTC_Bus","Bus 47A",           4.5),
    ("Injambakkam",       "Uthandi",          "MTC_Bus","Bus 47A",            3.5),
    ("Uthandi",           "Kovalam",          "MTC_Bus","Bus 47B",            5.0),
    ("Kovalam",           "Muttukadu",        "MTC_Bus","Bus 47B",            4.5),
    ("Broadway_Terminal", "Thiruvanmiyur",    "MTC_Bus","Bus 52",            22.0),
    ("Broadway_Terminal", "Injambakkam",      "MTC_Bus","Bus 52A",           28.0),
    ("Broadway_Terminal", "Thiruporur",       "MTC_Bus","Bus 47B",           40.0),
    ("Chennai_Central",   "Thiruporur",       "MTC_Bus","Bus 579",           45.0),
    ("Adyar",             "Thiruvanmiyur",    "Rapido_Bike","Rapido Bike",    3.5),
    ("Thiruvanmiyur",     "OMR_Sholinganallur","MTC_Bus","Bus 47",            8.5),

    # MRTS (Mass Rapid Transit) — Beach to Velachery via Adyar
    ("Chennai_Beach",     "Velachery",        "Suburban_Train","MRTS",        23.0),
    ("Chennai_Beach",     "Thiruvanmiyur",    "Suburban_Train","MRTS",        18.0),
    ("Thiruvanmiyur",     "Velachery",        "Suburban_Train","MRTS",         5.0),
    ("Velachery",         "Guindy_Station",   "MTC_Bus","Bus 5E",             5.0),
    ("Velachery",         "T_Nagar",          "MTC_Bus","Bus 56",             7.0),
    ("Velachery",         "OMR_Tidel_Park",   "Walk",   "Velachery Skywalk",  1.5),

    # ═══════════════════════════════════════════════════════════════════════════
    # SOUTH CHENNAI BUS NETWORK (Besant Nagar / Adyar / Velachery Hub)
    # ═══════════════════════════════════════════════════════════════════════════
    ("Broadway_Terminal", "Besant_Nagar",     "MTC_Bus","Bus 51",            18.0),
    ("Broadway_Terminal", "Adyar",            "MTC_Bus","Bus 41A",           16.0),
    ("Broadway_Terminal", "Velachery",        "MTC_Bus","Bus 41",            21.0),
    ("Broadway_Terminal", "Velachery",        "MTC_Bus","Bus 5C",            22.0),
    ("Chennai_Central",   "Velachery",        "MTC_Bus","Bus 5E",            18.0),
    ("Chennai_Central",   "Adyar",            "MTC_Bus","Bus 41A",           13.0),
    ("T_Nagar",           "Besant_Nagar",     "MTC_Bus","Bus 5C",             8.5),
    ("Saidapet",          "Velachery",        "MTC_Bus","Bus 5E",             6.0),
    ("Saidapet",          "Adyar",            "MTC_Bus","Bus 41A",           4.0),
    ("Adyar",             "Chennai_Central",  "MTC_Bus","Bus 41A",           13.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # KILAMBAKKAM KCBT → INTERCITY DEPARTURES
    # ═══════════════════════════════════════════════════════════════════════════
    ("Kilambakkam_KCBT",  "Pondicherry",      "SETC_Bus","SETC Pondicherry Express",  130.0),
    ("Kilambakkam_KCBT",  "Vellore",          "SETC_Bus","SETC Vellore Express",      120.0),
    ("Kilambakkam_KCBT",  "Kanchipuram",      "SETC_Bus","TNSTC Kanchipuram",          55.0),
    ("Kilambakkam_KCBT",  "Trichy",           "SETC_Bus","SETC Trichy Express",        330.0),
    ("Kilambakkam_KCBT",  "Madurai",          "SETC_Bus","SETC Madurai Express",       460.0),
    ("Kilambakkam_KCBT",  "Kelambakkam",      "MTC_Bus", "Bus 599",                    18.0),
    ("Koyambedu_CMBT",    "Pondicherry",      "SETC_Bus","SETC Pondy Express",         150.0),
    ("Koyambedu_CMBT",    "Vellore",          "SETC_Bus","SETC Vellore Bypass",        135.0),
    ("Koyambedu_CMBT",    "Trichy",           "SETC_Bus","SETC Trichy Express",        340.0),
    ("Koyambedu_CMBT",    "Madurai",          "SETC_Bus","SETC Madurai Express",       465.0),
    ("Koyambedu_CMBT",    "Coimbatore",       "SETC_Bus","SETC CBE Express",           500.0),
    ("Koyambedu_CMBT",    "Salem",            "SETC_Bus","SETC Salem Express",         340.0),
    ("Chengalpattu",      "Kanchipuram",      "SETC_Bus","TNSTC Kanchipuram Local",    35.0),
    ("Chengalpattu",      "Pondicherry",      "SETC_Bus","SETC Pondy via ECR",         90.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # SOUTHERN RAILWAY — INTERCITY TRAINS
    # ═══════════════════════════════════════════════════════════════════════════
    ("Chennai_Central",   "Vellore",          "Intercity_Train","Chennai–Vellore Express", 145.0),
    ("Chennai_Central",   "Coimbatore",       "Intercity_Train","Vande Bharat Express",    500.0),
    ("Chennai_Central",   "Salem",            "Intercity_Train","Salem Express",            370.0),
    ("Chennai_Central",   "Erode",            "Intercity_Train","Cheran Express",           420.0),
    ("Chennai_Central",   "Ariyalur",         "Intercity_Train","Tejas Express",            260.0),
    ("Chennai_Central",   "Trichy",           "Intercity_Train","Tejas Express",            320.0),
    ("Chennai_Egmore",    "Trichy",           "Intercity_Train","Vaigai Express",           320.0),
    ("Chennai_Egmore",    "Madurai",          "Intercity_Train","Vaigai Express",           460.0),
    ("Chennai_Egmore",    "Dindigul",         "Intercity_Train","Pandian Express",          440.0),
    ("Chennai_Egmore",    "Vriddhachalam",    "Intercity_Train","Suburban Express",         180.0),
    ("Chennai_Egmore",    "Villupuram",       "Intercity_Train","Villupuram Express",       165.0),
    ("Chengalpattu",      "Villupuram",       "Intercity_Train","Villupuram Passenger",     120.0),
    ("Chengalpattu",      "Trichy",           "Intercity_Train","Chengalpattu–Trichy",     260.0),
    ("Villupuram",        "Trichy",           "Intercity_Train","Vaigai Express Leg",       145.0),
    ("Trichy",            "Madurai",          "Intercity_Train","Nellai Express",           140.0),
    ("Trichy",            "Coimbatore",       "Intercity_Train","Nilgiri Express",          230.0),
    ("Trichy",            "Karur",            "Intercity_Train","Karur Passenger",           55.0),
    ("Trichy",            "Lalgudi",          "Suburban_Train", "Suburban Rail",             20.0),
    ("Trichy",            "Ariyalur",         "Intercity_Train","Ariyalur Express",          60.0),
    ("Trichy",            "Perambalur",       "Intercity_Train","Perambalur Passenger",      55.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # TRICHY CITY — TNSTC BUS NETWORK
    # ═══════════════════════════════════════════════════════════════════════════

    # ─ Junction ↔ Major Hubs ──────────────────────────────────────────────────
    ("Trichy",                "Trichy_Central_Bus_Stand","Walk",       "Junction Walk",     0.4),
    ("Trichy",                "Chatram_Bus_Stand",       "TNSTC_Bus",  "Bus T1",            2.5),
    ("Trichy_Central_Bus_Stand","Chatram_Bus_Stand",     "TNSTC_Bus",  "Bus T1",            2.2),
    ("Trichy_Central_Bus_Stand","Trichy_Fort",           "Walk",       "Fort Walk",         0.6),

    # ─ Srirangam Corridor ─────────────────────────────────────────────────────
    ("Chatram_Bus_Stand",     "Srirangam",               "TNSTC_Bus",  "Bus T1",            8.5),
    ("Trichy",                "Srirangam",               "TNSTC_Bus",  "Bus T1",           10.5),
    ("Trichy_Central_Bus_Stand","Srirangam",             "TNSTC_Bus",  "Bus T1",            9.5),
    ("Srirangam",             "Pullambadi",              "TNSTC_Bus",  "Bus T51",           15.0),
    ("Srirangam",             "Lalgudi",                 "TNSTC_Bus",  "Bus T51",           22.0),
    ("Kattur",                "Srirangam",               "Walk",       "Kattur Walk",        1.5),
    ("Kattur",                "Chatram_Bus_Stand",       "TNSTC_Bus",  "Bus T5",             3.0),

    # ─ Thiruverambur / Eastern Corridor ──────────────────────────────────────
    ("Chatram_Bus_Stand",     "Thiruverambur",           "TNSTC_Bus",  "Bus T2",            12.0),
    ("Trichy",                "Thiruverambur",           "TNSTC_Bus",  "Bus T2",            14.0),
    ("Thiruverambur",         "Ariyamangalam",           "TNSTC_Bus",  "Bus T3",             7.0),
    ("Ariyamangalam",         "Golden_Rock",             "TNSTC_Bus",  "Bus T10",            5.0),
    ("Golden_Rock",           "Trichy_Central_Bus_Stand","TNSTC_Bus",  "Bus T10",            7.5),
    ("Thiruverambur",         "Manachanallur",           "TNSTC_Bus",  "Bus T55",            9.0),

    # ─ Woraiyur / Western Suburbs ─────────────────────────────────────────────
    ("Chatram_Bus_Stand",     "Woraiyur",                "TNSTC_Bus",  "Bus T5",             5.5),
    ("Trichy",                "Woraiyur",                "TNSTC_Bus",  "Bus T5",             7.0),
    ("Woraiyur",              "Musiri",                  "TNSTC_Bus",  "Bus T52",           42.0),
    ("Woraiyur",              "Kulithalai",              "TNSTC_Bus",  "Bus T53",           40.0),
    ("Trichy",                "Manapparai",              "TNSTC_Bus",  "Bus T50",           30.0),
    ("Chatram_Bus_Stand",     "Manapparai",              "TNSTC_Bus",  "Bus T50",           28.0),
    ("Manapparai",            "Viralimalai",             "TNSTC_Bus",  "Bus T50",           20.0),

    # ─ KK Nagar / Residential Hub ─────────────────────────────────────────────
    ("Trichy_Central_Bus_Stand","KK_Nagar_Trichy",       "TNSTC_Bus",  "Bus T4",             4.0),
    ("Chatram_Bus_Stand",     "KK_Nagar_Trichy",         "TNSTC_Bus",  "Bus T4",             5.5),
    ("KK_Nagar_Trichy",       "Thillai_Nagar_Trichy",   "Walk",       "KK Nagar Walk",      1.5),
    ("KK_Nagar_Trichy",       "Ponmalaipatti",           "TNSTC_Bus",  "Bus T58",            5.5),

    # ─ Tennur / Thillai Nagar Corridor ───────────────────────────────────────
    ("Trichy_Central_Bus_Stand","Tennur_Trichy",         "TNSTC_Bus",  "Bus T7",             5.5),
    ("Tennur_Trichy",         "Palakarai",               "Walk",       "Tennur–Palakarai",   1.5),
    ("Palakarai",             "Trichy_Fort",             "Walk",       "Palakarai Walk",     1.2),
    ("Thillai_Nagar_Trichy",  "Chatram_Bus_Stand",       "TNSTC_Bus",  "Bus T7",             3.5),
    ("Thillai_Nagar_Trichy",  "Golden_Rock",             "TNSTC_Bus",  "Bus T10",            3.0),

    # ─ Lalgudi / Northeast ────────────────────────────────────────────────────
    ("Trichy",                "Lalgudi",                 "TNSTC_Bus",  "Bus T51",           25.0),
    ("Chatram_Bus_Stand",     "Lalgudi",                 "TNSTC_Bus",  "Bus T51",           23.0),
    ("Lalgudi",               "Manachanallur",           "TNSTC_Bus",  "Bus T55",           12.0),
    ("Lalgudi",               "Pullambadi",              "TNSTC_Bus",  "Bus T51",            8.0),

    # ─ Thuraiyur / North ──────────────────────────────────────────────────────
    ("Chatram_Bus_Stand",     "Thuraiyur",               "TNSTC_Bus",  "Bus T54",           40.0),
    ("Trichy",                "Thuraiyur",               "TNSTC_Bus",  "Bus T54",           42.0),
    ("Thuraiyur",             "Perambalur",              "TNSTC_Bus",  "Bus T54",           30.0),

    # ─ Auto / Rapido within Trichy ────────────────────────────────────────────
    ("Trichy",                "Chatram_Bus_Stand",       "Ola_Auto",   "Ola Auto",           2.5),
    ("Trichy",                "Srirangam",               "Ola_Auto",   "Ola Auto",          10.5),
    ("Trichy",                "KK_Nagar_Trichy",         "Ola_Auto",   "Ola Auto",           4.5),
    ("Trichy",                "Thiruverambur",           "Ola_Auto",   "Ola Auto",          14.0),
    ("Chatram_Bus_Stand",     "Srirangam",               "Ola_Auto",   "Ola Auto",           8.5),
    ("Chatram_Bus_Stand",     "Woraiyur",                "Ola_Auto",   "Ola Auto",           5.5),
    ("Chatram_Bus_Stand",     "Thillai_Nagar_Trichy",   "Ola_Auto",   "Ola Auto",           3.5),
    ("Trichy",                "Ariyamangalam",           "Rapido_Bike","Rapido Bike",        18.0),
    ("Trichy",                "Manapparai",              "Rapido_Bike","Rapido Bike",        30.0),

    # ─ SETC from Trichy ───────────────────────────────────────────────────────
    ("Trichy",                "Coimbatore",              "SETC_Bus",   "SETC Coimbatore",  220.0),
    ("Trichy",                "Karur",                   "SETC_Bus",   "SETC Karur Local",   55.0),
    ("Trichy",                "Manapparai",              "SETC_Bus",   "SETC Local",          30.0),
    ("Trichy",                "Vriddhachalam",           "SETC_Bus",   "SETC Villupuram",    120.0),
    ("Trichy",                "Villupuram",              "SETC_Bus",   "SETC Villupuram",    145.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # BROADWAY TERMINAL — CENTRAL DISPATCH HUB
    # ═══════════════════════════════════════════════════════════════════════════
    ("Broadway_Terminal",     "Chennai_Central",         "Walk",       "Broadway Walk",      1.5),
    ("Broadway_Terminal",     "Chennai_Beach",           "Walk",       "Beach Walk",         0.8),
    ("Broadway_Terminal",     "Washermenpet",            "MTC_Bus",    "Bus 1",              2.5),
    ("Broadway_Terminal",     "T_Nagar",                 "MTC_Bus",    "Bus 5",             10.0),
    ("Broadway_Terminal",     "Koyambedu_CMBT",          "MTC_Bus",    "Bus 5",             14.0),
    ("Broadway_Terminal",     "Guindy_Station",          "MTC_Bus",    "Bus 21G",           15.0),
    ("Broadway_Terminal",     "Airport",                 "MTC_Bus",    "Bus 43",            21.0),
    ("Broadway_Terminal",     "Velachery",               "MTC_Bus",    "Bus 41",            22.0),
    ("Broadway_Terminal",     "Anna_Nagar_Tower",        "MTC_Bus",    "Bus 27B",           10.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # INTER-CITY CONNECTIONS (Tamil Nadu Wide)
    # ═══════════════════════════════════════════════════════════════════════════
    ("Kanchipuram",           "Chengalpattu",            "SETC_Bus",   "TNSTC Kanchi Local", 35.0),
    ("Kanchipuram",           "Vellore",                 "SETC_Bus",   "TNSTC Vellore",      75.0),
    ("Vellore",               "Salem",                   "SETC_Bus",   "SETC Salem",        120.0),
    ("Salem",                 "Erode",                   "SETC_Bus",   "SETC Erode",         55.0),
    ("Erode",                 "Coimbatore",              "SETC_Bus",   "SETC Coimbatore",    65.0),
    ("Coimbatore",            "Karur",                   "SETC_Bus",   "SETC Karur",        130.0),
    ("Karur",                 "Trichy",                  "SETC_Bus",   "SETC Trichy",        55.0),
    ("Trichy",                "Dindigul",                "SETC_Bus",   "SETC Dindigul",      80.0),
    ("Dindigul",              "Madurai",                 "SETC_Bus",   "SETC Madurai",       65.0),
    ("Pondicherry",           "Villupuram",              "SETC_Bus",   "SETC Villupuram",    50.0),
    ("Villupuram",            "Vriddhachalam",           "SETC_Bus",   "SETC Vriddhachalam", 50.0),

    # ═══════════════════════════════════════════════════════════════════════════
    # LAST-MILE RAPIDO / OLA SHORTCUTS (Key interchange points)
    # ═══════════════════════════════════════════════════════════════════════════
    ("Chennai_Central",       "T_Nagar",                 "Rapido_Bike","Rapido Bike",        6.5),
    ("Chennai_Central",       "Anna_Nagar_Tower",        "Rapido_Bike","Rapido Bike",        9.5),
    ("Chennai_Central",       "Kilpauk",                 "Rapido_Bike","Rapido Bike",        3.5),
    ("Chennai_Egmore",        "Kilpauk",                 "Rapido_Bike","Rapido Bike",        2.5),
    ("Chennai_Egmore",        "T_Nagar",                 "Rapido_Bike","Rapido Bike",        5.5),
    ("Guindy_Station",        "Velachery",               "Rapido_Bike","Rapido Bike",        5.5),
    ("Guindy_Station",        "Adyar",                   "Rapido_Bike","Rapido Bike",        5.0),
    ("Guindy_Station",        "T_Nagar",                 "Rapido_Bike","Rapido Bike",        5.5),
    ("Guindy_Station",        "Tambaram_Station",        "Rapido_Bike","Rapido Bike",       14.0),
    ("Airport",               "Alandur",                 "Ola_Auto",   "Ola Auto",           4.5),
    ("Airport",               "Guindy_Station",          "Ola_Auto",   "Ola Auto",           7.5),
    ("OMR_Sholinganallur",    "Siruseri_IT",             "Rapido_Bike","Rapido Bike",        8.5),
    ("OMR_Sholinganallur",    "Kelambakkam",             "Rapido_Bike","Rapido Bike",       12.0),
    ("Koyambedu_CMBT",        "Anna_Nagar_Tower",        "Rapido_Bike","Rapido Bike",        3.0),
    ("Koyambedu_CMBT",        "Porur",                   "Rapido_Bike","Rapido Bike",       10.0),
    ("Koyambedu_CMBT",        "T_Nagar",                 "Rapido_Bike","Rapido Bike",        7.0),
    ("Tambaram_Station",      "Chrompet",                "Rapido_Bike","Rapido Bike",        4.0),
    ("Tambaram_Station",      "Pallavaram",              "Rapido_Bike","Rapido Bike",        5.5),
    ("Velachery",             "Tambaram_Station",        "Rapido_Bike","Rapido Bike",       10.5),
    ("Adyar",                 "Velachery",               "Rapido_Bike","Rapido Bike",        4.5),
    ("Adyar",                 "Besant_Nagar",            "Rapido_Bike","Rapido Bike",        3.0),
]


# ── DYNAMIC DATASET MERGE ─────────────────────────────────────────────────────
try:
    from data.dataset_loader import load_and_merge_data
    from data.database import COORDINATES
    _, _, _, EDGES = load_and_merge_data(COORDINATES, {}, {}, EDGES)
except Exception as e:
    print(f"[Warning] Failed to merge routing edges: {e}")



# ══════════════════════════════════════════════════════════════════════════════
# ROUTING ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def format_minutes_to_time(minutes: int) -> str:
    h = int(minutes // 60) % 24
    m = int(minutes % 60)
    am_pm = "AM" if h < 12 else "PM"
    h_display = h if 1 <= h <= 12 else (12 if h == 0 or h == 12 else h - 12)
    return f"{h_display:02d}:{m:02d} {am_pm}"

def get_bilingual_instruction(mode: str, line_name: str, from_node: str, to_node: str) -> Dict[str, str]:
    from_clean = from_node.replace("_", " ")
    to_clean = to_node.replace("_", " ")

    if mode == "Walk":
        return {
            "en": f"Walk from {from_clean} to {to_clean}.",
            "ta": f"{from_clean} லிருந்து {to_clean} வரை நடந்து செல்லவும்."
        }
    elif mode in ["Suburban_Train", "Intercity_Train"]:
        return {
            "en": f"Board {line_name} at {from_clean} towards {to_clean}.",
            "ta": f"{from_clean} ரயில் நிலையத்தில் {line_name} ரயிலில் ஏறவும்."
        }
    elif mode == "Metro":
        return {
            "en": f"Take Chennai Metro ({line_name}) from {from_clean} to {to_clean}.",
            "ta": f"{from_clean} மெட்ரோ நிலையத்திலிருந்து ({line_name}) {to_clean} செல்லவும்."
        }
    elif mode in ["SETC_Bus", "MTC_Bus", "Town_Bus"]:
        return {
            "en": f"Take {line_name} from {from_clean} to {to_clean}.",
            "ta": f"{from_clean} பேருந்து நிலையத்தில் {line_name} வண்டியில் ஏறவும்."
        }
    elif mode == "Rapido_Bike":
        return {
            "en": f"Book a Rapido Bike from {from_clean} to {to_clean}.",
            "ta": f"{from_clean} லிருந்து {to_clean} செல்ல ரேபிடோ பைக் புக் செய்யவும்."
        }
    elif mode == "Ola_Auto":
        return {
            "en": f"Book an Ola Auto from {from_clean} to {to_clean}.",
            "ta": f"{from_clean} லிருந்து {to_clean} செல்ல ஓலா ஆட்டோ புக் செய்யவும்."
        }
    return {
        "en": f"Travel from {from_clean} to {to_clean} via {line_name}.",
        "ta": f"{from_clean} லிருந்து {to_clean} நோக்கி {line_name} மூலம் பயணம்."
    }

def get_edge_weight(
    mode: str,
    line_name: str,
    dist: float,
    current_time: int,
    disrupted_modes: List[str]
) -> Tuple[float, float, float]:
    """Returns (duration_min, fare_inr, co2_grams) for a given edge and time."""
    mode_spec = TRANSIT_MODES.get(mode, TRANSIT_MODES["Walk"])

    fare = mode_spec["base_fare"] + (dist * mode_spec["per_km_fare"])
    co2 = dist * mode_spec["co2_per_km"]

    if mode == "Walk":
        duration = (dist / 5.0) * 60.0
    elif mode in ["Rapido_Bike", "Ola_Auto"]:
        wait_time = 4.0 if mode == "Rapido_Bike" else 6.0
        traffic = get_traffic_factor(current_time)
        speed = 35.0 if mode == "Rapido_Bike" else 25.0
        duration = wait_time + ((dist / speed) * 60.0 * traffic)
    elif mode == "Metro":
        duration = (dist / 40.0) * 60.0
    elif mode == "Suburban_Train":
        duration = (dist / 35.0) * 60.0
    elif mode == "Intercity_Train":
        speed = 85.0 if "Vande Bharat" in line_name else 70.0
        duration = (dist / speed) * 60.0
    elif mode in ["MTC_Bus", "SETC_Bus", "Town_Bus", "TNSTC_Bus"]:
        traffic = get_traffic_factor(current_time)
        speed = 28.0 if mode == "SETC_Bus" else 20.0
        duration = ((dist / speed) * 60.0 * traffic)
    else:
        duration = (dist / 30.0) * 60.0

    return duration, fare, co2

def heuristic(node: str, target: str, mood: str) -> float:
    c1 = COORDINATES.get(node)
    c2 = COORDINATES.get(target)
    if not c1 or not c2:
        return 0.0
    dist = haversine_distance(c1, c2)

    if mood == "fastest":
        return (dist / 80.0) * 60.0
    elif mood == "cheapest":
        return dist * 0.2
    elif mood == "greenest":
        return dist * 3.0
    elif mood == "safest":
        return (dist / 60.0) * 60.0
    return dist

def solve_route(
    start_node: str,
    target_node: str,
    start_time_min: int,
    mood: str,
    disrupted_modes: List[str]
) -> Optional[Dict[str, Any]]:
    heap: List[Tuple[float, int, int, str, List[Dict[str, Any]]]] = []
    visited_best: Dict[str, float] = {}

    counter = 0
    heapq.heappush(heap, (heuristic(start_node, target_node, mood), start_time_min, counter, start_node, []))

    while heap:
        f_score, curr_time, _, curr_node, path = heapq.heappop(heap)

        if curr_node == target_node:
            total_fare = sum(seg["fare"] for seg in path)
            total_co2 = sum(seg["co2"] for seg in path)
            total_time = curr_time - start_time_min

            return {
                "mood": mood,
                "total_time": round(total_time, 1),
                "total_fare": round(total_fare, 1),
                "total_co2": round(total_co2, 1),
                "start_time_str": format_minutes_to_time(start_time_min),
                "end_time_str": format_minutes_to_time(curr_time),
                "segments": path
            }

        score_metric = 0.0
        if mood == "fastest":
            score_metric = curr_time - start_time_min
        elif mood == "cheapest":
            score_metric = sum(seg["fare"] for seg in path)
        elif mood == "greenest":
            score_metric = sum(seg["co2"] for seg in path)
        elif mood == "safest":
            score_metric = (curr_time - start_time_min) + sum(100.0 for seg in path if seg["mode"] in ["Rapido_Bike", "Ola_Auto"])

        if curr_node in visited_best and visited_best[curr_node] <= score_metric:
            continue
        visited_best[curr_node] = score_metric

        for edge in EDGES:
            u, v, mode, line, dist = edge
            neighbor = None
            if u == curr_node:
                neighbor = v
            elif v == curr_node:
                neighbor = u

            if not neighbor:
                continue

            if mode in disrupted_modes:
                continue

            sched_mode = mode
            if mode in ["MTC_Bus", "TNSTC_Bus"]:
                sched_mode = line.replace(" ", "_")
            elif mode == "Town_Bus":
                sched_mode = "Town_Bus"

            next_dep = get_next_departure(sched_mode, curr_node, curr_time, disrupted_modes)
            if next_dep is None:
                continue

            wait_time = next_dep - curr_time
            dur, fare, co2 = get_edge_weight(mode, line, dist, next_dep, disrupted_modes)
            arr_time = next_dep + dur

            instruction = get_bilingual_instruction(mode, line, curr_node, neighbor)

            segment = {
                "from_node": curr_node,
                "to_node": neighbor,
                "from_coords": list(COORDINATES.get(curr_node, (0.0, 0.0))),
                "to_coords": list(COORDINATES.get(neighbor, (0.0, 0.0))),
                "mode": mode,
                "line_name": line,
                "wait_time": round(wait_time, 1),
                "duration": round(dur, 1),
                "fare": round(fare, 1),
                "co2": round(co2, 1),
                "start_time": int(next_dep),
                "end_time": int(arr_time),
                "start_time_str": format_minutes_to_time(int(next_dep)),
                "end_time_str": format_minutes_to_time(int(arr_time)),
                "instruction_en": instruction["en"],
                "instruction_ta": instruction["ta"]
            }

            new_path = path + [segment]

            g_score = 0.0
            if mood == "fastest":
                g_score = arr_time - start_time_min
            elif mood == "cheapest":
                g_score = sum(seg["fare"] for seg in new_path)
            elif mood == "greenest":
                g_score = sum(seg["co2"] for seg in new_path)
            elif mood == "safest":
                g_score = (arr_time - start_time_min) + sum(100.0 for seg in new_path if seg["mode"] in ["Rapido_Bike", "Ola_Auto"])

            h_score = heuristic(neighbor, target_node, mood)
            f_score_new = g_score + h_score

            counter += 1
            heapq.heappush(heap, (f_score_new, int(arr_time), counter, neighbor, new_path))

    return None
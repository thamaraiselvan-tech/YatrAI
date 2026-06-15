"""
engine_edges_expansion.py
─────────────────────────
Drop-in replacement for the EDGES list in engine.py.
Covers every major/minor route across Chennai District + Trichy District.

HOW TO USE:
  Replace the existing EDGES = [...] block in engine.py with this file's content.
  Then add TNSTC_Bus to the disrupted-mode checks in solve_route() the same way
  MTC_Bus is handled — they share the same scheduling logic.
"""

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

"""
══════════════════════════════════════════════════════════════════════
INTEGRATION INSTRUCTIONS
══════════════════════════════════════════════════════════════════════

Step 1 — Replace database.py:
  Copy the new database.py to backend/data/database.py

Step 2 — Replace EDGES in engine.py:
  Open backend/routing/engine.py
  Find the EDGES = [...] block (starts at line ~6)
  Delete the entire block
  Paste the EDGES list from this file

Step 3 — Update engine.py imports (if not already):
  The existing import line should be:
    from data.database import COORDINATES, TRANSIT_MODES, SCHEDULES,
                              haversine_distance, get_traffic_factor,
                              get_next_departure

Step 4 — Update solve_route() disruption check:
  Find the line that checks mode in disrupted_modes.
  Add TNSTC_Bus to the disruption-eligible modes
  alongside MTC_Bus and Suburban_Train.

Step 5 — Test:
  python -m pytest backend/test_routing.py -v
══════════════════════════════════════════════════════════════════════
"""

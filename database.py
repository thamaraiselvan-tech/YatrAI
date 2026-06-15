import math
from typing import Dict, List, Tuple, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# YatrAI Expanded Transit Database
# Coverage: Full Chennai District + Tiruchirappalli (Trichy) District
# Nodes: 170+ | Routes: Every major suburban, metro, MTC, TNSTC, SETC corridor
# ═══════════════════════════════════════════════════════════════════════════════

COORDINATES: Dict[str, Tuple[float, float]] = {

    # ── SRM Campus (Origin Nodes) ────────────────────────────────────────────
    "SRM_Dorm":                  (12.8235, 80.0425),
    "SRM_Main_Gate":             (12.8230, 80.0438),
    "SRM_Tech_Park":             (12.8218, 80.0452),

    # ── Chengalpattu–Potheri Corridor (Southern Railway) ────────────────────
    "Potheri_Station":           (12.8242, 80.0440),
    "Kattankulathur_Station":    (12.8340, 80.0520),
    "Singaperumal_Koil":         (12.8027, 80.0192),
    "Maraimalai_Nagar":          (12.8200, 80.0210),
    "Guduvanchery":              (12.8437, 80.0654),
    "Urapakkam":                 (12.8590, 80.0633),
    "Vandalur":                  (12.8888, 80.0945),
    "Perungalathur":             (12.8729, 80.0815),
    "Sembakkam":                 (12.9415, 80.1083),
    "Pallavaram":                (12.9698, 80.1523),
    "Chrompet":                  (12.9520, 80.1382),
    "Tambaram_Station":          (12.9250, 80.1200),
    "Tambaram_West":             (12.9212, 80.1058),
    "Chengalpattu":              (12.6934, 79.9772),

    # ── GST Road Corridor (NH-44 / NH-548) ──────────────────────────────────
    "Kilambakkam_KCBT":          (12.8710, 80.0810),
    "Padappai":                  (12.9050, 80.0200),
    "Walajabad":                 (12.8340, 79.9600),
    "GST_Paranur_Toll":          (12.8520, 80.0135),
    "GST_Oragadam":              (12.8730, 80.0310),

    # ── Tambaram → Guindy → Central (Main Suburban South Corridor) ──────────
    "St_Thomas_Mount":           (12.9862, 80.2035),
    "Alandur":                   (12.9978, 80.1946),
    "Nanganallur_Road":          (12.9760, 80.1867),
    "Guindy_Station":            (13.0084, 80.2131),
    "Little_Mount":              (13.0093, 80.2218),
    "Saidapet":                  (13.0188, 80.2247),
    "Mambalam":                  (13.0351, 80.2266),
    "Kodambakkam":               (13.0472, 80.2309),
    "Nungambakkam":              (13.0569, 80.2425),
    "Chetpet":                   (13.0716, 80.2419),
    "Chennai_Egmore":            (13.0783, 80.2598),
    "Park_Town":                 (13.0810, 80.2745),
    "Chennai_Fort":              (13.0848, 80.2773),
    "Chennai_Beach":             (13.0966, 80.2877),
    "Chennai_Central":           (13.0827, 80.2707),

    # ── CMRL Metro Blue Line: Airport → Chennai Central → Wimco Nagar ───────
    "Airport":                   (12.9856, 80.1809),
    "Meenambakkam":              (12.9780, 80.1743),
    "Ekkatuthangal":             (13.0172, 80.2133),
    "Nandanam":                  (13.0363, 80.2340),
    "Teynampet":                 (13.0465, 80.2427),
    "AG_DMS":                    (13.0535, 80.2503),
    "Thousand_Lights":           (13.0618, 80.2576),
    "LIC":                       (13.0716, 80.2644),
    "High_Court":                (13.0938, 80.2787),
    "Mannadi":                   (13.0970, 80.2843),

    # ── CMRL Metro Green Line: CMBT → Vadapalani → Alandur ─────────────────
    "Koyambedu_CMBT":            (13.0680, 80.2030),
    "Arumbakkam":                (13.0665, 80.2112),
    "Vadapalani":                (13.0501, 80.2123),
    "Ashok_Nagar":               (13.0363, 80.2103),

    # ── North Chennai: Thiruvottiyur–Wimco Nagar Line ───────────────────────
    "Wimco_Nagar":               (13.1793, 80.3112),
    "Tiruvottiyur":              (13.1563, 80.3057),
    "Kaladipet":                 (13.1650, 80.3000),
    "Ennore":                    (13.2128, 80.3234),
    "Tondiarpet":                (13.1310, 80.2890),
    "Washermenpet":              (13.1070, 80.2927),
    "Basin_Bridge":              (13.0967, 80.2667),
    "Madhavaram":                (13.1535, 80.2355),
    "Perambur":                  (13.1130, 80.2437),
    "Vyasarpadi":                (13.1215, 80.2530),

    # ── Northwest Corridor: Central → Villivakkam → Avadi ───────────────────
    "Villivakkam":               (13.1118, 80.2118),
    "Korattur":                  (13.1197, 80.1913),
    "Ambattur":                  (13.0983, 80.1718),
    "Ambattur_Industrial":       (13.1175, 80.1594),
    "Pattabiram":                (13.1139, 80.1261),
    "Avadi":                     (13.1151, 80.1014),
    "Tiruttani":                 (13.1910, 79.6350),
    "Arakkonam":                 (13.0778, 79.6707),

    # ── West Chennai ─────────────────────────────────────────────────────────
    "Anna_Nagar_Tower":          (13.0850, 80.2101),
    "Anna_Nagar_East":           (13.0868, 80.2198),
    "Mogappair":                 (13.0900, 80.1702),
    "Poonamallee":               (13.0454, 80.1211),
    "Porur":                     (13.0357, 80.1605),
    "Valasaravakkam":            (13.0474, 80.1808),
    "Maduravoyal":               (13.0728, 80.1521),

    # ── Central Hubs ─────────────────────────────────────────────────────────
    "T_Nagar":                   (13.0418, 80.2341),
    "Kilpauk":                   (13.0826, 80.2335),
    "Broadway_Terminal":         (13.0900, 80.2830),
    "Thirumangalam_Metro":       (13.1008, 80.2113),
    "Kolathur":                  (13.1302, 80.2278),

    # ── South-Central Chennai ─────────────────────────────────────────────────
    "Velachery":                 (12.9815, 80.2224),
    "Adyar":                     (13.0063, 80.2575),
    "Besant_Nagar":              (12.9994, 80.2685),
    "Thiruvanmiyur":             (12.9830, 80.2657),
    "Indira_Nagar":              (12.9878, 80.2493),

    # ── OMR / IT Corridor (Old Mahabalipuram Road) ───────────────────────────
    "OMR_Tidel_Park":            (12.9896, 80.2486),
    "Perungudi":                 (12.9654, 80.2382),
    "Thoraipakkam":              (12.9367, 80.2357),
    "Karapakkam":                (12.9202, 80.2310),
    "OMR_Sholinganallur":        (12.8976, 80.2281),
    "Navallur":                  (12.8527, 80.2295),
    "Siruseri_IT":               (12.8308, 80.2169),
    "Kelambakkam":               (12.7941, 80.2180),
    "Thiruporur":                (12.7235, 80.1945),

    # ── ECR Corridor (East Coast Road) ───────────────────────────────────────
    "Injambakkam":               (12.8845, 80.2506),
    "Neelankarai":               (12.9385, 80.2504),
    "Palavakkam":                (12.9093, 80.2379),
    "Uthandi":                   (12.8623, 80.2476),
    "Kovalam":                   (12.7918, 80.2526),
    "Muttukadu":                 (12.8250, 80.2544),

    # ── Anna Salai / Mount Road Corridor ─────────────────────────────────────
    "Anna_Salai_North":          (13.0700, 80.2570),
    "Anna_Salai_South":          (13.0440, 80.2470),
    "Gemini_Flyover":            (13.0618, 80.2493),

    # ── Tamil Nadu Intercity Hubs ─────────────────────────────────────────────
    "Kanchipuram":               (12.8387, 79.7016),
    "Vellore":                   (12.9165, 79.1325),
    "Pondicherry":               (11.9416, 79.8083),
    "Coimbatore":                (11.0168, 76.9558),
    "Madurai":                   (9.9252,  78.1198),
    "Salem":                     (11.6643, 78.1460),
    "Erode":                     (11.3410, 77.7172),

    # ═══════════════════════════════════════════════════════════════════════════
    # TIRUCHIRAPPALLI (TRICHY) DISTRICT
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Trichy City Core ─────────────────────────────────────────────────────
    "Trichy":                    (10.7905, 78.7047),  # Trichy Junction (Railway)
    "Trichy_Central_Bus_Stand":  (10.7867, 78.7095),
    "Chatram_Bus_Stand":         (10.8010, 78.6946),
    "Trichy_Fort":               (10.7910, 78.6955),

    # ── Trichy Suburbs ───────────────────────────────────────────────────────
    "Srirangam":                 (10.8655, 78.6877),
    "Thiruverambur":             (10.8285, 78.8079),
    "Ariyamangalam":             (10.8384, 78.7565),
    "Woraiyur":                  (10.8003, 78.6757),
    "KK_Nagar_Trichy":           (10.7784, 78.7168),
    "Thillai_Nagar_Trichy":      (10.8019, 78.7200),
    "Tennur_Trichy":             (10.8157, 78.7030),
    "Palakarai":                 (10.8101, 78.6895),
    "Ponmalaipatti":             (10.7629, 78.7360),
    "Kattur":                    (10.8180, 78.6815),
    "Golden_Rock":               (10.8062, 78.7528),
    "Arulmigu_Mariamman_Teppakulam": (10.8204, 78.6879),

    # ── Trichy District Outskirts ────────────────────────────────────────────
    "Manapparai":                (10.6071, 78.4183),
    "Lalgudi":                   (10.8666, 78.8220),
    "Musiri":                    (10.9453, 78.4489),
    "Kulithalai":                (10.9381, 78.4181),
    "Manachanallur":             (10.8752, 78.8344),
    "Thuraiyur":                 (11.1419, 78.5965),
    "Manaparai_Junction":        (10.6100, 78.4250),
    "Perambalur":                (11.2327, 78.8810),
    "Viralimalai":               (10.5700, 78.5560),
    "Pullambadi":                (10.8870, 78.8897),
    "Ayyalur":                   (10.9265, 78.5440),

    # ── Trichy → Salem / Karur / Coimbatore Corridor ─────────────────────────
    "Karur":                     (10.9601, 78.0766),
    "Dindigul":                  (10.3673, 77.9803),

    # ── Trichy → Chennai Midpoints ────────────────────────────────────────────
    "Villupuram":                (11.9395, 79.4920),
    "Vriddhachalam":             (11.5262, 79.3223),
    "Ariyalur":                  (11.1407, 79.0780),
    "Srirangam_Road_Jn":         (10.8700, 78.6700),
}


# ── Transit Mode Specifications (unchanged) ──────────────────────────────────
TRANSIT_MODES = {
    "Suburban_Train": {
        "base_fare": 5.0,
        "per_km_fare": 0.2,
        "co2_per_km": 5.0,
        "color": "#F59E0B",
        "name_en": "Suburban Rail",
        "name_ta": "புறநகர் ரயில்"
    },
    "Intercity_Train": {
        "base_fare": 80.0,
        "per_km_fare": 1.2,
        "co2_per_km": 4.0,
        "color": "#F59E0B",
        "name_en": "Intercity Express",
        "name_ta": "இடைநகர விரைவு ரயில்"
    },
    "Metro": {
        "base_fare": 10.0,
        "per_km_fare": 2.5,
        "co2_per_km": 3.0,
        "color": "#06B6D4",
        "name_en": "Chennai Metro (CMRL)",
        "name_ta": "மெட்ரோ ரயில் (CMRL)"
    },
    "MTC_Bus": {
        "base_fare": 5.0,
        "per_km_fare": 0.8,
        "co2_per_km": 12.0,
        "color": "#EF4444",
        "name_en": "MTC Bus",
        "name_ta": "மாநகர பேருந்து (MTC)"
    },
    "TNSTC_Bus": {
        "base_fare": 5.0,
        "per_km_fare": 0.7,
        "co2_per_km": 12.0,
        "color": "#EF4444",
        "name_en": "TNSTC City Bus",
        "name_ta": "TNSTC நகர பேருந்து"
    },
    "SETC_Bus": {
        "base_fare": 40.0,
        "per_km_fare": 1.1,
        "co2_per_km": 16.0,
        "color": "#EF4444",
        "name_en": "SETC Intercity Bus",
        "name_ta": "அரசு விரைவுப் பேருந்து (SETC)"
    },
    "Rapido_Bike": {
        "base_fare": 25.0,
        "per_km_fare": 6.0,
        "co2_per_km": 40.0,
        "color": "#10B981",
        "name_en": "Rapido Bike",
        "name_ta": "ரேபிடோ பைக்"
    },
    "Ola_Auto": {
        "base_fare": 35.0,
        "per_km_fare": 10.0,
        "co2_per_km": 80.0,
        "color": "#10B981",
        "name_en": "Ola Auto",
        "name_ta": "ஓலா ஆட்டோ"
    },
    "Walk": {
        "base_fare": 0.0,
        "per_km_fare": 0.0,
        "co2_per_km": 0.0,
        "color": "#64748B",
        "name_en": "Walk",
        "name_ta": "நடைபயணம்"
    },
}


# ── Schedule Database ─────────────────────────────────────────────────────────
# frequency = minutes between services
# first_departure / last_departure = minutes from midnight
SCHEDULES = {

    # ── Rail (fixed timetable, high frequency) ────────────────────────────────
    "Suburban_Train":   { "frequency": 12, "first_departure": 240,  "last_departure": 1380 },
    "Metro":            { "frequency": 6,  "first_departure": 300,  "last_departure": 1380 },
    "Intercity_Train":  { "frequency": 90, "first_departure": 360,  "last_departure": 1320 },

    # ── Chennai MTC Bus Routes ────────────────────────────────────────────────

    # GST Road / SRM Corridor
    "Bus_500C":   { "frequency": 8,  "first_departure": 300, "last_departure": 1380 },  # CMBT–Kilambakkam via GST
    "Bus_502":    { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # CMBT–Tambaram via GST
    "Bus_502A":   { "frequency": 15, "first_departure": 330, "last_departure": 1290 },  # Variant 502
    "Bus_508":    { "frequency": 15, "first_departure": 330, "last_departure": 1260 },  # Tambaram–Tiruporur

    # OMR Corridor
    "Bus_102":    { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Central–Sholinganallur
    "Bus_119":    { "frequency": 15, "first_departure": 330, "last_departure": 1260 },  # Tambaram–Sholinganallur
    "Bus_119A":   { "frequency": 20, "first_departure": 360, "last_departure": 1200 },  # Tambaram–Kelambakkam
    "Bus_570":    { "frequency": 10, "first_departure": 300, "last_departure": 1380 },  # CMBT–Sholinganallur via OMR
    "Bus_570A":   { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Broadway–Navallur
    "Bus_574":    { "frequency": 15, "first_departure": 330, "last_departure": 1260 },  # CMBT–Siruseri
    "Bus_576":    { "frequency": 20, "first_departure": 360, "last_departure": 1200 },  # Broadway–Kelambakkam
    "Bus_579":    { "frequency": 20, "first_departure": 360, "last_departure": 1200 },  # Central–Kelambakkam ECR
    "Bus_47":     { "frequency": 10, "first_departure": 300, "last_departure": 1380 },  # Adyar–Sholinganallur
    "Bus_47A":    { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Adyar–Thiruporur via ECR
    "Bus_47B":    { "frequency": 15, "first_departure": 330, "last_departure": 1260 },  # Central–Thiruporur ECR

    # T. Nagar / Guindy Corridor
    "Bus_21G":    { "frequency": 10, "first_departure": 300, "last_departure": 1380 },  # Guindy–Central via T.Nagar
    "Bus_21":     { "frequency": 8,  "first_departure": 300, "last_departure": 1380 },  # Tambaram–Central
    "Bus_21D":    { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Perungalathur–Egmore
    "Bus_5":      { "frequency": 8,  "first_departure": 270, "last_departure": 1380 },  # Broadway–CMBT via Central
    "Bus_5C":     { "frequency": 10, "first_departure": 300, "last_departure": 1350 },  # Broadway–Velachery

    # Anna Nagar / Northwest Corridor
    "Bus_70G":    { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Broadway–Avadi via Anna Nagar
    "Bus_70":     { "frequency": 10, "first_departure": 300, "last_departure": 1380 },  # Broadway–Ambattur
    "Bus_71":     { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Broadway–Pattabiram
    "Bus_29C":    { "frequency": 10, "first_departure": 300, "last_departure": 1380 },  # Central–Ambattur Industrial
    "Bus_10":     { "frequency": 8,  "first_departure": 270, "last_departure": 1380 },  # Broadway–Porur via Vadapalani
    "Bus_10A":    { "frequency": 10, "first_departure": 300, "last_departure": 1350 },  # Broadway–Poonamallee

    # Velachery / South Corridor
    "Bus_41":     { "frequency": 10, "first_departure": 300, "last_departure": 1350 },  # Broadway–Velachery
    "Bus_41A":    { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Central–Velachery via Adyar
    "Bus_56":     { "frequency": 15, "first_departure": 330, "last_departure": 1260 },  # T.Nagar–Velachery
    "Bus_5E":     { "frequency": 10, "first_departure": 300, "last_departure": 1350 },  # Broadway–Velachery via Saidapet

    # Besant Nagar / ECR Corridor
    "Bus_51":     { "frequency": 10, "first_departure": 300, "last_departure": 1350 },  # Broadway–Besant Nagar
    "Bus_52":     { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Broadway–Thiruvanmiyur
    "Bus_52A":    { "frequency": 15, "first_departure": 330, "last_departure": 1260 },  # Central–Injambakkam
    "Bus_43":     { "frequency": 15, "first_departure": 330, "last_departure": 1260 },  # Broadway–Airport via Saidapet

    # North Chennai
    "Bus_1":      { "frequency": 8,  "first_departure": 270, "last_departure": 1380 },  # Broadway–Thiruvottiyur
    "Bus_1A":     { "frequency": 10, "first_departure": 300, "last_departure": 1350 },  # Broadway–Wimco Nagar
    "Bus_20A":    { "frequency": 10, "first_departure": 300, "last_departure": 1350 },  # Perambur–Broadway
    "Bus_27B":    { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # T.Nagar–Anna Nagar

    # Kilambakkam / Intercity Feeder
    "Bus_500":    { "frequency": 10, "first_departure": 300, "last_departure": 1380 },  # CMBT–Vandalur
    "Bus_599":    { "frequency": 30, "first_departure": 360, "last_departure": 1260 },  # Kilambakkam–Kelambakkam

    # ── SETC Intercity ────────────────────────────────────────────────────────
    "SETC_Bus":         { "frequency": 20, "first_departure": 300, "last_departure": 1380 },
    "SETC_Trichy":      { "frequency": 30, "first_departure": 270, "last_departure": 1380 },
    "SETC_Madurai":     { "frequency": 30, "first_departure": 270, "last_departure": 1380 },
    "SETC_Coimbatore":  { "frequency": 45, "first_departure": 270, "last_departure": 1350 },
    "SETC_Pondicherry": { "frequency": 20, "first_departure": 300, "last_departure": 1380 },
    "SETC_Vellore":     { "frequency": 20, "first_departure": 300, "last_departure": 1380 },
    "SETC_Salem":       { "frequency": 30, "first_departure": 300, "last_departure": 1350 },

    # ── Trichy TNSTC City Buses ───────────────────────────────────────────────
    "Bus_T1":    { "frequency": 10, "first_departure": 300, "last_departure": 1380 },  # Chatram–Srirangam
    "Bus_T2":    { "frequency": 8,  "first_departure": 300, "last_departure": 1380 },  # Chatram–Thiruverambur
    "Bus_T3":    { "frequency": 10, "first_departure": 300, "last_departure": 1350 },  # Junction–Ariyamangalam
    "Bus_T4":    { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Junction–KK Nagar
    "Bus_T5":    { "frequency": 15, "first_departure": 330, "last_departure": 1290 },  # Chatram–Woraiyur
    "Bus_T7":    { "frequency": 12, "first_departure": 300, "last_departure": 1320 },  # Junction–Tennur
    "Bus_T10":   { "frequency": 15, "first_departure": 330, "last_departure": 1290 },  # Chatram–Golden Rock
    "Bus_T50":   { "frequency": 20, "first_departure": 330, "last_departure": 1260 },  # Junction–Manapparai
    "Bus_T51":   { "frequency": 20, "first_departure": 330, "last_departure": 1260 },  # Chatram–Lalgudi
    "Bus_T52":   { "frequency": 30, "first_departure": 360, "last_departure": 1200 },  # Junction–Musiri
    "Bus_T53":   { "frequency": 30, "first_departure": 360, "last_departure": 1200 },  # Chatram–Kulithalai
    "Bus_T54":   { "frequency": 30, "first_departure": 360, "last_departure": 1200 },  # Junction–Thuraiyur
    "Bus_T55":   { "frequency": 30, "first_departure": 360, "last_departure": 1200 },  # Chatram–Manachanallur
    "Bus_T58":   { "frequency": 20, "first_departure": 330, "last_departure": 1260 },  # Junction–Ponmalaipatti
}


# ── Haversine Distance ────────────────────────────────────────────────────────
def haversine_distance(coord1: Tuple[float, float],
                       coord2: Tuple[float, float]) -> float:
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ── Traffic Factor ────────────────────────────────────────────────────────────
def get_traffic_factor(time_of_day_min: int) -> float:
    """1.5× delay during Chennai/Trichy peak hours."""
    if (480 <= time_of_day_min <= 630) or (1020 <= time_of_day_min <= 1230):
        return 1.5
    return 1.0


# ── Next Departure Calculator ─────────────────────────────────────────────────
def get_next_departure(mode: str, line: str, current_time: int,
                       disrupted_modes: List[str]) -> Optional[int]:
    """Returns next departure (minutes from midnight) or None if disrupted/ended."""
    if mode in disrupted_modes:
        return None

    # Instantaneous modes
    if mode in ("Rapido_Bike", "Ola_Auto", "Walk"):
        return current_time

    # Build schedule key
    sched_key = mode
    if mode in ("MTC_Bus", "TNSTC_Bus", "SETC_Bus"):
        candidate = line.replace(" ", "_")
        if candidate in SCHEDULES:
            sched_key = candidate
        elif mode == "SETC_Bus":
            sched_key = "SETC_Bus"
        else:
            sched_key = "Suburban_Train"   # safe fallback frequency

    if sched_key not in SCHEDULES:
        return current_time

    sched = SCHEDULES[sched_key]
    freq  = sched["frequency"]
    start = sched["first_departure"]
    end   = sched["last_departure"]

    if current_time < start:
        return start
    if current_time > end:
        return None

    elapsed   = current_time - start
    intervals = math.ceil(elapsed / freq)
    next_dep  = start + intervals * freq
    return next_dep if next_dep <= end else None

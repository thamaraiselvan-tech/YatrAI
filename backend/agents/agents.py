"""
agents/agents.py
AI-powered query parsing and bilingual text generation for YatrAI.
Uses Google Gemini for NLP, with keyword-based fallback when API key is unavailable.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional

# Try to import and initialize Google GenAI
_client = None
try:
    from google import genai
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if api_key:
        _client = genai.Client(api_key=api_key)
except Exception:
    _client = None

# ── Node alias mappings (200+ aliases) ────────────────────────────────────────
NODE_ALIASES: Dict[str, str] = {
    # ── SRM Campus ────────────────────────────────────────────────────────────
    "srm": "SRM_Dorm", "srm dorm": "SRM_Dorm", "srm hostel": "SRM_Dorm",
    "srm university": "SRM_Dorm", "srm campus": "SRM_Dorm",

    # ── Chennai Suburban Rail Stations ─────────────────────────────────────────
    "beach station": "Chennai_Beach", "chennai beach": "Chennai_Beach",
    "fort station": "Chennai_Fort", "chennai fort": "Chennai_Fort",
    "park station": "Chennai_Park", "park town": "Chennai_Park",
    "central": "Chennai_Central", "chennai central": "Chennai_Central",
    "central station": "Chennai_Central",
    "egmore": "Chennai_Egmore", "chennai egmore": "Chennai_Egmore",
    "chetpet": "Chetpet", "chetpet station": "Chetpet",
    "nungambakkam": "Nungambakkam", "nungambakkam station": "Nungambakkam",
    "kodambakkam": "Kodambakkam",
    "mambalam": "Mambalam", "mambalam station": "Mambalam",
    "saidapet": "Saidapet", "saidapet station": "Saidapet",
    "guindy": "Guindy_Station", "guindy station": "Guindy_Station",
    "st thomas mount": "St_Thomas_Mount",
    "pallavaram": "Pallavaram", "pallavaram station": "Pallavaram",
    "chromepet": "Chromepet", "chrompet": "Chromepet",
    "tambaram": "Tambaram_Station", "tbm": "Tambaram_Station",
    "tambaram station": "Tambaram_Station",
    "perungalathur": "Perungalathur",
    "vandalur": "Vandalur", "vandalur zoo": "Vandalur",
    "urapakkam": "Urapakkam",
    "guduvanchery": "Guduvanchery",
    "kattankulathur": "Kattankulathur_Station", "kattu": "Kattankulathur_Station",
    "potheri": "Potheri_Station", "potheri station": "Potheri_Station",
    "chengalpattu": "Chengalpattu", "cgl": "Chengalpattu",

    # ── Chennai Metro Stations ────────────────────────────────────────────────
    "wimco nagar": "Wimco_Nagar",
    "washermanpet": "Washermanpet",
    "mannadi": "Mannadi",
    "high court": "High_Court", "high court metro": "High_Court",
    "lic": "LIC_Metro", "lic metro": "LIC_Metro",
    "thousand lights": "Thousand_Lights",
    "ag dms": "AG_DMS", "agdms": "AG_DMS",
    "nandanam": "Nandanam", "nandanam metro": "Nandanam",
    "saidapet metro": "Saidapet_Metro",
    "little mount": "Little_Mount",
    "guindy metro": "Guindy_Metro",
    "alandur": "Alandur", "alandur metro": "Alandur",
    "nanganallur": "Nanganallur",
    "meenambakkam": "Meenambakkam", "meenambakkam metro": "Meenambakkam",
    "airport": "Airport", "chennai airport": "Airport", "maa": "Airport",
    "arumbakkam": "Arumbakkam",
    "vadapalani": "Vadapalani", "vadapalani metro": "Vadapalani",
    "ashok nagar": "Ashok_Nagar",
    "ekkattuthangal": "Ekkattuthangal",

    # ── Chennai Bus Stands ────────────────────────────────────────────────────
    "koyambedu": "Koyambedu_CMBT", "cmbt": "Koyambedu_CMBT",
    "koyambedu cmbt": "Koyambedu_CMBT",
    "kilambakkam": "Kilambakkam_KCBT", "kcbt": "Kilambakkam_KCBT",
    "new bus stand": "Kilambakkam_KCBT",
    "broadway": "Broadway_Bus", "broadway bus stand": "Broadway_Bus",
    "tambaram bus stand": "Tambaram_Bus_Stand",
    "t nagar bus stand": "T_Nagar_Bus_Stand",

    # ── Chennai Temples ───────────────────────────────────────────────────────
    "kapaleeshwarar": "Kapaleeshwarar_Temple", "kapaleeshwarar temple": "Kapaleeshwarar_Temple",
    "mylapore temple": "Kapaleeshwarar_Temple", "கபாலீஸ்வரர்": "Kapaleeshwarar_Temple",
    "parthasarathy": "Parthasarathy_Temple", "parthasarathy temple": "Parthasarathy_Temple",
    "triplicane temple": "Parthasarathy_Temple",
    "marundeeswarar": "Marundeeswarar_Temple", "thiruvanmiyur temple": "Marundeeswarar_Temple",
    "ashtalakshmi": "Ashtalakshmi_Temple", "ashtalakshmi temple": "Ashtalakshmi_Temple",
    "vadapalani murugan": "Vadapalani_Murugan", "vadapalani temple": "Vadapalani_Murugan",
    "kalikambal": "Kalikambal_Temple", "kalikambal temple": "Kalikambal_Temple",
    "iskcon": "ISKCON_Chennai", "iskcon chennai": "ISKCON_Chennai", "hare krishna": "ISKCON_Chennai",
    "birla mandir": "Birla_Mandir", "birla temple": "Birla_Mandir",
    "thiruverkadu": "Thiruverkadu_Devi", "thiruverkadu temple": "Thiruverkadu_Devi",
    "kundrathur": "Kundrathur_Murugan", "kundrathur temple": "Kundrathur_Murugan",

    # ── Chennai Malls ─────────────────────────────────────────────────────────
    "phoenix mall": "Phoenix_MarketCity", "phoenix marketcity": "Phoenix_MarketCity",
    "phoenix velachery": "Phoenix_MarketCity",
    "express avenue": "Express_Avenue", "ea mall": "Express_Avenue",
    "vr mall": "VR_Mall_Anna_Nagar", "vr chennai": "VR_Mall_Anna_Nagar",
    "forum vijaya": "Forum_Vijaya", "forum mall": "Forum_Vijaya",
    "ampa skywalk": "Ampa_Skywalk",
    "spencer plaza": "Spencer_Plaza", "spencers": "Spencer_Plaza",
    "palladium": "Palladium_Mall", "palladium mall": "Palladium_Mall",

    # ── Chennai Hospitals ─────────────────────────────────────────────────────
    "apollo": "Apollo_Hospital", "apollo hospital": "Apollo_Hospital",
    "fortis malar": "Fortis_Malar", "fortis hospital": "Fortis_Malar",
    "miot": "MIOT_Hospital", "miot hospital": "MIOT_Hospital",
    "rajiv gandhi hospital": "Rajiv_Gandhi_GH", "rgggh": "Rajiv_Gandhi_GH",
    "general hospital": "Govt_General_Hospital",

    # ── Chennai Landmarks & Areas ─────────────────────────────────────────────
    "marina beach": "Marina_Beach", "marina": "Marina_Beach",
    "elliot beach": "Elliot_Beach", "elliots beach": "Elliot_Beach", "bessy beach": "Elliot_Beach",
    "besant nagar beach": "Besant_Nagar_Beach", "besant nagar": "Besant_Nagar_Beach",
    "valluvar kottam": "Valluvar_Kottam",
    "fort st george": "Fort_St_George", "fort": "Fort_St_George",
    "iit madras": "IIT_Madras", "iit chennai": "IIT_Madras", "iitm": "IIT_Madras",
    "anna university": "Anna_University", "anna univ": "Anna_University",
    "tidel park": "Tidel_Park", "tidel": "Tidel_Park",
    "omr tidel": "OMR_Tidel_Park",
    "sholinganallur": "OMR_Sholinganallur", "omr": "OMR_Sholinganallur",
    "velachery": "Velachery", "adyar": "Adyar",
    "t nagar": "T_Nagar", "t. nagar": "T_Nagar", "tnagar": "T_Nagar", "thyagaraya nagar": "T_Nagar",
    "mylapore": "Mylapore",
    "thiruvanmiyur": "Thiruvanmiyur",
    "royapettah": "Royapettah",
    "george town": "George_Town",
    "porur": "Porur_Junction", "porur junction": "Porur_Junction",
    "avadi": "Avadi",
    "ambattur": "Ambattur",
    "anna nagar": "Anna_Nagar_Tower", "anna nagar tower": "Anna_Nagar_Tower",
    "perambur": "Perambur",
    "dlf it park": "DLF_IT_Park",
    "sipcot": "SIPCOT_IT_Park",

    # ── Trichy Stations ───────────────────────────────────────────────────────
    "trichy": "Trichy_Junction", "tiruchirappalli": "Trichy_Junction",
    "trichy junction": "Trichy_Junction", "trichy station": "Trichy_Junction",
    "srirangam": "Srirangam_Station", "srirangam station": "Srirangam_Station",
    "lalgudi": "Lalgudi",
    "golden rock": "Golden_Rock", "ponmalai": "Golden_Rock",
    "thiruverumbur": "Thiruverumbur",

    # ── Trichy Temples ────────────────────────────────────────────────────────
    "ranganathaswamy": "Ranganathaswamy_Temple", "ranganathar temple": "Ranganathaswamy_Temple",
    "srirangam temple": "Ranganathaswamy_Temple", "ஸ்ரீரங்கம்": "Ranganathaswamy_Temple",
    "rockfort": "Rockfort_Temple", "rockfort temple": "Rockfort_Temple",
    "ucchi pillayar": "Ucchi_Pillayar_Temple", "rock fort ganesh": "Ucchi_Pillayar_Temple",
    "jambukeswarar": "Jambukeswarar_Temple", "thiruvanaikaval": "Jambukeswarar_Temple",
    "samayapuram": "Samayapuram_Mariamman", "samayapuram temple": "Samayapuram_Mariamman",
    "thayumanavar": "Thayumanavar_Temple",

    # ── Trichy Other ──────────────────────────────────────────────────────────
    "femina mall": "Femina_Mall_Trichy", "femina mall trichy": "Femina_Mall_Trichy",
    "chattram bus stand": "Chattram_Bus_Stand", "chattram": "Chattram_Bus_Stand",
    "chathiram bus stand": "Chattram_Bus_Stand", "chathiram": "Chattram_Bus_Stand",
    "trichy bus stand": "Central_Bus_Stand_Trichy", "central bus stand trichy": "Central_Bus_Stand_Trichy",
    "trichy central bus stand": "Central_Bus_Stand_Trichy", "central bus stand": "Central_Bus_Stand_Trichy",
    "trichy central": "Central_Bus_Stand_Trichy", "trichy cbs": "Central_Bus_Stand_Trichy",
    "cbs": "Central_Bus_Stand_Trichy", "tiruchirappalli junction": "Trichy_Junction",
    "tiruchirapalli junction": "Trichy_Junction",
    "teppakulam": "Teppakulam",
    "woraiyur": "Woraiyur",
    "bhel": "BHEL_Township", "bhel township": "BHEL_Township",
    "nit trichy": "NIT_Trichy", "nit tiruchirappalli": "NIT_Trichy",
    "trichy airport": "Trichy_Airport",
    "kallanai": "Kallanai_Dam", "grand anicut": "Kallanai_Dam",
    "kmc hospital trichy": "KMC_Hospital_Trichy",

    # ── Intercity Highway ─────────────────────────────────────────────────────
    "villupuram": "Villupuram",
    "ulundurpet": "Ulundurpet",
    "perambalur": "Perambalur",
    "ariyalur": "Ariyalur",

    # ── Other Intercity ───────────────────────────────────────────────────────
    "coimbatore": "Coimbatore", "kovai": "Coimbatore",
    "madurai": "Madurai",
    "pondicherry": "Pondicherry", "pondy": "Pondicherry", "puducherry": "Pondicherry",
    "vellore": "Vellore", "kanchipuram": "Kanchipuram", "kanchi": "Kanchipuram",
}

# ── Mood detection ────────────────────────────────────────────────────────────
MOOD_KEYWORDS: Dict[str, List[str]] = {
    "fastest": ["fast", "quick", "hurry", "urgent", "rush", "speed", "earliest", "soon", "vegam", "viraivu"],
    "cheapest": ["cheap", "budget", "save money", "low cost", "economical", "thrifty", "minimum fare", "kammi selavu"],
    "greenest": ["green", "eco", "environment", "carbon", "sustainable", "low emission", "pasumai"],
    "safest": ["safe", "secure", "comfortable", "reliable", "padhugappu"],
}

# ── Tamil detection ───────────────────────────────────────────────────────────
TAMIL_INDICATORS = [
    "irundhu", "irunthu", "ku", "la", "lam", "poga", "poganum",
    "vaanga", "selva", "sellu", "epdi", "eppadi", "enna",
    "enga", "engey", "engal", "yaaruku", "enakku",
    "போக", "இருந்து", "எப்படி", "வேணும்", "பஸ்", "ரயில்",
]


def _detect_tamil(query: str) -> bool:
    """Check if query contains Tamil words or characters."""
    q = query.lower()
    # Check for Tamil Unicode range
    if any("\u0B80" <= ch <= "\u0BFF" for ch in query):
        return True
    # Check for Tanglish indicators
    return any(indicator in q for indicator in TAMIL_INDICATORS)


def _resolve_node(text: str) -> Optional[str]:
    """Try to match text to a known transit node."""
    text = text.strip().lower()
    # Direct alias match
    if text in NODE_ALIASES:
        return NODE_ALIASES[text]
    # Partial match: sort by length descending to match longest alias first
    sorted_aliases = sorted(NODE_ALIASES.keys(), key=len, reverse=True)
    for alias in sorted_aliases:
        if alias in text:
            return NODE_ALIASES[alias]
    # Fuzzy: try matching underscored versions
    text_clean = text.replace(" ", "_").title()
    from data.database import COORDINATES
    if text_clean in COORDINATES:
        return text_clean
    return None


def _extract_time(query: str, default_time: Optional[int] = None) -> int:
    """Extract departure time from query. Default: current time."""
    if default_time is None:
        from datetime import datetime
        now = datetime.now()
        default_time = now.hour * 60 + now.minute

    # Match patterns like "8am", "8:30 am", "14:00", "2 pm", "morning", "evening"
    time_match = re.search(r'(\d{1,2})\s*:\s*(\d{2})\s*(am|pm)?', query, re.IGNORECASE)
    if time_match:
        h, m = int(time_match.group(1)), int(time_match.group(2))
        period = (time_match.group(3) or "").lower()
        if period == "pm" and h < 12:
            h += 12
        elif period == "am" and h == 12:
            h = 0
        return h * 60 + m

    time_match = re.search(r'(\d{1,2})\s*(am|pm)', query, re.IGNORECASE)
    if time_match:
        h = int(time_match.group(1))
        period = time_match.group(2).lower()
        if period == "pm" and h < 12:
            h += 12
        elif period == "am" and h == 12:
            h = 0
        return h * 60

    # Keywords
    q = query.lower()
    if "morning" in q or "காலை" in q:
        return 480   # 8 AM
    elif "afternoon" in q or "மதியம்" in q:
        return 780   # 1 PM
    elif "evening" in q or "மாலை" in q:
        return 1020  # 5 PM
    elif "night" in q or "இரவு" in q:
        return 1260  # 9 PM
    elif "now" in q or "இப்போ" in q:
        from datetime import datetime
        now = datetime.now()
        return now.hour * 60 + now.minute

    return default_time


def _detect_mood(query: str) -> str:
    """Detect travel preference mood from query text."""
    q = query.lower()
    for mood, keywords in MOOD_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            return mood
    return "fastest"  # Default


def _fallback_parse(query: str, current_time_min: int) -> Dict[str, Any]:
    """
    Keyword-based fallback parser when Gemini is unavailable.
    Extracts start/end nodes, time, mood, and Tamil flag from natural language.
    """
    q = query.lower()
    is_tamil = _detect_tamil(query)

    # Try to extract "from X to Y" pattern
    from_to = re.search(r'from\s+(.+?)\s+to\s+(.+?)(?:\s+at|\s+by|\s+in|\s*$)', q)
    if not from_to:
        # Try Tamil-style "X irundhu Y ku"
        from_to = re.search(r'(.+?)\s+(?:irundhu|irunthu|இருந்து)\s+(.+?)(?:\s+ku|\s+க்கு|\s*$)', q)
    if not from_to:
        # Try "X to Y"
        from_to = re.search(r'(.+?)\s+to\s+(.+?)(?:\s+at|\s+by|\s+in|\s*$)', q)

    start_node = "SRM_Dorm"
    target_node = "Chennai_Central"

    if from_to:
        start_text = from_to.group(1).strip()
        end_text = from_to.group(2).strip()
        resolved_start = _resolve_node(start_text)
        resolved_end = _resolve_node(end_text)
        if resolved_start:
            start_node = resolved_start
        if resolved_end:
            target_node = resolved_end
    else:
        # Try to find any known location in the query
        found_nodes = []
        for alias, node in NODE_ALIASES.items():
            if alias in q and node not in found_nodes:
                found_nodes.append(node)
        if len(found_nodes) >= 2:
            start_node, target_node = found_nodes[0], found_nodes[1]
        elif len(found_nodes) == 1:
            target_node = found_nodes[0]

    return {
        "start_node": start_node,
        "target_node": target_node,
        "start_time_min": _extract_time(query, current_time_min),
        "mood": _detect_mood(query),
        "is_tamil": is_tamil,
    }


def parse_user_query(query: str) -> Dict[str, Any]:
    """
    Parse a natural language travel query into structured routing parameters.
    Uses Gemini API when available, falls back to keyword matching.

    Returns:
        {
            "start_node": str,
            "target_node": str,
            "start_time_min": int,
            "mood": str,   # fastest | cheapest | greenest | safest
            "is_tamil": bool,
        }
    """
    from datetime import datetime
    now = datetime.now()
    current_time_min = now.hour * 60 + now.minute

    if _client:
        try:
            from data.database import COORDINATES
            node_list = list(COORDINATES.keys())
            prompt = f"""You are a transit assistant for Tamil Nadu, India.
Parse the user travel query and extract:
1. start_node: The starting location (must be one of: {', '.join(node_list)})
2. target_node: The destination (must be one of: {', '.join(node_list)})
3. start_time_min: Departure time in minutes from midnight (e.g., 8:00 AM = 480). If the query does not specify a specific time (e.g. 10am, 2pm, etc.), you MUST default to the current time: {current_time_min}.
4. mood: One of "fastest", "cheapest", "greenest", "safest"
5. is_tamil: true if the query is in Tamil or Tanglish

Respond ONLY with valid JSON, no markdown.

User query: "{query}"
"""
            response = _client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            text = response.text.strip()
            # Remove markdown code fences if present
            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            parsed = json.loads(text)

            # Validate nodes
            if parsed.get("start_node") not in node_list:
                parsed["start_node"] = _resolve_node(parsed.get("start_node", "")) or "SRM_Dorm"
            if parsed.get("target_node") not in node_list:
                parsed["target_node"] = _resolve_node(parsed.get("target_node", "")) or "Chennai_Central"
            if parsed.get("mood") not in ("fastest", "cheapest", "greenest", "safest"):
                parsed["mood"] = "fastest"
            if not isinstance(parsed.get("start_time_min"), (int, float)):
                parsed["start_time_min"] = _extract_time(query, current_time_min)
            parsed["is_tamil"] = parsed.get("is_tamil", _detect_tamil(query))

            return parsed
        except Exception:
            pass

    # Fallback
    return _fallback_parse(query, current_time_min)


def generate_bilingual_brief(query: str, route: Dict[str, Any], is_tamil: bool) -> Dict[str, str]:
    """
    Generate a human-friendly bilingual (English + Tamil) summary of a route.

    Returns:
        {"en": "English summary...", "ta": "Tamil summary..."}
    """
    segments = route.get("segments", [])
    total_time = route.get("total_time", 0)
    total_fare = route.get("total_fare", 0)
    total_co2 = route.get("total_co2", 0)
    start_time = route.get("start_time_str", "")
    end_time = route.get("end_time_str", "")

    if not segments:
        return {
            "en": "No route segments available.",
            "ta": "பாதை தகவல்கள் கிடைக்கவில்லை.",
        }

    start_node = segments[0]["from_node"].replace("_", " ")
    end_node = segments[-1]["to_node"].replace("_", " ")
    mode_list = list(dict.fromkeys(seg["mode"].replace("_", " ") for seg in segments))
    modes_str = ", ".join(mode_list)

    en_brief = (
        f"Travel from {start_node} to {end_node} using {modes_str}. "
        f"Depart at {start_time}, arrive by {end_time}. "
        f"Total journey: {total_time:.0f} min | ₹{total_fare:.0f} | {total_co2:.0f}g CO₂. "
        f"This route has {len(segments)} segment(s)."
    )

    ta_brief = (
        f"{start_node} லிருந்து {end_node} வரை {modes_str} மூலம் பயணம். "
        f"புறப்படும் நேரம்: {start_time}, வருகை: {end_time}. "
        f"மொத்த பயணம்: {total_time:.0f} நிமிடம் | ₹{total_fare:.0f} | {total_co2:.0f}g CO₂. "
        f"இந்த பாதையில் {len(segments)} பகுதி(கள்) உள்ளன."
    )

    if _client and is_tamil:
        try:
            prompt = f"""You are a Tamil-English bilingual transit guide.
Given this route summary, create a natural, friendly one-paragraph brief in both English and Tamil.
Route: {start_node} → {end_node}
Modes: {modes_str}
Time: {start_time} to {end_time} ({total_time:.0f} min)
Fare: ₹{total_fare:.0f}
CO2: {total_co2:.0f}g

Respond ONLY with valid JSON: {{"en": "...", "ta": "..."}}"""
            response = _client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            text = response.text.strip()
            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            result = json.loads(text)
            if "en" in result and "ta" in result:
                return result
        except Exception:
            pass

    return {"en": en_brief, "ta": ta_brief}


def parse_semantic_journal_log(text: str) -> Dict[str, Any]:
    """
    Parse a natural language journal entry into structured data.

    Input: "Went from Guindy to OMR by Metro, spent ₹40"
    Returns: {from_node, to_node, modes_used, cost, co2_saved, notes, category}
    """
    if _client:
        try:
            from data.database import COORDINATES
            node_list = list(COORDINATES.keys())
            prompt = f"""Parse this travel log into structured data.
Known nodes: {', '.join(node_list)}
Known modes: Walk, Suburban_Train, Metro, MTC_Bus, SETC_Bus, Rapido_Bike, Ola_Auto, Intercity_Train

Input: "{text}"

Respond ONLY with valid JSON:
{{
    "from_node": "...",
    "to_node": "...",
    "modes_used": ["..."],
    "cost": 0.0,
    "co2_saved": 0.0,
    "notes": "...",
    "category": "Commute"
}}"""
            response = _client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            result_text = response.text.strip()
            result_text = re.sub(r'^```(?:json)?\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            return json.loads(result_text)
        except Exception:
            pass

    # Fallback: basic extraction
    q = text.lower()

    # Try "from X to Y"
    from_to = re.search(r'from\s+(.+?)\s+to\s+(.+?)(?:\s+by|\s+via|\s+using|\s*,|\s*$)', q)
    from_node = "SRM_Dorm"
    to_node = "Chennai_Central"
    if from_to:
        resolved_start = _resolve_node(from_to.group(1))
        resolved_end = _resolve_node(from_to.group(2))
        if resolved_start:
            from_node = resolved_start
        if resolved_end:
            to_node = resolved_end

    # Extract modes
    modes_found = []
    mode_keywords = {
        "walk": "Walk", "metro": "Metro", "train": "Suburban_Train",
        "suburban": "Suburban_Train", "bus": "MTC_Bus", "mtc": "MTC_Bus",
        "setc": "SETC_Bus", "rapido": "Rapido_Bike", "bike": "Rapido_Bike",
        "ola": "Ola_Auto", "auto": "Ola_Auto",
    }
    for kw, mode in mode_keywords.items():
        if kw in q and mode not in modes_found:
            modes_found.append(mode)
    if not modes_found:
        modes_found = ["MTC_Bus"]

    # Extract cost
    cost_match = re.search(r'(?:₹|rs\.?|rupees?)\s*(\d+)', q)
    cost = float(cost_match.group(1)) if cost_match else 0.0

    return {
        "from_node": from_node,
        "to_node": to_node,
        "modes_used": modes_found,
        "cost": cost,
        "co2_saved": round(cost * 0.5, 1),  # Rough estimate
        "notes": text,
        "category": "Commute",
    }


def query_journal_history(question: str, journal_data: Dict[str, Any]) -> str:
    """
    Answer a question about past journal entries using AI or keyword search.

    Args:
        question: Natural language question about travel history
        journal_data: Full journal data from journal_service.read_journal()

    Returns:
        A string answer to the question.
    """
    entries = journal_data.get("entries", [])

    if _client:
        try:
            entries_text = json.dumps(entries[:50], indent=2)  # Limit context
            prompt = f"""You are a Tamil Nadu travel history assistant.
Answer the user's question based on their past travel journal entries.
If you can't find the answer in the data, say so politely.

Travel Journal Entries:
{entries_text}

Question: "{question}"

Respond with a helpful, concise answer."""
            response = _client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return response.text.strip()
        except Exception:
            pass

    # Fallback: basic stats
    if not entries:
        return "No journal entries found. Start logging your trips to build travel history!"

    total_trips = len(entries)
    total_cost = sum(e.get("cost", 0) for e in entries)
    total_co2 = sum(e.get("co2_saved", 0) for e in entries)
    modes_used = {}
    for e in entries:
        for m in e.get("modes_used", []):
            modes_used[m] = modes_used.get(m, 0) + 1

    q = question.lower()
    if "cost" in q or "spend" in q or "money" in q or "fare" in q:
        return f"You've spent a total of ₹{total_cost:.0f} across {total_trips} trips."
    elif "co2" in q or "carbon" in q or "green" in q:
        return f"You've saved approximately {total_co2:.0f}g of CO₂ across {total_trips} trips."
    elif "how many" in q or "total" in q:
        return f"You have {total_trips} trip(s) logged in your journal."
    elif "mode" in q or "transport" in q:
        mode_summary = ", ".join(f"{m}: {c} trips" for m, c in modes_used.items())
        return f"Transport modes used: {mode_summary}"
    else:
        return (
            f"Journal summary: {total_trips} trips logged, "
            f"₹{total_cost:.0f} total spent, {total_co2:.0f}g CO₂ saved. "
            f"Ask about costs, CO₂ savings, or transport modes for details."
        )

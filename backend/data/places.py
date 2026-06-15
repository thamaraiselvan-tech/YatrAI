"""
data/places.py
Rich POI metadata for every place in the YatrAI transit graph.
Categories, Tamil names, timings, tags for search and display.
"""

from typing import Dict, Any, List

# ══════════════════════════════════════════════════════════════════════════════
# PLACE METADATA
# ══════════════════════════════════════════════════════════════════════════════
PLACES: Dict[str, Dict[str, Any]] = {

    # ── CHENNAI: Railway Stations ────────────────────────────────────────────
    "Chennai_Beach": {"name": "Chennai Beach Station", "tamil_name": "சென்னை கடற்கரை", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "George Town", "tags": ["terminal", "suburban"]},
    "Chennai_Fort": {"name": "Chennai Fort Station", "tamil_name": "சென்னை கோட்டை", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "George Town", "tags": ["suburban"]},
    "Chennai_Park": {"name": "Chennai Park Station", "tamil_name": "சென்னை பார்க்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Park Town", "tags": ["suburban"]},
    "Chennai_Egmore": {"name": "Chennai Egmore Station", "tamil_name": "சென்னை எழும்பூர்", "category": "station", "sub_category": "main_rail", "city": "Chennai", "area": "Egmore", "tags": ["terminal", "intercity", "southern_railway"]},
    "Chennai_Central": {"name": "Chennai Central Station", "tamil_name": "சென்னை சென்ட்ரல்", "category": "station", "sub_category": "main_rail", "city": "Chennai", "area": "Park Town", "tags": ["terminal", "intercity", "southern_railway", "metro"]},
    "Chetpet": {"name": "Chetpet Station", "tamil_name": "சேத்புத்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Chetpet", "tags": ["suburban"]},
    "Nungambakkam": {"name": "Nungambakkam Station", "tamil_name": "நுங்கம்பாக்கம்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Nungambakkam", "tags": ["suburban"]},
    "Kodambakkam": {"name": "Kodambakkam Station", "tamil_name": "கோடம்பாக்கம்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Kodambakkam", "tags": ["suburban"]},
    "Mambalam": {"name": "Mambalam Station", "tamil_name": "மாம்பலம்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Mambalam", "tags": ["suburban"]},
    "Saidapet": {"name": "Saidapet Station", "tamil_name": "சைதாப்பேட்டை", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Saidapet", "tags": ["suburban"]},
    "Guindy_Station": {"name": "Guindy Station", "tamil_name": "கிண்டி", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Guindy", "tags": ["suburban", "interchange", "metro"]},
    "St_Thomas_Mount": {"name": "St. Thomas Mount Station", "tamil_name": "செயிண்ட் தாமஸ் மவுண்ட்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "St Thomas Mount", "tags": ["suburban"]},
    "Pallavaram": {"name": "Pallavaram Station", "tamil_name": "பல்லாவரம்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Pallavaram", "tags": ["suburban"]},
    "Chromepet": {"name": "Chromepet Station", "tamil_name": "குரோம்பேட்டை", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Chromepet", "tags": ["suburban"]},
    "Tambaram_Station": {"name": "Tambaram Station", "tamil_name": "தாம்பரம்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Tambaram", "tags": ["suburban", "junction", "interchange"]},
    "Perungalathur": {"name": "Perungalathur Station", "tamil_name": "பெருங்களத்தூர்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Perungalathur", "tags": ["suburban"]},
    "Vandalur": {"name": "Vandalur Station", "tamil_name": "வண்டலூர்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Vandalur", "tags": ["suburban", "zoo"]},
    "Urapakkam": {"name": "Urapakkam Station", "tamil_name": "ஊரப்பாக்கம்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Urapakkam", "tags": ["suburban"]},
    "Guduvanchery": {"name": "Guduvanchery Station", "tamil_name": "குடுவாஞ்சேரி", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Guduvanchery", "tags": ["suburban"]},
    "Kattankulathur_Station": {"name": "Kattankulathur Station", "tamil_name": "கட்டன்குளத்தூர்", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Kattankulathur", "tags": ["suburban", "srm"]},
    "Potheri_Station": {"name": "Potheri Station", "tamil_name": "போத்தேரி", "category": "station", "sub_category": "suburban_rail", "city": "Chennai", "area": "Potheri", "tags": ["suburban", "srm"]},
    "Chengalpattu": {"name": "Chengalpattu Junction", "tamil_name": "செங்கல்பட்டு", "category": "station", "sub_category": "main_rail", "city": "Chennai", "area": "Chengalpattu", "tags": ["junction", "intercity", "suburban"]},

    # ── CHENNAI: Metro Stations ──────────────────────────────────────────────
    "Wimco_Nagar": {"name": "Wimco Nagar Metro", "tamil_name": "விம்கோ நகர்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Wimco Nagar", "tags": ["metro", "blue_line"]},
    "Washermanpet": {"name": "Washermanpet Metro", "tamil_name": "வாஷர்மேன்பேட்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Washermanpet", "tags": ["metro", "blue_line"]},
    "Mannadi": {"name": "Mannadi Metro", "tamil_name": "மண்ணடி", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Mannadi", "tags": ["metro", "blue_line"]},
    "High_Court": {"name": "High Court Metro", "tamil_name": "உயர் நீதிமன்றம்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "High Court", "tags": ["metro", "blue_line"]},
    "LIC_Metro": {"name": "LIC Metro", "tamil_name": "எல்ஐசி", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Mount Road", "tags": ["metro", "blue_line"]},
    "Thousand_Lights": {"name": "Thousand Lights Metro", "tamil_name": "தௌசண்ட் லைட்ஸ்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Thousand Lights", "tags": ["metro", "blue_line"]},
    "AG_DMS": {"name": "AG-DMS Metro", "tamil_name": "ஏஜி-டிஎம்எஸ்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "AG DMS", "tags": ["metro", "blue_line"]},
    "Nandanam": {"name": "Nandanam Metro", "tamil_name": "நந்தனம்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Nandanam", "tags": ["metro", "blue_line"]},
    "Saidapet_Metro": {"name": "Saidapet Metro", "tamil_name": "சைதாப்பேட்டை மெட்ரோ", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Saidapet", "tags": ["metro", "blue_line"]},
    "Little_Mount": {"name": "Little Mount Metro", "tamil_name": "லிட்டில் மவுண்ட்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Little Mount", "tags": ["metro", "blue_line"]},
    "Guindy_Metro": {"name": "Guindy Metro", "tamil_name": "கிண்டி மெட்ரோ", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Guindy", "tags": ["metro", "blue_line"]},
    "Alandur": {"name": "Alandur Metro", "tamil_name": "ஆலந்தூர்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Alandur", "tags": ["metro", "blue_line", "interchange"]},
    "Nanganallur": {"name": "Nanganallur Road Metro", "tamil_name": "நாங்கநல்லூர்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Nanganallur", "tags": ["metro", "blue_line"]},
    "Meenambakkam": {"name": "Meenambakkam Metro", "tamil_name": "மீனம்பாக்கம்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Meenambakkam", "tags": ["metro", "blue_line"]},
    "Airport": {"name": "Chennai Airport", "tamil_name": "சென்னை விமான நிலையம்", "category": "station", "sub_category": "airport", "city": "Chennai", "area": "Tirusulam", "tags": ["airport", "metro", "international"]},
    "Arumbakkam": {"name": "Arumbakkam Metro", "tamil_name": "அரும்பாக்கம்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Arumbakkam", "tags": ["metro", "green_line"]},
    "Vadapalani": {"name": "Vadapalani Metro", "tamil_name": "வடபழனி", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Vadapalani", "tags": ["metro", "green_line"]},
    "Ashok_Nagar": {"name": "Ashok Nagar Metro", "tamil_name": "அசோக் நகர்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Ashok Nagar", "tags": ["metro", "green_line"]},
    "Ekkattuthangal": {"name": "Ekkattuthangal Metro", "tamil_name": "எக்கட்டுத்தாங்கல்", "category": "station", "sub_category": "metro", "city": "Chennai", "area": "Ekkattuthangal", "tags": ["metro", "green_line"]},

    # ── CHENNAI: Bus Stands ──────────────────────────────────────────────────
    "Koyambedu_CMBT": {"name": "Koyambedu CMBT", "tamil_name": "கோயம்பேடு", "category": "station", "sub_category": "bus_stand", "city": "Chennai", "area": "Koyambedu", "tags": ["cmbt", "intercity", "bus_terminal"]},
    "Kilambakkam_KCBT": {"name": "Kilambakkam KCBT", "tamil_name": "கிளம்பாக்கம்", "category": "station", "sub_category": "bus_stand", "city": "Chennai", "area": "Kilambakkam", "tags": ["kcbt", "intercity", "bus_terminal"]},
    "Broadway_Bus": {"name": "Broadway Bus Terminus", "tamil_name": "பிராட்வே", "category": "station", "sub_category": "bus_stand", "city": "Chennai", "area": "George Town", "tags": ["bus_terminal", "local"]},
    "Tambaram_Bus_Stand": {"name": "Tambaram Bus Stand", "tamil_name": "தாம்பரம் பேருந்து நிலையம்", "category": "station", "sub_category": "bus_stand", "city": "Chennai", "area": "Tambaram", "tags": ["bus_stand", "local"]},
    "T_Nagar_Bus_Stand": {"name": "T.Nagar Bus Terminus", "tamil_name": "தியாகராய நகர்", "category": "station", "sub_category": "bus_stand", "city": "Chennai", "area": "T Nagar", "tags": ["bus_stand", "local"]},

    # ── CHENNAI: Temples ─────────────────────────────────────────────────────
    "Kapaleeshwarar_Temple": {"name": "Kapaleeshwarar Temple", "tamil_name": "கபாலீஸ்வரர் கோவில்", "category": "temple", "city": "Chennai", "area": "Mylapore", "tags": ["shiva", "dravidian", "historic", "mylapore"], "timings": "5:30 AM – 12:00 PM, 4:00 PM – 9:30 PM"},
    "Parthasarathy_Temple": {"name": "Parthasarathy Temple", "tamil_name": "பார்த்தசாரதி கோவில்", "category": "temple", "city": "Chennai", "area": "Triplicane", "tags": ["vishnu", "divyadesam", "historic"], "timings": "6:00 AM – 12:00 PM, 4:00 PM – 9:00 PM"},
    "Marundeeswarar_Temple": {"name": "Marundeeswarar Temple", "tamil_name": "மருந்தீஸ்வரர் கோவில்", "category": "temple", "city": "Chennai", "area": "Thiruvanmiyur", "tags": ["shiva", "healing", "ancient"], "timings": "6:00 AM – 12:00 PM, 4:00 PM – 9:00 PM"},
    "Ashtalakshmi_Temple": {"name": "Ashtalakshmi Temple", "tamil_name": "அஷ்டலக்ஷ்மி கோவில்", "category": "temple", "city": "Chennai", "area": "Besant Nagar", "tags": ["lakshmi", "beach", "modern"], "timings": "6:30 AM – 12:00 PM, 4:00 PM – 8:30 PM"},
    "Vadapalani_Murugan": {"name": "Vadapalani Murugan Temple", "tamil_name": "வடபழனி முருகன் கோவில்", "category": "temple", "city": "Chennai", "area": "Vadapalani", "tags": ["murugan", "popular", "metro_access"], "timings": "5:00 AM – 12:30 PM, 4:00 PM – 9:30 PM"},
    "Kalikambal_Temple": {"name": "Kalikambal Temple", "tamil_name": "காளிகாம்பாள் கோவில்", "category": "temple", "city": "Chennai", "area": "George Town", "tags": ["amman", "historic", "george_town"], "timings": "6:00 AM – 12:00 PM, 4:30 PM – 9:00 PM"},
    "ISKCON_Chennai": {"name": "ISKCON Temple Chennai", "tamil_name": "இஸ்கான் கோவில்", "category": "temple", "city": "Chennai", "area": "Injambakkam", "tags": ["krishna", "iskcon", "modern"], "timings": "4:30 AM – 1:00 PM, 4:00 PM – 9:00 PM"},
    "Birla_Mandir": {"name": "Birla Mandir", "tamil_name": "பிர்லா மந்திர்", "category": "temple", "city": "Chennai", "area": "Alandur", "tags": ["modern", "hillside", "scenic"], "timings": "6:00 AM – 12:00 PM, 4:00 PM – 8:00 PM"},
    "Thiruverkadu_Devi": {"name": "Thiruverkadu Devi Temple", "tamil_name": "திருவேற்காடு", "category": "temple", "city": "Chennai", "area": "Thiruverkadu", "tags": ["amman", "shakti_peetham"], "timings": "6:00 AM – 12:30 PM, 4:00 PM – 9:00 PM"},
    "Kundrathur_Murugan": {"name": "Kundrathur Murugan Temple", "tamil_name": "குன்றத்தூர் முருகன்", "category": "temple", "city": "Chennai", "area": "Kundrathur", "tags": ["murugan", "hilltop"], "timings": "6:00 AM – 12:00 PM, 4:00 PM – 8:30 PM"},

    # ── CHENNAI: Malls ───────────────────────────────────────────────────────
    "Phoenix_MarketCity": {"name": "Phoenix MarketCity", "tamil_name": "பீனிக்ஸ் மார்க்கெட்சிட்டி", "category": "mall", "city": "Chennai", "area": "Velachery", "tags": ["shopping", "cinema", "food_court"], "timings": "10:00 AM – 10:00 PM"},
    "Express_Avenue": {"name": "Express Avenue Mall", "tamil_name": "எக்ஸ்பிரஸ் அவென்யூ", "category": "mall", "city": "Chennai", "area": "Royapettah", "tags": ["shopping", "cinema", "luxury"], "timings": "10:00 AM – 10:00 PM"},
    "VR_Mall_Anna_Nagar": {"name": "VR Mall Anna Nagar", "tamil_name": "விஆர் மால்", "category": "mall", "city": "Chennai", "area": "Anna Nagar", "tags": ["shopping", "cinema", "food_court"], "timings": "10:00 AM – 10:00 PM"},
    "Forum_Vijaya": {"name": "Forum Vijaya Mall", "tamil_name": "ஃபோரம் விஜயா", "category": "mall", "city": "Chennai", "area": "Vadapalani", "tags": ["shopping", "cinema"], "timings": "10:00 AM – 9:30 PM"},
    "Ampa_Skywalk": {"name": "Ampa Skywalk Mall", "tamil_name": "அம்பா ஸ்கைவாக்", "category": "mall", "city": "Chennai", "area": "Aminjikarai", "tags": ["shopping", "cinema"], "timings": "10:00 AM – 9:30 PM"},
    "Spencer_Plaza": {"name": "Spencer Plaza", "tamil_name": "ஸ்பென்சர் பிளாசா", "category": "mall", "city": "Chennai", "area": "Mount Road", "tags": ["heritage", "shopping"], "timings": "9:30 AM – 9:00 PM"},
    "Palladium_Mall": {"name": "Palladium Mall", "tamil_name": "பல்லாடியம்", "category": "mall", "city": "Chennai", "area": "RA Puram", "tags": ["luxury", "premium"], "timings": "10:00 AM – 10:00 PM"},

    # ── CHENNAI: Hospitals ───────────────────────────────────────────────────
    "Apollo_Hospital": {"name": "Apollo Hospital Greams Road", "tamil_name": "அப்போலோ மருத்துவமனை", "category": "hospital", "city": "Chennai", "area": "Greams Road", "tags": ["multi_specialty", "private", "emergency"]},
    "Fortis_Malar": {"name": "Fortis Malar Hospital", "tamil_name": "ஃபோர்டிஸ் மலர்", "category": "hospital", "city": "Chennai", "area": "Adyar", "tags": ["cardiac", "private"]},
    "MIOT_Hospital": {"name": "MIOT Hospital", "tamil_name": "எம்ஐஓடி", "category": "hospital", "city": "Chennai", "area": "Manapakkam", "tags": ["ortho", "private"]},
    "Rajiv_Gandhi_GH": {"name": "Rajiv Gandhi Govt Hospital", "tamil_name": "ராஜீவ் காந்தி அரசு மருத்துவமனை", "category": "hospital", "city": "Chennai", "area": "Park Town", "tags": ["government", "emergency", "trauma"]},
    "Govt_General_Hospital": {"name": "Government General Hospital", "tamil_name": "அரசு பொது மருத்துவமனை", "category": "hospital", "city": "Chennai", "area": "Park Town", "tags": ["government", "teaching"]},

    # ── CHENNAI: Landmarks ───────────────────────────────────────────────────
    "Marina_Beach": {"name": "Marina Beach", "tamil_name": "மெரீனா கடற்கரை", "category": "landmark", "city": "Chennai", "area": "Marina", "tags": ["beach", "tourist", "iconic"]},
    "Elliot_Beach": {"name": "Elliot's Beach", "tamil_name": "எலியட் கடற்கரை", "category": "landmark", "city": "Chennai", "area": "Besant Nagar", "tags": ["beach", "popular", "evening"]},
    "Valluvar_Kottam": {"name": "Valluvar Kottam", "tamil_name": "வள்ளுவர் கோட்டம்", "category": "landmark", "city": "Chennai", "area": "Nungambakkam", "tags": ["monument", "thiruvalluvar", "cultural"]},
    "Fort_St_George": {"name": "Fort St. George", "tamil_name": "செயிண்ட் ஜார்ஜ் கோட்டை", "category": "landmark", "city": "Chennai", "area": "George Town", "tags": ["fort", "historic", "museum", "british"]},
    "IIT_Madras": {"name": "IIT Madras", "tamil_name": "ஐஐடி சென்னை", "category": "landmark", "city": "Chennai", "area": "Adyar", "tags": ["university", "campus", "research"]},
    "Anna_University": {"name": "Anna University", "tamil_name": "அண்ணா பல்கலைக்கழகம்", "category": "landmark", "city": "Chennai", "area": "Guindy", "tags": ["university", "campus"]},
    "SRM_Dorm": {"name": "SRM University", "tamil_name": "எஸ்ஆர்எம் பல்கலைக்கழகம்", "category": "landmark", "city": "Chennai", "area": "Kattankulathur", "tags": ["university", "campus", "hostel"]},

    # ── TRICHY: Railway Stations ─────────────────────────────────────────────
    "Trichy_Junction": {"name": "Tiruchirappalli Junction", "tamil_name": "திருச்சி சந்திப்பு", "category": "station", "sub_category": "main_rail", "city": "Trichy", "area": "Trichy Town", "tags": ["junction", "intercity", "major"]},
    "Srirangam_Station": {"name": "Srirangam Station", "tamil_name": "ஸ்ரீரங்கம்", "category": "station", "sub_category": "suburban_rail", "city": "Trichy", "area": "Srirangam", "tags": ["temple_town"]},
    "Lalgudi": {"name": "Lalgudi Station", "tamil_name": "லால்குடி", "category": "station", "sub_category": "suburban_rail", "city": "Trichy", "area": "Lalgudi", "tags": ["rural"]},
    "Golden_Rock": {"name": "Golden Rock Station", "tamil_name": "பொன்மலை", "category": "station", "sub_category": "suburban_rail", "city": "Trichy", "area": "Ponmalai", "tags": ["railway_workshop"]},
    "Thiruverumbur": {"name": "Thiruverumbur Station", "tamil_name": "திருவெறும்பூர்", "category": "station", "sub_category": "suburban_rail", "city": "Trichy", "area": "Thiruverumbur", "tags": ["suburban"]},

    # ── TRICHY: Temples ──────────────────────────────────────────────────────
    "Ranganathaswamy_Temple": {"name": "Sri Ranganathaswamy Temple", "tamil_name": "ஸ்ரீ ரங்கநாதசுவாமி கோவில்", "category": "temple", "city": "Trichy", "area": "Srirangam", "tags": ["vishnu", "divyadesam", "largest_temple", "heritage", "unesco"], "timings": "6:00 AM – 1:00 PM, 3:15 PM – 9:00 PM"},
    "Rockfort_Temple": {"name": "Rockfort Ucchi Pillayar Temple", "tamil_name": "மலைக்கோட்டை உச்சிப்பிள்ளையார்", "category": "temple", "city": "Trichy", "area": "Rockfort", "tags": ["ganesh", "hilltop", "iconic", "rock_cut"], "timings": "6:00 AM – 8:00 PM"},
    "Jambukeswarar_Temple": {"name": "Jambukeswarar Temple", "tamil_name": "ஜம்புகேஸ்வரர் கோவில்", "category": "temple", "city": "Trichy", "area": "Thiruvanaikaval", "tags": ["shiva", "pancha_bhoota", "water_element"], "timings": "6:00 AM – 12:30 PM, 3:30 PM – 8:30 PM"},
    "Samayapuram_Mariamman": {"name": "Samayapuram Mariamman Temple", "tamil_name": "சமயபுரம் மாரியம்மன்", "category": "temple", "city": "Trichy", "area": "Samayapuram", "tags": ["amman", "very_popular", "weekend_crowd"], "timings": "5:30 AM – 1:00 PM, 3:00 PM – 9:30 PM"},
    "Ucchi_Pillayar_Temple": {"name": "Ucchi Pillayar Temple", "tamil_name": "உச்சிப்பிள்ளையார் கோவில்", "category": "temple", "city": "Trichy", "area": "Rockfort", "tags": ["ganesh", "hilltop", "view"], "timings": "6:00 AM – 8:00 PM"},
    "Thayumanavar_Temple": {"name": "Thayumanavar Temple", "tamil_name": "தாயுமானவர் கோவில்", "category": "temple", "city": "Trichy", "area": "Rockfort", "tags": ["shiva", "rock_temple"], "timings": "6:00 AM – 12:00 PM, 4:00 PM – 8:30 PM"},

    # ── TRICHY: Malls & Markets ──────────────────────────────────────────────
    "Femina_Mall_Trichy": {"name": "Femina Mall", "tamil_name": "ஃபெமினா மால்", "category": "mall", "city": "Trichy", "area": "Salai Road", "tags": ["shopping", "cinema"], "timings": "10:00 AM – 9:30 PM"},
    "Chattram_Bus_Stand": {"name": "Chattram Bus Stand", "tamil_name": "சத்திரம் பேருந்து நிலையம்", "category": "station", "sub_category": "bus_stand", "city": "Trichy", "area": "Chattram", "tags": ["bus_terminal", "local"]},
    "Central_Bus_Stand_Trichy": {"name": "Central Bus Stand Trichy", "tamil_name": "மத்திய பேருந்து நிலையம்", "category": "station", "sub_category": "bus_stand", "city": "Trichy", "area": "Central", "tags": ["bus_terminal", "intercity"]},
    "Teppakulam": {"name": "Teppakulam Market", "tamil_name": "தெப்பக்குளம்", "category": "landmark", "city": "Trichy", "area": "Teppakulam", "tags": ["market", "flower_market", "traditional"]},

    # ── TRICHY: Hospitals ────────────────────────────────────────────────────
    "KMC_Hospital_Trichy": {"name": "KMC Hospital", "tamil_name": "கேஎம்சி மருத்துவமனை", "category": "hospital", "city": "Trichy", "area": "Manachanallur Road", "tags": ["multi_specialty", "private"]},
    "MGMGH_Trichy": {"name": "Mahatma Gandhi Memorial GH", "tamil_name": "மகாத்மா காந்தி அரசு மருத்துவமனை", "category": "hospital", "city": "Trichy", "area": "Rockfort", "tags": ["government", "teaching"]},

    # ── TRICHY: Landmarks ────────────────────────────────────────────────────
    "BHEL_Township": {"name": "BHEL Township", "tamil_name": "பெல் குடியிருப்பு", "category": "landmark", "city": "Trichy", "area": "BHEL", "tags": ["industrial", "township"]},
    "NIT_Trichy": {"name": "NIT Tiruchirappalli", "tamil_name": "என்ஐடி திருச்சி", "category": "landmark", "city": "Trichy", "area": "Thuvakudi", "tags": ["university", "campus", "engineering"]},
    "Trichy_Airport": {"name": "Trichy Airport", "tamil_name": "திருச்சி விமான நிலையம்", "category": "station", "sub_category": "airport", "city": "Trichy", "area": "Tiruchirapalli", "tags": ["airport", "domestic", "international"]},
    "Kallanai_Dam": {"name": "Kallanai (Grand Anicut)", "tamil_name": "கல்லணை", "category": "landmark", "city": "Trichy", "area": "Grand Anicut", "tags": ["dam", "historic", "ancient_engineering", "tourist"]},

    # ── Intercity ────────────────────────────────────────────────────────────
    "Villupuram": {"name": "Villupuram Junction", "tamil_name": "விழுப்புரம்", "category": "station", "sub_category": "main_rail", "city": "Villupuram", "area": "Town", "tags": ["junction", "intercity"]},
    "Coimbatore": {"name": "Coimbatore Junction", "tamil_name": "கோவை", "category": "station", "sub_category": "main_rail", "city": "Coimbatore", "area": "Town", "tags": ["junction", "intercity"]},
    "Madurai": {"name": "Madurai Junction", "tamil_name": "மதுரை", "category": "station", "sub_category": "main_rail", "city": "Madurai", "area": "Town", "tags": ["junction", "intercity", "meenakshi_temple"]},
    "Pondicherry": {"name": "Puducherry", "tamil_name": "புதுச்சேரி", "category": "station", "sub_category": "main_rail", "city": "Pondicherry", "area": "Town", "tags": ["union_territory", "beach", "french_quarter"]},
    "Vellore": {"name": "Vellore Katpadi Junction", "tamil_name": "வேலூர்", "category": "station", "sub_category": "main_rail", "city": "Vellore", "area": "Katpadi", "tags": ["junction", "fort", "cmc_hospital"]},
    "Kanchipuram": {"name": "Kanchipuram", "tamil_name": "காஞ்சிபுரம்", "category": "station", "sub_category": "main_rail", "city": "Kanchipuram", "area": "Town", "tags": ["temple_city", "silk"]},
}


# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY ICONS & COLORS
# ══════════════════════════════════════════════════════════════════════════════
CATEGORY_CONFIG: Dict[str, Dict[str, str]] = {
    "station": {"icon": "🚉", "color": "#F59E0B", "label": "Station"},
    "temple": {"icon": "🛕", "color": "#E879F9", "label": "Temple"},
    "mall": {"icon": "🏬", "color": "#06B6D4", "label": "Mall"},
    "hospital": {"icon": "🏥", "color": "#EF4444", "label": "Hospital"},
    "landmark": {"icon": "🏛️", "color": "#10B981", "label": "Landmark"},
}


def search_places(
    query: str = "",
    category: str = "",
    city: str = "",
    limit: int = 30,
) -> List[Dict[str, Any]]:
    """Search places by name, category, or city."""
    from data.database import COORDINATES

    results = []
    q = query.lower()

    for node_id, meta in PLACES.items():
        if node_id not in COORDINATES:
            continue

        # Category filter
        if category and meta.get("category") != category:
            continue
        # City filter
        if city and meta.get("city", "").lower() != city.lower():
            continue
        # Query filter
        if q:
            searchable = " ".join([
                meta.get("name", ""),
                meta.get("tamil_name", ""),
                meta.get("area", ""),
                " ".join(meta.get("tags", [])),
                node_id.replace("_", " "),
            ]).lower()
            if q not in searchable:
                continue

        lat, lng = COORDINATES[node_id]
        results.append({
            "node": node_id,
            "name": meta["name"],
            "tamil_name": meta.get("tamil_name", ""),
            "category": meta["category"],
            "city": meta.get("city", ""),
            "area": meta.get("area", ""),
            "lat": lat,
            "lng": lng,
            "tags": meta.get("tags", []),
            "timings": meta.get("timings", ""),
        })

    return results[:limit]


# ── DYNAMIC DATASET MERGE ─────────────────────────────────────────────────────
try:
    from data.dataset_loader import load_and_merge_data
    _, PLACES, _, _ = load_and_merge_data({}, PLACES, {}, [])
except Exception as e:
    print(f"[Warning] Failed to merge places dictionary: {e}")


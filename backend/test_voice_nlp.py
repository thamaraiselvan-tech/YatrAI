import sys
sys.path.insert(0, '.')
from agents.agents import parse_user_query

def run_checks():
    test_cases = [
        "from SRM Dorm to Chennai Central",
        "SRM to Srirangam",
        "from Broadway to Srirangam",
        "Koyambedu to Tambaram",
        "from Trichy CBS to Airport",
        "Chathiram to NIT Trichy",
        "from Anna Nagar to Srirangam",
    ]
    
    print("Testing Voice-NLP Parsing Engine:")
    print("=" * 60)
    
    passed = 0
    for q in test_cases:
        result = parse_user_query(q)
        start = result.get("start_node")
        target = result.get("target_node")
        mood = result.get("mood")
        
        # Check if resolved correctly
        if start and target:
            passed += 1
            print(f"✅ Query: '{q}'")
            print(f"   Resolved: {start} ➔ {target} [Mood: {mood}]")
        else:
            print(f"❌ Query: '{q}'")
            print(f"   Failed to resolve: {start} ➔ {target}")
            
    print("=" * 60)
    print(f"Summary: {passed}/{len(test_cases)} passed.")
    sys.exit(0 if passed == len(test_cases) else 1)

if __name__ == "__main__":
    run_checks()

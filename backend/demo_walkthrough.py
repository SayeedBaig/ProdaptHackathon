import sys
import httpx

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_API_URL = "http://127.0.0.1:8000/api/v1"
BASE_ROOT_URL = "http://127.0.0.1:8000"

def print_section(title):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)

def main():
    client = httpx.Client(base_url=BASE_API_URL, timeout=10.0)

    # 1. Health Check
    print_section("1. SYSTEM HEALTH CHECK")
    res = httpx.get(f"{BASE_ROOT_URL}/health")
    print(f"Status: {res.status_code}")
    print(f"System State: {res.json()}")

    # 2. Login
    print_section("2. AUTHENTICATION (JWT)")
    login_data = {"email": "demo@pitchpilot.ai", "password": "password123"}
    res = client.post("/auth/login", json=login_data)
    token = res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Logged in successfully as demo@pitchpilot.ai")
    print(f"✓ JWT Access Token: {token[:30]}...")

    # 3. Fetch Startup & Current Profile (V1)
    print_section("3. FETCH STARTUP & PROFILE VERSION 1")
    res = client.get("/startups", headers=headers)
    startups = res.json()["data"]["items"]
    startup_id = startups[0]["id"]
    print(f"Startup Name: {startups[0]['name']} (ID: {startup_id})")

    res = client.get(f"/startups/{startup_id}", headers=headers)
    startup_detail = res.json()["data"]
    print(f"Current Profile Version: v{startup_detail['profile_version']}")
    print(f"Raw Idea: {startup_detail['raw_idea']}")
    print(f"Journey Stepper: {[s['key'] + ':' + s['status'] for s in startup_detail['progress']['steps']]}")

    # 4. Idea Analysis
    print_section("4. IDEA ANALYSIS")
    res = client.post(f"/startups/{startup_id}/idea/analyze", headers=headers)
    idea_analysis = res.json()["data"]
    print(f"Problem: {idea_analysis['problem']}")
    print(f"Target Customer: {idea_analysis['target_customer']}")
    print("Pain points detected:")
    for p in idea_analysis["pain_points"]:
        print(f"  - {p}")
    print("Key Risks:")
    for r in idea_analysis["risks"]:
        print(f"  - {r}")
    q1 = idea_analysis["first_question"]
    print(f"\nFirst AI Question: \"{q1['text']}\" (Target: {q1['target_field']})")

    # 5. Founder Answers Clarification -> Profile Updates to V2!
    print_section("5. CLARIFICATION LOOP (FOUNDER ANSWERS -> PROFILE V2)")
    ans_payload = {
        "question_id": q1["id"],
        "answer": "We are specifically targeting students living in college hostels who have daily food budgets under Rs 80 per meal.",
        "base_version": startup_detail["profile_version"],
    }
    res = client.post(f"/startups/{startup_id}/clarify/answer", json=ans_payload, headers=headers)
    clarify_res = res.json()["data"]
    print(f"Profile Patch Applied: {clarify_res['profile_diff']}")
    print(f"NEW Profile Version: v{clarify_res['profile_version']} (Saved in PostgreSQL/SQLite version table!)")
    print(f"Completeness Score: {clarify_res['completeness_pct']}%")
    print(f"Next Generated Question: \"{clarify_res['next_question']['text']}\"")

    # 6. Generate Value Proposition & Market Analysis
    print_section("6. VALUE PROPOSITION & MARKET ANALYSIS")
    res = client.post(f"/startups/{startup_id}/analyses/value_proposition", headers=headers)
    vp = res.json()["data"]["output"]
    print(f"One-Liner: {vp['one_line']}")
    print(f"Elevator Pitch: {vp['elevator']}")
    print(f"Defensibility: {vp['competitive_advantage']}")

    res = client.post(f"/startups/{startup_id}/analyses/market", headers=headers)
    mkt = res.json()["data"]["output"]
    print(f"\nMarket Research Status: {mkt['research_status']}")
    print("Competitor Breakdown:")
    for c in mkt["competitors"]:
        print(f"  - {c['name']} (Provenance: {c['provenance']})")

    # 7. Generate Pitch Deck
    print_section("7. GENERATE PITCH DECK")
    res = client.post(f"/startups/{startup_id}/pitch/generate", json={}, headers=headers)
    pitch = res.json()["data"]
    print(f"Generated Pitch Deck Version {pitch['version']} (Built from Profile v{pitch['profile_version']})")
    print(f"Total Slides: {len(pitch['slides'])}")
    for s in pitch["slides"]:
        print(f"  Slide [{s['key'].upper()}]: '{s['title']}' - Status: {s['status']}")

    # 8. Investor Simulation Mode
    print_section("8. INVESTOR SIMULATOR (ADAPTIVE QUESTIONING)")
    res = client.post(f"/startups/{startup_id}/investor/sessions", json={"max_turns": 3}, headers=headers)
    session = res.json()["data"]
    session_id = session["id"]
    t1 = session["current_turn"]
    print(f"Investor Session Started (ID: {session_id})")
    print(f"Turn {t1['seq']} [{t1['topic'].upper()}] - Intent: {t1['intent']}")
    print(f"Investor Asks: \"{t1['question']}\"")

    # 9. Founder Answers Investor
    print_section("9. FOUNDER DEFENDS PITCH & RECEIVES SCORING")
    ans_data = {
        "turn_seq": 1,
        "answer": "We cluster deliveries to designated hostel campus gates at set times (1pm and 8pm), eliminating individual delivery drivers and saving 65% on logistics.",
    }
    res = client.post(f"/investor/sessions/{session_id}/answer", json=ans_data, headers=headers)
    ans_res = res.json()["data"]
    evaluation = ans_res["evaluation"]
    print("Investor Scoring Breakdown:")
    for crit, score in evaluation["scores"].items():
        bar = "█" * score + "░" * (10 - score)
        print(f"  - {crit.capitalize():20}: {bar} ({score}/10)")
    print(f"Evaluation: {evaluation['explanation']}")
    next_t = ans_res["next_turn"]
    print(f"\nAdaptive Next Turn ({next_t['intent']}): \"{next_t['question']}\"")

    # 10. Finish Session & Fetch Readiness Report
    print_section("10. READINESS REPORT & COACHING SCORE")
    client.post(f"/investor/sessions/{session_id}/finish", headers=headers)
    res = client.get(f"/startups/{startup_id}/readiness", headers=headers)
    report = res.json()["data"]
    print(f"Overall Pitch Readiness Score: {report['overall']}/100")
    print("Dimension Breakdown:")
    for dim, score in report["dimensions"].items():
        print(f"  - {dim.replace('_', ' ').title():25}: {score}/100")
    print(f"Executive Summary: {report['narrative']['summary']}")
    print(f"Top Gaps: {report['narrative']['top_gaps']}")
    print("Actionable Feedback Items:")
    for fb in report["feedback_items"]:
        print(f"  [{fb['status'].upper()}] {fb['title']}: {fb['recommendation']}")

    # 11. Closing the Loop: Resolve Feedback -> Profile V3!
    print_section("11. CLOSING THE LOOP (RESOLVE WITH FACTS -> PROFILE V3)")
    target_fb = report["feedback_items"][0]
    resolve_payload = {
        "action": "accept",
        "founder_input": "Conducted in-person survey with 50 hostel students at campus. 38 signed up for the weekly trial.",
    }
    res = client.post(f"/feedback/{target_fb['id']}/resolve", json=resolve_payload, headers=headers)
    res_data = res.json()["data"]
    print(f"Feedback Action: {res_data['status']}")
    print(f"Profile Bumped to: v{res_data['profile_version']}")
    print(f"Diff committed: {res_data['profile_diff']}")

    res = client.get(f"/startups/{startup_id}", headers=headers)
    updated_profile = res.json()["data"]["profile"]
    print(f"\nVerified Profile in Database -> traction.interviews: \"{updated_profile['traction']['interviews']}\"")

    print("\n" + "=" * 65)
    print("  SUCCESS! FULL COACHING WORKFLOW EXECUTED END-TO-END!")
    print("=" * 65)

if __name__ == "__main__":
    main()

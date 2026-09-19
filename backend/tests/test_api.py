import uuid
import pytest

def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "ai_mode" in data

def test_auth_register_and_login(client):
    # Register
    reg_payload = {"email": "newuser@example.com", "password": "mypassword123"}
    res = client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    reg_data = res.json()
    assert "data" in reg_data
    assert "access_token" in reg_data["data"]

    # Duplicate registration should return 409
    res_dup = client.post("/api/v1/auth/register", json=reg_payload)
    assert res_dup.status_code == 409
    assert res_dup.json()["error"]["code"] == "CONFLICT"

    # Login
    login_payload = {"email": "newuser@example.com", "password": "mypassword123"}
    res_log = client.post("/api/v1/auth/login", json=login_payload)
    assert res_log.status_code == 200
    assert "access_token" in res_log.json()["data"]

    # Invalid login should return 401
    bad_login = {"email": "newuser@example.com", "password": "wrongpassword"}
    res_bad = client.post("/api/v1/auth/login", json=bad_login)
    assert res_bad.status_code == 401
    assert res_bad.json()["error"]["code"] == "UNAUTHENTICATED"

def test_startup_creation_and_validation(client, auth_headers):
    # 1. Valid startup creation creates profile v1
    payload = {
        "name": "NutriNest",
        "raw_idea": "An app that helps college students find affordable healthy food",
    }
    res = client.post("/api/v1/startups", json=payload, headers=auth_headers)
    assert res.status_code == 201
    body = res.json()
    assert "data" in body
    startup = body["data"]
    assert startup["name"] == "NutriNest"
    assert startup["profile_version"] == 1
    assert startup["profile"]["identity"]["startup_name"] == "NutriNest"
    assert startup["progress"] is not None

    startup_id = startup["id"]

    # 2. Empty/whitespace idea returns 422
    invalid_payload = {"name": "NutriNest", "raw_idea": "   "}
    res_inv = client.post("/api/v1/startups", json=invalid_payload, headers=auth_headers)
    assert res_inv.status_code == 422
    assert res_inv.json()["error"]["code"] == "VALIDATION_ERROR"

    # 3. Retrieve startup
    res_get = client.get(f"/api/v1/startups/{startup_id}", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.json()["data"]["id"] == startup_id

def test_ownership_isolation(client, auth_headers, auth_headers_b):
    # User A creates a startup
    payload = {
        "name": "SecretStartup",
        "raw_idea": "Proprietary algorithm for supply chains",
    }
    res = client.post("/api/v1/startups", json=payload, headers=auth_headers)
    startup_id = res.json()["data"]["id"]

    # User B requests User A's startup -> MUST return 404 (not 403) to prevent leaking existence
    res_b = client.get(f"/api/v1/startups/{startup_id}", headers=auth_headers_b)
    assert res_b.status_code == 404
    assert res_b.json()["error"]["code"] == "NOT_FOUND"

def test_idea_analysis_and_clarification_loop(client, auth_headers):
    # Create startup
    payload = {
        "name": "NutriNest",
        "raw_idea": "An app that helps college students find affordable healthy food",
    }
    res_create = client.post("/api/v1/startups", json=payload, headers=auth_headers)
    startup_id = res_create.json()["data"]["id"]

    # 1. Analyze idea
    res_an = client.post(f"/api/v1/startups/{startup_id}/idea/analyze", headers=auth_headers)
    assert res_an.status_code == 200
    analysis_data = res_an.json()["data"]
    assert "problem" in analysis_data
    assert "first_question" in analysis_data
    question_id = analysis_data["first_question"]["id"]

    # 2. Answer clarification question -> updates to profile v2
    clarify_payload = {
        "question_id": question_id,
        "answer": "We are specifically targeting students living in hostels who cannot cook and find delivery apps too expensive.",
        "base_version": 1,
    }
    res_clarify = client.post(f"/api/v1/startups/{startup_id}/clarify/answer", json=clarify_payload, headers=auth_headers)
    assert res_clarify.status_code == 200
    clarify_body = res_clarify.json()["data"]
    assert clarify_body["profile_version"] == 2
    assert len(clarify_body["profile_diff"]) > 0
    assert clarify_body["next_question"] is not None

    # 3. Conflict check: Submitting with outdated base_version (1 instead of 2) -> 409
    stale_payload = {
        "question_id": question_id,
        "answer": "Another answer",
        "base_version": 1,
    }
    res_conflict = client.post(f"/api/v1/startups/{startup_id}/clarify/answer", json=stale_payload, headers=auth_headers)
    assert res_conflict.status_code == 409
    assert res_conflict.json()["error"]["code"] == "VERSION_CONFLICT"

def test_analyses_and_pitch_deck(client, auth_headers):
    # Create startup
    payload = {
        "name": "NutriNest",
        "raw_idea": "An app that helps college students find affordable healthy food",
    }
    startup_id = client.post("/api/v1/startups", json=payload, headers=auth_headers).json()["data"]["id"]

    # Value proposition
    res_vp = client.post(f"/api/v1/startups/{startup_id}/analyses/value_proposition", headers=auth_headers)
    assert res_vp.status_code == 200
    assert "one_line" in res_vp.json()["data"]["output"]

    # Market analysis
    res_mkt = client.post(f"/api/v1/startups/{startup_id}/analyses/market", headers=auth_headers)
    assert res_mkt.status_code == 200
    assert "research_status" in res_mkt.json()["data"]["output"]

    # Business model
    res_bm = client.post(f"/api/v1/startups/{startup_id}/analyses/business_model", headers=auth_headers)
    assert res_bm.status_code == 200
    assert "revenue_source" in res_bm.json()["data"]["output"]

    # Generate Pitch deck
    res_pitch = client.post(f"/api/v1/startups/{startup_id}/pitch/generate", json={}, headers=auth_headers)
    assert res_pitch.status_code == 200
    pitch_data = res_pitch.json()["data"]
    assert len(pitch_data["slides"]) >= 3
    pitch_id = pitch_data["id"]

    # Critique pitch deck
    res_crit = client.post(f"/api/v1/startups/{startup_id}/pitch/{pitch_id}/critique", headers=auth_headers)
    assert res_crit.status_code == 200
    assert "issues" in res_crit.json()["data"]["output"]

def test_investor_simulation_readiness_and_feedback_loop(client, auth_headers):
    # Create startup
    payload = {
        "name": "NutriNest",
        "raw_idea": "An app that helps college students find affordable healthy food",
    }
    startup_id = client.post("/api/v1/startups", json=payload, headers=auth_headers).json()["data"]["id"]

    # 1. Start investor session
    res_sess = client.post(
        f"/api/v1/startups/{startup_id}/investor/sessions",
        json={"max_turns": 3},
        headers=auth_headers,
    )
    assert res_sess.status_code == 201
    sess_data = res_sess.json()["data"]
    session_id = sess_data["id"]
    assert sess_data["status"] == "active"
    assert sess_data["current_turn"]["seq"] == 1

    # 2. Answer turn 1
    ans_payload = {
        "turn_seq": 1,
        "answer": "Because we aggregate local cloud kitchens specifically for batch delivery to campus gates, reducing logistics cost by 60%.",
    }
    res_ans = client.post(
        f"/api/v1/investor/sessions/{session_id}/answer",
        json=ans_payload,
        headers=auth_headers,
    )
    assert res_ans.status_code == 200
    ans_body = res_ans.json()["data"]
    assert ans_body["evaluation"] is not None
    assert "clarity" in ans_body["evaluation"]["scores"]
    assert ans_body["next_turn"]["seq"] == 2

    # 3. Double-answering the same turn returns 409
    res_dup = client.post(
        f"/api/v1/investor/sessions/{session_id}/answer",
        json=ans_payload,
        headers=auth_headers,
    )
    assert res_dup.status_code == 409
    assert res_dup.json()["error"]["code"] == "SESSION_CLOSED"

    # 4. Finish session early -> triggers readiness report
    res_fin = client.post(f"/api/v1/investor/sessions/{session_id}/finish", headers=auth_headers)
    assert res_fin.status_code == 200
    assert res_fin.json()["data"]["status"] == "completed"

    # 5. Fetch readiness report
    res_read = client.get(f"/api/v1/startups/{startup_id}/readiness", headers=auth_headers)
    assert res_read.status_code == 200
    readiness_data = res_read.json()["data"]
    assert readiness_data["overall"] is not None
    assert len(readiness_data["dimensions"]) > 0
    assert len(readiness_data["feedback_items"]) > 0

    # 6. Resolve feedback item with founder empirical facts -> closes the loop to Profile V2!
    feedback_id = readiness_data["feedback_items"][0]["id"]
    resolve_payload = {
        "action": "accept",
        "founder_input": "Conducted survey with 50 hostel students, 32 signed up for pilot subscription.",
    }
    res_resolve = client.post(f"/api/v1/feedback/{feedback_id}/resolve", json=resolve_payload, headers=auth_headers)
    assert res_resolve.status_code == 200
    res_body = res_resolve.json()["data"]
    assert res_body["status"] == "accepted"
    assert res_body["profile_version"] == 2
    assert len(res_body["profile_diff"]) > 0

    # 7. Check that startup profile is now updated to V2 with the founder facts
    startup_updated = client.get(f"/api/v1/startups/{startup_id}", headers=auth_headers).json()["data"]
    assert startup_updated["profile_version"] == 2
    assert "50 hostel students" in startup_updated["profile"]["traction"]["interviews"]

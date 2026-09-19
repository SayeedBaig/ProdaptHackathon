import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.common import StartupIdeaInput

client = TestClient(app)

SAMPLE_STARTUP = {
    "title": "PitchCoach AI",
    "raw_description": "AI startup coach that helps entrepreneurs refine business ideas, create pitch decks, define value props, and prepare for VC Q&A.",
    "target_industry": "B2B SaaS / Artificial Intelligence",
    "stage": "Idea Stage",
    "location": "Global"
}

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_idea_analysis_endpoint():
    res = client.post("/api/v1/idea-analysis", json={"startup_info": SAMPLE_STARTUP})
    assert res.status_code == 200
    payload = res.json()
    assert payload["success"] is True
    assert payload["data"]["novelty_score"] >= 0

def test_clarification_questions_endpoint():
    res = client.post("/api/v1/clarification-questions", json={"startup_info": SAMPLE_STARTUP})
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data["questions"]) > 0

def test_value_proposition_endpoint():
    res = client.post("/api/v1/value-proposition", json={"startup_info": SAMPLE_STARTUP})
    assert res.status_code == 200
    data = res.json()["data"]
    assert "headline" in data
    assert "geoff_moore_template" in data

def test_market_analysis_endpoint():
    res = client.post("/api/v1/market-analysis", json={"startup_info": SAMPLE_STARTUP})
    assert res.status_code == 200
    data = res.json()["data"]
    assert "market_metrics" in data
    assert len(data["competitor_matrix"]) > 0

def test_pitch_generation_endpoint():
    res = client.post("/api/v1/pitch-generation", json={"startup_info": SAMPLE_STARTUP})
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data["slides"]) >= 5
    assert "elevator_pitch_30s" in data["scripts"]

def test_pitch_critique_endpoint():
    res = client.post("/api/v1/pitch-critique", json={})
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["overall_score"] > 0

def test_investor_questions_endpoint():
    res = client.post("/api/v1/investor-questions", json={"startup_info": SAMPLE_STARTUP})
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data["questions"]) > 0

def test_answer_evaluation_endpoint():
    res = client.post("/api/v1/answer-evaluation", json={
        "question": "What is your projected CAC?",
        "user_answer": "We don't know CAC yet."
    })
    assert res.status_code == 200
    data = res.json()["data"]
    assert "improved_answer" in data

def test_readiness_report_endpoint():
    res = client.post("/api/v1/readiness-report", json={"startup_info": SAMPLE_STARTUP})
    assert res.status_code == 200
    data = res.json()["data"]
    assert "overall_readiness_score" in data
    assert "readiness_badge" in data

def test_full_pipeline_endpoint():
    res = client.post("/api/v1/full-pipeline", json={"startup_info": SAMPLE_STARTUP})
    assert res.status_code == 200
    data = res.json()["data"]
    assert "idea_analysis" in data
    assert "readiness_report" in data

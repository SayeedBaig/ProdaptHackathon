# AI Startup Pitch Coach — AI Engine Service

**Member 2 — AI / LLM Engineer**  
**Branch:** `feature/ai-engine`  
**Problem Statement:** Group 6 — AI Startup Pitch Coach (Prodapt Hackathon)

---

## Overview

The **AI Startup Pitch Coach Engine** is a high-performance, structured Python AI microservice designed to transform raw business concepts into investor-ready pitch packages.

It provides **9 core AI modules** using structured Pydantic models, FastAPI endpoints, dual-mode LLM support (Gemini 2.5 Flash / OpenAI GPT-4o + built-in offline Mock LLM fallback), and pre-generated JSON contracts for zero-dependency team integration.

---

## 🚀 9 Core AI Modules

| # | Module | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | **Idea Analysis** | `POST /api/v1/idea-analysis` | Problem/solution breakdown, target audience, novelty score (0-100), strengths, weaknesses, and risk factors. |
| 2 | **Clarification Questions** | `POST /api/v1/clarification-questions` | Targeted follow-up questions categorized by domain (Monetization, Traction, Defensibility). |
| 3 | **Value Proposition** | `POST /api/v1/value-proposition` | Geoff Moore positioning template, 30s elevator pitch, USPs, and customer pain-relief matrix. |
| 4 | **Market Analysis** | `POST /api/v1/market-analysis` | TAM/SAM/SOM metrics, competitor matrix, market trends, entry barriers, and growth drivers. |
| 5 | **Pitch Generation** | `POST /api/v1/pitch-generation` | 5-slide deck structure with speaker notes & visuals + 30s, 2min, and 5min timed pitch scripts. |
| 6 | **Pitch Critique** | `POST /api/v1/pitch-critique` | Deck persuasion & clarity score (0-100), slide breakdowns, weak points, and actionable fixes. |
| 7 | **Investor Questions** | `POST /api/v1/investor-questions` | Simulated VC Q&A bank categorized by risk domain (Financial, Technical, Market) with difficulty ratings. |
| 8 | **Answer Evaluation** | `POST /api/v1/answer-evaluation` | Grades founder answers on clarity, persuasion & completeness + provides benchmark response. |
| 9 | **Readiness Report** | `POST /api/v1/readiness-report` | Composite Investment Readiness Score (0-100), readiness badge, radar dimensions, red flags, and next steps. |
| 🌟 | **Full Pipeline** | `POST /api/v1/full-pipeline` | Single endpoint executing all 9 modules sequentially for complete end-to-end coaching. |

---

## 📁 Directory Structure

```text
ai-engine/
├── app/
│   ├── main.py                     # FastAPI application entry & CORS configuration
│   ├── routers/
│   │   └── pitch_coach_router.py   # REST API endpoints for all 9 modules + full pipeline
│   ├── schemas/                    # Pydantic input/output contracts
│   │   ├── common.py
│   │   ├── idea_analysis.py
│   │   ├── clarification_questions.py
│   │   ├── value_prop.py
│   │   ├── market_analysis.py
│   │   ├── pitch_deck.py
│   │   ├── pitch_critique.py
│   │   ├── investor_questions.py
│   │   ├── answer_evaluation.py
│   │   ├── readiness_report.py
│   │   └── full_pipeline.py
│   └── services/
│       ├── llm_client.py           # Multi-provider LLM client (Gemini / OpenAI / Mock)
│       └── pitch_coach_service.py # Core business logic & prompt templates
├── contracts/                      # Sample JSON responses for instant frontend/backend mock integration
│   ├── idea_analysis_sample.json
│   ├── clarification_questions_sample.json
│   ├── value_proposition_sample.json
│   ├── market_analysis_sample.json
│   ├── pitch_generation_sample.json
│   ├── pitch_critique_sample.json
│   ├── investor_questions_sample.json
│   ├── answer_evaluation_sample.json
│   ├── readiness_report_sample.json
│   └── full_pipeline_sample.json
├── tests/
│   └── test_ai_engine.py           # Pytest test suite covering all 9 module endpoints
├── .env.example
├── generate_contracts.py           # Script to regenerate contract JSON samples
├── requirements.txt
└── README.md
```

---

## 🛠️ Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup (Optional for Live LLM)
Copy `.env.example` to `.env`:
```bash
# Optional: Provide API Key for live synthesis (otherwise built-in Mock provider is used automatically)
GEMINI_API_KEY=your_gemini_api_key_here
# or
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run FastAPI Web Server
```bash
python app/main.py
# or
uvicorn app.main:app --reload --port 8000
```
Open Interactive OpenAPI / Swagger Documentation at: **http://127.0.0.1:8000/docs**

---

## 🧪 Running Tests

Run the automated test suite to verify schema validations and endpoint execution:
```bash
python -m pytest tests/test_ai_engine.py
```

---

## 📄 Contracts for Frontend & Backend Teammates

All contract samples are pre-exported in the `contracts/` directory. Teammates can inspect or mock their frontend/backend APIs using:
- `contracts/idea_analysis_sample.json`
- `contracts/market_analysis_sample.json`
- `contracts/pitch_generation_sample.json`
- `contracts/readiness_report_sample.json`
- `contracts/full_pipeline_sample.json`

To re-generate updated contract files:
```bash
python generate_contracts.py
```

# 3. Shared conventions (everyone follows these)

### 3.1 Single source of truth for contracts
- Pydantic schemas in `backend/app/ai/schemas/` and `backend/app/schemas/` are the truth.
- JSON fixtures in `backend/app/ai/fixtures/*.json` are one example per schema. Backend mock AI and frontend mocks both use them.
- After M1 announces **"contracts frozen" at minute 15**, any contract change goes through M1: post in team chat + add a line to `CONTRACTS_CHANGELOG.md`. No silent renames.

### 3.2 Naming and format

| Thing | Rule |
|---|---|
| JSON keys | `snake_case` everywhere, including frontend types (no camelCase conversion) |
| IDs | UUID strings |
| Timestamps | ISO-8601 UTC strings |
| Nulls | Missing data is `null`, never `""`, `"N/A"` or invented values. UI renders null as "Not provided — requires validation" |
| Provenance enum | `source_backed \| founder_assumption \| calculated \| ai_analysis` |
| Topic enum | `problem \| market \| differentiation \| business_model \| validation` |
| Criteria keys | `clarity, specificity, evidence, business_reasoning, differentiation, scalability` (ints 0–10) |
| Slide keys | `problem, solution, product, target_market, market_opportunity, competition, advantage, business_model, gtm, traction, team, ask` |
| Gap status | `open \| resolved` |
| Feedback status | `open \| accepted \| dismissed \| done` |
| Session status | `active \| completed \| abandoned` |
| Turn intent | `opening \| follow_up \| new_topic` |
| AI capability names | `analyze_idea, generate_clarification_question, extract_profile_patch, generate_value_proposition, analyze_competitors, analyze_market, analyze_business_model, generate_pitch, critique_pitch, generate_investor_question, evaluate_answer, generate_readiness_narrative, extract_feedback_patches` |
| Provenance icons | 🟢 source_backed · 🟡 founder_assumption · 🔵 ai_analysis · 🔢 calculated |

### 3.3 Envelopes (M3 implements once, everyone relies on it)

Success (AI endpoints):
```json
{"data": {}, "meta": {"ai_mode": "live|fallback_provider|mock", "model": "gemini-2.0-flash",
                      "degraded": false, "warnings": [], "profile_version": 3}}
```
Error (all endpoints):
```json
{"error": {"code": "LLM_INVALID_OUTPUT", "message": "Friendly text", "details": {}, "request_id": "..."}}
```
Codes: `VALIDATION_ERROR 422`, `UNAUTHENTICATED 401`, `NOT_FOUND 404`, `VERSION_CONFLICT 409`, `SESSION_CLOSED 409`, `RATE_LIMITED 429`, `LLM_INVALID_OUTPUT 502`, `LLM_UNAVAILABLE 503`.

### 3.4 Environment variables (identical names everywhere)
Backend: `DATABASE_URL, JWT_SECRET, JWT_EXPIRE_MINUTES, AI_MODE (live|mock|scripted-demo), LLM_PRIMARY (gemini|openai), GEMINI_API_KEY, OPENAI_API_KEY, SEARCH_MODE (live|cached|off), TAVILY_API_KEY, CORS_ORIGIN`.
Frontend: `VITE_API_URL, VITE_USE_MOCKS`.
Everyone commits `.env.example`, never `.env`.

### 3.5 Layering rule
`routes → services → repositories → DB`, and `services → ai_service / research`.
- Routes contain no business logic. Repositories contain no business logic.
- Nothing outside `ai/providers/` imports an LLM vendor SDK.
- Nothing outside `research/` imports Tavily/SerpAPI.
- LLM calls happen **outside** DB transactions (persist → call LLM → persist result).

### 3.6 Mock-first rule
Every piece must run without the pieces it depends on. If you are blocked, build against a fixture or a fake.

# PitchPilot AI — Master Architecture & Team Execution Guide

> AI startup pitch coach. **Not** a pitch generator: it challenges the founder, finds gaps, asks questions, improves the idea, simulates investors, and closes the loop.
> This document is the single source of truth for all 5 team members. Read Sections 1–3 fully, then your own brief in Section 20.

---

## Table of Contents

1. Product summary and scope
2. Ambiguities found in the spec and the decisions taken
3. Shared conventions (everyone follows these)
4. High-level architecture (A)
5. Module architecture (B)
6. Startup Profile design (C)
7. Database design (D)
8. API design (E)
9. AI / LLM architecture (F)
10. Investor simulator architecture (G)
11. Market research architecture (H)
12. Frontend architecture (I)
13. Security architecture (J)
14. Testing strategy (K)
15. Performance and scalability (L)
16. 3-hour implementation plan (M)
17. Project structure (N)
18. Architectural decisions (O)
19. Judge-facing explanation (P)
20. **Per-person work briefs (M1–M5)**
21. Handshake matrix (who depends on whom)
22. Integration checklists
23. Git workflow
24. Demo script

---

## 1. Product summary and scope

**Flow:** Raw idea → Understand → Question → Refine → Analyze → Generate → Critique → Practice → Evaluate → Improve.

**Central concept:** the **Startup Profile** is the shared, versioned state. Every AI module reads it and (through validated patches) updates it. There are no independent chatbots.

**Human in the loop:** the AI suggests, analyzes, challenges, critiques. The founder answers, supplies facts, confirms edits and makes business decisions. The AI never claims a startup will succeed.

**Modules (in journey order):** Idea Analyzer + Refiner → Value Proposition → Market + Competitor Analysis → Business Model → Pitch Deck → Pitch Critique → Investor Simulator → Answer Evaluation → Readiness Report → Feedback → Updated Profile (V2) → Improved Pitch.

**Hard constraints (do not violate):** no microservices, Kubernetes, Redis, event buses, LangGraph, complex RAG, real-time collaboration, full financial modelling, PPTX as a core dependency, or voice as a core feature. External search must never be a hard dependency. The LLM must never invent TAM/SAM/SOM, market size, revenue, customer counts, statistics or competitor facts.

**Scope triage for 3 hours**
- **Must:** idea analysis + clarification loop, profile versions, value prop, market with evidence, pitch, critique, investor loop, readiness, feedback → V2 pitch.
- **Should:** business model page, auth, stale badges.
- **Cut unless time remains:** PPTX, SerpAPI (Tavily only), email verification, session-history pagination UI.

---

## 2. Ambiguities found in the spec and the decisions taken

The spec is strong but had 12 gaps. Each is resolved here so nobody blocks in the first 15 minutes. **With these decisions the architecture is final.**

| # | Ambiguity | Decision |
|---|---|---|
| 1 | "Profile updates from feedback" vs "founder confirms everything" | **Founder-stated facts** (clarification answers, edits) update the profile directly, with a visible diff and undo. **AI-generated content never becomes a fact automatically.** The AI may add *gaps/risks* (labelled AI-sourced) and *suggested* facts; the founder accepts or rejects suggestions. |
| 2 | Provenance (🟢🟡🔵 + calculated) has no defined home | A `provenance` map on the profile (JSON path → `founder \| source_backed \| calculated \| ai_analysis`). A null value renders as "Not provided / Requires validation". |
| 3 | Profile "versioning" vs "current state" | Append-only `profile_versions` rows + `current_version_id` pointer. Every generated artifact records the profile version it was built from. Version mismatch = **stale** (UI: "Out of date — regenerate"). |
| 4 | `ai_service` list omits refinement, competitors, business model | Added `extract_profile_patch`, `analyze_competitors`, `analyze_business_model`, `extract_feedback_patches`. 13 capabilities total. |
| 5 | Answer criteria (6) don't match report dimensions (5) | Each investor question is tagged with a **topic** (the 5 report dimensions). Each answer is scored on the 6 criteria. Dimension scores are **computed in code** from the criterion scores of that topic's turns. |
| 6 | Who computes the overall readiness score? | Code, not the LLM. Deterministic, testable, defensible. The LLM writes only the narrative and may not change numbers. |
| 7 | "Adaptive follow-up" vs predictable demo | A small deterministic **controller in code** picks the *intent* (follow up on the weakness vs new topic). The LLM writes the question text. |
| 8 | Business model: generate or elicit? | Extract from the profile, list **missing assumptions**, ask the founder. Pricing/cost stay null until the founder provides them. |
| 9 | "Calculated estimate" vs "never invent numbers" | Calculated only from **founder-supplied inputs**, computed in Python with the formula shown. Otherwise "Requires validation". |
| 10 | Ownership overlap (M1/M2 on AI, M2/M5 on investor prompts) | **M1** owns the `AIService` interface, provider chain, validation, fallback. **M2** owns all prompts + output schemas. **M5** owns simulator orchestration (controller, scoring, report assembly) and calls `ai_service`. |
| 11 | Async | No job queue. Synchronous HTTP with loading states; parallel calls via `asyncio.gather`. |
| 12 | Mock/fallback output must not pass as real analysis | Every AI response carries `meta.ai_mode = live \| fallback_provider \| mock`; the UI shows a badge when not `live`. |

---

## 3. Shared conventions (everyone follows these)

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

---

## 4. High-level architecture (A)

```
┌──────────────────────── React + TS + Vite + Tailwind ────────────────────────┐
│ Pages → Feature components → React Query hooks → api/ (axios)  [mocks toggle]│
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │ HTTPS JSON, JWT Bearer
┌───────────────────────────────▼──────────────────────────────────────────────┐
│ FastAPI (single stateless monolith)                                          │
│  routes/ ─► services/ (workflow orchestration, own the transaction)          │
│               │            │                 │                               │
│               │            │                 └─► research/ (SearchProvider)  │
│               │            ▼                       Tavily → cache → off      │
│               │      ai/ AIService                                           │
│               │       ├ prompts/ (1 file per capability)                     │
│               │       ├ schemas/ (Pydantic outputs)                          │
│               │       ├ context.py (profile projection per capability)       │
│               │       └ providers/ Gemini → OpenAI → Mock (chain)            │
│               ▼                                                              │
│         repositories/ ─► SQLAlchemy ─► PostgreSQL (JSONB + relational)       │
└──────────────────────────────────────────────────────────────────────────────┘
External (all optional-with-fallback): Gemini/OpenAI APIs, Tavily API
```

**Request flow — clarification answer**
1. Route validates input + JWT, checks ownership.
2. `IdeaService` loads the current profile.
3. `ai.extract_profile_patch(profile, question, answer)` → Pydantic-validated.
4. `ProfileService.apply_patch()` writes a new `profile_versions` row.
5. `ai.generate_clarification_question(profile_new)`.
6. Response: `{profile_diff, next_question, meta}`.

---

## 5. Module architecture (B)

**Frontend:** `pages/` (one per journey step), `features/` (profile, clarification, market, pitch, investor, readiness, feedback), `components/` (Card, Stepper, ProvenanceBadge, ScoreBar, DegradedBanner, Skeleton), `api/`, `hooks/`, `mocks/`, `types/`.

**Backend**
- `api/routes` — thin HTTP layer.
- `services` — `ProfileService` (patch/version logic), `IdeaService`, `AnalysisService` (value prop, market, business model), `PitchService`, `InvestorService` (M5), `ReadinessService` (M5), `FeedbackService`.
- `ai` — `AIService` facade with 13 capabilities, runner, context projection, prompts, schemas, providers.
- `research` — search providers, query builder, evidence normalizer, claim verifier.
- `repositories` — DB access only.
- `core` — config, security, errors, logging, deps, rate limiting.

**Integration layer:** `LLMClient.complete_json()` and `SearchProvider.search()` are the only two places that touch external vendors.

---

## 6. Startup Profile design (C)

**Relational columns** (things you filter/join on): `startup_id`, `version`, `created_at`, `change_reason`, `patch`, `completeness_pct`.
**JSONB** (`profile_versions.data`): the whole profile document.

```json
{
  "schema_version": 1,
  "identity": {"startup_name": "", "raw_idea": "", "one_liner": null},
  "problem": {"statement": null, "pain_points": []},
  "customer": {"primary_segment": null, "persona": null, "segments": []},
  "solution": {"description": null, "key_features": []},
  "value_proposition": {"one_line": null, "elevator": null, "differentiation": null, "advantage": null},
  "market": {"summary": null, "size_inputs": {"customers": null, "price": null, "frequency": null}},
  "competitor_summary": [{"name": "", "competitor_id": null}],
  "business_model": {"type": null, "customer": null, "payer": null, "revenue_source": null,
                     "pricing": null, "costs": null, "go_to_market": null},
  "traction": {"interviews": null, "interested": null, "users": null, "revenue": null,
               "partnerships": null, "notes": null},
  "team": null,
  "funding_ask": null,
  "assumptions": [{"id": "a1", "text": "", "status": "unvalidated|validated|invalidated", "source": "founder|ai"}],
  "risks":       [{"id": "r1", "text": "", "severity": "low|med|high", "source": "founder|ai"}],
  "gaps":        [{"id": "g1", "topic": "problem|market|differentiation|business_model|validation",
                   "text": "", "severity": 1, "status": "open|resolved",
                   "raised_by": "idea_analysis|critique|investor"}],
  "provenance": {"customer.primary_segment": "founder", "traction.interviews": "founder"}
}
```

Full competitor and evidence data lives in **tables**; the profile keeps only references (no duplication).

**Completeness:** % of required fields filled (`problem.statement`, `customer.primary_segment`, `solution.description`, at least one of competitor or differentiation). `ready_for_next_step` = required fields filled. The founder can also proceed early.

**How updates work**
- Every change is a `ProfilePatch`: `[{op: "set|add|remove", path: "customer.primary_segment", value: "...", source: "founder", reason: "..."}]`.
- `apply_patch()` deep-copies the current data, applies ops, **rejects unknown paths** (whitelist derived from the Pydantic `Profile` model), writes a new version row with the patch (for the diff UI), and moves `current_version_id`.
- Requests that modify the profile send `base_version`; a mismatch returns `409 VERSION_CONFLICT`.
- `change_reason` values: `clarification`, `founder_edit`, `investor_feedback`, `feedback_action`, `system`.

---

## 7. Database design (D)

```sql
users(id uuid PK, email text UNIQUE NOT NULL, password_hash text NOT NULL, created_at timestamptz)

startups(id uuid PK, user_id uuid FK→users, name text NOT NULL, raw_idea text NOT NULL,
         current_version_id uuid NULL,              -- FK→profile_versions (added after create)
         status text DEFAULT 'active', created_at, updated_at)
  INDEX (user_id, created_at DESC)

profile_versions(id uuid PK, startup_id uuid FK, version int NOT NULL,
         data jsonb NOT NULL, patch jsonb NULL, change_reason text NOT NULL,
         completeness_pct int, created_at,
         UNIQUE(startup_id, version))

clarification_turns(id uuid PK, startup_id FK, seq int, question text, target_field text,
         answer text NULL, profile_version_before int, profile_version_after int NULL,
         created_at, answered_at, UNIQUE(startup_id, seq))

analyses(id uuid PK, startup_id FK,
         kind text CHECK IN ('idea','value_proposition','market','business_model'),
         profile_version int NOT NULL, output jsonb NOT NULL,
         ai_mode text, model text, created_at)
  INDEX (startup_id, kind, created_at DESC)

evidence_sources(id uuid PK, startup_id FK, analysis_id FK NULL, query text,
         url text, title text, snippet text, provider text, retrieved_at timestamptz,
         kind text CHECK IN ('search_result','founder_provided'))
  INDEX (startup_id), INDEX (analysis_id)

competitors(id uuid PK, startup_id FK, name text, description text, differentiation text,
         strengths jsonb, weaknesses jsonb, evidence_ids uuid[], provenance text, created_at)
  INDEX (startup_id)

pitch_versions(id uuid PK, startup_id FK, version int, profile_version int, slides jsonb NOT NULL,
         parent_pitch_id uuid NULL, ai_mode text, created_at, UNIQUE(startup_id, version))

pitch_critiques(id uuid PK, pitch_version_id FK, output jsonb NOT NULL, created_at)

investor_sessions(id uuid PK, startup_id FK, pitch_version_id FK,
         status text CHECK IN ('active','completed','abandoned'),
         max_turns int DEFAULT 5, started_at, completed_at)
  INDEX (startup_id, started_at DESC)

investor_turns(id uuid PK, session_id FK, seq int, topic text,
         intent text CHECK IN ('opening','follow_up','new_topic'),
         question text NOT NULL, answer text NULL,
         evaluation jsonb NULL,          -- full AnswerEvaluation
         scores jsonb NULL,              -- {clarity:..,specificity:..,...} for cheap aggregation
         created_at, answered_at, UNIQUE(session_id, seq))

readiness_reports(id uuid PK, startup_id FK, session_id FK, profile_version int,
         overall int, dimension_scores jsonb, narrative jsonb, created_at)
  INDEX (startup_id, created_at DESC)

feedback_items(id uuid PK, startup_id FK, report_id FK NULL, topic text, title text,
         recommendation text, suggested_patch jsonb NULL,
         status text CHECK IN ('open','accepted','dismissed','done'), created_at, resolved_at)
  INDEX (startup_id, status)

llm_calls(id uuid PK, startup_id uuid NULL, capability text, provider text, model text,
         latency_ms int, prompt_tokens int, completion_tokens int, outcome text, created_at)
         -- metadata only, never prompt/answer content
```

**JSONB vs relational**
- **Relational:** anything joined, filtered, sorted or paginated on (ownership, versions, sessions, turns, evidence, competitors).
- **JSONB:** the profile document and LLM outputs (shape evolves during the hackathon; Pydantic validates them).
- **Versioning:** profile and pitch are append-only with integer `version`. Analyses store the `profile_version` they were built from, so staleness is one integer comparison.
- **Test portability:** use `JSONB().with_variant(JSON(), "sqlite")` so tests can run on SQLite.

**ER (short):** `users 1─* startups 1─* profile_versions`; `startups 1─* analyses / evidence_sources / competitors / pitch_versions / investor_sessions / readiness_reports / feedback_items / clarification_turns`; `pitch_versions 1─* pitch_critiques`; `investor_sessions 1─* investor_turns`.

---

## 8. API design (E)

Base path: `/api/v1`. All endpoints require `Authorization: Bearer <jwt>` except register, login, health. Other users' resources return **404** (not 403) so existence is not leaked.

| Method | Route | Purpose | Extra errors |
|---|---|---|---|
| POST | `/auth/register` | `{email,password}` → `{access_token}` | 409 email exists |
| POST | `/auth/login` | same | 401 bad credentials |
| GET | `/auth/me` | current user | |
| POST | `/startups` | create + seed profile v1 | 422 empty idea |
| GET | `/startups` | list, paginated (`?page=&page_size=`) | |
| GET | `/startups/{id}` | startup + current profile + `progress` steps | |
| PATCH | `/startups/{id}/profile` | founder edits: `{base_version, ops[]}` | 409 conflict |
| GET | `/startups/{id}/profile/versions` | history + patches | |
| POST | `/startups/{id}/idea/analyze` | idea analysis, gaps, first question | 502/503 |
| POST | `/startups/{id}/clarify/answer` | `{question_id, answer, base_version}` → patch + next question | 409 |
| POST | `/startups/{id}/clarify/skip` | skip question, get next | |
| POST | `/startups/{id}/analyses/{kind}` | generate `value_proposition \| market \| business_model` | 409 profile too thin |
| GET | `/startups/{id}/analyses/{kind}/latest` | latest + `stale` flag | 404 none |
| POST | `/startups/{id}/pitch/generate` | pitch from current profile (`{improve_from_pitch_id?}`) | |
| GET | `/startups/{id}/pitch?version=` | latest or specific + version list | |
| POST | `/startups/{id}/pitch/{pitch_id}/critique` | critique a pitch version | |
| POST | `/startups/{id}/investor/sessions` | start session → first question | |
| POST | `/investor/sessions/{sid}/answer` | evaluate + next question or `completed:true` | 409 SESSION_CLOSED / already answered |
| POST | `/investor/sessions/{sid}/finish` | end early and build report | |
| GET | `/investor/sessions/{sid}` | full session with turns | |
| GET | `/startups/{id}/investor/sessions` | history, paginated | |
| GET | `/startups/{id}/readiness` | latest report + open feedback | 404 none yet |
| POST | `/feedback/{fid}/resolve` | `{action:"accept\|dismiss", founder_input?}` → profile patch | |
| GET | `/health` | liveness + `ai_mode`, `search_mode` | |

### Key request/response examples

**POST `/startups`**
```json
{"name":"NutriNest","raw_idea":"An app that helps college students find affordable healthy food"}
→ {"id":"…","name":"NutriNest","profile_version":1}
```

**POST `/startups/{id}/idea/analyze`** → `data`
```json
{"problem":"College students struggle to find healthy affordable food",
 "target_customer":"College students","solution":"Food discovery app",
 "pain_points":["…"],"assumptions":["Students would switch from Swiggy/Zomato"],
 "risks":["Incumbents can add filters"],
 "missing_information":["Which students?","Definition of healthy","Evidence of demand"],
 "first_question":{"id":"q1","text":"Which students are you targeting?","target_field":"customer.primary_segment"}}
```

**POST `/startups/{id}/clarify/answer`**
```json
{"question_id":"q1","answer":"Students living in hostels","base_version":1}
→ {"profile_diff":[{"op":"set","path":"customer.primary_segment","value":"Hostel-dwelling college students"}],
   "profile_version":2,
   "next_question":{"id":"q2","text":"What is their biggest problem?","target_field":"problem.statement"},
   "ready_for_next_step":false,"completeness_pct":35}
```

**POST `/startups/{id}/analyses/market`** → `data`
```json
{"research_status":"ok|partial|unavailable",
 "segments":[{"name":"Hostel students","provenance":"founder_assumption"}],
 "competitors":[{"id":"…","name":"Swiggy","difference":"…","provenance":"source_backed","evidence_ids":["e1"]}],
 "opportunities":[{"text":"…","provenance":"ai_analysis"}],
 "threats":[{"text":"…","provenance":"ai_analysis"}],
 "market_size":{"tam":null,"sam":null,"som":null,"status":"Requires validation","calculation":null},
 "evidence":[{"id":"e1","title":"…","url":"…","snippet":"…"}]}
```

**POST `/startups/{id}/pitch/generate`** → `data`
```json
{"pitch_id":"…","version":1,"profile_version":4,
 "slides":[{"key":"problem","title":"Problem","bullets":["…"],"status":"complete"},
           {"key":"traction","title":"Traction","bullets":["Not provided — requires validation"],"status":"needs_input"}]}
```

**POST `/startups/{id}/pitch/{pitch_id}/critique`** → `data`
```json
{"issues":[{"topic":"differentiation","severity":"high","text":"Existing platforms can add similar filters",
            "recommendation":"Show a capability they cannot easily copy"}],
 "investor_objections":["Why won't Swiggy add a healthy filter?"],
 "top_priorities":["Validate demand","Clarify differentiation"]}
```

**POST `/startups/{id}/investor/sessions`** (`{pitch_version_id, max_turns:5}`)
```json
{"session_id":"…","turn":{"seq":1,"topic":"differentiation","intent":"opening",
  "question":"Why would students use your platform instead of Swiggy or Zomato?"}}
```

**POST `/investor/sessions/{sid}/answer`**
```json
{"turn_seq":1,"answer":"Because we focus specifically on healthy food."}
→ {"evaluation":{"scores":{"clarity":8,"specificity":5,"evidence":3,"business_reasoning":6,"differentiation":4,"scalability":5},
    "explanation":"…","strengths":["…"],"weaknesses":["No evidence students would switch"],
    "recommended_improvement":"…"},
   "next_turn":{"seq":2,"topic":"validation","intent":"follow_up","question":"Do you have any evidence that…"},
   "completed":false}
```

**GET `/startups/{id}/readiness`**
```json
{"overall":72,
 "dimensions":{"problem_clarity":85,"market_understanding":64,"differentiation":58,"business_model":null,"customer_validation":40},
 "narrative":{"summary":"…","why":{"customer_validation":"Willingness to pay is unsupported."},
              "top_gaps":["…"],"disclaimer":"Coaching metrics, not a prediction of success."},
 "feedback_items":[{"id":"…","title":"Validate willingness to pay",
    "recommendation":"Interview 20–30 target students and test pricing.","status":"open"}]}
```
A `null` dimension means "Not assessed" and is excluded from the overall.

**POST `/feedback/{fid}/resolve`**
```json
{"action":"accept","founder_input":"Interviewed 50 students, 32 interested"}
→ {"profile_version":7,"profile_diff":[{"op":"set","path":"traction.interviews","value":50},
                                       {"op":"set","path":"traction.interested","value":32}]}
```

**`progress` object on `GET /startups/{id}`**
```json
{"steps":[{"key":"idea","status":"done"},{"key":"clarify","status":"done"},
          {"key":"value_prop","status":"stale"},{"key":"market","status":"available"},
          {"key":"business_model","status":"locked"}, "..."]}
```
Statuses: `locked | available | done | stale`.

---

## 9. AI / LLM architecture (F)

### 9.1 Interface (M1 owns, M2 fills)
```python
class AIService(Protocol):
    async def analyze_idea(self, ctx) -> IdeaAnalysis
    async def generate_clarification_question(self, ctx) -> ClarificationQuestion
    async def extract_profile_patch(self, ctx, question, answer) -> ProfilePatch
    async def generate_value_proposition(self, ctx) -> ValueProposition
    async def analyze_competitors(self, ctx, evidence) -> CompetitorAnalysis
    async def analyze_market(self, ctx, evidence) -> MarketAnalysis
    async def analyze_business_model(self, ctx) -> BusinessModelAnalysis
    async def generate_pitch(self, ctx, prior_critique=None) -> Pitch
    async def critique_pitch(self, ctx, pitch) -> PitchCritique
    async def generate_investor_question(self, ctx, intent, topic, prev_turn=None) -> InvestorQuestion
    async def evaluate_answer(self, ctx, turn) -> AnswerEvaluation
    async def generate_readiness_narrative(self, ctx, turns, computed_scores) -> ReadinessNarrative
    async def extract_feedback_patches(self, ctx, report) -> list[FeedbackItemDraft]
```
The rest of the app only calls `get_ai_service()` and never knows which provider is behind it.

### 9.2 Core runner (used by every capability)
```python
async def run(capability, ctx, schema: type[BaseModel]):
    prompt = render(capability, ctx)                       # template + projected profile
    for provider in chain(settings.AI_MODE):               # gemini → openai → mock
        for attempt in range(2):                           # 1 repair retry
            raw = await provider.complete_json(prompt, timeout=25)
            try:
                return schema.model_validate(extract_json(raw))   # strips ``` fences
            except ValidationError as e:
                prompt = prompt.with_repair(e)             # "Your JSON failed: … return only valid JSON"
    raise LLMInvalidOutput   # mapped to 502; never a stack trace
```
The chain ends at the **mock provider** (loads `fixtures/{capability}.json`); that response gets `meta.ai_mode="mock"` and `degraded=true`.

### 9.3 Prompt separation
`ai/prompts/<capability>.py`, each exporting `CAPABILITY`, `TEMPERATURE`, `SYSTEM`, `USER_TEMPLATE`, `Output`. All system prompts import a shared `COMMON_RULES` preamble: never invent statistics/customers/revenue/partnerships; unknown → `null`; founder is the decision maker; no success predictions; return only JSON matching the schema. Use JSON mode where the provider supports it (`response_mime_type=application/json` for Gemini, `response_format=json_schema` for OpenAI) **plus** Pydantic validation regardless.

### 9.4 Context management
`context.py` builds a **projection per capability**; no prompt receives the whole profile.

| Capability | Profile fields sent |
|---|---|
| analyze_idea | identity, any provided optional fields |
| generate_clarification_question | profile + open gaps + previous questions (don't repeat) |
| extract_profile_patch | profile + the question + founder's answer + allowed paths list |
| value_proposition | problem, customer, solution, competitor_summary, pain_points, traction |
| analyze_market / competitors | customer, problem, solution, market.size_inputs, numbered evidence snippets |
| analyze_business_model | customer, solution, business_model, traction |
| generate_pitch | everything except `gaps`, plus market/competitor outputs and (for V2) prior critique |
| critique_pitch | pitch slides + profile |
| investor question / evaluate | profile + open gaps + topic + last 2 turns (question, answer, scores) |
| readiness narrative | gap list, computed scores, one-line weaknesses per turn |

Founder text is wrapped in `<founder_input>…</founder_input>` and declared untrusted in the system prompt. Temperature: 0.2 for analysis/eval/patch, 0.7 for question generation. Use a fast model (e.g. Gemini Flash) for question/eval/patch, a stronger one for pitch and report.

### 9.5 Key Pydantic schemas (M1 + M2 freeze these in minutes 0–15)
```python
class AnswerEvaluation(BaseModel):
    scores: dict[Literal["clarity","specificity","evidence","business_reasoning","differentiation","scalability"], int]  # 0-10
    explanation: str
    strengths: list[str]
    weaknesses: list[str]
    recommended_improvement: str
    weakest_criterion: str
    claims_made: list[str]            # founder facts asserted in the answer (unverified)
    follow_up_question: str | None

class ProfilePatchOp(BaseModel):
    op: Literal["set","add","remove"]; path: str; value: Any; reason: str
class ProfilePatch(BaseModel): ops: list[ProfilePatchOp]

class Claim(BaseModel):
    text: str
    provenance: Literal["source_backed","founder_assumption","calculated","ai_analysis"]
    evidence_ids: list[str] = []
    supporting_quote: str | None = None

class SlideContent(BaseModel):
    key: Literal["problem","solution","product","target_market","market_opportunity","competition",
                 "advantage","business_model","gtm","traction","team","ask"]
    title: str
    bullets: list[Claim | str]
    status: Literal["complete","needs_input"]
```
Validators enforce: a traction/revenue-like number in a slide when the profile field is null → reject.

### 9.6 Validation, retries, fallback
Flow: LLM → structured JSON → Pydantic → application logic → DB.
1. Malformed/invalid → one repair retry with the validation error appended.
2. Still invalid → next provider in the chain.
3. All providers fail → mock fixture (flagged degraded) **or** 503 `LLM_UNAVAILABLE`, per `AI_MODE`.
4. Nothing ever surfaces a raw stack trace.

### 9.7 Mock modes
- `AI_MODE=mock` — instant fixtures, no network.
- `AI_MODE=scripted-demo` — the mock returns different fixtures by turn number (investor questions/evals progress realistically). Best for a reliable live demo.
- `AI_MODE=live` — Gemini/OpenAI chain with mock as last resort.
Fixtures double as frontend mock data, so **they must be committed by minute 15**.

---

## 10. Investor simulator architecture (G)

**Session state** lives entirely in the DB (`investor_sessions` + `investor_turns`); the server is stateless.

### 10.1 Controller (M5, plain Python, no LLM)
```python
def next_intent(session, turns, profile):
    last = turns[-1]
    if last.scores and min(last.scores.values()) < 5 and follow_ups_on(last.topic, turns) < 2:
        return ("follow_up", last.topic)                    # dig into the weakness
    topic = pick_uncovered_topic(turns, profile.gaps)       # highest-severity open gap not yet asked
    return ("new_topic", topic)

def is_done(session, turns): return len(turns) >= session.max_turns
```
Opening question: `("opening", topic of the top critique objection or highest-severity gap)`.

### 10.2 Answer loop (`POST /investor/sessions/{sid}/answer`)
1. Load session and the open turn. **409** if the session is closed or the turn is already answered.
2. `ai.evaluate_answer(ctx, turn)`; save `answer`, `evaluation`, `scores` on the turn.
3. `claims_made` are stored as pending founder claims. They are **not** auto-applied to the profile.
4. If done → return `completed:true` (UI calls `/finish`). Otherwise `next_intent` → `ai.generate_investor_question(ctx, intent, topic, prev_turn)` → insert next turn (`UNIQUE(session_id, seq)` guards double-submits).

### 10.3 Question rules
The prompt receives `intent`, `topic`, previous Q/A, the weakest criterion and weakness text, plus all earlier questions. It must reference the specific weakness of the previous answer and must not repeat a question.

### 10.4 Scoring (coaching metrics, not predictions)
```python
TOPIC_WEIGHTS = {
  "problem":         {"clarity": .5, "specificity": .5},
  "market":          {"evidence": .6, "scalability": .4},
  "differentiation": {"differentiation": .6, "evidence": .4},
  "business_model":  {"business_reasoning": .7, "specificity": .3},
  "validation":      {"evidence": .8, "specificity": .2},
}
dimension = mean(weighted(turn.scores, TOPIC_WEIGHTS[topic]) for turns of that topic) * 10   # None if no turns
overall   = mean(non-null dimensions)                                                        # equal weights
```
Dimension names in the report: `problem_clarity, market_understanding, differentiation, business_model, customer_validation`.

### 10.5 Final report and feedback loop
`ReadinessService.build()`: compute numbers in code → `ai.generate_readiness_narrative(ctx, turns, computed_scores)` (explains, may not change numbers) → `ai.extract_feedback_patches` → DB writes:
1. Insert `readiness_reports`.
2. Insert `feedback_items` (each optionally with `suggested_patch`).
3. New profile version adding AI-raised `gaps` (`change_reason=investor_feedback`).
4. Session → `completed`.

**Closing the loop:** the founder opens a feedback item and enters facts (e.g. "50 students interviewed, 32 interested"). `POST /feedback/{id}/resolve` converts it into a founder-sourced profile patch, marks the related gap resolved, creates profile v(n+1). `POST /pitch/generate` then produces pitch v2, and the UI shows Startup V1 → V2 with a diff.

---

## 11. Market research architecture (H)

```
profile → query builder (3–5 queries: "<segment> <category> competitors", "<competitor> pricing", …)
  → SearchProvider (Tavily), 6s timeout each, asyncio.gather
  → store rows in evidence_sources
  → LLM gets numbered snippets [E1..En] + profile
  → LLM claims must cite evidence_ids and include supporting_quote
  → verifier (code) → provenance assigned
```

**Provenance rules (enforced in code, not left to the LLM)**
- 🟢 `source_backed`: claim cites a valid evidence id **and** `supporting_quote` appears in that snippet (case-insensitive substring). Otherwise it is **downgraded** to `ai_analysis`.
- 🟡 `founder_assumption`: comes from the profile / founder.
- 🔢 `calculated`: computed in Python from `market.size_inputs` (e.g. customers × price × frequency); formula and inputs shown.
- 🔵 `ai_analysis`: everything else.
- Any number (digits, %, currency, "million/billion") in a claim without a verified quote is **stripped** and replaced with "Requires validation".
- Honest caveat for judges: the verifier checks the source contains the quote, not that the source is credible. If time allows, add a small domain allow/blocklist.

**Fallback ladder** (`SEARCH_MODE=live|cached|off`): Tavily fails → reuse earlier `evidence_sources` for this startup → else `research_status="unavailable"`. The LLM then runs on the profile only: every claim is `founder_assumption` or `ai_analysis`, market size is "Requires validation", and the UI shows "Live research unavailable". For the demo startup keep cached results in `research/fixtures/` so the demo works offline.

Competitors from the analysis are upserted into `competitors` with provenance and evidence ids.

---

## 12. Frontend architecture (I)

**Routes:** `/login`, `/` (dashboard), `/startups/new`, and `/startups/:id/` with children `idea`, `clarify`, `value-prop`, `market`, `business-model`, `pitch`, `critique`, `investor/:sessionId?`, `readiness`.

**Layout:** left **Journey Stepper** (from `progress`: locked / available / done / stale) and right collapsible **Startup Profile panel** (completeness meter, open gaps, latest diff highlighted). This is what makes it feel like a coaching journey and not a chatbot.

**Key components:** `ProfilePanel`, `GapList`, `AnalysisCard`, `AssumptionCard`, `ClarificationCard` (one question at a time + "profile updated" toast with diff), `EvidenceCard`, `ProvenanceBadge`, `SlideDeck` (needs_input slides highlighted), `CritiqueList`, `InvestorChat`, `EvaluationCard` (`ScoreBar` per criterion), `ReadinessDashboard` (Recharts radar), `FeedbackActionList`, `DegradedBanner`.

**State:** React Query for server state; auth token in React context + `localStorage`; no Redux.

**API layer:** `api/client.ts` (axios, JWT interceptor, 401 redirect), one file per resource. `VITE_USE_MOCKS=true` swaps in `mocks/` handlers backed by the shared fixtures.

**Type contracts:** FastAPI exposes `/openapi.json`; run `openapi-typescript` after each backend merge to regenerate `types/api.ts`. Until then, hand-write types from the fixtures.

---

## 13. Security architecture (J)

- **Auth:** email + password, bcrypt (passlib), JWT HS256, 60 min expiry, secret from env. Seed a demo user so judges never need to register.
- **Authorization:** one dependency `get_owned_startup(id, user)` on every startup-scoped route; session and feedback routes resolve their startup through it. Other users get 404.
- **PII minimization:** the only PII is email. Profiles are business data. UI hint: "Don't enter personal data." Emails are never sent to an LLM. Logs contain request id, user id, capability, latency, token counts — never prompt bodies or answers (`llm_calls` is metadata only).
- **Secrets:** all keys in `.env`, read only by the backend. `.env.example` committed, `.env` gitignored. No keys in the frontend; LLM and search calls are backend-only.
- **Input validation:** Pydantic length limits (idea ≤ 2000 chars, answers ≤ 1500, name ≤ 100), strip control characters, reject empty/whitespace-only. CORS restricted to the frontend origin.
- **LLM security:** founder text is delimited and declared untrusted; outputs are schema-validated; the LLM has no tools and cannot write to the DB (only validated patches against a path whitelist); slowapi rate limit on AI routes (~20/min/user), which also protects API budget.

---

## 14. Testing strategy (K)

Tooling: `pytest`, `httpx.AsyncClient`, SQLite via the JSON variant, `FakeLLM` (scripted strings) and `FakeSearch`.

| Level | What |
|---|---|
| Unit | `apply_patch` (valid, unknown path rejected), provenance verifier (quote missing → downgraded, number stripped), score aggregation, `next_intent`, `extract_json` with fenced/garbage output |
| AI output | Each schema accepts its fixture. Fuzz: missing field, score 11, wrong enum → `ValidationError` → repair retry → provider fallback → mock |
| API | auth, ownership, validation, envelope shape |
| Integration | full flow on `AI_MODE=mock` |

### The 12 critical hackathon tests
1. Startup creation succeeds and creates profile v1.
2. Empty/whitespace idea → 422.
3. Invalid input (oversize, wrong types) → 422.
4. Idea analysis returns the schema and stores an analysis row.
5. Malformed LLM JSON → repair retry → success; second failure → fallback.
6. All providers fail → 503 with a friendly error (or flagged mock).
7. Search API failure → 200 with `research_status="unavailable"` and no fabricated numbers.
8. DB failure (patched session raises) → 500 error envelope without a stack trace.
9. User B requests user A's startup → 404.
10. Investor session: answer → evaluation → adaptive next question tied to the weakest criterion; second answer to the same turn → 409.
11. Readiness report numbers equal the deterministic computation from the turns.
12. Feedback resolve → profile v(n+1) → pitch v2 reflects the new traction.

Frontend: manual demo script plus Vitest for the mock layer only.

---

## 15. Performance and scalability (L)

**Now:** stateless FastAPI (`uvicorn --workers 2`), Postgres with the indexes above, SQLAlchemy pool (size 5–10), `asyncio.gather` for parallel calls (value prop ∥ market, competitors ∥ market, search queries), generated results stored and re-served (`GET .../latest`, never regenerated on page load), profile projection to keep prompts small, 25 s LLM timeout, skeleton loaders. Warm the app before the demo.

**Bottleneck:** LLM latency (2–15 s per call, more for the pitch). Mitigations: fast model for the interactive loop, pitch generated once and cached, `max_output_tokens` limits. If the investor turn feels slow in testing, merge evaluate + next-question into one call (fewer round trips, less separation).

**Later (upgrade path, no module-boundary changes):** background jobs (ARQ/Celery) for pitch/market/report with polling or SSE; Redis for caching and rate limits; SSE streaming for the investor chat; read replica; partition `investor_turns`; prompt-version column for A/B evaluation; async PPTX export.

---

## 16. 3-hour implementation plan (M)

| Time | M1 Architecture/AI core | M2 Prompts | M3 Backend/DB | M4 Frontend | M5 Investor/Test/Demo |
|---|---|---|---|---|---|
| 0–15 | Repo, `.env.example`, docker-compose (Postgres), **commit Pydantic schemas + fixtures + this doc**, announce "contracts frozen" | Review schemas, draft prompt skeletons, write demo fixtures | Skeleton FastAPI, DB up, SQLAlchemy models from §7 | Vite app, routes, API client with mock flag | Agree topics/scoring, pytest skeleton, FakeLLM |
| 15–30 | `LLMClient`, `MockProvider`, `run()`, `AIService` returning fixtures | analyze_idea + clarification + patch prompts | Alembic migration, auth, startups, profile versions, error envelope | Dashboard, create startup, layout, Stepper, ProfilePanel | `next_intent`, scoring (pure funcs) + unit tests |
| 30–60 | Gemini/OpenAI providers, fallback chain, `context.py` | value prop, competitors/market, pitch prompts | clarify + analyses routes, `apply_patch`; **`InvestorRepo` by minute 45** | Idea + clarification UI, value prop | `InvestorService` start/answer on mock AI |
| 60–75 | **Integration 1** (merge backend + AI + frontend) | Tune prompts on the demo idea with a live model | Fix contract mismatches | Switch mocks off for first flow, regenerate types | First API tests |
| 75–105 | Search provider + verifier, market service | critique, business model, investor question, eval prompts | pitch, critique routes, `progress`, stale flags | Market page, business model, pitch deck, critique | `ReadinessService`, feedback items |
| 105–120 | **Integration 2** (merge investor simulator) | Tune investor prompts with M5 | Pagination, rate limit, error paths | Investor chat, evaluation cards | Full-flow integration test on mock |
| 120–150 | Wire everything, degraded badge, health | Readiness narrative, improved-pitch prompt | Bug fixes, seed demo user + startup | Readiness dashboard, feedback → resolve → V2 diff | Run the 12 tests, fix failures with owners |
| 150–170 | Full run-throughs on live AI | Freeze prompts | Freeze | Polish, empty/error states | Demo script, backup recording |
| 170–180 | **STOP CODING.** Prepare: problem, solution, architecture, AI strategy, live demo, security, scalability, business value | | | | Rehearse twice |

**If behind, cut in this order:** business model page (fold into pitch) → PPTX → pagination → SerpAPI → stale badges.

---

## 17. Project structure (N)

```
backend/
  app/
    main.py
    core/            config.py security.py errors.py logging.py deps.py rate_limit.py
    api/routes/      auth.py startups.py idea.py analyses.py pitch.py investor.py readiness.py feedback.py health.py
    schemas/         common.py auth.py startup.py profile.py idea.py analyses.py pitch.py investor.py readiness.py
    models/          user.py startup.py profile_version.py analysis.py evidence.py competitor.py
                     pitch.py investor.py readiness.py feedback.py llm_call.py
    repositories/    startup_repo.py profile_repo.py analysis_repo.py pitch_repo.py investor_repo.py ...
    services/        profile_service.py idea_service.py analysis_service.py pitch_service.py
                     investor_service.py readiness_service.py feedback_service.py
                     investor/  controller.py scoring.py        # pure functions (M5)
    ai/
      service.py          # AIService facade
      runner.py           # run(): retry / repair / fallback
      context.py          # per-capability profile projections
      schemas/            # Pydantic outputs, one file per capability
      prompts/            # one file per capability + common.py
      providers/          base.py gemini.py openai.py mock.py
      fixtures/           # JSON per capability, shared with frontend mocks
    research/        base.py tavily.py cache.py query_builder.py verifier.py fixtures/
    db/              session.py base.py types.py   # JSONB variant
  alembic/  alembic.ini
  tests/    unit/ api/ integration/ ai/ conftest.py  # FakeLLM, FakeSearch
  .env.example  requirements.txt  Dockerfile

frontend/
  src/
    main.tsx  App.tsx  routes.tsx
    api/         client.ts auth.ts startups.ts idea.ts analyses.ts pitch.ts investor.ts readiness.ts feedback.ts
    mocks/       handlers.ts fixtures/            # copied from backend/app/ai/fixtures
    types/       api.ts
    hooks/       useStartup.ts useProfile.ts useAnalysis.ts useInvestor.ts ...
    pages/       Login Dashboard NewStartup Idea Clarify ValueProp Market BusinessModel Pitch Critique Investor Readiness
    features/    profile/ clarification/ market/ pitch/ investor/ readiness/ feedback/
    components/  Card Stepper ProvenanceBadge ScoreBar DegradedBanner Skeleton
    lib/         format.ts diff.ts
  vite.config.ts  tailwind.config.ts  .env.example

docker-compose.yml  README.md  CONVENTIONS.md  CONTRACTS_CHANGELOG.md
```

---

## 18. Architectural decisions (O)

| Decision | Chosen | Why | Rejected | Why rejected |
|---|---|---|---|---|
| Monolith vs microservices | Modular monolith | One deploy, in-process calls, fits 3 hours; module boundaries allow a later split | Microservices | Network contracts, deployment and debugging cost with zero demo value |
| Postgres vs MongoDB | PostgreSQL | Relational ownership/versions/sessions/joins plus JSONB for flexible LLM output | MongoDB | Weaker integrity for versioning/history; judges score data modeling |
| Direct API vs LangChain/LangGraph | Direct SDKs behind our `LLMClient` | Transparent, testable, few dependencies; our workflow is a fixed pipeline plus a ~30-line controller | LangChain/LangGraph | Abstraction overhead, debugging time |
| JSONB vs relational | Hybrid: JSONB for profile and LLM outputs; relational for sessions, turns, evidence, competitors | Fast iteration on shapes, integrity where it matters | All-relational / all-JSONB | All-relational means a migration per prompt change; all-JSONB loses auditability of turns and evidence |
| Sync vs async processing | Sync HTTP + `asyncio.gather` inside a request | Simple, no queue infra; calls take seconds | Job queue + workers | Needs Redis/worker infra and polling UI; documented as the upgrade path |
| External market search | Tavily, optional, with cache/fixture fallback and code-level claim verification | Real evidence is our credibility differentiator; failure degrades gracefully | LLM-only market analysis | Invents statistics — contradicts the core requirement |
| Provider-independent AI layer | `LLMClient` + fallback chain | Survive outages/rate limits, swap models, test with fakes | Direct calls everywhere | Vendor lock-in; no home for retries, validation or mock mode |
| Profile as versioned JSONB doc | Append-only versions with patches | History, diff UI, staleness detection, undo | Mutable row | Loses the Startup V1 → V2 story |
| Scores in code | Deterministic aggregation; LLM only explains | Reproducible, testable | LLM outputs the overall score | Inconsistent, hard to defend |

---

## 19. Judge-facing explanation (P) — say this in 1–2 minutes

"PitchPilot is a modular FastAPI monolith with a React front end and PostgreSQL. The central idea is the **Startup Profile**: a versioned, structured document that every AI module reads and updates. It isn't a set of separate chatbots. When a founder answers a question, we extract a validated patch, write a new profile version, and generate the next question from the updated profile. That's how a vague idea becomes a specific startup.

The AI layer is provider-independent. We have separate prompts per capability, each with a Pydantic output schema. Every response is validated, gets one repair retry, then falls back to another provider, and finally to a mock — and we flag the response as degraded so we never present fallback content as real analysis. Market analysis uses Tavily, but the LLM can't invent facts. Claims must cite a source and quote it, and code verifies the quote appears in the source. Unsupported numbers are stripped and labelled 'Requires validation'. Every claim is tagged source-backed, founder assumption, calculated, or AI analysis. If search fails, the app still works and says so.

The investor simulator is the core. A small controller decides whether to follow up on a weakness or move to a new topic, and the LLM writes the question from the profile, the previous answer and the scores. Scores are computed deterministically in code and the LLM explains them; they are coaching metrics, not predictions. The readiness report produces feedback items. When the founder adds real evidence, the profile updates to V2 and we generate an improved pitch — closing the loop.

For security we use JWT and bcrypt, ownership checks on every route, backend-only keys, input limits, untrusted-input delimiting for prompts, and metadata-only logging. It's stateless and indexed, and results are stored rather than regenerated, so it scales horizontally now. Queues, Redis and streaming are our upgrade path."

---

# 20. Per-person work briefs

Each member: read Sections 1–3 first, then your brief. **Ownership rule:** only edit files in your own folders. Need a change elsewhere? Ask the owner or open a small PR to them.

## 20.1 Member 1 — Architecture, Integration, AI orchestration

**Owns:** `backend/app/ai/service.py`, `runner.py`, `context.py`, `providers/`, `research/`, `core/`, `main.py`, `docker-compose.yml`, the contract freeze, `feature/integration`.

**Deliverables in order**
1. **0–15 min:** repo skeleton, docker-compose (Postgres), `.env.example`, all Pydantic schemas (with M2 and M3), the fixtures, `CONVENTIONS.md` (Section 3 of this doc). Announce **"contracts frozen"**.
2. **15–30:** `LLMClient` interface, `MockProvider` (loads `fixtures/{capability}.json`), `run()` (validate, 1 repair retry, provider chain, mock fallback), `AIService` with all 13 signatures returning fixtures.
3. **30–60:** Gemini and OpenAI providers, JSON-mode config, 25 s timeouts, `llm_calls` metadata logging, `context.py` projections.
4. **60–75:** **Integration 1**: merge backend + AI + frontend for idea → clarification → value prop → pitch.
5. **75–105:** `research/`: `SearchProvider` interface, Tavily provider, query builder, cache/fixture fallback, claim verifier (quote must appear in snippet; numbers without evidence stripped).
6. **105–120:** **Integration 2**: merge the investor simulator.
7. **120–170:** health endpoint (`ai_mode`, `search_mode`), `meta.degraded` data for the banner, full live-AI run-throughs, integration bug fixing.
8. **170–180:** rehearse the architecture explanation (Section 19).

**Interfaces you expose**
- `get_ai_service()` FastAPI dependency; M3 and M5 only ever call this.
- `AIService.<capability>(ctx, ...) -> <Pydantic model>`. Never raises raw provider errors; raises `LLMInvalidOutput` or `LLMUnavailable`, which the error handler maps to 502/503.

**Definition of done:** with `AI_MODE=mock` every method returns a valid fixture; with `AI_MODE=live` a deliberately corrupted response ends in fallback, not a crash; `curl /health` works.

**Don't:** write prompts (M2) or routes (M3).

## 20.2 Member 2 — AI / LLM engineer

**Owns:** `backend/app/ai/prompts/`, `backend/app/ai/schemas/` (co-owned with M1 for the freeze), and fixture content quality in `backend/app/ai/fixtures/`.

**Deliverables in order**
1. **0–15 min:** review schemas with M1; write **realistic fixtures for the demo startup** (hostel students, healthy affordable food). Good fixtures = a working frontend and a good demo.
2. **15–30:** prompts for `analyze_idea`, `generate_clarification_question`, `extract_profile_patch`.
3. **30–60:** `generate_value_proposition`, `analyze_competitors`, `analyze_market`, `generate_pitch`.
4. **60–75:** test these on the demo idea with a real model; tune until output validates on the first attempt.
5. **75–105:** `critique_pitch`, `analyze_business_model`, `generate_investor_question`, `evaluate_answer`.
6. **105–150:** `generate_readiness_narrative`, `extract_feedback_patches`, the improved-pitch prompt (uses the critique and the updated profile). Tune question/eval prompts with M5.
7. **150–170:** freeze prompts; bug fixes only.

**Prompt file format (uniformity)**
```python
# ai/prompts/evaluate_answer.py
CAPABILITY = "evaluate_answer"
TEMPERATURE = 0.2
SYSTEM = COMMON_RULES + """..."""
USER_TEMPLATE = """<startup_profile>{profile}</startup_profile>
<question>{question}</question>
<founder_answer>{answer}</founder_answer>"""
Output = AnswerEvaluation   # imported from ai/schemas
```

**Rules every prompt follows**
- Import the shared `COMMON_RULES` preamble (Section 9.3).
- Founder text always inside delimiter tags and declared untrusted.
- Clarification: exactly **one** question, about the **highest-priority missing field**, and it sets `target_field`.
- Pitch: unsupplied traction/team/ask → slide `status: needs_input` with the text "Not provided — requires validation".
- Market: every factual claim has `evidence_ids` and a `supporting_quote` copied from the snippet. No TAM/SAM/SOM numbers.
- Investor question: references the specific weakness of the previous answer; never repeats a prior question.
- Evaluation tone: coaching metrics, never "your startup will fail/succeed".

**Definition of done:** each capability passes schema validation on 5 different inputs against a live model, and all prompt files follow the format above.

**Don't:** touch providers or retry logic (M1).

## 20.3 Member 3 — Backend + Database

**Owns:** `backend/app/api/routes/`, `models/`, `repositories/`, `db/`, `alembic/`, request/response `schemas/`, `services/` **except** investor and readiness, `core/security.py`, `core/deps.py`.

**Deliverables in order**
1. **0–15 min:** SQLAlchemy models from Section 7; JSONB-with-JSON-variant type so tests can use SQLite.
2. **15–30:** Alembic initial migration, `session.py` (pool 5–10), error handler + envelopes, register/login/me, `get_owned_startup` dependency.
3. **30–60:** `POST/GET /startups`, `ProfileService.apply_patch()` (path whitelist from the `Profile` model, new version row, `base_version` conflict check), `PATCH /profile`, versions list, idea analyze + clarify routes. **Deliver `InvestorRepo` by minute 45.**
4. **60–75:** **Integration 1**: fix contract mismatches with M4 and M1.
5. **75–105:** analyses routes (`/analyses/{kind}` + `/latest` with `stale` flag), pitch routes, critique route, `progress` computation on `GET /startups/{id}`.
6. **105–120:** feedback resolve route, investor route stubs delegating to M5's `InvestorService`, `ReadinessService` wiring.
7. **120–150:** pagination on lists, rate limiting (slowapi on AI routes), seed data (demo user + demo startup).
8. **150–170:** bug fixes, error paths.

**Interfaces you expose**
- The API table in Section 8, exactly. Any deviation goes through M1.
- Repository classes with plain methods (e.g. `InvestorRepo.create_turn`, `.answer_turn`, `.list_turns(session_id)`).
- `/openapi.json` for M4 to generate types.

**Definition of done:** routes return the fixtures' shapes with `AI_MODE=mock`; the ownership test returns 404 for another user's startup; Alembic upgrades a clean DB.

**Don't:** put business logic in routes, or call an LLM SDK.

## 20.4 Member 4 — Frontend

**Owns:** everything in `frontend/`.

**Deliverables in order**
1. **0–15 min:** Vite + React + TS + Tailwind, React Router routes (Section 12), `api/client.ts` (axios, JWT interceptor, 401 redirect), `VITE_USE_MOCKS` switch, copy fixtures into `mocks/fixtures`.
2. **15–30:** app layout: **Journey Stepper** (left) and **Startup Profile panel** (right: completeness meter, open gaps, highlighted latest diff). Login, dashboard, create-startup.
3. **30–60:** Idea analysis page (analysis, assumption and risk cards, gaps), **Clarification page** (one question at a time, "profile updated" toast with the diff), value proposition page.
4. **60–75:** **Integration 1**: turn off mocks for the first flow; regenerate `types/api.ts` from `/openapi.json`.
5. **75–105:** Market page (evidence cards, provenance badges, competitor table, "research unavailable" banner), business model page (missing-assumption inputs), pitch deck viewer (slide carousel, `needs_input` highlighted), critique page.
6. **105–120:** Investor chat (question bubble, answer box, evaluation card with `ScoreBar` per criterion), turn counter.
7. **120–150:** Readiness dashboard (Recharts radar, "why" text, top gaps, disclaimer), feedback action list, "resolve with your evidence" form → profile v2 diff → regenerate pitch → V1 vs V2 view; `DegradedBanner` when `meta.degraded`.
8. **150–170:** skeletons, empty and error states, responsive polish.

**UI rules (uniformity)**
- Every AI-derived item shows a `ProvenanceBadge` (🟢🟡🔵🔢).
- `null` renders as "Not provided — requires validation" in a consistent muted style.
- Scores show the subtitle "coaching metric", never a prediction.
- Never render a raw error object; show `error.message` and a retry button.
- Steps flagged `stale` show "Out of date — regenerate".

**Definition of done:** the whole journey clicks through with `VITE_USE_MOCKS=true`, then against the real backend with no code changes except the env flag.

**Don't:** put API keys or business logic on the client.

## 20.5 Member 5 — Investor simulator, testing, demo

**Owns:** `backend/app/services/investor_service.py`, `readiness_service.py`, `services/investor/` (pure functions), `backend/tests/`, demo data and presentation.

**Deliverables in order**
1. **0–15 min:** agree the topic enum, criteria keys and scoring table with M1/M2; set up pytest, `conftest.py`, `FakeLLM`, `FakeSearch`.
2. **15–30:** pure functions with unit tests (no DB/LLM needed):
   - `next_intent(turns, profile)`: follow up when the last answer's lowest criterion is < 5 and fewer than 2 follow-ups on that topic; otherwise pick the highest-severity uncovered gap.
   - `is_done(session, turns)`.
   - `compute_dimension_scores(turns)` and `compute_overall(dimensions)` using the weights in Section 10.4 (null dimension = not assessed, excluded from overall).
3. **30–60:** `InvestorService.start()`, `.answer()`, `.finish()` using `get_ai_service()` and a repository Protocol (in-memory fake until M3's repo lands at ~45 min). Idempotency: answering an already-answered turn → 409; closed session → 409.
4. **60–75:** first API tests (startup creation, empty idea, invalid input, unauthorized access).
5. **75–105:** `ReadinessService`: compute numbers, call `generate_readiness_narrative` with the computed scores (the LLM may not change them), create `feedback_items` and the AI-raised gaps profile version.
6. **105–120:** **Integration 2**: merge; run the investor flow end-to-end on mock.
7. **120–150:** the 12 critical tests (Section 14); fix failures with the owners.
8. **150–170:** **demo script and data** (Section 24): seeded demo startup, scripted founder answers (weak, better, with evidence), backup screen recording, slide outline.
9. **170–180:** rehearse twice on stable Wi-Fi.

**Definition of done:** all 12 tests pass with `pytest -q`; the simulator completes a full 5-turn session on mock AI; the demo script runs start to finish in under 6 minutes.

**Don't:** write prompts (M2; give feedback on question/eval quality) or routes (M3 owns stubs that call your service).

---

## 21. Handshake matrix

| From → To | What is handed over | When (min) | Mock until then |
|---|---|---|---|
| M1 → all | Schemas + fixtures + conventions | 15 | n/a (root of everything) |
| M2 → M1 | Prompt modules in the standard format | 30, 60, 105, 150 | M1's mock provider serves fixtures |
| M1 → M3, M5 | `get_ai_service()` with all methods | 30 | returns fixtures |
| M3 → M4 | `/openapi.json`, real routes | 60 | M4's `mocks/` from fixtures |
| M3 → M5 | `InvestorRepo` | 45 | M5's in-memory fake |
| M5 → M3 | `InvestorService`, `ReadinessService` | 60 (start/answer), 105 (readiness) | M3's stub routes return fixtures |
| M1 → M2 | Research evidence format | 75 | M2 uses fixture evidence |

---

## 22. Integration checklists

**Integration 1 (~65–75 min):** create startup → analyze idea → answer 3 clarification questions → see profile v4 → generate value prop → generate pitch. Verify: envelope shape, `meta.ai_mode`, null rendering, ownership 404, no console errors.

**Integration 2 (~115–125 min):** critique the pitch → start investor session → 3 answers with adaptive follow-ups → finish → readiness report → resolve one feedback item → profile v(n+1) → pitch v2. Verify: scores match the deterministic computation, closed-session 409, stale badge appears after the profile changes.

**Pre-demo (170 min):** `AI_MODE=live` and `AI_MODE=mock` both run the full flow; `SEARCH_MODE=off` still completes the flow with the "unavailable" banner.

---

## 23. Git workflow

- Branches: `main`, `feature/ai-engine` (M1 + M2, small PRs), `feature/backend-db` (M3), `feature/frontend` (M4), `feature/investor-simulator` (M5), `feature/integration` (M1).
- Commit every 20–30 minutes; rebase on `main` before each integration point (~65 and ~120 min); M1 merges to `main`.
- Commit messages: `feat(area): message`, e.g. `feat(investor): add next_intent controller`.
- After minute 150: bug fixes and demo only. No new features.

---

## 24. Demo script (~6 minutes)

Startup: *"I want to build an app that helps college students find affordable healthy food."*

1. Raw idea entered → AI analyzes it and shows gaps (which students? what is "healthy"? why not Swiggy/Zomato? revenue? evidence?).
2. Clarification: "Students living in hostels" → profile updates (V2) with a visible diff; next question is generated from the updated profile.
3. "They can't cook and nearby food is unhealthy or expensive" → profile V3. "Those platforms don't focus on student budgets and nutrition" → V4.
4. Value proposition generated from the profile only.
5. Market + competitor analysis: show 🟢 source-backed vs 🟡 founder assumption vs 🔵 AI analysis; market size shows "Requires validation".
6. Business model: commission from restaurants; missing pricing assumptions flagged.
7. Pitch generated; traction slide says "Not provided — requires validation".
8. Pitch critique: weak differentiation, unsupported demand.
9. Investor mode: question → weak answer → evaluation (evidence 3/10) → adaptive follow-up on evidence → several rounds.
10. Readiness report with the *why* and recommended actions ("Interview 20–30 students, test pricing").
11. Founder adds "50 interviewed, 32 interested" → profile V-next → improved pitch V2.
12. Close: **"PitchPilot doesn't just generate a pitch. It makes the founder defend it, identifies what's weak, and continuously improves the startup before they face a real investor."**

Demo safety: run once with `AI_MODE=live` and keep `scripted-demo` ready as the fallback; keep a recorded backup.

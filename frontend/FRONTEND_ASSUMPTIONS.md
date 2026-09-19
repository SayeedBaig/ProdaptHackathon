# Frontend Assumptions & API Contract Register

This document tracks all frontend assumptions, centralized API endpoint routes, schema placeholders, and mock configurations, as required by Section 0 & 3 of `CONVENTIONS.md`.

---

## 1. Centralized Endpoint Paths (`src/api/endpoints.ts`)

Because backend routes are being developed concurrently, all frontend API calls route through `src/api/endpoints.ts`. Modifying any route requires a single-line update.

| AI Capability / Feature | Endpoint Path | Method | Notes |
|---|---|---|---|
| `analyze_idea` | `/api/ai/analyze_idea` | POST | Initial idea decomposition |
| `generate_clarification_question` | `/api/ai/generate_clarification_question` | POST | Clarification query generation |
| `extract_profile_patch` | `/api/ai/extract_profile_patch` | POST | Extracts RFC6902-style patches from founder answers |
| `generate_value_proposition` | `/api/ai/generate_value_proposition` | POST | 4-part value proposition |
| `analyze_competitors` | `/api/ai/analyze_competitors` | POST | Competitor comparison table & matrix |
| `analyze_market` | `/api/ai/analyze_market` | POST | TAM, SAM, SOM calculation and CAGR |
| `analyze_business_model` | `/api/ai/analyze_business_model` | POST | Revenue streams, pricing, unit economics |
| `generate_pitch` | `/api/ai/generate_pitch` | POST | 12-slide structured deck |
| `critique_pitch` | `/api/ai/critique_pitch` | POST | Deck evaluation, objections, priorities |
| `generate_investor_question` | `/api/ai/generate_investor_question` | POST | Dynamic partner-level investor question |
| `evaluate_answer` | `/api/ai/evaluate_answer` | POST | Scored across 6 criteria (0-10) |
| `generate_readiness_narrative` | `/api/ai/generate_readiness_narrative` | POST | Final investor readiness report narrative |
| `extract_feedback_patches` | `/api/ai/extract_feedback_patches` | POST | Turns accepted critique/feedback into profile patches |
| Get Startup Profile | `/api/profile/:id` | GET | Returns full Profile schema |
| Patch Startup Profile | `/api/profile/:id` | PATCH | Applies ProfilePatch ops, updates version |
| List Startups | `/api/startups` | GET | List of founder's startups |
| Create Startup | `/api/startups` | POST | Initialize a new startup workspace |
| Auth Login | `/api/auth/login` | POST | JWT login (bypassed in mock mode) |
| Auth Register | `/api/auth/register` | POST | Founder registration |

---

## 2. Inferred Schemas for Unfinished Backend Capabilities

In `backend/app/ai/schemas/capabilities.py`, several models were placeholders (`pass # To be defined fully by M2`). The frontend defined strict, typed schemas adhering to standard investor conventions:

1. **`ValueProposition`**:
   - `one_line`: str
   - `elevator`: str
   - `differentiation`: str
   - `advantage`: str
   - `target_segment`: str
   - `provenance`: dict mapping fields to provenance enums

2. **`CompetitorAnalysis`**:
   - `direct_competitors`: list of competitor objects with `name`, `pricing`, `strengths`, `weaknesses`, `market_share`, `differentiator`, `provenance`, `source_urls`
   - `indirect_competitors`: list of alternatives
   - `matrix_axes`: `{ x_axis: str, y_axis: str }`
   - `competitor_positions`: list of `{ name, x, y }`

3. **`MarketAnalysis`**:
   - `tam`: `{ value: number, formatted: str, description: str, provenance, sources: list[str] }`
   - `sam`: `{ value: number, formatted: str, description: str, provenance, sources: list[str] }`
   - `som`: `{ value: number, formatted: str, description: str, provenance, sources: list[str] }`
   - `cagr`: number
   - `growth_drivers`: list[str]
   - `market_risks`: list[str]
   - `assumptions`: list[str]

4. **`BusinessModelAnalysis`**:
   - `type`: str (e.g. "B2B SaaS")
   - `revenue_streams`: list of `{ name, model_type, price_point, frequency, margin, calculated }`
   - `pricing_tiers`: list of `{ name, price, billing, features, target_segment }`
   - `unit_economics`: `{ cac: number, ltv: number, payback_months: number, gross_margin: number, ltv_cac_ratio: number, calculated: true }`
   - `cost_structure`: list of cost drivers

5. **`ReadinessNarrative`**:
   - `overall_score`: number (0-100)
   - `verdict`: "Strong Pitch" | "Needs Validation" | "High Risk"
   - `executive_summary`: str
   - `criteria_scores`: dict of all 6 criteria (0-10)
   - `topic_coverage`: dict of 5 topics (0-100%)
   - `top_strengths`: list[str]
   - `critical_gaps`: list[str]
   - `action_plan`: list[str]

6. **`FeedbackItemDraft`**:
   - `id`: UUID
   - `topic`: Topic enum
   - `title`: str
   - `description`: str
   - `source`: "critique" | "investor" | "founder"
   - `status`: "open" | "accepted" | "dismissed" | "done"
   - `suggested_patch`: ProfilePatch | null

---

## 3. Mock Data Strategy
- Fixtures located in `src/mocks/fixtures/` cover realistic startup data for **HyperScale AI** (autonomous cloud Kubernetes cost optimizer).
- In mock mode (`VITE_USE_MOCKS=true`), an in-memory mutable store retains changes (patch applications, gap status updates, new feedback, chat history) throughout the user's browser session.
- "Load Sample Startup" instantly re-initializes complete data across all tabs to ensure a fail-safe hackathon demo.
- Error simulation query parameter `?mock_error=<CODE>` allows deterministic verification of all error states (e.g. `LLM_UNAVAILABLE`, `VERSION_CONFLICT`, `SESSION_CLOSED`).

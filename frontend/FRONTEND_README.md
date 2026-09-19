# PitchPilot Frontend

PitchPilot is an AI startup pitch coach taking founders from a raw idea to an institutional investor-ready 12-slide pitch deck, competitive positioning matrix, and simulated partner Q&A practice session.

---

## 1. Quick Start

### Running with Full Mock Layer (Offline / Hackathon Demo)
To run the complete application end-to-end with simulated latency and zero backend dependencies:

```bash
cd frontend
npm install
npm run dev
```

By default, `.env.example` has `VITE_USE_MOCKS=true`. When `VITE_USE_MOCKS=true`:
1. The app automatically logs in a demo founder (`Alex Vance`, `founder@hyperscale.ai`).
2. All 13 AI capabilities return realistic, structured venture diligence data for **HyperScale AI** (autonomous Kubernetes cost optimizer).
3. The **"Load sample startup"** button in the header instantly pre-fills the workspace with all 12 slides, profile fields, unit economics, and feedback items (a fail-safe demo guarantee).

### Running with Live Backend
To connect to the live backend:

```bash
VITE_API_URL=http://localhost:8000
VITE_USE_MOCKS=false
```

No code changes are required.

---

## 2. Strict Adherence to `CONVENTIONS.md`

- **Snake_case Throughout**: All frontend TypeScript types, API envelopes, and payload schemas use `snake_case` keys matching the backend Pydantic models. No camelCase conversion layer exists anywhere.
- **Contract Enums**: Centralized in `src/types/contracts.ts` with string-literal unions and `as const` arrays:
  - `provenance`: `source_backed | founder_assumption | calculated | ai_analysis` (🟢, 🟡, 🔵, 🔢)
  - `topic`: `problem | market | differentiation | business_model | validation`
  - `criteria`: `clarity, specificity, evidence, business_reasoning, differentiation, scalability` (0–10)
  - `slide_keys`: 12 slide keys (`problem` to `ask`)
  - `gap_status`: `open | resolved`
  - `feedback_status`: `open | accepted | dismissed | done`
  - `session_status`: `active | completed | abandoned`
  - `turn_intent`: `opening | follow_up | new_topic`
  - `ai_capabilities`: 13 capabilities
  - `error_codes`: `VALIDATION_ERROR (422), UNAUTHENTICATED (401), NOT_FOUND (404), VERSION_CONFLICT (409), SESSION_CLOSED (409), RATE_LIMITED (429), LLM_INVALID_OUTPUT (502), LLM_UNAVAILABLE (503)`
- **Null Safety**: Missing data is strictly represented as `null`. It is never coerced to `""`, `"N/A"`, or invented placeholders. The unified `<NullValue />` component renders `"Not provided — requires validation"` for any null datum.
- **Layering**: UI Components → TanStack Query Hooks → Typed `apiClient` (`src/api/client.ts`). No vendor LLM SDKs are imported into the frontend.

---

## 3. Screen Architecture & Capabilities

| Page / Screen | AI Capability | Features |
|---|---|---|
| **1. Overview & Profile** | `analyze_idea`, `generate_clarification_question`, `extract_profile_patch` | Idea decomposition, structured cards, provenance badges + legend, open diligence gaps filter, clarification modal with before/after patch diffs. |
| **2. Value Proposition** | `generate_value_proposition` | One-liner, 30s elevator pitch, core differentiation, unfair advantage, regeneration button. |
| **3. Market & Competition** | `analyze_market`, `analyze_competitors` | TAM/SAM/SOM tiered cards with calculation steps, CAGR, comparison table with audit links, 2x2 competitive positioning matrix. |
| **4. Business Model** | `analyze_business_model` | Monetization cards, 3 pricing tiers, unit economics cards (CAC, LTV, payback, gross margin) with 🔢 `calculated` icon and formula breakdown. |
| **5. Pitch Deck** | `generate_pitch`, `critique_pitch` | 12-slide rail + large 16:9 presentation preview, client-side `.pptx` dynamic export via `pptxgenjs`, critique drawer with investor objections. |
| **6. Feedback** | `extract_feedback_patches` | Unified feedback triage, status transitions (`open`, `accepted`, `dismissed`, `done`), one-click patch extraction and application to profile. |
| **7. Investor Practice** | `generate_investor_question`, `evaluate_answer` | Interactive partner Q&A, turn intent badges, 6-criteria Recharts radar & bar scoring, strengths/weaknesses commentary, new gaps auto-recording. |
| **8. Readiness Report** | `generate_readiness_narrative` | Executive readiness summary, verdict, aggregate radar chart, topic coverage bars, prioritized action plan, print / PDF export stylesheet. |

---

## 4. Client-Side PPTX Export

PitchPilot dynamically imports `pptxgenjs` inside the click handler to export a customized, widescreen (16:9) presentation containing all 12 slides with custom brand styles and provenance annotations.

---

## 5. Developer Error Simulation

Test all error states deterministically using the **"Simulate Error"** dropdown in the top header or appending `?mock_error=<CODE>` to the URL:

- `?mock_error=503` or `?mock_error=LLM_UNAVAILABLE`: Displays service unavailable banner with retry.
- `?mock_error=502` or `?mock_error=LLM_INVALID_OUTPUT`: Displays inline AI output failure callout.
- `?mock_error=409` or `?mock_error=VERSION_CONFLICT`: Refetches profile and toasts conflict notice.
- `?mock_error=SESSION_CLOSED`: Shows session concluded state and disables input.
- `?mock_error=429` or `?mock_error=RATE_LIMITED`: Toasts rate limit alert.
- `?mock_error=422` or `?mock_error=VALIDATION_ERROR`: Field validation error display with copyable `request_id`.

---

## 6. Verification Commands

```bash
# Typecheck strict TypeScript
npm run typecheck

# Production build
npm run build

# Sync backend fixtures if available
npm run sync-fixtures
```

# M1 Work Summary and Presentation Notes

## Your Role (Member 1 - Architecture, Integration, AI orchestration)
You are the **Lead Architect and Integrator** for the PitchPilot project. Your main goal is to lay the foundation for all other teammates to build upon and to stitch the entire system together at key milestones.

You **do not** write API endpoints (M3 does this). You **do not** write LLM prompts (M2 does this). You **do not** write the frontend (M4 does this). Instead, you define the "contracts" (data structures) they all use to communicate with each other.

### The First 15 Minutes (What you just did)
To unblock the team, you executed the "0-15 minute" setup phase:
1. **Repository Skeleton:** Created the base folders (`backend/app/schemas`, `backend/app/ai/schemas`, `backend/app/ai/fixtures`).
2. **Docker Compose:** Created `docker-compose.yml` to spin up PostgreSQL quickly.
3. **Environment Config:** Created `.env.example` mapping out all backend and frontend secrets so everyone has identical names.
4. **Conventions:** Extracted Section 3 of the architecture guide into `CONVENTIONS.md` as the single source of truth for naming (e.g. `snake_case`, ID formats).
5. **Contracts (Schemas & Fixtures):** Created the Pydantic schemas that define the shape of the Startup Profile and all 13 AI capabilities. You also created mock JSON data (fixtures) for the demo startup ("NutriNest"). 

**Milestone Reached:** You can now announce **"Contracts Frozen."** M4 can use your JSON fixtures to build the frontend mocks. M3 can use your Pydantic schemas to build the API. M2 can use your schemas to enforce LLM output shapes.

---

## Explaining PitchPilot to the Judges (1-2 minutes)

*Here is the script you can use to explain your architecture during the presentation. You should own this part of the pitch.*

"PitchPilot is a modular FastAPI monolith with a React front end and PostgreSQL. The central idea is the **Startup Profile**: a versioned, structured document that every AI module reads and updates. It isn't a set of separate chatbots. When a founder answers a question, we extract a validated patch, write a new profile version, and generate the next question from the updated profile. That's how a vague idea becomes a specific startup.

The AI layer is provider-independent. We have separate prompts per capability, each with a Pydantic output schema. Every response is validated, gets one repair retry, then falls back to another provider, and finally to a mock — and we flag the response as degraded so we never present fallback content as real analysis. Market analysis uses Tavily, but the LLM can't invent facts. Claims must cite a source and quote it, and code verifies the quote appears in the source. Unsupported numbers are stripped and labelled 'Requires validation'. Every claim is tagged source-backed, founder assumption, calculated, or AI analysis. If search fails, the app still works and says so.

The investor simulator is the core. A small controller decides whether to follow up on a weakness or move to a new topic, and the LLM writes the question from the profile, the previous answer and the scores. Scores are computed deterministically in code and the LLM explains them; they are coaching metrics, not predictions. The readiness report produces feedback items. When the founder adds real evidence, the profile updates to V2 and we generate an improved pitch — closing the loop.

For security we use JWT and bcrypt, ownership checks on every route, backend-only keys, input limits, untrusted-input delimiting for prompts, and metadata-only logging. It's stateless and indexed, and results are stored rather than regenerated, so it scales horizontally now. Queues, Redis and streaming are our upgrade path."

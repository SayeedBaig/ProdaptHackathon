# Contract Issues & Inconsistencies Log

*Frozen Contract Register — logged for Backend / AI Contract Owner review.*

---

### Issue 1: `provenance` Enum Mismatch (`founder` vs `founder_assumption`)
- **Location**: `backend/app/schemas/profile.py:94` vs `CONVENTIONS.md:16` and `backend/app/ai/schemas/capabilities.py:30`
- **Description**:
  `CONVENTIONS.md` specifies the enum as:
  `source_backed | founder_assumption | calculated | ai_analysis`
  However, `backend/app/schemas/profile.py` defines the provenance dict as:
  `dict[str, Literal["founder", "source_backed", "calculated", "ai_analysis"]]`
  (using `"founder"` instead of `"founder_assumption"`).
- **Frontend Resolution**:
  The frontend accepts both `"founder"` and `"founder_assumption"`, automatically normalizing `"founder"` to `"founder_assumption"` in the UI display layer to maintain strict adherence to the conventions.

---

### Issue 2: Gap Severity Typing (`int` vs `Literal["low", "med", "high"]`)
- **Location**: `backend/app/schemas/profile.py:74` vs `backend/app/schemas/profile.py:67`
- **Description**:
  `Risk` uses `severity: Literal["low", "med", "high"]`, while `Gap` uses `severity: int`.
- **Frontend Resolution**:
  The frontend models Gap severity as `number` (1 to 5 scale), rendering badges for Low (1-2), Medium (3), and High/Critical (4-5).

---

### Issue 3: Incomplete Capability Schemas in `capabilities.py`
- **Location**: `backend/app/ai/schemas/capabilities.py:43-54, 79-84`
- **Description**:
  `ValueProposition`, `CompetitorAnalysis`, `MarketAnalysis`, `BusinessModelAnalysis`, `ReadinessNarrative`, and `FeedbackItemDraft` contain only `pass`.
- **Frontend Resolution**:
  Structured schemas have been modeled in `src/types/capabilities.ts` and registered in `frontend/FRONTEND_ASSUMPTIONS.md`.

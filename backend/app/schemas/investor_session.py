"""
Investor Simulator session schemas (M5).

These are NOT part of the frozen AI contracts in ``app.ai.schemas`` -- they are
the Investor Simulator's own session/domain models, built on top of the
frozen ``InvestorQuestion`` / ``AnswerEvaluation`` contracts.

Conventions followed (see CONVENTIONS.md):
- Session status reuses the shared enum: active | completed | abandoned.
- Turn intent reuses the shared enum: opening | follow_up | new_topic.
- Topic values reused on questions: problem | market | differentiation |
  business_model | validation.
- Timestamps are ISO-8601 UTC (datetime, serialized by Pydantic as such).
- IDs are UUID strings.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.ai.schemas import AnswerEvaluation, InvestorQuestion

SessionStatus = Literal["active", "completed", "abandoned"]
TurnIntent = Literal["opening", "follow_up", "new_topic"]


class AnswerTurn(BaseModel):
    """One question/answer/evaluation cycle within a session."""

    question: InvestorQuestion
    turn_intent: TurnIntent = "opening"
    answer_text: str | None = None
    evaluation: AnswerEvaluation | None = None
    answered_at: datetime | None = None
    evaluated_at: datetime | None = None


class InvestorSession(BaseModel):
    """Full state of one investor-simulator session."""

    session_id: str
    startup_id: str
    status: SessionStatus = "active"
    current_question_index: int = 0
    turns: list[AnswerTurn] = Field(default_factory=list)
    started_at: datetime
    completed_at: datetime | None = None

    @property
    def current_turn(self) -> AnswerTurn | None:
        if 0 <= self.current_question_index < len(self.turns):
            return self.turns[self.current_question_index]
        return None

    @property
    def asked_question_ids(self) -> list[str]:
        return [turn.question.id for turn in self.turns]


ReadinessCategory = Literal[
    "Needs Significant Improvement",
    "Developing",
    "Investor-ready with Improvements",
    "Strong Readiness",
]


class ReadinessReport(BaseModel):
    """Coaching-style readiness report generated after a session completes."""

    session_id: str
    startup_id: str
    overall_score: float  # 0-100, normalized
    category: ReadinessCategory
    per_criterion_averages: dict[str, float]
    weakest_criterion: str
    strengths: list[str]
    weaknesses: list[str]
    turn_count: int
    generated_at: datetime

"""
Abstraction the Investor Simulator service depends on, instead of any
concrete AI implementation.

Per CONVENTIONS.md 3.5, nothing outside ``ai/providers/`` may import an LLM
vendor SDK. M1 can add a ``live_investor_provider.py`` here later that
satisfies the same Protocol (calling Gemini/OpenAI), and swap it in via
``AI_MODE`` at the composition root -- ``InvestorSimulatorService`` itself
never needs to change.
"""

from __future__ import annotations

from typing import Protocol

from app.ai.schemas import AnswerEvaluation, InvestorQuestion
from app.schemas.profile import Profile


class InvestorAIProvider(Protocol):
    def generate_investor_question(
        self,
        profile: Profile,
        asked_question_ids: list[str],
    ) -> InvestorQuestion | None:
        """Return the next investor question, or None if the question bank
        is exhausted for this session."""
        ...

    def generate_follow_up_question(
        self,
        profile: Profile,
        base_question: InvestorQuestion,
        follow_up_text: str,
    ) -> InvestorQuestion:
        """Wrap a follow-up prompt (e.g. AnswerEvaluation.follow_up_question)
        as a proper InvestorQuestion, same topic as the question it follows."""
        ...

    def evaluate_answer(
        self,
        profile: Profile,
        question: InvestorQuestion,
        answer_text: str,
    ) -> AnswerEvaluation:
        ...

from __future__ import annotations
from typing import Protocol
from app.ai.schemas import AnswerEvaluation, InvestorQuestion
from app.schemas.profile import Profile

class LLMProvider(Protocol):
    async def complete_json(self, prompt: str, timeout: int = 25) -> str:
        """
        Calls the LLM provider and returns the raw response string, which should be JSON.
        Raises LLMUnavailable on network or timeout errors.
        """
        ...

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

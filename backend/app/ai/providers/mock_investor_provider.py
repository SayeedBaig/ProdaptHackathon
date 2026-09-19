"""
Deterministic mock implementation of InvestorAIProvider.

No network calls, no vendor SDK, no randomness: the same inputs always
produce the same outputs, so pytest tests are fully stable. This satisfies
CONVENTIONS.md 3.6 (mock-first rule) and the task's "MOCK-FIRST REQUIREMENT".

Question bank and topics:
    Topics reuse the frozen enum (problem | market | differentiation |
    business_model | validation) -- no new topic values are introduced.
"""

from __future__ import annotations

import uuid

from app.ai.providers.base import InvestorAIProvider
from app.ai.schemas import AnswerEvaluation, InvestorQuestion
from app.schemas.profile import Profile
from app.services.errors import AIProviderError

# id, text, intent, topic
_QUESTION_BANK: list[tuple[str, str, str, str]] = [
    ("q1", "What specific problem are you solving?", "problem_definition", "problem"),
    ("q2", "Who is your target customer and who is actually paying?", "customer_segmentation", "market"),
    ("q3", "What evidence do you have that customers need this?", "evidence_of_demand", "validation"),
    ("q4", "Who are your main competitors and why would customers choose you?", "competitive_landscape", "differentiation"),
    ("q5", "How will you make money?", "revenue_model", "business_model"),
    ("q6", "How will you acquire your first customers?", "go_to_market", "market"),
    ("q7", "What prevents competitors from copying your solution?", "defensibility", "differentiation"),
    ("q8", "How does the business scale?", "scalability", "business_model"),
    ("q9", "What evidence do you have that your solution works?", "solution_validation", "validation"),
]

_CRITERIA = ("clarity", "specificity", "evidence", "business_reasoning", "differentiation", "scalability")

_EVIDENCE_WORDS = ("data", "survey", "interview", "%", "pilot", "customers", "users", "revenue")
_REASONING_WORDS = ("because", "since", "so that", "therefore", "as a result")
_DIFFERENTIATION_WORDS = ("unlike", "compared to", "competitor", "unique", "instead of", "different from")
_SCALABILITY_WORDS = ("scale", "expand", "grow", "market size", "automat", "repeatable")


class MockInvestorProvider:
    """Implements InvestorAIProvider deterministically. Satisfies the
    InvestorAIProvider Protocol structurally (duck typing), no inheritance
    needed."""

    def __init__(self, simulate_failure: bool = False):
        self.simulate_failure = simulate_failure

    def generate_investor_question(
        self,
        profile: Profile,
        asked_question_ids: list[str],
    ) -> InvestorQuestion | None:
        if self.simulate_failure:
            raise AIProviderError("Mock AI provider simulated failure while generating a question.")

        for qid, text, intent, topic in _QUESTION_BANK:
            if qid not in asked_question_ids:
                return InvestorQuestion(id=qid, text=text, intent=intent, topic=topic)
        return None  # question bank exhausted

    def generate_follow_up_question(
        self,
        profile: Profile,
        base_question: InvestorQuestion,
        follow_up_text: str,
    ) -> InvestorQuestion:
        if self.simulate_failure:
            raise AIProviderError("Mock AI provider simulated failure while generating a follow-up.")

        return InvestorQuestion(
            id=f"{base_question.id}-follow-up-{uuid.uuid4().hex[:8]}",
            text=follow_up_text,
            intent="follow_up",
            topic=base_question.topic,
        )

    def evaluate_answer(
        self,
        profile: Profile,
        question: InvestorQuestion,
        answer_text: str,
    ) -> AnswerEvaluation:
        if self.simulate_failure:
            raise AIProviderError("Mock AI provider simulated failure while evaluating an answer.")

        scores = self._score_answer(answer_text)
        weakest = min(scores, key=lambda criterion: scores[criterion])

        strengths = [c for c, v in scores.items() if v >= 7]
        weaknesses = [c for c, v in scores.items() if v <= 4]

        follow_up = None
        if scores[weakest] <= 5:
            follow_up = f"Can you go deeper on {weakest.replace('_', ' ')} for this answer?"

        return AnswerEvaluation(
            scores=scores,
            explanation=(
                f"Deterministic mock evaluation of the answer to '{question.text}' "
                f"based on length, evidence markers, and reasoning markers found in the text."
            ),
            strengths=strengths or ["clear_attempt"],
            weaknesses=weaknesses or [],
            recommended_improvement=f"Strengthen {weakest.replace('_', ' ')} with concrete specifics.",
            weakest_criterion=weakest,
            claims_made=self._extract_claims(answer_text),
            follow_up_question=follow_up,
        )

    @staticmethod
    def _score_answer(answer_text: str) -> dict[str, int]:
        text = answer_text.lower()
        word_count = len(text.split())

        def clamp(value: float) -> int:
            return max(0, min(10, round(value)))

        # Clarity: rewards a reasonable, non-trivial length; penalizes very
        # short or extremely long/rambling answers.
        if word_count == 0:
            clarity = 0
        elif word_count < 5:
            clarity = 2
        elif word_count <= 60:
            clarity = 6 + min(4, word_count // 15)
        else:
            clarity = 6

        specificity = clamp(2 + min(6, word_count / 12))

        evidence = clamp(2 + 2 * sum(1 for w in _EVIDENCE_WORDS if w in text))
        business_reasoning = clamp(2 + 2 * sum(1 for w in _REASONING_WORDS if w in text))
        differentiation = clamp(2 + 2 * sum(1 for w in _DIFFERENTIATION_WORDS if w in text))
        scalability = clamp(2 + 2 * sum(1 for w in _SCALABILITY_WORDS if w in text))

        return {
            "clarity": clamp(clarity),
            "specificity": specificity,
            "evidence": evidence,
            "business_reasoning": business_reasoning,
            "differentiation": differentiation,
            "scalability": scalability,
        }

    @staticmethod
    def _extract_claims(answer_text: str) -> list[str]:
        sentences = [s.strip() for s in answer_text.replace("\n", " ").split(".") if s.strip()]
        return sentences[:3]

"""
Investor Simulator business logic (M5).

Flow implemented:
    START SESSION -> GENERATE QUESTION -> USER ANSWER -> EVALUATE ANSWER ->
    STORE TURN -> CALCULATE SCORE -> SHOW FEEDBACK -> NEXT QUESTION -> REPEAT
    -> COMPLETE SESSION -> READINESS REPORT

Depends only on the InvestorAIProvider and InvestorSessionRepository
Protocols (dependency injection) -- no LLM vendor import, no DB import, no
knowledge of HTTP. This keeps the module swappable per CONVENTIONS.md 3.5
and independently testable per 3.6.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.ai.providers.base import InvestorAIProvider
from app.repositories.investor_session_repository import InvestorSessionRepository
from app.schemas.investor_session import AnswerTurn, InvestorSession, ReadinessReport
from app.schemas.profile import Profile
from app.services import scoring
from app.services.errors import SessionClosedError, SessionNotFoundError, ValidationError


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class InvestorSimulatorService:
    def __init__(self, ai_provider: InvestorAIProvider, repo: InvestorSessionRepository):
        self._ai_provider = ai_provider
        self._repo = repo

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start_session(self, startup_id: str, profile: Profile) -> InvestorSession:
        first_question = self._ai_provider.generate_investor_question(
            profile=profile, asked_question_ids=[]
        )
        if first_question is None:
            raise ValidationError("No investor questions available to start a session.")

        session = InvestorSession(
            session_id=str(uuid.uuid4()),
            startup_id=startup_id,
            status="active",
            current_question_index=0,
            turns=[AnswerTurn(question=first_question, turn_intent="opening")],
            started_at=_utcnow(),
        )
        self._repo.create(session)
        return session

    def get_current_question(self, session_id: str):
        session = self._require_active_session(session_id)
        turn = session.current_turn
        if turn is None:
            raise ValidationError("No current question for this session.")
        return turn.question

    # ------------------------------------------------------------------
    # Answering
    # ------------------------------------------------------------------

    def submit_answer(self, session_id: str, answer_text: str) -> InvestorSession:
        if answer_text is None or not answer_text.strip():
            raise ValidationError("Answer text must not be empty.")

        session = self._require_active_session(session_id)
        turn = session.current_turn
        if turn is None:
            raise ValidationError("No current question to answer.")

        turn.answer_text = answer_text.strip()
        turn.answered_at = _utcnow()
        self._repo.update(session)
        return session

    def evaluate_current_answer(self, session_id: str, profile: Profile):
        session = self._require_active_session(session_id)
        turn = session.current_turn
        if turn is None:
            raise ValidationError("No current question to evaluate.")
        if turn.answer_text is None:
            raise ValidationError("Cannot evaluate before an answer has been submitted.")

        evaluation = self._ai_provider.evaluate_answer(
            profile=profile, question=turn.question, answer_text=turn.answer_text
        )
        turn.evaluation = evaluation
        turn.evaluated_at = _utcnow()
        self._repo.update(session)
        return evaluation

    # ------------------------------------------------------------------
    # Progression
    # ------------------------------------------------------------------

    def get_next_question(self, session_id: str, profile: Profile):
        """Returns the next InvestorQuestion, or None when there are no more
        questions (caller should call complete_session next)."""
        session = self._require_active_session(session_id)
        current_turn = session.current_turn
        if current_turn is None or current_turn.evaluation is None:
            raise ValidationError("Current question must be evaluated before advancing.")

        # If the evaluator produced a follow-up prompt, ask that first.
        if current_turn.turn_intent != "follow_up" and current_turn.evaluation.follow_up_question:
            follow_up_question = self._ai_provider.generate_follow_up_question(
                profile=profile,
                base_question=current_turn.question,
                follow_up_text=current_turn.evaluation.follow_up_question,
            )
            session.turns.append(AnswerTurn(question=follow_up_question, turn_intent="follow_up"))
            session.current_question_index += 1
            self._repo.update(session)
            return follow_up_question

        next_question = self._ai_provider.generate_investor_question(
            profile=profile, asked_question_ids=session.asked_question_ids
        )
        if next_question is None:
            return None  # question bank exhausted; caller should complete the session

        session.turns.append(AnswerTurn(question=next_question, turn_intent="new_topic"))
        session.current_question_index += 1
        self._repo.update(session)
        return next_question

    def complete_session(self, session_id: str) -> InvestorSession:
        session = self._require_active_session(session_id)
        session.status = "completed"
        session.completed_at = _utcnow()
        self._repo.update(session)
        return session

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def get_readiness_report(self, session_id: str) -> ReadinessReport:
        session = self._repo.get(session_id)
        if session is None:
            raise SessionNotFoundError(f"Session '{session_id}' was not found.")
        if session.status != "completed":
            raise SessionClosedError("Readiness report requires a completed session.")

        evaluated_turns = [t for t in session.turns if t.evaluation is not None]
        turn_scores = [t.evaluation.scores for t in evaluated_turns]

        overall_score = scoring.session_readiness_score(turn_scores)
        averages = scoring.per_criterion_averages(turn_scores)
        weakest = scoring.weakest_criterion(averages)

        strengths: list[str] = []
        weaknesses: list[str] = []
        for turn in evaluated_turns:
            strengths.extend(turn.evaluation.strengths)
            weaknesses.extend(turn.evaluation.weaknesses)

        return ReadinessReport(
            session_id=session.session_id,
            startup_id=session.startup_id,
            overall_score=overall_score,
            category=scoring.readiness_category(overall_score),
            per_criterion_averages=averages,
            weakest_criterion=weakest,
            strengths=sorted(set(strengths)),
            weaknesses=sorted(set(weaknesses)),
            turn_count=len(evaluated_turns),
            generated_at=_utcnow(),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _require_active_session(self, session_id: str) -> InvestorSession:
        session = self._repo.get(session_id)
        if session is None:
            raise SessionNotFoundError(f"Session '{session_id}' was not found.")
        if session.status != "active":
            raise SessionClosedError(f"Session '{session_id}' is '{session.status}', not active.")
        return session

import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.core.errors import AppException, NotFoundError, SessionClosedError
from app.models.investor import InvestorSession, InvestorTurn
from app.models.startup import Startup
from app.repositories.investor_repo import InvestorRepo
from app.repositories.profile_repo import ProfileRepo
from app.services.ai_service import MockAIService

TOPICS_ORDER = ["differentiation", "validation", "problem", "market", "business_model"]

class InvestorService:
    @staticmethod
    async def start_session(
        db: Session,
        startup: Startup,
        pitch_version_id: uuid.UUID | None,
        max_turns: int,
        ai_service: MockAIService,
    ) -> tuple[InvestorSession, InvestorTurn]:
        session = InvestorRepo.create_session(
            db=db,
            startup_id=startup.id,
            pitch_version_id=pitch_version_id,
            max_turns=max_turns,
        )

        pv = ProfileRepo.get_latest_version(db, startup.id)
        first_topic = "differentiation"
        question_obj = await ai_service.generate_investor_question(
            ctx=pv.data if pv else {},
            intent="opening",
            topic=first_topic,
        )

        turn = InvestorRepo.create_turn(
            db=db,
            session_id=session.id,
            seq=1,
            topic=first_topic,
            intent="opening",
            question=question_obj.text,
        )

        return session, turn

    @staticmethod
    async def answer_turn(
        db: Session,
        session_id: uuid.UUID,
        turn_seq: int,
        answer: str,
        ai_service: MockAIService,
    ) -> tuple[dict[str, Any], InvestorTurn | None, bool]:
        session = InvestorRepo.get_session(db, session_id)
        if not session:
            raise NotFoundError("Investor session not found")

        if session.status != "active":
            raise SessionClosedError("Session is already completed or closed")

        turn = InvestorRepo.get_turn(db, session_id, turn_seq)
        if not turn:
            raise NotFoundError(f"Turn {turn_seq} not found in session")

        if turn.answer is not None:
            raise AppException(
                code="SESSION_CLOSED",
                message="Turn has already been answered",
                status_code=409,
            )

        pv = ProfileRepo.get_latest_version(db, session.startup_id)
        profile_data = pv.data if pv else {}

        # 1. Evaluate answer
        eval_result = await ai_service.evaluate_answer(
            ctx=profile_data,
            turn={"seq": turn.seq, "topic": turn.topic, "question": turn.question, "answer": answer},
        )
        eval_dict = eval_result.model_dump()
        scores = eval_result.scores

        # 2. Persist turn evaluation
        InvestorRepo.answer_turn(
            db=db,
            turn=turn,
            answer=answer,
            evaluation=eval_dict,
            scores=scores,
        )

        # 3. Check completion
        if turn_seq >= session.max_turns:
            InvestorRepo.complete_session(db, session)
            return eval_dict, None, True

        # 4. Adaptive next question controller
        next_seq = turn_seq + 1
        lowest_score = min(scores.values()) if scores else 10
        if lowest_score < 5:
            next_intent = "follow_up"
            next_topic = turn.topic
        else:
            next_intent = "new_topic"
            next_topic = TOPICS_ORDER[turn_seq % len(TOPICS_ORDER)]

        next_q = await ai_service.generate_investor_question(
            ctx=profile_data,
            intent=next_intent,
            topic=next_topic,
            prev_turn={"question": turn.question, "answer": answer, "scores": scores},
        )

        next_turn = InvestorRepo.create_turn(
            db=db,
            session_id=session.id,
            seq=next_seq,
            topic=next_topic,
            intent=next_intent,
            question=next_q.text,
        )

        return eval_dict, next_turn, False

    @staticmethod
    def finish_session(db: Session, session_id: uuid.UUID) -> InvestorSession:
        session = InvestorRepo.get_session(db, session_id)
        if not session:
            raise NotFoundError("Investor session not found")
        if session.status == "active":
            InvestorRepo.complete_session(db, session)
        return session

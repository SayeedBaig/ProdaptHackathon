import uuid
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.orm import Session
from app.models.investor import InvestorSession, InvestorTurn

class InvestorRepo:
    @staticmethod
    def create_session(
        db: Session,
        startup_id: uuid.UUID,
        pitch_version_id: uuid.UUID | None = None,
        max_turns: int = 5,
    ) -> InvestorSession:
        session = InvestorSession(
            startup_id=startup_id,
            pitch_version_id=pitch_version_id,
            status="active",
            max_turns=max_turns,
            started_at=datetime.now(timezone.utc),
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_session(db: Session, session_id: uuid.UUID) -> InvestorSession | None:
        return db.query(InvestorSession).filter(InvestorSession.id == session_id).first()

    @staticmethod
    def get_active_session(db: Session, startup_id: uuid.UUID) -> InvestorSession | None:
        return (
            db.query(InvestorSession)
            .filter(InvestorSession.startup_id == startup_id, InvestorSession.status == "active")
            .order_by(InvestorSession.started_at.desc())
            .first()
        )

    @staticmethod
    def list_sessions(db: Session, startup_id: uuid.UUID, skip: int = 0, limit: int = 20) -> list[InvestorSession]:
        return (
            db.query(InvestorSession)
            .filter(InvestorSession.startup_id == startup_id)
            .order_by(InvestorSession.started_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_turn(
        db: Session,
        session_id: uuid.UUID,
        seq: int,
        topic: str,
        intent: str,
        question: str,
    ) -> InvestorTurn:
        turn = InvestorTurn(
            session_id=session_id,
            seq=seq,
            topic=topic,
            intent=intent,
            question=question,
            created_at=datetime.now(timezone.utc),
        )
        db.add(turn)
        db.commit()
        db.refresh(turn)
        return turn

    @staticmethod
    def get_turn(db: Session, session_id: uuid.UUID, seq: int) -> InvestorTurn | None:
        return (
            db.query(InvestorTurn)
            .filter(InvestorTurn.session_id == session_id, InvestorTurn.seq == seq)
            .first()
        )

    @staticmethod
    def answer_turn(
        db: Session,
        turn: InvestorTurn,
        answer: str,
        evaluation: dict[str, Any],
        scores: dict[str, int],
    ) -> InvestorTurn:
        turn.answer = answer
        turn.evaluation = evaluation
        turn.scores = scores
        turn.answered_at = datetime.now(timezone.utc)
        db.add(turn)
        db.commit()
        db.refresh(turn)
        return turn

    @staticmethod
    def list_turns(db: Session, session_id: uuid.UUID) -> list[InvestorTurn]:
        return (
            db.query(InvestorTurn)
            .filter(InvestorTurn.session_id == session_id)
            .order_by(InvestorTurn.seq.asc())
            .all()
        )

    @staticmethod
    def complete_session(db: Session, session: InvestorSession) -> InvestorSession:
        session.status = "completed"
        session.completed_at = datetime.now(timezone.utc)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

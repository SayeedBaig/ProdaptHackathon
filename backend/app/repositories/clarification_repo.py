import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.clarification import ClarificationTurn

class ClarificationRepo:
    @staticmethod
    def create_turn(
        db: Session,
        startup_id: uuid.UUID,
        seq: int,
        question: str,
        target_field: str | None,
        profile_version_before: int,
    ) -> ClarificationTurn:
        turn = ClarificationTurn(
            startup_id=startup_id,
            seq=seq,
            question=question,
            target_field=target_field,
            profile_version_before=profile_version_before,
        )
        db.add(turn)
        db.commit()
        db.refresh(turn)
        return turn

    @staticmethod
    def get_turn(db: Session, startup_id: uuid.UUID, seq: int) -> ClarificationTurn | None:
        return (
            db.query(ClarificationTurn)
            .filter(ClarificationTurn.startup_id == startup_id, ClarificationTurn.seq == seq)
            .first()
        )

    @staticmethod
    def get_latest_turn(db: Session, startup_id: uuid.UUID) -> ClarificationTurn | None:
        return (
            db.query(ClarificationTurn)
            .filter(ClarificationTurn.startup_id == startup_id)
            .order_by(ClarificationTurn.seq.desc())
            .first()
        )

    @staticmethod
    def answer_turn(
        db: Session,
        turn: ClarificationTurn,
        answer: str,
        profile_version_after: int,
    ) -> ClarificationTurn:
        turn.answer = answer
        turn.profile_version_after = profile_version_after
        turn.answered_at = datetime.now(timezone.utc)
        db.add(turn)
        db.commit()
        db.refresh(turn)
        return turn

    @staticmethod
    def list_turns(db: Session, startup_id: uuid.UUID) -> list[ClarificationTurn]:
        return (
            db.query(ClarificationTurn)
            .filter(ClarificationTurn.startup_id == startup_id)
            .order_by(ClarificationTurn.seq.asc())
            .all()
        )

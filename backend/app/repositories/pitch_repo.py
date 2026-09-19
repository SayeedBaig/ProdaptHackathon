import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.models.pitch import PitchVersion, PitchCritique

class PitchRepo:
    @staticmethod
    def create_pitch(
        db: Session,
        startup_id: uuid.UUID,
        version: int,
        profile_version: int,
        slides: list[dict[str, Any]],
        parent_pitch_id: uuid.UUID | None = None,
        ai_mode: str | None = None,
    ) -> PitchVersion:
        pv = PitchVersion(
            startup_id=startup_id,
            version=version,
            profile_version=profile_version,
            slides=slides,
            parent_pitch_id=parent_pitch_id,
            ai_mode=ai_mode,
        )
        db.add(pv)
        db.commit()
        db.refresh(pv)
        return pv

    @staticmethod
    def get_pitch_by_version(db: Session, startup_id: uuid.UUID, version: int) -> PitchVersion | None:
        return (
            db.query(PitchVersion)
            .filter(PitchVersion.startup_id == startup_id, PitchVersion.version == version)
            .first()
        )

    @staticmethod
    def get_pitch_by_id(db: Session, pitch_id: uuid.UUID) -> PitchVersion | None:
        return db.query(PitchVersion).filter(PitchVersion.id == pitch_id).first()

    @staticmethod
    def get_latest_pitch(db: Session, startup_id: uuid.UUID) -> PitchVersion | None:
        return (
            db.query(PitchVersion)
            .filter(PitchVersion.startup_id == startup_id)
            .order_by(PitchVersion.version.desc())
            .first()
        )

    @staticmethod
    def list_pitches(db: Session, startup_id: uuid.UUID) -> list[PitchVersion]:
        return (
            db.query(PitchVersion)
            .filter(PitchVersion.startup_id == startup_id)
            .order_by(PitchVersion.version.desc())
            .all()
        )

    @staticmethod
    def save_critique(db: Session, pitch_version_id: uuid.UUID, output: dict[str, Any]) -> PitchCritique:
        critique = PitchCritique(
            pitch_version_id=pitch_version_id,
            output=output,
        )
        db.add(critique)
        db.commit()
        db.refresh(critique)
        return critique

    @staticmethod
    def get_latest_critique(db: Session, pitch_version_id: uuid.UUID) -> PitchCritique | None:
        return (
            db.query(PitchCritique)
            .filter(PitchCritique.pitch_version_id == pitch_version_id)
            .order_by(PitchCritique.created_at.desc())
            .first()
        )

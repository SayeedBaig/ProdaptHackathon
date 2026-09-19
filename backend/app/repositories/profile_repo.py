import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.models.profile_version import ProfileVersion

class ProfileRepo:
    @staticmethod
    def create_version(
        db: Session,
        startup_id: uuid.UUID,
        version: int,
        data: dict[str, Any],
        change_reason: str,
        patch: list[dict[str, Any]] | None = None,
        completeness_pct: int | None = None,
    ) -> ProfileVersion:
        pv = ProfileVersion(
            startup_id=startup_id,
            version=version,
            data=data,
            patch=patch,
            change_reason=change_reason,
            completeness_pct=completeness_pct,
        )
        db.add(pv)
        db.commit()
        db.refresh(pv)
        return pv

    @staticmethod
    def get_version(db: Session, startup_id: uuid.UUID, version: int) -> ProfileVersion | None:
        return (
            db.query(ProfileVersion)
            .filter(ProfileVersion.startup_id == startup_id, ProfileVersion.version == version)
            .first()
        )

    @staticmethod
    def get_latest_version(db: Session, startup_id: uuid.UUID) -> ProfileVersion | None:
        return (
            db.query(ProfileVersion)
            .filter(ProfileVersion.startup_id == startup_id)
            .order_by(ProfileVersion.version.desc())
            .first()
        )

    @staticmethod
    def list_versions(db: Session, startup_id: uuid.UUID) -> list[ProfileVersion]:
        return (
            db.query(ProfileVersion)
            .filter(ProfileVersion.startup_id == startup_id)
            .order_by(ProfileVersion.version.asc())
            .all()
        )

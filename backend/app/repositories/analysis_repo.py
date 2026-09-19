import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.models.analysis import Analysis

class AnalysisRepo:
    @staticmethod
    def save_analysis(
        db: Session,
        startup_id: uuid.UUID,
        kind: str,
        profile_version: int,
        output: dict[str, Any],
        ai_mode: str | None = None,
        model: str | None = None,
    ) -> Analysis:
        analysis = Analysis(
            startup_id=startup_id,
            kind=kind,
            profile_version=profile_version,
            output=output,
            ai_mode=ai_mode,
            model=model,
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    @staticmethod
    def get_latest_analysis(db: Session, startup_id: uuid.UUID, kind: str) -> Analysis | None:
        return (
            db.query(Analysis)
            .filter(Analysis.startup_id == startup_id, Analysis.kind == kind)
            .order_by(Analysis.created_at.desc())
            .first()
        )

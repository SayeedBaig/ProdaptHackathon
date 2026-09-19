import uuid
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.orm import Session
from app.models.readiness import ReadinessReport
from app.models.feedback import FeedbackItem

class ReadinessRepo:
    @staticmethod
    def save_report(
        db: Session,
        startup_id: uuid.UUID,
        session_id: uuid.UUID | None,
        profile_version: int,
        overall: int | None,
        dimension_scores: dict[str, Any],
        narrative: dict[str, Any],
    ) -> ReadinessReport:
        report = ReadinessReport(
            startup_id=startup_id,
            session_id=session_id,
            profile_version=profile_version,
            overall=overall,
            dimension_scores=dimension_scores,
            narrative=narrative,
            created_at=datetime.now(timezone.utc),
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_latest_report(db: Session, startup_id: uuid.UUID) -> ReadinessReport | None:
        return (
            db.query(ReadinessReport)
            .filter(ReadinessReport.startup_id == startup_id)
            .order_by(ReadinessReport.created_at.desc())
            .first()
        )

    @staticmethod
    def create_feedback_item(
        db: Session,
        startup_id: uuid.UUID,
        title: str,
        recommendation: str,
        report_id: uuid.UUID | None = None,
        topic: str | None = None,
        suggested_patch: list[dict[str, Any]] | None = None,
    ) -> FeedbackItem:
        item = FeedbackItem(
            startup_id=startup_id,
            report_id=report_id,
            topic=topic,
            title=title,
            recommendation=recommendation,
            suggested_patch=suggested_patch,
            status="open",
            created_at=datetime.now(timezone.utc),
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get_feedback_item(db: Session, feedback_id: uuid.UUID) -> FeedbackItem | None:
        return db.query(FeedbackItem).filter(FeedbackItem.id == feedback_id).first()

    @staticmethod
    def list_feedback(db: Session, startup_id: uuid.UUID, status: str | None = None) -> list[FeedbackItem]:
        query = db.query(FeedbackItem).filter(FeedbackItem.startup_id == startup_id)
        if status:
            query = query.filter(FeedbackItem.status == status)
        return query.order_by(FeedbackItem.created_at.desc()).all()

    @staticmethod
    def resolve_feedback(db: Session, item: FeedbackItem, status: str) -> FeedbackItem:
        item.status = status
        item.resolved_at = datetime.now(timezone.utc)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

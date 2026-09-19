import uuid
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID, JSONType

class FeedbackItem(Base):
    __tablename__ = "feedback_items"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False, index=True)
    report_id = Column(GUID, ForeignKey("readiness_reports.id", ondelete="SET NULL"), nullable=True, index=True)
    topic = Column(String(50), nullable=True)
    title = Column(String(255), nullable=False)
    recommendation = Column(Text, nullable=False)
    suggested_patch = Column(JSONType, nullable=True)
    status = Column(String(50), default="open", nullable=False)  # open | accepted | dismissed | done
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("status IN ('open', 'accepted', 'dismissed', 'done')", name="ck_feedback_items_status"),
        Index("ix_feedback_items_startup_status", "startup_id", "status"),
    )

    startup = relationship("Startup", back_populates="feedback_items")
    report = relationship("ReadinessReport", back_populates="feedback_items")

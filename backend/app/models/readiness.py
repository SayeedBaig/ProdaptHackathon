import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID, JSONType

class ReadinessReport(Base):
    __tablename__ = "readiness_reports"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id = Column(GUID, ForeignKey("investor_sessions.id", ondelete="SET NULL"), nullable=True, index=True)
    profile_version = Column(Integer, nullable=False)
    overall = Column(Integer, nullable=True)
    dimension_scores = Column(JSONType, nullable=True)
    narrative = Column(JSONType, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        Index("ix_readiness_reports_startup_created", "startup_id", created_at.desc()),
    )

    startup = relationship("Startup", back_populates="readiness_reports")
    session = relationship("InvestorSession", back_populates="readiness_reports")
    feedback_items = relationship("FeedbackItem", back_populates="report")

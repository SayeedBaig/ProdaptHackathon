import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID

class Startup(Base):
    __tablename__ = "startups"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    raw_idea = Column(Text, nullable=False)
    current_version_id = Column(GUID, ForeignKey("profile_versions.id", use_alter=True, name="fk_startup_current_version"), nullable=True)
    status = Column(String(50), default="active", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        Index("ix_startups_user_created", "user_id", created_at.desc()),
    )

    user = relationship("User", back_populates="startups")
    profile_versions = relationship("ProfileVersion", back_populates="startup", foreign_keys="[ProfileVersion.startup_id]", cascade="all, delete-orphan")
    clarification_turns = relationship("ClarificationTurn", back_populates="startup", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="startup", cascade="all, delete-orphan")
    evidence_sources = relationship("EvidenceSource", back_populates="startup", cascade="all, delete-orphan")
    competitors = relationship("Competitor", back_populates="startup", cascade="all, delete-orphan")
    pitch_versions = relationship("PitchVersion", back_populates="startup", cascade="all, delete-orphan")
    investor_sessions = relationship("InvestorSession", back_populates="startup", cascade="all, delete-orphan")
    readiness_reports = relationship("ReadinessReport", back_populates="startup", cascade="all, delete-orphan")
    feedback_items = relationship("FeedbackItem", back_populates="startup", cascade="all, delete-orphan")

import uuid
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID, JSONType

class InvestorSession(Base):
    __tablename__ = "investor_sessions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False, index=True)
    pitch_version_id = Column(GUID, ForeignKey("pitch_versions.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(50), default="active", nullable=False)  # active | completed | abandoned
    max_turns = Column(Integer, default=5, nullable=False)
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("status IN ('active', 'completed', 'abandoned')", name="ck_investor_sessions_status"),
        Index("ix_investor_sessions_startup_started", "startup_id", started_at.desc()),
    )

    startup = relationship("Startup", back_populates="investor_sessions")
    turns = relationship("InvestorTurn", back_populates="session", cascade="all, delete-orphan", order_by="InvestorTurn.seq")
    readiness_reports = relationship("ReadinessReport", back_populates="session")


class InvestorTurn(Base):
    __tablename__ = "investor_turns"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    session_id = Column(GUID, ForeignKey("investor_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    seq = Column(Integer, nullable=False)
    topic = Column(String(50), nullable=False)  # problem | market | differentiation | business_model | validation
    intent = Column(String(50), nullable=False)  # opening | follow_up | new_topic
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    evaluation = Column(JSONType, nullable=True)
    scores = Column(JSONType, nullable=True)  # {clarity, specificity, evidence, business_reasoning, differentiation, scalability}
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    answered_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("intent IN ('opening', 'follow_up', 'new_topic')", name="ck_investor_turns_intent"),
        UniqueConstraint("session_id", "seq", name="uq_investor_turns_session_seq"),
    )

    session = relationship("InvestorSession", back_populates="turns")

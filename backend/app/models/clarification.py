import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID

class ClarificationTurn(Base):
    __tablename__ = "clarification_turns"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False, index=True)
    seq = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    target_field = Column(String(255), nullable=True)
    answer = Column(Text, nullable=True)
    profile_version_before = Column(Integer, nullable=False)
    profile_version_after = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    answered_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("startup_id", "seq", name="uq_clarification_turns_startup_seq"),
    )

    startup = relationship("Startup", back_populates="clarification_turns")

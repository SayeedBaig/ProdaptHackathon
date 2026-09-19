import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID, JSONType

class ProfileVersion(Base):
    __tablename__ = "profile_versions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    data = Column(JSONType, nullable=False)
    patch = Column(JSONType, nullable=True)
    change_reason = Column(String(50), nullable=False)  # clarification | founder_edit | investor_feedback | feedback_action | system
    completeness_pct = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint("startup_id", "version", name="uq_profile_versions_startup_version"),
    )

    startup = relationship("Startup", back_populates="profile_versions", foreign_keys=[startup_id])

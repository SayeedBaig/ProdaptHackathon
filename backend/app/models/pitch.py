import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID, JSONType

class PitchVersion(Base):
    __tablename__ = "pitch_versions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    profile_version = Column(Integer, nullable=False)
    slides = Column(JSONType, nullable=False)
    parent_pitch_id = Column(GUID, ForeignKey("pitch_versions.id", ondelete="SET NULL"), nullable=True)
    ai_mode = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        UniqueConstraint("startup_id", "version", name="uq_pitch_versions_startup_version"),
    )

    startup = relationship("Startup", back_populates="pitch_versions")
    critiques = relationship("PitchCritique", back_populates="pitch_version", cascade="all, delete-orphan")


class PitchCritique(Base):
    __tablename__ = "pitch_critiques"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    pitch_version_id = Column(GUID, ForeignKey("pitch_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    output = Column(JSONType, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    pitch_version = relationship("PitchVersion", back_populates="critiques")

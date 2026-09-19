import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID, JSONType

class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    differentiation = Column(Text, nullable=True)
    strengths = Column(JSONType, nullable=True)
    weaknesses = Column(JSONType, nullable=True)
    evidence_ids = Column(JSONType, nullable=True)  # List of UUID strings
    provenance = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    startup = relationship("Startup", back_populates="competitors")

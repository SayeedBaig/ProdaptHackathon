import uuid
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID

class EvidenceSource(Base):
    __tablename__ = "evidence_sources"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False, index=True)
    analysis_id = Column(GUID, ForeignKey("analyses.id", ondelete="SET NULL"), nullable=True, index=True)
    query = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    title = Column(Text, nullable=True)
    snippet = Column(Text, nullable=True)
    provider = Column(String(50), nullable=True)
    retrieved_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    kind = Column(String(50), default="search_result", nullable=False)

    __table_args__ = (
        CheckConstraint("kind IN ('search_result', 'founder_provided')", name="ck_evidence_sources_kind"),
    )

    startup = relationship("Startup", back_populates="evidence_sources")
    analysis = relationship("Analysis", back_populates="evidence_sources")

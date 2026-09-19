import uuid
from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.db.types import GUID, JSONType

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, ForeignKey("startups.id", ondelete="CASCADE"), nullable=False, index=True)
    kind = Column(String(50), nullable=False)  # idea | value_proposition | market | business_model
    profile_version = Column(Integer, nullable=False)
    output = Column(JSONType, nullable=False)
    ai_mode = Column(String(50), nullable=True)
    model = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (
        CheckConstraint("kind IN ('idea', 'value_proposition', 'market', 'business_model')", name="ck_analyses_kind"),
        Index("ix_analyses_startup_kind_created", "startup_id", "kind", created_at.desc()),
    )

    startup = relationship("Startup", back_populates="analyses")
    evidence_sources = relationship("EvidenceSource", back_populates="analysis")

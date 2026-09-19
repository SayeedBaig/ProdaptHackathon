import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from app.db.session import Base
from app.db.types import GUID

class LLMCall(Base):
    __tablename__ = "llm_calls"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    startup_id = Column(GUID, nullable=True, index=True)
    capability = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    latency_ms = Column(Integer, nullable=True)
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    outcome = Column(String(50), nullable=False)  # success | error | fallback | degraded
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

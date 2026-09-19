import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    id: uuid.UUID
    startup_id: uuid.UUID
    kind: str
    profile_version: int
    output: dict[str, Any]
    stale: bool = False
    ai_mode: str | None = None
    model: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict

class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    kind: str
    profile_version: int
    output: dict[str, Any]
    stale: bool = False
    ai_mode: str | None = None
    model: str | None = None
    created_at: datetime

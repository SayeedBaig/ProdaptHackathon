import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel

class GeneratePitchRequest(BaseModel):
    improve_from_pitch_id: uuid.UUID | None = None

class PitchResponse(BaseModel):
    id: uuid.UUID
    startup_id: uuid.UUID
    version: int
    profile_version: int
    slides: list[dict[str, Any]]
    parent_pitch_id: uuid.UUID | None = None
    stale: bool = False
    ai_mode: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class CritiqueResponse(BaseModel):
    id: uuid.UUID
    pitch_version_id: uuid.UUID
    output: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict

class GeneratePitchRequest(BaseModel):
    improve_from_pitch_id: uuid.UUID | None = None

class PitchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    version: int
    profile_version: int
    slides: list[dict[str, Any]]
    parent_pitch_id: uuid.UUID | None = None
    stale: bool = False
    ai_mode: str | None = None
    created_at: datetime

class CritiqueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    pitch_version_id: uuid.UUID
    output: dict[str, Any]
    created_at: datetime

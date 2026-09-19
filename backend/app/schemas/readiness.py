import uuid
from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

class FeedbackItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    report_id: uuid.UUID | None = None
    topic: str | None = None
    title: str
    recommendation: str
    suggested_patch: list[dict[str, Any]] | None = None
    status: str  # open | accepted | dismissed | done
    created_at: datetime
    resolved_at: datetime | None = None

class ResolveFeedbackRequest(BaseModel):
    action: Literal["accept", "dismiss"]
    founder_input: str | None = None

class ReadinessReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    startup_id: uuid.UUID
    session_id: uuid.UUID | None = None
    profile_version: int
    overall: int | None = None
    dimensions: dict[str, int | None] = Field(default_factory=dict)
    narrative: dict[str, Any] = Field(default_factory=dict)
    feedback_items: list[FeedbackItemResponse] = Field(default_factory=list)
    created_at: datetime

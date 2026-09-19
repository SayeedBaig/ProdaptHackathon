import uuid
from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.profile import Profile

class CreateStartupRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    raw_idea: str = Field(min_length=5, max_length=2000)

class UpdateStartupRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    status: str | None = None

class ProfilePatchOpRequest(BaseModel):
    op: Literal["set", "add", "remove"]
    path: str
    value: Any
    reason: str = "founder_edit"

class UpdateProfileRequest(BaseModel):
    base_version: int
    ops: list[ProfilePatchOpRequest]

class ProgressStep(BaseModel):
    key: str
    status: Literal["locked", "available", "done", "stale"]

class ProgressResponse(BaseModel):
    steps: list[ProgressStep]

class StartupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    raw_idea: str
    current_version_id: uuid.UUID | None = None
    profile_version: int = 1
    profile: Profile | dict[str, Any] | None = None
    progress: ProgressResponse | None = None
    status: str
    created_at: datetime
    updated_at: datetime

class StartupListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    raw_idea: str
    profile_version: int = 1
    status: str
    created_at: datetime
    updated_at: datetime

class StartupListResponse(BaseModel):
    items: list[StartupListItem]
    total: int
    page: int
    page_size: int

class ProfileVersionItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    version: int
    change_reason: str
    completeness_pct: int | None = None
    created_at: datetime
    data: dict[str, Any]
    patch: list[dict[str, Any]] | None = None

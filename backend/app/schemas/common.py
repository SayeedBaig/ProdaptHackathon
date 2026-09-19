from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class Meta(BaseModel):
    ai_mode: str = "mock"  # live | fallback_provider | mock
    model: str = "gemini-2.0-flash"
    degraded: bool = False
    warnings: list[str] = Field(default_factory=list)
    profile_version: int | None = None

class DataEnvelope(BaseModel, Generic[T]):
    data: T
    meta: Meta | None = None

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)
    request_id: str | None = None

class ErrorEnvelope(BaseModel):
    error: ErrorDetail

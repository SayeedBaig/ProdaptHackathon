from typing import Any
from pydantic import BaseModel, Field
from app.ai.schemas.capabilities import ClarificationQuestion, ProfilePatchOp

class ClarificationAnswerRequest(BaseModel):
    question_id: str
    answer: str = Field(min_length=1, max_length=1500)
    base_version: int

class ClarificationSkipRequest(BaseModel):
    question_id: str

class ClarificationResponse(BaseModel):
    profile_diff: list[ProfilePatchOp] = Field(default_factory=list)
    profile_version: int
    next_question: ClarificationQuestion | None = None
    ready_for_next_step: bool = False
    completeness_pct: int = 0

import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

class StartInvestorSessionRequest(BaseModel):
    pitch_version_id: uuid.UUID | None = None
    max_turns: int = 5

class SubmitInvestorAnswerRequest(BaseModel):
    turn_seq: int
    answer: str = Field(min_length=1, max_length=1500)

class InvestorTurnResponse(BaseModel):
    id: uuid.UUID | None = None
    seq: int
    topic: str
    intent: str
    question: str
    answer: str | None = None
    evaluation: dict[str, Any] | None = None
    scores: dict[str, int] | None = None
    created_at: datetime | None = None
    answered_at: datetime | None = None

    class Config:
        from_attributes = True

class InvestorSessionResponse(BaseModel):
    id: uuid.UUID
    startup_id: uuid.UUID
    pitch_version_id: uuid.UUID | None = None
    status: str
    max_turns: int
    turns: list[InvestorTurnResponse] = Field(default_factory=list)
    current_turn: InvestorTurnResponse | None = None
    completed: bool = False
    started_at: datetime
    completed_at: datetime | None = None

    class Config:
        from_attributes = True

class InvestorAnswerResponse(BaseModel):
    evaluation: dict[str, Any] | None = None
    next_turn: InvestorTurnResponse | None = None
    completed: bool = False

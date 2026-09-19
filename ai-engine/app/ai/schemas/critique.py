from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from app.ai.schemas.common import TopicType

class CritiqueIssue(BaseModel):
    topic: TopicType
    severity: Literal["low", "medium", "high"] = "medium"
    text: str
    recommendation: str

class PitchCritique(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=100.0)
    clarity_score: float = Field(..., ge=0.0, le=100.0)
    persuasion_score: float = Field(..., ge=0.0, le=100.0)
    issues: List[CritiqueIssue] = Field(default_factory=list)
    investor_objections: List[str] = Field(default_factory=list)
    top_priorities: List[str] = Field(default_factory=list)

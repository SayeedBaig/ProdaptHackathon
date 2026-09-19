from pydantic import BaseModel, Field
from typing import List, Optional
from app.ai.schemas.common import GapItem

class FirstQuestion(BaseModel):
    id: str = "q1"
    text: str = Field(..., description="First targeted follow-up question")
    target_field: str = Field("customer.primary_segment", description="Profile path to fill")

class IdeaAnalysis(BaseModel):
    problem: str = Field(..., description="Core problem statement")
    target_customer: str = Field(..., description="Target customer segment")
    solution: str = Field(..., description="Proposed solution summary")
    pain_points: List[str] = Field(default_factory=list, description="Key pain points")
    assumptions: List[str] = Field(default_factory=list, description="Key unvalidated assumptions")
    risks: List[str] = Field(default_factory=list, description="Identified risk factors")
    missing_information: List[str] = Field(default_factory=list, description="Critical information gaps")
    first_question: FirstQuestion

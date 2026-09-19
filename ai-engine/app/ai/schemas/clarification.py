from pydantic import BaseModel, Field
from typing import List, Optional, Any, Literal

class ClarificationQuestion(BaseModel):
    id: str = "cq1"
    text: str = Field(..., description="Targeted clarification question")
    target_field: str = Field(..., description="Profile path aimed at")
    category: str = Field("Market", description="Topic category: Problem, Market, Monetization, Traction, Defensibility")
    rationale: str = Field(..., description="Why this detail is crucial for investors")
    sample_answer_hint: str = Field(..., description="Example of a strong founder answer")

class ProfilePatchOp(BaseModel):
    op: Literal["set", "add", "remove"]
    path: str = Field(..., description="Whitelisted profile JSON path (e.g. customer.primary_segment)")
    value: Any
    source: Literal["founder", "ai"] = "founder"
    reason: str = Field(..., description="Explanation of patch change")

class ProfilePatch(BaseModel):
    ops: List[ProfilePatchOp] = Field(default_factory=list)

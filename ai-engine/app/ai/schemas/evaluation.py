from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class CriterionScores(BaseModel):
    clarity: int = Field(..., ge=0, le=10, description="Clarity score (0-10)")
    specificity: int = Field(..., ge=0, le=10, description="Specificity score (0-10)")
    evidence: int = Field(..., ge=0, le=10, description="Evidence score (0-10)")
    business_reasoning: int = Field(..., ge=0, le=10, description="Business reasoning score (0-10)")
    differentiation: int = Field(..., ge=0, le=10, description="Differentiation score (0-10)")
    scalability: int = Field(..., ge=0, le=10, description="Scalability score (0-10)")

class AnswerEvaluation(BaseModel):
    scores: CriterionScores
    explanation: str = Field(..., description="Qualitative feedback on the founder's answer")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommended_improvement: str = Field(..., description="Model answer for the founder to practice")
    weakest_criterion: str = Field(..., description="Name of lowest-scoring criterion (e.g., evidence)")
    claims_made: List[str] = Field(default_factory=list, description="Founder facts asserted in answer")
    follow_up_question: Optional[str] = None

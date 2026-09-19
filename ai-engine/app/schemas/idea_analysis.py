from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.common import StartupIdeaInput

class RiskFactor(BaseModel):
    category: str = Field(..., description="Category: Technical, Market, Execution, Financial", example="Market")
    risk: str = Field(..., description="Description of the risk", example="High competition from established generic AI writing tools.")
    mitigation: str = Field(..., description="Recommended mitigation strategy", example="Focus on domain-specific investor pitch deck workflows and real-time audio Q&A coaching.")

class IdeaAnalysisRequest(BaseModel):
    startup_info: StartupIdeaInput

class IdeaAnalysisResponse(BaseModel):
    title: str = Field(..., example="PitchCoach AI")
    problem_statement: str = Field(..., description="Refined definition of the core problem being solved")
    proposed_solution: str = Field(..., description="Refined summary of the solution")
    target_audience: str = Field(..., description="Primary user persona and target customer segment")
    novelty_score: float = Field(..., ge=0.0, le=100.0, description="Innovation / uniqueness score out of 100")
    clarity_score: float = Field(..., ge=0.0, le=100.0, description="Clarity and completeness score out of 100")
    key_strengths: List[str] = Field(..., description="Core advantages of the concept")
    potential_weaknesses: List[str] = Field(..., description="Areas needing improvement or validation")
    risk_factors: List[RiskFactor] = Field(..., description="Identified risk factors and mitigations")
    summary: str = Field(..., description="Executive summary of the idea analysis")

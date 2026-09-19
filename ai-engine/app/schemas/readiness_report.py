from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.common import StartupIdeaInput

class DimensionScore(BaseModel):
    dimension: str = Field(..., description="Idea Clarity, Market Viability, Value Prop & Product, Pitch Quality, Investor Defense", example="Idea Clarity")
    score: float = Field(..., ge=0.0, le=100.0)
    summary: str = Field(..., description="Brief status of this dimension")

class ReadinessReportRequest(BaseModel):
    startup_info: StartupIdeaInput
    idea_analysis_score: Optional[float] = None
    market_score: Optional[float] = None
    pitch_score: Optional[float] = None
    qna_score: Optional[float] = None

class ReadinessReportResponse(BaseModel):
    overall_readiness_score: float = Field(..., ge=0.0, le=100.0, description="Composite Investment Readiness Score (0-100)")
    readiness_badge: str = Field(..., description="Not Ready, Early Stage, Pitch Ready, Investor Approved", example="Pitch Ready")
    dimension_scores: List[DimensionScore]
    key_highlights: List[str] = Field(..., description="Top investor-attractive aspects of the startup")
    red_flags: List[str] = Field(..., description="Urgent red flags that could cause investor rejection")
    actionable_next_steps: List[str] = Field(..., description="Prioritized roadmap to reach 90+ readiness score")

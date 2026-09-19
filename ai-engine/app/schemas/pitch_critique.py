from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.pitch_deck import PitchSlide

class SlideCritique(BaseModel):
    slide_number: int = Field(..., example=1)
    title: str = Field(..., example="Problem")
    clarity_score: float = Field(..., ge=0.0, le=100.0, description="Clarity score for this slide")
    persuasion_score: float = Field(..., ge=0.0, le=100.0, description="Persuasiveness score for this slide")
    feedback: str = Field(..., description="Detailed critique of the slide content")
    suggested_fix: str = Field(..., description="Actionable improvement to make this slide punchier")

class PitchCritiqueRequest(BaseModel):
    slides: Optional[List[PitchSlide]] = None
    pitch_script: Optional[str] = None

class PitchCritiqueResponse(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=100.0, description="Overall pitch deck score (0-100)")
    clarity_score: float = Field(..., ge=0.0, le=100.0)
    persuasion_score: float = Field(..., ge=0.0, le=100.0)
    slide_critiques: List[SlideCritique]
    top_strengths: List[str] = Field(..., description="Strongest parts of the pitch")
    critical_gaps: List[str] = Field(..., description="Missing key information or weak claims")
    actionable_recommendations: List[str] = Field(..., description="Step-by-step improvements to raise the score")

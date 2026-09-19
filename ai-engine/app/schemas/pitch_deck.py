from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.common import StartupIdeaInput
from app.schemas.value_prop import ValuePropositionResponse
from app.schemas.market_analysis import MarketAnalysisResponse

class PitchSlide(BaseModel):
    slide_number: int = Field(..., example=1)
    title: str = Field(..., example="Problem: Pitch Prep is Broken")
    key_bullets: List[str] = Field(..., description="Main bullet points for the slide")
    visual_suggestion: str = Field(..., description="Suggested chart, visual, or layout concept")
    speaker_notes: str = Field(..., description="Script notes for the founder while presenting this slide")

class PitchScriptSet(BaseModel):
    elevator_pitch_30s: str = Field(..., description="30-second high-energy pitch script")
    overview_pitch_2min: str = Field(..., description="2-minute executive pitch script")
    full_pitch_5min: str = Field(..., description="5-minute comprehensive slide-by-slide script")

class PitchGenerationRequest(BaseModel):
    startup_info: StartupIdeaInput
    value_prop: Optional[ValuePropositionResponse] = None
    market_analysis: Optional[MarketAnalysisResponse] = None

class PitchGenerationResponse(BaseModel):
    slides: List[PitchSlide]
    scripts: PitchScriptSet

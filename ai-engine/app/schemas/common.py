from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List, Dict, Any
from datetime import datetime, timezone

T = TypeVar('T')

class StartupIdeaInput(BaseModel):
    title: str = Field(..., description="Startup or Project Name", json_schema_extra={"example": "PitchCoach AI"})
    raw_description: str = Field(..., description="Detailed description of the startup idea, problem solved, or product vision", json_schema_extra={"example": "An AI startup coach that helps entrepreneurs refine ideas, generate pitch decks, analyze market opportunities, and practice investor Q&A."})
    target_industry: Optional[str] = Field("B2B SaaS / Artificial Intelligence", description="Industry or sector", json_schema_extra={"example": "AI & Enterprise Software"})
    stage: Optional[str] = Field("Idea Stage", description="Current stage: Idea, Prototype, MVP, Pre-Seed, Seed", json_schema_extra={"example": "Idea Stage"})
    location: Optional[str] = Field("Global", description="Target geographical market", json_schema_extra={"example": "North America / Global"})
    team_summary: Optional[str] = Field(None, description="Key team background or technical capabilities", json_schema_extra={"example": "2 Co-founders with AI/LLM & Business background"})

class BaseAIResponse(BaseModel, Generic[T]):
    success: bool = True
    module: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    processing_time_ms: float = 0.0
    data: T

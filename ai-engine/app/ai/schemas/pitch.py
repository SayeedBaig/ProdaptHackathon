from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union
from app.ai.schemas.common import SlideKeyType
from app.ai.schemas.market import Claim

class SlideContent(BaseModel):
    key: SlideKeyType
    title: str
    bullets: List[Union[Claim, str]] = Field(default_factory=list)
    visual_concept: Optional[str] = None
    speaker_notes: Optional[str] = None
    status: Literal["complete", "needs_input"] = "complete"

class PitchScripts(BaseModel):
    elevator_pitch_30s: str
    overview_pitch_2min: str
    full_pitch_5min: str

class Pitch(BaseModel):
    pitch_id: Optional[str] = None
    version: int = 1
    profile_version: int = 1
    slides: List[SlideContent] = Field(default_factory=list)
    scripts: PitchScripts

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ReadinessNarrative(BaseModel):
    summary: str = Field(..., description="Executive summary of startup readiness")
    why: Dict[str, str] = Field(..., description="Key reasoning per readiness dimension")
    top_gaps: List[str] = Field(default_factory=list, description="Critical unaddressed gaps")
    disclaimer: str = Field(
        "Coaching metrics, not a prediction of success.",
        description="Standard disclaimer statement"
    )

from pydantic import BaseModel, Field
from typing import List, Optional
from app.ai.schemas.common import ProvenanceType

class CompetitorItem(BaseModel):
    id: str = "c1"
    name: str
    description: str
    differentiation: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    provenance: ProvenanceType = "source_backed"

class CompetitorAnalysis(BaseModel):
    competitors: List[CompetitorItem] = Field(default_factory=list)
    analysis_summary: str = Field(..., description="Summary of competitive landscape and moat")

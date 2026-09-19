from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from app.ai.schemas.common import ProvenanceType

class Claim(BaseModel):
    text: str
    provenance: ProvenanceType = "ai_analysis"
    evidence_ids: List[str] = Field(default_factory=list)
    supporting_quote: Optional[str] = None

class MarketSegment(BaseModel):
    name: str
    description: Optional[str] = None
    provenance: ProvenanceType = "founder_assumption"

class MarketSize(BaseModel):
    tam: Optional[str] = None
    sam: Optional[str] = None
    som: Optional[str] = None
    status: Literal["ok", "partial", "Requires validation"] = "Requires validation"
    calculation: Optional[str] = None

class EvidenceSource(BaseModel):
    id: str
    title: str
    url: str
    snippet: str
    provider: str = "tavily"

class MarketAnalysis(BaseModel):
    research_status: Literal["ok", "partial", "unavailable"] = "ok"
    segments: List[MarketSegment] = Field(default_factory=list)
    market_size: MarketSize = Field(default_factory=MarketSize)
    opportunities: List[Claim] = Field(default_factory=list)
    threats: List[Claim] = Field(default_factory=list)
    evidence: List[EvidenceSource] = Field(default_factory=list)

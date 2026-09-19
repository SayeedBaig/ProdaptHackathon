from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List, Dict, Any, Literal
from datetime import datetime, timezone

T = TypeVar('T')

# Master Provenance Enum
ProvenanceType = Literal["source_backed", "founder_assumption", "calculated", "ai_analysis"]

# Master Topic Enum
TopicType = Literal["problem", "market", "differentiation", "business_model", "validation"]

# Standard Slide Keys
SlideKeyType = Literal[
    "problem", "solution", "product", "target_market", "market_opportunity",
    "competition", "advantage", "business_model", "gtm", "traction", "team", "ask"
]

class ResponseMeta(BaseModel):
    ai_mode: Literal["live", "fallback_provider", "mock", "scripted-demo"] = "mock"
    model: str = "gemini-2.5-flash"
    degraded: bool = False
    warnings: List[str] = Field(default_factory=list)
    profile_version: int = 1
    processing_time_ms: float = 0.0

class SuccessEnvelope(BaseModel, Generic[T]):
    data: T
    meta: ResponseMeta

class ErrorDetails(BaseModel):
    code: str = Field(..., example="VALIDATION_ERROR")
    message: str = Field(..., example="Friendly error description")
    details: Dict[str, Any] = Field(default_factory=dict)
    request_id: Optional[str] = None

class ErrorEnvelope(BaseModel):
    error: ErrorDetails

# Startup Profile Sub-Schemas
class IdentitySection(BaseModel):
    startup_name: str = ""
    raw_idea: str = ""
    one_liner: Optional[str] = None

class ProblemSection(BaseModel):
    statement: Optional[str] = None
    pain_points: List[str] = Field(default_factory=list)

class CustomerSection(BaseModel):
    primary_segment: Optional[str] = None
    persona: Optional[str] = None
    segments: List[str] = Field(default_factory=list)

class SolutionSection(BaseModel):
    description: Optional[str] = None
    key_features: List[str] = Field(default_factory=list)

class ValuePropositionSection(BaseModel):
    one_line: Optional[str] = None
    elevator: Optional[str] = None
    differentiation: Optional[str] = None
    advantage: Optional[str] = None

class MarketSizeInputs(BaseModel):
    customers: Optional[float] = None
    price: Optional[float] = None
    frequency: Optional[float] = None

class MarketSection(BaseModel):
    summary: Optional[str] = None
    size_inputs: MarketSizeInputs = Field(default_factory=MarketSizeInputs)

class CompetitorRef(BaseModel):
    name: str = ""
    competitor_id: Optional[str] = None

class BusinessModelSection(BaseModel):
    type: Optional[str] = None
    customer: Optional[str] = None
    payer: Optional[str] = None
    revenue_source: Optional[str] = None
    pricing: Optional[str] = None
    costs: Optional[str] = None
    go_to_market: Optional[str] = None

class TractionSection(BaseModel):
    interviews: Optional[int] = None
    interested: Optional[int] = None
    users: Optional[int] = None
    revenue: Optional[float] = None
    partnerships: Optional[str] = None
    notes: Optional[str] = None

class AssumptionItem(BaseModel):
    id: str
    text: str
    status: Literal["unvalidated", "validated", "invalidated"] = "unvalidated"
    source: Literal["founder", "ai"] = "founder"

class RiskItem(BaseModel):
    id: str
    text: str
    severity: Literal["low", "med", "high"] = "med"
    source: Literal["founder", "ai"] = "ai"

class GapItem(BaseModel):
    id: str
    topic: TopicType
    text: str
    severity: int = Field(1, ge=1, le=5)
    status: Literal["open", "resolved"] = "open"
    raised_by: Literal["idea_analysis", "critique", "investor"] = "idea_analysis"

class StartupProfile(BaseModel):
    schema_version: int = 1
    identity: IdentitySection = Field(default_factory=IdentitySection)
    problem: ProblemSection = Field(default_factory=ProblemSection)
    customer: CustomerSection = Field(default_factory=CustomerSection)
    solution: SolutionSection = Field(default_factory=SolutionSection)
    value_proposition: ValuePropositionSection = Field(default_factory=ValuePropositionSection)
    market: MarketSection = Field(default_factory=MarketSection)
    competitor_summary: List[CompetitorRef] = Field(default_factory=list)
    business_model: BusinessModelSection = Field(default_factory=BusinessModelSection)
    traction: TractionSection = Field(default_factory=TractionSection)
    team: Optional[str] = None
    funding_ask: Optional[str] = None
    assumptions: List[AssumptionItem] = Field(default_factory=list)
    risks: List[RiskItem] = Field(default_factory=list)
    gaps: List[GapItem] = Field(default_factory=list)
    provenance: Dict[str, ProvenanceType] = Field(default_factory=dict)

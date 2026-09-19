from typing import Any, Literal
from pydantic import BaseModel, Field

class Identity(BaseModel):
    startup_name: str
    raw_idea: str
    one_liner: str | None = None

class Problem(BaseModel):
    statement: str | None = None
    pain_points: list[str] = Field(default_factory=list)

class Customer(BaseModel):
    primary_segment: str | None = None
    persona: str | None = None
    segments: list[str] = Field(default_factory=list)

class Solution(BaseModel):
    description: str | None = None
    key_features: list[str] = Field(default_factory=list)

class ValueProposition(BaseModel):
    one_line: str | None = None
    elevator: str | None = None
    differentiation: str | None = None
    advantage: str | None = None

class MarketSizeInputs(BaseModel):
    customers: str | None = None
    price: str | None = None
    frequency: str | None = None

class Market(BaseModel):
    summary: str | None = None
    size_inputs: MarketSizeInputs = Field(default_factory=MarketSizeInputs)

class CompetitorSummaryItem(BaseModel):
    name: str
    competitor_id: str | None = None

class BusinessModel(BaseModel):
    type: str | None = None
    customer: str | None = None
    payer: str | None = None
    revenue_source: str | None = None
    pricing: str | None = None
    costs: str | None = None
    go_to_market: str | None = None

class Traction(BaseModel):
    interviews: str | None = None
    interested: str | None = None
    users: str | None = None
    revenue: str | None = None
    partnerships: str | None = None
    notes: str | None = None

class Assumption(BaseModel):
    id: str
    text: str
    status: Literal["unvalidated", "validated", "invalidated"]
    source: Literal["founder", "ai"]

class Risk(BaseModel):
    id: str
    text: str
    severity: Literal["low", "med", "high"]
    source: Literal["founder", "ai"]

class Gap(BaseModel):
    id: str
    topic: Literal["problem", "market", "differentiation", "business_model", "validation"]
    text: str
    severity: int
    status: Literal["open", "resolved"]
    raised_by: Literal["idea_analysis", "critique", "investor"]

class Profile(BaseModel):
    schema_version: int = 1
    identity: Identity
    problem: Problem = Field(default_factory=Problem)
    customer: Customer = Field(default_factory=Customer)
    solution: Solution = Field(default_factory=Solution)
    value_proposition: ValueProposition = Field(default_factory=ValueProposition)
    market: Market = Field(default_factory=Market)
    competitor_summary: list[CompetitorSummaryItem] = Field(default_factory=list)
    business_model: BusinessModel = Field(default_factory=BusinessModel)
    traction: Traction = Field(default_factory=Traction)
    team: Any | None = None
    funding_ask: Any | None = None
    assumptions: list[Assumption] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    gaps: list[Gap] = Field(default_factory=list)
    provenance: dict[str, Literal["founder", "source_backed", "calculated", "ai_analysis"]] = Field(default_factory=dict)

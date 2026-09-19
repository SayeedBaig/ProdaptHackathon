from typing import Any, Literal
from pydantic import BaseModel, Field

class IdeaAnalysis(BaseModel):
    problem: str
    target_customer: str
    solution: str
    pain_points: list[str]
    assumptions: list[str]
    risks: list[str]
    missing_information: list[str]
    first_question: dict[str, Any]

class ClarificationQuestion(BaseModel):
    id: str
    text: str
    target_field: str

class ProfilePatchOp(BaseModel):
    op: Literal["set", "add", "remove"]
    path: str
    value: Any
    reason: str

class ProfilePatch(BaseModel):
    ops: list[ProfilePatchOp]

class Claim(BaseModel):
    text: str
    provenance: Literal["source_backed", "founder_assumption", "calculated", "ai_analysis"]
    evidence_ids: list[str] = Field(default_factory=list)
    supporting_quote: str | None = None

class SlideContent(BaseModel):
    key: Literal[
        "problem", "solution", "product", "target_market", "market_opportunity",
        "competition", "advantage", "business_model", "gtm", "traction", "team", "ask"
    ]
    title: str
    bullets: list[Claim | str]
    status: Literal["complete", "needs_input"]

class ValueProposition(BaseModel):
    pass # To be defined fully by M2

class CompetitorAnalysis(BaseModel):
    pass # To be defined fully by M2

class MarketAnalysis(BaseModel):
    pass # To be defined fully by M2

class BusinessModelAnalysis(BaseModel):
    pass # To be defined fully by M2

class Pitch(BaseModel):
    slides: list[SlideContent]

class PitchCritique(BaseModel):
    issues: list[dict[str, Any]]
    investor_objections: list[str]
    top_priorities: list[str]

class InvestorQuestion(BaseModel):
    id: str
    text: str
    intent: str
    topic: str

class AnswerEvaluation(BaseModel):
    scores: dict[Literal["clarity", "specificity", "evidence", "business_reasoning", "differentiation", "scalability"], int]
    explanation: str
    strengths: list[str]
    weaknesses: list[str]
    recommended_improvement: str
    weakest_criterion: str
    claims_made: list[str]
    follow_up_question: str | None

class ReadinessNarrative(BaseModel):
    pass # To be defined fully by M2

class FeedbackItemDraft(BaseModel):
    pass # To be defined fully by M2

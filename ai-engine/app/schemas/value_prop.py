from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.schemas.common import StartupIdeaInput

class GeoffMooreTemplate(BaseModel):
    target_customer: str = Field(..., description="FOR (target customer)", example="Early-stage startup founders")
    statement_of_need: str = Field(..., description="WHO (statement of need/opportunity)", example="struggling to articulate their business vision and prepare for investor meetings")
    product_name: str = Field(..., description="THE (product name)", example="PitchCoach AI")
    product_category: str = Field(..., description="IS A (product category)", example="AI-powered pitch coach and deck generator")
    key_benefit: str = Field(..., description="THAT (key benefit / compelling reason to buy)", example="transforms raw ideas into investor-grade pitch decks and provides real-time Q&A critique")
    primary_competitor: str = Field(..., description="UNLIKE (primary competitive alternative)", example="generic presentation templates or expensive pitch consultants")
    our_differentiation: str = Field(..., description="OUR PRODUCT (statement of primary differentiation)", example="combines structured VC-evaluated frameworks with instant AI feedback and market scoring.")

class PainReliefItem(BaseModel):
    customer_pain: str = Field(..., description="Customer pain point", example="Uncertainty about what hard questions VCs will ask")
    product_feature: str = Field(..., description="Startup solution feature", example="AI Investor Q&A Simulator")
    relief_value: str = Field(..., description="Value generated", example="Boosts founder confidence and eliminates surprise questions during pitches")

class ValuePropRequest(BaseModel):
    startup_info: StartupIdeaInput
    clarification_answers: Optional[Dict[str, str]] = None

class ValuePropositionResponse(BaseModel):
    headline: str = Field(..., description="Catchy primary value proposition headline", example="Turn Raw Ideas into VC-Ready Pitches in Minutes")
    subheadline: str = Field(..., description="Supporting explanation statement", example="The AI startup coach that structures your deck, benchmarks your market, and trains you to pass investor grillings.")
    geoff_moore_template: GeoffMooreTemplate
    elevator_pitch_30s: str = Field(..., description="30-second elevator pitch script")
    unique_selling_points: List[str] = Field(..., description="List of top USPs")
    pain_relief_matrix: List[PainReliefItem] = Field(..., description="Customer Pain vs Feature Relief Matrix")

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class GeoffMooreTemplate(BaseModel):
    target_customer: str
    statement_of_need: str
    product_name: str
    product_category: str
    key_benefit: str
    primary_competitor: str
    our_differentiation: str

class PainReliefItem(BaseModel):
    customer_pain: str
    product_feature: str
    relief_value: str

class ValueProposition(BaseModel):
    headline: str = Field(..., description="Catchy value proposition headline")
    subheadline: str = Field(..., description="Supporting subheadline")
    geoff_moore_template: GeoffMooreTemplate
    elevator_pitch_30s: str = Field(..., description="30-second elevator pitch script")
    unique_selling_points: List[str] = Field(..., description="Key USPs")
    pain_relief_matrix: List[PainReliefItem] = Field(default_factory=list)

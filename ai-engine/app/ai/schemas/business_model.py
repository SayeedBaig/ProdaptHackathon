from pydantic import BaseModel, Field
from typing import List, Optional

class BusinessModelAnalysis(BaseModel):
    revenue_type: str = Field(..., description="Monetization model (e.g., Freemium SaaS, B2B Licensing)")
    customer_segment: str = Field(..., description="Primary user segment")
    payer_segment: str = Field(..., description="Entity paying for the product")
    revenue_streams: List[str] = Field(default_factory=list, description="List of monetization sources")
    pricing_structure: Optional[str] = Field(None, description="Pricing tiers or unit rates")
    cost_drivers: List[str] = Field(default_factory=list, description="Primary cost categories")
    go_to_market_strategy: str = Field(..., description="GTM channel strategy")
    missing_assumptions: List[str] = Field(default_factory=list, description="Unverified unit economics or pricing gaps")

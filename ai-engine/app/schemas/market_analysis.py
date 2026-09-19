from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.common import StartupIdeaInput

class MarketMetrics(BaseModel):
    tam: str = Field(..., description="Total Addressable Market", example="$15.4 Billion (Global Pitch & Presentation Software)")
    sam: str = Field(..., description="Serviceable Addressable Market", example="$2.1 Billion (Startup Founder Software Tools)")
    som: str = Field(..., description="Serviceable Obtainable Market (Target Year 1-3)", example="$85 Million (Early-stage Tech Founders in NA/EU)")
    cagr: str = Field(..., description="Compound Annual Growth Rate", example="18.5% (2024 - 2030)")

class Competitor(BaseModel):
    name: str = Field(..., example="Slidebean / Pitch.com")
    type: str = Field(..., description="Direct or Indirect", example="Direct")
    strengths: str = Field(..., example="Great visual templates, established brand.")
    weaknesses: str = Field(..., example="Lack deep AI investor Q&A practice and readiness scoring.")
    differentiation_angle: str = Field(..., example="We provide interactive AI coaching, market benchmarking, and pitch defense evaluation.")

class MarketAnalysisRequest(BaseModel):
    startup_info: StartupIdeaInput

class MarketAnalysisResponse(BaseModel):
    industry: str = Field(..., example="B2B SaaS / Productivity Software")
    market_metrics: MarketMetrics
    competitor_matrix: List[Competitor]
    key_market_trends: List[str] = Field(..., description="Macro trends supporting this startup")
    barriers_to_entry: List[str] = Field(..., description="Potential barriers to entry")
    growth_drivers: List[str] = Field(..., description="Main drivers fueling growth in this sector")

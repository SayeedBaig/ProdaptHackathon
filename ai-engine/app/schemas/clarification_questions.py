from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.common import StartupIdeaInput

class ClarificationQuestion(BaseModel):
    id: str = Field(..., example="Q1")
    category: str = Field(..., description="Product, Market, Monetization, Traction, or Defensibility", example="Monetization")
    question: str = Field(..., description="Targeted follow-up question to clarify missing startup details", example="What is your planned pricing model (e.g. per-deck subscription, pay-per-pitch, or enterprise licenses)?")
    rationale: str = Field(..., description="Why this information is critical for investors", example="Investors need to evaluate unit economics and revenue scalability.")
    sample_answer_hint: str = Field(..., description="Example of a strong answer", example="Freemium model: free deck outline, $29/mo founder tier, $199 one-time pitch clinic.")

class ClarificationQuestionsRequest(BaseModel):
    startup_info: StartupIdeaInput

class ClarificationQuestionsResponse(BaseModel):
    questions: List[ClarificationQuestion]
    guidance_notes: str = Field(..., description="General advice on answering these clarification questions effectively")

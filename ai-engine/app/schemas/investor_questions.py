from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.common import StartupIdeaInput

class InvestorQuestion(BaseModel):
    id: str = Field(..., example="IQ1")
    category: str = Field(..., description="Financial, Technical, Market, Team, Execution", example="Financial")
    question: str = Field(..., description="Challenging question an investor will likely ask")
    difficulty: str = Field(..., description="Medium, Hard, Brutal", example="Brutal")
    investor_intent: str = Field(..., description="What the investor is secretly probing for")
    key_points_to_include: List[str] = Field(..., description="Key elements required in a strong answer")

class InvestorQuestionsRequest(BaseModel):
    startup_info: StartupIdeaInput
    focus_category: Optional[str] = Field(None, description="Optional category filter")

class InvestorQuestionsResponse(BaseModel):
    questions: List[InvestorQuestion]
    preparation_advice: str = Field(..., description="Strategic guidelines for pitch defense")

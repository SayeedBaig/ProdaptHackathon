from pydantic import BaseModel, Field
from typing import List, Optional

class AnswerEvaluationRequest(BaseModel):
    question: str = Field(..., description="The investor question asked", example="What is your customer acquisition cost (CAC) and how will you lower it?")
    category: Optional[str] = Field("Financial", description="Question category", example="Financial")
    user_answer: str = Field(..., description="The founder's raw answer", example="We don't know CAC yet because we are in early beta, but we will run ads.")

class AnswerEvaluationResponse(BaseModel):
    clarity_score: float = Field(..., ge=0.0, le=100.0)
    persuasiveness_score: float = Field(..., ge=0.0, le=100.0)
    completeness_score: float = Field(..., ge=0.0, le=100.0)
    overall_answer_score: float = Field(..., ge=0.0, le=100.0, description="Overall answer grade (0-100)")
    strengths: List[str] = Field(..., description="Good points mentioned in the user's answer")
    weaknesses: List[str] = Field(..., description="Flaws or missing data points in the answer")
    missing_key_points: List[str] = Field(..., description="Critical facts or frameworks omitted")
    improved_answer: str = Field(..., description="Optimized, benchmark investor response for the founder to practice")

from pydantic import BaseModel, Field
from typing import Optional, Literal
from app.ai.schemas.common import TopicType

class InvestorQuestion(BaseModel):
    seq: int = 1
    topic: TopicType = "differentiation"
    intent: Literal["opening", "follow_up", "new_topic"] = "opening"
    question: str = Field(..., description="The investor question text")
    difficulty: Literal["Medium", "Hard", "Brutal"] = "Hard"
    investor_intent: Optional[str] = Field(None, description="Secret intent behind the question")

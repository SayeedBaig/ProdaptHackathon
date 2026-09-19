from pydantic import BaseModel, Field
from typing import List, Optional
from app.ai.schemas.common import TopicType
from app.ai.schemas.clarification import ProfilePatch

class FeedbackItemDraft(BaseModel):
    id: str = "f1"
    topic: TopicType = "validation"
    title: str = Field(..., description="Action title (e.g. Validate willingness to pay)")
    recommendation: str = Field(..., description="Actionable steps for the founder")
    suggested_patch: Optional[ProfilePatch] = None
    status: str = "open"

class FeedbackDraftList(BaseModel):
    items: List[FeedbackItemDraft] = Field(default_factory=list)

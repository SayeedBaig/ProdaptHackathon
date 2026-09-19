import uuid
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_owned_startup
from app.core.errors import NotFoundError
from app.db.session import get_db
from app.models.user import User
from app.repositories.readiness_repo import ReadinessRepo
from app.schemas.common import DataEnvelope, Meta
from app.schemas.readiness import ResolveFeedbackRequest
from app.services.feedback_service import FeedbackService

router = APIRouter(prefix="/feedback", tags=["Feedback Resolution"])

@router.post("/{fid}/resolve", response_model=DataEnvelope[dict[str, Any]])
def resolve_feedback(
    fid: uuid.UUID,
    req: ResolveFeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = ReadinessRepo.get_feedback_item(db, fid)
    if not item:
        raise NotFoundError(f"Feedback item {fid} not found")

    startup = get_owned_startup(item.startup_id, current_user, db)

    new_pv, applied_ops = FeedbackService.resolve_feedback(
        db=db,
        startup=startup,
        feedback_id=fid,
        action=req.action,
        founder_input=req.founder_input,
    )

    data: dict[str, Any] = {
        "status": "dismissed" if req.action == "dismiss" else "accepted",
        "profile_version": new_pv.version if new_pv else None,
        "profile_diff": applied_ops,
    }

    return DataEnvelope(
        data=data,
        meta=Meta(profile_version=new_pv.version if new_pv else None),
    )

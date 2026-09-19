from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_owned_startup
from app.core.errors import NotFoundError
from app.db.session import get_db
from app.models.startup import Startup
from app.repositories.profile_repo import ProfileRepo
from app.repositories.readiness_repo import ReadinessRepo
from app.schemas.common import DataEnvelope, Meta
from app.schemas.readiness import FeedbackItemResponse, ReadinessReportResponse
from app.services.ai_service import MockAIService, get_ai_service
from app.services.readiness_service import ReadinessService

router = APIRouter(prefix="/startups", tags=["Readiness Report"])

@router.get("/{startup_id}/readiness", response_model=DataEnvelope[ReadinessReportResponse])
async def get_readiness_report(
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    report = ReadinessRepo.get_latest_report(db, startup.id)
    if not report:
        # Generate baseline readiness report if not generated yet
        report = await ReadinessService.build_report(
            db=db,
            startup=startup,
            session_id=None,
            ai_service=ai_service,
        )

    feedback_items = ReadinessRepo.list_feedback(db, startup.id, status="open")
    resp = ReadinessReportResponse(
        id=report.id,
        startup_id=report.startup_id,
        session_id=report.session_id,
        profile_version=report.profile_version,
        overall=report.overall,
        dimensions=report.dimension_scores or {},
        narrative=report.narrative or {},
        feedback_items=[FeedbackItemResponse.model_validate(f) for f in feedback_items],
        created_at=report.created_at,
    )
    return DataEnvelope(data=resp, meta=Meta(profile_version=report.profile_version))

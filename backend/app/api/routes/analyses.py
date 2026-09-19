from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_owned_startup
from app.core.errors import NotFoundError
from app.db.session import get_db
from app.models.startup import Startup
from app.schemas.analyses import AnalysisResponse
from app.schemas.common import DataEnvelope, Meta
from app.services.ai_service import MockAIService, get_ai_service
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/startups", tags=["Analyses"])

@router.post("/{startup_id}/analyses/{kind}", response_model=DataEnvelope[AnalysisResponse])
async def generate_startup_analysis(
    kind: str,
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    analysis, is_stale = await AnalysisService.generate_analysis(
        db=db,
        startup=startup,
        kind=kind,
        ai_service=ai_service,
    )
    resp = AnalysisResponse(
        id=analysis.id,
        startup_id=analysis.startup_id,
        kind=analysis.kind,
        profile_version=analysis.profile_version,
        output=analysis.output,
        stale=is_stale,
        ai_mode=analysis.ai_mode,
        model=analysis.model,
        created_at=analysis.created_at,
    )
    return DataEnvelope(data=resp, meta=Meta(profile_version=analysis.profile_version))

@router.get("/{startup_id}/analyses/{kind}/latest", response_model=DataEnvelope[AnalysisResponse])
def get_latest_analysis(
    kind: str,
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
):
    analysis, is_stale = AnalysisService.get_latest_analysis(db=db, startup=startup, kind=kind)
    if not analysis:
        raise NotFoundError(f"No {kind} analysis found for startup")

    resp = AnalysisResponse(
        id=analysis.id,
        startup_id=analysis.startup_id,
        kind=analysis.kind,
        profile_version=analysis.profile_version,
        output=analysis.output,
        stale=is_stale,
        ai_mode=analysis.ai_mode,
        model=analysis.model,
        created_at=analysis.created_at,
    )
    return DataEnvelope(data=resp, meta=Meta(profile_version=analysis.profile_version))

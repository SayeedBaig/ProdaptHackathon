import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_owned_startup
from app.core.errors import NotFoundError
from app.db.session import get_db
from app.models.startup import Startup
from app.repositories.pitch_repo import PitchRepo
from app.repositories.profile_repo import ProfileRepo
from app.schemas.common import DataEnvelope, Meta
from app.schemas.pitch import CritiqueResponse, GeneratePitchRequest, PitchResponse
from app.services.ai_service import MockAIService, get_ai_service
from app.services.pitch_service import PitchService

router = APIRouter(prefix="/startups", tags=["Pitch Deck"])

@router.post("/{startup_id}/pitch/generate", response_model=DataEnvelope[PitchResponse])
async def generate_pitch_deck(
    req: GeneratePitchRequest = GeneratePitchRequest(),
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    pitch = await PitchService.generate_pitch(
        db=db,
        startup=startup,
        improve_from_pitch_id=req.improve_from_pitch_id,
        ai_service=ai_service,
    )
    resp = PitchResponse(
        id=pitch.id,
        startup_id=pitch.startup_id,
        version=pitch.version,
        profile_version=pitch.profile_version,
        slides=pitch.slides,
        parent_pitch_id=pitch.parent_pitch_id,
        stale=False,
        ai_mode=pitch.ai_mode,
        created_at=pitch.created_at,
    )
    return DataEnvelope(data=resp, meta=Meta(profile_version=pitch.profile_version))

@router.get("/{startup_id}/pitch", response_model=DataEnvelope[PitchResponse])
def get_pitch_deck(
    version: int | None = Query(default=None),
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
):
    if version:
        pitch = PitchRepo.get_pitch_by_version(db, startup.id, version)
    else:
        pitch = PitchRepo.get_latest_pitch(db, startup.id)

    if not pitch:
        raise NotFoundError("No pitch deck found for startup")

    pv = ProfileRepo.get_latest_version(db, startup.id)
    is_stale = pv and pitch.profile_version < pv.version

    resp = PitchResponse(
        id=pitch.id,
        startup_id=pitch.startup_id,
        version=pitch.version,
        profile_version=pitch.profile_version,
        slides=pitch.slides,
        parent_pitch_id=pitch.parent_pitch_id,
        stale=bool(is_stale),
        ai_mode=pitch.ai_mode,
        created_at=pitch.created_at,
    )
    return DataEnvelope(data=resp, meta=Meta(profile_version=pitch.profile_version))

@router.post("/{startup_id}/pitch/{pitch_id}/critique", response_model=DataEnvelope[CritiqueResponse])
async def critique_pitch_deck(
    pitch_id: uuid.UUID,
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    critique = await PitchService.critique_pitch(
        db=db,
        startup=startup,
        pitch_id=pitch_id,
        ai_service=ai_service,
    )
    resp = CritiqueResponse(
        id=critique.id,
        pitch_version_id=critique.pitch_version_id,
        output=critique.output,
        created_at=critique.created_at,
    )
    return DataEnvelope(data=resp)

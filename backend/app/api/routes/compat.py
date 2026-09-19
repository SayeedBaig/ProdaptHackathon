import uuid
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.core.errors import NotFoundError
from app.db.session import get_db
from app.models.startup import Startup
from app.models.user import User
from app.repositories.pitch_repo import PitchRepo
from app.repositories.profile_repo import ProfileRepo
from app.repositories.startup_repo import StartupRepo
from app.schemas.common import DataEnvelope, Meta
from app.services.ai_service import MockAIService, get_ai_service
from app.services.pitch_service import PitchService
from app.services.profile_service import ProfileService

router = APIRouter(tags=["Frontend Compatibility"])


class StartupScopedRequest(BaseModel):
    startup_id: str


class ProfilePatchRequest(BaseModel):
    ops: list[dict[str, Any]]
    expected_version: int | None = None
    base_version: int | None = None


class ClarificationPatchRequest(StartupScopedRequest):
    question_id: str | None = None
    answer: str
    target_field: str | None = None


class InvestorQuestionRequest(StartupScopedRequest):
    intent: str = "opening"
    topic: str = "differentiation"
    previous_question_id: str | None = None


class EvaluateAnswerRequest(StartupScopedRequest):
    question_id: str | None = None
    answer: str
    topic: str = "differentiation"


def _parse_startup_id(startup_id: str) -> uuid.UUID:
    try:
        return uuid.UUID(startup_id)
    except ValueError:
        raise NotFoundError(f"Startup {startup_id} not found")


def _get_owned_startup_by_id(db: Session, current_user: User, startup_id: str) -> Startup:
    parsed_id = _parse_startup_id(startup_id)
    startup = StartupRepo.get_owned_startup(db, parsed_id, current_user.id)
    if not startup:
        raise NotFoundError(f"Startup {startup_id} not found")
    return startup


def _profile_payload(db: Session, startup: Startup) -> tuple[dict[str, Any], int]:
    pv = ProfileRepo.get_latest_version(db, startup.id)
    if not pv:
        raise NotFoundError("Profile version not found")

    data = dict(pv.data)
    data["schema_version"] = pv.version
    return data, pv.version


def _normalize_patch_ops(ops: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for op in ops:
        next_op = dict(op)
        path = str(next_op.get("path", ""))
        if path.startswith("/"):
            next_op["path"] = path.strip("/").replace("/", ".")
        normalized.append(next_op)
    return normalized


@router.get("/profile/{startup_id}", response_model=DataEnvelope[dict[str, Any]])
def get_profile_compat(
    startup_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    startup = _get_owned_startup_by_id(db, current_user, startup_id)
    data, version = _profile_payload(db, startup)
    return DataEnvelope(data=data, meta=Meta(profile_version=version))


@router.patch("/profile/{startup_id}", response_model=DataEnvelope[dict[str, Any]])
def patch_profile_compat(
    startup_id: str,
    req: ProfilePatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    startup = _get_owned_startup_by_id(db, current_user, startup_id)
    base_version = req.base_version or req.expected_version
    if base_version is None:
        _, base_version = _profile_payload(db, startup)

    new_pv, _ = ProfileService.apply_patch_to_startup(
        db=db,
        startup=startup,
        base_version=base_version,
        ops=_normalize_patch_ops(req.ops),
        change_reason="frontend_compat_patch",
        source="founder",
    )
    data = dict(new_pv.data)
    data["schema_version"] = new_pv.version
    return DataEnvelope(data=data, meta=Meta(profile_version=new_pv.version))


@router.post("/ai/analyze_idea", response_model=DataEnvelope[dict[str, Any]])
async def analyze_idea_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.analyze_idea(profile)
    return DataEnvelope(data=result.model_dump(), meta=Meta(profile_version=version))


@router.post("/ai/generate_clarification_question", response_model=DataEnvelope[dict[str, Any]])
async def generate_clarification_question_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.generate_clarification_question(profile)
    return DataEnvelope(data=result.model_dump(), meta=Meta(profile_version=version))


@router.post("/ai/extract_profile_patch", response_model=DataEnvelope[dict[str, Any]])
async def extract_profile_patch_compat(
    req: ClarificationPatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.extract_profile_patch(
        ctx=profile,
        question=req.question_id or req.target_field or "",
        answer=req.answer,
    )
    return DataEnvelope(data=result.model_dump(), meta=Meta(profile_version=version))


@router.post("/ai/generate_value_proposition", response_model=DataEnvelope[dict[str, Any]])
async def generate_value_proposition_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.generate_value_proposition(profile)
    return DataEnvelope(data=result, meta=Meta(profile_version=version))


@router.post("/ai/analyze_competitors", response_model=DataEnvelope[dict[str, Any]])
async def analyze_competitors_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.analyze_competitors(profile)
    return DataEnvelope(data=result, meta=Meta(profile_version=version))


@router.post("/ai/analyze_market", response_model=DataEnvelope[dict[str, Any]])
async def analyze_market_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.analyze_market(profile)
    return DataEnvelope(data=result, meta=Meta(profile_version=version))


@router.post("/ai/analyze_business_model", response_model=DataEnvelope[dict[str, Any]])
async def analyze_business_model_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.analyze_business_model(profile)
    return DataEnvelope(data=result, meta=Meta(profile_version=version))


@router.post("/ai/generate_pitch", response_model=DataEnvelope[dict[str, Any]])
async def generate_pitch_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    pitch = await PitchService.generate_pitch(db, startup, None, ai_service)
    return DataEnvelope(
        data={"id": str(pitch.id), "slides": pitch.slides},
        meta=Meta(profile_version=pitch.profile_version),
    )


@router.post("/ai/critique_pitch", response_model=DataEnvelope[dict[str, Any]])
async def critique_pitch_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    pitch = PitchRepo.get_latest_pitch(db, startup.id)
    if not pitch:
        pitch = await PitchService.generate_pitch(db, startup, None, ai_service)
    critique = await PitchService.critique_pitch(db, startup, pitch.id, ai_service)
    return DataEnvelope(data=critique.output, meta=Meta())


@router.post("/ai/generate_investor_question", response_model=DataEnvelope[dict[str, Any]])
async def generate_investor_question_compat(
    req: InvestorQuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.generate_investor_question(profile, req.intent, req.topic)
    return DataEnvelope(data=result.model_dump(), meta=Meta(profile_version=version))


@router.post("/ai/evaluate_answer", response_model=DataEnvelope[dict[str, Any]])
async def evaluate_answer_compat(
    req: EvaluateAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.evaluate_answer(
        profile,
        {
            "question_id": req.question_id,
            "answer": req.answer,
            "topic": req.topic,
        },
    )
    return DataEnvelope(data=result.model_dump(), meta=Meta(profile_version=version))


@router.post("/ai/generate_readiness_narrative", response_model=DataEnvelope[dict[str, Any]])
async def generate_readiness_narrative_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.generate_readiness_narrative(profile, [], {})
    return DataEnvelope(data=result, meta=Meta(profile_version=version))


@router.post("/ai/extract_feedback_patches", response_model=DataEnvelope[dict[str, Any]])
async def extract_feedback_patches_compat(
    req: StartupScopedRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    startup = _get_owned_startup_by_id(db, current_user, req.startup_id)
    profile, version = _profile_payload(db, startup)
    result = await ai_service.extract_feedback_patches(profile, {})
    ops = result[0].get("suggested_patch", []) if result else []
    return DataEnvelope(data={"ops": ops}, meta=Meta(profile_version=version))

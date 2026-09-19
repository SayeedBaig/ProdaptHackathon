from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.ai.schemas.capabilities import IdeaAnalysis
from app.core.deps import get_owned_startup
from app.db.session import get_db
from app.models.startup import Startup
from app.repositories.analysis_repo import AnalysisRepo
from app.repositories.clarification_repo import ClarificationRepo
from app.repositories.profile_repo import ProfileRepo
from app.schemas.common import DataEnvelope, Meta
from app.schemas.idea import ClarificationAnswerRequest, ClarificationResponse, ClarificationSkipRequest
from app.services.ai_service import MockAIService, get_ai_service
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/startups", tags=["Idea & Clarification"])

@router.post("/{startup_id}/idea/analyze", response_model=DataEnvelope[IdeaAnalysis])
async def analyze_startup_idea(
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    pv = ProfileRepo.get_latest_version(db, startup.id)
    ctx = pv.data if pv else {"identity": {"startup_name": startup.name, "raw_idea": startup.raw_idea}}

    analysis_res = await ai_service.analyze_idea(ctx)
    output_dict = analysis_res.model_dump()

    # Save to analyses table
    AnalysisRepo.save_analysis(
        db=db,
        startup_id=startup.id,
        kind="idea",
        profile_version=pv.version if pv else 1,
        output=output_dict,
        ai_mode="mock",
        model="gemini-2.0-flash",
    )

    # Record first clarification turn if not already created
    if analysis_res.first_question:
        existing_turn = ClarificationRepo.get_turn(db, startup.id, 1)
        if not existing_turn:
            ClarificationRepo.create_turn(
                db=db,
                startup_id=startup.id,
                seq=1,
                question=analysis_res.first_question.get("text", "Clarification question"),
                target_field=analysis_res.first_question.get("target_field"),
                profile_version_before=pv.version if pv else 1,
            )

    return DataEnvelope(data=analysis_res, meta=Meta(profile_version=pv.version if pv else 1))

@router.post("/{startup_id}/clarify/answer", response_model=DataEnvelope[ClarificationResponse])
async def answer_clarification(
    req: ClarificationAnswerRequest,
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    pv = ProfileRepo.get_latest_version(db, startup.id)
    profile_data = pv.data if pv else {}

    # 1. Extract patch via AI
    patch_result = await ai_service.extract_profile_patch(
        ctx=profile_data,
        question=req.question_id,
        answer=req.answer,
    )
    ops_dicts = [op.model_dump() for op in patch_result.ops]

    # 2. Apply patch to profile (handles base_version conflict check)
    new_pv, applied_ops = ProfileService.apply_patch_to_startup(
        db=db,
        startup=startup,
        base_version=req.base_version,
        ops=ops_dicts,
        change_reason="clarification",
        source="founder",
    )

    # 3. Update clarification turn in DB
    latest_turn = ClarificationRepo.get_latest_turn(db, startup.id)
    if latest_turn:
        ClarificationRepo.answer_turn(
            db=db,
            turn=latest_turn,
            answer=req.answer,
            profile_version_after=new_pv.version,
        )

    # 4. Generate next question
    next_question = await ai_service.generate_clarification_question(new_pv.data)
    next_seq = (latest_turn.seq + 1) if latest_turn else 1
    ClarificationRepo.create_turn(
        db=db,
        startup_id=startup.id,
        seq=next_seq,
        question=next_question.text,
        target_field=next_question.target_field,
        profile_version_before=new_pv.version,
    )

    ready = (new_pv.completeness_pct or 0) >= 60

    resp = ClarificationResponse(
        profile_diff=patch_result.ops,
        profile_version=new_pv.version,
        next_question=next_question,
        ready_for_next_step=ready,
        completeness_pct=new_pv.completeness_pct or 0,
    )
    return DataEnvelope(data=resp, meta=Meta(profile_version=new_pv.version))

@router.post("/{startup_id}/clarify/skip", response_model=DataEnvelope[ClarificationResponse])
async def skip_clarification(
    req: ClarificationSkipRequest,
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    pv = ProfileRepo.get_latest_version(db, startup.id)
    version = pv.version if pv else 1
    next_question = await ai_service.generate_clarification_question(pv.data if pv else {})

    latest_turn = ClarificationRepo.get_latest_turn(db, startup.id)
    next_seq = (latest_turn.seq + 1) if latest_turn else 1
    ClarificationRepo.create_turn(
        db=db,
        startup_id=startup.id,
        seq=next_seq,
        question=next_question.text,
        target_field=next_question.target_field,
        profile_version_before=version,
    )

    resp = ClarificationResponse(
        profile_diff=[],
        profile_version=version,
        next_question=next_question,
        ready_for_next_step=(pv.completeness_pct or 0) >= 60 if pv else False,
        completeness_pct=pv.completeness_pct if pv else 0,
    )
    return DataEnvelope(data=resp, meta=Meta(profile_version=version))

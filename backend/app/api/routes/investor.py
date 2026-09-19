import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_owned_startup
from app.core.errors import NotFoundError
from app.db.session import get_db
from app.models.startup import Startup
from app.models.user import User
from app.repositories.investor_repo import InvestorRepo
from app.schemas.common import DataEnvelope
from app.schemas.investor import (
    InvestorAnswerResponse,
    InvestorSessionResponse,
    InvestorTurnResponse,
    StartInvestorSessionRequest,
    SubmitInvestorAnswerRequest,
)
from app.services.ai_service import MockAIService, get_ai_service
from app.services.investor_service import InvestorService
from app.services.readiness_service import ReadinessService

router = APIRouter(tags=["Investor Simulator"])

@router.post("/startups/{startup_id}/investor/sessions", response_model=DataEnvelope[InvestorSessionResponse], status_code=status.HTTP_201_CREATED)
async def start_investor_session(
    req: StartInvestorSessionRequest = StartInvestorSessionRequest(),
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    session, first_turn = await InvestorService.start_session(
        db=db,
        startup=startup,
        pitch_version_id=req.pitch_version_id,
        max_turns=req.max_turns,
        ai_service=ai_service,
    )
    turn_resp = InvestorTurnResponse.model_validate(first_turn)
    resp = InvestorSessionResponse(
        id=session.id,
        startup_id=session.startup_id,
        pitch_version_id=session.pitch_version_id,
        status=session.status,
        max_turns=session.max_turns,
        turns=[turn_resp],
        current_turn=turn_resp,
        completed=False,
        started_at=session.started_at,
        completed_at=session.completed_at,
    )
    return DataEnvelope(data=resp)

@router.post("/investor/sessions/{sid}/answer", response_model=DataEnvelope[InvestorAnswerResponse])
async def submit_investor_answer(
    sid: uuid.UUID,
    req: SubmitInvestorAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    session = InvestorRepo.get_session(db, sid)
    if not session:
        raise NotFoundError(f"Session {sid} not found")

    # Ownership check
    startup = get_owned_startup(session.startup_id, current_user, db)

    evaluation, next_turn, completed = await InvestorService.answer_turn(
        db=db,
        session_id=sid,
        turn_seq=req.turn_seq,
        answer=req.answer,
        ai_service=ai_service,
    )

    # If completed, auto-trigger readiness report
    if completed:
        await ReadinessService.build_report(
            db=db,
            startup=startup,
            session_id=session.id,
            ai_service=ai_service,
        )

    next_turn_resp = InvestorTurnResponse.model_validate(next_turn) if next_turn else None
    return DataEnvelope(
        data=InvestorAnswerResponse(
            evaluation=evaluation,
            next_turn=next_turn_resp,
            completed=completed,
        )
    )

@router.post("/investor/sessions/{sid}/finish", response_model=DataEnvelope[InvestorSessionResponse])
async def finish_investor_session(
    sid: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: MockAIService = Depends(get_ai_service),
):
    session = InvestorRepo.get_session(db, sid)
    if not session:
        raise NotFoundError(f"Session {sid} not found")

    startup = get_owned_startup(session.startup_id, current_user, db)
    completed_session = InvestorService.finish_session(db, sid)

    await ReadinessService.build_report(
        db=db,
        startup=startup,
        session_id=completed_session.id,
        ai_service=ai_service,
    )

    turns = InvestorRepo.list_turns(db, sid)
    resp = InvestorSessionResponse(
        id=completed_session.id,
        startup_id=completed_session.startup_id,
        pitch_version_id=completed_session.pitch_version_id,
        status=completed_session.status,
        max_turns=completed_session.max_turns,
        turns=[InvestorTurnResponse.model_validate(t) for t in turns],
        current_turn=None,
        completed=True,
        started_at=completed_session.started_at,
        completed_at=completed_session.completed_at,
    )
    return DataEnvelope(data=resp)

@router.get("/investor/sessions/{sid}", response_model=DataEnvelope[InvestorSessionResponse])
def get_investor_session(
    sid: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = InvestorRepo.get_session(db, sid)
    if not session:
        raise NotFoundError(f"Session {sid} not found")

    # Ownership check
    get_owned_startup(session.startup_id, current_user, db)

    turns = InvestorRepo.list_turns(db, sid)
    turns_resp = [InvestorTurnResponse.model_validate(t) for t in turns]
    current = next((t for t in turns_resp if t.answer is None), None)

    resp = InvestorSessionResponse(
        id=session.id,
        startup_id=session.startup_id,
        pitch_version_id=session.pitch_version_id,
        status=session.status,
        max_turns=session.max_turns,
        turns=turns_resp,
        current_turn=current,
        completed=session.status == "completed",
        started_at=session.started_at,
        completed_at=session.completed_at,
    )
    return DataEnvelope(data=resp)

@router.get("/startups/{startup_id}/investor/sessions", response_model=DataEnvelope[list[InvestorSessionResponse]])
def list_startup_investor_sessions(
    startup: Startup = Depends(get_owned_startup),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    sessions = InvestorRepo.list_sessions(db, startup.id, skip=skip, limit=page_size)
    items = []
    for s in sessions:
        turns = InvestorRepo.list_turns(db, s.id)
        items.append(
            InvestorSessionResponse(
                id=s.id,
                startup_id=s.startup_id,
                pitch_version_id=s.pitch_version_id,
                status=s.status,
                max_turns=s.max_turns,
                turns=[InvestorTurnResponse.model_validate(t) for t in turns],
                completed=s.status == "completed",
                started_at=s.started_at,
                completed_at=s.completed_at,
            )
        )
    return DataEnvelope(data=items)

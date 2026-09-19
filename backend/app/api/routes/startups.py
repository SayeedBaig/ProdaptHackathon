import uuid
from typing import Any
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_owned_startup
from app.db.session import get_db
from app.models.startup import Startup
from app.models.user import User
from app.repositories.profile_repo import ProfileRepo
from app.repositories.startup_repo import StartupRepo
from app.schemas.common import DataEnvelope, Meta
from app.schemas.startup import (
    CreateStartupRequest,
    ProfileVersionItem,
    StartupListItem,
    StartupListResponse,
    StartupResponse,
    UpdateProfileRequest,
    UpdateStartupRequest,
)
from app.services.profile_service import ProfileService
from app.services.startup_service import StartupService

router = APIRouter(prefix="/startups", tags=["Startups"])

@router.post("", response_model=DataEnvelope[StartupResponse], status_code=status.HTTP_201_CREATED)
def create_startup(
    req: CreateStartupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    startup, profile_data, version = StartupService.create_startup(
        db=db,
        user_id=current_user.id,
        name=req.name,
        raw_idea=req.raw_idea,
    )
    progress = StartupService.compute_progress(db, startup.id, version)

    resp = StartupResponse(
        id=startup.id,
        user_id=startup.user_id,
        name=startup.name,
        raw_idea=startup.raw_idea,
        current_version_id=startup.current_version_id,
        profile_version=version,
        profile=profile_data,
        progress=progress,
        status=startup.status,
        created_at=startup.created_at,
        updated_at=startup.updated_at,
    )
    return DataEnvelope(data=resp, meta=Meta(profile_version=version))

@router.get("", response_model=DataEnvelope[StartupListResponse])
def list_startups(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * page_size
    items = StartupRepo.list_by_user(db, current_user.id, skip=skip, limit=page_size)
    total = StartupRepo.count_by_user(db, current_user.id)

    list_items = []
    for s in items:
        pv = ProfileRepo.get_latest_version(db, s.id)
        list_items.append(
            StartupListItem(
                id=s.id,
                name=s.name,
                raw_idea=s.raw_idea,
                profile_version=pv.version if pv else 1,
                status=s.status,
                created_at=s.created_at,
                updated_at=s.updated_at,
            )
        )

    return DataEnvelope(
        data=StartupListResponse(
            items=list_items,
            total=total,
            page=page,
            page_size=page_size,
        )
    )

@router.get("/{startup_id}", response_model=DataEnvelope[StartupResponse])
def get_startup(
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
):
    pv = ProfileRepo.get_latest_version(db, startup.id)
    version = pv.version if pv else 1
    profile_data = pv.data if pv else {}
    progress = StartupService.compute_progress(db, startup.id, version)

    resp = StartupResponse(
        id=startup.id,
        user_id=startup.user_id,
        name=startup.name,
        raw_idea=startup.raw_idea,
        current_version_id=startup.current_version_id,
        profile_version=version,
        profile=profile_data,
        progress=progress,
        status=startup.status,
        created_at=startup.created_at,
        updated_at=startup.updated_at,
    )
    return DataEnvelope(data=resp, meta=Meta(profile_version=version))

@router.patch("/{startup_id}/profile", response_model=DataEnvelope[dict[str, Any]])
def update_profile(
    req: UpdateProfileRequest,
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
):
    ops_dicts = [op.model_dump() for op in req.ops]
    new_pv, applied = ProfileService.apply_patch_to_startup(
        db=db,
        startup=startup,
        base_version=req.base_version,
        ops=ops_dicts,
        change_reason="founder_edit",
        source="founder",
    )
    return DataEnvelope(
        data={
            "profile_version": new_pv.version,
            "profile_diff": applied,
            "completeness_pct": new_pv.completeness_pct,
        },
        meta=Meta(profile_version=new_pv.version),
    )

@router.get("/{startup_id}/profile/versions", response_model=DataEnvelope[list[ProfileVersionItem]])
def list_profile_versions(
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
):
    versions = ProfileRepo.list_versions(db, startup.id)
    items = [ProfileVersionItem.model_validate(v) for v in versions]
    return DataEnvelope(data=items)

@router.put("/{startup_id}", response_model=DataEnvelope[StartupResponse])
def update_startup_details(
    req: UpdateStartupRequest,
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
):
    StartupRepo.update(db, startup, **req.model_dump(exclude_unset=True))
    pv = ProfileRepo.get_latest_version(db, startup.id)
    version = pv.version if pv else 1
    progress = StartupService.compute_progress(db, startup.id, version)

    resp = StartupResponse(
        id=startup.id,
        user_id=startup.user_id,
        name=startup.name,
        raw_idea=startup.raw_idea,
        current_version_id=startup.current_version_id,
        profile_version=version,
        profile=pv.data if pv else {},
        progress=progress,
        status=startup.status,
        created_at=startup.created_at,
        updated_at=startup.updated_at,
    )
    return DataEnvelope(data=resp)

@router.delete("/{startup_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_startup(
    startup: Startup = Depends(get_owned_startup),
    db: Session = Depends(get_db),
):
    StartupRepo.delete(db, startup)
    return None

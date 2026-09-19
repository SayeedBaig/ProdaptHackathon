import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.models.startup import Startup
from app.repositories.startup_repo import StartupRepo
from app.repositories.profile_repo import ProfileRepo
from app.repositories.analysis_repo import AnalysisRepo
from app.repositories.pitch_repo import PitchRepo
from app.repositories.investor_repo import InvestorRepo
from app.repositories.readiness_repo import ReadinessRepo
from app.services.profile_service import ProfileService
from app.schemas.startup import ProgressResponse, ProgressStep

class StartupService:
    @staticmethod
    def create_startup(db: Session, user_id: uuid.UUID, name: str, raw_idea: str) -> tuple[Startup, dict[str, Any], int]:
        # 1. Create Startup entity
        startup = StartupRepo.create(db=db, user_id=user_id, name=name, raw_idea=raw_idea)
        
        # 2. Generate initial profile v1
        initial_data = ProfileService.create_initial_profile(startup_name=name, raw_idea=raw_idea)
        completeness = ProfileService.compute_completeness(initial_data)
        
        # 3. Save profile version 1
        pv1 = ProfileRepo.create_version(
            db=db,
            startup_id=startup.id,
            version=1,
            data=initial_data,
            patch=[],
            change_reason="initial_creation",
            completeness_pct=completeness,
        )
        
        # 4. Link current_version_id
        StartupRepo.update_current_version(db=db, startup=startup, version_id=pv1.id)
        
        return startup, pv1.data, pv1.version

    @staticmethod
    def compute_progress(db: Session, startup_id: uuid.UUID, current_version: int) -> ProgressResponse:
        steps = []
        
        # 1. Idea
        steps.append(ProgressStep(key="idea", status="done"))
        
        # 2. Clarify
        steps.append(ProgressStep(key="clarify", status="available"))
        
        # 3. Value prop
        vp = AnalysisRepo.get_latest_analysis(db, startup_id, "value_proposition")
        if not vp:
            steps.append(ProgressStep(key="value_prop", status="available"))
        elif vp.profile_version < current_version:
            steps.append(ProgressStep(key="value_prop", status="stale"))
        else:
            steps.append(ProgressStep(key="value_prop", status="done"))
            
        # 4. Market
        mkt = AnalysisRepo.get_latest_analysis(db, startup_id, "market")
        if not mkt:
            steps.append(ProgressStep(key="market", status="available"))
        elif mkt.profile_version < current_version:
            steps.append(ProgressStep(key="market", status="stale"))
        else:
            steps.append(ProgressStep(key="market", status="done"))
            
        # 5. Business model
        bm = AnalysisRepo.get_latest_analysis(db, startup_id, "business_model")
        if not bm:
            steps.append(ProgressStep(key="business_model", status="available"))
        elif bm.profile_version < current_version:
            steps.append(ProgressStep(key="business_model", status="stale"))
        else:
            steps.append(ProgressStep(key="business_model", status="done"))
            
        # 6. Pitch
        pitch = PitchRepo.get_latest_pitch(db, startup_id)
        if not pitch:
            steps.append(ProgressStep(key="pitch", status="available"))
        elif pitch.profile_version < current_version:
            steps.append(ProgressStep(key="pitch", status="stale"))
        else:
            steps.append(ProgressStep(key="pitch", status="done"))
            
        # 7. Critique
        if pitch and pitch.critiques:
            steps.append(ProgressStep(key="critique", status="done"))
        elif pitch:
            steps.append(ProgressStep(key="critique", status="available"))
        else:
            steps.append(ProgressStep(key="critique", status="locked"))
            
        # 8. Investor
        session = InvestorRepo.get_active_session(db, startup_id)
        if session:
            steps.append(ProgressStep(key="investor", status="available"))
        else:
            steps.append(ProgressStep(key="investor", status="available"))
            
        # 9. Readiness
        report = ReadinessRepo.get_latest_report(db, startup_id)
        if not report:
            steps.append(ProgressStep(key="readiness", status="available"))
        elif report.profile_version < current_version:
            steps.append(ProgressStep(key="readiness", status="stale"))
        else:
            steps.append(ProgressStep(key="readiness", status="done"))
            
        return ProgressResponse(steps=steps)

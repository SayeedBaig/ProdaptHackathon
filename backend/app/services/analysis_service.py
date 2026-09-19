from typing import Any
from sqlalchemy.orm import Session
from app.core.errors import AppException
from app.models.analysis import Analysis
from app.models.startup import Startup
from app.repositories.analysis_repo import AnalysisRepo
from app.repositories.profile_repo import ProfileRepo
from app.services.ai_service import MockAIService

class AnalysisService:
    @staticmethod
    async def generate_analysis(
        db: Session,
        startup: Startup,
        kind: str,
        ai_service: MockAIService,
    ) -> tuple[Analysis, bool]:
        if kind not in {"value_proposition", "market", "business_model"}:
            raise AppException(code="VALIDATION_ERROR", message=f"Invalid analysis kind: {kind}", status_code=422)

        pv = ProfileRepo.get_latest_version(db, startup.id)
        if not pv:
            raise AppException(code="NOT_FOUND", message="Profile version not found", status_code=404)

        if kind == "value_proposition":
            raw_output = await ai_service.generate_value_proposition(pv.data)
        elif kind == "market":
            raw_output = await ai_service.analyze_market(pv.data)
        elif kind == "business_model":
            raw_output = await ai_service.analyze_business_model(pv.data)
        else:
            raw_output = {}

        output = raw_output if isinstance(raw_output, dict) else raw_output.model_dump()

        analysis = AnalysisRepo.save_analysis(
            db=db,
            startup_id=startup.id,
            kind=kind,
            profile_version=pv.version,
            output=output,
            ai_mode="mock",
            model="gemini-2.0-flash",
        )
        return analysis, False

    @staticmethod
    def get_latest_analysis(db: Session, startup: Startup, kind: str) -> tuple[Analysis | None, bool]:
        analysis = AnalysisRepo.get_latest_analysis(db, startup.id, kind)
        if not analysis:
            return None, False

        pv = ProfileRepo.get_latest_version(db, startup.id)
        is_stale = False
        if pv and analysis.profile_version < pv.version:
            is_stale = True

        return analysis, is_stale

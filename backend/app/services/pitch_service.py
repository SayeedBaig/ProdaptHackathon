import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.core.errors import AppException, NotFoundError
from app.models.pitch import PitchVersion, PitchCritique
from app.models.startup import Startup
from app.repositories.pitch_repo import PitchRepo
from app.repositories.profile_repo import ProfileRepo
from app.services.ai_service import MockAIService

class PitchService:
    @staticmethod
    async def generate_pitch(
        db: Session,
        startup: Startup,
        improve_from_pitch_id: uuid.UUID | None,
        ai_service: MockAIService,
    ) -> PitchVersion:
        pv = ProfileRepo.get_latest_version(db, startup.id)
        if not pv:
            raise NotFoundError("Profile version not found")

        prior_critique = None
        if improve_from_pitch_id:
            critique = PitchRepo.get_latest_critique(db, improve_from_pitch_id)
            if critique:
                prior_critique = critique.output

        pitch_output = await ai_service.generate_pitch(pv.data, prior_critique=prior_critique)
        slides_data = [s.model_dump() for s in pitch_output.slides]

        latest_pitch = PitchRepo.get_latest_pitch(db, startup.id)
        next_version = (latest_pitch.version + 1) if latest_pitch else 1

        pitch = PitchRepo.create_pitch(
            db=db,
            startup_id=startup.id,
            version=next_version,
            profile_version=pv.version,
            slides=slides_data,
            parent_pitch_id=improve_from_pitch_id,
            ai_mode="mock",
        )
        return pitch

    @staticmethod
    async def critique_pitch(
        db: Session,
        startup: Startup,
        pitch_id: uuid.UUID,
        ai_service: MockAIService,
    ) -> PitchCritique:
        pitch = PitchRepo.get_pitch_by_id(db, pitch_id)
        if not pitch or pitch.startup_id != startup.id:
            raise NotFoundError("Pitch version not found")

        pv = ProfileRepo.get_latest_version(db, startup.id)
        critique_output = await ai_service.critique_pitch(pv.data if pv else {}, {"slides": pitch.slides})
        output_dict = critique_output.model_dump()

        critique = PitchRepo.save_critique(
            db=db,
            pitch_version_id=pitch.id,
            output=output_dict,
        )
        return critique

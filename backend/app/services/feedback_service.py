import uuid
from sqlalchemy.orm import Session
from app.core.errors import NotFoundError
from app.models.profile_version import ProfileVersion
from app.models.startup import Startup
from app.repositories.profile_repo import ProfileRepo
from app.repositories.readiness_repo import ReadinessRepo
from app.services.profile_service import ProfileService

class FeedbackService:
    @staticmethod
    def resolve_feedback(
        db: Session,
        startup: Startup,
        feedback_id: uuid.UUID,
        action: str,
        founder_input: str | None = None,
    ) -> tuple[ProfileVersion | None, list[dict]]:
        item = ReadinessRepo.get_feedback_item(db, feedback_id)
        if not item or item.startup_id != startup.id:
            raise NotFoundError("Feedback item not found")

        if action == "dismiss":
            ReadinessRepo.resolve_feedback(db, item, "dismissed")
            return None, []

        # Action is 'accept'
        ReadinessRepo.resolve_feedback(db, item, "accepted")

        ops = []
        if founder_input:
            # Check for numbers/facts in founder input
            ops.append({
                "op": "set",
                "path": "traction.notes",
                "value": founder_input,
                "reason": f"Resolved feedback: {item.title}",
            })
            if "interview" in founder_input.lower():
                ops.append({
                    "op": "set",
                    "path": "traction.interviews",
                    "value": founder_input,
                    "reason": f"Resolved feedback: {item.title}",
                })
        elif item.suggested_patch:
            ops = item.suggested_patch

        if ops:
            pv = ProfileRepo.get_latest_version(db, startup.id)
            if pv:
                new_pv, applied = ProfileService.apply_patch_to_startup(
                    db=db,
                    startup=startup,
                    base_version=pv.version,
                    ops=ops,
                    change_reason="feedback_action",
                    source="founder",
                )
                return new_pv, applied

        return None, []

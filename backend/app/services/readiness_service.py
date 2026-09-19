import uuid
from typing import Any
from sqlalchemy.orm import Session
from app.core.errors import NotFoundError
from app.models.readiness import ReadinessReport
from app.models.startup import Startup
from app.repositories.investor_repo import InvestorRepo
from app.repositories.profile_repo import ProfileRepo
from app.repositories.readiness_repo import ReadinessRepo
from app.services.ai_service import MockAIService

TOPIC_WEIGHTS = {
    "problem": {"clarity": 0.5, "specificity": 0.5},
    "market": {"evidence": 0.6, "scalability": 0.4},
    "differentiation": {"differentiation": 0.6, "evidence": 0.4},
    "business_model": {"business_reasoning": 0.7, "specificity": 0.3},
    "validation": {"evidence": 0.8, "specificity": 0.2},
}

DIMENSION_NAMES = {
    "problem": "problem_clarity",
    "market": "market_understanding",
    "differentiation": "differentiation",
    "business_model": "business_model",
    "validation": "customer_validation",
}

class ReadinessService:
    @classmethod
    def compute_scores(cls, turns: list[Any]) -> tuple[dict[str, int | None], int]:
        topic_turns: dict[str, list[dict[str, int]]] = {t: [] for t in TOPIC_WEIGHTS}

        for turn in turns:
            if turn.scores and turn.topic in topic_turns:
                topic_turns[turn.topic].append(turn.scores)

        dimensions: dict[str, int | None] = {}
        for topic, weight_map in TOPIC_WEIGHTS.items():
            dim_key = DIMENSION_NAMES[topic]
            scores_list = topic_turns[topic]
            if not scores_list:
                # Default baseline score if not directly asked in turns
                dimensions[dim_key] = 60
                continue

            turn_scores = []
            for s in scores_list:
                turn_val = sum(s.get(crit, 5) * w for crit, w in weight_map.items())
                turn_scores.append(turn_val * 10)  # scale to 0-100

            dimensions[dim_key] = int(sum(turn_scores) / len(turn_scores))

        valid_dims = [v for v in dimensions.values() if v is not None]
        overall = int(sum(valid_dims) / len(valid_dims)) if valid_dims else 60
        return dimensions, overall

    @classmethod
    async def build_report(
        cls,
        db: Session,
        startup: Startup,
        session_id: uuid.UUID | None,
        ai_service: MockAIService,
    ) -> ReadinessReport:
        pv = ProfileRepo.get_latest_version(db, startup.id)
        if not pv:
            raise NotFoundError("Profile version not found")

        turns = []
        if session_id:
            turns = InvestorRepo.list_turns(db, session_id)

        dimensions, overall = cls.compute_scores(turns)

        narrative = await ai_service.generate_readiness_narrative(
            ctx=pv.data,
            turns=[{"seq": t.seq, "topic": t.topic, "question": t.question, "scores": t.scores} for t in turns],
            computed_scores={"dimensions": dimensions, "overall": overall},
        )

        report = ReadinessRepo.save_report(
            db=db,
            startup_id=startup.id,
            session_id=session_id,
            profile_version=pv.version,
            overall=overall,
            dimension_scores=dimensions,
            narrative=narrative if isinstance(narrative, dict) else narrative.model_dump(),
        )

        # Generate feedback items
        feedback_drafts = await ai_service.extract_feedback_patches(pv.data, narrative)
        for fb in feedback_drafts:
            ReadinessRepo.create_feedback_item(
                db=db,
                startup_id=startup.id,
                report_id=report.id,
                topic=fb.get("topic"),
                title=fb.get("title", "Improvement Action"),
                recommendation=fb.get("recommendation", ""),
                suggested_patch=fb.get("suggested_patch"),
            )

        return report

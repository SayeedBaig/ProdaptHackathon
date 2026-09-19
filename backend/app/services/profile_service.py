import copy
from typing import Any
from sqlalchemy.orm import Session
from app.core.errors import NotFoundError, VersionConflictError
from app.models.profile_version import ProfileVersion
from app.models.startup import Startup
from app.repositories.profile_repo import ProfileRepo
from app.repositories.startup_repo import StartupRepo
from app.schemas.profile import Profile, Identity

ALLOWED_PREFIXES = {
    "identity",
    "problem",
    "customer",
    "solution",
    "value_proposition",
    "market",
    "competitor_summary",
    "business_model",
    "traction",
    "team",
    "funding_ask",
    "assumptions",
    "risks",
    "gaps",
    "provenance",
}

class ProfileService:
    @staticmethod
    def create_initial_profile(startup_name: str, raw_idea: str) -> dict[str, Any]:
        profile = Profile(
            identity=Identity(
                startup_name=startup_name,
                raw_idea=raw_idea,
                one_liner=None,
            )
        )
        return profile.model_dump()

    @staticmethod
    def compute_completeness(data: dict[str, Any]) -> int:
        checks = [
            bool(data.get("problem", {}).get("statement")),
            bool(data.get("customer", {}).get("primary_segment")),
            bool(data.get("solution", {}).get("description")),
            bool(data.get("value_proposition", {}).get("differentiation")),
            bool(data.get("business_model", {}).get("revenue_source")),
            bool(data.get("competitor_summary")),
            bool(data.get("traction", {}).get("interviews")),
            bool(data.get("market", {}).get("summary")),
        ]
        score = sum(1 for c in checks if c)
        return int((score / len(checks)) * 100)

    @staticmethod
    def apply_patch(
        current_data: dict[str, Any],
        ops: list[dict[str, Any]],
        default_source: str = "founder",
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        updated_data = copy.deepcopy(current_data)
        applied_ops = []

        if "provenance" not in updated_data:
            updated_data["provenance"] = {}

        for op_item in ops:
            op_type = op_item.get("op", "set")
            path = op_item.get("path", "")
            val = op_item.get("value")
            reason = op_item.get("reason", "update")

            parts = path.split(".")
            if not parts or parts[0] not in ALLOWED_PREFIXES:
                continue

            target = updated_data
            for part in parts[:-1]:
                if part not in target or not isinstance(target[part], dict):
                    target[part] = {}
                target = target[part]

            leaf = parts[-1]

            if op_type == "set":
                target[leaf] = val
                updated_data["provenance"][path] = default_source
                applied_ops.append(op_item)
            elif op_type == "add":
                if leaf not in target or not isinstance(target[leaf], list):
                    target[leaf] = []
                if isinstance(val, list):
                    target[leaf].extend(val)
                else:
                    target[leaf].append(val)
                applied_ops.append(op_item)
            elif op_type == "remove":
                if isinstance(target, dict) and leaf in target:
                    del target[leaf]
                    applied_ops.append(op_item)

        return updated_data, applied_ops

    @classmethod
    def apply_patch_to_startup(
        cls,
        db: Session,
        startup: Startup,
        base_version: int,
        ops: list[dict[str, Any]],
        change_reason: str,
        source: str = "founder",
    ) -> tuple[ProfileVersion, list[dict[str, Any]]]:
        current_pv = ProfileRepo.get_latest_version(db, startup.id)
        if not current_pv:
            raise NotFoundError("Profile version not found")

        if current_pv.version != base_version:
            raise VersionConflictError(
                f"Base version conflict: provided {base_version}, latest is {current_pv.version}"
            )

        new_data, applied_ops = cls.apply_patch(current_pv.data, ops, default_source=source)
        completeness = cls.compute_completeness(new_data)
        new_version_num = current_pv.version + 1

        new_pv = ProfileRepo.create_version(
            db=db,
            startup_id=startup.id,
            version=new_version_num,
            data=new_data,
            patch=applied_ops,
            change_reason=change_reason,
            completeness_pct=completeness,
        )

        StartupRepo.update_current_version(db, startup, new_pv.id)
        return new_pv, applied_ops

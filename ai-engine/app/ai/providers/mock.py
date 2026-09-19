"""
Mock provider: returns fixture JSON from app/ai/fixtures/*.json.
Never calls any external API.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Type, TypeVar
from pydantic import BaseModel

from app.ai.providers.base import BaseProvider, ProviderResult

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger("ai_engine.providers.mock")

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


class MockProvider(BaseProvider):
    name = "mock"

    # Map capability name → fixture filename (without .json)
    CAPABILITY_MAP: dict[str, str] = {
        "analyze_idea": "analyze_idea",
        "generate_clarification_question": "generate_clarification_question",
        "extract_profile_patch": "extract_profile_patch",
        "generate_value_proposition": "generate_value_proposition",
        "analyze_competitors": "analyze_competitors",
        "analyze_market": "analyze_market",
        "analyze_business_model": "analyze_business_model",
        "generate_pitch": "generate_pitch",
        "critique_pitch": "critique_pitch",
        "generate_investor_question": "generate_investor_question",
        "evaluate_answer": "evaluate_answer",
        "generate_readiness_narrative": "generate_readiness_narrative",
        "extract_feedback_patches": "extract_feedback_patches",
    }

    def call(
        self,
        *,
        system: str,
        user: str,
        response_model: Type[T],
        temperature: float = 0.3,
    ) -> ProviderResult:
        """
        Derive the capability key from the system prompt to find the right fixture.
        Falls back to an empty JSON object if no fixture found.
        """
        capability = self._infer_capability(system)
        raw_text = self._load_fixture(capability)
        return ProviderResult(
            raw_text=raw_text,
            model="mock-v1",
            ai_mode="mock",
            degraded=False,
            warnings=[] if capability else ["MockProvider: no fixture matched; using empty {}"],
            processing_time_ms=0.1,
        )

    # ------------------------------------------------------------------
    def _infer_capability(self, system: str) -> str:
        """Simple keyword scan of the system prompt → capability key."""
        system_lower = system.lower()
        for cap_key in self.CAPABILITY_MAP:
            # Heuristic: match first word(s) of each capability
            keyword = cap_key.replace("_", " ")
            if keyword in system_lower or cap_key in system_lower:
                return cap_key
        # Secondary keyword fallbacks
        if "idea" in system_lower and "analys" in system_lower:
            return "analyze_idea"
        if "clarification" in system_lower or "question" in system_lower:
            return "generate_clarification_question"
        if "patch" in system_lower or "extract" in system_lower:
            return "extract_profile_patch"
        if "value prop" in system_lower or "geoff moore" in system_lower:
            return "generate_value_proposition"
        if "competitor" in system_lower:
            return "analyze_competitors"
        if "market" in system_lower:
            return "analyze_market"
        if "business model" in system_lower:
            return "analyze_business_model"
        if "pitch deck" in system_lower or "generate pitch" in system_lower:
            return "generate_pitch"
        if "critique" in system_lower:
            return "critique_pitch"
        if "investor" in system_lower and "evaluat" not in system_lower:
            return "generate_investor_question"
        if "evaluat" in system_lower and "answer" in system_lower:
            return "evaluate_answer"
        if "readiness" in system_lower or "narrative" in system_lower:
            return "generate_readiness_narrative"
        if "feedback" in system_lower:
            return "extract_feedback_patches"
        return ""

    def _load_fixture(self, capability: str) -> str:
        if not capability:
            return "{}"
        fixture_name = self.CAPABILITY_MAP.get(capability, capability)
        fixture_path = FIXTURES_DIR / f"{fixture_name}.json"
        if fixture_path.exists():
            return fixture_path.read_text(encoding="utf-8")
        logger.warning("MockProvider: fixture not found: %s", fixture_path)
        return "{}"

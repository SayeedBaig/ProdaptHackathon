"""
AI Runner: Retry / repair / provider-chain execution logic.

Flow:
  1. Try primary provider (Gemini if key present, else Mock).
  2. On provider error or JSON parse failure, try repair (re-prompt for JSON fix).
  3. On second failure, fall back to MockProvider.
  4. Validate parsed JSON against the Pydantic response_model.
  5. Return (model_instance, ProviderResult).
"""
from __future__ import annotations

import json
import logging
import os
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError

from app.ai.providers.base import BaseProvider, ProviderResult
from app.ai.providers.mock import MockProvider
from app.ai.providers.gemini import GeminiProvider

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger("ai_engine.runner")

MAX_RETRIES = 2  # total attempts before hard fallback to mock


class AIRunner:
    """
    Orchestrates provider selection, retry, JSON repair, and fallback.
    Instantiate once and reuse across the service lifecycle.
    """

    def __init__(self):
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        use_mock = os.getenv("USE_MOCK_LLM", "false").lower() in ("true", "1", "yes")

        self._mock = MockProvider()

        if use_mock or not gemini_key:
            logger.info("AIRunner: using MockProvider (USE_MOCK_LLM=%s, key_present=%s)", use_mock, bool(gemini_key))
            self._primary: BaseProvider = self._mock
        else:
            logger.info("AIRunner: using GeminiProvider (model=%s)", os.getenv("DEFAULT_MODEL", "gemini-2.0-flash"))
            self._primary = GeminiProvider(api_key=gemini_key)

    # ------------------------------------------------------------------
    def run(
        self,
        *,
        capability: str,
        system: str,
        user: str,
        response_model: Type[T],
        temperature: float = 0.3,
    ) -> tuple[T, ProviderResult]:
        """
        Execute one AI capability call and return (parsed_model, provider_result).
        Never raises — always returns a valid model instance.
        """
        pr: ProviderResult | None = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                pr = self._primary.call(
                    system=system,
                    user=user,
                    response_model=response_model,
                    temperature=temperature,
                )
                if not pr.raw_text or pr.degraded:
                    raise ValueError("Provider returned empty/degraded result")

                parsed = response_model.model_validate_json(pr.raw_text)
                logger.info("[%s] SUCCESS on attempt %d via %s", capability, attempt, self._primary.name)
                return parsed, pr

            except (ValidationError, ValueError, json.JSONDecodeError) as exc:
                logger.warning("[%s] Attempt %d failed: %s — retrying…", capability, attempt, exc)
                # Inject a repair instruction into the user prompt for next attempt
                if attempt < MAX_RETRIES:
                    user = (
                        f"The previous response was invalid JSON or failed schema validation.\n"
                        f"Error: {exc}\n"
                        f"Please return ONLY valid JSON matching the schema. Original request:\n{user}"
                    )
            except Exception as exc:
                logger.error("[%s] Attempt %d unexpected error: %s", capability, attempt, exc)
                break

        # Hard fallback: MockProvider
        logger.warning("[%s] All attempts failed. Falling back to MockProvider.", capability)
        pr_mock = self._mock.call(
            system=system,
            user=user,
            response_model=response_model,
            temperature=temperature,
        )
        pr_mock.degraded = True
        pr_mock.warnings.append(f"Primary provider ({self._primary.name}) failed; using mock fixture.")

        try:
            parsed_mock = response_model.model_validate_json(pr_mock.raw_text)
        except Exception:
            # Absolute last resort: return a blank default instance
            parsed_mock = response_model.model_construct()

        return parsed_mock, pr_mock


# Singleton — imported by AIService
ai_runner = AIRunner()

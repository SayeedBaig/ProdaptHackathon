"""
Google Gemini provider using google-genai SDK.
Uses native JSON/schema mode (response_mime_type=application/json).
"""
from __future__ import annotations

import json
import logging
import os
from typing import Type, TypeVar
from pydantic import BaseModel

from app.ai.providers.base import BaseProvider, ProviderResult

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger("ai_engine.providers.gemini")


class GeminiProvider(BaseProvider):
    name = "gemini"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = model or os.getenv("DEFAULT_MODEL", "gemini-2.0-flash")

    def call(
        self,
        *,
        system: str,
        user: str,
        response_model: Type[T],
        temperature: float = 0.3,
    ) -> ProviderResult:
        from google import genai
        from google.genai import types

        warnings: list[str] = []
        client = genai.Client(api_key=self.api_key)

        full_prompt = f"{system}\n\n{user}"

        def _do_call():
            return client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_model,
                    temperature=temperature,
                ),
            )

        try:
            gemini_response, ms = self._timed(_do_call)
            raw_text = gemini_response.text or ""
            return ProviderResult(
                raw_text=raw_text,
                model=self.model,
                ai_mode="live",
                degraded=False,
                warnings=warnings,
                processing_time_ms=ms,
            )
        except Exception as exc:
            logger.warning("Gemini call failed: %s", exc)
            return ProviderResult(
                raw_text="",
                model=self.model,
                ai_mode="fallback_provider",
                degraded=True,
                warnings=[f"Gemini error: {exc}"],
                processing_time_ms=0.0,
            )

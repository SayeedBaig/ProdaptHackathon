"""
OpenAI provider using openai SDK structured-output (beta.chat.completions.parse).
"""
from __future__ import annotations

import logging
import os
from typing import Type, TypeVar
from pydantic import BaseModel

from app.ai.providers.base import BaseProvider, ProviderResult

T = TypeVar("T", bound=BaseModel)
logger = logging.getLogger("ai_engine.providers.openai")


class OpenAIProvider(BaseProvider):
    name = "openai"

    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model

    def call(
        self,
        *,
        system: str,
        user: str,
        response_model: Type[T],
        temperature: float = 0.3,
    ) -> ProviderResult:
        import openai

        client = openai.OpenAI(api_key=self.api_key)
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        def _do_call():
            return client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                response_format=response_model,
                temperature=temperature,
            )

        try:
            oai_response, ms = self._timed(_do_call)
            parsed = oai_response.choices[0].message.parsed
            raw_text = parsed.model_dump_json() if parsed else ""
            return ProviderResult(
                raw_text=raw_text,
                model=self.model,
                ai_mode="live",
                degraded=False,
                warnings=[],
                processing_time_ms=ms,
            )
        except Exception as exc:
            logger.warning("OpenAI call failed: %s", exc)
            return ProviderResult(
                raw_text="",
                model=self.model,
                ai_mode="fallback_provider",
                degraded=True,
                warnings=[f"OpenAI error: {exc}"],
                processing_time_ms=0.0,
            )

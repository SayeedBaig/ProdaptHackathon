"""
Base LLM provider interface.
All providers implement call() and return ProviderResult.
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class ProviderResult:
    """Uniform result wrapper returned by every provider."""
    raw_text: str = ""
    model: str = "unknown"
    ai_mode: str = "mock"           # "live" | "fallback_provider" | "mock" | "scripted-demo"
    degraded: bool = False
    warnings: list[str] = field(default_factory=list)
    processing_time_ms: float = 0.0


class BaseProvider(ABC):
    """Abstract base for all LLM providers."""

    name: str = "base"

    @abstractmethod
    def call(
        self,
        *,
        system: str,
        user: str,
        response_model: Type[T],
        temperature: float = 0.3,
    ) -> ProviderResult:
        """
        Call the LLM and return a ProviderResult whose .raw_text is
        a valid JSON string that can be validated against response_model.
        """

    # Convenience timer helper
    @staticmethod
    def _timed(fn) -> tuple[Any, float]:
        t0 = time.perf_counter()
        result = fn()
        return result, round((time.perf_counter() - t0) * 1000, 2)

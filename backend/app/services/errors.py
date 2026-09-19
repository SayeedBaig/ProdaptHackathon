"""
Investor Simulator domain errors.

Each carries a ``code`` attribute matching the error codes defined in
CONVENTIONS.md section 3.3, so that whenever a routes layer is added, it can
translate these directly into the shared error envelope
``{"error": {"code", "message", "details", "request_id"}}`` without the
service layer knowing anything about HTTP.
"""

from __future__ import annotations


class InvestorSimulatorError(Exception):
    code = "VALIDATION_ERROR"

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ValidationError(InvestorSimulatorError):
    code = "VALIDATION_ERROR"


class SessionNotFoundError(InvestorSimulatorError):
    code = "NOT_FOUND"


class SessionClosedError(InvestorSimulatorError):
    code = "SESSION_CLOSED"


class AIProviderError(InvestorSimulatorError):
    code = "LLM_UNAVAILABLE"

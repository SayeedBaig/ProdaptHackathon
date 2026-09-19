"""
Repository for InvestorSession state.

Per CONVENTIONS.md 3.5 (routes -> services -> repositories -> DB), this
repository holds no business logic -- only storage. M3 can later add a
Postgres-backed implementation of the same InvestorSessionRepository
Protocol; InvestorSimulatorService only ever depends on the Protocol, so it
does not need to change when that happens.
"""

from __future__ import annotations

from typing import Protocol

from app.schemas.investor_session import InvestorSession


class InvestorSessionRepository(Protocol):
    def create(self, session: InvestorSession) -> None: ...

    def get(self, session_id: str) -> InvestorSession | None: ...

    def update(self, session: InvestorSession) -> None: ...


class InMemoryInvestorSessionRepository:
    """Deterministic, dependency-free fake for tests/demo. Satisfies
    InvestorSessionRepository structurally."""

    def __init__(self):
        self._sessions: dict[str, InvestorSession] = {}

    def create(self, session: InvestorSession) -> None:
        self._sessions[session.session_id] = session.model_copy(deep=True)

    def get(self, session_id: str) -> InvestorSession | None:
        session = self._sessions.get(session_id)
        return session.model_copy(deep=True) if session else None

    def update(self, session: InvestorSession) -> None:
        self._sessions[session.session_id] = session.model_copy(deep=True)

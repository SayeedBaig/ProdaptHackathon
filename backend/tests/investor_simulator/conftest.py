import pytest

from app.ai.providers.mock_investor_provider import MockInvestorProvider
from app.repositories.investor_session_repository import InMemoryInvestorSessionRepository
from app.schemas.profile import Identity, Profile
from app.services.investor_simulator_service import InvestorSimulatorService


@pytest.fixture
def demo_profile() -> Profile:
    """InternAI: the fixed demo startup used throughout the pitch."""
    return Profile(
        identity=Identity(
            startup_name="InternAI",
            raw_idea=(
                "An AI-powered platform that helps college students discover "
                "internships based on their skills, interests and career goals."
            ),
            one_liner="AI-matched internships for college students.",
        )
    )


@pytest.fixture
def provider() -> MockInvestorProvider:
    return MockInvestorProvider()


@pytest.fixture
def failing_provider() -> MockInvestorProvider:
    return MockInvestorProvider(simulate_failure=True)


@pytest.fixture
def repo() -> InMemoryInvestorSessionRepository:
    return InMemoryInvestorSessionRepository()


@pytest.fixture
def service(provider, repo) -> InvestorSimulatorService:
    return InvestorSimulatorService(ai_provider=provider, repo=repo)


@pytest.fixture
def failing_service(failing_provider, repo) -> InvestorSimulatorService:
    return InvestorSimulatorService(ai_provider=failing_provider, repo=repo)


GOOD_ANSWER = (
    "We are solving the problem that 70% of college students struggle to find "
    "relevant internships because listings are scattered and not personalized. "
    "We validated this with a survey of 400 students and interviews with 20 "
    "career center staff, and our pilot with 3 universities showed strong demand."
)

WEAK_ANSWER = "Not sure."

# Deliberately scores >5 on all six criteria with the mock heuristic, so it
# never triggers a follow-up question -- used for tests that need to advance
# straight through the question bank.
SOLID_ANSWER_NO_FOLLOWUP = (
    "We have data from a pilot survey of 200 students showing strong demand, "
    "and because our AI matching is unique and different from any competitor, "
    "unlike a generic job board, we can scale and expand by automating recommendations "
    "as we grow to serve more universities across the country, and since students "
    "consistently report frustration, therefore our solution directly addresses the core problem."
)

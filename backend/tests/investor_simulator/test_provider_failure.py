import pytest

from app.services.errors import AIProviderError

from .conftest import GOOD_ANSWER


def test_start_session_propagates_ai_provider_failure(failing_service, demo_profile):
    with pytest.raises(AIProviderError):
        failing_service.start_session(startup_id="internai", profile=demo_profile)


def test_evaluate_answer_propagates_ai_provider_failure(service, failing_service, demo_profile, repo):
    # `service` and `failing_service` share the same function-scoped `repo`
    # fixture, so a session started via the working service is visible to
    # the failing one -- only the AI call itself should fail.
    session = service.start_session(startup_id="internai", profile=demo_profile)
    service.submit_answer(session.session_id, GOOD_ANSWER)

    with pytest.raises(AIProviderError):
        failing_service.evaluate_current_answer(session.session_id, demo_profile)

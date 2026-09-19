import pytest

from app.services.errors import SessionClosedError, SessionNotFoundError, ValidationError

from .conftest import GOOD_ANSWER


def test_start_session_creates_active_session_with_first_question(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)

    assert session.status == "active"
    assert session.startup_id == "internai"
    assert session.current_question_index == 0
    assert len(session.turns) == 1
    assert session.turns[0].question.text == "What specific problem are you solving?"
    assert session.completed_at is None


def test_get_current_question_returns_first_question(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)

    question = service.get_current_question(session.session_id)

    assert question.id == session.turns[0].question.id


def test_submit_answer_stores_answer_text_and_timestamp(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)

    updated = service.submit_answer(session.session_id, GOOD_ANSWER)

    assert updated.turns[0].answer_text == GOOD_ANSWER
    assert updated.turns[0].answered_at is not None


def test_empty_answer_raises_validation_error(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)

    with pytest.raises(ValidationError):
        service.submit_answer(session.session_id, "")

    with pytest.raises(ValidationError):
        service.submit_answer(session.session_id, "   ")


def test_invalid_session_id_raises_not_found(service):
    with pytest.raises(SessionNotFoundError):
        service.get_current_question("does-not-exist")

    with pytest.raises(SessionNotFoundError):
        service.submit_answer("does-not-exist", "hello")


def test_complete_session_sets_completed_status(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)

    completed = service.complete_session(session.session_id)

    assert completed.status == "completed"
    assert completed.completed_at is not None


def test_operating_on_completed_session_raises_session_closed(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)
    service.complete_session(session.session_id)

    with pytest.raises(SessionClosedError):
        service.get_current_question(session.session_id)

    with pytest.raises(SessionClosedError):
        service.submit_answer(session.session_id, GOOD_ANSWER)

    with pytest.raises(SessionClosedError):
        service.complete_session(session.session_id)

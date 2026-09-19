import pytest

from app.services.errors import ValidationError

from .conftest import GOOD_ANSWER, SOLID_ANSWER_NO_FOLLOWUP


def _answer_and_evaluate(service, profile, session_id, answer_text):
    service.submit_answer(session_id, answer_text)
    return service.evaluate_current_answer(session_id, profile)


def test_next_question_advances_to_a_new_topic(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)
    first_question_id = session.turns[0].question.id
    _answer_and_evaluate(service, demo_profile, session.session_id, SOLID_ANSWER_NO_FOLLOWUP)

    next_question = service.get_next_question(session.session_id, demo_profile)

    assert next_question is not None
    assert next_question.id != first_question_id


def test_cannot_advance_before_current_answer_is_evaluated(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)
    service.submit_answer(session.session_id, SOLID_ANSWER_NO_FOLLOWUP)

    with pytest.raises(ValidationError):
        service.get_next_question(session.session_id, demo_profile)


def test_weak_evaluation_triggers_a_follow_up_question(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)
    evaluation = _answer_and_evaluate(service, demo_profile, session.session_id, GOOD_ANSWER)
    assert evaluation.follow_up_question is not None  # sanity check on the fixture answer

    follow_up = service.get_next_question(session.session_id, demo_profile)

    assert follow_up is not None
    assert follow_up.intent == "follow_up"
    assert follow_up.topic == session.turns[0].question.topic
    assert follow_up.text == evaluation.follow_up_question


def test_follow_up_is_only_asked_once_per_turn(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)
    _answer_and_evaluate(service, demo_profile, session.session_id, GOOD_ANSWER)
    service.get_next_question(session.session_id, demo_profile)  # -> follow-up question

    # Answer the follow-up solidly so it doesn't chain into another follow-up.
    _answer_and_evaluate(service, demo_profile, session.session_id, SOLID_ANSWER_NO_FOLLOWUP)
    second_next = service.get_next_question(session.session_id, demo_profile)

    assert second_next is not None
    assert second_next.intent != "follow_up"


def test_question_bank_exhaustion_returns_none(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)

    # Answer solidly (no follow-ups) until the mock's 9-question bank runs out.
    next_question = session.turns[0].question
    seen_ids = set()
    guard = 0
    while next_question is not None and guard < 50:
        guard += 1
        seen_ids.add(next_question.id)
        _answer_and_evaluate(service, demo_profile, session.session_id, SOLID_ANSWER_NO_FOLLOWUP)
        next_question = service.get_next_question(session.session_id, demo_profile)

    assert next_question is None
    assert len(seen_ids) == 9  # exactly the mock question bank size

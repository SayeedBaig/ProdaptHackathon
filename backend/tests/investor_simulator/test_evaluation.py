import pytest

from app.services.errors import ValidationError

from .conftest import GOOD_ANSWER, WEAK_ANSWER


def test_evaluate_current_answer_returns_scored_evaluation(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)
    service.submit_answer(session.session_id, GOOD_ANSWER)

    evaluation = service.evaluate_current_answer(session.session_id, demo_profile)

    assert set(evaluation.scores.keys()) == {
        "clarity", "specificity", "evidence", "business_reasoning",
        "differentiation", "scalability",
    }
    assert all(0 <= v <= 10 for v in evaluation.scores.values())
    assert evaluation.weakest_criterion in evaluation.scores
    assert evaluation.explanation


def test_evaluation_is_deterministic_for_same_answer(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)
    service.submit_answer(session.session_id, GOOD_ANSWER)
    first = service.evaluate_current_answer(session.session_id, demo_profile)

    session2 = service.start_session(startup_id="internai", profile=demo_profile)
    service.submit_answer(session2.session_id, GOOD_ANSWER)
    second = service.evaluate_current_answer(session2.session_id, demo_profile)

    assert first.scores == second.scores


def test_weak_answer_scores_lower_than_strong_answer(service, demo_profile):
    strong_session = service.start_session(startup_id="internai", profile=demo_profile)
    service.submit_answer(strong_session.session_id, GOOD_ANSWER)
    strong_eval = service.evaluate_current_answer(strong_session.session_id, demo_profile)

    weak_session = service.start_session(startup_id="internai", profile=demo_profile)
    service.submit_answer(weak_session.session_id, WEAK_ANSWER)
    weak_eval = service.evaluate_current_answer(weak_session.session_id, demo_profile)

    strong_total = sum(strong_eval.scores.values())
    weak_total = sum(weak_eval.scores.values())
    assert strong_total > weak_total


def test_cannot_evaluate_before_answer_submitted(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)

    with pytest.raises(ValidationError):
        service.evaluate_current_answer(session.session_id, demo_profile)

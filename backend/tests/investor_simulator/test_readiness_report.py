import pytest

from app.services.errors import SessionClosedError, SessionNotFoundError

from .conftest import SOLID_ANSWER_NO_FOLLOWUP


def test_readiness_report_requires_completed_session(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)

    with pytest.raises(SessionClosedError):
        service.get_readiness_report(session.session_id)


def test_readiness_report_unknown_session_raises_not_found(service):
    with pytest.raises(SessionNotFoundError):
        service.get_readiness_report("does-not-exist")


def test_readiness_report_after_completed_session(service, demo_profile):
    session = service.start_session(startup_id="internai", profile=demo_profile)
    service.submit_answer(session.session_id, SOLID_ANSWER_NO_FOLLOWUP)
    service.evaluate_current_answer(session.session_id, demo_profile)
    service.complete_session(session.session_id)

    report = service.get_readiness_report(session.session_id)

    assert report.session_id == session.session_id
    assert report.startup_id == "internai"
    assert 0 <= report.overall_score <= 100
    assert report.category in (
        "Needs Significant Improvement", "Developing",
        "Investor-ready with Improvements", "Strong Readiness",
    )
    assert report.turn_count == 1
    assert set(report.per_criterion_averages.keys()) == {
        "clarity", "specificity", "evidence", "business_reasoning",
        "differentiation", "scalability",
    }
    assert report.weakest_criterion in report.per_criterion_averages

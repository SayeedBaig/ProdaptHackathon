from app.services import scoring


def test_weighted_turn_score_uses_documented_weights():
    scores = {
        "clarity": 10, "specificity": 10, "evidence": 10,
        "business_reasoning": 10, "differentiation": 10, "scalability": 10,
    }
    assert scoring.weighted_turn_score(scores) == 10.0

    scores_zero = {k: 0 for k in scores}
    assert scoring.weighted_turn_score(scores_zero) == 0.0

    mixed = {
        "clarity": 10, "specificity": 0, "evidence": 10,
        "business_reasoning": 0, "differentiation": 0, "scalability": 0,
    }
    # 10*0.20 (clarity) + 10*0.20 (evidence) = 4.0
    assert scoring.weighted_turn_score(mixed) == 4.0


def test_session_readiness_score_normalizes_to_0_100():
    perfect_turns = [{
        "clarity": 10, "specificity": 10, "evidence": 10,
        "business_reasoning": 10, "differentiation": 10, "scalability": 10,
    }] * 3
    assert scoring.session_readiness_score(perfect_turns) == 100.0

    zero_turns = [{
        "clarity": 0, "specificity": 0, "evidence": 0,
        "business_reasoning": 0, "differentiation": 0, "scalability": 0,
    }] * 2
    assert scoring.session_readiness_score(zero_turns) == 0.0

    assert scoring.session_readiness_score([]) == 0.0


def test_readiness_category_buckets():
    assert scoring.readiness_category(0) == "Needs Significant Improvement"
    assert scoring.readiness_category(40) == "Needs Significant Improvement"
    assert scoring.readiness_category(41) == "Developing"
    assert scoring.readiness_category(60) == "Developing"
    assert scoring.readiness_category(61) == "Investor-ready with Improvements"
    assert scoring.readiness_category(80) == "Investor-ready with Improvements"
    assert scoring.readiness_category(81) == "Strong Readiness"
    assert scoring.readiness_category(100) == "Strong Readiness"


def test_per_criterion_averages_and_weakest_criterion():
    turns = [
        {"clarity": 8, "specificity": 4, "evidence": 6, "business_reasoning": 6, "differentiation": 6, "scalability": 6},
        {"clarity": 6, "specificity": 2, "evidence": 6, "business_reasoning": 6, "differentiation": 6, "scalability": 6},
    ]
    averages = scoring.per_criterion_averages(turns)
    assert averages["specificity"] == 3.0
    assert scoring.weakest_criterion(averages) == "specificity"

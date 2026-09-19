"""
Investor Simulator scoring.

Weights match the task brief; the six criteria keys match the frozen
CONVENTIONS.md criteria list exactly:
clarity, specificity, evidence, business_reasoning, differentiation, scalability
"""

from __future__ import annotations

from app.schemas.investor_session import ReadinessCategory

CRITERIA_WEIGHTS: dict[str, float] = {
    "clarity": 0.20,
    "specificity": 0.15,
    "evidence": 0.20,
    "business_reasoning": 0.15,
    "differentiation": 0.15,
    "scalability": 0.15,
}

assert abs(sum(CRITERIA_WEIGHTS.values()) - 1.0) < 1e-9

# (inclusive lower bound, inclusive upper bound, category label)
READINESS_BUCKETS: list[tuple[int, int, ReadinessCategory]] = [
    (0, 40, "Needs Significant Improvement"),
    (41, 60, "Developing"),
    (61, 80, "Investor-ready with Improvements"),
    (81, 100, "Strong Readiness"),
]


def weighted_turn_score(scores: dict[str, int]) -> float:
    """Weighted composite of one turn's six criterion scores, 0-10 scale."""
    return sum(scores[criterion] * weight for criterion, weight in CRITERIA_WEIGHTS.items())


def session_readiness_score(turn_scores: list[dict[str, int]]) -> float:
    """Mean weighted composite across all evaluated turns, normalized to 0-100."""
    if not turn_scores:
        return 0.0
    composites = [weighted_turn_score(scores) for scores in turn_scores]
    mean_composite_0_to_10 = sum(composites) / len(composites)
    return round(mean_composite_0_to_10 * 10, 2)


def readiness_category(score: float) -> ReadinessCategory:
    for low, high, label in READINESS_BUCKETS:
        if low <= score <= high:
            return label
    # score > 100 shouldn't happen, but fail safe to the top bucket
    return READINESS_BUCKETS[-1][2]


def per_criterion_averages(turn_scores: list[dict[str, int]]) -> dict[str, float]:
    if not turn_scores:
        return {criterion: 0.0 for criterion in CRITERIA_WEIGHTS}
    return {
        criterion: round(sum(s[criterion] for s in turn_scores) / len(turn_scores), 2)
        for criterion in CRITERIA_WEIGHTS
    }


def weakest_criterion(averages: dict[str, float]) -> str:
    return min(averages, key=lambda criterion: averages[criterion])

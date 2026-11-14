from app.services.operational_recommendations import (
    build_operational_recommendations,
)


def test_recommends_smaller_batch_when_remaining_is_high():
    evidence = {
        "waste_by_branch": [
            ("A", 24.2),
        ],
        "preparation_vs_sales": [
            ("A", 100, 70, 30),
        ],
        "branch_summary": [
            (
                "A",
                "Branch A",
                "City Centre",
                "High weekday lunch demand",
                "Fixed staffing based on expected peak demand",
                "Minimum stock based inventory",
                "Large initial preparation batches",
            ),
        ],
    }

    recommendations = build_operational_recommendations(evidence)

    assert len(recommendations) > 0
    assert any(
        "smaller initial preparation batch" in recommendation
        for recommendation in recommendations
    )


def test_no_recommendation_when_remaining_is_low():
    evidence = {
        "waste_by_branch": [
            ("B", 5.8),
        ],
        "preparation_vs_sales": [
            ("B", 100, 95, 5),
        ],
        "branch_summary": [
            (
                "B",
                "Branch B",
                "Residential",
                "Strong evening and weekend demand",
                "Demand-adjusted staffing",
                "Demand-based purchasing",
                "Smaller batches with replenishment",
            ),
        ],
    }

    recommendations = build_operational_recommendations(evidence)

    assert not any(
        "smaller initial preparation batch" in recommendation
        for recommendation in recommendations
    )


def test_empty_evidence_returns_empty_list():
    recommendations = build_operational_recommendations({})

    assert recommendations == []


def test_unknown_branch_is_skipped():
    evidence = {
        "waste_by_branch": [
            ("A", 24.2),
        ],
        "preparation_vs_sales": [
            ("A", 100, 70, 30),
        ],
        "branch_summary": [],
    }

    recommendations = build_operational_recommendations(evidence)

    assert recommendations == []
from app.services.operational_reasoning import (
    build_operational_reasoning_context,
)


def sample_operational_evidence():
    return {
        "waste_by_branch": [
            ("A", 24.20),
            ("C", 8.20),
            ("B", 5.80),
        ],
        "preparation_vs_sales": [
            ("A", 294, 219, 75),
            ("C", 105, 79, 26),
            ("B", 157, 137, 20),
        ],
        "waste_by_reason": [
            ("A", "Over-preparation", 24.20),
            ("B", "Unsold prepared food", 5.80),
            ("C", "Demand uncertainty", 8.20),
        ],
        "inventory_spoilage": [
            ("A", 10.50),
            ("C", 3.80),
            ("B", 2.80),
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
            (
                "B",
                "Branch B",
                "Residential",
                "Strong evening and weekend demand",
                "Demand-adjusted staffing",
                "Demand-based purchasing",
                "Smaller batches with replenishment",
            ),
            (
                "C",
                "Branch C",
                "Tourist Area",
                "Highly variable demand",
                "Forecast-adjusted staffing",
                "Moderate stock with forecast-based purchasing",
                "Forecast-based preparation",
            ),
        ],
    }


def test_build_reasoning_context_contains_question():
    context = build_operational_reasoning_context(
        "Why is Branch A generating more food waste?",
        sample_operational_evidence(),
    )

    assert (
        context["question"]
        == "Why is Branch A generating more food waste?"
    )


def test_context_contains_observed_facts():
    context = build_operational_reasoning_context(
        "Why is Branch A generating more food waste?",
        sample_operational_evidence(),
    )

    assert context["observed_facts"]
    assert any(
        fact["branch_id"] == "A"
        and fact["waste_kg"] == 24.20
        for fact in context["observed_facts"]
    )


def test_context_contains_potential_contributor():
    context = build_operational_reasoning_context(
        "Why is Branch A generating more food waste?",
        sample_operational_evidence(),
    )

    contributors = context["potential_contributors"]

    assert contributors
    assert contributors[0]["branch_id"] == "A"
    assert contributors[0]["status"] == "potential_contributor"


def test_rag_evidence_is_marked_as_internal_knowledge():
    rag_evidence = [
        {
            "source": "data/knowledge_base/kitchen_sops/batch_preparation.md",
            "title": "Batch Preparation SOP",
            "content": "Branch A uses larger initial preparation batches.",
        }
    ]

    context = build_operational_reasoning_context(
        "Why is Branch A generating more food waste?",
        sample_operational_evidence(),
        rag_evidence,
    )

    knowledge = context["restaurant_knowledge"]

    assert len(knowledge) == 1
    assert knowledge[0]["source_type"] == (
        "internal_restaurant_knowledge"
    )


def test_causality_is_explicitly_limited():
    context = build_operational_reasoning_context(
        "Why is Branch A generating more food waste?",
        sample_operational_evidence(),
    )

    assert any(
        "association" in gap.lower()
        and "causation" in gap.lower()
        for gap in context["evidence_gaps"]
    )
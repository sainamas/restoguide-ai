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


def test_reasoning_contains_question():
    result = build_operational_reasoning_context(
        "Why is food waste higher in Branch A than Branch B?",
        sample_operational_evidence(),
    )

    assert (
        result["question"]
        == "Why is food waste higher in Branch A than Branch B?"
    )


def test_reasoning_contains_observed_facts():
    result = build_operational_reasoning_context(
        "Why is food waste higher in Branch A than Branch B?",
        sample_operational_evidence(),
    )

    facts = " ".join(result["observed_facts"])

    assert "24.2" in facts
    assert "294" in facts
    assert "219" in facts
    assert "75" in facts
    assert "10.5" in facts


def test_reasoning_identifies_preparation_contributor():
    result = build_operational_reasoning_context(
        "Why is food waste higher in Branch A than Branch B?",
        sample_operational_evidence(),
    )

    contributors = " ".join(result["potential_contributors"]).lower()

    assert "large initial preparation batches" in contributors
    assert "smaller batches with replenishment" in contributors
    assert "294" in contributors
    assert "75" in contributors


def test_reasoning_identifies_inventory_contributor():
    result = build_operational_reasoning_context(
        "Why is food waste higher in Branch A than Branch B?",
        sample_operational_evidence(),
    )

    contributors = " ".join(result["potential_contributors"]).lower()

    assert "minimum-stock" in contributors
    assert "10.50 kg" in contributors
    assert "2.80 kg" in contributors


def test_reasoning_avoids_definitive_causality():
    result = build_operational_reasoning_context(
        "Why is food waste higher in Branch A than Branch B?",
        sample_operational_evidence(),
    )

    gaps = " ".join(result["evidence_gaps"]).lower()

    assert "association" in gaps
    assert "causation" in gaps


def test_rag_sources_are_preserved():
    rag_evidence = [
        {
            "title": "POL-003_waste.md",
            "content": "Prepare ingredients according to service needs.",
        },
        {
            "title": "SOP-006_closing.md",
            "content": "Handle retained food under approved storage policy.",
        },
    ]

    result = build_operational_reasoning_context(
        "Why is food waste higher in Branch A than Branch B?",
        sample_operational_evidence(),
        rag_evidence,
    )

    sources = result["restaurant_knowledge"]

    assert len(sources) == 2
    assert sources[0]["source"] == "POL-003_waste.md"
    assert sources[1]["source"] == "SOP-006_closing.md"
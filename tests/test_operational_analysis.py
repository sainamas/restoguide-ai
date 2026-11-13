from app.services.operational_analysis import get_operational_evidence


def test_operational_evidence_contains_all_sections():
    evidence = get_operational_evidence()

    assert "waste_by_branch" in evidence
    assert "preparation_vs_sales" in evidence
    assert "waste_by_reason" in evidence
    assert "inventory_spoilage" in evidence
    assert "branch_summary" in evidence


def test_waste_by_branch_contains_three_branches():
    evidence = get_operational_evidence()

    assert len(evidence["waste_by_branch"]) == 3


def test_branch_a_has_highest_waste():
    evidence = get_operational_evidence()

    first_branch = evidence["waste_by_branch"][0]

    assert first_branch[0] == "A"
    assert float(first_branch[1]) == 24.20


def test_branch_a_has_highest_spoilage():
    evidence = get_operational_evidence()

    first_branch = evidence["inventory_spoilage"][0]

    assert first_branch[0] == "A"
    assert float(first_branch[1]) == 10.50
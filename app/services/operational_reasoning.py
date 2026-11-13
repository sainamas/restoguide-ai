from typing import Any


def build_operational_reasoning_context(
    question: str,
    operational_evidence: dict[str, Any],
    rag_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Combine structured PostgreSQL evidence with restaurant knowledge
    retrieved through RAG.

    This layer does not generate an answer. It prepares grounded evidence
    for a later reasoning component.
    """

    rag_evidence = rag_evidence or []

    observed_facts = _extract_observed_facts(operational_evidence)
    knowledge_context = _extract_knowledge_context(rag_evidence)
    potential_contributors = _identify_potential_contributors(
        operational_evidence
    )

    return {
        "question": question,
        "observed_facts": observed_facts,
        "restaurant_knowledge": knowledge_context,
        "potential_contributors": potential_contributors,
        "evidence_gaps": _identify_evidence_gaps(
            operational_evidence,
            rag_evidence,
        ),
    }


def _extract_observed_facts(
    evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    """Convert SQL results into explicit observed facts."""

    facts = []

    waste_by_branch = evidence.get("waste_by_branch", [])

    if waste_by_branch:
        highest_branch = waste_by_branch[0]

        facts.append(
            {
                "type": "branch_waste",
                "branch_id": highest_branch[0],
                "waste_kg": float(highest_branch[1]),
                "statement": (
                    f"Branch {highest_branch[0]} has the highest recorded "
                    f"food waste at {float(highest_branch[1]):.2f} kg."
                ),
            }
        )

    preparation_vs_sales = evidence.get("preparation_vs_sales", [])

    for row in preparation_vs_sales:
        branch_id, prepared, sold, remaining = row

        facts.append(
            {
                "type": "preparation_vs_sales",
                "branch_id": branch_id,
                "prepared": prepared,
                "sold": sold,
                "remaining": remaining,
                "statement": (
                    f"Branch {branch_id} prepared {prepared} units, sold "
                    f"{sold} units, and had {remaining} units remaining."
                ),
            }
        )

    inventory_spoilage = evidence.get("inventory_spoilage", [])

    for row in inventory_spoilage:
        branch_id, spoilage = row

        facts.append(
            {
                "type": "inventory_spoilage",
                "branch_id": branch_id,
                "spoilage_kg": float(spoilage),
                "statement": (
                    f"Branch {branch_id} recorded {float(spoilage):.2f} kg "
                    "of inventory spoilage."
                ),
            }
        )

    waste_by_reason = evidence.get("waste_by_reason", [])

    for row in waste_by_reason:
        branch_id, reason, waste = row

        facts.append(
            {
                "type": "waste_reason",
                "branch_id": branch_id,
                "reason": reason,
                "waste_kg": float(waste),
                "statement": (
                    f"Branch {branch_id} recorded {float(waste):.2f} kg "
                    f"of waste associated with '{reason}'."
                ),
            }
        )

    return facts


def _extract_knowledge_context(
    rag_evidence: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Normalize RAG results into a trusted knowledge section."""

    knowledge = []

    for item in rag_evidence:
        knowledge.append(
            {
                "source": item.get("source"),
                "title": item.get("title"),
                "content": item.get("content", item.get("text", "")),
                "source_type": "internal_restaurant_knowledge",
            }
        )

    return knowledge


def _identify_potential_contributors(
    evidence: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Identify relationships supported by the current operational data.

    These are hypotheses/potential contributors, not causal conclusions.
    """

    contributors = []

    waste_by_branch = evidence.get("waste_by_branch", [])
    branch_summary = evidence.get("branch_summary", [])

    if waste_by_branch and branch_summary:
        highest_waste_branch = waste_by_branch[0][0]

        branch_models = {
            row[0]: {
                "location_type": row[2],
                "demand_pattern": row[3],
                "staffing_model": row[4],
                "inventory_model": row[5],
                "preparation_model": row[6],
            }
            for row in branch_summary
        }

        model = branch_models.get(highest_waste_branch)

        if model:
            contributors.append(
                {
                    "branch_id": highest_waste_branch,
                    "status": "potential_contributor",
                    "factors": [
                        model["preparation_model"],
                        model["inventory_model"],
                        model["staffing_model"],
                    ],
                    "reason": (
                        f"Branch {highest_waste_branch}'s operating model "
                        "contains preparation, inventory, and staffing "
                        "characteristics that may contribute to its "
                        "observed waste pattern."
                    ),
                }
            )

    return contributors


def _identify_evidence_gaps(
    operational_evidence: dict[str, Any],
    rag_evidence: list[dict[str, Any]],
) -> list[str]:
    """Identify information that is not currently supported."""

    gaps = []

    if not operational_evidence:
        gaps.append("No operational database evidence was available.")

    if not rag_evidence:
        gaps.append(
            "No relevant internal restaurant knowledge was retrieved."
        )

    if not operational_evidence.get("sales"):
        gaps.append(
            "Detailed item-level sales evidence is not currently included."
        )

    gaps.append(
        "The available data supports association, not definitive causation."
    )

    return gaps
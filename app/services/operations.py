from app.services.operational_db import get_connection


def get_operational_evidence():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            # 1. Waste by branch
            cursor.execute(
                """
                SELECT
                    branch_id,
                    SUM(waste_quantity_kg) AS total_waste_kg
                FROM waste_records
                GROUP BY branch_id
                ORDER BY total_waste_kg DESC;
                """
            )
            waste_by_branch = cursor.fetchall()

            # 2. Preparation vs sales
            cursor.execute(
                """
                SELECT
                    branch_id,
                    SUM(quantity_prepared) AS prepared,
                    SUM(quantity_sold) AS sold,
                    SUM(remaining_quantity) AS remaining
                FROM preparations
                GROUP BY branch_id
                ORDER BY remaining DESC;
                """
            )
            preparation_vs_sales = cursor.fetchall()

            # 3. Waste reason
            cursor.execute(
                """
                SELECT
                    branch_id,
                    waste_reason,
                    SUM(waste_quantity_kg) AS total_waste_kg
                FROM waste_records
                GROUP BY branch_id, waste_reason
                ORDER BY branch_id;
                """
            )
            waste_by_reason = cursor.fetchall()

            # 4. Inventory spoilage
            cursor.execute(
                """
                SELECT
                    branch_id,
                    SUM(spoilage_kg) AS total_spoilage_kg
                FROM inventory
                GROUP BY branch_id
                ORDER BY total_spoilage_kg DESC;
                """
            )
            inventory_spoilage = cursor.fetchall()

            # 5. Branch operating model
            cursor.execute(
                """
                SELECT
                    branch_id,
                    branch_name,
                    location_type,
                    demand_pattern,
                    staffing_model,
                    inventory_model,
                    preparation_model
                FROM branches
                ORDER BY branch_id;
                """
            )
            branch_summary = cursor.fetchall()

    return {
        "waste_by_branch": waste_by_branch,
        "preparation_vs_sales": preparation_vs_sales,
        "waste_by_reason": waste_by_reason,
        "inventory_spoilage": inventory_spoilage,
        "branch_summary": branch_summary,
    }


def print_operational_evidence():
    evidence = get_operational_evidence()

    print("\n=== FOOD WASTE BY BRANCH ===")
    for row in evidence["waste_by_branch"]:
        print(row)

    print("\n=== PREPARATION VS SALES ===")
    for row in evidence["preparation_vs_sales"]:
        print(row)

    print("\n=== WASTE BY REASON ===")
    for row in evidence["waste_by_reason"]:
        print(row)

    print("\n=== INVENTORY SPOILAGE ===")
    for row in evidence["inventory_spoilage"]:
        print(row)

    print("\n=== BRANCH SUMMARY ===")
    for row in evidence["branch_summary"]:
        print(row)


if __name__ == "__main__":
    print_operational_evidence()

from typing import Any


def build_operational_reasoning_context(
    question: str,
    operational_evidence: dict[str, Any],
    rag_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Combine structured operational evidence with internal restaurant knowledge.

    The reasoning remains evidence-based and deliberately avoids claiming
    definitive causation from synthetic operational data.
    """
    observed_facts = _extract_observed_facts(operational_evidence)
    knowledge = _extract_knowledge_context(rag_evidence or [])

    potential_contributors = _identify_potential_contributors(
        operational_evidence
    )

    evidence_gaps = _identify_evidence_gaps(operational_evidence)

    return {
        "question": question,
        "observed_facts": observed_facts,
        "restaurant_knowledge": knowledge,
        "potential_contributors": potential_contributors,
        "evidence_gaps": evidence_gaps,
    }


def _extract_observed_facts(
    operational_evidence: dict[str, Any],
) -> list[str]:
    """Convert SQL analysis results into readable observed facts."""

    facts: list[str] = []

    waste_by_branch = operational_evidence.get("waste_by_branch", [])
    if waste_by_branch:
        branch, waste = waste_by_branch[0]
        facts.append(
            f"Branch {branch} has the highest recorded food waste at {waste} kg."
        )

    preparation_vs_sales = operational_evidence.get(
        "preparation_vs_sales", []
    )

    for branch, prepared, sold, remaining in preparation_vs_sales:
        facts.append(
            f"Branch {branch} prepared {prepared} units, sold {sold} units, "
            f"and had {remaining} units remaining."
        )

    inventory_spoilage = operational_evidence.get(
        "inventory_spoilage", []
    )

    if inventory_spoilage:
        for branch, spoilage in inventory_spoilage:
            facts.append(
                f"Branch {branch} recorded {spoilage} kg of inventory spoilage."
            )

    waste_by_reason = operational_evidence.get("waste_by_reason", [])

    for branch, reason, amount in waste_by_reason:
        facts.append(
            f"Branch {branch} recorded {amount} kg of waste associated with "
            f"'{reason}'."
        )

    return facts


def _extract_knowledge_context(
    rag_evidence: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """Keep only the RAG evidence actually used by the reasoning layer."""

    knowledge: list[dict[str, str]] = []

    for item in rag_evidence:
        title = item.get("title") or item.get("source") or "Unknown source"
        content = (
            item.get("content")
            or item.get("text")
            or item.get("snippet")
            or ""
        )

        if not content.strip():
            continue

        knowledge.append(
            {
                "source": title,
                "content": content.strip(),
            }
        )

    return knowledge


def _identify_potential_contributors(
    operational_evidence: dict[str, Any],
) -> list[str]:
    """
    Identify operational factors that are consistent with the observed data.

    These are hypotheses, not causal conclusions.
    """

    contributors: list[str] = []

    branch_summary = operational_evidence.get("branch_summary", [])

    branch_models = {
        row[0]: {
            "name": row[1],
            "location_type": row[2],
            "demand_pattern": row[3],
            "staffing_model": row[4],
            "inventory_model": row[5],
            "preparation_model": row[6],
        }
        for row in branch_summary
        if len(row) >= 7
    }

    preparation_vs_sales = {
        row[0]: {
            "prepared": row[1],
            "sold": row[2],
            "remaining": row[3],
        }
        for row in operational_evidence.get("preparation_vs_sales", [])
        if len(row) >= 4
    }

    waste_by_branch = {
        row[0]: float(row[1])
        for row in operational_evidence.get("waste_by_branch", [])
        if len(row) >= 2
    }

    inventory_spoilage = {
        row[0]: float(row[1])
        for row in operational_evidence.get("inventory_spoilage", [])
        if len(row) >= 2
    }

    if "A" in branch_models and "B" in branch_models:
        branch_a = branch_models["A"]
        branch_b = branch_models["B"]

        a_prep = preparation_vs_sales.get("A")
        b_prep = preparation_vs_sales.get("B")

        # Preparation model comparison
        if (
            a_prep
            and b_prep
            and branch_a["preparation_model"]
            and branch_b["preparation_model"]
        ):
            if (
                "large" in branch_a["preparation_model"].lower()
                and "small" in branch_b["preparation_model"].lower()
            ):
                contributors.append(
                    "Preparation strategy may be a contributor: Branch A uses "
                    "large initial preparation batches, while Branch B uses "
                    "smaller batches with replenishment. Branch A prepared "
                    f"{a_prep['prepared']} units and had "
                    f"{a_prep['remaining']} units remaining, compared with "
                    f"{b_prep['prepared']} prepared and "
                    f"{b_prep['remaining']} remaining in Branch B."
                )

        # Inventory model comparison
        if "inventory_model" in branch_a and "inventory_model" in branch_b:
            if (
                "minimum stock" in branch_a["inventory_model"].lower()
                and "demand-based" in branch_b["inventory_model"].lower()
            ):
                if (
                    "A" in inventory_spoilage
                    and "B" in inventory_spoilage
                ):
                    contributors.append(
                        "Inventory strategy may also contribute: Branch A uses "
                        "minimum-stock-based inventory and recorded "
                        f"{inventory_spoilage['A']:.2f} kg of spoilage, while "
                        f"Branch B uses demand-based purchasing and recorded "
                        f"{inventory_spoilage['B']:.2f} kg."
                    )

        # Demand/staffing model comparison
        if (
            branch_a["staffing_model"]
            and branch_b["staffing_model"]
            and branch_a["demand_pattern"]
            and branch_b["demand_pattern"]
        ):
            contributors.append(
                "Demand-response practices differ between the branches: "
                f"Branch A has {branch_a['demand_pattern'].lower()} and uses "
                f"{branch_a['staffing_model'].lower()}, while Branch B has "
                f"{branch_b['demand_pattern'].lower()} and uses "
                f"{branch_b['staffing_model'].lower()}. This difference may "
                "affect how preparation quantities are planned."
            )

    if waste_by_branch.get("A", 0) > waste_by_branch.get("B", 0):
        contributors.append(
            "The observed waste pattern is substantially higher in Branch A "
            "than Branch B, so the differences in their operating models are "
            "relevant factors to investigate."
        )

    return contributors


def _identify_evidence_gaps(
    operational_evidence: dict[str, Any],
) -> list[str]:
    """State what the available data cannot establish."""

    gaps = [
        "Detailed item-level sales evidence is not currently included.",
        "The available data supports association, not definitive causation.",
    ]

    if not operational_evidence.get("preparation_vs_sales"):
        gaps.append(
            "Preparation and sales quantities are not available for comparison."
        )

    return gaps
from typing import Any


def build_operational_recommendations(
    operational_evidence: dict[str, Any],
    target_branches: list[str] | None = None,
) -> list[str]:
    """
    Build evidence-based operational recommendations.

    Recommendations are based only on the operational evidence
    currently available from PostgreSQL.

    If target_branches is provided, recommendations are generated
    only for those branches. If it is not provided, recommendations
    are generated for all available branches.
    """

    recommendations: list[str] = []

    waste_by_branch = operational_evidence.get(
        "waste_by_branch",
        [],
    )

    preparation_vs_sales = operational_evidence.get(
        "preparation_vs_sales",
        [],
    )

    branch_summary = operational_evidence.get(
        "branch_summary",
        [],
    )

    if not waste_by_branch or not preparation_vs_sales:
        return recommendations

    waste_lookup = {
        row[0]: float(row[1])
        for row in waste_by_branch
    }

    preparation_lookup = {
        row[0]: {
            "prepared": int(row[1]),
            "sold": int(row[2]),
            "remaining": int(row[3]),
        }
        for row in preparation_vs_sales
    }

    branch_lookup = {
        row[0]: {
            "branch_name": row[1],
            "location_type": row[2],
            "demand_pattern": row[3],
            "staffing_model": row[4],
            "inventory_model": row[5],
            "preparation_model": row[6],
        }
        for row in branch_summary
    }

    if target_branches:
        target_branch_set = set(target_branches)
    else:
        target_branch_set = set(branch_lookup.keys())

    for branch_id, preparation in preparation_lookup.items():

        if branch_id not in target_branch_set:
            continue

        waste = waste_lookup.get(
            branch_id,
            0.0,
        )

        branch = branch_lookup.get(branch_id)

        if not branch:
            continue

        prepared = preparation["prepared"]
        sold = preparation["sold"]
        remaining = preparation["remaining"]

        if prepared <= 0:
            continue

        remaining_rate = remaining / prepared

        if remaining_rate >= 0.20 and waste > 0:
            recommendations.append(
                f"{branch['branch_name']} may benefit from testing "
                f"a smaller initial preparation batch with replenishment "
                f"based on observed demand. The branch currently has "
                f"{remaining} remaining units from {prepared} prepared units."
            )

        if branch["preparation_model"]:
            recommendations.append(
                f"Review the preparation procedure for "
                f"{branch['branch_name']} against its "
                f"{branch['location_type']} demand pattern. "
                f"The current model is "
                f"'{branch['preparation_model']}', "
                f"so preparation quantities should be validated "
                f"against actual branch-level demand."
            )

    return recommendations


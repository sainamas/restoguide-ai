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
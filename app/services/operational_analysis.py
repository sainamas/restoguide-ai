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
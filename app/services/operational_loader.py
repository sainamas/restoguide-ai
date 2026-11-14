import csv
from pathlib import Path

from app.services.operational_db import get_connection


DATA_DIR = Path("data/operational")


def load_branches():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open(DATA_DIR / "branches.csv", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    cursor.execute(
                        """
                        INSERT INTO branches
                        (
                            branch_id,
                            branch_name,
                            location_type,
                            cuisine_focus,
                            demand_pattern,
                            staffing_model,
                            inventory_model,
                            preparation_model
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (branch_id) DO NOTHING
                        """,
                        (
                            row["branch_id"],
                            row["branch_name"],
                            row["location_type"],
                            row["cuisine_focus"],
                            row["demand_pattern"],
                            row["staffing_model"],
                            row["inventory_model"],
                            row["preparation_model"],
                        ),
                    )

        connection.commit()


def load_sales():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open(DATA_DIR / "sales.csv", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    cursor.execute(
                        """
                        INSERT INTO sales
                        (
                            sale_id,
                            branch_id,
                            sale_date,
                            meal_period,
                            item_name,
                            quantity_sold
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (sale_id) DO NOTHING
                        """,
                        (
                            row["sale_id"],
                            row["branch_id"],
                            row["sale_date"],
                            row["meal_period"],
                            row["item_name"],
                            row["quantity_sold"],
                        ),
                    )

        connection.commit()


def load_preparations():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open(
                DATA_DIR / "preparations.csv",
                newline="",
                encoding="utf-8",
            ) as file:
                reader = csv.DictReader(file)

                for row in reader:
                    cursor.execute(
                        """
                        INSERT INTO preparations
                        (
                            preparation_id,
                            branch_id,
                            prep_date,
                            meal_period,
                            item_name,
                            quantity_prepared,
                            quantity_sold,
                            remaining_quantity
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (preparation_id) DO NOTHING
                        """,
                        (
                            row["preparation_id"],
                            row["branch_id"],
                            row["prep_date"],
                            row["meal_period"],
                            row["item_name"],
                            row["quantity_prepared"],
                            row["quantity_sold"],
                            row["remaining_quantity"],
                        ),
                    )

        connection.commit()


def load_waste_records():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open(
                DATA_DIR / "waste_records.csv",
                newline="",
                encoding="utf-8",
            ) as file:
                reader = csv.DictReader(file)

                for row in reader:
                    cursor.execute(
                        """
                        INSERT INTO waste_records
                        (
                            waste_id,
                            branch_id,
                            waste_date,
                            meal_period,
                            item_name,
                            waste_quantity_kg,
                            waste_reason
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (waste_id) DO NOTHING
                        """,
                        (
                            row["waste_id"],
                            row["branch_id"],
                            row["waste_date"],
                            row["meal_period"],
                            row["item_name"],
                            row["waste_quantity_kg"],
                            row["waste_reason"],
                        ),
                    )

        connection.commit()


def load_inventory():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open(
                DATA_DIR / "inventory.csv",
                newline="",
                encoding="utf-8",
            ) as file:
                reader = csv.DictReader(file)

                for row in reader:
                    cursor.execute(
                        """
                        INSERT INTO inventory
                        (
                            inventory_id,
                            branch_id,
                            inventory_date,
                            item_name,
                            opening_stock_kg,
                            purchased_stock_kg,
                            closing_stock_kg,
                            spoilage_kg
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (inventory_id) DO NOTHING
                        """,
                        (
                            row["inventory_id"],
                            row["branch_id"],
                            row["inventory_date"],
                            row["item_name"],
                            row["opening_stock_kg"],
                            row["purchased_stock_kg"],
                            row["closing_stock_kg"],
                            row["spoilage_kg"],
                        ),
                    )

        connection.commit()


def load_purchases():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open(
                DATA_DIR / "purchases.csv",
                newline="",
                encoding="utf-8",
            ) as file:
                reader = csv.DictReader(file)

                for row in reader:
                    cursor.execute(
                        """
                        INSERT INTO purchases
                        (
                            purchase_id,
                            branch_id,
                            purchase_date,
                            item_name,
                            quantity_kg,
                            supplier_category,
                            unit_cost
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (purchase_id) DO NOTHING
                        """,
                        (
                            row["purchase_id"],
                            row["branch_id"],
                            row["purchase_date"],
                            row["item_name"],
                            row["quantity_kg"],
                            row["supplier_category"],
                            row["unit_cost"],
                        ),
                    )

        connection.commit()


if __name__ == "__main__":
    load_branches()
    load_sales()
    load_preparations()
    load_waste_records()
    load_inventory()
    load_purchases()

    print("All operational data loaded successfully")
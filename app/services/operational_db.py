from app.services.operational_schema import SCHEMA_SQL
import os

import psycopg


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://restoguide:restoguide_dev_password@localhost:5432/restoguide",
)


def get_connection():
    """Create a PostgreSQL connection for operational restaurant data."""
    return psycopg.connect(DATABASE_URL)


def check_connection() -> bool:
    """Check whether the operational PostgreSQL database is available."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()

        return result == (1,)
    except psycopg.Error:
        return False
def initialize_schema() -> None:
    """Create the operational database tables if they do not exist."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SCHEMA_SQL)
        connection.commit()
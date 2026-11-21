import sqlite3
from pathlib import Path
from datetime import datetime, timezone


def init_db(name):
    Path(name).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(name) as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY,
                question TEXT,
                answer TEXT,
                created TEXT,
                feedback TEXT
            )
            """
        )

        columns = {
            row[1] for row in c.execute("PRAGMA table_info(history)")
        }

        if "feedback" not in columns:
            c.execute("ALTER TABLE history ADD COLUMN feedback TEXT")


def save(name, q, a):
    with sqlite3.connect(name) as c:
        cursor = c.execute(
            """
            INSERT INTO history(question, answer, created)
            VALUES(?,?,?)
            """,
            (q, a, datetime.now(timezone.utc).isoformat()),
        )

        return cursor.lastrowid


def add_feedback(name, history_id, feedback):
    if feedback not in {"useful", "not_useful"}:
        raise ValueError("Invalid feedback value.")

    with sqlite3.connect(name) as c:
        cursor = c.execute(
            """
            UPDATE history
            SET feedback = ?
            WHERE id = ?
            """,
            (feedback, history_id),
        )

        return cursor.rowcount == 1


def history(name):
    with sqlite3.connect(name) as c:
        c.row_factory = sqlite3.Row

        return [
            dict(r)
            for r in c.execute(
                "SELECT * FROM history ORDER BY id DESC LIMIT 40"
            )
        ]
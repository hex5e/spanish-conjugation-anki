import sqlite3
from pathlib import Path

DB_FILE = Path("cards.db")
TABLE_NAME = "cards"


def main() -> None:
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        row_count = cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
        verb_count = cur.execute(
            f"SELECT COUNT(DISTINCT verb) FROM {TABLE_NAME}"
        ).fetchone()[0]
        form_count = cur.execute(
            f"SELECT COUNT(DISTINCT form) FROM {TABLE_NAME}"
        ).fetchone()[0]
        person_count = cur.execute(
            f"SELECT COUNT(DISTINCT person) FROM {TABLE_NAME}"
        ).fetchone()[0]
        class_counts = cur.execute(
            f"SELECT regularity_class, COUNT(*) FROM {TABLE_NAME} GROUP BY regularity_class"
        ).fetchall()

    print(f"Total rows: {row_count}")
    print(f"Unique verbs: {verb_count}")
    print(f"Unique forms: {form_count}")
    print(f"Unique persons: {person_count}")
    print("Counts by regularity_class:")
    for cls, cnt in class_counts:
        label = cls if cls is not None else "NULL"
        print(f"  {label}: {cnt}")


if __name__ == "__main__":
    main()

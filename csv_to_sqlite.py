import csv
import sqlite3
from pathlib import Path

CSV_FILE = Path("cards.csv")
DB_FILE = Path("cards.db")
TABLE_NAME = "cards"

FIELDNAMES = [
    "verb_id",
    "verb",
    "form_id",
    "form",
    "person_id",
    "person",
    "conjugation_id",
    "hypothetical_regular_conjugation",
    "conjugation",
    "regularity_class",
    "example_sentence",
    "attempts_count",
    "failure_counts",
]

INT_FIELDS = {"verb_id", "form_id", "person_id", "attempts_count"}


def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    cursor.execute(
        f"""
        CREATE TABLE {TABLE_NAME} (
            verb_id INTEGER,
            verb TEXT,
            form_id INTEGER,
            form TEXT,
            person_id INTEGER,
            person TEXT,
            conjugation_id TEXT,
            hypothetical_regular_conjugation TEXT,
            conjugation TEXT,
            regularity_class TEXT,
            example_sentence TEXT,
            attempts_count INTEGER,
            failure_counts TEXT
        )
        """
    )

    with CSV_FILE.open("r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            processed = [
                int(row[f]) if f in INT_FIELDS and row[f] != "" else row[f]
                for f in FIELDNAMES
            ]
            rows.append(tuple(processed))

    placeholders = ", ".join("?" for _ in FIELDNAMES)
    insert_sql = f"INSERT INTO {TABLE_NAME} VALUES ({placeholders})"
    cursor.executemany(insert_sql, rows)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()

import argparse
import sqlite3
from pathlib import Path


def add_columns(db_path: str) -> None:
    """Add speaker_gender and audio_path columns to the cards table."""
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(cards);")
        existing_cols = {row[1] for row in cur.fetchall()}
        if "speaker_gender" not in existing_cols:
            cur.execute("ALTER TABLE cards ADD COLUMN speaker_gender TEXT;")
        if "audio_path" not in existing_cols:
            cur.execute("ALTER TABLE cards ADD COLUMN audio_path TEXT;")
        conn.commit()
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add speaker_gender and audio_path columns to cards"
    )
    parser.add_argument(
        "--db",
        default="cards.db",
        help="Path to the SQLite database (default: cards.db)",
    )
    args = parser.parse_args()
    add_columns(Path(args.db))
    print("Columns added if missing.")


if __name__ == "__main__":
    main()

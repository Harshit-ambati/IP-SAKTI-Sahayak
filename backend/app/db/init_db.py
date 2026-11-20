"""
Database initialization script for IP-SAKTI Sahayak (Task Su-01).
Applies schema DDL, verifies SQLite FTS5 support, and loads fixtures.
"""

import csv
import json
import sqlite3
import sys
from pathlib import Path

# Adjust path for standalone execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.config import DB_PATH
from app.db.database import get_db_connection, init_database

FIXTURES_PATH = BACKEND_ROOT / "fixtures" / "synthetic_fixtures.json"
CORPUS_DOCS_PATH = PROJECT_ROOT / "data" / "corpus" / "documents.csv"
CORPUS_PASSAGES_PATH = PROJECT_ROOT / "data" / "corpus" / "passages.csv"


def seed_fixtures(conn: sqlite3.Connection) -> None:
    """
    Inserts visibly synthetic fixtures for testing.
    """
    if not FIXTURES_PATH.exists():
        print(f"[WARN] Fixtures file not found at {FIXTURES_PATH}")
        return

    with open(FIXTURES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    cur = conn.cursor()

    # Seed synthetic sources — activated=1 so they appear in public lookup endpoints
    for src in data.get("sources", []):
        cur.execute(
            """
            INSERT OR REPLACE INTO sources (
                source_id, topic, authority, title, official_url, format, role, priority, verification_status, review_note, is_synthetic, activated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
            """,
            (
                src["source_id"],
                src["topic"],
                src["authority"],
                src["title"],
                src["official_url"],
                src.get("format", "html"),
                src.get("role", "primary"),
                src.get("priority", "required"),
                src["verification_status"],
                src.get("review_note", ""),
            )
        )

    # Seed synthetic passages — activated=1
    for pas in data.get("passages", []):
        cur.execute(
            """
            INSERT OR REPLACE INTO passages (
                passage_id, source_id, jurisdiction, authority, document_title, locator, paraphrased_content, source_url, source_type, review_status, review_note, is_synthetic, activated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
            """,
            (
                pas["passage_id"],
                pas["source_id"],
                pas["jurisdiction"],
                pas["authority"],
                pas["document_title"],
                pas["locator"],
                pas["paraphrased_content"],
                pas["source_url"],
                pas.get("source_type", "statute"),
                pas["review_status"],
                pas.get("review_note", ""),
            )
        )

    conn.commit()
    print(f"[INFO] Loaded {len(data.get('sources', []))} synthetic sources and {len(data.get('passages', []))} synthetic passages.")


def seed_real_corpus_if_available(conn: sqlite3.Connection) -> None:
    """
    Seeds initial corpus CSV rows into the database as PRELIMINARY (activated=0).
    These rows are stored locally for internal reference but are intentionally NOT
    returned from public /sources or /passages API endpoints.
    Activation requires Thulasi's review and Harshit's corpus activation gate.
    """
    cur = conn.cursor()

    if CORPUS_DOCS_PATH.exists():
        with open(CORPUS_DOCS_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            doc_count = 0
            for row in reader:
                cur.execute(
                    """
                    INSERT OR REPLACE INTO sources (
                        source_id, topic, authority, title, official_url, format, role, priority, verification_status, review_note, is_synthetic, activated
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
                    """,
                    (
                        row["source_id"],
                        row["topic"],
                        row["authority"],
                        row["title"],
                        row["official_url"],
                        row.get("format", "html"),
                        row.get("role", "primary"),
                        row.get("priority", "required"),
                        row.get("verification_status", "pending"),
                        row.get("review_note", ""),
                    )
                )
                doc_count += 1
        print(f"[INFO] Staged {doc_count} real corpus document records as preliminary (activated=0).")

    if CORPUS_PASSAGES_PATH.exists():
        with open(CORPUS_PASSAGES_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            pas_count = 0
            for row in reader:
                cur.execute(
                    """
                    INSERT OR REPLACE INTO passages (
                        passage_id, source_id, jurisdiction, authority, document_title, locator, paraphrased_content, source_url, source_type, review_status, review_note, is_synthetic, activated
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
                    """,
                    (
                        row["passage_id"],
                        row["source_id"],
                        row["jurisdiction"],
                        row["authority"],
                        row["document_title"],
                        row["locator"],
                        row["paraphrased_content"],
                        row["source_url"],
                        row.get("source_type", "statute"),
                        row.get("review_status", "pending"),
                        row.get("review_note", ""),
                    )
                )
                pas_count += 1
        print(f"[INFO] Staged {pas_count} real corpus passage records as preliminary (activated=0).")

    conn.commit()


def main() -> None:
    print(f"[INFO] Initializing SQLite database at: {DB_PATH}")
    init_database()
    conn = get_db_connection()
    seed_fixtures(conn)
    seed_real_corpus_if_available(conn)
    conn.close()
    print("[SUCCESS] Database initialization and fixture seeding complete.")


if __name__ == "__main__":
    main()

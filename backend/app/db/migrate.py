"""
Database migration utilities for IP-SAKTI Sahayak.
Safely migrates existing SQLite databases by ensuring the 'activated' column
is added to sources and passages tables if missing, and updating synthetic fixtures.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from .database import get_db_connection


def run_migrations(db_path: Optional[Path] = None) -> None:
    """
    Applies schema migrations to an existing SQLite database.
    Idempotent: safe to run against new or already-migrated databases.
    """
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    # 1. Migrate sources table if needed
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='sources';")
    if cur.fetchone()[0] > 0:
        cur.execute("PRAGMA table_info(sources);")
        source_cols = {row["name"] for row in cur.fetchall()}
        if "activated" not in source_cols:
            conn.execute("ALTER TABLE sources ADD COLUMN activated INTEGER NOT NULL DEFAULT 0;")
            print("[MIGRATE] Added 'activated' column to sources table.")

    # 2. Migrate passages table if needed
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='passages';")
    if cur.fetchone()[0] > 0:
        cur.execute("PRAGMA table_info(passages);")
        passage_cols = {row["name"] for row in cur.fetchall()}
        if "activated" not in passage_cols:
            conn.execute("ALTER TABLE passages ADD COLUMN activated INTEGER NOT NULL DEFAULT 0;")
            print("[MIGRATE] Added 'activated' column to passages table.")

    # 3. Ensure synthetic fixtures are marked activated=1
    try:
        conn.execute("UPDATE sources SET activated = 1 WHERE is_synthetic = 1;")
        conn.execute("UPDATE passages SET activated = 1 WHERE is_synthetic = 1;")
    except Exception:
        pass

    conn.commit()
    conn.close()

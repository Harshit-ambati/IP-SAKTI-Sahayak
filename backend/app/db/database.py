"""
Database connection and session management for IP-SAKTI Sahayak.
Uses SQLite with FTS5 virtual table support.
"""

import sqlite3
from pathlib import Path
from typing import Generator, Optional
from ..config import DB_PATH

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_db_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """
    Returns an SQLite connection configured with Row factory and foreign keys.
    """
    target_path = db_path or DB_PATH
    if target_path != Path(":memory:"):
        target_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(target_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    FastAPI dependency yielding a managed database connection.
    """
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


def check_db_health(db_path: Optional[Path] = None) -> dict:
    """
    Validates database connectivity and FTS5 extension functionality.
    """
    try:
        conn = get_db_connection(db_path)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='passages_fts';")
        has_fts = cur.fetchone()[0] > 0
        conn.close()
        return {
            "status": "connected",
            "fts5_supported": True,
            "has_fts_table": bool(has_fts),
        }
    except Exception as e:
        return {
            "status": "error",
            "fts5_supported": False,
            "error": str(e),
        }


def init_database(db_path: Optional[Path] = None) -> None:
    """
    Applies schema.sql to initialize all tables and triggers.
    """
    conn = get_db_connection(db_path)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

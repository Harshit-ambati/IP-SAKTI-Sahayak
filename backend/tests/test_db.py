"""
Tests for SQLite schema, FTS5 virtual table, and privacy table boundaries (Task Su-01).
"""

from pathlib import Path
from app.db.database import get_db_connection, check_db_health


def test_db_health_check(test_db_path: Path):
    health = check_db_health(test_db_path)
    assert health["status"] == "connected"
    assert health["fts5_supported"] is True
    assert health["has_fts_table"] is True


def test_fts5_search_on_passages(test_db_path: Path):
    conn = get_db_connection(test_db_path)
    cur = conn.cursor()

    # Search for traditional knowledge in FTS5 virtual table
    cur.execute("SELECT passage_id, locator FROM passages_fts WHERE passages_fts MATCH 'traditional';")
    results = cur.fetchall()
    conn.close()

    assert len(results) > 0
    assert any("Section 3(p)" in r["locator"] for r in results)


def test_audit_table_schema_privacy(test_db_path: Path):
    conn = get_db_connection(test_db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(audit_events);")
    columns = [row["name"] for row in cur.fetchall()]
    conn.close()

    # Enforce privacy architecture: No confidential formulation text or user prompt columns
    assert "query" not in columns
    assert "query_text" not in columns
    assert "formulation" not in columns
    assert "formulation_title" not in columns
    assert "ingredients" not in columns
    assert "secret" not in columns

    # Required metadata columns must exist
    for expected in ["audit_id", "request_id", "timestamp", "route", "jurisdiction", "evidence_ids", "versions", "status"]:
        assert expected in columns

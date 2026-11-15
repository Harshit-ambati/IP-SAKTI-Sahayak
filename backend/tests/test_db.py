"""
Tests for SQLite schema, FTS5 virtual table, and privacy/activation table boundaries (Task Su-01).
Updated after PR #3 review fixes.
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
    cur.execute("SELECT passage_id, locator FROM passages_fts WHERE passages_fts MATCH 'traditional';")
    results = cur.fetchall()
    conn.close()
    assert len(results) > 0
    assert any("Section 3(p)" in r["locator"] for r in results)


def test_activation_gate_schema_exists(test_db_path: Path):
    """FIX-3: Both sources and passages tables must have an 'activated' column."""
    conn = get_db_connection(test_db_path)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(sources);")
    source_cols = [row["name"] for row in cur.fetchall()]
    assert "activated" in source_cols, "sources table is missing the 'activated' gate column."

    cur.execute("PRAGMA table_info(passages);")
    passage_cols = [row["name"] for row in cur.fetchall()]
    assert "activated" in passage_cols, "passages table is missing the 'activated' gate column."

    conn.close()


def test_preliminary_corpus_rows_are_not_activated(test_db_path: Path):
    """FIX-3: Real preliminary corpus rows (REAL-*) must have activated=0."""
    conn = get_db_connection(test_db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT source_id, activated FROM sources WHERE source_id LIKE 'REAL-%';"
    )
    real_rows = cur.fetchall()
    conn.close()

    for row in real_rows:
        assert row["activated"] == 0, (
            f"Preliminary corpus source {row['source_id']} has activated=1 but was not reviewed. "
            "Real corpus rows must stay at activated=0 until Harshit's corpus activation gate."
        )


def test_synthetic_fixtures_are_activated(test_db_path: Path):
    """Synthetic test fixtures must have activated=1 so they appear in public endpoints."""
    conn = get_db_connection(test_db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT source_id, activated FROM sources WHERE is_synthetic = 1;"
    )
    synth_rows = cur.fetchall()
    conn.close()

    assert len(synth_rows) > 0, "No synthetic sources found in database."
    for row in synth_rows:
        assert row["activated"] == 1, (
            f"Synthetic source {row['source_id']} has activated=0. "
            "Synthetic test fixtures must be activated=1 for public endpoint visibility."
        )


def test_audit_table_schema_privacy(test_db_path: Path):
    conn = get_db_connection(test_db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(audit_events);")
    columns = [row["name"] for row in cur.fetchall()]
    conn.close()

    # Strict privacy: NO formulation text, query, or secrets in audit_events
    for forbidden in ["query", "query_text", "formulation", "formulation_title", "ingredients", "secret"]:
        assert forbidden not in columns, (
            f"Privacy violation: audit_events has column '{forbidden}' which must not exist."
        )

    for expected in ["audit_id", "request_id", "timestamp", "route", "jurisdiction", "evidence_ids", "versions", "status"]:
        assert expected in columns, f"Required audit column '{expected}' is missing."


def test_database_migration_adds_activated_column(tmp_path: Path):
    """
    Simulates an existing database from before d961cc7 (missing 'activated' column)
    and verifies that run_migrations idempotently adds the column and activates synthetic rows.
    """
    from app.db.migrate import run_migrations

    legacy_db = tmp_path / "legacy.db"
    conn = get_db_connection(legacy_db)
    # Create tables without 'activated' column
    conn.execute("""
        CREATE TABLE sources (
            source_id TEXT PRIMARY KEY,
            topic TEXT NOT NULL,
            authority TEXT NOT NULL,
            title TEXT NOT NULL,
            official_url TEXT NOT NULL,
            format TEXT NOT NULL DEFAULT 'html',
            role TEXT NOT NULL DEFAULT 'primary',
            priority TEXT NOT NULL DEFAULT 'required',
            verification_status TEXT NOT NULL,
            review_note TEXT,
            is_synthetic INTEGER NOT NULL DEFAULT 0
        );
    """)
    conn.execute("""
        CREATE TABLE passages (
            passage_id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL REFERENCES sources(source_id),
            jurisdiction TEXT NOT NULL,
            authority TEXT NOT NULL,
            document_title TEXT NOT NULL,
            locator TEXT NOT NULL,
            paraphrased_content TEXT NOT NULL,
            source_url TEXT NOT NULL,
            source_type TEXT NOT NULL DEFAULT 'statute',
            review_status TEXT NOT NULL,
            review_note TEXT,
            is_synthetic INTEGER NOT NULL DEFAULT 0
        );
    """)
    # Insert a synthetic record
    conn.execute("""
        INSERT INTO sources (source_id, topic, authority, title, official_url, verification_status, is_synthetic)
        VALUES ('SYNTH-LEGACY-001', 'patents', 'Test', 'Test Title', 'http://example.com', 'verified', 1);
    """)
    conn.commit()
    conn.close()

    # Verify column is missing initially
    conn = get_db_connection(legacy_db)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(sources);")
    cols = {r["name"] for r in cur.fetchall()}
    assert "activated" not in cols
    conn.close()

    # Run migration
    run_migrations(legacy_db)

    # Verify column now exists and synthetic record is activated
    conn = get_db_connection(legacy_db)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(sources);")
    cols = {r["name"] for r in cur.fetchall()}
    assert "activated" in cols

    cur.execute("PRAGMA table_info(passages);")
    cols_pas = {r["name"] for r in cur.fetchall()}
    assert "activated" in cols_pas

    cur.execute("SELECT activated FROM sources WHERE source_id = 'SYNTH-LEGACY-001';")
    row = cur.fetchone()
    assert row["activated"] == 1
    conn.close()

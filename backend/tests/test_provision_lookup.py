"""Exercise the H-02 lookup with staged corpus data and isolated test records."""

import json
import sqlite3
import subprocess
import sys
from contextlib import closing
from pathlib import Path

from backend.app.db.init_db import seed_fixtures, seed_real_corpus_if_available
from backend.app.provision_lookup import lookup


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "backend/app/db/schema.sql"


def test_staged_corpus_abstains_through_cli(tmp_path):
    database = tmp_path / "staged corpus.sqlite"
    with closing(sqlite3.connect(database)) as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        seed_fixtures(conn)
        seed_real_corpus_if_available(conn)
        assert conn.execute(
            "SELECT is_synthetic, activated FROM passages WHERE passage_id = 'PASS-002'"
        ).fetchone() == (0, 0)
    run = subprocess.run(
        [sys.executable, "-B", "-m", "backend.app.provision_lookup", "--db",
         str(database), "--jurisdiction", "India", "PASS-002"],
        cwd=ROOT, capture_output=True, check=True, text=True,
    )
    result = json.loads(run.stdout)
    assert result["status"] == "abstained"
    assert result["claims"] == result["evidence"] == []
    assert "No approved, active evidence" in result["limitations"][0]


def test_lookup_keeps_provision_locator_and_excludes_ineligible_records():
    with closing(sqlite3.connect(":memory:")) as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        conn.executemany(
            """
            INSERT INTO sources (
                source_id, topic, authority, title, official_url, verification_status, activated, is_synthetic
            ) VALUES (?, 'test', 'Test only', 'Fixture', 'https://example.invalid/fixture', 'fixture', ?, ?)
            """,
            [("ACTIVE", 1, 0), ("INACTIVE", 0, 0), ("SYNTHETIC", 1, 1)],
        )
        conn.executemany(
            """
            INSERT INTO passages (
                passage_id, source_id, jurisdiction, authority, document_title, locator,
                paraphrased_content, source_url, review_status, activated, is_synthetic
            ) VALUES (?, ?, ?, 'Test only', 'Fixture', 'Clause 7',
                      'The library opens at nine.', 'https://example.invalid/fixture', ?, ?, ?)
            """,
            [
                ("PASS-901", "ACTIVE", "India", "approved", 1, 0),
                ("PASS-902", "ACTIVE", "International", "approved", 1, 0),
                ("PASS-903", "ACTIVE", "India", "pending", 1, 0),
                ("PASS-904", "ACTIVE", "India", "approved", 0, 0),
                ("PASS-905", "INACTIVE", "India", "approved", 1, 0),
                ("PASS-906", "SYNTHETIC", "India", "approved", 1, 0),
                ("PASS-907", "ACTIVE", "India", "approved", 1, 1),
            ],
        )

        response = lookup(conn, "India", "library opens")
        assert response["status"] == "answered"
        assert response["claims"] == [
            {"text": "The library opens at nine.", "evidence_ids": ["PASS-901"]}
        ]
        evidence, = response["evidence"]
        assert evidence["passage_id"] == "PASS-901"
        assert evidence["locator"] == "Clause 7"
        assert evidence["source_url"] == "https://example.invalid/fixture"
        assert evidence["corpus_version"] == response["corpus_version"]
        assert lookup(conn, "international_overview", "library opens")["claims"][0][
            "evidence_ids"
        ] == ["PASS-902"]
        assert lookup(conn, "India", "PASS-902")["status"] == "abstained"
        assert lookup(conn, "India", 'unrelated" OR "library')["status"] == "abstained"

        conn.execute("UPDATE passages SET review_status = 'approved' WHERE passage_id = 'PASS-903'")
        assert lookup(conn, "India", "library opens")["status"] == "clarify"
        assert lookup(conn, "India", "pass-901")["status"] == "answered"

"""H-02 local lookup for a named provision or an exact keyword phrase."""

import argparse
import hashlib
import json
import re
import sqlite3
import uuid
from contextlib import closing
from pathlib import Path


JURISDICTIONS = {"India": "India", "international_overview": "International"}


def lookup(conn: sqlite3.Connection, jurisdiction: str, phrase: str) -> dict:
    """Return an H-01 answer object for a provision lookup, without generation."""
    phrase = phrase.strip()
    if not 1 <= len(phrase) <= 200 or not any(char.isalnum() for char in phrase):
        raise ValueError("Enter a passage ID or keyword phrase of 1–200 characters.")
    if jurisdiction not in JURISDICTIONS:
        raise ValueError("Select India or international_overview.")

    passage_id = phrase.upper() if re.fullmatch(r"PASS-\d+", phrase, re.IGNORECASE) else ""
    literal = '{document_title locator paraphrased_content} : "' + phrase.replace('"', '""') + '"'
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    rows = cursor.execute(
        """
        SELECT p.passage_id, p.source_id, p.document_title, p.source_url, p.locator,
               p.paraphrased_content,
               CASE WHEN ? <> '' THEN upper(p.passage_id) = ?
                    ELSE p.rowid IN (
                        SELECT rowid FROM passages_fts WHERE passages_fts MATCH ?
                    )
               END AS matched
        FROM passages p JOIN sources s ON s.source_id = p.source_id
        WHERE p.jurisdiction = ? AND p.review_status = 'approved'
          AND p.activated = 1 AND s.activated = 1
          AND p.is_synthetic = 0 AND s.is_synthetic = 0
          AND length(trim(p.locator)) > 0
          AND length(trim(p.paraphrased_content)) > 0
          AND p.source_url LIKE 'https://_%'
        ORDER BY p.passage_id
        """,
        (passage_id, passage_id, literal, JURISDICTIONS[jurisdiction]),
    ).fetchall()
    snapshot = json.dumps([tuple(row)[:-1] for row in rows], ensure_ascii=False).encode("utf-8")
    corpus_version = "h02-" + hashlib.sha256(snapshot).hexdigest()
    result = {
        "contract_version": "1.0.0",
        "request_id": str(uuid.uuid4()),
        "status": "abstained",
        "jurisdiction": jurisdiction,
        "language": "en",
        "route": "unknown",
        "assumptions": [],
        "claims": [],
        "evidence": [],
        "limitations": ["No approved, active evidence is available for this lookup."],
        "corpus_version": corpus_version,
        "model_version": "none",
    }
    matches = [row for row in rows if row["matched"]]
    if not matches:
        return result
    if len(matches) != 1:
        result["status"] = "clarify"
        result["limitations"] = ["Multiple provisions match. Enter the specific passage ID."]
        return result

    row = matches[0]
    result["status"] = "answered"
    result["limitations"] = [
        "Reviewed corpus paraphrase. Consult the official source at the cited locator.",
        "This lookup does not assess how a provision applies to a specific formulation.",
    ]
    result["claims"] = [{
        "text": row["paraphrased_content"], "evidence_ids": [row["passage_id"]]
    }]
    result["evidence"] = [{
        "passage_id": row["passage_id"],
        "source_id": row["source_id"],
        "jurisdiction": jurisdiction,
        "source_title": row["document_title"],
        "source_url": row["source_url"],
        "locator": row["locator"],
        "text": row["paraphrased_content"],
        "review_status": "approved",
        "corpus_version": corpus_version,
    }]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, type=Path, help="Path to the staged SQLite corpus")
    parser.add_argument("--jurisdiction", required=True, choices=JURISDICTIONS)
    parser.add_argument("phrase", help="Passage ID, provision locator, or precise keyword phrase")
    args = parser.parse_args()
    try:
        uri = args.db.resolve(strict=True).as_uri() + "?mode=ro"
        with closing(sqlite3.connect(uri, uri=True)) as conn:
            result = lookup(conn, args.jurisdiction, args.phrase)
    except (OSError, sqlite3.Error, ValueError) as exc:
        parser.exit(2, f"Provision lookup failed: {exc}\n")
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()

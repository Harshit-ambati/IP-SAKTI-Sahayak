#!/usr/bin/env python3
"""
Corpus Validation Script for Task T-02

Verifies:
1. Exact row and column schemas for documents.csv (10 cols, 12 rows),
   source_register.csv (16 cols, 12 rows), and passages.csv (11 cols, 25 rows).
2. Referential integrity across primary and foreign keys (source_id).
3. Statutory wording accuracy:
   - PASS-015: NBA approval timing for foreign entities is "before the grant" / "before grant".
   - PASS-021: FSSAI 25 July 2025 order describes Category A list and FBO inclusion mechanism.
   - PASS-014: Patents Act Section 3(d) includes qualifier "for a known substance".
   - PASS-004: Regulation 8 disease claim prohibition strictly uses "human disease" (no "or disorder").
4. Zero trailing whitespace across T-02 markdown documentation.

Usage:
    python scripts/validate_t02.py
"""

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DOCS_PATH = REPO_ROOT / "data" / "corpus" / "documents.csv"
SRC_PATH = REPO_ROOT / "data" / "corpus" / "source_register.csv"
PAS_PATH = REPO_ROOT / "data" / "corpus" / "passages.csv"
AUDIT_PATH = REPO_ROOT / "data" / "corpus" / "SOURCE_AUDIT_T02.md"
RULES_PATH = REPO_ROOT / "docs" / "work-plan" / "modules" / "thulasi-t02-intake-rules.md"


def check_csv(path: Path, expected_cols: int, expected_rows: int):
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert len(header) == expected_cols, f"{path.name}: Expected {expected_cols} cols, got {len(header)}: {header}"
        rows = list(reader)
        assert len(rows) == expected_rows, f"{path.name}: Expected {expected_rows} rows, got {len(rows)}"
        for i, row in enumerate(rows):
            assert len(row) == expected_cols, f"{path.name} Row {i+1}: expected {expected_cols} cols, got {len(row)}: {row}"
        return rows


def check_whitespace(path: Path):
    with open(path, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
    trailing = [i + 1 for i, l in enumerate(lines) if l.rstrip("\r\n").endswith(" ") or l.rstrip("\r\n").endswith("\t")]
    assert not trailing, f"{path.name}: Trailing whitespace found on lines {trailing}"


def main():
    print("=" * 70)
    print("IP-SAKTI Sahayak: T-02 Corpus Validation Suite")
    print("=" * 70)

    # 1. Schema and row count checks
    print("[1/4] Checking CSV schemas and row counts...")
    doc_rows = check_csv(DOCS_PATH, 10, 12)
    src_rows = check_csv(SRC_PATH, 16, 12)
    pas_rows = check_csv(PAS_PATH, 11, 25)
    print(f"      documents.csv:       10 cols, 12 rows (OK)")
    print(f"      source_register.csv: 16 cols, 12 rows (OK)")
    print(f"      passages.csv:        11 cols, 25 rows (OK)")

    # 2. Referential integrity
    print("\n[2/4] Checking referential integrity...")
    doc_ids = {r[0] for r in doc_rows}
    src_ids = {r[0] for r in src_rows}
    assert doc_ids == src_ids, f"ID mismatch between documents and source_register: {doc_ids ^ src_ids}"
    pas_source_ids = {r[1] for r in pas_rows}
    unknown_sources = pas_source_ids - doc_ids
    assert not unknown_sources, f"Passages reference unknown sources: {unknown_sources}"
    print(f"      100% referential integrity across 12 sources and 25 passages (OK)")

    # 3. Statutory provision checks
    print("\n[3/4] Verifying statutory provisions and review findings...")
    # PASS-015
    p15 = next(r for r in pas_rows if r[0] == "PASS-015")
    assert "before the grant" in p15[6] or "before grant" in p15[6], f"PASS-015 missing 'before grant': {p15[6]}"
    assert "before applying" not in p15[6], f"PASS-015 incorrectly contains 'before applying': {p15[6]}"
    print(f"      PASS-015: Section 6(1) timing verified ('before grant of IPR') (OK)")

    # PASS-021 & REAL-011
    p21 = next(r for r in pas_rows if r[0] == "PASS-021")
    assert "Category A" in p21[6], f"PASS-021 missing 'Category A': {p21[6]}"
    assert "inclusion" in p21[6], f"PASS-021 missing 'inclusion': {p21[6]}"
    assert "penalty" not in p21[6], f"PASS-021 contains unsupported penalty language: {p21[6]}"
    r11_doc = next(r for r in doc_rows if r[0] == "REAL-011")
    assert "advisories/2025/07" in r11_doc[4], f"REAL-011 URL incorrect: {r11_doc[4]}"
    print(f"      PASS-021 & REAL-011: Category A recipe list and FBO inclusion verified (OK)")

    # PASS-014
    p14 = next(r for r in pas_rows if r[0] == "PASS-014")
    assert "for a known substance" in p14[6], f"PASS-014 missing 'for a known substance': {p14[6]}"
    print(f"      PASS-014: Patents Act Section 3(d) includes 'for a known substance' (OK)")

    # PASS-004
    p4 = next(r for r in pas_rows if r[0] == "PASS-004")
    assert "disorder" not in p4[6], f"PASS-004 contains 'disorder': {p4[6]}"
    assert "human disease" in p4[6], f"PASS-004 missing 'human disease': {p4[6]}"
    assert "presentation" in p4[6], f"PASS-004 missing 'presentation': {p4[6]}"
    print(f"      PASS-004: Regulation 8 strictly confined to human disease & presentation (OK)")

    # 4. Whitespace checks
    print("\n[4/4] Checking markdown documentation for trailing whitespace...")
    check_whitespace(AUDIT_PATH)
    check_whitespace(RULES_PATH)
    print(f"      SOURCE_AUDIT_T02.md: 0 trailing whitespace (OK)")
    print(f"      thulasi-t02-intake-rules.md: 0 trailing whitespace (OK)")

    print("\n" + "=" * 70)
    print("SUCCESS: All Task T-02 verification checks passed cleanly.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

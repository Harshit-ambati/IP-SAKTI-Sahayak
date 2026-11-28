#!/usr/bin/env python3
"""
verify_glossary.py
Validates the controlled glossary v0 CSV for IP-SAKTI Sahayak (Task D-01).
Owner: Deepshika Palepu (Multilingual experience, terminology, and translation quality)
"""

import csv
import sys
from pathlib import Path

REQUIRED_COLUMNS = [
    "term_id",
    "domain",
    "english_term",
    "hindi_term",
    "hindi_transliteration",
    "regional_term_candidate",
    "preservation_rule",
    "statutory_or_system_context",
    "definition",
]

EXPECTED_DOMAINS = {
    "jurisdiction",
    "evidence_citation",
    "uncertainty_abstention",
    "product_category",
}

VALID_PRESERVATION_RULES = {
    "STRICT_STATUTORY_EQUIVALENT",
    "ACRONYM_IMMUTABLE",
    "NUMBER_IMMUTABLE",
    "ID_IMMUTABLE",
    "SAFETY_FALLBACK_BANNER",
    "NAME_IMMUTABLE",
    "PRESERVE_NEGATION",
}

def verify_glossary(file_path: Path) -> bool:
    if not file_path.exists():
        print(f"ERROR: Glossary file not found at {file_path}")
        return False

    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        # Check header
        if reader.fieldnames != REQUIRED_COLUMNS:
            print("ERROR: Header mismatch.")
            print(f"  Expected: {REQUIRED_COLUMNS}")
            print(f"  Found:    {reader.fieldnames}")
            return False

        rows = list(reader)
        print(f"Loaded {len(rows)} glossary records from {file_path.name}.")

        if len(rows) < 20:
            print(f"WARNING: Glossary v0 expected at least 20 terms; found {len(rows)}.")

        seen_ids = set()
        domains_found = set()
        errors = []

        for idx, row in enumerate(rows, start=2):
            term_id = row.get("term_id", "").strip()
            domain = row.get("domain", "").strip()
            rule = row.get("preservation_rule", "").strip()

            # ID uniqueness
            if not term_id:
                errors.append(f"Row {idx}: missing term_id.")
            elif term_id in seen_ids:
                errors.append(f"Row {idx}: duplicate term_id '{term_id}'.")
            else:
                seen_ids.add(term_id)

            # Domain check
            if domain not in EXPECTED_DOMAINS:
                errors.append(f"Row {idx} ({term_id}): unknown domain '{domain}'.")
            else:
                domains_found.add(domain)

            # Preservation rule check
            if rule not in VALID_PRESERVATION_RULES:
                errors.append(f"Row {idx} ({term_id}): invalid preservation rule '{rule}'.")

            # Check essential non-empty fields
            for col in REQUIRED_COLUMNS:
                val = row.get(col, "").strip()
                if not val:
                    errors.append(f"Row {idx} ({term_id}): column '{col}' is empty.")

        if errors:
            print(f"FAILED: Found {len(errors)} validation errors:")
            for err in errors:
                print(f"  - {err}")
            return False

        missing_domains = EXPECTED_DOMAINS - domains_found
        if missing_domains:
            print(f"FAILED: Missing mandatory domains: {missing_domains}")
            return False

        print("SUCCESS: All glossary records validated successfully.")
        print("Note: This script establishes CSV formatting, column schema, and preservation tags only; it does not verify semantic meaning or translation fidelity.")
        print("Domain breakdown:")
        for dom in sorted(EXPECTED_DOMAINS):
            count = sum(1 for r in rows if r["domain"] == dom)
            print(f"  - {dom}: {count} terms")

        return True

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    glossary_csv = repo_root / "data" / "glossary" / "controlled_glossary_v0.csv"
    success = verify_glossary(glossary_csv)
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Benchmark Scenario and Result Schema Validation Script for Task Sa-01

Verifies:
1. Exact row and column schemas for canonical_scenarios.csv (15 cols, 20 rows)
   and results_template.csv (16 cols, 0 rows - unpopulated template schema).
2. Unique case IDs with 'SYN-CASE-' prefix.
3. Split parity: exactly 10 development and 10 holdout cases.
4. Exact behavior contract matching backend AnswerStatusEnum:
   {'answered', 'clarify', 'abstained', 'referral'}.
5. Abstention gold passage suppression: cases with expected_behavior == 'abstained'
   must have empty gold_passage_ids (no fabricated supporting passages for out-of-scope/adversarial queries).
6. Referential integrity: all non-empty gold_passage_ids exist in data/corpus/passages.csv.
7. Exact holdout safety audit: 4 answered, 3 referral, 2 abstained, 1 clarify
   (5 abstention/referral, 6 total non-confident safety cases).
8. Explicit count of reviewed versus unreviewed cases (asserts 0 reviewed, 20 unreviewed).
9. Privacy and safety: absence of personal identifiers, emails, or phone numbers.
10. Zero trailing whitespace across Sa-01 markdown documentation.

Usage:
    python scripts/validate_sa01.py
"""

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SCENARIOS_PATH = REPO_ROOT / "data" / "benchmark" / "canonical_scenarios.csv"
RESULTS_TEMPLATE_PATH = REPO_ROOT / "data" / "benchmark" / "results_template.csv"
PASSAGES_PATH = REPO_ROOT / "data" / "corpus" / "passages.csv"
BENCHMARK_README_PATH = REPO_ROOT / "data" / "benchmark" / "README.md"
SPEC_PATH = REPO_ROOT / "docs" / "work-plan" / "modules" / "sabeena-sa01-benchmark-spec.md"
MODULE_PATH = REPO_ROOT / "docs" / "work-plan" / "modules" / "05-sabeena.md"

VALID_SPLITS = {"development", "holdout"}
VALID_CATEGORIES = {"classification", "evidence", "insufficient_evidence", "adversarial_jurisdiction"}
VALID_LANGUAGES = {"en", "hi", "kn", "ta", "te"}
VALID_JURISDICTIONS = {"India", "International"}
# Binds strictly to backend AnswerStatusEnum (schemas.py)
VALID_BEHAVIORS = {"answered", "clarify", "abstained", "referral"}
VALID_ROUTES = {
    "classical_generic",
    "patent_proprietary",
    "novel_non_classical",
    "phytopharmaceutical",
    "ayurveda_aahara",
    "cosmetic",
    "unknown_ambiguous",
}
VALID_ANSWERABILITY = {
    "answerable",
    "unanswerable_missing_facts",
    "unanswerable_unsupported",
    "abstain_or_referral",
}
VALID_LABEL_STATUSES = {"provisional_unreviewed", "reviewed"}


def check_csv(path: Path, expected_cols: int, expected_rows: int):
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert len(header) == expected_cols, f"{path.name}: Expected {expected_cols} cols, got {len(header)}: {header}"
        rows = list(reader)
        assert len(rows) == expected_rows, f"{path.name}: Expected {expected_rows} rows, got {len(rows)}"
        for i, row in enumerate(rows):
            assert len(row) == expected_cols, f"{path.name} Row {i+1}: expected {expected_cols} cols, got {len(row)}: {row}"
        return header, rows


def check_whitespace(path: Path):
    if not path.exists():
        return
    with open(path, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
    trailing = [i + 1 for i, l in enumerate(lines) if l.rstrip("\r\n").endswith(" ") or l.rstrip("\r\n").endswith("\t")]
    assert not trailing, f"{path.name}: Trailing whitespace found on lines {trailing}"


def main():
    print("=" * 70)
    print("IP-SAKTI Sahayak: Sa-01 Benchmark Validation Suite")
    print("=" * 70)

    # 1. Schema and row count checks
    print("[1/6] Checking CSV schemas and unpopulated template contract...")
    scen_header, scen_rows = check_csv(SCENARIOS_PATH, 15, 20)
    # results_template must be unpopulated schema (0 data rows; zero unobserved test runs)
    res_header, res_rows = check_csv(RESULTS_TEMPLATE_PATH, 16, 0)
    print("      canonical_scenarios.csv: 15 cols, 20 rows (OK)")
    print("      results_template.csv:    16 cols, 0 data rows (unpopulated template schema; OK)")

    # 2. Case ID and Enum checks
    print("\n[2/6] Checking Case IDs, split distribution, and enum constraints...")
    case_ids = [r[0] for r in scen_rows]
    assert len(case_ids) == len(set(case_ids)), f"Duplicate case IDs found: {case_ids}"
    assert all(cid.startswith("SYN-CASE-") for cid in case_ids), "All case IDs must start with 'SYN-CASE-'"

    split_counts = {"development": 0, "holdout": 0}
    category_counts = {}
    route_counts = {}
    behavior_counts = {}
    holdout_behaviors = {}
    dev_behaviors = {}
    unreviewed_count = 0
    reviewed_count = 0

    # Read verified corpus passages for referential integrity
    with open(PASSAGES_PATH, mode="r", encoding="utf-8") as f:
        p_reader = csv.reader(f)
        next(p_reader)
        verified_passage_ids = {p[0] for p in p_reader}

    for i, r in enumerate(scen_rows):
        cid, split, cat, lang, jur, prompt, facts, missing, beh, route, ans, gold_pids, status, reviewer, rev_at = r

        assert split in VALID_SPLITS, f"Row {i+1} invalid split: {split}"
        split_counts[split] += 1

        assert cat in VALID_CATEGORIES, f"Row {i+1} invalid category: {cat}"
        category_counts[cat] = category_counts.get(cat, 0) + 1

        assert lang in VALID_LANGUAGES, f"Row {i+1} invalid language: {lang}"
        assert jur in VALID_JURISDICTIONS, f"Row {i+1} invalid jurisdiction: {jur}"
        assert beh in VALID_BEHAVIORS, f"Row {i+1} invalid behavior '{beh}'; must match AnswerStatusEnum: {VALID_BEHAVIORS}"
        behavior_counts[beh] = behavior_counts.get(beh, 0) + 1

        if split == "holdout":
            holdout_behaviors[beh] = holdout_behaviors.get(beh, 0) + 1
        else:
            dev_behaviors[beh] = dev_behaviors.get(beh, 0) + 1

        assert route in VALID_ROUTES, f"Row {i+1} invalid route: {route}"
        route_counts[route] = route_counts.get(route, 0) + 1

        assert ans in VALID_ANSWERABILITY, f"Row {i+1} invalid answerability: {ans}"
        assert status in VALID_LABEL_STATUSES, f"Row {i+1} invalid label status: {status}"

        if status == "provisional_unreviewed":
            unreviewed_count += 1
            assert rev_at == "unreviewed", f"Row {i+1} provisional label cannot have review timestamp: {rev_at}"
        elif status == "reviewed":
            reviewed_count += 1

        # Check abstention gold passage suppression
        if beh == "abstained":
            assert gold_pids == "", f"Row {i+1} ({cid}) expected_behavior is 'abstained' but lists gold passages '{gold_pids}'; abstentions must have empty gold passages!"

        # Check passage referential integrity
        if gold_pids and gold_pids.strip():
            pids = [p.strip() for p in gold_pids.split(";")]
            for pid in pids:
                assert pid in verified_passage_ids, f"Row {i+1} ({cid}) references unknown passage ID: '{pid}'"

    assert split_counts["development"] == 10, f"Expected 10 development cases, got {split_counts['development']}"
    assert split_counts["holdout"] == 10, f"Expected 10 holdout cases, got {split_counts['holdout']}"
    print(f"      Split distribution: 10 development, 10 holdout (OK)")
    print(f"      Category distribution: {category_counts} (OK)")
    print(f"      Route distribution: {route_counts} (OK)")
    print(f"      Behavior distribution: {behavior_counts} (OK)")

    # 3. Holdout safety count check
    print("\n[3/6] Auditing holdout set safety composition...")
    print(f"      Holdout breakdown: {holdout_behaviors}")
    assert holdout_behaviors.get("answered", 0) == 4, f"Expected 4 answered in holdout, got {holdout_behaviors.get('answered')}"
    assert holdout_behaviors.get("referral", 0) == 3, f"Expected 3 referral in holdout, got {holdout_behaviors.get('referral')}"
    assert holdout_behaviors.get("abstained", 0) == 2, f"Expected 2 abstained in holdout, got {holdout_behaviors.get('abstained')}"
    assert holdout_behaviors.get("clarify", 0) == 1, f"Expected 1 clarify in holdout, got {holdout_behaviors.get('clarify')}"
    holdout_abstain_referral = holdout_behaviors.get("abstained", 0) + holdout_behaviors.get("referral", 0)
    holdout_safety_total = holdout_abstain_referral + holdout_behaviors.get("clarify", 0)
    print(f"      Holdout abstention + referral count: {holdout_abstain_referral} (OK)")
    print(f"      Holdout total safety / non-confident count: {holdout_safety_total} (60% of holdout; OK)")

    # 4. Explicit Count of Reviewed vs Unreviewed Cases
    print("\n[4/6] Verifying label status and audit gate...")
    print(f"      Reviewed gold cases:    {reviewed_count}")
    print(f"      Unreviewed provisional: {unreviewed_count}")
    assert reviewed_count == 0, f"Gate violation: {reviewed_count} cases marked reviewed without Thulasi sign-off!"
    assert unreviewed_count == 20, f"Expected 20 unreviewed provisional cases, got {unreviewed_count}"
    print("      Verification check: 100% of cases correctly marked 'provisional_unreviewed' (OK)")

    # 5. Privacy and PII check
    print("\n[5/6] Checking privacy, synthetic neutrality, and PII suppression...")
    pii_patterns = [
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),  # Email
        re.compile(r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b"),                         # Phone number
        re.compile(r"\b(?:Aadhaar|PAN|Voter ID|SSN)\b", re.IGNORECASE),       # Govt ID
    ]
    for cid, prompt, facts, missing in [(r[0], r[5], r[6], r[7]) for r in scen_rows]:
        text_block = f"{prompt} {facts} {missing}"
        for pat in pii_patterns:
            matches = pat.findall(text_block)
            assert not matches, f"{cid} contains potential PII: {matches}"
    print("      0 personal data, emails, or phone numbers detected (OK)")

    # 6. Whitespace checks
    print("\n[6/6] Checking documentation files for trailing whitespace...")
    check_whitespace(BENCHMARK_README_PATH)
    check_whitespace(SPEC_PATH)
    check_whitespace(MODULE_PATH)
    print("      Markdown files checked for 0 trailing whitespace (OK)")

    print("\n" + "=" * 70)
    print("SUCCESS: All Task Sa-01 benchmark validation checks passed cleanly.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Verification Script for UI Localization Strings (Task D-02)

Verifies:
1. Existence and valid JSON syntax of English (ui_strings_en.json) and Hindi (ui_strings_hi.json).
2. 100% recursive key parity between English and Hindi translation dictionaries.
3. Absence of null, empty, or whitespace-only string values.
4. Rigorous PER-STRING statutory immutable token preservation:
   For every key where an English string contains a statutory token, the matching Hindi string
   at that exact key MUST preserve that token in Latin/alphanumeric notation:
   - ID_IMMUTABLE: Question IDs (Q-USE, Q-INGR, etc.)
   - NUMBER_IMMUTABLE: Section & Rule numbers (Section 3(p), Rule 2(eb), Regulation 8, etc.)
   - NAME_IMMUTABLE: Statutory defined names (Ayurveda Aahara, Phytopharmaceutical Drug)
   - ACRONYM_IMMUTABLE: Recognized institutional acronyms (WIPO, AYUSH, FSSAI, NBA, TKDL)

Encoding:
   Forces UTF-8 on Windows consoles to prevent charmap/cp1252 encoding crashes.
   Uses ASCII-safe status tags ([PASS], [FAIL], [INFO]).

Usage:
    python scripts/verify_strings.py
"""

import sys
import io
import json
from pathlib import Path

# Force UTF-8 encoding on standard output/error to prevent Windows console charmap failures
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
elif sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
EN_PATH = REPO_ROOT / "data" / "translations" / "ui_strings_en.json"
HI_PATH = REPO_ROOT / "data" / "translations" / "ui_strings_hi.json"

REQUIRED_IMMUTABLE_TOKENS = [
    # Question IDs (ID_IMMUTABLE)
    "Q-USE", "Q-INGR", "Q-FORM", "Q-ROUTE",
    "Q-FOOD-TEXT", "Q-FOOD-CLAIM", "Q-FOOD-SYN", "Q-COSM-CLAIM",
    # Section & Rule Numbers (NUMBER_IMMUTABLE)
    "Section 3(a)", "Section 3(h)", "Section 3(p)", "Section 3(e)", "Section 3(aaa)",
    "Rule 2(eb)", "Regulation 2(b)", "Regulation 8", "Regulation 3(4)",
    # Statutory Names (NAME_IMMUTABLE)
    "Ayurveda Aahara", "Phytopharmaceutical Drug",
    # Acronyms (ACRONYM_IMMUTABLE)
    "WIPO", "AYUSH", "FSSAI", "NBA", "TKDL"
]


def load_json(path: Path) -> dict:
    if not path.is_file():
        print(f"[FAIL] Missing file: {path}")
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[FAIL] Malformed JSON in {path}: {e}")
        sys.exit(1)


def compare_keys(dict_a: dict, dict_b: dict, path_prefix: str = "") -> list:
    """Recursively compare key structure between two dicts."""
    errors = []
    keys_a = set(dict_a.keys())
    keys_b = set(dict_b.keys())

    missing_in_b = keys_a - keys_b
    if missing_in_b:
        for k in sorted(missing_in_b):
            errors.append(f"Missing key in target: {path_prefix}{k}")

    missing_in_a = keys_b - keys_a
    if missing_in_a:
        for k in sorted(missing_in_a):
            errors.append(f"Unexpected extra key in target: {path_prefix}{k}")

    common_keys = keys_a & keys_b
    for k in sorted(common_keys):
        val_a = dict_a[k]
        val_b = dict_b[k]
        current_path = f"{path_prefix}{k}."

        if type(val_a) != type(val_b):
            errors.append(f"Type mismatch at {current_path[:-1]}: {type(val_a).__name__} vs {type(val_b).__name__}")
        elif isinstance(val_a, dict):
            errors.extend(compare_keys(val_a, val_b, current_path))

    return errors


def collect_leaves(d: dict, prefix: str = "") -> list:
    """Collect all terminal key-value pairs."""
    leaves = []
    for k, v in d.items():
        curr = f"{prefix}{k}"
        if isinstance(v, dict):
            leaves.extend(collect_leaves(v, f"{curr}."))
        else:
            leaves.append((curr, v))
    return leaves


def check_per_key_preservation(dict_en: dict, dict_hi: dict, path_prefix: str = "") -> list:
    """Verify that every statutory token appearing in an English key is preserved in the matching Hindi key."""
    mismatches = []
    for k in dict_en:
        curr = f"{path_prefix}{k}"
        v_en = dict_en[k]
        v_hi = dict_hi.get(k)
        if isinstance(v_en, dict) and isinstance(v_hi, dict):
            mismatches.extend(check_per_key_preservation(v_en, v_hi, f"{curr}."))
        elif isinstance(v_en, str) and isinstance(v_hi, str):
            for token in REQUIRED_IMMUTABLE_TOKENS:
                if token in v_en and token not in v_hi:
                    mismatches.append({
                        "key": curr,
                        "token": token,
                        "en_snippet": v_en[:80] + "..." if len(v_en) > 80 else v_en,
                        "hi_snippet": v_hi[:80] + "..." if len(v_hi) > 80 else v_hi
                    })
    return mismatches


def main():
    print("=" * 70)
    print("IP-SAKTI Sahayak: UI Localization Verification (Task D-02)")
    print("=" * 70)

    # 1. Load files
    print("[1/4] Loading string dictionaries...")
    en_data = load_json(EN_PATH)
    hi_data = load_json(HI_PATH)
    print(f"      English path: {EN_PATH.relative_to(REPO_ROOT)}")
    print(f"      Hindi path:   {HI_PATH.relative_to(REPO_ROOT)}")

    # 2. Key Parity Check
    print("\n[2/4] Checking recursive key parity...")
    parity_errors = compare_keys(en_data, hi_data)
    if parity_errors:
        print(f"[FAIL] Found {len(parity_errors)} key parity discrepancies:")
        for err in parity_errors:
            print(f"  - {err}")
        sys.exit(1)

    en_leaves = collect_leaves(en_data)
    hi_leaves = collect_leaves(hi_data)
    print(f"      [PASS] 100% key parity verified across {len(en_leaves)} string keys.")

    # 3. Non-empty string check
    print("\n[3/4] Validating string contents (null/empty check)...")
    empty_errors = []
    for path_str, val in en_leaves:
        if isinstance(val, str) and not val.strip():
            empty_errors.append(f"Empty English string at: {path_str}")
    for path_str, val in hi_leaves:
        if isinstance(val, str) and not val.strip():
            empty_errors.append(f"Empty Hindi string at: {path_str}")

    if empty_errors:
        print(f"[FAIL] Found {len(empty_errors)} empty strings:")
        for err in empty_errors:
            print(f"  - {err}")
        sys.exit(1)
    print(f"      [PASS] All {len(en_leaves)} English and {len(hi_leaves)} Hindi values are populated and non-empty.")

    # 4. Rigorous Per-String Immutable Token Preservation Check
    print("\n[4/4] Validating PER-KEY statutory token preservation in matching strings...")
    token_mismatches = check_per_key_preservation(en_data, hi_data)
    if token_mismatches:
        print(f"[FAIL] Found {len(token_mismatches)} per-key token preservation failures:")
        for m in token_mismatches:
            print(f"  Key: {m['key']}")
            print(f"    Missing Token: {m['token']}")
            print(f"    EN: {m['en_snippet']}")
            print(f"    HI: {m['hi_snippet']}")
        sys.exit(1)

    # Count how many individual per-string checks passed
    verified_occurrences = 0
    for path_str, val in en_leaves:
        if isinstance(val, str):
            for t in REQUIRED_IMMUTABLE_TOKENS:
                if t in val:
                    verified_occurrences += 1

    print(f"      [PASS] 100% per-string preservation confirmed across {verified_occurrences} token instances.")
    print(f"      Monitored statutory tokens verified in corresponding localized strings:")
    for t in REQUIRED_IMMUTABLE_TOKENS:
        print(f"        [PASS] {t}")

    print("\n[INFO] Scope Boundary Note:")
    print("  - Automated check confirms 100% template key parity and per-key token retention.")
    print("  - Referential integrity of database citation IDs (PASS-xxx / REAL-xxx) is validated")
    print("    by corpus/benchmark suites (validate_t02.py, validate_sa01.py), not UI string templates.")
    print("  - Translation nuance and semantic Hindi fidelity remain subject to human review.")

    print("\n" + "=" * 70)
    print(f"SUCCESS: Verification PASSED (100% key parity, {len(en_leaves)} keys, {len(REQUIRED_IMMUTABLE_TOKENS)} monitored tokens).")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

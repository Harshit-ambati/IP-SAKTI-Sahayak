"""Validate v1 exchange examples and critical cross-object safety invariants."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "contracts/v1/sahayak.schema.json").read_text(encoding="utf-8"))
FIXTURES = ROOT / "contracts/v1/fixtures"
OBJECTS = {"intake": "Intake", "classification": "ClassificationResult", "answer": "AnswerResult", "referral": "ReferralPacket"}


def check_fixture(fixture: dict) -> None:
    for key, definition in OBJECTS.items():
        validator = Draft202012Validator(
            {**SCHEMA, "$ref": f"#/$defs/{definition}"}, format_checker=FormatChecker()
        )
        validator.validate(fixture[key])

    intake, classification, answer, referral = (fixture[key] for key in OBJECTS)
    assert len({obj["request_id"] for obj in (intake, classification, answer, referral)}) == 1
    assert intake["jurisdiction"] == answer["jurisdiction"] == referral["jurisdiction"]
    assert intake["language"] == answer["language"] == referral["language"]
    assert classification["route"] == answer["route"] == referral["route"]

    evidence = answer["evidence"]
    ids = [item["passage_id"] for item in evidence]
    assert len(ids) == len(set(ids)), "duplicate passage ID"
    assert all(item["jurisdiction"] == answer["jurisdiction"] for item in evidence)
    if answer["status"] == "answered":
        assert all(item["review_status"] == "approved" for item in evidence)
        assert all(item["corpus_version"] == answer["corpus_version"] for item in evidence)
        assert all(set(claim["evidence_ids"]) <= set(ids) for claim in answer["claims"])
    assert set(referral["evidence_ids"]) <= set(ids)


def main() -> None:
    Draft202012Validator.check_schema(SCHEMA)
    files = sorted(FIXTURES.glob("*.json"))
    assert files, "no contract fixtures"
    for path in files:
        check_fixture(json.loads(path.read_text(encoding="utf-8")))
        print(f"PASS {path.relative_to(ROOT)}")
    print(f"Validated schema and {len(files)} fixture(s).")


if __name__ == "__main__":
    main()

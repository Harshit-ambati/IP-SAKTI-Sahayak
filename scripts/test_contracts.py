"""Focused negative checks for the proposed v1 safety contract."""

import copy
import json
import unittest
from pathlib import Path

from check_contracts import check_fixture


FIXTURE = json.loads(
    (Path(__file__).resolve().parents[1] / "contracts/v1/fixtures/no_approved_evidence.json").read_text(encoding="utf-8")
)


class ContractTests(unittest.TestCase):
    def test_safe_no_evidence_fixture(self):
        check_fixture(FIXTURE)

    def test_wrong_jurisdiction_rejected(self):
        case = copy.deepcopy(FIXTURE)
        case["answer"]["jurisdiction"] = "international_overview"
        with self.assertRaises(AssertionError):
            check_fixture(case)

    def test_answer_cannot_use_pending_passage(self):
        case = copy.deepcopy(FIXTURE)
        case["answer"]["status"] = "answered"
        case["answer"]["claims"] = [{"text": "Synthetic claim", "evidence_ids": ["SYN-PASS-1"]}]
        case["answer"]["evidence"] = [{
            "passage_id": "SYN-PASS-1", "source_id": "SYN-SOURCE-1", "jurisdiction": "India",
            "source_title": "Synthetic source", "source_url": "https://example.org/synthetic",
            "locator": "Synthetic locator", "text": "Synthetic passage", "review_status": "pending",
            "corpus_version": "unapproved-starter-inventory"
        }]
        with self.assertRaises(AssertionError):
            check_fixture(case)

    def test_unknown_citation_rejected(self):
        case = copy.deepcopy(FIXTURE)
        case["answer"]["status"] = "answered"
        case["answer"]["claims"] = [{"text": "Synthetic claim", "evidence_ids": ["MISSING"]}]
        case["answer"]["evidence"] = [{
            "passage_id": "SYN-PASS-1", "source_id": "SYN-SOURCE-1", "jurisdiction": "India",
            "source_title": "Synthetic source", "source_url": "https://example.org/synthetic",
            "locator": "Synthetic locator", "text": "Synthetic passage", "review_status": "approved",
            "corpus_version": "unapproved-starter-inventory"
        }]
        with self.assertRaises(AssertionError):
            check_fixture(case)


if __name__ == "__main__":
    unittest.main()

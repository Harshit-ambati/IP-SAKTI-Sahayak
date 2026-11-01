# Benchmark dataset protocol

The twelve rows in [scenarios_dev.csv](scenarios_dev.csv) are synthetic prompts for early interface and routing work. They are not a validated legal-answer benchmark. No answer or citation should be scored as correct until Thulasi checks the expected route and official evidence.

## Canonical scenario fields

- `case_id`: stable ID; use SYN for early fixtures.
- `split`: development or holdout. Never tune on holdout cases.
- `category`: classification, evidence, insufficient_evidence or adversarial_jurisdiction.
- `language`: English, Hindi or selected regional-language code.
- `jurisdiction_requested`: India or international overview.
- `prompt`: synthetic user question, without personal data.
- `facts_present` and `missing_facts`: important intake conditions.
- `expected_behavior`: ask_clarification, answer_with_citations, abstain or referral. It is a provisional safety label in this starter file.
- `provisional_route`: one of six product routes or unknown.
- `gold_passage_ids`: reviewed source passage IDs; blank until curation.
- `label_status`, `reviewer`, `reviewed_at`: prevent provisional labels being treated as gold.

## Target composition

Create 120 canonical cases: 60 classification cases (10 per provisional route), 20 IP/ABS/TK evidence cases, 20 insufficient/conflicting-evidence cases and 20 adversarial/jurisdiction/privacy cases. Split 60/60 between development and holdout, stratifying by category, route and answerability. Ensure at least 20 held-out cases require abstention or referral across categories. Select 30 cases for Hindi and regional-language variants; keep every variant in its original case's split.

Record output, corpus/model/release version, claim-support scoring, citation resolution, classification result, abstention appropriateness and reviewer disagreement in a separate results file. Do not claim expert legal validation without qualified expert review.

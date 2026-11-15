# H-01 architecture and v1 exchange contract

Status: proposed for Suresh's technical review and Thulasi's evidence/routing review. This is a contract proposal, not a running API or an approved legal corpus.

## Small local architecture

The planned UI sends an `Intake` to one Python API. The API obtains a provisional `ClassificationResult`, requests evidence from a local index filtered by jurisdiction and approval, and returns an `AnswerResult`. A user-triggered export builds a `ReferralPacket`. Source administration and ingestion are staff-only operations owned by Suresh and Thulasi. No endpoint paths or database schema are fixed here; Suresh owns those choices.

The initial store may be SQLite with FTS5 and a local file-backed source snapshot. Exact-term retrieval should be established before adding semantic search. No current CSV row is approved for a legal answer. The existing corpus is an inventory for format and source navigation only.

## Contract

`contracts/v1/sahayak.schema.json` defines `Intake`, `ClassificationResult`, `EvidencePassage`, `AnswerResult` and `ReferralPacket`. `contracts/v1/fixtures/no_approved_evidence.json` is synthetic handoff data for Suresh's API and Akshay's abstention/referral UI. All objects carry version `1.0.0` where applicable. API consumers should reject unsupported major versions.

The seven routes are provisional labels, including `unknown`. `international_overview` means treaty/organization overview, not an export decision for a particular country. Language is a two or three letter code; the selected regional language remains a kickoff decision. `model_version: none` is used when no model generated the response.

## Invariants and limits

- The request ID, jurisdiction and language must agree across intake and output. A jurisdiction change requires fresh retrieval.
- An `answered` result needs material claims and evidence. Each claim has one or more evidence IDs that resolve to listed passages in the same approved corpus version, with a source URL and provision locator. A source link alone does not establish claim support; reviewers must assess entailment.
- A non-answer result has no material claims. Missing facts, unresolved conflicts, unapproved/stale evidence or a wrong-jurisdiction match lead to clarification, abstention or referral.
- The index must exclude pending, rejected and stale passages from substantive answers. India and international overview evidence are filtered separately at query time.
- Translated displays retain evidence IDs, legal terms and locators. A translation that is not reviewed must not alter a material claim.
- A referral packet is generated on user action. Do not persist the question by default; routine audit records should contain only request ID, route/status, evidence IDs and versions.

`python scripts/check_contracts.py` checks structure and the cross-object invariants represented by fixtures. Runtime validation must enforce them for every response; this script does not prove legal support.

## Open decisions and dependencies

Suresh: confirm endpoint names, validation ownership, staff authorization and source lookup response. Akshay: confirm whether the abstention fixture covers the required empty/source/referral states. Thulasi: confirm route definitions and activate reviewed provisions before any answered fixture is added. Deepshika: confirm regional language and translated notice wording. Sabeena: supply the development-case template. Harshit/team: record demo laptop, local model license, size, memory use, response latency and offline operation before selecting a generator.

## Local model feasibility observation, 15 November 2026

This Windows 11 environment reports 8 logical CPUs, 15.28 GiB total RAM and 3.93 GiB available RAM at the time of inspection. Python has `transformers`, but no `ollama`, `llama-server`, `llama-cli`, `llama_cpp`, `nvidia-smi` or local Hugging Face model cache was found. The system memory query through CIM was denied, so the RAM reading came from `psutil`. No model inference, download, license check, latency measurement or offline generation test was performed. Local generation feasibility therefore remains **unproven**, and no model has been selected. A named demo laptop and permitted model download are needed for the week-2 trial.

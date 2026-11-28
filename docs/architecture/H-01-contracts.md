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

Suresh: confirm endpoint names, validation ownership, staff authorization and source lookup response. Akshay: confirm whether the abstention fixture covers the required empty/source/referral states. Thulasi: confirm route definitions and activate reviewed provisions before any answered fixture is added. Deepshika: confirm regional language and translated notice wording. Sabeena: supply the development-case template. Harshit/team: confirm whether the tested laptop is the demo laptop and agree on the demo latency budget.

## Local model feasibility trial, 26 November 2026

The trial used the current Windows 11 laptop (build 26300, AMD Ryzen 5 7520U, 8 logical CPUs, 15,648 MiB RAM). It ran on four CPU threads in float32 with Python 3.14.2, PyTorch 2.14.0+cpu, Transformers 5.17.0 and psutil 7.2.2. The checkpoint was [SmolLM2-135M-Instruct at revision `12fd25f`](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct/tree/12fd25f77366fa6b3b4b768ec3050bf629380bac), published under Apache-2.0. Its weights were 269,060,552 bytes and the downloaded snapshot files totaled 272,496,399 bytes (259.9 MiB, excluding download metadata).

| Measurement | Observed result |
|---|---:|
| Startup through first complete response, including imports | 33.15 s |
| Checkpoint and tokenizer load within startup | 4.711 s |
| Peak process working set, including Python and libraries | 1,029.5 MiB |
| Median complete response time for the two subsequent prompts | 1.411 s |
| Python network attempts during loading and inference | 0 |

| Synthetic case | Complete response | Result |
|---|---:|---|
| Explain the value of a source link | 3.271 s, 28 generated tokens | Explained that a direct source link lets the reader verify information. |
| Answer from a synthetic passage and cite `SYN-001` | 1.181 s, 10 generated tokens | Returned “The demo library opens at 9 AM.” and omitted the requested citation ID. |
| Explain why there is no answer without reviewed evidence | 1.641 s, 15 generated tokens | Said it could not determine eligibility without reviewing the evidence. |

The run demonstrates offline CPU generation on this laptop. The citation omission rules out relying on this checkpoint to emit citations correctly on its own. Keep citation resolution and suppression of unsupported output in application code. These are three short English prompts from one process launch. Legal answer quality, multilingual behavior, performance with a loaded application, and performance on any different demo laptop remain unmeasured. Startup makes preloading useful for an interactive demo. Generator selection remains open pending evidence quality evaluation.

### Reproduce the measurement

Download the pinned snapshot once, then run the trial in a separate Python process. The trial uses local files only and blocks Python socket connection and DNS attempts. It prints all three outputs and metrics as JSON. Model files belong outside the repository.

```powershell
$trialPath = Join-Path ([IO.Path]::GetTempPath()) 'sahayak-h01-smollm2-12fd25f'
python -m pip install 'torch==2.14.0' 'transformers==5.17.0' 'psutil==7.2.2'
python -B -c "import sys; from huggingface_hub import snapshot_download; snapshot_download('HuggingFaceTB/SmolLM2-135M-Instruct', revision='12fd25f77366fa6b3b4b768ec3050bf629380bac', local_dir=sys.argv[1], allow_patterns=['*.json','*.safetensors','merges.txt','vocab.json'], token=False)" $trialPath
python -B scripts/trial_local_model.py $trialPath
```

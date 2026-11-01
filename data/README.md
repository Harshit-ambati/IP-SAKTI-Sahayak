# Project data package

This is a starter package for collecting the project data. It contains source candidates and synthetic test prompts, not a reviewed legal corpus or completed benchmark. See [methodology](../docs/methodology.md) for collection and evaluation steps.

| File | Use | Owner | Release condition |
|---|---|---|---|
| [Source register](sources/source_register.csv) | Track official source candidates and provenance | Thulasi | Reviewed status and exact instrument URL |
| [Provision template](sources/provisions.template.csv) | One row per citable passage | Thulasi | Verbatim checked against official source |
| [Development scenarios](benchmark/scenarios_dev.csv) | Synthetic prompts for early routing and safety tests | Sabeena | Gold labels and evidence independently reviewed |
| [Benchmark guide](benchmark/README.md) | Scenario schema and split rules | Sabeena | Frozen development/holdout split |
| [Glossary template](glossary/terms.template.csv) | Controlled legal and Ayurveda terms | Deepshika | Hindi and regional terms reviewed |

## Required data by the midpoint

1. Approved public-source corpus: target 25-35 useful official documents or a smaller set that covers all supported topics. Store source metadata, the approved passages and a version manifest.
2. Evaluation set: target 120 canonical synthetic cases, split 60 development and 60 held out. Include six formulation routes, evidence questions, unclear cases and adversarial/jurisdiction cases.
3. Language set: 30 selected cases with reviewed Hindi and regional-language versions, kept in the same development or holdout split as the English originals.
4. Human review records: who reviewed each provision, expected answer, translation and final output; date, decision and disagreement.

The application retrieves sources; it does not need a patient dataset or a model trained from scratch. Use only public information whose use and redistribution have been checked. Do not commit user formulations, restricted TKDL records, credentials or raw copies whose reuse terms are unclear.

Create active corpus and holdout files only after review. Suggested later files: `sources/approved.csv`, `sources/provisions.csv`, `sources/corpus_manifest.json`, `benchmark/scenarios_holdout.csv`, `benchmark/translations.csv`, `evaluation/results.csv`. Record actual metrics in results, never in the templates.

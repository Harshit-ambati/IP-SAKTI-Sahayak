# IP-SAKTI Sahayak

**SIH26045 · A multilingual, source-cited assistant for intellectual-property and regulatory information in Ayurveda.**

IP-SAKTI Sahayak is a six-member capstone project. The intended system guides users through formulation intake, provisional product classification, jurisdiction-specific retrieval, cited answers, uncertainty handling and referral to a human professional.

> The system provides information, not legal advice. Evidence coverage or AI confidence is not proof of legal correctness.

## Current status

**Planning and work allocation.** This repository currently contains the project overview, full 16-week plan and six individual work-plan modules. Application code, trained models, a curated corpus and measured evaluation results are future deliverables. Installation and run commands will be added when a runnable implementation exists.

## Start with the work plan

- [Team module index and handoffs](docs/work-plan/README.md)
- [Complete 16-week plan: scope, schedule, ownership, workflow, evaluation and risks](docs/work-plan/MASTER_PLAN.md)
- [Data package and dataset inventory](data/README.md)
- [Real official sources for the first corpus](data/sources/REAL_DATA_GUIDE.md)
- [Data collection and evaluation methodology](docs/methodology.md)

| Member | Primary responsibility | Individual module |
|---|---|---|
| Harshit | Technical leadership, architecture, RAG and evidence validation | [Open work plan](docs/work-plan/modules/01-harshit.md) |
| Thulasi | Authoritative source corpus, formulation categories and decision rules | [Open work plan](docs/work-plan/modules/02-thulasi.md) |
| Deepshika | Multilingual experience, terminology, translation quality and accessibility | [Open work plan](docs/work-plan/modules/03-deepshika.md) |
| Suresh | Backend APIs, database, authentication, privacy and deployment | [Open work plan](docs/work-plan/modules/04-suresh.md) |
| Sabeena | Test cases, evaluation records, user documentation and feedback | [Open work plan](docs/work-plan/modules/05-sabeena.md) |
| Akshay | Frontend screens, source display, interface checks and demonstration | [Open work plan](docs/work-plan/modules/06-akshay.md) |

Harshit leads technical architecture, RAG, evidence validation, difficult integrations and final technical review. Each member owns their module. Suresh is the integration deputy so routine work can continue without waiting for Harshit. Akshay and Sabeena own smaller modules with measurable deliverables and early handoffs.

## Minimum viable product

- Guided formulation intake with six provisional routing labels and an explicit unknown/ambiguous outcome. Novel or insufficiently supported cases are referred rather than forced into a confident category.
- A small, public, authoritative corpus covering selected India-focused patent/TK, biodiversity/ABS and product-category topics, with source authority, URL, jurisdiction, dates, version and provision locators.
- Exact-term and semantic retrieval, constrained answer generation, claim-to-evidence mapping and checks that citation IDs resolve to real sources. Claim support is also evaluated by reviewers.
- Clearly separate **India** and **international overview** controls and answers. Detailed country-specific export compliance is outside the initial scope.
- **English, Hindi and one regional language selected at kickoff**, with reviewed terminology and the same citation IDs across languages.
- Clarification, safe abstention and a user-controlled referral packet when facts or evidence are insufficient. Live access to an expert is not assumed.
- Minimal user-data collection, protected staff-only corpus operations, access checks, limited audit events and documented retention/deletion controls.
- A reproducible local release, benchmark, actual evaluation report, user guide, final report and live demonstration with a backup.

Voice, a knowledge graph, autonomous multi-step agents, paid-source integrations, broad export-market coverage and extra languages are stretch work after the MVP passes its gates. No paid APIs, unrestricted TKDL access, private datasets or cloud credits are assumed.

## Planned flow

Guided intake → provisional formulation route → jurisdiction and topic filters → authoritative evidence retrieval → supported answer or abstention → original sources and optional referral packet.

The selected implementation stack and model are to be confirmed during kickoff and tested on team hardware by week 2. Technical scope should remain small enough for six part-time students.

## Delivery milestones

| Week | Planned outcome |
|---|---|
| 2 | Shared contracts, mock flow, first sources and model/translation feasibility |
| 4 | Real intake-to-cited-answer flow, including abstention |
| 8 | Integrated beta and baseline corpus; English/Hindi core flow |
| 10 | Three-language core experience and user guide |
| 12 | Feature freeze |
| 14 | Evaluated release candidate, report and rehearsed demo |
| 15-16 | Protected testing, critical repairs, packaging and submission buffer |

Weeks are relative to kickoff. Confirm the institution's actual deadline; historical SIH dates are not used as this project's schedule.

## Evaluation goals

The master plan defines the complete protocol. Proposed goals include classification macro-F1 of at least 0.85; supporting evidence retrieved in the top five for at least 85% of answerable evidence-labelled cases; at least 90% supported material claims; zero fabricated authorities; zero critical jurisdiction-mixing errors; and 100% citation-ID parity in paired-language tests.

The planned benchmark has 120 canonical scenarios split into 60 development and 60 held-out cases, plus 60 translated prompt variants. These are targets, not existing data or achieved scores. Independent expert legal validation is not assumed; report reviewer qualifications, failures and limitations honestly.

## Repository contents

```text
README.md
docs/
  work-plan/
    README.md
    MASTER_PLAN.md
    modules/
      01-harshit.md
      02-thulasi.md
      03-deepshika.md
      04-suresh.md
      05-sabeena.md
      06-akshay.md
```

## Collaboration

Use small issues and PRs linked to module task IDs. Share fixtures early and demonstrate the integrated flow weekly. Routine changes receive one independent peer review; critical architecture, citation, jurisdiction and security changes require Harshit's review. Harshit's own critical work also receives independent review.

Use individual accounts and appropriate repository/deployment permissions. Keep credentials, private formulations, user data and restricted-source content out of commits, issues and screenshots. Access-control policy in these documents must be configured separately in GitHub and the eventual deployment.

Before implementation, confirm the kickoff date, regional language and reviewers, supported topics, available hardware/stack, collaborator permissions and submission format.

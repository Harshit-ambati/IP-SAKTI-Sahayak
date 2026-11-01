# Team work-plan modules

[Project README](../../README.md) · [Full 16-week execution plan](MASTER_PLAN.md)

This directory contains the work allocation for IP-SAKTI Sahayak (SIH26045). The [real-source corpus CSVs](../../data/corpus/README.md) now contain seven document records and eight preliminary passage summaries pending domain review. The application and validated benchmark have not been implemented.

## Individual ownership

| Member | Primary module | Weekly capacity | Planned effort |
|---|---|---:|---:|
| [Harshit](modules/01-harshit.md) | Technical leadership, architecture, RAG and evidence validation | 12 h | 150 h |
| [Thulasi](modules/02-thulasi.md) | Authoritative source corpus, formulation categories and decision rules | 10 h | 125 h |
| [Deepshika](modules/03-deepshika.md) | Multilingual experience, terminology, translation quality and accessibility | 10 h | 125 h |
| [Suresh](modules/04-suresh.md) | Backend APIs, database, authentication, privacy and deployment | 10 h | 125 h |
| [Sabeena](modules/05-sabeena.md) | Test cases, evaluation records, user documentation and feedback | 6 h | 75 h |
| [Akshay](modules/06-akshay.md) | Frontend screens, source display, interface checks and demonstration | 6 h | 75 h |

Total planned effort is 675 hours against 864 hours of estimated team capacity. Keep the remaining 189 hours available for rework, integration and absence. Akshay and Sabeena have smaller, clearly testable modules. Harshit leads architecture, RAG, evidence validation and final integration; Suresh is the deputy for routine integration.

## How to use the files

1. Read the master plan for scope, dependencies, weekly milestones, decision rights, evaluation gates and submission checklist.
2. Each member reads their module, confirms inputs and converts task packages into small issues when implementation begins.
3. Track actual progress with links to PRs, source records, test outputs or documents; do not mark goals achieved without evidence.
4. Demonstrate a shared integrated build every Friday. Share fixtures early rather than waiting for whole modules.
5. Update the master plan and affected member files together when scope, contracts or deadlines change.

## Shared handoffs

| Producer | Early input | Consumer | Required by |
|---|---|---|---|
| Harshit + Suresh | Architecture, response schemas and mock JSON | All owners | W2 |
| Thulasi | Three official sources and draft category rules | Harshit, Suresh, Sabeena | W2 |
| Deepshika | UX specifications, reviewed strings and glossary v0 | Akshay, Harshit | W2 |
| Sabeena | Scenario/result templates and twenty initial cases | Harshit, Thulasi, Deepshika | W2 |
| Akshay | Mock intake and answer screens | Suresh, Deepshika | W2 |
| All owners | Real cited end-to-end flow | Whole team | W4 |

## Review and completion

One independent peer review is required for routine changes. Harshit reviews architecture, evidence policy, jurisdiction controls, sensitive security changes and final releases. Suresh can integrate routine reviewed changes. Harshit's own critical changes need independent review by Suresh and evidence review by Thulasi where relevant.

This is a team policy; these documents do not configure GitHub permissions or branch protections. Use individual accounts, give Harshit administrator access, grant other members only the repository/deployment access they need, and never share passwords or personal access tokens.

A task is complete only when its deliverable, relevant checks, review, documentation and integration are complete. Weeks 15-16 remain the testing/submission buffer. No live expert access, paid API, restricted TKDL dataset or cloud credit is assumed.

## Decisions at kickoff

Confirm the actual dates and member availability, regional language/reviewers, supported question list, development/demo hardware and stack, and repository access plus institutional submission requirements.

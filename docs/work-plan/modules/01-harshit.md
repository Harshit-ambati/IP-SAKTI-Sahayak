# Harshit: Technical leadership, architecture, RAG and evidence validation

[Work-plan index](../README.md) · [Master plan](../MASTER_PLAN.md) · [Project README](../../../README.md)

**Owner:** Harshit

**Schedule:** weeks 1-16 from kickoff

**Capacity:** 12 hours/week; 150 planned hours over 16 weeks, with remaining capacity reserved for review, rework and integration.

**Status:** planned; completion must be supported by linked deliverables and checks.

## Module specification

- **Primary tasks:** define module boundaries and response contracts; implement ingestion adapters, provision-aware chunking, exact-term/semantic retrieval, evidence-constrained generation, citation validation, abstention and jurisdiction isolation; integrate the system and lead technical decisions.
- **Supporting tasks:** mentor difficult fixes, review critical PRs, maintain architectural decisions, compare retrieval baseline against hybrid retrieval, assemble reproducible release and evaluation configuration.
- **Inputs needed:** the existing seven-document/eight-passage [corpus inventory](../../../data/corpus/README.md), with at least three passages reviewed by Thulasi for the week-2 ingestion gate; API fixtures from Suresh; glossary constraints from Deepshika; benchmark format from Sabeena. Exclude unreviewed rows from substantive answers.
- **Outputs:** architecture note, versioned schemas, retrieval/generation module, claim-evidence validator, safety policy, evaluation runner and integrated release.
- **Acceptance:** every emitted citation resolves to a real indexed passage and provision locator; wrong-jurisdiction sources are blocked; missing evidence yields clarification/abstention; citation support and retrieval meet section 6 gates. Automatic ID checks are not presented as proof of legal entailment.
- **Dependencies and handoff:** start with synthetic fixtures in week 1 and three real documents in week 2; ingest weekly batches instead of waiting for the entire corpus.
- **Effort:** 150 planned hours: architecture/contracts 20; retrieval/ingestion 45; answer validation/safety 35; integration/reviews 30; evaluation/release 20.

## Work boundaries and review

Own cross-module technical decisions and review access to every module. Delegate routine API, UI, content and documentation decisions to their owners. Do not make all merges depend on your availability; Suresh is the integration deputy.

Suresh reviews technical changes; Thulasi reviews source support and legal routing. Harshit approves integration after independent review.

Harshit has project-wide technical review and integration access. Each member remains accountable for their own deliverables. Routine work proceeds through the designated peer reviewer; access settings must be configured separately by the repository owner.

## Task packages

| Task | Target | Deliverable |
|---|---|---|
| H-01 | W1-2 | Publish architecture, response schemas and fixtures; prove local model feasibility. |
| H-02 | W3-4 | Connect ingestion and retrieval to a real end-to-end cited response. |
| H-03 | W5-6 | Implement jurisdiction filters, evidence IDs and unsupported-claim suppression. |
| H-04 | W7-10 | Run the development benchmark and integrate all three languages without changing citation mappings. |
| H-05 | W11-14 | Resolve safety findings, freeze features and assemble the evaluated release candidate. |
| H-06 | W15-16 | Lead regression, approve the technical release and package reproducible artifacts. |

## Weekly responsibilities

| Week | Responsibility |
|---|---|
| 1 | Architecture and contracts |
| 2 | Model feasibility and fixtures |
| 3 | Ingestion and retrieval baseline |
| 4 | Vertical slice; evidence IDs |
| 5 | Jurisdiction and abstention |
| 6 | Hybrid search and validator |
| 7 | Evaluation runner |
| 8 | Full beta integration |
| 9 | Evidence/safety fixes |
| 10 | Citation/translation integration |
| 11 | Injection/conflict tests |
| 12 | Feature freeze and dev metrics |
| 13 | Analyze held-out errors |
| 14 | Release candidate approval |
| 15 | Critical fixes/regression |
| 16 | Tag/package technical release |

Weeks 15-16 are reserved for testing, repairs, packaging and submission; do not introduce new features during this buffer.

## Deliverable checklist

- [ ] Architecture and shared request/response schemas
- [ ] Ingestion, provision-aware chunking and hybrid retrieval
- [ ] Evidence-constrained response assembly and citation validator
- [ ] Jurisdiction isolation, clarification, abstention and referral decisions
- [ ] Benchmark runner, baseline comparison and integrated release
- [ ] Relevant master-plan acceptance gates met and actual evidence recorded.
- [ ] Independent peer review completed and all critical findings resolved.
- [ ] Outputs integrated into the shared project; handoff notes and limitations documented.

## Start here

1. Agree v1 contracts with Suresh and circulate sample JSON to all owners.
2. Ask Thulasi for three official source records and Sabeena for the test template.
3. Record the demo laptop's model memory, response latency and offline behavior.

## Progress record

Use task IDs in issues and PRs. Replace the placeholder row only when work starts; checked boxes must link to real artifacts or results.

| Task ID | Status | Evidence / issue / PR | Reviewer | Blocker / next action |
|---|---|---|---|---|
| Not started | Planned | None yet | Unassigned | Confirm kickoff inputs |

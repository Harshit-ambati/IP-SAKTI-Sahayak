# Thulasi: Authoritative source corpus, formulation categories and decision rules

[Work-plan index](../README.md) · [Master plan](../MASTER_PLAN.md) · [Project README](../../../README.md)

**Owner:** Thulasi

**Schedule:** weeks 1-16 from kickoff

**Capacity:** 10 hours/week; 125 planned hours over 16 weeks, with remaining capacity reserved for review, rework and integration.

**Status:** planned; completion must be supported by linked deliverables and checks.

## Module specification

- **Primary tasks:** research public official sources; record provenance and access rights; extract provision locators; build formulation questions, category rules and bounded IP/ABS/TK routing tables.
- **Supporting tasks:** create source-grounded expected answers, verify corpus revisions, review citation support, document unresolved interpretations and international scope boundaries.
- **Inputs needed:** frozen MVP topic list, the existing [corpus documents and passages](../../../data/corpus/README.md), and ingestion feedback; public source portals, not private datasets.
- **Outputs:** reviewed and expanded corpus CSVs, approved provision extracts, version/change log, rule table with question/condition/route/source fields, coverage map and expected-evidence annotations. The present eight paraphrases still need domain and amendment review.
- **Acceptance:** at least 25 useful approved documents or a documented smaller corpus covering every supported topic; every source has URL, authority, jurisdiction, publication/effective date and version where available, capture date, checksum, access/reuse status and reviewer. Missing dates are explicitly unknown, never invented; uncertain legal status excludes an item from definitive guidance. Every decision rule cites a provision; ambiguity produces clarification/referral.
- **Dependencies and handoff:** deliver three records in week 2, 10 approved sources in week 4, around 20 in week 6 and baseline coverage in week 8. One reviewer checks a sample from each batch before activation.
- **Effort:** 125 hours: research 45; metadata/extraction 25; rules 25; evidence annotation 20; freshness/report review 10.

## Work boundaries and review

Own the evidence and rule specification. Harshit implements reasoning and retrieval; Sabeena records evaluations. Treat novel/non-classical and phytopharmaceutical categories as referral routes unless a narrow source-backed answer is approved. Do not equate Ayurveda Aahara with all nutraceuticals.

Harshit reviews provenance integration and activates corpus versions; Deepshika reviews terminology. An independent teammate checks each source batch.

Harshit has project-wide technical review and integration access. Each member remains accountable for their own deliverables. Routine work proceeds through the designated peer reviewer; access settings must be configured separately by the repository owner.

## Task packages

| Task | Target | Deliverable |
|---|---|---|
| T-01 | W1-2 | Define supported topics; deliver three complete source records and draft category rules. |
| T-02 | W3-4 | Deliver ten reviewed sources and classify representative product scenarios. |
| T-03 | W5-6 | Complete bounded IP/ABS/TK rules and approximately twenty useful source records. |
| T-04 | W7-8 | Check benchmark evidence and publish the baseline corpus coverage map. |
| T-05 | W9-14 | Review conflicts, evaluate claim support and sign off source status for release candidate. |
| T-06 | W15-16 | Recheck sources and deliver the versioned corpus and exclusions log. |

## Weekly responsibilities

| Week | Responsibility |
|---|---|
| 1 | Topic/source coverage map |
| 2 | Three sources; draft rules |
| 3 | Category questions; six sources |
| 4 | Ten sources; expected evidence |
| 5 | IP/ABS/TK rule table |
| 6 | About 20 sources; rule review |
| 7 | Check benchmark evidence |
| 8 | Corpus baseline v1 |
| 9 | Conflict/freshness review |
| 10 | Review supported answers |
| 11 | Review legal error cases |
| 12 | Corpus/rules freeze |
| 13 | Evidence scoring |
| 14 | Source-status signoff |
| 15 | Source recheck |
| 16 | Verify corpus handover |

Weeks 15-16 are reserved for testing, repairs, packaging and submission; do not introduce new features during this buffer.

## Deliverable checklist

- [ ] Source register and access/reuse metadata
- [ ] Approved provision excerpts with locators and version manifest
- [ ] Formulation intake questions and source-backed routing table
- [ ] Topic coverage map, exclusions and supersession/change log
- [ ] Expected evidence and claim-support annotations
- [ ] Relevant master-plan acceptance gates met and actual evidence recorded.
- [ ] Independent peer review completed and all critical findings resolved.
- [ ] Outputs integrated into the shared project; handoff notes and limitations documented.

## Start here

1. Create one source-record example with authority, URL, jurisdiction, dates, version and locator.
2. Identify sources for the first supported question in each selected topic.
3. Mark missing dates, unclear applicability and restricted access explicitly.

## Progress record

Use task IDs in issues and PRs. Replace the placeholder row only when work starts; checked boxes must link to real artifacts or results.

| Task ID | Status | Evidence / issue / PR | Reviewer | Blocker / next action |
|---|---|---|---|---|
| Not started | Planned | None yet | Unassigned | Confirm kickoff inputs |

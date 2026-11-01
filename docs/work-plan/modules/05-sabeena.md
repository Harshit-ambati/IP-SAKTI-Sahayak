# Sabeena: Test cases, evaluation records, user documentation and feedback

[Work-plan index](../README.md) · [Master plan](../MASTER_PLAN.md) · [Project README](../../../README.md)

**Owner:** Sabeena

**Schedule:** weeks 1-16 from kickoff

**Capacity:** 6 hours/week; 75 planned hours over 16 weeks, with remaining capacity reserved for review, rework and integration.

**Status:** planned; completion must be supported by linked deliverables and checks.

## Module specification

- **Primary tasks:** create the synthetic but source-grounded scenarios described in the [benchmark protocol](../../../data/benchmark/README.md); maintain expected-result records; execute repeatable test checklists; record results, defects and user feedback; write the guide and organize report/presentation evidence. The earlier unreviewed fixture CSV was removed, so no validated cases exist yet.
- **Supporting tasks:** coordinate six to eight consenting student/potential-user walkthroughs where feasible, maintain milestone checklist and rehearse the live demo with Akshay. Usability participants do not certify legal correctness.
- **Inputs needed:** test template from Harshit, source-based labels from Thulasi and language fixtures from Deepshika. Sabeena records legal evaluations but does not independently determine legal truth.
- **Outputs:** 120 canonical scenarios, test-run ledger, issue evidence, user guide, feedback summary, report draft and presentation outline.
- **Acceptance:** scenarios contain ID, facts, jurisdiction, expected route, answerability, evidence IDs and rubric; development/holdout labels are frozen separately; each final result records release/model/corpus version and actual output; documentation covers supported scope, limitations, citations, abstention, privacy and referral.
- **Dependencies and handoff:** 20 scenarios by week 2, 60 by week 4, 120 by week 7; guide skeleton by week 4 and usable guide by week 10. Complex automation belongs to Harshit/Suresh.
- **Effort:** 75 hours: scenario organization 20; test execution 20; guide/report/presentation 25; feedback/coordination 10.

## Work boundaries and review

Own organization, manual test execution and reporting. Harshit/Suresh implement complex test automation; Thulasi supplies source-grounded labels. Do not independently certify legal correctness or invent passed results. Keep the module manageable with reusable tables and checklists.

Thulasi checks source-based expected answers; Deepshika checks language labels; Harshit reviews the benchmark protocol; Suresh checks reproducibility.

Harshit has project-wide technical review and integration access. Each member remains accountable for their own deliverables. Routine work proceeds through the designated peer reviewer; access settings must be configured separately by the repository owner.

## Task packages

| Task | Target | Deliverable |
|---|---|---|
| Sa-01 | W1-2 | Create simple scenario/result templates and collect the first twenty cases. |
| Sa-02 | W3-4 | Organize sixty scenarios and a user-guide outline. |
| Sa-03 | W5-7 | Record safety tests and freeze the 120-case development/holdout split. |
| Sa-04 | W8-10 | Record beta runs and publish a usable guide for the complete core flow. |
| Sa-05 | W11-14 | Coordinate feedback, draft the report and record independently scored evaluation results. |
| Sa-06 | W15-16 | Complete the test ledger and submission inventory; capture submission receipt. |

## Weekly responsibilities

| Week | Responsibility |
|---|---|
| 1 | Test/report templates |
| 2 | First 20 scenarios |
| 3 | Alpha checklist |
| 4 | 60 scenarios; guide outline |
| 5 | Safety-case records |
| 6 | Citation/interface test runs |
| 7 | Freeze 120-case split |
| 8 | Beta results and guide draft |
| 9 | Defect tracking |
| 10 | User guide v1 |
| 11 | Feedback sessions/summary |
| 12 | Report draft/results tables |
| 13 | Record blinded results |
| 14 | Final report/slides |
| 15 | Final test ledger |
| 16 | Submission checklist/receipt |

Weeks 15-16 are reserved for testing, repairs, packaging and submission; do not introduce new features during this buffer.

## Deliverable checklist

- [ ] 120 canonical benchmark scenarios and split manifest
- [ ] Repeatable test checklists, raw result ledger and defect evidence
- [ ] User guide and privacy/referral instructions
- [ ] Feedback summary and presentation/report drafts
- [ ] Final submission checklist and artifact inventory
- [ ] Relevant master-plan acceptance gates met and actual evidence recorded.
- [ ] Independent peer review completed and all critical findings resolved.
- [ ] Outputs integrated into the shared project; handoff notes and limitations documented.

## Start here

1. Use fields for scenario ID, facts, jurisdiction, expected route, answerability and evidence IDs.
2. Prepare a result sheet with release, corpus/model version, output, reviewer and defect link.
3. Request expected evidence from Thulasi rather than guessing legal outcomes.

## Progress record

Use task IDs in issues and PRs. Replace the placeholder row only when work starts; checked boxes must link to real artifacts or results.

| Task ID | Status | Evidence / issue / PR | Reviewer | Blocker / next action |
|---|---|---|---|---|
| Not started | Planned | None yet | Unassigned | Confirm kickoff inputs |

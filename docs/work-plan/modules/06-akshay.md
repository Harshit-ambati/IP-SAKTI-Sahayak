# Akshay: Frontend screens, source display, interface checks and demonstration

[Work-plan index](../README.md) · [Master plan](../MASTER_PLAN.md) · [Project README](../../../README.md)

**Owner:** Akshay

**Schedule:** weeks 1-16 from kickoff

**Capacity:** 6 hours/week; 75 planned hours over 16 weeks, with remaining capacity reserved for review, rework and integration.

**Status:** planned; completion must be supported by linked deliverables and checks.

## Module specification

- **Primary tasks:** implement home/scope notice, intake form, answer view, jurisdiction/language controls, source cards and referral-download screen from approved specifications.
- **Supporting tasks:** add loading/error/empty/abstention states, responsive styles, basic interface checks, screenshots and demo setup.
- **Inputs needed:** Deepshika's layouts/strings and Suresh's response fixtures. Harshit owns evidence logic; Suresh owns authentication.
- **Outputs:** six simple screen/component groups, source-link behavior, API-connected interface, UI checklist and demonstration assets.
- **Acceptance:** the complete flow works with mock data by week 4 and real data by week 8; citations open the correct source/excerpt; jurisdiction and language persist correctly; unsupported/error states remain understandable; no backend rules or secrets are embedded in the interface.
- **Dependencies and handoff:** start with fixture JSON in week 2; finish core components by week 6 and end-to-end UI by week 8, leaving later capacity for testing and demo work.
- **Effort:** 75 hours: screen/components 35; API wiring 15; interface checks 15; demo assets 10.

## Work boundaries and review

Own straightforward component implementation and demo operation. Deepshika owns UX and translation quality; Suresh owns authentication and backend rules; Harshit owns citations and evidence logic. Render API states rather than deciding legal outcomes in the browser.

Deepshika reviews UX, language use and accessibility; Suresh reviews API integration; Harshit reviews citation/jurisdiction behavior.

Harshit has project-wide technical review and integration access. Each member remains accountable for their own deliverables. Routine work proceeds through the designated peer reviewer; access settings must be configured separately by the repository owner.

## Task packages

| Task | Target | Deliverable |
|---|---|---|
| A-01 | W1-2 | Build the screen skeleton and mock intake/answer flow. |
| A-02 | W3-4 | Complete the six simple screen/component groups against fixture data. |
| A-03 | W5-6 | Complete source/referral screens and core UI states. |
| A-04 | W7-8 | Connect the real APIs and complete an end-to-end interface check. |
| A-05 | W9-14 | Fix responsive/accessibility issues and prepare screenshots and rehearsed demonstration. |
| A-06 | W15-16 | Smoke-test the UI and deliver the live-demo and backup assets. |

## Weekly responsibilities

| Week | Responsibility |
|---|---|
| 1 | Screen skeleton |
| 2 | Mock intake/answer |
| 3 | Intake validation/states |
| 4 | Six component groups |
| 5 | Source/referral views |
| 6 | Finish core screens |
| 7 | API wiring and error states |
| 8 | End-to-end UI acceptance |
| 9 | Responsive/keyboard fixes |
| 10 | Full-flow UI regression |
| 11 | UI feedback repairs |
| 12 | Screenshots/demo draft |
| 13 | Browser/accessibility checks |
| 14 | Demo rehearsal/backup |
| 15 | Demo/UI smoke tests |
| 16 | Live demo/video handover |

Weeks 15-16 are reserved for testing, repairs, packaging and submission; do not introduce new features during this buffer.

## Deliverable checklist

- [ ] Home/scope notice and guided intake
- [ ] Answer view with visible jurisdiction and language controls
- [ ] Source cards/excerpt view and referral-download screen
- [ ] Loading/error/empty/abstention states and responsive styling
- [ ] UI checklist, screenshots and demo script/backup assets
- [ ] Relevant master-plan acceptance gates met and actual evidence recorded.
- [ ] Independent peer review completed and all critical findings resolved.
- [ ] Outputs integrated into the shared project; handoff notes and limitations documented.

## Start here

1. Request fixture JSON from Suresh and screen/strings specifications from Deepshika.
2. Build loading, validation, no-evidence and network-failure states early.
3. Ensure each source card opens the actual cited source and displays the provision locator.

## Progress record

Use task IDs in issues and PRs. Replace the placeholder row only when work starts; checked boxes must link to real artifacts or results.

| Task ID | Status | Evidence / issue / PR | Reviewer | Blocker / next action |
|---|---|---|---|---|
| Not started | Planned | None yet | Unassigned | Confirm kickoff inputs |

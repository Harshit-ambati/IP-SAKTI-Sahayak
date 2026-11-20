# Deepshika: Multilingual experience, terminology, translation quality and accessibility

[Work-plan index](../README.md) · [Master plan](../MASTER_PLAN.md) · [Project README](../../../README.md)

**Owner:** Deepshika

**Schedule:** weeks 1-16 from kickoff

**Capacity:** 10 hours/week; 125 planned hours over 16 weeks, with remaining capacity reserved for review, rework and integration.

**Status:** planned; completion must be supported by linked deliverables and checks.

## Module specification

- **Primary tasks:** design intake and answer flows; own translation resources, language switching, glossary and accessible interaction; implement multilingual rendering and legal-term preservation with Harshit.
- **Supporting tasks:** give Akshay component specifications and reviewed strings; arrange language review within the team; help assess comprehension and translation failures.
- **Inputs needed:** response schema, initial source terminology, supported-topic list and confirmed regional language. Do not assume external bilingual experts are available.
- **Outputs:** user-flow sketches, three-language strings, 80-120 controlled glossary entries, reviewed translation fixtures, citation-parity checks and accessibility findings.
- **Acceptance:** core task can be completed in all three languages; legal names/provision IDs remain stable; no critical change to negation, duty, exception or jurisdiction in release samples; 100% citation-ID parity across translated benchmark variants; keyboard navigation, visible labels and usable mobile layout. Unverified dynamic translation falls back to a localized uncertainty message and cited source, not an invented translation.
- **Dependencies and handoff:** strings and screen specifications begin in week 2; integrate against mocked answers in week 3; English/Hindi by week 8 and regional language by week 10.
- **Effort:** 125 hours: UX 20; glossary/strings 30; multilingual integration 30; meaning review 25; accessibility/usability 20.

## Work boundaries and review

Own UX and language quality, including simple multilingual rendering work. Akshay builds straightforward components from your specifications. Harshit owns evidence correctness; do not translate new legal conclusions independently or permit a translation layer to replace citations.

Thulasi reviews domain terminology; Sabeena tests task completion; Harshit reviews evidence mapping and shared-contract changes.

Harshit has project-wide technical review and integration access. Each member remains accountable for their own deliverables. Routine work proceeds through the designated peer reviewer; access settings must be configured separately by the repository owner.

## Task packages

| Task | Target | Deliverable |
|---|---|---|
| D-01 | W1-2 | Confirm reviewable languages, user flows and a small translation feasibility sample. |
| D-02 | W3-4 | Deliver English/Hindi strings and accessible source-view specifications. |
| D-03 | W5-8 | Integrate Hindi, preserve legal terms and complete English/Hindi acceptance. |
| D-04 | W9-10 | Complete regional-language core flow and paired-language evidence checks. |
| D-05 | W11-14 | Resolve usability issues, freeze language resources and score multilingual fidelity. |
| D-06 | W15-16 | Run translation regression and verify final language assets. |

## Weekly responsibilities

| Week | Responsibility |
|---|---|
| 1 | User flow and language audit |
| 2 | Glossary v0; translation trial |
| 3 | English/Hindi strings |
| 4 | Source-view UX |
| 5 | Multilingual answer contract |
| 6 | Hindi render integration |
| 7 | Glossary v1; Hindi QA |
| 8 | English/Hindi acceptance |
| 9 | Regional integration |
| 10 | Three-language acceptance |
| 11 | Usability and meaning review |
| 12 | Freeze strings/glossary |
| 13 | Language scoring |
| 14 | Language/UX signoff |
| 15 | Translation regression |
| 16 | Verify language assets |

Weeks 15-16 are reserved for testing, repairs, packaging and submission; do not introduce new features during this buffer.

## Deliverable checklist

- [x] Intake and answer-flow specifications for Akshay ([deepshika-d01-specification.md](deepshika-d01-specification.md))
- [x] Controlled glossary v0 of 30 foundational terms ([controlled_glossary_v0.csv](../../../data/glossary/controlled_glossary_v0.csv); expanding to 80-120 in v1)
- [x] Accessibility checklist, semantic-fidelity and translation feasibility results ([deepshika-d01-specification.md](deepshika-d01-specification.md))
- [ ] English, Hindi and selected regional-language UI strings (Scheduled for Task D-02, Weeks 3–4)
- [ ] Reviewed translated answer fixtures and citation-parity checks (Scheduled for Tasks D-03/D-04)
- [ ] Relevant master-plan acceptance gates met and actual evidence recorded.
- [ ] Independent peer review completed and all critical findings resolved (Pending Thulasi, Sabeena, and Harshit review).
- [ ] Outputs integrated into the shared project; handoff notes and limitations documented.

## Start here

1. Name available Hindi and regional-language reviewers at kickoff. (Completed in Phase 1: see [deepshika-d01-specification.md](deepshika-d01-specification.md) Section 2; Telugu identified as leading candidate, maintained as an explicit kickoff decision awaiting team sign-off).
2. Define reviewed translations for jurisdiction, uncertainty, abstention and referral. (Completed in Phase 1: 30 terms in [controlled_glossary_v0.csv](../../../data/glossary/controlled_glossary_v0.csv)).
3. Specify how original legal names, section numbers and source IDs remain visible. (Completed in Phase 1: preservation rules `ID_IMMUTABLE`, `NUMBER_IMMUTABLE`, `NAME_IMMUTABLE` in [deepshika-d01-specification.md](deepshika-d01-specification.md)).

## Progress record

Use task IDs in issues and PRs. Replace the placeholder row only when work starts; checked boxes must link to real artifacts or results.

| Task ID | Status | Evidence / issue / PR | Reviewer | Blocker / next action |
|---|---|---|---|---|
| D-01 | In review (draft PR) | Branch `deepshika/d-01-phase-1`; [Draft PR #2](https://github.com/Harshit-ambati/IP-SAKTI-Sahayak/pull/2); [deepshika-d01-specification.md](deepshika-d01-specification.md), [controlled_glossary_v0.csv](../../../data/glossary/controlled_glossary_v0.csv), [verify_glossary.py](../../../scripts/verify_glossary.py) | Thulasi (terminology), Sabeena (usability), Harshit (evidence mapping) | Awaiting team kickoff sign-off on regional language; peer re-review following resolution of GLOSS-004, GLOSS-024, GLOSS-025, GLOSS-030, and feasibility sample framing |

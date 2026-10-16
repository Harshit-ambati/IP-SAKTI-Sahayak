# Suresh: Backend APIs, database, authentication, privacy and deployment

[Work-plan index](../README.md) · [Master plan](../MASTER_PLAN.md) · [Project README](../../../README.md)

**Owner:** Suresh

**Schedule:** weeks 1-16 from kickoff

**Capacity:** 10 hours/week; 125 planned hours over 16 weeks, with remaining capacity reserved for review, rework and integration.

**Status:** planned; completion must be supported by linked deliverables and checks.

## Module specification

- **Primary tasks:** build validated APIs, database/migrations, staff authentication and authorization, privacy controls, audit events, health checks, configuration and installation/deployment scripts.
- **Supporting tasks:** integrate Harshit's engine, support frontend fixtures, implement backup/restore and serve as deputy integrator.
- **Inputs needed:** week-1 contracts, data-retention policy and sample records. Use a stub retrieval adapter until the real engine arrives.
- **Outputs:** documented endpoints, schema/migrations, anonymous query sessions, staff-only corpus operations, minimal audit log, retention/deletion command and reproducible runbook.
- **Acceptance:** malformed requests fail cleanly; anonymous visitors cannot administer sources; staff privileges are checked server-side; no secrets or full user formulations enter routine logs; session boundaries prevent data leakage; deletion and restore are demonstrated. Staff passwords use an established password-hashing library. Networked release uses HTTPS; retained sensitive data needs encrypted storage or remains disabled.
- **Dependencies and handoff:** stub API in week 2, real query path in week 4, authentication by week 6, deployment rehearsal by week 8. Public hosting is not a completion dependency.
- **Effort:** 125 hours: API/data 45; access/security 25; privacy/audit 15; operations 20; integration/reviews 20.

## Work boundaries and review

Own backend and operations, and act as integration deputy. Merge routine reviewed changes within approved contracts; hold architecture, citation-policy and security-sensitive changes for Harshit's review. Use your own credentials and least-privilege deployment access.

Harshit reviews contracts, security and critical integration. Akshay checks client compatibility; Sabeena executes documented operational checks.

Harshit has project-wide technical review and integration access. Each member remains accountable for their own deliverables. Routine work proceeds through the designated peer reviewer; access settings must be configured separately by the repository owner.

## Task packages

| Task | Target | Deliverable |
|---|---|---|
| Su-01 | W1-2 | Publish service/data skeleton and stub classify/answer/source responses. |
| Su-02 | W3-4 | Integrate the real query engine through a stable adapter. |
| Su-03 | W5-6 | Add referral export, server-side validation and staff access checks. |
| Su-04 | W7-10 | Add minimal audit/retention, deletion, install scripts and restore rehearsal. |
| Su-05 | W11-14 | Harden permission boundaries, freeze configuration and reproduce on a second laptop. |
| Su-06 | W15-16 | Run access/recovery regression and deliver the installation archive. |

## Weekly responsibilities

| Week | Responsibility |
|---|---|
| 1 | Service/data skeleton |
| 2 | Stub endpoints |
| 3 | Real query adapter |
| 4 | API/data integration |
| 5 | Referral export; validation |
| 6 | Staff authentication/RBAC |
| 7 | Audit/retention implementation |
| 8 | Install/restore rehearsal |
| 9 | Deletion and isolation tests |
| 10 | Referral/privacy integration |
| 11 | Access/security fixes |
| 12 | Runbook and configuration |
| 13 | Reproduce test runs |
| 14 | Second-machine installation |
| 15 | Restore/access regression |
| 16 | Verify installation archive |

Weeks 15-16 are reserved for testing, repairs, packaging and submission; do not introduce new features during this buffer.

## Deliverable checklist

- [ ] Validated API contracts, fixtures and API documentation
- [ ] Database schema and migrations
- [ ] Staff authentication, role checks and protected corpus administration
- [ ] Minimal audit events and retention/deletion controls
- [ ] Install/deployment runbook, health checks and backup/restore instructions
- [ ] Relevant master-plan acceptance gates met and actual evidence recorded.
- [ ] Independent peer review completed and all critical findings resolved.
- [ ] Outputs integrated into the shared project; handoff notes and limitations documented.

## Start here

1. Agree request/response fields with Harshit and publish fixtures for Akshay.
2. Keep anonymous guidance separate from staff-only source administration.
3. Start with synthetic cases; leave persistent user-case storage disabled by default.

## Progress record

Use task IDs in issues and PRs. Replace the placeholder row only when work starts; checked boxes must link to real artifacts or results.

| Task ID | Status | Evidence / issue / PR | Reviewer | Blocker / next action |
|---|---|---|---|---|
| Not started | Planned | None yet | Unassigned | Confirm kickoff inputs |

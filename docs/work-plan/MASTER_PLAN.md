# IP-SAKTI Sahayak (SIH26045): 16-week execution plan

Status: planned work; implementation and evaluation results are not yet available. This plan is based on the project description and the six-member team's agreed allocation. Initial repository inspection on 16 October 2026 found an empty repository; this documentation establishes the starting work breakdown.

All weeks are relative to kickoff. Confirm the actual institutional deadline at kickoff; dated SIH details in the background report are not the schedule used here. All numerical targets are proposed acceptance gates, not achieved results or legal validation.

Start with the [work-plan index](README.md) or your [individual module](modules/). This master plan is the source of truth for shared scope, milestones and release gates. Keep member files consistent when the plan changes.

## 1. Scope, assumptions and achievable MVP

Build a text-based assistant that asks clarifying questions, identifies a provisional formulation route, retrieves authoritative evidence, and presents supported information with citations. Users can select English, Hindi or one regional language and explicitly choose India or international overview. The system provides information, not legal advice or a regulatory approval.

Assume part-time student availability, an existing laptop for development and demonstration, no spending commitment, no guaranteed domain expert and no unrestricted TKDL access. Validate laptop capability and language-review skills in weeks 1-2. A locally runnable release is required; a public hosted deployment is conditional on a suitable free environment.

### Required and optional work

| Area | Required by submission | Stretch after all release gates pass |
|---|---|---|
| Guided classification | Six provisional routes: classical/generic; patent-or-proprietary; novel/non-classical; phytopharmaceutical; Ayurveda Aahara; cosmetic. Ask for missing facts; allow unknown/ambiguous. Thulasi validates how these labels map to actual source definitions. | Learned classifier, ingredient extraction and richer product taxonomy. |
| Depth of guidance | Small, explicitly documented sets of India-focused patent/TK, biodiversity/ABS and product-category questions. Classical, proprietary, Aahara and cosmetic examples have tested intake and routing; detailed answers exist only where corpus coverage is approved. Novel/non-classical and phytopharmaceutical routes default to referral unless a narrow answer is supported. Aahara and other nutraceutical categories are not assumed interchangeable. | Broader regulatory, advertising, labelling and additional IP-right workflows. |
| International support | Separate WIPO/treaty overview and official links, with instrument status, party and jurisdiction checks where relevant. No country-specific export eligibility decisions. | One carefully selected export market, then others. |
| Evidence | Approximately 25-35 approved official documents and 150-250 useful provision-level passages; coverage and traceability take priority over counts. Versioned metadata, reproducible ingestion, exact-term plus semantic retrieval, source viewer and claim-to-source mapping. | Knowledge graph, automatic source monitoring and sophisticated reranking. |
| Answers and safety | One affordable local generation path proven on team hardware by week 2; structured output constrained to retrieved evidence. Block unknown citations; suppress unsupported claims; clarify, abstain or refer on missing/conflicting evidence. | Complex agents and autonomous multi-source research. |
| Languages | English, Hindi and one regional language for all core screens, intake, notices, supported answer topics and referral flow. Preserve source IDs and legal terms; suppress unverified translations. | Voice, speech recognition and more languages. |
| Referral | Downloadable review packet and official facilitator/registry pointers. User initiates any contact; no promise that an expert will respond. | Live expert portal, messaging and appointments. |
| Privacy and operation | Anonymous guidance, staff-only corpus administration, role checks, minimal audit events, retention/deletion controls, local installation, reproducible release and demo backup. | Public user accounts, dashboards and scale engineering. |

**Scope lock:** establish topic coverage in week 2, baseline corpus in week 8, feature freeze in week 12 and release candidate in week 14. Weeks 15-16 contain testing, repairs, packaging and submission only. Stretch work cannot displace required features, safety fixes or buffer.

### Capacity and workload

These are planning allowances, including meetings, reviews and documentation. Commit about 78% to planned work; leave the remainder for integration problems, absence and rework. The hours are estimates, not equal grading weights.

| Member | Weekly capacity | 16-week capacity | Planned effort | Uncommitted capacity |
|---|---:|---:|---:|---:|
| Harshit | 12 h | 192 h | 150 h | 42 h |
| Thulasi | 10 h | 160 h | 125 h | 35 h |
| Deepshika | 10 h | 160 h | 125 h | 35 h |
| Suresh | 10 h | 160 h | 125 h | 35 h |
| Sabeena | 6 h | 96 h | 75 h | 21 h |
| Akshay | 6 h | 96 h | 75 h | 21 h |
| **Total** | **54 h** | **864 h** | **675 h** | **189 h** |

Harshit owns the hardest technical work and cross-module integration. Suresh is the integration deputy and can merge routine changes after independent review. Every owner decides routine implementation within the agreed contracts. Harshit reviews all architecture, evidence-validation, jurisdiction, security-sensitive and release changes, and may inspect or request changes in every module. His review does not replace ownership.

## 2. Modules, responsibilities and acceptance

### Harshit: architecture, RAG and evidence validation

- **Primary tasks:** define module boundaries and response contracts; implement ingestion adapters, provision-aware chunking, exact-term/semantic retrieval, evidence-constrained generation, citation validation, abstention and jurisdiction isolation; integrate the system and lead technical decisions.
- **Supporting tasks:** mentor difficult fixes, review critical PRs, maintain architectural decisions, compare retrieval baseline against hybrid retrieval, assemble reproducible release and evaluation configuration.
- **Inputs needed:** three sample sources and draft rules from Thulasi by week 2; API fixtures from Suresh; glossary constraints from Deepshika; benchmark format from Sabeena.
- **Outputs:** architecture note, versioned schemas, retrieval/generation module, claim-evidence validator, safety policy, evaluation runner and integrated release.
- **Acceptance:** every emitted citation resolves to a real indexed passage and provision locator; wrong-jurisdiction sources are blocked; missing evidence yields clarification/abstention; citation support and retrieval meet section 6 gates. Automatic ID checks are not presented as proof of legal entailment.
- **Dependencies and handoff:** start with synthetic fixtures in week 1 and three real documents in week 2; ingest weekly batches instead of waiting for the entire corpus.
- **Effort:** 150 planned hours: architecture/contracts 20; retrieval/ingestion 45; answer validation/safety 35; integration/reviews 30; evaluation/release 20.

### Thulasi: authoritative corpus and decision-rule specification

- **Primary tasks:** research public official sources; record provenance and access rights; extract provision locators; build formulation questions, category rules and bounded IP/ABS/TK routing tables.
- **Supporting tasks:** create source-grounded expected answers, verify corpus revisions, review citation support, document unresolved interpretations and international scope boundaries.
- **Inputs needed:** frozen MVP topic list, metadata template and ingestion feedback; public source portals, not private datasets.
- **Outputs:** source register, approved provision extracts, version/change log, rule table with question/condition/route/source fields, coverage map and expected-evidence annotations.
- **Acceptance:** at least 25 useful approved documents or a documented smaller corpus covering every supported topic; every source has URL, authority, jurisdiction, publication/effective date and version where available, capture date, checksum, access/reuse status and reviewer. Missing dates are explicitly unknown, never invented; uncertain legal status excludes an item from definitive guidance. Every decision rule cites a provision; ambiguity produces clarification/referral.
- **Dependencies and handoff:** deliver three records in week 2, 10 approved sources in week 4, around 20 in week 6 and baseline coverage in week 8. One reviewer checks a sample from each batch before activation.
- **Effort:** 125 hours: research 45; metadata/extraction 25; rules 25; evidence annotation 20; freshness/report review 10.

### Deepshika: multilingual experience, terminology and accessibility

- **Primary tasks:** design intake and answer flows; own translation resources, language switching, glossary and accessible interaction; implement multilingual rendering and legal-term preservation with Harshit.
- **Supporting tasks:** give Akshay component specifications and reviewed strings; arrange language review within the team; help assess comprehension and translation failures.
- **Inputs needed:** response schema, initial source terminology, supported-topic list and confirmed regional language. Do not assume external bilingual experts are available.
- **Outputs:** user-flow sketches, three-language strings, 80-120 controlled glossary entries, reviewed translation fixtures, citation-parity checks and accessibility findings.
- **Acceptance:** core task can be completed in all three languages; legal names/provision IDs remain stable; no critical change to negation, duty, exception or jurisdiction in release samples; 100% citation-ID parity across translated benchmark variants; keyboard navigation, visible labels and usable mobile layout. Unverified dynamic translation falls back to a localized uncertainty message and cited source, not an invented translation.
- **Dependencies and handoff:** strings and screen specifications begin in week 2; integrate against mocked answers in week 3; English/Hindi by week 8 and regional language by week 10.
- **Effort:** 125 hours: UX 20; glossary/strings 30; multilingual integration 30; meaning review 25; accessibility/usability 20.

### Suresh: backend, data, access controls and deployment

- **Primary tasks:** build validated APIs, database/migrations, staff authentication and authorization, privacy controls, audit events, health checks, configuration and installation/deployment scripts.
- **Supporting tasks:** integrate Harshit's engine, support frontend fixtures, implement backup/restore and serve as deputy integrator.
- **Inputs needed:** week-1 contracts, data-retention policy and sample records. Use a stub retrieval adapter until the real engine arrives.
- **Outputs:** documented endpoints, schema/migrations, anonymous query sessions, staff-only corpus operations, minimal audit log, retention/deletion command and reproducible runbook.
- **Acceptance:** malformed requests fail cleanly; anonymous visitors cannot administer sources; staff privileges are checked server-side; no secrets or full user formulations enter routine logs; session boundaries prevent data leakage; deletion and restore are demonstrated. Staff passwords use an established password-hashing library. Networked release uses HTTPS; retained sensitive data needs encrypted storage or remains disabled.
- **Dependencies and handoff:** stub API in week 2, real query path in week 4, authentication by week 6, deployment rehearsal by week 8. Public hosting is not a completion dependency.
- **Effort:** 125 hours: API/data 45; access/security 25; privacy/audit 15; operations 20; integration/reviews 20.

### Sabeena: benchmark records, user documentation and feedback

- **Primary tasks:** maintain scenario files and expected-result templates; execute repeatable test checklists; record results, defects and user feedback; write the guide and organize report/presentation evidence.
- **Supporting tasks:** coordinate six to eight consenting student/potential-user walkthroughs where feasible, maintain milestone checklist and rehearse the live demo with Akshay. Usability participants do not certify legal correctness.
- **Inputs needed:** test template from Harshit, source-based labels from Thulasi and language fixtures from Deepshika. Sabeena records legal evaluations but does not independently determine legal truth.
- **Outputs:** 120 canonical scenarios, test-run ledger, issue evidence, user guide, feedback summary, report draft and presentation outline.
- **Acceptance:** scenarios contain ID, facts, jurisdiction, expected route, answerability, evidence IDs and rubric; development/holdout labels are frozen separately; each final result records release/model/corpus version and actual output; documentation covers supported scope, limitations, citations, abstention, privacy and referral.
- **Dependencies and handoff:** 20 scenarios by week 2, 60 by week 4, 120 by week 7; guide skeleton by week 4 and usable guide by week 10. Complex automation belongs to Harshit/Suresh.
- **Effort:** 75 hours: scenario organization 20; test execution 20; guide/report/presentation 25; feedback/coordination 10.

### Akshay: straightforward frontend screens and demo operation

- **Primary tasks:** implement home/scope notice, intake form, answer view, jurisdiction/language controls, source cards and referral-download screen from approved specifications.
- **Supporting tasks:** add loading/error/empty/abstention states, responsive styles, basic interface checks, screenshots and demo setup.
- **Inputs needed:** Deepshika's layouts/strings and Suresh's response fixtures. Harshit owns evidence logic; Suresh owns authentication.
- **Outputs:** six simple screen/component groups, source-link behavior, API-connected interface, UI checklist and demonstration assets.
- **Acceptance:** the complete flow works with mock data by week 4 and real data by week 8; citations open the correct source/excerpt; jurisdiction and language persist correctly; unsupported/error states remain understandable; no backend rules or secrets are embedded in the interface.
- **Dependencies and handoff:** start with fixture JSON in week 2; finish core components by week 6 and end-to-end UI by week 8, leaving later capacity for testing and demo work.
- **Effort:** 75 hours: screen/components 35; API wiring 15; interface checks 15; demo assets 10.

## 3. Weekly schedule and integration gates

Every week includes a 20-minute Monday planning/blocker meeting, asynchronous midweek updates and a 45-minute Friday integrated demonstration with issue triage. Alternate-week reviews reserve 20 additional minutes for evidence and safety. These meetings are included in capacity. A blocked owner flags the issue within one working day; Suresh/Harshit arrange fixtures, pairing or a narrower task within the next day.

| Week | Team milestone and integration/acceptance gate |
|---|---|
| 1 | Kickoff; confirm language, hours and supported topics; create repository skeleton, issue board and architecture decision record. All six can run the skeleton locally. |
| 2 | Freeze v1 request/response/source contracts; three real sources and 20 scenarios available. Mock flow works across frontend/backend. Prove local generation and translation feasibility; select fallback scope immediately if either fails. |
| 3 | Integrate first source ingestion, classifier questions and English intake; run a cited response using a small real corpus. Log evidence and API failures. |
| 4 | First vertical-slice milestone: intake → provisional class → real retrieval → cited answer or abstention → source view. Ten sources and 60 draft scenarios; alpha review. |
| 5 | Add IP/ABS/TK route flags, explicit unknown state, jurisdiction filtering and downloadable referral packet. Test missing-facts and wrong-jurisdiction cases. |
| 6 | Hybrid retrieval, claim IDs, backend staff authorization and source cards integrated. Around 20 sources. Core Akshay screen work complete; review denial paths and citation failures. |
| 7 | Complete 120 canonical scenarios and freeze 60 development/60 holdout cases. Start Hindi integration and translation checks; run development benchmark only. |
| 8 | Midpoint beta: baseline corpus coverage, English/Hindi core flow, real UI/API/engine integration and local deployment rehearsal. Demonstrate backup/restore; re-estimate remaining work. |
| 9 | Improve only benchmark-identified retrieval/safety faults; integrate regional strings/answers and privacy deletion; audit permission boundaries. |
| 10 | Three-language feature milestone; complete core UX, approved multilingual answer topics, referral packet and user guide. Test citation parity end to end. |
| 11 | Conduct usability sessions; test retrieval against stale/conflicting evidence and prompt injection; fix critical comprehension, leakage and routing defects. |
| 12 | Feature freeze. Required flows complete, no new features. Produce report draft, deployment runbook and repeatable full development-suite result. |
| 13 | Formal held-out evaluation by independent teammates; record raw outputs, metrics, errors and review disagreements. Verify source status and multilingual semantic fidelity. |
| 14 | Release candidate, report and presentation complete; full installation rehearsal on a second laptop; 8-10-minute demo rehearsal with backup. Gate review confirms week-15 readiness. |
| 15 | Buffer week 1: regression, browser/accessibility/security checks, critical fixes and re-tests; final documentation and corpus/source-link check. No feature expansion. |
| 16 | Buffer week 2: contingency fixes, final smoke test, release archive/checksums, report and video verification, submission and receipt capture. Target internal handoff at least 48 hours before the actual deadline. |

### Responsibilities in every week

Abbreviations: H = Harshit; T = Thulasi; D = Deepshika; Su = Suresh; Sa = Sabeena; A = Akshay. Owners also review the relevant PRs and record their work each week.

| Week | H | T | D | Su | Sa | A |
|---|---|---|---|---|---|---|
| 1 | Architecture and contracts | Topic/source coverage map | User flow and language audit | Service/data skeleton | Test/report templates | Screen skeleton |
| 2 | Model feasibility and fixtures | Three sources; draft rules | Glossary v0; translation trial | Stub endpoints | First 20 scenarios | Mock intake/answer |
| 3 | Ingestion and retrieval baseline | Category questions; six sources | English/Hindi strings | Real query adapter | Alpha checklist | Intake validation/states |
| 4 | Vertical slice; evidence IDs | Ten sources; expected evidence | Source-view UX | API/data integration | 60 scenarios; guide outline | Six component groups |
| 5 | Jurisdiction and abstention | IP/ABS/TK rule table | Multilingual answer contract | Referral export; validation | Safety-case records | Source/referral views |
| 6 | Hybrid search and validator | About 20 sources; rule review | Hindi render integration | Staff authentication/RBAC | Citation/interface test runs | Finish core screens |
| 7 | Evaluation runner | Check benchmark evidence | Glossary v1; Hindi QA | Audit/retention implementation | Freeze 120-case split | API wiring and error states |
| 8 | Full beta integration | Corpus baseline v1 | English/Hindi acceptance | Install/restore rehearsal | Beta results and guide draft | End-to-end UI acceptance |
| 9 | Evidence/safety fixes | Conflict/freshness review | Regional integration | Deletion and isolation tests | Defect tracking | Responsive/keyboard fixes |
| 10 | Citation/translation integration | Review supported answers | Three-language acceptance | Referral/privacy integration | User guide v1 | Full-flow UI regression |
| 11 | Injection/conflict tests | Review legal error cases | Usability and meaning review | Access/security fixes | Feedback sessions/summary | UI feedback repairs |
| 12 | Feature freeze and dev metrics | Corpus/rules freeze | Freeze strings/glossary | Runbook and configuration | Report draft/results tables | Screenshots/demo draft |
| 13 | Analyze held-out errors | Evidence scoring | Language scoring | Reproduce test runs | Record blinded results | Browser/accessibility checks |
| 14 | Release candidate approval | Source-status signoff | Language/UX signoff | Second-machine installation | Final report/slides | Demo rehearsal/backup |
| 15 | Critical fixes/regression | Source recheck | Translation regression | Restore/access regression | Final test ledger | Demo/UI smoke tests |
| 16 | Tag/package technical release | Verify corpus handover | Verify language assets | Verify installation archive | Submission checklist/receipt | Live demo/video handover |

Critical path: contracts and sample sources (week 2) → real cited vertical slice (week 4) → full integration (week 8) → three-language scope (week 10) → feature freeze (week 12) → held-out evaluation and release candidate (weeks 13-14). Frontend, documentation and translation start with fixtures; none waits for the full RAG module.

## 4. Responsibility and decision matrix

Owner is accountable for producing the deliverable. Support contributes work. Reviewer checks it independently. Approver accepts it for integration or release; approval is a capstone engineering/content decision, not legal certification.

| Deliverable | Owner | Support | Reviewer | Approver |
|---|---|---|---|---|
| Architecture and contracts | H | Su | Su, D | H after independent review |
| Source register/corpus | T | Sa | H for provenance; D for terminology | T for content; H for corpus activation |
| Classification/routing specification | T | H | Su, D | T for evidence; H for technical adoption |
| RAG, citations and abstention | H | Su, T | Su for code; T for claim support | H after both reviews |
| APIs and database | Su | H | H for contracts/security; A for client compatibility | Su for routine changes; H for sensitive changes |
| Authentication, privacy and deployment | Su | H | H, Sa for checklists | H |
| Multilingual and accessibility module | D | A, T | T for terms; Sa for task tests | D for routine content; H for evidence/contract changes |
| Frontend components | A | D | D, Su | D for routine UI; H for citation/jurisdiction behavior |
| Benchmark design and labels | Sa | T, D | H for metrics; Su for reproducibility | T/D for domain/language labels; H for benchmark protocol |
| Evaluation results | Sa | H, T, D | Su reproduces; A checks UI evidence | H, with unresolved disagreements disclosed |
| User guide and final report | Sa | All module owners | T, D, H on their sections | H; all owners acknowledge their sections |
| Demo and submission package | A for demo; Sa for package | All | Su for installation; D for presentation | H for technical release; team for final submission |

All members have repository read access. Harshit retains repository administration and access to every module. Others receive only contributor access needed for their work; Suresh receives deployment operations permissions, not personal account credentials. Personal repositories may not offer every granular role: use the permissions actually available, or an organization repository if the team needs finer control. Only Harshit and Suresh handle deployment secrets. Each uses their own account and credentials; no shared passwords or personal access tokens.

Routine PRs need one independent peer review and passing checks. Suresh or Harshit can integrate them. Harshit's own critical code needs Suresh's review and Thulasi's evidence review where applicable; self-approval is not a substitute for independent review. If Harshit is unavailable, Suresh can merge routine work but holds critical architecture/safety changes for review.

## 5. Day-to-day workflow and integration contracts

### Source collection and activation

1. Thulasi opens a source issue tied to a supported question or routing rule. Prefer statutes, gazettes, rules, official regulators and treaty instruments; distinguish guidance from binding text and drafts from operative instruments.
2. Record source ID, title, URL, issuing authority, country/jurisdiction, instrument type, publication/effective dates when available, version/amendment/supersession status, retrieval date, checksum and access/reuse conditions. A portal landing page is a discovery link, not a provision citation.
3. Preserve authorized source copies or refetch instructions. Public visibility does not automatically grant unrestricted redistribution. Never scrape restricted TKDL material or use unofficial mirrors as controlling authority.
4. Extract short, useful provision passages with page/section/article locators. Review extraction quality, amendments and relevance. Quarantine doubtful records.
5. Harshit validates schema/chunks; Thulasi and an independent teammate check sample mappings and source support. Publish an immutable corpus version only after checks pass.
6. Recheck sources at weeks 8, 13 and 15, and before any affected answer is re-enabled after a change. Retain older versions for reproducibility, not as current default evidence.

Suggested official discovery sources: [IP India patent rules](https://ipindia.gov.in/pages/patents/publications/rules), [India Code Patents Act](https://www.indiacode.nic.in/bitstream/123456789/1392/1/A1970-39.pdf), [Ministry of Ayush rules collection](https://ayush.gov.in/resources/pdf/quality_standards/Drugs-and-Cosmetics-Act-Rules.pdf), [National Biodiversity Authority](https://www.nbaindia.nic.in/), [FSSAI Ayurveda Aahara order and annexure](https://www.fssai.gov.in/upload/uploadfiles/files/Order%20dated%2025-07-2025%20enclosing%20Ayurveda%20Aahara.pdf), [WIPO treaty page](https://www.wipo.int/en/web/treaties/ip/gratk/index) and [TKDL public overview](https://www.tkdl.res.in/tkdl/langdefault/common/Abouttkdl.asp). These are starting points; the corpus must verify the exact applicable text and status at ingestion. WIPO adoption is not automatically treated as a domestic obligation, and TKDL public background is not access to its restricted records.

### Contracts and implementation

Choose a familiar web UI, one Python API service and one local database in week 1. FastAPI and SQLite with FTS5 are a small-stack option documented by their [official API framework documentation](https://fastapi.tiangolo.com/) and [SQLite full-text search documentation](https://www.sqlite.org/fts5.html). Add a local embedding index and one tested local generation model, after checking license, download size, memory and latency. Pin actual versions after the week-2 feasibility run. Do not introduce microservices or a graph database for the MVP.

Freeze these objects in week 2: Intake, ClassificationResult, SourceRecord, EvidencePassage, AnswerResult and ReferralPacket. Use a few endpoints such as classify, answer, source lookup, referral export, health and staff-only corpus administration; exact naming is Suresh's decision within the contract.

An answer includes status (`clarify`, `answered`, `abstained`, `referral`), selected jurisdiction/language, provisional class, assumptions, claims with evidence IDs, cited provision locators, limitations and corpus/model versions. India and international requests use separate filters; changing jurisdiction reruns retrieval. Language changes retain the same evidence mapping. Unknown source IDs, missing mandatory facts and unresolved jurisdiction mismatches block substantive output.

Display evidence status as supported, partial or insufficient, with reasons such as missing facts or conflicting passages. A model's numerical confidence or similarity score is not legal correctness. Prefer short evidence-constrained answers and quotations with careful paraphrases over broad generated advice.

### Issues, pull requests and completion

- One issue per task, with owner, week, dependency, acceptance evidence and size estimate. Break work larger than roughly one week into smaller tasks. Labels can identify module, blocker, defect severity and release gate.
- Work on short branches; open small PRs at least twice a week during implementation. Avoid week-long private integration branches. Contract changes require a migration note and updates to all affected fixtures.
- PR evidence includes linked issue, behavior change, checks, relevant screenshot or sample response, and evidence/corpus implications. Do not put sensitive formulations in issues or screenshots.
- CI checks formatting/build, schema compatibility, critical rule/citation/jurisdiction tests, permission-denial tests and a small offline end-to-end smoke suite. The large evaluation suite runs at milestone gates, not on every text edit.
- A task is done only after implementation, independent review, relevant tests, documentation and integration into the shared development branch. A mock response is labelled as a fixture and never reported as a completed real integration.
- Default to no saved user case. Audit request ID, time, route, evidence IDs, versions and status without recording full questions/formulations. If optional case storage is enabled, require consent, access checks, encrypted storage and a short documented retention period, provisionally seven days, with user deletion. Use synthetic demo data.

## 6. Submission artifacts and evaluation gates

### Concrete artifacts

| Artifact | Required contents | Due |
|---|---|---|
| Code release | UI/API/engine, staff access controls, rule definitions, migrations, dependency lockfiles, example configuration without secrets, run/install scripts, relevant automated tests and release tag | RC W14; final W16 |
| Source corpus | Approximately 25-35 approved sources; source/provision records, lawful snapshots or retrieval instructions, version manifest/checksums, coverage map, exclusions and change log | Baseline W8; recheck W15 |
| Benchmark | 120 canonical cases: 60 classification cases (10 per provisional route), 20 IP/ABS/TK evidence cases, 20 insufficient/conflicting-evidence cases and 20 adversarial/jurisdiction/privacy cases. Label answerability separately and ensure at least 20 unanswerable held-out cases across groups. | Frozen W7 |
| Language benchmark | Thirty selected canonical cases also rendered in Hindi and the regional language: 10 development and 20 holdout cases. This adds 60 prompt variants, producing 180 prompts in total; report unique-case and variant counts separately. | W10 |
| Evaluation package | 60 canonical development and 60 canonical holdout cases, with the language variants kept in the same split as their originals; raw outputs, rubrics, scores, denominators, reviewers, disagreement log and model/corpus/release versions | W13-14 |
| User guide | Installation/user quick start, guided intake, jurisdiction/language controls, source interpretation, scope limits, abstention/referral, privacy/deletion and troubleshooting | W10; final W15 |
| Final report | Problem, bounded scope, architecture, source methodology, each member's contribution, benchmark method, baseline comparison, actual results, failed cases, limitations, privacy/threat model and future work | Draft W12; final W15 |
| Live demonstration | 8-10-minute script, synthetic inputs, local installation, source view, three languages, India/international separation, abstention and referral; backup video and source snapshot | Rehearsal W14; final W16 |

Holdout expected answers remain outside model prompts and retrieval indexes. Freeze them before tuning; Sabeena coordinates independent scoring by teammates who did not author the relevant module. If a holdout failure is used to make a fix, report that rerun as regression on a previously seen test and add a small untouched confirmation set where feasible. Do not relabel the same cases as a new independent evaluation.

### Proposed release gates

| Dimension | Acceptance and measurement |
|---|---|
| Classification | At least 0.85 macro-F1 on the held-out classification subset; no high-risk route below 0.75 recall. Report each class's sample count, confusion matrix and ambiguous-case behavior. Correct referral routing counts as routing, not proof of a legal classification. |
| Retrieval | Gold supporting provision appears in top five for at least 85% of answerable evidence-labelled cases; aim for 90%. Compare exact-term baseline with hybrid retrieval on the same frozen questions. |
| Citation integrity | 100% emitted citation IDs/locators resolve; zero fabricated authorities; at least 90% of scored material claims are supported by the cited passage. Thulasi and another teammate score claim support using a shared rubric. Report disagreements and critical errors separately. |
| Safety | At least 90% of known unanswerable cases trigger safe abstention/referral (recall); at least 90% of abstentions are appropriate (precision). Report answer rate on answerable cases to expose an assistant that refuses everything. |
| Jurisdiction | Every answer visibly labelled; zero critical mixing errors in the release suite; country-specific unsupported export questions abstain. |
| Multilingual | 100% citation-ID parity on paired cases; zero unresolved critical semantic reversals in release samples; average meaning/comprehension rating at least 4/5 from available bilingual team reviewers. Report reviewer qualifications and missing expertise. |
| Usability | Target at least 80% completion and average comprehension at least 4/5 on a small documented sample, ideally 6-8 participants. Report actual counts and participant background; do not generalize from a small convenience sample. |
| Privacy/security | All defined unauthorized-operation and session-isolation tests pass; no secrets in repository/logs; retention/deletion and recovery demonstrated; document remaining threat-model limitations. |
| Operation | Second-machine installation passes, core synthetic demo runs without live third-party APIs, and observed latency is recorded on the actual demo hardware. Set a practical latency budget by week 2 rather than promising GPU performance. |

These are student-reviewed engineering and evidence-support results. Without an independent qualified domain expert, do not claim expert-validated legal-answer accuracy. The report's expert-scoring aspirations remain future validation. A known consequential unsupported claim, fabricated authority, data leak or critical translation reversal blocks release of the affected feature even if an average score passes. If a target is missed, narrow or disable the failing scope and rerun the affected tests; do not lower the target silently.

## 7. Risks, triggers and fallback plans

| Risk and owner | Trigger | Practical fallback |
|---|---|---|
| Missing/restricted sources — T | Required provision unavailable, undated or not reusable | Replace with lawful official material where possible; exclude unsupported topic; document the gap and use referral. TKDL remains public explanatory guidance and access pointers. |
| Paid/unreliable API — H, Su | No funded account or unstable free quota by W2 | Use a tested local model with cached authorized corpus. If generation cannot run adequately, deliver an explicitly reduced extractive evidence-search/templated assistant and disclose that it does not satisfy the full generative MVP; agree this scope at W2, not during final week. |
| Laptop capacity — H | Memory/latency trial fails W2 | Reduce model size, context and corpus; constrain response length; retain laptop-local retrieval. A recorded demo backs up the live demo but is not represented as live execution. |
| Incorrect legal information — T, H | Unsupported claim, obsolete provision or failed source review | Quarantine source/topic, switch affected answers to abstention, repair evidence mapping and rerun regression. Make no patentability, approval or compliance guarantees. |
| Translation error/reviewer gap — D | Duty, exception, negation or category meaning changes; no competent reviewer | Use reviewed topic-limited translations and localized safe messages; retain original evidence text. Choose a regional language the team can actually review at kickoff. Disclose any remaining language limitation. |
| No external legal expert — T, Sa | Expert unavailable by W3 | Use transparent student source-based labels with two-person review; document unresolved interpretations; do not claim legal certification. Optional expert feedback can be added if it arrives. |
| Integration failure — Su, H | Two weekly vertical-slice checks fail | Freeze contract changes, pair on minimal failing path, restore last passing build and cut low-priority scope. Keep independent modules moving with fixtures. |
| Schedule delay — all owners | Task slips over three working days or W4/W8 gate missed | Reassign support, split the task and remove stretch work immediately. Reduce supported topics before reducing evidence or privacy safeguards. Protect W15-16. |
| Harshit overload — Su | Critical reviews queue beyond two working days | Deputy handles routine integration, peers review scoped changes, owners bring reproducible issues. Escalate only architecture, safety, security and contract decisions to Harshit. |
| Data/secret exposure — Su | Logs or commit contain user data/credentials | Disable affected storage/access, rotate exposed credentials, remove sensitive material through the appropriate repository process and verify the fix. Prevent with synthetic data and minimal logging. |
| Legal update — T | Source status changes after corpus freeze | Mark affected route stale, review replacement text and rerun related tests; abstain until cleared. Preserve evaluation corpus separately for reproducibility. |
| Hosting/network failure — Su, A | Free host unavailable or venue network fails | Run on the tested laptop/local network with cached corpus, bundled model and backup video; validate setup on a second machine in W14. |

## 8. Final submission checklist

- [ ] All six have completed their owned artifacts; contribution records link to issues/PRs/documents.
- [ ] A clean checkout/archive installs on a second laptop using documented commands and no shared credentials.
- [ ] Intake asks necessary clarifications; all six provisional routes and unknown/referral states are demonstrated.
- [ ] Supported topics are explicit; unsupported legal/export questions safely abstain.
- [ ] India and international retrieval/output remain separate and visibly labelled.
- [ ] Every substantive claim has verifiable provision evidence; no fabricated authorities or known consequential unsupported release claims remain.
- [ ] Sources have provenance, status checks and version records; unknown metadata is explicit and restricted material is excluded.
- [ ] English, Hindi and the selected regional language complete the supported core flow with reviewed terminology and citation parity.
- [ ] Evidence status states coverage/limitations without claiming legal certainty.
- [ ] Referral packet includes the question, class, jurisdiction, assumptions, citations and unresolved issues, under user control.
- [ ] Staff access checks, privacy notices, minimal audit logs, retention/deletion and backup/restore are verified.
- [ ] Development/holdout metrics, raw outputs, reviewer qualifications, failures and limitations are included accurately.
- [ ] User guide, final report, architecture, source manifest, code release, slides and demo/video are consistent with the actual delivered scope.
- [ ] No unresolved critical safety/security defects remain; lower-priority defects have documented impact and workarounds.
- [ ] Harshit approves the technical release; every owner verifies their section; the team completes submission and saves the receipt.

## Kickoff decisions: resolve these five items

1. Confirm kickoff date, actual institutional deadline and each member's weekly hours; keep the plan relative until dates are agreed.
2. Select the regional language and name a competent reviewer for both Hindi and that language.
3. Agree the exact supported question/topic list and international-overview boundary; reject country-by-country export work from the MVP.
4. Select the demo laptop, familiar implementation stack and W2 model/translation feasibility test; decide whether hosting is needed beyond local submission.
5. Confirm repository collaborator/deployment permissions, review deputy, privacy defaults and the institution's report/demo submission format.

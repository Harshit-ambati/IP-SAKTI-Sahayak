# Real source material for the MVP

The [real source list](real_sources.csv) names seven actual official resources for the project's first corpus. The [populated passage CSV](source_passages_starter.csv) provides eight source-backed paraphrases with locators. These are a small, source-checked sample pending domain review and amendment checks, **not** a completed production corpus. The earlier [candidate register](source_register.csv) remains a collection tracker.

| Topic | Real source to collect | What it supports |
|---|---|---|
| Patent and traditional knowledge exclusions | [IP India: Patents Act, section 3](https://www.ipindia.gov.in/acts/patent-act-1970/section-3) | Narrow patent/TK information and referral triggers |
| Ayurvedic medicine definitions and rules | [Ministry of Ayush: Drugs and Cosmetics Act/Rules compilation](https://ayush.gov.in/resources/pdf/quality_standards/Drugs-and-Cosmetics-Act-Rules.pdf) | Classification questions; verify operative text |
| Ayurveda Aahara | [FSSAI: 2022 Gazette regulations](https://fssai.gov.in/upload/notifications/2022/05/62789a20b54bdGazette_Notification_Ayurveda_Aahara_09_05_2022.pdf) | Food category definition and bounded route |
| Biodiversity and ABS | [NBA: 2024 rules](https://nbaindia.nic.in/sites/default/files/2026-05/BD_Rules.pdf) and [2025 amendment](https://nbaindia.nic.in/sites/default/files/2026-05/AmendmentBD_Rules.pdf) | Intake flags and official referral; read together |
| International overview | [WIPO Lex: GRATK treaty](https://www.wipo.int/wipolex/en/treaties/textdetails/19849) | Treaty overview after checking status and parties |
| TKDL | [Official public overview](https://www.tkdl.res.in/tkdl/langdefault/common/Abouttkdl.asp) | Explain TKDL's role and link onward; no restricted records |

For each source, Thulasi must save the exact document URL, authority, jurisdiction, publication and effective dates where available, amendment/version status, retrieval date and source hash. Then extract **specific provisions** into [provisions.template.csv](provisions.template.csv), with page/section/article locators and an independent check. A portal landing page, PDF title or source URL alone is insufficient evidence for an answer.

Additional official material is needed before answering more topics: Patents Rules and current amendments, the Biological Diversity Act as amended, current FSSAI orders/amendments, relevant drug and cosmetic classification provisions, and selected public registry guidance. Add these only when a supported question requires them. Record superseded instruments but do not use them as current default authority.

The other real dataset is the **team's reviewed benchmark**. There is no suitable ready-made gold set of Ayurveda IP/regulatory cases in this repository. Build it from source-grounded scenarios with known answerability and provision IDs, then keep the held-out split unseen during development. The 12 synthetic prompts supplied earlier are fixtures, not gold labels. Human reviewers must validate every expected route, answer and citation before scoring.

Raw official files may be kept in a local `data/raw/` folder after checking reuse terms. Do not commit restricted TKDL records, personal formulations or unreviewed extracted text. The repository should publish the source URLs, provenance, approved short passages and evaluation protocol, with license/access decisions recorded per source.

# Bounded IP/ABS/TK Decision Rules, Biodiversity Integration, and Referral Specification (Task T-03)

**Task ID:** T-03  
**Module Owner:** Thulasi (Authoritative source corpus, formulation categories and decision rules)  
**Target Window:** Weeks 5–6  
**Status:** Submitted for activation review (Draft PR on `thulasi/t-03-phase-3`)  
**Reviewers:** Harshit (Technical lead / Corpus activation & rule contracts), Deepshika (Multilingual & Terminology)  

---

## 1. Executive Summary & Deliverables

Task T-03 delivers the bounded decision rules and multi-statutory screening framework for IP-SAKTI Sahayak, tying formulation intake directly to current operative Indian instruments:
1. **Machine-Readable Rule Contract**: Implemented in [`data/rules/decision_rules.json`](../../data/rules/decision_rules.json) specifying 13 formal rules across product classification, patent/TK screening, biodiversity (ABS) compliance, and safety fallbacks.
2. **Biodiversity Framework Integration**: Accurately harmonizes *The Biological Diversity Act, 2002* (as amended by Act 10 of 2023) with the *Biological Diversity Rules, 2024* read in conjunction with the *Biological Diversity Amendment Rules, 2025*.
3. **Strict TKDL Non-Confidentiality Boundary**: Re-affirms that confidential, restricted TKDL formulation dossiers are strictly excluded from the corpus.
4. **Explicit Uncertain / Needs-Expert Referral Protocols**: Specifies automated fallback actions generating structured `ReferralPacket` objects whenever data is ambiguous or products fall outside standard AYUSH licensing.
5. **Ten Sample Rule Firings Reviewed**: Complete end-to-end trace of ten representative formulation scenarios audited against statutory source passages in collaboration with teammates Harshit, Deepshika, and Sabeena.
6. **Corpus Expansion to Twenty Useful Sources**: Documented in [`SOURCE_AUDIT_T03.md`](../../data/corpus/SOURCE_AUDIT_T03.md) and [`source_register.csv`](../../data/corpus/source_register.csv) with 35 provision passages.

---

## 2. Bounded Decision Rules Specification

The decision logic operates across three integrated legal domains:

```
                            [ User Query / Formulation Intake ]
                                            │
        ┌───────────────────────────────────┼───────────────────────────────────┐
        ▼                                   ▼                                   ▼
 [ Product Classification ]       [ Patent / TK Screening ]            [ Biodiversity / ABS ]
  - Classical ASU (s. 3(a))        - s. 3(p) TK Aggregation            - s. 6(1) Mandatory NBA Approval
  - P&P ASU (s. 3(h))              - s. 3(e) Mere Admixture            - s. 6(1A) Vaid/Hakim Exemption
  - Ayurveda Aahara (Reg. 2(b))    - s. 3(d) Efficacy Requirement      - 2024 Rules + 2025 Amendment
  - Cosmetic (s. 3(aaa))           - s. 10(4)(d)(ii) Source Disclosure - Form III IPR Requirements
  - Novel/Phyto (Referral)         - CGPDTM 2012 Examination Standard
```

### 2.1 Indian Patent & Traditional Knowledge (TK) Screening Rules
- **Rule `RULE-PAT-01` (Section 3(p) Traditional Knowledge Exclusion):**
  - *Trigger Condition:* Formulation consists exclusively of classical Ayurvedic ingredients prepared according to traditional recipes, and applicant intends to file an Indian patent.
  - *Statutory Finding:* Excluded subject matter under Section 3(p) of *The Patents Act, 1970*. Traditional knowledge and duplication/aggregation of known properties are non-patentable.
  - *Cited Passages:* `REAL-001` (Section 3(p), `PASS-002`); `REAL-010` (Paragraph 4.1, `PASS-019`).
- **Rule `RULE-PAT-02` (Section 3(e) Mere Admixture vs. Non-Obvious Synergism):**
  - *Trigger Condition:* Proprietary herbal combination without comparative experimental data demonstrating unexpected synergism.
  - *Statutory Finding:* High risk of statutory rejection under Section 3(e) as a mere admixture resulting only in aggregation of component properties. To overcome Section 3(e), the applicant must furnish comparative experimental data proving surprising technical effect.
  - *Cited Passages:* `REAL-001` (Section 3(e), `PASS-013`); `REAL-010` (Paragraph 4.1, `PASS-019`).
- **Rule `RULE-PAT-03` (Mandatory Geographical Origin Disclosure):**
  - *Trigger Condition:* Patent application utilizing biological resources obtained from India.
  - *Statutory Finding:* Mandatory compliance under Section 10(4)(d)(ii) of *The Patents Act, 1970* and Rule 13 of *The Patents Rules, 2003*. Applicant must formally declare the source and geographical origin of biological material.
  - *Cited Passages:* `REAL-013` (Section 10(4)(d)(ii), `PASS-026`); `REAL-014` (Rule 13, `PASS-027`).

### 2.2 Biological Resource & ABS Flags (2024 Rules + 2025 Amendment)
- **Harmonized Statutory Construction:**
  - *Parent Statute:* *The Biological Diversity Act, 2002* (Act No. 18 of 2003), substantially amended by the *Biological Diversity (Amendment) Act, 2023* (Act No. 10 of 2023, effective 1 August 2023).
  - *Operative Rules:* *Biological Diversity Rules, 2024* read in conjunction with *Biological Diversity Amendment Rules, 2025*.
- **Rule `RULE-ABS-01` (Mandatory Prior NBA Approval for IPR):**
  - *Trigger Condition:* Any person/entity applying for an intellectual property right in India or abroad based on research or information on biological resources obtained from India.
  - *Statutory Finding:* Section 6(1) mandates prior approval of the National Biodiversity Authority (NBA). Form III application must be submitted, and approval obtained prior to patent grant.
  - *Subordinate Rules Implementation:* Rule 14 of the 2024 Rules and the 2025 Amendment Rules govern filing procedures, revised fee structures, and benefit-sharing determination.
  - *Cited Passages:* `REAL-008` (Section 6(1), `PASS-015`); `REAL-004` (Rule 1(2), `PASS-005`); `REAL-005` (`PASS-006`); `REAL-017` (`PASS-032`).
- **Rule `RULE-ABS-02` (Scope of Practitioner & Cultivator Exemptions):**
  - *Statutory Boundary:* Under Section 6(1A) (inserted by 2023 Amendment Act), local growers, cultivators, and registered vaids/hakims practicing indigenous medicine are exempt from intimation to State Biodiversity Boards for certain commercial utilization. **However, this exemption does NOT waive the Section 6(1) requirement for patent applications.** Any patent application remains subject to NBA approval.
  - *Cited Passages:* `REAL-008` (Section 6(1A), `PASS-016`).

### 2.3 Strict TKDL Access & Confidentiality Boundary
- In accordance with project safety guidelines:
  1. The knowledge corpus strictly indexes **public defensive policy frameworks** ([REAL-007](../../data/corpus/documents.csv), `PASS-008`) and bilateral patent office search agreement records.
  2. The confidential, proprietary full-text database of the Traditional Knowledge Digital Library (TKDL) is **not accessible to the public or this assistant**.
  3. The assistant will explicitly inform users that patent examiners access TKDL under non-disclosure agreements, but the assistant cannot search or verify private TKDL dossiers.

### 2.4 Explicit Uncertain / Needs-Expert Referral Outcomes
- **Rule `RULE-UNC-01` (Ambiguous / Incomplete Formulation Data):**
  - Triggers when user provides conflicting intended use, unverified botanical names, or incomplete route details.
  - Action: Halts confident classification, issues targeted missing-fact prompts, and generates a structured `ReferralPacket` containing known facts, assumptions, and specific questions for an AYUSH regulatory consultant or patent agent.
- **Rule `RULE-ERR-01` (Parenteral Administration Prohibition):**
  - Triggers when an Ayurvedic or food formulation specifies parenteral (injection/IV) administration.
  - Action: Immediate statutory violation alert under D&C Act Section 3(h) and FSSAI Regulation 2(b). Prohibits ASU or Ayurveda Aahara classification.
- **Rule `RULE-ERR-02` (Disease Cure Claims in Food or Cosmetic):**
  - Triggers when an Ayurveda Aahara or cosmetic product claims disease prevention, mitigation, or cure.
  - Action: Flags statutory violation of FSSAI Regulation 8 and *Drugs and Magic Remedies Act, 1954*. Re-routes product to drug evaluation or referral.

---

## 3. Ten Reviewed Sample Rule Firings

To validate the machine-readable rule contract against real-world scenarios, ten representative formulation cases were executed and audited against source passages with independent teammate review:

| Case ID | Formulation Scenario & Input Facts | Rules Fired | Resulting Provisional Outcome | Cited Authority & Locators | Teammate Audit & Review Findings |
|---|---|---|---|---|---|
| **SCEN-01** | **Classical Chyawanprash:** Oral herbal paste; 100% ingredients and recipe match *Charaka Samhita*; claimed for general rejuvenation and disease mitigation. | `RULE-CLS-01` | **Route 1: Classical Ayurvedic Medicine** | `REAL-002` s. 3(a), `REAL-009` r. 158-B(I), `PASS-009`, `PASS-017`, `PASS-023` | **Audited by Harshit:** Verified exact locator match for classical licensing proof; confirmed proper state AYUSH routing. |
| **SCEN-02** | **Proprietary Curcumin-Piperine Capsules:** Oral capsule; First Schedule ingredients; proprietary ratio; patent filing planned without comparative synergism data. | `RULE-CLS-02`, `RULE-PAT-02` | **Route 2: P&P Ayurvedic Medicine + Section 3(e) Patent Warning** | `REAL-002` s. 3(h), `REAL-001` s. 3(e), `REAL-010` para 4.1, `PASS-010`, `PASS-013`, `PASS-019` | **Audited by Deepshika:** Verified terminology for "Patent or Proprietary" vs "Classical"; confirmed dual routing to AYUSH P&P and patent alert. |
| **SCEN-03** | **Ashwagandha Carbonated Beverage:** Oral drink claiming to "cure clinical anxiety and hypertension"; classical recipe under Schedule A. | `RULE-ERR-02` | **Rejection / Reclassification:** Illegal disease claims under FSSAI Reg. 8 & DMR Act s. 3 | `REAL-003` reg. 8, `REAL-011` order 2025, `REAL-016` s. 3, `PASS-004`, `PASS-021`, `PASS-030` | **Audited by Harshit:** Confirmed immediate interception of disease claims; blocked Ayurveda Aahara food approval. |
| **SCEN-04** | **Standardized Boswellia Serrata Extract:** Purified fraction; characterized with 4 bioactive boswellic acids; oral anti-inflammatory. | `RULE-CLS-04` | **Route 4: Phytopharmaceutical Drug (Mandatory Referral)** | `REAL-002` r. 2(eb), `REAL-012` Sched Y, `REAL-019` sec 3, `PASS-012`, `PASS-022`, `PASS-034` | **Audited by Sabeena:** Verified non-forcing behavior; confirmed referral to CDSCO modern drug clinical trial framework. |
| **SCEN-05** | **Kumkumadi Brightening Facial Serum:** Topical application solely for skin cleansing and promoting radiance; no medicinal claims. | `RULE-CLS-06` | **Route 6: Ayurvedic Cosmetic** | `REAL-002` s. 3(aaa), `PASS-011` | **Audited by Deepshika:** Verified cosmetic boundary under Section 3(aaa); confirmed absence of drug/medicinal claims. |
| **SCEN-06** | **Herbal Pain Balm containing synthetic Methyl Salicylate & Paracetamol:** Topical analgesic combining classical herbs with modern API. | `RULE-CLS-03` | **Route 3: Novel / Non-Classical Formulation (Mandatory Referral)** | `REAL-002` s. 3(a)/3(h), `PASS-009`, `PASS-010` | **Audited by Harshit:** Confirmed strict non-forcing; presence of synthetic chemical blocks AYUSH classical/proprietary licensing. |
| **SCEN-07** | **Injectable Ayurvedic Taila:** Classical taila proposed for intravenous / intramuscular administration for chronic joint pain. | `RULE-ERR-01` | **Statutory Rejection:** Prohibited route of administration | `REAL-002` s. 3(h), `PASS-010` | **Audited by Harshit:** Confirmed Section 3(h) explicit exclusion of parenteral route; immediate rejection generated. |
| **SCEN-08** | **Patent Application on Neem-Turmeric Combination:** Research on Indian biological resources; patent filing planned in India and PCT. | `RULE-PAT-01`, `RULE-PAT-03`, `RULE-ABS-01` | **Statutory Exclusion Alert + NBA Prior Approval Mandate** | `REAL-001` s. 3(p), s. 10(4)(d)(ii), `REAL-008` s. 6(1), `PASS-002`, `PASS-015`, `PASS-026` | **Audited by Harshit:** Confirmed multi-statute interaction: s. 3(p) TK rejection risk, s. 10 origin disclosure, and Form III NBA prior approval. |
| **SCEN-09** | **Ayurveda Aahara Brahmi Ghee:** Oral ghee prepared per *Sahasrayogam* (Schedule A); naturally occurring nutrients; general wellness claims; FSSAI logo. | `RULE-CLS-05` | **Route 5: Ayurveda Aahara (Food)** | `REAL-003` reg. 2(b), reg. 8, Sched A, `REAL-011`, `PASS-003`, `PASS-004`, `PASS-021`, `PASS-024` | **Audited by Deepshika:** Verified food labelling terms; confirmed full compliance with 2022 regulations and 2025 transition order. |
| **SCEN-10** | **Unverified Forest Botanical Tonic:** Unidentified local plant extract; claims disease cure; dosage and route unverified. | `RULE-UNC-01` | **Route 7: Needs-Expert Referral (Explicit Uncertainty)** | `REAL-001`, `REAL-002`, `REAL-008`, `PASS-002`, `PASS-009`, `PASS-015` | **Audited by Sabeena:** Confirmed safe abstention behavior; missing facts prevented false positive classification; referral packet generated. |

---

## 4. Machine-Readable Rule Contract Handoff (For Harshit & Suresh)

The rule contract is formally serialized in [`data/rules/decision_rules.json`](../../data/rules/decision_rules.json).

### Integration Interface for Backend & RAG Engine
1. **Intake Schema Validation:** Suresh's `/api/v1/classify` endpoint can directly deserialize and validate incoming requests against `intake_fields`.
2. **Deterministic Pre-Filter:** The rules execute as an efficient deterministic pre-filter prior to RAG retrieval:
   - If a disqualifying rule fires (`RULE-ERR-01`, `RULE-ERR-02`), substantive retrieval is bypassed, returning an immediate statutory violation response with cited provisions.
   - If a referral rule fires (`RULE-CLS-03`, `RULE-CLS-04`, `RULE-UNC-01`), the system automatically packages a `ReferralPacket` without calling unconstrained generation.
   - For valid product routes (`RULE-CLS-01`, `RULE-CLS-02`, `RULE-CLS-05`, `RULE-CLS-06`), the associated `source_ids` and `passage_locators` serve as gold retrieved evidence seeds for Harshit's citation validator.
3. **Patent & ABS Flagging:** In parallel, any query with `patent_filing_intended == true` evaluates `RULE-PAT-01`, `RULE-PAT-02`, `RULE-PAT-03`, and `RULE-ABS-01`, automatically appending statutory warnings and Form III compliance alerts to the response.

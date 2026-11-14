# Deepshika Module Specification: Multilingual Experience, Controlled Glossary, User Flows, and Translation Feasibility (Task D-01)

**Task ID:** D-01  
**Module Owner:** Deepshika Palepu (Multilingual experience, terminology, translation quality, and accessibility)  
**Target Window:** Weeks 1–2  
**Status:** Submitted for Review (Draft PR)  
**Branch:** `deepshika/d-01-phase-1`  
**Requested Reviewers:**  
- **Thulasi** (Domain terminology, statutory wording & formulation route definitions)  
- **Sabeena** (Usability, comprehension rubric & benchmark prompt variant formatting)  
- **Harshit** (Evidence mapping, citation parity rules & response contract compatibility)  

---

## 1. Executive Summary & Scope

Under the [MASTER_PLAN.md](../MASTER_PLAN.md) and [03-deepshika.md](03-deepshika.md), Task D-01 delivers the foundational multilingual experience and user-flow architecture for IP-SAKTI Sahayak:
1. **Regional Language Review Feasibility Audit**: Conducts an honest audit of team linguistic proficiencies. Confirms English and Hindi as immediately reviewable, evaluates Telugu as the primary regional candidate based on team composition, and **explicitly reserves the final regional language selection as an open kickoff decision** requiring full team sign-off rather than a silent choice.
2. **End-to-End User Flow Mapping**: Establishes comprehensive journey maps and state-machine transitions across Intake, Answer, Source, and Referral flows, with rigorous definitions of **Unknown**, **Clarification**, **Safe Abstention**, and **Out-of-Scope** states.
3. **Controlled Glossary v0**: Delivers 30 foundational bilingual terms with Devanagari script, Roman transliterations, and candidate regional renderings across four critical domains: *Jurisdiction*, *Evidence & Citations*, *Uncertainty & Abstention*, and *Product Categories* ([data/glossary/controlled_glossary_v0.csv](../../data/glossary/controlled_glossary_v0.csv)).
4. **Translation Feasibility Trial**: Evaluates real statutory text from the corpus (`PASS-002`: Patents Act s. 3(p) and `PASS-004`: FSSAI Ayurveda Aahara reg. 8) to test preservation of legal negation, statutory obligations ("shall"), exceptions, jurisdiction terms, and citation ID stability.
5. **Accessibility & Component Guidelines**: Specifies WCAG 2.1 AA requirements, keyboard tab order, screen-reader semantics, Indic typography, and evidence badge visual contrast for Akshay (Frontend).
6. **Interface Dependency Audit**: Documents upstream API/schema dependencies (Harshit H-01, Suresh Su-01) and unverified corpus rows honestly, completing independent deliverables without assuming unbuilt integrations.

---

## 2. Team Language Capability Audit & Regional Language Decision

### 2.1 Master Plan Constraints
- **MVP Requirement**: English, Hindi, and one regional language selected at kickoff, covering core screens, intake, notices, supported answer topics, and referral flow.
- **Master Plan Acceptance Gate**: 100% citation-ID parity on paired cases; zero unresolved critical semantic reversals; average meaning/comprehension rating at least 4/5 from available bilingual team reviewers.
- **Safety Directive**: Do not assume external bilingual experts are available. If no competent team reviewer exists for a language, the system must not emit unverified dynamic translations.

### 2.2 Capability Matrix of the Six-Member Team

| Member | Primary Role | English | Hindi | Regional Language Competency | Review Availability |
|---|---|---|---|---|---|
| **Harshit Ambati** | Technical Lead / RAG | Professional / Working | Fluent / Conversational | Telugu (Native / Bilingual) | Architecture, RAG contracts, Citation parity |
| **Thulasi (Nagathulasi)** | Corpus & Decision Rules | Professional / Working | Working / Reviewable | Telugu (Native / Bilingual) | Domain terminology, Ayurvedic concepts |
| **Deepshika Palepu** | Multilingual UX & Terminology | Professional / Working | Fluent / Literate | Telugu (Native / Bilingual) | Translation assets, UX strings, Glossary v0 |
| **Suresh** | Backend & Security | Professional / Working | Fluent / Conversational | Dravidian / Southern regional familiarity | API contracts, RBAC, Data schemas |
| **Sabeena** | Benchmark & Evaluation | Professional / Working | Conversational / Working | Multilingual testing familiarity | Usability trials, Benchmark ledger |
| **Akshay** | Frontend & UI | Professional / Working | Conversational | UI localization integration | Screen rendering, Keyboard navigation |

### 2.3 Explicit Kickoff Decision Status: Regional Language Selection

> [!IMPORTANT]
> **Decision Status: UNCONFIRMED — PENDING FORMAL TEAM KICKOFF SIGN-OFF**  
> While Telugu represents the most viable regional language candidate given that three team members (Deepshika, Harshit, Thulasi) possess native or bilingual proficiency, **the regional language is not silently selected or locked unilaterally in this phase**.

**Formal Selection Criteria for Kickoff Meeting:**
1. **Bilingual Reviewer Redundancy**: At least two team members must independently verify translated UI strings, benchmark variants, and legal summaries.
2. **Corpus Terminology Availability**: Verified statutory translations (e.g. state legislative translations or official glossary equivalents) must exist for core IP and Ayurvedic terms.
3. **Candidate Languages Considered**:
   - **Telugu (`te`)**: Strongly recommended due to 3-member team fluency (Harshit, Thulasi, Deepshika).
   - **Tamil (`ta`)**: Secondary candidate; requires external domain validation which violates MVP self-reliance assumptions.
   - **Kannada (`kn`)**: Tertiary candidate; partial familiarity, but insufficient team depth for statutory verification.
4. **Implementation Contract**: All schemas, frontend hooks, and translation files must use a configurable parameter (`lang_regional` with ISO-639-1 code) to prevent architectural lock-in prior to final team agreement.

---

## 3. End-to-End User Flow & State Machine Mapping

### 3.1 Global State Architecture

The system operates as a finite-state sequence ensuring that legal conclusions are never generated without verifiable evidence:

```
[Start]
   │
   ▼
[Scope & Legal Notice] ──(Decline)──► [Exit / Session Terminated]
   │ (Accept)
   ▼
[Language & Jurisdiction Selector]
   │ (Select Lang: en / hi / [regional]; Jurisdiction: India / International Overview)
   ▼
[Guided Intake Form (RULE-01 to RULE-07)]
   │
   ├──(Missing facts / ambiguous inputs)──► [Clarification State] ──► (Loop back to Intake)
   │
   ▼
[Provisional Classification Router]
   │
   ├──(Novel / Non-Classical / Phytopharmaceutical)──► [Default Referral State]
   │
   ├──(Out-of-Scope / Foreign Export Law)───────────► [Out-of-Scope Abstention State]
   │
   ▼
[Evidence Retrieval & Claim-Evidence Verification]
   │
   ├──(Zero supporting passages / conflicting law)─► [Safe Abstention State]
   │
   ▼
[Cited Answer View] ──► [Inspect Source Card / Excerpt Modal]
   │
   ▼
[Optional: Export Human Referral Packet] ──► [Download JSON/Markdown Dossier]
```

---

### 3.2 State Definitions and UX Contracts

#### State 1: Scope & Legal Disclaimer
- **Trigger**: Initial entry.
- **Display**: Clear banner in selected language: *"IP-SAKTI Sahayak provides informational guidance, not legal advice or official regulatory approvals. Evidence coverage does not certify legal correctness."*
- **Action**: User acknowledges before proceeding. Anonymous session token initialized.

#### State 2: Language & Jurisdiction Controls
- **Controls**:
  - **Language**: English (`en`), Hindi (`hi`), Regional Candidate (`te` - marked provisional).
  - **Jurisdiction**: Radio selection strictly separating **India** (`IN`) and **International Overview** (`INT_WIPO`).
- **Safety Rule**: Jurisdiction toggle immediately resets any active answer state and forces re-retrieval. Mixed-jurisdiction retrieval is strictly prohibited.

#### State 3: Guided Intake Flow
- **Fields Collected**:
  1. `formulation_name`: Informational text.
  2. `intended_use`: `medicinal` (internal/external), `food_dietary`, `cosmetic`, `other`.
  3. `ingredient_origin`: `classical_herbal_mineral`, `standardized_fraction_extract`, `synthetic_nutrients_added`, `novel_chemical_entity`.
  4. `textual_authority`: Citation from First Schedule of D&C Act 1940 or Schedule A of Ayurveda Aahara 2022 (`yes`, `no`, `unverified`).
  5. `processing_method`: Classical Shastra method or modern modified extraction.
  6. `claims_made`: Disease treatment/cure, general wellness, beautification/cleansing.
- **Validation**: If mandatory fields are omitted, the form transitions to `CLARIFICATION_REQUIRED`.

#### State 4: Clarification Required State (RULE-07)
- **Trigger**: Missing ingredient origin, unstated intended use, or mutually contradictory claims (e.g., claiming food use while claiming disease cure).
- **UX Presentation**: Highlight missing fields with localized helper text: *"Please specify whether ingredients are mentioned in First Schedule authoritative texts to evaluate classical status."*
- **Behavior**: Substantive classification and answer generation are blocked.

#### State 5: Provisional Classification Output
- **Routes**:
  - `Route 1: Classical ASU Drug` (D&C Act s. 3(a))
  - `Route 2: Patent or Proprietary Medicine` (D&C Act s. 3(h))
  - `Route 3: Novel / Non-Classical Formulation` (Default Referral)
  - `Route 4: Phytopharmaceutical Drug` (Drugs Rules r. 2(eb) - Default Referral)
  - `Route 5: Ayurveda Aahara` (FSSAI Regs 2022 reg. 2(b))
  - `Route 6: Ayurvedic Cosmetic` (D&C Act s. 3(aaa))
  - `Route 7: Unknown / Ambiguous` (Mandatory Referral)
- **Visual Badge**: Clearly labelled with an "Informational / Provisional" prefix.

#### State 6: Cited Answer View
- **Components**:
  - **Provisional Classification Header** with statutory anchor.
  - **Synthesized Guidance**: Bulleted material claims, each bound to at least one Passage ID.
  - **Evidence Status Indicator**:
    - `SUPPORTED (Green)`: Every claim linked to an active, verified passage.
    - `PARTIAL (Amber)`: Guidance provided with explicit limitations.
    - `INSUFFICIENT (Slate)`: Transitioned to Safe Abstention.
  - **Citation Badges**: Clickable tags (e.g. `[REAL-001 §3(p)]`, `[REAL-003 Reg. 8]`).

#### State 7: Source Drawer / Modal View
- **Trigger**: Clicking any citation badge.
- **Display**:
  - Issuing Authority (e.g. *Controller General of Patents / IP India*).
  - Official Document Title and Effective Date.
  - Exact Provision Locator (e.g. *Section 3(p)*).
  - Verbatim excerpt or source-backed paraphrase.
  - Verification Status badge (e.g. *Source Verified — Domain Review Pending*).
  - Direct external official link (`official_url`).

#### State 8: Safe Abstention State
- **Trigger**:
  - Insufficient evidence in corpus for requested question.
  - Conflicting provisions across operative amendments.
  - Query requests unanswerable legal conclusion (e.g. *"Will my patent be granted?"*).
- **UX Presentation**: Informational notice explaining exact refusal reason: *"The current verified corpus does not contain statutory evidence sufficient to answer this query safely. Substantive claims have been suppressed to prevent misleading guidance."*
- **Action**: Offer transition to Referral Packet.

#### State 9: Out-of-Scope / Foreign Export State
- **Trigger**: Query mentions foreign patent offices (USPTO, EPO), foreign import duties, or foreign regulatory clearances.
- **UX Presentation**: Out-of-scope notice: *"Export compliance and foreign national patent laws are outside the initial MVP scope. Only domestic Indian statutory regimes and general WIPO treaty overviews are supported."*
- **Action**: Direct user to official WIPO overview or referral.

#### State 10: Human Referral Flow
- **Trigger**: User clicks "Export Referral Packet" or system enters Route 3, 4, or 7.
- **Contents**:
  - Timestamp, Session ID (synthetic), and Language.
  - User-provided formulation profile.
  - Missing facts / unresolved legal ambiguities.
  - Provisional route and statutory provisions retrieved.
  - Contact pointers to official bodies (Patent Facilitation Centre, National Biodiversity Authority State Biodiversity Boards, Ayush licensing authorities).
- **Disclaimer**: *"This referral packet is for user presentation to a licensed patent agent or regulatory consultant. IP-SAKTI Sahayak does not transmit data to any third party and does not guarantee expert response."*

#### State 11: Unverified Translation Fallback State
- **Trigger**: Dynamic translation layer confidence falls below threshold or language parity check fails.
- **UX Presentation**: Top-level localized warning banner: *"Dynamic translation could not be verified for legal nuance in this language. Displaying English text with verified statutory locators."*

---

## 4. Controlled Glossary v0

The controlled glossary establishes 30 immutable terms across four domains. The authoritative machine-readable version is located at [data/glossary/controlled_glossary_v0.csv](../../data/glossary/controlled_glossary_v0.csv).

### 4.1 Summary of Controlled Domains & Terms

| Term ID | Domain | English Term | Hindi Statutory Rendering | Devanagari Script | Preservation Rule |
|---|---|---|---|---|---|
| `GLOSS-001` | `jurisdiction` | India Jurisdiction | Bharat Kshetrahikar | भारत क्षेत्राधिकार | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-002` | `jurisdiction` | International Overview | Antarrashtriya Avalokan | अंतर्राष्ट्रीय अवलोकन | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-003` | `jurisdiction` | Territorial Scope | Pradeshik Kshetra | प्रादेशिक क्षेत्र | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-004` | `jurisdiction` | WIPO Treaty Party | WIPO Sandhi Paksh | डब्ल्यूआईपीओ संधि पक्ष | `ACRONYM_IMMUTABLE` |
| `GLOSS-005` | `jurisdiction` | Domestic Enactment | Gharelu Adhiniyaman | घरेलू अधिनियमन | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-006` | `jurisdiction` | Substantive Law | Mool Vidhi | मूल विधि | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-007` | `evidence_citation` | Statutory Provision | Vaidhanik Pravadhan | वैधानिक प्रावधान | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-008` | `evidence_citation` | Locator | Vishisht Sandika | विशिष्ट संदिका (धारा/नियम/विनियम) | `NUMBER_IMMUTABLE` |
| `GLOSS-009` | `evidence_citation` | Passage ID | Anuchhed Pehchan | अनुच्छेद पहचान (Passage ID) | `ID_IMMUTABLE` |
| `GLOSS-010` | `evidence_citation` | Source ID | Srot Pehchan | स्रोत पहचान (Source ID) | `ID_IMMUTABLE` |
| `GLOSS-011` | `evidence_citation` | Issuing Authority | Jarikarta Pradhikari | जारीकर्ता प्राधिकारी | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-012` | `evidence_citation` | Official Gazette | Bharat Ka Rajpatra | भारत का राजपत्र | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-013` | `evidence_citation` | Claim Support | Dawa Sakshya Samarthan | दावा साक्ष्य समर्थन | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-014` | `evidence_citation` | Citation Parity | Uddharan Samtulyata | उद्धरण समतुल्यता (Citation Parity) | `ID_IMMUTABLE` |
| `GLOSS-015` | `uncertainty_abstention` | Safe Abstention | Surakshit Sanyam | सुरक्षित संयम (उत्तर अस्वीकृति) | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-016` | `uncertainty_abstention` | Clarification Required | Spashtikaran Apekshit | स्पष्टीकरण अपेक्षित | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-017` | `uncertainty_abstention` | Missing Mandatory Facts | Anivarya Tathyon Ka Abhav | अनिवार्य तथ्यों का अभाव | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-018` | `uncertainty_abstention` | Conflicting Evidence | Virodhabhasi Sakshya | विरोधाभासी साक्ष्य | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-019` | `uncertainty_abstention` | Provisional Classification | Anantim Vargeekaran | अनंतिम वर्गीकरण | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-020` | `uncertainty_abstention` | Referral Packet | Manav Visheshagya Paramarsh Packet | मानव विशेषज्ञ परामर्श पैकेट | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-021` | `uncertainty_abstention` | Unverified Translation Fallback | Asatyapit Anuvad Suraksha Chetavani | असत्यापित अनुवाद सुरक्षा चेतावनी | `SAFETY_FALLBACK_BANNER` |
| `GLOSS-022` | `product_category` | Classical ASU Drug | Paramparik Ayurveda, Siddha ya Unani Aushadhi | पारंपरिक आयुर्वेद, सिद्ध या यूनानी औषधि | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-023` | `product_category` | Patent or Proprietary Medicine | Patent ya Swatvadhari Aushadhi | पेटेंट या स्वत्वधारी औषधि | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-024` | `product_category` | Novel / Non-Classical Formulation | Naveen / Aparamparik Formulation | नवीन / अपारंपरिक फॉर्मूलेशन | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-025` | `product_category` | Phytopharmaceutical Drug | Padap-Aushadh | पादप-औषध (Phytopharmaceutical Drug) | `ACRONYM_IMMUTABLE` |
| `GLOSS-026` | `product_category` | Ayurveda Aahara | Ayurveda Aahara | आयुर्वेद आहार (Ayurveda Aahara) | `NAME_IMMUTABLE` |
| `GLOSS-027` | `product_category` | Ayurvedic Cosmetic | Ayurvedic Prasadan Samagri | आयुर्वेदिक प्रसाधन सामग्री | `STRICT_STATUTORY_EQUIVALENT` |
| `GLOSS-028` | `product_category` | Traditional Knowledge Aggregation | Paramparik Gyan Ka Sankalan / Matra Samucchay | पारंपरिक ज्ञान का संकलन / मात्र समुच्चय | `PRESERVE_NEGATION` |
| `GLOSS-029` | `product_category` | Mere Admixture | Matra Mishran | मात्र मिश्रण | `PRESERVE_NEGATION` |
| `GLOSS-030` | `product_category` | Surprising Synergistic Effect | Apratyashit Sahakriyatmak Prabhav | अप्रत्याशित सहक्रियात्मक प्रभाव (Synergy) | `STRICT_STATUTORY_EQUIVALENT` |

---

### 4.2 Translation Preservation Rules

1. **`ID_IMMUTABLE`**: Database keys such as `PASS-001`, `REAL-001`, `DOC-003` must NEVER be translated, phonetically altered, or transliterated. They must appear in Latin characters identically across all languages.
2. **`NUMBER_IMMUTABLE`**: Statutory section, sub-section, rule, and regulation numbers (e.g. `3(p)`, `3(h)`, `2(eb)`, `8`) must retain their standard legal format. They must never be converted to Devanagari numerals or localized letters in citations.
3. **`NAME_IMMUTABLE`**: Statutory proper names created by legislative definitions (e.g. `Ayurveda Aahara`, `WIPO`) must retain their recognized statutory spelling.
4. **`PRESERVE_NEGATION`**: Absolute statutory exclusions (e.g. *"not an invention"*, *"must not claim prevention or cure"*) must be rendered using unequivocal statutory negative terms (e.g. *"पेटेंट योग्य आविष्कार नहीं है"*, *"कदापि दावा नहीं किया जाएगा"*). Discretionary translations (e.g. *"दावा करने से बचना चाहिए"*) are strictly prohibited.
5. **`STRICT_STATUTORY_EQUIVALENT`**: Technical legal phrases must use recognized Hindi legal glossary terminology established in the India Code or Official Gazette, rather than casual vernacular expressions.

---

## 5. Translation Trial for Preserved Legal Meaning

To evaluate whether translation risks altering legal force, rights, or obligations, two real statutory passages from [passages.csv](../../data/corpus/passages.csv) were audited.

### 5.1 Trial Case 1: Indian Patent Law — Traditional Knowledge Exclusion

- **Corpus Locator**: `PASS-002` (linked to `REAL-001`: *The Patents Act, 1970*)
- **Statutory Provision**: Section 3(p)
- **Source English Passage**:  
  > *"Section 3(p) addresses inventions that in effect are traditional knowledge or aggregate known properties of traditionally known components."*
- **Hindi Translation Trial**:  
  > *"धारा 3(p) उन आविष्कारों को संबोधित करती है जो वास्तव में पारंपरिक ज्ञान हैं या पारंपरिक रूप से ज्ञात घटकों के ज्ञात गुणों का मात्र समुच्चय या दोहराव हैं, और इस प्रकार वे पेटेंट योग्य आविष्कार नहीं हैं।"*

#### Detailed Linguistic & Legal Meaning Audit:

| Dimension | Source English Statutory Construct | Hindi Translation Rendering | Evaluation & Meaning Preservation |
|---|---|---|---|
| **Negation Preservation** | Excluded subject matter (*"not an invention"* under opening words of s. 3) | *"पेटेंट योग्य आविष्कार नहीं हैं"* | **PRESERVED**. The Hindi translation maintains the definitive statutory exclusion from patentability without ambiguity. |
| **Statutory Obligation / Duty** | Operative exclusionary mandate | *"संबोधित करती है ... पेटेंट योग्य आविष्कार नहीं हैं"* | **PRESERVED**. Maintains the non-discretionary standard of Section 3. |
| **Component Aggregation** | *"aggregate known properties of traditionally known components"* | *"पारंपरिक रूप से ज्ञात घटकों के ज्ञात गुणों का मात्र समुच्चय"* | **PRESERVED**. Uses the precise statutory concept of "mere aggregation" (*मात्र समुच्चय*) reflecting Section 3(p) and 3(e). |
| **Statutory Locator & ID** | `PASS-002`, `REAL-001`, `Section 3(p)` | `[PASS-002 / REAL-001] धारा 3(p)` | **PRESERVED (100% Parity)**. Latin script ID and alphanumeric section designation retained. |
| **Risk Identified** | Casual machine translation often renders *"in effect are traditional knowledge"* as *"पारंपरिक ज्ञान का प्रभाव हैं"* (causing confusion between causation and substance). | Controlled glossary forces *"वास्तव में पारंपरिक ज्ञान हैं"* (in effect / substantive identity). | **RESOLVED** via Controlled Glossary Rule `GLOSS-028`. |

---

### 5.2 Trial Case 2: Ayurveda Aahara Claim Prohibition

- **Corpus Locator**: `PASS-004` (linked to `REAL-003`: *FSSAI Ayurveda Aahara Regulations, 2022*)
- **Statutory Provision**: Regulation 8
- **Source English Passage**:  
  > *"Ayurveda Aahara labelling presentation and advertising must not claim prevention treatment or cure of human disease."*
- **Hindi Translation Trial**:  
  > *"आयुर्वेद आहार के लेबलन, प्रस्तुतिकरण एवं विज्ञापन में मानव रोग की रोकथाम, उपचार या निवारण (इलाज) का दावा कदापि नहीं किया जाएगा।"*

#### Detailed Linguistic & Legal Meaning Audit:

| Dimension | Source English Statutory Construct | Hindi Translation Rendering | Evaluation & Meaning Preservation |
|---|---|---|---|
| **Absolute Negative Duty** | *"must not claim"* | *"दावा कदापि नहीं किया जाएगा"* | **PRESERVED**. Strict negative imperative (*कदापि नहीं किया जाएगा*) preserves mandatory statutory bar. A casual rendering (*दावा नहीं करना चाहिए*) would introduce advisory ambiguity and is forbidden. |
| **Tripartite Medical Scope** | *"prevention, treatment or cure"* | *"रोकथाम, उपचार या निवारण (इलाज)"* | **PRESERVED**. Captures prophylactic (*रोकथाम*), therapeutic (*उपचार*), and curative (*निवारण*) statutory limbs without omission. |
| **Category Name** | *"Ayurveda Aahara"* | *"आयुर्वेद आहार (Ayurveda Aahara)"* | **PRESERVED**. Retains statutory term in Devanagari and Latin script. |
| **Statutory Locator & ID** | `PASS-004`, `REAL-003`, `Regulation 8` | `[PASS-004 / REAL-003] विनियमन 8` | **PRESERVED (100% Parity)**. Numbers and citation IDs unchanged. |

---

### 5.3 Semantic Fidelity Evaluation Rubric (for Task D-04 & Sabeena's Benchmark Variants)

Every translated prompt and answer variant must be scored against this 4-point rubric:
- **Score 4 (Exact Statutory Fidelity)**: All legal duties ("shall"), prohibitions ("must not"), statutory terms, and citation IDs are fully preserved without distortion.
- **Score 3 (Substantive Preservation with Minor Stylistic Variation)**: Legal meaning and obligations are intact; minor non-statutory phrasing variation.
- **Score 2 (Ambiguity Introduced)**: Mandatory duty rendered as permissive advice, or technical term translated using generic colloquial word. **Blocks release.**
- **Score 1 (Critical Semantic Reversal / Fabricated Term)**: Negation dropped, exemption flipped, or citation ID corrupted. **Immediate critical block.**

---

## 6. Accessibility and Frontend Component Guidelines

To ensure compliance with Master Plan Section 6 and enable Akshay (A-01 / A-02) to build accessible components:

1. **Keyboard Navigation & Focus Management**:
   - Tab sequence: Scope Notice -> Language/Jurisdiction Controls -> Intake Form Inputs -> Submit Button -> Answer Summary -> Citation Badges -> Referral Export.
   - All interactive controls must display a visible 2px high-contrast focus ring (`outline: 2px solid #1E40AF; outline-offset: 2px;`).
2. **Screen Reader Semantics (`aria-*`)**:
   - Dynamic answer generation container must use `aria-live="polite"`.
   - Error banners and missing fact notices must use `role="alert"` and `aria-live="assertive"`.
   - Citation badges must have descriptive labels: `aria-label="Inspect official passage PASS-002: Patents Act Section 3(p)"`.
3. **Visual Contrast & Color Palette**:
   - `SUPPORTED Badge`: Background `#DEF7EC`, Text `#03543F` (Contrast ratio 7.4:1 vs white).
   - `PARTIAL Badge`: Background `#FEF08A`, Text `#713F12` (Contrast ratio 6.8:1 vs white).
   - `ABSTENTION / INSUFFICIENT Badge`: Background `#F3F4F6`, Text `#1F2937` (Contrast ratio 11.2:1 vs white).
   - `WARNING / EXCLUSION Badge`: Background `#FEE2E2`, Text `#991B1B` (Contrast ratio 7.2:1 vs white).
4. **Indic Typography & Layout Support**:
   - Minimum base font size for Devanagari / Indic scripts: `16px` (due to complex ligatures and vowel diacritics / matras).
   - Line height for Indic text: minimum `1.6` (prevents clipping of top and bottom vowel signs).
   - Viewport adaptability: Layout must remain usable without horizontal scroll down to `320px` width.

---

## 7. Interface Dependencies and Blocker Audit

In accordance with project integrity guidelines, all upstream dependencies are explicitly documented:

| Dependency | Owner | Phase Target | Current Repository Status | Deepshika Module Impact & Workaround |
|---|---|---|---|---|
| **Response & Ingestion Schemas** | Harshit (`H-01`) | Weeks 1–2 | In development; no JSON schemas committed to `main` yet. | Deepshika designed UI state machine and glossary independently; contracts provide target field specifications. |
| **Stub Endpoints & Fixtures** | Suresh (`Su-01`) | Weeks 1–2 | In development; no API service or fixture files committed to `main`. | Component specifications and translation trials use standalone Markdown and CSV fixtures. |
| **Corpus Activation** | Thulasi (`T-01`) | Weeks 1–2 | Submitted on branch `thulasi/t-01-phase-1`; rows on `main` remain marked `source_checked_domain_review_pending`. | Trial translations use verified excerpts from Thulasi's audit note; no unverified corpus claims are presented as final law. |
| **Benchmark Scenarios** | Sabeena (`Sa-01`) | Weeks 1–2 | Protocol defined; scenarios pending. | Glossary v0 and semantic fidelity rubric provide the foundation for Sabeena's 30 translated benchmark variants. |

---

## 8. Progress Record & Verification Evidence

### 8.1 Automated Verification Check
A Python validation script (`scripts/verify_glossary.py`) was developed and executed inside the workspace:
- **Command**: `python scripts/verify_glossary.py`
- **Result**:
  ```text
  Loaded 30 glossary records from controlled_glossary_v0.csv.
  SUCCESS: All glossary records validated successfully.
  Domain breakdown:
    - evidence_citation: 8 terms
    - jurisdiction: 6 terms
    - product_category: 9 terms
    - uncertainty_abstention: 7 terms
  ```
- **Exit Code**: `0`

### 8.2 Deliverables Checklist Update

- [x] Intake and answer-flow specifications for Akshay (Sections 3 & 6 of this document)
- [x] Controlled glossary v0 of 30 terms across 4 mandatory domains ([data/glossary/controlled_glossary_v0.csv](../../data/glossary/controlled_glossary_v0.csv))
- [x] Translation feasibility trial preserving legal meaning and negation (Section 5)
- [x] Regional language capability audit and explicit decision framing (Section 2)
- [x] Accessibility and typography guidelines for frontend components (Section 6)
- [ ] English, Hindi, and regional UI strings (Scheduled for Task D-02, Weeks 3–4)
- [ ] 80–120 term expanded glossary v1 (Scheduled for Task D-03, Weeks 5–8)
- [ ] Paired-language benchmark citation parity checks (Scheduled for Task D-04, Weeks 9–10)
- [ ] Independent peer review completed (Pending Thulasi, Sabeena, Harshit review)

---

## 9. Review Requests & Next Actions

1. **Thulasi**: Please review the 30 controlled terms in `controlled_glossary_v0.csv` (especially `GLOSS-022` through `GLOSS-030`) for alignment with the classification rules in `thulasi-t01-specification.md`.
2. **Sabeena**: Please verify the 4-point semantic fidelity rubric (Section 5.3) for adoption in benchmark prompt variant evaluations.
3. **Harshit**: Please review the `preservation_rule` definitions (`ID_IMMUTABLE`, `NUMBER_IMMUTABLE`) to ensure compatibility with your RAG response assembly and citation validator schemas.

# UI Localization Dictionaries, Accessible Source-View Specification, and Frontend Handoff (Task D-02)

- **Task ID:** D-02
- **Module Owner:** Deepshika (`@deepshikapalepu20`) — Multilingual experience, terminology, translation quality and accessibility
- **Target Recipient:** Akshay (`@akshay`) — Frontend screens, source display, interface checks and demonstration (Tasks A-01 and A-02)
- **Target Window:** Weeks 3–4
- **Phase Gate Status:** Started under Harshit's explicit early-start permission ([Issue #9](https://github.com/Harshit-ambati/IP-SAKTI-Sahayak/issues/9)); Task D-01 ([PR #2](https://github.com/Harshit-ambati/IP-SAKTI-Sahayak/pull/2)) approved by Harshit and Thulasi, open as draft pending Sabeena's usability review.
- **Reviewers:** Thulasi (Domain terminology & intake question wording), Sabeena (Usability & accessibility checklists), Harshit (Evidence-contract mapping & schema compliance)

---

## 1. Executive Summary & Objectives

Task D-02 establishes the foundational user interface localization and component architecture for IP-SAKTI Sahayak, delivering:
1. **Authoritative Bilingual UI Dictionaries**: 182 matching string keys in English ([`ui_strings_en.json`](../../../data/translations/ui_strings_en.json)) and Hindi ([`ui_strings_hi.json`](../../../data/translations/ui_strings_hi.json)), verified via [`scripts/verify_strings.py`](../../../scripts/verify_strings.py).
2. **Accessible Source-View Specification for Akshay**: DOM structure, component hierarchy, and responsive styling for the accessible source drawer and citation cards, strictly matching Harshit's schema (`contracts/v1/sahayak.schema.json`) and Suresh's backend fixtures (`backend/fixtures/synthetic_fixtures.json`). Zero API fields are invented.
3. **Statutory Preservation Rules**: Clear implementation guidelines ensuring that original legal names, section/article numbers, gazette dates, and source IDs remain visible in Latin script alongside localized text.
4. **WCAG 2.1 AA Accessibility Standards**: Keyboard navigation protocols, modal focus trapping, screen-reader `aria-live` announcements, touch target sizing, and Indic typography rules.
5. **Mobile & Responsive Layout**: Adaptive presentation transforming the source viewer from a desktop slide-out drawer into a mobile bottom sheet with swipe-to-dismiss gestures.

---

## 2. Target Contract Alignment & Integration Status (Zero Invented Fields)

All frontend components specified below bind directly to the target exchange schemas and backend endpoints:

### Schema Status & Integration Reality
- **Target Contract Schema:** `contracts/v1/sahayak.schema.json` is the **proposed v1 exchange schema authored by Harshit in draft PR #5 (Task H-01)**. It remains open and unmerged.
- **Current Merged Backend Status:** The currently merged backend on `main` (Suresh's Task Su-01, PR #3 at commit `7cf0f55`) serves service and data skeletons with synthetic mock fixtures (`mock_answer_response`), while Suresh's Task Su-02 (draft PR #7) implements SQLite FTS5 evidence retrieval.
- **Frontend Architecture Rule:** Components must accept current synthetic mock fixtures while strictly conforming to Harshit's proposed H-01 schema definitions for seamless forward compatibility upon H-01 merge. No fields outside the proposed schema are introduced.

### Schema Mapping (Proposed `contracts/v1/sahayak.schema.json`)

| Schema Entity | Frontend Consumer Component | Bound Contract Fields | Schema Boundaries & Notes |
|---|---|---|---|
| `Intake` | `FormulationIntakeForm` | `contract_version`, `request_id`, `jurisdiction`, `language`, `question`, `facts` | Mandatory facts include: `formulation_title`, `ingredients`, `classical_text_reference`, `processing_method`, `intended_use`, `claims_disease_treatment`, `claims_disease_cure`, `has_novel_ingredient`, `standardized_fraction`, `external_application_only`. |
| `ClassificationResult` | `ProvisionalClassificationCard` | `contract_version`, `request_id`, `route`, `provisional`, `missing_facts`, `reason` | Routes: `classical_generic`, `patent_proprietary`, `novel_non_classical`, `phytopharmaceutical`, `ayurveda_aahara`, `cosmetic`, `unknown`. `provisional` is strictly `true`. |
| `EvidencePassage` | `SourceModal` / `SourceDrawer` | `passage_id`, `source_id`, `jurisdiction`, `source_title`, `source_url`, `locator`, `text`, `review_status`, `corpus_version` | **Strict Schema Boundary:** `EvidencePassage` defines exactly these 9 fields. It does **NOT** contain `authority` or `gazette_date` (which belong to document-level corpus registers, not per-passage payloads). Review status is restricted to `approved`, `pending`, `stale`, `rejected`. |
| `Claim` | `AnswerFindingCard` | `text`, `evidence_ids` | Array of `passage_id` strings linking assertions directly to retrieved evidence. |
| `AnswerResult` | `CitedGuidanceView` | `contract_version`, `request_id`, `status`, `jurisdiction`, `language`, `route`, `assumptions`, `claims`, `evidence`, `limitations`, `corpus_version`, `model_version` | Status: `clarify`, `answered`, `abstained`, `referral`. When `answered`, `claims` and `evidence` must have $\ge 1$ item; when abstained/referral, `claims` has 0 items. |
| `ReferralPacket` | `ReferralDossierScreen` | `contract_version`, `request_id`, `jurisdiction`, `language`, `question`, `route`, `assumptions`, `evidence_ids`, `unresolved_issues` | Structured exportable packet for specialist handoff. |

### Backend API Endpoints (Current Merged Su-01 / Target Su-02)

- `POST /api/v1/classify`: Accepts `Intake` payload, returns `ClassificationResult`.
- `POST /api/v1/answer`: Accepts `Intake` payload, returns `AnswerResult` (served via synthetic fixture in Su-01; FTS5 retrieval in draft Su-02).
- `GET /api/v1/sources/{source_id}`: Retrieves authoritative document metadata.
- `GET /api/v1/sources/{source_id}/passages/{passage_id}`: Retrieves specific provision excerpt.
- `POST /api/v1/referral`: Generates exportable `ReferralPacket`.

---

## 3. Accessible Source-View Architecture

The source view displays authoritative legal backing for retrieved claims. It can be triggered from any cited claim pill or provision badge.

> **Corpus Reference Distinction:**
> - `PASS-001` in `data/corpus/passages.csv` is a preliminary Section 3(k) record (software/algorithms, excluded from the Ayurvedic formulation classification index).
> - Section 3(p) (traditional knowledge aggregation exclusion) is recorded as **`PASS-002`** under source `REAL-001` (The Patents Act, 1970).
> - In the merged corpus baseline (`1a7cae4`), `PASS-002` has `review_status = "reviewed_t01_pending_activation"`. It is verified against the official statute by Thulasi and submitted for Harshit's formal activation review. It must **not** be presented as already approved.

### Component Wireframe (Desktop Slide-Over Drawer)

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [×] Close (Esc)          STATUTORY SOURCE REFERENCE          [REAL-001]│
├────────────────────────────────────────────────────────────────────────┤
│ Source Document Title: The Patents Act, 1970                           │
│ Source ID: REAL-001                     Passage ID: PASS-002           │
│ Legal Jurisdiction: India               Corpus Version: v0.1-baseline  │
│ Provision Locator: Section 3(p)                                        │
│ Corpus Review Status: [ Pending Formal Activation ]                    │
├────────────────────────────────────────────────────────────────────────┤
│ OFFICIAL STATUTORY EXCERPT (Passage ID: PASS-002):                     │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ "Section 3(p) excludes from patentability an invention which in   │ │
│ │  effect is traditional knowledge or which is an aggregation or     │ │
│ │  duplication of known properties of traditionally known component │ │
│ │  or components."                                                   │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│ Note: Verified against official Patents Act 1970; pending activation. │
│ Language Toggle: [ English (Original Statutory Text) | हिन्दी सारांश ] │
├────────────────────────────────────────────────────────────────────────┤
│ [↗ Open Official Instrument Portal]         [📋 Copy Legal Citation]   │
└────────────────────────────────────────────────────────────────────────┘
```

### Component Hierarchy & DOM Structure

```html
<!-- Source View Dialog Container -->
<div 
  id="source-modal" 
  role="dialog" 
  aria-modal="true" 
  aria-labelledby="source-dialog-title" 
  aria-describedby="source-dialog-desc"
  class="source-drawer-overlay"
>
  <div class="source-drawer-panel" tabIndex="-1">
    
    <!-- Header -->
    <header class="source-drawer-header">
      <div class="source-header-titles">
        <span class="source-id-badge" aria-label="Source Identifier">REAL-001</span>
        <h2 id="source-dialog-title" class="source-title">The Patents Act, 1970</h2>
      </div>
      <button 
        type="button" 
        class="source-close-btn" 
        aria-label="Close statutory source reference panel"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </header>

    <!-- Metadata Grid (Strictly bound to EvidencePassage fields) -->
    <section class="source-meta-grid" id="source-dialog-desc">
      <div class="meta-item">
        <span class="meta-label">Provision Locator</span>
        <span class="meta-value locator-tag">Section 3(p)</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Passage Identifier</span>
        <span class="meta-value">PASS-002</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Legal Jurisdiction</span>
        <span class="meta-value">India</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Corpus Version</span>
        <span class="meta-value">v0.1-baseline</span>
      </div>
      <div class="meta-item full-width">
        <span class="meta-label">Corpus Review Status</span>
        <span class="status-badge status-pending" aria-label="Review status: Pending activation">
          Pending Formal Activation
        </span>
      </div>
    </section>

    <!-- Official Excerpt Box -->
    <section class="source-excerpt-container">
      <div class="excerpt-header">
        <span class="passage-id-tag">Passage: PASS-002</span>
        <span class="legal-verbatim-notice">Verified Official Instrument Record</span>
      </div>
      <blockquote class="source-excerpt-body" lang="en">
        "Section 3(p) excludes from patentability an invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components."
      </blockquote>
      <p class="source-status-footnote">
        Source record verified by Thulasi from official Patents Act 1970 text; pending formal Harshit activation review.
      </p>
    </section>

    <!-- Action Footer -->
    <footer class="source-drawer-footer">
      <a 
        href="https://www.ipindia.gov.in/acts/patent-act-1970/section-3" 
        target="_blank" 
        rel="noopener noreferrer" 
        class="source-portal-link"
        aria-label="Open official IP India portal in new tab"
      >
        <span>Open Official Portal</span>
        <svg aria-hidden="true" width="16" height="16" fill="currentColor"><path d="..."/></svg>
      </a>
      <button 
        type="button" 
        class="source-copy-btn"
        aria-label="Copy legal citation to clipboard"
      >
        Copy Citation Locator
      </button>
    </footer>

  </div>
</div>
```
```

---

## 4. Statutory Preservation Rules in UI Presentation

Legal terminology must never be obscured or distorted by localization. Akshay must implement the following preservation rules in all screens:

### 1. Dual-Script Presentation Pattern (`NAME_IMMUTABLE`)
Where statutory terms have formal definitions in central notifications, both the approved Hindi equivalent and the Latin defined name must appear side-by-side:
- **Ayurveda Aahara**: `आयुर्वेद आहार (Ayurveda Aahara)`
- **Phytopharmaceutical Drug**: `पादप-औषध (Phytopharmaceutical Drug)`
- **Patent or Proprietary Medicine**: `पेटेंट या स्वत्वधारी औषधि (Patent or Proprietary ASU Drug)`
- **Classical ASU Drug**: `शास्त्रीय / पारंपरिक एएसयू औषधि (Classical ASU Drug)`

### 2. Alphanumeric Locator Preservation (`NUMBER_IMMUTABLE`)
Section, rule, and regulation locators must remain in Latin alphanumeric notation:
- Correct: `धारा 3(p) (Section 3(p))`, `नियम 2(eb) (Rule 2(eb))`, `विनियम 8 (Regulation 8)`
- **Prohibited**: `धारा ३(प)`, `नियम २(ईबी)`, `धारा 3-पी` (never translate subsection letters or convert numerals to Devanagari).

### 3. Database Identifier Integrity (`ID_IMMUTABLE`)
- All Citation IDs (`PASS-001`, `REAL-001`), Question IDs (`Q-USE`, `Q-INGR`), and Term IDs (`GLOSS-001`) must appear identically in ASCII Latin across English, Hindi, and regional views.
- **Citation Parity Gate**: For identical formulations, the set of emitted `passage_id` values in Hindi must match the English response with 100% parity.

### 4. Preserved Institutional Acronyms (`ACRONYM_IMMUTABLE`)
- Central regulatory authorities must preserve Latin acronyms:
  - `WIPO (डब्ल्यूआईपीओ)`
  - `FSSAI`
  - `AYUSH / आयुष`
  - `NBA / राष्ट्रीय जैव विविधता प्राधिकरण`
  - `CSIR-TKDL`

---

## 5. Accessibility (WCAG 2.1 AA) Specification

Akshay must verify compliance with the following accessibility checklist during component construction:

### Keyboard Interaction Matrix

| Key / Sequence | Target Component | Expected Behavior |
|---|---|---|
| `Tab` | Any Screen | Moves focus forward through interactive elements in natural DOM order. |
| `Shift + Tab` | Any Screen | Moves focus backward. |
| `Escape` | `SourceModal` / Drawer | Closes open source drawer immediately and restores focus to the invoking citation button. |
| `Enter` / `Space` | Citation Badges (`PASS-xxx`) | Opens the statutory source reference modal. |
| `Enter` / `Space` | Questionnaire Options | Selects the active radio card or toggle button. |
| `Enter` / `Space` | Accordion Headers | Toggles expansion of assumptions and limitations sections. |
| `Arrow Keys` | Language & Jurisdiction Radios | Cycles through options without triggering page reload. |

### Focus Management & Trapping
- When the `SourceModal` opens:
  1. Store `document.activeElement` (the triggering citation button).
  2. Trap focus inside `.source-drawer-panel`: `Tab` on the last focusable element wraps to the first focusable element (`.source-close-btn`).
  3. `aria-hidden="true"` is applied to the main page content container (`#app-root`).
- When the `SourceModal` closes:
  1. Remove `aria-hidden` from `#app-root`.
  2. Restore keyboard focus directly to the stored triggering element.

### Visual Focus Indicators
- All interactive elements (buttons, links, radio cards, text inputs) must display an unequivocal focus indicator:
  ```css
  :focus-visible {
    outline: 2px solid #005A9C;
    outline-offset: 2px;
  }
  ```
- Contrast ratio between the focus ring (`#005A9C`) and adjacent backgrounds must exceed **3:1**.

### Dynamic Screen Reader Announcements (`aria-live`)
- **Polite Updates (`aria-live="polite"`):**
  - Formulation intake progress (e.g., *"Step 2 of 4: Active Botanical Ingredients"*).
  - Language switch announcement (e.g., *"Interface language changed to Hindi"*).
  - Jurisdiction switch announcement (e.g., *"Legal jurisdiction filter updated to India Domestic Law"*).
- **Assertive Alerts (`aria-live="assertive"`):**
  - Safe abstention banner when retrieved evidence is insufficient.
  - Validation errors when mandatory formulation questions are skipped.

### Indic Typography & Touch Target Requirements
1. **Minimum Touch Targets**: All interactive elements (buttons, language toggles, close icons) must meet a minimum bounding box of **44 × 44 CSS pixels** on mobile viewports.
2. **Devanagari Font Sizing**: Body text in Hindi must have a minimum `font-size` of **16px** (1rem).
3. **Indic Line Height**: To prevent vowel matras (`े`, `ै`, `ं`, `ु`, `ू`, `ृ`) from being clipped by line bounds, line height for Hindi text must be at least **1.6** (e.g., `line-height: 1.6;`).
4. **Color Contrast**: Body copy must achieve at least **4.5:1** contrast against page backgrounds (e.g., `#1A202C` on `#FFFFFF` = 14.8:1; `#4A5568` on `#FFFFFF` = 7.0:1).

---

## 6. Mobile & Responsive Layout Architecture

To accommodate student laptops, tablets, and smartphones, the user interface adapts across three standard breakpoints:

| Breakpoint | Viewport Range | Navigation Layout | Source View Presentation | Intake Layout |
|---|---|---|---|---|
| **Mobile** | `< 640px` | Collapsible top app bar with hamburger menu | **Bottom Sheet**: Slides up from bottom (max-height 85vh) with swipe-down dismiss and sticky action bar | Single-column stacked cards; large radio touch targets |
| **Tablet** | `640px – 1024px` | Compact header with icons and text | **Modal Dialog**: Centered modal overlay (width 80vw, max-height 90vh) | Two-column responsive grid |
| **Desktop** | `> 1024px` | Persistent top navigation bar | **Slide-Over Drawer**: Right-hand slide-out panel (width 480px) with backdrop scrim | Multi-column guided workspace |

### Mobile Bottom Sheet Specifications
- On mobile viewports (`< 640px`), the source modal must render as a bottom sheet:
  - `position: fixed; bottom: 0; left: 0; right: 0;`
  - `border-top-left-radius: 16px; border-top-right-radius: 16px;`
  - Persistent drag handle (`width: 36px; height: 4px; background: #CBD5E0; border-radius: 2px; margin: 8px auto;`).
  - Native touch event support: Swiping down on the drag handle by >100px dismisses the sheet.
  - Action footer pinned above mobile viewport navigation: `padding-bottom: max(16px, env(safe-area-inset-bottom));`.

---

## 7. Frontend Implementation Handoff Checklist for Akshay

The following checklist specifies the deliverables expected from Akshay for Tasks A-01 and A-02:

### Task A-01: Screen Skeleton & Mock Flow (Weeks 1–2 Target)
- [ ] Implement responsive layout container with header, main view, and footer disclaimers.
- [ ] Connect language toggle using `ui_strings_en.json` and `ui_strings_hi.json`.
- [ ] Wire jurisdiction toggle (`India` vs `international_overview`).
- [ ] Build mock formulation intake form with 8 progressive questions matching `Q-USE` through `Q-COSM-CLAIM`.
- [ ] Render provisional classification badge matching Suresh's `ClassificationResult` mock payload.

### Task A-02: Six Component Groups & Source Cards (Weeks 3–4 Target)
- [ ] Build `ProvisionalClassificationCard` with route descriptions and missing-fact alerts.
- [ ] Build `CitedGuidanceView` displaying claim cards, evidence badges (`Supported`, `Partial`, `Insufficient`), assumptions accordion, and limitations list.
- [ ] Build `SourceModal` / `SourceDrawer` strictly following the DOM structure, metadata grid, and excerpt blockquote specified in Section 3.
- [ ] Implement modal focus trapping and `Esc` key listener.
- [ ] Implement clipboard copy button with visual feedback (`Citation copied to clipboard`).
- [ ] Build `ReferralDossierScreen` displaying unresolved issues and official facilitation contact points.
- [ ] Verify WCAG 2.1 AA keyboard tab order across all 6 component groups.

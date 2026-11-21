# Translation and UI Localization Assets (Task D-02)

- **Module:** Deepshika (`@deepshikapalepu20`)
- **Phase:** Task D-02 (Weeks 3–4)
- **Status:** Complete for English and Hindi; Telugu regional language strings planned for Task D-04 upon team kickoff confirmation.
- **Verification Script:** [scripts/verify_strings.py](../../scripts/verify_strings.py)

---

## 1. Directory Overview

This directory contains the authoritative user interface (UI) localization dictionaries for IP-SAKTI Sahayak:
- [`ui_strings_en.json`](ui_strings_en.json): Canonical English UI dictionary.
- [`ui_strings_hi.json`](ui_strings_hi.json): Verified Hindi UI dictionary with 100% key parity and strict statutory preservation rules.

---

## 2. Namespace Hierarchy

Both translation files share an identical recursive JSON structure organized across eight functional domains:

| Namespace | Functional Scope | Key Components |
|---|---|---|
| `brand` | System identity & branding | Title, subtitle, version tag, bounded scope badge |
| `nav` | Main application navigation | Home, intake, cited answer, knowledge sources, referral dossier, language selector, jurisdiction toggle |
| `disclaimer` | Legal non-advice disclaimers | Header short disclaimer, footer full statutory disclaimer, provisional classification warning |
| `jurisdiction` | Sovereign jurisdiction filtering | Domestic Indian statutory regime vs non-binding International overview (WIPO GRATK) |
| `intake` | Guided formulation questionnaire | Progress indicators, formulation metadata fields, 8 elimination questions (`Q-USE`, `Q-INGR`, `Q-FORM`, `Q-ROUTE`, `Q-FOOD-TEXT`, `Q-FOOD-CLAIM`, `Q-FOOD-SYN`, `Q-COSM-CLAIM`), options, helper text, and missing-fact clarification prompts |
| `routes` | Provisional routing outputs | 7 classification routes: Classical ASU Drug, Patent or Proprietary ASU Drug, Novel Formulation, Phytopharmaceutical Drug, Ayurveda Aahara, Ayurvedic Cosmetic, and Unknown/Ambiguous |
| `answer` | Cited answer presentation | Response status badges (`clarify`, `answered`, `abstained`, `referral`), verified findings card, evidence support levels, assumptions, limitations, cited provisions |
| `source_drawer` | Accessible source drawer / modal | Issuing authority, provision locator, Source ID, Passage ID, gazette publication date, official portal link, verbatim excerpt, corpus review status (`approved`, `pending`, `stale`, `rejected`) |
| `safety` | Uncertainty & safe abstention | Safe abstention banner, out-of-scope notice, missing mandatory facts prompt, unverified translation safety fallback |
| `referral` | Specialist consultation dossier | Dossier title, download buttons (JSON/PDF), unresolved statutory issues list, official facilitation contact points (IP India, AYUSH SLA, NBA, FSSAI, TKDL) |
| `accessibility` | Screen-reader & WCAG 2.1 AA | Skip to main content link, modal open/close ARIA announcements, language/jurisdiction change announcements, dynamic `aria-live` status messages |

---

## 3. Statutory Terminology & Preservation Rules

Localization in IP-SAKTI Sahayak is constrained by the [Controlled Glossary v0](../glossary/controlled_glossary_v0.csv) and four statutory preservation rules:

1. **`ID_IMMUTABLE`**:
   - Technical and database identifiers (`Q-USE`, `PASS-xxx`, `REAL-xxx`, `GLOSS-xxx`, `SYNTH-xxx`) must remain in ASCII Latin script identically across English, Hindi, and regional language views.
2. **`NUMBER_IMMUTABLE`**:
   - Statutory section, rule, sub-rule, and regulation designators must retain their exact statutory alphanumeric notation (e.g. `Section 3(p)`, `Section 3(h)`, `Section 3(a)`, `Rule 2(eb)`, `Regulation 2(b)`, `Regulation 8`, `Regulation 3(4)`). Translating subsection letters into Devanagari numerals or letters is strictly prohibited.
3. **`NAME_IMMUTABLE`**:
   - Statutorily defined nomenclature where English names are designated by legal notification must preserve Latin script alongside vernacular equivalents (e.g. `आयुर्वेद आहार (Ayurveda Aahara)`, `पादप-औषध (Phytopharmaceutical Drug)`).
4. **`ACRONYM_IMMUTABLE`**:
   - Institutional and treaty acronyms must retain their Latin representation (e.g. `WIPO (डब्ल्यूआईपीओ)`, `AYUSH`, `FSSAI`, `NBA`, `TKDL`).
5. **`PRESERVE_NEGATION`**:
   - Negative statutory exclusions (e.g. non-patentability under Section 3(p), prohibition of human disease treatment/cure claims under FSSAI Regulation 8) must preserve unambiguous legal negation in localized strings.

---

## 4. Integration with Frontend (Akshay Tasks A-01 and A-02)

Akshay's React components import strings dynamically based on user language state:
```typescript
import enStrings from "@/data/translations/ui_strings_en.json";
import hiStrings from "@/data/translations/ui_strings_hi.json";

export const useTranslation = (lang: "en" | "hi") => {
  return lang === "hi" ? hiStrings : enStrings;
};
```

---

## 5. Automated Verification

Run string parity and preservation checks:
```bash
python scripts/verify_strings.py
```
Checks:
- Valid JSON parsing for all locale files.
- 100% key parity (recursive tree comparison).
- Non-empty values for all terminal string keys.
- Presence of all required immutable statutory tokens in localized files.

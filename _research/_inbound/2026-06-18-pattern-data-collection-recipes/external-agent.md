# Data-collection recipes — external-agent pass

*Second independent pass for the Data-collection recipes pattern brief. Captured as the dual-agent audit record (the stray `aws sso login` line from the paste is omitted). Synthesised with `claude.md` into `patterns/data-collection-recipes.md`.*

---

## Data-collection recipes

Forms-as-a-system orchestrates the experience; Data-collection recipes construct the actual data nodes. While the overarching form shell dictates validation timing, focus management, error summarization, and the persistence model, the recipes defined herein govern the per-datum reality — the precise input counts, autocomplete contracts, formatting tolerances, and internationalization postures the shell itself remains entirely agnostic toward.

### Problem & context

Digital interfaces consistently capture the same six dimensions of human identity and commerce: names, physical locations, birth dates, telecom routing digits, digital routing addresses, and financial credentials. Despite their ubiquity, extraction methods remain fragmented and frequently hostile — restrictive input masks, multi-column layouts that break visual scanning, rigid localized schemas. The core problem stems from failing to separate the data a system requires for backend processing from the cognitive model the user employs to provide it. The "falsehoods programmers believe" lineage catalogues these failures; WCAG 2.2 §1.3.5 (Identify Input Purpose) and §3.3.7 (Redundant Entry) make optimised collection a mandate, not a nicety. The fix: shift the burden of parsing and normalisation from the human to the backend.

### Composition

Strictly compositional — no new atomic components. Text Field is the primary vehicle; Select is used sparingly (country only); Checkbox/Radio for boolean toggles (billing-same-as-shipping); Fieldset + Legend for compound-datum grouping. The recipes inject into the Forms-as-a-system shell, which alone owns the `<form>` wrapper, the error summary, submit actions, and validation timing.

| Datum | Primary assembly | Wrapper | Peripheral |
|---|---|---|---|
| Name | Text Field (single) | none | — |
| Address | Text Field (multiple), Select (country) | Fieldset & Legend | Checkbox (billing toggle) |
| Date of birth | Text Field (3×) | Fieldset & Legend | — |
| Phone | Text Field (single) | none | Select (country-code fallback) |
| Email | Text Field (single) | none | — |
| Payment card | API-driven iframe (segmented) | Fieldset & Legend | — |

### Decision rules

**1. One input vs many.** IF the datum is highly variable/culturally dependent (names) → single unstructured input. IF it requires precise backend segmentation AND international variance is high (global addresses) → structured multi-line inputs driven by locale schemas. IF memorable but format-ambiguous (DOB) → structured multi-input text (D/M/Y). IF conceptually a single contiguous string (phone, email) → single input with high tolerance.

**2. The autocomplete token contract.** IF a field collects data about the current user → the exact WHATWG token. IF it collects a third party's data ("Recipient's name") → standard labelling but **omit** the personal token (prevents the browser overwriting the user's own saved profile). IF tempted to disable autofill → `autocomplete="off"` only for one-time codes/sensitive internal identifiers, never standard personal data.

**3. Format tolerance & normalisation.** Postel's Law — accept spaces/dashes/brackets/varied casing; normalise on blur or backend. Avoid strict character masking, especially for international data.

**4. Internationalisation posture.** Assume a global user base unless business logic fences it. Phone → accommodate country codes by default (libphonenumber). Address → country selector is the primary determining variable (it shifts the schema).

**5. Privacy & proportionality.** IF age verification but not exact DOB → boolean/age-range. IF billing address but shipping already given → default-checked "same as" toggle (satisfies §3.3.7).

### The recipes

**Name.** Single full-width field, label "Full name"; `autocomplete="name"` (split only if forced: given-name/family-name, and prefer "Given names"/"Family name" globally). Accept all Unicode, no forced casing ("McNamara", "van der Waals"), `spellcheck="false"` (don't flag ethnic/uncommon names). Sorting: some cultures (Thai, Icelandic) sort by given name. Signature anti-pattern: the honorific/title trap (mandatory Mr/Mrs/Dr dropdown — forces gender/marital disclosure; if required, optional free text).

**Address.** Prefer API lookup with a **mandatory manual-entry fallback**. Manual structure = stacked single-column text lines (Baymard: multi-column address forms cause visual-tracking errors and skipped fields). Labels: Address line 1 / line 2 (optional) / Town or city / State-Province-Region (localised) / Postcode-ZIP (localised). Tokens: street-address or address-line1/2, address-level2 (city), address-level1 (state), postal-code, country. Country first; selection drives field visibility/labels/requirement (Google libaddressinput keys: N/O/A/C/S/Z). Always allow force-submit of the user's typed version over an API "correction." Anti-pattern: rejecting addresses lacking a street number/postcode or containing slashes.

**Date of birth.** Three side-by-side text inputs (Day/Month/Year) under a fieldset/legend "Date of birth"; tokens bday-day/-month/-year; accept single digits (4 or 04); validate real calendar date + business range (18+); `inputmode="numeric"`. Signature anti-pattern: a Date Picker calendar (navigating back 35 years is a usability/accessibility failure — users know their DOB, typing is faster).

**Phone.** Single unstructured field, label "Phone number" (or "Mobile phone number" if SMS); `autocomplete="tel"`, `type="tel"` (numeric keypad). Accept spaces/dashes/+/parens; parse + normalise to E.164 via libphonenumber. Allow full international (+) or local with inferred/selected country code. Anti-pattern: rigid `(XXX) XXX-XXXX` visual mask; separate area-code boxes (Baymard: raises mobile interaction cost).

**Email.** Single field wide enough for ~30 chars; label "Email address"; `autocomplete="email"`, `type="email"` (keyboard with @ and .com), `spellcheck="false"`. Structural regex only. Signature anti-pattern: the confirm-email re-type field (users copy-paste, defeating it) — use a verification loop (magic link / OTP) instead.

**Payment card.** Segmented: full-width PAN on its own line for verification, then Expiry + Security code (Baymard supports these two on one line as a single logical entity). Labels: Card number / Expiry date / Security code (avoid CVV/CVC jargon without a locating graphic). Tokens cc-number, cc-exp (or cc-exp-month/-year), cc-csc, cc-name. Client-side Luhn; **auto-space the PAN** in groups of 4 (the one place dynamic visual formatting is recommended). Security/PCI: serve via secure iframe (Stripe Elements / Braintree Hosted Fields) for SAQ A compliance; pass the shell's design tokens through the provider API so the iframe matches the native UI.

### Accessibility orchestration

The autocomplete contract is the primary mechanism for WCAG 2.2 §1.3.5. Compound datums (DOB, address) wrap in `<fieldset>` with the question in `<legend>`, so AT announces "Date of birth, Month" rather than a context-free "Month"; `aria-describedby`/visually-hidden text disambiguates micro-inputs. (Error announcement, focus during errors, and the Error Summary are the shell's, not the recipe's.)

### Content & copy

Static top-aligned labels, never placeholder-as-label (disappears on focus, fails contrast). Hint text between label and input with localised format examples ("For example, 07700 900 982 or +44 808 157 0192"; "QQ 12 34 56 C"). Sensitive/unexpected datums (phone, DOB) get a progressive-disclosure "Why we need this information" link explaining usage/retention — builds trust, raises completion.

### Variants & responsive

Horizontally grouped fields (Expiry + CVC) collapse to stacked single-column on mobile. Address: default "Search for address" (API) with a "Enter address manually" link that swaps in the full structured recipe. Use `type`/`inputmode` to trigger the right virtual keyboards (email; numeric for DOB and card).

### Anti-patterns

Date pickers for historical dates; splitting names unnecessarily; rejecting valid international formats (missing postcode, non-10-digit phone); confirm-email re-type; disabling autofill for pseudo-security (breaks §1.3.5); data hoarding without proportionality (full DOB when "18 or older?" suffices).

### Related patterns & components

- **Forms-as-a-system (pattern)** — parent shell: save model, submit timing, error summary, focus routing. Recipes live inside it.
- **Date Picker (component)** — calendar GUI for forward-looking scheduling; barred from the DOB recipe.
- **Login & Authentication (pattern)** — password/MFA/session; email & phone *as auth* rely on its security logic, distinct from initial capture here.
- **13-Internationalization (foundation)** — RTL, translation strings, currency; the broad engine. Per-datum i18n shape resolved here.

### Field POV evolution

Historically backend DBs dictated the frontend (first_name/last_name columns → forced name splits; zip-required shipping → globally mandatory postcodes). The modern POV reverses this: shift parsing/validation/formatting onto the machine. Evident in lookup-over-manual address entry, libphonenumber normalisation over input masks, and the research-backed abandonment of multi-column layouts. The `autocomplete` attribute evolved from convenience to non-negotiable accessibility mandate.

### Reference instantiations & sources cited

GOV.UK Design System ("Ask users for…" — dates, names, addresses, phone); WHATWG HTML + W3C WCAG 2.2 (autocomplete token list; §1.3.5, §3.3.7); W3C Internationalization WG (name capture, cultural variance); Google open source (libaddressinput, libphonenumber); Baymard Institute checkout research (multi-column harm; payment auto-spacing; friction points); the "Falsehoods Programmers Believe" lineage. Verified across 2024–2026.

### Agent-consumable schema (external pass)

```yaml
id: pattern-data-collection-recipes
name: Data-collection recipes
aliases: [Form fields, Input recipes, High-frequency datums]
tier: composition
goal: ask-for-data
status: finalized
problem: >
  High-frequency data (names, addresses, phone numbers) are highly variable across global locales.
  Forcing restrictive formats (multi-column layouts, strict input masks, forced name splitting)
  increases abandonment, pollutes backend data, and creates severe accessibility barriers.
composition:
  requires: [component-text-field, component-select, component-checkbox, component-radio, component-fieldset]
decision_rules:
  - { if: "datum requires cultural variance absorption (e.g., Names)", use: "single free-text field, no forced casing" }
  - { if: "datum collects user identity information", use: "strict WHATWG autocomplete token (WCAG 1.3.5)" }
  - { if: "datum receives non-standard but logical human spacing (phones, cards)", use: "lenient acceptance, normalize on blur/backend" }
  - { if: "datum requires global compatibility", use: "libaddressinput/libphonenumber parsing, driven by Country selection" }
  - { if: "datum can be inferred or previously supplied", use: "pre-fill or boolean toggle (WCAG 3.3.7)" }
recipes:
  name: { input_count: "1 (default)", autocomplete: "name", validation: "all Unicode, no forced casing, spellcheck=false", i18n: "mononyms, patronymics, varied sorting", anti_pattern: "forcing Given/Family split; honorific dropdowns" }
  address: { input_count: "multi-line structured", autocomplete: [street-address, address-line1, address-level2, postal-code, country], validation: "lenient, manual override always permitted", i18n: "libaddressinput; country selection dictates fields", anti_pattern: "multi-column layout; rigid postal-code enforcement" }
  date_of_birth: { input_count: "3 (D,M,Y)", autocomplete: [bday-day, bday-month, bday-year], validation: "numeric, real-date, range bounds", i18n: "numeric entry bypasses MM/DD ambiguity", anti_pattern: "Date Picker for historical dates" }
  phone_number: { input_count: 1, autocomplete: "tel", validation: "libphonenumber to E.164", i18n: "accept + and spaces; country code inferred/selected", anti_pattern: "visual input masking; separated codes" }
  email_address: { input_count: 1, autocomplete: "email", validation: "regex, spellcheck=false, inputmode=email", i18n: "ASCII + valid international domain", anti_pattern: "confirm-email re-type" }
  payment_card: { input_count: "segmented (PAN, Expiry, CVC)", autocomplete: [cc-number, cc-exp, cc-csc], validation: "Luhn; auto-spacing PAN", i18n: "Stripe Elements/iframe", anti_pattern: "unspaced numbers; non-compliant native storage" }
accessibility_orchestration:
  - "WCAG 1.3.5 via strict autocomplete adherence."
  - "Wrap compound datums (DOB, address) in fieldset/legend for AT context."
  - "aria-describedby for multi-input hinting to prevent navigation traps."
content:
  - "Static top-aligned labels (never disappearing placeholders)."
  - "Hint text with localized format examples."
  - "Sensitive requests: 'Why we ask for this' progressive disclosure."
variants:
  - "Address: API lookup (primary) <-> manual entry (fallback)."
  - "Responsive: horizontal pairings collapse to single column on mobile."
anti_patterns: [date pickers for DOB, splitting names unnecessarily, rejecting valid international formats, confirm-email re-type, disabling autofill for security]
relations:
  composes: []
  relates_to: [component-date-picker, pattern-login-authentication]
  boundary:
    - "pattern-forms-as-a-system: shell owns validation timing, focus, error summary."
    - "foundation-13-internationalization: global RTL logic and core strings."
notes:
  contested: "Baymard allows CVC/Expiry on one line; all other inputs strictly single-column."
  unverified: "None. All decisions mapped to GOV.UK, WHATWG, or W3C standards."
```

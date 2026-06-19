---
okf_version: "0.1"
type: pattern-brief
title: Data-collection recipes
description: The "Ask users for X" family — the per-datum field recipes that live inside the Forms-as-a-system shell. How to ask for a name, an address, a date of birth, a phone number, an email, and a payment card: the one-input-vs-many decision, the non-negotiable autocomplete-token contract (the third-party-data caveat included), tolerate-and-normalise, the i18n-first posture, proportionality, and each datum's signature anti-pattern. Composes Text Field/Select/Fieldset/Date Picker; borders Forms-as-a-system (the shell), the Date Picker component (the DOB recipe refuses it), the Login pattern, and 13-internationalization.
tags: [patterns, forms, data-collection, autocomplete, internationalization, accessibility]
tier: composition
goal: ask-for-data
status: stable
aliases: [Data-collection recipes, Ask users for, field recipes, input recipes, high-frequency datums]
last-audited: 2026-06-18
timestamp: 2026-06-18
---

# Data-collection recipes

> Forms-as-a-system owns *how a form behaves*; it knows nothing about *what it is asking for*. But the high-frequency datums every product collects — a name, an address, a date of birth, a phone number, an email, a payment card — each carry a settled, hard-won field shape: how many inputs they need, how they must be labelled, which `autocomplete` tokens make them autofillable, what formats to tolerate, and how they vary across the world. Get these wrong and the form thrashes no matter how good the shell is — a date picker for a birth year, a name split that erases half the planet's names, a country dropdown that rejects a valid address. This brief is the family of per-datum recipes that drop into the shell. It defers all orchestration to Forms-as-a-system and owns only the datum.

---

## Problem & context

A form is mostly the same six or seven things, asked over and over: a name, a location, a birth date, a phone number, an email, a payment card. The reason to brief them together is that they share a spine — an `autocomplete` contract, a tolerate-and-normalise discipline, an internationalisation posture, a one-input-vs-many decision — and that each has a *signature mistake* the field has already made and learned from. GOV.UK codified this as the "Ask users for…" family, and it is the most battle-tested form corpus in existence precisely because it serves the whole population, including the people every other system's defaults quietly exclude.

The deeper failure these recipes correct is a single one: confusing the data the *backend* wants to store with the model the *user* holds in their head. When a system assumes every name is a "first" and a "last," every address a building-street-city-state-ZIP, every phone a ten-digit domestic number, the interface becomes a barrier — and the "falsehoods programmers believe about names / addresses / phone numbers" lineage is the catalogue of exactly these assumptions failing. The fix is to shift the burden of parsing, validating, and formatting *off the human and onto the machine*: accept what the user honestly types, normalise it server-side. The modern compliance floor makes this a mandate, not a nicety — WCAG 2.2 §1.3.5 (Identify Input Purpose) and §3.3.7 (Redundant Entry).

The pattern applies whenever a product collects standard personal or transactional data. It does not apply to bespoke domain fields (an invoice line, a medical code) — those get the generic shell treatment. The field diverges here not over taste but because the *world* is heterogeneous; the recipes resolve that by treating the global case as the default, not the exception.

## Composition

These recipes are strictly compositional — they introduce no new component. They assemble briefed controls and add only the datum-level shape; the orchestration is the shell's.

- **Text Field** (see text-field) — the workhorse for almost everything: name, address lines, the DOB day/month/year inputs, phone, email, card number/CVC. With the right `inputmode`, `type`, `autocomplete`, and `spellcheck`.
- **Select / Combobox** (see select, see combobox) — used sparingly, reserved for genuinely fixed global sets: **country** (address, phone-code fallback). Not the default for things that merely *look* enumerable.
- **Checkbox** (see checkbox) — the proportionality toggles ("Billing address same as shipping").
- **Fieldset + legend** — the structural grouping for compound datums (DOB, address), so AT announces the question before the parts.
- **Date Picker** (see date-picker) — deliberately **not** used for date of birth; reserved for calendar/future dates. The DOB recipe is the explicit counter-example.
- **The Forms-as-a-system shell** (see patterns/forms-as-a-system) — composes these recipes; owns the `<form>` wrapper, validation *timing*, the error summary, focus, and save. This brief plugs into it and never duplicates it.

**The delta this pattern adds** is per-datum: the input count and structure, the labels, the `autocomplete` tokens, the format tolerance, and the i18n shape — none of which any control or the shell can decide on its own.

## Decision rules

The cross-cutting spine first; the per-datum recipes follow in §6.

**1. One input vs many** — the most consequential recipe decision. The bias is **the fewest inputs that still parse and autofill**; every extra input is a tab stop and a place to disagree with the user's reality.
- `IF the datum is culturally variable (name)` → a single unstructured field; segmenting guarantees exclusion and data corruption.
- `IF the datum needs precise backend segmentation AND international variance is high (address)` → structured multi-line inputs driven by a locale schema (logistics need a distinct postcode/region a single textarea can't reliably parse worldwide).
- `IF the datum is memorable but format-ambiguous (date of birth)` → structured plain-text inputs (day/month/year), not a picker — separating the parts kills the MM/DD-vs-DD/MM ambiguity.
- `IF the datum is one contiguous string in the user's mind (phone, email)` → a single high-tolerance field.

**2. The `autocomplete` token contract — non-negotiable.** Correct tokens satisfy WCAG 2.2 §1.3.5, let the browser/password-manager fill instantly, and let AT overlay personalised iconography — measurably cutting error and abandonment.
- `IF a field collects data about the current user` → set the exact WHATWG token (`name`, `bday-year`, `tel`, `email`, `cc-number`…).
- `IF a field collects a third party's data ("Recipient's name", a gift address)` → label it normally but **omit the personal token**, so the browser doesn't overwrite the user's own saved profile with someone else's details.
- `NEVER` use `autocomplete="off"` on standard personal data; reserve it for one-time codes and sensitive internal identifiers.

**3. Format tolerance & normalisation.** Postel's Law: liberal in what you accept, conservative in what you store. `ALWAYS` accept spaces, dashes, parens, `+`, varied case — and **normalise on blur or server-side**; `NEVER` reject a syntactically valid international value for not matching a domestic template. Avoid strict character-by-character masking for international data; it breaks on the first edge case. Strip, don't scold.

**4. Internationalisation posture.** The default assumption is **global users** unless the service is provably single-locale. Address: the **country selector is the primary variable** — choosing it shifts the schema. Phone: accommodate country codes by default. Resolve the *per-datum* shape here; reference the general RTL/translation/locale POV to 13-internationalization rather than re-deriving it.

**5. Privacy & proportionality.** `IF you don't need a datum to deliver the service` → don't ask. `IF you only need a derived fact` → ask for that, not the raw datum (an over-18 check is a checkbox or an age, not necessarily a full DOB). `IF a value was already given this session` → pre-fill or offer a "same as" toggle (the default-checked "Billing address is the same as shipping"), satisfying §3.3.7. Fewer fields, less PII, lower abandonment, less to secure.

## The recipes

Per-datum shape. Each: input count + structure, labels, `autocomplete`, validation/normalisation, i18n, signature anti-pattern.

| Datum | Inputs | `autocomplete` | Validate / normalise | i18n shape | Signature anti-pattern |
|---|---|---|---|---|---|
| **Name** | **One** "Full name" field | `name` (parts only if independently needed) | Accept all Unicode, any length, no two-word rule, no forced casing; `spellcheck="false"` | Mononyms, multiple family names, no given/family split are all valid; some cultures sort by given name | First/Middle/Last split; rejecting non-Latin/single-token names; the **honorific dropdown** |
| **Address** | **Structured lines, country-first**; lookup + manual fallback | `country`, `address-line1/2`, `address-level2` (city), `address-level1` (state), `postal-code` | Postcode/state optional and country-driven; always allow force-submit of the typed value over an API "correction" | Country chosen first → schema adapts (libaddressinput); some have no postcode, no state | Fixed US/UK template; mandatory global "State"; multi-column lines; no manual fallback after lookup |
| **Date of birth** | **Three text inputs** D / M / Y, in a fieldset | `bday` + `bday-day/-month/-year` | Accept 1- or 2-digit parts; validate the real composite date + range (18+); `inputmode="numeric"` | Labelled parts sidestep the locale order trap | A **calendar Date Picker** (paging to 1965); a single free-text date; auto-advancing focus between parts |
| **Phone** | **One** international field | `tel` (+ `type="tel"` for the keypad) | Accept `+`, spaces, dashes, parens; normalise toward E.164 (libphonenumber); no mask | One field + optional country selector; no domestic length/format assumption | Separate area-code boxes; a forced `(___) ___-____` mask; rejecting `+`/non-domestic lengths |
| **Email** | **One** field, `type="email"` `inputmode="email"`, ~30 chars wide | `email` | Lenient syntactic check; trim; `spellcheck="false"` | Internationalised (Unicode) addresses exist — don't over-restrict | A **confirm-email re-type** field; aggressive regex rejecting valid addresses |
| **Payment card** | PAN full-width; **expiry + security code may share a row**; via hosted iframe | `cc-number`, `cc-exp` (or `-month/-year`), `cc-csc`, `cc-name` | Luhn-check client-side; **auto-space the PAN** in 4s; accept pasted values | Mostly universal; CSC length varies (Amex 4) | Segmented 4×4 number boxes; blocking spaces/paste; "CVV" jargon with no locating graphic; manual card-type select |

A note on payment: the PAN's auto-spacing is the *one* place dynamic visual formatting earns its keep (it mirrors the embossed card and aids transcription). And the security boundary is real — serve card fields through a hosted iframe (Stripe Elements, Braintree Hosted Fields) for PCI-DSS SAQ A scope, passing the shell's design tokens through the provider's theming API so the iframe matches the native UI. The PCI mechanics themselves are out of scope here (reference, don't re-derive).

## Accessibility orchestration

The a11y this brief owns; the error-summary/focus contract is the shell's.
- **Identify Input Purpose (WCAG 2.2 §1.3.5)** — the `autocomplete` token *is* the a11y feature: it exposes input purpose to AT and personalisation tools, not just autofill.
- **Compound-datum grouping** — wrap multi-input datums (DOB day/month/year, the address block) in `fieldset` + `legend` ("Date of birth"), so a screen-reader user tabbing straight to the second box hears "Date of birth, Month," not a context-free "Month." Each sub-input carries a real `<label>`, never a placeholder; `aria-describedby` or visually-hidden text disambiguates where needed.
- **The multi-input labelling trap** — three unlabelled boxes are unusable to AT; the composite error (an impossible date) attaches to the group, the per-part format error to the part.
- **Input mode & keyboard** — `inputmode="numeric"` for card/CVC/DOB parts, `type="email"`/`tel` where apt, so mobile keyboards match the datum.

## Content & copy

- **Labels** are static, top-aligned, and the plain name of the datum ("Full name," "Date of birth," "Mobile number") — never the placeholder (placeholder-as-label disappears on focus and fails contrast).
- **Hint text** sits between label and input, carrying a format *example*, not a rule ("For example, 31 3 1980"; "QQ 12 34 56 C"); persistent, read in the natural vertical flow.
- **Say why** for anything sensitive or unexpected (DOB, phone) — a "Why we need this" disclosure detailing use and retention raises completion and trust.
- **The honorific/title trap** — don't ask for a title unless you genuinely use it; it's forced, often wrong, and disproportionately makes women disclose marital status. If truly needed, an optional free-text field.
- **Optional discipline** — mark per the shell's mark-the-minority rule; better still, don't ask.

## Variants & responsive

- **Address: lookup vs manual** — a postcode/address lookup as the fast path, with an always-available "Enter address manually" link that swaps in the full structured recipe. Lookup is never the only route.
- **Payment: single auto-spaced PAN** (default) with expiry + CVC sharing a row on desktop, collapsing to stacked single-column on mobile.
- **Phone: one field** vs field + country-code selector for international services.
- Horizontally paired inputs (card expiry, DOB parts) stay on one row but collapse gracefully on narrow viewports; `type`/`inputmode` trigger the right virtual keyboard throughout.

## Anti-patterns

A Date Picker for date of birth. Splitting a name into First/Middle/Last (and requiring all three). Rejecting valid international names, addresses, or phone numbers for not matching a domestic template. A mandatory "State/Province" dropdown for the whole world. A 200-item country dropdown with no search, or a wrong default. Multi-column address lines (Baymard: they break visual tracking and cause skipped fields). Confirm-email re-type fields. Blocking spaces or paste in card/phone fields. Segmented card-number boxes. `autocomplete="off"` on standard personal data. Asking for a full DOB when an age or over-18 check would do. Honorific dropdowns nobody uses.

## Related patterns & components

- **vs Forms-as-a-system** (see patterns/forms-as-a-system) — the shell owns validation *timing*, the error summary, focus management, and the save model; this brief owns the per-datum field *shape*. The shell composes these recipes; they never duplicate its orchestration.
- **vs the Date Picker component** (see date-picker) — the calendar control for chosen/future dates; the DOB recipe is the explicit case where the field-truth answer is *not* a date picker.
- **vs Login & authentication (pattern)** — email-and-password *for authentication* (sign-in, reset, MFA, the verification-link flow) lives there; this brief owns email and phone as *data capture*.
- **vs Foundations / 13-internationalization** — the general RTL/translation/locale POV is the numbered file; this brief references it and resolves only the per-datum i18n shape.
- **`composes`:** text-field, select, combobox, checkbox, date-picker.

## Field POV evolution

The baseline reversed: historically the backend database dictated the UI — `first_name`/`last_name` columns forced a name split, a zip-required shipping table made postcodes globally mandatory. The modern POV shifts the burden of parsing, validating, and formatting *off the user and onto the machine*. It shows in three moves: manual address entry gave way to **lookup-first with a manual fallback**; rigid phone masks gave way to a **single international field** normalised to E.164 (libphonenumber); and quantitative research retired **multi-column layouts** as harmful to scanning and completion. Alongside, the `autocomplete` contract went from a nice-to-have to a **non-negotiable accessibility mandate** (WCAG 2.2 §1.3.5), cementing the browser as the user's trusted data proxy — and the default assumption moved from a domestic template to an **i18n-first** one, the "falsehoods programmers believe" literature having done the work of making the inclusive shape the professional default.

## Reference instantiations

Go look at: **GOV.UK** "Ask users for…" (addresses, names, dates, email, phone, payment card) and the memorable-date pattern — the reference corpus; the **WHATWG/W3C `autocomplete` token list** and **WCAG 2.2 §1.3.5/§3.3.7**; **Google's libaddressinput** (the i18n address schema: N/O/A/C/S/Z keys) and **libphonenumber** (E.164); **Stripe Elements / Braintree Hosted Fields** for payment-field UX and PCI scope; **Baymard Institute** checkout research for the layout findings.

## Sources cited

- GOV.UK Design System — "Ask users for…" patterns (addresses, names, dates, email addresses, phone numbers, payment card details, National Insurance number), memorable dates, "Check your answers" (2025; *verify current version*).
- WHATWG HTML — the `autocomplete` autofill token list; W3C WCAG 2.2 — §1.3.5 Identify Input Purpose, §3.3.7 Redundant Entry.
- W3C Internationalization Working Group — personal-names guidance and cultural variance.
- Google libaddressinput / i18n address format data — international address structure; libphonenumber — E.164 parsing/normalisation (*verify currency*).
- Baymard Institute — checkout address & payment-form research (multi-column harm; PAN auto-spacing; the expiry+CVC-on-one-line finding) (*verify specific figures before quoting*).
- "Falsehoods programmers believe about names" (Patrick McKenzie, 2010) and the "…about addresses / phone numbers" lineage — the i18n-default lineage (*secondary, widely cited*).
- Stripe — Elements / Hosted Fields and PCI-DSS SAQ A scope (*verify*).
- Design-system precedents (Carbon, Polaris, Material, Atlassian) for address/payment/name where documented (*spotty; flagged*).

`notes.unverified`: GOV.UK is the clear corpus for *named* address/name/date recipes; whether the product design systems (Carbon, Polaris, Material, Atlassian) ship a comparably *named* address/payment recipe vs deferring to the form shell is spottier — verify before asserting convergence. Specific Baymard completion figures and current version strings are flagged for verification. The confirm-email recommendation (verification loop over re-type) is strongly supported by both passes but can be contested in some commerce contexts — noted.

## Agent-consumable schema

```yaml
identity:
  id: data-collection-recipes
  name: Data-collection recipes
  aliases: [Ask users for, field recipes, input recipes, high-frequency datums, personal-data fields]
  tier: composition
  goal: ask-for-data
  status: stable
problem: >
  The high-frequency datums (name, address, date of birth, phone, email,
  payment card) each carry a settled field shape — input count, autocomplete
  tokens, format tolerance, i18n form — that the generic form shell cannot
  decide. This brief is the family of per-datum recipes composed inside
  Forms-as-a-system; it shifts parsing/normalisation off the user and onto the
  machine, and defers all orchestration to the shell.
composition:
  requires: [text-field, select, combobox, checkbox, date-picker]
  shell: forms-as-a-system
  delta: per-datum input count/structure, labels, autocomplete tokens, format tolerance/normalisation, i18n shape
decision_rules:
  one_vs_many:
    - { if: "culturally variable datum (name)", use: "single unstructured field" }
    - { if: "needs precise backend segmentation AND high international variance (address)", use: "structured multi-line, locale-schema-driven" }
    - { if: "memorable but format-ambiguous (date of birth)", use: "structured plain-text day/month/year, NOT a date picker" }
    - { if: "one contiguous string in the user's mind (phone, email)", use: "single high-tolerance field" }
  autocomplete:
    - { if: "field collects current-user data", use: "exact WHATWG token (WCAG 1.3.5)" }
    - { if: "field collects a third party's data (recipient/gift)", use: "label normally but OMIT the personal token (avoid overwriting user's profile)" }
    - { if: "tempted to use autocomplete=off on standard personal data", use: "do not; reserve for one-time codes / sensitive internal ids" }
  format_tolerance:
    - { if: "user types spaces/dashes/+/varied case", use: "accept and normalise on blur/server" }
    - { if: "value is a valid international form", use: "never reject for not matching a domestic template; avoid strict masks" }
  i18n:
    - { if: "service not provably single-locale", use: "assume global; country selector drives address/phone shape" }
  proportionality:
    - { if: "datum not needed to deliver the service", use: "do not ask" }
    - { if: "only a derived fact needed (e.g. over-18)", use: "ask for that, not the raw datum" }
    - { if: "value already given this session", use: "pre-fill or 'same as' toggle (WCAG 3.3.7)" }
recipes:
  name: { inputs: "one full-name field", autocomplete: "name (parts only if needed)", validate: "Unicode, any length, no two-word rule, no forced casing, spellcheck=false", i18n: "mononyms/multiple family names valid; some cultures sort by given name", anti_pattern: "First/Middle/Last split; honorific dropdown" }
  address: { inputs: "structured lines, country-first; lookup + manual fallback", autocomplete: "country, address-line1/2, address-level2/1, postal-code", validate: "postcode/state optional, country-driven; allow force-submit over API correction", i18n: "libaddressinput; country selection dictates fields", anti_pattern: "fixed US/UK template; mandatory global State; multi-column lines" }
  date_of_birth: { inputs: "three text inputs D/M/Y in a fieldset", autocomplete: "bday (+ bday-day/-month/-year)", validate: "lenient digits, real composite date, range (18+), inputmode=numeric", i18n: "labelled parts sidestep order trap", anti_pattern: "calendar Date Picker; auto-advancing focus" }
  phone: { inputs: "one international field", autocomplete: "tel (+ type=tel)", validate: "accept +/spaces/dashes/parens, normalise to E.164 (libphonenumber)", i18n: "no domestic length/format assumption; optional country selector", anti_pattern: "area-code boxes; forced US mask" }
  email: { inputs: "one field type=email inputmode=email ~30ch", autocomplete: "email", validate: "lenient syntactic, trim, spellcheck=false", i18n: "Unicode addresses exist", anti_pattern: "confirm-email re-type; over-strict regex" }
  payment_card: { inputs: "PAN full-width; expiry + security code may share a row; hosted iframe", autocomplete: "cc-number, cc-exp(-month/-year), cc-csc, cc-name", validate: "Luhn; auto-space PAN in 4s; accept paste", i18n: "CSC length varies (Amex 4)", anti_pattern: "segmented number boxes; block paste; CVV jargon w/o graphic; manual card-type select", security: "hosted iframe (Stripe Elements/Braintree) for PCI SAQ A; theme via provider API" }
accessibility_orchestration: >
  autocomplete token = Identify Input Purpose (1.3.5); fieldset/legend around
  compound datums (DOB, address) so AT hears the question before the part;
  real <label> per sub-input (never placeholder); composite error to the
  group, format error to the part; inputmode/type per datum. (Error summary +
  focus routing are the shell's.)
content: >
  Static top-aligned plain-name labels; hint text as a format example not a
  rule; say-why progressive disclosure for sensitive data; avoid honorific
  fields; mark per the shell's mark-the-minority rule (better not to ask).
variants: [address-lookup-vs-manual, payment-PAN-fullwidth-expiry+cvc-row, phone-with-country-selector]
anti_patterns:
  - date picker for date of birth
  - splitting names into First/Middle/Last
  - rejecting valid international names/addresses/phones
  - mandatory global State/Province dropdown
  - multi-column address lines
  - unsearchable 200-item country dropdown / wrong default
  - confirm-email re-type field
  - blocking spaces or paste in card/phone fields
  - segmented card-number boxes
  - autocomplete=off on standard personal data
  - asking full DOB when an age/over-18 check suffices
  - honorific/title dropdowns
reference_instantiations:
  - { system: "GOV.UK", look_at: "Ask users for… (address, name, date, email, phone, payment card); memorable dates" }
  - { system: "WHATWG/W3C", look_at: "autocomplete token list; WCAG 2.2 1.3.5 / 3.3.7" }
  - { system: "Google libaddressinput / libphonenumber", look_at: "i18n address schema; E.164" }
  - { system: "Stripe Elements / Braintree Hosted Fields", look_at: "payment-field UX + PCI SAQ A scope" }
  - { system: "Baymard Institute", look_at: "checkout layout findings" }
relations:
  composes: [text-field, select, combobox, checkbox, date-picker]
  relates-to: [forms-as-a-system, login-and-authentication, multi-step-wizard]
  boundary: >
    Forms-as-a-system (shell) owns timing/summary/focus/save and composes
    these recipes; the Date Picker component is deliberately NOT used for DOB;
    email/phone FOR AUTH live in the Login pattern; the general i18n/RTL POV is
    13-internationalization, referenced not re-derived; PCI mechanics are
    referenced via the hosted-fields provider, not re-derived.
notes:
  contested: "confirm-email re-type vs verification loop (contested in some commerce contexts); whether a name should ever split; expiry+CVC on one line (Baymard supports it) vs strict single-column for everything else"
  unverified: "which product design systems ship a NAMED address/payment recipe vs defer to the shell (GOV.UK is the clear corpus); specific Baymard figures; current version strings"
```

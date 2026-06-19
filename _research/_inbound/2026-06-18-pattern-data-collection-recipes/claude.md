*Claude pass — one of two dual-agent inputs for the Data-collection recipes pattern brief. A full draft against the patterns spine; to be synthesised with `external-agent.md` into `patterns/data-collection-recipes.md`.*

---

okf_version: "0.1"
type: pattern-brief
title: Data-collection recipes
description: The "Ask users for X" family — the per-datum field recipes that live inside the Forms-as-a-system shell. How to ask for a name, an address, a date of birth, a phone number, an email, and a payment card: the one-input-vs-many decision, the non-negotiable autocomplete-token contract, format tolerance and normalisation, the internationalisation shape of each datum, and proportionality. Composes Text Field/Select/Date Picker; borders Forms-as-a-system (the shell), the Date Picker component (the DOB recipe refuses it), the Login pattern, and 13-internationalization.
tags: [patterns, forms, data-collection, autocomplete, internationalization, accessibility]
tier: composition
goal: ask-for-data
status: draft
aliases: [Data-collection recipes, Ask users for, field recipes, input recipes]
last-audited: 2026-06-18
timestamp: 2026-06-18

---

# Data-collection recipes

> Forms-as-a-system owns *how a form behaves*; it knows nothing about *what it is asking for*. But the high-frequency datums every product collects — a name, an address, a date of birth, a phone number, an email, a payment card — each carry a settled, hard-won field shape: how many inputs they need, how they must be labelled, which `autocomplete` tokens make them autofillable, what formats to tolerate, and how they vary across the world. Get these wrong and the form thrashes no matter how good the shell is — a date picker for a birth year, a name split that erases half the planet's names, a country dropdown that rejects a valid address. This brief is the family of per-datum recipes that drop into the shell. It defers all orchestration to Forms-as-a-system and owns only the datum.

---

## Problem & context

A form is mostly the same six or seven things, asked over and over. The reason to brief them together is that they share a spine — an `autocomplete` contract, a tolerance-and-normalise discipline, an internationalisation posture, a one-input-vs-many decision — and that each has a *signature mistake* the field has already made and learned from. GOV.UK codified this as the "Ask users for…" family, and it is the most battle-tested form corpus in existence precisely because it serves the whole population, including the people every other system's defaults quietly exclude.

The pattern applies whenever a product collects standard personal or transactional data. It does **not** apply to bespoke domain fields (an invoice line, a medical code) — those get the generic shell treatment. The field diverges here not because designers disagree about taste but because the *world* is heterogeneous: names, addresses, phone formats, and date orders genuinely differ by locale, and most defaults are quietly built for one country. The recipes resolve that by treating the global case as the default, not the exception.

## Composition

Each recipe assembles briefed controls and adds only the datum-level shape; the orchestration is the shell's.

- **Text Field** (see text-field) — the workhorse for almost everything: name, address lines, the DOB day/month/year inputs, phone, email, card number/CVC. With the right `inputmode`, `type`, and `autocomplete`.
- **Select / Combobox** (see select, see combobox) — country (address, phone code), with the searchable-long-list caveat; *not* the default for things that look enumerable but aren't.
- **Date Picker** (see date-picker) — deliberately **not** used for date of birth; reserved for calendar/future dates. The DOB recipe is the explicit counter-example.
- **Button** (see button) — address-lookup trigger, "enter address manually" fallback.
- **The Forms-as-a-system shell** (see patterns/forms-as-a-system) — composes these recipes; owns validation timing, the error summary, focus, and save. This brief plugs into it.

**The delta this pattern adds** is per-datum: the input count and structure, the labels, the `autocomplete` tokens, the format tolerance, and the i18n shape — none of which any control or the shell can decide on its own.

## Decision rules

The cross-cutting spine first; the per-datum recipes follow in §6.

**1. One input vs many.** The most consequential recipe decision.
- `IF the datum is a memorable value the user knows by heart (date of birth)` → **multiple plain text inputs**, not a picker (GOV.UK day/month/year). A calendar to find a 1973 birthday is hostile.
- `IF the datum is a calendar/future date being chosen (booking, appointment)` → Date Picker (see date-picker).
- `IF a sub-part is independently useful (given name for greetings; address lines for shipping)` → structure it. `ELSE` → one field (full name).
- `IF the datum varies wildly by locale (address, name)` → fewer, more flexible inputs + country-driven shape, never a rigid Anglo template.
- Bias: **the fewest inputs that still parse and autofill.** Every extra input is a tab stop and a place to disagree with the user's reality.

**2. The `autocomplete` token contract — non-negotiable.** Every recipe names its tokens (`name`/`given-name`/`family-name`, `street-address`/`address-line1`/`postal-code`/`country`, `bday`, `tel`, `email`, `cc-number`/`cc-exp`/`cc-csc`). Correct tokens satisfy WCAG 2.2 §1.3.5 (Identify Input Purpose), let the browser/password-manager fill instantly, and reduce error rates measurably. `NEVER` ship a personal-data field without its token; `NEVER` use `autocomplete="off"` on standard data to "tidy" autofill (it's ignored where it matters and harms where it's honoured).

**3. Format tolerance & normalisation.** `ALWAYS` accept what the user types — spaces and dashes in card/phone numbers, any case, varied separators — and **normalise on input or submit**; `NEVER` reject a syntactically valid international value for not matching a domestic template. Validate *intent* leniently (does this look like an email/phone/card?), not *format* strictly. Strip, don't scold.

**4. Internationalisation posture.** The default assumption is **global users** unless the service is provably single-locale. Each datum varies (names that don't split, addresses with no postcode or no state, phone country codes, date orders, postal formats). Resolve the *per-datum* shape here; reference the general RTL/translation/locale POV to 13-internationalization rather than re-deriving it.

**5. Privacy & proportionality.** `IF you don't need a datum to deliver the service` → don't ask (the GOV.UK discipline). `IF you only need a derived fact` → ask for that, not the raw datum (an over-18 check is a yes/no or an age, not necessarily a full DOB). Fewer fields, less PII, lower abandonment, less to secure — and §3.3.7 Redundant Entry means never asking twice for what you already have this session.

## The recipes

Per-datum shape. Each: input count + structure, labels, `autocomplete`, validation/normalisation, i18n, signature anti-pattern.

| Datum | Inputs | `autocomplete` | Validate / normalise | i18n shape | Signature anti-pattern |
|---|---|---|---|---|---|
| **Name** | **One** "Full name" field by default | `name` (or `given-name`+`family-name` only if parts are independently needed) | Accept any characters, any length, Unicode; don't enforce "two words" | Many cultures have one name, multiple family names, or no given/family split; mononyms are valid | Splitting into First/Last (and worse, "Middle"); rejecting non-Latin or single-token names |
| **Address** | **Structured lines**, country-first | `country`, `address-line1/2`, `address-level2` (city), `address-level1` (state/region), `postal-code` | Postcode/state optional and country-driven; never require a state outside the US-shaped world | Country chosen first, then format adapts (libaddressinput); some have no postcode, no state | A fixed US/UK template for everyone; mandatory "State" dropdown globally; no manual fallback after lookup |
| **Date of birth** | **Three text inputs** D / M / Y | `bday` (with `bday-day/-month/-year` on the parts) | Accept 1 or 2-digit day/month; sensible year range; validate the composite, not each keystroke | Display order can vary, but separate labelled inputs sidestep the locale order trap | A **calendar Date Picker** (paging to 1965); a single free-text date; auto-advancing focus between parts |
| **Phone** | **One** international field | `tel` | Accept spaces, dashes, parens, `+`; normalise toward E.164; don't force a mask | One field + optional country selector; never assume domestic length/format | Separate area-code boxes; rejecting `+` or non-domestic lengths; a forced US `(___) ___-____` mask |
| **Email** | **One** field, `type="email"` `inputmode="email"` | `email` | Lenient syntactic check only; trim; lowercase the domain, not the local part | Internationalised addresses exist (Unicode local parts) — don't over-restrict | A **confirm-email re-type** field (use a verification link instead); aggressive regex that rejects valid addresses |
| **Payment card** | Number, expiry (MM/YY), security code | `cc-number`, `cc-exp` (or `cc-exp-month/-year`), `cc-csc`, `cc-name` | Accept spaces (auto-space in groups of 4); Luhn-check the number; expiry as MM/YY | Mostly universal; CSC length varies (Amex 4); name-on-card optional | Blocking spaces/paste; segmented 4×4 number boxes; rejecting valid lengths; demanding card "type" the user picks manually (detect it) |

## Accessibility orchestration

The a11y this brief owns (the error-summary/focus contract is the shell's):
- **Identify Input Purpose (WCAG 2.2 §1.3.5)** — the `autocomplete` token *is* the a11y feature: it exposes input purpose to AT and personalisation tools, not just autofill.
- **Compound-datum grouping** — wrap multi-input datums (DOB day/month/year, the address block) in `fieldset` + `legend` ("Date of birth"), so each input has both its own label *and* the group name; the day/month/year inputs each carry a real `<label>`, never a placeholder.
- **The multi-input labelling trap** — three unlabelled boxes are unusable to a screen-reader user; the composite error (an invalid date) attaches to the group, the individual format error to the part.
- **Input mode & keyboard** — `inputmode="numeric"` for card/CVC/DOB parts, `inputmode="email"`/`tel` where apt, so mobile keyboards match the datum.

## Content & copy

- **Labels** are the plain name of the datum ("Full name," "Date of birth," "Mobile number"), not jargon.
- **Hint text** carries the format *example*, not a rule ("For example, 31 3 1980"); persistent, before the inputs.
- **Say why** when asking for anything sensitive (DOB, phone) — a one-line reason raises completion and trust.
- **Honorific/title trap** — don't ask for a title (Mr/Mrs/Ms/Dr) unless you genuinely use it; it's a forced, often-wrong, sometimes-gendered choice.
- **Optional discipline** — mark per the shell's mark-the-minority rule; better to not ask.

## Variants & responsive

- **Address: lookup vs manual** — a postcode/address lookup as the fast path, with an always-available "enter address manually" fallback (lookup never the only route).
- **Payment: single number field with auto-spacing** (default) vs segmented (avoid).
- **Phone: one field** vs field + country-code selector (for international services).
- Multi-input rows (DOB day/month/year, card expiry) stay on one row but never wrap awkwardly; collapse gracefully on narrow screens.

## Anti-patterns

A Date Picker for date of birth. Splitting a name into First/Middle/Last (and requiring all three). Rejecting valid international names, addresses, or phone numbers for not matching a domestic template. A mandatory "State/Province" dropdown for the whole world. A 200-item country dropdown with no search, or defaulting to the wrong country. Confirm-email re-type fields. Blocking spaces or paste in card/phone fields. Segmented card-number boxes. `autocomplete="off"` on standard personal data. Asking for a full DOB when an age or over-18 check would do. Honorific dropdowns nobody uses.

## Related patterns & components

- **vs Forms-as-a-system** (see patterns/forms-as-a-system) — the shell owns validation *timing*, the error summary, focus management, and the save model; this brief owns the per-datum field *shape*. The shell composes these recipes; they never duplicate its orchestration.
- **vs the Date Picker component** (see date-picker) — the calendar control for chosen/future dates; the DOB recipe is the explicit case where the field-truth answer is *not* a date picker.
- **vs Login & authentication (pattern)** — email-and-password *for authentication* (sign-in, reset, MFA, the verification-link flow) lives there; this brief owns email and phone as *data capture*.
- **vs Foundations / 13-internationalization** — the general RTL/translation/locale POV is the numbered file; this brief references it and resolves only the per-datum i18n shape.
- **`composes`:** text-field, select, combobox, date-picker, button.

## Field POV evolution

Address entry shifted from long manual forms to **lookup-first with a manual fallback**. Phone capture consolidated from area-code-boxes to a **single international field** (libphonenumber/E.164 normalisation). The **`autocomplete` token contract went from nice-to-have to non-negotiable** once WCAG 2.2 §1.3.5 and measurable autofill-completion gains landed. And the baseline assumption moved from a **domestic default to an i18n-first default** — the "falsehoods programmers believe about names/addresses" literature did real work here, making the inclusive shape the professional default rather than an edge-case afterthought.

## Reference instantiations

Go look at: **GOV.UK** "Ask users for…" (addresses, names, dates, email, phone, payment card) and the memorable-date pattern — the reference corpus; the **HTML/WHATWG `autocomplete` token list** and **WCAG 2.2 §1.3.5**; **Google's libaddressinput** / the i18n address-format data; **libphonenumber** (E.164); **Stripe Elements** for payment-field UX.

## Sources cited

- GOV.UK Design System — "Ask users for…" patterns (addresses, names, dates, email addresses, phone numbers, payment card details, NINO), memorable dates, "Check your answers" (2025; *verify current version*).
- WHATWG HTML — the `autocomplete` autofill token list; WCAG 2.2 §1.3.5 Identify Input Purpose, §3.3.7 Redundant Entry.
- Google libaddressinput / i18n address format data — international address structure (*verify currency*).
- libphonenumber — E.164 parsing/normalisation.
- Baymard Institute — checkout address & payment-form research (*verify specific figures before quoting*).
- "Falsehoods programmers believe about names" (Patrick McKenzie, 2010) and "…about addresses" — the i18n-default lineage (*secondary, widely cited*).
- Stripe — Elements / payment-field UX guidance (*verify*).
- Design-system precedents (Carbon, Polaris, Material, Atlassian) for address/payment/name where documented (*spotty; flag where absent*).

`notes.unverified`: which design systems ship a *named* address/payment recipe vs leave it to the form shell (GOV.UK is the clear corpus; others are spottier — verify before asserting convergence). Specific Baymard completion figures. The confirm-email recommendation (verification link over re-type) is well-supported but contested in some commerce contexts — flagged.

## Agent-consumable schema

```yaml
identity:
  id: data-collection-recipes
  name: Data-collection recipes
  aliases: [Ask users for, field recipes, input recipes, personal-data fields]
  tier: composition
  goal: ask-for-data
  status: draft
problem: >
  The high-frequency datums (name, address, date of birth, phone, email,
  payment card) each carry a settled field shape — input count, autocomplete
  tokens, format tolerance, i18n form — that the generic form shell cannot
  decide. This brief is the family of per-datum recipes composed inside
  Forms-as-a-system; it defers all orchestration to the shell.
composition:
  requires: [text-field, select, combobox, date-picker, button]
  shell: forms-as-a-system
  delta: per-datum input count/structure, labels, autocomplete tokens, format tolerance/normalisation, i18n shape
decision_rules:
  one_vs_many:
    - { if: "memorable value known by heart (date of birth)", use: "multiple plain text inputs, NOT a date picker" }
    - { if: "calendar/future date being chosen", use: "Date Picker component" }
    - { if: "sub-part independently useful", use: "structure it; else single field" }
    - { if: "datum varies wildly by locale (address, name)", use: "fewest flexible inputs, country-driven shape" }
  autocomplete:
    - { if: "any standard personal-data field", use: "set the correct autocomplete token (WCAG 1.3.5)" }
    - { if: "tempted to use autocomplete=off to tidy autofill", use: "do not" }
  format_tolerance:
    - { if: "user types spaces/dashes/varied case/format", use: "accept and normalise on input/submit" }
    - { if: "value is a valid international form", use: "never reject for not matching a domestic template" }
  i18n:
    - { if: "service not provably single-locale", use: "assume global users; country-driven datum shape" }
  proportionality:
    - { if: "datum not needed to deliver the service", use: "do not ask" }
    - { if: "only a derived fact needed (e.g. over-18)", use: "ask for that, not the raw datum" }
recipes:
  name: { inputs: "one full-name field", autocomplete: "name (parts only if needed)", validate: "Unicode, any length, no two-word rule", i18n: "mononyms/multiple family names valid", anti_pattern: "First/Middle/Last split" }
  address: { inputs: "structured lines, country-first", autocomplete: "country, address-line1/2, address-level2/1, postal-code", validate: "postcode/state optional, country-driven", i18n: "format adapts to country (libaddressinput)", anti_pattern: "fixed US/UK template; mandatory global State" }
  date_of_birth: { inputs: "three text inputs D/M/Y", autocomplete: "bday (+ bday-day/-month/-year)", validate: "composite, lenient digits, sensible year range", i18n: "labelled parts sidestep order trap", anti_pattern: "calendar Date Picker" }
  phone: { inputs: "one international field", autocomplete: "tel", validate: "accept +/spaces/dashes, normalise to E.164", i18n: "no domestic length/format assumption", anti_pattern: "area-code boxes; forced US mask" }
  email: { inputs: "one field type=email inputmode=email", autocomplete: "email", validate: "lenient syntactic, trim, lowercase domain", i18n: "Unicode addresses exist", anti_pattern: "confirm-email re-type; over-strict regex" }
  payment_card: { inputs: "number, expiry MM/YY, security code", autocomplete: "cc-number, cc-exp(-month/-year), cc-csc, cc-name", validate: "accept spaces, Luhn, MM/YY", i18n: "CSC length varies (Amex 4)", anti_pattern: "segmented number boxes; block paste; manual card-type select" }
accessibility_orchestration: >
  autocomplete token = Identify Input Purpose (1.3.5); fieldset/legend around
  compound datums (DOB, address); real <label> per sub-input (never
  placeholder); composite error to the group, format error to the part;
  inputmode per datum.
content: >
  Plain-name labels; hint text as a format example not a rule; say why for
  sensitive data; avoid honorific/title fields; mark per the shell's
  mark-the-minority rule (better not to ask).
variants: [address-lookup-vs-manual, payment-single-vs-segmented, phone-with-country-selector]
anti_patterns:
  - date picker for date of birth
  - splitting names into First/Middle/Last
  - rejecting valid international names/addresses/phones
  - mandatory global State/Province dropdown
  - unsearchable 200-item country dropdown / wrong default
  - confirm-email re-type field
  - blocking spaces or paste in card/phone fields
  - segmented card-number boxes
  - autocomplete=off on standard personal data
  - asking full DOB when an age/over-18 check suffices
  - honorific/title dropdowns nobody uses
reference_instantiations:
  - { system: "GOV.UK", look_at: "Ask users for… (address, name, date, email, phone, payment card); memorable dates" }
  - { system: "WHATWG/W3C", look_at: "autocomplete token list; WCAG 2.2 1.3.5" }
  - { system: "Google libaddressinput", look_at: "i18n address format data" }
  - { system: "Stripe Elements", look_at: "payment-field UX" }
relations:
  composes: [text-field, select, combobox, date-picker, button]
  relates-to: [forms-as-a-system, login-and-authentication, multi-step-wizard]
  boundary: >
    Forms-as-a-system (shell) owns timing/summary/focus/save and composes
    these recipes; the Date Picker component is deliberately NOT used for DOB;
    email/password FOR AUTH lives in the Login pattern; the general i18n/RTL
    POV is 13-internationalization, referenced not re-derived.
notes:
  contested: "confirm-email re-type vs verification link (contested in some commerce contexts); whether name should ever split"
  unverified: "which design systems ship a NAMED address/payment recipe vs defer to the shell (GOV.UK is the clear corpus); specific Baymard figures; current version strings"
```

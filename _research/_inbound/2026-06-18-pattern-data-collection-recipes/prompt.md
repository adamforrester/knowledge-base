You are advising a senior design systems practitioner at a digital agency
who maintains a personal knowledge base of design-systems field-truth. The
knowledge base has a ~45-component catalogue and an opening PATTERNS layer
above it (tiers: composition / flow / layout-and-shell; each pattern carries
a GOV.UK-style `goal` facet). The first pattern brief, **Forms-as-a-system**,
is done — the orchestration SHELL (validation timing, error-summary + focus
contract, the save model, the long-form/wizard threshold).

This brief is its sibling: **Data-collection recipes** — the GOV.UK
"Ask users for X" family. Tier: `composition`. Goal: `ask-for-data`.

These are the per-DATUM field recipes that live INSIDE the form shell: how to
ask for the high-frequency data every product collects — **a name, an
address, a date of birth, a phone number, an email address, a payment card**
(and the transferable rules behind them). The single most important boundary:
this brief does NOT re-derive Forms-as-a-system. It does not own validation
timing, the error summary, focus management, or the save model — those are the
shell's. It owns the DATUM-level decisions the shell knows nothing about: how
many inputs a datum needs, how each field is grouped and labelled, the
`autocomplete` token contract, the format/normalisation/parsing rules, and
the internationalisation shape of each datum. Assume Forms-as-a-system, the
Form component, and the individual controls (Text Field, Select, Date Picker)
are briefed; cite the boundary, don't repeat them.

This is field-truth synthesis for someone who has shipped many forms. Explain
the non-obvious — where leading systems and the i18n reality genuinely
disagree, and the defensible default. Be opinionated and declarative.

=== WHAT TO SURVEY (the field) ===

Cite each with a version date; note the verification path for current claims.
- GOV.UK Design System — the "Ask users for…" patterns (addresses, names,
  dates, email addresses, phone numbers, payment card details, National
  Insurance number) and "Check your answers." The reference corpus.
- The `autocomplete` substrate — the HTML/WHATWG autofill token list and
  WCAG 2.2 §1.3.5 Identify Input Purpose (and §3.3.7 Redundant Entry). The
  spine that makes every recipe browser-autofillable.
- Address: the international-address problem — Google's libaddressinput /
  i18n address format data, address-lookup/autocomplete services, the
  "falsehoods programmers believe about addresses" lineage; Baymard's
  checkout-address research.
- Name: the "falsehoods programmers believe about names" lineage; the
  single-full-name vs given/family split; W3C personal-names guidance.
- Phone: E.164, libphonenumber, the single-international-field model.
- Date: the GOV.UK memorable-date (3 text inputs, NOT a calendar) vs the
  Date Picker (calendar) distinction; the DOB case specifically.
- Payment card: the number/expiry/security-code anatomy, the autocomplete
  tokens (cc-number/cc-exp/cc-csc), Stripe Elements / payment-field UX,
  Baymard's payment research, the one-field-with-auto-spacing vs segmented
  debate.
- Design-system precedents where they exist: Carbon, Polaris, Material,
  Atlassian, Spectrum patterns for address/payment/name where documented.

=== WHAT TO RESOLVE (decision rules are the deliverable) ===

Give cross-cutting rules first, then a per-datum recipe for each. Make rules
machine-resolvable (`IF condition → USE resolution`) wherever a real
threshold exists.

CROSS-CUTTING (the transferable spine):
1. **One input vs many** — when a datum is one free-text field vs structured
   multiple inputs (the date-of-birth-as-3-inputs vs date-picker decision;
   the full-name vs given/family decision; the single-address-textarea vs
   structured-lines decision). Give the deciding axes (memorability, parsing
   need, international variance, autofill).
2. **The `autocomplete` token contract** — every recipe must name its tokens;
   the cost of getting them wrong (autofill breaks). The non-negotiable.
3. **Format tolerance & normalisation** — accept what users type (spaces in
   card/phone, varied case/format), normalise on input/submit, never reject a
   valid international value; where validation should be lenient vs strict.
4. **Internationalisation posture** — the default assumption (your users are
   global unless proven otherwise); how each datum varies by locale; what to
   reference to 13-internationalization vs resolve here.
5. **Privacy & proportionality** — don't ask for what you don't need (the
   GOV.UK "only ask for X if…" discipline); the DOB-vs-age-checkbox kind of
   substitution; redundant-entry avoidance.

PER-DATUM RECIPES (resolve each: input count + structure, labels, the
autocomplete tokens, validation/normalisation, i18n shape, the anti-pattern):
- **Name** — full-name single field vs given/family; honorifics; the i18n trap.
- **Address** — structured lines, country-first ordering, address lookup,
  the international-format problem, manual-entry fallback.
- **Date of birth** — 3 text inputs (GOV.UK) vs date picker; why; the age
  alternative.
- **Phone number** — single international field; E.164; country code.
- **Email address** — single field; the confirm-email debate (re-type vs a
  verification link); inputmode/type.
- **Payment card** — number/expiry/CVC anatomy; segmented vs single+spacing;
  the autocomplete tokens; the security/PCI note (reference, don't re-derive).

=== THE BOUNDARIES TO HOLD (state in a Related section) ===

- **vs Forms-as-a-system** — the shell owns timing/summary/focus/save; this
  brief owns the per-datum field shape. The shell composes these recipes.
- **vs the Date Picker component** — the calendar control; the DOB recipe
  deliberately does NOT use it.
- **vs Login & authentication (pattern)** — email/password-for-auth specifics
  live there; this brief owns email/phone as data capture.
- **vs Foundations / 13-internationalization** — the general i18n/RTL POV is a
  numbered file; reference it, resolve only the per-datum shape here.

=== OUTPUT — follow this pattern-brief spine ===

Structured markdown. ALWAYS sections appear; SCALES appear when they carry
weight. Order = reading order.
1. **Frontmatter** — YAML: type: pattern-brief, title, description, tags,
   tier: composition, goal: ask-for-data, status, timestamp.
2. **`# Data-collection recipes` H1 + a one-paragraph blockquote** framing
   the problem and the boundary it holds (the per-datum recipes inside the
   shell).
3. **Problem & context** — why the high-frequency datums deserve a shared
   brief; when it applies; why the field/i18n reality diverges.
4. **Composition** — the components each recipe assembles as typed references
   (Text Field, Select, Date Picker…) and the relationship to the
   Forms-as-a-system shell. Don't re-derive them.
5. **Decision rules** — the cross-cutting spine (1–5 above) as machine-
   resolvable rules.
6. **The recipes** (SCALES, but the substance here) — a sub-section per datum
   (Name, Address, Date of birth, Phone, Email, Payment card): input count +
   structure, labels, `autocomplete` tokens, validation/normalisation, i18n
   shape, the datum's signature anti-pattern. A per-datum reference table is
   welcome.
7. **Accessibility orchestration** — the a11y this brief owns: the
   autocomplete/Identify-Input-Purpose contract, grouping compound datums
   with fieldset/legend, labelling multi-input datums (the day/month/year
   trap), input purpose for AT. (Defer the error-summary/focus contract to
   the shell.)
8. **Content & copy** (near-ALWAYS here) — label wording per datum, the hint
   text (format examples), why not to ask, the honorific/title trap.
9. **Variants & responsive** (SCALES) — segmented vs single, the address
   lookup-vs-manual variant, the responsive collapse of multi-input rows.
10. **Anti-patterns** — the recurring traps (date pickers for DOB, splitting
    names that don't split, rejecting valid international formats, dropdowns
    of 200 countries done badly, confirm-email re-type, disabling autofill,
    asking for data you don't need).
11. **Related patterns & components** — the four boundaries above, typed.
12. **Field POV evolution** (SCALES) — the shifts (address lookup over manual
    entry; the move to single international phone fields; autocomplete tokens
    becoming non-negotiable; the i18n-first default).
13. **Reference instantiations** (SCALES) — where to look (GOV.UK "Ask users
    for…", the autocomplete spec, libaddressinput).
14. **Sources cited** — with version dates; flag unsourced claims as
    unverified rather than inventing citations.
15. **Agent-consumable schema** — a fenced YAML block: identity (id, name,
    aliases, tier, goal, status), problem, composition (requires: [typed
    component ids]), decision_rules (as `{ if, use }`), recipes (a structured
    per-datum map: input_count, autocomplete, validation, i18n,
    anti_pattern), accessibility_orchestration, content, variants,
    anti_patterns, reference_instantiations, relations (composes / relates-to
    / boundary), notes (contested / unverified).

Synthesize; give frameworks where context (locale, audience) decides, defaults
where the field has genuinely converged. Date current-state claims. Flag what
you can't source.

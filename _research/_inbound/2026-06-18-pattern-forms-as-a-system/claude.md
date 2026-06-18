*Claude pass — one of two dual-agent inputs for the Forms-as-a-system pattern brief. A full draft against the patterns spine; to be synthesised with `external-agent.md` into `patterns/forms-as-a-system.md`.*

---

okf_version: "0.1"
type: pattern-brief
title: Forms-as-a-system
description: The multi-field form as a system — composition across controls, validation orchestration over fields and time, conditional field reveal, the save model, and the threshold at which a long form becomes a wizard. The Form component is the primitive; this pattern is the orchestration the Form brief forward-referenced.
tags: [patterns, forms, validation, accessibility, composition]
tier: composition
goal: ask-for-data
status: draft
timestamp: 2026-06-18

---

# Forms-as-a-system

> A single Form component renders a `<form>`, wires submit, and owns one field's validation. A *system* of fields is a different problem: how fields are grouped and sequenced, how validation is timed and surfaced across many fields at once, how one field's answer reveals or constrains another, how progress survives a closed tab, and the point at which a long scroll should have been a wizard. This brief owns that orchestration — the decisions no single control can make — and holds the line against the Form component below it and the multi-step wizard beside it.

---

## Problem & context

Every product collects structured input, and the hard part is never the input — it is the *coordination*. A text field knows whether it is empty; it does not know that it must not show its error until the user has finished, that its error must also appear in a summary at the top of the form, that submitting with errors should move focus to that summary, that it should reveal a second field when a particular option is chosen, or that the whole form should have been four pages. Those are system decisions, and the field where leading systems most visibly disagree.

The pattern applies whenever a form has **more than a couple of fields, cross-field logic, or a completion stake** — sign-up, checkout, application, settings, onboarding data capture. It does **not** apply to the single-input search box or the one-field inline edit (those are their own patterns), and it stops where a flow becomes genuinely sequential and branching (that is the multi-step wizard).

Systems diverge because they optimise for different failure modes. **GOV.UK** optimises for the highest-stakes, lowest-trust, assistive-tech-critical context (a citizen filing taxes once a year on a borrowed phone): server-authoritative validation, one question per page, an error summary as the backbone. **Product design systems** (Carbon, Atlassian, Material) optimise for repeat users in rich clients: inline, reactive validation; sectioned single-page forms; client-side schemas. Neither is wrong; the divergence *is* the decision space.

## Composition

Forms-as-a-system assembles briefed components and adds orchestration — it re-derives none of them.

- **Form** (`see form`) — the shell: the `<form>` element, submit handling, the single-form validation hook the component already owns. This pattern extends it to *many* fields.
- **The controls** — Text Field, Select, Checkbox, Radio Group, Date Picker, Combobox, Switch (`see` each). The pattern arranges and sequences them; their own labels, states, and a11y are inherited, not repeated.
- **Button** (`see button`) — the submit (primary) and any secondary/cancel. The submit's pending/disabled behaviour is a system decision (below).
- **Inline Message / field error text** (`see inline-message`) — the per-field error, plus the **error summary** the pattern introduces (no single control owns a cross-field summary).
- **Fieldset + legend** — grouping primitive for related fields (a radio/checkbox group, an address block); the heading structure of the whole form.
- **Banner / Toast** (`see banner`, `see toast`) — SCALES: the form-level success/failure result.

**The delta this pattern adds:** validation *coordination* across fields and time, the error-summary + focus contract, conditional field reveal, cross-field validation, the save model, and the long-form/wizard threshold. Everything below is that delta.

## Decision rules

The heart. Forks given as machine-resolvable rules where a real threshold exists, prose where it genuinely depends.

**1. Validation timing.** The field's most-litigated decision. The converged default is **"validate late, re-validate early"** (reward early, punish late): never error a field the user has not finished, but once a field is in error, re-check it on every change so the error clears the instant it is fixed.
- `IF progressive-enhancement / no-JS-must-work / high-stakes (gov, legal, finance)` → **validate on submit, server-authoritative**; show all errors at once via the summary. (GOV.UK model.)
- `IF rich client form` → **hybrid**: first validation for a field fires on **blur or submit** (not before first blur); after a field has errored, re-validate **on change**.
- `NEVER` validate a pristine field on every keystroke before its first blur (the thrash anti-pattern).
- `IF the field has objective, completable format feedback (password rules, username availability)` → live positive feedback on change is acceptable and helpful (the exception to "validate late").

**2. Error presentation.** Inline-per-field is non-negotiable; the question is whether to *add* a summary.
- `IF form > ~3 fields OR errors can scroll off-screen OR a11y-critical` → **error summary at top AND inline per field** (GOV.UK model). The summary is an in-page region (h2, `tabindex="-1"`), lists each error as a link that moves focus to the field.
- `IF short form (≤3 fields, all visible)` → **inline-only** is sufficient.
- **Focus on submit-with-errors:** `IF a summary exists` → move focus to the summary; `ELSE` → move focus to the **first invalid field**. Never leave focus on a disabled/static submit with errors below the fold.
- Each invalid field: `aria-invalid="true"` + error text linked via `aria-describedby`. Do **not** fire a live-region announcement per inline error (live-region budget) — the summary focus move carries the cross-field news.

**3. Required vs optional.**
- `IF most fields required` → **mark the optional ones** ("(optional)" in the label text, not colour). (GOV.UK / NN/g.)
- `IF most fields optional` → mark the required ones; if using an asterisk, **include a visible legend** and never rely on colour alone.
- Prefer reducing optional fields out of existence over marking them.

**4. The long-form / wizard / one-thing-per-page threshold.** Three shapes for the same data:
- **Sectioned single scroll** — `IF` the form is short-to-medium, fields are familiar, the user has all info to hand, and there is no branching (e.g. a checkout for a returning user).
- **One question per page** (GOV.UK) — `IF` the audience is broad/low-trust, branching is significant, error recovery matters, or it is mobile-first transactional. Higher page count, far lower cognitive load and abandonment.
- **Multi-step wizard** — `IF` there is a natural sequence, the user benefits from progress indication, and steps are grouped (3–6 steps). *This is the boundary to the wizard pattern — see Related.*
- Decision axes, not a single number: **field count** (>~7–10 invites splitting), **branching** (split), **abandonment/error stakes**, **info-to-hand**, **save/resume need**, **completion context** (one-handed mobile → split).

**5. Field dependency & conditional reveal.**
- `ALWAYS` reveal (insert into the DOM) rather than disable a dependent field — disabled controls are skipped by AT and give no reason.
- Place the revealed field **immediately after its trigger** in DOM and tab order; wire `aria-expanded`/`aria-controls` on the trigger.
- `IF the reveal is a single obvious next input` → move focus to it; `ELSE` → leave focus on the trigger and let tab reach it. Avoid aggressive auto-scroll.

**6. Cross-field validation.** Password-confirm, date ranges, "at least one of."
- Attach the error to the **dependent field** (confirm-password) or, for group rules ("at least one"), to the **fieldset/legend**.
- Fire on **blur of the dependent field** and on **submit** — not on change of the field it depends on (thrash).

**7. Save model.**
- `IF transactional (checkout, sign-up)` → **explicit submit**, no autosave.
- `IF document/settings-like editing` → **autosave** with a save-status indicator.
- `IF long, multi-session (applications, gov)` → **save-and-resume / draft**, with explicit "save and come back."
- `IF the form holds unsaved input` → a **dirty-state guard** (route/`beforeunload`). *Boundary: the full autosave + unsaved-changes machinery is its own pattern — here, resolve only the form-intrinsic part.*

**8. Submission states.**
- `NEVER` disable the submit button to *enforce* validation — it hides what is wrong and strands AT users. Let the form submit and surface errors.
- `DO` move the submit to a **pending/busy** state while the request is in flight (prevents double-submit; `aria-busy`, spinner-in-button).
- On failure: **preserve all input**, show the error summary. `NEVER` clear the form on error.
- On partial failure: keep the succeeded portion, surface only the failed bits.

## Flow & states

The form lifecycle as a state machine: **pristine** (untouched, no errors shown) → **editing** (per-field touched/dirty tracking) → **validating** (blur/submit triggers field or form validation) → **submitting** (request in flight, submit busy, inputs ideally locked) → **success** (confirmation / redirect) | **error** (summary + inline, focus moved, input preserved). The key invariant: error *visibility* lags input (validate late) but tracks correction (re-validate early). Field-level `touched` state is what gates "late."

## Layout & structure

- **Single column is the default**, and the evidence is strong (Baymard, NN/g): a single column completes faster and avoids the eye-zigzag and the ambiguous-next-field problem of multi-column.
- **Exception:** short, semantically-paired fields may share a row — first/last name, city/state/zip, card expiry MM/YY. Multi-column *forms* are an anti-pattern; multi-field *rows* are fine.
- **Labels top-aligned** by default — fastest scan, robust to long/i18n labels, responsive-safe. Left-aligned labels only for dense internal data-entry where vertical compression matters.
- **Group** related fields in `fieldset` + `legend`; give long forms **section headings** that establish the document outline.

## Accessibility orchestration

The cross-component a11y the *system* owns (each control's own a11y is inherited):
- **The error-summary focus contract** — on invalid submit, move focus to the summary (or first invalid field); the summary lists errors as links that focus the corresponding field. This is the single most important reason the form is briefed as a system.
- **`aria-describedby` wiring** from each input to its error and help text; `aria-invalid` on errored fields.
- **Status messages (WCAG 4.1.3)** — submit success/failure announced via a polite live region; the *live-region budget* spent on the summary/result, not on every inline error.
- **Structure** — `fieldset`/`legend` for groups, a heading hierarchy for sections, a logical tab order that matches visual order.
- **Dynamic insertion** — revealed/added fields land in tab order right after their trigger and are perceivable to AT (no focus traps, no orphaned controls).

## Content & copy

Near-ALWAYS load-bearing for this pattern.
- **Errors are specific and actionable** — "Enter a date in DD/MM/YYYY format," not "Invalid." Say what was wrong *and* what to do. Match the summary text to the inline text.
- **Labels** are persistent and visible; **never** the placeholder (placeholder-as-label is a hard anti-pattern). Placeholders are for format examples only.
- **Help text** before the input, not after; concise.
- **Required/optional wording** explicit in the label, not encoded only in colour.
- **Success copy** confirms what happened and the next step.

## Variants & responsive

- **Single-scroll** ↔ **sectioned** ↔ **one-per-page** ↔ **wizard** — the same data at four scopes; the threshold rules above choose.
- Responsive: multi-field rows collapse to single column; sticky submit on long mobile forms; consider one-per-page *because* of mobile, not despite it.

## Anti-patterns

Placeholder-as-label. Disabling the submit button to "enforce" validation (hides the errors, strands AT). On-keystroke validation before first blur (thrash). Clearing the form (or losing input) on error. Multi-column form layouts. Reset/clear buttons next to submit (accidental data loss; almost never wanted). Asterisk-only required marking with no legend. Encoding errors in colour alone. Aggressive auto-scroll/auto-focus on conditional reveal. Auto-advancing focus between fields (acceptable for a well-built OTP input, harmful for date parts). One giant page when the data branches.

## Related patterns & components

- **Form (component) vs Forms-as-a-system (pattern)** — the Form brief owns the `<form>` element, submit wiring, and single-field validation mechanics. This pattern owns multi-field orchestration: validation coordination, the summary, focus management, conditional reveal, the save model, the wizard threshold.
- **Forms-as-a-system vs Multi-step wizard (pattern)** — the flow sibling. When the data is sequential/branching and benefits from step progress, the system *becomes* a wizard (decision rule #4). The wizard pattern owns the step model, per-step vs end validation, and the wizard→accordion transform; this pattern owns the within-step form.
- **Forms-as-a-system vs the data-collection "Ask users for X" recipes** — this pattern is the orchestration *shell*; the per-datum recipes (address, name, date-of-birth, payment card) are a sibling `composition` pattern that resolves the field grouping/validation/copy for each specific datum. Compose them inside the shell; don't absorb them.
- **Foundations, not here** — the bare disabled/read-only state rules and theming are foundations guidance (numbered files), cited not re-derived.
- **`composes`:** form, text-field, select, checkbox, radio-group, date-picker, combobox, button, inline-message, banner.

## Field POV evolution

Three real arcs. **Disabled-submit fell out of favour** — once common, now widely rejected as an accessibility and feedback failure; let users submit and show errors. **Inline-only → summary + inline** — WCAG 3.3.x and GOV.UK's evidence pushed the error summary from a gov quirk to a mainstream best practice for non-trivial forms. **Schema-driven / headless forms** — React Hook Form (uncontrolled-by-default for performance), Zod/Yup resolvers, and TanStack Form moved validation from imperative handlers to declarative schemas, which is why the agent-consumable `decision_rules` here lean toward conditions a schema can encode.

## Reference instantiations

Go look at: **Carbon** Forms pattern (validation + inline error treatment); **GOV.UK** "Question pages," the **error summary** component, and "Check your answers" (the one-per-page + summary spine); **Atlassian** Forms pattern and `@atlaskit/form` (the field/validation API model); **Material 3** text-field + form guidance; **React Hook Form** docs (validation timing modes — `onSubmit`/`onBlur`/`onChange`/`onTouched` — and `reValidateMode`).

## Sources cited

- IBM Carbon — Forms pattern (v11, 2025). *Verify current at carbondesignsystem.com.*
- GOV.UK Design System — Question pages, Error summary, "Check your answers," one-thing-per-page (v5, 2025).
- Shopify Polaris — form layout + error messages pattern (2024–25).
- Material Design 3 — text fields / form guidance (2024–25).
- Atlassian Design System — Forms pattern + `@atlaskit/form` (2025).
- Mihael Konjević, "UX of form validation" / "reward early, punish late" (2018) — the validate-late/re-validate-early convention. *Secondary source; widely adopted.*
- Baymard Institute & NN/g — single-column form completion, label placement. *Verify specific figures before quoting.*
- WCAG 2.2 — 3.3.1/3.3.3/3.3.4 (error identification, suggestion, prevention), 4.1.3 (status messages); WAI-ARIA APG; HTML `autocomplete` tokens.
- React Hook Form — validation modes / `reValidateMode` (current docs). *Verify version.*

`notes.unverified`: specific Baymard/NN/g completion-rate figures; exact current version strings for each system. The decision-rule *shape* is well-attested; the numeric thresholds (field counts) are heuristics, not sourced constants — flagged as such.

## Agent-consumable schema

```yaml
identity:
  id: forms-as-a-system
  name: Forms-as-a-system
  aliases: [multi-field form, form system, form orchestration]
  tier: composition
  goal: ask-for-data
  status: draft
problem: >
  Coordinate a multi-field form — validation timing and surfacing across
  fields, conditional reveal, cross-field rules, save model, and the
  long-form/wizard threshold. Applies when a form has >2 fields, cross-field
  logic, or a completion stake; not for single-input search or inline edit.
composition:
  requires: [form, text-field, select, checkbox, radio-group, date-picker, combobox, button, inline-message, banner]
  delta: validation coordination, error summary, focus management, conditional reveal, save model, wizard threshold
decision_rules:
  validation_timing:
    - { if: "progressive-enhancement or high-stakes (gov/finance/legal)", use: "validate on submit, server-authoritative, error summary" }
    - { if: "rich client form", use: "hybrid: first validate on blur/submit; re-validate on change once errored" }
    - { if: "pristine field before first blur", use: "do NOT validate (avoid thrash)" }
    - { if: "objective completable feedback (password rules, availability)", use: "live positive feedback on change OK" }
  error_presentation:
    - { if: "form > ~3 fields or errors can scroll off-screen or a11y-critical", use: "error summary (focused on submit) + inline per field" }
    - { if: "short form <=3 visible fields", use: "inline only" }
    - { if: "invalid submit and summary exists", use: "focus the summary; else focus first invalid field" }
  required_optional:
    - { if: "most fields required", use: "mark the optional ones in label text" }
    - { if: "most fields optional", use: "mark required; asterisk needs a visible legend" }
  form_shape:
    - { if: "short/familiar, no branching, info to hand", use: "sectioned single scroll" }
    - { if: "broad audience, branching, error stakes, mobile transactional", use: "one question per page" }
    - { if: "natural sequence + progress benefit, 3-6 grouped steps", use: "multi-step wizard (boundary -> wizard pattern)" }
  conditional_reveal:
    - { if: "field depends on another's value", use: "reveal (insert) not disable; place after trigger; aria-expanded/controls" }
  save_model:
    - { if: "transactional", use: "explicit submit" }
    - { if: "document/settings editing", use: "autosave + status" }
    - { if: "long multi-session", use: "save-and-resume/draft" }
    - { if: "unsaved input present", use: "dirty-state guard" }
  submission:
    - { if: "always", use: "never disable submit to enforce validation; do show pending/busy in flight" }
    - { if: "submit fails", use: "preserve input, show summary, never clear form" }
accessibility_orchestration: >
  Error-summary focus contract (errors as links to fields); aria-describedby +
  aria-invalid wiring; WCAG 4.1.3 status announcement via polite live region
  (budget spent on summary/result, not per inline error); fieldset/legend +
  heading structure; logical tab order; revealed/added fields land in tab
  order after their trigger.
content: >
  Specific actionable errors (what was wrong + what to do; summary text
  matches inline); persistent visible labels (never placeholder-as-label);
  help text before input; explicit required/optional wording; success copy
  confirms + next step.
variants: [single-scroll, sectioned, one-per-page, wizard]
anti_patterns:
  - placeholder-as-label
  - disabled submit to enforce validation
  - on-keystroke validation before first blur
  - clearing/losing input on error
  - multi-column form layout
  - reset/clear button next to submit
  - asterisk-only required marking without legend
  - error encoded in colour alone
  - aggressive auto-scroll/focus on reveal
reference_instantiations:
  - { system: "GOV.UK", look_at: "Question pages, Error summary, Check your answers" }
  - { system: "IBM Carbon", look_at: "Forms pattern (validation + inline error)" }
  - { system: "Atlassian", look_at: "Forms pattern + @atlaskit/form" }
  - { system: "React Hook Form", look_at: "validation modes + reValidateMode" }
relations:
  composes: [form, text-field, select, checkbox, radio-group, date-picker, combobox, button, inline-message, banner]
  relates-to: [multi-step-wizard, data-collection-recipes, save-and-unsaved-changes, view-state-orchestration]
  boundary: >
    Form (component) owns the <form> element, submit wiring, single-field
    validation; this pattern owns multi-field orchestration. Becomes the
    multi-step wizard above the form-shape threshold. The per-datum field
    recipes (address/name/dob/payment) are the sibling data-collection
    pattern, composed inside, not absorbed.
notes:
  contested: "validation timing (submit-only vs hybrid); error summary always vs short-form exemption; required-vs-optional marking convention"
  unverified: "numeric field-count thresholds are heuristics not sourced constants; specific Baymard/NN-g figures; current version strings"
  secondary-tier: "flow (the form is a composition that shades into a flow as it lengthens)"
```

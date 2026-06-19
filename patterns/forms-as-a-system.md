---
okf_version: "0.1"
type: pattern-brief
title: Forms-as-a-system
description: The multi-field form as a system — the orchestration the Form component forward-referenced. A field-truth study of the validation-timing fork (reward early, punish late), the dual inline + error-summary model and its focus contract, the mark-the-minority required/optional rule, the long-form/sectioned/one-thing-per-page/wizard threshold, conditional field reveal, cross-field validation, the save model, single-column layout, repeatable fields, and the never-disable-submit submission contract — composing Form + every control + Button + Inline Message, holding the line against the Form component below it, the multi-step wizard beside it, the data-collection "Ask users for X" recipes it composes, and the state/token rules that belong in Foundations.
tags: [patterns, forms, validation, accessibility, composition]
tier: composition
goal: ask-for-data
status: stable
aliases: [Forms-as-a-system, form orchestration, multi-field form, form system, data-collection shell]
last-audited: 2026-06-18
timestamp: 2026-06-18
---

# Forms-as-a-system

> A single control is a vessel for one value; a Form component renders the `<form>`, wires submit, and orchestrates one field's validation. A *system* of fields is a different problem — the choreography of many values across time, state, and intent that no single input can govern: when validation fires, how errors aggregate and route focus, how one answer reveals or constrains another, how progress survives a closed tab, and the point at which a long scroll should have been a sequence of pages. This brief owns that orchestration. It holds the line against the Form component below it (see form), the multi-step wizard beside it (the sibling flow pattern), the data-collection recipes it composes ("Ask users for X"), and the state/token rules that live in Foundations.

---

## Problem & context

Treat a form as a vertical stack of self-contained inputs and it degrades predictably. One field validates on every keystroke and scolds the user before they have typed the `@`; the next stays silent until submit. A dependent field appears abruptly and the layout jumps, and the user loses their place. A screen-reader user submits, the page does nothing they can perceive, and they never learn why — because no one orchestrated the announcement at the level *above* the fields. Each control is doing its job correctly and the form is still broken, because the broken part was never a control's job. Cross-field dependency, error aggregation, focus routing, the global submission state, the structural announcement to assistive tech — these are system decisions, and they are where the leading systems most visibly disagree.

The pattern applies whenever a form has **more than a couple of fields, cross-field logic, or a completion stake** — sign-up, checkout, application, settings, onboarding capture. It does not apply to the single-input search box or the one-field inline edit (their own patterns), and it stops where a flow becomes genuinely sequential and branching — that is the multi-step wizard.

Systems diverge because they optimise for different failure modes. **GOV.UK** indexes on the broadest, lowest-trust, assistive-tech-critical audience — a citizen filing once a year on a borrowed phone — and lands on server-authoritative validation, one thing per page, and a verbose error summary as the backbone (GOV.UK Design System, 2025). **Enterprise systems** — IBM Carbon, Shopify Polaris, Atlassian — index on repeat expert users in dense rich clients and land on inline validation, sectioned layouts, and client-side schemas (Carbon v11, 2025; Atlassian, 2025). Neither is wrong; the divergence *is* the decision space, resolved below by audience and stakes rather than by taste.

## Composition

Forms-as-a-system assembles briefed components into a data-collection state machine and adds the logic that coordinates them. It re-derives none of them — each control's own anatomy, states, and a11y live in its brief and are inherited, not repeated.

- **Form** (see form) — the shell: the `<form>` element with `novalidate` (the field has converged on suppressing the browser's native validation bubbles in favour of a controlled UI — GOV.UK, Carbon), submit interception, and the single-form validation hook the component already owns. This pattern extends it across *many* fields.
- **The controls** — Text Field, Select, Checkbox, Radio Group, Date Picker, Combobox, Switch (see each). The system sequences and groups them; it decides *when and why* an invalid state is passed, not how the control renders it.
- **Button** (see button) — submit (primary) and secondary/cancel; the submit's pending/disabled behaviour is a system decision (below).
- **Inline Message** (see inline-message) — the per-field error, bound to its control, *and* the **error summary** the pattern introduces. Inline Message's own brief already splits field-error from form-summary; this pattern owns when the summary renders and where focus goes.
- **Fieldset + legend** — the grouping primitive for related fields and the heading structure of the whole form.
- **Banner / Toast** (see banner, see toast) — SCALES: the form-level success/failure result.

**The delta this pattern adds** is the substrate the controls cannot see: the validation engine and its timing, the error-summary and focus contract, conditional reveal, cross-field rules, the save model, and the threshold at which the form should stop being one form. Everything below is that delta.

## Decision rules

The heart. Forks given as machine-resolvable rules where a real threshold exists, prose where it genuinely depends. (The §16 block restates these for agents.)

**1. Validation timing** — the most-litigated decision, and the field has converged. The rule is **reward early, punish late** (Konjević, *UX of validation*, 2018; carried into React Hook Form's `mode`/`reValidateMode`, 2025): never validate a pristine field; fire the first check on **blur or submit** (punish late); once a field is in error, switch to **on-change** and clear it the instant the input becomes valid (reward early).
- `IF pristine field, before first blur` → do not validate (the thrash anti-pattern).
- `IF field touched, on blur` → validate.
- `IF field already errored, on change` → re-validate; clear on first valid keystroke.
- `IF high-stakes / progressive-enhancement / no-JS-must-work (gov, finance, legal)` → submit-only, server-authoritative; show all errors at once via the summary.
- `IF objective completable feedback (password rules, character count, availability)` → live on-change feedback is the helpful exception.

**2. Error presentation** — inline-per-field is non-negotiable; the question is whether to *add* a summary. The converged answer for non-trivial forms is **both** (GOV.UK; WCAG 2.2 §3.3.1/§3.3.3).
- `IF form > ~3 fields OR errors can scroll off-screen OR a11y-critical` → **inline per field AND an error summary** at the top, listing each error as a link to its field.
- `IF short form (≤3 visible fields)` → inline-only suffices.
- **Focus on invalid submit:** `IF a summary exists` → move focus to the summary; `ELSE` → focus the first invalid field. A summary link, when activated, moves focus to its field (and to the sub-target for a compound field).
- Each invalid field: `aria-invalid="true"` + error text linked by `aria-describedby`. Spend the live-region budget on the summary focus move, not on announcing every inline error.

**3. Required vs optional** — **mark the minority** (the scalable rule Carbon formalised; GOV.UK's evidence that users assume fields are required unless told otherwise).
- `IF most fields required` → mark only the optional ones, "(optional)" in the label text, not colour.
- `IF most fields optional` → mark only the required ones; if using an asterisk, include a visible legend and never rely on colour alone.
- Better still: delete optional fields rather than mark them.

**4. The long-form / sectioned / one-thing-per-page / wizard threshold** — four shapes for the same data; the axes decide, not a single number.
- **Sectioned single scroll** — `IF` short-to-medium, familiar, no branching, info to hand (the returning-user checkout).
- **One question per page** (GOV.UK) — `IF` broad/low-trust audience, branching, high error stakes, or mobile-first transactional.
- **Multi-step wizard** — `IF` a natural sequence the user benefits from seeing progress through, grouped into ~3–6 steps. *This is the boundary to the wizard pattern — see Related.*
- Axes: **field count** (a soft band around ~10–15 invites splitting — a heuristic, not a constant; see notes), **branching** (split, to avoid a reflowing page), **info-to-hand / external-document need** (split + save-and-resume), **completion context** (one-handed mobile → split), **abandonment stakes**.

**5. Field dependency & conditional reveal**
- `ALWAYS` reveal by mounting/unmounting, not by `disabled` or `display:none` — a disabled control gives no reason and falsely implies it could be enabled; an unmounted one is honest to AT.
- Insert the revealed field **immediately after its trigger** in the DOM so the next Tab lands on it naturally; wire `aria-expanded`/`aria-controls` on the trigger.
- `IF the reveal is a single obvious next input` → move focus to it; `ELSE` → leave focus on the trigger. Avoid aggressive auto-scroll.

**6. Cross-field validation** — lift the rule to the parent schema (password-confirm, date ranges, "at least one of").
- Attach the error to the **field being edited** that violates the rule; if it is holistic, hoist it to the **fieldset/legend**.
- `IF not all fields in the dependency graph are touched` → suppress (don't error "start date" because "end date" is empty).
- Fire on blur of the dependent field and on submit, never on change of the field it depends on.

**7. Save model**
- `IF transactional (checkout, sign-up)` → explicit submit, no autosave.
- `IF document/settings-like editing` → autosave with a save-status indicator.
- `IF long, multi-session (applications, gov)` → save-and-resume / draft (localStorage or API), with explicit "save and come back."
- `IF the form holds unsaved input AND navigation is attempted` → a dirty-state guard (route guard / `beforeunload`). *The full autosave + unsaved-changes machinery is its own pattern; resolve only the form-intrinsic part here.*

**8. Submission states**
- `NEVER` disable the submit button to *enforce* validation — it hides what is wrong and strands AT users hunting for a missed field. Let the form submit; clicking while invalid runs the holistic validation and routes to the summary.
- `DO` move the submit to a pending/busy state in flight (`aria-disabled`/`aria-busy`, spinner-in-button) to prevent double-submit.
- On failure: preserve all input, show the summary; never clear the form. On partial (server) failure: map server errors back to field paths, keep the succeeded portion, surface the failed bits.

## Flow & states

The lifecycle as a finite state machine; controls react to the macro state, they don't drive it. **Pristine** (mounted, defaults hydrated, no validation shown) → **Editing / dirty** (per-field touched tracking, `isDirty` set for the guard, errors clear on change per reward-early) → **Validating** (blur/submit runs the schema + cross-field graph) → **Submitting** (inputs frozen, navigation blocked, async request, submit shows busy) → **Success** (dirty cleared, route to confirmation / success banner) | **Error / partial failure** (summary rendered, focus moved, input preserved, server errors mapped to fields). The invariant: error *visibility* lags input (validate late) but tracks correction (re-validate early); the per-field `touched` flag is what gates "late."

## Layout & structure

- **Single column is the default**, and the evidence is strong (Baymard; NN/g): a single column completes faster and avoids the eye-zigzag and the ambiguous-next-field problem. Multi-column *forms* are an anti-pattern.
- **Exception:** short, semantically-paired fields may share a row — first/last name, city/state/zip, card expiry MM/YY. Multi-field *rows* are fine; they collapse to single column on narrow viewports.
- **Labels top-aligned** by default — fastest scan, robust to long/i18n labels, responsive-safe. Left-aligned labels only for dense internal data-entry where vertical space is at a premium.
- **Group** related fields in `fieldset`/`legend`; give long forms section headings that establish a real document outline. If a section outgrows the viewport, that is a signal to split (rule #4).
- **Action area** footer-aligned. Primary action placement is a system convention, not a universal: enterprise SaaS tends primary-right/secondary-left; GOV.UK puts the primary action first in reading order. Pick one per product and hold it.
- A note on spacing: the *rhythm* should be consistent and sectionable (e.g. Carbon's ~32px field / ~48px section gap on its 2x grid is one defensible scale), but the specific values are a token decision for the system, not a field-truth constant — see Foundations.

## Accessibility orchestration

The cross-component a11y the *system* owns; each control's own a11y is inherited.
- **The error-summary focus contract** — on invalid submit, move focus to the summary; the summary lists errors as links that focus the corresponding field. Moving focus *is* the announcement; the summary doubles as the failure landmark. This is the single most important reason the form is briefed as a system (GOV.UK error summary; WCAG 2.2 §3.3.1).
- **`aria-describedby` + `aria-invalid` wiring** from each input to its error and help text, generated with stable ids.
- **Status messages (WCAG 2.2 §4.1.3)** — submit success/failure via a polite live region; the budget is spent here and on the summary, not on per-field chatter.
- **Redundant Entry (WCAG 2.2 §3.3.7)** — never make the user re-enter information already given this session; provide autofill (`autocomplete` tokens — see the Form brief's autofill contract) or a "same as billing" affordance.
- **Allow paste** — do not block paste in password/credential fields; preventing it is an explicit WCAG failure (F109). Authentication that leans on a cognitive test without an accessible alternative fails §3.3.8/§3.3.9 — but resolve the auth specifics in the Login & authentication pattern, not here.
- **Structure & dynamic insertion** — `fieldset`/`legend` and a heading hierarchy for sections; a tab order matching visual order; revealed/added fields land in tab order right after their trigger and are announced via a polite live region so the changed topography is perceivable.

## Content & copy

Load-bearing here — in a form, words are interface, not prose.
- **Errors are specific, actionable, blame-free.** Not "You entered an invalid email" (blame), not "Invalid input" (useless) — "Enter an email address in the format name@example.com." Say what was wrong *and* what to do, and match the summary text to the inline text.
- **Labels** are persistent, visible, concise (1–3 words), no trailing colons, and never phrased as questions unless following GOV.UK's conversational one-thing-per-page. Never the placeholder (placeholder-as-label is a hard anti-pattern).
- **Help text** carries format constraints ("Must be at least 8 characters"), placed before the input and persistent.
- **Required/optional** wording explicit in the label, not encoded only in colour.
- **Success copy** confirms what happened and the next step.

## Variants & responsive

- **Single-scroll** ↔ **sectioned** ↔ **one-per-page** ↔ **wizard** — the same data at four scopes; rule #4 chooses. Multi-field rows collapse to single column; consider one-per-page *because* of mobile, not despite it.
- **Side panel / drawer** — denser; full-width takeover on mobile.
- **Dialog / modal form** — 3–5 inputs maximum, footer-anchored actions, never a nested scrollbar; if content would exceed the viewport, promote it to a full page rather than scroll inside the modal.
- **Wizard** — steppers degrade to a textual "Step 2 of 5" and full-width buttons on mobile (owned by the wizard pattern).

## Anti-patterns

Placeholder-as-label. Disabling the submit button to "enforce" validation (hides the errors, strands AT). On-keystroke validation before first blur (thrash). Clearing or losing input on error. Multi-column form layouts. Reset/clear buttons beside submit (accidental, catastrophic data loss; almost never wanted). Asterisk-only required marking with no legend. Errors encoded in colour alone. Disabling (rather than unmounting) irrelevant conditional fields. Aggressive auto-scroll/auto-focus on reveal. Blocking paste in password fields. One giant page when the data branches.

## Related patterns & components

- **Form (component) vs Forms-as-a-system (pattern)** — the Form brief (see form) owns the `<form>` element, `novalidate`, submit wiring, the field stack, and single-field validation mechanics. This pattern owns the multi-field state machine: validation timing across fields, the summary + focus contract, conditional reveal, cross-field rules, the save model, and the threshold.
- **Forms-as-a-system vs Multi-step wizard (pattern)** — the **flow** sibling, and a correction to the earlier framing that bundled the two: this pattern is single-view orchestration; when rule #4 trips (branching, or the ~10–15-field band, or external-document pauses) the form *graduates* into the wizard pattern, which owns step routing, inter-step persistence, and progress indication. The Form component still governs each step; this pattern governs a single-view form; the wizard governs the progression.
- **Forms-as-a-system vs the data-collection "Ask users for X" recipes** — this pattern is the orchestration *shell*; the per-datum recipes (address, name, date-of-birth, payment card — the "3 inputs vs 1" decisions) are a sibling `composition` pattern composed *inside* the shell, not absorbed.
- **Foundations, not here** — the visual styling of disabled/read-only/focus-visible states and the spacing/grid tokens belong in Foundations (see 03-component-library and the token POV); this pattern references *when* to apply them.
- **`composes`:** form, text-field, select, checkbox, radio-group, date-picker, combobox, button, inline-message, banner.

## Field POV evolution

Four real arcs. **Validation architecture** moved from imperative DOM/jQuery rules attached to inputs to **schema-driven** validation (Zod, Valibot) detached from the DOM and fed to a state manager — driven by isomorphic client/server reuse and type inference, and the reason this brief's decision rules lean toward conditions a schema can encode. **State management** moved from fully controlled inputs (re-rendering on every keystroke) to **uncontrolled, subscription-based** models (React Hook Form, TanStack Form) for performance on large forms. **Required marking** moved from the universal asterisk to **mark-the-minority**. And **disabled-submit fell out of favour** — once standard, now widely rejected as a feedback and accessibility failure. Alongside, **inline-only → summary + inline** as WCAG 3.3.x and GOV.UK's evidence made the error summary mainstream.

## Reference instantiations

Go look at: **GOV.UK** — Question pages, the Error summary component, and "Check your answers" (the one-per-page + summary spine, and the canonical accessible form). **IBM Carbon** — Forms pattern: fluid-vs-default layouts, top-aligned labels, the minority-marking rule. **Atlassian** — `@atlaskit/form` (the Header/Section/Footer model and the field/validation API). **Ant Design ProComponents** — `ProFormList` / `ProFormDependency` for repeatable, dependent field arrays. **React Hook Form** — the `mode`/`reValidateMode` timing modes and the Zod resolver.

## Sources cited

- GOV.UK Design System — Question pages, Error summary (focus management), "Check your answers," one-thing-per-page, turning off HTML5 validation (2025; release notes cited to v6.2.0, *verify*).
- IBM Carbon — Forms pattern, top-aligned labels, mark-the-minority, fluid-vs-default, 2x grid (v11, 2025; changelog cited to v11.109.0, *verify*).
- Shopify Polaris — form layout + error/validation alignment (2024–25; web-components/Preact migration noted, *verify version*).
- Atlassian Design System — Forms pattern + `@atlaskit/form` (Header/Section/Footer, character counters) (2025).
- Material Design 3 — form anatomy, error messages replacing helper text (2024–25).
- Microsoft Fluent / Design System QLD — avoid placeholders, column limits.
- React Hook Form — `mode`/`reValidateMode` timing, Zod resolver, uncontrolled/mobile performance, aria-invalid mapping (current docs, *verify version*); TanStack Form — headless, array fields, field dependencies.
- Ant Design ProComponents — ProForm, ProFormList, ProFormDependency.
- WCAG 2.2 — §3.3.1/§3.3.3 (error identification/suggestion), §3.3.7 (Redundant Entry), §3.3.8/§3.3.9 (Accessible Authentication), §4.1.3 (Status Messages), F109 (preventing paste); WAI-ARIA APG; the HTML `autocomplete` token substrate.
- Mihael Konjević, "UX of form validation" — "reward early, punish late" (2018; secondary, widely adopted).
- Baymard Institute & NN/g — single-column completion, label placement (*verify specific figures before quoting*).

`notes.unverified`: the field-count band (~10–15) is a heuristic, not a sourced constant — the axes (branching, info-to-hand, context) carry the decision; the two passes proposed different numbers (~7–10 vs ~15–20), which is itself the evidence it is contextual. Specific current version strings (GOV.UK v6.2.0, Carbon v11.109.0, Polaris 2026-04) and exact Baymard/NN-g figures are flagged for verification rather than asserted.

## Agent-consumable schema

```yaml
identity:
  id: forms-as-a-system
  name: Forms-as-a-system
  aliases: [form orchestration, multi-field form, form system, data-collection shell]
  tier: composition
  goal: ask-for-data
  status: stable
problem: >
  Coordinate a multi-field form — validation timing and surfacing across
  fields, conditional reveal, cross-field rules, the save model, and the
  long-form/wizard threshold — so a stack of correct controls does not add up
  to a broken, thrashing, inaccessible form. Applies when a form has >2
  fields, cross-field logic, or a completion stake; not for single-input
  search or inline edit.
composition:
  requires: [form, text-field, select, checkbox, radio-group, date-picker, combobox, button, inline-message, banner]
  delta: validation timing + engine, error-summary + focus contract, conditional reveal, cross-field rules, save model, the long-form/wizard threshold
decision_rules:
  validation_timing:
    - { if: "pristine field before first blur", use: "do NOT validate (avoid thrash)" }
    - { if: "field touched, on blur", use: "validate (punish late)" }
    - { if: "field already errored, on change", use: "re-validate; clear on first valid keystroke (reward early)" }
    - { if: "high-stakes or progressive-enhancement (gov/finance/legal)", use: "submit-only, server-authoritative" }
    - { if: "objective completable feedback (password rules, char count, availability)", use: "live on-change feedback OK" }
  error_presentation:
    - { if: "form > ~3 fields or errors can scroll off-screen or a11y-critical", use: "inline per field AND error summary at top" }
    - { if: "short form <=3 visible fields", use: "inline only" }
    - { if: "invalid submit and summary exists", use: "move focus to summary; else focus first invalid field" }
    - { if: "field invalid", use: "aria-invalid=true + aria-describedby to error id" }
  required_optional:
    - { if: "most fields required", use: "mark only optional ones, '(optional)' in label text" }
    - { if: "most fields optional", use: "mark required; asterisk needs a visible legend" }
  form_shape:
    - { if: "short/familiar, no branching, info to hand", use: "sectioned single scroll" }
    - { if: "broad/low-trust audience, branching, error stakes, mobile transactional", use: "one question per page" }
    - { if: "natural sequence + progress benefit, ~3-6 grouped steps, or field band ~10-15 / external-doc pause", use: "multi-step wizard (boundary -> wizard pattern)" }
  conditional_reveal:
    - { if: "field depends on another value", use: "mount/unmount (never disabled or display:none); insert after trigger; aria-expanded/controls" }
  cross_field_validation:
    - { if: "not all dependency-graph fields touched", use: "suppress" }
    - { if: "violation, attributable to edited field", use: "attach to that field; else hoist to fieldset/legend" }
  save_model:
    - { if: "transactional", use: "explicit submit" }
    - { if: "document/settings editing", use: "autosave + status" }
    - { if: "long multi-session", use: "save-and-resume/draft" }
    - { if: "unsaved input and navigation attempted", use: "dirty-state guard" }
  submission:
    - { if: "always", use: "never disable submit to enforce validation; click-while-invalid routes to summary" }
    - { if: "in flight", use: "pending/busy submit (aria-busy) to prevent double-submit" }
    - { if: "submit fails", use: "preserve input, show summary; map server errors to field paths; never clear form" }
  layout:
    - { if: "default", use: "single column, top-aligned labels" }
    - { if: "semantically-paired short fields (name, city/state/zip, MM/YY)", use: "multi-field row, collapses on narrow viewport" }
flow: [pristine, editing-dirty, validating, submitting, success, error-or-partial-failure]
accessibility_orchestration: >
  Error-summary focus contract (focus the summary on invalid submit; errors as
  links to fields; moving focus IS the announcement); aria-describedby +
  aria-invalid wiring; WCAG 2.2 4.1.3 status via polite live region; 3.3.7
  Redundant Entry (autofill / "same as"); allow paste in credential fields
  (F109); fieldset/legend + heading structure; logical tab order; revealed/
  added fields land in tab order after their trigger and are announced.
content: >
  Specific, actionable, blame-free errors ("Enter an email in the format
  name@example.com"; summary text matches inline); persistent visible labels
  1-3 words, no trailing colons, never placeholder-as-label; constraints in
  persistent help text; explicit required/optional wording; success copy
  confirms + next step.
variants: [single-scroll, sectioned, one-per-page, wizard, side-panel, dialog-modal]
anti_patterns:
  - placeholder-as-label
  - disabled submit to enforce validation
  - on-keystroke validation before first blur
  - clearing/losing input on error
  - multi-column form layout
  - reset/clear button next to submit
  - asterisk-only required marking without legend
  - error encoded in colour alone
  - disabling (not unmounting) irrelevant conditional fields
  - blocking paste in password fields
reference_instantiations:
  - { system: "GOV.UK", look_at: "Question pages, Error summary, Check your answers" }
  - { system: "IBM Carbon", look_at: "Forms pattern: fluid-vs-default, labels, mark-the-minority" }
  - { system: "Atlassian", look_at: "@atlaskit/form (Header/Section/Footer, validation API)" }
  - { system: "Ant Design ProComponents", look_at: "ProFormList / ProFormDependency" }
  - { system: "React Hook Form", look_at: "mode / reValidateMode + Zod resolver" }
relations:
  composes: [form, text-field, select, checkbox, radio-group, date-picker, combobox, button, inline-message, banner]
  relates-to: [multi-step-wizard, data-collection-recipes, save-and-unsaved-changes, view-state-orchestration]
  boundary: >
    Form (component) owns the <form> element, novalidate, submit wiring,
    single-field validation; this pattern owns multi-field orchestration on a
    single view; it graduates into the multi-step wizard (flow) above the
    form-shape threshold; the per-datum field recipes (address/name/dob/
    payment) are the sibling data-collection composition pattern, composed
    inside, not absorbed; state/token styling is Foundations.
notes:
  contested: "validation timing (submit-only vs hybrid); error summary always vs short-form exemption; asterisk vs (optional) — resolved by mark-the-minority; the field-count threshold number"
  unverified: "the ~10-15 field band is a heuristic not a constant (the two passes proposed ~7-10 vs ~15-20); current version strings (GOV.UK v6.2.0, Carbon v11.109.0, Polaris 2026-04); specific Baymard/NN-g figures"
  secondary-tier: "flow — the composition shades into a flow as it lengthens, until it graduates to the wizard"
```

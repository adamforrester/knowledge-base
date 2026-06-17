---
okf_version: "0.1"
type: component-brief
title: Inline Message
description: The third Feedback brief and the catalogue's first explicit cross-category interlock — the field/section contextual message that closes the live-region trio (Toast established, Banner refined, Inline Message applies to field association) and stitches Feedback to Form (the field-level case IS Text Field's helper/error slot, the primitive form controls compose). A field-truth study of the field-vs-section scope, the settled announcement model (aria-describedby + aria-invalid + focus management, NOT a field-level live region — the double-announce bug), reward-early/punish-late validation timing, the GOV.UK error-summary + visually-hidden Error: prefix + label-parity patterns, the helper↔error slot swap, the static-vs-dynamic refinement, and the reserve-space-vs-dynamic-expansion layout-shift model — with the practice's defaults.
tags: [components, feedback]
category: Feedback
status: stable
aliases: [inline-error, help-text, form-helper-text, error-message, field-error, validation-message, supporting-text]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Inline Message

> An Inline Message is the **atomic unit of contextual feedback** — a short message attached to a single control or scoped to a form section, communicating validation, requirement, or help *in place*. It is the third Feedback brief and the catalogue's **first explicit cross-category interlock**: it sits exactly where Feedback meets Form. The **field-level** inline message *is* the helper/error slot Text Field already established (wired to the control via `aria-describedby`, with `aria-invalid` on the field), so **Inline Message is the primitive that the form controls compose** — Text Field, Textarea, Select, Combobox, Checkbox/Radio group all render it in their message slot rather than re-deriving validation typography and a11y wiring. It inherits **Text Field** (the describedby/invalid chain + the helper↔error slot), the **live-region pattern + static-vs-dynamic refinement** from **Toast** and **Banner**, **Icon** (severity), and **Link** (error-summary/inline links). It closes the live-region trio (Toast *established*, Banner *refined*, Inline Message *applies to field association*) — and the one genuinely hard, recently-settled call is the **announcement model**: the field has converged on **`aria-describedby` + `aria-invalid` + focus management, and abandoned field-level live regions**, because a live region firing *plus* focus moving to the field is the **double-announcement bug**.

---

## 1. Framing

An Inline Message is strictly **contextual, state-bound, and tethered to the interactive surface it describes** — the physical manifestation of the system's evaluation of user input. It exists at two scopes:
- **Field-level** — bound to a single control, occupying its helper/error slot (tightly-coupled padding, matches input width, no background fill). **This is Text Field's message slot, and Inline Message is the primitive the controls compose** (passing state down via a Context API so every field's validation looks and announces identically).
- **Section-level** — scoped to a fieldset / group of fields / form section (lighter than a page Banner, fill-stripped; the Spectrum-`InlineAlert`/Banner-inline boundary), used for **cross-field/relational** errors ("End date can't precede start date" — don't blame one input).

It inherits **Text Field** (the `aria-describedby`/`aria-invalid` chain + the helper↔error slot — see text-field), the **live-region pattern + static-vs-dynamic** from **Toast/Banner** (see toast, banner), **Icon** (severity), **Link** (summary/inline links).

What it *isn't*: a **Banner** (standalone, dismissible, page/section, heavy fill — the inline message is state-bound and **never dismissible** — see banner), a **Toast** (transient, on a timer — *fundamentally incompatible with validation*, since it removes the context the user needs — see toast), or a bare **helper text** with no association (the inline message is the *associated, possibly-validated* version). Why systems disagree: the announcement model, validation timing, and the helper-vs-error naming.

## 2. Anatomy and parts
- **severity icon** (inherits Icon) — error/warning/success/info; **required for error/warning to satisfy WCAG 1.4.1** (the geometric indicator of failure, not decoration); `aria-hidden`; token-mapped to match the page Banner's icon for the same severity.
- **message text** — the helper/validation payload; one step down from body (12–14px); **wraps infinitely** (never truncates — truncating a constraint defeats the purpose).
- **the visually-hidden assistive prefix** — a screen-reader-only `<span class="visually-hidden">Error:</span>` injected before the text (GOV.UK), so AT announces the severity explicitly; **translatable** (§9).
- **optional links** (inherit Link) — an inline link to docs/policy, or (error summary) a link to the field.
- **the field-association wiring** — *not visible*: the message has an `id`; the **field** points `aria-describedby` at it + sets `aria-invalid` (the chain inherited from Text Field — §6/§11).
- **no dismiss** — it's a live reflection of form state; resolved only by correcting the input, never by a close button.

## 3. Properties / API
Two API topologies:
- **Declarative string-passing** (opinionated) — the parent control accepts raw strings (`invalidText` — Carbon; `errorMessage`/`description` — React Spectrum); the control instantiates the hidden Inline Message and **handles all id generation + ARIA binding internally** (guarantees compliance, low friction; limits rich content).
- **Composable slots** (headless/flexible) — the message is an explicit sub-component (`FormControl.Validation` — Primer; `FormHelperText error` — MUI); allows rich nodes/links, but **requires a Context API to secretly wire the message id to the input's `aria-describedby`** (else a developer mistypes the id and severs the a11y tree).
- **`severity` / `validationState`** — error / warning / success / info(helper) → toggles the colour tokens + swaps the icon (Fluent's `validationState`, Ant's `validateStatus`).
- **`message` / `children`** — text or rich node.
- **`id`** — must map 1:1 to the field's `aria-describedby` (usually wired by the field/`FormControl`, not typed by the consumer).
- the **live-region role** — per the static-vs-dynamic + the settled no-field-live-region default (§6).

## 4. States and variants
- **The helper↔error slot swap** — the dominant state transition: in a neutral state the slot shows **helper** ("Password must be 8+ characters"); on invalid, the helper is **unmounted and fully replaced** by the error ("Password is too short") — React Spectrum hides `description` from the DOM entirely when `validationState="invalid"` and an `errorMessage` is present (so the user isn't read redundant info). (Some systems coexist helper + error; replacement is the cleaner default.)
- **Variants:**
  - **severity:** error (dominant; danger token + alert icon; blocks submit; `aria-invalid`) / warning (caution; suboptimal, allows submit; no `aria-invalid`) / success (positive; async confirmation) / info(helper).
  - **scope:** field-level / section-level / **error summary** (form-level — §5/§6).
  - with-icon / text-only.
  - **static** (server-rendered at load) vs **dynamic** (client validation on blur/submit) — the announcement fork (§6).

## 5. Usage guidance
- **Field-level Inline Message** — validation/help attached to a control; the form control's message slot.
- **Section-level Inline Message** — a **cross-field/relational** error or a state scoped to a group ("End date can't precede start date" above the fieldset — don't put the blame on one input).
- **Error Summary** — at the top of a **long/complex/multi-section form** submitted with errors (§6).
- **Don't use an Inline Message for:** a standalone dismissible page/section announcement (→ **Banner**), a transient confirmation (→ **Toast** — and *never* validation in a Toast: it disappears, removing the context to fix the form), or feedback not tied to a field/section.
- **Validation timing — reward-early / punish-late (the central UX rule, Primer's framing):**
  - **Punish late:** while a field is **pristine or valid**, suspend validation until the user **leaves the field** (`onBlur`) or **submits** — *never* error a field the user hasn't finished or hasn't touched (eager on-focus/first-keystroke validation is hostile).
  - **Reward early:** once a field is **already in error**, switch to **eager `onChange`** so the error clears *the exact keystroke* the constraint is met — immediate positive feedback.
  - On-submit-only is the safe floor; **on-blur + re-validate-on-change** is the practice default.

## 6. Accessibility
This brief sits where Feedback's live-region pattern meets Form's field-association chain — and the **announcement model is the crux, recently settled**:

- **The three patterns:** (1) **`aria-describedby`** on the field → announced **when the field receives focus** (reliable, non-interruptive — the canonical association); (2) a **live region** (`role=alert`/`aria-live`) on the message → announced **when it appears** (but doesn't fire on focus); (3) **both** → the **Double-Announcement Bug**: on submit, JS injects the error into a live region *and* moves focus to the field, so the screen reader reads it **twice** (a race condition; documented on NVDA/JAWS and Android TalkBack).
- **The settled practice default (GOV.UK / GitHub Primer): drop the field-level live region; use `aria-describedby` + `aria-invalid="true"` + focus management.** On validation failure, update the DOM, set `aria-invalid`, and **programmatically move focus to the invalid field** (or the error summary) so the native `describedby` announces the error cleanly and once. Primer explicitly **"removes live region from FormControl validation."** (A field-level live region is justified *only* in the rare case where focus is **not** moved — e.g. Spectrum's Enter-on-empty-field WCAG-4.1.3 problem, which is the open friction, sometimes solved with a programmatic JS `LiveAnnouncer` rather than a static DOM live region.)
- **The static-vs-dynamic refinement (from Banner) applied to fields:** a **server-rendered error at load** is read in document order + via `describedby` on focus — no special wiring; a **client-inserted error** relies on focus-routing + `describedby` (not a live region). Same principle, field-scoped.
- **The error summary (GOV.UK) + focus management (WCAG 3.3.1):** on submit-with-errors, render a focusable summary at the top (`role="alert"` and/or `tabindex="-1"`), **move focus to the summary heading**, list each error as a **Link whose `href` targets the field id** (native focus routing to jump to the field). Per-field messages remain (the summary is additive). **Label parity:** the summary text and the inline text must be a **1:1 match**, and reuse the field's label terminology, or screen-reader users lose the mental map.
- **The visually-hidden "Error:" prefix** (GOV.UK) — prepended to the message so AT announces the severity even where the icon is ignored; translatable.
- **Color-not-sole-carrier (1.4.1)** — never a red border/text alone; the icon + text are mandatory. Text contrast ≥4.5:1; icon/border ≥3:1.
- **WCAG SCs:** **3.3.1 (Error Identification)**, **3.3.3 (Error Suggestion — how to fix)**, 4.1.3 (Status Messages — the summary/dynamic case), 1.4.1 (colour not alone), 3.3.2 (labels/instructions — helper), 1.4.3/1.4.11 (contrast), 1.3.1 / 4.1.2 (`aria-invalid`/`describedby`).

## 7. Content guidelines
- **Specific + actionable — what's wrong AND how to fix it** — "Enter a valid email address, like name@example.com" / "First name must be 35 characters or less", never "Invalid" / "An error occurred" / a raw exception code. State the constraint parameters (WCAG 3.3.3) to kill trial-and-error.
- **No blame, no hostility, plain language** — "Enter your first name", not "You forgot to enter your name"; never "illegal"/"forbidden"; no "Oops!"/humour (condescending in a failure moment).
- **Label parity (GOV.UK)** — reuse the label's exact terminology ("How many hours…?" → "Enter how many hours…"), and the inline text **must be identical to the error-summary text**.
- **Positive validation** sparingly (async confirmation like "Username available"); **helper text** states the requirement up front to prevent the error.

## 8. Motion and transition
The risk is **layout shift** — an injected message occupies vertical space. Two models: **Space Reservation** (a fixed `min-height` slot, zero shift, but sparse/disjointed empty forms) vs **Dynamic Expansion** (the container grows, pushing content down — the enterprise default for tight vertical rhythm; Carbon's 32px rhythm). Dynamic expansion needs **grouped-row lateral compensation**: in a two-column grid, if the left field's error expands it, the right column must grow to match so the horizontal axis stays aligned (Carbon). **Anti-pattern: `position: absolute`** on the message to dodge the shift — it overlaps the next field's label and breaks on small viewports. Animate insertion minimally (a short fade/slide), snapping instantly under `prefers-reduced-motion`. (See banner §8, 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **Text expansion up to ~300%** (German/Russian error strings) — the container **must wrap infinitely**, never `text-overflow: ellipsis` (hiding a constraint blocks the task); the layout-shift logic must handle 2–4-line messages on mobile.
- **RTL** — the severity icon flips from the leading to the trailing edge (and its margin offset) via **logical properties** (`margin-inline-start`); the message aligns with text direction.
- **The visually-hidden "Error:" prefix must be translatable** (GOV.UK overrides it per locale, e.g. "Gwall:" for Welsh) — a hardcoded English prefix before a localized message is a disjointed AT experience. (See 13-internationalization-and-rtl.)

## 10. Naming
Mostly *slot*/*attribute*-named, not a standalone component: **`InlineError`** (Polaris — error-only, which *conceptually limits* it), **`HelpText`** (Spectrum — neutral+error in one), **`FormHelperText`** + `error` (MUI), **`ErrorMessage`**/`HelperMessage` (Atlassian), **`validationMessage`**/`validationState` (Fluent), **`invalidText`** (Carbon), **supporting text** (Material). **The modern practice leans to generic structural naming** (`FormHelperText`/`FormControl.Validation`) precisely because of the helper↔error slot swap — the slot serves multiple severities, so an error-only name like `InlineError` forces a second component and fragments the ecosystem. **The practice default: `InlineMessage`** as the primitive (severity + icon + text + the association hooks), composed by the controls as their `HelperText`/`ErrorMessage` slot, with a separate **`ErrorSummary`** for the form-level pattern. Aliases to map: `InlineError`, `HelpText`, `FormHelperText`, `ErrorMessage`, `FieldError`, `ValidationMessage`, `SupportingText`.

## 11. Implementation notes
- **The field owns the association; the Inline Message is the rendered content.** A `FormControl`/`Field` wrapper generates a base id with **`useId()`** and orchestrates: `<label for="x">`, `<input id="x" aria-describedby="x-validation" aria-invalid>`, `<InlineMessage id="x-validation">`. In a composable API, a **Context/Provide-Inject** passes the id down so the consumer never hand-types/matches it (the #1 source of broken a11y trees).
- **The settled announcement wiring** — `aria-describedby` + `aria-invalid` + **focus management** (move focus to the invalid field / the error summary on failure); **no field-level live region** (it double-announces with focus). A programmatic `LiveAnnouncer` only for the focus-not-moved edge case.
- **Static vs dynamic** — server-rendered-at-load errors parse linearly (describedby on focus); client-inserted errors re-render the message, swap helper→error, and toggle `aria-invalid` together.
- **The error summary** — keep a registry of input refs; on `onSubmit` → `preventDefault()`, compute errors, render the summary, **imperatively `.focus()` the summary**, and map each summary anchor `href` to the input `id`.
- **Layout shift** — reserve space or dynamic-expand with grouped-row compensation; never `position:absolute` (§8).
- **Don't hand-roll the wiring** — React Aria / Radix / Base UI / Ark `Field`/`FormControl` generate the id/`describedby`/`invalid` correctly; the Inline Message slots in. Skin them.

## 12. Related and alternative components
- **Composed by:** Text Field, Textarea, Select, Combobox, Checkbox/Radio group — every form control renders the field-level Inline Message as its helper/error slot (the primitive; see text-field, textarea, select, combobox, checkbox, radio).
- **Stands on:** Text Field (the `aria-describedby`/`aria-invalid` chain + the helper↔error slot — see text-field), the live-region pattern + static-vs-dynamic from Toast/Banner (see toast, banner), Icon (severity — see icon), Link (summary/inline links — see link).
- **Alternative to / boundary with:** **Banner** (standalone, dismissible, page/section, heavy fill — state-bound + not-dismissible here; the section-level cases converge — see banner), **Toast** (transient — incompatible with validation — see toast), a bare **helper text** (unassociated).
- **Aggregated by:** the **Error Summary** (form-level) and the **Form** composite (see form when briefed).

(The third Feedback brief — the field/section contextual message that closes the live-region trio (Toast established, Banner refined, Inline Message applies to field association) and is the catalogue's first explicit cross-category interlock, stitching Feedback to Form: the field-level case is Text Field's error/helper slot, the primitive form controls compose. See text-field for the describedby/invalid chain, toast/banner for the live-region pattern + static-vs-dynamic, icon/link for the parts, form when briefed for the composite that aggregates it. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **Native HTML5 constraint bubbles → custom JS validation** — the unstyleable, inconsistent native popups fell out of enterprise use for custom inline text.
2. **The rise and fall of field-level live regions** — a11y advocates pushed `aria-live`/`role=alert` on field errors for dynamic announcement; in SPAs this collided with focus management and produced the **double-announcement bug** (NVDA/JAWS/TalkBack).
3. **The settled consensus — focus management + `aria-describedby`, no field-level live region** (GOV.UK, GitHub Primer) — `describedby` + `aria-invalid` + move-focus, with the **error summary** for the form level. The live region survives only at the form/summary level.
4. **Reward-early / punish-late** hardened as the validation-timing model (on-blur/submit, re-validate-on-change once in error, never error untouched).
5. **Inline Message recognised as the shared primitive fields compose** — and the move to generic structural naming (helper↔error slot) over error-only naming.

## 14. Sources cited
(Conservative; the external pass cited Primer React v36.x, Carbon v11.x, React Spectrum v3.x, Polaris v12.x, Fluent v9, Atlassian `@atlaskit/form` v7.x — held loosely and flagged unverified.) **GOV.UK Design System** — Error message + **Error summary** + the visually-hidden "Error:" prefix + label-parity (the canonical accessible form-validation pattern) (2024–2026); **GitHub Primer** — `FormControl.Validation`, the removal of field-level live regions, reward-early/punish-late (2024–2026); **IBM Carbon** — `invalidText`, the 32px rhythm + grouped-row layout-shift rules (2024–2026); **Adobe Spectrum / React Aria** — `HelpText`/`errorMessage`/`description` (the slot-swap-as-replacement), `InlineAlert`, the LiveAnnouncer debate (2024–2026); **MUI** — `FormHelperText` + `error` (2024–2026); **Microsoft Fluent** — `Field` `validationState`/`validationMessage` (2024–2026); **Atlassian** — `HelperMessage`/`ErrorMessage` (2024–2026); **Shopify Polaris** — `InlineError` (2024–2026); **Ant Design** — `Form.Item` `help`/`validateStatus` (2024–2026); **Google Material 3** — supporting/error text (the TalkBack double-announce note) (2024–2026); **WAI-ARIA APG** — no formal inline-message pattern (the `aria-describedby`/`aria-invalid` association + the Alert pattern + live regions); the inherited Text Field chain (see text-field) and the Feedback live-region pattern (see toast, banner). WCAG 2.2 (W3C Recommendation, Oct 2023) — 3.3.1, 3.3.3, 4.1.3, 1.4.1, 3.3.2, 1.4.3, 1.4.11, 1.3.1, 4.1.2.

## 15. Agent-consumable schema

```yaml
identity:
  id: inline-message
  name: Inline Message
  aliases: [inline-error, help-text, form-helper-text, error-message, field-error, validation-message, supporting-text]
  category: feedback
  status: stable
description: >
  The atomic contextual feedback unit — a short message attached to a control
  or scoped to a form section. The field-level case IS Text Field's helper/
  error slot, the PRIMITIVE form controls compose. Closes the live-region trio
  (Toast established, Banner refined, Inline Message applies to field
  association) + is the catalogue's first cross-category interlock (Feedback x
  Form). NOT a Banner (standalone/dismissible/heavy), NOT a Toast (transient —
  incompatible with validation), NOT a bare unassociated helper.
anatomy:
  parts:
    - "severity icon (inherits icon; REQUIRED for error/warning per 1.4.1; aria-hidden; token-matched to the Banner icon)"
    - "message text (helper/validation payload; 12-14px; WRAPS infinitely, never truncates)"
    - "visually-hidden 'Error:' prefix (GOV.UK; AT announces severity; TRANSLATABLE)"
    - "optional links (inherit link; docs / error-summary jump)"
    - "field-association wiring (NOT visible: message has id; the FIELD points aria-describedby + sets aria-invalid)"
    - "NO dismiss (state-bound; resolved by correcting the input)"
  scopes: "field-level (control's slot — the composed primitive) / section-level (cross-field/relational, fill-stripped) / form-level error summary"
api:
  inherits: [text-field (describedby/invalid chain + helper-error slot), "toast/banner (live-region pattern + static-vs-dynamic)", icon (severity), link (summary/inline links)]
  topologies:
    - "declarative string-passing (Carbon invalidText / Spectrum errorMessage) — control instantiates the hidden message + handles id/ARIA internally (compliant, low-friction, limits rich content)"
    - "composable slots (Primer FormControl.Validation / MUI FormHelperText) — explicit sub-component, rich nodes, but needs a Context API to wire id->aria-describedby"
  props:
    - {name: severity/validationState, type: enum, values: [error, warning, success, info], description: toggles tokens + swaps icon}
    - {name: message/children, type: "string | node"}
    - {name: id, type: string, description: "must map 1:1 to the field's aria-describedby (usually wired by the field, not the consumer)"}
states:
  slot-swap: "helper (neutral) is UNMOUNTED and fully REPLACED by error on invalid (Spectrum hides description when validationState=invalid + errorMessage present); some systems coexist — replacement is the cleaner default"
variants:
  severity: "error (danger + alert icon, blocks submit, aria-invalid) / warning (caution, allows submit, no aria-invalid) / success (positive, async confirm) / info(helper)"
  scope: [field-level, section-level, error-summary]
  rendering: "static (server-rendered at load) vs dynamic (client validation on blur/submit)"
accessibility:
  wcag-criteria: ["3.3.1", "3.3.3", "4.1.3", "1.4.1", "3.3.2", "1.4.3", "1.4.11", "1.3.1", "4.1.2"]
  announcement-model: "(1) aria-describedby = announced on FIELD FOCUS (canonical association, non-interruptive); (2) live region role=alert = announced on APPEARANCE (not on focus); (3) BOTH = the DOUBLE-ANNOUNCEMENT BUG (live region + focus-move reads it twice — NVDA/JAWS/TalkBack)"
  settled-default: "DROP the field-level live region; use aria-describedby + aria-invalid=true + FOCUS MANAGEMENT (move focus to the invalid field / the error summary so describedby announces once). Primer 'removes live region from FormControl validation'. A field-level live region (or a JS LiveAnnouncer) only when focus is NOT moved (Spectrum Enter-on-empty edge case)"
  static-vs-dynamic: "server-rendered-at-load = read in order + describedby on focus; client-inserted = focus-routing + describedby (not a live region)"
  error-summary: "GOV.UK — focusable summary at form top on submit-with-errors (role=alert/tabindex=-1), MOVE FOCUS TO IT, each error a Link href->field id; per-field messages kept (additive); LABEL PARITY — summary text == inline text == reuses the label terminology"
  prefix: "visually-hidden 'Error:' before the message (translatable)"
  color: "never colour alone (1.4.1) — icon + text mandatory; text >=4.5:1, icon/border >=3:1"
content:
  specific-actionable: "what's wrong AND how to fix ('Enter a valid email, like name@example.com'); state the constraint; never 'Invalid'/'Error'/exception codes (3.3.3)"
  tone: "no blame ('Enter your first name' not 'You forgot...'); no 'illegal'/'forbidden'; no humour/'Oops!'"
  label-parity: "reuse the label's terminology; inline text == error-summary text (1:1)"
  positive: "success validation sparingly; helper states the requirement up front"
motion:
  layout-shift: "Space Reservation (fixed min-height, zero shift, sparse) vs Dynamic Expansion (grows + pushes content — enterprise default, Carbon 32px rhythm) with GROUPED-ROW lateral compensation (two-column: if left expands, right grows to match)"
  anti-pattern: "position:absolute on the message to dodge shift -> overlaps the next label, breaks on mobile"
  reduce-motion: "snap; minimal fade/slide otherwise"
i18n:
  expansion: "up to ~300% (de/ru) — WRAP infinitely, NEVER text-overflow:ellipsis (hiding a constraint blocks the task); handle 2-4 lines on mobile"
  rtl: "icon flips leading->trailing edge + margin via logical properties (margin-inline-start)"
  prefix-translatable: "the visually-hidden 'Error:' must be localized (GOV.UK 'Gwall:' for Welsh), not hardcoded English"
implementation:
  - "the FIELD owns the association; Inline Message is the rendered content — FormControl/Field generates a base id with useId(): label for=x, input id=x aria-describedby=x-validation aria-invalid, InlineMessage id=x-validation; composable API uses Context/Provide-Inject to pass the id (no hand-typed matching)"
  - "settled wiring: aria-describedby + aria-invalid + FOCUS MANAGEMENT, NO field-level live region (double-announce); LiveAnnouncer only for focus-not-moved edge"
  - "static vs dynamic: server-at-load parses linearly; client-inserted re-renders + swaps helper->error + toggles aria-invalid together"
  - "error summary: input-ref registry; onSubmit -> preventDefault, render summary, imperatively .focus() it, anchor href -> input id"
  - "layout shift: reserve space or dynamic-expand + grouped-row compensation; NEVER position:absolute"
  - "don't hand-roll — React Aria/Radix/Base UI/Ark Field/FormControl generate id/describedby/invalid; Inline Message slots in"
composition:
  composed-by: [text-field, textarea, select, combobox, checkbox-group, radio-group]
  stands-on: [text-field (describedby/invalid chain + helper-error slot), "toast/banner (live-region pattern + static-vs-dynamic)", icon (severity), link (summary/inline links)]
  alternative-to: [banner (standalone/dismissible/heavy — section-level converges), toast (transient — incompatible with validation), bare-helper (unassociated)]
  aggregated-by: [error-summary (form-level), form (composite)]
notes:
  contested:
    - "the announcement model (settled: describedby + focus management, NO field-level live region; the double-announce bug killed the live-region approach)"
    - "validation timing (reward-early/punish-late — on-blur/submit, re-validate-on-change once in error)"
    - "helper+error coexist vs replace (Spectrum replaces — the cleaner default)"
    - "generic-structural naming (FormHelperText) vs error-only (InlineError)"
  trap:
    - "field-level live region + focus-move = DOUBLE-ANNOUNCEMENT BUG"
    - "erroring untouched/mid-typing fields (eager validation)"
    - "missing aria-invalid; mistyped describedby id (severed a11y tree)"
    - "position:absolute message (overlaps the next label); truncating an error (text-overflow:ellipsis)"
    - "colour-only error (red border, no icon/text); summary text != inline text (lost mental map)"
  inherited: "Text Field describedby/invalid chain + helper-error slot; Toast/Banner live-region pattern + static-vs-dynamic; Icon severity; Link summary links"
  role-in-family: "the third Feedback brief — closes the live-region trio (Toast established, Banner refined, Inline Message applies to field association) + the catalogue's first cross-category interlock (Feedback x Form: the field-level case IS Text Field's slot, the primitive fields compose)"
  evolution: "native constraint bubbles -> custom JS; rise+fall of field-level live regions (double-announce); settled on describedby + focus management + error summary (GOV.UK/Primer); reward-early/punish-late; recognised as the shared primitive + generic-structural naming"
  unverified:
    - "external 2026 version numbers"
    - "the describedby-vs-live-region + double-announce AT specifics — verify against current screen readers (NVDA/JAWS/VoiceOver/TalkBack)"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-inline-message/` (16 June 2026), the third Feedback brief and the catalogue's first explicit cross-category interlock — the field/section contextual message that closes the live-region trio (Toast established, Banner refined, Inline Message applies to field association) and stitches Feedback to Form (the field-level case is Text Field's helper/error slot, the primitive form controls compose). It stands on Text Field (the `aria-describedby`/`aria-invalid` chain + the helper↔error slot), Toast/Banner (the live-region pattern + static-vs-dynamic), Icon (severity), and Link (summary/inline links). The two passes converged almost completely — the field-vs-section scope and the fields-compose-the-primitive relationship, the validation-timing model (reward-early/punish-late: on-blur/submit, re-validate-on-change once in error, never error untouched), the GOV.UK error-summary + focus-on-submit + label-parity patterns, the severity + helper↔error slot-swap model, the static-vs-dynamic refinement, the layout-shift consideration, and the Banner/Toast/bare-helper boundaries. The decisive reconciliation was the **announcement model**: the external pass sharpened the practice default from a hedge to the settled field consensus — **`aria-describedby` + `aria-invalid` + focus management, with field-level live regions abandoned** because a live region firing plus focus moving is the double-announcement bug (GitHub Primer "removes live region from FormControl validation"; GOV.UK's focus-the-summary pattern), the live region surviving only at the form/summary level or the focus-not-moved edge (Spectrum's LiveAnnouncer debate). External-pass contributions folded in: the visually-hidden "Error:" prefix (translatable), label parity (inline text == summary text, reuse the label), the slot-swap-as-full-replacement (Spectrum hides `description` when invalid), the Space-Reservation-vs-Dynamic-Expansion layout model + grouped-row compensation + the `position:absolute` anti-pattern, the declarative-string-vs-composable-slot API topologies + the Context-wires-the-id requirement, `useId()` orchestration, the ~300% text-expansion/never-truncate rule, and the cross-field-error→section-message example. Claude-pass contributions: the framing as the live-region-trio closer and the first cross-category interlock, and the substrate map. The 2026 version numbers and the describedby-vs-live-region AT specifics are flagged unverified. Conformant to `components/_schema.md`. The third Feedback brief; Progress and Empty State remain.*

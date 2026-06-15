---
okf_version: "0.1"
type: component-brief
title: Checkbox
description: The catalogue's decomposition calibration — the same control at three granularities (atomic box, labelled row, group). A field-truth study that resolves the decomposition (a two-component surface — Checkbox + CheckboxGroup — plus an exposed atomic primitive), the indeterminate-as-DOM-property mechanic, the whole-row hit target, the Tab-each-vs-arrow-within difference from radio, and the checkbox-vs-switch boundary, with the practice's defaults. Establishes the selection-control decomposition that Radio and Switch refine.
tags: [components, form]
category: Form
status: stable
aliases: [check, tickbox, checkbox-field, checkbox-list, choice-list, multiselect]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Checkbox

> Checkbox looks atomic and isn't — and that is exactly why it is here. The same control appears at three granularities (the bare box, the labelled row, the group), and the catalogue's headline job in this brief is to decide how many components that becomes and where each boundary sits. Both research passes landed independently on the same answer, which is the answer the practice adopts: **two components — `Checkbox` and `CheckboxGroup` — plus the atomic box exposed as a primitive**, the same bundled-vs-composed hybrid the Text Field brief settled, applied to a control instead of a field. This brief is the decomposition calibration, and the pattern it sets carries straight to Radio and Switch.

---

## 1. Framing

A Checkbox is a control for an **independent binary choice that is *staged* into a form and submitted** — on/off, included/excluded, agreed/not — optionally one of many in a set. Its conceptual simplicity (a Boolean) hides where the real complexity lives: the associative contracts with its label, description, group, and sibling controls, and the **decomposition** those force (§2).

What it *isn't*: an **immediate-effect** toggle — that is a Switch, and the boundary is execution latency (§5); a **mutually-exclusive** one-of-many — that is Radio; or an **action with pressed state** — that is a ToggleButton (`aria-pressed`). The tell for Checkbox over Switch: the change takes effect on *save/submit*, not instantly; both agents frame this as deferred-vs-immediate intent, and conflating them makes users unsure whether their click already mutated live state. Only Checkbox has the **indeterminate** third visual state (§4).

Why systems disagree: almost entirely on **decomposition** and on whether the group is a first-class component or a layout convention — which is what §2 resolves.

## 2. Anatomy and parts — the decomposition

Three real tiers exist in the field (both agents enumerate them identically):

1. **Atomic control** — the box + check/indeterminate glyph, no label, no padding; the `<input type="checkbox">` (or a `role="checkbox"` custom control) that is the accessibility target.
2. **Labelled row / field** — control + adjacent label + optional description + optional inline error, as one clickable line whose *entire* spatial extent is the hit target.
3. **Group** — multiple rows under a shared label, a layout axis (vertical/horizontal), and group-level required/validation/error.

The field splits into three paradigms (the external pass's taxonomy):

- **Monolithic** (Carbon, Atlassian) — atomic + row fused into one `Checkbox` (label as a prop), plus a separate `CheckboxGroup` (often a `fieldset`). Consistent, but resists embedding a bare box in a custom layout.
- **Highly composed** (Primer, Fluent v9) — an atomic `Checkbox` plus a generic `FormControl`/slots wrapper (`FormControl.Label`, `FormControl.Caption`) that assembles the row.
- **Hybrid / headless** (Spectrum/React Aria, Base Web) — a `Checkbox` that *is* the row, backed by extracted hooks (`useCheckbox`, `useCheckboxGroup`) or overrides that let you detach the atomic control.

**The practice's resolution — and both passes converged on it:** a **two-component public surface plus an exposed atomic primitive.**

- **`Checkbox` is the labelled row** — control + label + optional description, the component engineers reach for in ~90% of cases. It owns the control-to-label alignment, the whole-row hit target, and its description slot.
- **`CheckboxGroup` is distinct** — it owns the shared group label, the **value array**, group-level required/validation/error, and the layout axis. Critically, *the group owns validation, not the rows* — an individual checkbox inside a group never manages its own `required`/error; that establishes the correct semantic boundary for assistive tech (both agents).
- **`Checkbox.Control` is the exposed atomic primitive** — for the layout edge cases where the label is decoupled (a select-all in a dense table's first column, a card-select where the card is the accessible name). It accepts group context and forwards the ref, but injects no layout CSS.

This is the **same encapsulation hybrid the Text Field brief settled** (bundled props for the common case, composed slots for the exceptions — see text-field §3), applied here to a control. It folds the atomic+row tiers into one polymorphic `Checkbox` and keeps the group separate, rather than shipping three co-equal top-level components — because the atomic-only case is the exception, not the rule. **This decomposition is the pattern; Radio and Switch refine it** (Radio's group is *mandatory*; Switch usually has *no* group — §12).

**Nesting the atomic control — the two-component surface is a convenience layer, not a closed system.** `Checkbox` and `CheckboxGroup` are the standalone-form ergonomics; underneath, **`Checkbox.Control` is the nestable unit** you drop into any host — a list row, a table cell, a menu item, a selectable card — and this is the load-bearing reason the atomic primitive is exposed rather than buried. When the control is nested, responsibilities redistribute to the host: (1) **the host provides the accessible name** — the row's own text names the control via `aria-labelledby`, so you never double-label; (2) **the host owns the hit target** — the whole row toggles, *unless* the row carries its own primary action (it navigates), in which case the control is a distinct secondary affordance with its own name (`aria-label="Select <item>"`) and the row's action stays separately reachable; (3) **the enclosing collection owns the selection state and group semantics** — a selectable List/Table/Menu plays the `CheckboxGroup` role at the collection level (the selected-ids array, select-all, `role=group`/grid-selection), so **you do not nest a `CheckboxGroup` inside a List** — the collection *is* the group (React Aria's `GridList`/`Table` with `selectionMode="multiple"` is the canonical example: rows carry checkboxes, the collection owns selection). The same mechanism lets one list mix control types — each row hosts the appropriate `*.Control` (`Checkbox.Control` / `Radio.Control` / `Switch.Control`) — provided **the selection semantics match the control type** (multi-select collection → checkbox; per-row independent immediate toggle → switch, no group; single-select collection → radio, and the collection *is* the radiogroup). The one trap to avoid is the **ambiguous nested interactive** — a control inside a row that is itself a button/link with no clear model of which the click hits; resolve it to either "the whole row is one control" or "the control is a named secondary affordance."

Named parts: control (box + check/indeterminate glyph + focus ring), label, description, inline error; and at the group: group label, group description, group error, layout container.

## 3. Properties / API

Inherits the generic form-field substrate (`error`, `description`/helper, describedby wiring — see text-field §3); the Checkbox label model differs (beside the control, doubling as hit target, and — the refinement below — rich-content-capable). **API naming follows native DOM**, not framework idiom: `checked`/`indeterminate`/`disabled`, not `isChecked`/`isIndeterminate` (both agents; Atlassian's `is*` and React Aria's `isSelected` are recorded as aliases).

**`Checkbox` (the row):**
- `checked` + `defaultChecked` / `onChange` — controlled/uncontrolled binary (the change exposes both the event and the resulting boolean).
- `indeterminate` — the mixed visual state (a *presentational* flag, not a third value — §4, §11).
- **`label` accepts rich content (a node / children), not a string only** — this is the one place my initial pass was refined by the external pass: a string-only label breaks the single most common real label, the **consent line with an embedded link** ("I agree to the *Terms of Service*"). The label is part of the accessible name and the hit target; omit it only for the bare `Checkbox.Control` (then an external `aria-label`/`aria-labelledby` is required).
- `description` — optional helper under the label, describedby-wired.
- `value` — the string submitted when checked; an element of a group's array.
- `name`, `disabled`, `isReadOnly` (with the native-readonly caveat, §4).

**`CheckboxGroup` (the set):**
- `label` — the shared group label (the group's accessible name).
- `value` / `defaultValue` / `onChange` — the **array** of selected child values; the group owns this state.
- `required`, `isInvalid`/`errorMessage`, `description` — **group-level** validation, announced once for the set.
- `orientation` — `vertical` (default) / `horizontal`.

The load-bearing rule: **selection state lives at the tier that owns it.** A standalone `Checkbox` owns its boolean; inside a `CheckboxGroup` the group owns the array and children read from group context (§11). Don't make consumers wire both.

## 4. States and variants

Runtime states: rest, hover, focus-visible, pressed, **checked / unchecked**, **indeterminate**, disabled, read-only, error.

| State | Checkbox-specific contract |
| --- | --- |
| checked / unchecked | the binary; checkmark glyph on checked, high-contrast border at rest to delineate the box |
| indeterminate | a **third visual state, not a third value** — dash glyph, `aria-checked="mixed"`; the underlying value is still true/false. Set via the DOM `.indeterminate` property (§11). For parent/child select-all hierarchy only — never a user-clickable third state. |
| focus-visible | ring on the **control**, offset, ≥3:1 (1.4.11/2.4.13); appears for keyboard traversal, not mouse/touch |
| error | isolated row: border shifts to the error token; in a group: rows stay neutral and the **group** shows the error (§3) |
| read-only | **the awkward one** — native `<input type=checkbox>` has no working `readonly` (only `disabled`), so a true read-only checkbox needs `aria-readonly` + prevented toggling, or is better rendered as static text (flag, like select's no-native-readonly) |
| pressed | brief active feedback, mainly mobile/touch-down |

**Intentional variants:** `size` (control scales with the type); **alignment** — **top/baseline alignment is the non-negotiable default**, not center: center-aligning the control to a multi-line label floats it mid-paragraph and breaks the scan line; top-anchoring keeps it at the first line's reading start regardless of wrap (both agents emphatic). Group **orientation** (vertical default; horizontal only for few short options) and density. No tone/emphasis axis — a checkbox is neutral.

## 5. Usage guidance

- **Use** a single Checkbox for one independent opt-in (consent "I agree", "Remember me"); a CheckboxGroup to select **any number (zero to many)** from a bounded set; and the indeterminate state for a **select-all** broadcasting partial selection over a table/tree.
- **Don't use** for: a single **immediate-effect** setting (→ **Switch**); **mutually exclusive** one-of-many (→ **Radio**); a binary that's really an action in a dense toolbar (→ **ToggleButton** with `aria-pressed`); or more than ~7–10 options where scanning/vertical space suffers (→ a multi-select **Combobox**/Listbox with filtering — see combobox).
- **Decision frameworks:**
  - **Checkbox vs. Switch is staged-vs-immediate** — does the change apply on save (Checkbox) or the instant you toggle (Switch)? Plus only Checkbox has indeterminate. (See switch when briefed.)
  - **Checkbox vs. Radio is any-number-vs-exactly-one.** A two-option mutually-exclusive choice is Radio (or a Switch if it's truly on/off), never two checkboxes.
  - **A single checkbox needs no group**; a set with a shared label and group validation needs `CheckboxGroup`.
  - **Never pre-check consent**, and **indeterminate is hierarchy-only** — not a user-settable third click state.

## 6. Accessibility

Inherits the substrate (describedby, error wiring — see text-field §6). Checkbox-specific:

- **Native `<input type="checkbox">` is the baseline** — role, checked state, Space-to-toggle for free; a custom control must reproduce `role="checkbox"` + `aria-checked` (`true`/`false`/`mixed`) exactly, and **`aria-checked="mixed"` must be set explicitly** — relying on the visual dash glyph alone to convey indeterminate is an accessibility failure (both agents).
- **The whole row is the hit target.** The visual box is only ~16–18px and fails SC 2.5.8 in isolation; the **labelled row** is engineered as the single hit target (clicking the label or the padding toggles), giving a ≥**24×24** target (WCAG 2.5.8 AA), scaling to **44** (Apple HIG) / **48** (Material) on touch — visual control tight, interactive footprint generous. Label sits beside the control (inline-end), not above (unlike text field).
- **Group semantics: `role="group"` + `aria-labelledby` over `fieldset`/`legend`.** Both are valid, but the practice defaults to `role="group"` because `fieldset` has notorious flexbox/grid layout quirks that make it hard to style predictably; `role="group"` on a `<div>` wired to the group label keeps CSS-layout freedom while preserving the shared-label announcement screen-reader users need for context (external — the sharpening over my pass's "fieldset or role=group"). Group error/required associate to the group and announce once.
- **Keyboard model — the key cross-control difference from Radio:** each checkbox is its **own Tab stop** (Tab/Shift+Tab between them), and **Space** toggles. Radio, by contrast, is one Tab stop for the group with **arrows** moving within. **Never override Enter** to toggle — Enter submits the enclosing form, and hijacking it breaks universal web behaviour (external).
- **WCAG SCs:** 1.3.1 (group structure), 3.3.1/3.3.2/3.3.3 (group error/labels), 1.4.11/2.4.13 (control focus + boundary contrast), 4.1.2 (role/checked/mixed), 2.5.8 (target size), 3.3.7 (Redundant Entry) for repeated consents.

## 7. Content guidelines

- **Positive phrasing, always.** The label states what becomes true when checked — "Subscribe to newsletter", never "Do not send me emails" (a double-negative the user has to mentally invert when unchecking). Sentence case; no terminal period for a terse single-sentence label (apply punctuation only for multi-sentence/legal labels).
- **Abstract shared words into the group label.** A group "Notification preferences" lets its rows read "Email", "SMS", "Push" rather than repeating "…notifications" three times (external).
- **Error copy is group-level for sets** ("Select at least one option") and follows SC 3.3.3.
- **Consent checkboxes** state exactly what is agreed (rich-content label, §3) and are **never pre-checked** — a dark pattern, and for marketing consent often unlawful.

## 8. Motion and transition

The check/uncheck glyph transition is the signature micro-motion — systems "draw" the checkmark via SVG `stroke-dasharray`/`stroke-dashoffset` (mimicking a pen stroke) while the container fill crossfades, ~100–150ms, eased. Indeterminate↔checked morphs the dash to the check. Under `prefers-reduced-motion: reduce`, **bypass the draw/spatial animation and flip instantly**; a sub-150ms opacity crossfade may remain (opacity doesn't trigger vestibular issues). No layout motion. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL mirrors the row** — the control swaps to the right, the label aligns right and flows leftward, padding flips, via logical properties. **But the checkmark glyph itself does *not* mirror** — the check shape is universally recognised, so the SVG keeps its standard stroke direction even in RTL (external — a nice nuance).
- **Text expansion** (German/Russian, +150–200%) — the row wraps freely; top/baseline alignment (§4) keeps the control anchored to the first line so multi-line labels don't fracture the layout.
- No text input, so IME is moot for the control; group labels and errors expand like any string. (See 13-internationalization-and-rtl.)

## 10. Naming

The row is universally **`Checkbox`**. The group splits: **`CheckboxGroup`** (Spectrum/React Aria, Atlassian, Primer) vs. Polaris's **`ChoiceList`** vs. composing under a generic `Field`/`FormControl` (Primer's other path) vs. Material's `FormGroup`. The atomic primitive: `Input` (Base Web), `Checkbox.Root` (Fluent). **The practice default: `Checkbox`** (the labelled row) **+ `CheckboxGroup`** (the set) **+ `Checkbox.Control`** (the atomic primitive). Aliases to map in docs search: `check`, `tickbox`, `checkbox-field`, `checklist`, `multiselect`, `ChoiceList`, and `<input type="checkbox">`.

## 11. Implementation notes

- **`indeterminate` is a DOM property, not an attribute or value** — the single most common checkbox bug. There is no `indeterminate` HTML attribute and it is not a third checked value; you set `node.indeterminate = true`. In React, passing `indeterminate={true}` as a JSX prop does nothing — apply it via a **synchronous ref callback** (Primer's evolution over the older `useLayoutEffect`, which forced an extra render and hurt perf in big checkbox lists):
  ```ts
  const setIndeterminate = useCallback((node) => { if (node) node.indeterminate = indeterminate ?? false }, [indeterminate])
  ```
- **The group owns the value array via context** — `CheckboxGroup` holds the selected-values array (React Aria's `useCheckboxGroupState` + `CheckboxGroupContext` is the reference); each child reads whether its `value` is in the array and dispatches back, avoiding prop-drilling and double-control. Children inherit `name`/disabled/size from group context.
- **Prefer the styled native input** — `<input type="checkbox">` + `appearance: none` + a styled pseudo-element/SVG keeps native semantics and keyboard for free; a `role="checkbox"` div is a last resort.
- **Expand the hit target to the whole row** with padding on the wrapper; the visual control stays tight (the icon-only-button parallel — the target lives on the wrapper, see icon §5).
- **Read-only has no native support** (§4) — decide explicitly (`disabled` / `aria-readonly` + prevented toggle / static text).
- **Form value gotcha** — a checked box submits its `value` (default `"on"`); an **unchecked box submits nothing** (the missing-key trap); a group maps to an array.
- **Headless escape hatch** — expose `Checkbox.Control` so a consumer building a card-select doesn't fight the opinionated row's label CSS and revert to a raw `<input>`.

## 12. Related and alternative components

- **Composes with:** Label, Description, FieldError, Form — and the decomposition relationship: **`Checkbox` composes into `CheckboxGroup`**; **`Checkbox.Control`** composes into custom rows (table select-all, card-select).
- **Alternative to:** Switch (immediate-effect binary), Radio/RadioGroup (exactly-one), ToggleButton (`aria-pressed` action), multi-select Combobox/Listbox (large sets — see combobox), Chip/Tag (selectable token). *(The external pass listed Switch/Combobox as `superseded-by`; that overstates it — they're sibling alternatives chosen by intent and scale, not replacements. Prose wins; the schema is corrected.)*
- **Supersedes:** a bare `<input type=checkbox>` without label wiring; a `role=checkbox` div where a styled native input would do.
- **Superseded by:** nothing for staged binary choice.

(This brief establishes the **selection-control decomposition** — labelled control + distinct group + exposed atomic primitive — that **Radio** (group mandatory) and **Switch** (no group) refine. See text-field for the encapsulation-hybrid precedent it mirrors; 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **Styling the native input won** — `appearance: none` + pseudo-element/SVG replaced both the `role=checkbox` div and the hidden-input-plus-fake-box hacks, keeping native semantics.
2. **The group as a first-class component** (owning the value array + group validation) replaced ad-hoc hand-wired fieldsets.
3. **`role="group"` + `aria-labelledby` over `fieldset`/`legend`** for the group, driven by `fieldset`'s CSS-layout quirks.
4. **Decomposition converged on polymorphic-row + distinct-group + exposed-atomic-primitive** (over both the fully-monolithic and the fully-atomic three-component splits) — which is the practice's call, and maps cleanly onto both React composition and Web Component shadow-DOM slots.
5. **The `indeterminate` ref-callback** superseding `useLayoutEffect` for perf in large lists.

## 14. Sources cited

Conservative dating (the external pass supplied precise, largely 2026-stamped versions — Spectrum/React Aria v3.49.0, Carbon React v1.109.0, Primer React v38.28.0, Atlassian `@atlaskit/checkbox` v17/v21.12, Base Web 5.x/13.x, Fluent v9, Polaris Web Components 2025-10→2026 — held loosely and unverified; the Polaris React→Web-Components migration is the same cross-brief unverified claim flagged on Button/Text Field; `last-audited` is the re-run trigger):

- Adobe Spectrum / React Aria — `Checkbox` + `CheckboxGroup`, `useCheckbox(Group)`, `CheckboxGroupContext`, `isIndeterminate` (Spectrum, 2024–2025).
- IBM Carbon — `Checkbox` + `CheckboxGroup` (fieldset-wrapped) (Carbon, 2024–2025).
- GitHub Primer — atomic `Checkbox` + `FormControl`/`CheckboxGroup`, the indeterminate ref-callback (Primer, 2024–2026).
- Atlassian Design System — `@atlaskit/checkbox` (`isChecked`/`isIndeterminate` naming) (Atlassian, 2024–2025).
- Microsoft Fluent UI v9 — recomposable slots (root/input/icon/box), keyboard-only focus ring (Fluent, 2024–2025).
- Shopify Polaris — `Checkbox`, `ChoiceList`; the (unverified) Web Components `<s-checkbox>` migration and the `label`-prop-over-children move (Polaris, 2025–2026).
- Uber Base Web — `Checkbox` (overrides, `STYLE_TYPE`) (Base Web, 2024).
- Google Material 3 — `md-checkbox`, `FormGroup`, Compose mobile (Material 3, 2024).
- Apple Human Interface Guidelines — 44pt target size, toggles (Apple HIG, 2024–2025).
- WAI-ARIA APG — Checkbox (single + mixed/tri-state) pattern; `role="group"` + `aria-labelledby`.
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.3.1, 3.3.1, 3.3.2, 3.3.3, 1.4.11, 2.4.13, 4.1.2, 2.5.8, 3.3.7.

## 15. Agent-consumable schema

```yaml
identity:
  id: checkbox
  name: Checkbox
  aliases: [check, tickbox, checkbox-field, checkbox-list, choice-list, multiselect]
  category: form
  status: stable
description: >
  Control for an independent binary choice STAGED into a form and
  submitted (not immediate — that's a switch), optionally one of many in a
  set, with an indeterminate (mixed) visual state for select-all
  hierarchy. Not a switch (immediate effect), not a radio (exactly-one),
  not a toggle-button (aria-pressed action).
anatomy:
  decomposition:
    tiers: [atomic-control, labelled-row, group]
    practice-model: >
      TWO public components — Checkbox (folds atomic+row: control + rich-
      content label + optional description; the ~90% case) and
      CheckboxGroup (distinct: shared label + value array + group
      validation + layout; the group owns validation, NOT the rows) —
      PLUS Checkbox.Control, the atomic primitive exposed for decoupled
      layouts (table select-all, card-select). Mirrors the text-field
      bundled-props-vs-composed-slots hybrid. Both research passes
      converged on this.
    pattern-carries-to: [radio (group MANDATORY), switch (no group)]
    nesting: >
      The two-component surface is a convenience layer, not closed.
      Checkbox.Control is the NESTABLE unit (list row, table cell, menu
      item, card). When nested: host provides the accessible name (row
      text via aria-labelledby), host owns the hit target (whole row,
      unless the row has a primary action -> control is a named secondary
      affordance), and the enclosing collection (selectable List/Table/
      Menu) owns selection + group semantics — do NOT nest CheckboxGroup
      in a List, the collection IS the group. Mixing control types per
      row is fine via *.Control if selection semantics match (multi ->
      checkbox; per-row immediate -> switch; single -> radio). Avoid the
      ambiguous nested-interactive (control inside a button/link row).
  parts: [control, check-glyph, indeterminate-glyph, label, description, inline-error, group-label, group-description, group-error, layout-container]
api:
  inherits: text-field   # error/description/describedby substrate; label model differs (beside, rich-content, = hit target); native DOM naming (checked/indeterminate, not isChecked/isSelected)
  checkbox:
    - {name: checked, type: boolean, required: false, description: controlled binary; pair defaultChecked/onChange (exposes event + boolean)}
    - {name: indeterminate, type: boolean, default: false, description: PRESENTATIONAL mixed state (aria-checked=mixed), NOT a third value; set via DOM .indeterminate}
    - {name: label, type: node, required: false, description: "RICH CONTENT (node/children), not string-only — must support a consent link ('I agree to the <a>Terms</a>'); accessible name + part of hit target; omit only for the bare Checkbox.Control"}
    - {name: description, type: node, required: false, description: helper under the label, describedby-wired}
    - {name: value, type: string, required: false, description: submitted when checked; element of a group's array}
    - {name: name, type: string, required: false}
    - {name: disabled, type: boolean, default: false}
    - {name: isReadOnly, type: boolean, default: false, description: NO native support — aria-readonly + prevented toggle, or render static}
  group:
    - {name: label, type: node, required: true, description: shared group label (group's accessible name)}
    - {name: value/defaultValue/onChange, type: array<string>, description: the GROUP owns the selected-values array (via context)}
    - {name: required, type: boolean, default: false, description: group-level (select at least one)}
    - {name: isInvalid/errorMessage, type: boolean/node, description: GROUP-level validation, announced once — rows never own error/required}
    - {name: orientation, type: enum, values: [vertical, horizontal], default: vertical}
states:
  runtime: [rest, hover, focus-visible, pressed, checked, unchecked, indeterminate, disabled, read-only, error]
  notes:
    indeterminate: "third VISUAL state (dash glyph, aria-checked=mixed), not a third value; parent/child select-all hierarchy only"
    read-only: "no working native readonly (like select) — aria-readonly + prevent toggle, or static text"
    error: "isolated row recolours the border; in a group the rows stay neutral and the GROUP shows the error"
variants:
  size: [small, medium, large]
  alignment: [top-baseline-default]   # NEVER center — drifts mid-paragraph on multi-line labels
  group: {orientation: [vertical, horizontal], density: [comfortable, compact]}
accessibility:
  inherits: text-field
  wcag-criteria: ["1.3.1", "3.3.1", "3.3.2", "3.3.3", "1.4.11", "2.4.13", "4.1.2", "2.5.8", "3.3.7"]
  control: "native <input type=checkbox> baseline | role=checkbox + aria-checked (true/false/mixed) — set MIXED explicitly, never rely on the visual dash"
  hit-target: "the whole ROW is the single target; >=24x24 (2.5.8), 44 (Apple)/48 (Material) on touch; label beside not above"
  group: "role=group + aria-labelledby (DEFAULT, over fieldset/legend — fieldset has flexbox/grid quirks); group error/required announced once"
  keyboard-model:
    tab: "each checkbox is its OWN tab stop (UNLIKE radio's group-as-one-stop + arrows) — the key cross-control difference"
    space: toggles
    enter: "NEVER override — Enter submits the enclosing form"
  focus-behavior: "ring on the CONTROL, offset, >=3:1 (1.4.11/2.4.13); keyboard-only, not mouse/touch"
content:
  label-pattern: "POSITIVE statement true when checked ('Subscribe to newsletter'); sentence case; no negatives/double-negatives; rich content for consent links"
  group-label-pattern: "names the decision; abstract shared words up ('Notification preferences' -> 'Email'/'SMS'/'Push')"
  error-pattern: "group-level for sets ('Select at least one'); SC 3.3.3"
  consent-pattern: "state exactly what is agreed; NEVER pre-check"
motion:
  check-transition: "~100-150ms SVG stroke-dashoffset 'draw' + container fill crossfade, eased; indeterminate<->checked morphs dash to check"
  reduce-motion: "bypass draw/spatial animation, flip instantly; sub-150ms opacity crossfade may remain"
i18n:
  rtl: "row mirrors (control to the right, label flows leftward, via logical properties) — BUT the checkmark glyph does NOT mirror (universally recognised shape)"
  expansion: "label wraps freely (+150-200% in de/ru); top/baseline alignment keeps the control on the first line"
implementation:
  - "indeterminate = DOM property (node.indeterminate=true) via SYNCHRONOUS ref callback — NOT a JSX/HTML attribute, NOT a checked value; the #1 checkbox bug (ref-callback over useLayoutEffect for perf)"
  - "CheckboxGroup owns the value array via context (useCheckboxGroupState/CheckboxGroupContext); children read membership, dispatch back — no double-control"
  - "prefer styled native input (appearance:none + pseudo-element/SVG); role=checkbox div is a last resort"
  - "expand hit target to the whole row (wrapper padding); control stays visually tight"
  - "form value: checked submits its value (default 'on'); UNCHECKED submits NOTHING (missing-key gotcha); group -> array"
composition:
  composes-with: [label, description, field-error, form]
  decomposition-relationship: "Checkbox composes into CheckboxGroup; Checkbox.Control composes into custom rows (table select-all, card-select)"
  alternative-to: [switch, radio-group, toggle-button, multiselect-combobox, listbox, chip]   # NOT superseded-by — siblings chosen by intent/scale
  supersedes: ["bare <input type=checkbox> without label wiring", "role=checkbox div where a styled native input would do"]
  superseded-by: null
notes:
  contested:
    - "decomposition: two-component surface (Checkbox + CheckboxGroup) + exposed Checkbox.Control primitive — both passes converged; the fully-atomic 3-component split is the headless alternative"
    - "label as rich-content node/slot vs string prop (rich content wins — consent links)"
    - "role=group + aria-labelledby vs fieldset/legend (role=group default, for CSS layout)"
    - "read-only handling (no native support)"
  unverified:
    - "Polaris React->Web-Components migration + label-prop move (shared cross-brief claim; needs _source-text)"
    - "external-supplied 2026 version numbers"
  evolution: "styled native input won; group first-class; role=group over fieldset; decomposition -> row+group+atomic-primitive; indeterminate ref-callback"
  pattern-note: "establishes the selection-control decomposition for radio (group mandatory) and switch (no group)"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-checkbox/` (15 June 2026), the first of the boolean/choice controls. The headline finding is convergence on the decomposition: both passes independently landed on a two-component public surface (`Checkbox` labelled row + distinct `CheckboxGroup`) plus an exposed atomic primitive (`Checkbox.Control`), which is the text-field bundled-vs-composed hybrid applied to a control — and the pattern this brief sets for Radio (group mandatory) and Switch (no group). Other convergences: indeterminate as a DOM property / `aria-checked="mixed"` and not a third value, the whole-row hit target meeting 2.5.8/44/48, top-baseline alignment as non-negotiable, the Tab-each-vs-arrow-within difference from radio, positive-phrasing/sentence-case labels with shared-word abstraction into the group label, the staged-vs-immediate checkbox-vs-switch boundary, and the styled-native-input implementation. External-pass contributions folded in: the three-paradigm taxonomy (monolithic/composed/headless), the **label-as-rich-content** refinement (the consent-link case, which corrected my initial string-prop framing), `role="group"`+`aria-labelledby` as the practice default over `fieldset` (CSS-layout quirks), the indeterminate ref-callback over `useLayoutEffect`, the `CheckboxGroupContext`/value-array pattern, the explicit target-size numbers, the Enter-key-never-override rule, the checkmark-doesn't-mirror-in-RTL nuance, and the `ChoiceList` alias. Claude-pass contributions: the native-DOM-naming default (`checked`/`indeterminate` over `is*`), the no-native-readonly caveat, the icon-only-button hit-target parallel, and the explicit framing against the text-field encapsulation precedent. Two corrections against the external §15, prose winning: Switch/Combobox are **alternative-to**, not `superseded-by` (siblings chosen by intent/scale); and the label is rich-content (node), reconciling the prop-vs-children split. The Polaris Web-Components migration and the 2026 version numbers are flagged unverified pending `_source-text/` backing. Conformant to `components/_schema.md`.*

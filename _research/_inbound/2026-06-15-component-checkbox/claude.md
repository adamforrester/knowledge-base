# Checkbox — field-truth study (Claude pass)

## 1. Framing

Checkbox looks atomic and isn't. It is the catalogue's clearest test of **component decomposition**: the same control appears at three granularities — the bare box, the labelled row, and the group — and the practice's headline job here is to decide how many components that becomes and where each boundary sits (§2). That decision then carries to Radio and Switch, so this brief sets the pattern.

What a Checkbox *is*: a control for an **independent binary choice** that is *staged* into a form and submitted — on/off, included/excluded, agreed/not — optionally one of many in a set. What it *isn't*: an **immediate-effect** toggle (that's a Switch — the checkbox-vs-switch boundary, §5), a **mutually-exclusive** choice within a set (that's Radio), or an **action with pressed state** (that's a ToggleButton with `aria-pressed`). The tell for Checkbox over Switch: the change takes effect on *save/submit*, not instantly, and a checkbox can be **indeterminate** (a third, mixed visual state) where a switch cannot.

Why systems disagree: almost entirely on decomposition (§2) and on whether the group is a first-class component or a layout convention.

## 2. Anatomy and parts — the decomposition

Three real tiers exist in the field:

1. **Atomic control** — the box + checkmark/indeterminate glyph, no label. The accessibility target (`<input type="checkbox">` or a custom control with `role="checkbox"`).
2. **Labelled row / field** — control + adjacent label + optional description line + optional inline error, as one clickable line item.
3. **Group** — multiple rows under a shared group label (a `fieldset`/`legend` or `role="group"` + `aria-labelledby`), often with group-level required/validation/error and a layout axis.

The field splits on how many components these become. Most systems (Polaris, Spectrum, Carbon, Material, Base Web) **fold the atomic control and the row into one polymorphic `Checkbox`** — the label is a prop, an unlabelled checkbox is just the label omitted — and ship a **separate `CheckboxGroup`**. A minority (Primer, strict-headless systems) keep the **atomic control separate** and compose the row from a generic `FormControl`/`Field` wrapper (control + `FormControl.Label` + `FormControl.Caption`).

**The practice's position (consistent with the text-field encapsulation hybrid — see text-field §3):**

- **`Checkbox` is the labelled control** — box + `label` + optional `description`, label as a prop. This is the default unit because the labelled row is the overwhelmingly common case and an unlabelled box is the exception. (This is the "bundled props" default.)
- **The atomic box is exposed as a composable primitive/slot** (`Checkbox` with no label, or a headless `Checkbox.Control`) for the custom-layout 10% — a select-all in a table header cell, a card-select where the whole card is the target. (This is the "composed slot" escape hatch.)
- **`CheckboxGroup` is a distinct component** — because the group has genuine state and semantics the row doesn't: it owns the shared group label, the **value array**, group-level `required`/validation/error, and the layout axis. A group is *not* mere layout.

So the public surface is **two components — `Checkbox` and `CheckboxGroup`** — with the atomic box as an exposed primitive, rather than three separate top-level components. The three-component split (atomic / row / group) is a defensible alternative, and the right one for a strict headless system, but it taxes the 90% case with composition ceremony for an atomic-only scenario that's rare. The practice collapses atomic+row into one polymorphic control and keeps the group distinct. **(This is the selection-control decomposition pattern; Radio and Switch refine it — Radio's group is mandatory, Switch usually has no group. See §12.)**

Named parts: **control** (box + check/indeterminate glyph + focus ring), **label** (inline-end of the control), **description** (helper line under the label), **inline error** (row-level), and at the group: **group label/legend**, **group description**, **group error**, **layout container**.

## 3. Properties / API

Inherits the generic form-field substrate (`error`, `helpText`/`description`, `required`, `disabled`, describedby wiring — see text-field §3); the Checkbox label model differs (label beside, a prop, doubling as the hit target). The two-tier API:

**`Checkbox` (the labelled control):**
- `isSelected`/`checked` + `defaultSelected` / `onChange` — controlled/uncontrolled binary.
- `isIndeterminate` — the mixed visual state (a *presentational* flag, not a third value — §4, §11).
- `label` — string or node; the accessible name and part of the hit target. Omit for the bare-primitive case (then an external `aria-label`/`aria-labelledby` is required).
- `description` — optional helper under the label, `aria-describedby`-wired.
- `value` — the string submitted when checked and part of a group's value array.
- `name` — form field name.
- `isDisabled`, `isReadOnly` (with the native-readonly caveat, §4), `isInvalid`/`error`, `size`.

**`CheckboxGroup` (the set):**
- `label` — the shared group label (rendered as `legend`/`role=group` name).
- `value` / `defaultValue` / `onChange` — the **array** of selected child values (the group owns selection state).
- `isRequired`, `isInvalid`/`errorMessage`, `description` — **group-level** validation and messaging (one error for the set, e.g. "Select at least one").
- `orientation` — `vertical` (default) / `horizontal`.
- children: `Checkbox`es (which inherit `name`/disabled/size from group context).

The load-bearing API call: **selection state lives at the tier that owns it** — a standalone `Checkbox` owns its own boolean; inside a `CheckboxGroup`, the *group* owns the array and the children are controlled by it. Don't make consumers wire both.

## 4. States and variants

Runtime states: rest, hover, focus-visible, pressed, **checked / unchecked**, **indeterminate**, disabled, error, read-only.

| State | Checkbox-specific contract |
| --- | --- |
| checked / unchecked | the binary; checkmark glyph on checked |
| indeterminate | a **third visual state, not a third value** — a dash glyph, `aria-checked="mixed"`; the value underneath is still true/false. Set via the DOM `.indeterminate` property, never an HTML attribute (§11). The parent of a partially-checked "select all" set. |
| focus-visible | ring on the control, ≥3:1 (1.4.11/2.4.13); the row is the click target but the *control* carries the visible focus |
| error | `aria-invalid`; at the group, the error is group-level and announced once, not per row |
| read-only | **the awkward one** — native `<input type=checkbox>` has no working `readonly` (only `disabled`), so a true read-only checkbox needs `aria-readonly` + prevented toggling, or is better rendered as static text; flag this like select's no-native-readonly |
| pressed | brief active feedback, mainly mobile |

**Intentional variants:** `size` (small/medium/large — control scales with the type), **alignment** (control top-aligned to the first line when the label/description wraps — *not* center-aligned, which drifts on multi-line), and group **density** + **orientation** (vertical default; horizontal only for few short options). No tone/emphasis axis — a checkbox is neutral.

## 5. Usage guidance

- **Use** a single Checkbox for one independent opt-in (consent "I agree", "Remember me", "Subscribe"); a CheckboxGroup for selecting **any number (zero to many)** from a set.
- **Don't use** for: a single immediate-effect setting (→ **Switch** — the change applies now, not on submit); **mutually exclusive** one-of-many (→ **Radio**); a binary that's really an action (→ ToggleButton); or more than ~7–10 options where scanning is hard (→ a filterable list / multi-select Combobox — see combobox).
- **Decision frameworks:**
  - **Checkbox vs. Switch** is *staged-vs-immediate*: does the change take effect on save (Checkbox) or instantly (Switch)? Plus only Checkbox has indeterminate. (See switch when briefed.)
  - **Checkbox vs. Radio** is *any-number vs. exactly-one*. A two-option mutually-exclusive choice is Radio (or a Switch if it's on/off), never two checkboxes.
  - **Single checkbox needs no group**; a set with a shared label and group validation needs `CheckboxGroup` (the fieldset).
  - **Indeterminate is for hierarchy only** — a parent reflecting partially-selected children; never a user-settable third state by click.

## 6. Accessibility

Inherits the substrate (describedby, error wiring — see text-field §6). Checkbox-specific:

- **Native `<input type="checkbox">` is the baseline** — role, checked state, and keyboard (Space toggles) for free; a custom control must reproduce `role="checkbox"` + `aria-checked` (`true`/`false`/`mixed`) exactly.
- **The label must be programmatically associated** (`<label for>`/wrapping, or `aria-labelledby`), and the **whole row — control + label — is the hit target** (clicking the label toggles), meeting target size (SC 2.5.8; 44px recommended). Label sits at the control's inline-end (beside), unlike text field's label-above.
- **Indeterminate → `aria-checked="mixed"`** (native reflects the `.indeterminate` property). It is announced as "mixed"; ensure activating it resolves to a defined state.
- **The group is a `fieldset` + `legend`** (or `role="group"` + `aria-labelledby`) so the shared label is announced with each option — without it, screen-reader users hear orphaned checkboxes with no group context. Group-level error/required associate to the group via `aria-describedby`/`aria-invalid`, announced once.
- **Keyboard:** Tab moves between checkboxes (each is a tab stop — *unlike* radios, where the group is one tab stop and arrows move within); Space toggles. This Tab-each vs. arrow-within difference from Radio is the most common cross-control confusion.
- **WCAG SCs:** 1.3.1 (the group structure), 3.3.1/3.3.2 (group error/labels), 1.4.11/2.4.13 (control focus + boundary contrast), 4.1.2 (role/checked/mixed), 2.5.8 (target size), 3.3.7 (Redundant Entry) for repeated consents.

## 7. Content guidelines

- **Label: a positive, parallel statement** the checked state makes true — "Email me about updates", not "Don't email me" (avoid negatives that invert on check). Sentence case, no trailing period unless multi-sentence.
- **Group label** names the decision ("Notifications"); the group description carries the rule ("Select all that apply").
- **Error copy** is group-level for sets ("Select at least one option") and follows SC 3.3.3.
- **Consent checkboxes** state exactly what is agreed; never pre-check consent (a dark pattern and, for marketing consent, often unlawful).

## 8. Motion and transition

The check/uncheck glyph transition is the signature micro-motion — a quick (~100–150ms) draw/scale of the checkmark and a background fill, eased. Indeterminate↔checked morphs the dash to the check. Keep it short; under `prefers-reduced-motion: reduce`, drop the draw/scale and snap the glyph (the state change must remain instant and legible). No layout motion. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL** mirrors the row: the control moves to the inline-end-becomes-right → it sits on the right with the label to its left, via logical properties (the control leads on the reading side).
- **Label text expansion** — the row wraps to multiple lines (German/Russian); the control stays top-aligned to the first line (§4), never center-drifting.
- Inherits the substrate's locale/IME concerns; checkbox has no text input so IME is moot, but group labels and errors expand like any string. (See 13-internationalization-and-rtl.)

## 10. Naming

The control is universally **`Checkbox`**. The group splits: **`CheckboxGroup`** (Spectrum/React Aria, Carbon, Fluent) vs. composing under a generic `Field`/`FormControl` (Primer, Atlassian) vs. Material's `FormGroup`. **The practice default: `Checkbox`** (the labelled control, label optional) **+ `CheckboxGroup`** (the set). The atomic primitive, if separately exposed, is `Checkbox` with no label or a headless `Checkbox.Control`. Aliases to map: `Check`, `Tickbox`, `CheckboxField`, `CheckboxList`, `CheckGroup`.

## 11. Implementation notes

- **Indeterminate is a DOM property, not an attribute or value.** You set `inputEl.indeterminate = true` via a ref/effect — there is no `indeterminate` HTML attribute and it is not a third checked value. This is the single most common checkbox implementation bug. A custom control sets `aria-checked="mixed"`.
- **Controlled/uncontrolled** mirror text-field's traps (controlled `checked` with no `onChange` = frozen). The group owns the array; children read from group context — don't double-control.
- **Don't hand-roll the box if you can style the native input** — prefer `<input type="checkbox">` + `appearance: none` + a styled pseudo-element / SVG, keeping native semantics and keyboard for free; a `role="checkbox"` div is a last resort.
- **Hit target** — expand the clickable area to the whole row with padding, not just the 16–20px box, while keeping the visual control tight (the icon-only-button parallel — the target lives on the wrapper).
- **Read-only** has no native support (§4) — decide explicitly: `disabled` (removed from submission), `aria-readonly` + prevented toggle, or static text.
- **Form value** — emit a real `name`/`value`; a checked box submits its `value` (default `"on"`), an unchecked box submits nothing (the classic "missing key" gotcha); a group maps to an array.

## 12. Related and alternative components

- **Composes with:** Label, Description/Helper, FieldError, and — the decomposition relationship — **`Checkbox` composes into `CheckboxGroup`**; the atomic control composes into custom rows (table select-all, card-select). Form.
- **Alternative to:** Switch (immediate-effect binary), Radio/RadioGroup (exactly-one), ToggleButton (`aria-pressed` action), multi-select Combobox/Select (large sets), Chip/Tag (selectable token).
- **Supersedes:** a bare `<input type=checkbox>` without label wiring; a `role=checkbox` div where a styled native input would do.
- **Superseded by:** nothing for staged binary choice; large sets migrate to a filterable multi-select.

(The selection-control decomposition established here — labelled control + distinct group, atomic box as a primitive — carries to **Radio** (group mandatory) and **Switch** (no group). See text-field for the encapsulation-hybrid precedent this mirrors; 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **Styling the native input won** — `appearance: none` + pseudo-element/SVG replaced the old `role=checkbox` div and the hidden-input-plus-fake-box hacks, keeping native semantics.
2. **The group as a first-class component** (`CheckboxGroup` owning the value array + group validation) is now standard, replacing ad-hoc fieldsets wired by hand.
3. **Indeterminate is better understood** — explicitly a presentational `mixed` state for hierarchy, not a tri-state value, with the parent/child select-all as the canonical pattern.
4. **Decomposition is converging on polymorphic-control-plus-group** (label as a prop, group distinct) over the fully-atomic three-component split, except in strict headless systems — which is the practice's call.

## 14. Sources cited

(Conservative; reconcile with external pass.) Adobe Spectrum / React Aria `Checkbox` + `CheckboxGroup` (`isIndeterminate`, group value array, validation) (2024–2025); IBM Carbon `Checkbox` / `CheckboxGroup` (2024); Shopify Polaris `Checkbox` (2024); GitHub Primer `Checkbox` + `FormControl` + `CheckboxGroup` (2024); Atlassian `Checkbox` (2024); Google Material 3 checkbox + `FormGroup` (2024); Base Web `Checkbox` (`STYLE_TYPE`, indeterminate) (2024); Apple HIG / Material Compose (2024); WAI-ARIA APG Checkbox (single + mixed) pattern; WCAG 2.2 (Oct 2023) — 1.3.1, 3.3.1/2/3, 1.4.11, 2.4.13, 4.1.2, 2.5.8, 3.3.7.

## 15. Agent-consumable schema

```yaml
identity:
  id: checkbox
  name: Checkbox
  aliases: [check, tickbox, checkbox-field, checkbox-list, check-group]
  category: form
  status: stable
description: >
  Control for an independent binary choice STAGED into a form and
  submitted (not immediate — that's a switch), optionally one of many in
  a set. Supports an indeterminate (mixed) visual state. Decomposes into
  Checkbox (labelled control, label optional) + CheckboxGroup (the set);
  atomic box exposed as a primitive. Not a switch (immediate effect), not
  a radio (exactly-one), not a toggle-button (aria-pressed action).
anatomy:
  decomposition:
    tiers: [atomic-control, labelled-row, group]
    practice-model: >
      TWO components — Checkbox (folds atomic+row: box + label prop +
      optional description) and CheckboxGroup (distinct: shared label +
      value array + group validation + layout). Atomic box exposed as a
      composable primitive (Checkbox sans label / Checkbox.Control) for
      custom layouts (table select-all, card-select). Mirrors the
      text-field bundled-props-vs-composed-slots hybrid. The 3-component
      atomic/row/group split is the defensible headless alternative.
    pattern-carries-to: [radio (group MANDATORY), switch (no group)]
  parts: [control, check-glyph, indeterminate-glyph, label, description, inline-error, group-label/legend, group-description, group-error, layout-container]
api:
  inherits: text-field   # error/helper/required/disabled/describedby substrate; label model differs (beside, a prop, = hit target)
  checkbox:
    - {name: isSelected/checked, type: boolean, required: false, description: controlled binary; pair defaultSelected/onChange}
    - {name: isIndeterminate, type: boolean, default: false, description: PRESENTATIONAL mixed state (aria-checked=mixed), NOT a third value; set via DOM .indeterminate}
    - {name: label, type: string | node, required: false, description: accessible name + part of the hit target; omit for the bare primitive (then external aria-label required)}
    - {name: description, type: node, required: false, description: helper under the label, describedby-wired}
    - {name: value, type: string, required: false, description: submitted when checked; element of a group's array}
    - {name: name, type: string, required: false}
    - {name: isReadOnly, type: boolean, default: false, description: NO native support — needs aria-readonly + prevented toggle, or render static}
  group:
    - {name: label, type: string | node, required: true, description: shared group label (legend / role=group name)}
    - {name: value/defaultValue/onChange, type: array<string>, description: the GROUP owns the selected-values array}
    - {name: isRequired, type: boolean, default: false}
    - {name: isInvalid/errorMessage, type: boolean/node, description: GROUP-level validation, announced once}
    - {name: orientation, type: enum, values: [vertical, horizontal], default: vertical}
states:
  runtime: [rest, hover, focus-visible, pressed, checked, unchecked, indeterminate, disabled, error, read-only]
  notes:
    indeterminate: "third VISUAL state (dash glyph, aria-checked=mixed), not a third value; for parent/child select-all hierarchy only"
    read-only: "no working native readonly (like select) — aria-readonly + prevent toggle, or static text"
variants:
  size: [small, medium, large]
  alignment: [control-top-aligned-to-first-line]   # never center, drifts on multi-line
  group: {orientation: [vertical, horizontal], density: [comfortable, compact]}
accessibility:
  inherits: text-field
  wcag-criteria: ["1.3.1", "3.3.1", "3.3.2", "3.3.3", "1.4.11", "2.4.13", "4.1.2", "2.5.8", "3.3.7"]
  control: "native <input type=checkbox> baseline | role=checkbox + aria-checked (true/false/mixed)"
  label: "programmatically associated; whole row (control + label) is the hit target (2.5.8, 44px rec); label BESIDE not above"
  group: "fieldset+legend or role=group + aria-labelledby so the shared label is announced; group error/required via aria-describedby/aria-invalid, announced once"
  keyboard-model:
    tab: "each checkbox is its OWN tab stop (UNLIKE radio's group-as-one-stop + arrows) — the key cross-control difference"
    space: toggles
  focus-behavior: "ring on the CONTROL (not the row), >=3:1 (1.4.11/2.4.13)"
content:
  label-pattern: "positive parallel statement the checked state makes true ('Email me about updates'); sentence case; avoid negatives that invert on check"
  group-label-pattern: "names the decision; group description carries the rule ('Select all that apply')"
  error-pattern: "group-level for sets ('Select at least one'); SC 3.3.3"
  consent-pattern: "state exactly what is agreed; NEVER pre-check consent"
motion:
  check-transition: "~100-150ms checkmark draw/scale + background fill, eased; indeterminate<->checked morphs dash to check"
  reduce-motion: "drop draw/scale, snap the glyph; state change stays instant + legible"
i18n:
  rtl: "row mirrors — control leads on the reading (right) side, label to its left, via logical properties"
  expansion: "label wraps multi-line; control stays top-aligned to the first line"
implementation:
  - "indeterminate = DOM property (inputEl.indeterminate=true via ref/effect); NOT an HTML attribute, NOT a checked value — the #1 checkbox bug"
  - "prefer native input + appearance:none + styled pseudo-element/SVG; role=checkbox div is a last resort"
  - "group owns the array; children read from group context — don't double-control"
  - "expand hit target to the whole row (padding on the wrapper), control stays visually tight"
  - "form value: checked submits its value (default 'on'), unchecked submits NOTHING (missing-key gotcha); group -> array"
composition:
  composes-with: [label, description, field-error, form]
  decomposition-relationship: "Checkbox composes into CheckboxGroup; atomic control composes into custom rows (table select-all, card-select)"
  alternative-to: [switch, radio-group, toggle-button, multiselect-combobox, chip]
  supersedes: ["bare <input type=checkbox> without label wiring", "role=checkbox div where a styled native input would do"]
  superseded-by: null
notes:
  contested:
    - "decomposition: polymorphic Checkbox+label + distinct CheckboxGroup (practice) vs fully-atomic 3-component split (headless alternative)"
    - "read-only handling (no native support)"
    - "indeterminate as presentational mixed-state vs misuse as a tri-state value"
  evolution: "styled native input won; group as first-class component; decomposition converging on control+group"
  pattern-note: "establishes the selection-control decomposition for radio (group mandatory) and switch (no group)"
```

# Radio — field-truth study (Claude pass)

## 1. Framing

Radio inherits the Checkbox brief's selection-control decomposition wholesale — labelled control + distinct group + exposed atomic primitive (see checkbox §2) — so this brief does not re-derive it. It exists to nail the **one structural difference that changes everything**: for Radio, **the group is mandatory**. A lone checkbox is a valid control (a consent box); a lone radio is semantically meaningless — a radio only means "one of these" and needs siblings and a shared `name` to mean anything. That single fact cascades into the API (the group owns the value), the keyboard model (the group is one tab stop, arrows move *and* select), and the interaction (you cannot deselect a radio).

What a Radio *is*: a control for choosing **exactly one** from a small set of **mutually exclusive, all-visible** options. What it *isn't*: any-number selection (Checkbox), an on/off setting (Switch), the same single-select but collapsed (Select, past ~5–7 options) or in a denser horizontal presentation (Segmented Control), or an action (Button). The analogous components are **`Radio`** (the labelled control), **`RadioGroup`** (mandatory — owns `name`, the single value, validation), and **`Radio.Control`** (the nestable atomic primitive — same contract as `Checkbox.Control`, but the host collection must be single-selection and *is* the radiogroup).

## 2. Anatomy and parts

Inherits the Checkbox decomposition (see checkbox §2) — control / labelled row / group, with the atomic `Radio.Control` as the nestable unit for hosts (a single-select list/table/menu where the collection is the radiogroup). The difference is emphasis: **`RadioGroup` is not optional here.** Where `CheckboxGroup` is reached for only when a set needs a shared label/validation, `RadioGroup` is the *unit of use* — you never ship a bare `Radio`. Named parts mirror checkbox (control + dot glyph + label + description + inline error; group label/description/error + layout container), with the dot/disc glyph replacing the checkmark and **no indeterminate glyph**.

## 3. Properties / API

Inherits the form-field substrate and the checkbox row API shape (label as rich content, description, disabled, top-baseline alignment — see checkbox §3). The radio-specific weighting:

**`RadioGroup` (the mandatory owner):**
- `name` — the shared HTML name binding the radios into one exclusive set; the group owns it (a child radio never sets its own).
- `value` / `defaultValue` / `onChange` — a **single scalar** (not an array — the checkbox-group contrast). The group owns selection.
- `label` — the shared group label (the group's accessible name; the radios' options have no meaning without it).
- `isRequired`, `isInvalid`/`errorMessage`, `description` — group-level.
- `orientation` — vertical (default) / horizontal.

**`Radio` (the option):**
- `value` — the string this option contributes when selected (required; it's the option's identity in the group).
- `label`, `description`, `isDisabled` — per-option.
- **No `checked`/`onChange` on the individual radio** — selection is derived from whether its `value` equals the group's value; the child reads from group context (§11). This is the key API difference from checkbox, where a standalone box owns its own boolean.

**The default-selection decision** is a genuine API/UX call (§5): a `RadioGroup` may pre-select a `defaultValue` or start with none. Pre-selecting is better when a sensible default exists and the choice is required (it models the recommended path); starting empty is correct when there's no safe default and the user must make a deliberate choice — but an empty radio group **cannot be returned to empty** by the user (§4), so "no default" is a one-way door unless an explicit "None"/"No preference" option is provided.

## 4. States and variants

Inherits checkbox runtime states (rest/hover/focus-visible/pressed/disabled/error/read-only — see checkbox §4), with radio-specific differences:

| State | Radio-specific contract |
| --- | --- |
| selected | the dot/disc fills; **exactly one per group** |
| no-deselect | **clicking/activating a selected radio does not unselect it** — unlike checkbox, there is no toggle-off; the only way out of a value is selecting a sibling (or an explicit "None" option). The most-felt behavioural difference from checkbox. |
| no indeterminate | radio has no mixed state |
| focus vs. selection | with selection-follows-focus, arrowing to an option both focuses *and* selects it; the selected option is the group's single tab stop (§6) |
| error | group-level (the set failed validation, e.g. "Select an option"), never per-option |

**Variants:** `size`; group **orientation** (vertical default; horizontal for few short options); density. The presentation axis is where Radio meets **Segmented Control** — same exactly-one semantics, different skin (§5). No tone/emphasis.

## 5. Usage guidance

- **Use** a `RadioGroup` for **exactly one of 2–~7 mutually exclusive, all-visible options** where seeing them all aids the decision (shipping speed, plan tier, yes/no-with-nuance).
- **Don't use** for: **any-number** selection (→ Checkbox); a binary on/off **setting that applies immediately** (→ Switch); **one-of-many past ~5–7 options** or where vertical space is tight (→ Select — collapses the list; see select); a **dense, toggle-like** exclusive choice (→ Segmented Control / Connected Button Group — same semantics, compact horizontal presentation, for view switches and short option sets); or an **action** (→ Button).
- **Decision frameworks:**
  - **Radio vs. Checkbox is exactly-one-vs-any-number.** A pair of radios ("Yes"/"No") is right for a required exclusive choice; never model an exclusive choice as two checkboxes.
  - **Radio vs. Select is exposed-vs-collapsed** — radios when the options should be visible and compared (~≤5–7); Select when the list is long or space-constrained (see select §5).
  - **Radio vs. Segmented Control** is presentation, not semantics — segmented for compact, frequent, view-switch-style choices; radio for standard form options with descriptions.
  - **Default selection:** pre-select when a safe recommended default exists; start empty only when the user must choose deliberately — and then provide an explicit "None" option if "no choice" is a valid end state (because no-deselect, §4).

## 6. Accessibility

Inherits the substrate and the checkbox group-context principle (see checkbox §6). Radio-specific, and the keyboard model is the headline:

- **The radiogroup ARIA pattern** — a container with `role="radiogroup"` (or native `<fieldset>`; the practice defaults to `role="radiogroup"` + `aria-labelledby` for the same CSS-layout reason as checkbox §6) wrapping options with `role="radio"` + `aria-checked`. Native `<input type="radio">` with a shared `name` gives all of this plus the keyboard model for free and is the baseline.
- **The keyboard model is the key difference from checkbox:** the group is a **single tab stop** (roving tabindex — only the selected, or first, radio is tabbable). **Arrow keys (Up/Down/Left/Right) move focus between options *and* select them** (selection-follows-focus, the APG default for radios), wrapping at the ends; Home/End optional; Space selects the focused option if not already selected. This is the opposite of checkbox (Tab-to-each + Space-only). Getting it wrong — making each radio a tab stop — is the most common radio a11y failure.
- **Selection-follows-focus has a cost:** if `onChange` is expensive (a network call, a re-render of dependent UI) or the group is large, arrowing fires it on every step. The mitigation is to keep `onChange` cheap, or — rarely — decouple focus from selection (requiring Space to commit), which deviates from the APG default and should be a deliberate, documented exception.
- **The group label is mandatory for meaning** — without the `radiogroup` name (fieldset/legend or `aria-labelledby`), a screen-reader user hears orphaned radios ("radio button, 1 of 3") with no idea what the choice is about. Group-level error/required associate to the group and announce once.
- **WCAG SCs:** 1.3.1 (group structure), 3.3.1/3.3.2 (group error/labels), 1.4.11/2.4.13 (control focus + boundary contrast), 4.1.2 (role/checked), 2.5.8 (target size — the whole row, as checkbox §6).

## 7. Content guidelines

- **Option labels: parallel, mutually exclusive, scannable** — the same grammatical shape ("Standard shipping", "Express shipping"), no overlap that makes two options both apply. Sentence case; descriptions carry the per-option detail/price.
- **Group label names the decision** ("Shipping method"); abstract shared words up so options don't repeat them (checkbox §7).
- **Error copy is group-level** ("Select a shipping method") and follows SC 3.3.3.
- **Two options only?** If they're truly binary on/off, consider a Switch; if they're two named alternatives ("Card" / "Bank transfer"), radios are right.

## 8. Motion and transition

The select transition is the signature micro-motion — the dot/disc scales/fades in as the option becomes selected (~100–150ms, eased), and the previously-selected option's dot fades out (the exclusivity made visible). Under `prefers-reduced-motion: reduce`, snap the dot; the selection change stays instant. No layout motion. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

Inherits checkbox i18n (see checkbox §9): RTL mirrors the row (control to the reading-start side via logical properties); the disc glyph is symmetrical so mirroring is moot; labels wrap with top/baseline alignment holding the control to the first line; group labels/errors expand like any string. Horizontal radio groups should wrap or reflow under expansion rather than overflow. (See 13-internationalization-and-rtl.)

## 10. Naming

The control is universally **`Radio`** / `RadioButton`; the group **`RadioGroup`** (Spectrum/React Aria, Atlassian, Primer, Carbon) or Polaris's `ChoiceList` (the same component it uses for checkbox groups, single-select mode). **The practice default: `RadioGroup`** (the mandatory unit of use) **+ `Radio`** (the option) **+ `Radio.Control`** (the atomic primitive). Aliases to map: `RadioButton`, `Option`, `ChoiceList`, `<input type="radio">`.

## 11. Implementation notes

- **The group owns the shared `name` and the single value** — children must not set their own `name` (that would break exclusivity) or their own checked state; they read selection from group context (React Aria's `RadioGroupContext`/`useRadioGroupState` is the reference, mirroring checkbox §11 but with a scalar value, not an array).
- **Roving tabindex** — only one radio in the group is `tabindex="0"` (the selected one, or the first if none selected); the rest are `tabindex="-1"`, and arrow handling moves both focus and the `0`. Native radios with a shared `name` do this for free — another argument for the styled-native-input approach (checkbox §11).
- **Controlled/uncontrolled** — a single scalar `value`/`defaultValue` on the group; the controlled-without-onChange and string↔undefined traps from text-field apply.
- **No-deselect is native behaviour** — don't add code to toggle a radio off on re-click; if "none" must be reachable, add an explicit option.
- **`Radio.Control` nesting** — same as checkbox, but the host collection must enforce single-selection and act as the radiogroup (the collection owns the single selected id). Don't nest a `RadioGroup` inside a single-select list — the list is the group.
- **Form value** — the group submits the single selected `value` under the shared `name`; an unselected group submits nothing.

## 12. Related and alternative components

- **Composes with:** Label, Description, FieldError, Form — and the decomposition relationship: **`Radio` composes into `RadioGroup`** (mandatory); **`Radio.Control`** composes into single-select collection rows.
- **Alternative to:** Checkbox/CheckboxGroup (any-number), Switch (immediate on/off), Select (collapsed single-select past ~5–7 — see select), Segmented Control / Connected Button Group (compact exclusive choice), ToggleButtonGroup (single-select pressed buttons).
- **Supersedes:** a set of checkboxes misused for an exclusive choice; a bare `<input type=radio>` set without a group label.
- **Superseded by:** Select when the option count grows; Segmented Control when the presentation should be compact/toggle-like.

(Inherits the selection-control decomposition and nesting POV from checkbox; Switch refines it further (no group). See select for the exposed-vs-collapsed boundary; 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **Group as the mandatory first-class component** (owning `name` + single value + validation) is now standard — the bare radio is understood as an incomplete unit.
2. **Styled native inputs + shared `name`** for free roving tabindex and exclusivity, over hand-rolled `role=radio` div groups.
3. **`role="radiogroup"` + `aria-labelledby`** over `fieldset`/`legend`, same CSS-layout driver as checkbox.
4. **Segmented Control split out** as a distinct presentation of the same semantics — and Material 3 pushing Connected Button Groups for the compact exclusive-choice case, narrowing where classic radios are reached for.
5. **Selection-follows-focus** affirmed as the APG default, with the expensive-onChange caveat better understood.

## 14. Sources cited

(Conservative; reconcile with external pass.) Adobe Spectrum / React Aria `RadioGroup` + `Radio` (`useRadioGroupState`, single value, roving focus) (2024–2025); IBM Carbon `RadioButton` + `RadioButtonGroup` (2024); Shopify Polaris `RadioButton` / `ChoiceList` (2024); GitHub Primer `Radio` + `RadioGroup` (2024); Atlassian `Radio` + `RadioGroup` (2024); Google Material 3 radio button + Compose (2024); Base Web `Radio` + `RadioGroup` (2024); Apple HIG / Material Compose (2024); WAI-ARIA APG Radio Group pattern (roving tabindex, selection-follows-focus); WCAG 2.2 (Oct 2023) — 1.3.1, 3.3.1/2, 1.4.11, 2.4.13, 4.1.2, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: radio
  name: Radio
  aliases: [radio-button, radio-group, option, choice-list]
  category: form
  status: stable
description: >
  Control for choosing EXACTLY ONE from a small set of mutually
  exclusive, all-visible options. The group is MANDATORY — a lone radio
  is meaningless. Not any-number (checkbox), not immediate on/off
  (switch), not collapsed single-select (select) or compact (segmented
  control). Components: Radio (option) + RadioGroup (mandatory owner) +
  Radio.Control (atomic primitive).
anatomy:
  decomposition:
    inherits: checkbox   # control / labelled-row / group + Radio.Control as the nestable primitive (see checkbox §2)
    radio-difference: >
      RadioGroup is the MANDATORY unit of use (never ship a bare Radio),
      vs CheckboxGroup which is reached for only when a set needs it. When
      Radio.Control is nested in a collection, the collection must be
      SINGLE-selection and IS the radiogroup (owns the single selected
      id) — don't nest a RadioGroup inside a single-select list.
    glyph: "disc/dot; NO indeterminate glyph"
  parts: [control, dot-glyph, label, description, inline-error, group-label, group-description, group-error, layout-container]
api:
  inherits: [text-field, checkbox]   # field substrate + checkbox row shape (rich-content label, description, top-baseline alignment, native naming)
  group:
    - {name: name, type: string, required: true, description: shared HTML name binding the exclusive set; the GROUP owns it — children never set their own}
    - {name: value/defaultValue/onChange, type: scalar, description: SINGLE selected value (NOT an array — the checkbox-group contrast); group owns selection}
    - {name: label, type: node, required: true, description: shared group label — options are meaningless without it}
    - {name: isRequired, type: boolean, default: false}
    - {name: isInvalid/errorMessage, type: boolean/node, description: GROUP-level, announced once}
    - {name: orientation, type: enum, values: [vertical, horizontal], default: vertical}
  option:
    - {name: value, type: string, required: true, description: this option's identity in the group; selection = (value == group.value)}
    - {name: label, type: node, required: false}
    - {name: description, type: node, required: false}
    - {name: isDisabled, type: boolean, default: false}
    - {name: "checked/onChange", type: "—", description: "NOT on the option — selection derived from group context (key difference from checkbox)"}
  default-selection: "pre-select a defaultValue when a safe recommended default exists; start empty only for deliberate required choices — but empty is a one-way door (no-deselect), so add an explicit 'None' option if 'no choice' is valid"
states:
  inherits: checkbox   # rest, hover, focus-visible, pressed, disabled, error, read-only
  radio-specific: [selected, no-deselect, no-indeterminate]
  notes:
    no-deselect: "activating a selected radio does NOT unselect it (unlike checkbox); only a sibling (or explicit None) changes the value"
    error: "group-level only, never per-option"
variants:
  size: [small, medium, large]
  group: {orientation: [vertical, horizontal], density: [comfortable, compact]}
accessibility:
  inherits: [text-field, checkbox]
  wcag-criteria: ["1.3.1", "3.3.1", "3.3.2", "1.4.11", "2.4.13", "4.1.2", "2.5.8"]
  pattern: "native <input type=radio> + shared name (baseline) | role=radiogroup + aria-labelledby (default over fieldset/legend) wrapping role=radio + aria-checked"
  keyboard-model:
    tab: "the GROUP is a SINGLE tab stop (roving tabindex) — opposite of checkbox's tab-each"
    arrows: "Up/Down/Left/Right move focus AND select (selection-follows-focus, APG default), wrapping; Home/End optional"
    space: "selects the focused option if not already selected"
  selection-follows-focus: "APG default; caveat — expensive onChange fires per arrow step; keep onChange cheap, or decouple (Space to commit) as a documented exception"
  group-label: "mandatory for meaning — without it, orphaned 'radio, 1 of 3' announcements"
content:
  option-label-pattern: "parallel, mutually exclusive, scannable, sentence case; per-option detail in description"
  group-label-pattern: "names the decision ('Shipping method'); abstract shared words up"
  error-pattern: "group-level ('Select a shipping method'); SC 3.3.3"
motion:
  select-transition: "~100-150ms dot scale/fade in; previous dot fades out (exclusivity made visible)"
  reduce-motion: "snap the dot; selection stays instant"
i18n:
  inherits: checkbox   # RTL row mirror via logical props; top-baseline alignment holds control to first line; expansion
  radio-specific: "disc glyph symmetrical (mirroring moot); horizontal groups wrap/reflow under expansion"
implementation:
  - "group owns the shared name + single scalar value; children read selection from group context (RadioGroupContext/useRadioGroupState), set NEITHER name NOR checked"
  - "roving tabindex: one radio tabindex=0 (selected or first), rest -1; arrows move both focus and the 0 — native radios + shared name do this free"
  - "no-deselect is native — don't add toggle-off code; add an explicit 'None' option if needed"
  - "Radio.Control nesting: host collection must be single-select and IS the radiogroup; don't nest RadioGroup in the list"
  - "form value: group submits the single value under the shared name; unselected group submits nothing"
composition:
  composes-with: [label, description, field-error, form]
  decomposition-relationship: "Radio composes into RadioGroup (MANDATORY); Radio.Control composes into single-select collection rows"
  alternative-to: [checkbox-group, switch, select, segmented-control, toggle-button-group]
  supersedes: ["checkboxes misused for an exclusive choice", "bare <input type=radio> set without a group label"]
  superseded-by: ["select when option count grows past ~5-7", "segmented control when presentation should be compact"]
notes:
  contested:
    - "default selection: pre-select a recommended default vs start empty (one-way door without an explicit None)"
    - "selection-follows-focus (APG default) vs decoupled selection for expensive onChange"
    - "role=radiogroup + aria-labelledby vs fieldset/legend (role=radiogroup default)"
  inherited: "the selection-control decomposition + nesting POV from checkbox; group MANDATORY is the radio difference"
  evolution: "group as mandatory first-class; styled native input + shared name; role=radiogroup over fieldset; segmented control split out"
```

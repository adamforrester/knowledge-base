---
okf_version: "0.1"
type: component-brief
title: Radio
description: The Checkbox decomposition with one structural mutation — the group is mandatory. A field-truth study that confirms the inherited control/group/atomic-primitive model (RadioGroup owns name + single value + validation), resolves the roving-tabindex keyboard model and the contested selection-follows-focus question, and covers no-deselect, the default-selection decision, and the radio-vs-segmented-control / radio-vs-select boundaries, with the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [radio-button, radio-group, option, choice-list]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Radio

> Radio is the Checkbox decomposition with one mutation that changes everything: **the group is mandatory.** A lone checkbox is a valid control (a consent box); a lone radio is meaningless — it only means "one of these," and needs siblings and a shared `name` to mean anything at all. Both research passes inherited the Checkbox selection-control decomposition without argument and spent themselves on what that mutation forces: the group owns the value, the keyboard model collapses to a single tab stop with arrow-selection, and — uniquely — you cannot deselect a radio. This brief confirms the inherited structure and resolves the radio-specific calls, including the one genuine fork the field is split on: whether selection follows focus.

---

## 1. Framing

A Radio is a control for choosing **exactly one** from a small set of **mutually exclusive, all-visible** options. Its defining property, traceable to the earliest HTML, is that it has **no validity in isolation** — its identity is predicated on plurality (external's framing, and both passes converge). That forces the inherited decomposition's one mutation: the group is elevated from *optional organiser* (CheckboxGroup) to *mandatory functional controller* (RadioGroup), owning the shared `name`, the single value, and validation.

What it *isn't*: any-number selection (Checkbox), an on/off setting that applies immediately (Switch), the same single-select collapsed (Select, past ~5–7 options) or in a denser horizontal skin (Segmented Control), or an action (Button). The analogous components — inherited from checkbox §2 — are **`Radio`** (the labelled option), **`RadioGroup`** (the mandatory owner), and **`Radio.Control`** (the nestable atomic primitive). Where systems disagree: the options-array-vs-composition API, the roving-tabindex-vs-`aria-activedescendant` focus model, and — the live one — selection-follows-focus vs. explicit selection (§6).

## 2. Anatomy and parts

Inherits the Checkbox decomposition wholesale (control / labelled row / group, with the atomic primitive as the nestable unit for hosts — see checkbox §2). The difference is **emphasis, not structure**: `RadioGroup` is the *unit of use*, never optional. You ship a `RadioGroup` containing `Radio`s; you never ship a bare `Radio`. Named parts mirror checkbox (control + label + description + inline error; group label/description/error + layout container), with a **disc/dot glyph** replacing the checkmark and **no indeterminate glyph**. The nesting POV carries over verbatim (checkbox §2): a selectable card or list row embeds `Radio.Control`, the host supplies the accessible name and hit target, and the enclosing **single-select** collection *is* the radiogroup (external confirms: "selectable tiles must secretly embed the atomic Radio.Control").

## 3. Properties / API

Inherits the form-field substrate and the checkbox row shape (rich-content label, description, disabled, top-baseline alignment, native naming — see checkbox §3). The radio-specific weighting puts the state on the group:

**`RadioGroup` (the mandatory owner):**
- `name` — the shared HTML name enforcing mutual exclusivity at the browser level; the group owns it, children never set their own (doing so breaks exclusivity).
- `value` / `defaultValue` / `onChange` — a **single scalar**, not an array (the CheckboxGroup contrast). The group is the sole arbiter of selection; `onChange` fires with the newly selected value.
- `label` — the shared group label; options are meaningless without it (§6).
- `isRequired`, `isInvalid`/`errorMessage`, `description` — group-level, cascading.
- `orientation` — vertical (default) / horizontal.

**`Radio` (the option):**
- `value` — required; this option's identity in the group. Selection is *derived*: `checked = (group.value === props.value)`.
- `label`, `description`, `isDisabled` — per-option.
- **No `checked`/`onChange`/`name` on the option** — it reads selection from group context and dispatches the group's callback (§11). This is the sharpest API difference from checkbox, where a standalone box owns its own boolean.

**The options-array vs. composition fork** (external's clearest API finding): the *Configuration* pattern passes `options={[{label, value}]}` (Atlassian, Fluent v8 `ChoiceGroup`) — terse and layout-safe, but a bottleneck the moment an option needs a thumbnail, tooltip, or rich description. The *Composability* pattern renders `<Radio>` children inside `<RadioGroup>` (Primer, Fluent **v9 — which deprecated its array `ChoiceGroup` for exactly this reason**, Spectrum, Base Web). **The practice defaults to composition**, binding children via context — consistent with the checkbox value-array-via-context model (§11), differing only in scalar-vs-array.

**The default-selection decision** is a real call (§5): a `RadioGroup` may pre-select a `defaultValue` or start empty. The modern consensus (Carbon, Windows) — which the practice adopts — is **start empty to force a deliberate choice**, with focus landing safely on the first option; pre-select only when a genuinely safe recommended default exists. But empty is a *one-way door* (no-deselect, §4), so an optional group that allows "no choice" must include an explicit "None" option.

## 4. States and variants

Inherits checkbox runtime states (rest/hover/focus-visible/pressed/disabled/error/read-only — see checkbox §4), with three radio-specific differences:

| State | Radio-specific contract |
| --- | --- |
| selected | the disc fills; **exactly one per group** |
| **no-deselect** | activating a *selected* radio does nothing — there is no toggle-off. The only way out of a value is selecting a sibling (or an explicit "None"). The most-felt behavioural difference from checkbox, and the source of the optional-form trap (§5). |
| **no indeterminate** | a mutually-exclusive choice has no partial state — radio simply has no mixed glyph (the clean contrast with checkbox) |
| error | group-level only ("Select an option"), never per-option |

**Variants:** `size`; group **orientation** (vertical default — and strongly preferred for scannability and safe text wrapping; horizontal only for few short options, with strict spacing to avoid ambiguous label association); density (touch targets hold to 44/48 on mobile). The presentation axis is where Radio meets **Segmented Control** — the same single-select *intent*, different skin — though, per the segmented-control brief, a *different a11y model* (a true immediate-switch segmented is `role=group` + `aria-current`, not a `radiogroup`; see segmented-control §6). No tone/emphasis. A frontier note: Carbon's "AI presence" variant embeds an AI-explainability label beside a recommended option (a dual-action row needing careful focus management so AT doesn't conflate the explainer button with the radio) — the same AI-presence signal flagged on text-field/select; a watch item, not a default.

## 5. Usage guidance

- **Use** a `RadioGroup` for **exactly one of 2–~7 mutually exclusive, all-visible options** where seeing them all aids the decision (shipping method, plan tier).
- **Don't use** for: **any-number** selection (→ Checkbox); a binary **on/off that applies immediately** (→ Switch — and never two radios for a true/false toggle); **one-of-many past ~5–7** or tight vertical space (→ Select, the collapsed alternative — see select); a **dense, frequent, toggle-like** exclusive choice (→ Segmented Control / Connected Button Group); or an **action** (→ Button).
- **Decision frameworks:**
  - **Radio vs. Checkbox is exactly-one-vs-any-number** — never model an exclusive choice as multiple checkboxes.
  - **Radio vs. Select is exposed-vs-collapsed** (~≤5–7 visible vs. long/space-constrained — see select §5).
  - **Radio vs. Segmented Control is immediate-vs-deferred + density** — segmented for compact view-switches that take effect now (and so carries a different a11y model — see segmented-control §6); radio for standard form options with descriptions, committed on submit.
  - **The optional-group rule:** because of no-deselect, an *optional* radio group must provide an explicit "None"/"N/A" option — otherwise a stray click permanently pollutes the data and can't be undone. If a "None" option corrupts the data model, the choice belongs in a clearable Select instead. (Worth a lint/console warning when an optional group lacks a null option — external.)
  - **Default selection:** start empty to force a deliberate choice; pre-select only a genuinely safe default.

## 6. Accessibility

Inherits the substrate and the checkbox group-context principle (see checkbox §6). The keyboard model is the headline, and it is the **opposite of checkbox**:

- **The radiogroup pattern:** a container with `role="radiogroup"` (or native `<fieldset>`/`<legend>`; the practice defaults to `role="radiogroup"` + `aria-labelledby` for the same CSS-layout reason as checkbox §6) wrapping options with `role="radio"` + `aria-checked`. Native `<input type="radio">` sharing a `name` gives the grouping, exclusivity, *and* the keyboard model for free — the baseline, and another argument for the styled-native-input approach (§11).
- **Single tab stop + arrow navigation via roving tabindex.** Tab moves *into* the group and the next Tab moves *out*; within the group, **arrow keys** move between options. Implement with **roving tabindex** (one radio `tabindex="0"` — the selected one, or the first if none; siblings `-1`; arrow handling moves both focus and the `0` and calls `.focus()`), the APG/React-Aria/Carbon standard — over `aria-activedescendant`, which is more verbose and synchronization-bug-prone. Home/End jump to first/last; focus **wraps** at the ends. Making each radio its own tab stop is the most common radio a11y failure.
- **Selection-follows-focus — the contested call, resolved.** The APG permits arrowing to both move focus *and* select; native radios do exactly this. The external pass argues for **explicit selection** as the default (arrow moves, Space selects), citing the screen-reader-exploration trap (arrowing to hear options fires `onChange` on every step) and Windows' gamepad behaviour (which disables follows-focus). **The practice defaults to selection-follows-focus** — it is native `<input type=radio>` behaviour and the APG default, and the catalogue's standing principle is to keep native semantics rather than reimplement them (checkbox §11, the styled-native-input stance). The exploration-fires-`onChange` problem is real but is better solved by **keeping radio `onChange` cheap** — a radio selection should never trigger navigation or expensive work; if it must, that is the signal to *decouple selection from focus as a documented exception* (or reconsider the control). So: follows-focus by default, explicit-selection as a deliberate, documented opt-out for the rare unavoidable-expensive case — with the external pass's contrary default recorded as a legitimate position.
- **The group label is mandatory for meaning** — without it, AT announces orphaned "radio button, 1 of 3" with no idea what the choice is; group error/required associate to the group and announce once.
- **WCAG SCs:** 1.3.1 (group structure), 3.3.1/3.3.2 (group error/labels), 1.4.11/2.4.13 (focus + boundary contrast), 4.1.2 (role/checked), 2.5.8 (target size — the whole row, as checkbox §6).

## 7. Content guidelines

- **Group label names the decision or asks the question** — "Shipping method" / "How should we contact you?"; may be visually hidden if an enclosing labelled section already frames it, but must stay programmatically present.
- **Option labels: parallel, mutually exclusive, scannable** — same grammatical shape, brief, sentence case, no terminal punctuation, no overlap that makes two options both apply; per-option detail/price goes in the description. Long labels **wrap** (never ellipsis-truncate) and align under the text with the control top-anchored (inherited, checkbox §7).
- **Error copy is group-level and specific** ("Select a preferred contact method," not "Invalid input" — SC 3.3.3).

## 8. Motion and transition

The select transition is the signature micro-motion — a spring/scale-up of the inner dot with a border-colour crossfade (~100–150ms); selecting a sibling animates the previous dot *out* (exclusivity made visible), the one exit animation a radio has (it never animates out on its own, since it can't be deselected). **The focus ring must appear instantly** — fading it lags rapid arrow navigation. Under `prefers-reduced-motion: reduce`, snap the dot via opacity/colour only. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

Inherits checkbox i18n (see checkbox §9): RTL mirrors the row (control to the reading-start side via logical properties); the disc glyph is symmetrical so mirroring is moot; labels wrap with the control top-anchored. **Vertical orientation is strongly preferred** in part for i18n — horizontal radio rows are fragile under text expansion (German up to ~300%), prone to clipping and ambiguous label proximity; vertical stacking wraps safely. (See 13-internationalization-and-rtl.)

## 10. Naming

The control is universally **`Radio`** / `RadioButton`; the group **`RadioGroup`** (Spectrum/React Aria, Atlassian, Primer, Carbon, and Fluent v9 after deprecating `ChoiceGroup`), or Polaris's **`ChoiceList`** (the same polymorphic component it uses for checkbox groups — an abstraction the external pass flags as friction, since it historically used a `selected` prop over native `checked`, breaking form-lib integration). **The practice default: `RadioGroup`** (the mandatory unit of use) **+ `Radio`** (the option) **+ `Radio.Control`** (the atomic primitive) — DOM-aligned, no clever abstraction. Aliases to map: `RadioButton` (Compose/older Material), `Option`, `ChoiceList`, `<input type="radio">`.

## 11. Implementation notes

- **The group owns `name` + the single scalar value; children read from context.** `RadioGroup` broadcasts `name`, `value`, and `onChange` via context (React Aria's `useRadioGroupState`/`RadioGroupContext` is the reference); each `Radio` computes `checked = (context.value === props.value)` and fires `context.onChange(props.value)` — so arbitrary layout, tooltips, or grid columns can sit between group and option without severing state. Same mechanism as checkbox §11, scalar instead of array.
- **Roving tabindex + focus restoration trap:** only one radio is `tabindex="0"`. When focus is routed back to the group (a validation error, a legend click), **focus the *checked* radio, not blindly the first** — query for the checked element; if none, focus the first non-disabled option (external). Native radios + a shared `name` do roving tabindex for free.
- **No-deselect is native** — don't add toggle-off code; add an explicit "None" option if "no choice" must be reachable (§5).
- **`Radio.Control` nesting** — the host collection must enforce single-selection and *be* the radiogroup; don't nest a `RadioGroup` inside a single-select list.
- **Mobile (Jetpack Compose):** put the click/selectable on the *row*, not the dot — `Modifier.selectableGroup()` on the parent, `Modifier.selectable(role = Role.RadioButton)` on the Row, and `onClick = null` on the `RadioButton` itself, or you get double-firing and duplicated AT announcements (external — the mobile analogue of the whole-row hit target).
- **Form value** — the group submits the single value under the shared `name`; an unselected group submits nothing.

## 12. Related and alternative components

- **Composes with:** Label, Description, FieldError, Form, Tile/Card (which embeds `Radio.Control` for rich selectable options) — and the decomposition relationship: **`Radio` composes into `RadioGroup`** (mandatory); **`Radio.Control`** composes into single-select collection rows.
- **Alternative to:** Checkbox/CheckboxGroup (any-number — see checkbox), Switch (immediate on/off — see switch), Select (collapsed single-select past ~5–7 — see select), Segmented Control / Connected Button Group (compact exclusive choice), ToggleButtonGroup (single-select pressed buttons).
- **Supersedes:** a set of checkboxes misused for an exclusive choice; a bare `<input type=radio>` set without a group label.
- **Superseded by:** Select when the option count grows past ~5–7; Segmented Control when the presentation should be compact/toggle-like.

(Inherits the selection-control decomposition and nesting POV from checkbox; Switch refines it further — *no* group. See select for the exposed-vs-collapsed boundary; 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **The group as the mandatory first-class component** (owning `name` + single value + validation) is now standard; the bare radio is understood as an incomplete unit.
2. **The demise of the options-array** — composition (`<RadioGroup>` wrapping `<Radio>`) has all but won; Fluent v9 deprecating its array `ChoiceGroup` for a composable `RadioGroup` is the marker.
3. **Styled native inputs + a shared `name`** for free roving tabindex and exclusivity, over hand-rolled `role=radio` div groups; and **`role="radiogroup"` + `aria-labelledby`** over `fieldset` (CSS-layout driver, checkbox §6).
4. **Segmented Control / Connected Button Groups split out** as a distinct compact presentation of the same semantics (Material 3), narrowing where classic radios are reached for.
5. **Selection-follows-focus** affirmed as the APG/native default, with the expensive-`onChange` caveat now well understood (§6) — and **AI-presence** recommendation styling (Carbon) emerging at the frontier (§4).

## 14. Sources cited

Conservative dating (the external pass supplied precise, largely 2024–2026 versions — Spectrum/React Aria v3.31+, Primer React v36+, Carbon v11 (2026), Fluent v9, Base Web v13/14+, Material 3 web v2.5/Compose v1.4+, Polaris v12 — held loosely; the Polaris/Material Web-Components migration is the same cross-brief unverified claim flagged on Button/Text Field; `last-audited` is the re-run trigger):

- Adobe Spectrum / React Aria — `RadioGroup` + `Radio`, `useRadioGroupState`, roving-tabindex/arrow-wrap utilities (Spectrum, 2024–2025).
- IBM Carbon — `RadioButton` + `RadioButtonGroup`, the no-default-selection stance, AI-presence variant (Carbon, 2024–2026).
- GitHub Primer — `Radio` + `RadioGroup` (`RadioGroup.Caption`/`.Validation`), `FormControl`, context binding (Primer, 2024–2025).
- Microsoft Fluent UI v9 — composable `RadioGroup` replacing the deprecated array `ChoiceGroup` (Fluent, 2024).
- Atlassian Design System — `Radio` + `RadioGroup`, the legacy options-array and "None"-option friction (Atlassian, 2024–2025).
- Shopify Polaris — `RadioButton` / `ChoiceList` (the `selected`-vs-`checked` friction); the (unverified) `<s-choice-list>` Web Components move (Polaris, 2025–2026).
- Uber Base Web — `Radio` + `RadioGroup`, the `RadioMarkOuter`/`RadioMarkInner` overrides (Base Web, 2024).
- Google Material 3 — `md-radio`, density tokens, Compose mobile (Material 3, 2024–2025).
- Apple HIG / Windows (WinUI) — target size; the gamepad/explicit-selection-vs-follows-focus distinction (2024–2026).
- WAI-ARIA APG — Radio Group pattern (roving tabindex, selection-follows-focus, wrap-around).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.3.1, 3.3.1, 3.3.2, 1.4.11, 2.4.13, 4.1.2, 2.5.8.

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
  (switch), not collapsed (select) or compact (segmented control).
  Components: Radio (option) + RadioGroup (mandatory owner) + Radio.Control
  (atomic primitive).
anatomy:
  decomposition:
    inherits: checkbox   # control / labelled-row / group + Radio.Control as the nestable primitive + the nesting POV (see checkbox §2)
    radio-difference: >
      RadioGroup is the MANDATORY unit of use (never ship a bare Radio),
      vs CheckboxGroup which is optional. When Radio.Control is nested in a
      collection, the collection must be SINGLE-selection and IS the
      radiogroup — don't nest a RadioGroup inside the list.
    glyph: "disc/dot; NO indeterminate glyph"
  parts: [control, dot-glyph, label, description, inline-error, group-label, group-description, group-error, layout-container]
api:
  inherits: [text-field, checkbox]   # field substrate + checkbox row shape (rich-content label, description, top-baseline alignment, native naming)
  pattern: "COMPOSITION (<RadioGroup> wrapping <Radio> children via context) over the legacy options-array; Fluent v9 deprecated its array ChoiceGroup for this"
  group:
    - {name: name, type: string, required: true, description: shared HTML name enforcing exclusivity; the GROUP owns it — children never set their own}
    - {name: value/defaultValue/onChange, type: scalar, description: SINGLE selected value (NOT an array — the checkbox-group contrast); group is sole arbiter}
    - {name: label, type: node, required: true, description: shared group label — options meaningless without it}
    - {name: isRequired, type: boolean, default: false}
    - {name: isInvalid/errorMessage, type: boolean/node, description: GROUP-level, announced once}
    - {name: orientation, type: enum, values: [vertical, horizontal], default: vertical}
  option:
    - {name: value, type: string, required: true, description: this option's identity; checked = (group.value == value)}
    - {name: label, type: node, required: false}
    - {name: description, type: node, required: false}
    - {name: isDisabled, type: boolean, default: false}
    - {name: "checked/onChange/name", type: "—", description: "NOT on the option — selection derived from group context (key difference from checkbox)"}
  default-selection: "start EMPTY to force a deliberate choice (Carbon/Windows consensus); pre-select only a genuinely safe default. Empty is a one-way door (no-deselect) — add an explicit 'None' option if 'no choice' is valid"
states:
  inherits: checkbox   # rest, hover, focus-visible, pressed, disabled, error, read-only
  radio-specific: [selected, no-deselect, no-indeterminate]
  notes:
    no-deselect: "activating a selected radio does NOTHING (unlike checkbox); only a sibling (or explicit None) changes the value"
    error: "group-level only, never per-option"
variants:
  size: [small, medium, large]
  group: {orientation: [vertical, horizontal], density: [comfortable, compact]}
  frontier: [ai-presence]   # Carbon recommendation styling; dual-action row, not a default
accessibility:
  inherits: [text-field, checkbox]
  wcag-criteria: ["1.3.1", "3.3.1", "3.3.2", "1.4.11", "2.4.13", "4.1.2", "2.5.8"]
  pattern: "native <input type=radio> + shared name (baseline) | role=radiogroup + aria-labelledby (default over fieldset/legend) wrapping role=radio + aria-checked"
  keyboard-model:
    tab: "the GROUP is a SINGLE tab stop (roving tabindex) — opposite of checkbox's tab-each"
    arrows: "move focus between options, wrapping at ends; Home/End to first/last"
    space: "selects the focused option"
    implementation: "roving tabindex (one radio tabindex=0, rest -1; arrow moves focus + the 0 + .focus()) over aria-activedescendant (verbose, sync-bug-prone)"
  selection-follows-focus:
    practice-default: "FOLLOWS FOCUS — native <input type=radio> behaviour + APG default; keep onChange cheap (a radio must never trigger navigation/expensive work)"
    exception: "decouple (Space to commit) as a documented opt-out for unavoidable-expensive cases; the external pass argued explicit-by-default — recorded as legitimate"
  group-label: "mandatory for meaning — without it, orphaned 'radio, 1 of 3' announcements"
content:
  group-label-pattern: "names the decision / asks the question ('Shipping method'); may be visually hidden but programmatically present"
  option-label-pattern: "parallel, mutually exclusive, brief, sentence case, no terminal punctuation; detail in description; wraps (no ellipsis), control top-anchored"
  error-pattern: "group-level + specific ('Select a preferred contact method'); SC 3.3.3"
motion:
  select-transition: "~100-150ms dot scale/fade in; selecting a sibling animates the previous dot OUT (the only exit a radio has); focus ring appears INSTANTLY"
  reduce-motion: "snap the dot (opacity/colour only)"
i18n:
  inherits: checkbox   # RTL row mirror via logical props; control top-anchored; disc glyph symmetrical (mirroring moot)
  radio-specific: "vertical orientation strongly preferred — horizontal rows fragile under expansion (de ~300%); vertical wraps safely"
implementation:
  - "group owns shared name + single scalar value via context (useRadioGroupState/RadioGroupContext); option computes checked=(context.value==value), fires context.onChange — sets NEITHER name NOR checked"
  - "roving tabindex; on focus-restore to the group, focus the CHECKED radio, not blindly the first (else first non-disabled); native radios + shared name do this free"
  - "no-deselect is native — don't add toggle-off; add explicit 'None' if needed"
  - "Radio.Control nesting: host collection single-select and IS the radiogroup; don't nest RadioGroup in the list"
  - "Jetpack Compose: selectable on the ROW (Modifier.selectableGroup() parent + Modifier.selectable(role=RadioButton) Row + onClick=null on RadioButton) to avoid double-fire/AT duplication"
  - "form value: group submits the single value under the shared name; unselected group submits nothing"
composition:
  composes-with: [label, description, field-error, form, tile, card]
  decomposition-relationship: "Radio composes into RadioGroup (MANDATORY); Radio.Control composes into single-select collection rows / selectable tiles"
  alternative-to: [checkbox-group, switch, select, segmented-control, toggle-button-group]
  supersedes: ["checkboxes misused for an exclusive choice", "bare <input type=radio> set without a group label"]
  superseded-by: ["select when option count grows past ~5-7", "segmented control when presentation should be compact"]
notes:
  contested:
    - "selection-follows-focus (practice default, native-aligned) vs explicit selection (external argued; legitimate for expensive onChange) — resolved to follows-focus + documented opt-out"
    - "default selection: start empty (practice) vs always pre-select (legacy)"
    - "options-array vs composition (composition wins)"
    - "role=radiogroup + aria-labelledby vs fieldset/legend (role=radiogroup default)"
  inherited: "the selection-control decomposition + nesting POV from checkbox; group MANDATORY is the radio mutation"
  unverified:
    - "Polaris/Material Web-Components migration (<s-choice-list>/<md-radio>) — shared cross-brief claim; needs _source-text"
    - "external-supplied 2026 version numbers; aria-activedescendant-vs-roving perf in Shadow DOM"
  evolution: "group mandatory first-class; demise of the options-array; styled native input + shared name; role=radiogroup over fieldset; segmented control split out"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-radio/` (15 June 2026), the second of the boolean/choice controls. Both passes inherited the Checkbox selection-control decomposition without dispute and converged on the radio mutation — the group is mandatory (`RadioGroup` owns `name` + single scalar value + validation; a lone `Radio` is meaningless) — plus roving-tabindex single-tab-stop navigation over `aria-activedescendant`, no-deselect with an explicit "None" for optional groups, start-empty default selection, no indeterminate state, composition over the options-array, `role="radiogroup"`+`aria-labelledby` over `fieldset`, and the checkbox/switch/select/segmented-control boundaries. The one genuine fork was **selection-follows-focus vs. explicit selection**: the external pass argued explicit-by-default (the SR-exploration trap, Windows gamepad precedent); the practice resolved to **selection-follows-focus** as the default (native `<input type=radio>` behaviour and the APG default, consistent with the catalogue's style-the-native-input principle), with cheap-`onChange` as the discipline and explicit-selection as a documented opt-out for unavoidable-expensive cases — the external's position recorded as legitimate. External-pass contributions folded in: the options-array-vs-composition history (Fluent v9 deprecating `ChoiceGroup`), the roving-tabindex focus-restoration trap (focus the checked option, not the first), the Jetpack Compose row-selectable pattern, the `ChoiceList` `selected`-vs-`checked` friction, the Carbon AI-presence variant, and the 300%-expansion argument for vertical-default. Claude-pass contributions: the selection-follows-focus resolution and its native-alignment rationale, the explicit framing as the checkbox decomposition + one mutation, and the scalar-vs-array context model. The Polaris/Material Web-Components migration and the 2026 version numbers are flagged unverified pending `_source-text/` backing. Conformant to `components/_schema.md` (inherits checkbox in the decomposition/api/states/i18n keys). Switch closes the batch and refines the decomposition once more — no group at all.*

---
okf_version: "0.1"
type: component-brief
title: Segmented Control
description: The group of the Toggle Button presented as a connected control — and the catalogue's most semantically contested component. A field-truth study that resolves the four-model ARIA fork to a context-dependent default (group + aria-current for the immediate view-switcher; radiogroup only for a deferred form input; aria-pressed for multi-select), the two visual paradigms (track-and-pill vs. connected buttons), the segmented-vs-tabs / -radio / -select boundaries, the 2–5-segment no-overflow rule, disallowEmptySelection, and the sliding-indicator implementation.
tags: [components, form]
category: Form
status: stable
aliases: [segmented-control, toggle-button-group, connected-button-group, content-switcher, segmented-buttons]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Segmented Control

> Segmented Control is the **group of the Toggle Button** worn as a single connected control — and the most semantically contested component in the catalogue, because its physical form (a contiguous horizontal row of options) overlaps with radio groups, tabs, and selects all at once. It inherits the Toggle Button atomic and, for the single-select case, much of Radio's model — but the research forced one sharp correction to a simplification the Radio brief made: a segmented control that switches a view *immediately* should **not** be a `radiogroup`. "Radio" tells a screen-reader user the change is deferred, and selection-follows-focus would mutate the view on every arrow key. The defining work of this brief is resolving that ARIA fork by the control's *purpose*, not its appearance.

---

## 1. Framing

A Segmented Control is a compact, horizontally adjoined set of 2–5 options where the user picks among them and the view responds **immediately** — a value/filter/view switcher (Grid/List, Day/Week/Month, All/Unread). It is built on the **ToggleButtonGroup** primitive (the atomic Toggle Button × N — see toggle-button) and, for single-select, draws on Radio's mutual-exclusivity and data-binding model (see radio). But it is "not merely a reskinned radio group" (external): it is defined by horizontal spatial constraint, **immediate** temporal execution, and a distinct visual composition.

What it *isn't*: a **Radio** group (same single-select *intent*, but standard vertical form presentation and *deferred* submission — §5); **Tabs** (which switch whole *panels* — a disclosure/navigation pattern — §5, the most-violated boundary); a **Select** (the same options *collapsed* — §5); or a lone **Toggle Button** (independent, not a mutually-related set). The contested core is the ARIA fork (§6): four models exist in the field, and the practice resolves them by purpose.

## 2. Anatomy and parts

Inherits the Toggle Button per-segment anatomy (see toggle-button §2). The structure is a **group container** + 2–5 **segments** + a **selected indicator** + (track model only) **dividers**. The field has split into two visual paradigms (external):

- **Track-and-pill (Apple/iOS lineage)** — a master *track* (low-contrast, often inset) housing a floating *pill* indicator that **slides** beneath the active segment; vertical dividers sit between *unselected* segments and disappear adjacent to the selected one (the pill carries the boundary). The "single continuous switch" metaphor.
- **Connected-button (Material 3 "Connected Button Group", which deprecated the older "Segmented Button" in the Expressive update — *verify the 2024/2026 dating*)** — no track, no pill: independent toggle buttons joined at squared inner borders (outer corners rounded), selection shown by the segment's own active fill plus a **checkmark icon that displaces the label**.

**The practice defaults to track-and-pill** as the canonical segmented presentation (the most recognizable "segmented control" look, and the sliding indicator is the signature affordance — §8), with connected-button available as a themed variant; each has distinct implementation costs (§11). Required DOM regardless of skin: a `role="group"`/`role="radiogroup"` container (§6), `<button>` segments, the indicator (a dedicated node in the track model; the segment's own background in the connected model), and dividers (track model only).

## 3. Properties / API

Inherits the form-field substrate where relevant and the Toggle Button segment shape (size, icon/label, per-segment disabled — see toggle-button §3). Segmented-specific:

- **`selectionMode`** — `single` (default) | `multiple`. The practice uses the **explicit string literal** over MUI's `exclusive` boolean — it drives the ARIA model *and* the `value` type, and a literal union lets TypeScript infer the `onChange` payload (scalar vs. array) precisely (external).
- **`value` / `defaultValue` / `onChange`** — scalar for `single`, array for `multiple`; the group owns selection (the radio/checkbox-group context model — see radio §3).
- **`disallowEmptySelection`** (default `true` for the practice) — the **zero-selection trap**: clicking the active segment can deselect it and yield `null`/`[]`, breaking a view that needs an active filter. As a first-class prop, the internal handler ignores clicks on the sole active segment so `onChange` never fires empty (external — React Spectrum's prop; MUI forces a manual guard clause). The practice defaults it on, because a segmented control almost always needs a persistent selection.
- **`size`**, **`fullWidth`** (equal-width across the parent), **`disabled`** (group-level, cascades + removes the group from focus order; per-segment disable also supported — §4).
- Segments as composed `<Segment>` children (icon/label/value) — the composition default (per radio/select).

## 4. States and variants

Two hierarchical levels (external):

- **Group (macro):** `disabled` cascades to all segments and removes the group from focus; per-segment `disabled` is independently supported (disable a subset on permissions while the group stays functional).
- **Segment (micro):** inherits Toggle Button states (rest / hover / focus-visible / pressed / **selected** / disabled — see toggle-button §4), with adjoined-layout caveats: hover must not bleed into adjacent segments (connected model); the focus ring aligns to the track interior (track model) or triggers **z-index elevation** to clear collapsed borders (connected model — §11); `selected` is the pill-in-position (track) or active fill + checkmark (connected).

**Variants:** `size`; **content** — text-only / icon-only / icon+text, and **never mix content types within one group** (Gestalt similarity; all segments conform — external); **sizing** — **equal-width by default** (`flex: 1`, visual equilibrium and predictable targeting) with a content-width fallback (`isIntrinsic`) when equal-width wastes space or under responsive compression; **selectionMode** (single/multiple). The selected indicator (sliding pill) is the signature visual.

## 5. Usage guidance

- **Use** for a compact, exposed switch among **2–5** options (6 for icon-only) that the user toggles frequently and that take effect **immediately**: view switches, short filters, sort modes, time ranges.
- **Don't use** for: standard form one-of-many with descriptions or deferred submit (→ **Radio**); switching whole content **panels** (→ **Tabs**); **>5 text** options or overflow risk (→ **Select**); a single on/off (→ **Switch** / Toggle Button); navigation to new URLs (→ Tabs / Link — Primer explicitly forbids segmented for routing).
- **Decision frameworks (the three contested boundaries):**
  - **Segmented vs. Radio** — *immediate-vs-deferred + density*. Segmented switches the view now and is compact/horizontal; Radio collects form data (deferred to submit) and scans vertically with room for descriptions. If a Save/Apply commits the change, it's Radio (see radio §5).
  - **Segmented vs. Tabs (the most-violated boundary)** — *value-in-place vs. panel-switching*. Tabs (`role=tablist`/`tab`/`tabpanel`) swap whole panels with divergent layouts and data lifecycles (the filing-cabinet metaphor); a segmented control re-sorts/filters/re-visualizes the *same* content context in place. If selecting unmounts the panel for a different interface → Tabs; if it changes a parameter of the current view → Segmented.
  - **Segmented vs. Select** — *exposed-vs-collapsed*. Segmented exposes all options for one-tap switching (max information scent) at a linear horizontal cost; Select collapses them (two taps + a search) to save space. ≤5 and frequently toggled → Segmented; longer or space-constrained → Select.
- **No overflow** — a segmented control never scrolls or wraps on desktop; if it would, it's the wrong component (use Select). Scrollable segments are a mobile-only concession.

## 6. Accessibility — the four-model fork, resolved

There is no native `<segmentedcontrol>`, so the field composes it from disparate ARIA roles, and four models compete (external):

1. **`role="radiogroup"` + `role="radio"` + `aria-checked`** (Material 3, older) — roving tabindex, arrows, selection-follows-focus. *Primer's objection:* "radio" implies a *deferred* choice, so announcing it on a control that mutates the view immediately causes cognitive dissonance — and selection-follows-focus re-renders the view on every arrow.
2. **`role="group"` + `role="button"` + `aria-pressed`** (MUI) — Tab to each segment, Space/Enter toggles, no arrows. Right for multi-select; heavy keyboard friction for single.
3. **`<ul>` + `role="button"` (or `role="link"`) + `aria-current`** (GitHub Primer) — treats it as a list of immediate view-switching commands; clean "list of actions" announcement, Tab navigation, no deferred-selection implication.
4. **`role="tablist"` + `role="tab"`** (IBM Carbon ContentSwitcher) — excellent roving-tabindex ergonomics, but an ARIA-spec mismatch (a tab should own a `tabpanel`; a content switcher filters in place) — Carbon has open issues acknowledging it.

**The practice resolves the fork by purpose, not appearance — and this refines the Radio brief's simplification that "segmented = radiogroup, same a11y tree":**

| Mode / context | Container | Segment | State attr | Keyboard |
| --- | --- | --- | --- | --- |
| **Instant view filter (the default)** — in-place DOM update | `role="group"` | `role="button"` | `aria-current="true"` | Tab to each; Enter/Space activates |
| **Multi-select** | `role="group"` | `role="button"` | `aria-pressed` | Tab to each; Enter/Space toggles |
| **Deferred form input** — staged, inside a `<form>`, committed on submit | `role="radiogroup"` | `role="radio"` | `aria-checked` | roving tabindex + arrows |

The default for a *true* segmented control (immediate view switch) is **Model 3** — `role="group"` + `aria-current` — because the control's defining property is immediate mutation, and `aria-current` ("list of view-switching commands") matches that without the deferred-selection implication or the mutate-on-arrow hazard of `radiogroup`. The `radiogroup` model (Model 1) is reserved for the genuine *deferred form input* case — which is, in truth, a Radio group that happens to be styled as segments (use Radio, see radio §6). **Tablist (Model 4) is not the practice default** — if the segments genuinely control distinct panels, that's **Tabs**; Carbon's use is a pragmatic legacy-AT concession (flagged in notes.unverified). Other a11y: a **group label** is mandatory (`aria-label`/`aria-labelledby`) or AT hears disconnected terms; selected state not colour-only; ≥24px inner target (Primer) / 2.5.8; ≥3:1 boundary contrast. WCAG: 1.3.1, 4.1.2, 1.4.1, 1.4.11/2.4.13, 2.5.8.

## 7. Content guidelines

Militant brevity — horizontal space is the binding constraint. **2–5 text segments** (6 icon-only); past that, the layout fails → Select. Labels are **nouns/short noun phrases** ("Daily", "Weekly", "Monthly"), not verbs ("View Daily" inflates the count); **no multiline labels, ever** (wrapping breaks the unified track and creates uneven targets). Icon-only segments need an `aria-label`/visually-hidden text **and** a tooltip (external — Primer). Every control carries a **group label** (visible or `aria-label`) naming the dimension being switched ("View", "Time range"). No per-segment descriptions — if options need explaining, it's Radio.

## 8. Motion and transition

The **sliding pill** is the signature micro-interaction (track model): the indicator glides from the previous to the new segment (~150–200ms, eased), giving spatial confirmation. It can't be a pseudo-element (you can't transition across DOM nodes — §11); its `transform: translateX` and `width` are computed from the active segment's measured box. **Reduce-motion is a non-negotiable contract** — horizontal swiping motion is a vestibular trigger, so under `prefers-reduced-motion: reduce` strip the transition and **snap** the pill (or cross-fade opacity instead of sliding). The connected-button model has no slide (the active fill just changes), sidestepping this. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

i18n exposes the control's fragility — an equal-width control balanced for English **collapses** under German/Russian expansion. Rules (external): **never wrap** (it breaks the track); transition equal-width → content-width under expansion; overflow is discouraged on desktop (→ Select), tolerated on mobile (scroll). **RTL** reverses segment order (native flex in an RTL context) **and** inverts the sliding-pill `translateX` math — `offsetLeft` must be measured from the right edge when `dir="rtl"`. Icon-only sidesteps expansion entirely. (See 13-internationalization-and-rtl.)

## 10. Naming

Heavily fragmented: **`SegmentedControl`** (Primer, Apple), **Connected/Segmented Button Group** (Material 3), **`ToggleButtonGroup`** (MUI — the implementation primitive), **`ContentSwitcher`** (IBM Carbon), **`ActionGroup`** (Spectrum), **`ButtonGroup`** (Base Web). **The practice default is `SegmentedControl`** (the user-facing single-select switcher), implemented on the **`ToggleButtonGroup`** primitive (the Toggle Button × N). Aliases to map: `ToggleButtonGroup`, `ConnectedButtonGroup`, `ContentSwitcher`, `SegmentedButtons`.

## 11. Implementation notes

Two visual models, two distinct implementation challenges (external):

- **Track-and-pill — the pill measurement lifecycle.** The indicator must be a dedicated `<div aria-hidden="true">` sibling of the segment list (not a `::before`/`::after`, since CSS can't transition a pseudo-element across DOM nodes). A `useEffect`-equivalent reads the active segment's `offsetLeft`/`offsetWidth` and writes them as inline `transform`/`width` on the pill; hook a **`ResizeObserver`** (not just `window.resize`) so the pill tracks container/flex/locale-driven size changes, and recompute on `dir` change for RTL.
- **Connected-button — the shared-border trap + z-index wars.** Adjacent 1px borders double to 2px at intersections; collapse with `margin-inline-start: -1px` on overlapping siblings and zero the inner radii. Those negative-margin overlaps then **clip the focus ring** of a focused middle segment — dynamically raise the focused segment's `z-index` so its ring renders over the neighbours.
- **`selectionMode` drives ARIA + keyboard** (§6) — single-view-filter = `role=group` + `aria-current` + Tab/Enter; multi = `role=group` + `aria-pressed`; deferred-form = `radiogroup` + roving arrows. Don't ship one wired as another.
- Built on the **ToggleButtonGroup** primitive; the group owns the value (scalar/array) via context (radio/checkbox-group model); `disallowEmptySelection` guard lives in the click handler.
- **Composition guard:** `fullWidth` fills a parent, but an unconstrained `fullWidth` control on a wide viewport violates Fitts's Law (label-to-edge distance balloons) — parents should cap it with a `max-width`.

## 12. Related and alternative components

- **Composes with:** Toggle Button (the segment/atomic — see toggle-button), Icon, Tooltip (icon-only segment names — see icon), Toolbar / Action Bar / Table & Card headers (the canonical hosts).
- **Alternative to:** Radio (deferred form single-select — see radio), Tabs (panel-switching — the key boundary), Select (collapsed — see select), Switch (single on/off — see switch).
- **Supersedes:** a radio group misused where a compact immediate switcher is wanted; a row of ad-hoc buttons with hand-rolled active state and no group semantics.
- **Superseded by:** Tabs when selecting switches whole panels; Select/ActionMenu when the option count grows past ~5; a Toolbar of independent toggles when the options aren't a mutually-related set.

(Built on the Toggle Button atomic (toggle-button) and the ToggleButtonGroup primitive; for single-select it draws on Radio but **diverges on the a11y model** — see radio §5/§6 and the refinement note there. Tabs, when briefed, owns the panel-switching boundary from its side. See 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **Material 3 split out the Connected Button Group** (deprecating the older "Segmented Button" in the Expressive update — verify dating) as a distinct compact presentation, abandoning the track+pill for joined toggle buttons with a checkmark.
2. **The single-vs-multi fork made explicit** in APIs (MUI `exclusive`, Spectrum `selectionMode`) rather than two unrelated components.
3. **The ARIA model is actively contested** — four field models (radiogroup / group+aria-pressed / list+aria-current / tablist), with Primer's group+`aria-current` gaining ground for the immediate-switcher case as the cognitive-dissonance argument against `radiogroup` lands.
4. **The segmented-vs-tabs confusion** is increasingly called out explicitly (value-in-place vs. panel-switching).

## 14. Sources cited

Conservative dating (the external pass cited iOS 13 UISegmentedControl, Material 3 Expressive 2024/2026, MUI v5, React Spectrum v3, Base Web v12, Carbon v10/v11, Mantine — held loosely; the Material 3 deprecation dating and the legacy-AT tablist claim are flagged unverified; `last-audited` is the re-run trigger):

- Apple HIG — `UISegmentedControl` (the canonical track-and-pill) (Apple HIG, 2024).
- Google Material 3 — Connected Button Group (deprecating Segmented Button), checkmark-on-select, shape morphing (Material 3, 2024–2026).
- GitHub Primer — `SegmentedControl`, the `<ul>` + `aria-current` model, the no-routing rule, the radiogroup-cognitive-dissonance argument, 24px inner target (Primer, 2024).
- IBM Carbon — `ContentSwitcher` (tablist model + acknowledged ARIA-mismatch issues) (Carbon, 2024).
- MUI — `ToggleButtonGroup` (`exclusive`, `role=group` + `aria-pressed`, the manual empty-guard) (MUI, 2024).
- Adobe React Spectrum — `ActionGroup`/`selectionMode`/`disallowEmptySelection`, ActionBar composition, RTL flipping (Spectrum, 2024).
- Uber Base Web — `ButtonGroup` (`mode`), group + per-segment disabled (Base Web, 2024).
- Mantine — the reduce-motion `transition: none` blueprint for the sliding indicator (Mantine, 2024).
- WAI-ARIA APG — Radio Group, Button (toggle), Tabs patterns.
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 1.3.1, 4.1.2, 1.4.1, 1.4.11, 2.4.13, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: segmented-control
  name: Segmented Control
  aliases: [toggle-button-group, connected-button-group, content-switcher, segmented-buttons, action-group]
  category: form
  status: stable
description: >
  A compact, horizontally adjoined set of 2-5 options switched in place
  with IMMEDIATE effect — a value/filter/view switcher built on the
  ToggleButtonGroup primitive. Not a Radio group (deferred form input),
  not Tabs (panel switching), not a Select (collapsed). The most
  semantically contested component; resolved by purpose, not appearance.
anatomy:
  inherits: [toggle-button]   # per-segment states/pressed semantics
  built-on: toggle-button-group   # the atomic ToggleButton x N
  visual-paradigms:
    track-and-pill: "iOS lineage — a track housing a sliding pill indicator + dividers between unselected segments; PRACTICE DEFAULT (signature affordance)"
    connected-button: "Material 3 Connected Button Group — joined toggle buttons, squared inner borders, active fill + checkmark-displaces-label; themed variant"
  parts: [group-container, segment, selected-indicator (pill node | segment background), divider (track model only)]
api:
  inherits: [toggle-button]   # size, icon/label, per-segment disabled
  props:
    - {name: selectionMode, type: enum, values: [single, multiple], default: single, description: "explicit literal over MUI's exclusive boolean — drives the ARIA model AND the value type"}
    - {name: value/defaultValue/onChange, type: "scalar (single) | array (multiple)", description: group owns selection via context (radio/checkbox-group model)}
    - {name: disallowEmptySelection, type: boolean, default: true, description: "the zero-selection trap — ignore clicks on the sole active segment so onChange never fires empty; a segmented control almost always needs a persistent selection"}
    - {name: size, type: enum, values: [small, medium, large], default: medium}
    - {name: fullWidth, type: boolean, default: false, description: equal-width across the parent; cap with parent max-width (Fitts's Law)}
    - {name: disabled, type: boolean, default: false, description: group-level cascade + removes group from focus; per-segment disable also supported}
  segments: composed <Segment> children (icon/label/value)
states:
  group: [disabled (cascades + removes from focus)]
  segment:
    inherits: toggle-button   # rest, hover, focus-visible, pressed, selected, disabled
    adjoined-caveats: ["hover must not bleed to neighbours (connected)", "focus ring aligns to track interior (track) or elevates z-index over collapsed borders (connected)", "per-segment disabled independent of group"]
variants:
  size: [small, medium, large]
  content: [text-only, icon-only, icon+text]   # NEVER mix types within one group (Gestalt)
  sizing: [equal-width-default, content-width-fallback]   # equal-width (flex:1) default; isIntrinsic fallback
  selectionMode: [single, multiple]
  visual: [track-and-pill (default), connected-button]
accessibility:
  inherits: [toggle-button, radio]
  wcag-criteria: ["1.3.1", "4.1.2", "1.4.1", "1.4.11", "2.4.13", "2.5.8"]
  aria-fork:   # FOUR field models, resolved by PURPOSE not appearance
    instant-view-filter-DEFAULT: "role=group + role=button + aria-current=true; Tab to each + Enter/Space activates (Primer model — matches immediate mutation, no deferred-selection implication, no mutate-on-arrow)"
    multi-select: "role=group + role=button + aria-pressed; Tab + Enter/Space"
    deferred-form-input: "role=radiogroup + role=radio + aria-checked; roving tabindex + arrows — reserved for a staged form value (really a styled Radio group — see radio)"
    NOT-default: "tablist (Carbon) — only if segments control real panels (then it's Tabs); Carbon's use is a legacy-AT concession (unverified)"
  refines: "the Radio brief's simplification that 'segmented = radiogroup, same a11y tree' — a true immediate-switch segmented is group+aria-current, NOT radiogroup"
  group-label: "mandatory (aria-label/labelledby) or AT hears disconnected terms"
  target: ">=24px inner box (Primer/2.5.8); selected not colour-only; >=3:1 boundary"
content:
  segment-count: "2-5 text (6 icon-only); past that -> Select"
  label-pattern: "nouns/short noun phrases ('Daily'); no verbs, NO multiline; icon-only needs aria-label + tooltip"
  group-label: "names the switched dimension ('View','Time range'); visible or aria-label"
  no-descriptions: "per-segment descriptions -> use Radio instead"
motion:
  sliding-pill: "~150-200ms translateX between segments (track model); spatial confirmation; computed from measured box, not a pseudo-element"
  reduce-motion: "NON-NEGOTIABLE — horizontal swipe is a vestibular trigger; strip transition + snap, or cross-fade opacity"
  connected-model: "no slide (active fill changes) — sidesteps the motion contract"
i18n:
  rules: ["NEVER wrap (breaks the track)", "equal-width -> content-width under expansion (de/ru)", "overflow discouraged desktop (-> Select), scroll tolerated mobile"]
  rtl: "segment order reverses (native flex); sliding-pill translateX inverts — measure offsetLeft from the right edge when dir=rtl"
implementation:
  - "track-and-pill: indicator is a dedicated <div aria-hidden> sibling (NOT a pseudo-element — can't transition across DOM nodes); useEffect reads active offsetLeft/offsetWidth -> inline transform/width; ResizeObserver (not just window.resize); recompute on dir change"
  - "connected-button: collapse double borders with margin-inline-start:-1px + zero inner radii; raise focused segment z-index so the ring clears neighbours (z-index wars)"
  - "selectionMode drives ARIA + keyboard (see accessibility.aria-fork); don't ship one wired as another"
  - "built on ToggleButtonGroup; group owns value via context; disallowEmptySelection guard in the click handler"
  - "fullWidth caps with parent max-width (Fitts's Law on wide viewports)"
composition:
  composes-with: [toggle-button, icon, tooltip, toolbar, action-bar, table-header, card-header]
  built-on: toggle-button-group
  alternative-to: [radio, tabs, select, switch]
  supersedes: ["radio group misused as a compact immediate switcher", "ad-hoc buttons with hand-rolled active state + no group semantics"]
  superseded-by: ["tabs when selecting switches whole panels", "select/action-menu past ~5 options", "toolbar of independent toggles when not a mutually-related set"]
notes:
  contested:
    - "the ARIA fork (4 models) — resolved by purpose: group+aria-current default (immediate switcher), radiogroup for deferred form, aria-pressed for multi, tablist only if real panels"
    - "visual paradigm: track-and-pill (default) vs connected-button"
    - "equal-width vs content-width sizing (equal default, content fallback)"
  refines: "radio §5/§6 — segmented and radio share single-select INTENT but differ on the a11y MODEL (immediate group+aria-current vs deferred radiogroup)"
  inherited: "toggle-button atomic + ToggleButtonGroup primitive; radio's single-select data-binding (but not its radiogroup a11y for the immediate case)"
  unverified:
    - "Material 3 'Connected Button Group' deprecation/Expressive dating (2024/2026)"
    - "the legacy-AT-prefers-tablist field-testing claim (Carbon) — validate with JAWS/VoiceOver"
  evolution: "Material connected-button split-out; explicit single-vs-multi prop; ARIA model contested (aria-current gaining); segmented-vs-tabs confusion called out"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-segmented-control/` (15 June 2026), the second half of the toggle-group pair (with toggle-button). Both passes agree it is built on the Toggle Button / ToggleButtonGroup primitive and shares Radio's single-select intent, and converge on the 2–5-segment no-overflow rule, the segmented-vs-tabs (value-in-place vs. panel) / -vs-radio (immediate vs. deferred) / -vs-select (exposed vs. collapsed) boundaries, `selectionMode` over a boolean, equal-width-default sizing, the never-wrap i18n rule, and `SegmentedControl`-on-`ToggleButtonGroup` naming. The external pass materially advanced the brief: the **four-model ARIA fork** (radiogroup / group+aria-pressed / list+aria-current / tablist) and its resolution by *purpose* — the headline finding, which **refines the Radio brief's simplification** that "segmented = radiogroup, same a11y tree": a true immediate-view-switcher is `role=group` + `aria-current` (Primer), not `radiogroup`, because "radio" implies deferred selection and selection-follows-focus would mutate the view on every arrow; `radiogroup` is reserved for a genuinely deferred form input (which is really a styled Radio group). Also from the external pass: the two visual paradigms (track-and-pill vs. Material's connected-button), `disallowEmptySelection` for the zero-selection trap, the never-mix-content-types rule, the sliding-pill measurement lifecycle (dedicated node + `ResizeObserver`), the shared-border/z-index-wars traps, the Mantine reduce-motion blueprint, and the Fitts's-Law `max-width` guard on `fullWidth`. Claude-pass contributions: the framing as the ToggleButtonGroup presentation, the track-and-pill-as-default call, and the boundary set carried from radio/select. The Radio brief's cross-references are being updated to point here for the a11y-model nuance. The Material 3 Connected-Button deprecation dating and the legacy-AT-tablist claim are flagged unverified. Conformant to `components/_schema.md` (inherits toggle-button/radio). This closes the toggle-group pair the form batch repeatedly referenced.*

# Segmented Control — Claude pass

## 1. Framing
A Segmented Control is the **group of the Toggle Button** (the atomic unit — see toggle-button) presented as a connected, horizontally joined control: a small set of options shown side by side where the user picks among them in place. It inherits the Toggle Button atomic and, for the single-select case, Radio's semantics and keyboard model (radio §5 calls it "identical single-select semantics, different skin"). What it is: a compact, exposed switcher for a value/view/filter — 2–5 options, all visible. What it isn't: a Radio group (same single-select semantics but standard form presentation with descriptions), **Tabs** (which switch *panels* — a disclosure/navigation pattern), a Select (collapsed), or a lone Toggle Button (independent). The contested core: is it a single-select radiogroup or a multi-select pressed-button group?

## 2. Anatomy and parts
A **group container** (the connected track) + 2–5 **segments** (each a Toggle Button / radio, icon and/or text) + a **selected indicator** (often a sliding pill/background). Inherits Toggle Button anatomy per segment and the group label. The connected visual (shared borders, a single rounded outer shape) is the "segmented" skin; the same logical group rendered as separate buttons is just a ToggleButtonGroup.

## 3. Properties / API
- **`value`/`defaultValue`/`onChange`** — single scalar (single-select) or array (multi). The group owns selection (radio §3 / checkbox-group model).
- **`selectionMode`** — `single` (default, the common case) | `multiple`. This drives the ARIA fork (§6).
- options as composed `<Segment>` children (icon/label/value) or a data array (the select/radio options-vs-composition tension; composition default).
- `size`, `isDisabled` (group + per-segment), `fullWidth`/equal-width, `orientation` (horizontal default).
- group `label` (accessible name; often visually hidden for a compact control but programmatically present).
No per-segment `onChange` — selection derives from the group (radio §3).

## 4. States and variants
Per-segment: inherits Toggle Button states (rest/hover/focus-visible/selected/disabled). The **selected segment** is the one active option (single) or each active (multi). Group states: disabled (whole control). Variants: size; width (equal-width vs content-width); content (text / icon-only / icon+text); selectionMode (single/multi). The selected indicator (sliding pill) is the signature visual.

## 5. Usage guidance
- **Use** for a compact, exposed single-select among 2–5 options where seeing them all and switching in place matters: view switches (Grid/List, Day/Week/Month), short filters, unit toggles. Multi-select segmented (a group of independent toggles) for a small set of compact on/off filters.
- **Don't use** for: standard form one-of-many with descriptions (→ Radio); >~5 options or variable-width/overflowing labels (→ Select, or Radio); switching **content panels** (→ Tabs); a single on/off (→ Switch/Toggle Button); navigation between pages (→ Tabs/Nav).
- **Segmented vs. Radio** = presentation/density: segmented for compact frequent switches, radio for standard form options needing labels/descriptions (radio §5).
- **Segmented vs. Tabs** (the most-confused boundary) = *value vs. panel*: a segmented control sets a value/filter/view in place (`role=radiogroup`/`group`); Tabs switch among associated `tabpanel`s (`role=tablist`/`tab`/`tabpanel`) and are a disclosure pattern. If each option reveals a distinct panel of content, it's Tabs; if it changes a parameter of the *same* view, it's segmented.
- **Segmented vs. Select** = exposed-vs-collapsed (segmented when ≤5 and worth showing; Select when long/space-constrained).
- **No overflow** — segmented controls don't scroll or wrap; if the set is too large for the width, it's the wrong component.

## 6. Accessibility — the single-vs-multi fork
- **Single-select → radiogroup.** `role="radiogroup"` + `aria-labelledby`, segments `role="radio"` + `aria-checked`, **roving tabindex + arrow selection (selection-follows-focus)** — inherited wholesale from Radio (radio §6). This is the default and the common case.
- **Multi-select → group of toggle buttons.** `role="group"` + `aria-labelledby`, segments are `role="button"` + `aria-pressed`, **each its own tab stop, Space/Enter toggles** — inherited from Toggle Button (toggle-button §6). 
- **The fork is the whole a11y story:** the same visual control maps to *two different ARIA patterns and keyboard models* depending on `selectionMode`. Picking the wrong one (e.g. a single-select segmented wired as `aria-pressed` buttons, losing the exactly-one radiogroup semantics) is the recurring failure. GitHub Primer's `SegmentedControl` is single-select radiogroup-style; MUI `ToggleButtonGroup` exposes both via `exclusive`.
- Selected state not colour-only (the pill/indicator carries it); group label present even when visually hidden; ≥3:1 boundary contrast and target size (2.5.8).
- WCAG: 1.3.1, 4.1.2, 1.4.1, 1.4.11/2.4.13, 2.5.8 (+ radio/toggle-button inherited sets).

## 7. Content guidelines
Short, parallel segment labels (1–2 words), ideally equal length so segments balance; icon-only segments need accessible names (tooltip/aria-label) and an unambiguous glyph. Group label names the dimension being switched ("View", "Time range"), often visually hidden. No descriptions per segment (that's Radio's job — if options need explanation, use Radio).

## 8. Motion and transition
The **selected indicator slides** between segments (~150–200ms, eased) — the signature motion, communicating the switch. Reduce-motion: drop the slide, snap the indicator (instant). Don't animate segment widths. (See 18/19.)

## 9. Internationalization
RTL mirrors segment order and the indicator travel direction (logical layout); labels expand (de/ru) — equal-width segments are fragile under expansion, so size to content or cap and verify; icon-only sidesteps expansion. Inherits radio/toggle-button i18n.

## 10. Naming
Fragmented: **`SegmentedControl`** (Primer, Apple), **Segmented/Connected Button Group** (Material 3), **`ContentSwitcher`** (Carbon), **`ToggleButtonGroup`** (MUI, the implementation primitive), **`ButtonGroup`** (Base Web). Practice default: **`SegmentedControl`** (the user-facing single-select switcher), implemented on the `ToggleButtonGroup` primitive. Aliases: `ToggleButtonGroup`, `ContentSwitcher`, `ConnectedButtonGroup`, `SegmentedButtons`.

## 11. Implementation notes
- **`selectionMode` drives the ARIA + keyboard** (§6) — single = radiogroup (roving tabindex, arrow-select), multi = role=group of `aria-pressed` toggle buttons (tab-each, Space). Don't ship one wired as the other.
- Built on the **ToggleButtonGroup** primitive (the atomic Toggle Button × N); single-select adds the radiogroup roving model from Radio.
- The **sliding indicator** is a presentational layer (a translated pill behind the active segment); it must track the selected segment, not the focused one, and recompute on resize/content change.
- Equal-width via the container (grid/flex), not fixed pixels; no overflow handling (if it overflows, wrong component).
- Group owns the value (scalar/array); segments read from group context (radio/checkbox-group model).

## 12. Related and alternative components
- **Composes with:** Toggle Button (the segment/atomic — see toggle-button), Icon, Toolbar, Tooltip (icon-only segment names).
- **Alternative to:** Radio (standard form single-select — see radio), Select (collapsed — see select), Tabs (panel switching — the key boundary), Switch (single on/off).
- **Supersedes:** a radio group misused where a compact switcher is wanted; a row of ad-hoc buttons with hand-rolled active state.
- **Superseded by:** Tabs when switching panels; Select/Radio when the option count grows; a Toolbar of independent toggles when options aren't a mutually-exclusive set.

(Inherits the Toggle Button atomic and Radio's single-select group/keyboard model; the single-vs-multi fork is the segmented-specific resolution. See radio for the boundary from its side, toggle-button for the atomic, and Tabs when briefed for the panel-switching boundary.)

## 13. Field POV evolution
1. Material 3 formalised Segmented/Connected Button Groups as a distinct compact single-select presentation (radio §13).
2. The single-vs-multi fork made explicit in APIs (MUI `exclusive`), rather than two unrelated components.
3. iOS `UISegmentedControl` remains the canonical single-select switcher; the web converged on `SegmentedControl`/`ToggleButtonGroup` naming.
4. The segmented-vs-tabs confusion increasingly called out (segmented = value in place, tabs = panels).

## 14. Sources cited
(Conservative; reconcile with external.) GitHub Primer `SegmentedControl` (2024); Material 3 Segmented/Connected Buttons (2024); IBM Carbon `ContentSwitcher` (2024); Adobe Spectrum (2024); MUI `ToggleButtonGroup` (`exclusive`) (2024); Base Web `ButtonGroup` (2024); Apple HIG `UISegmentedControl` (2024); WAI-ARIA APG Radio Group + Button (toggle) patterns; WCAG 2.2 (Oct 2023) — 1.3.1, 4.1.2, 1.4.1, 1.4.11, 2.4.13, 2.5.8.

## 15. Agent-consumable schema (conform to _schema.md in segmented-control.md)
identity/description/anatomy(group+segments+indicator; inherits toggle-button)/api(value scalar|array, selectionMode)/states(inherits toggle-button; selected segment)/variants(size/width/content/selectionMode)/accessibility(THE FORK: single=radiogroup+roving, multi=group+aria-pressed)/content/motion(sliding indicator)/i18n/implementation/composition/notes(single-vs-multi fork; segmented-vs-tabs boundary; no-overflow).

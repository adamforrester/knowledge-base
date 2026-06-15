---
okf_version: "0.1"
type: component-brief
title: Slider
description: The analog fader forced into a discrete DOM — and the last standalone form control. A field-truth study of the single-vs-range model (one overloaded component, scalar|tuple value), the step/tick + float-rounding math, the value-display and finger-occlusion problem, the Arrow/Page/Home-End keyboard and aria-valuetext contract, the slider-vs-NumberField precision boundary with the paired-input composite, and the pointer-capture / thumb-overhang / thumb-collision implementation traps, with the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [range-slider, range-input, range, track]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Slider

> A Slider forces an analog metaphor — the mechanical fader — into a discrete, pixel-bound DOM, and that mismatch is the source of every hard decision in the component. It maps a numeric scalar (or a tuple, for a range) onto a spatial axis, which makes it superb for *approximate, relative* adjustment and actively bad for *precise* entry: a 200px track cannot address 1,000 distinct values without skipping integers. So the defining calls are about managing that tension — single vs. range, step granularity and float rounding, the precision boundary with a number input, and an accessibility contract that has to bridge spatial pointer manipulation and text-based assistive tech. The last of the standalone form controls, and one of the most engineering-dense.

---

## 1. Framing

A Slider lets a user pick a value (or a min–max range) by moving a thumb along a track — trading precision for *seeing the value within its bounds*. It inherits the Text Field form-field substrate (label/helper/error wiring — see text-field) but is otherwise its own pattern, not part of the selection-control decomposition.

What it *is*: a control for an **approximate/relative value where position-in-range matters more than the exact number** — volume, brightness, opacity, zoom, a price/size filter window — and where live feedback as the value changes is valuable. What it *isn't*: a control for a **precise** value the user knows (→ NumberField — see text-field §3; dragging to exactly $4,532 on a 0–10,000 track is misery), an **unbounded/huge** range (the track can't map 1→1,000,000 at step 1 — single-pixel moves jump hundreds), a **small enumerable** set (→ Radio/Segmented), or **on/off** (→ Switch).

Why systems disagree — and why this earned a dual-agent pass: the **single-vs-range** architecture, the **step/tick + floating-point** math, **value display** (tooltip vs. label) and finger occlusion, the **keyboard + aria-valuetext** contract, the **precision boundary** with NumberField, and a stack of **implementation traps** (pointer capture, thumb overhang, thumb collision) that recur across codebases. A near-universal field move: **abandon the native `<input type="range">` for rendering** (unstylable across engines, no multi-thumb) while **retaining a visually-hidden native input** for focus, keyboard, form submission, and AT semantics.

## 2. Anatomy and parts

Inherits the field substrate (label/helper/error). Slider-specific parts (both agents converge):

- **Root** — the bounding box that establishes the track geometry (CSS custom props / measured width) and positioning context.
- **Track** — the full scale; the click-to-jump hit area.
- **Fill / indicator** — the selected segment: min→thumb (single) or between the two thumbs (range).
- **Thumb(s)** — the draggable handle(s); owns pointer capture and the active coordinate.
- **Hidden input(s)** — a visually-clipped `<input type="range">` per thumb, anchoring focus / keyboard / form value / `role="slider"` semantics.
- **Value label** — inline (above/beside) or a thumb-anchored tooltip.
- **Ticks / marks** — step or point-of-interest markers along the track.
- **Min/max end labels** — the boundary values.

The API ships **hybrid** (consistent with the catalogue's encapsulation posture): an opinionated bundled `Slider` for the 90% case, with composable sub-parts (`Slider.Track`, `Slider.Thumb`) exposed for the 10% that injects custom DOM (a histogram above the track) — both agents land here.

## 3. Properties / API

Inherits the substrate (`label`, `helperText`, `error`, `isDisabled`, `isReadOnly` — see text-field §3). Slider-specific:

- **`value` / `defaultValue` / `onChange` — scalar for single, tuple `[a,b]` for range.** Both passes recommend **one overloaded `Slider`** (range spawns from a tuple value) over distinct `Slider`/`RangeSlider` exports (Spectrum/Primer split them; React Aria/Base UI/Material overload). The practice overloads — smaller API surface, and a UI can switch single↔range on data without swapping imports. The cost (weaker TypeScript narrowing than separate components) is accepted; document the range additions clearly.
- **`onChange` vs. `onChangeEnd`** — fire continuously during drag (live preview) vs. only on commit. **Expose both** (Spectrum's split): bind expensive effects (network filter, heavy re-render) to `onChangeEnd` so a drag doesn't fire per pixel — the slider analogue of the combobox/switch async discipline.
- **`min` / `max` / `step`** (granularity for drag *and* Arrow) **/ `largeStep`** (PageUp/Down, Shift+Arrow; ~10× step).
- **`marks`/`ticks`** (discrete labelled stops) **/ `formatOptions`** (`Intl.NumberFormat` → drives both the display label *and* `aria-valuetext`).
- **`orientation`** (horizontal default; vertical inverts the Y math — §4), **scale** (linear default; logarithmic for price/audio/zoom — decouples on-screen % from output value).
- **Range-only:** **`thumbCollisionBehavior`** (`push` default for pointer / `none` for keyboard — §4) and **`minStepsBetweenThumbs`** (a minimum delta so thumbs can't fully occlude each other).
- **Float-step rounding is mandatory:** IEEE-754 (`0.1 + 0.2 = 0.30000000000000004`) breaks ticks, tooltips, and formatters — snap the interpolated coordinate to the nearest exact `step` multiple *before* `onChange`.

## 4. States and variants

The track and thumb hold **independent** states (the track can be hovered while a thumb is focused). States: rest / hover / focus-visible (ring on the **thumb**, never the track — supports Windows HCM) / **dragging** (active pointer capture; thumb may shrink/deepen shadow, value tooltip appears) / disabled / read-only / error.

| State | Slider-specific contract |
| --- | --- |
| dragging | track stays active for pointer capture; spatial transitions OFF (§8) |
| disabled | pointer + keyboard removed; **hidden input dropped from form payload** |
| read-only | thumb stays keyboard-focusable, value immutable, **value still submitted** in the form POST (the disabled-vs-read-only serialization distinction — same discipline as checkbox/select) |
| error | rare for a standalone slider (its value is always within min/max); arises mainly via a **paired number input out of range** or external validation — fill/thumb shift to the critical token, message via `aria-describedby` |

**Variants:** single vs. range; continuous vs. stepped (with ticks); linear vs. logarithmic scale; with/without value label; with paired input; orientation (horizontal/vertical — vertical inverts the Y-axis so Arrow Up *increments* despite DOM `0,0` being top-left). No tone/emphasis.

## 5. Usage guidance

- **Use** for an **approximate/relative value where seeing position-in-range helps** and exactness doesn't matter (volume, brightness, opacity, zoom), where **live feedback** as it changes is valuable (filtering a table, scaling a model), or for a **discrete spectrum** (a 5-point Poor→Excellent scale).
- **Don't use** for: a **precise** value (→ NumberField — typing "47" is exact and faster); an **unbounded/huge** range where pixels can't map the precision; a **small enumerable** textual set (→ Segmented/Radio); or **on/off** (→ Switch).
- **The slider-vs-NumberField precision boundary is the headline call**, and the resolution is the **composite**: when both range-visibility *and* precision matter, **pair a slider with a NumberField** (Carbon ships this bundled) — slider for gross adjustment, input for exact entry, the two **bi-directionally synced** off one source of truth (guard against the React update loop by only applying an incoming value that differs). This is also the **accessibility escape hatch** (§6).
- **Range** for a min–max window (price filter, date range); single thumb otherwise.

## 6. Accessibility

Inherits the substrate (label association, describedby — see text-field §6). Slider-specific, and it is one of the harder a11y contracts in the catalogue:

- **`role="slider"`** (free via the hidden `<input type="range">`) with live **`aria-valuenow` / `aria-valuemin` / `aria-valuemax`**, and **`aria-valuetext` whenever the value isn't a bare number** — "$50", "Medium", "March 2026" — so AT announces the *meaningful* value, not "50" (the most-missed slider a11y point, and what `formatOptions` should also feed).
- **The keyboard contract is non-negotiable** (a drag-only slider is inaccessible): Arrow = `step`; PageUp/Down (or Shift+Arrow) = `largeStep`; Home/End = min/max. Each thumb is focusable.
- **Range needs per-thumb labels and windows:** two `role="slider"` thumbs, each with its own accessible name ("Minimum price" / "Maximum price") and its own `aria-valuemin`/`max` window; Tab moves between the thumbs' hidden inputs as distinct stops. Unlabelled thumbs ("slider… slider…") is the most-broken range a11y failure. Keyboard collision is `none` (block at the adjacent thumb) to prevent accidental bound inversion, even when pointer uses `push`.
- **Hit target:** the visual thumb may be 16px, but the interactive target must be **≥24px (2.5.8), ideally 44px** on touch — expand via a transparent `::before`/padding centered on the thumb; **the whole track is click-to-jump** so tremor users needn't drag.
- **The precision/motor critique is a genuine a11y concern, not just UX** — fine values are hard to hit for motor-impaired and screen-reader users; the **paired NumberField is the accessibility escape hatch**, and for critical exact values a slider may be the wrong component.
- **WCAG SCs:** 4.1.2 (role/value/valuetext), 2.1.1 (keyboard operable), 1.4.11 (thumb/track/fill ≥3:1), 1.4.1 (fill not the sole indicator), 2.4.13/1.4.11 (focus), 2.5.8 (target size).

## 7. Content guidelines

- **Label** the dimension ("Volume", "Price range"); **value formatting** carries units/currency/% via `Intl.NumberFormat` (locale-aware — `5,000` vs `5.000`) and feeds `aria-valuetext`. **Min/max end labels** orient the scale where helpful. Range shows two labelled values.
- **Finger occlusion** is the touch-specific content trap: a thumb tooltip directly above the thumb is hidden by the user's own finger — offset it **32–48px** above the thumb on touch so the live value clears the fingertip. Don't rely on a transient tooltip as the *only* readout of the committed value.

## 8. Motion and transition

The thumb/fill track the pointer **1:1 during drag** — any CSS position transition makes the thumb rubber-band behind the cursor, so inject a `data-dragging` attribute on pointer-capture that sets `transition: none` on thumb and fill (the same lag trap as the textarea resize handle and the segmented pill). A **track-click** *may* animate a short slide (~100–200ms ease) for continuity; snapping to ticks animates briefly. Under `prefers-reduced-motion: reduce`, **drop the slide and jump instantly** — lateral snapping is a vestibular trigger. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

**RTL inverts the math, not just the visuals** — min sits at the inline-start (right edge in RTL), the fill originates from the right and grows left, and a track-click measures from the right edge. The **keyboard adapts to visual direction**: in RTL, ArrowRight *decrements* (moves toward min on the right), ArrowLeft *increments* — while **ArrowUp/Down stay absolute** (Up always increments) regardless of text direction. Value formatting is locale-aware (`Intl.NumberFormat`); labels expand like any string. Use logical properties / a measured `dir` so this is automatic. (See 13-internationalization-and-rtl.)

## 10. Naming

`Slider` is near-universal for the single case; the range case splits — distinct `RangeSlider` (Spectrum, Primer) vs. an overloaded `Slider` with a tuple (React Aria, Base UI, Material via `range`), with Polaris naming its overloaded component `RangeSlider`. **The practice default is `Slider`** (single *and* range, via the scalar|tuple value type) — branching into a separate `RangeSlider` import adds cognitive load for no behavioural payoff once the value type drives the mode. Aliases to map: `RangeSlider`, `RangeInput`, `Range`, `track`.

## 11. Implementation notes

Sliders are notoriously trap-laden; the recurring ones (both agents):

- **Pointer capture is mandatory.** On `pointerdown`, call `setPointerCapture(pointerId)` on the thumb so drag coordinates keep flowing even when the cursor leaves the track's bounding box (or the window) — without it, a fast vertical wobble drops the drag and the thumb freezes. Release on `pointerup`/`pointercancel`.
- **The thumb-overhang problem.** At 0%/100% the thumb's centre aligns with the track edge, so half the thumb overhangs — causing horizontal scrollbars or clipping under `overflow: hidden`. Use edge-aware positioning (Base UI's `thumbAlignment="edge"`): interpolate the thumb's `translate` from `0%`→`-100%` of its own width across the range so its outer edge stays flush at the extremes. The practice defaults to edge alignment.
- **Track geometry math.** value↔pixel from the track's measured `getBoundingClientRect`; recompute on resize via `ResizeObserver` (and on `dir` change for RTL).
- **Float-step rounding** (§3) — snap to the step's precision before emitting.
- **`onChangeEnd` for expensive effects** (§3) so a drag doesn't fire a network call per pixel.
- **Paired-input sync** — slider + NumberField share one controlled value; apply an incoming value only if it differs from local state (prevents the React update loop).
- **Prefer the hidden native `<input type="range">`** for focus/keyboard/form/AT even in a custom-rendered slider (React Aria `useSlider`/`useSliderThumb` is the reference); a pure `role="slider"` div is the last resort and must own the full contract.
- **Range collision** — clamp to `minStepsBetweenThumbs`, route a track-click to the nearer thumb, and apply `push` (pointer) / `none` (keyboard).

## 12. Related and alternative components

- **Composes with:** the field substrate (label/helper/error), a paired **NumberField** (the precision composite, sharing validation/step logic — see text-field), a value **Tooltip** (see Tooltip when briefed), ticks/marks.
- **Alternative to:** NumberField (precise entry — see text-field §3), Stepper/SpinButton (very small ranges, e.g. 1–5), Radio/Segmented (a small discrete textual set — see radio, segmented-control), Switch (on/off), a Rating component (discrete stars).
- **Supersedes:** a bare `<input type="range">` for *rendering* (retained only as the hidden a11y/form node); a drag-only custom slider with no keyboard.
- **Superseded by:** NumberField when precision matters more than range-visibility; Segmented/Radio when the values are a small discrete set.

(Inherits the Text Field substrate; the slider+NumberField composite is the precision pattern. See text-field for the substrate and NumberField; 03-component-library; 29 for the docs template. The last of the standalone form controls.)

## 13. Field POV evolution

1. **Native render abandoned, native semantics retained** — the field moved from styling `<input type="range">` (engine-inconsistent, single-thumb-only) to custom DOM with a *visually-hidden* native input overlaid on the thumb (React Aria, Zag.js, Base UI), delegating focus/keyboard/mobile-keyboard/form/AT to the browser and shrinking the custom bug surface.
2. **Range standardised as a first-class mode** (tuple value), not a separate hack.
3. **`aria-valuetext`** for formatted/non-numeric values is now expected, not optional.
4. **The slider+NumberField composite** is increasingly the recommended pattern when precision matters, over slider-alone.
5. **Multi-thumb collision formalised** — Base UI's `thumbCollisionBehavior` (push/swap/none) elevated edge-case physics to an expected API; and `onChange`/`onChangeEnd` split standardised for expensive live effects.

## 14. Sources cited

Conservative dating (the external pass cited Base UI React v1.0.0-beta, Spectrum S2/React Aria 2025, Carbon React v1.109.0, Polaris v13.9 2026, Material 3 Expressive 2024–2025, Atlassian Range ^16.8.0, Fluent v9.68.0, Apple HIG iOS 18/macOS 15 — held loosely; `last-audited` is the re-run trigger):

- Adobe Spectrum / React Aria — `Slider` / `RangeSlider`, `useSlider`/`useSliderThumb`, `onChange` vs `onChangeEnd`, `formatOptions` (Spectrum, 2025).
- Base UI — the compound-parts model, `thumbCollisionBehavior` (push/swap/none), `thumbAlignment="edge"` (Base UI, 2026 beta).
- IBM Carbon — `Slider` bundled with a paired number input (the composite reference) (Carbon, 2026).
- Google Material 3 — continuous/discrete + range, the Expressive press-shrink handle and stop indicators (Material 3, 2024–2025).
- Shopify Polaris — `RangeSlider` (overloaded single/dual) (Polaris, 2026).
- GitHub Primer, Atlassian (`Range`), Microsoft Fluent — slider/range implementations (2024–2026).
- Radix UI — `minStepsBetweenThumbs` (the min-delta reference).
- Apple Human Interface Guidelines / Material Compose — slider, hit-target guidance (Apple HIG, 2025).
- WAI-ARIA APG — Slider and Slider (Multi-Thumb) patterns.
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 4.1.2, 2.1.1, 1.4.11, 1.4.1, 2.4.13, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: slider
  name: Slider
  aliases: [range-slider, range-input, range, track]
  category: form
  status: stable
description: >
  Maps a numeric scalar (or a tuple, for a range) onto a spatial axis —
  for APPROXIMATE/relative values where position-in-range matters more
  than the exact number. One overloaded component (range spawns from a
  tuple value). Not for precise entry (number-field), unbounded ranges,
  small enumerable sets (radio/segmented), or on/off (switch).
anatomy:
  inherits: text-field   # label/helper/error substrate (see text-field)
  parts: [root, track, fill-indicator, thumb(s), hidden-input(s) (<input type=range> for focus/keyboard/form/a11y), value-label, ticks-marks, min-max-labels]
  delivery: "native <input type=range> abandoned for RENDERING (engine-inconsistent, single-thumb-only); retained visually-hidden for semantics/form"
  composition: "hybrid — bundled Slider (90%) + composable Slider.Track/.Thumb sub-parts (custom DOM, e.g. histogram)"
api:
  inherits: text-field   # label, helperText, error, isDisabled, isReadOnly
  props:
    - {name: value/defaultValue/onChange, type: "number (single) | [number,number] (range)", description: "ONE overloaded Slider — range spawns from a tuple; over distinct Slider/RangeSlider exports"}
    - {name: onChangeEnd, type: function, description: "fires on commit (not per-drag-pixel) — bind expensive effects here"}
    - {name: min, type: number, default: 0}
    - {name: max, type: number, default: 100}
    - {name: step, type: number, default: 1, description: "drag + Arrow granularity; MUST snap-round to neutralise IEEE-754 float error before onChange"}
    - {name: largeStep, type: number, default: 10, description: "PageUp/Down + Shift+Arrow (~10x step)"}
    - {name: marks/ticks, type: array, required: false}
    - {name: formatOptions, type: Intl.NumberFormatOptions, description: "drives the display label AND aria-valuetext; locale-aware"}
    - {name: orientation, type: enum, values: [horizontal, vertical], default: horizontal, description: "vertical inverts Y math (Arrow Up increments despite DOM 0,0 top-left)"}
    - {name: scale, type: enum, values: [linear, logarithmic], default: linear, description: "log decouples on-screen % from output value (price/audio/zoom)"}
    - {name: thumbCollisionBehavior, type: enum, values: [push, swap, none], default: push, description: "RANGE — push for pointer, none for keyboard (block bound inversion)"}
    - {name: minStepsBetweenThumbs, type: number, description: "RANGE — minimum delta so thumbs can't fully occlude"}
states:
  inherits: text-field
  slider-specific: [rest, hover, focus-visible (ring on the THUMB), dragging, disabled, read-only, error]
  notes:
    track-thumb-decoupled: "track and thumb hold independent states simultaneously"
    disabled-vs-readonly: "disabled drops the hidden input from the form payload; read-only keeps it submitted but immutable (focusable)"
    error: "rare for a standalone slider (always within min/max) — arises via a paired number input out of range or external validation"
variants:
  selection: [single, range]
  step: [continuous, stepped-with-ticks]
  scale: [linear, logarithmic]
  value-display: [inline-label, thumb-tooltip, min-max-end-labels]
  composite: [standalone, with-number-field]
  orientation: [horizontal, vertical]
accessibility:
  inherits: text-field
  wcag-criteria: ["4.1.2", "2.1.1", "1.4.11", "1.4.1", "2.4.13", "2.5.8"]
  role: "role=slider (free via hidden <input type=range>); live aria-valuenow/valuemin/valuemax"
  valuetext: "aria-valuetext WHENEVER the value isn't a bare number ('$50','Medium','March 2026') — the most-missed slider a11y point; fed by formatOptions"
  keyboard-model:
    arrow: "step (Up/Right increment, Down/Left decrement)"
    page-or-shift-arrow: "largeStep"
    home-end: "min / max"
    non-negotiable: "drag-only slider is inaccessible"
  range: "two role=slider thumbs, each with its own accessible name (Minimum/Maximum) + its own valuemin/max window; Tab between thumbs; keyboard collision=none"
  hit-target: "visual thumb may be 16px but target >=24px (2.5.8), 44px touch (transparent ::before/padding); whole track click-to-jump"
  precision-critique: "fine values hard for motor-impaired/SR users — the paired NumberField is the a11y escape hatch; a slider may be the wrong component for critical exact values"
content:
  label-pattern: "name the dimension ('Volume','Price range'); value formatting carries units/currency/% via Intl.NumberFormat -> aria-valuetext"
  finger-occlusion: "touch thumb-tooltip offset 32-48px above the thumb so the value clears the fingertip; don't rely on a transient tooltip as the only committed-value readout"
motion:
  drag: "thumb/fill track the pointer 1:1 — set transition:none via a data-dragging attr on pointer-capture (rubber-band trap)"
  track-click: "may animate a short slide (~100-200ms); snapping animates briefly"
  reduce-motion: "drop the slide, jump instantly (lateral snap is a vestibular trigger)"
i18n:
  rtl: "min at inline-start (right); fill originates right -> grows left; track-click measured from the right edge; ArrowRight DECREMENTS / ArrowLeft increments; ArrowUp/Down stay absolute (Up=increment)"
  locale: "Intl.NumberFormat for value formatting (5,000 vs 5.000)"
implementation:
  - "setPointerCapture(pointerId) on pointerdown so drag survives the cursor leaving the bounding box; release on pointerup/cancel"
  - "thumb-overhang: edge-aware positioning (thumbAlignment=edge) interpolates translate 0%->-100% of thumb width so the outer edge stays flush at extremes (avoids scrollbars/clipping) — practice default"
  - "track geometry from getBoundingClientRect; recompute on resize (ResizeObserver) + dir change"
  - "float-step: snap interpolated value to the nearest step multiple before onChange"
  - "onChangeEnd for expensive effects (no per-pixel network calls)"
  - "paired-input sync: shared controlled value; apply incoming only if it differs (no React loop)"
  - "prefer hidden native <input type=range> for focus/keyboard/form/AT (useSlider reference); role=slider div is last resort"
  - "range: clamp minStepsBetweenThumbs, route track-click to nearer thumb, push (pointer)/none (keyboard)"
composition:
  composes-with: [text-field-substrate, number-field, tooltip, ticks]
  precision-composite: "Slider + NumberField, bi-directionally synced off one source of truth — the precision AND accessibility escape hatch"
  alternative-to: [number-field, stepper-spinbutton, radio, segmented-control, switch, rating]
  supersedes: ["<input type=range> for rendering (retained hidden for a11y/form)", "drag-only custom slider with no keyboard"]
  superseded-by: ["number-field when precision > range-visibility", "segmented/radio for a small discrete set"]
notes:
  contested:
    - "single vs range: one overloaded component (tuple value) vs distinct Slider/RangeSlider — practice overloads"
    - "thumb collision push/swap/none (push pointer, none keyboard)"
    - "the slider-vs-number-field precision boundary -> the paired-input composite"
  inherited: "the text-field form-field substrate"
  unverified:
    - "external-supplied 2026 version numbers (Base UI beta, Polaris v13.9, Carbon v1.109, Fluent v9.68, Atlassian ^16.8)"
  evolution: "native render abandoned / semantics retained; range first-class (tuple); aria-valuetext expected; slider+input composite; collision formalised; onChange/onChangeEnd split"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-slider/` (15 June 2026), the last of the standalone form controls. Both passes converged on the spine — one overloaded `Slider` (scalar|tuple value) over distinct exports, the native-render-abandoned/native-semantics-retained delivery (a visually-hidden `<input type="range">` for focus/keyboard/form/AT), `aria-valuetext` for formatted values as the most-missed a11y point, the Arrow/Page/Home-End keyboard contract with per-thumb labelling for range, the 1:1-drag-no-lag motion rule, RTL inverting both the math and the Arrow-key direction, float-step snap-rounding, the ≥24/44px hit target with whole-track click-to-jump, and — the headline usage call — the slider-vs-NumberField precision boundary resolved via the bi-directionally-synced paired-input composite (which is also the accessibility escape hatch). External-pass contributions folded in: the pointer-capture (`setPointerCapture`) drag-survival fix, the thumb-overhang problem and `thumbAlignment="edge"` resolution, `thumbCollisionBehavior` (push/swap/none) with push-pointer/none-keyboard, the disabled-vs-read-only form-serialization distinction, the vertical Y-axis inversion and logarithmic-scale math, the finger-occlusion 32–48px tooltip offset, `onChange` vs `onChangeEnd`, and `minStepsBetweenThumbs`. Claude-pass contributions: the framing of the precision boundary as the headline call, the composite-as-a11y-escape-hatch tie, and the inheritance from the text-field substrate. The external pass's 2026 version numbers are flagged unverified. Conformant to `components/_schema.md` (inherits text-field). With Slider, the standalone form-control set is complete.*

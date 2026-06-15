# Slider — field-truth study (Claude pass)

## 1. Framing
A Slider lets a user pick a value (or a range) by moving a thumb along a track — it trades precision for *seeing the value in its range*. It inherits the Text Field form-field substrate (label/helper/error, describedby — see text-field) but is otherwise its own thing (not part of the selection-control decomposition). What it is: a control for an **approximate/relative numeric value where the range and relative position matter** — volume, brightness, opacity, a price filter, zoom. What it isn't: a control for a **precise** value (→ NumberField — see text-field §3; sliders are imprecise by nature), a small enumerable set (→ Radio/Segmented), or an on/off (→ Switch). Why systems disagree: **single vs. range (two-thumb)**, the **step/tick** model, **value display** (tooltip vs. label), the **keyboard contract**, and the **precision/accessibility critique** (sliders are hard to operate exactly — the paired-number-input escape hatch).

## 2. Anatomy and parts
- **Track** (the rail) + **fill** (the portion from min to the value — or between the two thumbs in a range) + **thumb(s)** (the draggable handle) + optional **ticks/marks** (stepped) + optional **value label / tooltip** + optional **min/max end labels** + the inherited field label/helper/error.
- Range adds a second thumb and the fill becomes the between-thumbs segment.
- A common composite: **slider + a paired number input** for precise entry (§5, §12).
- A hidden native `<input type="range">` can anchor the value/keyboard/a11y, or a custom `role="slider"` element.

## 3. Properties / API
Inherits the substrate (label, helperText, error, isDisabled, isReadOnly — see text-field §3). Slider-specific:
- `min` / `max` / `step` — the range and granularity; `step` continuous (small/float) or coarse (snapping). Watch float-step rounding.
- **`value` / `defaultValue` / `onChange`** — **scalar for single, tuple `[a,b]` for range**. The single-vs-range mode drives the value type (the radio/checkbox scalar-vs-array parallel).
- **`onChange` vs `onChangeEnd`** — fire continuously during drag (live preview) vs. only on commit (expensive effects); expose both (Spectrum splits these). Critical for sliders whose effect is costly.
- `marks`/`ticks` — discrete labelled stops; `formatOptions`/`valueLabel` — how the value renders (currency, %, units, a date) → drives `aria-valuetext`.
- `orientation` (horizontal default; vertical rare), `minStepsBetweenThumbs` (range collision/min-distance).
- The practice exposes single + range in **one component** via the value type (scalar/tuple), not two components — but documents the range additions clearly.

## 4. States and variants
States: rest / hover / focus-visible (ring on the **thumb**) / **dragging** (active grab; thumb may enlarge, tooltip appears) / disabled / read-only / error (rare — a slider value is usually always-valid within min/max; error applies if a paired input is out of range). Variants: **single vs. range**; **continuous vs. stepped (with ticks)**; **with/without value label**; **with paired input**; orientation. No tone/emphasis.

## 5. Usage guidance
- **Use** for an **approximate/relative value where seeing the range and position helps** and exactness doesn't matter: volume, brightness, opacity, zoom, a price/size *filter* range.
- **Don't use** for: a **precise** value the user knows (→ NumberField — entering "47" is faster and exact); a **small enumerable** set (→ Radio/Segmented); **on/off** (→ Switch); or any value where being off-by-one matters and the user can't easily hit it.
- **The slider-vs-NumberField precision boundary is the key call:** sliders are imprecise — fine for "roughly 70%," wrong for "exactly $1,247." When both range-visibility *and* precision matter, **pair a slider with a number input** (the composite): the slider for gross adjustment, the input for exact entry, kept in sync (§11).
- **Range slider** for a min–max window (price filter, date range); single thumb otherwise.
- **Accessibility caution:** sliders are hard for motor-impaired and screen-reader users to operate precisely; always provide the keyboard contract (§6), and prefer the paired input when precision is needed — or reconsider the slider entirely for critical exact values.

## 6. Accessibility
Inherits the substrate (label association, describedby — see text-field §6). Slider-specific:
- **`role="slider"`** (native `<input type="range">` gives it free) with **`aria-valuenow` / `aria-valuemin` / `aria-valuemax`**, and **`aria-valuetext`** whenever the value isn't a bare number — "$50", "Medium", "March 2026" — so AT announces the meaningful value, not "50" (the most-missed slider a11y point).
- **Keyboard contract:** Arrow keys = one `step`; PageUp/PageDown = a larger step (e.g. 10%); Home/End = min/max. Each thumb is focusable; this is non-negotiable (a drag-only slider is inaccessible).
- **Range:** two `role="slider"` thumbs, each with its own `aria-valuemin`/`max` window (thumb A's max is B's current value, or they may cross per config) and its own accessible name ("Minimum price" / "Maximum price"); the most-broken range-slider a11y failure is unlabelled or wrongly-windowed thumbs.
- **Hit target:** the thumb is visually small but its target must meet 2.5.8 (≥24px, ideally 44 on touch) — expand the hit area beyond the visual thumb; track-click-to-move and drag supplement, never replace, keyboard.
- **The precision critique is a real a11y concern**, not just UX: fine-grained values are hard to hit for motor-impaired users — the paired number input is the accessibility escape hatch, not just a convenience.
- WCAG: 4.1.2 (role/value), 1.4.11 (thumb/track/fill contrast ≥3:1), 2.4.13/1.4.11 (focus), 2.5.8 (target), 1.4.1 (fill not the sole indicator), 2.1.1 (keyboard operable).

## 7. Content guidelines
- **Label** the dimension ("Volume", "Price range"); **value formatting** carries units/currency/% and feeds `aria-valuetext`. **Min/max end labels** orient the range when helpful ("$0"–"$1,000"). Range needs two labelled values ("Min"/"Max" or the two endpoints). Keep the live value legible during drag (tooltip), but don't rely on the tooltip alone for the committed value (it vanishes).

## 8. Motion and transition
Thumb/fill track the pointer 1:1 during drag (no lag — a transition on the thumb position rubber-bands behind the cursor, the same trap as the resize handle in textarea/the segmented pill). Keyboard steps may animate a short slide (~100ms). Snapping to ticks animates briefly. Under `prefers-reduced-motion`, snap without the slide. (See 18/19.)

## 9. Internationalization
**RTL flips the track** — min at the inline-start (right in RTL), fill direction and thumb travel mirror via logical properties; Arrow-key direction should follow visual direction. Locale-aware **value formatting** (decimal/grouping/currency — `Intl.NumberFormat`). Labels expand like any string. (See 13.)

## 10. Naming
**`Slider`** is near-universal (Spectrum, Material, Carbon, Base Web, Fluent); the range case is a `RangeSlider` or the same `Slider` with a tuple value. Practice default: **`Slider`** (single + range via value type), with `RangeSlider` documented as the alias/preset. Aliases: `RangeSlider`, `RangeInput`, `track`.

## 11. Implementation notes
- **Prefer native `<input type="range">`** where possible — free role/keyboard/value; style the track/thumb via the vendor pseudo-elements. Custom `role="slider"` only when native can't deliver (range two-thumb, ticks with labels, rich tooltips) — and then own the full keyboard/ARIA contract (React Aria `useSlider` is the reference).
- **Track geometry math:** value↔pixel mapping from the track's measured box (clientWidth, getBoundingClientRect), pointer events for drag, snapping to step; recompute on resize (ResizeObserver) and RTL.
- **Controlled value + onChange/onChangeEnd:** debounce or use `onChangeEnd` for expensive effects so dragging doesn't fire a network call per pixel (the slider analogue of the combobox/switch async discipline).
- **Range:** clamp thumbs to `minStepsBetweenThumbs`, decide cross-vs-no-cross, and route track-clicks to the nearer thumb.
- **Paired input sync:** the slider and number input share one controlled value; the input allows exact entry and validates against min/max; keep them the single source of truth.
- **Float step rounding** — snap to step with care (0.1 increments accumulate float error); round to the step's precision.

## 12. Related and alternative components
- **Composes with:** the field substrate (label/helper/error), a paired **NumberField** (the precision composite — see text-field), value Tooltip, Ticks/marks.
- **Alternative to:** NumberField (precise entry — see text-field §3), Radio/Segmented (small enumerable set), Switch (on/off), a Rating component (discrete stars).
- **Supersedes:** a bare `<input type=range>` without label/value-text wiring; a drag-only custom slider with no keyboard.
- **Superseded by:** NumberField when precision matters more than range-visibility; a Segmented/Radio when the values are a small discrete set.

(Inherits the Text Field substrate; the slider+NumberField composite is the precision pattern. See text-field for the substrate and NumberField; 03-component-library; 29 for the docs template. The last of the standalone form controls.)

## 13. Field POV evolution
1. Range (two-thumb) standardised as a first-class mode (Spectrum/Material/MUI), not a separate hack.
2. `aria-valuetext` adoption for formatted/non-numeric values is now expected, not optional.
3. The **slider+input composite** is increasingly the recommended pattern when precision matters, rather than slider-alone.
4. `onChange` vs `onChangeEnd` split standardised for expensive live effects.
5. Native `<input type=range>` styling matured (vendor pseudo-elements), narrowing where a custom slider is needed — though range/ticks/tooltips still push to custom.

## 14. Sources cited
(Conservative; reconcile with external.) Adobe Spectrum / React Aria `Slider`/`RangeSlider`, `useSlider`, onChange/onChangeEnd (2024–2025); Material 3 Slider (continuous/discrete, range) (2024); IBM Carbon `Slider` (with number input) (2024); Shopify Polaris `RangeSlider` (2024); GitHub Primer (2024); Atlassian `Range` (2024); Base Web `Slider` (2024); Apple HIG slider / Material Compose (2024); WAI-ARIA APG Slider + Slider (Multi-Thumb) patterns; WCAG 2.2 (Oct 2023) — 4.1.2, 1.4.11, 2.4.13, 2.5.8, 1.4.1, 2.1.1.

## 15. Agent-consumable schema (conform to _schema.md in slider.md)
identity/description/anatomy(track/fill/thumb(s)/ticks/value-label)/api(min/max/step, value scalar|tuple, onChange/onChangeEnd, marks, formatOptions, minStepsBetweenThumbs; inherits text-field substrate)/states(rest/hover/focus/dragging/disabled/read-only/error)/variants(single|range, continuous|stepped, with-input, orientation)/accessibility(role=slider, aria-valuenow/min/max/valuetext, keyboard Arrow/Page/Home-End, per-thumb labelling, precision critique)/content(value formatting + units)/motion(1:1 drag, no lag)/i18n(RTL track flip, locale format)/implementation(native input preferred, track geometry, onChangeEnd for expensive, paired-input sync, float rounding)/composition(NumberField composite)/notes(single-vs-range; slider-vs-numberfield precision boundary; paired-input escape hatch).

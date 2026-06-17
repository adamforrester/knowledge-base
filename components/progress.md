---
okf_version: "0.1"
type: component-brief
title: Progress
description: The fourth Feedback brief — the loading/in-progress indicator, reusing Toast's live-region pattern for milestone/completion announcements. A field-truth study of the determinate-vs-indeterminate fork (the role=progressbar value contract + the don't-fake-determinate rule), the live-region milestone announcement (don't-announce-every-percent, throttle to 25/50/75/100), the progress-vs-spinner-vs-skeleton three-loading-patterns decision, the meter-vs-progressbar semantic boundary, linear/circular/dashboard/global placement + the Stop Indicator, the anti-flash delay/min-display rules, and the reduce-motion-can't-remove-the-only-indicator substitution — with the practice's defaults.
tags: [components, feedback]
category: Feedback
status: stable
aliases: [progress-bar, progress-indicator, linear-progress, circular-progress, loader]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Progress

> A Progress indicator manages user expectations during temporal uncertainty — it signals **a task is underway** and, when it can, *how far along*. It is the fourth Feedback brief and reuses the **live-region announcement pattern Toast established** (for milestone/completion announcements, *not* a per-percent flood). Its defining fork is **determinate vs. indeterminate**: determinate when the system can genuinely measure advancement (a file upload's byte count, "step 3 of 5") — `role="progressbar"` with `aria-valuenow`/`valuemin`/`valuemax`; indeterminate when it can't (waiting on a server) — the animated bar/ring that **omits `aria-valuenow`** (with `aria-busy="true"` on the loading region). The cardinal rule: **don't fake determinate** — a bar that crawls to 99% and hangs violates the value contract, distorts the mental model, and erodes trust. And it anchors two boundaries the field routinely botches: the **three-loading-patterns decision** (Progress vs Spinner vs Skeleton) and the **`role=meter` vs `role=progressbar`** semantic divide (a meter is a *static measurement* — battery, disk, a gauge — not a task advancing; React Aria/Spectrum ship them as separate `useMeter`/`useProgressBar` hooks).

---

## 1. Framing

Progress is the programmatic + visual bridge between a user's action and an asynchronous resolution. It reuses the **live-region pattern from Toast** (see toast) for announcements. Its core decision is **determinate vs. indeterminate** (§4/§6), governed by the **don't-fake-determinate** rule.

It must be disambiguated from **three sibling loading patterns** + the meter:
- **Progress bar** — a value contract for a *longer/measurable* task (this brief; >~5s, or a known file size/step count, or a large area where a tiny spinner would look lost).
- **Spinner** — the minimal *indeterminate inline busy* indicator (~1–5s; a button, a dropdown fetching) — no value contract — see spinner.
- **Skeleton** — the content-shaped *placeholder* for an *initial page/section load*, reserving space to prevent CLS — see skeleton when briefed.
- **`role=meter`** (the sharp boundary) — a *static measurement within a range* (disk usage, battery, score); **not a task**; a different role/component.

What it *isn't*: a **Spinner** (minimal inline, no value), a **Skeleton** (placeholder), a **Meter** (static measurement), or a **Stepper** (discrete *user* steps, not *system* labour). Why systems disagree: the determinate threshold, the announcement model, the linear/circular/global placement, and unified-vs-distinct naming.

## 2. Anatomy and parts
- **track (rail)** — the static spatial reference defining the operation's scope + the contrast baseline.
- **indicator (fill)** — the active element traversing the track; bound to the value (determinate) or detached for the cyclical animation (indeterminate).
- **label** — the accessible name (what's progressing — "Uploading avatar"); via `aria-labelledby`/`aria-label`; **never embedded inside the track** (contrast failure as the fill sweeps behind it + truncation — §7).
- **value text** — the visible "45%" / "45 MB of 100 MB" / "Step 3 of 5" (mirrors `aria-valuetext`).
- **buffer** — an optional lower-opacity secondary fill advancing ahead of the primary (media streaming: loaded vs consumed).
- **stop indicator** — Material 3's **4dp terminal dot** at the track end, ensuring the track's *length* is perceivable when the unfilled rail can't meet 3:1 against the surface (WCAG 1.4.11 — §6).
- **live-region wrapper** — a visually-hidden `aria-live="polite"` `<div>` (pre-existing in the DOM) carrying throttled milestone/completion announcements (the Toast pattern — §6).

## 3. Properties / API
- **`value` (+ `min`/`max`, default 0–100)** — determinate; **omitting / `null`** implicitly forces indeterminate.
- **`indeterminate`** — the animated, no-value variant (or inferred from absent `value`).
- **`valueLabel` / `format` / `aria-valuetext`** — the displayed + announced value, incl. **non-percentage** ("Step 3 of 5", byte counts) — React Aria's `formatOptions`/`valueLabel`, run through `Intl.NumberFormat` (§9).
- **`variant` / `type`** — `linear` / `circular` / `dashboard` (gauge) / segmented (`steps`).
- **`size` / `thickness`**.
- **`buffer` / `bufferValue`** — the secondary fill.
- **`label` / `aria-label` / `aria-labelledby`** — required for an accessible name.
- **anti-flash** — `delay` (don't mount before ~200–500ms) + `minDisplay` (lock visible ~500ms once shown) (§5/§11).
- **API philosophy** — headless hooks (React Aria `useProgressBar`/`useMeter` — abstract the ARIA/format/calc) vs opinionated declarative primitives (MUI/Chakra — `value` sets determinate, omitting it triggers indeterminate).

## 4. States and variants
- **States:** **determinate** (value, fill advances) / **indeterminate** (animated, no value, `aria-busy`) / **buffer** (secondary fill) / **complete** (100% — success token + optional checkmark replacing the %) / **error** (halts, critical token, the label names the failure — §7). Systems support **indeterminate→determinate morphing** (begin indeterminate while establishing the connection/size, morph to determinate once measurable — Fluent/M3).
- **Variants:**
  - **determinate vs indeterminate** (the core fork).
  - **linear / circular / dashboard (arc gauge) / segmented (stepped)**.
  - **placement:** inline (in a button/row) / block (a section/page loader) / **global** (the top-of-viewport route-change bar — nprogress style — §11).
  - **size**, with/without the value label, buffer.

## 5. Usage guidance
- **Determinate Progress bar** — when you can **genuinely measure**: a file upload (bytes), a multi-step process (step N of M), a known-length batch.
- **Indeterminate Progress bar** — a longer *unmeasurable* process where a bar is the right weight (a server op of unknown duration).
- **Don't use a Progress bar for:** a **minimal inline wait** (→ **Spinner**, ~1–5s, a button/dropdown), an **initial content load** (→ **Skeleton**, prevents CLS), a **static measurement** (→ **Meter**), or **discrete navigable steps** (→ **Stepper**).
- **Decision frameworks:**
  - **Determinate vs indeterminate:** can you *measure* it? Determinate. If not, indeterminate — **never fake a determinate value**.
  - **Progress vs Spinner vs Skeleton:** value/longer (Progress, >~5s/large area) vs minimal-inline (Spinner, ~1–5s) vs content-placeholder-on-load (Skeleton).
  - **The anti-flash rules:** **delay before showing** (~200–500ms — if the op resolves first, never render → instant update); **minimum display time** (~500ms once shown — so it doesn't vanish in one jarring frame). A spinner flashed for 50ms feels *worse* than nothing.
  - **The button-loading boundary:** a Button's loading state shows a **Spinner in-place** (the width-preserving loading contract — see button), not a Progress bar. But a button that kicks off a *multi-megabyte upload* should disable + spawn a **separate determinate bar** nearby (a spinner can't show metrics).

## 6. Accessibility
- **`role="progressbar"` + the value contract:**
  - **Determinate:** `aria-valuenow` + `aria-valuemin` + `aria-valuemax` (+ `aria-valuetext` for human-readable/non-%) + a label.
  - **Indeterminate:** `role="progressbar"` **without `aria-valuenow`/`min`/`max`** (a static `aria-valuenow="0"` falsely signals "stalled at 0%"); set **`aria-busy="true"`** on the region undergoing the change.
- **The live-region announcement (the crux, reusing Toast's pattern):** screen readers **do not reliably announce `aria-valuenow` changes**, and announcing **every percent floods** the user with an inescapable queue. So: a pre-existing visually-hidden `aria-live="polite"` region, with **milestone throttling** — inject updates only at **25 / 50 / 75 / 100%** (and especially the **completion/error** end state). Don't inject the region and its text simultaneously (AT ignores it — the Toast pre-existing-region rule).
- **The `meter` vs `progressbar` boundary** — `role="meter"` is a *static measurement* (battery/disk/gauge), **not** a task; using `progressbar` for a static value (or vice versa) makes AT announce it wrong. Separate components (React Aria `useMeter` vs `useProgressBar`).
- **The Stop Indicator (WCAG 1.4.11 Non-text Contrast)** — if the unfilled rail doesn't meet **3:1** against the surface, the track's *length/bounds* aren't perceivable to low-vision users; Material 3's 4dp terminal dot marks the end so the total scope is always visible.
- **Reduce-motion can't remove the only indicator** — the indeterminate animation *is* the busy cue, so `prefers-reduced-motion: reduce` **substitutes** (a slow opacity pulse ~40%↔100% over ~1.5s, or static "Loading…" + a minimal ellipsis), never deletes — a frozen spinner reads as a crash. (Determinate fill transition → instant set under reduce-motion.)
- **Color-not-sole-carrier** — position/fill conveys progress (not colour alone); the label + value are the explicit signal; completion/error end states aren't colour-only (icon/text).
- **WCAG SCs:** 4.1.2 (name/role/value), 4.1.3 (Status Messages — the milestone/completion region), 1.4.11 (non-text contrast — the track/stop indicator), 1.4.1 (colour not alone), 2.3.3/2.2.2 (motion — indeterminate + reduce-motion), 1.4.3 (contrast).

## 7. Content guidelines
- **A clear label, active verb** — "Uploading", "Saving", "Connecting"; **above/adjacent to the track, never embedded inside it** (the fill sweeping behind text fails contrast + truncates on narrow viewports).
- **Concrete value over abstract percentage** — "45 MB of 100 MB" / "Step 3 of 5" beats a bare "45%" when the data exists; whenever the visible text deviates from a raw %, sync **`aria-valuetext`**.
- **Don't over-narrate** — cycling the label through technical micro-states ("Resolving DNS…", "Handshaking…") strobes the text and floods the live-region queue; stay on the user's mental model.
- **Completion + error messaging** — transition to past-tense done ("Upload complete") or an actionable error ("Upload failed — file too large"); the error names the **remediation**, not just the failure.

## 8. Motion and transition
- **Indeterminate linear:** an indicator block scales + translates across the track (asymmetric ease curves for an organic feel). **Indeterminate circular:** a simultaneous SVG rotation + `stroke-dasharray`/`stroke-dashoffset` grow/shrink (the notoriously fiddly spinner loop). Under `prefers-reduced-motion: reduce`, **substitute** with the slow opacity pulse / static "Loading…" (§6).
- **Determinate:** the fill animates to each new value (~200–300ms ease) so chunked/bursty network data reads as steady advancement; under reduce-motion, snap (0ms).
- **Completion:** a brief settle to 100% / success transition; the global route-bar fills then fades.
- *(Emerging/unverified: Material 3 Expressive "wavy" determinate tracks, Aug 2024 — amplitude/wavelength tokens — flag, don't bake in.)* (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** — the **linear bar fills from the trailing (right) edge** leftward via logical properties; the circular direction + the value-label side mirror (a left-label/right-% LTR layout flips).
- **Number/format** — percentage symbol position (`50%` vs `%50`), decimal separators, byte counts, and time-remaining run through **`Intl.NumberFormat`** (React Aria/Chakra do this natively); "Step 3 of 5" word order localizes.
- **Text expansion** — the label/value expands; don't truncate the value. (See 13-internationalization-and-rtl.)

## 10. Naming
The field splits on **unified vs distinct primitives**: unified **`Progress`** with a `type`/`variant` prop (Ant `line`/`circle`/`dashboard`, Primer `ProgressBar`, Chakra) vs distinct **`LinearProgress`** + **`CircularProgress`** (MUI; Fluent's `fluent-progress` + `fluent-progress-ring`). **The practice default: a unified `Progress`** with **`variant: linear | circular`** + an **`indeterminate`** flag (consistent with the catalogue's one-component-+-variant POV — cf. Dialog's `modal` prop, Drawer's `placement`), the **global route-bar** as a placement variant, the minimal-inline-indeterminate case routed to **`Spinner`**, and the static-measurement case to **`Meter`**. (The distinct-primitives argument — radial SVG logic shouldn't ship when you need a `<div>` bar — is real but largely answered by tree-shaking/code-splitting; flagged contested.) Aliases to map: `ProgressBar`, `ProgressIndicator`, `LinearProgress`, `CircularProgress`, `Loader`.

## 11. Implementation notes
- **The determinate value contract** — `role=progressbar` + `aria-valuenow`/`min`/`max` + `aria-valuetext`; the fill width/ring arc derives from the value; **clamp out-of-range** values (silent clamp + a dev-mode warning).
- **The indeterminate case** — omit `aria-valuenow`, animate, set **`aria-busy="true"`** on the loading region.
- **The throttled live-region** — render the empty `aria-live="polite"` region on mount (pre-existing rule); track the last-announced milestone in a `ref`; when the value crosses a 25/50/75 boundary not yet announced, update the region's `textContent`; push the completion/error string at `value === max`. **Never** bind announcements to `aria-valuenow`.
- **The anti-flash timers** — a `delay` `setTimeout` (~200–500ms; cleared on early resolution → no mount); once shown, a `minDisplay` lock (~500ms) deferring unmount. Manage the overlapping timers carefully (cleanup to avoid leaks).
- **The global route-change bar** — a thin top-of-viewport linear bar; visually it uses a **"fake-easing" trick** (rush to ~20%, slow toward ~80%, snap to 100% on resolve) — **but it must stay indeterminate to AT**: `aria-busy` on the document / a polite "Loading page" announcement, **never a fabricated `aria-valuenow`**. (This is the one place a *visual* fake is acceptable — because the *value contract* is never faked.)
- **Reduce-motion substitution** — branch on `prefers-reduced-motion` to the opacity pulse / static indicator (§6/§8).
- **Don't hand-roll** — React Aria `useProgressBar`/`useMeter` (the semantic split + format/calc) or the system's `Progress`; skin them.

## 12. Related and alternative components
- **Stands on:** the **live-region announcement pattern** inherited from Toast (the Feedback substrate — for milestone/completion — see toast).
- **Alternative to / boundary with:** **Spinner** (minimal indeterminate inline busy indicator, no value contract — see spinner), **Skeleton** (content-shaped initial-load placeholder, prevents CLS — see skeleton when briefed), **Meter** (`role=meter` static measurement — a separate component), **Stepper** (discrete *user* steps vs system labour), the **loading/promise Toast** (see toast §promise — shades into progress feedback).
- **Composed by:** Button (the loading state uses a Spinner, not a Progress bar — see button), File Upload (a determinate upload bar — see file-upload when briefed), measurable processes.

(The fourth Feedback brief — the loading/in-progress indicator, reusing Toast's live-region pattern for milestone/completion announcements and anchoring the three-loading-patterns decision (Progress / Spinner / Skeleton) plus the `meter`-vs-`progressbar` semantic boundary. See toast for the live-region pattern, spinner/skeleton/meter when briefed for the boundaries, button for the loading-button boundary, breadcrumbs for the stepper boundary. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The meter-vs-progressbar clarification** — the W3C/ARIA working groups formalised the split (after years of interchangeable `<progress>`/`<meter>` use); React Aria/Spectrum ship `Meter` and `ProgressBar` as distinct hooks/components.
2. **The don't-announce-every-percent settling** — milestone throttling (25/50/75/100 via a polite region) replaced binding AT to `aria-valuenow` (unreliable + flooding).
3. **The anti-flash discipline** (delay-before-show ~200–500ms + minimum-display ~500ms) hardened as the perceived-performance standard — UX research showed a 50ms flash feels worse than nothing.
4. **Reduce-motion substitution** aligned — the indeterminate animation is reduced (opacity pulse), never removed (a frozen spinner reads as a crash).
5. **The Stop Indicator** (Material 3, Dec 2023) — the 4dp terminal dot for WCAG 1.4.11, correcting the faint-rail contrast failure; plus the Material 3 Expressive "wavy" tracks (Aug 2024, unverified).

## 14. Sources cited
(Conservative; the external pass cited Carbon `@carbon/react ^1.109.0`, React Aria v3.49.0, Ant v5.16–v6.0, Base Web v18.1.0, MUI v5/X v9, the M3 stop-indicator Dec 2023 + wavy Aug 2024 — held loosely and flagged unverified.) **Google Material 3** — Progress indicators (linear/circular, determinate/indeterminate, buffer, the **stop indicator** for 1.4.11, the Expressive wavy tracks) (2024–2026); **IBM Carbon** — `ProgressBar` + `InlineLoading` + `Loading` (the polite live-region testing mandate) (2024–2026); **Shopify Polaris** — `ProgressBar` + `Spinner` (known-vs-unknown duration boundary) (2024–2026); **GitHub Primer** — `ProgressBar`(`.Item` segmented) + `Spinner` (2024–2026); **Adobe Spectrum / React Aria** — `useProgressBar` + `useMeter` (the semantic split; `formatOptions`/`valueLabel`) (2024–2026); **Microsoft Fluent 2** — `ProgressBar`/`Spinner` (+ the indeterminate→determinate morph) (2024–2026); **MUI** — `LinearProgress` + `CircularProgress` (`variant="buffer"`, `min`/`max`) (2024–2026); **Ant Design** — `Progress` (line/circle/**dashboard**, `steps`) (2024–2026); **Chakra** — `Progress`/`CircularProgress`/`Spinner` (`Intl.NumberFormat`) (2024–2026); **Base Web (Uber)** — `ProgressBar`/`Spinner` (anti-flash timers) (2024); **WAI-ARIA APG** — the `progressbar` role + `aria-valuenow`/`min`/`max`/`valuetext`; the `meter` role distinction; the live-region announcement question; the inherited Feedback live-region pattern (see toast). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.2, 4.1.3, 1.4.11, 1.4.1, 2.3.3, 2.2.2, 1.4.3.

## 15. Agent-consumable schema

```yaml
identity:
  id: progress
  name: Progress
  aliases: [progress-bar, progress-indicator, linear-progress, circular-progress, loader]
  category: feedback
  status: stable
description: >
  The loading/in-progress indicator — signals a task is underway and, when
  measurable, how far. Determinate (role=progressbar + aria-valuenow/min/max)
  vs indeterminate (animated, no valuenow, aria-busy); DON'T fake determinate.
  Reuses Toast's live-region pattern for MILESTONE/completion announcements
  (not per-percent). Anchors the three-loading-patterns decision (Progress/
  Spinner/Skeleton) + the meter-vs-progressbar boundary. NOT a Spinner
  (minimal inline), NOT a Skeleton (placeholder), NOT a Meter (static
  measurement), NOT a Stepper (discrete user steps).
anatomy:
  parts:
    - "track/rail (static scope reference + contrast baseline)"
    - "indicator/fill (bound to value [determinate] / detached cyclical animation [indeterminate])"
    - "label (accessible name; aria-labelledby; NEVER embedded inside the track — contrast + truncation)"
    - "value text ('45%' / '45 MB of 100 MB' / 'Step 3 of 5'; mirrors aria-valuetext)"
    - "buffer (lower-opacity secondary fill ahead of primary — media)"
    - "stop indicator (M3 4dp terminal dot for WCAG 1.4.11 when the rail can't hit 3:1)"
    - "live-region wrapper (pre-existing visually-hidden aria-live=polite for throttled milestones — Toast pattern)"
api:
  inherits: toast (live-region pattern for milestone/completion)
  philosophy: "headless hooks (React Aria useProgressBar/useMeter) vs opinionated declarative (MUI/Chakra — value sets determinate, omitting triggers indeterminate)"
  props:
    - {name: value, type: "number | null", description: "determinate; null/omit -> indeterminate; clamp to min/max"}
    - {name: min/max, type: number, default: "0/100"}
    - {name: indeterminate, type: boolean}
    - {name: valueLabel/format/aria-valuetext, type: "string/function", description: "displayed+announced; non-% via Intl.NumberFormat"}
    - {name: variant/type, type: enum, values: [linear, circular, dashboard, segmented]}
    - {name: size/thickness, type: token}
    - {name: buffer/bufferValue, type: number}
    - {name: label/aria-label/labelledby, type: string, description: required accessible name}
    - {name: delay/minDisplay, type: number, description: "anti-flash (~200-500ms delay / ~500ms min-display)"}
states:
  runtime: [determinate, "indeterminate (aria-busy)", buffer, "complete (100%, success token, checkmark)", "error (halts, critical token, label names failure)"]
  morphing: "indeterminate -> determinate once measurable (begin while establishing connection/size)"
variants:
  fork: "determinate vs indeterminate"
  geometry: [linear, circular, "dashboard (arc gauge)", "segmented (stepped)"]
  placement: "inline (button/row) / block (section/page) / GLOBAL (top route-change bar, nprogress)"
accessibility:
  wcag-criteria: ["4.1.2", "4.1.3", "1.4.11", "1.4.1", "2.3.3", "2.2.2", "1.4.3"]
  determinate: "role=progressbar + aria-valuenow/min/max (+ aria-valuetext non-%) + label"
  indeterminate: "role=progressbar WITHOUT valuenow (static valuenow=0 falsely reads 'stalled'); aria-busy=true on the loading region"
  live-region: "SR doesn't reliably announce aria-valuenow + every-% floods -> pre-existing polite region, MILESTONE THROTTLE (25/50/75/100 + completion/error); don't inject region+text together (Toast rule)"
  meter-boundary: "role=meter = STATIC measurement (battery/disk/gauge) NOT a task; separate component (React Aria useMeter vs useProgressBar)"
  stop-indicator: "WCAG 1.4.11 — if the unfilled rail <3:1 vs surface, the track length isn't perceivable; M3 4dp terminal dot marks the end"
  reduce-motion: "the indeterminate animation IS the cue -> SUBSTITUTE (slow opacity pulse 40<->100% ~1.5s / static 'Loading…'), never remove (frozen = crash); determinate fill -> instant set"
  color: "position/fill + label/value the signal, not colour alone; completion/error not colour-only"
content:
  label: "active verb ('Uploading'); above/adjacent, NEVER inside the track"
  value: "concrete over abstract ('45 MB of 100 MB' / 'Step 3 of 5' > bare '45%'); sync aria-valuetext when it deviates from %"
  no-over-narrate: "don't cycle technical micro-states (strobes text + floods the queue)"
  end-state: "past-tense done ('Upload complete') / actionable error ('Upload failed — file too large', names remediation)"
motion:
  indeterminate: "linear scale+translate (asymmetric ease); circular SVG rotation + stroke-dasharray/dashoffset; reduce-motion -> opacity pulse / static"
  determinate: "fill animates to value ~200-300ms (steady from bursty data); reduce-motion -> snap 0ms"
  completion: "settle to 100% / route-bar fill+fade"
  emerging: "M3 Expressive wavy tracks (Aug 2024, unverified)"
i18n:
  rtl: "linear bar fills from the TRAILING (right) edge leftward via logical properties; circular direction + value-label side mirror"
  format: "% symbol position / decimals / bytes / time via Intl.NumberFormat; 'Step 3 of 5' word order localizes"
implementation:
  - "determinate: role=progressbar + valuenow/min/max + valuetext; fill derives from value; CLAMP out-of-range (silent + dev warning)"
  - "indeterminate: omit valuenow + aria-busy=true on the region"
  - "throttled live-region: empty polite region on mount; track last-announced milestone in a ref; update textContent at 25/50/75 boundaries; push completion/error at value==max; NEVER bind to aria-valuenow"
  - "anti-flash: delay setTimeout (~200-500ms, cleared on early resolve -> no mount) + minDisplay lock (~500ms) deferring unmount; manage overlapping timers (cleanup)"
  - "global route-bar: thin top linear, FAKE-EASING visual trick (rush 20% -> slow 80% -> snap 100%) BUT stays indeterminate to AT (aria-busy / 'Loading page', NEVER a fake aria-valuenow) — the value contract is never faked"
  - "reduce-motion branch to opacity pulse / static indicator"
  - "don't hand-roll — React Aria useProgressBar/useMeter or the system Progress"
composition:
  stands-on: [toast (live-region pattern — milestone/completion)]
  alternative-to: [spinner (minimal inline indeterminate, no value), skeleton (content placeholder on load, prevents CLS), meter (role=meter static measurement — separate), stepper (discrete user steps), loading-Toast (promise toast)]
  composed-by: [button (loading uses a Spinner, not a bar), file-upload (determinate upload bar), measurable processes]
notes:
  contested:
    - "the determinate threshold (when can you honestly measure — don't-fake-determinate)"
    - "the announcement model (milestone-throttle vs aria-valuenow)"
    - "progress-vs-spinner-vs-skeleton lines"
    - "unified Progress+variant (practice default) vs distinct LinearProgress/CircularProgress (bundle-size argument, answered by tree-shaking)"
    - "global route-bar as part of Progress or separate"
  trap:
    - "faking a determinate VALUE (aria-valuenow) — stalls erode trust (the visual route-bar easing is OK only because it stays indeterminate to AT)"
    - "announcing every percent (SR flood)"
    - "role=progressbar for a static value / role=meter for a task"
    - "static aria-valuenow=0 on an indeterminate spinner (reads 'stalled')"
    - "removing the indeterminate animation under reduce-motion (no cue = crash)"
    - "flashing a loader for a <1s op (delay) / one frame (min-display)"
    - "label embedded in the track (contrast + truncation); faint rail <3:1 (needs stop indicator)"
  inherited: "Toast's live-region pattern (milestone/completion announcement)"
  role-in-family: "the fourth Feedback brief — the loading indicator; anchors the three-loading-patterns decision (Progress/Spinner/Skeleton) + the meter-vs-progressbar boundary; reuses the live-region pattern"
  evolution: "meter-vs-progressbar formalised; don't-announce-every-percent (milestone throttle) settled; anti-flash delay/min-display discipline; reduce-motion substitution; M3 stop indicator (1.4.11) + Expressive wavy tracks"
  unverified:
    - "external 2026 version numbers"
    - "M3 Expressive wavy tracks (Aug 2024 claim)"
    - "the live-region/progressbar AT announcement specifics — verify against current screen readers"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-progress/` (16 June 2026), the fourth Feedback brief — the loading/in-progress indicator, reusing Toast's live-region pattern for milestone/completion announcements. It stands on Toast's live-region pattern and forward-references Spinner, Skeleton, Meter, Button (loading), and Stepper. The two passes converged almost completely — the determinate-vs-indeterminate fork (the `role=progressbar` value contract; the don't-fake-determinate rule), the live-region crux (SR doesn't reliably announce `aria-valuenow` + per-percent floods → milestone-throttle at 25/50/75/100 + completion via a pre-existing polite region), the three-loading-patterns decision (Progress / Spinner / Skeleton) and the `meter`-vs-`progressbar` semantic boundary (React Aria's separate `useMeter`/`useProgressBar`), the anti-flash delay/min-display rules, and the reduce-motion-substitution problem (the indeterminate animation can't be removed — it's the only cue). External-pass contributions folded in: the **Stop Indicator** (Material 3's 4dp terminal dot for WCAG 1.4.11 when the rail can't hit 3:1), the **dashboard/gauge + segmented** variants, the concrete anti-flash timers (~200–500ms delay / ~500ms min-display), the milestone-throttle implementation (a `ref` tracking the last-announced milestone), the **value-text-never-in-the-track** rule, the reduce-motion opacity-pulse substitution (~40↔100% over ~1.5s), the indeterminate→determinate morph, the circular `stroke-dasharray`/`dashoffset` mechanics, and the global-route-bar fake-easing trick — reconciled with the don't-fake-determinate rule: the *visual* easing is acceptable only because the bar **stays indeterminate to AT** (`aria-busy`, never a fabricated `aria-valuenow`). The one genuine fork was naming — distinct `LinearProgress`/`CircularProgress` (the external's bundle-size argument) vs unified `Progress`+variant; the practice keeps unified for consistency with the catalogue's one-component-+-variant POV and flags the bundle argument as answered by tree-shaking. Claude-pass contributions: the framing as the three-loading-patterns + meter-boundary anchor, and the substrate map. The 2026 version numbers, the M3 Expressive wavy-tracks claim, and the live-region AT specifics are flagged unverified. Conformant to `components/_schema.md`. The fourth Feedback brief; Empty State remains to close the category.*

# Progress — field-truth study (Claude pass)

## 1. Framing
A Progress indicator communicates that **a task is underway** and — when it can — *how far along* it is. It is the fourth Feedback brief and reuses the **live-region announcement pattern Toast established** (for milestone/completion announcements, *not* a per-percent flood). Its defining fork is **determinate vs. indeterminate**: determinate when the system can genuinely measure advancement (a file upload's byte count, "step 3 of 5") — `role="progressbar"` with `aria-valuenow`/`valuemin`/`valuemax`; indeterminate when it can't (waiting on a server) — the animated bar/ring that **omits `aria-valuenow`** (with `aria-busy` on the region). The cardinal rule: **don't fake determinate** — a progress bar that crawls to 90% and stalls is worse than an honest spinner.

It forward-references three siblings it must be disambiguated from — the **three loading patterns** plus the meter:
- **Progress bar** — a value contract for a *known or longer* process (this brief).
- **Spinner** — the minimal *indeterminate inline busy* indicator (a button, a small area; `role=status` "Loading") — see spinner when briefed.
- **Skeleton** — the content-shaped *placeholder* for an *initial page/section load* — see skeleton when briefed.
- **`role=meter`** (the sharp, often-missed boundary) — a *static measurement* within a range (disk usage, battery, a score gauge), **not a task advancing**; it is a different role/component (Spectrum and React Aria ship `Meter` separately from `ProgressBar`).

What it *isn't*: a **Spinner** (minimal inline, no value), a **Skeleton** (placeholder, not a progress value), a **Meter** (static measurement), or a **Stepper** (discrete navigable steps, not a continuous fill — see breadcrumbs boundary). Why systems disagree: the determinate threshold, the announcement model, and the linear/circular/global placement.

## 2. Anatomy and parts
- **track + indicator** — the rail and the fill (**linear** bar) or the ring arc (**circular**); the indeterminate variant animates the indicator with no fixed value.
- **label** — the accessible name (what's progressing — "Uploading file"); `aria-label`/`labelledby`.
- **value / percentage display** — the visible "45%" / "3 of 5" / "45 MB of 100 MB" text (mirrors `aria-valuetext`).
- **buffer** — an optional secondary fill (media buffering — Material's buffer variant).
- **the live-region wiring** — a polite region (or `aria-valuetext`) carrying milestone/completion announcements (§6), reusing Toast's pattern.

## 3. Properties / API
- **`value` (+ `min`/`max`, default 0–100)** — determinate; omit/`indeterminate` for the unknown case.
- **`indeterminate`** (or value `null`/absent) — the animated, no-value variant.
- **`valueLabel` / `formatOptions` / `aria-valuetext`** — the displayed + announced value, including **non-percentage** ("Step 3 of 5", byte counts) — React Aria's `formatOptions`/`valueLabel`.
- **`variant`** — `linear` / `circular`.
- **`size` / `thickness`** — the dimensions.
- **`buffer` / `bufferValue`** — the buffered secondary fill.
- **label/aria** — `label`/`aria-label`/`aria-labelledby` (required for an accessible name).
- **anti-flash** — `delay` (don't show before ~Xms) + `minDisplay` (don't flash for <Yms) — sometimes consumer-side, but worth a documented hook (§5/§11).

## 4. States and variants
- **States:** **determinate** (a value, fill advances) / **indeterminate** (animated, no value) / **buffer** (secondary fill) / **complete** (100% / success end state) / **error** (a failed process — a determinate bar can turn error-styled). 
- **Variants:**
  - **determinate vs indeterminate** (the core fork).
  - **linear vs circular** (+ the small circular shading into Spinner — §5).
  - **placement:** inline (in a button/row) / block (a section/page loader) / **global** (the top-of-page route-change bar — nprogress/YouTube style, usually a thin indeterminate-then-complete linear bar).
  - **size** (sm/md/lg), with/without the value label.

## 5. Usage guidance
- **Use a determinate Progress bar** when you can **genuinely measure** advancement — a file upload (bytes), a multi-step process (step N of M), a known-length batch. The value reassures and sets expectations.
- **Use an indeterminate Progress bar** for a **known-ish but unmeasurable** longer process (a server operation you expect to take seconds) where a bar is the right weight.
- **Don't use a Progress bar for:**
  - A **minimal inline wait** (a button submitting, a small area) → a **Spinner** (see spinner when briefed).
  - An **initial page/section content load** → a **Skeleton** (content-shaped placeholder — see skeleton when briefed).
  - A **static measurement** (disk usage, battery, a score) → a **Meter** (`role=meter` — NOT progress; §6).
  - **Discrete navigable steps** (a checkout wizard) → a **Stepper**.
- **Decision frameworks:**
  - **Determinate vs indeterminate:** can you *measure* it? Determinate. If not, indeterminate — **never fake a determinate value** (a stalling fake bar erodes trust more than an honest spinner).
  - **Progress vs Spinner vs Skeleton:** value/longer-process (Progress) vs minimal-inline-wait (Spinner) vs content-placeholder-on-load (Skeleton).
  - **The anti-flash rules:** **delay before showing** (~300–1000ms) so a fast operation never flashes a loader; and a **minimum display time** so a loader that *does* appear doesn't vanish after one frame (the jarring flash). Both serve perceived performance.
  - **The button-loading boundary:** a Button's loading state shows a Spinner in-place (the width-preserving loading contract — see button §loading), not a Progress bar.

## 6. Accessibility
- **`role="progressbar"` + the value contract:**
  - **Determinate:** `aria-valuenow` + `aria-valuemin` + `aria-valuemax` (+ `aria-valuetext` for non-percentage/human-readable — "Step 3 of 5", "45 MB of 100 MB"); a label via `aria-label`/`labelledby`.
  - **Indeterminate:** `role="progressbar"` **without `aria-valuenow`** (AT announces it as busy/indeterminate); set **`aria-busy="true"`** on the region being loaded.
- **The live-region announcement (the crux, reusing Toast's pattern):** **progressbar value changes are NOT reliably announced** by screen readers, and announcing **every percent is a flood**. So: **throttle** — announce **milestones** (e.g. 25/50/75%) and especially **completion** (and error) via a **polite live region** (or carefully-updated `aria-valuetext`), not continuous updates. The completion/error end state is the most important thing to announce.
- **The `meter` vs `progressbar` boundary** — `role="meter"` is a *static measurement within a range* (battery, disk, a gauge), **not** a task; using `progressbar` for a static value (or `meter` for a task) is the semantic error. They're separate components (React Aria/Spectrum split them).
- **Reduce-motion can't simply remove the only indicator** — the indeterminate animation *is* the busy signal, so `prefers-reduced-motion: reduce` must **substitute** (a slowed/simplified animation, or a non-animated indicator + a visible/announced "Loading…"), not delete it. (The determinate fill transition can be dropped to an instant set.)
- **Color-not-sole-carrier** — the bar's *position/fill* conveys progress (not colour alone), and the **label + value text** are the explicit signal; the completion/error end state isn't colour-only (icon/text).
- **WCAG SCs:** 4.1.2 (name/role/value — the progressbar role + valuenow/valuetext + label), 4.1.3 (Status Messages — the milestone/completion live region), 1.4.1 (colour not alone), 2.3.3/2.2.2 (motion — the indeterminate animation + reduce-motion), 1.4.3 (contrast).

## 7. Content guidelines
- **A clear label** — name what's progressing ("Uploading photo", "Saving"), not a bare bar.
- **The value text** — "45%" for percentage, or **human-readable non-%** when it's more meaningful ("Step 3 of 5", "45 MB of 100 MB", "About 2 minutes left"); mirror it in `aria-valuetext`.
- **Completion + error messaging** — confirm done ("Upload complete") and name a failure ("Upload failed — retry"); the end state, not just the bar vanishing.
- **Don't over-narrate** — don't announce every percent (visually fine; for AT, throttle); don't pair a progress bar with a redundant spinner.

## 8. Motion and transition
- **Indeterminate:** the bar's indeterminate sweep / the ring's rotation is continuous; under `prefers-reduced-motion: reduce`, **substitute** (slow/simplify or a static indicator + "Loading…") — never remove the only cue (§6).
- **Determinate:** the fill animates smoothly to each new value (~a short ease); under reduce-motion, snap to the value.
- **Completion:** a brief settle to 100% / a success transition; the global route-bar fills then fades.
- (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** — the **linear bar fills from the trailing edge** (right-to-left) via logical properties; the circular ring direction and the value-label side mirror.
- **Number/format** — the percentage, byte counts, and time-remaining localize (`Intl.NumberFormat` / locale digits); "Step 3 of 5" word order localizes.
- **Text expansion** — the label/value text expands; don't truncate the value. (See 13-internationalization-and-rtl.)

## 10. Naming
**`Progress`** / **`ProgressBar`** is the common name (Carbon, Polaris, Primer, React Aria, Fluent, Base Web); **`ProgressIndicator`** (Material — "progress indicators" covering linear + circular); **`LinearProgress`** + **`CircularProgress`** (MUI — split by shape); **`Progress`** with `line`/`circle`/`dashboard` types (Ant). **The practice default: `Progress`** (or `ProgressBar`) with a **`variant: linear | circular`** prop and an **`indeterminate`** flag, the **global route-bar** as a placement variant, and the minimal-inline-indeterminate case routed to **`Spinner`** and the static-measurement case to **`Meter`**. Aliases to map: `ProgressBar`, `ProgressIndicator`, `LinearProgress`, `CircularProgress`, `Loader` (loosely).

## 11. Implementation notes
- **The determinate value contract** — render `role=progressbar` + `aria-valuenow`/`min`/`max` + `aria-valuetext`; the visible fill width/ring arc derives from the value; clamp out-of-range values.
- **The indeterminate case** — omit `aria-valuenow`, animate the indicator, and set **`aria-busy="true"`** on the region whose content is loading (so AT knows it's busy).
- **The throttled live-region announcement** — don't bind announcements to `aria-valuenow` (unreliable + floods); push **milestone + completion/error** strings to a polite live region (the Toast pattern — a pre-existing region), throttled.
- **The anti-flash timers** — a **delay** before showing (cancel if the op finishes first → no flash for fast ops) and a **minimum display time** once shown (so it doesn't vanish in one frame). These are the two timers that make loaders feel calm; document them as defaults/hooks.
- **Reduce-motion substitution** — branch on `prefers-reduced-motion` to a reduced/static indicator (never remove the only cue).
- **The global route-change bar** — a thin top-of-viewport linear bar that starts indeterminate on navigation and completes on load (nprogress-style); it's a `progressbar` with a label like "Loading page".
- **Don't hand-roll** — React Aria `ProgressBar`/`Meter`, or the system's `Progress`; skin them (they get the role/value/`aria-busy` right).

## 12. Related and alternative components
- **Stands on:** the **live-region announcement pattern** inherited from Toast (the Feedback substrate — for milestone/completion — see toast).
- **Alternative to / boundary with:** **Spinner** (the minimal indeterminate inline busy indicator — see spinner when briefed; the progress-vs-spinner boundary), **Skeleton** (the content-shaped initial-load placeholder — see skeleton when briefed; the third loading pattern), **Meter** (`role=meter` static measurement — *not* a task; a separate component), **Stepper** (discrete navigable steps — not a continuous fill), the **loading Toast** (a promise/loading toast — see toast §promise; shades into progress feedback).
- **Composed by:** Button (the loading state uses a Spinner, not a Progress bar — see button), File Upload (a determinate upload bar — see file-upload when briefed), forms/processes with measurable steps.

(The fourth Feedback brief — the loading/in-progress indicator, reusing Toast's live-region pattern for milestone/completion announcements and anchoring the three-loading-patterns decision (Progress / Spinner / Skeleton) plus the meter-vs-progressbar semantic boundary. See toast for the live-region pattern, spinner/skeleton/meter when briefed for the boundaries, button for the loading-button boundary, breadcrumbs for the stepper boundary. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The meter-vs-progressbar clarification** — systems separated `role=meter` (static measurement) from `role=progressbar` (task progress); React Aria/Spectrum ship `Meter` and `ProgressBar` as distinct components.
2. **The don't-announce-every-percent live-region settling** — practice converged on throttled milestone/completion announcements (a polite region) over binding AT to `aria-valuenow` (unreliable + flooding).
3. **The anti-flash discipline** (delay-before-show + minimum-display-time) spread as the perceived-performance standard for loaders.
4. **Reduce-motion-substitution** hardened — the indeterminate animation can't be removed (it's the only cue), so it's reduced/substituted, not deleted.
5. **The three-loading-patterns split** (Progress / Spinner / Skeleton) became the documented decision, with Skeleton rising for initial loads.

## 14. Sources cited
(Conservative; reconcile with external.) **Google Material 3** — Progress indicators (linear/circular, determinate/indeterminate, the buffer variant) (2024–2026); **IBM Carbon** — `ProgressBar` + `InlineLoading` + `Loading` (2024–2026); **Shopify Polaris** — `ProgressBar` + `Spinner` (2024–2026); **GitHub Primer** — `ProgressBar` + `Spinner` (2024–2026); **Adobe Spectrum / React Aria** — `ProgressBar` + `Meter` (separate; `formatOptions`/`valueLabel`) (2024–2026); **Microsoft Fluent** — `ProgressBar` + `Spinner` (2024–2026); **MUI** — `LinearProgress` + `CircularProgress` (2024–2026); **Ant Design** — `Progress` (line/circle/dashboard) (2024–2026); **Chakra** — `Progress`/`CircularProgress`/`Spinner` (2024–2026); **Base Web (Uber)** — `ProgressBar`/`Spinner` (2024); **WAI-ARIA APG** — the `progressbar` role + `aria-valuenow`/`min`/`max`/`valuetext`; the `meter` role distinction; the live-region announcement question; the inherited Feedback live-region pattern (see toast). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.2, 4.1.3, 1.4.1, 2.3.3, 2.2.2, 1.4.3.

## 15. Agent-consumable schema (conform to _schema.md in progress.md)
identity(Progress; aliases ProgressBar/ProgressIndicator/LinearProgress/CircularProgress/Loader; feedback; stable)/description(the loading/in-progress indicator — communicates a task is underway and, when measurable, how far; determinate (role=progressbar + aria-valuenow/min/max) vs indeterminate (animated, no valuenow, aria-busy); reuses Toast's live-region pattern for MILESTONE/completion announcements not per-percent; NOT a Spinner (minimal inline), NOT a Skeleton (content placeholder), NOT a Meter (static measurement, role=meter), NOT a Stepper (discrete steps))/anatomy(track + indicator (linear bar fill / circular ring arc; indeterminate animates with no value); label (accessible name); value/percentage display ('45%' / '3 of 5' / '45 MB of 100 MB'); optional buffer (secondary fill — media); live-region wiring (polite region / aria-valuetext for milestone/completion — Toast pattern))/api(inherits: toast (live-region pattern for milestone/completion); value (+min/max default 0-100) — determinate; indeterminate (value null/absent — animated no-value); valueLabel/formatOptions/aria-valuetext (displayed+announced, incl non-% 'Step 3 of 5'/bytes); variant linear|circular; size/thickness; buffer/bufferValue; label/aria-label/labelledby (required); anti-flash delay + minDisplay hooks)/states(determinate (value, fill advances) / indeterminate (animated, no value) / buffer / complete (100%/success) / error (failed process); variants determinate-vs-indeterminate, linear-vs-circular (small circular -> Spinner), placement inline/block/GLOBAL (top route-change bar nprogress-style), size +/- value label)/accessibility(role=progressbar + DETERMINATE aria-valuenow/min/max (+ aria-valuetext for non-%) + label; INDETERMINATE omits aria-valuenow + aria-busy=true on the region; LIVE-REGION crux (reuses Toast) — progressbar value changes NOT reliably announced + every-% is a flood -> THROTTLE to milestones (25/50/75) + COMPLETION/error via a polite region, not continuous; METER vs PROGRESSBAR — role=meter is a STATIC measurement (battery/disk/gauge) NOT a task, separate component; REDUCE-MOTION can't remove the only indicator -> SUBSTITUTE (slow/simplify or static + 'Loading…'); color-not-sole-carrier (position + label/value the signal); SC 4.1.2/4.1.3/1.4.1/2.3.3/2.2.2/1.4.3)/content(clear label naming what's progressing; value text '45%' or human-readable non-% ('Step 3 of 5'/'45 MB of 100 MB'/'2 min left'); completion + error messaging (confirm done / name failure, not just vanish); DON'T over-narrate (no per-% announce, no redundant spinner+bar))/motion(indeterminate sweep/rotation continuous -> reduce-motion SUBSTITUTE not remove; determinate fill animates to value -> reduce-motion snap; completion settle/route-bar fill+fade)/i18n(RTL linear bar fills from trailing edge via logical properties + ring direction + value-label side mirror; % / bytes / time-remaining localize (Intl.NumberFormat); 'Step 3 of 5' word order localizes; don't truncate the value)/implementation(determinate value contract role=progressbar + aria-valuenow/min/max/valuetext, fill derives from value, clamp out-of-range; indeterminate omits valuenow + aria-busy=true on the loading region; THROTTLED live-region — don't bind to aria-valuenow (unreliable+floods), push milestone+completion/error to a pre-existing polite region; ANTI-FLASH delay-before-show (cancel if op finishes first) + minimum-display-time (don't vanish in one frame); reduce-motion branch to a reduced/static indicator; global route-change bar = thin top linear bar indeterminate->complete; don't hand-roll — React Aria ProgressBar/Meter or the system Progress)/composition(stands-on toast (live-region pattern — milestone/completion); alternative-to spinner (minimal inline indeterminate), skeleton (content placeholder on load), meter (role=meter static measurement — separate), stepper (discrete steps), loading-Toast (promise toast); composed-by button (loading uses a Spinner not a bar), file-upload (determinate upload bar), measurable processes)/notes(contested: the determinate threshold (when can you honestly measure — don't-fake-determinate); the announcement model (throttle vs aria-valuenow); progress-vs-spinner-vs-skeleton lines; the global route-bar as part of Progress or separate. trap: faking a determinate value (stalls erode trust); announcing every percent (SR flood); role=progressbar for a static value or role=meter for a task; removing the indeterminate animation under reduce-motion (no cue left); flashing a loader for a <1s op (needs delay) / for one frame (needs min-display); colour-only completion/error. inherited: Toast's live-region pattern (milestone/completion announcement). role-in-family: the fourth Feedback brief — the loading indicator; anchors the three-loading-patterns decision (Progress/Spinner/Skeleton) + the meter-vs-progressbar boundary; reuses the live-region pattern. evolution: meter-vs-progressbar clarified; don't-announce-every-percent settled; anti-flash delay/min-display discipline; reduce-motion substitution; three-loading-patterns split. unverified: external 2026 version numbers; the live-region/progressbar AT announcement specifics — verify against current screen readers.)

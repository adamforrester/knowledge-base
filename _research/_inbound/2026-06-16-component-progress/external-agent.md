# Progress — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/progress.md`; version numbers, the M3 Expressive wavy-tracks claim, and the live-region AT specifics flagged unverified. The two passes converged almost completely; the external pass added the Stop Indicator, the dashboard/segmented variants, the concrete anti-flash/throttle timers, and the global-route-bar fake-easing reconciliation.*

---

Research Report: Progress Indicators in Enterprise Design Systems

## 1. Framing
The progress component manages user expectations during temporal uncertainty — the programmatic/visual bridge between an action and an asynchronous resolution. It stands on the live-region announcement pattern shared with Toast. The defining decision is the Determinate-vs-Indeterminate fork: determinate (known measurable metric — file upload bytes, multi-step array) requires role=progressbar + aria-valuenow/valuemin/valuemax; indeterminate (unknown duration) relies on continuous motion, OMITS aria-valuenow, and applies aria-busy=true. Universal mandate: the "don't-fake-determinate" rule — never animate a bar to ~99% and hang (violates the value contract, distorts the mental model, erodes trust). Three sibling loading patterns + the meter: Progress (longer/measurable, large area), Spinner (minimal inline indeterminate, micro-interactions), Skeleton (content-shaped placeholder for initial load, prevents CLS). The sharpest boundary: role=meter (a STATIC measurement within a range — battery/disk/score, a snapshot, no temporal directionality) vs role=progressbar (a TASK advancing toward completion). Misusing them makes AT parse incorrectly.

## 2. Anatomy
Track/rail (static spatial reference + contrast baseline). Indicator/fill (determinate: length/sweep bound to %; indeterminate: detached translation/scaling). Label (human-readable; aria-labelledby). Value Text (percentage or custom "45 MB of 100 MB"/"Step 3 of 5", tied to aria-valuetext). Buffer (lower-opacity secondary, ahead of primary — media streaming, loaded vs consumed). Stop Indicator (M3 late-2023: a 4dp circle at the terminal end for WCAG 1.4.11 — if the unfilled track <3:1 vs background, users can't perceive the bar's length). Live-Region Wrapper (visually hidden aria-live=polite, present BEFORE the sequence — SRs don't auto-announce aria-valuenow changes; injecting region+text simultaneously is ignored).

## 3. Properties / API
value/progress (number; omit/null -> indeterminate). min/max (boundaries; native % calc). variant/type (determinate/indeterminate/buffer/line/circle/dashboard). label/aria-label. format/valueText (override % for units). buffer/valueBuffer. delay/minDisplay (anti-flash). Two philosophies: headless hooks (React Aria useProgressBar — abstracts ARIA/localization/calc, DOM to the dev) vs opinionated declarative (MUI/Chakra <LinearProgress variant="determinate" value={50}/> — value sets determinate, omitting triggers indeterminate). Ant expands with steps (count or object with gap).

## 4. States and variants
Determinate vs indeterminate (Fluent 2/M3: a process may begin indeterminate while establishing connection/size, then morph to determinate). Linear (horizontal, page/section, good for adjacent text, the NProgress global route bar). Circular (space-constrained, replaces an element e.g. spinning in a submit button). Dashboard (Ant — semi-circle/arc ~295°, gauge/speedometer). Segmented/stepped (Primer/Ant — discrete blocks for phases). Buffer (linear — downloaded vs consumed). Terminal end states: Success (track fills, success token green, checkmark may replace %), Error (indicator halts, critical red, label updates to explain the failure — don't leave the user staring at a stalled bar).

## 5. Usage guidance
The Three-Loading-Patterns matrix: Skeleton for initial structural loads (reserve space, prevent CLS); Spinner for minimal inline indeterminate ~1-5s (dropdown fetch, button submit); Progress bar for >5s, measurable file size/step count, or large screen/container. The "loading flash" trap — a fast request renders a loader for a fraction of a second then disappears; the flicker degrades perceived performance (feels slower/jerkier than no indicator). Anti-flash: delay-before-showing (~200-500ms; if it resolves in the silent window, never render) + minimum-display-time (~500ms once painted, even if the op completes instantly). Button-loading boundary: a button morphs to a spinner in-place; a massive upload disables the button + spawns a separate linear determinate bar (a spinner can't show metrics).

## 6. Accessibility
The core issue: visual feedback is continuous, SR consumption is discrete. role=progressbar + updating aria-valuenow does NOT auto-trigger announcements in most browser/AT combos. Reuse Toast's live-region: a visually hidden aria-live=polite present before the sequence (injecting region+text together is ignored). NEVER announce every percent ("1 percent... 2 percent..." traps the user in an inescapable queue) -> Milestone Throttling: inject at 25/50/75/100 (completion). Determinate: role=progressbar + aria-valuenow/min/max + accessible name. Indeterminate: omit valuenow/min/max (static valuenow=0 falsely signals "stalled at 0%"); container gets aria-busy=true. The Reduce-Motion Paradox: motion is the defining characteristic of indeterminate; removing it leaves a frozen shape implying a crash. Field convergence: reduce-motion != no motion if the motion conveys status — substitute rapid loops with a slow opacity pulse (~1000-1500ms fade 40<->100%) or swap to static "Loading" + minimal ellipsis (WCAG 2.3.3). Meter vs progressbar: meter = static quantity, announced differently; React Aria provides separate useMeter/useProgressBar.

## 7. Content guidelines
Clear concise label, active verb ("Uploading"/"Saving"/"Connecting"), above/adjacent — NEVER inside the track (contrast failure as the fill sweeps behind text + truncation on narrow viewports). Concrete data over abstract %: "45 MB of 100 MB" > "45%"; "Step 3 of 5" for wizards; sync aria-valuetext when visible text deviates from %. Don't over-narrate (cycling "Resolving DNS.../Handshaking.../Parsing JSON..." strobes the label + floods the polite queue). Completion/failure: transition active verb -> past tense ("Saved"/"Upload complete") or actionable error ("Upload failed. File too large.") — instruct on remediation.

## 8. Motion
Linear indeterminate: indicator scales horizontally + translates across x (asymmetric ease-in-out). Circular indeterminate: SVG rotation + stroke-dasharray/dashoffset grow/shrink. Determinate increment: animate width/stroke-dashoffset ~200-300ms (steady narrative from bursty network chunks; instant jumps feel cheap). prefers-reduced-motion: determinate fill duration -> 0ms; indeterminate -> slow opacity keyframe (40-100% over 1.5s) (WCAG 2.3.3). M3 Expressive (Aug 2024) introduced wavy tracks (amplitude/wavelength tokens).

## 9. i18n
RTL: time maps right-to-left; linear bars originate fill on the right, progress leftward; label/percentage alignment mirror. Intl.NumberFormat for % position (50% vs %50) + decimal separators; Chakra/React Aria handle via internal formatting hooks + locale props.

## 10. Naming
Unified (Ant Progress type-prop, Primer ProgressBar) vs distinct primitives (MUI LinearProgress/CircularProgress, Fluent fluent-progress/fluent-progress-ring). Industry default leans distinct primitives for enterprise — the SVG DOM/animation/CSS for a radial spinner differ vastly from a div bar; forcing both into one component bloats the bundle with unused SVG when a dev needs a linear bar. Spinner disambiguation: though visually identical to an indeterminate CircularProgress, export a separate <Spinner> constrained to inline/small without value props, safeguarding against treating a button loader as a progress bar needing an ARIA value contract.

## 11. Implementation notes
Clamp value between min/max (silent clamp + dev-mode console warning). Throttled live-region: render empty aria-live=polite div on mount; useRef tracks last-announced milestone; cross a 25/50/75 boundary not yet announced -> update textContent to aria-valuetext; value===max -> push completion string. Anti-flash: a 200ms showTimer; if loading resolves before, clear (no mount); if breached, mount + a separate hideTimer locks the component for +500ms min. Global route-change bars: top z-index layer; technically indeterminate but use a "fake determinate" CSS easing trick (rush to 20%, slow toward 80%, snap to 100% on resolve) — but NEVER expose the fake interpolated values to SRs (aria-busy on the document / polite "Loading new page").

## 12. Related and alternative components
Toast (ancestral provider — Progress relies on its queued polite live-region announcements). Spinner (minimal circular indeterminate; no value contract/props). Skeleton (placeholder geometry before content; progress tracks temporal duration). Meter (static capacity gauge). Button (internalizes a Spinner; prevents dual-rendering a button + adjacent bar). Stepper (discrete user-driven phases; progress = system labour).

## 13. Field POV evolution
WCAG 1.4.11 enforcement revealed faint rails (#F3F4F6) make the track imperceptible -> M3 stop indicator (late 2023). The <progress>/<meter> interchangeable-use era ended; W3C/ARIA + React Aria/APG formalized the split. The sub-second SPA obsession birthed the loading-flash epidemic -> the delay/min-display pattern formalized as architectural necessity (a 50ms flash feels worse than nothing). Draconian reduce-motion (stripping all animation -> frozen spinners simulating lockups) -> the "substitution" principle (opacity transitions). M3 Expressive wavy tracks (Aug 2024) inject organic motion.

## 14. Sources cited
Google Material 3 (wavy Aug 2024, 4dp stop indicator Dec 2023, sizing tokens). IBM Carbon @carbon/react ^1.109.0 (June 2026; text alignment, onSuccess 1.5s, polite live-region testing). Shopify Polaris (ProgressBar vs Spinner known/unknown duration). GitHub Primer (multi-segment ProgressBar.Item, 3:1 segment contrast). Adobe Spectrum / React Aria v3.49.0 (useProgressBar vs useMeter semantic split). Microsoft Fluent 2 (indeterminate->determinate morph, distinct naming). MUI X v9 / MUI v5 (variant=buffer, min/max). Ant Design v5.16-v6.0 (dashboard, steps, semantic DOM tokens root/body/rail/track). Chakra v2 (Intl.NumberFormat). Base Web v18.1.0 / LobeHub (anti-flash timers, min display, standalone spinner). W3C WAI-ARIA APG + HTML-AAM (progressbar role, live-region DOM injection, meter mapping disputes).

## 15. Agent-consumable schema

```yaml
type: component
category: Feedback
description: A temporal indicator managing user expectations during active computational tasks, via determinate (measurable) or indeterminate (unmeasurable) states.
inherits:
  - pattern: live-region-announcement (from Toast)
    details: pre-existing visually-hidden aria-live=polite container injected before updates; reliable milestone announcements without dropping events.
anatomy: [track, indicator, label, valueText, buffer, stopIndicator (M3 4dp for 1.4.11)]
api:
  - value: number | null (null -> indeterminate)
  - min/max: number
  - variant: enum (determinate, indeterminate, buffer, line, circle, dashboard)
  - format/valuetext: function/string
accessibility:
  - role: progressbar (advancing tasks) NOT meter (static capacity)
  - properties: aria-valuenow/min/max (determinate only)
  - properties: aria-busy (regions with indeterminate operations)
  - live-region: throttle to milestones (25/50/75/100), avoid per-percent spam
  - motion: prefers-reduced-motion -> slow opacity pulse or static text, never frozen dead states
usage:
  - boundaries: Progress for measurable/long (>5s); Spinner for minimal/inline/short; Skeleton for layout loading (CLS)
  - timers: 200ms delay + 500ms min-display anti-flash
```

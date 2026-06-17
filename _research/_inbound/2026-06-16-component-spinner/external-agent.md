# Spinner — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/spinner.md`; version numbers and the M3 May-2025 "Loading indicator" separation flagged unverified. The two passes converged almost completely; the external pass corroborated the separate-primitive recommendation (M3 fractured it out) and added disableShrink, the disabled-vs-aria-disabled focus trap, the time thresholds, and the RTL force-clockwise rule.*

---

The Spinner Component: Architectural Primitives, State Management, and Accessibility

## 1. Framing
The loading state is a triad: Progress Bar, Skeleton, Spinner. The Spinner operates under a strict "no-value contract" — the minimal, indeterminate, inline indicator that a process is active but whose duration/percentage can't be quantified. Unlike a determinate progress bar (aria-valuenow, a measurable transition to a known endpoint) or a Skeleton (a structural placeholder predicting the incoming layout to reduce CLS), the Spinner is structurally agnostic and fundamentally inline (elevated to block/overlay via wrappers). The Progress-vs-Spinner split is among the most debated decisions. Older paradigms conflated them in one CircularProgress with a boolean toggle; Material Design 3 fractured the monolith, introducing the "Loading indicator" as a separate primitive for short tasks (<5s), separated from the indeterminate progress indicator. The semantic meanings differ: a progress bar implies eventual completion of a measurable task; a spinner implies busyness/a suspended state awaiting server resolution. Opinionated default: ship the Spinner as a distinct primitive, not an isIndeterminate variant of ProgressCircle — so developers don't map value contracts to inline button loaders, simplifying the API and reducing malformed-progressbar-ARIA violations.

## 2. Anatomy and Parts
Visual Indicator (Head + Track): an <svg> with a faint background circle (track) + an animated foreground stroke (head). Base Web/Chakra expose TrackPath/ActivePath subcomponents. SVG replaced border-radius animations and GIFs (perfect HiDPI scaling + currentColor inheritance). Accessible Wrapper (live-region wiring): the SVG is silent unless annotated; wrapped in <span role="status"> / <div aria-live="polite">. Fluent v9 designates spinner / spinnerTail slots. Optional Label/Description: Ant's description (deprecating tip); can be visually hidden via clip. Overlay Mask/Backdrop (context-dependent): Ant's embedded mode / fullscreen wraps content in a relative container, injects an absolute overlay mask dimming the underlying content, centers the spinner on z-axis — converting the inline primitive into a blocking element.

## 3. Properties / API
size (enum/string — Spectrum strict t-shirt S/M/L; MUI numeric px/rem; strict semantic scale recommended). color (default currentColor — inherits parent text color). thickness (often tied to size; Chakra explicit). delay (ms, default 0 — the anti-flash mechanism). label (ReactNode — replaces legacy tip). labelPosition (before/after/above/below — Fluent flex-direction). spinning (boolean — overlay/embedded toggle). The delay property (200-500ms) intercepts the render cycle: if a promise resolves in 150ms the spinner never mounts (bypassing layout thrash); Fluent v9 and Ant treat delay as first-class. API divide: Base Web exhaustive overrides (drill into Svg/TrackPath) for multi-tenant brand; Adobe Spectrum locked-down (only staticColor white/black) for consistency.

## 4. States and Variants
Theoretically stateless (binary active/inactive); compositional variants dictate DOM/layout interaction. Bare/Inline: unadorned inline-flex beside typography (Carbon InlineLoading for create/update/delete; preserves text flow). Nested/Overlay: Ant Spin wraps children, position:relative, reduces opacity of wrapped children, centers the SVG absolutely; fullscreen expands to viewport (merges the visual cue with modal-overlay interaction-blocking). Static Color: Spectrum staticColor (white/black) over full-bleed imagery/video/banners where theme tokens fail WCAG contrast. Button-Loading Composition (the single most common): isPending (Spectrum) / isLoading (Base Web/Chakra); the spinner replaces the leading icon or the text label; requires strict width-preservation to prevent horizontal collapse and layout shift.

## 5. Usage Guidance
M3's time-based heuristics. <200ms: no indicator (a sub-200ms spinner strobes and degrades perceived performance; use optimistic state updates). 200ms-5s: the Spinner/Loading Indicator (the indeterminate loop captures attention without computing progress). >5s: a Determinate Progress Bar (extended indeterminate spinning increases anxiety / implies a stall/infinite loop). M3 explicitly forbids transitioning from an indeterminate loading indicator directly into a determinate progress indicator (the shifting paradigm confuses). Primer warns against over-use (a 20-widget dashboard shouldn't fire 20 spinners — use a unified Skeleton for the layout, reserve the Spinner for granular user-triggered micro-interactions). Carbon: interactive elements associated with the fetched data must be disabled during the spin (introduces focus-management challenges).

## 6. Accessibility
The most contested topic. A bare animated <svg> has no semantic meaning — silent to a screen reader, a severe WCAG violation if it's the sole status indicator. Three methodologies. (1) Indeterminate Progressbar Role (MUI/Chakra): role="progressbar" + aria-label="Loading…"; but the APG notes progressbar is for measurable progress, and relying on it for a pure status indicator makes some SRs persistently announce the lack of a value (cognitive noise). (2) Status Role (APG recommended): role="status" (implicit aria-live=polite) announces text content without stealing focus; inject a visually hidden "Loading" span (mirrors the Toast pattern). (3) Silent Graphic + Region Busy (Primer): the SVG is aria-hidden="true" (decorative); set aria-busy="true" on the region being updated (SR halts partial-DOM-update announcements until false) + an external aria-live notification.

The loading-button focus trap: native disabled removes the element from the a11y tree and drops keyboard focus — a visually-impaired user who activates a button that instantly disables has focus violently thrown to document.body. The systemic solution (USWDS, increasingly enterprise): aria-disabled="true" instead of disabled (exposes inactive but keeps the button in the focus order), then manually suppress onClick/onPress via JS. The opinionated default for any new system.

Reduce-motion paradox: removing the motion entirely implies a crash. Primer: loading animations should not be removed for reduced-motion users but made as subtle as possible. Emerging consensus: substitution not elimination — a slow opacity pulse (multi-second) or a static indicator + a text ellipsis updated via low-frequency intervals.

## 7. Content Guidelines
The "Never Unlabeled" directive — always a label, even if visually hidden via clip-rect. High specificity over generic "Loading…" (Primer: "Loading status checks" / "Processing transaction" — reassures the system is doing the exact task, lowers abandonment). Sentence case ("Updating profile") over title case (lower cognitive load, conversational). Avoid progressive over-spinning — chaining "Fetching…/Parsing…/Rendering…" floods aria-live; a single holistic status for the lifecycle.

## 8. Motion
Two concurrent transforms: continuous 360deg rotation of the SVG canvas + a dynamic stroke (animating stroke-dasharray/stroke-dashoffset so the visible line chases its tail). The CPU Main-Thread Blocking Problem: SVG stroke animations are layout/paint-engine-computed, susceptible to jank; under high main-thread load (parsing a massive JSON, rendering a complex tree) the stroke-dasharray animation drops frames or freezes, looking broken. MUI's disableShrink prop turns off the expensive stroke-dasharray, leaving only the cheaper GPU transform:rotate. prefers-reduced-motion: removing motion implies a crash; Primer dictates loading animations made subtle not removed; substitution — replace the 360deg rotation with a slow opacity pulse or a static indicator + a periodically-updated text ellipsis.

## 9. Internationalization
RTL force-clockwise (Adobe Spectrum explicit exception): when the UI flips RTL, standard elements mirror via logical properties, BUT progress circles/spinners must continue clockwise. Mechanical/chronological paradigms (a clock face, a turning wheel) are universal representations of elapsed time/ongoing process; mirroring to counter-clockwise creates cognitive dissonance (implies undo/backward action). labelPosition must be context-aware: an after label renders logically left of the spinner in Arabic via the flexbox respecting RTL. currentColor for the stroke ensures i18n neutrality.

## 10. Naming
Material 3 "Loading indicator" (separated from Progress; replaced M2's indeterminate CircularProgress to emphasize short waits). IBM Carbon "Inline loading" (action/position over geometry). GitHub Primer "Spinner" (distinct isolated SVG, indeterminate only). Adobe Spectrum "ProgressCircle" (merged — isIndeterminate variant). MUI "CircularProgress" (merged — variant=indeterminate default). Ant "Spin" (independent — inline primitive + masking wrapper). Recommended: "Spinner" — disambiguates from Progress, signals indeterminate busyness/no value props; merging into CircularProgress blurs the measurable-vs-blocking boundary. Loader/ActivityIndicator (React Native) acceptable but less descriptive.

## 11. Implementation Notes
DOM: <span role=status aria-live=polite> > <svg aria-hidden=true viewBox> (circle track + circle head) + <span class=visually-hidden>Loading data…</span>. Anti-flash delay: a useDelay hook initiates setTimeout on mount, returns null until the delay threshold; a companion minDisplayTime keeps it visible >=500ms once committed for visual stability. Button width preservation: when a text label ("Submit Form") is replaced by a small spinner, the button shrinks and the layout reflows violently; calculate the button's width on onClick, apply a hard min-width/width inline before transitioning to isLoading, freezing dimensions.

## 12. Related and Alternative Components
Progress Bar (determinate): the measurable, value-driven sibling; shares the anti-flash + reduce-motion substrates but adds a value contract (aria-valuenow); >5s. Skeleton: the content-placeholder boundary (pre-paints layout, reduces CLS); Spinners are for subsequent micro-interactions/small refreshes. Button: the primary compositional target (isLoading; aria-disabled focus retention + width calc). Toast/Snackbar: the conclusion boundary (a spinner resolves -> a Toast verifies success/failure, closing the feedback loop).

## 13. Field POV Evolution
GIF -> CSS border-radius -> inline SVG (mathematical precision for track/dash-offset). Five years ago nearly all systems conflated Spinner with Progress Bar (Material 2); the realization that indeterminate is a fundamentally different psychological/semantic contract led to the current bifurcation (M3's distinct "Loading indicator"). The never-unlabeled hardening shifted away from bare visual decorations (a raw SVG without aria-live/aria-busy excludes visually impaired users). The shift from disabled to aria-disabled in Button-Spinner compositions marks the current leading edge — preserving user focus/workflow over mere contrast-checker compliance.

## 14. Sources Cited
Google Material Design 3: Loading indicator and Progress indicator (Expressive Update, May 2025). IBM Carbon: React v1.109.0, Inline Loading. GitHub Primer: Spinner, accessibility/loading UI. Adobe React Spectrum: v3.0.0 ProgressCircle, S2 Migration. Microsoft Fluent UI: React v9.74.1, Spinner overrides. MUI: v4/v5 CircularProgress, disableShrink. Ant Design: v5/v6 Spin, Embedded mode, delay, Fullscreen. Chakra UI: v1/v2 Spinner. Base Web: v11 Spinner, Button isLoading, Overrides. Shopify Polaris: Spinner. WAI-ARIA APG: Meter, Progressbar, Status role guidelines.

## 15. Agent-Consumable Schema

```yaml
component_identity:
  name: Spinner
  aliases: [Loading, Inline loading, CircularProgress, ProgressCircle, Spin, Loader, ActivityIndicator]
  category: Feedback / State
  contract: minimal, indeterminate, inline, no-value
anatomy:
  elements:
    - {name: wrapper, dom: span|div, semantics: [role=status, aria-live=polite]}
    - {name: svg_container, dom: svg, aria: aria-hidden=true}
    - {name: track, dom: circle, role: visual_background}
    - {name: head, dom: circle, role: visual_indicator}
    - {name: label, dom: span, modifiers: [visually_hidden, visible]}
    - {name: overlay_mask, dom: div, condition: contextual (embedded/fullscreen)}
api:
  props:
    size: {type: enum|string, default: M}
    color: {type: string, default: currentColor}
    thickness: {type: number|string, default: auto (scales with size)}
    delay: {type: number(ms), default: 0}
    label: {type: string|ReactNode, required: true (fallback visually hidden)}
    labelPosition: {type: enum [before, after, above, below], default: after}
accessibility:
  roles: {preferred: 'role=status + visually hidden label', fallback: 'role=progressbar + aria-label', region_wrapper: 'aria-busy=true on parent'}
  button_composition: {focus_retention: 'use aria-disabled=true instead of disabled'}
  motion: {reduce_motion: 'substitute infinite 360deg with slow opacity pulse (do not freeze)'}
internationalization:
  rtl_behavior: force clockwise rotation
  layout: reverse labelPosition logically via flex-direction
dependencies:
  inherits: [anti_flash_delay (from Progress), reduce_motion_substitution (from Progress)]
  composed_by: [Button (isLoading state)]
  boundaries: [Progress (determinate/valuenow), Skeleton (structural placeholders)]
```

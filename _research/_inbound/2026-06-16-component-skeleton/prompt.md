You are researching the Skeleton component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a skeleton
/ skeleton screen is, knows what a design system is, and has shipped
multiple component libraries. Explain the non-obvious — the prop choices
field leaders disagree on, the accessibility decisions still contested,
the implementation traps that recur across codebases.

Skeleton is a Foundations loading primitive that CLOSES the three-loading-
patterns triad (Progress / Spinner / Skeleton) the Progress and Spinner
briefs anchored. It is the content-shaped placeholder for an INITIAL load.
It STANDS ON the loading-family substrate and boundaries with its siblings:
- THE ANTI-FLASH (delay/min-display) + the aria-busy REGION pattern are
  INHERITED from PROGRESS and SPINNER (components/progress.md,
  components/spinner.md): the same delay-before-show / min-display timers,
  and the aria-busy="true" on the loading region. Don't re-derive these —
  reference them and resolve the Skeleton-specific substance (below).
- THE "LOADING" ANNOUNCEMENT lightly reuses the LIVE-REGION PATTERN from
  TOAST (components/toast.md): a status announcement, not the skeleton
  boxes themselves. Don't re-derive the pattern.
It boundaries with Spinner (the minimal no-shape inline busy indicator —
see components/spinner.md), Progress (the value/measurable sibling — see
components/progress.md), and Empty State (the EMPTY terminal state — see
components/empty-state.md; Skeleton is the LOADING terminal state of the
same data-container machine). It is the initial-load state of the Data /
Card / Image hosts (Table/List/Card — not yet briefed).

THE DEFINING SKELETON-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE CONTENT-SHAPED / LAYOUT-RESERVING CONTRACT (the headline, the
  Spinner opposite): a Skeleton mimics the SHAPE and DIMENSIONS of the
  incoming content (text lines, avatar circles, image/card rectangles) to
  RESERVE the layout and reduce Cumulative Layout Shift (CLS), and to make
  the wait feel shorter (perceived performance). Resolve the contract, the
  shape-match-fidelity requirement, and the skeleton-MISMATCH trap (a
  skeleton whose shape/size doesn't match the real content causes a WORSE
  jump than no skeleton).
- THE THREE-LOADING-PATTERNS DECISION (from the Skeleton side): Skeleton
  for an INITIAL page/section load where the layout is known/predictable
  (lists, cards, profiles, feeds, tables); Spinner for a minimal inline
  indeterminate micro-interaction / short or unknown-layout wait; Progress
  for a measurable/longer task. Resolve when each applies.
- THE REDUCE-MOTION DIFFERENCE FROM SPINNER (the sharp accessibility/
  motion point): a Skeleton's information is the SHAPE, not the motion —
  so unlike a Spinner (whose motion is the only cue and must be
  SUBSTITUTED), prefers-reduced-motion can simply DROP the shimmer/pulse
  to a STATIC skeleton (the shape still communicates "loading"). Resolve
  this distinction and the shimmer-vs-pulse-vs-static animation debate.
- THE ACCESSIBILITY MODEL (the contested point): the skeleton is
  PRESENTATIONAL scaffolding, not content — it must be aria-hidden (don't
  let a screen reader read "gray box gray box gray box"); the LOADING
  REGION carries aria-busy="true" + a status announcement ("Loading"),
  flipping to false + the content on resolution. Resolve the
  aria-hidden-skeleton + aria-busy-region + status pattern and the
  focus/announcement on load-complete.
- THE VARIANT MODEL + AUTO-DERIVATION — the primitive variants (text/lines
  with a shorter last line, circular/avatar, rectangular/rounded/image)
  vs per-component skeletons (SkeletonText / SkeletonAvatar / SkeletonButton
  / SkeletonImage); the auto-derive-dimensions-from-children approach (MUI
  infers from the wrapped element) vs hand-built SKELETON SCREENS (Polaris
  SkeletonPage — a whole layout of skeletons mirroring the final page).
  Resolve the variant model + the auto-vs-hand-built trade.
- THE SHAPE-MATCH / CLS purpose — the skeleton must match the content's
  final dimensions so there's NO layout shift on swap (the whole point);
  the don't-skeleton-everything discipline; the skeleton-screen composition.
- THE ANTI-FLASH (inherited) — delay-before-show + min-display applied to
  skeletons (don't flash a skeleton for a fast load; don't vanish it in a
  frame).
- ANIMATION + COLOR — shimmer (a gradient sweep) vs pulse (opacity) vs
  static; the base + highlight color tokens; dark mode; the RTL shimmer
  direction (the sweep flips).

Field-leader systems to survey (web): MUI (Skeleton — variant text/
circular/rectangular/rounded, infers dimensions from children, animation
pulse/wave/false), Ant Design (Skeleton — avatar/title/paragraph/active +
Skeleton.Image/Button/Input/Avatar/Node), IBM Carbon (SkeletonText /
SkeletonPlaceholder / SkeletonIcon + the DataTable skeleton), Shopify
Polaris (SkeletonBodyText / SkeletonDisplayText / SkeletonThumbnail /
SkeletonPage — the skeleton-screen composition), GitHub Primer (SkeletonText
/ SkeletonAvatar / SkeletonBox), Chakra UI (Skeleton / SkeletonCircle /
SkeletonText + isLoaded), Microsoft Fluent (Skeleton + SkeletonItem),
Adobe Spectrum / React Aria (the skeleton/loading patterns), Google
Material 3 (loading/placeholder guidance), Base Web (Uber) (Skeleton).
WAI-ARIA APG (no formal skeleton pattern — aria-hidden + aria-busy + the
status role). Mobile reference where relevant. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Progress/Spinner anti-flash +
aria-busy region substrate and the Toast live-region pattern; flag
unverified claims under notes.unverified).

1. Framing — what it is (the content-shaped initial-load placeholder) and
   what it isn't (a Spinner with no shape / a Progress with a value / an
   Empty State); the layout-reserving/CLS contract + the three-loading-
   patterns decision up front; why systems disagree.
2. Anatomy and parts — the placeholder shapes (text line / circle / rect),
   the base + highlight, the skeleton screen (composed), the aria-busy
   region wiring.
3. Properties / API — variant (text/circular/rectangular/rounded), width/
   height, lines (count), animation (pulse/wave/none), isLoaded/loading,
   the auto-derive-from-children, per-component skeletons.
4. States and variants — loading (the only state) -> content swap; text/
   circular/rectangular; per-component vs primitive; the skeleton screen;
   animation variants.
5. Usage guidance — Skeleton (initial known-layout load) vs Spinner
   (minimal/inline/short) vs Progress (measurable) vs Empty State (the
   empty terminal state); the shape-match rule + the mismatch trap; the
   don't-skeleton-everything + the anti-flash discipline.
6. Accessibility — the skeleton is aria-hidden (presentational), the
   region carries aria-busy + a status "Loading" announcement, the
   load-complete swap + focus, the never-read-the-boxes rule, WCAG SCs.
7. Content guidelines — the skeleton has no content (it's scaffolding);
   the shape-match guidance; the loaded announcement; don't fake content.
8. Motion and transition — shimmer vs pulse vs static, the reduce-motion
   DROP-to-static (the Spinner difference), the content-swap transition.
9. Internationalization — RTL (the shimmer sweep direction flips, the
   shape layout mirrors), text-line skeletons + expansion, dark mode.
10. Naming — Skeleton / Placeholder / Shimmer / Ghost; the practice's
    default; the per-component naming; aliases.
11. Implementation notes — the aria-hidden skeleton + aria-busy region +
    status, the shape-match-the-final-layout (CLS), the auto-derive vs
    skeleton-screen, the anti-flash delay + min-display, the shimmer/pulse
    + reduce-motion drop, the isLoaded swap, headless vs opinionated.
12. Related and alternative components — typed relationships (Progress/
    Spinner loading siblings + the inherited anti-flash/aria-busy, Empty
    State the empty terminal state, the Data/Card/Image hosts, the Toast
    live-region pattern).
13. Field POV evolution — recent shifts (skeleton-over-spinner for initial
    loads, the shape-match/CLS discipline, the aria-hidden+aria-busy
    settling, shimmer-vs-pulse, the reduce-motion-drop-to-static).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a skeleton is — explain the
content-shaped/layout-reserving (CLS) contract (the Spinner opposite) + the
shape-match/mismatch trap, the three-loading-patterns decision, the
reduce-motion difference from Spinner (drop-to-static because the cue is
the shape not the motion), the accessibility model (aria-hidden skeleton +
aria-busy region + status, never read the boxes), the variant model +
auto-derive-vs-skeleton-screen, and the shimmer-vs-pulse animation that
field leaders still diverge on.

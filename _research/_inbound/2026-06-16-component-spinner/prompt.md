You are researching the Spinner component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a spinner
/ loading indicator is, knows what a design system is, and has shipped
multiple component libraries. Explain the non-obvious — the prop choices
field leaders disagree on, the accessibility decisions still contested,
the implementation traps that recur across codebases.

Spinner is a Foundations loading primitive — the MINIMAL, indeterminate,
inline busy indicator — and one corner of the three-loading-patterns
triad (Progress / Spinner / Skeleton) that the Progress brief anchored.
It STANDS ON two briefed substrates and is composed by Button:
- THE ANTI-FLASH (delay/min-display) + REDUCE-MOTION substitution +
  the indeterminate-busy contract are INHERITED from PROGRESS
  (components/progress.md): Spinner is the minimal, NO-VALUE, inline
  sibling of an indeterminate Progress indicator (Progress is the value
  contract / longer-or-measurable case; Spinner is the small inline case).
  Don't re-derive these — reference them and resolve the Spinner-specific
  substance (below).
- THE "LOADING" ANNOUNCEMENT lightly reuses the LIVE-REGION PATTERN from
  TOAST (components/toast.md): a status/"Loading" announcement via
  role=status, not focus. Don't re-derive the pattern.
It is COMPOSED BY BUTTON (components/button.md) — the spinner-in-a-button
loading state is the single most common use. It boundaries with Skeleton
(the content-placeholder loading pattern — not yet briefed) and Progress
(the determinate / value sibling — see components/progress.md).

THE DEFINING SPINNER-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE MINIMAL / INDETERMINATE / INLINE / NO-VALUE CONTRACT (the headline,
  the Progress-vs-Spinner boundary from the Spinner side): a Spinner is a
  small indeterminate busy indicator with NO value contract (no
  aria-valuenow), for ~1-5s waits in a button, a small area, or a
  dropdown fetching. Resolve the contract and when it's a Spinner vs a
  Progress bar vs a Skeleton (the three-loading-patterns decision restated).
- THE SPINNER-vs-INDETERMINATE-CIRCULAR-PROGRESS OVERLAP (the naming/
  architecture question): a spinner is visually identical to an
  indeterminate CircularProgress; some systems make Spinner a separate
  primitive (Polaris/Primer/Fluent/Chakra/Ant Spin), others fold it into
  CircularProgress (MUI) or ProgressCircle (Spectrum). Resolve whether to
  ship a SEPARATE Spinner (constrained to inline/small/no-value, so a
  button loader isn't mistaken for a progressbar needing a value contract)
  vs a variant.
- THE ACCESSIBILITY ANNOUNCEMENT (the contested point): how is a spinner
  announced? Resolve the options — role=status + a visually-hidden
  "Loading" label (announced once, the common practice), vs
  role=progressbar (indeterminate, no valuenow), vs aria-busy="true" on
  the region being loaded; and the hard rule that a spinner must NEVER be
  unlabeled (a bare animated SVG is silent to AT). The
  spinner-replaces-content vs spinner-overlays-content focus question.
- THE BUTTON-LOADING COMPOSITION (the most common use): the spinner inside
  a Button's loading state — width-preserving (don't reflow the button),
  disable-during-load / aria-disabled, the label-stays-or-is-replaced
  question, and the announcement of the loading state. (Inherits the
  Button loading contract — see components/button.md.)
- THE ANTI-FLASH + REDUCE-MOTION (inherited from Progress): the
  delay-before-showing (~200-500ms — don't flash a spinner for a fast op)
  + minimum-display-time (~500ms); and the reduce-motion problem (the
  rotation IS the only cue, so prefers-reduced-motion SUBSTITUTES — a slow
  opacity pulse / static "Loading…", never removes). Resolve how these
  apply to the inline spinner.
- PLACEMENT — inline (in a button / next to text / in a small control)
  vs centered/overlay/block (a section/page loader; the nested-content
  masking pattern — Ant Spin wrapping content with an overlay + the
  scroll/interaction-blocking question).
- SIZING + COLOR — size scales to context (button-sized to page-sized);
  currentColor / inherit so it adopts the surrounding text/brand color;
  the track-vs-head treatment; thickness.

Field-leader systems to survey (web): Google Material 3 (Circular progress
indicator — indeterminate; Material folds the spinner into circular
progress), IBM Carbon (Loading / InlineLoading — the spinner + the inline
loading-with-text + success states), Shopify Polaris (Spinner), GitHub
Primer (Spinner), Adobe Spectrum / React Aria (ProgressCircle indeterminate
/ the absence of a distinct Spinner — a finding), Microsoft Fluent (Spinner),
MUI (CircularProgress — no separate Spinner), Ant Design (Spin — the
nested-content mask + the delay prop + tip text), Chakra UI (Spinner),
Base Web (Uber) (Spinner / the in-button spinner). WAI-ARIA APG (no formal
spinner pattern — role=status / aria-busy / the indeterminate progressbar).
Mobile reference where relevant. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Progress anti-flash/reduce-motion/
indeterminate-busy substrate and the Toast live-region pattern; flag
unverified claims under notes.unverified).

1. Framing — what it is (the minimal indeterminate inline busy indicator)
   and what it isn't (a Progress bar with a value / a Skeleton placeholder);
   the no-value contract + the three-loading-patterns decision up front;
   why systems disagree.
2. Anatomy and parts — the rotating indicator (SVG arc/ring), the optional
   label/tip text, the optional overlay/mask, the live-region wiring.
3. Properties / API — size, color (currentColor), label/aria-label, the
   delay (anti-flash), the overlay/nested-content (spinning prop), the
   thickness/track.
4. States and variants — spinning (the only state); sizes; inline vs
   overlay/centered; with-label / bare; in-button.
5. Usage guidance — Spinner (minimal inline indeterminate, ~1-5s) vs
   Progress (value/longer) vs Skeleton (content placeholder); the
   button-loading use; the anti-flash rules; the overlay-vs-inline choice.
6. Accessibility — role=status + "Loading" vs role=progressbar
   (indeterminate) vs aria-busy on the region, the never-unlabeled rule,
   the reduce-motion substitution, the focus/announcement on
   load-start/load-complete, WCAG SCs.
7. Content guidelines — the "Loading" label, contextual labels, the
   loaded announcement, don't-over-spin.
8. Motion and transition — the rotation (SVG stroke-dasharray / rotate),
   smoothness, the reduce-motion substitution, the appear/disappear.
9. Internationalization — RTL (rotation direction neutrality, the label
   side), the label text, currentColor neutrality.
10. Naming — Spinner / Loading / CircularProgress / ProgressCircle / Spin;
    the practice's default; the Progress disambiguation; aliases.
11. Implementation notes — the no-value indeterminate markup (role=status
    / aria-busy), the anti-flash delay + min-display, reduce-motion
    substitution, the in-button width-preservation, the overlay/mask +
    interaction blocking, currentColor theming, headless vs opinionated.
12. Related and alternative components — typed relationships (Progress
    value sibling + the inherited anti-flash/reduce-motion, Skeleton
    content-placeholder boundary, Button loading composition, the Toast
    live-region pattern).
13. Field POV evolution — recent shifts (the spinner-vs-circular-progress
    consolidation, the never-unlabeled accessibility hardening, the
    anti-flash discipline, reduce-motion substitution).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a spinner is — explain the
minimal/indeterminate/inline/no-value contract (the Progress-vs-Spinner
boundary), the Spinner-vs-indeterminate-CircularProgress overlap (separate
primitive vs variant), the accessibility announcement (role=status +
"Loading" vs progressbar-indeterminate vs aria-busy + the never-unlabeled
rule), the button-loading composition, the anti-flash + reduce-motion
(inherited from Progress), and the inline-vs-overlay placement that field
leaders still diverge on.

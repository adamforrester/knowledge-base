You are researching the Progress component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a progress
indicator is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Progress is the FOURTH Feedback brief — the loading/in-progress indicator.
It STANDS ON one category substrate and forward-references three siblings:
- THE LIVE-REGION ANNOUNCEMENT PATTERN is INHERITED from TOAST
  (components/toast.md), which established it for the Feedback category
  (role=status/polite + the pre-existing-region rule). Progress reuses it
  for MILESTONE / completion announcements (NOT every percent). Don't
  re-derive the pattern — reference it and resolve the progress-specific
  announcement question (below).
It FORWARD-REFERENCES: Spinner (the minimal indeterminate inline busy
indicator — not yet briefed; draw the progress-vs-spinner boundary),
Skeleton (the content-shaped placeholder for initial load — not yet
briefed; draw the third loading-pattern boundary), Button (the
loading-button state — see components/button.md), and Stepper (the
multi-step boundary — not yet briefed).

THE DEFINING PROGRESS-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE DETERMINATE vs INDETERMINATE FORK (the headline): determinate (a
  known, measurable percentage — role=progressbar with aria-valuenow /
  aria-valuemin / aria-valuemax) vs indeterminate (unknown duration — the
  animated bar/ring; OMITS aria-valuenow). Resolve the decision (use
  determinate ONLY when you can genuinely measure — file upload, multi-step
  byte count; indeterminate when you cannot — waiting on a server; the
  DON'T-FAKE-DETERMINATE rule) and the ARIA contract for each (incl.
  aria-busy on the region for indeterminate).
- THE LIVE-REGION ANNOUNCEMENT (the accessibility crux, reusing Toast's
  pattern): progressbar value changes are NOT reliably announced by AT, so
  resolve how progress is announced — DON'T announce every percent (a
  screen-reader flood); throttle to MILESTONES (e.g. 25/50/75%) and
  COMPLETION via a polite live region / aria-valuetext updates; the
  completion + error/success end states; aria-valuetext for non-percentage
  progress ("Step 3 of 5", "45 MB of 100 MB").
- THE PROGRESS vs SPINNER vs SKELETON THREE-LOADING-PATTERNS DECISION (the
  defining boundary): Progress bar (determinate or a longer/known
  indeterminate process, with a value contract) vs Spinner (the minimal
  indeterminate inline busy indicator — a button, a small area, role=status
  "Loading") vs Skeleton (the content-shaped placeholder for an initial
  page/section load). Resolve when each applies.
- THE METER vs PROGRESSBAR BOUNDARY (the sharp, often-missed semantic
  point): role=meter is a STATIC measurement within a known range (disk
  usage, battery, score, a rating gauge) — NOT a task advancing toward
  completion; role=progressbar is a TASK progressing toward completion.
  Resolve the rule and that they are different roles/components.
- LINEAR vs CIRCULAR + PLACEMENT — linear bar vs circular ring; inline (in
  a button/row) vs block (a section/page loader) vs GLOBAL (the
  top-of-page route-change loading bar — nprogress/YouTube style); the
  buffer variant (media buffering — Material).
- THE ANTI-FLASH RULES — delay-before-showing (don't flash a
  spinner/bar for a <~1s operation) and minimum-display-time (don't flash
  it for one frame if the op completes instantly); the perceived-
  performance trade.
- MOTION + REDUCE-MOTION (the hard case): the indeterminate animation IS
  the only indication, so prefers-reduced-motion can't simply remove it —
  resolve the substitution (a non-animated / reduced indicator, or a
  "Loading…" text); the circular-spinner rotation; the determinate fill
  transition.
- THE VALUE DISPLAY + LABEL — the visible "Uploading… 45%" / "3 of 5"
  text, the accessible label (aria-label/labelledby), and color-not-sole-
  carrier (position conveys it, but the label/value is the signal).

Field-leader systems to survey (web): Google Material 3 (Progress
indicators — linear/circular, determinate/indeterminate, the buffer
variant), IBM Carbon (ProgressBar + InlineLoading + Loading spinner),
Shopify Polaris (ProgressBar + Spinner), GitHub Primer (ProgressBar +
Spinner), Adobe Spectrum / React Aria (ProgressBar + Meter as SEPARATE
components — the meter distinction), Microsoft Fluent (ProgressBar +
Spinner), MUI (LinearProgress + CircularProgress), Ant Design (Progress —
line/circle/dashboard), Chakra (Progress + CircularProgress + Spinner),
Base Web (Uber) (ProgressBar + Spinner). WAI-ARIA APG (the progressbar
role + aria-valuenow/min/max/valuetext; the meter role distinction; the
live-region announcement question). Mobile reference where relevant.
Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Toast live-region pattern; flag
unverified claims under notes.unverified).

1. Framing — what it is (the loading/in-progress indicator) and what it
   isn't (a Spinner / a Skeleton / a Meter / a Stepper); the
   determinate-vs-indeterminate + the three-loading-patterns realities up
   front; why systems disagree.
2. Anatomy and parts — the track + indicator (linear/circular), the label,
   the value/percentage display, the buffer; the live-region wiring.
3. Properties / API — value/min/max (determinate), indeterminate,
   valuetext/label, variant (linear/circular), size, the buffer, the
   anti-flash delay/min-display.
4. States and variants — determinate/indeterminate; linear/circular;
   inline/block/global; buffer; completion/success/error end states; sizes.
5. Usage guidance — Progress (value contract, longer/known) vs Spinner
   (minimal inline indeterminate) vs Skeleton (content placeholder) vs
   Meter (static measurement) vs Stepper (discrete steps); determinate-
   when-measurable; the anti-flash rules; the button-loading boundary.
6. Accessibility — role=progressbar + aria-valuenow/min/max/valuetext
   (determinate) vs indeterminate (no valuenow, aria-busy), the live-region
   milestone/completion announcement (don't-announce-every-percent), the
   meter-vs-progressbar boundary, the label, reduce-motion-can't-remove-the-
   only-indicator, WCAG SCs.
7. Content guidelines — the label, the value/percentage text, non-%
   valuetext, completion/error messaging, don't-over-narrate.
8. Motion and transition — the indeterminate animation + the
   reduce-motion substitution, the determinate fill transition, the
   spinner rotation, completion.
9. Internationalization — RTL (linear bar fill direction flip, % format),
   the value text, locale number/byte formatting.
10. Naming — Progress / ProgressBar / ProgressIndicator / LinearProgress /
    CircularProgress; the practice's default; the Spinner/Meter
    disambiguation; aliases.
11. Implementation notes — the determinate value contract + the
    indeterminate aria-busy, the throttled live-region announcement, the
    anti-flash delay + min-display timers, reduce-motion substitution, the
    global route-change bar, headless vs opinionated.
12. Related and alternative components — typed relationships (Toast
    live-region pattern, Spinner boundary, Skeleton boundary, Meter
    boundary, Button loading, Stepper boundary).
13. Field POV evolution — recent shifts (the meter-vs-progressbar
    clarification, the don't-announce-every-percent live-region settling,
    the anti-flash delay/min-display discipline, reduce-motion handling).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a progress indicator is —
explain the determinate-vs-indeterminate fork (and the role=progressbar
value contract / the don't-fake-determinate rule), the live-region
milestone announcement (don't-announce-every-percent, reusing Toast's
pattern), the progress-vs-spinner-vs-skeleton three-loading-patterns
decision, the meter-vs-progressbar semantic boundary, the anti-flash
delay/min-display rules, and the reduce-motion-can't-remove-the-only-
indicator problem that field leaders still diverge on.

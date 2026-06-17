You are researching the Empty State component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what an empty
state is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Empty State is the FIFTH and FINAL Feedback brief — and it CLOSES the
Feedback category. It is the rendered content of a data container when
there is nothing to show. It STANDS ON three component substrates and one
category substrate, and is COMPOSED BY the Data components:
- THE ACTION (CTA) inherits BUTTON (components/button.md) — the
  create/retry/clear-filters affordance. Don't re-derive Button.
- THE VISUAL inherits ICON (components/icon.md) for the icon case (the
  illustration is its own asset); INLINE/SECONDARY LINKS inherit LINK
  (components/link.md).
- THE DYNAMIC "NO RESULTS" ANNOUNCEMENT lightly reuses the LIVE-REGION
  PATTERN from TOAST (components/toast.md): when a search/filter returns
  nothing, the result count ("No results found") is announced via a
  status live region — the empty-state CONTENT itself is not a live
  region, only the dynamic announcement is. Don't re-derive the pattern.
It is COMPOSED BY (forward-references): Table / List / Tree (the data
hosts whose zero-state IS the empty state — not yet briefed), and it
boundaries with Skeleton / Progress (the LOADING terminal state — not yet
briefed / see components/progress.md) and Banner / Inline Message (the
ERROR terminal state — see components/banner.md, components/inline-message.md).

THE DEFINING EMPTY-STATE-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE GENRE TAXONOMY (the headline — the WHY drives the content + action):
  first-use / onboarding (no data ever created — the most valuable, the
  user's first impression of a feature), no-results (a search/filter
  returned nothing), user-cleared / all-done (inbox-zero, task complete),
  error / failure (couldn't load — the empty-vs-error boundary), and
  no-permission / no-access. Resolve the taxonomy and how each genre maps
  to a different heading, body, and action.
- THE EMPTY-vs-ERROR-vs-LOADING TERMINAL-STATES BOUNDARY (the structural
  framing): a data container has a lifecycle — loading -> {content |
  empty | error | no-permission}. Empty State is one terminal state.
  Resolve the boundary with the LOADING state (Skeleton/Progress — the
  in-between), the ERROR state (a failed load — when is it an
  error-flavored empty state vs a Banner/Inline error), and that an empty
  result is EXPECTED while an error is a FAILURE.
- THE ACTION MAPPING (genre -> CTA): first-use -> a primary create CTA;
  no-results -> clear-filters / adjust-search / broaden; error -> retry;
  all-done -> often NO action (or a gentle next step); no-permission ->
  request-access / contact-admin. Resolve the mapping and the
  primary-vs-secondary action discipline.
- THE ILLUSTRATION QUESTION — illustrated vs icon vs text-only; the
  illustration as DECORATIVE (aria-hidden, not announced); the
  over-illustration / bespoke-illustration-cost trap; when an icon or no
  visual is better; the illustration-consistency-across-states concern.
- THE DYNAMIC NO-RESULTS ANNOUNCEMENT + FOCUS — when a search/filter
  empties the results, announce the count ("No results found") via a
  status live region (reusing Toast's pattern lightly) and resolve the
  focus question (does focus move to the empty state / stay in the search
  field); the empty-state heading in the document outline.
- CONTENT + TONE BY GENRE — the heading (positive/neutral, not "Error" /
  "Nothing here"), the body (explain WHY it's empty + WHAT to do), the
  action label; the tone shift (encouraging for first-use, helpful for
  no-results, reassuring for all-done, no-blame for error).
- PLACEMENT + SIZING — full-page vs in-card vs in-table-row vs in-section;
  compact vs full; the "never leave a blank container" rule (absence
  without guidance is a dead end).

Field-leader systems to survey (web): Shopify Polaris (EmptyState — the
canonical illustration + heading + action), Adobe Spectrum (Illustrated
Message — the unified empty/error/no-results name), GitHub Primer
(Blankslate), Atlassian Design System (EmptyState), Ant Design (Empty —
image/description, the default vs simple image), Chakra UI (EmptyState —
the newer Root/Indicator/Title/Description/Content parts), IBM Carbon (the
empty-state pattern for Data Table / the "no data" pattern), Google
Material 3 (empty-state guidance), Base Web (Uber). WAI-ARIA APG (no
formal empty-state pattern — content + a status live region for the
dynamic no-results case). Mobile reference where relevant. Cite each with
a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Button CTA, the Icon visual, the
Link links, and the Toast live-region pattern (no-results); flag
unverified claims under notes.unverified).

1. Framing — what it is (the zero-state content of a data container) and
   what it isn't (a loading Skeleton/Progress / a Banner-or-Inline error);
   the genre taxonomy + the terminal-states boundary up front; why systems
   disagree.
2. Anatomy and parts — the illustration/icon, the heading, the body/
   description, the primary action, the secondary action; the container.
3. Properties / API — the parts (illustration/icon, heading, description,
   action slots), the genre/variant, compact/full, the composable-parts vs
   monolithic API.
4. States and variants — by genre (first-use / no-results / all-done /
   error / no-permission); illustrated / icon / text-only; full-page /
   in-card / in-row; compact / full.
5. Usage guidance — Empty State (expected absence, with guidance) vs
   Loading (Skeleton/Progress) vs Error (Banner/Inline); the genre->action
   mapping; the never-leave-a-blank-container rule; the first-use-as-
   onboarding opportunity.
6. Accessibility — the empty-state content is not a live region (it's
   rendered content), the dynamic no-results status announcement + focus,
   the heading in the outline, the decorative illustration (aria-hidden),
   the action in the tab order, WCAG SCs.
7. Content guidelines — heading (positive/neutral), body (why + what to
   do), action label, tone by genre, no-blame, the first-use copy.
8. Motion and transition — minimal (appearance when content is absent),
   reduce-motion.
9. Internationalization — RTL (layout mirror), text expansion (the
   heading/body wrap), the illustration neutrality.
10. Naming — Empty State / EmptyState / Blankslate / IllustratedMessage /
    Empty; the practice's default; aliases.
11. Implementation notes — the data-container terminal-state machine
    (loading/content/empty/error), the no-results status announcement +
    focus, the decorative illustration, the composable parts, headless vs
    opinionated.
12. Related and alternative components — typed relationships (Button CTA,
    Icon/illustration, Link, the Toast live-region pattern, Skeleton/
    Progress loading boundary, Banner/Inline Message error boundary, the
    Table/List/Tree hosts that compose it).
13. Field POV evolution — recent shifts (the genre taxonomy maturing,
    empty-state-as-onboarding, the unified IllustratedMessage approach,
    the no-results-announcement settling, illustration restraint).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what an empty state is — explain
the genre taxonomy (first-use / no-results / all-done / error /
no-permission) and how it drives content + action, the empty-vs-error-vs-
loading terminal-states boundary, the genre->action mapping, the
illustration question (decorative/aria-hidden, illustrated vs icon vs
text, over-illustration cost), the dynamic no-results status announcement
+ focus, and the content/tone-by-genre + never-leave-a-blank-container
rules that field leaders still diverge on.

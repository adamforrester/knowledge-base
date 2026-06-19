You are advising a senior design systems practitioner at a digital agency
who maintains a personal knowledge base of design-systems field-truth. The
knowledge base has a ~45-component catalogue (each a field-truth brief: how
the leading systems handle a component, where they converge/diverge, the
practice's opinionated default) and is opening a PATTERNS layer above it.

This is the SECOND pattern brief: **View-state orchestration**. A pattern is
not a component — it is an opinionated, goal-contextual COMPOSITION of
components that owns the orchestration no single component can. The boundary
the practice draws (per `patterns/_schema.md`): cross-cutting rules a single
component obeys (the bare disabled rule; the bare loading-spinner rule;
theming) are **Foundations**, not patterns; cross-region *orchestration*
(coordinating empty / loading / error across a view, deciding when the
Table is replaced with a centred message vs. when it stays and renders
row-skeletons, what gets announced to AT) is a `composition` pattern. This
brief is the worked example that validates that distinction. Tier:
`composition`. Goal facet: `recover-from-error`.

Do NOT re-derive Empty State, Spinner, Skeleton, Banner, Toast, or Inline
Message — assume those are briefed in `components/`. Document the DELTA the
view-level orchestration adds: the cross-component coordination, the
state-taxonomy decisions, and the layout-vs-replacement rules. This is
field-truth synthesis, not a tutorial. Assume the reader has shipped multiple
design systems. Explain the non-obvious — where leading systems genuinely
disagree, and what the defensible default is.

=== WHAT TO SURVEY (the field) ===

Resolve how these sources actually handle empty/loading/error orchestration
at view (not component) scale, and where they diverge. Cite each with a
version date and note the verification path:
- Design systems: IBM Carbon (Empty States, Loading, Error states; the
  inline-loading vs skeleton split), Shopify Polaris (Empty State + Skeleton
  Page + Loading), Material Design 3 (Loading indicators, the
  progress-vs-skeleton stance), Atlassian (Empty state + Loading state +
  Error state + the page-shells), Microsoft Fluent (Empty/Error/Loading
  patterns), Adobe Spectrum (Illustrated message + Progress circle), GOV.UK
  Design System (Error pages, the recovery voice; less skeleton-heavy by
  design), Atlassian Forge / Salesforce Lightning / Cloudscape, Ant Design
  (Empty / Skeleton / Result), Mantine, Chakra UI.
- Field literature: Brad Frost on skeleton screens; the Bill Chung 2020 NN/g
  treatment of empty states; Page Laubheimer / NN/g on skeleton vs spinner;
  Luke Wroblewski on optimistic UI; the Polaris "skeleton first" stance.
- The Daniel Eden / Facebook 2013 skeleton-screens lineage and the Luke
  Wroblewski "let it load" critique that walked some of it back.
- Standards: WCAG 2.2 (4.1.3 Status Messages, the polite vs assertive
  live-region contract), WAI-ARIA `aria-busy` and `aria-live`, the React
  Suspense / streaming-SSR rendering model that informs current orchestration
  defaults.

=== WHAT TO RESOLVE (the decision rules are the deliverable) ===

A pattern earns its keep in its DECISION RULES — the contested forks, given
as frameworks not winners, and made machine-resolvable (`IF condition → USE
resolution`) wherever a rule genuinely has a threshold. Resolve at least:

1. **Skeleton vs spinner vs optimistic vs nothing.** The most-litigated
   loading decision. The four real options at view scale and when each is
   right — duration thresholds (perceived <300ms / 300ms–1s / 1s+ / >10s),
   predictability of layout, scope of region, navigation-shape (in-page
   refresh vs route change vs sub-region update), and whether the result is
   reasonably guessable (optimistic).
2. **All-at-once vs staggered loading** of multiple regions on a page. When
   to render every skeleton in parallel; when to stream regions in priority
   order (the streaming-SSR / Suspense-boundary pattern); how to avoid the
   layout-thrash problem of multiple regions popping in independently.
3. **The empty-state taxonomy at view scale.** First-use / zero-data;
   no-results (after a query); no-permission; filtered-out; system-empty
   (everything was deleted). The fork: do these share a single component
   surface and differ only in copy + action, or do they call for different
   visual treatments? When is the empty *itself* an onboarding moment
   (boundary to the onboarding pattern)?
4. **The error-state taxonomy at region scale.** Recoverable (retry) /
   non-recoverable (the data is gone) / partial (some loaded, some failed) /
   network (offline / connectivity) / permission (auth / 403) / not-found
   (404 at region rather than page scale). When inline-banner-in-region vs
   full-region replacement vs page-level error vs toast for the transient
   blip — and the boundary against full-page error pages (which are their
   own pattern).
5. **Replacing the underlying layout vs preserving it.** The choice that
   most distinguishes a pattern from a component: when the Table stays and
   renders row-shaped skeletons (preserve scaffold) vs when the Table is
   *replaced* with a centred Empty State / Error message (collapse to the
   message). Decision axes: is the layout itself meaningful when there's no
   data; is the skeleton informative or merely decorative; the perceived-vs-
   actual-information cost of preserving the chrome.
6. **State-message-in-region vs toast vs banner** for transient or recoverable
   issues. The boundary against the sibling **Notification orchestration**
   pattern — what gets routed to a toast/banner system vs what stays
   in-region. The "where does the user need their attention" axis.
7. **The live-region budget at view scale.** WCAG 4.1.3 / 5.1.3 status
   messages; `aria-busy` on the region; the polite-vs-assertive split;
   how many things can announce per page-load without becoming a barrier
   for AT users. The single most-skipped accessibility consideration in
   loading/error orchestration.
8. **The transition contract.** When a region moves between states
   (loading → empty; loading → loaded; loaded → error), what should
   *not* flicker, what should preserve scroll position, what counts as a
   "real" state change vs noise. The reduce-motion contract for any
   animation between states. The 200–300ms minimum-display threshold for
   transient loading (avoid the flash-of-loading-then-content thrash).
9. **Optimistic UI's failure mode.** When optimistic updates are appropriate
   at view scale (vs strictly per-component); how to roll back on failure;
   the rollback's relationship to the error orchestration; when *not* to
   ship optimism (destructive, financial, or asynchronous-by-design
   operations).
10. **The skeleton's faithfulness contract.** When a skeleton must match
    the loaded layout exactly (same heights, same column count) vs. when
    a generic skeleton is acceptable; the cost of layout-shift-on-load;
    Lighthouse CLS implications; the "skeleton drift" anti-pattern where
    designers ship a skeleton that no longer matches the component's
    current layout.

=== THE BOUNDARIES TO HOLD ===

State explicitly, in a Related section:
- **View-state orchestration (pattern) vs Empty State / Spinner / Skeleton /
  Banner / Toast / Inline Message (components)** — what stays in each
  component's brief vs what this pattern owns. The component owns its own
  visuals, props, states, a11y; the pattern owns the *coordination across*
  components and the *taxonomy of when each is right*.
- **View-state orchestration vs Notification orchestration** — both are
  composition patterns; the notification pattern owns Toast/Banner/Inline-
  message routing system-wide and the do-not-disturb / batching / live-
  region budget. View-state orchestration owns *one region's* state
  coordination. The boundary: who triggered the state? Foreground user
  action that affects *this* view → view-state. Background event /
  cross-cutting system message → notification.
- **View-state orchestration vs Error pages (pattern)** — the layout-and-
  shell error-page pattern owns full-page 404/500/403/offline states; this
  pattern owns *region-scale* errors that don't replace the page.
- **View-state orchestration vs the bare disabled / loading state rules
  (Foundations)** — the foundations-exile distinction the schema codifies.
  The bare "a button shows a spinner while it's pending" is a component
  rule a Button obeys; this pattern is the *region's* coordination of
  state, which no component owns. State this distinction explicitly — it
  is the discriminating principle the schema rests on, and this brief is
  the worked example.
- **View-state orchestration vs Onboarding (pattern)** — when the empty
  state *is* the onboarding moment. The boundary: a one-frame empty state
  with one CTA is view-state; a multi-step product tour is the onboarding
  pattern. The threshold is the journey's length, not its trigger.

=== OUTPUT — follow this pattern-brief spine ===

Structured markdown. ALWAYS sections appear; SCALES appear when they carry
weight. Order = reading order.
1. **Frontmatter** — YAML: type: pattern-brief, title, description, tags,
   tier: composition, goal: recover-from-error, status, timestamp.
2. **`# View-state orchestration` H1 + a one-paragraph blockquote** framing
   the problem and the boundary it holds (especially the foundations-exile
   distinction this pattern's existence validates).
3. **Problem & context** — the recurring problem; when it applies / doesn't;
   why systems diverge; the foundations-exile principle this brief tests.
4. **Composition** — the components this assembles as typed references
   (Empty State, Spinner, Skeleton, Banner, Toast, Inline Message, plus
   the layout primitive — Table, List, Card, Grid, etc. — the orchestration
   wraps); how they fit; the DELTA the orchestration adds. Don't re-derive
   them.
5. **Decision rules** — the heart. The forks above, as machine-resolvable
   `IF → USE` rules where possible, prose for the genuinely-it-depends axes.
6. **Flow & states** (SCALES — yes here) — the region's lifecycle as a
   state machine: pristine → loading → loaded | empty | error; the
   transitions; what doesn't flicker; the optimistic + rollback path.
7. **Layout & structure** (SCALES — light here; the layout is the
   underlying component's, this pattern is *about* whether to preserve or
   replace it).
8. **Accessibility orchestration** — the cross-component a11y the SYSTEM
   owns: the `aria-busy` on the region; the polite-vs-assertive live-region
   budget at view scale; the `role="status"` for empty/error messages;
   the focus-management contract on state transitions (when to move focus,
   when not to); the AT announcement contract for state changes.
9. **Content & copy** (SCALES — yes for empty / error; the per-state copy
   conventions: the empty state's voice, the error's actionability, the
   loading message's optionality). Reference 04 §Content as a system layer
   for the system-level voice constraint.
10. **Variants & responsive** (SCALES — light; mostly the layout-vs-
    replacement choice across breakpoints).
11. **Anti-patterns** — the recurring traps (the flash-of-loading-then-
    content; skeleton-drift where the skeleton no longer matches the
    component; spinner-by-default-everywhere; empty-states-as-error;
    polite-everything-for-AT; replacing the layout when the layout was
    informative; preserving the layout when the layout was decorative;
    optimistic-UI-on-destructive-actions; the same Empty State component
    used for first-use AND no-results without copy differentiation).
12. **Related patterns & components** — the typed relationships and the
    five boundaries above. The foundations-exile distinction stated
    explicitly.
13. **Field POV evolution** (SCALES) — how the field's answer has shifted
    (the rise of skeletons via Facebook 2013; the partial walk-back via
    Luke W; the React Suspense / streaming-SSR contract that's reshaping
    "all-at-once vs staggered"; the optimistic-UI lineage from React Query
    / TanStack / Apollo).
14. **Reference instantiations** (SCALES — yes here; this is example-driven
    territory): Carbon Empty States, Polaris Skeleton Page, Atlassian Empty
    state + Loading state, Material 3 progress indicators, Spectrum
    Illustrated message, Cloudscape and Ant Design's Empty/Skeleton/Result.
15. **Sources cited** — with version dates; flag any claim lacking a solid
    source as unverified rather than inventing a citation.
16. **Agent-consumable schema** — a fenced YAML block: identity (id, name,
    aliases, tier, goal, status), problem, composition (requires: [typed
    component ids]), decision_rules (as `{ if, use }` where resolvable),
    flow, accessibility_orchestration, content, anti_patterns,
    reference_instantiations, relations (composes / relates-to / boundary —
    state the foundations-exile distinction here too), notes (contested /
    unverified / secondary-tier).

Synthesize; give frameworks where context decides, defaults where the field
has genuinely converged. Be opinionated and declarative — the practice has
a POV. Flag contested claims and anything you can't source. Date current-
state platform claims.

This is the second pattern brief and the worked example for the foundations-
exile distinction. The schema explicitly notes that View-state orchestration
must "validate the orchestration-as-`composition` call." If, in writing this
brief, you find that the foundations-exile distinction *doesn't* hold for
this material — that the empty/loading/error rules really are foundations
guidance and there's no orchestration-pattern-shaped material above them —
flag that as a finding rather than synthesising a pattern that isn't there.
The schema will refine in response. (This is the same exercise-the-spine
discipline the schema applies to Forms-as-a-system as the first pattern.)

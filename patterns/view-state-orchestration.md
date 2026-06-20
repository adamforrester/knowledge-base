---
okf_version: "0.1"
type: pattern-brief
title: View-state orchestration
description: Coordinating empty / loading / error states across a region — the duration-threshold taxonomy of loading affordances (skeleton vs spinner vs optimistic vs nothing at 300ms / 1s / 10s), the five-category empty-state taxonomy, the four-axis error-state taxonomy at region scale, the layout-preserve-vs-replace threshold, the live-region budget for AT, the optimistic + rollback contract with the destructive/financial/async-by-design carve-out, and the skeleton-faithfulness contract. The components own visuals; this pattern owns the orchestration above them — the worked example that validates the schema's foundations-exile distinction.
tags: [patterns, view-state, loading, empty, error, accessibility, composition]
tier: composition
goal: recover-from-error
status: draft
timestamp: 2026-06-18
---

# View-state orchestration

> A region — a Table, a List, a Card grid, a dashboard panel — has data, or it doesn't, or it's loading, or it's broken. Each of those is its own component (Skeleton, Spinner, Empty State, Banner) with its own props and a11y. None of those components knows whether to *replace the underlying layout or preserve it*, when to render in parallel vs streaming, what to announce to AT, or which empty (first-use, no-results, no-permission, filtered-out, system-empty) the user is actually in. Those are coordination decisions, and they live above any single component. This brief owns that coordination and is, by design, the worked example that distinguishes a `composition` pattern from foundations guidance — the validating run for the schema's foundations-exile call.

---

## 1. Problem & context

Every product surface that loads data crosses the same four-state matrix — pristine, loading, populated, terminal (empty / error) — and the field most visibly disagrees on which surface to use, when to use it, and whether to preserve the surrounding layout or collapse to a centred message. The component briefs cover *what* a Skeleton looks like or *what* an Empty State component takes as props; this pattern covers the orchestration *above* them: the decision rules that resolve the contested forks, the cross-component a11y contract, the taxonomy of states, and the layout-preserve-vs-replace threshold.

The pattern applies anywhere a region renders data that may not be there yet, may not be there ever, or may have failed to arrive — Tables, Lists, Card grids, dashboards, search results, settings panels, profile views, content galleries. It does **not** apply to single-shot UI that has no async data path (a static marketing block); to global notification routing (that's the sibling Notification orchestration pattern); or to full-page error pages (that's the Error pages layout-and-shell pattern).

Systems diverge because they optimise for different perceived-performance regimes. **Polaris and Carbon** lean skeleton-first across the catalogue (the Facebook 2013 lineage; assume content layout is informative; preserve the chrome). **GOV.UK** stays minimal — small, polite spinners on transitional states, full-page error states for genuine failures, and a deliberate rejection of HTML5 browser validation in favour of server-driven Error Summaries (the lowest-trust, AT-critical context; preserve cognitive load over visual continuity). **Material 3** treats progress indicators as the loading default and skeletons as one option among several. **Atlassian and Cloudscape** distinguish region-loading from page-loading explicitly. None of those are wrong; the divergence *is* the decision space.

**The foundations-exile distinction this brief validates.** The schema (`patterns/_schema.md`) draws a sharp line: cross-cutting rules a single component obeys (the bare disabled rule; the bare loading-spinner rule; theming) are Foundations, not patterns. Cross-region *orchestration* — coordinating empty/loading/error across a view, deciding when the Table is replaced with a centred Empty State vs. when it stays and renders row-skeletons — is a `composition` pattern. This brief is the worked example for that distinction. If, on writing it, the material collapsed to "the Skeleton component has these props" or "spinners use ARIA like this," the foundations-exile call would be wrong. It doesn't collapse. The orchestration genuinely owns decisions no single component can: the five-category empty taxonomy, the layout-vs-replacement choice, the live-region budget across simultaneously-loading regions, the optimistic-UI rollback path. That is what makes it a pattern.

## 2. Composition

View-state orchestration assembles briefed components and adds the cross-component coordination — it re-derives none of them.

- **Empty State** (`see empty-state`) — the shipped surface for zero-data conditions. Already briefed: visual treatment, the illustration-vs-icon-vs-text axes, the action affordance, the genre taxonomy. The pattern's delta: *which* empty (per §3.3's five categories), the per-category copy + action contract, when the region collapses to it vs. preserves the underlying layout.
- **Spinner** (`see spinner`) — circular indeterminate progress. Already briefed: sizes, the indeterminate-vs-determinate question, the `aria-label` contract. The pattern's delta: when a spinner is appropriate at view scale (vs. skeleton; vs. optimistic; vs. nothing) and the duration thresholds.
- **Skeleton** (`see skeleton`) — content-shaped placeholders. Already briefed: the shape primitives, the shimmer-vs-pulse animation, the reduced-motion contract. The pattern's delta: when to skeleton, what to skeleton, the faithfulness contract (§3.10), the all-at-once-vs-staggered choice across multiple regions.
- **Banner** (`see banner`) — region-scoped persistent message. The pattern's delta: when an in-region banner is the right surface for a recoverable error (vs. replacing the region, vs. routing to a toast).
- **Toast** (`see toast`) — transient, dismissed automatically. The pattern's delta: the boundary against in-region state messaging — what a toast carries vs. what stays in-region.
- **Inline Message** (`see inline-message`) — small per-control message, typically per-field. The pattern's delta: when an inline message is the right surface for a partial-failure within a region.
- **The underlying layout component** — Table (`see table`), List (`see list`), Card grid (`see card`), Grid (`see grid`), Dashboard panel. These are the surfaces the pattern coordinates state *for*. Their own a11y, structure, and props are inherited; the pattern decides whether they stay or are replaced.

**The orchestrator's responsibility, contrasted with the component's.** Each row of this table holds the foundations-exile line: the component column is what *cannot* be a pattern (it has no cross-region awareness); the orchestrator column is what *cannot* be a component (it requires it).

| Layer | Component owns | Orchestrator owns |
|---|---|---|
| **Loading affordance** | The SVG spinner; the skeleton's pulse animation; local color tokens; the `aria-label` contract. | Whether the delay warrants a spinner, a skeleton, optimistic UI, or nothing; the minimum-display threshold preventing flicker. |
| **Empty surface** | The illustration, the heading + body slot, the CTA button slot; the genre primitives. | Which of the five empty categories applies; the per-category copy + action contract; layout-preserve-vs-replace at view scale. |
| **Inline error** | The icon + border + text styling; the dismiss affordance. | Mapping the network/validation failure to the right region; whether the layout collapses or persists. |
| **Layout primitive** | Columns, rows, grid gaps, the Table's headers and pagination chrome. | Whether the scaffold is preserved during refresh or unmounted and replaced. |

**The delta this pattern adds**: the five-category empty taxonomy at view scale, the four-axis error taxonomy at region scale, the layout-vs-replacement threshold, the all-at-once-vs-staggered loading choice, the live-region budget across simultaneously-loading regions, the transition contract between states (what should not flicker), the optimistic-UI + rollback path with its destructive/financial/async-by-design carve-out, the skeleton-faithfulness governance rule. Everything below is that delta.

## 3. Decision rules

The heart. Forks given as machine-resolvable rules where a real threshold exists, prose where it genuinely depends.

### 3.1 Loading affordance — skeleton vs spinner vs optimistic vs nothing

The most-litigated loading decision at view scale. The duration bands below are **300ms / 1s / 10s** — the field-truth thresholds attested by NN/g (Page Laubheimer, Samhita Tankala 2020/2023) and the broader UX research lineage. Skeleton-vs-spinner crossover sits at ~1s, not the larger band sometimes cited.

| `IF` | `USE` | Rationale |
|---|---|---|
| Anticipated fetch < ~300ms (perceived as instantaneous) | **Nothing** | Rendering any affordance for sub-300ms loads produces a flash of loading-then-content that perversely makes the system feel slower. |
| Action is user-driven, predictable, and non-destructive (e.g., favouriting, toggling a status, adding a row) | **Optimistic UI** (per §3.9) | Eliminates the friction of waiting; reconcile in the background; roll back on failure with a banner. |
| Anticipated fetch ~300ms–1s OR layout is genuinely unpredictable | **Spinner / progress indicator** | Spinners signal "the system is working" without making a layout claim. The right default when skeleton would mislead. |
| Anticipated fetch ~1s–10s, region is substantial, layout is predictable | **Skeleton screen** | Stabilises the layout; reduces perceived wait time by communicating structural progress; the lineage runs Facebook/Eden 2013 → Polaris/Carbon → modern Suspense-driven defaults. |
| Anticipated fetch > 10s or involves heavy file/data transactions | **Determinate progress bar with explanatory copy** | Indeterminate affordances induce abandonment past ~10s. Percent-done or time-remaining is mandatory; the user must be able to navigate away without losing state. |

Hard rules across the band:

- **Never combine spinner and skeleton in the same region.** Mid-skeleton spinners are noise; pick one loading affordance per region.
- **Never skeleton single-line content.** A one-sentence label or a small badge costs more in affordance than the load is worth.
- **The minimum-display threshold is ~500ms.** If a loading indicator renders at all, it stays for at least 500ms — even if data resolves earlier — to avoid the flash-of-loading-then-content thrash that paradoxically degrades perceived performance. (Source: NN/g; threshold figure widely cited; see `notes.unverified` on exact attribution.)

### 3.2 All-at-once vs staggered loading

A page typically has multiple async regions. The Suspense Contract (React 18, 2022) reshaped the field default from "every region loads imperatively" to declarative boundary management.

| `IF` | `USE` |
|---|---|
| All regions arrive on roughly the same timeline (within ~500ms of each other) AND share a data context | **All-at-once skeletons.** Render every region's skeleton in parallel; the page settles to its loaded state in a single visual transition. Wrap regions in a single unified orchestration boundary. |
| Regions have meaningfully different timelines AND priority differs (header is critical; recommendations are nice-to-have) | **Staggered / streaming.** Render each region's skeleton; resolve as data arrives; prioritise the user's primary task. The React Suspense / streaming-SSR boundary is the modern default. |
| Deeply nested child components require independent fetches | **Consolidate boundaries upward.** Position Suspense boundaries at natural loading units (routes, cards) rather than wrapping leaf components individually — over-nested Suspense produces a chaotic "popcorn" load. |

The discipline: pick all-at-once *or* staggered *deliberately*; never let the rendering shape be an accident of which API resolved first. The skeleton is the layout-stability claim — without it, the page layout shifts visibly multiple times per load (the layout-thrash anti-pattern).

### 3.3 The empty-state taxonomy

Not a single empty — a family of five. Shipping a single Empty State surface that doesn't differentiate copy across these categories is the most-common anti-pattern in view-state work.

- **First-use / blank slate.** The user has the right to see content here, but has not created any yet. **Empty State + illustration + primary CTA + educational copy.** Voice: encouraging without being saccharine ("Add your first project to get started"). The empty IS the onboarding moment for this region. Boundary against the Onboarding pattern: a one-frame empty with one CTA is view-state; a multi-step product tour is Onboarding.
- **No-results / filtered-out.** A query was made and returned nothing, or filters reduced everything away. **Empty State, no illustration, secondary "Clear filters" CTA.** Cloudscape (AWS) explicitly *mandates* this shape — a secondary-styled "Clear filter" button is the prescribed action; an illustration would be jarring. Voice: clarifying ("0 of 247 results match. Clear filters?"). When the query came from a *search*, the no-results content (did-you-mean, broaden, alternatives) is owned by the Search orchestration pattern (see patterns/search-orchestration); this taxonomy supplies the empty-state *shape*, search supplies the recovery *copy*.
- **No-permission.** The user is in the right place but lacks access. **Empty State + factual permission message + path to permission.** Voice: factual without blame ("Only admins can see this. Contact your team owner."). Action buttons direct to access requests, not creation.
- **System-empty / inbox-zero / cleared.** The user *had* data here and resolved/deleted it all (inbox cleared, all tasks done, archive emptied). **Empty State + celebratory or respectful framing — no immediate primary action required.** Voice: respectful (the user *had* data; this is success, not absence). Some systems (Atlassian) ship this as a deliberate "you're done" moment.
- **System-pending / not-yet-configured.** The platform is set up but the data pipeline hasn't run yet (a fresh integration; a queued job that hasn't completed). **Empty State + status copy + link to the configuration / queue surface.** This is the rarest of the five and where field practice diverges most.

**The Atlassian "Blank Slate" vs "Empty State" distinction is a citable variant.** Atlassian Design System splits the family further: a *Blank Slate* is specifically the first-use discovery moment (illustration + onboarding action), and an *Empty State* covers the rest of the family (no-permission, cleared, etc.). The substantive content is the same; the naming is sharper. The practice's default uses the five-category taxonomy above; engagements where the client is on Atlassian's vocabulary should adopt their split inline.

**Where the empty *itself* is the onboarding moment**, expand to multi-step Onboarding only when the journey requires more than one frame. Single-frame onboarding-as-empty-state stays in this pattern.

### 3.4 The error-state taxonomy at region scale

Error orchestration must match the scale and recoverability of the failure. Applying a full-page error state for a localized component failure destroys the user's surrounding context; using a subtle toast for a fatal data fetch leaves the main viewport in a perpetually broken state. Four axes, each with sub-cases.

| Severity | `USE` | Sub-cases / notes |
|---|---|---|
| **Transient blip** (network, transient sync) | **Toast / notification with retry** | The user keeps operating on cached data; the message is ephemeral. Routes to the Notification orchestration pattern's surface, not in-region. |
| **Section-level failure** (one region's fetch fails) | **In-region error boundary with retry** | Replace the failed widget with an inline error message and Retry button; preserve the rest of the page so other tasks continue. **Sub-cases**: permission/403 at region scale (no retry — show permission path); not-found/404 at region scale (show alternative path: search, list); partial-failure (render what loaded; inline-message for the failed bits). |
| **Form validation failure** | **Inline field errors + Error Summary** | The Forms-as-a-system pattern owns this in detail; view-state defers to it. Field highlighted; summary at top of form linked to fields for screen-reader navigation. |
| **Total view failure** (500, complete payload failure) | **Full-page Error State** | Replace the structural layout entirely with a centralised error illustration and a safe egress (Reload, Go Home). **Boundary**: this is where view-state hands off to the **Error Pages** layout-and-shell pattern. |

The discriminating axis: **scale of disruption**. A 404 within a Table row → in-region; a 404 of the entire URL → Error Pages. A widget failure → in-region; a payload failure of the core view → full-page.

### 3.5 Replacing the underlying layout vs preserving it

The decision that most distinguishes a pattern from a component. The component cannot make this call; the pattern owns it.

| `IF` | `USE` | Examples |
|---|---|---|
| The layout itself carries information when populated (a Table's column structure tells you what data lives here; a Kanban's columns tell you the workflow stages) | **Preserve scaffold.** Render the chrome (headers, filters, pagination); fill the data area with skeleton rows / empty messaging. | Tables, datagrids, Kanban boards, billing ledgers. |
| The layout is decorative / containing (a Card grid that simply lays out items; an image gallery; a feed) | **Replace layout.** Unmount the data container; render a centred Empty State / error message in the parent region. | Card grids, image galleries, feeds, detail views. |
| Complex composition (a dashboard panel with header, chart, footer) | **Partial preserve.** Panel chrome (header, footer) stays; the content area renders the appropriate state. | Dashboard widgets, multi-section reports. |
| Mobile viewport with vertical constraint | **Lean replace.** Keeping complex filter bars visible alongside an empty state on mobile forces the recovery action below the fold; the contextual preservation argument is weaker on mobile. | A Table that preserves on desktop may replace on mobile. |

When in doubt, lean preserve for tabular and structured data; lean replace for grid and list-style content where the layout is just a container. **The minimum-height contract is mandatory either way**: the orchestration wrapper enforces the loaded state's minimum height during transition states, preventing the page footer from violently jumping when data unmounts.

### 3.6 State-message-in-region vs toast vs banner

The boundary against the sibling **Notification orchestration** pattern.

| `IF` | `USE` |
|---|---|
| User just took an action that affects this region AND the state of THIS region needs to communicate | **In-region** (banner above the region; or replace) |
| User just took an action AND the result is success/failure of an isolated operation that doesn't affect a visible region | **Toast** (Notification orchestration owns this) |
| A system event affects this region without a user trigger (a polling refresh failed; a websocket dropped) | **In-region** (subtle banner / status icon), NOT toast — a toast for every background event is noise |
| A global system state affects multiple regions (maintenance mode, network down, read-only mode) | **Global banner / system bar** (Notification orchestration). One global banner > many in-region duplicates |

The discriminating axis: **who triggered the state change, and what's the user's visual locus?** User-triggered + this-region-focus → in-region; everything else routes to the notification system.

### 3.7 The live-region budget at view scale

The single most-skipped accessibility consideration in view-state work. WCAG 4.1.3 status messages; `aria-busy`; the polite-vs-assertive split. Politeness creep is the failure mode.

- **`IF a region is loading`** → set `aria-busy="true"` on the region's container; remove on resolution. Do **not** also fire a polite live-region announcement ("Loading…") — `aria-busy` is the AT signal and `aria-live` on top of it produces auditory fatigue.
- **`IF a region resolves to empty (any of the five categories)`** → render the empty state inside a container with `role="status"` (polite). The first focus / first-tab into the region exposes the message naturally.
- **`IF a region resolves to error`** → `role="alert"` (assertive) for *non-recoverable* errors that block the user; `role="status"` (polite) for recoverable / retry-able errors. The assertive budget is small; spend it on errors that need immediate attention.
- **`IF multiple regions load on the same page`** → resolve to **at most one** assertive announcement per page-load. Multiple polite announcements are acceptable but should be sequenced by Notification orchestration's global rules.

**Politeness creep is the failure mode.** Setting everything to `role="alert"` "to make sure AT users hear it" is the most-common a11y anti-pattern in view-state work; AT users abandon assertive-noise sites within seconds. The budget is real.

### 3.8 The transition contract

When a region moves between states.

- **Minimum-display threshold of ~500ms** for any rendered loading affordance. A skeleton or spinner that would render and replace itself in under 500ms should not render at all (per §3.1).
- **Preserve scroll position** across all state transitions. The user's vertical position is part of their state; rebuilding the layout into a state should not jump them.
- **Do not flicker between near-identical states.** If `loaded → loaded-with-fresh-data` shares the same layout, do not pass through a skeleton in between.
- **Respect `prefers-reduced-motion`.** Any cross-fade or shimmer is replaced with a hard cut between states. The loading-affordance choice (skeleton/spinner/optimistic/nothing) is unaffected; only the animation between states changes.
- **M3's pulse direction.** Material Design 3 specifies skeleton pulse animations move from top-left to bottom-right at 1.5–2s per cycle, ease-in-out timing. The convention is widely adopted; deviations should be deliberate.
- **Optimistic transitions** (§3.9) need a rollback that does not feel punitive. A soft cross-fade to the pre-action state with a banner naming the failure is the convergent pattern.

### 3.9 Optimistic UI's failure mode

Optimistic updates instantly resolve the user's action in the UI while handling the request asynchronously. Powerful for perceived performance; requires a strict rollback contract.

| `IF` | `USE` |
|---|---|
| User action AND predictable result AND low failure rate AND non-destructive | **Optimistic UI** with rollback path |
| Destructive action (delete, archive) | **Never optimistic.** Confirm explicitly; await server response. Rollback of a "delete" is too cognitively jarring (the destroyed data "magically reappears"). |
| Financial action (charge, transfer, refund) | **Never optimistic.** The error case is too consequential to roll back gracefully; the trust cost is permanent. |
| Async-by-design (moderation queue, render job, batch export) | **Never optimistic.** The user's mental model needs to match the system's "this will happen later." Show a determinate progress indicator or explicit pending state. |
| Optimistic update fails | **Instant rollback + contextual banner/toast** naming the failure with a retry path. **Never silently revert** — the user thought they did something; the system needs to acknowledge it didn't take. |

### 3.10 The skeleton's faithfulness contract

A skeleton is a visual promise of future layout. Violating that promise causes Cumulative Layout Shift (CLS), disorients the user, and degrades Lighthouse metrics.

- **Match the loaded layout's heights, column counts, and major shape** — not pixel-perfect, but architecturally faithful. The skeleton's job is the layout-stability claim.
- **Skeletons drift.** The loaded component evolves (a column is added, a height changes); the skeleton doesn't update. **Skeleton drift is silent until shipped.** The discipline: every skeleton is **generated from the same layout primitive as the loaded state** (the structural-CSS approach Cloudscape and Atlassian both ship), OR is reviewed alongside every layout change. Hard-coded SVG skeletons are the trap; they always drift.
- **A generic skeleton is acceptable when the loaded layout is genuinely simple** OR the cost of a faithful skeleton is unjustified. This is rare; defaulting to generic when faithful is achievable is the anti-pattern.
- **CLS as the proxy metric.** A skeleton that is shorter than the loaded content fails its job; ship the skeleton at the loaded content's dimensions, not at a smaller placeholder size.

## 4. Flow & states

The region's lifecycle as a state machine.

**pristine** (the region exists in the DOM but has not started loading; rare — typically only for lazy-loaded regions below the fold) → **loading** (data fetch is in flight; `aria-busy="true"`; the appropriate loading affordance per §3.1) → **loaded | empty | error**:

- **loaded** — data arrived; the region renders its populated state.
- **empty** — the data set is empty (one of the five categories per §3.3); the region renders the appropriate Empty State surface.
- **error** — the fetch failed (one of the four axes per §3.4); the region renders the appropriate error surface.

Transitions:

- `loading → loaded`: cross-fade or hard-cut; skeleton dissolves to populated content.
- `loading → empty`: the skeleton is replaced by the empty state (typically a layout-replace, even if the loaded state would have preserved layout — the empty has nothing to render against).
- `loading → error`: per §3.5 preserve-vs-replace; partial-failure is in-region per §3.4.
- `loaded → loading-fresh-data` (refetch / refresh): typically *no* visible loading state; render fresh data when arrived. If a long-running refetch is in flight, optionally show a subtle indicator (top-of-region progress bar) that does not block interaction.
- `loaded → error` (the data was there, then something broke — websocket dropped, polling failed): show an in-region banner; do not replace the loaded data unless it's invalidated.
- `empty → loaded` (user added data; the empty state's CTA was used): re-fetch and render loaded; hard transition is fine because the user intended the change.
- `error → loading` (retry triggered): re-enter loading; preserve scroll position; the previous error message disappears.

**Optimistic path** (§3.9): `loaded → optimistic-loaded → reconciled (= loaded with fresh data) | rolled-back (= loaded with banner explaining failure)`. The optimistic state visually equals loaded; the difference is internal to the orchestrator.

The key invariant: state changes the user did not initiate (background polling, websocket events) get the lightest-touch transition possible (no skeleton, no flash); state changes the user initiated get explicit acknowledgment.

## 5. Layout & structure

This pattern is about whether to preserve or replace the underlying layout, not about any particular layout. The composition is regional and lives within whatever layout surface the consuming region occupies (Table, List, Card grid, dashboard panel). The pattern's structural decision is per §3.5 (preserve-vs-replace) and per §3.2 (all-at-once vs staggered loading regions); no separate spatial recipe applies.

**The minimum-height contract.** During transition states, the orchestration wrapper enforces a minimum height matching the loaded state's height (or the skeleton's dimensions, if rendering one). Without the contract, an empty Table can collapse from 800px tall to 200px tall, throwing the page footer upward and disorienting the user. The wrapper's job is to hold the vertical real estate that the loaded state will occupy.

For responsive: the preserve-vs-replace decision can vary by breakpoint. A Table that preserves layout with row-skeletons on desktop may collapse to Card-shaped skeletons on mobile (because the Table itself collapses to a Card list at mobile breakpoints); the pattern follows the loaded-layout's responsive shape.

## 6. Accessibility orchestration

The cross-component a11y the system owns (each component's own a11y is inherited):

- **`aria-busy`** — set on the region's container while loading; unset on resolution. The single most useful AT signal for "this region is in flight" and the WCAG 4.1.3 path. `aria-busy` *suppresses* internal mutation announcements; never combine with `aria-live` for the same region during loading.
- **Live-region budget** — at most one assertive announcement per page-load (per §3.7); the rest are polite or silent.
- **`role="status"` for empty / recoverable error** — polite live-region for non-blocking state messages.
- **`role="alert"` only for blocking errors** — non-recoverable failures that prevent the user from continuing. Use sparingly; politeness creep is the failure mode.
- **Focus management on transitions** — generally *do not* move focus on state transitions (loading → loaded). Forced focus shifts disorient AT users. Exceptions: when the user explicitly retried an error (move focus to the retried region's first interactive element); when a fatal full-page error boundary unmounts the user's previous focus target (move focus to the recovery heading or summary). Single-frame empty-state CTAs typically *do not* move focus; the user reaches the CTA via tab.
- **Keyboard traversal** — the region's tab order must be consistent across states. The empty state's CTA, the error state's retry button, and the loaded state's first interactive element should occupy roughly equivalent positions.
- **The skeleton's a11y** — skeletons are decorative; mark them `aria-hidden="true"` and rely on the parent region's `aria-busy` for the AT signal. Never use skeleton elements as labels or focus targets.
- **Multiple-region coordination** — when a page loads multiple regions in parallel (per §3.2), per-region `aria-busy` signals are individually announced as their state changes; the page itself does not need a global "page loading" announcement.

This is the single most-important reason view-state orchestration is briefed as a pattern: the a11y contract is cross-component (the region's `aria-busy`, the live-region budget, the focus contract) and no single component can own it. Empty State doesn't know about the Spinner; Skeleton doesn't know about the Banner. The pattern coordinates.

## 7. Content & copy

Near-ALWAYS load-bearing for empty and error states. **All view-state copy follows the system-level voice-and-tone matrix per 04 §Content as a system layer** — the matrix's error tone-context governs error voice; the matrix's empty tone-context governs empty voice. The pattern doesn't author voice; it consumes the system's voice constraint and applies it.

**Empty-state copy per category** (per §3.3):

- **First-use / blank slate**: encouraging without being saccharine. *"Add your first project to get started."* Not *"You don't have any projects (sad face)."*
- **No-results / filtered-out**: clarifying + path back. *"No results for *acne*. Try a different term, or clear filters."* Cloudscape mandates the secondary "Clear filter" CTA shape.
- **No-permission**: factual + path forward. *"Only admins can see this. Contact your team owner for access."* Not *"Forbidden."*
- **System-empty / cleared**: respectful (the user *had* data). *"Your archive is empty. Items archived in the last 30 days appear here."* Not *"No archived items."*
- **System-pending**: status + path. *"Your data is syncing. Check back in a few minutes."* Not *"No data."*

**Error-state copy** (per §3.4):

- Specific + actionable: *"Couldn't reach the server. Check your connection and retry."* Not *"Something went wrong."*
- Voice for partial failure: acknowledge what loaded, name what didn't. *"Showing 7 of 10 items. 3 items failed to load. Retry?"*
- Never blame the user. *"Your search returned no results"* → never *"You searched wrong."*
- Never expose raw machine-generated exception strings. *"Couldn't load your invoices"* — never *"SQL Connection pool timeout error 0x044."*

**Loading-state copy** (mostly: don't):

- Skeletons get no copy; they are the loading affordance.
- Spinners get an `aria-label` (`aria-label="Loading"` or `aria-label="Loading user data"`) but generally no visible label unless the load is genuinely long (>~3s).
- For long loads (>~10s): a status message ("Building your dashboard. This usually takes about 5 seconds.") — but only if the load is consistently long; transient long loads should not be over-explained.

**Cross-system copy conventions worth lifting verbatim**:

- **Cloudscape and Atlassian** explicitly mandate that empty-state and error-state headings avoid terminal punctuation — they read as structural titles, not prose. *"No distributions"*, not *"No distributions."*
- **Avoid directional language** (*"click the button below"*) — fails on assistive tech and shifts on responsive layout reflows. Reference actions by name: *"Use Clear filters to reset"*, not *"Click the button below."*
- **The body must not redundantly repeat the heading**. *"No distributions"* (heading) + *"Create a distribution to start serving your content"* (body), not *"No distributions"* + *"You don't have any distributions yet."*

## 8. Variants & responsive

The variants are mostly the layout-preserve-vs-replace choice across breakpoints (per §3.5).

- **Desktop preserve (Table with row-skeletons)** ↔ **Mobile preserve (List with card-skeletons)** — when the loaded Table collapses to a Card list at mobile breakpoints, the skeleton follows the same collapse.
- **Desktop preserve** ↔ **Mobile replace** — when the layout-information argument is weaker on mobile (Table column structure is collapsed anyway), some systems replace with a centred Empty State at mobile breakpoint. Decide deliberately.
- **Multi-column dashboard preserve** ↔ **Mobile single-column collapse** — each panel preserves or replaces independently per §3.5; the mobile collapse is the dashboard layout's, not this pattern's.

Reduced-motion: any cross-fade or shimmer is replaced with hard-cut transitions; the loading-affordance choice (skeleton/spinner/optimistic/nothing) is unaffected. Reduced-motion users still see skeletons; they just don't see the shimmer animation.

## 9. Anti-patterns

- **Flash-of-loading-then-content** — rendering a skeleton or spinner for sub-300ms (or sub-500ms with the minimum-display threshold) loads. The flicker paradoxically makes the system feel slower.
- **Skeleton drift** — the skeleton no longer matches the loaded component's layout (a column was added; a height changed; a section was rearranged). Silent until shipped; produces severe CLS on resolve.
- **Spinner-by-default-everywhere** — using the Spinner as the loading default for every region, ignoring skeleton's perceived-performance benefit for predictable layouts.
- **One Empty State surface, five categories of empty** — shipping a single Empty State component with the same copy for first-use, no-results, no-permission, system-empty, and system-pending. Each is its own copy + action contract.
- **Politeness creep** — `role="alert"` on every state message; the AT user's experience degrades to assertive noise.
- **Polite-everything-for-AT** — the inverse failure: `role="status"` on every state change; the polite live-region budget overflows; AT users can't distinguish important state changes from background noise.
- **Layout-thrash** — each region renders its content as data arrives, with no skeleton claim, so the page layout shifts visibly multiple times per load.
- **Replacing the layout when the layout was informative** — collapsing an empty Table into a centred Empty State, losing the column-structure information that told the user what data lives here.
- **Preserving the layout when the layout was decorative** — rendering Card-grid skeletons for an empty Card grid where the grid carries no information; the chrome adds noise.
- **Optimistic UI on destructive actions** — optimistic delete, optimistic charge, optimistic transfer. The error case is too consequential to roll back gracefully; the trust cost is permanent.
- **Toast everywhere** — routing every region-scoped state message to a toast; the toast surface becomes noise; the in-region location loses its information value.
- **Same Empty State without copy differentiation** — same surface for first-use AND no-results. The user's mental model needs the copy to differentiate.
- **Empty-states-as-errors** — using the cheerful first-use empty illustration for a 500 error or a 403. Violates contextual trust; appears mocking.
- **Forced focus on every transition** — moving focus on every state change disorients AT users.
- **Over-nested Suspense** — wrapping every leaf component in a Suspense boundary; produces popcorn loading, layout thrashing, and visual fatigue.
- **The skeleton-with-spinner combo** — skeletons inside skeletons or spinners on top of skeletons. Pick one loading affordance per region.
- **Aggressive auto-scroll on transition** — moving the scroll position to "show" the user the new state. The user's vertical position is part of their state; preserve it.

## 10. Related patterns & components

- **View-state orchestration (pattern) vs Empty State / Spinner / Skeleton / Banner / Toast / Inline Message (components)** — each component owns its visuals, props, states, a11y. This pattern owns the *coordination across* components and the *taxonomy of when each is right* — the empty-category-discriminator, the layout-preserve-vs-replace decision, the live-region budget, the optimistic + rollback path.
- **View-state orchestration vs Notification orchestration (pattern)** — both `composition` patterns. Notification orchestration owns Toast/Banner/Inline Message routing system-wide and the do-not-disturb / batching / global live-region budget. View-state orchestration owns *one region's* state coordination. The boundary axis: **who triggered the state, and what's the user's visual locus?** User-triggered + this-region-focus → view-state. Background event / cross-cutting system message / multi-region affecting → notification.
- **View-state orchestration vs Error pages (pattern)** — Error Pages is the layout-and-shell pattern that owns full-page 404/500/403/offline. View-state orchestration owns *region-scale* errors that don't replace the page. The boundary: scope. A 404 within a Table row → view-state; a 404 of the entire URL → Error Pages.
- **View-state orchestration vs Onboarding (pattern)** — when the empty state *is* the onboarding moment. The boundary: a one-frame empty state with one CTA is view-state. A multi-step product tour, a guided checklist, or a multi-screen first-run flow is the Onboarding pattern. Threshold: journey length, not trigger.
- **View-state orchestration vs Forms-as-a-system (pattern)** — form validation failure is form-shaped (the Forms-as-a-system pattern owns the inline-error + Error Summary + per-field `aria-invalid` contract); view-state hands off to it for any payload that's a form. The boundary: a form's payload is structured input; a view's payload is data the user reads.
- **View-state orchestration vs Bulk actions & selection (pattern)** — the selection pattern owns the multi-select-to-action bar; view-state owns what happens when the bulk operation results in an empty list (replace with system-empty), an error (in-region banner), or a partial-failure (in-region inline message per row).
- **View-state orchestration vs Search orchestration (pattern)** — the reciprocal of the no-results seam. This pattern owns the empty-state *shape* of a region (the five-category taxonomy, the no-illustration no-results form); Search orchestration (see patterns/search-orchestration) owns the search-specific recovery *content* (did-you-mean, broaden scope, suggested queries) that fills that shape when the query was a search. View-state supplies the container; search supplies the recovery.
- **View-state orchestration vs Destructive confirmation (pattern)** — the optimistic-UI overlap. Both touch optimistic execution: this pattern owns a region's optimistic + rollback contract (the visual state while a mutation is in flight or being reverted); Destructive confirmation (see patterns/destructive-confirmation) owns the *decision* to act optimistically with undo vs confirm, and the soft-delete grace-period/undo-toast model. View-state renders the optimistic state; destructive-confirmation decides whether it's an undo or a confirm.
- **View-state orchestration vs the bare disabled / loading state rules (Foundations)** — the foundations-exile distinction this brief validates. The bare *"a button shows a spinner while pending"* or *"a disabled control gets these visual treatments"* are component rules a Button/Form obeys; this pattern is the *region's* coordination of state, which no component owns. The pattern's existence is the worked example for the schema's `composition` tier.

**`composes`:** empty-state, spinner, skeleton, banner, toast, inline-message; **reads from**: table, list, card, grid (the underlying layout components).

## 11. Field POV evolution

The field's loading-affordance default has shifted across three eras.

**Era 1 (pre-2013): Spinner everywhere.** Every region got a centred Spinner (or progress bar) on load. Layout thrash on resolve was the standard cost. Luke Wroblewski's "Let it Load" critique (~2013) named the anxiety-inducing failure mode of spinner-by-default and argued against drawing visual attention to loading overhead.

**Era 2 (2013–~2021): Skeletons everywhere — with a partial walkback.** Daniel Eden's Facebook 2013 skeleton-screens lineage and Wroblewski's work on the Polar app pushed skeletons as the default for any predictable layout. Polaris's "Skeleton Page" became the canonical example. Then the partial walkback: a 2017 Viget study and subsequent NN/g research (Page Laubheimer, Samhita Tankala) revealed that poorly-implemented skeletons — static splash-screens-without-motion, skeletons applied to >10s loads, skeletons drifting from the loaded layout — actually performed *worse* than spinners in user-perception tests. The field consolidated: skeletons require motion (pulse or shimmer); they must mathematically match the loaded layout; they belong in the 1s–10s band, not above or below.

**Era 3 (2022–present): The Suspense Contract.** React 18's `<Suspense>` boundaries (2022) and the streaming-SSR rendering model fundamentally reshaped orchestration. Imperative `if (loading) return <Skeleton/>` logic was replaced by declarative boundary management; regions group into logical chunks that stream into the DOM cohesively, deferring rendering until data dependencies are met. The all-at-once-vs-staggered choice became architecturally explicit. In parallel, optimistic UI normalised: TanStack Query / React Query / Apollo all ship optimistic-update primitives; the pattern moved from "app-like novelty" to baseline expectation, necessitating the rigid rollback rules at §3.9.

The empty-state taxonomy matured similarly. Bill Chung's NN/g treatment (2020, *"Designing UX Empty States"*) named the first-use vs no-results vs system-empty distinctions; the field now generally agrees that one Empty State component with five different copy contracts is the right shape (vs. five different visual surfaces). Copy is the primary differentiator; visual treatment is shared. Atlassian's deeper Blank-Slate-vs-Empty-State naming split is the variant most engagements adopt.

## 12. Reference instantiations

Go look at:

- **Shopify Polaris** — Skeleton Page (the canonical full-region skeleton), Empty State, Loading. The skeleton-first stance at its most-articulated. **Polaris explicitly restricts its `<Spinner>` component from full-page loads** — skeleton-screens are mandated for full-page contexts to preserve layout context during heavy data fetches.
- **IBM Carbon** — Empty States, Loading patterns, the inline-loading vs skeleton split. Strong on the per-empty-category copy guidance; clear `<InlineLoading>` for form submissions vs skeletons for layout-stability.
- **Atlassian Design System** — *"Blank Slate"* (the first-use discovery moment with illustration + onboarding action) vs *"Empty State"* (the rest of the family). Strong on the region-vs-page distinction; clear preserve-vs-replace examples; the `headingLevel` slot for outline integration.
- **Material Design 3** — Loading indicators (the progress-vs-skeleton stance). Skeleton loaders specified as **top-left to bottom-right pulse, 1.5–2s per cycle, ease-in-out timing**. Less skeleton-heavy than Polaris/Carbon; useful as the contrast.
- **Adobe Spectrum** — Illustrated message (Spectrum's empty-state surface), Progress circle. Strong on the illustration-as-empty-state visual treatment.
- **Microsoft Fluent** — Empty/Error/Loading patterns. Good on the partial-failure case.
- **GOV.UK Design System** — Error pages, the recovery voice. The minimalist counter-default: small polite spinners, full-page error states, **explicit rejection of HTML5 browser validation in favour of server-driven Error Summaries** ensuring form values remain intact during the orchestration cycle. The skeleton-skeptical reference.
- **Cloudscape (AWS)** — region loading, error, empty. Strong on the multi-region staggered-loading pattern at scale; mandates a secondary *"Clear filter"* CTA on Zero-Results states; defines section/page/component error boundaries explicitly so a crashed chart doesn't take down the dashboard.
- **Ant Design** — three-part orchestration suite: `<Empty>` for data absence, `<Skeleton>` for latency, `<Result>` for heavy operational conclusions (successful submissions, fatal access-denied errors). The cleanest component-side reference for the per-state-category decision rules.

## 13. Sources cited

- IBM Carbon — Empty States, Loading, Error states (v11, 2025). *Verify current at carbondesignsystem.com.*
- Shopify Polaris — Skeleton Page, Empty State, Loading; Spinner full-page restriction (2024–25).
- Material Design 3 — Loading indicators; skeleton pulse-direction specification (2024–25).
- Atlassian Design System — Blank Slate / Empty State / Loading state / Error state (2025).
- Adobe Spectrum — Illustrated message, Progress circle (2025).
- Microsoft Fluent — Loading patterns, Empty patterns (2025).
- GOV.UK Design System — Error pages, recovery voice, HTML5-validation rejection in favour of server-driven Error Summaries (v5, 2025).
- Cloudscape (AWS) — Empty/Loading/Error patterns; "Zero Results" with mandated Clear filter CTA; per-level Error Boundaries (2025).
- Ant Design — `<Empty>` / `<Skeleton>` / `<Result>` components (2025).
- Daniel Eden — *"Skeleton Screens"* (Facebook, ~2013) — the canonical skeleton-screens lineage.
- Luke Wroblewski — *"Let it Load"* critique of spinner-by-default; Polar app skeleton-screen origin (~2013).
- Viget — 2017 study revealing static-skeleton failures vs spinners in user-perception testing.
- Bill Chung — *"Designing UX Empty States"* (NN/g, 2020). The empty-state taxonomy lineage.
- Page Laubheimer & Samhita Tankala — NN/g research validating 300ms / 1s / 10s duration thresholds and the danger of frame-only skeletons (2020, 2023).
- WCAG 2.2 — 4.1.3 Status Messages; WAI-ARIA 1.2 — `aria-busy`, `aria-live`, `role="status"`, `role="alert"`.
- React Suspense / streaming SSR (React 18, 2022; current docs 2024–25) — informs the all-at-once-vs-staggered contract and the Suspense Contract era.
- TanStack Query / React Query / Apollo — optimistic-update primitives (current docs, 2025–26).

`notes.unverified` (per the practice's `_source-text/`-backing discipline):
- The exact 500ms minimum-display threshold is widely cited; the precise NN/g article URL substantiating the figure is not single-sourceable across the field (multiple NN/g articles cite ~300ms / ~500ms / ~1s with slightly different framings; the 500ms display-minimum is a practitioner consolidation).
- Polaris's *exact* Spinner full-page restriction wording vs inferred stance from documentation reading.
- Daniel Eden's current Facebook engineering-blog URL — Facebook's blog has reorganised since the original 2013 post; the canonical historical URL is not stable.
- The Viget 2017 study's specific URL and methodology — widely cited; specific URL not currently locatable for direct linking.
- M3's pulse-direction and timing specifics — verified per current Material 3 docs at capture time; M3 ships rapid revisions, verify per project.

## 14. Agent-consumable schema

```yaml
identity:
  id: view-state-orchestration
  name: View-state orchestration
  aliases: [empty-loading-error orchestration, region state coordination, view state machine, suspense-boundaries, state-coordination]
  tier: composition
  goal: recover-from-error
  status: draft
problem: >
  Coordinate empty / loading / error states across a region (Table, List,
  Card grid, dashboard panel). The taxonomy of states, the
  skeleton-vs-spinner-vs-optimistic-vs-nothing decision at the 300ms / 1s /
  10s duration thresholds, the layout-preserve-vs-replace choice, the
  live-region budget, and the transition contract. Applies to any region
  rendering async data; does not apply to single-shot UI, global
  notification routing, or full-page error pages.
composition:
  requires: [empty-state, spinner, skeleton, banner, toast, inline-message]
  reads_from: [table, list, card, grid]
  delta: >
    The five-category empty taxonomy at view scale, the four-axis error
    taxonomy at region scale, the layout-vs-replacement threshold, the
    all-at-once-vs-staggered loading choice, the live-region budget across
    simultaneously-loading regions, the transition contract, the optimistic +
    rollback path with the destructive/financial/async-by-design carve-out,
    the skeleton-faithfulness governance rule.
decision_rules:
  loading_affordance:
    - { if: "perceived duration < ~300ms", use: "render no loading affordance" }
    - { if: "user action AND predictable AND low failure rate AND non-destructive", use: "optimistic UI with rollback path" }
    - { if: "duration ~300ms-1s OR layout unpredictable", use: "spinner centred in region" }
    - { if: "duration ~1s-10s AND layout predictable", use: "skeleton" }
    - { if: "duration > ~10s OR genuinely indeterminate", use: "determinate progress bar with explanatory copy; user can navigate away" }
    - { if: "always", use: "never combine spinner and skeleton; never skeleton single-line content; minimum-display threshold ~500ms" }
  multi_region_loading:
    - { if: "all regions resolve within ~500ms of each other AND share data context", use: "all-at-once skeletons in unified Suspense boundary" }
    - { if: "regions have different timelines AND different priority", use: "staggered / streaming-SSR boundaries" }
    - { if: "deeply nested children require independent fetches", use: "consolidate boundaries upward at route/card scope; never wrap leaf components individually" }
  empty_taxonomy:
    - { if: "user has not yet acted (first-use / blank slate)", use: "Empty State + illustration + primary CTA + educational copy" }
    - { if: "query/filter returned zero (no-results / filtered-out)", use: "Empty State, no illustration, secondary 'Clear filters' CTA (Cloudscape mandated shape)" }
    - { if: "user lacks access (no-permission)", use: "Empty State + factual permission message + path to permission" }
    - { if: "user cleared everything (system-empty / cleared / inbox-zero)", use: "Empty State + celebratory or respectful framing; no immediate action required" }
    - { if: "system not yet configured / pending data", use: "Empty State + status copy + link to configuration" }
    - { if: "always", use: "differentiate copy per category even if visual surface is shared; Atlassian splits Blank Slate (first-use) from Empty State (rest) as a citable variant" }
  error_taxonomy:
    - { if: "transient blip (network / sync)", use: "toast/notification with retry; routes to Notification orchestration" }
    - { if: "section-level fetch failure", use: "in-region error boundary with retry; preserve rest of page" }
    - { if: "permission 403 at region scale", use: "in-region: replace with permission message; no retry" }
    - { if: "not-found 404 at region scale", use: "in-region: replace with not-found message + alternative path" }
    - { if: "partial failure", use: "render what loaded, inline-message for failed bits, retry per-bit" }
    - { if: "form validation failure", use: "Forms-as-a-system pattern owns this; view-state defers" }
    - { if: "total view failure (500, payload failure)", use: "full-page Error State; hands off to Error Pages pattern" }
  preserve_vs_replace:
    - { if: "layout carries information when populated (e.g., Table column structure, Kanban columns)", use: "preserve scaffold, render row/column-shaped skeletons" }
    - { if: "layout is decorative / containing (e.g., Card grid, image gallery, feed)", use: "replace with centred empty/error message" }
    - { if: "complex composition (e.g., dashboard panel)", use: "partial preserve: chrome stays, content area renders state" }
    - { if: "mobile viewport vertical constraint", use: "lean replace; the layout-information argument is weaker on mobile" }
    - { if: "always", use: "minimum-height contract — wrapper enforces loaded-state height during transitions to prevent footer jump" }
  in_region_vs_toast_vs_global:
    - { if: "user took action affecting this region AND state matters here", use: "in-region (banner or replace)" }
    - { if: "user took action AND result is isolated success/failure", use: "toast (Notification orchestration)" }
    - { if: "background event affects this region without user trigger", use: "in-region (subtle banner / status icon), NOT toast" }
    - { if: "global system state affects multiple regions", use: "global banner / system bar (Notification orchestration)" }
  live_region_budget:
    - { if: "region loading", use: "aria-busy=true on region container; do not also fire polite live-region announcement" }
    - { if: "region resolves to empty", use: "role=status (polite)" }
    - { if: "non-recoverable error blocks user", use: "role=alert (assertive)" }
    - { if: "recoverable error", use: "role=status (polite)" }
    - { if: "always", use: "at most one assertive announcement per page-load; politeness creep is the failure mode" }
  transition_contract:
    - { if: "state would render and replace itself in <500ms", use: "render neither; wait for replacement (avoid flash)" }
    - { if: "always", use: "preserve scroll position; never flicker between near-identical states; respect prefers-reduced-motion (hard cuts only); M3 specifies skeleton pulse top-left to bottom-right at 1.5-2s ease-in-out" }
  optimistic_ui:
    - { if: "user action + predictable + low failure + non-destructive", use: "optimistic UI" }
    - { if: "destructive action (delete, archive)", use: "never optimistic; await server" }
    - { if: "financial action (charge, transfer, refund)", use: "never optimistic; await server" }
    - { if: "async-by-design (moderation queue, render job)", use: "never optimistic; explicit async messaging" }
    - { if: "optimistic update fails", use: "render pre-action state + banner naming failure + retry path; never silently revert" }
  skeleton_faithfulness:
    - { if: "skeleton being designed", use: "match heights, column counts, and major shape of loaded layout" }
    - { if: "always", use: "generate skeleton from same layout primitive as loaded state, OR review skeleton on every layout change" }
    - { if: "skeleton would be shorter than loaded content", use: "ship at loaded dimensions to prevent CLS" }
flow:
  states: [pristine, loading, loaded, empty, error]
  transitions:
    - "loading -> loaded: cross-fade or hard-cut"
    - "loading -> empty: replace with empty state (typically layout-replace)"
    - "loading -> error: per preserve-vs-replace; partial-failure stays in-region"
    - "loaded -> loading-fresh-data: typically no visible state; subtle indicator if long-running"
    - "loaded -> error: in-region banner; do not replace unless invalidated"
    - "empty -> loaded: hard transition (user intended the change)"
    - "error -> loading (retry): re-enter loading, preserve scroll"
  optimistic_path: "loaded -> optimistic-loaded -> reconciled | rolled-back-with-banner"
accessibility_orchestration:
  aria_busy: "set aria-busy=true on region container while loading; never combine with aria-live for same region during loading"
  live_regions: "role=status (polite) for empty/recoverable; role=alert (assertive) for blocking; at most one assertive per page-load"
  focus_management: "do not move focus on transitions except (a) user explicitly retried or (b) fatal error unmounts focus target; single-frame empty-state CTAs do not move focus"
  tab_order: "consistent across states; empty CTA, error retry, loaded first-interactive occupy roughly equivalent positions"
  skeleton_a11y: "aria-hidden=true; rely on parent region's aria-busy for AT signal"
  multi_region: "per-region aria-busy signals; no global page-loading announcement needed"
content:
  voice_consistency: "all view-state copy follows the system-level voice-and-tone matrix per 04 Content as a system layer; the pattern consumes voice constraint, does not author it"
  empty_per_category:
    first-use: "encouraging, not saccharine: 'Add your first project to get started.'"
    no-results: "clarifying with path back: '0 of 247 results match. Clear filters?'"
    no-permission: "factual without blame: 'Only admins can see this. Contact your team owner.'"
    system-empty: "respectful: user had data; 'Your archive is empty. Items archived in last 30 days appear here.'"
    system-pending: "status + path: 'Your data is syncing. Check back in a few minutes.'"
  error: "specific + actionable; says what failed and what to do; never blame user; partial-failure acknowledges what loaded and what didn't; never expose raw exception strings"
  loading: "skeletons get no copy; spinners get aria-label only; long loads (>10s) may get status message"
  conventions:
    - "no terminal punctuation in headings (Cloudscape, Atlassian mandate): 'No distributions' not 'No distributions.'"
    - "avoid directional language ('click the button below'): reference actions by name"
    - "body must not redundantly repeat heading text"
variants: [preserve-layout, replace-layout, partial-preserve, all-at-once-multi-region, staggered-multi-region]
anti_patterns:
  - flash-of-loading-then-content (skeleton or spinner <500ms minimum-display)
  - skeleton drift (skeleton no longer matches loaded layout, causing CLS)
  - spinner-by-default-everywhere
  - one Empty State surface with same copy for all five empty categories
  - politeness creep (role=alert on every state message)
  - polite-everything-for-AT (role=status overflow)
  - layout-thrash (regions popping in independently with no skeleton claim)
  - replacing layout when layout was informative
  - preserving layout when layout was decorative
  - optimistic UI on destructive/financial/async-by-design actions
  - toast everywhere (every region message routed to global toast)
  - empty-states-as-errors (cheerful first-use illustration for 500/403)
  - forced focus on every transition
  - over-nested Suspense (popcorn loading)
  - skeleton-with-spinner combo
  - aggressive auto-scroll on transition
reference_instantiations:
  - { system: "Shopify Polaris", look_at: "Skeleton Page; Spinner restricted from full-page loads" }
  - { system: "IBM Carbon", look_at: "Empty States, InlineLoading vs skeleton split" }
  - { system: "Atlassian Design System", look_at: "Blank Slate vs Empty State distinction; headingLevel for outline" }
  - { system: "Material Design 3", look_at: "Loading indicators; top-left-to-bottom-right pulse direction at 1.5-2s ease-in-out" }
  - { system: "Adobe Spectrum", look_at: "Illustrated message, Progress circle" }
  - { system: "Microsoft Fluent", look_at: "Empty/Error/Loading patterns (partial-failure)" }
  - { system: "GOV.UK", look_at: "Error pages, recovery voice; HTML5-validation rejection; server-driven Error Summary" }
  - { system: "Cloudscape (AWS)", look_at: "Multi-region staggered-loading at scale; mandated 'Clear filter' CTA for Zero-Results; section/page/component Error Boundaries" }
  - { system: "Ant Design", look_at: "<Empty> / <Skeleton> / <Result> three-part suite" }
relations:
  composes: [empty-state, spinner, skeleton, banner, toast, inline-message]
  reads-from: [table, list, card, grid]
  relates-to: [notification-orchestration, error-pages, onboarding, forms-as-a-system, bulk-actions-and-selection, search-orchestration, destructive-confirmation]
  boundary: >
    Components own visuals/props/states/a11y; this pattern owns coordination
    across them and the taxonomy of when each is right. Notification
    orchestration owns global toast/banner routing; this pattern owns
    one-region's state. Error Pages owns full-page errors; this pattern owns
    region-scale errors. Forms-as-a-system owns form validation orchestration;
    this pattern defers to it for forms. Foundations (the bare disabled/loading
    rules) are component-obeyed; this pattern is the region's orchestration.
    Onboarding is multi-step; one-frame empty-as-onboarding stays here.
  foundations_exile_validation: >
    This pattern is the worked example for the schema's foundations-exile
    distinction: cross-region orchestration is a `composition` pattern; bare
    state rules a component obeys are foundations. The pattern's existence
    as substantive material — the five-category empty taxonomy, the
    preserve-vs-replace threshold, the live-region budget, the optimistic +
    rollback contract — confirms the call.
notes:
  contested:
    - "skeleton-default vs spinner-default (Polaris/Carbon vs Material/GOV.UK)"
    - "exact duration thresholds (NN/g converged on 300ms/1s/10s; Wroblewski's 2013 originals slightly differ)"
    - "no-permission and not-found as empty-state vs error-state categories"
    - "all-at-once-vs-staggered default in 2026 (streaming SSR is shifting this)"
    - "Atlassian's Blank Slate vs Empty State naming (citable variant of the practice's five-category default)"
  unverified:
    - "exact 500ms minimum-display threshold attribution (NN/g cites multiple variants; figure is practitioner consolidation)"
    - "Polaris's exact Spinner full-page restriction wording vs inferred stance"
    - "Daniel Eden's current Facebook engineering-blog URL (post-reorganisation)"
    - "Viget 2017 study URL and methodology"
    - "M3's pulse-direction and timing specifics (verified at capture; M3 ships rapid revisions)"
  secondary-tier: "none — this is a pure `composition` pattern"
```

---

## Provenance

This brief synthesises a 2026-06-18 dual-agent run on view-state orchestration (`_research/_inbound/2026-06-18-pattern-view-state-orchestration/`). Both passes converged at ~94% on architectural shape — the foundations-exile validation, the four-fork shape (loading affordance / multi-region / empty / error), the layout-preserve-vs-replace decision as the discriminating call, the live-region budget with politeness creep as the named failure mode, the optimistic UI rollback contract, the skeleton-faithfulness governance, and the transition contract.

Three taxonomic divergences reconciled in synthesis:

- **Duration thresholds** — external converged on 300ms / 1s / 10s with NN/g attribution (Page Laubheimer, Samhita Tankala 2020/2023); Claude's pass had 300ms / 3s / 10s. External's bands match the field-truth and were lifted; the skeleton-spinner crossover sits at ~1s.
- **Empty-state taxonomy** — Claude landed five categories (first-use, no-results, no-permission, filtered-out, system-empty); external landed four (first-use, filtered-out, inbox-zero/cleared, system-empty/permission). Synthesis lands **five** with system-pending added as the rarest and most-contested case, and explicitly names Atlassian's *Blank Slate / Empty State* split as a citable variant. Claude's "filtered-out" merges into "no-results" (they're the same operational case under different labels).
- **Error-state taxonomy** — Claude had six categories at region scale; external had four at the broader scale (transient/section/inline-form/full-page). Synthesis adopts external's four-axis structure with permission/not-found preserved as sub-cases of section-level — the architectural cut is cleaner; the granular sub-cases are still recoverable inside the table.

Three artefacts lifted from external specifically: the **Atlassian Blank Slate / Empty State naming variant** as the deeper taxonomic cut at §3.3 + §11; the **Cloudscape "Clear filter" CTA mandate** as the canonical no-results action shape; the **M3 pulse-direction specification** (top-left to bottom-right, 1.5–2s ease-in-out). Other specific field-truth lifted: Polaris's spinner-restricted-from-full-page rule; Ant Design's three-part `<Empty>`/`<Skeleton>`/`<Result>` suite; GOV.UK's HTML5-validation rejection in favour of server-driven Error Summary; the no-terminal-punctuation copy convention from Cloudscape and Atlassian; the Viget 2017 partial-walkback study and its triggering of the field's skeleton-skepticism era; React 18 Suspense Contract / 2022 framing as the era marker.

Preserved from Claude's pass: the optimistic-UI four-category carve-out (destructive / financial / async-by-design / non-destructive); the skeleton-faithfulness governance rule (regenerate from layout primitive OR review-on-every-layout-change); the desktop-preserve-vs-mobile-replace responsive logic; the layered Composition table structure (Component owns / Orchestrator owns); the explicit voice-back-reference to 04 §Content as a system layer's matrix as system-level constraint; the full `notes.unverified` flagging discipline.

Five `notes.unverified` flags logged against the practice's `_source-text/`-backing discipline — the 500ms minimum-display threshold's exact NN/g attribution; Polaris's spinner-restriction wording; the Daniel Eden Facebook 2013 URL post-reorganisation; the Viget 2017 study URL; M3's pulse-direction specifics. None of these is load-bearing for the architectural shape; all are field-truth specifics that warrant verification before client-facing quotation.

The pattern is the worked example for the schema's foundations-exile distinction. The synthesis confirms the call: the substantive material — the five-category empty taxonomy, the four-axis error taxonomy, the preserve-vs-replace threshold, the live-region budget with named politeness creep, the optimistic + rollback contract with the four-category carve-out, the skeleton-faithfulness governance — is genuinely cross-component orchestration that no single component can own. The schema's `composition` tier holds.

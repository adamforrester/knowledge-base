*Claude pass — one of two dual-agent inputs for the View-state orchestration pattern brief. A full draft against the patterns spine; to be synthesised with `external-agent.md` into `patterns/view-state-orchestration.md`.*

---

okf_version: "0.1"
type: pattern-brief
title: View-state orchestration
description: Coordinating empty / loading / error states across a region — the taxonomy of states, the skeleton-vs-spinner-vs-optimistic-vs-nothing decision, the layout-preserve-vs-replace choice, and the live-region budget for AT. The components (Empty State, Spinner, Skeleton, Banner, Toast, Inline Message) own their own visuals; this pattern owns the orchestration above them — and the worked example that validates the schema's foundations-exile distinction.
tags: [patterns, view-state, loading, empty, error, accessibility, composition]
tier: composition
goal: recover-from-error
status: draft
timestamp: 2026-06-18

---

# View-state orchestration

> A region — a Table, a List, a Card grid, a dashboard panel — has data, or it doesn't, or it's loading, or it's broken. Each of those is its own component (Skeleton, Spinner, Empty State, Banner) with its own props and a11y. None of those components knows whether to *replace the underlying layout or preserve it*, when to render in parallel vs streaming, what to announce to AT, or which empty (first-use, no-results, no-permission) the user is actually in. Those are coordination decisions, and they live above any single component. This brief owns that coordination and is, by design, the worked example that distinguishes a `composition` pattern from foundations guidance.

---

## Problem & context

Every product surface that loads data crosses the same four-state matrix — pristine, loading, populated, terminal (empty / error) — and the field most visibly disagrees on which surface to use, when to use it, and whether to preserve the surrounding layout or collapse to a centred message. The component briefs cover *what* a Skeleton looks like or *what* an Empty State component takes as props; this pattern covers the orchestration *above* them: the decision rules that resolve the contested forks, the cross-component a11y contract, the taxonomy of states, and the layout-preserve-vs-replace threshold.

The pattern applies anywhere a region renders data that may not be there yet, may not be there ever, or may have failed to arrive — Tables, Lists, Card grids, dashboards, search results, settings panels, profile views, content galleries. It does **not** apply to single-shot UI that has no async data path (a static marketing block); to global notification routing (that's the sibling Notification orchestration pattern); or to full-page error pages (that's the Error pages layout-and-shell pattern).

Systems diverge because they optimise for different perceived-performance regimes. **Polaris and Carbon** lean skeleton-first across the catalogue (the Facebook 2013 lineage; assume content layout is informative; preserve the chrome). **GOV.UK** stays minimal — small, polite spinners on transitional states, and full-page error states for genuine failures (the lowest-trust, AT-critical context; preserve cognitive load over visual continuity). **Material 3** treats progress indicators as the loading default and skeletons as one option among several. **Atlassian and Cloudscape** distinguish region-loading from page-loading explicitly. None of those are wrong; the divergence *is* the decision space.

**The foundations-exile distinction this brief validates.** The schema (`patterns/_schema.md`) draws a sharp line: cross-cutting rules a single component obeys (the bare disabled rule; the bare loading-spinner rule; theming) are Foundations, not patterns. Cross-region *orchestration* — coordinating empty/loading/error across a view, deciding when the Table is replaced with a centred Empty State vs. when it stays and renders row-skeletons — is a `composition` pattern. This brief is the worked example for that distinction. If, on writing it, the material collapsed to "the Skeleton component has these props" or "spinners use ARIA like this," the foundations-exile call would be wrong. It doesn't collapse. The orchestration genuinely owns decisions no single component can: the taxonomy of empty states, the layout-vs-replacement choice, the live-region budget across simultaneously-loading regions, the optimistic-UI rollback path. That is what makes it a pattern.

## Composition

View-state orchestration assembles briefed components and adds the cross-component coordination — it re-derives none of them.

- **Empty State** (`see empty-state`) — the shipped surface for zero-data conditions. Already briefed: visual treatment, the illustration-vs-icon-vs-text axes, the action affordance. The pattern's delta: *which* empty (first-use / no-results / no-permission / filtered-out / system-empty), the per-category copy + action discipline, when the region collapses to it vs. preserves the underlying layout.
- **Spinner** (`see spinner`) — circular indeterminate progress. Already briefed: sizes, the indeterminate-vs-determinate question, the `aria-label` contract. The pattern's delta: when a spinner is appropriate at view scale (vs. skeleton; vs. optimistic; vs. nothing) and the duration thresholds.
- **Skeleton** (`see skeleton`) — content-shaped placeholders. Already briefed: the shape primitives (text-line, circle, rect), the shimmer-vs-pulse animation, the reduced-motion contract. The pattern's delta: when to skeleton, what to skeleton, the faithfulness contract (does the skeleton match the loaded layout's heights and column counts), the all-at-once-vs-staggered choice across multiple regions.
- **Banner** (`see banner`) — region-scoped persistent message. Already briefed: severity (info/warning/error/success), dismissibility, the icon contract. The pattern's delta: when an in-region banner is the right surface for a recoverable error (vs. replacing the region, vs. routing to a toast).
- **Toast** (`see toast`) — transient, dismissed automatically. Already briefed at the component layer. The pattern's delta: the boundary against in-region state messaging — what a toast carries vs. what stays in-region.
- **Inline Message** (`see inline-message`) — small per-control message, typically per-field. Already briefed. The pattern's delta: when an inline message is the right surface for a partial-failure within a region.
- **The underlying layout component** — Table (`see table`), List (`see list`), Card grid (`see card`), Grid (`see grid`), Dashboard panel. These are the surfaces the pattern coordinates state *for*. Their own a11y, structure, and props are inherited; the pattern decides whether they stay or are replaced.

**The delta this pattern adds**: the empty/error taxonomy at view scale, the layout-vs-replacement threshold, the all-at-once-vs-staggered loading choice, the live-region budget across simultaneously-loading regions, the transition contract between states (what should not flicker), the optimistic-UI + rollback path at region scale. Everything below is that delta.

## Decision rules

The heart. Forks given as machine-resolvable rules where a real threshold exists, prose where it genuinely depends.

**1. Loading affordance — skeleton vs spinner vs optimistic vs nothing.** The most-litigated loading decision at view scale.
- `IF perceived duration < ~300ms` → **nothing**. Don't render any loading affordance; the result will arrive before the user looks for it. Rendering a 100ms-skeleton-then-content is the worst of both worlds (the flash-of-loading-then-content thrash).
- `IF predictable layout AND duration ~300ms–~3s AND result is content (not action)` → **skeleton**. Preserves perceived layout stability; signals "data is loading into a known shape."
- `IF unknown/unpredictable layout AND duration ~300ms–~3s` → **spinner** (centred in the region). Skeleton would mislead; spinner says "loading, no claim about what arrives."
- `IF the operation is the result of a user action AND the result is reasonably predictable AND failure rate is low AND failure is non-destructive` → **optimistic UI**. Render the predicted state immediately; reconcile on response; roll back on failure. (Per #9 below.)
- `IF duration > ~10s OR genuinely indeterminate` → **spinner with explanatory text**, OR a status message ("This is taking longer than usual..."), AND ensure user can navigate away without losing state.
- `NEVER` show a spinner that is *also* a skeleton (mid-skeleton spinners are noise). `NEVER` show a skeleton if the layout is a single sentence or a small badge — the affordance costs more than the loading state.

**2. All-at-once vs staggered loading across multiple regions.** A page typically has multiple async regions (header user info, main content, sidebar related items, footer recommendations).
- `IF all regions arrive on roughly the same timeline (within ~500ms of each other)` → **all-at-once skeletons**. Render every region's skeleton in parallel; the page settles to its loaded state in a single visual transition.
- `IF regions have meaningfully different timelines AND priority differs (header is critical; recommendations are nice-to-have)` → **staggered / streaming**. Render each region's skeleton; resolve them as data arrives; prioritise the user's primary task. The React Suspense / streaming-SSR boundary is the modern default for this.
- `NEVER` ship the layout-thrash anti-pattern: regions popping in independently with no skeleton claim, the page layout shifting visibly as each loads. The skeleton is the layout-stability claim.
- The discipline: pick all-at-once *or* staggered *deliberately*; never let the rendering shape be an accident of which API resolved first.

**3. The empty-state taxonomy.** Not a single empty — a family.
- **First-use / zero-data** — the user has the right to see content here, but has not created any yet. Voice: encouraging, one CTA ("Add your first item"). The empty state IS the onboarding moment for this region. Boundary against the Onboarding pattern: a one-frame empty with one CTA is view-state; a multi-step product tour is Onboarding.
- **No-results** — a query was made and returned nothing. Voice: clarifying, with a path back ("No results for *acne*. Try removing filters."). Distinct from first-use because the user *did* something to land here.
- **No-permission** — the user is in the right place but lacks access. Voice: factual, with the path to permission ("This is admin-only. Ask your team owner.")
- **Filtered-out** — a subset of #2: filters reduced everything away. Distinct from no-results because there *is* data, the user just filtered it out. Voice: invites filter relaxation ("0 of 247 results match. Clear filters?").
- **System-empty** — the data has been deleted/archived to zero. Voice: respectful (the user *had* data here). The CTA is typically "Restore from archive" or "Add new."
- `RULE`: shipping a single Empty State surface that doesn't differentiate copy across these five categories is the most-common anti-pattern. Each category has a different copy + action contract; the visual treatment may share an Empty State component, but the *content* is per-category.
- `RULE`: where the empty *itself* is the onboarding moment (first-use only), expand to multi-step Onboarding only when the journey requires more than one frame. Single-frame onboarding-as-empty-state stays here.

**4. The error-state taxonomy at region scale.**
- **Recoverable** — user can retry; render an in-region message + retry action. Banner-shaped (in-region) for transient blips ("Couldn't reach the server. Retry."). Replace-region only if the data is genuinely gone.
- **Non-recoverable** — the data has failed permanently (corrupted; deleted while loading). Replace the region with an error message that names the failure and offers an alternative path.
- **Partial** — some loaded, some failed (a Table where 3 of 10 rows failed). Render what loaded; show an inline-message or banner for the failed portion; offer retry for the failed bits only.
- **Network / offline** — the connection failed. Distinct from server-error because the path forward is "wait for connectivity" not "retry the operation." Render an offline-aware affordance; reconcile when the connection returns.
- **Permission / auth (403)** — the operation is forbidden. Replace the region with the permission message; do not retry (retrying won't help). Boundary: full-page 403 is the Error pages pattern; region 403 lives here.
- **Not-found / 404 at region scale** — the entity within the region is gone, but the page itself is valid. Replace the region; offer a path back (search, list).
- `RULE`: not every region error becomes a toast. Toasts are for *system events* the user should know about; in-region errors stay in-region because the user is looking at the failure. The boundary against Notification orchestration: triggered-by-this-view's-load → in-region; triggered-elsewhere → notification system.

**5. Replacing the underlying layout vs preserving it.** The decision that most distinguishes a pattern from a component.
- `IF the layout itself carries information when populated (a Table's column structure tells you what data lives here)` → **preserve the layout**, render row-shaped skeletons. The empty Table tells the user "this is a list of users with name, role, email." The skeleton preserves that.
- `IF the layout is decorative / containing (a Card grid that simply lays out items)` → **replace** with a centred Empty State / error message. The empty grid carries no information; preserving its chrome is noise.
- `IF the region is a complex composition (a dashboard panel with header, chart, footer)` → **partial preserve**: the panel chrome (header, footer) stays; the content area (chart) renders the appropriate state.
- `RULE`: this is the foundation-exile validating call. The bare "Skeleton component renders this animation" is the component rule. The "preserve-vs-replace per layout-information-content" is the orchestration. The component cannot make this call; the pattern owns it.
- `RULE`: when in doubt, lean preserve for tabular and structured data; lean replace for grid and list-style content where the layout is just a container.

**6. State-message-in-region vs toast vs banner.** The boundary against the Notification orchestration pattern.
- `IF the user just took an action that affects this region AND the state of THIS region needs to communicate` → **in-region** (banner above the region; or replace).
- `IF the user just took an action AND the result is success/failure of an isolated operation that doesn't affect a visible region` → **toast** (Notification orchestration owns this).
- `IF a system event affects this region without a user trigger (a polling refresh failed; a websocket dropped)` → **in-region** (subtle banner / status icon), NOT toast. A toast for every background event is noise.
- `IF the message is a global system state that affects multiple regions (maintenance mode, network down)` → **global banner / system bar** (Notification orchestration). One global banner > many in-region duplicates.
- The discriminating axis: *who triggered the state change, and what's the user's visual locus?* User-triggered + this-region-focus → in-region; everything else routes to the notification system.

**7. The live-region budget at view scale.** WCAG 4.1.3 status messages; `aria-busy`; the polite/assertive split.
- `IF a region is loading` → set `aria-busy="true"` on the region's container; remove on resolution. Do NOT also fire a polite live-region announcement ("Loading…") — `aria-busy` is the AT signal.
- `IF a region resolves to empty (any of the five categories)` → render the empty state with `role="status"` (polite). The first focus / first-tab into the region exposes it naturally.
- `IF a region resolves to error` → `role="alert"` (assertive) for *non-recoverable* errors that block the user; `role="status"` (polite) for recoverable / retry-able errors. The assertive budget is small; spend it on errors that need immediate attention.
- `IF multiple regions load on the same page` → resolve to **at most one** assertive announcement per page-load. Multiple polite announcements are acceptable but should be batched or sequenced (the Notification pattern owns the sequencing rules globally; the pattern owns the per-region call).
- `RULE`: politeness creep is the failure mode. Setting everything to `role="alert"` "to make sure AT users hear it" is the most common a11y anti-pattern in view-state work; AT users abandon assertive-noise sites within seconds. The budget is real.

**8. The transition contract.** When a region moves between states.
- `RULE`: minimum-display threshold of ~200–300ms for any transient state. If a state would render and replace itself in under 200ms, render *neither* — wait for the replacement and skip the transient. (The flash-of-loading-then-content avoidance.)
- `RULE`: preserve scroll position across all state transitions. The user's vertical position within the page is part of their state; rebuilding the layout into a state should not jump them.
- `RULE`: do not flicker between near-identical states. If `loaded → loaded-with-fresh-data` shares the same layout, do not pass through a skeleton in between.
- `RULE`: respect `prefers-reduced-motion`. Any animated transition between states (skeleton shimmer ending; the cross-fade between states) needs a reduced-motion equivalent (often: just hard-cut between states).
- `RULE`: optimistic transitions (#9) need a rollback that does not feel punitive. The rollback animation should signal "this didn't work" without making the user feel wrong; soft cross-fade to the pre-action state with a banner is the convergent pattern.

**9. Optimistic UI's failure mode.**
- `IF the operation is a user action AND the result is reasonably predictable AND failure rate is low AND failure is non-destructive` → **optimistic** is appropriate.
- `IF the operation is destructive (delete, archive)` → **never optimistic**. Confirm explicitly; await server response; show explicit success.
- `IF the operation is financial (charge, transfer, refund)` → **never optimistic**. The error case is too consequential to roll back gracefully.
- `IF the operation is async-by-design (a moderation queue; a render job)` → **never optimistic**. The user's mental model needs to match the system's "this will happen later."
- `RULE` on rollback: when an optimistic update fails, render the pre-action state + a banner naming the failure + a retry path. Do not silently revert — the user thought they did something; the system needs to acknowledge it didn't take.

**10. The skeleton's faithfulness contract.**
- `RULE`: a skeleton must match the loaded layout's heights, column counts, and major shape — not pixel-perfect, but architecturally faithful. The skeleton's job is layout-stability claim.
- `RULE`: skeletons drift. The component evolves (a column is added, a height changes); the skeleton doesn't update. **Skeleton drift is silent until shipping.** The discipline: every skeleton is generated from the same layout primitive as the loaded state, OR is reviewed alongside every layout change. Cloudscape and Atlassian both ship skeletons as derived from the loaded component; this is the durable discipline.
- `RULE`: a generic skeleton (text-line + image-rect) is acceptable when the loaded layout is genuinely simple OR the cost of a faithful skeleton is unjustified. This is rare; defaulting to generic when faithful is achievable is the anti-pattern.
- `RULE` on CLS: the skeleton's job is preventing layout shift. A skeleton that is shorter than the loaded content fails this job; ship the skeleton at the loaded content's dimensions, not at a smaller placeholder size. Lighthouse CLS is the proxy metric.

## Flow & states

The region's lifecycle as a state machine:

**pristine** (the region exists in the DOM but has not started loading; rare — typically only for lazy-loaded regions below the fold) → **loading** (data fetch is in flight; `aria-busy="true"`; the appropriate loading affordance — skeleton/spinner/optimistic/nothing per #1) → **loaded | empty | error**:
- **loaded** — data arrived; the region renders its populated state.
- **empty** — the data set is empty (one of the five categories per #3); the region renders the appropriate Empty State surface.
- **error** — the fetch failed (one of the six categories per #4); the region renders the appropriate error surface.

Transitions:
- `loading → loaded`: cross-fade or hard-cut; skeleton dissolves to populated content.
- `loading → empty`: the skeleton is replaced by the empty state surface (typically a layout-replace, even if the loaded state would have preserved layout — the empty has nothing to render against).
- `loading → error`: the skeleton is replaced by the error surface (preserve-vs-replace per #5; partial-failure is in-region per #4).
- `loaded → loading-fresh-data` (refetch / refresh): typically *no* visible loading state; render fresh data when arrived. If a long-running refetch is in flight, optionally show a subtle indicator (top-of-region progress bar) that does not block interaction.
- `loaded → error` (the data was there, then something broke — websocket dropped, polling failed): show an in-region banner; do not replace the loaded data unless it's invalidated.
- `empty → loaded` (user added data; the empty state's CTA was used): re-fetch and render loaded; hard transition is fine because the user intended the change.
- `error → loading` (retry triggered): re-enter loading; preserve scroll position; the previous error message disappears.

**Optimistic path:** `loaded → optimistic-loaded → reconciled (= loaded with fresh data) | rolled-back (= loaded with banner explaining failure)`. The optimistic state visually = loaded; the difference is internal to the component.

The key invariant: state changes the user did not initiate (background polling, websocket events) get the lightest-touch transition possible (no skeleton, no flash); state changes the user initiated get explicit acknowledgment (loading affordance, success/error message).

## Layout & structure

This pattern is about whether to preserve or replace the underlying layout, not about any particular layout. The composition is regional and lives within whatever layout surface the consuming region occupies (Table, List, Card grid, dashboard panel). The pattern's structural decision is per #5 (preserve-vs-replace) and per #2 (all-at-once vs staggered loading regions); no separate spatial recipe applies.

For responsive: the preserve-vs-replace decision can vary by breakpoint. A Table that preserves layout with row-skeletons on desktop may collapse to Card-shaped skeletons on mobile (because the Table itself collapses to a Card list at mobile breakpoints); the pattern follows the loaded-layout's responsive shape.

## Accessibility orchestration

The cross-component a11y the system owns (each component's own a11y is inherited):

- **`aria-busy`** — set on the region's container while loading; unset on resolution. The single most useful AT signal for "this region is in flight."
- **Live-region budget** — at most one assertive announcement per page-load (per #7); the rest are polite or silent. Assertive is for blocking errors; polite for empty/recoverable errors; silent for `aria-busy`-already-signalled loading.
- **`role="status"` for empty / recoverable error** — polite live-region for non-blocking state messages.
- **`role="alert"` only for blocking errors** — non-recoverable failures that prevent the user from continuing in this region. Use sparingly; politeness creep is the failure mode.
- **Focus management on transitions** — generally *do not* move focus on state transitions (loading → loaded). Forced focus shifts disorient AT users. Exceptions: when the user explicitly retried an error (move focus to the retried region's first interactive element); when the empty state's CTA is the only path forward (move focus to the CTA — but only if the user clearly arrived to act, not browse).
- **Keyboard traversal** — the region's tab order must be consistent across states. The empty state's CTA, the error state's retry button, and the loaded state's first interactive element should occupy roughly equivalent positions in the tab order.
- **The skeleton's a11y** — skeletons are decorative; mark them `aria-hidden="true"` and rely on the parent region's `aria-busy` for the AT signal. Never use skeleton elements as labels or focus targets.
- **Multiple-region coordination** — when a page loads multiple regions in parallel (per #2), the `aria-busy` regions are individually announced as their state changes; the page itself does not need a global "page loading" announcement (the per-region signals carry the news).

This is the single most-important reason view-state orchestration is briefed as a pattern: the a11y contract is cross-component (the region's `aria-busy`, the live-region budget, the focus contract) and no single component can own it. Empty State doesn't know about the Spinner; Skeleton doesn't know about the Banner. The pattern coordinates.

## Content & copy

Near-ALWAYS load-bearing for empty and error states.

**Empty-state copy per category** (per #3):
- **First-use**: encouraging without being saccharine. "Add your first project to get started." Not "You don't have any projects (sad face)."
- **No-results**: clarifying + path back. "No results for *acne*. Try a different term, or clear filters." Not "Empty."
- **No-permission**: factual + path forward. "Only admins can see this. Contact your team owner for access." Not "Forbidden."
- **Filtered-out**: invites filter relaxation. "0 of 247 results match. Clear filters?" Not "No items."
- **System-empty**: respectful (the user *had* data). "Your archive is empty. Items archived in the last 30 days appear here." Not "No archived items."

**Error-state copy** (per #4):
- Specific + actionable: "Couldn't reach the server. Check your connection and retry." Not "Something went wrong."
- The error message says *what* failed and *what to do*; the retry button confirms the path forward.
- Voice for partial failure: acknowledge what loaded, name what didn't. "Showing 7 of 10 items. 3 items failed to load. Retry?"
- Never blame the user. "Your search returned no results" → not "You searched wrong."

**Loading-state copy** (mostly: don't):
- Skeletons get no copy; they are the loading affordance.
- Spinners get an `aria-label` (`aria-label="Loading"` or `aria-label="Loading user data"`) but generally no visible label unless the load is genuinely long (>~3s).
- For long loads: a status message ("Building your dashboard. This usually takes about 5 seconds.") — but only if the load is consistently long; transient long loads should not be over-explained.

**Cross-pattern voice consistency:** all view-state copy follows the system-level voice-and-tone matrix (per `04 §Content as a system layer`). The error voice is the matrix's error tone-context; the empty voice is the matrix's empty tone-context. The pattern doesn't author voice; it consumes the system's voice constraint and applies it to view-state copy. The content tokens for these states (per 04 §Content tokens) ship the templates; this pattern uses them.

## Variants & responsive

The variants are mostly the layout-preserve-vs-replace choice across breakpoints. Per #5 and #10:

- **Desktop preserve (Table with row-skeletons)** ↔ **Mobile preserve (List with card-skeletons)** — when the loaded Table collapses to a Card list at mobile breakpoints, the skeleton follows the same collapse.
- **Desktop preserve** ↔ **Mobile replace** — when the layout-information argument is weaker on mobile (the Table's column structure is collapsed anyway, so preserving an empty Table's chrome is less informative), some systems replace with a centred Empty State at mobile breakpoint. Decide deliberately.
- **Multi-column dashboard preserve** ↔ **Mobile single-column collapse** — each panel preserves or replaces independently per #5; the mobile collapse is the dashboard layout's, not this pattern's.

Reduced-motion: any cross-fade or shimmer is replaced with hard-cut transitions; the loading-affordance choice (skeleton/spinner/optimistic/nothing) is unaffected. Reduced-motion users still see skeletons; they just don't see the shimmer animation.

## Anti-patterns

- **Flash-of-loading-then-content** — rendering a 100ms skeleton-then-content. Either show the skeleton for ≥200ms or don't show it at all.
- **Skeleton drift** — the skeleton no longer matches the loaded component's layout (a column was added; a height changed; a section was rearranged). Silent until shipped.
- **Spinner-by-default-everywhere** — using the Spinner as the loading default, ignoring skeleton's perceived-performance benefit for predictable layouts.
- **One Empty State surface, five categories of empty** — shipping a single Empty State component with the same copy for first-use, no-results, no-permission, filtered-out, and system-empty. Each is its own copy + action contract.
- **Politeness creep** — `role="alert"` on every non-blocking state message; the AT user's experience degrades to assertive noise.
- **Layout-thrash** — each region renders its content as data arrives, with no skeleton claim, so the page layout shifts visibly multiple times per load. The skeleton is the layout-stability claim.
- **Replacing the layout when the layout was informative** — collapsing an empty Table into a centred Empty State, losing the column-structure information that told the user what data lives here.
- **Preserving the layout when the layout was decorative** — rendering Card-grid skeletons for an empty Card grid where the grid carries no information; the chrome adds noise.
- **Optimistic UI on destructive actions** — optimistic delete, optimistic charge, optimistic transfer. The error case is too consequential to roll back gracefully.
- **Toast everywhere** — routing every region-scoped state message to a toast; the toast surface becomes noise; the in-region location loses its information value.
- **Same Empty State without copy differentiation** — same surface for first-use AND no-results. The user's mental model needs the copy to differentiate.
- **Polite-everything-for-AT** — `role="status"` on every state change; the polite live-region budget overflows; AT users can't distinguish important state changes from background noise.
- **Forced focus on every transition** — moving focus on every state change disorients AT users. Move focus only when the user's intent demands it.
- **The skeleton-with-spinner combo** — skeletons inside skeletons or spinners on top of skeletons. Pick one loading affordance per region.

## Related patterns & components

- **View-state orchestration (pattern) vs Empty State / Spinner / Skeleton / Banner / Toast / Inline Message (components)** — each component owns its visuals, props, states, a11y. This pattern owns the *coordination across* components and the *taxonomy of when each is right* — the empty-category-discriminator, the layout-preserve-vs-replace decision, the live-region budget, the optimistic + rollback path.
- **View-state orchestration vs Notification orchestration (pattern)** — both `composition` patterns. Notification orchestration owns Toast/Banner/Inline Message routing system-wide and the do-not-disturb / batching / global live-region budget. View-state orchestration owns *one region's* state coordination. The boundary axis: **who triggered the state, and what's the user's visual locus?** User-triggered + this-region-focus → view-state. Background event / cross-cutting system message / multi-region affecting → notification.
- **View-state orchestration vs Error pages (pattern)** — Error pages is the layout-and-shell pattern that owns full-page 404/500/403/offline. View-state orchestration owns *region-scale* errors that don't replace the page. The boundary: scope. A 404 within a Table row → view-state; a 404 of the entire URL → Error pages.
- **View-state orchestration vs the bare disabled / loading state rules (Foundations)** — the foundations-exile distinction this brief validates. The bare "a button shows a spinner while pending" or "a disabled control gets these visual treatments" are component rules a Button/Form obeys; this pattern is the *region's* coordination of state, which no component owns. The pattern's existence is the worked example for the schema's `composition` tier.
- **View-state orchestration vs Onboarding (pattern)** — when the empty state *is* the onboarding moment. The boundary: a one-frame empty state with one CTA is view-state. A multi-step product tour, a guided checklist, or a multi-screen first-run flow is the Onboarding pattern. Threshold: journey length, not trigger.
- **View-state orchestration vs Bulk actions & selection (pattern)** — the selection pattern owns the multi-select-to-action bar; view-state owns what happens when the bulk operation results in an empty list (replace with Empty State system-empty), an error (in-region banner), or a partial-failure (in-region inline message per row).
- **`composes`:** empty-state, spinner, skeleton, banner, toast, inline-message; reads from the underlying layout component (table, list, card, grid, dashboard).

## Field POV evolution

The field's loading-affordance default has shifted twice in fifteen years.

**Era 1 (pre-2013): spinners by default.** Every region got a centred Spinner (or progress bar) on load. Layout thrash on resolve was the standard cost.

**Era 2 (2013–2020): skeletons everywhere.** Daniel Eden's Facebook 2013 skeleton-screens post and the broader Brad-Frost / Polaris / Carbon skeleton-first stance pushed skeletons as the default for any predictable layout. Polaris's "Skeleton Page" became the canonical example. The trade-off — skeleton-as-noise for very-fast loads, skeleton-drift over time — was undertheorised.

**Era 3 (2020–present): contextual orchestration.** Luke Wroblewski's "let it load" critique and Page Laubheimer / NN/g's work on perceived-performance moved the field toward duration thresholds (don't render any affordance under ~300ms; choose skeleton vs. spinner per layout-predictability) and the React Suspense / streaming-SSR rendering model that shapes "all-at-once vs staggered" today. The current field default: skeleton when layout is predictable AND duration is in the 300ms–3s sweet spot; spinner otherwise; nothing for very-fast loads; optimistic for low-stakes user-action operations.

The optimistic-UI lineage runs in parallel: React Query / TanStack Query / Apollo all ship optimistic-update primitives that have made the pattern accessible. The field has converged on optimistic-for-non-destructive-user-actions; the destructive-financial-async carve-out per #9 is well-attested.

The empty-state taxonomy has matured similarly. Bill Chung's 2020 NN/g treatment of empty states named the first-use vs. no-results vs. system-empty distinctions; the field now generally agrees that one Empty State surface with five different copy contracts is the right shape (vs. five different visual surfaces). Copy is the primary differentiator; visual treatment is shared.

## Reference instantiations

Go look at:
- **IBM Carbon** — Empty States, Loading patterns, the inline-loading vs. skeleton split. Strong on the per-empty-category copy guidance.
- **Shopify Polaris** — Skeleton Page (the canonical full-region skeleton), Empty State, Loading. The skeleton-first stance at its most-articulated.
- **Atlassian Design System** — Empty state, Loading state, Error state. Strong on the region-vs-page distinction; clear preserve-vs-replace examples.
- **Material 3** — Loading indicators (the progress-vs-skeleton stance). Less skeleton-heavy than Polaris/Carbon; useful as the contrast.
- **Adobe Spectrum** — Illustrated message (Spectrum's empty-state surface), Progress circle. Strong on the illustration-as-empty-state visual treatment.
- **Microsoft Fluent** — Empty/Error/Loading patterns. Good on the partial-failure case.
- **GOV.UK Design System** — Error pages, the recovery voice. The minimalist counter-default: small polite spinners, full-page error states. Useful as the "what skeleton-skepticism looks like" reference.
- **Cloudscape** (AWS) — region loading, error, empty. Strong on the multi-region staggered-loading pattern at scale.
- **Ant Design** — Empty / Skeleton / Result. Comprehensive component-side; useful for the per-state-category decision rules.

## Sources cited

- IBM Carbon — Empty States, Loading, Error states (v11, 2025). *Verify current at carbondesignsystem.com.*
- Shopify Polaris — Skeleton Page, Empty State, Loading (2024–25).
- Material Design 3 — Loading indicators (2024–25).
- Atlassian Design System — Empty state / Loading state / Error state (2025).
- Adobe Spectrum — Illustrated message, Progress circle (2025).
- Microsoft Fluent — Loading patterns, Empty patterns (2025).
- GOV.UK Design System — Error pages, recovery voice (v5, 2025).
- Cloudscape (AWS) — Empty/Loading/Error patterns (2025).
- Ant Design — Empty / Skeleton / Result components (2025).
- Daniel Eden — "Skeleton Screens" (Facebook, 2013) — the canonical skeleton-screens lineage.
- Bill Chung — "Empty States: Designing for the Hard-to-Design" (NN/g, 2020). *Secondary source; the empty-state taxonomy lineage.*
- Page Laubheimer — Skeleton vs. spinner work (NN/g). *Verify specific articles.*
- Luke Wroblewski — "Let it Load" critique of skeleton overuse. *Verify specific post.*
- WCAG 2.2 — 4.1.3 Status Messages, 5.1.3 (where applicable); WAI-ARIA — `aria-busy`, `aria-live`, `role="status"`, `role="alert"`.
- React Suspense / streaming SSR — informs the all-at-once-vs-staggered contract (current React docs, 2025–26).
- TanStack Query / React Query — optimistic-update primitives (current docs, 2025–26).

`notes.unverified`: specific NN/g article URLs and dates; Polaris's exact "skeleton first" wording vs. inferred stance; the Daniel Eden post's current URL (Facebook engineering blog has reorganised). The decision-rule *shape* is well-attested across the field; specific quotation depends on per-source verification.

## Agent-consumable schema

```yaml
identity:
  id: view-state-orchestration
  name: View-state orchestration
  aliases: [empty-loading-error orchestration, region state coordination, view state machine]
  tier: composition
  goal: recover-from-error
  status: draft
problem: >
  Coordinate empty / loading / error states across a region (Table, List,
  Card grid, dashboard panel). The taxonomy of states, the
  skeleton-vs-spinner-vs-optimistic-vs-nothing decision, the
  layout-preserve-vs-replace choice, the live-region budget, and the
  transition contract. Applies to any region rendering async data;
  does not apply to single-shot UI, global notification routing, or
  full-page error pages.
composition:
  requires: [empty-state, spinner, skeleton, banner, toast, inline-message]
  reads_from: [table, list, card, grid]  # the underlying layout components
  delta: >
    The empty/error taxonomy at view scale, the layout-vs-replacement
    threshold, the all-at-once-vs-staggered loading choice, the
    live-region budget across simultaneously-loading regions, the
    transition contract, the optimistic + rollback path at region scale.
decision_rules:
  loading_affordance:
    - { if: "perceived duration < ~300ms", use: "render no loading affordance" }
    - { if: "predictable layout AND duration ~300ms-3s AND content (not action)", use: "skeleton" }
    - { if: "unpredictable layout AND duration ~300ms-3s", use: "spinner centred in region" }
    - { if: "user action AND predictable result AND low failure rate AND non-destructive", use: "optimistic UI with rollback path" }
    - { if: "duration > ~10s OR genuinely indeterminate", use: "spinner with explanatory text and let user navigate away" }
    - { if: "always", use: "never combine spinner and skeleton; never skeleton single-line content" }
  multi_region_loading:
    - { if: "all regions resolve within ~500ms of each other", use: "all-at-once skeletons" }
    - { if: "regions have different timelines AND different priority", use: "staggered / streaming SSR" }
    - { if: "always", use: "never let regions pop in independently with no skeleton claim" }
  empty_taxonomy:
    - { if: "empty + user has not yet acted", use: "first-use empty state with encouraging CTA" }
    - { if: "empty + user just queried", use: "no-results empty state with path back" }
    - { if: "empty + user lacks access", use: "no-permission empty state with permission path" }
    - { if: "empty + filters reduced to zero", use: "filtered-out empty state with clear-filters CTA" }
    - { if: "empty + data was previously here", use: "system-empty empty state, respectful voice" }
    - { if: "always", use: "differentiate copy per category even if visual surface is shared" }
  error_taxonomy:
    - { if: "recoverable + transient", use: "in-region banner with retry" }
    - { if: "non-recoverable", use: "replace region with error message" }
    - { if: "partial failure", use: "render what loaded, inline-message for failed bits" }
    - { if: "network / offline", use: "offline-aware affordance, reconcile on connectivity" }
    - { if: "permission 403 at region scale", use: "replace region with permission message; no retry" }
    - { if: "not-found 404 at region scale", use: "replace region with not-found message" }
  preserve_vs_replace:
    - { if: "layout carries information when populated (e.g. Table column structure)", use: "preserve layout, render row-shaped skeletons" }
    - { if: "layout is decorative / containing (e.g. Card grid)", use: "replace with centred empty/error message" }
    - { if: "complex composition (e.g. dashboard panel)", use: "partial preserve: chrome stays, content area renders state" }
    - { if: "always", use: "lean preserve for tabular/structured data; lean replace for grid/list-style" }
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
    - { if: "state would render and replace itself in <200ms", use: "render neither; wait for replacement (avoid flash)" }
    - { if: "always", use: "preserve scroll position across state transitions; never flicker between near-identical states; respect prefers-reduced-motion" }
  optimistic_ui:
    - { if: "user action + predictable + low failure + non-destructive", use: "optimistic UI" }
    - { if: "destructive action (delete, archive)", use: "never optimistic; await server" }
    - { if: "financial action (charge, transfer)", use: "never optimistic; await server" }
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
    - "loading -> empty: replace with empty state (typically layout-replace even if loaded would preserve)"
    - "loading -> error: per #5 preserve-vs-replace; partial-failure stays in-region"
    - "loaded -> loading-fresh-data: typically no visible state; subtle indicator if long-running"
    - "loaded -> error: in-region banner, do not replace unless invalidated"
    - "empty -> loaded: hard transition (user intended the change)"
    - "error -> loading (retry): re-enter loading, preserve scroll"
  optimistic_path: "loaded -> optimistic-loaded -> reconciled | rolled-back-with-banner"
accessibility_orchestration: >
  aria-busy on region container while loading; live-region budget (at most
  one assertive per page-load; politeness creep is the failure mode);
  role=status for empty/recoverable, role=alert for blocking; do not move
  focus on transitions except when user explicitly retried or empty CTA is
  the only path forward; consistent tab order across states; skeletons are
  aria-hidden=true; multiple-region loading uses per-region aria-busy
  signals not a global page-loading announcement.
content:
  empty_per_category: "first-use encouraging, no-results clarifying with path back, no-permission factual with permission path, filtered-out invites filter relaxation, system-empty respectful"
  error: "specific + actionable; says what failed and what to do; never blame user; partial-failure acknowledges what loaded and what didn't"
  loading: "skeletons get no copy; spinners get aria-label only; long loads (>3s) may get status message"
  voice_consistency: "all view-state copy follows the system-level voice-and-tone matrix per 04 Content as a system layer; the pattern consumes voice constraint, does not author it"
variants: [preserve-layout, replace-layout, partial-preserve, all-at-once-multi-region, staggered-multi-region]
anti_patterns:
  - flash-of-loading-then-content (skeleton <200ms)
  - skeleton drift (skeleton no longer matches loaded layout)
  - spinner-by-default-everywhere
  - one Empty State surface with same copy for all five empty categories
  - politeness creep (role=alert on every state message)
  - layout-thrash (regions popping in independently with no skeleton claim)
  - replacing layout when layout was informative
  - preserving layout when layout was decorative
  - optimistic UI on destructive/financial/async-by-design actions
  - toast everywhere (every region message routed to global toast)
  - polite-everything-for-AT (role=status overflow)
  - forced focus on every transition
  - skeleton-with-spinner combo
reference_instantiations:
  - { system: "IBM Carbon", look_at: "Empty States, Loading, Error patterns" }
  - { system: "Shopify Polaris", look_at: "Skeleton Page, Empty State, Loading (skeleton-first stance)" }
  - { system: "Atlassian", look_at: "Empty state / Loading state / Error state (region-vs-page distinction)" }
  - { system: "Material 3", look_at: "Loading indicators (progress-vs-skeleton stance)" }
  - { system: "Adobe Spectrum", look_at: "Illustrated message, Progress circle" }
  - { system: "Microsoft Fluent", look_at: "Empty/Error/Loading patterns (partial-failure)" }
  - { system: "GOV.UK", look_at: "Error pages, recovery voice (skeleton-skeptical default)" }
  - { system: "Cloudscape (AWS)", look_at: "Multi-region staggered-loading at scale" }
  - { system: "Ant Design", look_at: "Empty / Skeleton / Result components" }
relations:
  composes: [empty-state, spinner, skeleton, banner, toast, inline-message]
  reads-from: [table, list, card, grid]  # the underlying layout components
  relates-to: [notification-orchestration, error-pages, onboarding, bulk-actions-and-selection]
  boundary: >
    Components own visuals/props/states/a11y; this pattern owns coordination
    across them and the taxonomy of when each is right. Notification
    orchestration owns global toast/banner routing; this pattern owns
    one-region's state. Error pages owns full-page errors; this pattern owns
    region-scale errors. Foundations (the bare disabled/loading rules) are
    component-obeyed; this pattern is the region's orchestration. Onboarding
    is multi-step; one-frame empty-as-onboarding stays here.
  foundations_exile_validation: >
    This pattern is the worked example for the schema's foundations-exile
    distinction: cross-region orchestration is a `composition` pattern; bare
    state rules a component obeys are foundations. The pattern's existence
    as substantive material — the empty taxonomy, the preserve-vs-replace
    threshold, the live-region budget, the optimistic + rollback path —
    confirms the call.
notes:
  contested: >
    skeleton-default vs spinner-default (Polaris/Carbon vs Material/GOV.UK);
    the optimistic-UI threshold for low-stakes actions; whether
    no-permission and not-found are empty-state or error-state categories;
    the all-at-once-vs-staggered default in 2026 (streaming SSR is shifting
    this).
  unverified: >
    specific NN/g article URLs and dates; Daniel Eden's current Facebook
    engineering blog URL; Polaris's exact "skeleton first" wording; the
    300ms / 200ms threshold figures (well-attested heuristics, not single-
    sourced constants).
  secondary-tier: >
    none — this is a pure `composition` pattern.
```

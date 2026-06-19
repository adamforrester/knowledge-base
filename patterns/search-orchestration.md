---
okf_version: "0.1"
type: pattern-brief
title: Search orchestration
description: The search EXPERIENCE around the Search field component — the zero-query state, typeahead suggestions (query-suggestions vs result-previews vs federated), scoped/autodirect search, the results surface, the no-results state, and the instant-vs-submit decision with its debounce + AbortController race contract. Composes Search field/Combobox + Popover + List + Empty State + Spinner/Skeleton; borders the Search field component (the input), the Filtering pattern (narrowing a known set), View-state orchestration (the results' states), the Command palette (search-as-action-launcher), and results pagination.
tags: [patterns, search, combobox, accessibility, navigate]
tier: composition
goal: navigate
status: stable
aliases: [Search orchestration, search experience, typeahead, autocomplete search, instant search, omnibox]
last-audited: 2026-06-18
timestamp: 2026-06-18
---

# Search orchestration

> The Search field is a text input that takes a query; it knows nothing about what happens around it. The *experience* is the pattern: what the dropdown shows before a key is pressed, whether results update as you type or wait for Enter, whether suggestions complete the query or jump to a result, what the results surface looks like, and — the state everything hinges on — what happens when there are no results. Get the field right and the search can still fail: a dead-end "0 results," a dropdown that thrashes the server on every keystroke, stale results from an out-of-order response, suggestions that don't say whether they search or navigate. This brief owns the orchestration around the field. It defers the input control to the Search field/Combobox component and the result states to View-state orchestration, and resolves only the search-specific decisions.

---

## Problem & context

Search is the second navigation system of any content-dense product — the one users reach for when the primary nav fails them, which is exactly when they are least patient, and for a high-intent cohort it is the *first* interaction, not the fallback. The cost of getting it wrong is well-measured: search problems are the most-cited navigation frustration, an unsuccessful search routinely converts to an abandoned session, and missing typo-tolerance drives abandonment outright (Baymard / NN/g — *figures to verify before quoting*). The recurring trap is that the input is easy and the *experience* is hard: the moment of truth is not the field but the dropdown, the result list, and the empty state. Ship a styled search box without a considered zero-query state, a debounce, an out-of-order guard, a suggestion model, and a no-results state that recovers rather than dead-ends, and the search is worse than none — it tells users their thing isn't here when it is.

The pattern applies wherever users query an *unknown* — site/app search, docs, a large data set, command launching. It does **not** apply to narrowing a known, visible set (that is Filtering, the sibling) or to a simple select-from-a-list (that is the Combobox component). The field and the literature genuinely diverge: NN/g cautions that enriched suggestions are often ignored or mistaken for ads; Baymard insists on typo tolerance, query persistence, and no dead ends; hosted platforms push aggressive instant federated search. They diverge because search optimises for different things at different scales — a 50-item client-side list wants instant as-you-type; a billion-document backend wants a debounced, ranked, typo-tolerant query with a real results page. The decisions below resolve by scale, latency, and intent rather than by fashion.

## Composition

Search orchestration assembles briefed components into an accessible state machine and adds the experience; it re-derives none of them.

- **Search field / Combobox** (see combobox, see text-field) — the input control, with its `role`, `aria-expanded`, activedescendant tracking, and keyboard capture. Orchestration treats it as a black box: it listens to change events and overrides the ARIA references by data state, deciding *what the combobox is wired to* and *what its popup contains*.
- **Popover / Flyout** (see popover) — the transient overlay surface for suggestions/results; orchestration owns its positioning, dimensional constraints, and z-index (critical inside modals and nested DOM).
- **Empty State** (see empty-state) — the no-results surface; the most important state, and a search-specific instance of the empty taxonomy.
- **List / Menu** (see list, see menu) — the suggestions popup and the results list.
- **Spinner / Skeleton** (see spinner, see skeleton) — the loading state, via View-state orchestration.
- **Tag** (see tag) — applied scope/filter chips when search combines with filtering.
- **View-state orchestration** (see patterns/view-state-orchestration) — composes the results region's loading/empty/error states; this pattern adds only the search-specific no-results content.

**The delta this pattern adds** is the orchestration: the instant-vs-submit decision and its debounce + race guard, the suggestion model, the zero-query and no-results content, the scope/autodirect model, and the live announcement of results — none of which the field or any single component owns.

## Decision rules

The heart. Machine-resolvable where a real threshold exists.

**1. Instant (as-you-type) vs submit-on-enter** — the central fork.
- `IF the corpus is small/client-side (≲ a few thousand rows) OR latency consistently < 100ms AND the index supports partial-word fuzzy` → **instant**, results update on keystrokes.
- `IF the query is expensive, the corpus is large/remote, or latency > ~300ms` → **submit on Enter**, route to a dedicated results page, with as-you-type **suggestions** (not full results) in the dropdown.
- `IF instant` → **debounce** (≈150–300ms desktop; longer on mobile/slow networks — a heuristic band, not a constant) **and guard against out-of-order responses** with an `AbortController`/cancellation token: cancel the in-flight request on each new keystroke so a slow "java" response can't arrive after and overwrite "javascript". This is the single most common search bug.
- `IF a query is shorter than the minimum useful length (~1–2 chars)` → don't fire; show the zero-query state.
- Mobile leans toward submit/suggestions over instant full-result reloads (cost, keyboard occlusion).

**2. Suggestion / typeahead model** — what the dropdown contains.
- `IF a homogeneous document/article corpus` → **query suggestions** (completions): selecting one *fills and searches*; wire `aria-autocomplete="list"`; bold the suggested completion against the standard-weight typed portion.
- `IF discrete actionable entities (profiles, tickets, products)` → **result previews** (jump-to): selecting one *navigates to the item*, bypassing the results page. Make the two visually and behaviourally distinct so the user knows whether Enter searches or navigates.
- `IF multiple content domains` → **federated** dropdown: grouped, labelled sections (≈3–5 suggestions + 3–5 result previews, maybe actions/people).
- `NEVER` use `aria-autocomplete="both"` (auto-injecting the prediction inline) unless heavily optimised — it needs fragile selection-range management and fights the user's typing.
- Cap the list at **≈5–9** items — more overwhelms and forces an internal scrollbar.

**3. The zero-query state** — what shows before typing; never an empty dropdown.
- `IF authenticated AND privacy permits` → **recent searches** (last 3–5, with a clear/manage control; store locally with no PII/tokens, mind shared devices).
- `IF anonymous OR no history` → **trending/popular** (3–5) to show catalogue breadth.
- `IF a ⌘K palette` → global navigation nodes / recent files / top actions.

**4. Scoped & autodirect.**
- `IF the product has distinct entities/sections (projects, repos)` → offer **scope**, defaulting to the most-likely scope (often the current section) with a one-tap widen to global; the affordance lives on the leading edge of the field; echo the active scope in the results header.
- `IF a query is a 1:1 exact match to a top-level category` → **autodirect**: intercept the submission and navigate straight to that category page rather than a generic results list.
- `IF results span entities` → **federate**: group by entity with labelled sections and a "see all in X."

**5. The results surface.**
- `IF results are few and selection is the goal` → inline **dropdown popover** (limited, closes on outside click).
- `IF results are many, rankable, refinable` → a **full results page** (with filters — the seam to Filtering) reached on submit; the dropdown carries suggestions only.
- `ALWAYS` **highlight the matched substring**, show a **result count**, and signal ranking by order. Pagination vs infinite scroll of the results is the data-pattern's call (reference, don't re-derive) — bias to "load more"/pagination for findability.

**6. The no-results state** — the state everything hinges on; `NEVER` a dead end.
- `IF the literal query returns zero` → **fuzzy / typo tolerance** (Levenshtein "did you mean…?"); content corpora must have this — its absence is a top abandonment cause.
- `IF tolerance still yields nothing` → an intelligent no-results state: confirm the query, then offer a route forward — broaden the scope, drop a filter, suggested/popular alternatives. Fire a no-results analytics event (a primary conversion signal).
- Composes View-state orchestration's empty taxonomy; this is its search-specific instance — distinct from "no data exists," because the data may exist under a different query.

**7. Loading & latency.**
- `IF results refresh in place` → **keep the stale results visible** (optionally dimmed) with a subtle busy indicator rather than flashing a skeleton (avoids layout thrash on fast queries).
- `IF a request is initiated` → wait a slight **~50ms before showing a spinner**, so fast connections never flicker.
- `IF first load / scope change` → skeleton. `IF slow (> ~1s)` → a clear in-progress signal; never an indefinite spinner with no fallback.

**8. Search affordance & invocation.**
- `IF search is primary to the product` → a **persistent, visible field** in the shell; don't hide it behind an icon.
- `IF search is secondary / space is tight (mobile, dense headers)` → an **icon that expands** and immediately focuses; labelled and keyboard-reachable.
- Offer a **keyboard shortcut** (`/` to focus; `⌘K`/`Ctrl-K` for a command-palette overlay) shown as a hint in the field.
- Mobile: tapping search transitions to a **full-screen** search view, auto-focused, with an explicit Submit/Cancel (don't rely on the keyboard return key alone).

**9. Query handling.** Typo tolerance and synonyms are table stakes for content search. Provide a **clear (×)** control. **Persist the query and scope** in the field and the URL so a search is shareable, survives reload, and supports iterative refinement ("sofa" → "blue sofa") — clearing the box on submit is a top failure. Store recent searches locally with a clear control.

## Flow & states

The lifecycle as a state machine: **idle** (placeholder, optional shortcut hint; no network) → **zero-query / focused** (dropdown opens immediately with recent/trending; parse local store / fetch trending) → **typing / debounce** (clear-× appears, existing results may dim; timer running, no call yet; below min-length stays zero-query) → **fetching** (AbortController cancels pending; spinner after ~50ms or skeleton) → **results-completions** (typed chars bolded) | **results-entities** (cards/rows) | **no-results** (query confirmed, recovery offered, analytics event fired) | **error** (retry — via View-state orchestration) → **submitted** (viewport navigates to the results page; query to URL `?q=`). Esc collapses the popup, a second Esc clears; the active query persists in the field and URL.

## Accessibility orchestration

The a11y the *experience* owns; the field's own combobox basics are inherited.
- **The combobox/listbox contract** — the field is a `combobox` with `aria-expanded` and `aria-controls` pointing at the `listbox` popup of `option`s; arrow keys move a visible active option via `aria-activedescendant` **while DOM focus stays in the input**, so typing never breaks. Orchestration's job is keeping this correct as content changes.
- **Result-count announcement, on a separate region** — a dedicated **visually-hidden** `aria-live="polite"` / `role="status"` region announces the **aggregate count + how to navigate** ("12 results, use up and down arrows"), not the individual items, debounced so as-you-type doesn't spam it (the live-region budget). **Do not** put `aria-live` on the listbox itself while using `aria-activedescendant` — it double-speaks badly in VoiceOver (reading the whole list *and* the active option).
- **Instructional cue** on focus via `aria-describedby` ("Search available. Type to filter suggestions."); **no-results** announced immediately ("No results found for [query].").
- **Focus management** — focus stays in the input during suggestion navigation; moving to a full results page moves focus to the results heading; Esc returns predictably. Mobile full-screen search announces the transition and moves focus into the field.
- Defer to the Search field component for the input's own label, `role`, and clear-button a11y.

## Content & copy

- **Placeholder** states the scope or an example ("Search invoices," "Search documentation"), never a generic "Search…" where scope is ambiguous, never the only label (a11y — always a persistent, optionally visually-hidden `<label>`), and never overloaded with instructions.
- **No-results copy** confirms the exact query and points forward: "No results for '*xyzz*'. Check the spelling, try fewer words, or browse popular topics." Never a bare "No results," never blame.
- **Result count** is explicit ("12 results for '*foo*'") and doubles as the live-region text.
- **Suggestion labelling** distinguishes query-suggestions from jump-to-results (icon or section label) so Enter's behaviour is predictable.
- **Clear control** carries an explicit label (`aria-label="Clear search"`).
- **Scope copy** echoes the active scope ("Results in Billing") with a widen affordance.

## Variants & responsive

- **Inline dropdown** (suggestions/quick results) vs **full results page** (ranked, refinable) vs **both** (dropdown suggests, Enter goes to the page).
- **Icon-expand** field for tight spaces; **persistent** field where search is primary.
- **Command palette** (`⌘K`) — the federated, action-launching variant: shares the combobox/listbox machinery and federated model, adds command execution, **subsequence fuzzy matching** ("dm" → "Dark Mode"), a strict focus trap, and recent-actions (borders the Command palette pattern).
- **Full-screen mobile** search view: intercept the tap, route to a focused full-screen view with an explicit Submit/Cancel (inline dropdowns collide with the software keyboard).

## Anti-patterns

The orphaned promise — as-you-type firing async queries with no `AbortController`, so out-of-order responses overwrite fresh results with stale ones. As-you-type heavy/remote queries with no debounce (server thrash, jank). Query amnesia — clearing the box on submit, forcing users to retype to iterate. The dead-end "No results" with no route forward. Over-rendering suggestions (>10, scroll-within-scroll). Hiding search behind an icon when it's primary. Suggestions that don't signal whether they search or navigate. No result count exposed to AT, or `aria-live` on the listbox (double-speak). Stealing the Enter key — if the user hits Enter before suggestions load, abort the suggestion fetch and submit the typed string, don't block or run a default. An indefinite spinner with no slow-search fallback; flashing a skeleton over millisecond refreshes. A scope selector that resets the query. Exact-substring-only matching on a content corpus.

## Related patterns & components

- **vs the Search field / Combobox (component)** (see combobox) — the raw input control (anatomy, clear button, the `combobox`/`searchbox` role, baseline ARIA) vs the experience around it (this pattern, which connects it to networks, state, debounce, and the popup contents). The field is composed, not re-derived.
- **vs Filtering (pattern)** — search queries an *unknown* via free text ("find me X"); filtering narrows a *known, visible* set via structured facets ("show only Y"). They combine as **faceted search** on a results page (the search query funnels, filters refine); the seam is that search produces the set, filters refine it.
- **vs View-state orchestration (pattern)** (see patterns/view-state-orchestration) — the results region's loading/empty/error states compose it; the **no-results** state is the search-specific empty instance (the data may exist under another query — distinct from "no data exists").
- **vs Command palette** — search-as-action-launcher (`⌘K`): the same combobox/federated machinery and focus-trap, but it executes commands and navigates rather than returning content results, with subsequence matching and sub-50ms latency expectations. The boundary case this pattern shades into.
- **vs results pagination / infinite scroll** — on the full results page, orchestration hands off to the data pattern; referenced, not re-derived.
- **`composes`:** combobox, text-field, popover, empty-state, list, menu, spinner, skeleton, tag.

## Field POV evolution

Four phases. **Synchronous form-submit** (1990s–2000s): type, Enter, full reload, no dynamic feedback. **AJAX autocomplete** (2010s): basic typeahead, but plagued by race conditions, jank, and silent DOM mutations that left screen readers behind — NN/g flagged early implementations as distracting. **Federated & instant** (2015+, driven by Algolia and cheap hosted search): the dropdown became a mini-application rendering rich previews across multiple indexes, and instant-as-you-type became the default for small/fast corpora while large corpora kept submit + suggestions — the scale-dependent split this brief encodes. **The action launcher / ⌘K** (2020+, VS Code/Linear/Raycast): search became command execution; subsequence matching and sub-50ms latency became table stakes, normalising keyboard-first search. Typo tolerance and synonyms moved from premium to baseline across the same arc.

## Reference instantiations

Go look at: the **WAI-ARIA APG combobox pattern** (the listbox/activedescendant contract and the editable-combobox-with-list example); **Algolia Autocomplete + InstantSearch** (the federated suggestion/result model and the debounce/cancellation handling); **IBM Carbon** search (default vs fluid variants + labelling); **Material** docked/full-screen search; **GOV.UK** search and no-results; the **⌘K palettes** (Linear, Raycast, Algolia DocSearch) for the action-launcher variant; **Baymard** and **NN/g** for the e-commerce search and zero-results research.

## Sources cited

- WAI-ARIA Authoring Practices Guide — combobox pattern, `aria-autocomplete`, listbox/option roles, `aria-activedescendant`, the editable-combobox-with-list example (2026; *verify*).
- Nielsen Norman Group — search UX, autocomplete/enriched suggestions, zero/low-results (the 23%-suggestion-selection finding) (*verify articles/dates/figures*).
- Baymard Institute — e-commerce search, autocomplete spelling/typo tolerance, category-scope autodirect, query persistence, B2B/mobile search (the 53%/76%/69%/37% figures) (*verify specific figures before quoting*).
- Algolia — Autocomplete library and InstantSearch (the federated model; debounce/cancellation) (*verify version*).
- IBM Carbon — Search component + pattern (default vs fluid) (v11, 2025; *verify*); Shopify Polaris (autocomplete/portal z-index), Material 3, Atlassian, Adobe Spectrum, Microsoft Fluent SearchBox — search patterns where documented (*spotty; flag where absent*).
- GOV.UK Design System — search and no-results guidance (2025; *verify*).
- MDN / ARIA — `aria-live` regions, `aria-autocomplete`, the activedescendant double-speak caveat; the JS `AbortController` race-condition pattern (current; *verify*).
- The ⌘K / command-palette lineage — Linear, Raycast (DESIGN notes), Algolia DocSearch; subsequence matching (*secondary; product observation*).

`notes.unverified`: the percentage figures (53% search frustration, 76% lost sale, 23% suggestion selection, 69% typo abandonment, 37% no-persistence) come from the external pass attributed to Baymard/NN-g — compelling and directionally well-established, but **verify each against the primary source before quoting**. The debounce band (≈150–300ms; longer on mobile) and minimum-query-length (~1–2 chars) are widely-used heuristics, not sourced constants. Which design systems ship a *named* search-experience pattern vs only a Search component is spotty (Carbon is clearest); verify before asserting convergence. Current version strings flagged.

## Agent-consumable schema

```yaml
identity:
  id: search-orchestration
  name: Search orchestration
  aliases: [search experience, typeahead, autocomplete search, instant search, omnibox]
  tier: composition
  goal: navigate
  status: stable
problem: >
  The search experience around the Search field — zero-query state, typeahead
  suggestions, scope/autodirect, the results surface, and (above all) the
  no-results state — plus the instant-vs-submit decision and its debounce +
  AbortController race contract, and the AT announcement budget. Applies when
  users query an unknown; not for narrowing a known set (Filtering) or
  select-from-list (Combobox).
composition:
  requires: [combobox, text-field, popover, empty-state, list, menu, spinner, skeleton, tag]
  delta: instant-vs-submit + debounce + race guard, suggestion model, zero-query + no-results content, scope/autodirect, live result announcement
decision_rules:
  instant_vs_submit:
    - { if: "corpus small/client-side (<= ~few thousand) or latency <100ms with partial-word fuzzy", use: "instant as-you-type" }
    - { if: "query expensive, corpus large/remote, or latency >~300ms", use: "submit on Enter -> results page + suggestions-only dropdown" }
    - { if: "instant", use: "debounce ~150-300ms (longer on mobile) AND AbortController to cancel out-of-order responses" }
    - { if: "query below min length (~1-2 chars)", use: "do not fire; show zero-query state" }
  suggestion_model:
    - { if: "homogeneous document corpus", use: "query suggestions (fill+search), aria-autocomplete=list, bold the completion" }
    - { if: "discrete actionable entities", use: "result previews (jump-to/navigate), visually distinct from suggestions" }
    - { if: "multiple content domains", use: "federated grouped dropdown (~3-5 each, labelled)" }
    - { if: "tempted by aria-autocomplete=both", use: "avoid unless heavily optimised" }
    - { if: "always", use: "cap suggestions ~5-9 (no internal scrollbar)" }
  zero_query:
    - { if: "authenticated and privacy permits", use: "recent searches (3-5, clearable, no PII/tokens)" }
    - { if: "anonymous or no history", use: "trending/popular (3-5)" }
  scope_autodirect:
    - { if: "distinct entities/sections", use: "scope selector on leading edge, default most-likely, one-tap widen" }
    - { if: "query is 1:1 exact category match", use: "autodirect to the category page (skip generic results)" }
    - { if: "results span entities", use: "federate: labelled groups + see-all-in-X" }
  results_surface:
    - { if: "few results, selection is the goal", use: "inline dropdown popover" }
    - { if: "many, rankable, refinable", use: "full results page (+ filters); dropdown = suggestions only" }
    - { if: "always", use: "highlight match, show result count, signal ranking by order" }
  no_results:
    - { if: "zero exact matches", use: "fuzzy/typo tolerance + did-you-mean" }
    - { if: "still nothing", use: "confirm query + route forward (broaden, drop filter, popular); fire analytics; never a dead end" }
  loading:
    - { if: "results refresh in place", use: "keep stale results (dimmed) + subtle busy indicator" }
    - { if: "request initiated", use: "~50ms delay before spinner (no flicker)" }
    - { if: "first load / scope change", use: "skeleton" }
    - { if: "slow (>~1s)", use: "clear in-progress signal; never indefinite spinner" }
  invocation:
    - { if: "search primary", use: "persistent visible field" }
    - { if: "secondary / tight space", use: "labelled icon-expand (immediate focus)" }
    - { if: "always", use: "offer / and cmd-K shortcuts, shown as a hint" }
    - { if: "mobile", use: "full-screen view, auto-focus, explicit Submit/Cancel" }
  query_handling:
    - { if: "content corpus", use: "typo tolerance + synonyms as table stakes" }
    - { if: "always", use: "clear (x); persist query+scope in field and URL; local recent-search store" }
flow: [idle, zero-query, typing-debounce, fetching, results-completions, results-entities, no-results, error, submitted]
accessibility_orchestration: >
  combobox + aria-expanded + aria-controls -> listbox of options; arrow keys move
  aria-activedescendant while DOM focus stays in the input; a SEPARATE
  visually-hidden aria-live=polite/role=status region announces the aggregate
  count + nav instruction (debounced), never the items, and NEVER aria-live on
  the listbox itself (VoiceOver double-speak); aria-describedby instructional
  cue on focus; no-results announced immediately; focus to results heading on
  full-page search; mobile full-screen transition announced + focus moved.
  (Field's own label/role/clear a11y deferred to the component.)
content: >
  Placeholder states scope/example (not the only label, not overloaded);
  no-results copy confirms the exact query + points forward (no blame);
  explicit result count doubles as live-region text; suggestions signal
  search-vs-navigate; clear control labelled; scope copy echoes active scope.
variants: [inline-dropdown, full-results-page, both, icon-expand, persistent-field, command-palette, full-screen-mobile]
anti_patterns:
  - orphaned promise (no AbortController -> stale out-of-order results)
  - as-you-type heavy/remote queries with no debounce
  - query amnesia (clearing the box on submit)
  - dead-end no-results with no route forward
  - over-rendering suggestions (>10, scroll-within-scroll)
  - hiding search behind an icon when it is primary
  - suggestions that do not signal search-vs-navigate
  - no result count for AT, or aria-live on the listbox (double-speak)
  - stealing the Enter key (not submitting typed string if Enter precedes suggestions)
  - indefinite spinner with no slow-search fallback; skeleton flash on fast refresh
  - scope selector that resets the query
  - exact-substring-only matching on a content corpus
reference_instantiations:
  - { system: "WAI-ARIA APG", look_at: "combobox pattern: listbox + activedescendant; editable-combobox-with-list" }
  - { system: "Algolia", look_at: "Autocomplete + InstantSearch (federated, debounce, cancellation)" }
  - { system: "IBM Carbon", look_at: "Search component + pattern (default vs fluid)" }
  - { system: "Material 3", look_at: "docked / full-screen search" }
  - { system: "Command palettes", look_at: "Linear / Raycast / Algolia DocSearch (cmd-K, subsequence match)" }
relations:
  composes: [combobox, text-field, popover, empty-state, list, menu, spinner, skeleton, tag]
  relates-to: [filtering, view-state-orchestration, command-palette, forms-as-a-system]
  boundary: >
    The Search field/Combobox component is the input; this pattern is the
    experience around it. Filtering narrows a known set; search queries an
    unknown; they combine as faceted search (search produces the set, filters
    refine). View-state orchestration owns the results' loading/empty/error;
    no-results is the search-specific empty instance. Command palette is
    search-as-action-launcher (shares the machinery, executes commands).
    Results pagination/infinite-scroll referenced, not re-derived.
notes:
  contested: "instant vs submit at mid-size corpora; dropdown-results vs page-results; how aggressive typo tolerance should be"
  unverified: "the percentage figures (53/76/23/69/37%) are attributed to Baymard/NN-g via the external pass — verify against the primary source before quoting; debounce ~150-300ms and min-length ~1-2 chars are heuristics not constants; which design systems ship a NAMED search experience pattern (Carbon clearest); version strings"
```

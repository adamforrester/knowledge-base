*Claude pass — one of two dual-agent inputs for the Search orchestration pattern brief. A full draft against the patterns spine; to be synthesised with `external-agent.md` into `patterns/search-orchestration.md`.*

---

okf_version: "0.1"
type: pattern-brief
title: Search orchestration
description: The search EXPERIENCE around the Search field component — the zero-query state, typeahead/suggestions (query-suggestions vs result-previews vs federated), scoped vs global search, the results surface, the no-results state, and the instant-vs-submit decision with its debounce/race-condition contract. Composes Search field/Combobox + Empty State + List + Spinner/Skeleton; borders the Search field component (the input), the Filtering pattern (narrowing a known set), View-state orchestration (the results' states), the Command palette (search-as-action-launcher), and results pagination.
tags: [patterns, search, combobox, accessibility, navigate]
tier: composition
goal: navigate
status: draft
aliases: [Search orchestration, search experience, typeahead, autocomplete search, instant search]
last-audited: 2026-06-18
timestamp: 2026-06-18

---

# Search orchestration

> The Search field is a text input that takes a query; it knows nothing about what happens around it. The *experience* is the pattern: what the dropdown shows before a key is pressed, whether results update as you type or wait for Enter, whether suggestions complete the query or jump to a result, what the results surface looks like, and — the state everything hinges on — what happens when there are no results. Get the field right and the search can still fail: a dead-end "0 results," a dropdown that thrashes the server on every keystroke, suggestions that don't say whether they search or navigate. This brief owns the orchestration around the field. It defers the input control to the Search field/Combobox component and the result states to View-state orchestration, and resolves only the search-specific decisions.

---

## Problem & context

Search is the second navigation system of any content-dense product — the one users reach for when the primary nav fails them, which is exactly when they are least patient. The recurring problem is that the input is easy and the *experience* is hard: the moment of truth is not the field but the dropdown, the result list, and the empty state. Teams ship a styled search box and discover that without a considered zero-query state, a debounce, a federated suggestion model, and a no-results state that recovers rather than dead-ends, the search is worse than no search — it actively tells users their thing isn't here when it is.

The pattern applies wherever users query an unknown — site/app search, docs, a large data set, command launching. It does **not** apply to narrowing a known, visible set (that is Filtering, the sibling) or to a simple select-from-a-list (that is the Combobox component). The field and the literature diverge because search optimises for different things at different scales: a 50-item client-side list wants instant as-you-type; a billion-document backend wants a debounced, ranked, typo-tolerant query with a real results page. The decisions below resolve by scale, latency, and intent rather than by fashion.

## Composition

Search orchestration assembles briefed components and adds the experience; it re-derives none of them.

- **Search field / Combobox** (see combobox, see text-field) — the input control, with its `role`, `aria-expanded`, and `aria-autocomplete` basics. This pattern decides *what the combobox is wired to* and *what its popup contains*, not how the input renders.
- **Empty State** (see empty-state) — the no-results surface; the most important state, and a search-specific instance of the empty taxonomy.
- **List / Menu** (see list, see menu) — the suggestions popup and the results list; the option/row anatomy.
- **Spinner / Skeleton** (see spinner, see skeleton) — the results loading state, via View-state orchestration.
- **Tag** (see tag) — applied scope/filter chips when search combines with filtering.
- **View-state orchestration** (see patterns/view-state-orchestration) — composes the results region's loading/empty/error states; this pattern adds only the search-specific no-results content.

**The delta this pattern adds** is the orchestration: the instant-vs-submit decision and its debounce, the suggestion model, the zero-query and no-results content, the scope model, and the live announcement of results — none of which the field or any single component owns.

## Decision rules

The heart. Machine-resolvable where a real threshold exists.

**1. Instant (as-you-type) vs submit-on-enter** — the central fork.
- `IF the corpus is small and client-side (≲ a few thousand rows) OR latency is sub-100ms` → **instant**, filtering live as the user types.
- `IF the query is expensive, the corpus is large/remote, or results navigate away/reload` → **submit on Enter**, with as-you-type **suggestions** (not full results) in the dropdown.
- `IF instant` → debounce input (≈150–300ms) and **guard against out-of-order responses** (ignore a response older than the latest dispatched query — the race-condition bug that shows stale results).
- `IF a query is shorter than the minimum useful length (often 1–2 chars)` → don't fire; show the zero-query state.
- Mobile leans toward submit/suggestions over instant full-result reloads (cost, keyboard occlusion).

**2. Suggestion / typeahead model** — what the dropdown contains.
- `IF you can cheaply predict the query` → **query suggestions** (completions): selecting one *fills and searches*. Wire `aria-autocomplete="list"`.
- `IF you can cheaply preview results` → **result previews** (jump-to): selecting one *navigates to the item*. Make the two visually and behaviourally distinct so the user knows whether Enter searches or navigates.
- `IF both are valuable (rich apps, docs)` → **federated** dropdown: grouped sections (suggestions, results, maybe actions/people), each labelled.
- `NEVER` use `aria-autocomplete="inline"` (auto-typing into the field) as the only model — it fights the user's typing.
- Keep the list short (≈5–10), keyboard-navigable (↑/↓, Enter, Esc), with a visible active option.

**3. The zero-query state** — what shows before typing. `IF` you have signal → **recent searches** (with a clear/manage control and a privacy mind on shared devices) and/or **popular/suggested** entries; `ELSE` → a helpful placeholder and nothing more. Don't show an empty dropdown.

**4. Scoped vs global search.**
- `IF the product has distinct entities/sections` → offer scope, but default to the **most-likely scope** (often the current section) with a one-tap widen to global.
- The scope affordance lives adjacent to the field (a leading selector or "in: X" chip); echo the active scope in the results header.
- `IF results span entities` → **federate**: group by entity with labelled sections and a "see all in X."

**5. The results surface.**
- `IF results are few and selection is the goal` → inline **dropdown results**.
- `IF results are many, rankable, refinable` → a **full results page** (with filters — the seam to Filtering) reached on submit; the dropdown carries suggestions only.
- `ALWAYS` **highlight the matched substring**, show a **result count**, and signal ranking implicitly by order. Pagination vs infinite scroll of results is the data-pattern's call (reference, don't re-derive) — bias to "load more"/pagination for findability over infinite scroll.

**6. The no-results state** — the state everything hinges on; `NEVER` a dead end.
- `ALWAYS` confirm the query, then **offer a route forward**: spelling/"did you mean," broaden the scope, drop a filter, suggested/popular alternatives, a contact/again affordance.
- Composes View-state orchestration's empty taxonomy; this is its search-specific instance (it is *not* the same as "no data exists" — the data may exist under a different query).

**7. Loading & latency.**
- `IF results refresh in place` → **keep the stale results visible** with a subtle busy indicator rather than flashing a skeleton (avoids layout thrash on fast queries).
- `IF first load / scope change` → skeleton.
- `IF a query is slow (> ~1s)` → a clear in-progress signal; never an indefinite spinner with no fallback.

**8. Search affordance & invocation.**
- `IF search is primary to the product` → a **persistent, visible field** in the shell.
- `IF search is secondary / space is tight (mobile, toolbars)` → an **icon that expands**; ensure it's labelled and keyboard-reachable.
- Offer a **keyboard shortcut** (`/` to focus search; `⌘K`/`Ctrl-K` for a command-palette-style overlay) and show it as a hint in the field.
- Mobile: tapping search may transition to a **full-screen** search view (field + suggestions), with a clear back/cancel.

**9. Query handling.** Typo tolerance / fuzzy matching and synonyms are table stakes for content search; offer **"did you mean"** for likely misspellings. Provide a **clear (×)** control. **Persist the query and scope in the URL** so a search is shareable and survives reload. Store recent searches locally with a clear control.

## Flow & states

The lifecycle as a state machine: **idle / zero-query** (field empty, dropdown shows recent/popular or nothing) → **typing** (debounce timer running; below-min-length stays in zero-query) → **suggesting** (dropdown shows suggestions/result-previews for the current query; one option active) → **searching** (submit or instant fetch in flight; stale results kept or skeleton shown) → **results** (count announced, matches highlighted) | **no-results** (query confirmed, recovery routes offered) | **error** (retry offered — via View-state orchestration). Esc collapses the popup and, on a second press, clears; the active query persists in the field and URL.

## Accessibility orchestration

The a11y the *experience* owns; the field's own combobox basics are inherited.
- **The combobox/listbox contract** — the field is a `combobox` controlling a `listbox` popup of `option`s; `aria-expanded` reflects popup state, `aria-activedescendant` tracks the active option without moving DOM focus (focus stays in the input so typing continues). The pattern's job is wiring this to the suggestion/result model and keeping it correct as content changes.
- **Result-count announcement** — a polite `aria-live` region announces the count ("12 results") on settle, so non-sighted users know the search resolved and how many; debounce the announcement so as-you-type doesn't spam it (the live-region-budget discipline from View-state orchestration).
- **Focus management** — focus stays in the input during suggestion navigation (activedescendant); moving to a full results page moves focus to the results heading; Esc returns predictably.
- **Mobile / full-screen search** — the transition must be announced and focus moved into the field; the cancel/back control is reachable.
- Defer to the Search field component for the input's own label, `role=searchbox`/`combobox`, and clear-button a11y.

## Content & copy

- **Placeholder** states the scope or an example query ("Search invoices," "Search by name or email"), not a generic "Search…" alone where scope is ambiguous; never the only label (a11y). Don't overload it with instructions.
- **No-results copy** confirms the query and points forward: "No results for '*foo*'. Check the spelling, try fewer words, or browse popular topics." Never a bare "No results."
- **Result count** is explicit ("12 results for '*foo*'") and doubles as the live-region text.
- **Suggestion labelling** distinguishes query-suggestions from jump-to-results (an icon or a section label), so Enter's behaviour is predictable.
- **Scope copy** echoes the active scope ("Results in Billing") with a widen affordance.

## Variants & responsive

- **Inline dropdown** (suggestions/quick results) vs **full results page** (ranked, refinable) vs **both** (dropdown suggests, Enter goes to the page).
- **Icon-expand** field for tight spaces; **persistent** field where search is primary.
- **Command palette** (`⌘K`) — the federated, action-launching variant; shares the combobox/listbox machinery and the federated-suggestion model, adds command execution and recent-actions (borders the Command palette pattern).
- **Full-screen mobile** search view on small viewports.

## Anti-patterns

As-you-type firing heavy/remote queries with no debounce (server thrash, janky UI). Out-of-order responses showing stale results. A dead-end "No results" with no route forward. Hiding search behind an icon when search is primary to the task. Clearing the query on blur/focus. Suggestions that don't signal whether they search or navigate. No result count exposed to AT. An indefinite spinner with no slow-search fallback. Flashing a skeleton over results that refresh in milliseconds. `aria-autocomplete="inline"` auto-typing over the user. A scope selector that resets the query. Searching only exact substrings (no typo tolerance) on a content corpus.

## Related patterns & components

- **vs the Search field / Combobox (component)** (see combobox) — the input control (anatomy, clear button, the `combobox`/`searchbox` role) vs the experience around it (this pattern). The field is composed, not re-derived.
- **vs Filtering (pattern)** — search queries an *unknown* ("find me X"); filtering narrows a *known, visible* set ("show only Y"). They frequently combine on a results page (a search query + facets); the seam is that search produces the set, filters refine it.
- **vs View-state orchestration (pattern)** (see patterns/view-state-orchestration) — the results region's loading/empty/error states compose it; the **no-results** state is the search-specific empty instance (the data may exist under another query — distinct from "no data exists").
- **vs Command palette** — search-as-action-launcher (`⌘K`): same combobox/federated machinery, but it executes commands and navigates rather than returning content results. The boundary case this pattern shades into.
- **vs results pagination / infinite scroll** — how the results list pages is the data-pattern's call; referenced, not re-derived.
- **`composes`:** combobox, text-field, empty-state, list, menu, spinner, skeleton, tag.

## Field POV evolution

Three arcs. **Submit → instant**: cheap client-side and fast hosted search (Algolia and friends) made as-you-type the default for small/fast corpora, while large corpora kept submit + suggestions — the scale-dependent split this brief encodes. **Static autocomplete → federated**: the dropdown moved from a flat list of query completions to grouped, multi-source results (suggestions + results + people + actions), the Algolia Autocomplete model. And **the rise of `⌘K`**: the command palette turned search into the primary navigation and action surface of pro apps (Linear, Raycast, DocSearch), normalising keyboard-first search. Typo tolerance and synonyms moved from premium to table stakes over the same period.

## Reference instantiations

Go look at: the **WAI-ARIA APG combobox pattern** (the listbox/activedescendant contract); **Algolia Autocomplete + InstantSearch** (the federated suggestion/result model and the debounce/race handling); **IBM Carbon** search (field + pattern); **Material** docked/full-screen search; **GOV.UK** search and no-results; the **⌘K palettes** (Linear, Algolia DocSearch, Raycast) for the action-launcher variant; **Baymard** and **NN/g** for the e-commerce search and zero-results research.

## Sources cited

- WAI-ARIA Authoring Practices Guide — combobox pattern, `aria-autocomplete`, listbox/option roles, `aria-activedescendant`, `role=searchbox` (current; *verify*).
- Nielsen Norman Group — search UX, autocomplete suggestions, zero/low-results (*verify articles/dates*).
- Baymard Institute — e-commerce search, autocomplete, no-results handling (*verify specific figures before quoting*).
- Algolia — Autocomplete library and InstantSearch (the federated model; debounce/race guidance) (*verify version*).
- IBM Carbon — Search component + pattern (v11, 2025; *verify*); Shopify Polaris, Material 3, Atlassian, Adobe Spectrum, Microsoft Fluent — search patterns where documented (*spotty; flag where absent*).
- GOV.UK Design System — search and no-results guidance (2025; *verify*).
- The ⌘K / command-palette lineage — Linear, Algolia DocSearch, Raycast (*secondary; product observation*).

`notes.unverified`: the debounce timing band (≈150–300ms) and minimum-query-length (1–2 chars) are widely-used heuristics, not sourced constants — flag as such. Which design systems ship a *named* search experience pattern vs only a Search component is spotty (Carbon is the clearest); verify before asserting convergence. Specific Baymard/NN-g figures and current version strings flagged.

## Agent-consumable schema

```yaml
identity:
  id: search-orchestration
  name: Search orchestration
  aliases: [search experience, typeahead, autocomplete search, instant search]
  tier: composition
  goal: navigate
  status: draft
problem: >
  The search experience around the Search field — zero-query state, typeahead
  suggestions, scope, the results surface, and (above all) the no-results
  state, plus the instant-vs-submit decision and its debounce/race contract.
  Applies when users query an unknown; not for narrowing a known set
  (Filtering) or select-from-list (Combobox).
composition:
  requires: [combobox, text-field, empty-state, list, menu, spinner, skeleton, tag]
  delta: instant-vs-submit + debounce, suggestion model, zero-query + no-results content, scope model, live result announcement
decision_rules:
  instant_vs_submit:
    - { if: "corpus small/client-side (<= ~few thousand) or latency <100ms", use: "instant as-you-type" }
    - { if: "query expensive, corpus large/remote, or results navigate/reload", use: "submit on Enter + as-you-type suggestions only" }
    - { if: "instant", use: "debounce ~150-300ms AND ignore out-of-order responses" }
    - { if: "query below min length (~1-2 chars)", use: "do not fire; show zero-query state" }
  suggestion_model:
    - { if: "can cheaply predict query", use: "query suggestions (fill+search); aria-autocomplete=list" }
    - { if: "can cheaply preview results", use: "result previews (jump-to/navigate); visually distinct from suggestions" }
    - { if: "both valuable", use: "federated grouped dropdown (labelled sections)" }
    - { if: "tempted by aria-autocomplete=inline as the only model", use: "do not (it fights typing)" }
  zero_query:
    - { if: "signal available", use: "recent searches (clearable, privacy-aware) and/or popular/suggested" }
    - { if: "no signal", use: "helpful placeholder; no empty dropdown" }
  scope:
    - { if: "distinct entities/sections exist", use: "offer scope, default to most-likely (current section), one-tap widen to global" }
    - { if: "results span entities", use: "federate: labelled groups + see-all-in-X" }
  results_surface:
    - { if: "few results, selection is the goal", use: "inline dropdown results" }
    - { if: "many, rankable, refinable", use: "full results page (+ filters); dropdown = suggestions only" }
    - { if: "always", use: "highlight match, show result count, signal ranking by order" }
  no_results:
    - { if: "zero results", use: "confirm query + offer route forward (did-you-mean, broaden, drop filter, popular); never a dead end" }
  loading:
    - { if: "results refresh in place", use: "keep stale results + subtle busy indicator (no skeleton flash)" }
    - { if: "first load / scope change", use: "skeleton" }
    - { if: "slow (>~1s)", use: "clear in-progress signal; never indefinite spinner" }
  invocation:
    - { if: "search primary to product", use: "persistent visible field" }
    - { if: "secondary / tight space", use: "labelled icon-expand" }
    - { if: "always", use: "offer / and cmd-K shortcuts, shown as a hint" }
    - { if: "mobile", use: "full-screen search view with cancel/back" }
  query_handling:
    - { if: "content corpus", use: "typo tolerance + synonyms + did-you-mean as table stakes" }
    - { if: "always", use: "clear (x) control; persist query+scope in URL; local recent-search store" }
flow: [idle-zero-query, typing-debounce, suggesting, searching, results, no-results, error]
accessibility_orchestration: >
  combobox controls a listbox of options; aria-expanded reflects popup;
  aria-activedescendant tracks the active option while focus stays in the
  input; polite aria-live announces the result count on settle (debounced for
  the live-region budget); focus moves to the results heading on a full-page
  search and returns predictably on Esc; mobile full-screen transition is
  announced and moves focus into the field. (Field's own label/role/clear
  a11y deferred to the component.)
content: >
  Placeholder states scope/example (not the only label, not overloaded);
  no-results copy confirms the query + points forward; explicit result count
  doubles as live-region text; suggestions signal search-vs-navigate; scope
  copy echoes the active scope with a widen affordance.
variants: [inline-dropdown, full-results-page, both, icon-expand, persistent-field, command-palette, full-screen-mobile]
anti_patterns:
  - as-you-type heavy/remote queries with no debounce
  - out-of-order responses showing stale results
  - dead-end no-results with no route forward
  - hiding search behind an icon when it is primary
  - clearing the query on blur/focus
  - suggestions that do not signal search-vs-navigate
  - no result count exposed to AT
  - indefinite spinner with no slow-search fallback
  - skeleton flash over millisecond refreshes
  - aria-autocomplete=inline auto-typing over the user
  - scope selector that resets the query
  - exact-substring-only matching on a content corpus
reference_instantiations:
  - { system: "WAI-ARIA APG", look_at: "combobox pattern: listbox + activedescendant" }
  - { system: "Algolia", look_at: "Autocomplete + InstantSearch (federated model, debounce/race)" }
  - { system: "IBM Carbon", look_at: "Search component + pattern" }
  - { system: "Material 3", look_at: "docked / full-screen search" }
  - { system: "Command palettes", look_at: "Linear / Algolia DocSearch / Raycast (cmd-K)" }
relations:
  composes: [combobox, text-field, empty-state, list, menu, spinner, skeleton, tag]
  relates-to: [filtering, view-state-orchestration, command-palette, forms-as-a-system]
  boundary: >
    The Search field/Combobox component is the input; this pattern is the
    experience around it. Filtering narrows a known set; search queries an
    unknown; they combine on a results page (search produces the set, filters
    refine). View-state orchestration owns the results' loading/empty/error;
    the no-results state is the search-specific empty instance. Command palette
    is search-as-action-launcher (shares the machinery, executes commands).
    Results pagination/infinite-scroll referenced, not re-derived.
notes:
  contested: "instant vs submit at mid-size corpora; dropdown-results vs page-results; how aggressive typo tolerance should be"
  unverified: "debounce ~150-300ms and min-length ~1-2 chars are heuristics not constants; which design systems ship a NAMED search experience pattern (Carbon clearest); Baymard/NN-g figures; version strings"
```

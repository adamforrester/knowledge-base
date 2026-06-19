# Search orchestration — external-agent pass

*Second independent pass for the Search orchestration pattern brief. Captured as the dual-agent audit record. Synthesised with `claude.md` into `patterns/search-orchestration.md`. The `[cite: N]` markers and percentage figures are the external pass's own; flagged for verification in the synthesis.*

---

## Search orchestration

Search orchestration defines the end-to-end interactive experience surrounding a search input field. It owns the logic that the standalone combobox component cannot: network race-condition mitigation, debouncing logic, federated result synthesis, zero-query states, no-results remediation, and the precise timing of assistive technology announcements. This pattern explicitly establishes the boundary between the basic HTML control and the complex, stateful experience of retrieving, ranking, and rendering data before the user commits to a full page reload.

### Problem & context

Search frequently serves as the primary navigation fallback, and for high-intent users it's the first and most critical interaction. Quantitative impact (Baymard/NN-g, *figures to verify*): 53% of users cite search problems as their primary navigation frustration; 76% report an unsuccessful search directly results in a lost sale/abandoned session; users select suggested queries in only 23% of instances (NN/g — enriched suggestions are often ignored or mistaken for ads); lack of typo tolerance triggers abandonment in 69% of instances; 37% of sites fail to persist the query after submission. Component libraries provide only primitives (textbox, popover, list items); the gap to an enterprise-grade experience is *orchestration*. Without it: race conditions overwrite fresh data, autocomplete breaks on typos, and AT is overwhelmed by DOM mutations. The literature diverges (NN/g cautious on enriched suggestions; Baymard insistent on typo tolerance/persistence/no-dead-ends; enterprise platforms pushing aggressive instant federated search); this pattern bridges them into a defensible default.

### Composition

A macro-level composition pattern; assembles, does not re-derive. **Search field / Combobox** — primary input; manages its own activedescendant, keyboard capture, baseline ARIA (aria-expanded); orchestration treats it as a black box, listening to change events and overriding ARIA refs by data state. **Popover / Flyout** — the transient overlay (positioning, z-index — crucial in nested DOM/modals, dimensional constraints). **List** — renders suggestions/entities. **Empty State** (zero-results), **Loading Indicators** (inline spinner / skeleton), **Clear Button**.

### Decision rules

**1. Instant vs submit-on-enter.** IF backend latency consistently <100ms AND index supports partial-word fuzzy → instant (update on keystrokes). IF dataset massive / deep comparative queries / latency >300ms → submit-on-enter, route to a dedicated results page. IF instant → strict network debounce (200–250ms desktop, 300–500ms mobile). IF multiple async requests from rapid typing → AbortController (cancellation token) to terminate previous requests, preventing stale out-of-order responses overwriting fresh data ("java" then "javascript": if the older resolves last it corrupts the UI).

**2. Suggestion / typeahead model.** IF homogeneous document/article index → query suggestions (completions); selecting executes a search; `aria-autocomplete="list"`. IF discrete actionable entities (profiles, tickets, products) → result previews (jump-to); selecting navigates to the entity, bypassing the results page. IF multiple content domains → federated (multi-column/grouped: 3–5 query suggestions + 3–5 visual previews). Visual differentiation mandatory: the typed portion standard weight, the suggested completion bolded. Cap suggestions 4–9 to avoid internal scrollbars (>10 overwhelms).

**3. Zero-query state.** IF authenticated AND privacy permits → recent searches (last 3–5 from localStorage/profile; explicit clear affordance). IF anonymous OR no history → trending/popular (3–5). IF ⌘K palette → global navigation nodes/actions/recent files. localStorage: parse JSON safely, handle 5MiB quota, store no PII/tokens.

**4. Scoped vs global.** IF deeply siloed verticals (Jira projects, repos) → scope selector on the leading edge of the input. IF a query is a 1:1 exact match with a top-level category ("Men's Shirts") → **autodirect** (intercept submission, navigate to the category page rather than a generic results page) — failing to do so forces users through mixed-relevance results when a curated page exists.

**5. Results surface.** IF rapid context-preserving discovery → inline dropdown popover (limited, closes on outside click). IF deep comparative analysis / faceted filtering / sorting → full results page (hand off to layout + pagination patterns).

**6. No-results state — the single most critical failure path.** IF literal query returns zero → fuzzy matching / typo tolerance (Levenshtein, "Did you mean…?"). IF typo tolerance yields nothing → an intelligent no-results state; never a dead end; broaden scope, suggest removing filters, offer curated starting points.

**7. Loading & latency.** IF a request is initiated → a slight artificial delay (~50ms) before showing a spinner (prevents flicker on fast connections). IF the user types to update an already-visible list → keep-stale (maintain old results, optionally dimmed) rather than clearing to empty.

**8. Affordance & invocation.** IF search is primary (large catalogs, docs) → persistent open field (don't hide behind an icon). IF real estate constrained (mobile, dense headers) → icon-to-expand (immediate focus on interaction). IF developer/power-user → command palette (⌘K) global shortcut.

**9. Query handling.** IF a user lands on a results page → query persistence (the box retains the exact typed string; don't clear on submission) — users iterate ("sofa" → "blue sofa").

### Flow & states

Idle (placeholder, optional shortcut hint; no network) → Zero-Query/Focused (dropdown opens immediately, recent/trending; parse localStorage / fetch trending) → Typing/Debounce (clear-X appears, existing results may dim; debounce timer, no call yet) → Fetching (spinner/skeleton; AbortController cancels pending; new request) → Results-Completions (autocomplete strings, typed chars bolded) | Results-Entities (cards/rows) | No-Results (empty state, corrections/broaden; fire analytics event — a critical conversion metric) | Submitted (navigate viewport to results page; string to URL `?q=`).

### Accessibility orchestration

Principle: the visual experience of suggestions appearing/updating must translate to an auditory one *without overwhelming*. The combobox pattern owns baseline ARIA; orchestration owns timing, focus, and the announcement budget.

**Combobox contract:** input `role="combobox"`, toggles `aria-expanded`, defines `aria-controls` → the dropdown's `role="listbox"` id. On arrow navigation, **DOM focus never leaves the input**; orchestration updates `aria-activedescendant` to the highlighted option's id so the user keeps typing while the SR announces the highlighted option.

**The announcement budget & aria-live:** announcing every keystroke is auditory chaos. Use a dedicated **visually-hidden live region** (`aria-live="polite"`, `role="status"`) independent of the visual dropdown. Budget: on focus/zero-query → an instructional cue via `aria-describedby` ("Search available. Type to filter suggestions."); on results → announce the **aggregate count** + navigation instruction ("7 suggestions found, use up and down arrows to review."), not the items; on no-results → "No results found for [query]." **Critical bug to avoid:** never put `aria-live` directly on the listbox container while using `aria-activedescendant` — it causes severe double-speaking in VoiceOver (it reads the whole list while also announcing the active descendant).

**Autocomplete semantics:** `aria-autocomplete="list"` (a distinct list below the input) vs `aria-autocomplete="both"` (list + inline injection of the top predicted value into the field) — `both` needs complex selection-range management and is generally discouraged unless heavily optimised.

### Content & copy

Ruthless minimalism. Placeholder: action verbs, name the scope ("Search products…", "Search documentation…"), never generic "Type here." Clear affordance: `aria-label="Clear search input"`. Recent searches: brief group heading. No-results header: empathetic, repeat the exact query ("No results found for 'xyzz'."). No-results body: actionable, no blame ("Check your spelling or try broader terms."). Never rely on placeholder as the accessible name — always a persistent (optionally visually-hidden) `<label>`.

### Variants & responsive

**Command palette (⌘K):** shifts from content discovery to action execution; subsequence fuzzy matching ("dm" → "Dark Mode"); strict focus trap (keyboard never escapes until action/Escape); monochrome surfaces, distinct groups (commands/recent/settings). **Mobile full-screen:** inline dropdowns collide with the software keyboard; intercept the tap and transition to a full-screen modal/route, auto-focus the input; provide an explicit "Search"/"Submit" button (relying on the keyboard return key causes friction).

### Anti-patterns

The Orphaned Promise (race conditions without AbortController). Query Amnesia (clearing the field on submit). The Dead-End No-Results (0 results, no paths). Over-rendering suggestions (>10, scroll-within-scroll). Stealing the Enter key (if the user hits Enter before suggestions load, abort the suggestion fetch and submit the typed string as a global search — don't block or run a default action).

### Related patterns & components

vs Search Field/Combobox (component): raw HTML/ARIA material vs the blueprint connecting it to networks/state/debounce. vs Filtering: search queries an unknown via free text; filtering narrows a known set via structured facets; intersect in faceted search (search funnels, filters refine). vs View-State Orchestration: search relies on it for fetch/error/empty; no-results is a specialised Empty State. vs Command Palette: a keyboard-first action-execution variant. vs Pagination/Infinite Scroll: on the results page, orchestration hands off.

### Field POV evolution

Phase 1 synchronous form submit (1990s–2000s). Phase 2 AJAX autocomplete (2010s) — race conditions, jank, silent DOM mutations; NN/g flagged early implementations as distracting. Phase 3 federated & instant (2015+, Algolia) — the dropdown became a mini-app with rich previews. Phase 4 the action launcher/⌘K (2020+, VS Code/Linear/Raycast) — search became command execution; subsequence matching + <50ms latency became table stakes.

### Reference instantiations

W3C APG Combobox (`aria-autocomplete="list"`) — the accessible baseline. Algolia Autocomplete — federated, debounce, cancellation. Raycast/Linear (⌘K) — command palettes, subsequence fuzzy. IBM Carbon — visual variants (default vs fluid) + labelling.

### Sources cited (external pass)

W3C WAI-ARIA APG Combobox pattern + editable-combobox-with-list examples (2026); IBM Carbon Search component/pattern; NN/g site-search suggestions / enriched suggestions (2026); Baymard e-commerce search UX, autocomplete spelling, category scopes, query persistence, B2B/mobile (2026); Atlassian, Adobe Spectrum, Microsoft Fluent SearchBox, GOV.UK search; JS AbortController / race-condition guides; Algolia Autocomplete / federated; Raycast DESIGN.md / subsequence matching; Shopify Polaris autocomplete/portal z-index; MDN/ARIA live-region + aria-autocomplete; localStorage capacity/privacy. (`[cite: N]` markers retained in the practitioner's source notes; percentages and version strings to verify.)

### Agent-consumable schema (external pass)

```yaml
id: search-orchestration
name: Search Orchestration
aliases: [autocomplete, typeahead, instant-search, command-palette, omnibox]
tier: composition
goal: navigate
status: published
problem: >
  Providing real-time query suggestions and results while mitigating asynchronous
  network race conditions, managing DOM focus, and communicating dynamic visual changes
  to assistive technologies without overwhelming the user.
composition:
  requires: [search-field (combobox), popover, list (options), empty-state, loading-indicator]
decision_rules:
  - { if: "latency < 100ms AND fuzzy-matching supported", use: "instant-search" }
  - { if: "typing triggers API", use: "AbortController to prevent race conditions" }
  - { if: "dataset encompasses multiple domains", use: "federated search with categorized jump-to results" }
  - { if: "no exact matches", use: "intelligent typo tolerance and scope broadening; never a dead end" }
  - { if: "user lands on results page", use: "persist the search query string in the input field" }
flow:
  - { state: "Zero-Query", action: "Renders Recent/Popular" }
  - { state: "Typing", action: "Debounce initiated" }
  - { state: "Fetching", action: "Abort previous requests, show spinner" }
  - { state: "Results", action: "Render list, bold exact matches, update aria-live budget" }
accessibility_orchestration:
  roles: [combobox, listbox, option]
  focus: "DOM focus remains on input, uses aria-activedescendant to track highlighted option"
  live_region: "aria-live='polite', visually hidden, announces aggregate counts, strictly avoids per-keystroke spam"
content:
  placeholder: "Action-oriented verbs, explicitly indicates scope boundaries"
  clear_button: "Requires distinct aria-label for destructive action"
variants: [inline-dropdown, full-results-page, mobile-full-screen, command-palette (modal focus trap)]
anti_patterns:
  - "Orphaned Promises (Race conditions without AbortController)"
  - "Query Amnesia (Clearing field on submit)"
  - "Dead-end Zero Results"
  - "Over-announcing to screen readers"
reference_instantiations: [W3C APG Combobox, Algolia Autocomplete, Raycast (Command Palette), IBM Carbon]
relations:
  composes: [combobox, list, popover, empty-state]
  boundary: [filtering, pagination]
notes:
  unverified: []
  contested: "Instant search vs Submit-on-enter depends heavily on query complexity and baseline network latency."
```

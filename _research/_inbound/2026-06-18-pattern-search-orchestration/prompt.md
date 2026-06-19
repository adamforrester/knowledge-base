You are advising a senior design systems practitioner at a digital agency
who maintains a personal knowledge base of design-systems field-truth. The
knowledge base has a ~45-component catalogue and a PATTERNS layer above it
(tiers: composition / flow / layout-and-shell; each pattern carries a
GOV.UK-style `goal` facet). Three pattern briefs are done — Forms-as-a-system,
View-state orchestration, and Data-collection recipes.

This brief: **Search orchestration**. Tier: `composition`. Goal: `navigate`.

The Search *field* is the component (the input — a text input or combobox,
already briefed). **Search orchestration is the pattern**: the whole search
EXPERIENCE around that field — the zero-query state, typeahead/suggestions,
scoped search, the results surface, the no-results state, and the instant-vs-
submit decision. The single most important boundary: this brief does NOT
re-derive the Search field/Combobox control (its anatomy, its ARIA basics) or
the Filtering pattern (narrowing a known set). It owns the orchestration the
field cannot: when results appear, what suggestions are, how the results
surface behaves, and how the whole thing is announced. Assume the Search
field, Combobox, Empty State, and List components are briefed; cite the
boundary, don't repeat them.

This is field-truth synthesis for someone who has shipped search many times.
Explain the non-obvious — where leading systems and the search-UX literature
genuinely disagree, and the defensible default. Be opinionated and declarative.

=== WHAT TO SURVEY (the field) ===

Cite each with a version date; note the verification path for current claims.
- WAI-ARIA Authoring Practices — the combobox pattern (`aria-autocomplete`
  list/both/inline), the listbox/option roles, `role=searchbox`, and the
  as-you-type announcement contract. The accessibility spine.
- Search-UX literature — Nielsen Norman Group (search UX, autocomplete,
  zero-results), Baymard Institute (e-commerce search, autocomplete,
  no-results) — the quantitative corpus.
- Search platforms — Algolia (InstantSearch, the Autocomplete library, the
  "federated/multi-source" model, query suggestions vs results), Elastic /
  typesense patterns, the debounce/race-condition reality.
- Design systems — IBM Carbon (Search component + pattern), Shopify Polaris,
  Material (search, the docked/full-screen search), Atlassian, Adobe Spectrum,
  Microsoft Fluent, GOV.UK (search). Where each draws the field-vs-experience
  line.
- The command-palette lineage (⌘K — Linear, Algolia DocSearch, Raycast) as
  the boundary case: search-as-action-launcher.

=== WHAT TO RESOLVE (decision rules are the deliverable) ===

Make rules machine-resolvable (`IF condition → USE resolution`) wherever a
real threshold exists. Resolve at least:

1. **Instant (as-you-type) vs submit-on-enter** — the central fork. When does
   search update live vs wait for Enter? The deciding axes (latency, query
   cost, result-set size, predictability of intent, mobile). The debounce
   contract (timing, minimum query length). Race conditions / out-of-order
   responses.
2. **Suggestions / typeahead model** — what appears in the dropdown: query
   suggestions (completions) vs result previews (jump-to) vs both
   (federated). When each; how many; how the keyboard moves through them;
   the `aria-autocomplete` value that matches; whether selecting a suggestion
   searches or navigates.
3. **The zero-query state** — what the dropdown/page shows BEFORE typing:
   nothing, recent searches, popular/suggested, scoped entry points. When to
   show history and the privacy of it.
4. **Scoped vs global search** — searching within a section vs everything;
   the scope selector (where it lives, the "search in X" affordance); the
   federated/multi-entity results model.
5. **The results surface** — inline dropdown results vs a full results page
   vs both; match highlighting; result count; ranking/relevance signalling;
   pagination vs infinite scroll of results (reference the boundary to those
   patterns). 
6. **The no-results state** — the most important state. What it must do
   (suggest spelling, broaden, alternatives, never a dead end); the
   relationship to View-state orchestration's empty-state taxonomy.
7. **Loading & latency** — the results loading state (skeleton vs spinner vs
   keep-stale), perceived performance, the slow-search contract.
8. **Search affordance & invocation** — a persistent open field vs an icon
   that expands; the keyboard shortcut (`/`, `⌘K`); placement in the app
   shell; the mobile full-screen search transition.
9. **Query handling** — typo tolerance / fuzzy / did-you-mean; synonyms;
   clearing the query; URL/state persistence of the query and scope; the
   recent-search store.

=== THE BOUNDARIES TO HOLD (state in a Related section) ===

- **vs the Search field / Combobox (component)** — the input control vs the
  experience around it.
- **vs Filtering (pattern)** — search queries an unknown; filters narrow a
  known set; they frequently combine (search + facets) — name the seam.
- **vs View-state orchestration (pattern)** — the results' loading/empty/error
  states compose it; the no-results state is the search-specific empty case.
- **vs Command palette** — search-as-action-launcher (⌘K) as the boundary
  case; what's shared, what's different.
- **vs results pagination / infinite scroll** — reference, don't re-derive.

=== OUTPUT — follow this pattern-brief spine ===

Structured markdown. ALWAYS sections appear; SCALES appear when they carry
weight. Order = reading order.
1. **Frontmatter** — YAML: type: pattern-brief, title, description, tags,
   tier: composition, goal: navigate, status, timestamp.
2. **`# Search orchestration` H1 + a one-paragraph blockquote** framing the
   problem and the boundary (the experience around the field).
3. **Problem & context** — the recurring problem; when it applies; why
   systems/the literature diverge.
4. **Composition** — the components it assembles as typed references (Search
   field/Combobox, Empty State, List, Spinner/Skeleton…) and the relationship
   to the field. Don't re-derive them.
5. **Decision rules** — the forks above (1–9) as machine-resolvable rules.
6. **Flow & states** (SCALES — carries weight here) — the lifecycle:
   idle/zero-query → typing (debounce) → suggesting → results → no-results /
   error; the state machine.
7. **Accessibility orchestration** — the a11y the experience owns: the
   combobox/listbox roles, the `aria-live` result-count announcement, focus
   management between input and results/suggestions, the as-you-type
   announcement budget, mobile. (Defer the field's own ARIA basics to the
   component.)
8. **Content & copy** (SCALES) — the placeholder (and why not to overload
   it), the no-results copy, result counts, suggestion labelling, the
   scope affordance copy.
9. **Variants & responsive** (SCALES) — inline-dropdown vs full-page vs
   full-screen-mobile; the icon-expand variant; the command-palette variant.
10. **Anti-patterns** — the recurring traps (search-as-you-type with heavy
    queries, no debounce, dead-end no-results, hiding search behind an icon
    without need, clearing the query on focus, suggestions that don't say
    whether they search or navigate, no result count for AT, infinite spinner).
11. **Related patterns & components** — the five boundaries above, typed.
12. **Field POV evolution** (SCALES) — the shifts (submit → instant; static
    autocomplete → federated query-suggestions+results; the rise of ⌘K;
    typo-tolerance as table stakes).
13. **Reference instantiations** (SCALES) — where to look (Algolia
    Autocomplete, the ARIA combobox pattern, Carbon search, ⌘K palettes).
14. **Sources cited** — with version dates; flag unsourced claims as
    unverified rather than inventing citations.
15. **Agent-consumable schema** — a fenced YAML block: identity (id, name,
    aliases, tier, goal, status), problem, composition (requires: [typed
    component ids]), decision_rules (as `{ if, use }`), flow,
    accessibility_orchestration, content, variants, anti_patterns,
    reference_instantiations, relations (composes / relates-to / boundary),
    notes (contested / unverified).

Synthesize; give frameworks where context (data size, latency, intent)
decides, defaults where the field has genuinely converged. Date current-state
claims. Flag what you can't source.

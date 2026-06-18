# Pattern-library structure — field-truth study (Claude pass)

*A meta study validating the patterns-layer scaffolding (taxonomy + spine + list) before authoring. Written to correct the scaffolding where it's wrong, not ratify it.*

## 1. Framing — why the field disagrees on what a "pattern" is
There is no settled definition of a UI "pattern," and the leading systems slice the tier differently because they are answering different questions. Two lineages collide:
- **The problem/task lineage** (Christopher Alexander's *A Pattern Language*, 1977 → Jenifer Tidwell's *Designing Interfaces*, 2005/2011/2020 → UI-Patterns.com): a pattern is a **named solution to a recurring problem in a context**, organized by *what the user is trying to do* (get around, enter data, show complex data, do things). Task-led.
- **The design-system lineage** (Carbon, Polaris, Material): a pattern is **whatever isn't a component or a token** — the leftover bucket for compositions, states, and layouts a single component can't own. Structure-led, and inconsistent system to system.

The practical consequence: **GOV.UK organizes patterns by task** ("Ask users for…", "Help users to…", "Pages"), while **Carbon organizes by structural kind** ("Dialog", "Empty states", "Loading", "Notifications", "Forms"). Neither is wrong; they optimize for different lookups. A field-truth KB has to pick a *primary* axis and offer the other as a *facet*. That tension is the central finding of this study, and it's the thing the practitioner's purely-structural four-tier taxonomy under-weights.

## 2. The survey — how leading systems structure their pattern libraries

| System (version) | Top-level cut | What lives in the "patterns" tier | Axis |
|---|---|---|---|
| **GOV.UK Design System** (v5, 2025) | Styles / Components / **Patterns** | **"Ask users for…"** (addresses, bank details, dates, email, names, NI numbers, passwords, payment-card details, phone numbers), **"Help users to…"** (check answers before submitting, confirm an email/phone, navigate, recover from validation errors, stay safe online), **"Pages"** (confirmation, error, question, start, step-by-step) | **Task / user-goal** |
| **IBM Carbon** (v11, 2025) | Components / **Patterns** / (Elements) | Dialog, Disabled states, **Empty states**, **Forms**, **Loading**, **Notifications**, Status indicators, Themes, **Search**, Fluid components | **Structural kind** (recipes + state conventions) |
| **Shopify Polaris** (2024–25) | Foundations / Content / Components / **Patterns** | **"App settings layout", "Resource index/detail layouts"** (templates), Date picking, Error messages, "Page layouts" | **Layout templates + a few recipes** |
| **Atlassian Design System** (2025) | Foundations / Components / **Patterns** / Content | **Forms, Empty states, Inline edit, Messaging, Page layouts, Premium/upgrade states, Help** | **Mixed (recipes + states + templates)** |
| **Material Design 3** (2024–25) | **Foundations** / Styles / Components | (No big "patterns" bucket) — pattern-ish content under Foundations: **Layout, Navigation (drawer/bar/rail), Adaptive design, Content design** | **Foundations-absorbed** |
| **Adobe Spectrum** (2024) | Foundations / **Patterns** / Components | **Drag and drop, Help, Internationalization, Inline alerts, Status light** | **Cross-cutting recipes** |
| **Microsoft Fluent 2** (2024) | (lighter) Layout + some patterns | Layout, a handful of compositions | **Layout-led** |
| **Ant Design** (v5, 2025) | Components + a thin guidelines layer | Form-validation guidance, some recipes | **Component-absorbed** |
| **Tidwell, *Designing Interfaces*** (3e, 2020) | Chapters by goal | "Getting Around" (nav), "Organizing the Content", "Getting Input from Users", "Doing Things: Actions/Commands", "Showing Complex Data", "Builders & Editors" | **Task / user-goal** |
| **NN/g** | Articles, not a library | Treats patterns as documented best practices per task | **Task** |

**Reading of the survey:** (a) Every mature system has a patterns tier *distinct from components*, so the layer is well-founded. (b) The **content** of the tier is wildly inconsistent — Carbon's "Empty states" is GOV.UK's nonexistent (it's absorbed into pages), Polaris's "patterns" are mostly *layouts*, Material has almost no patterns bucket (folded into Foundations). (c) The **axis** splits cleanly: the design-task references (GOV.UK, Tidwell, NN/g) go **task-based**; the component-library systems (Carbon, Polaris, Atlassian) go **structural-kind-based** and end up with messy, overlapping buckets. (d) Critically, **the practitioner's "state-convention" tier IS attested** — Carbon ships "Disabled states / Empty states / Loading / Notifications" as patterns, and Atlassian ships "Empty states / Premium states." So that tier is not invented. (e) **"page-template" is frequently a separate artifact**, not a pattern — Polaris calls them "layouts," Material puts them in Foundations.

## 3. The pattern-vs-component boundary — as the field draws it
The field's line is fuzzier than the practitioner's clean "thing-with-props vs composition-of-things." Hard cases:
- **Search** — Carbon ships it as a *pattern*; many systems ship a `SearchField` *component*. Both are right: the input is a component, the experience (suggestions + results + empty state) is a pattern. The practitioner's catalogue already has this tension noted.
- **Data table** — a component in most systems, but the *sortable/filterable/paginated/bulk-action data grid experience* is a pattern. The catalogue's Table brief already absorbed much of this.
- **Card** — universally a component, never a pattern, despite being a composition. Why? It has a stable prop/slot surface and ships as one thing. This *confirms* the practitioner's "ships-as-one-importable-thing" test.
- **Empty state** — the catalogue made it a *component*; Carbon/Atlassian make it a *pattern*. This is a genuine disagreement and a flag: the practitioner has Empty State as a component brief, so the patterns layer must not re-brief it — the *pattern* would be "empty/loading/error state orchestration across a view," not the empty-state surface itself.

**Verdict:** the practitioner's boundary (composition + decision-rules + cross-component-orchestration + doesn't-ship-as-one-thing) **holds and is sharper than most systems' implicit line** — the "ships as one importable thing" test is the cleanest discriminator (it correctly keeps Card a component and Forms-as-a-system a pattern). Two refinements: (1) name the **scaffolding blur** explicitly — systems *do* ship an `AppShell`/`<Wizard>`/`<DataGrid>` that packages a pattern as a component; the rule is that the *pattern brief* documents the decisions even when a *component* packages one instantiation. (2) Add the **"already briefed as a component" guard**: where the catalogue made something a component (Empty State, Table, Search-as-SearchField), the pattern is the *orchestration*, not a re-brief.

## 4. The taxonomy — verdict on the four tiers
**The four tiers are defensible but mix two axes and under-serve findability.**

The problem: tiers 1–2 (`cross-component-recipe`, `state-convention`) classify by *kind of solution*; tiers 3–4 (`flow-and-shell`, `page-template`) classify by *scale/scope of solution*. That's not one clean axis, which is why the boundaries feel arbitrary (is a "wizard" a recipe or a flow? is "app shell" a flow or a template?).

Three specific challenges:
- **`state-convention` is half-pattern, half-foundations-guidance.** Carbon validates it as a pattern tier, but the practice already has a numbered-file foundations layer (00–10+) that is the natural home for cross-cutting guidance. The risk is duplication: each control's brief *already* covers its own disabled/read-only/loading behaviour. The state-convention pattern must be the **cross-component synthesis** ("here's how disabled is expressed consistently across *all* controls, and the do/hide/explain decision"), not a re-statement — and it sits uneasily between "pattern" and "foundations doc."
- **`page-template` is arguably a separate artifact.** Polaris ("layouts"), Material (Foundations > Layout), and the practice's own instinct treat full-page skeletons as distinct from compositional patterns. Folding them in as a tier is fine for a single-practitioner KB, but flag them as the *scaffolding* tier (closest to shipping a real layout component).
- **Pure structure under-serves the agent + human lookup "how do I let users do X."** GOV.UK's task-based cut ("Ask users for an address") is far more findable for the KB's eventual MCP-agent consumption than "cross-component-recipe."

**Recommended taxonomy (the hybrid I'd defend):** keep the **four structural tiers as the PRIMARY axis** — because they predict the brief's *shape* (which SCALES sections fire), which is the schema's real engineering value — **but add a task/goal facet** (a `goal:` frontmatter field or tags, GOV.UK-style: "ask-for-data", "help-user-decide", "navigate", "do-an-action", "show-data", "recover-from-error") so patterns are findable by user intent, and add a cross-index in `patterns/index.md`. This captures Carbon's structural cut (which the practitioner already has) *and* GOV.UK's task cut (which the practitioner is missing). One refinement to the tiers themselves: rename to make the axis-mix explicit — e.g. group as **"recipes & conventions"** (kind) and **"flows & templates"** (scope) two-level, or simply accept the four but document that 1–2 are kind and 3–4 are scope.

## 5. The pattern-brief spine — verdict on ALWAYS/SCALES
**The spine is well-matched and only slightly over/under in two places.** Real pattern-library entries (Carbon, Polaris, GOV.UK, Atlassian) converge on: *when to use / problem*, *how it works / anatomy*, *variants*, *do's and don'ts*, *accessibility*, *content/UX writing*, and *code/examples*. The proposed ALWAYS core (problem, composition, decision-rules, a11y-orchestration, anti-patterns, related, schema) maps onto that cleanly, and **"decision rules" as the center of gravity is exactly right for a field-truth KB** (the practice documents *the contested choice and its resolution*, not a how-to — that's the whole differentiator from a vendor pattern library).

Two adjustments:
- **Missing: an "examples / reference instantiations" pointer.** Every real pattern library is example-driven (GOV.UK shows the actual rendered pattern; Carbon shows live code). A text KB can't render, but the spine should have a SCALES "reference instantiations" note (which real systems implement this pattern, with a link) so a reader/agent can ground the decisions. This is lighter than the component briefs' "sources" but distinct — it's "go look at Carbon's Forms pattern," not a citation.
- **"Content & copy" should arguably be ALWAYS, not SCALES, for the task-based patterns.** GOV.UK's patterns are *dominated* by content/UX-writing guidance (the question wording, the error copy). For `cross-component-recipe` and `flow-and-shell` patterns, copy is load-bearing, not optional. Keep it SCALES globally but note it's near-ALWAYS for task/flow patterns.

The agent-consumable schema should differ from the component schema exactly as proposed — `composes` (typed component refs) + `decision_rules` (resolved forks) are the right center, not props. Add the `goal:` facet to the schema for the task-findability above.

## 6. The pattern list — tier-by-tier validation
**The list is a reasonable seed but under-weights data-collection patterns (the GOV.UK "ask users for" family) and misses several first-class modern patterns. A few items are really components or really guidance.**

**`cross-component-recipe` — additions + corrections:**
- **MISSING (high priority): the "Ask users for X" data-collection family** (GOV.UK's core) — address, name, date-of-birth, payment-card, phone, email-with-confirmation. These are the most reused, most field-attested patterns in existence and the list barely touches them. Should be first-class recipes (or a single "data-collection recipes" pattern with sub-cases).
- **MISSING: Inline edit / in-context editing** (Atlassian ships it as a pattern) — edit-in-place vs edit-in-form.
- **MISSING: Bulk actions / multi-select** (table/list selection → a bulk-action bar) — a core data-management pattern.
- **MISSING: Command palette** (the modern ⌘K staple).
- **"Common actions (action priority & overflow)"** — partly a pattern, but the *Toolbar* it implies is really a **component** the catalogue is missing. Split: Toolbar → component; action-priority/overflow → recipe.
- **"Overflow content"** — borderline; truncation is component-level (Text/Tooltip already cover it). Keep only as a thin "show more / progressive disclosure" recipe or fold into a progressive-disclosure pattern.

**`state-convention` — mostly sound, watch duplication:**
- Disabled, Read-only, Loading orchestration, Notifications orchestration are all attested. **Risk:** Disabled/Read-only overlap heavily with each control's brief — these must be the *cross-component synthesis*, not re-statements (the do/hide/explain decision, the never-disable-submit rule already drawn in Form). **Consider** whether Disabled/Read-only belong in a numbered foundations file instead, with only Loading-orchestration and Notifications-orchestration as true patterns.
- **MISSING: Selection** (the cross-component selected-state convention — checkbox/row/card/toggle).

**`flow-and-shell` — sound; one addition:**
- App shell, Auth, Wizard, Destructive confirmation, Save/unsaved-changes are all well-attested. **MISSING: Onboarding/first-run flow** (currently under page-template — it's more a flow than a template; see below). **MISSING: Sharing & permissions** flow (common in SaaS).

**`page-template` — sound; recategorize one:**
- Master-detail, dashboard, settings, error pages are textbook templates. **Onboarding** is better a flow than a template (move to flow-and-shell, or accept it spans both). **MISSING: the index/list page** (Polaris's "Resource index layout" — the most common app page) and the **detail/record page**. **MISSING: feed/timeline**.

**Really-a-component (not patterns):** Toolbar (build the component); the "Search" *input* (already SearchField-adjacent in the catalogue — the *pattern* is the search experience).
**Really-guidance (numbered foundations file, not patterns):** Theming/dark-mode, internationalization-as-a-whole (the catalogue has 13-i18n), responsive/adaptive layout philosophy — these are cross-cutting POV, not compositions. (Specific adaptive *patterns* like master-detail-stacks-on-mobile live in the template's responsive section.)

**Prioritized validated seed (the order I'd author in):**
1. **Forms-as-a-system** (recipe) — the trigger; exercises composition + decision + flow.
2. **Data-collection recipes / "Ask users for X"** (recipe) — highest field-attestation, GOV.UK gold standard.
3. **Filtering** (recipe) — ubiquitous, composition-heavy.
4. **App shell / global header** (shell) — the substrate every template sits in.
5. **Destructive confirmation** (flow) — small, sharp, high-reuse, sets the flow-tier shape.
6. **Loading & skeleton orchestration** (state-convention) — exercises the cross-component-synthesis test.
7. **Master-detail** (template) — the first template, sets that tier's shape.
…then Search, Wizard, Auth, Notifications-orchestration, Dashboard, Settings, Bulk actions, Inline edit, Empty/error-state orchestration, Save/unsaved-changes, Command palette.

## 7. The agent-consumability angle
The KB's MCP-server intent **reinforces the hybrid taxonomy and the typed schema**:
- **Machine-resolvable decision rules** — the `decision_rules` block should be structured (`{ choice, resolution, depends-on }`) so an agent can answer "should I use a modal or a drawer here?" not just read prose. This is a stronger reason for the decision-rules-as-center-of-gravity than human docs would give.
- **Typed `composes` references** — an agent assembling a UI needs the pattern to name its component dependencies as resolvable IDs (`form`, `table`) so it can pull the component briefs' schemas. The `composes: [ids]` field is exactly right.
- **The task/goal facet matters more for agents than humans** — an agent prompts "build a flow to collect a shipping address"; a `goal: ask-for-data` facet + the data-collection recipe is the resolvable answer. A purely structural taxonomy makes that lookup harder. **This is the strongest argument for adding the task facet.**

## 8. Net recommendations (what to change before authoring)
1. **Keep the four tiers as the primary axis** (they predict the spine shape — real engineering value) but **add a `goal:` task facet** (GOV.UK-style) to the frontmatter/schema and a cross-index in `patterns/index.md`. Document that tiers 1–2 are "kind," 3–4 are "scope."
2. **Sharpen the boundary** with two named rules: the *scaffolding blur* (a pattern can be packaged as a component; the brief documents the decisions regardless) and the *already-briefed-as-component guard* (Empty State/Table/Search → the pattern is the orchestration, not a re-brief).
3. **Spine: add a SCALES "reference instantiations"** pointer (which systems ship this, go look) and note **content/copy is near-ALWAYS for task/flow patterns.**
4. **List: add the data-collection "Ask users for X" family** (highest priority gap), Inline edit, Bulk actions/Selection, Command palette, index/detail page templates; **move Onboarding** to flow; **split "Common actions"** into a Toolbar *component* + an action-priority recipe; **reconsider Disabled/Read-only** as foundations-guidance vs patterns (keep Loading/Notifications orchestration as patterns).
5. **Author in the priority order** above — Forms-as-a-system first (validates the spine), then the data-collection family (validates the task facet + the recipe tier).

These are refinements, not a teardown: the layer is well-founded, the boundary test is sound, and the spine is close. The two real corrections are the **task facet** (the field's task-based lineage that pure structure misses) and the **data-collection recipe family** (the list's biggest gap).

## Sources cited
*(External-pass version dates to be reconciled; flag unverified.)*
- **GOV.UK Design System** — Patterns ("Ask users for…", "Help users to…", "Pages"); v5, 2025 — the task-based gold standard.
- **IBM Carbon** — Patterns (Dialog, Disabled/Empty/Loading states, Forms, Notifications, Search); v11, 2025.
- **Shopify Polaris** — Patterns + layouts (app-settings, resource index/detail); 2024–25.
- **Atlassian Design System** — Patterns (Forms, Empty states, Inline edit, Messaging, Page layouts, Premium states); 2025.
- **Material Design 3** — Foundations (Layout, Navigation, Adaptive, Content design); 2024–25 (no distinct patterns bucket).
- **Adobe Spectrum** — Patterns (Drag and drop, Help, Internationalization, Inline alerts); 2024.
- **Microsoft Fluent 2** — layout + patterns; 2024.
- **Jenifer Tidwell, *Designing Interfaces*** (3rd ed., 2020) — the canonical task-organized UI pattern catalogue.
- **Christopher Alexander, *A Pattern Language*** (1977) — the pattern-language origin.
- **UI-Patterns.com** + **Nielsen Norman Group** — problem/task-organized pattern references.

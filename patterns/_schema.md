---
okf_version: "0.1"
type: schema
title: Pattern Brief Schema
description: The flexible spine for a pattern brief — the patterns-layer counterpart to the component catalogue's locked §15 schema. A pattern is an opinionated, goal-contextual composition of components solving a problem, so the spine encodes the PROBLEM, the COMPOSITION (typed references into the component catalogue), and the DECISION RULES (machine-resolvable where they can be) — not a thing's props. Unlike the component spine (keys locked, values prose), the pattern spine is a RECOMMENDED spine that bends to the pattern's tier — Composition, Flow, or Layout & Shell — and carries a GOAL facet (the GOV.UK-style user intent) for task-based lookup. A small ALWAYS core plus tier-conditional SCALES sections. Sets the convention for the patterns layer the way components/_schema.md set it for the catalogue.
tags: [patterns, schema]
timestamp: 2026-06-18
---

# Pattern Brief Schema

The component catalogue (`components/`) studies *things* — a Button, a Date Picker — each with props, states, variants, an API. A **pattern** is a different artifact: a **recurring composition of components that solves a problem** — Forms-as-a-system, Filtering, a multi-step wizard, a dashboard template. A pattern has no props. It has a *problem*, the *components it assembles*, the *way it arranges and sequences them*, and — above all — the *decision rules* that resolve the contested choices. So the pattern brief needs its own spine.

This file is to the patterns layer what `components/_schema.md` is to the catalogue: it locks the convention. But it locks it **more loosely, on purpose** — patterns are heterogeneous (a state convention like *Disabled* and a page template like *Dashboard* share almost no structure), so a rigid 15-key spine would force empty sections and false symmetry. The pattern spine is therefore a **recommended spine** — a small ALWAYS core that every pattern carries, plus SCALES sections that appear only when the pattern's **tier** calls for them.

This was the practice's deliberate plan: *"we will want to come up with a plan for patterns — a schema, although it might need to be flexible."* The flexibility is the design, not a concession.

---

## The pattern-vs-component boundary

A pattern is reached for when a problem recurs across an engagement but the answer is an *opinionated, goal-contextual assembly*, not a *thing*. The distinguishing test is **not packaging** — it is **opinionation and contextual dependency**. A component is **goal-agnostic**: a `<Button>` or a `<form>` primitive does not care whether it sits in a checkout, a profile edit, or a settings page. A pattern is the opposite — a **highly opinionated resolution to a specific user goal**, contextualised by business logic, layout, and flow, that **owns the orchestration no single component can own**. The line the Form brief drew is the canonical example: **Form** is the component (the `<form>` primitive + the validation orchestration); **Forms-as-a-system** (the multi-step wizard, save-and-resume, the cross-page flow) is the pattern. A pattern:

- **composes components** (it names them as typed references into `components/`, and does not re-derive them);
- **is mostly decisions** (its value is the resolved forks — when variant A vs B — far more than any markup);
- **owns cross-component / business-logic orchestration** (focus moving *across* components, the landmark structure of a whole region, the live-region coordination, the data-persistence and error-recovery sequence) that no single component can own;
- **is goal-contextual** (it carries an opinion about *what the user is trying to do* — captured in its `goal` facet — where a component is intentionally goal-neutral).

**Importability is a signal, not the test.** Modern systems routinely *do* ship a pattern packaged as a macro-component — Ant Design's `ProForm`/`ProTable`, a `<Wizard>`, a shipped `AppShell`, a command palette. That does not demote the pattern to a component; the **pattern brief documents the decisions, orchestration, and goal regardless of whether one instantiation happens to ship as code**. The discriminator is opinionation, not packaging.

**The already-briefed-as-component guard.** Where the catalogue already briefs something as a component (Empty State, Table, the Search *field*), the *pattern* is the **orchestration around it**, never a re-brief: the pattern is "empty/loading/error state orchestration across a view," "the sortable/filterable/paginated data-grid experience," "the search experience (typeahead + results + scope + no-results)" — not the surface the component already owns. When a candidate has a stable, goal-agnostic prop surface and nothing to orchestrate, it's a component; promote it to `components/`.

---

## The three tiers

Every pattern declares a `tier`. The tier is the primary axis because it predicts the spine's shape — which SCALES sections carry weight. The three tiers cut on a coherent axis — a **local recipe** (space), a **journey** (time), or an **archetype** (the macro-frame) — mirroring where the field has settled (Material 3's Canonical Layouts, Fluent's recipes, GOV.UK's task flows):

1. **`composition`** — a localised, single-screen *spatial recipe*: a reusable assembly that orchestrates several components to solve a recurring micro-problem. *Forms-as-a-system, the data-collection "Ask users for X" recipes, Filtering, Search orchestration, action-priority/overflow, view-state orchestration (empty/loading/error across a region), notification orchestration, data visualization, inline edit, bulk actions.* Composition- and decision-rule-heavy; light on layout and flow.
2. **`flow`** — a *temporal journey*: a multi-step interaction unfolding over time, requiring step sequencing, state persistence, and error recovery. *Login/Auth, the multi-step wizard, destructive confirmation, save / unsaved-changes, onboarding, check-answers, eligibility/triage, AI conversational flows.* Flow-and-state- and content-heavy.
3. **`layout-and-shell`** — a *structural archetype*: the responsive macro-architecture of a screen or app frame. *App shell / global header, master-detail (list-detail), dashboard, settings, error pages, feed, supporting-pane.* Layout-and-structure-heavy; the composition is a regional skeleton.

A pattern occasionally spans two tiers (a wizard is a `flow` that often fills a `layout-and-shell` archetype); declare the dominant tier and note the secondary in `notes.secondary-tier`.

**What is NOT a pattern tier — the Foundations exile.** Cross-cutting *rules for expressing a state or system property consistently* are **not patterns** — they are foundations guidance, and the practice already has a home for them in the numbered files (00–10+). **Disabled** and **read-only** semantics, **theming / dark-mode**, and **internationalisation / RTL** are system-wide heuristics that modify components globally; they belong in (or are cited from) the numbered files, not here. The field agrees: Material 3 keeps interaction states under Foundations; Spectrum handles states as global token properties. The earlier `state-convention` tier is dissolved on this basis. The discriminating question: *is this a global rule a component obeys (→ Foundations), or genuine cross-region orchestration with its own composition and decision rules (→ a `composition` pattern)?* Loading/empty/error **orchestration across a view**, and **notification routing** across a system, pass that test and live in the `composition` tier — they compose components and resolve real forks. The bare state rule does not.

---

## The recommended spine

H2 sections, problem-led. **ALWAYS** sections appear in every pattern; **SCALES** sections appear when the tier (or the specific pattern) gives them weight. The order is the reading order; omit a SCALES section rather than writing an empty one (the Divider-collapses-cleanly principle, applied at the pattern level).

1. **Frontmatter** — ALWAYS. OKF YAML: `okf_version`, `type: pattern-brief`, `title`, `description`, `tags`, `tier` (one of the three), `goal` (the GOV.UK-style user intent — see below), `status`, `timestamp`. (`tier` and `goal` are the patterns-layer additions to the component frontmatter shape.)
2. **`# NN — Title` H1 + a blockquote framing** — ALWAYS. The one-paragraph "what problem this solves / what it isn't / the boundary it holds" (the component briefs' blockquote, problem-led).
3. **Problem & context** — ALWAYS. The recurring problem; when it applies and when it doesn't; why systems diverge. (≈ component §1, but it opens on the *problem*, not the *thing*.)
4. **Composition** — ALWAYS. The components the pattern assembles, as **typed references into `components/`**, and how they fit together. This is the heart — a pattern *is* its composition. Name the briefs (`see form`, `see table`); record the *delta* the pattern adds, never re-derive the component.
5. **Decision rules** — ALWAYS. The contested choices the pattern resolves, as frameworks not winners: when variant A vs B, the forks, the "it depends" axes. A pattern earns its keep here — most of a pattern brief is decisions.
6. **Flow & states** — SCALES (flows-and-shells; some recipes). The step sequence / state machine / orchestration over time (the wizard's steps, the auth flow, the confirmation's commit/cancel). Omit for page templates and most state conventions.
7. **Layout & structure** — SCALES (`layout-and-shell`). The spatial arrangement — regions, the responsive skeleton, the breakpoints. Heavy for archetypes and shells; absent for most `composition` recipes.
8. **Accessibility orchestration** — ALWAYS. The cross-component a11y the **pattern** owns — focus management *across* components, the landmark/heading structure of the whole region, the live-region coordination, the keyboard flow between parts — distinct from each component's own a11y (which is inherited, not repeated). The single most important reason a pattern is briefed rather than left implicit.
9. **Content & copy** — SCALES, but **near-ALWAYS for `flow` and task-led `composition` patterns**. The copy conventions the pattern dictates (the confirmation wording, the empty/error voice, the step labels, the question phrasing). GOV.UK's patterns are *dominated* by this — for the data-collection and flow patterns, copy is load-bearing, not optional. Omit only when the composed components already own all the copy (rare for flows).
10. **Variants & responsive** — SCALES. The intentional variants and the responsive transforms (the wizard → accordion on mobile; the master-detail → stacked).
11. **Anti-patterns** — ALWAYS. What not to do. Patterns are as much about the recurring trap as the recipe; this section is load-bearing, not a footnote.
12. **Related patterns & components** — ALWAYS. Typed relationships: `composes` (the components), `relates-to` / `composed-of` (other patterns), and the explicit **pattern-vs-component boundary** this pattern holds.
13. **Field POV evolution** — SCALES. How the field's answer to this pattern has changed (lighter than the component briefs' §13; include when there's a real arc).
14. **Reference instantiations** — SCALES (but expected on most). Which real systems ship this pattern and where to look (e.g. *Carbon's Forms pattern, GOV.UK's "Ask users for an address"*) — a grounding pointer, distinct from Sources: "go look at this live," not a citation backing a claim. Pattern libraries are example-driven; a text KB substitutes the pointer.
15. **Sources cited** — ALWAYS. With version dates; the same `_source-text/`-backing discipline as the catalogue.
16. **Agent-consumable schema** — ALWAYS. The structured projection (below).

---

## The agent-consumable schema (§16)

Like the component briefs, every pattern ends with a fenced YAML block — the structured projection of the prose. It is **pattern-shaped, not component-shaped**: it encodes composition + decision rules, not props. This block carries extra weight for the patterns layer: the vault is intended to be exposed via an MCP server, and a pattern is exactly what an agent asks for ("build a flow to collect a shipping address"). The block is therefore engineered for **lazy, resolvable retrieval** — `goal` + the one-line `problem` are what a `list_patterns()` index surfaces; the agent then pulls the full schema on demand. Recommended keys (ALWAYS unless noted):

- **`identity`** — `id`, `name`, `aliases`, `tier`, `goal`, `status`. The `goal` is the GOV.UK-style user-intent facet (`ask-for-data`, `help-user-decide`, `help-user-act`, `navigate`, `show-data`, `recover-from-error`) — the task-based lookup axis layered over the structural tier, so a pattern is findable by *what the user is trying to do*, not only by its shape. This is the single most important field for agent retrieval.
- **`problem`** — the one-line problem statement + when-it-applies / when-it-doesn't.
- **`composition`** — the **typed, resolvable** component references (`requires: [form, table, ...]`, ids that map to `components/<slug>.md`) + how they assemble. The pattern's defining field; an agent fetches the named components' own schemas before generating, so the ids must be real catalogue slugs.
- **`decision_rules`** — the resolved forks, **machine-resolvable wherever the rule genuinely has a threshold**: prefer `{ if, use }` form (`{ if: "options <= 4", use: "radio-group" }`, `{ if: "options > 4", use: "select" }`) over interpretive prose, so an agent can execute the choice without a judgement leap. Keep prose only for genuinely "it depends" axes that cannot be reduced to a condition. The pattern's value lives here.
- **`flow`** — SCALES. The step/state sequence (`flow` tier).
- **`layout`** — SCALES. The regional skeleton (`layout-and-shell` tier).
- **`accessibility_orchestration`** — the cross-component focus/landmark/live-region contract the pattern owns.
- **`content`** — SCALES (near-ALWAYS for `flow`/task patterns). The copy conventions.
- **`variants`** — SCALES. Including responsive transforms.
- **`anti_patterns`** — the recurring traps.
- **`reference_instantiations`** — SCALES. The "go look at this live" pointers (system + where).
- **`relations`** — `composes` (components), `relates-to` / `composed-of` (patterns), `boundary` (the pattern-vs-component line this pattern holds).
- **`notes`** — `contested`, `unverified` (the standing home for unbacked claims — same discipline as the catalogue), `secondary-tier`.

Values stay free-form prose **except `decision_rules` and `requires`, which lean structured** for agent execution. The discipline is structural consistency within the flexibility, not a rigid type system — but the machine-resolvable fields are where the patterns layer earns its MCP keep.

---

## Conventions carried over from the catalogue

- **`inherits:` / composition over re-derivation.** A pattern names the components it composes and records only the *delta* — it never re-derives a briefed component. The component's a11y, states, and API live in `components/<slug>.md`; the pattern cites them.
- **`notes.unverified`.** Claims surfaced in research but lacking `_source-text/` backing are flagged, never silently laundered into an asserted default.
- **Voice.** Prose-led, opinionated, first-person plural, citations to real systems with version dates — identical to the numbered files and the catalogue.
- **Cross-reference style.** Inline prose (`see form`, `see 01-discovery-and-strategy`), not wikilinks or markdown links — the vault convention.

---

## Research & synthesis workflow

Patterns use the **same dual-agent flow** as the component catalogue (the practice's chosen default for the layer): a single prompt run against two agents, both raw outputs captured under `_research/_inbound/YYYY-MM-DD-pattern-<slug>/` (`prompt.md`, `claude.md`, `external-agent.md`), synthesized directly into `patterns/<slug>.md`. The dual-agent default holds because patterns are contested by nature; the convergent-primitive claude-only escape hatch (Divider/Spinner) is available but will be rarer here. The `_inbound/` folder stays as the audit record; synthesis is direct-to-file unless two outputs diverge enough to need a `_research/_synthesis/` reconciliation.

When a pattern lands: add its entry to `patterns/index.md` (from a `scope:` stub to a stable link + one-line hook + status), and add inline cross-references from the component briefs and numbered files where the pattern is now relevant — the same promotion discipline the catalogue uses, run in the pattern→component and pattern→numbered-file directions.

---

## Conformance

`patterns/_schema.md` defines the shared shape; each pattern's §16 block stays complete and self-contained. The first pattern — **Forms-as-a-system**, the `composition` pattern (`goal: ask-for-data`) the Form component forward-referenced — is the worked example that will exercise (and, where it must, refine) this spine before it hardens: it spans composition, decision rules, flow, and content, so it stress-tests the most of the spine in one run. As with the catalogue, a genuinely new key proves itself across multiple patterns before it's added here.

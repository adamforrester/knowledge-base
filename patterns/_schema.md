---
okf_version: "0.1"
type: schema
title: Pattern Brief Schema
description: The flexible spine for a pattern brief — the patterns-layer counterpart to the component catalogue's locked §15 schema. A pattern is a recurring composition of components solving a problem, so the spine encodes the PROBLEM, the COMPOSITION (typed references into the component catalogue), and the DECISION RULES — not a thing's props. Unlike the component spine (keys locked, values prose), the pattern spine is a RECOMMENDED spine that bends to the pattern's tier: a small ALWAYS core plus tier-conditional SCALES sections. Sets the convention for the patterns layer the way components/_schema.md set it for the catalogue.
tags: [patterns, schema]
timestamp: 2026-06-18
---

# Pattern Brief Schema

The component catalogue (`components/`) studies *things* — a Button, a Date Picker — each with props, states, variants, an API. A **pattern** is a different artifact: a **recurring composition of components that solves a problem** — Forms-as-a-system, Filtering, a multi-step wizard, a dashboard template. A pattern has no props. It has a *problem*, the *components it assembles*, the *way it arranges and sequences them*, and — above all — the *decision rules* that resolve the contested choices. So the pattern brief needs its own spine.

This file is to the patterns layer what `components/_schema.md` is to the catalogue: it locks the convention. But it locks it **more loosely, on purpose** — patterns are heterogeneous (a state convention like *Disabled* and a page template like *Dashboard* share almost no structure), so a rigid 15-key spine would force empty sections and false symmetry. The pattern spine is therefore a **recommended spine** — a small ALWAYS core that every pattern carries, plus SCALES sections that appear only when the pattern's **tier** calls for them.

This was the practice's deliberate plan: *"we will want to come up with a plan for patterns — a schema, although it might need to be flexible."* The flexibility is the design, not a concession.

---

## The pattern-vs-component boundary

A pattern is reached for when a problem recurs across an engagement but the answer is an *assembly*, not a *component*. The line the Form brief drew is the canonical example: **Form** is the component (the `<form>` primitive + the validation orchestration); **Forms-as-a-system** (the multi-step wizard, save-and-resume, the cross-page flow) is the pattern. A pattern:

- **composes components** (it names them as typed references into `components/`, and does not re-derive them);
- **is mostly decisions** (its value is the resolved forks — when variant A vs B — far more than any markup);
- **owns cross-component orchestration** (focus moving *across* components, the landmark structure of a whole region, the live-region coordination) that no single component can own;
- **does not ship as one importable thing** (it's a recipe an engagement instantiates, though a system may ship scaffolding — an `AppShell`, a `<Wizard>` — for the heavier ones).

When a "pattern" turns out to have a stable prop surface and ships as one component, it belongs in `components/`, not here.

---

## The four tiers

Every pattern declares a `tier`. The tier is the primary axis because it predicts the spine's shape — which SCALES sections carry weight.

1. **`cross-component-recipe`** — a reusable assembly solving a recurring micro-problem. *Forms-as-a-system, Filtering, Search, Common actions (the action-priority/overflow model), Overflow content.* Composition- and decision-rule-heavy; light on layout and flow.
2. **`state-convention`** — a cross-cutting rule for expressing one *state* consistently across all components. *Disabled, Read-only, Loading orchestration, Notifications orchestration.* Decision-rule- and accessibility-heavy; almost no layout or flow. (These are closest to the numbered files' cross-cutting POV; a state convention may cite many briefs at once.)
3. **`flow-and-shell`** — a multi-step or app-frame interaction unfolding over time and space. *Login/Auth, App shell / global header, the multi-step wizard, destructive confirmation, save / unsaved-changes.* Flow-and-state- and layout-heavy.
4. **`page-template`** — a full-page composition archetype. *Master-detail, dashboard, settings, error pages, onboarding.* Layout-and-structure-heavy; the composition is a regional skeleton.

A pattern occasionally spans two tiers (a wizard is a flow that often fills a page template); declare the dominant tier and note the secondary in `notes`.

---

## The recommended spine

H2 sections, problem-led. **ALWAYS** sections appear in every pattern; **SCALES** sections appear when the tier (or the specific pattern) gives them weight. The order is the reading order; omit a SCALES section rather than writing an empty one (the Divider-collapses-cleanly principle, applied at the pattern level).

1. **Frontmatter** — ALWAYS. OKF YAML: `okf_version`, `type: pattern-brief`, `title`, `description`, `tags`, `tier` (one of the four), `status`, `timestamp`. (The `tier` field is the patterns-layer addition to the component frontmatter shape.)
2. **`# NN — Title` H1 + a blockquote framing** — ALWAYS. The one-paragraph "what problem this solves / what it isn't / the boundary it holds" (the component briefs' blockquote, problem-led).
3. **Problem & context** — ALWAYS. The recurring problem; when it applies and when it doesn't; why systems diverge. (≈ component §1, but it opens on the *problem*, not the *thing*.)
4. **Composition** — ALWAYS. The components the pattern assembles, as **typed references into `components/`**, and how they fit together. This is the heart — a pattern *is* its composition. Name the briefs (`see form`, `see table`); record the *delta* the pattern adds, never re-derive the component.
5. **Decision rules** — ALWAYS. The contested choices the pattern resolves, as frameworks not winners: when variant A vs B, the forks, the "it depends" axes. A pattern earns its keep here — most of a pattern brief is decisions.
6. **Flow & states** — SCALES (flows-and-shells; some recipes). The step sequence / state machine / orchestration over time (the wizard's steps, the auth flow, the confirmation's commit/cancel). Omit for page templates and most state conventions.
7. **Layout & structure** — SCALES (page-templates; shells). The spatial arrangement — regions, the responsive skeleton, the breakpoints. Heavy for templates/shells; absent for state conventions.
8. **Accessibility orchestration** — ALWAYS. The cross-component a11y the **pattern** owns — focus management *across* components, the landmark/heading structure of the whole region, the live-region coordination, the keyboard flow between parts — distinct from each component's own a11y (which is inherited, not repeated). The single most important reason a pattern is briefed rather than left implicit.
9. **Content & copy** — SCALES. The copy conventions the pattern dictates (the confirmation wording, the empty/error voice, the step labels). Omit when the composed components already own all the copy.
10. **Variants & responsive** — SCALES. The intentional variants and the responsive transforms (the wizard → accordion on mobile; the master-detail → stacked).
11. **Anti-patterns** — ALWAYS. What not to do. Patterns are as much about the recurring trap as the recipe; this section is load-bearing, not a footnote.
12. **Related patterns & components** — ALWAYS. Typed relationships: `composes` (the components), `relates-to` / `composed-of` (other patterns), and the explicit **pattern-vs-component boundary** this pattern holds.
13. **Field POV evolution** — SCALES. How the field's answer to this pattern has changed (lighter than the component briefs' §13; include when there's a real arc).
14. **Sources cited** — ALWAYS. With version dates; the same `_source-text/`-backing discipline as the catalogue.
15. **Agent-consumable schema** — ALWAYS. The structured projection (below).

---

## The agent-consumable schema (§15)

Like the component briefs, every pattern ends with a fenced YAML block — the structured projection of the prose. It is **pattern-shaped, not component-shaped**: it encodes composition + decision rules, not props. Recommended keys (ALWAYS unless noted):

- **`identity`** — `id`, `name`, `aliases`, `tier`, `status`.
- **`problem`** — the one-line problem statement + when-it-applies / when-it-doesn't.
- **`composition`** — the typed component references (`components: [form, table, ...]`) + how they assemble. The pattern's defining field.
- **`decision_rules`** — the resolved forks, each as `{ choice, resolution, depends-on }` (or prose). The pattern's value.
- **`flow`** — SCALES. The step/state sequence (flows-and-shells).
- **`layout`** — SCALES. The regional skeleton (page-templates/shells).
- **`accessibility_orchestration`** — the cross-component focus/landmark/live-region contract the pattern owns.
- **`content`** — SCALES. The copy conventions.
- **`variants`** — SCALES. Including responsive transforms.
- **`anti_patterns`** — the recurring traps.
- **`relations`** — `composes` (components), `relates-to` / `composed-of` (patterns), `boundary` (the pattern-vs-component line).
- **`notes`** — `contested`, `unverified` (the standing home for unbacked claims — same discipline as the catalogue), `secondary-tier`.

Values stay free-form prose, as in the catalogue. The discipline is structural consistency within the flexibility, not a rigid type system.

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

`patterns/_schema.md` defines the shared shape; each pattern's §15 block stays complete and self-contained. The first pattern — **Forms-as-a-system**, the `flow-and-shell`/`cross-component-recipe` the Form component forward-referenced — is the worked example that will exercise (and, where it must, refine) this spine before it hardens. As with the catalogue, a genuinely new key proves itself across multiple patterns before it's added here.

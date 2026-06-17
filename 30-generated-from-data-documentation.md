---
type: practice-area
title: Generated-From-Data Documentation as Commercial Default
description: The architecture that treats the component data file as the source of truth — the pipeline, the upfront engineering cost, the per-component hours redistribution, the decision framework, the migration playbook, the cluster relationship to AI-readiness, the commercial pitch, and the tooling realities where the field is genuinely behind in 2026.
tags: [extension, documentation, components, mdx, storybook, ai-json, mcp, code-connect, commercial]
timestamp: 2026-06-14
---

# 30 — Generated-From-Data Documentation as Commercial Default

> 04-documentation covers the strategy and 29-per-component-documentation-template covers the artefact. This file covers the *commercial-default angle* — the engineering investment, the tooling realities, the migration playbook, the cost shift, the pitch. The architecture has been articulated across the vault for years; the gap that remains is in the SOW. The practice ships authored prose by default and treats generation as aspirational; this file is the corrective. The thesis: the architectural decision and the commercial transition are two orthogonal problems. Solving the architectural problem (which the vault largely has) does not by itself solve the commercial problem (the proposal language, the line-item discipline, the cost narrative, the objection handling). This file is what the practice commits to so that the next engagement starts in the right shape.

---

## 1. The architecture in production — what generated-from-data documentation actually looks like in 2026

Generated-from-data documentation rests on a single load-bearing decision: **the component data file is the source of truth.** Every consumer of the docs — Storybook, MDX docs site, `.ai.json` registry served via MCP, Figma library properties, AI-assistant catalog, conformance dossier — derives its content from this source. Per 29-per-component-documentation-template, 03-component-library, and Curtis (*Components as Data*, Sep 2025), this is the architectural answer the practice has accepted. The questions for this file are about the *shape* of the source, the *consumers* that derive from it, the *seams* where authoring still happens, and the *commercial transition* that converts the architecture into a sellable scope item.

**The data file's seed is the per-component brief.** Per 03's *Per-component briefs* section and `components/index.md`, every component in the practice's catalogue carries a §15 *Agent-consumable schema* — a free-form YAML block that is the structured projection of the brief's prose. The brief's §15 is not the engagement's source of truth (that is the engagement's component data file in its own codebase); it is the seed that data file is instantiated from. The brief documents what the practice would ship if starting from scratch; the engagement's reality — existing component model, framework choice, brand-specific extensions — overrides where it has to. The two-source-of-truth concern dissolves once the relationship is read this way: the brief is upstream and prescriptive; the engagement's data file is downstream and authoritative for that codebase.

### Source-format choices

Three credible source formats in 2026, with materially different downstream consequences.

**TypeScript types as the implicit source.** The most-common starting point. The component is a `.tsx` file; props are a `type ButtonProps = { ... }` declaration; defaults are React `defaultProps` or destructured assignments; deprecation flags are `@deprecated` JSDoc. `react-docgen-typescript` (or the SWC-based docgen pipeline shipped in Storybook 9) extracts types and JSDoc into the structured representation Storybook autodocs renders. For Svelte, `sveld` is the AST-driven equivalent — analysing the source to emit structured JSON detailing props, slots, and reactive bindings, with the conservative discipline of refusing to evaluate arbitrary code *(external)*.

- **Enables:** zero-friction adoption for React-first systems; tight coupling between source and docs; rich JSDoc as the authoring surface; AI tools that consume TypeScript directly (Cursor, Copilot, Claude Code) get reasonable behaviour without a separate metadata layer.
- **Forbids:** non-TypeScript consumers (Figma, design-side tooling) cannot read TypeScript directly; the source is locked to the runtime framework; cross-framework systems hit a wall.

**Explicit JSON Schema or YAML definition.** The component is defined in a neutral structured format (`Button.component.json` with schema-driven validation) before it touches any framework. The implementation derives from the definition; the docs derive from the definition; the Figma library properties derive from the definition. Adobe Spectrum's architecture is the canonical public exemplar — extensive JSON schema definitions mapping component APIs, deprecations, and tokens across platform outputs *(external)*.

- **Enables:** framework-agnostic. The same definition produces React, Vue, Svelte, and native iOS / Android / Flutter implementations. The Figma sync is direct because Figma component properties map to the schema. The `.ai.json` is a projection of the schema. AI tools consume the schema directly via MCP.
- **Forbids:** the upfront design cost is real — defining the schema takes work the team would not otherwise do. Mismatches between the schema and the implementation are a new class of bug. Engineering teams trained on TypeScript-as-source resist the indirection.

**Framework-native definition with sufficient metadata.** A Lit web component with `@property` decorators, a Stencil component with explicit metadata, or a React component with a Zod schema co-located. The framework is the source; the framework's metadata model is rich enough to drive generation downstream.

- **Enables:** keeps engineering teams in their preferred framework; metadata is extracted automatically; web-component-based systems get a portability win because Lit components are framework-agnostic at consumption time.
- **Forbids:** cross-framework definitions are still per-framework. The shared metadata layer has to live above the framework-native definition.

**The practice's default position.** For most agency engagements (React-first, web-led, single-framework), TypeScript-as-source plus `.ai.json` overlay is the right starting point. For multi-platform engagements (web + iOS + Android) or multi-framework consumers, explicit JSON Schema is justified. For web-component-based systems shipping as portable libraries, framework-native (Lit + ElementInternals per 28 §1) is the answer. **The decision is a Discovery deliverable, not a Foundations deliverable** — committing to the source format in week 1 is what unblocks every downstream pipeline choice.

### Generation targets

The pipeline projects the source to five distinct consumption targets, each requiring a different projection.

- **Storybook autodocs.** The interactive developer surface. Storybook 9 (May 2026) ships consolidated docs architecture with SWC-based docgen replacing the older Babel path; controls panel, props table, and live canvas are all generated from the source types and JSDoc.
- **MDX docs site.** The comprehensive portal. Pulls type signatures, defaults, and deprecations from the source; renders alongside authored editorial prose. Cross-references between components are resolved at build time.
- **`.ai.json` registry, served via MCP.** The AI-agent surface. Schema generated from types, JSDoc, and `@ai` tags; merged with authored fields (`when_to_use`, `avoid_when`, `business_context`, `semantic_prompt`, the accessibility schema). Aggregated into a registry; the MCP server (per 15-ai-in-ds and §6 below) is the protocol surface.
- **Figma library properties via Code Connect.** The design-tool surface. Component-side props and variant declarations map to Figma component properties; Code Connect 1.x for React handles the source→Figma direction; iOS / Android / Flutter Code Connect is at 0.x to 1.x maturity (see §8).
- **Conformance dossier.** The auditor surface. Automated test results from CI plus serialised manual-AT walkthrough logs map to WCAG 2.2 / Section 508 success criteria; the dossier is per-component, aggregating into the consuming product's ACR.

The non-obvious divergence: **Figma needs prop-value enumeration** (the actual list of `tone` enum values to populate the variant property) which TypeScript types provide but JSDoc-only sources do not. **AI agents need *semantic prompts*** (one-line use-case framings) which neither types nor JSDoc carry — they have to be authored separately into `.ai.json`. **Storybook needs *control declarations*** (the explicit "this is a select with these options" affordance) which can be derived from types but often need overrides for richer controls. The pipeline is one source with multiple projections; the projections are not symmetric.

There is also an emerging contender alongside `.ai.json`: **`DESIGN.md`** as a standardising AI-metadata format, with markdown body plus YAML frontmatter *(external — held with the caveat that as of mid-2026 no canonical AI-metadata format has fully emerged in the field; both `.ai.json` and `DESIGN.md` are credible options the practice should track and pick one of in week 1)*. The practice's discipline is to commit to a single format per engagement, document the schema as practice IP, and revisit when the field's standardisation story settles.

### The CI surface

What runs when a source change lands:

- **Schema validation.** The component data file parses against the schema; types resolve; JSDoc is extracted. Failure: invalid prop, missing required JSDoc, broken type reference.
- **Freshness check.** Per 29 §5: the component's authored doc fields produce a content hash; if the source changed but the hash didn't, the build fails. The single highest-leverage CI rule the practice ships.
- **Accessibility schema enforcement.** The `.a11y.json` (or the accessibility section of `.ai.json`) must include rows for every concern in the contract per 17 / 28; missing rows fail the build. axe-core runs in headless against generated component variants identifying missing ARIA, contrast failures, and WCAG violations *(external — sharper articulation)*.
- **Link verification.** Cross-references between component pages are verified; broken links fail the build.
- **Visual regression.** Chromatic, Percy, or self-hosted Playwright captures screenshots of generated stories and detects unintended cascading effects.
- **Semver bump detection.** Breaking type changes trigger a major-version requirement; deprecation propagates across all five generation targets simultaneously *(both agents — load-bearing)*. Per 24-tokens-at-scale, this is the same discipline applied to the component layer.
- **MDX rendering check.** The MDX docs file compiles; component imports resolve; embedded examples render without runtime errors.

The CI pipeline is the practice's quality contract. Without it, the source-of-truth model is aspirational; with it, the source-of-truth model is enforced.

### The single-source-of-truth file structure

The shape from 29 §5, with engineering-tier ownership annotations:

```
component-source/
├── Button.tsx                  # implementation               [engineering]
├── Button.types.ts             # types (consumed by docs)     [engineering]
├── Button.stories.tsx          # Storybook stories            [engineering]
├── Button.docs.mdx             # authored prose               [UX Designer]
├── Button.tokens.ts            # design tokens consumed       [eng-authored, design-audited]
├── Button.ai.json              # AI metadata (auth + gen)     [UX Designer + generated]
├── Button.a11y.json            # accessibility schema         [UX Designer + generated]
└── Button.test.tsx             # automated tests              [engineering]
```

Strict compartmentalisation ensures machine-generated facts are never commingled with human-authored intent in a way that risks destructive overwrites during the build *(external — sharp framing)*. The CI freshness check fires when engineer-owned files change without designer-owned files updating, forcing the conversation between the two roles before the change merges.

### The authoring seam

Generation produces the technical layer; authoring produces the intent layer. The seam:

- **Generated:** props tables, type signatures, default values, deprecation flags, version-introduced metadata, default Storybook examples, design-token references, accessibility schema fields the schema can derive, the per-component changelog from commit history, the Figma component-property mappings, the `.ai.json` `props` and `tokens` arrays.
- **Authored:** purpose, when-to-use, avoid-when, anatomy diagrams, do/don't pairs, content guidelines, the accessibility "consumer must specify" rows, the example captions, the `.ai.json` `business_context` and `semantic_prompt` fields, the typed relationships graph (`alternativeTo`, `composesWith`, `supersedes`).
- **Generated-with-overlay:** state matrices (declared in source, rows authored — visual treatment, token transition, announced state, interaction model, triggering condition per 29 §3), variants (generated from prop combinations, screenshots authored or auto-captured), conformance dossier (test results from CI, manual-AT walkthrough links authored, SC-by-SC mapping authored once and validated).

The authoring discipline that survives generation is the editorial one. Generation removes the *technical* duplicate-authoring; it does not — and should not attempt to — remove the editorial work. Per 29's anti-patterns and external's framing on this: when LLMs author purpose / when-to-use prose, the result is dangerously generic, frequently hallucinates business rules, or misses the subtle constraints of the specific enterprise domain. The example external offers is concrete and worth keeping: an LLM might confidently state a red button is for "destructive actions," missing that in a healthcare system red specifically denotes "critical patient alert." Human curation at the authoring seam is non-negotiable.

The MDX overlay file is the designated authoring seam — pulling generated facts via component imports while preserving a CI-verified space for expert editorial prose. Authored prose remains authored.

---

## 2. The pipeline shape — the concrete dependency graph

The pipeline is a directed graph from source to consumers. Every arrow has a tool, a failure mode, and a recovery path.

### From source change to consumer update

A commit triggers static extraction. For React-based systems, tooling parses the component source's AST, extracting interfaces and JSDoc annotations. Malformed types or unresolved inheritance chains fail the build immediately, preventing cascading errors throughout the downstream documentation. After successful extraction, the pipeline forks into parallel generation paths so all consumers receive synchronous updates.

### Storybook + MDX path

`Button.types.ts` + `Button.tsx` JSDoc + `Button.stories.tsx` → `react-docgen-typescript` / SWC docgen → Storybook 9 docs page.

- **What runs.** Docgen extracts types, JSDoc, default values into Storybook's `argTypes`, populating the controls panel without manual story configuration. Storybook renders props table, controls panel, canvas. Stories render as live examples; addon-a11y runs axe-core on each story; Chromatic / Percy / Playwright captures visual variants in parallel.
- **What blocks what.** Docgen failures fail the build; Storybook fails if a story throws. Visual regression runs after Storybook builds and gates the deploy.
- **What fails build vs. warns.** Docgen errors fail; addon-a11y violations are configurable — the practice ships them as "fail on serious-or-critical, warn on moderate-or-minor." Visual regression diffs warn by default; ship as "fail on diff > 0.1% per story unless explicitly approved."
- **Failure mode.** Slow docgen on large libraries (Storybook 9's SWC path is materially faster than the Babel-based path; teams on Storybook 8 with the older docgen should upgrade specifically for this).

The MDX docs site path operates as an aggregator. The MDX compiler ingests the markdown file, but at render time dynamically resolves custom documentation components (e.g., `<PropsTable component="Button" />`) by querying the centralised data object *(external)*. Technical specifications on the docs site are dynamically injected at build time, never more than one CI cycle removed from production reality.

### `.ai.json` emission path

`Button.types.ts` + `Button.tsx` JSDoc + `@ai` tags + `Button.ai.json` overlay → schema validator → registry build → MCP server.

- **What runs.** Schema validator validates the merged `.ai.json` (generated fields + authored fields) against the registry schema. Registry builder aggregates all components into a queryable registry. MCP server exposes the registry to AI clients.
- **The merge must be aggressively deterministic** *(external — sharp discipline)*. The consolidation pipeline avoids using LLMs during the merge to prevent hallucinated data fabrication; independent parsers segment the data into discrete semantic categories (behavior, state, layout) before the merge.
- **Format discipline.** Industry benchmarking on AI-readable docs reports semantic chunking with concept-aligned boundaries materially outperforming monolithic JSON or raw Markdown — external cites ~92% retrieval accuracy and ~88% token-consumption reduction *(both figures held as external-cited rather than asserted; the directional argument is the load-bearing claim)*. The practical implication: emit per-concept chunks rather than full-component JSON dumps.
- **What blocks what.** Schema validation failure blocks registry build; registry build failure blocks MCP server start.
- **What fails build vs. warns.** Missing required authored fields (`when_to_use`, `avoid_when`) fail; missing optional fields (`semantic_prompt`) warn.
- **Failure mode.** Schema-evolution problem — when the registry schema changes (a new required field), every component's `.ai.json` must update; the practice ships migration scripts as part of pipeline maintenance.

When an AI agent — Atlassian's Rovo Dev CLI is the most-cited 2026 example, querying via tools like `ads_plan` *(external; tool name held as cited pending verification)* — queries the system, the MCP server delivers the exact import paths, token applications, and accessibility requirements the agent needs to generate compliant code.

### Figma library sync path

`Button.types.ts` props + variants → Code Connect figma-config → Figma library properties.

- **What runs.** Code Connect CLI in CI scans the repo for `.figma.ts`, `.figma.tsx`, `.figma.swift` mapping files, parses the templates, verifies that code-side properties (`isDisabled` boolean, `ButtonVariant` enum) map to defined Figma component properties.
- **Direction.** Largely unidirectional in 2026 — code projects into Figma Dev Mode, surfacing the exact API and framework-specific snippets to designers and developers inspecting the canvas. The Figma→source direction remains partial.
- **What blocks what.** Figma sync runs on a CI cadence (per-PR or per-merge); does not block the code build because Figma is downstream.
- **What fails build vs. warns.** Sync failures warn rather than fail — Figma is a separate system that may be unavailable; ship a "Figma sync passed at HEAD" status check that is required for release but not for merge.
- **Failure mode.** The single most-cited drift point. Designers continue using the old library; engineering ships the new one; designers reach for properties that don't exist in source. The mitigation: ship Code Connect with every component as default, run Figma sync per-merge, treat a stale Figma library as a release blocker. If a property is deleted in code but remains in the Figma library, the CLI emits a warning during the build alerting the team to the architectural drift *(external)*.

### Conformance dossier path

`Button.test.tsx` results + `Button.a11y.json` schema + manual-AT walkthrough logs → CI artefact → consuming product's ACR.

- **What runs.** Tests run on every PR; results emit per-component dossier files; manual-AT walkthrough links are stored alongside. The CI extracts axe-core headless results and merges with serialised manual-AT audit logs (stored as data alongside the components). Aggregated data maps section-by-section to specific WCAG and Section 508 criteria *(external — sharp framing)*.
- **What blocks what.** Test failures block merge; missing manual-AT links per minor version warn.
- **Output.** A highly structured ACR reflecting the exact, verifiable state of the current system deployment. Eliminates the periodic, reverse-engineered compliance audit pattern.
- **Failure mode.** The dossier is per-component; the consuming product needs application-level evidence too (per 28 §8). The practice's responsibility is the per-component layer; the consuming product's accessibility lead aggregates.

### Cross-pipeline failure modes

The most-cited 2026 failure mode involves complex monorepo resolution. `react-docgen-typescript` frequently breaks in Turborepo, Nx, and Vite workspaces when dealing with cross-package inheritance. If a component extends an interface from a different package root, the generator outputs empty prop tables or defaults to obscure object types instead of specific literals *(external — practitioner-tier specificity)*. Recovery: enforce strict direct-source import paths or write custom plugins (Vite plugins manually resolve the AST) that resolve the inheritance correctly.

The silent-extraction-failure path is the one to fear. If metadata extraction silently fails — empty prop table, unresolved inheritance — the drift goes unnoticed until an AI agent hallucinates an API during code generation. **Strict schema validation before merge is the only reliable mitigation.**

Other recurring cross-pipeline failures:

- **Schema drift.** Registry schema updates; not every `.ai.json` migrates; some components ship stale schema. CI catches the validation failure; the migration script catches the lift; the practice ships both as default infrastructure.
- **Visual-regression noise.** Anti-aliasing differences between platforms (macOS dev runner vs. Linux CI runner) produce false-positive diffs. Storybook's `chromatic-config.js` plus Docker-for-snapshot-generation discipline mitigates.
- **Code Connect drift.** As above — the Figma library lags the source. Treat the Figma library as a deploy artefact, not an authored artefact; every system release ships a Figma library update.
- **MCP server outages.** The AI assistant cannot reach the registry. Fallback: the registry's static JSON output is consumable by AI tools that don't yet speak MCP; the system ships both surfaces.

---

## 3. The hours-and-cost shift — what changes commercially when generation replaces authoring

The economic model shifts from high ongoing operational expenditure (manual maintenance) to higher upfront capital expenditure (infrastructure), reducing lifetime cost of ownership *(external's Capex/Opex framing — sharper procurement language)*. The break-even is at the component count where the per-component redistribution exceeds the upfront cost.

### The upfront pipeline investment

A realistic 2026 estimate, with a phased adoption split that lets clients land Phase 1 at engagement start and defer Phase 2/3 to retainer or follow-on:

**Phase 1 — baseline generation (~50–80 hours).** Source format and schema authoring (8–16h); Storybook autodocs configuration (8–16h); MDX template and rendering layer (8–16h); CI freshness check, schema validation, link checking (8–16h); per-section minimum-prose rules (4–8h); accessibility-test scaffolding (8–16h); pipeline-itself documentation including engineering onboarding (8–16h).

**Phase 2 — Figma sync and `.ai.json` registry (+~25–50 hours).** `.ai.json` schema, registry build, migration script scaffolding (8–16h); Code Connect integration for React (8–16h); visual regression setup, hosted (4–8h) or self-hosted Playwright (16–24h); Code Connect for iOS / Android / Flutter (16–32h per additional platform).

**Phase 3 — custom DS MCP server (+~40–80 hours).** A custom MCP server in 2026 is the dominant single line item. The field does not yet have a turnkey "DS MCP server" the practice can ship as a vendor selection; it is a bespoke engineering project handling JSON-RPC lifecycle, secure design-token parsing, component metadata validation, and the semantic chunking strategy *(external — the 40–80h figure converges between the two agents and is held as the practitioner-tier estimate)*.

**Total upfront pipeline investment, depending on phase scope:**

- **Pipeline without MCP:** ~50–80 hours for React-first base; multi-platform adds 30–60 hours per additional Code Connect platform.
- **Pipeline with MCP and full Phase 1+2+3:** ~108–216 hours for React-first; multi-platform adds 30–60 hours per platform.

This is the line item the practice currently absorbs as overhead. **Itemising it as a Foundations-tier deliverable named "AI-Ready Documentation Architecture" or "Documentation Pipeline" is the commercial discipline this file is arguing for.** External's framing is right: the pipeline is analogous to CI/CD setup, design token architecture, or deployment environments — infrastructure that makes the system usable at scale, not a sub-bullet under "Documentation."

### The per-component hours redistribution

What changes per-component when the pipeline is in place. The two agents diverge on the per-component generated estimate (Claude: 6.25–11.5 hours; external: 1.2–2 hours); the divergence is real and worth interrogating. The synthesis holds a wider range than either agent: **the authored-prose model takes 4–11 hours per component depending on complexity; the generated-from-data model takes 2–8 hours, with 1.5–3.5 of those hours shifting to engineering for data-file authoring.** Both ends are defensible; the low end matches a primitive component (icon, divider, layout primitive); the high end matches a complex form component or data-grid.

| Section | Authored-prose (h) | Generated-from-data (h) |
|---|---|---|
| Header / summary | 0.25–0.5 | 0–0.25 |
| Live example | 0.5 | 0.25 (caption) |
| Purpose / when-to-use / avoid-when | 1.5–2.5 | 1.5–2.5 (unchanged) |
| Anatomy diagram | 0.5–2 | 0.5–2 (unchanged) |
| Props / API | 1.5–3 | 0 (generated) |
| States | 1–2 | 0.5–1 (overlay only) |
| Variants | 0.5–1 | 0.25 (overlay) |
| Examples | 1.5–3 | 1–2 (captions only; renders generated) |
| Do / don't | 0.5–1 | 0.5–1 (unchanged) |
| Accessibility | 1.5–3 | 0.75–1.5 (consumer-must-specify rows only) |
| Content guidelines | 0.5–1.5 | 0.5–1.5 (unchanged) |
| Composition / related | 0.5 | 0.5 (unchanged) |
| Changelog | 0.25 | 0–0.25 (mostly generated) |
| Conformance dossier | 1 | 0.25 (manual-AT links only) |

Net per-component savings: roughly 3–6 hours. Across 60 components: **180–360 hours saved.**

### The break-even component count

Crude calculation:

- **Phase 1 only (no MCP):** 50–80 hours upfront; 3–6 hours saved per component; break-even at **9–27 components**. Below 30 components, Phase 1 alone pays back; this is the phased-adoption argument.
- **Phase 1+2+3 (full pipeline):** 108–216 hours upfront; 3–6 hours saved per component; break-even at **18–72 components**. Midpoint roughly **30–35 components**.

External lands on **27 components** as the break-even with an 80h upfront and 3h-per-component-saved calculation; this is at the lower end of the synthesis range and is plausible for a Phase-1-only adoption. The honest answer is that the break-even depends heavily on which phase scope and which complexity distribution applies; **roughly 30 components is the practice's working heuristic**, with the genuine answer being "below 20 components, authored prose is competitive on cost; above 60 components, generation is unambiguously cheaper even on first engagement; the 20–60 band is dominated by non-cost factors."

### The lifetime benefit

Authored-prose docs accumulate drift at a rate that depends on source-update cadence. Cross-engagement memory (not from a published source) suggests roughly 15–25% doc drift over an 18-month post-handoff window — measured as components where the docs and the source disagree on at least one prop, default, or behaviour.

Generated docs eliminate drift on the technical layer; the freshness check eliminates drift on the authored layer. Authored-prose systems have needed quarterly maintenance budgets of 60–120 hours to stay current; generated systems need ~10–20 hours per quarter for pipeline maintenance (schema migrations, CI rule updates, vendor version bumps). External cites a directionally similar **~70% maintenance reduction over a three-year lifecycle** *(held as cited; the directional argument — materially smaller — is the load-bearing claim, the specific 70% figure is one estimate among several)*.

The retainer shape per 08-ongoing-maintenance is materially smaller for generated systems; this is the durable commercial argument that survives the post-handoff window when the upfront investment is long-since-amortised.

### The commercial discipline

What changes in the SOW:

- **A new line item.** "AI-Ready Documentation Architecture" or "Documentation Pipeline" as a Foundations-tier deliverable. 50–80 hours for Phase 1 only (the proposal-ready base case); +25–50 for Phase 2; +40–80 for Phase 3 if MCP is in scope at engagement start.
- **A reduced "per-component documentation authoring" line.** 2–8 hours per component split between UX Designer (intent) and engineering (data file) — instead of 4–11 hours of UX Designer and engineering combined under the authored-prose model.
- **A reduced "quarterly documentation maintenance" retainer.** ~10–20 hours per quarter instead of 60–120.
- **A new line item.** "Documentation pipeline maintenance retainer" — CI rules, schema migrations, vendor upgrades. ~8–16 hours per quarter, separate from content maintenance.

The practice currently absorbs the upfront pipeline as overhead and bills the higher per-component authoring hours; this leaves money on the table while quietly carrying the engineering investment. Itemising the pipeline as a named deliverable with its own line item, defending it as the architecture that makes the per-component hours and the retainer hours materially smaller, is the discipline this file argues for.

---

## 4. The decision framework — when is generation justified, when is authored prose enough

A 5-question decision tree the practice applies in the proposal-shaping conversation. Both agents converge on the structure; external's "3-of-5 = mandate generation" threshold is the sharper articulation.

1. **Scale.** Will the system exceed 30 components and serve more than two distinct consuming product teams?
2. **Longevity.** Is the anticipated lifecycle of the system greater than 18 months?
3. **Complexity.** Must the system enforce parity across multiple platforms (web / iOS / Android / Flutter) or multiple brand themes per 24-tokens-at-scale?
4. **Compliance.** Is there a strict legal or contractual requirement for continuous Accessibility Conformance Reports — EAA, Section 508, HIPAA?
5. **AI-integration.** Does the client's engineering culture utilise or plan to utilise AI coding agents (Cursor, Copilot, Claude Code, Rovo) that require programmatic context?

**If three or more answers are yes, the practice formally proposes the generated-from-data pipeline as the commercial default.** If fewer than three, the practice scopes authored prose, explicitly outlining the manual drift risks in the proposal to protect the agency against future liability *(external — sharp procurement language)*.

The framework is opinionated and the practice should hold it. Clients will push for "just the docs site" when their actual requirement is the full architecture; the practice's discipline is to apply the framework honestly and either ship the architecture explicitly or scope down explicitly. There is no in-between where generation is half-shipped.

The one elaboration the synthesis adds beyond the 5-question gate: **engineering culture matters for adoption shape, not for the gate itself.** Engineering-resident, code-as-source-of-truth teams adopt fast. Designer-led, design-tool-as-source-of-truth organisations need culture work; the Storybook + MDX flow is hostile to non-engineers; the practice should pair generation with a hosted design-side surface (Zeroheight) and treat the code-side as the technical-layer source. Mixed organisations work if the engineering team owns the pipeline; the design team consumes via the hosted surface. None of these change whether generation is justified — only how the rollout is shaped.

---

## 5. Migration paths — moving an existing authored-prose docs site onto a generated substrate

Most engagements arrive with documentation in some form. The practice executes migrations over a 6–12 week timeline, divided into two phases. **Treating migration as purely an engineering task is an anti-pattern; it is fundamentally a data-remediation and editorial process** *(external — sharp framing)*.

### Starting points and the migration shape

| Starting point | Migration shape | Realistic timeline |
|---|---|---|
| **Notion / Confluence** | Treat as throwaway. Content is in the wrong tool; even editorial content needs reformatting. Extract editorial content (purpose, when-to-use, do/don't, content guidelines) into a structured spreadsheet, hand it to UX Designers as authoring source, build the pipeline alongside, retire at docs-site launch. | **2–4 weeks**, dominated by content extraction. |
| **GitBook** | Slightly better — GitBook's structure carries closer to the per-component template. Same migration shape, faster content extraction. | **2–3 weeks.** |
| **Zeroheight (or similar hosted)** | Keep Zeroheight as the design-side surface. Build the code-side pipeline as the source. Sync Zeroheight from the pipeline via Zeroheight's REST API — the relationship is *inverted*, with Zeroheight becoming a read-only consumer of the codebase rather than the primary authoring environment *(external — sharp framing)*. The migration is *additive*. | **3–5 weeks**, dominated by API integration and cadence rules. |
| **Storybook without autodocs** | The most-favorable starting point. Components are already where the source lives; the pipeline adds autodocs, the MDX template, the `.ai.json` overlay, the CI rules. | **2–3 weeks.** |
| **Hand-rolled custom site (Next.js / Astro)** | Depends on architecture. If the site is already pulling from TypeScript types, the pipeline is mostly a CI and `.ai.json` addition. If the site is hand-authored prose with hand-typed prop tables, treat as Notion-equivalent. | **1–4 weeks**, wide variance. |

### The two-phase migration

**Phase 1 — parallel scaffolding and extraction.** The engineering team stands up the extraction pipeline alongside the existing codebase in a non-blocking branch — `react-docgen-typescript`, `sveld`, or the explicit JSON schemas. Simultaneously, the design team performs a rigorous editorial audit: separating immutable facts from editorial intent. Stale authored prose attempting to describe props, broken code snippets, deprecated screenshots, and manually formatted API tables are systematically marked for deletion. What is meticulously preserved: purpose statements, when-to-use guidelines, accessibility context, tone-of-voice instructions. This legacy intent is mapped into the new MDX overlay files. **3–8 weeks for a 60-component system, 50–80 hours per week of UX Designer / UX Copywriter time.**

**Phase 2 — dual-publishing and cutover.** The new pipeline emits a parallel docs site at a different URL. The team monitors which pages still get traffic on the old site and prioritises migration accordingly. **2–4 weeks.** Once the new site reaches feature parity on editorial content, the old site is permanently retired.

### What to throw away

- **Stale authored prose** that disagrees with the current source (purpose statements no longer matching the component, when-to-use rules referencing deprecated patterns).
- **Broken examples** with missing imports or deprecated APIs.
- **Deprecated screenshots** — automatically captured screenshots are regenerated by the pipeline; manually captured variant screenshots are typically out of date.
- **Redundant prop documentation** — hand-typed prop tables that contradict the source. Always defer to the source.

### What to keep

- **Purpose / when-to-use / avoid-when content** that still aligns — most editorial content is reusable even when the technical layer has drifted.
- **Do/don't pairs** — re-screenshot the visual element, but the framing is typically still correct.
- **Content guidelines** — almost always reusable; copywriter outputs are the most-durable editorial content.
- **Architecture decision records** — historical decisions are what they are.

### The Zeroheight reality

Many design-led engagements have Zeroheight in production with substantial designer engagement. The practice's discipline:

- Keep Zeroheight as the design-side consumer surface; designers continue their workflow.
- The code-side pipeline is the authoritative source.
- Sync Zeroheight from the pipeline — the practice ships a sync job running per-merge or per-release. Zeroheight becomes a *projection* of the source rather than an independent authoring system.
- The cadence: per-merge or per-day is sufficient; real-time is rarely required.
- The failure mode: sync breaks (Zeroheight API outage, schema mismatch, rate limit). Ship a "Zeroheight sync passed at HEAD" status check separate from the build; designers see a stale Zeroheight, the practice reconciles in the next sync. **When sync fails, the code-side generated site is the definitive arbiter of truth** *(external)*.

### Migration anti-patterns

- **Discarding all existing documentation simply because it was hand-authored** — burns years of institutional knowledge about component usage constraints *(external — sharper than my framing)*.
- **Allowing legacy hand-typed prop descriptions to persist in the new MDX files** — defeats the architecture, produces immediate contradictions with the source's generated output.
- **Treating migration as engineering-only** when it is half editorial.
- **Skipping the dual-publish phase** — strands consumers on the wrong URL; no migration feedback before the old site is gone.
- **Migrating without simultaneously setting up the CI freshness checks** — the new system begins rotting the day it is deployed *(external — load-bearing)*.

---

## 6. The cluster relationship — generated documentation in the AI-readiness commercial default

Generated-from-data documentation does not stand alone. It is one of four practice deliverables that together constitute *AI-ready design system architecture* — the practice's defensible commercial position against vendor templates and incumbent consultancies.

### The four-prerequisite minimum architecture

Per 15-ai-in-ds and 25-ai-aware-patterns-and-conversational-ui:

1. **Tokens with descriptions.** Every token has a `$description` per DTCG (the W3C Design Tokens Community Group format). The descriptions are AI-readable. (See 02-design-foundations and 22-token-architecture-extensions.)
2. **Component metadata.** The `.ai.json` registry per component plus the registry aggregation. The `DESIGN.md` specification is an emerging alternative format with similar architectural intent — the practice picks one per engagement and documents the schema.
3. **Agent instructions.** `AGENTS.md` / `CLAUDE.md` at the system level and at the consuming product level. The instruction-file layer is the practice's defensible POV that no external source names by default.
4. **Figma pipeline.** Figma variables → DTCG export → Style Dictionary → Code Connect → MCP. Bidirectional where possible; unidirectional where not.

Generated-from-data documentation is the **delivery surface** for layers 1–4 to the human consumer. The same source produces:

- The docs site (human-readable, for designers, developers, executives).
- The `.ai.json` registry (machine-readable, for AI agents via MCP).
- The Figma library properties (for the design tool).
- The conformance dossier (for auditors and procurement).

### The same artefact at different altitudes

Both agents converge on this exact framing: the generated documentation site and the AI-readable metadata are not separate products requiring separate maintenance streams — they are the same artefact rendered at different altitudes. The same CI process that builds the interactive MDX props table builds the `.ai.json` (or `DESIGN.md`) and outputs the semantically chunked payload for the MCP server. When an AI agent (Atlassian's Rovo Dev CLI is the most-cited 2026 example, querying via tools like `ads_plan`) reaches the MCP server for component usage, it receives the same API constraints, token mappings, and accessibility guidelines a human reads on the documentation website *(external; tool name held as cited)*.

### The cluster of unsold IP

Per 09 §1.7 and §1.12:

- **Code Connect not defaulted.** The Figma↔code mapping that AI agents use to ground component selection. The practice has the IP; commercial proposals don't ship Code Connect bindings by default.
- **Custom MCP server / registry not commercial.** Internal POV; not yet sold.
- **`.ai.json` is in the AI-Compatible doc but not the commercial proposal.** Should ship with every component by 2027.
- **AGENTS.md / CLAUDE.md** as the instruction-file layer is unique IP; the practice can claim this layer publicly.
- **Token descriptions as a default Foundations deliverable.** Aspirational, not contractual.
- **Engineering-onboarding artefact** (per 09 §1.7) — Couldwell's `docs/decisions/`, `docs/onboarding/`, `docs/meeting-notes/`. Almost no client has them; the per-component docs pipeline produces the substrate.

These six items are a cluster: the architecture is in the vault, the proposal language isn't. The practice's commercial transition is not "ship more architecture"; it is "itemise the architecture in the SOW with defensible per-line costs and defend the package." Generated documentation is the delivery surface; the cluster is what makes it real.

### Publishing the schema

A specific recommendation that comes out of the synthesis: **the practice should publish its `.ai.json` schema as a public artefact in 2026.** No canonical schema for component AI metadata has emerged in the field. Each practice that ships AI-readiness ships its own schema; the schemas vary in completeness and field names. A published schema that the field adopts becomes the de facto standard; the practice that publishes it claims the architectural authority. The cost is low (the schema is documented internally); the strategic upside is high. The same logic applies if the practice picks `DESIGN.md` instead — published schemas establish layers.

### The pitch

The practice's offer is the *whole cluster*, not just the docs site:

> An AI-ready design system is an architecture, not a feature. The architecture has four prerequisites — tokens with descriptions, component metadata, agent instructions, and the Figma pipeline. The delivery surface that makes the architecture legible to your team is generated-from-data documentation, including a docs site, an `.ai.json` registry served via MCP, a Figma library kept in sync with the source, and a per-component conformance dossier that aggregates into your product's ACR. The practice ships the four prerequisites and the delivery surface as the engagement default. Vendor templates ship structure; we ship the architecture, the editorial discipline, the cluster of artefacts that make the structure load-bearing, and the pipeline maintenance retainer that keeps it aligned over time.

---

## 7. The commercial pitch — articulating this to clients who haven't asked for it

Most clients haven't asked for generated-from-data documentation because they don't know to. They ask for "a docs site" or, increasingly, vaguely for "an AI-ready design system" without articulating what that means architecturally.

### The procurement framing

"AI-ready design system" is the surface clients increasingly ask for. The practice's specific articulation is the four-prerequisite architecture (per §6) with generated documentation as the delivery surface. When the client says "we want our design system to work with our AI tools," the practice's response is "yes, here is what that requires architecturally, and here is the delivery surface that makes it real."

### The cost narrative

"The upfront pipeline investment is a one-time capital expenditure that pays back across the initial 30–40 components and the system's lifetime. Authored-prose docs carry an ongoing operational tax — quarterly maintenance budgets of 60–120 hours, drift accumulating at 15–25% of pages over 18 months, and an AI-readiness gap that is increasingly procurement-grade. The break-even on the pipeline is around 30 components; the lifetime savings on retainer alone are substantial."

This is a defensible commercial argument with quantifiable numbers per §3.

### The risk narrative

Without generation, three predictable failures occur within 18 months:

- **The docs and the implementation drift.** 15–25% of pages have at least one disagreement with the source.
- **The conformance dossier is reverse-engineered every audit.** The accessibility lead spends 40–80 hours per audit cycle re-validating the docs site against the implementation. This is expensive and legally risky as EAA enforcement matures *(external — sharp procurement-grade framing)*.
- **The AI tools your team uses cannot reliably reach the system.** Cursor / Copilot / Claude Code generate code that uses hardcoded values, invents component names, ignores composition rules. The system's adoption rate against AI-generated work plateaus.

These are not theoretical; they are observed across the practice's portfolio. The risk narrative converts "nice-to-have" into "we'd rather pay for it now than the consequences later."

### The competitive narrative

Vendor templates (Zeroheight, Supernova, Knapsack out-of-the-box) ship structure. The practice ships the architecture, the editorial discipline (the authoring seam), and the integrated cluster of artefacts (per §6) that make the structure load-bearing. Tools provide the database; the practice provides the schema, the semantic intent, the accessibility rigor, and the governance mechanisms. Clients who pick a vendor template without the editorial layer ship empty rooms; clients who pick the practice can host on free / self-hosted infrastructure.

Selling a "docs site" commoditises the work and invites price comparison with basic offshore development. **Selling the "AI-Ready Design System Architecture" — where human documentation, Figma mapping, and LLM context are continuously generated from a single source of truth — establishes a defensible, premium market position that external competitors cannot easily replicate** *(external — sharp commercial framing worth keeping)*.

### Phased adoption

Clients who can't take the full pipeline at engagement start adopt incrementally:

- **Phase 1 — Storybook autodocs + MDX template + CI freshness checks + `.ai.json` schema.** ~50–80 hours of upfront pipeline. Defers MCP and Figma sync. The technical layer is generated; the AI-readable layer exists in registry form but isn't served via MCP yet. Gets the practice 70% of the way to the full architecture.
- **Phase 2 — Code Connect integration + Figma library sync.** Adds ~25–50 hours. Closes design-side drift.
- **Phase 3 — Custom DS MCP server + `.ai.json` registry served via MCP.** Adds 40–80 hours. Closes the AI-readable layer.

Most engagements land Phase 1 in the initial commercial proposal and Phase 2/3 in retainer or follow-on engagements. The phased shape lets clients accept the architecture without paying the full upfront cost on day one; the practice retains the defensible commercial position because the architecture is the same regardless of phase order.

### Objection handling

**"We just want a docs site."** Two responses depending on engagement shape:

1. *Scope down explicitly.* "Yes — we can ship a docs site. It will be authored-prose, will not include the AI-readable layer, will require quarterly maintenance, and will not produce conformance evidence by default. Here is the smaller scope, here is the price, and here is the upgrade path when you're ready." Retains the relationship; surfaces the architecture as a future option.

2. *Walk away if the client is also asking for AI-tool integration.* "What you're describing is two contradictory requirements. We can ship one, but not both. Let's reset the conversation." The practice does not ship an AI-integration commitment on top of an authored-prose substrate — the resulting deliverable is unreliable and the engagement ends badly.

**"Our team already uses Notion / Confluence / GitBook."** The migration playbook (§5) handles this. Migration is a Discovery deliverable that decides whether to retire the legacy tool or run it in parallel.

**"This is more engineering than we budgeted."** The cost-vs-savings argument (§3) addresses this. Where the math doesn't work (small system, single consumer, short lifetime), the decision framework (§4) returns "authored prose is acceptable" honestly and the practice scopes down.

**"Our designers won't use Storybook."** The hosted design-side surface (Zeroheight synced from the pipeline per §5) addresses this. The technical layer is generated; the design surface is hosted; designers use the surface they're comfortable with.

**"We want everything in Figma."** The Figma sync direction is the answer; the practice ships Code Connect plus a Figma library kept current via per-merge sync.

---

## 8. Anti-patterns and tooling realities — where the field is genuinely behind in 2026

The practice should be honest about where the architecture works and where it doesn't.

### "Storybook autodocs alone is enough"

Storybook autodocs ships the props table, the controls panel, and the canvas — the developer-facing technical layer. It does not ship the AI-readable `.ai.json`, the typed relationship graph, the conformance dossier, or the Figma sync. Teams that adopt Storybook autodocs and stop are 30% of the way there. The remaining 70% — the AI layer, the design-side sync, the conformance aggregation — is what closes 09 §1.10 and §1.12. Ship Storybook autodocs as the foundation, but explicitly scope the additional pipeline layers as separate deliverables.

### "Generate everything including intent"

The failure mode where the LLM authors purpose, when-to-use, and avoid-when prose. The result is dangerously generic, frequently hallucinates business rules, and misses the subtle constraints of the specific enterprise domain *(both agents — load-bearing)*. The example external offers: an LLM might confidently state a red button is for "destructive actions," missing that in a healthcare system red specifically denotes "critical patient alert."

The discipline per 29 §3 and §1 above: intent is authored, not generated. AI assistance during authoring is plausible (the generator suggests draft `avoid_when` entries based on adjacent components' usage), but the human author is the decision-maker and the source-of-truth for editorial content.

### Monorepo tooling failures

`react-docgen-typescript` frequently breaks in Turborepo, Nx, and Vite workspaces when dealing with cross-package inheritance. Components extending an interface from a different package root produce empty prop tables or types resolving to obscure object types instead of specific literals *(external — practitioner-tier specificity)*. The workaround: enforce strict direct-source import paths across the monorepo, or write custom plugins (Vite plugins manually resolve the AST) that resolve the inheritance correctly. The hours impact is real — this can add 8–24 hours of pipeline-setup time on a complex monorepo.

### The complex-multi-variable-state cliff

Automated state rendering for compound states (`selected + focused + server-error` data-grid cells; `loading + error + read-only` form fields) is fragile in 2026. Storybook controls handle binary states cleanly; multi-variable combinations require explicit story declarations and screenshots typically need manual regeneration. The practitioner workaround: generate base states algorithmically; hand-author visual examples for high-complexity multi-variable edge cases; mark the generated vs. authored split in the docs page so consumers know which is which. The component-type-specific extensions in 29 §2 (forms need a validation-state matrix; data-grids need a row-state matrix) carry the authored portion.

### The Figma sync seam and Code Connect asymmetry

Design-side libraries do not yet pull from the same source automatically. Code Connect 1.x for React is Baseline-grade; Code Connect for iOS (SwiftUI), Android (Jetpack Compose), Flutter, and HTML Web Components is materially less mature regarding complex variant mapping and dynamic property resolution *(external — sharp framing of the asymmetry)*. Cross-platform systems collide with this — the React side gets full Code Connect; the non-React side requires manual intervention via `figmaApply` helpers in Swift or Kotlin to maintain sync.

The mitigation: treat the Figma library as a deploy artefact, not an authored artefact. Every system release ships a Figma library update. The drift window is bounded by the release cadence rather than allowed to accumulate.

### The `.ai.json` / `DESIGN.md` standards reality

No canonical schema for component AI metadata has emerged in the field. `.ai.json` is internal-tier IP for many practices; `DESIGN.md` is an emerging spec that may stabilise. As of mid-2026 the field has not converged. The practice's discipline: pick one format per engagement, document the schema as practice IP, and revisit when the field's standardisation story settles. **Publishing the practice's schema is the move that establishes the layer** — a published schema the field adopts becomes the de facto standard, and the practice that publishes it claims the architectural authority.

### Zeroheight's API maturity

Zeroheight's API for generated content has matured significantly through 2025–2026 but remains constraining. Zeroheight's data model is opinionated about what a component page contains; the 17-section template per 29 has to map onto Zeroheight's default sections plus custom blocks. The mapping is feasible but lossy; some sections (the conformance dossier in particular) don't fit Zeroheight's model cleanly. The mitigation: treat Zeroheight as a *design-consumer* surface emphasising the sections designers consume (summary, examples, do/don't, accessibility), with the full template living on the code-side MDX site and Zeroheight linking back for technical depth.

### Authoring tooling that cannot consume the source

Notion, Confluence, GitBook cannot consume the generated source at all. Teams that have invested in these tools face a hard migration (per §5). The practice should not pretend this is a soft transition — it is a tool replacement, with the associated change management.

### The MCP server tooling reality

Building a custom DS MCP server in 2026 is a 40–80-hour project. The MCP specification (revision 2025-06-18 with subsequent revisions through early 2026) is stable enough to build against; the field does not yet have a turnkey "DS MCP server" the practice can ship as a vendor selection.

The practitioner approach: build it once, reuse it across engagements. The MCP server is a piece of practice IP that compounds in value across the portfolio. Each engagement adapts the schema, the registry build, and the client-specific configuration; the core server architecture is portable. The recommendation: invest the 40–80 hours once in a reference MCP server implementation; ship it as a Foundations-tier deliverable on subsequent engagements. The first engagement bears the full cost; the second engagement onwards reuses the implementation. **This is the durable engineering investment that pays back across the practice's portfolio.** (The custom DS MCP server is the *productisation surface* — billable per engagement, transferred to the client at handoff. The complementary surface is the senior practitioner's *workstation MCP stack* — Figma Dev Mode + Console MCP, Storybook MCP, axe-core, Style Dictionary wrapper, firecrawl, one search MCP — which is general-purpose, agency-internal, career-amortised, and never billed. The two layers compose; 34-mcps-for-ds-practice covers the workstation stack as the standardisation companion to this productisation argument.)

### Silent extraction failure as the failure to fear

If metadata extraction silently fails — empty prop table, unresolved inheritance, schema validation that wasn't strict enough — the drift goes unnoticed until the AI agent hallucinates an API during code generation. **Strict schema validation before merge is the only reliable mitigation** *(external — load-bearing).* The CI freshness check plus the schema validation plus the registry validation are the three rules that together prevent the silent-failure path. Skipping any one of them returns the system to authored-prose's drift profile.

---

## See also

For the documentation strategy this generation pipeline operationalises, see 04-documentation.

For the per-component template the pipeline produces, see 29-per-component-documentation-template.

For the components-as-data substrate that the pipeline assumes, see 03-component-library and 15-ai-in-ds.

For the accessibility schema the pipeline emits as part of the conformance dossier, see 17-accessibility-annotation-contract, 16-mobile-accessibility-implementation, and 28-web-accessibility-implementation.

For the semver discipline the pipeline applies at the component layer, see 24-tokens-at-scale.

For the maintenance retainer shape the lifetime cost argument depends on, see 08-ongoing-maintenance.

For the practice gaps this file addresses — generated-from-data as commercial default (residual gap from 09 §1.10), AI-readiness as commercial default (09 §1.12), Code Connect not defaulted, custom MCP server / registry not commercial, engineering-onboarding artefact (09 §1.7) — see 09-gaps-and-open-questions.

---

## Provenance

Synthesis of the dual-agent research run filed 2026-06-13 (`_research/_inbound/2026-06-13-generated-from-data-docs/`). The two agents converged substantively on every load-bearing claim — the architectural decision, the five generation targets, the CI surface, the file structure, the authoring seam discipline, the per-component hours redistribution shape, the ~30-component break-even, the 5-question decision tree (with external's 3-of-5 threshold absorbed), the two-phase migration playbook, the four-prerequisite minimum architecture, the same-artefact-at-different-altitudes framing, the phased adoption, and the anti-patterns. Where they diverged, the synthesis applied judgement: external's MCP server hours range and Capex/Opex framing are absorbed; external's `DESIGN.md` reference is included as one option alongside `.ai.json` with the caveat that no canonical AI-metadata format has fully emerged; external's quantitative claims (92% retrieval accuracy, 88% token reduction, 70% maintenance reduction over 3-year lifecycle, 27-component break-even) are held as cited rather than asserted, with the directional argument being the load-bearing claim; external's monorepo-tooling specifics (`react-docgen-typescript` failures in Turborepo / Nx / Vite, the `figmaApply` helpers in Swift/Kotlin, `sveld` for Svelte, Adobe Spectrum's JSON Schema as exemplar, Atlassian Rovo Dev CLI with `ads_plan` tool name) are absorbed; external's "silent extraction failure" framing as the failure to fear is absorbed; the per-component hours range was widened beyond either agent's individual range to 2–8 hours per component, distributed by complexity; the upfront pipeline cost is held as a Phase 1 / Phase 1+2 / Phase 1+2+3 split rather than a single point; the framework-native + explicit-data + framework-native-with-metadata three-way source format choice (Claude) is preferred over external's two-way; the 17–62 sensitivity range on break-even (Claude) is preserved alongside external's 27-component point estimate. Closes the residual generated-from-data gap from 09-gaps-and-open-questions §1.10 (per-component template was closed by 29; this file closes the substrate-as-default residual). Partially closes §1.7 (Code Connect not defaulted, custom MCP server not commercial, engineering-onboarding artefact) and §1.12 (AI-readiness as commercial default) — the file articulates the commercial pitch and the phased adoption path, but the deliverables themselves still depend on the next engagement actually shipping them.

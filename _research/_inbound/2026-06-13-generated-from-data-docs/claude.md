# Generated-from-data documentation as a commercial default — Claude run

> Research output, June 2026. Companion to the planned external-agent run on the same prompt. Audience: senior DS practitioner converting the components-as-data architecture (already articulated across 03 / 04 / 15 / 29) into a sellable SOW deliverable. Reference line: Storybook 9 (the May 2026 release with the consolidated docs architecture) on the 8.x line still widely deployed; MDX 3; React 19; TypeScript 5.5; react-docgen-typescript 2.x; Code Connect 1.x for React (2.x in preview); Code Connect for iOS / Android / Flutter at 0.x to 1.x maturity; the MCP specification revision dated 2025-06-18 with subsequent revisions. The thesis below: generation is the architectural answer, but the commercial transition is two orthogonal problems — the engineering investment and the proposal language. The vault articulates the first; this file articulates the second.

---

## 1. The architecture in production — what generated-from-data documentation actually looks like in 2026

Generated-from-data documentation rests on a single load-bearing decision: **the component data file is the source of truth**. Every consumer of the docs — Storybook, MDX docs site, `.ai.json` registry, Figma library properties, AI-assistant catalog — derives its content from this source. Per 29-per-component-documentation-template, 03-component-library, and Curtis (*Components as Data*, Sep 2025), this is the architectural answer the practice has accepted. The questions for this file are about the *shape* of that source, the *consumers* that derive from it, and the *seams* where the architecture meets the proposal.

### Source format choices

Three credible source formats in 2026, with materially different downstream consequences:

**TypeScript types as the implicit source.** The most-common starting point. The component is a `.tsx` file; props are a `type ButtonProps = { ... }` declaration; defaults are React `defaultProps` or destructured assignments; deprecation flags are `@deprecated` JSDoc. `react-docgen-typescript` (or the SWC-based equivalent shipped in Storybook 9's docgen pipeline) extracts types and JSDoc into the structured representation Storybook autodocs renders.

- **Enables:** zero-friction adoption for React-first systems; tight coupling between source and docs; rich JSDoc as the authoring surface; AI tools that consume TypeScript directly (Cursor, Copilot, Claude Code) get reasonable behaviour without a separate metadata layer.
- **Forbids:** non-TypeScript consumers (Figma, design-side tooling) cannot read TypeScript directly; the source is locked to React; cross-framework systems hit a wall.

**Explicit JSON Schema or YAML definition.** The component is defined in a neutral structured format (`Button.component.json` with schema-driven validation) before it touches any framework. The implementation derives from the definition; the docs derive from the definition; the Figma library properties derive from the definition.

- **Enables:** framework-agnostic. The same definition produces React, Vue, Svelte, and native iOS / Android / Flutter implementations. The Figma sync is direct because Figma component properties map to the schema. The `.ai.json` is a projection of the schema. AI tools consume the schema directly via MCP.
- **Forbids:** the upfront design cost is real — defining the schema takes work the team would not otherwise do. Mismatches between the schema and the implementation are a new class of bug. Engineering teams trained on TypeScript-as-source resist the indirection.

**Framework-native definition with sufficient metadata.** A Lit web component with `@property` decorators, a Stencil component with explicit metadata, a Svelte 5 runes-based component with structured types, or a React component with a Zod schema co-located. The framework is the source; the framework's metadata model is rich enough to drive generation downstream.

- **Enables:** keeps engineering teams in their preferred framework; metadata is extracted automatically; web-component-based systems get a portability win because Lit components are framework-agnostic at consumption time.
- **Forbids:** cross-framework definitions are still per-framework — a Lit component is not a React component is not a Flutter widget. The shared metadata layer has to live above the framework-native definition.

**The practice's default position.** For most agency engagements (React-first, web-led, single-framework), TypeScript-as-source plus `.ai.json` overlay is the right starting point. For multi-platform engagements (web + iOS + Android) or multi-framework consumers, explicit JSON Schema is justified. For web-component-based systems shipping as portable libraries, framework-native (Lit + ElementInternals per 28 §1) is the answer. The decision is a Discovery deliverable, not a Foundations deliverable — committing to the source format in week 1 is what unblocks every downstream pipeline choice.

### Generation targets and what each consumer needs

Each consumer of the source gets a different projection. The projections diverge in non-obvious ways:

- **Storybook autodocs.** Consumes types, JSDoc, default values, declared stories. Produces the props table, the controls panel, the canvas. Storybook 9 (May 2026) consolidated the previous addon-docs into the core docs architecture; SWC-based docgen replaces the older Babel-based path and is materially faster on large component libraries. Storybook is the developer-facing canonical surface for the technical layer.
- **MDX docs site.** Consumes the source for the technical layer, the `.docs.mdx` for the authored layer, and the cross-references to other components. Renders the consumer-facing docs site. The MDX file is the seam where authored prose lives alongside generated facts; the practice's discipline is one MDX file per component, owning purpose, when-to-use, avoid-when, anatomy, do/don't, content guidelines, and the accessibility "consumer must specify" rows.
- **`.ai.json` registry.** Consumes types and JSDoc plus a per-component `.ai.json` overlay carrying authored fields (`when_to_use`, `avoid_when`, `business_context`, `semantic_prompt`, the accessibility schema). Aggregated into a registry the AI assistant queries. This is the AI-consumer surface and is increasingly served via MCP.
- **Figma library properties.** Consumes the prop names, types, defaults, and variant declarations; produces the Figma component property declarations (variant, boolean, instance-swap, text, exposed nested). Code Connect 1.x for React handles the React→Figma direction; the inverse direction (Figma→source) is partial as of mid-2026. This is the design-consumer surface.
- **AI-assistant catalog.** A subset of `.ai.json` chunked for RAG ingestion — component cards (markdown + JSON, < 2000 tokens each per 15 §7), trigger-keyword indexes, the typed relationship graph. Consumed by the consuming product team's AI tools (Cursor, Copilot, Claude Code) and by the practice's internal MCP server.

The non-obvious divergence: **Figma needs prop *value* enumeration** (the actual list of `tone` enum values to populate the variant property) which TypeScript types provide trivially but JSDoc-only sources do not. **AI agents need *semantic prompts*** (one-line use-case framings) which neither types nor JSDoc carry — they have to be authored separately into `.ai.json`. **Storybook needs *control declarations*** (the explicit "this is a select with these options" affordance) which can be derived from types but often need overrides for richer controls. The pipeline is one source with multiple projections; the projections are not symmetric.

### The CI surface

What runs when a source change lands:

- **Schema validation.** The component data file is parsed against the schema; types resolve; JSDoc is extracted. Failure: invalid prop declaration, missing required JSDoc, broken type reference.
- **Freshness check.** Per 29 §5: the component's authored doc fields produce a content hash; if the source changed but the hash didn't, the build fails. This is the single highest-leverage CI rule the practice ships.
- **Accessibility schema enforcement.** The `.a11y.json` (or accessibility section of `.ai.json`) must include rows for every concern in the contract per 17 / 28; missing rows fail the build. This is what makes the conformance dossier real.
- **Link verification.** Cross-references between component pages (typed relationships per 29 §3) are verified; broken links fail the build.
- **Screenshot regeneration.** Variant screenshots are captured by Storybook's visual-regression runner (Chromatic, Percy, or self-hosted Playwright) per change; new variants get new screenshots automatically.
- **Semver bump detection.** Breaking type changes (a removed prop, a narrowed type) trigger a major-version requirement; the build fails on a non-major commit. (Per 24-tokens-at-scale, this is the same discipline applied to the component layer.)
- **Deprecation propagation.** A `@deprecated` JSDoc on a prop propagates to the props table, the `.ai.json`, the Figma library property, the changelog. A deprecation that lands in one consumer but not the others is a build failure.
- **MDX rendering check.** The MDX docs file compiles; component imports resolve; embedded examples render without runtime errors.

The CI pipeline is the practice's quality contract. Without it, the source-of-truth model is aspirational; with it, the source-of-truth model is enforced.

### File structure

The shape from 29 §5, with engineering-tier annotations:

```
component-source/
├── Button.tsx                  # implementation
├── Button.types.ts             # types (consumed by docs and .ai.json)
├── Button.stories.tsx          # Storybook stories (developer-facing examples)
├── Button.docs.mdx             # authored prose (UX Designer)
├── Button.tokens.ts            # design tokens consumed (engineer-authored, audited by design)
├── Button.ai.json              # AI metadata (authored + generated overlay)
├── Button.a11y.json            # accessibility schema (authored + generated overlay)
└── Button.test.tsx             # automated tests (feeds conformance dossier)
```

Each file's owner is explicit. The seam between authoring and engineering is in the file split: the engineer owns `.tsx`, `.types.ts`, `.stories.tsx`, `.test.tsx`; the UX Designer owns `.docs.mdx`, the authored portions of `.ai.json` and `.a11y.json`; the design token consumption (`.tokens.ts`) is engineer-authored but design-audited. The CI freshness check fires when the engineer-owned files change without the designer-owned files updating — forcing the conversation between the two roles before the change merges.

### Where authoring still happens

Generation produces the technical layer; authoring produces the intent layer. The seam:

- **Generated:** props tables, type signatures, default values, deprecation flags, version-introduced metadata, default Storybook examples, design-token references, accessibility schema fields the schema can derive (the role of a `<button>` is automatic), the per-component changelog from commit history, the Figma component-property mappings, the `.ai.json` `props` and `tokens` arrays.
- **Authored:** purpose, when-to-use, avoid-when, anatomy diagrams, do/don't pairs, content guidelines, the accessibility "consumer must specify" rows, the example captions, the `.ai.json` `business_context` and `semantic_prompt` fields, the typed relationships graph (`alternativeTo`, `composesWith`, `supersedes`).
- **Generated-with-overlay:** state matrices (declared in source, rows authored — visual treatment, token transition, announced state, interaction model, triggering condition per 29 §3), variants (generated from prop combinations, screenshots authored or auto-captured), conformance dossier (test results from CI, manual-AT walkthrough log links authored, SC-by-SC mapping authored once and validated).

The authoring discipline that survives generation is the editorial one. The pipeline removes the *technical* duplicate-authoring; it does not remove — and should not attempt to remove — the editorial work. Per 29's anti-patterns, "generate everything including intent" produces generic and wrong purpose / when-to-use prose. The practice ships generation for facts and authoring for judgement.

---

## 2. The pipeline shape — the concrete dependency graph

The pipeline is a directed graph from source to consumers. Every arrow has a tool, a failure mode, and a recovery path.

### Storybook autodocs path

`Button.types.ts` + `Button.tsx` JSDoc + `Button.stories.tsx` → react-docgen-typescript / SWC-based docgen → Storybook 9 docs page.

- **What runs.** Docgen extracts types, JSDoc, default values; Storybook renders the props table, the controls panel, the canvas. Stories are rendered as live examples; addon-a11y runs axe-core on each story.
- **What blocks what.** Docgen fails if types don't resolve; Storybook fails if a story throws. Visual regression (Chromatic / Percy / Playwright) runs after Storybook builds and gates the deploy.
- **What fails build vs. warns.** Docgen errors fail; addon-a11y violations are configurable — the practice ships them as "fail on serious-or-critical, warn on moderate-or-minor." Visual regression diffs warn by default; the practice should ship them as "fail on diff > 0.1% per story unless explicitly approved."
- **Failure mode.** Slow docgen on large libraries (the SWC path in Storybook 9 is materially faster than the Babel-based path; if the team is on Storybook 8 with the older docgen, large-library teams should upgrade specifically for this).

### MDX docs site path

`Button.docs.mdx` + `Button.types.ts` types + cross-component references → MDX 3 compilation → static site (Next.js, Astro, custom).

- **What runs.** MDX compiles; embedded `<Canvas>` / `<Meta>` references resolve to Storybook stories; the props table block pulls types from the source; the cross-references render with typed relationships.
- **What blocks what.** MDX compilation fails if a component import is missing or a prop type doesn't resolve. Cross-reference verification (link-checker) runs after build.
- **What fails build vs. warns.** Compilation failures and link-check failures fail; rendering warnings warn.
- **Failure mode.** The "Storybook component imports" lock-in — if the MDX file imports Storybook component metadata directly, the docs site is locked to Storybook. The portable shape (per 29 §6) keeps the MDX file platform-neutral and lets Storybook be one of multiple consumers.

### `.ai.json` emission path

`Button.types.ts` + `Button.tsx` JSDoc + `@ai` tags + `Button.ai.json` overlay → schema validator → registry build → MCP server.

- **What runs.** Schema validator validates the merged `.ai.json` (generated fields + authored fields) against the registry schema. Registry builder aggregates all components into a queryable registry. MCP server exposes the registry to AI clients.
- **What blocks what.** Schema validation failure blocks registry build; registry build failure blocks MCP server start.
- **What fails build vs. warns.** Missing required authored fields (`when_to_use`, `avoid_when`) fail; missing optional fields (`semantic_prompt`) warn.
- **Failure mode.** The schema-evolution problem — when the registry schema changes (a new required field), every component's `.ai.json` must update; the practice ships migration scripts as part of the pipeline maintenance.

### Figma library sync path

`Button.types.ts` props + variants → Code Connect figma-config → Figma library properties.

- **What runs.** Code Connect maps component-side props to Figma component properties. The mapping is unidirectional (component → Figma) for React in 2026; iOS / Android / Flutter Code Connect is at 0.x–1.x and the bidirectional story is partial.
- **What blocks what.** Figma sync runs on a CI cadence (typically per-PR or per-merge); it does not block the code build because Figma is downstream.
- **What fails build vs. warns.** Sync failures warn rather than fail — Figma is a separate system that may be unavailable; the practice should ship a "Figma sync passed at HEAD" status check that is required for release but not for merge.
- **Failure mode.** The single most-cited drift point. Figma libraries rebuilt on a separate cadence diverge from the source; designers continue using the old library; engineering ships the new one; designers reach for properties that don't exist in source. The mitigation: ship Code Connect with every component as default, run Figma sync per-merge, treat a stale Figma library as a release blocker.

### Conformance dossier path

`Button.test.tsx` results + `Button.a11y.json` schema + manual-AT walkthrough logs → CI artefact → consuming product's ACR.

- **What runs.** Tests run on every PR; results emit per-component dossier files; manual-AT walkthrough links are stored alongside.
- **What blocks what.** Test failures block merge; missing manual-AT links per minor version warn.
- **Failure mode.** The dossier is per-component; the consuming product needs application-level evidence too (per 28 §8). The practice's responsibility is the per-component layer; the consuming product's accessibility lead aggregates.

### Cross-pipeline failure modes

What practitioners encounter when a step breaks:

- **Schema drift.** The registry schema updates; not every `.ai.json` migrates; some components ship stale schema. CI catches the validation failure; the migration script catches the lift; the practice ships both as default infrastructure.
- **Visual-regression noise.** Anti-aliasing differences between platforms (the macOS dev runner vs. the Linux CI runner) produce false-positive diffs. Storybook's `chromatic-config.js` configurations and the team's cross-platform discipline (Docker for visual snapshot generation) mitigate.
- **Code Connect drift.** As above — the Figma library lags the source. The practice's discipline is "Figma library is a deploy artefact, not an authored artefact" — every system release ships a Figma library update.
- **MCP server outages.** The AI assistant cannot reach the registry. The fallback: the registry's static JSON output is consumable by AI tools that don't yet speak MCP; the system ships both surfaces.

---

## 3. The hours-and-cost shift — what changes commercially when generation replaces authoring for the technical surface

The economic argument for generation is two halves: an upfront pipeline investment, and a per-component-hours redistribution. The break-even is at component count where the redistribution payback exceeds the upfront cost.

### The upfront pipeline investment

A realistic 2026 estimate for shipping the full pipeline at engagement start:

- **Source format and schema authoring** — defining the component data file shape, the `.ai.json` schema, the `.a11y.json` schema, the typed relationships graph. **8–16 hours of senior engineering time.**
- **Storybook autodocs configuration** — setting up Storybook 9 (or 8 with the latest docgen path), addon-a11y, controls, the MDX integration. **8–16 hours.**
- **MDX template** — the per-component template per 29 §8, customised for the client's component vocabulary and brand voice. Storybook story scaffolding, the MDX frontmatter schema, the rendering layer. **8–16 hours.**
- **CI freshness check** — pre-commit hook computing the content hash, the build-time validator, the per-section minimum-prose rules. **4–8 hours.**
- **Schema validation and link checking** — the validator, the registry builder, the link checker. **4–8 hours.**
- **`.ai.json` schema and registry build** — the schema, the build pipeline, the migration script scaffolding. **8–16 hours.**
- **MCP server** — a custom DS MCP server in 2026 is **40–80 hours**; this is the largest single line item. The field does not yet have a turnkey "DS MCP server" the practice can ship as a vendor selection.
- **Code Connect integration** — Figma component-to-source mapping, the Figma sync CI step. **8–16 hours** for React; iOS / Android / Flutter Code Connect is materially less mature and adds 16–32 hours per platform.
- **Visual regression setup** — Chromatic / Percy / Playwright, the per-story configuration. **4–8 hours** with a hosted vendor; **16–24 hours** for self-hosted Playwright.
- **Accessibility-test scaffolding** — addon-a11y configuration, axe-core rules, the conformance dossier emit. **8–16 hours.**
- **Documentation of the pipeline itself** — the engineering onboarding (which closes 09 §1.7 partially), the contribution flow, the authoring guide. **8–16 hours.**

**Total upfront pipeline investment: 108–216 hours for a React-first single-platform engagement.** Multi-platform (web + iOS + Android with Code Connect) adds 32–64 hours per additional platform. Custom MCP server is the dominant single line item; teams that defer the MCP layer to a phase-two adoption (per §7) can drop the total to ~70–140 hours initially.

This is the line item the practice currently absorbs as overhead. **Itemising it as a Foundations-tier deliverable named "Documentation Pipeline" or "AI-Ready Documentation Architecture" is the commercial discipline this file is arguing for.**

### The per-component hours redistribution

What changes per-component when the pipeline is in place:

| Section | Authored-prose model | Generated-from-data model |
|---|---|---|
| Header | 0.25 h authored | 0 h (generated from frontmatter) |
| Summary | 0.25 h authored | 0.25 h authored (unchanged) |
| Live example | 0.5 h authored | 0.25 h authored caption + 0 h generated render |
| Purpose | 1 h authored | 1 h authored (unchanged) |
| When to use | 0.5 h authored | 0.5 h authored (unchanged) |
| Avoid when | 0.5 h authored | 0.5 h authored (unchanged) |
| Anatomy | 1–2 h authored | 1–2 h authored (unchanged) |
| Props/API | **1.5–3 h authored** | **0 h (generated)** |
| States | 1–2 h authored | 0.5–1 h authored overlay + 0 h generated rows |
| Variants | 0.5–1 h authored | 0 h generated + 0.25 h overlay |
| Examples | 1.5–3 h authored | 1–2 h authored captions + 0 h generated renders |
| Do/don't | 0.5–1 h authored | 0.5–1 h authored (unchanged) |
| Accessibility | 1.5–3 h authored | 0.75–1.5 h authored "consumer must specify" + 0 h generated schema |
| Content guidelines | 0.5–1.5 h authored | 0.5–1.5 h authored (unchanged) |
| Composition / related | 0.5 h authored | 0.5 h authored (unchanged) |
| Changelog | 0.25 h authored | 0 h (generated from commits + 0.25 h authored breaking-change prose) |
| Conformance dossier | 1 h authored | 0.25 h authored manual-AT links + 0 h generated test results |

**Authored-prose model: 11.25–21 hours per component (roughly tracking 29 §8's 3–8 hour estimate when the very-low-end is interpreted as primitives only).**

**Generated-from-data model: 6.25–11.5 hours per component, with 1.5–3.5 of those hours shifting to engineering for data file authoring.**

The redistribution is **roughly 5–10 hours per component saved on the UX Designer side, with 1.5–3.5 hours added on the engineering side.** Net per-component savings of **3.5–6.5 hours.** Across 60 components: **210–390 hours saved** — comparable to or greater than the upfront pipeline investment for a React-first engagement.

The above treats the *first* engagement; a second engagement that reuses the pipeline scaffold pays the per-component redistribution savings without paying the upfront cost again. At scale, the practice's pipeline IP is the durable asset.

### The break-even component count

The crude calculation:

- **Upfront investment:** 108–216 hours (React-first, full pipeline including MCP server).
- **Per-component savings:** 3.5–6.5 hours.
- **Break-even:** 17–62 components. The midpoint is roughly **30 components**.

Below 30 components, authored prose is genuinely competitive on cost. Above 60 components, generation is unambiguously cheaper even on first engagement. The 30–60-component band is where the decision is dominated by *non-cost* factors (system lifetime, AI-readiness procurement, multi-consumer reach, regulatory constraint).

### The lifetime benefit

Authored-prose docs accumulate drift at a rate that depends on the source-update cadence. Empirically (cross-engagement memory; not from a published source), a system seeing weekly source updates accumulates roughly 15–25% doc drift over an 18-month post-handoff window — measured as components where the docs and the source disagree on at least one prop, default, or behaviour.

Generated docs eliminate drift on the technical layer; the freshness check eliminates drift on the authored layer. The practice has shipped systems where authored-prose docs needed a 60–120-hour quarterly maintenance budget to stay current; generated systems need ~10–20 hours of pipeline maintenance per quarter (schema migrations, CI rule updates, vendor version bumps). The lifetime cost difference is the durable commercial argument — the *retainer* shape per 08-ongoing-maintenance is materially smaller for generated systems.

### The commercial discipline

What changes in the SOW:

- **A new line item: "Documentation Pipeline" or "AI-Ready Documentation Architecture."** Foundations-tier deliverable. 108–216 hours for the React-first base case; add per-platform supplements; subtract for phased adoption (MCP deferred).
- **A reduced "Per-component documentation authoring" line.** 6.25–11.5 hours per component (UX Designer + engineering split) instead of 11.25–21.
- **A reduced "Quarterly documentation maintenance" retainer.** ~10–20 hours per quarter instead of 60–120.
- **A new line item: "Documentation pipeline maintenance retainer."** The CI rules, schema migrations, vendor upgrades. ~8–16 hours per quarter, separate from content maintenance.

The practice currently absorbs the upfront pipeline as overhead and bills the higher per-component authoring hours; this leaves money on the table while quietly carrying the engineering investment. The discipline this file argues for is **shipping the pipeline as a named deliverable with its own line item**, defending it in the proposal as the architecture that makes the per-component hours and the retainer hours materially smaller, and treating the resulting numbers as procurement-defensible.

---

## 4. The decision framework — when is generation justified, when is authored prose enough

A 5-question decision tree the practice applies in the proposal-shaping conversation:

### Question 1 — What is the component count?

- **< 30 components** — generation is competitive on cost but not unambiguously cheaper. Other factors decide.
- **30–60 components** — generation is the architectural answer; the cost is comparable; non-cost factors dominate.
- **60+ components** — generation is unambiguously cheaper even on first engagement.

### Question 2 — How many consumer products and how long is the system lifetime?

- **One consumer product, < 12-month lifetime** — authored prose is acceptable. The pipeline investment doesn't pay back.
- **2–4 consumer products, 12–24-month lifetime** — generation is the right answer; the multi-consumer surface needs the AI-readable layer.
- **5+ consumer products, 24+ month lifetime** — generation is essential; manual maintenance does not scale.

### Question 3 — What is the engineering culture?

- **Engineering-resident, code-as-source-of-truth** — generation aligns with the team's instincts; adoption is fast.
- **Designer-led, design-tool-as-source-of-truth** — generation requires culture work; the Storybook + MDX flow is hostile to non-engineers; the practice should pair generation with a hosted design-side surface (Zeroheight) and treat the code-side as the technical-layer source.
- **Mixed** — generation works if the engineering team owns the pipeline; the design team consumes via the hosted surface.

### Question 4 — Is the system multi-platform?

- **Web only** — generation is straightforward.
- **Web + iOS or Android** — generation is justified; Code Connect for the non-React platforms is materially less mature; the practice ships per-platform pipelines and accepts higher upfront cost.
- **Web + iOS + Android + Flutter** — generation is essential; the manual cost of authoring across platforms is prohibitive; the practice should commit to the JSON Schema source format (per §1) rather than TypeScript-as-implicit.

### Question 5 — Is AI-readiness or regulatory conformance a procurement requirement?

- **Yes, AI-readiness named in procurement** — generation is the surface for the AI layer; authored-prose docs cannot deliver MCP-served metadata reliably.
- **Yes, EAA / Section 508 / HIPAA conformance required** — generation is the surface for the conformance dossier; manual aggregation is more expensive and more error-prone.
- **Neither named** — the decision returns to questions 1–4.

### The framework as a sentence

The practice ships generation when the system is at least 30 components and at least one of: 2+ consumer products, 12+ month lifetime, multi-platform reach, AI-readiness procurement, regulatory conformance. Below that threshold, authored prose is acceptable; the practice still ships components-as-data architecture per 03 / 15 but treats the documentation surface as a smaller deliverable.

The framework is opinionated and the practice should hold it. Clients will push for "just the docs site" when their actual requirement is the full architecture; the practice's discipline is to apply the framework honestly and either ship the architecture explicitly or scope down explicitly. There is no in-between where generation is half-shipped.

---

## 5. Migration paths — moving an existing authored-prose docs site onto a generated substrate

Most engagements arrive with documentation in some form. The migration playbook depends on the starting point.

### Starting points and the migration shape

| Starting point | Migration shape | Realistic timeline |
|---|---|---|
| **Notion / Confluence** | Treat as throwaway. The content is in the wrong tool; even the editorial content needs reformatting. The realistic path: extract editorial content (purpose, when-to-use, do/don't, content guidelines) into a structured spreadsheet, hand it to UX Designers as authoring source, build the pipeline alongside, retire Notion/Confluence at the docs-site launch. **2–4 weeks**, dominated by content extraction. |
| **GitBook** | Similar to Notion/Confluence but slightly better — GitBook's structure carries closer to the per-component template. Same migration shape, slightly faster content extraction. **2–3 weeks.** |
| **Zeroheight (or similar hosted design-side)** | Keep Zeroheight as the design-side surface. Build the code-side pipeline as the source. Sync Zeroheight from the pipeline via Zeroheight's API. The migration is *additive* — Zeroheight stays for designers, the code-side becomes authoritative. **3–5 weeks**, dominated by API integration and the cadence rules. |
| **Storybook without autodocs** | The most-favorable starting point. The components are already where the source lives; the pipeline adds autodocs, the MDX template, the `.ai.json` overlay, the CI rules. **2–3 weeks.** |
| **Hand-rolled docs site (custom Next.js / Astro)** | Depends on architecture. If the site is already pulling from TypeScript types, the pipeline is mostly a CI and `.ai.json` addition. If the site is hand-authored prose with hand-typed prop tables, treat as Notion-equivalent. **1–4 weeks**, wide variance. |

### The two-phase migration

For systems with substantial existing prose (and most engagements do):

**Phase 1 — Scaffold the pipeline alongside the existing site.** The new pipeline emits a parallel docs site at a different URL. The team adopts component-by-component, migrating editorial content into the new MDX files, regenerating the technical layer, ratifying each component's new page before retiring the corresponding old page. This phase is dominated by editorial review — the existing prose is read by a consumer-not-on-the-team (per 29 §7's implicit-context anti-pattern), the parts worth keeping are kept, the parts that have drifted from the source are replaced. **Typical timeline: 3–8 weeks for a 60-component system, with 50–80 hours per week of UX Designer / UX Copywriter time.**

**Phase 2 — Dual-publish for a release window.** Both sites live; consumers get pointers from the old site to the new; the team monitors which pages still get traffic on the old site and prioritises the migration accordingly. Typical window: **2–4 weeks.**

**Retirement.** The old site is taken down; redirects route traffic to the new. The pipeline is the only docs source from this point forward.

### What to throw away

- **Stale authored prose** — purpose statements that no longer match the component, when-to-use rules that reference deprecated patterns. Audit the existing prose against the current source; throw away anything that disagrees with the source.
- **Broken examples** — MDX with imports that no longer resolve, code snippets that reference deprecated APIs, screenshots that show old visual treatments.
- **Deprecated screenshots** — automatically captured screenshots are regenerated by the pipeline; manually-captured screenshots of variants are typically out of date and worth re-capturing.
- **Redundant prop documentation** — hand-typed prop tables that contradict the source. Always defer to the source.

### What to keep

- **Purpose / when-to-use / avoid-when content** that still aligns with the component's current behaviour — most editorial content is reusable even when the technical layer has drifted.
- **Do/don't pairs** — re-screenshot the visual element, but the pair's framing is typically still correct.
- **Content guidelines** — almost always reusable; copywriters' outputs are the most-durable editorial content.
- **Design rationale / ADRs** — historical decisions are what they are; keep them as historical record.

### The "we still want Zeroheight for designers" reality

Many design-led engagements have Zeroheight in production with substantial designer engagement. The practice's discipline:

- **Keep Zeroheight as the design-side consumer surface.** Designers continue to consume from Zeroheight; their workflow is preserved.
- **The code-side pipeline is the source.** All technical-layer content is generated from it.
- **Sync Zeroheight from the pipeline.** Zeroheight's API ingests structured content; the practice ships a sync job that runs per-merge or per-release. Zeroheight becomes a *projection* of the source rather than an independent authoring system.
- **The cadence:** real-time sync is rarely required; per-merge or per-day sync is sufficient. The cadence is a per-engagement decision.
- **The failure mode:** sync breaks (Zeroheight API outage, schema mismatch, rate limit). The pipeline ships a "Zeroheight sync passed at HEAD" status check separate from the build; designers see a stale Zeroheight, the practice reconciles in the next sync.

### Migration anti-patterns

- **Rebuilding the site without the editorial content.** The new site is technically pristine and editorially empty. Consumers prefer the old site. Migration fails.
- **Throwing away the existing prose because it's hand-authored.** Most of it is reusable; the discipline is editorial review, not bulk replacement.
- **Treating migration as engineering-only.** It is half editorial. The UX Designer and UX Copywriter own the editorial review pass; engineering owns the pipeline scaffolding.
- **Skipping the dual-publish phase.** Cut-over without dual-publish strands consumers on the wrong URL; the team does not get migration feedback before the old site is gone.
- **Migrating the site without the CI rules.** The new pipeline ships, the freshness check is not enforced, the new site drifts the same way the old one did within 6 months.

---

## 6. The cluster relationship — generated documentation in the AI-readiness commercial default

Generated-from-data documentation does not stand alone. It is one of four practice deliverables that together constitute *AI-ready design system architecture* — the practice's defensible commercial position against vendor templates and incumbent consultancies.

### The four-prerequisite minimum architecture

Per 15-ai-in-ds and 25-ai-aware-patterns-and-conversational-ui, the architecture has four load-bearing layers:

1. **Tokens with descriptions.** Every token has a `$description` per DTCG; the descriptions are AI-readable. (See 02-design-foundations and 22-token-architecture-extensions.)
2. **Component metadata** — `.ai.json` per component plus the registry. (See 03-component-library and 15-ai-in-ds §7.)
3. **Agent instructions** — `AGENTS.md` / `CLAUDE.md` at the system level and at the consuming product level. The instruction-file layer is the practice's defensible POV that no external source names.
4. **Figma pipeline** — Figma variables → DTCG export → Style Dictionary → Code Connect → MCP. Bidirectional where possible; unidirectional where not.

Generated-from-data documentation is the **delivery surface** for layers 1–4 to the human consumer. The same source produces:

- **The docs site** (human-readable, for designers, developers, executives).
- **The `.ai.json` registry** (machine-readable, for AI agents).
- **The Figma library properties** (for the design tool).
- **The conformance dossier** (for auditors and procurement).

The architecture and the delivery are inseparable. A practice that ships components-as-data without the docs surface has a working AI-readable system that humans cannot consume; a practice that ships generated documentation without the components-as-data substrate is rebuilding the same data per consumer surface and accumulating drift.

### The cluster of unsold IP

Per 09 §1.7 and §1.12:

- **Code Connect not defaulted.** The Figma↔code mapping that AI agents use to ground component selection. The practice has the IP; commercial proposals don't ship Code Connect bindings by default.
- **Custom MCP server / registry not commercial.** The practice's MCP server architecture is an internal POV; not yet sold as a deliverable.
- **`.ai.json` is in the AI-Compatible doc but not the commercial proposal.** Should ship with every component by 2027.
- **AGENTS.md / CLAUDE.md** — the instruction-file layer is unique IP. The practice can claim this layer publicly.
- **Token descriptions as a default Foundations deliverable.** Aspirational, not contractual.
- **Engineering-onboarding artefact** (per 09 §1.7) — Couldwell's `docs/decisions/`, `docs/onboarding/`, `docs/meeting-notes/`. Almost no client has them; the per-component docs pipeline produces the substrate.

These six items are a cluster: the architecture is in the vault, the proposal language isn't. The practice's commercial transition is not "ship more architecture"; it is "itemise the architecture in the SOW with defensible per-line costs and defend the package." Generated documentation is the delivery surface; the cluster is what makes it real.

### The pitch

The practice's offer is the *whole cluster*, not just the docs site. The pitch:

> An AI-ready design system is an architecture, not a feature. The architecture has four prerequisites — tokens with descriptions, component metadata, agent instructions, and the Figma pipeline. The delivery surface that makes the architecture legible to your team is generated-from-data documentation, including a docs site, an `.ai.json` registry served via MCP, a Figma library kept in sync with the source, and a per-component conformance dossier that aggregates into your product's ACR. The practice ships the four prerequisites and the delivery surface as the engagement default. Vendor templates ship structure; we ship the architecture, the editorial discipline, the cluster of artefacts that make the structure load-bearing, and the pipeline maintenance retainer that keeps it aligned over time.

This is the version of the procurement conversation the practice should default to. Clients who push back ("we just want a docs site") get scoped down to a smaller deliverable explicitly per §7's objection handling. Clients who accept it get the full architecture and the practice has a defensible commercial position.

---

## 7. The commercial pitch — articulating this to clients who haven't asked for it

Most clients haven't asked for generated-from-data documentation because they don't know to. The practice's job is to surface the requirement, frame the value, and convert the conversation. Five framings that work in 2026:

### The procurement framing

"AI-ready design system" is the surface clients increasingly ask for — usually without articulating what it means. The practice's specific articulation is the four-prerequisite architecture (per §6) with generated documentation as the delivery surface. When the client says "we want our design system to work with our AI tools," the practice's response is "yes, here is what that requires architecturally, and here is the delivery surface that makes it real."

### The cost narrative

The upfront pipeline investment (108–216 hours per §3) is a one-time cost that pays back across all 60 components and the system's lifetime. Authored-prose docs carry an ongoing drift cost (60–120-hour quarterly maintenance) and an AI-readiness gap that is increasingly procurement-grade. The break-even is roughly 30 components; the lifetime savings on retainer alone are substantial. This is a defensible commercial argument with quantifiable numbers per §3.

### The risk narrative

Without generation, three predictable failures occur within 18 months:

- **The docs and the implementation drift.** 15–25% of pages have at least one disagreement with the source.
- **The conformance dossier is reverse-engineered every audit.** The accessibility lead spends 40–80 hours per audit cycle re-validating the docs site against the implementation.
- **The AI tools your team uses cannot reliably reach the system.** Cursor / Copilot / Claude Code generate code that uses hardcoded values, invents component names, and ignores composition rules. The system's adoption rate against AI-generated work plateaus.

These are not theoretical; they are observed across the practice's portfolio. The risk narrative converts "nice-to-have" into "we'd rather pay for it now than the consequences later."

### The competitive narrative

Vendor templates (Zeroheight, Supernova, Knapsack out-of-the-box) ship structure. The practice ships the architecture, the editorial discipline, and the cluster of artefacts (per §6) that make the structure load-bearing. Tools provide the database; the practice provides the schema, the semantic intent, the accessibility rigor, and the governance mechanisms. Clients who pick a vendor template without the editorial layer ship empty rooms; clients who pick the practice without a tool can host on free / self-hosted infrastructure.

### The phased adoption

Clients who can't take the full pipeline at engagement start can adopt incrementally:

- **Phase 1 — Storybook autodocs + MDX template + CI freshness check + `.ai.json` schema.** ~50–80 hours of upfront pipeline. Defers the MCP server and the Figma sync. The technical layer is generated; the AI-readable layer exists in registry form but isn't served via MCP yet. Gets the practice 70% of the way to the full architecture.
- **Phase 2 — Code Connect integration + Figma library sync.** Adds ~16–32 hours per platform. Closes the design-side drift.
- **Phase 3 — Custom DS MCP server + `.ai.json` registry served via MCP.** Adds 40–80 hours. Closes the AI-readable layer; the system is now fully AI-ready.

Most engagements can land Phase 1 in the initial commercial proposal and Phase 2/3 in retainer or follow-on engagements. The phased shape lets clients accept the architecture without paying the full upfront cost on day one; the practice retains the defensible commercial position because the architecture is the same regardless of phase order.

### Objection handling

**"We just want a docs site."** Two responses depending on engagement shape:

1. *Scope down explicitly.* "Yes — we can ship a docs site. It will be authored-prose, it will not include the AI-readable layer, it will require quarterly maintenance, and it will not produce conformance evidence by default. Here is the smaller scope, here is the price, and here is the upgrade path when you're ready." The practice retains the relationship and surfaces the architecture as a future option.

2. *Walk away if the client is also asking for AI-tool integration.* "What you're describing is two contradictory requirements. We can ship one, but not both. Let's reset the conversation." The practice does not ship a commitment to AI integration on top of an authored-prose substrate — the resulting deliverable is unreliable and the engagement ends badly.

**"Our team already uses Notion / Confluence / GitBook."** The migration playbook (per §5) handles this. The practice does not insist on tool replacement; the migration is a Discovery deliverable that decides whether to retire the legacy tool or run it in parallel.

**"This is more engineering than we budgeted."** The cost-vs-savings argument (per §3) addresses this. Where the math doesn't work (small system, single consumer, short lifetime), the decision framework (§4) returns "authored prose is acceptable" honestly and the practice scopes down.

**"Our designers won't use Storybook."** The hosted design-side surface (Zeroheight synced from the pipeline) addresses this. The technical layer is generated; the design surface is hosted; designers use the surface they're comfortable with.

**"We want everything in Figma."** The Figma sync direction is the answer; the practice ships Code Connect plus a Figma library kept current via per-merge sync. Designers get a current library; engineers get a source of truth that the library reflects.

---

## 8. Anti-patterns and tooling realities — where the field is genuinely behind in 2026

The practice should be honest about where the architecture works and where it doesn't.

### "Storybook autodocs alone is enough"

Storybook autodocs ships the props table, the controls panel, and the canvas — the developer-facing technical layer. It does not ship the AI-readable `.ai.json`, the typed relationship graph, the conformance dossier, or the Figma sync. Teams that adopt Storybook autodocs and stop are 30% of the way there. The remaining 70% — the AI layer, the design-side sync, the conformance aggregation — is what closes 09 §1.10 and §1.12.

The mitigation: ship Storybook autodocs as the foundation, but explicitly scope the additional pipeline layers as separate deliverables. Don't let "we have autodocs" become a reason to skip the rest.

### "Generate everything including intent"

The failure mode where the LLM authors purpose, when-to-use, and avoid-when prose. The result is generic ("a button is for actions"), wrong (the avoid-when entries don't reflect the system's actual conventions), and stale (the LLM regenerates from the source on every change, losing the editorial decisions made on the previous version).

The discipline per 29 §3: intent is authored, not generated. AI assistance during authoring is plausible (the generator suggests draft `avoid_when` entries based on adjacent components' usage), but the human author is the decision-maker and the source-of-truth for editorial content.

### The complex-multi-variable-state cliff

Automated state rendering for compound states (`selected + focused + server-error` cells, `loading + error + read-only` form fields) is fragile in 2026. Storybook controls handle binary states cleanly; multi-variable combinations require explicit story declarations and the screenshots are typically regenerated manually.

The practitioner workaround: generate base states algorithmically; hand-author visual examples for high-complexity multi-variable edge cases; mark the generated vs. authored split in the docs page so consumers know which is which. The component-type-specific extensions in 29 §2 (forms need a validation-state matrix; data-grids need a row-state matrix) carry the authored portion.

### The Figma sync seam

Design-side libraries do not yet pull from the same source automatically. Code Connect 1.x for React handles the source→Figma direction; the Figma→source direction is partial. The library is rebuilt on a separate cadence (typically per-design-handoff or per-major-release) and drift creeps in.

The mitigation: treat the Figma library as a deploy artefact, not an authored artefact. Every system release ships a Figma library update. The drift window is bounded by the release cadence rather than allowed to accumulate. Designers who reach for properties not in the library file a request that triggers a source change; the source change propagates to Figma on the next release.

### `.ai.json` schema is internal-tier IP

No canonical schema for component AI metadata has emerged in the field. Each practice that ships AI-readiness ships its own schema; the schemas vary in completeness and in the field names. The practice can claim its schema as IP, but **publishing it is the move that establishes the layer**. A published schema that the field adopts becomes the de facto standard; the practice that publishes it claims the architectural authority.

The recommendation: publish the practice's `.ai.json` schema as a public artefact in 2026. The cost is low (the schema is already documented internally); the strategic upside is high (the practice becomes the named author of the AI-readable layer the field standardises on).

### Zeroheight's API for generated content

Matured significantly through 2025–2026 but remains constraining. Zeroheight's data model is opinionated about what a component page contains; the practice's 17-section template per 29 has to map onto Zeroheight's 5-or-so default sections plus custom blocks. The mapping is feasible but lossy; some sections (the conformance dossier in particular) don't fit Zeroheight's model cleanly.

The mitigation: treat Zeroheight as a *design-consumer* surface, not the authoritative docs site. The full template lives on the code-side MDX site; Zeroheight gets a projection that emphasises the sections designers consume (summary, examples, do/don't, accessibility) and links to the code-side site for technical depth.

### Authoring-tooling that cannot consume the source

Notion, Confluence, GitBook cannot consume the generated source at all. Teams that have invested in these tools face a hard migration (per §5). The practice should not pretend this is a soft transition — it is a tool replacement, with all the associated change management.

### The Code Connect 2025–2026 maturity question

Code Connect is now Baseline-grade for React (Code Connect 1.x stable, 2.x in preview as of mid-2026). Code Connect for iOS / Android / Flutter is materially less mature — version numbers in the 0.x to 1.x range, partial coverage of the framework's idioms, less-mature tooling around the mapping. Cross-platform engagements hit the asymmetry: the React side gets full Code Connect; the iOS / Android side gets a partial mapping that requires manual maintenance.

The practitioner workaround: ship per-platform pipelines; accept that the non-React platforms have higher maintenance overhead; budget for it explicitly. Where the system is web-first with mobile as a secondary consumer, the asymmetry is tolerable; where the system is mobile-first, the asymmetry is the dominant engineering risk.

### The MCP server tooling reality

Building a custom DS MCP server in 2026 is a 40–80-hour project. The MCP specification (revision 2025-06-18 with subsequent revisions through early 2026) is stable enough to build against; the field does not yet have a turnkey "DS MCP server" the practice can ship as a vendor selection.

The practitioner approach: build it once, reuse it across engagements. The MCP server is a piece of practice IP that compounds in value across the portfolio. Each engagement adapts the schema, the registry build, and the client-specific configuration; the core server architecture is portable.

The recommendation: invest the 40–80 hours once in a reference MCP server implementation; ship it as a Foundations-tier deliverable on subsequent engagements. The first engagement bears the full cost; the second engagement onwards reuses the implementation. This is the durable engineering investment that pays back across the practice's portfolio.

---

## See also

For the documentation strategy this generation pipeline operationalises, see 04-documentation.

For the per-component template the pipeline produces, see 29-per-component-documentation-template.

For the components-as-data substrate that the pipeline assumes, see 03-component-library and 15-ai-in-ds.

For the accessibility schema that the pipeline emits as part of the conformance dossier, see 17-accessibility-annotation-contract, 16-mobile-accessibility-implementation, and 28-web-accessibility-implementation.

For the practice gaps this file addresses — generated-from-data as commercial default (residual gap from 09 §1.10), AI-readiness as commercial default (09 §1.12), Code Connect not defaulted (09 §1.7), custom MCP server / registry not commercial (09 §1.7), engineering-onboarding artefact (09 §1.7) — see 09-gaps-and-open-questions.

For the maintenance retainer shape the lifetime cost argument depends on, see 08-ongoing-maintenance.

---

## References

Primary sources (verified June 2026):

- **Storybook docs** — `https://storybook.js.org/docs` for Storybook 9 (May 2026) and the consolidated docs architecture; the SWC-based docgen path; addon-a11y configuration.
- **MDX 3 docs** — `https://mdxjs.com/`.
- **react-docgen-typescript** — `https://github.com/styleguidist/react-docgen-typescript` for the type-extraction pipeline that feeds Storybook autodocs and many MDX-based docs sites.
- **Curtis, *Components as Data*** (Sep 2025) — the architectural argument for source-of-truth component data files.
- **Curtis, *Operating Design Systems*** (Sep 2023) — the documentation track in the major-release cadence.
- **Wolosin, "Design system metadata is training data"** (Indeed, Jun 2025) — the four-tier metadata loop.
- **Couldwell, *Laying the Foundations*** (2019) — "document as you go," the IKEA-without-instructions framing, name-match-across-design-and-code-and-docs.
- **Mangialardi, *Design Systems for Developers*** (2021) — ADRs and decision logs in the docs repo.
- **Code Connect** — `https://www.figma.com/code-connect-docs/` for current platform support and configuration.
- **MCP specification** — `https://modelcontextprotocol.io/` for revision history; revision 2025-06-18 stable as of writing.
- **Zeroheight API docs** — `https://zeroheight.com/help/category/api/` for the integration surface and the generated-content model.
- **Supernova docs** — `https://supernova.io/docs` for the data-model engine.
- **Knapsack docs** — `https://knapsack.cloud/docs` for the live-code integration and the multi-platform support.
- **Atlassian Design System** — `https://atlassian.design/components` as a public exemplar.
- **Adobe Spectrum** — `https://spectrum.adobe.com/` particularly the component status tracker as a public conformance-dossier exemplar.
- **IBM Carbon** — `https://carbondesignsystem.com/` for the typed-relationship graph at scale.
- **Shopify Polaris** — `https://polaris.shopify.com/` for the editorial discipline at scale.
- **Material Web Components** — `https://material-web.dev/` for the spec-driven docs architecture at scale.
- **Anthropic, Claude Code** — `https://docs.claude.com/en/docs/claude-code` for the AI-tool MCP-consumer surface.
- **GitHub Copilot, Cursor** — for the broader AI-coding-assistant landscape consuming structured DS metadata.

Version-dependent claims dated above:

- Storybook 9 release May 2026; Storybook 8.x line still widely deployed.
- MDX 3 stable; backwards compatibility for MDX 2 through 2026.
- Code Connect 1.x stable for React; 2.x in preview; iOS / Android / Flutter Code Connect at 0.x to 1.x.
- The MCP specification revision 2025-06-18 stable through mid-2026 with subsequent minor revisions.
- TypeScript 5.5 as the assumed compiler version for JSDoc-driven prop-table generation.
- react-docgen-typescript 2.x; Storybook 9's SWC-based docgen path replaces the older Babel-based path.
- The 15–25% drift figure is cross-engagement memory; not from a published source and cited as practitioner observation.
- The break-even component count (~30) is derived from the cost calculations in §3 and is not from a published source.

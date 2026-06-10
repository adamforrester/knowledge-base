# 04 — Documentation

> The system's user manual for two distinct audiences: humans, and machines. Most published thinking still treats docs as a website for humans. The 2024+ practice ships docs as a parallel layer — human-readable Storybook/MDX *and* machine-readable metadata + registries — generated from the same source. Documentation is not the appendix; it is the system's surface.

---

## What this phase is, and why it matters

A component without documentation is a component that consumers will guess at. Guessing scales poorly. Documentation is the artifact that makes the system legible to the people (and now agents) who weren't in the room when decisions were made. It's also the artifact most likely to be deferred, under-resourced, and out of date — because shipping the component feels like the work, and writing about it feels like overhead.

Three reasons documentation deserves a phase, not a footnote:

1. **Intent does not survive otherwise.** A token, component, or pattern without a description of *why* and *when* will be misused within months. Couldwell's IKEA-without-instructions analogy still lands: the diagram doesn't tell you how to assemble it. (*Laying the Foundations*, 2019.)
2. **AI agents and code generators consume docs literally.** What humans can infer from brand context, agents cannot. Documentation that omits intent now produces wrong-component, wrong-token, off-brand outputs at scale. (Figma DS x AI, 2025; Wolosin, Jun 2025.)
3. **Documentation *is* training data.** Each tagged component, each token description, each `avoid_when` rule is a labeled data point that informs future AI selection — and, increasingly, future model fine-tuning. (Wolosin: *"Metadata isn't busywork. It's training data for the future of design."*)

Internal practice already names a dedicated UX Designer role to own documentation strategy across the engagement (CareCentrix 2026). The opportunity is to extend that role from "human docs strategist" to "human + machine docs strategist" and ship both layers as standard.

## What actually happens in this phase

Six clusters of work, run continuously through the engagement.

### 1. Documentation strategy and information architecture

- **Reference-site IA.** Standard sections (per scoping doc and CareCentrix): Home / Getting Started / Guidelines (Accessibility, Color, Typography, Layout, Theme, Tokens) / Component Overview / Per-Component pages / Patterns / Support / Changelog.
- **Per-component minimum.** Name, short description, primary purpose, examples (design + code), do's & don'ts, accessibility rules, states (rest/hover/focus/disabled/error/loading), content guidelines, historical context (Couldwell's Adobe Portfolio cautionary tale: undocumented, lost the "why").
- **Cross-disciplinary collaborative naming.** Designers, engineers, PMs, and content strategists agree on what things are called *before* docs are written. (Mall, 90 Days Activity #25 — glossary as a Discovery deliverable, not an appendix.)
- **Tooling decision.** The standard menu (Storybook, Supernova, Pattern Lab, Zeroheight, GitBook, custom site) is well-known; the choice is rarely the leverage point. The leverage point is *consistency between design files, code, and docs* — the same name in all three places (Couldwell).

### 2. Document intent, not appearance

- **Explain the *why*.** Not "this is a button"; "use this component when the user must take an action that progresses the primary task." (CareCentrix 2026 + Figma DS x AI 2025.)
- **Color guidance includes purpose.** "Why these brand colors? When and why use X over Y?" (Couldwell.)
- **Tokens carry descriptions** (`$description`). The single highest-ROI single action for AI compatibility — and equally valuable to human juniors. (AI-Compatible Design Systems, Feb 2025.)
- **Components carry usage rules with explicit *avoid_when*.** Negative selection prevents more mistakes than positive examples alone. (Wolosin Jun 2025; AI-Compatible Design Systems Feb 2025.)

### 3. Layered documentation architecture (2024+ standard)

The practice's emerging stance — and the one that differentiates from legacy "docs site" thinking — is that documentation is **a parallel layer**, not a single artifact. Wolosin's four-tier metadata loop (Jun 2025) is the cleanest articulation:

| Tier | Location | Audience | Update mechanic |
|---|---|---|---|
| **1. Structured metadata** | `.ai.json` per component + registry | AI agents (via MCP) | Authored alongside component |
| **2. Embedded in design tool** | Figma component descriptions, variable names, variant labels | Designers in Figma | Updated in design |
| **3. Embedded in code** | TypeScript types, JSDoc, semantic prop naming | Developers in their IDE | Updated in code |
| **4. Cross-tool links** | Figma↔Storybook dev links; Code Connect | Both, switching contexts | Generated from ID joins |

The internal AI-Compatible doc maps these tiers to an explicit four-layer stack:

1. **Tokens with descriptions** (every token has `$description` in DTCG JSON).
2. **Component metadata** (`.ai.json` + registry).
3. **Agent instructions** (`AGENTS.md` / `CLAUDE.md`) — the practice's claim is that none of the public discourse names this artifact yet; this is a defensible POV differentiator.
4. **Figma pipeline** (variables → DTCG export → Style Dictionary → CSS custom properties; Code Connect; MCP).

### 4. Generated, not handwritten

The 2025+ standard: docs are generated from component definitions, not handwritten alongside them. Curtis's *Components as Data* (Sep 2025) makes the case explicit — when components are YAML/JSON definitions, the documentation site, the code, the Figma assets, and the AI registry all derive from the same source. This is what closes the gap between "documented" and "actually accurate."

The mechanism (drawn from Curtis + Wolosin + Mangialardi):

- Component data file (YAML/JSON) is the source.
- Storybook stories are generated from the data + variants.
- MDX prose pages are authored, but every parameter list, every default, every example state is generated.
- `.ai.json` is generated (with human-authored `when_to_use` / `avoid_when` / `business_context`).
- Code templates per framework are generated (or scaffolded).
- Figma component sets are generated (or rebuilt from data).
- A CI check fails the build if the component code changes but `.ai.json` doesn't. (AI-Compatible doc Ch.7 — *metadata freshness tracking*.)

Most clients will not arrive at this on day one. The practice's job is to set the architecture so that when the client is ready to add generation, the foundation supports it.

### 5. Layer hygiene and structure

A practical Figma-side discipline named in Figma DS x AI (2025): clean files parse better. No unnecessary groups or frames; consistent layer naming; component instances rather than detached copies; variants properly structured. AI agents (and humans new to a file) read the structure as signal — chaos in the file becomes chaos in the output.

### 6. Documentation as sales surface

The site is also a sales artifact for adoption. Couldwell's stance: *"The guidelines and decisions you make when designing a system are no good just in your head."* If consumers can't find, understand, and trust the documentation in three minutes, they will either build wrong or build their own. Both are adoption failures.

Tactics:

- Search-first IA. Most consumers arrive looking for one thing.
- Examples before specs. Show the working component, then explain the props.
- Right-and-wrong examples explicit. Do/don't side-by-side.
- States documented and visible (rest / hover / focus / disabled / loading / error / empty).
- Accessibility details inline (color contrast, keyboard nav, screen reader expectations) — not in a separate a11y page consumers won't visit. (Figma DS x AI, 2025.)
- Changelog and versioning visible. Adopters need to know what's stable, what's deprecated, what's coming.

## Our POV

The CareCentrix 2026 commercial standard:

- **Dedicated UX Designer role** owns documentation strategy across the engagement. Defines structure and format of Figma component documentation; documents do/don't, states, accessibility notes; ensures docs are actionable for an engineering audience.
- **Usage documentation per component** (when/how to use, do/don't, annotated specs).
- **Design patterns documentation** (common workflows and interface patterns for internal tooling).
- **Content guidelines** (tone of voice, error message patterns, help text best practices).
- **UX Copywriter role** (75 hours scoped): integrates content guidelines into component documentation.
- **Accessibility standards documentation** (contrast ratios, type minimums, focus state specs).
- **Digital style guide in Figma** covering all foundational elements with usage doc.
- **Published Figma component library** ready for engineering consumption.

**Practice-distinctive POVs in this phase:**

- **Documentation is a named role, not a residue.** A dedicated UX Designer owning docs strategy across the engagement is rarer than it should be in consultancy practice. We sell this; we should sell it harder.
- **UX Copywriter for content standards.** A consistent dedicated role for tone, error messages, and help text — operationalized as hours, not aspirations. (CareCentrix 2026 introduced this; Thrive 2024 didn't.)
- **Accessibility integrated into component docs**, not as a separate chapter.
- **Token descriptions as a default deliverable.** Every token gets a description; the AI-Compatible doc names this as the highest-leverage move. We should make this default in commercial proposals (currently aspirational).
- **The four-layer AI documentation stack** (tokens with descriptions / `.ai.json` + registry / `AGENTS.md` + `CLAUDE.md` / Figma pipeline). The instruction-file layer (`AGENTS.md`/`CLAUDE.md`) is genuinely under-theorized in public DS discourse; the practice can claim it.
- **AI-aware patterns ship with their own documentation contract.** When the system also publishes consumer-facing AI patterns (chat input, streaming, citation, refusal, tool-call), the disclosure copy, refusal copy, citation behaviour, and approval workflow become docs deliverables in their own right — and they sit alongside legal/governance artefacts (PIA, Article 50 disclosure language) the docs site does not normally host. (See 25-ai-aware-patterns-and-conversational-ui.)

**Gaps in our current commercial Documentation standard, honestly named:**

- **The IA of the docs site itself is not a deliverable.** "Reference website v1" is named in scoping; the IA, search behavior, navigation patterns, and per-component template aren't. They should be — the site experience is the adoption experience.
- **Generated-from-data documentation is not yet our default.** Curtis's *Components as Data* model makes generation possible; our 2026 commercial proposals still treat docs as authored prose. By 2027, the architecture should be source-of-truth-data with generated docs.
- **Machine-readable docs are aspirational, not contractual.** AI-Compatible doc covers `.ai.json` and registries; CareCentrix-style proposals don't yet ship them. This needs to flip — every component shipped should have a peer `.ai.json`.
- **Tooling opinion is thin.** Scoping doc lists Storybook / Supernova / Pattern Lab / Zeroheight / GitBook without trade-offs. Clients ask which to use; we should have a defensible recommendation framework rather than "depends."
- **No template for the per-component doc page.** A standard practice template (purpose / when-to-use / avoid-when / props table / states / accessibility / examples / do-don't / content guidance / related components / changelog) would speed every engagement and improve consistency.
- **Glossary is not a default deliverable.** Mall's Activity #25 framing — glossary as a *negotiation* between disciplines, produced in Discovery — is missing from our commercial flow.
- **Documentation-as-training-data narrative is undeveloped.** Wolosin's framing ("metadata is training data") is a strong argument for fully-described documentation. We don't yet make this argument explicitly in pitches.

## External perspectives

### Validate

- **Couldwell's "document as you go"** — directly aligns with our practice's continuous-documentation stance.
- **Couldwell's "name in design = name in code = name in docs"** — exactly the discipline our practice insists on.
- **Curtis on documentation as a major-release track** — alongside Visual Style, UI Components, Tech Architecture. Validates docs as a first-class product surface, not an afterthought.
- **Curtis's documentation substeps** (template setup, examples, design guidelines, accessibility, code API, component explorer states, code usage examples, writing/editorial, images, prototype demos) — directly maps to a usable per-component doc template.
- **Figma DS x AI (2025)** on the "explain the why," "show right and wrong examples," "include accessibility details," "maintain layer hygiene" — directly validates the practice's documentation principles.
- **Wolosin (Jun 2025)** on the four-tier metadata loop — validates the practice's `.ai.json` + registry layer; extends with explicit cross-tool linking.

### Challenge

- **Frost on "docs site as historical artifact."** Frost (2016) treated the style-guide site as the primary documentation surface. By 2025, the docs site is one of four layers (per Wolosin). Practice should not lead with "we'll build a docs site" — should lead with the layered model.
- **Curtis on "Figma is one target among many."** If the design tool is downstream of component data, then Figma documentation (component descriptions, variant labels) is also generated. Practice should treat Figma metadata as derived from the source data, not as the source itself.
- **Idean's "make tools, not rules."** Pushes against doc-heavy systems. Documentation should serve practitioners, not regulate them. The discipline test: if a section of docs isn't used by a practitioner in three months, delete it (or move to archive).
- **Figma DS x AI's "AI as documentation consumer."** Pushes the practice to write docs that are simultaneously human-readable and machine-parseable. Specifically: avoid implicit context, write declaratively, structure consistently. This changes prose style.
- **Anderson's "DS as infrastructure"** (Nov 2024) — implies documentation is the infrastructure's *contract*, not its description. Contracts are versioned, machine-readable, and enforced. Documentation that doesn't behave like a contract is informational, not infrastructural.

### Extend

- **Wolosin's 4-tier metadata loop** is a clearer pedagogical frame than the practice's current 4-layer AI stack. Worth absorbing as a teaching frame for clients.
- **Curtis's component pipeline + documentation step** as a structural artifact in the project plan — explicit doc substeps per component, gated as part of release.
- **Mall's glossary-as-Discovery** (Activity #25) — adopt as standard Discovery deliverable.
- **Figma DS x AI's prompting-conventions artifact** — increasingly, design systems should ship a "how to prompt against this system" guide for client teams using AI tools. Practice does not yet do this.
- **Mangialardi's decision logs / ADRs** in the docs repo (`docs/decisions/`) — lightweight architecture decision records. Almost no client has them. Easy adoption win.
- **Couldwell's intent-documentation discipline for color** ("why these brand colors? when use X over Y?") generalizes to every foundation: every token, every component, every pattern documents *intent*, not just appearance.
- **Wolosin's "training data" framing** strengthens the ROI argument for full documentation: even if no AI agent reads it today, the data accumulates and pays off as soon as one does.

## Tensions and open questions

1. **Human vs. machine docs as a single artifact.** Our scoping doc says docs must be "an ongoing part of the design and build process, not an afterthought" — written for humans. Our AI-Compatible doc says human-only docs are now a *failure mode*. Working synthesis: docs are produced as a parallel layer, not one or the other. Generated-from-data architecture closes the loop — author once, generate both surfaces.
2. **Tooling choice.** Storybook is the engineering-side standard. Zeroheight, Supernova, Knapsack are the design-side options. The right answer is "the docs live where they're consumed and generate from one source." Practice should articulate a recommendation framework: codebases with strong dev culture → Storybook + MDX is sufficient; designer-heavy orgs → Zeroheight/Supernova on top; high-budget enterprise → Knapsack with Code Connect.
3. **How much prose is enough.** Idean's "make tools not rules" warns against doc-heavy systems. Couldwell argues for thorough documentation including intent. Both are right at different scales. Working principle: prose only when generation can't capture it. Anything that can be derived from data should be derived; anything that's irreducibly human (intent, when-to-use, anti-patterns, do/don't with reasoning) is prose.
4. **Versioning and changelog.** SemVer is well-established. The harder question is *what* gets versioned — every component, the whole library, the tokens separately? Curtis's library tiers suggest the answer: each tier (Core foundation, Core library, Shared library, Team library) has its own version cadence. The practice's commercial standard hasn't yet articulated this clearly.
5. **AGENTS.md / CLAUDE.md as a public-facing artifact.** The instruction file is unique IP — the practice claims it; external sources don't yet name it. As a stance for clients: ship it by default, document its purpose, treat its evolution as a release event.
6. **Documentation tooling lock-in.** Zeroheight, Supernova, Knapsack are SaaS; their hosted docs become a dependency. For regulated/on-prem clients (Penpot territory), self-hosted is required. Practice should have an opinion on portability.
7. **Documentation for whom.** Practice defaults to writing for designers consuming the system. The increasingly important audiences are (a) developers consuming components, (b) AI agents consuming metadata, (c) brand/marketing teams consuming guidelines, (d) executives evaluating the system. Each needs different surfaces. The 4-layer model addresses (a) and (b); (c) and (d) are usually under-served.

## Failure modes specific to this phase

- **Documentation deferred.** "We'll write the docs once components are built." Components ship; docs lag by weeks; consumers either build wrong or wait. Both damage adoption. (Couldwell.)
- **Tooling first, content later.** Six weeks spent picking Zeroheight vs. Supernova; one week spent writing actual content. The site is empty, then half-empty, then forgotten.
- **Documentation that doesn't explain intent.** Props tables and screenshots — no when-to-use, no avoid-when, no purpose statement. Consumers (and AI) can use the components but can't *choose* between them.
- **Tokens without descriptions.** Every token is a name and a value; no `$description`. AI agents fail silently; junior designers misuse silently.
- **Implicit context.** Documentation written for the team that built the system — references shared assumptions, abbreviations, internal lore. New consumers (and AI) can't follow it.
- **Stale documentation.** Components evolve; docs don't update. Trust erodes — once consumers find one wrong page, they trust nothing on the site.
- **Generic component pages.** Every component has the same template, but the template doesn't include the things this specific component actually needs (e.g., Form components need validation guidance; Toast needs auto-dismiss behavior; Modal needs focus-trap notes).
- **Accessibility as a separate chapter.** Color contrast, keyboard navigation, ARIA documented in a "/accessibility" page nobody reads. Should live inline with each component's docs.
- **No machine-readable layer.** Beautifully written docs that no agent can parse. By 2026, this is functional debt — the system is already older than its peers.
- **Glossary missing.** Six months in, "pattern," "template," and "page" mean different things to different teams; the system is three systems and no one noticed.
- **Documentation tooling as adoption substitute.** "We bought Zeroheight, so we have a docs strategy." Tooling without staffed authoring is empty.

---

*Provenance: The dedicated UX Designer documentation-strategy role, UX Copywriter content-standards role, accessibility integrated into component docs, and Figma-style-guide-with-usage standard are internal POV from CareCentrix 2026. The reference-site IA, per-component minimum, and tooling menu are from DS-Scoping (2026) and VML library (2024–2026). The four-layer AI documentation stack (tokens-with-descriptions / `.ai.json` + registry / `AGENTS.md`+`CLAUDE.md` / Figma pipeline) is internal POV from AI-Compatible Design Systems (Feb 2025). The instruction-file layer (`AGENTS.md`/`CLAUDE.md`) is a defensible POV differentiator — external sources do not yet name it. The four-tier metadata loop (structured metadata / Figma-native / React-native / cross-link) and "metadata is training data" framing are from Diana Wolosin (Indeed, Jun 2025). "Document as you go," "name match across design+code+docs," and the IKEA-without-instructions analogy are from Andrew Couldwell (Laying the Foundations, 2019). The component-pipeline documentation step and "Documentation Platform" as a major-release track are from Nathan Curtis (Operating Design Systems, Sep 2023), treated as near-internal-tier weight. "Components as Data" generates documentation is from Curtis (Sep 2025). "Explain the why," "show right and wrong examples," "include accessibility details inline," "maintain layer hygiene," and AI-as-documentation-consumer are from Figma DS x AI (2025). "Make tools, not rules" is from Idean (Hack the Design System, 2019). The glossary-as-Discovery activity is from Mall (90 Days, 2023). Decision logs / ADRs in the docs repo are from Mangialardi (Design Systems for Developers, 2021). The "DS as infrastructure / docs as contract" reframe is from Sam Anderson (Nov 2024).*

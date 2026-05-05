# 05 — Development Support

> The system reaches engineers at the framework, the build, and the IDE — or it does not reach them at all. Development support is what turns a Figma file into something a consuming codebase can run, version, and trust. It is also the phase the practice currently sells lightest, and where most engagements quietly fail to translate design intent into production reality.

---

## What this phase is, and why it matters

Most consultancy DS engagements stop at the design library. The internal practice's CareCentrix 2026 standard explicitly *excludes* front-end development, code delivery, and engineering implementation from scope — the Figma library is the deliverable. This is a defensible commercial scoping choice for a particular kind of engagement. It is also a recognized gap: a Figma library that doesn't reach the consuming codebase, with a token pipeline the engineering team can run on every build, becomes a liability within months. Visual designs and production code drift; consumers hardcode values when they can't find tokens; the system "exists" but is never adopted in production.

This phase is about building the bridge from the design source of truth to every consuming application — and doing it in a way that survives team turnover, framework changes, and brand evolutions.

The 2024+ shift: AI agents and code generators are now active consumers of this layer. Code Connect, MCP, and the increasingly common pattern of "generated component code from structured component data" make the build pipeline simultaneously a design contract, a developer contract, and an AI contract. Get the architecture right and all three flow naturally. Get it wrong and each becomes its own integration project.

## What actually happens in this phase

Five clusters of work.

### 1. Token build pipeline

The architectural pattern has stabilized (Mangialardi 2021; Curtis 2024; AI-Compatible 2025; Figma DS x AI 2025):

```
Figma Variables (with descriptions)
    ↓ DTCG export (Token Forge / Tokens Studio / equivalent)
Tokens (DTCG JSON — source of truth)
    ↓ Style Dictionary
Platform deliverables
    • CSS custom properties
    • SCSS variables
    • JS modules / TypeScript types
    • iOS Swift
    • Android XML
    • Tailwind theme config
    ↓ Distribution
    • npm package (JS consumers)
    • GitHub Actions copying deliverables to consumer repos (Mangialardi's recommended pattern)
    • API endpoint (consumers fetch)
Consuming applications
```

Key decisions:

- **Style Dictionary** as the canonical transformation tool. Curtis names it. Mangialardi spends 60 pages on it. Internal practice endorses it.
- **DTCG JSON** as the interchange format. Aligns with W3C draft; works with most tooling.
- **Custom transforms and formats** when defaults don't fit. Style Dictionary is extensible; treat the transforms as system code, version them, review them.
- **GitHub Actions distribution** (e.g., `andstor/copycat-action`) as Mangialardi's recommended distribution mechanism — each consumer gets one parallel job; new consumer = one new entry. Beats npm-only (which forces JS) and beats API-fetch (which requires consumer polling).

### 2. Component code architecture

Two patterns to choose between:

**Opinionated component libraries.** Material UI as the canonical example. Functionality and styling tightly coupled. Faster to start with, harder to brand-extend. Mangialardi explicitly criticizes this: "consumers spend energy undoing Material defaults to apply their own brand."

**Headless UI components.** Tailwind Labs' Headless UI, Radix UI, React Aria. Functionality (focus management, keyboard nav, ARIA) encapsulated in unstyled components; styling applied via consumers' choice (styled-components, Tailwind, vanilla CSS, CSS-in-JS). Decoupling lets the UI library outlive any single design language. Mangialardi's recommendation, and the right answer for multi-framework or multi-brand orgs.

Practice POV implication: for clients with multiple consuming frameworks (React + Vue + native), recommend headless. For clients with a single React stack and no theming complexity, opinionated is faster to ship. Discovery determines. The "native" leg of that decision — iOS/Android/Flutter — has its own component-architecture trade-offs that don't reduce to the headless-vs-opinionated axis. (See 11-mobile-and-cross-platform.)

### 3. Storybook, docs site, and developer surfaces

Storybook is the engineering-side standard. Components ship with stories; stories are the testbench, the docs, and the visual regression baseline.

What Storybook delivers (well-implemented):

- Live component explorer with all states and variants.
- Accessibility checks (a11y addon).
- Visual regression baseline (Chromatic or equivalent).
- API documentation auto-generated from props.
- Code Connect target — Figma maps components to Storybook stories.
- MDX prose alongside stories for usage guidance.

What's frequently missing in commercial engagements (and rarely shipped by the practice):

- **Visual regression testing in CI.** Chromatic, Percy, or self-hosted. Without it, every release risks unintended visual changes.
- **Accessibility CI.** axe-core, pa11y, or equivalent on every PR.
- **Token drift detection.** A check that fails the build if Figma Variables and code tokens diverge.
- **Component contract tests.** Unit-level tests that verify props validate, states render, edge cases handle.

Mangialardi *also* doesn't cover these (a real gap in his book). They are not yet in any consultancy's commercial standard the practice has been benchmarked against. This is consequently both a gap *and* an opportunity — the practice can claim leadership by shipping CI quality gates as part of standard engagement scope.

### 4. AI / agent integration layer

The 2024+ standard for development support extends beyond build pipeline to AI integration:

- **Code Connect** (Figma) — maps Figma components to real code components. Generated code references production code, not generic snippets. Reduces context switching; keeps designs and implementations aligned.
- **Figma's MCP server** — exposes the design file structure to agents. Curtis's caveat applies: "stochastic, incomplete, and imprecise" if used naively; valuable when paired with a structured component-data source.
- **Custom MCP server** — exposes the registry, `.ai.json` files, and token definitions to agents (`list_components`, `get_component`, `search`). Internal practice has named this as a future direction; it is the right move for clients with heavy AI tool usage.
- **`AGENTS.md` / `CLAUDE.md` instruction files** — workflow-specific rule files. The internal AI-Compatible doc names a Figma MCP rule flow: `get_variable_defs` → `get_code` → `get_code_connect_map` → `get_screenshot` → translate / implement / validate. These instruction files are 200–600 lines, version-controlled, treated as system code. The practice's claim: external public DS discourse does not yet name this artifact — it's a defensible POV differentiator.
- **Figma Make + Figma Sites** — Figma's house pipeline products. Make generates prototypes against the system; Sites publishes design directly to the web. By 2025–2026 these are increasingly the first AI tool a Figma-using client encounters. Practice should have a stance: where they fit, where they don't, how to govern their outputs.

Internal practice's "required Figma MCP tool flow" (AI-Compatible doc, Feb 2025): explicit, sequenced steps for every AI-assisted component implementation. This is operational rigor most pitches don't yet articulate. (See 12-figma-practice for the Figma-side mechanics — Dev Mode, Code Connect maturity and limitations, the MCP sequence, and the structured-component-data prerequisite.)

### 5. Adoption enablement

Per Curtis's *Operating Design Systems* workshop (Sep 2023) — Adoption Enablement is its own initiative track:

- **Roadshow** — present to consuming teams.
- **Getting Started materials** — onboarding for new engineers (cf. `engineering-onboarding` skill — a documented onboarding artifact for new dev hires).
- **Training sessions** — recurring, format-varied (lunch-and-learns, formal training, sprint demos).
- **Office hours** — semi-monthly recurring window for consumer questions.
- **Release announcements** — Slack, email, internal blog. Every release is communicated.
- **Slack support** — `#system-dev` public channel for releases + tech help.
- **Warranty period after launch** — rapid releases of fixes, priority enhancements, integration support.

The point: development support is not an artifact, it's a practice. The engineering org's relationship to the system is shaped over months by the rituals of release, support, and communication — not by the quality of the npm package alone.

## Our POV

The CareCentrix 2026 commercial standard is explicit about scope:

- **Out of scope:** front-end development, code delivery, engineering implementation, application-specific UI redesign.
- **In scope:** Figma library, design tokens (W3C DTCG-compliant), documentation, design-engineering alignment sessions, incremental handoff, pilot validation in Storybook with the engineering team.

The practice's claim: design-side delivery + alignment is the offering; the consuming team's engineers do the implementation, with our designers embedded throughout.

**Practice-distinctive POVs in this phase:**

- **Embedded model, incremental handoff.** "Components are handed off to engineering as they're completed — so your team starts building with the system before the engagement ends." (CareCentrix 2026.) This is the procurement-grade differentiator vs. consultancies that ship a Figma file and walk away.
- **W3C DTCG token output as procurement standard.** Named explicitly in CareCentrix; not in Thrive. Tightens the technical conversation with engineering stakeholders.
- **Pilot validation milestone** with engineering, in Storybook, before final handoff.
- **Engineering availability as a discovery question.** The CareCentrix 10 procurement questions explicitly ask about engineering availability for alignment and handoff — naming it as a constraint we'll plan around.
- **The required Figma MCP tool flow** (`get_variable_defs` → `get_code` → `get_code_connect_map` → `get_screenshot` → translate / implement / validate) — operational rigor for AI-assisted implementation. (AI-Compatible doc, Feb 2025.)

**Gaps in our current commercial Development Support standard, honestly named:**

- **The token pipeline is not in the deliverables.** We name DTCG-compliant tokens; we don't typically include Style Dictionary configuration, GitHub Actions distribution, or any pipeline artifacts as deliverables. For most enterprise clients this means the tokens stop at Figma and the engineering team rebuilds the pipeline. Adding "design-token build pipeline" as a deliverable (or as a clearly-priced add-on) would close the most consequential gap.
- **CI quality gates not in scope.** Visual regression, accessibility CI, token drift detection — none of these are typically part of our engagement scope. Practice could claim leadership here; clients would value it.
- **Code Connect is named but not defaulted.** The practice has the IP; commercial proposals don't ship a Code Connect map by default. Should flip — Code Connect bindings are now table-stakes for any Figma-using engineering org.
- **Custom MCP server / registry is internal POV but not commercial.** When client engineering teams are heavy AI users (increasingly common in 2026), custom MCP integration is real value; we don't yet sell it.
- **No engineering onboarding artifact.** Couldwell argues for `docs/decisions/`, `docs/onboarding/`. We should ship a documented engineering-onboarding guide as a default deliverable — saves the consuming team weeks of orientation.
- **Headless vs. opinionated guidance.** Practice does not have a documented stance for clients facing this architectural choice. We should.
- **Testing coverage is under-articulated.** Component contract tests, accessibility tests, visual regression — neither our materials nor most external sources articulate the testing layer. Genuine gap in the broader literature, but the practice could lead here.

## External perspectives

### Validate

- **Mangialardi** (*Design Systems for Developers*, 2021) — directly validates the token pipeline architecture (Figma → JSON → Style Dictionary → platform deliverables → consumers). Naming taxonomy from Curtis (namespace / object / base / modifier). Token contracts as "API contracts." GitHub Actions delivery via copycat-action. Recommended manual extraction first sprint to force collaboration.
- **Curtis** (*Operating Design Systems*, Sep 2023) on the feature pipeline (Plan → Design → Specs → Code → Doc → Assets → Release) and the embedded handoff between Spec and Code. Adoption Enablement as its own initiative track. Code substeps including unit tests, manual + automated accessibility, visual regression, API docs, dependent updates.
- **Curtis** on Style Dictionary as the canonical transformation pipeline; DTCG `$type` / `$value` syntax for composite tokens.
- **Figma DS x AI (2025)** on Code Connect and MCP — directly validates the practice's AI-Compatible doc's Figma pipeline layer. Specifically: Code Connect ties Figma and the codebase together so developers see real production code without leaving Figma. MCP enables AI to reference real structure and logic.
- **AI-Compatible Design Systems (Feb 2025)** on the four-layer AI stack — internal POV with strong external 2025 alignment (Figma DS x AI, Wolosin, Anderson).

### Challenge

- **Mangialardi on opinionated component libraries.** Material UI is the cautionary example — tightly coupled functionality and styling means consumers undo Material defaults to apply their own brand. Practice should adopt headless UI as default recommendation for multi-framework or theming-heavy clients.
- **Mangialardi on manual token extraction first.** Pushes against full automation in the first sprint. Forces designer-developer naming negotiation and creates the "API contract." Right answer for early sprints; automation from sprint 2.
- **Curtis on "Figma Variables ≠ tokens."** Many clients (and many of our pitches) treat them as synonymous. They become tokens only with the discipline of versioning, multi-format export, deliberate naming. Pushback we should incorporate into our discovery diagnostic.
- **Curtis on "Figma Dev Mode MCP is a trap."** Don't position MCP as the AI-readiness solution. Formalize the data first; MCP exposes data, doesn't replace it.
- **Curtis on adoption: "Slack + Office Hours ≠ communications plan."** Pushes against the easy "we'll do office hours" answer. Real adoption requires structured communication, sprint demos, training events, scheduled releases.
- **Mangialardi's testing gap is also our gap.** His book covers token pipeline beautifully but doesn't cover Storybook, visual regression, or testing strategies. Neither does the field broadly. This is not validation but mutual silence; the practice can lead by filling it.

### Extend

- **Code Connect as default deliverable.** Validated in Figma DS x AI (2025) as the bridge between Figma and code. Practice should ship Code Connect bindings by default for any Figma-source engagement.
- **Custom MCP server pattern.** Internal POV (AI-Compatible doc) names a future MCP server exposing `list_components`, `get_component`, `search`. The practice can productize this as a deliverable for AI-heavy client teams.
- **Visual regression testing in CI** as default scope. Chromatic, Percy, or Storybook test runner. The practice can claim leadership here — it's not in commercial standards across the field.
- **Accessibility CI** (axe-core, pa11y) as default scope. Same as above.
- **Token drift detection.** A CI job that fails when Figma Variables and code tokens diverge. Solves the most common silent-failure mode of token systems.
- **`AGENTS.md` / `CLAUDE.md` workflow rule files** — internal POV; the practice can claim this layer as defensible differentiation. External public DS discourse does not yet name it.
- **Decision logs / ADRs in repo** (Mangialardi) — `docs/decisions/` for architecture decisions. Almost no client has them. Cheap adoption win.
- **Headless UI as architectural default** for multi-framework clients (Mangialardi). Practice POV should name this explicitly.
- **The "warranty period" framing** (Curtis) — post-launch rapid-fix support window. Names what most clients implicitly expect; making it explicit improves the contract.

## Tensions and open questions

1. **Should we sell the engineering pipeline?** Our current scoping excludes front-end development. The technology team is increasingly the buying audience for design system engagements (per Figma Design Leaders ebook 2025: 80% of developers want closer collaboration). Selling the pipeline (Style Dictionary, GitHub Actions delivery, CI gates) without selling implementation is a defensible middle path. Discuss: should "design token build pipeline" be a default deliverable or a priced add-on?
2. **Headless vs. opinionated.** Practice doesn't have a documented stance. The right answer is: discovery determines, but for multi-framework or theming-heavy clients headless is the default; for single-React clients opinionated may be faster. Articulate this.
3. **Storybook vs. design-tool-native docs.** Storybook is engineering-side; Zeroheight is design-side. Some orgs don't have a Storybook setup. Should the practice fund Storybook setup as part of the engagement when one doesn't exist? Often yes, but not currently scoped.
4. **CI quality gates as differentiator.** The field is silent on this. The practice could lead — but visual regression and accessibility CI require client engineering buy-in, sometimes a culture shift. Worth claiming as a recommended scope add for clients ready for it.
5. **Custom MCP vs. Figma's MCP.** Figma's Dev Mode MCP is the path of least resistance. Curtis says it's a trap. A custom MCP server exposing the practice's registry + `.ai.json` is the rigorous path. Resource-intensive to build, valuable when the client's engineering team uses agents heavily. Discovery question: how many of the engineering team are using AI coding tools regularly?
6. **Manual token extraction as a teaching exercise.** Mangialardi argues for manual extraction first sprint to force naming collaboration. Tools have matured (Tokens Studio, Specify, Variables export). Working synthesis: manual *for the naming conversation*, automated for the actual JSON generation, so the team owns the names but doesn't own the typing.
7. **The 2025+ Code Connect default.** External 2025 sources increasingly treat Code Connect as standard. Practice should commit to shipping Code Connect bindings by default — it's the bridge that makes "design system" feel like one system in both tools.
8. **Pricing for ongoing development support.** Our commercial proposals end at handoff. Engineering team support — bug fixes, integration questions, evolution requests — is the steady-state work that makes systems durable. Practice does not yet sell this. (See `08-ongoing-maintenance.md`.)

## Failure modes specific to this phase

- **Tokens stop at Figma.** Designers ship a Variables setup; engineers can't consume it. They hardcode. The system "exists" but is never deployed.
- **Pipeline as black box.** The token build runs but only the original setup engineer understands it. They leave; nothing updates.
- **No CI gates.** Components ship, regressions ship, accessibility regressions ship. Trust erodes.
- **Code Connect missing.** Engineers see Figma, then read Storybook, then read code, three places to verify the same thing. Round-tripping kills adoption.
- **Opinionated library locks brand.** Material/Bootstrap defaults bleed through; the brand fights its own components.
- **Tightly-coupled component code.** Adding Vue, native, or a new framework requires rewriting every component.
- **Adoption Enablement as afterthought.** Roadshow, training, office hours, releases — none of these scoped, all assumed. Adoption stalls; client's internal team gets blamed.
- **MCP without rule files.** AI agents pull from Figma MCP and produce inconsistent code. No `AGENTS.md` to govern the workflow; the agent's outputs vary day to day.
- **Documentation in a different repo than code.** Engineers don't update it; it goes stale.
- **No `docs/decisions/`.** Six months later, no one remembers why the team chose `inline-md` over `space-3` and re-litigates the decision every quarter.
- **Visual regression deferred to "later."** Three months in, "later" is "never," and a redesign breaks half the consuming product silently.
- **Single npm package as distribution.** Works for JS consumers; Java, Swift, Kotlin teams build their own. Three systems pretending to be one. (See 11-mobile-and-cross-platform for the platform-specific delivery pipeline this failure mode breaks.)

---

*Provenance: The CareCentrix 2026 scope boundary (excludes front-end dev, includes design + tokens + docs + alignment + Storybook pilot validation), the embedded incremental-handoff model, the W3C DTCG procurement-grade commitment, and the engineering-availability discovery question are internal POV from CareCentrix 2026. The required Figma MCP tool flow (`get_variable_defs` → `get_code` → `get_code_connect_map` → `get_screenshot` → translate/implement/validate), the four-layer AI stack, and the future custom MCP server exposing the component registry are internal POV from AI-Compatible Design Systems (Feb 2025). The token build pipeline architecture (Figma → DTCG JSON → Style Dictionary → platform deliverables → GitHub Actions distribution), headless UI vs. opinionated component library framing, manual-extraction-then-automate, naming taxonomy (namespace/object/base/modifier), token contracts as API contracts, and decision logs / ADRs in the docs repo are from Michael Mangialardi (Design Systems for Developers, 2021). The feature pipeline (Plan → Design → Specs → Code → Doc → Assets → Release), embedded handoff between Spec and Code, Adoption Enablement as a separate initiative track, the warranty period after launch, and "Slack + Office Hours ≠ communications plan" are from Nathan Curtis (Operating Design Systems, Sep 2023), treated as near-internal-tier weight. Style Dictionary as canonical tool, DTCG composite types ($type, $value), and "Figma Variables ≠ tokens" / "Figma Dev Mode MCP is a trap" are from Curtis (Design Tokens, Nov 2024). Code Connect, MCP as design-to-code-pipeline, and "AI as documentation consumer" are from Figma DS x AI (2025). The "DS as infrastructure" framing for engineering pipelines is from Sam Anderson (Nov 2024).*

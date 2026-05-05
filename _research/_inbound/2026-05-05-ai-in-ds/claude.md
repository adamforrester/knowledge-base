# AI in Design Systems Practice — End to End

A practitioner's reference for senior design systems engineers and designers. Covers how AI tools, agents, and workflows integrate into DS work — token creation, Figma operations, component development, documentation, design-to-development handoff, governance, the architectural prerequisites that make any of this work, and the honest assessment of where it ships today vs. where it's still aspirational. Assumes fluency with design systems and basic familiarity with current AI coding tools; focuses on the workflow, the architecture, and the gaps as of January 2026.

A note on currency before the rest of the document: this space rotates fast. Specific feature names, MCP tool surfaces, plan-tier capabilities, and AI-assistant integrations cited below reflect the platform state as of early 2026 and may have evolved by the time anyone reads this. Where claims are platform-state-dependent, verify against current docs. The architectural shape — components-as-data, DTCG tokens, structured metadata exposed via MCP — is more durable than the tool names attached to it.

---

## 1. AI in token creation and validation

### Generating, validating, and critiquing taxonomies

Out of the gate, the most useful pattern is **AI as critic, not author**. Asked to "generate a token taxonomy from scratch," current frontier models produce plausible but over-engineered output — too many tiers, redundant naming, semantic tokens that wrap one primitive each, and conventions that don't match any actual codebase. Asked to "audit this token taxonomy for missing semantic coverage, redundant primitives, and naming inconsistencies," the same models produce useful, surgical critique.

The workflow that works:

1. Human (or an existing system) drafts the taxonomy.
2. AI is given the full taxonomy plus a contextual brief (the brand intent, target consumers, scale, theming dimensions).
3. AI returns a critique: gaps, inconsistencies, duplications, naming suggestions.
4. Human curates the critique — about 50–70% of the suggestions are useful; the rest are too cautious or miss the point of a deliberate design choice.

For taxonomy *generation*, AI is best used to expand within a structure the human has decided. "Given this primitive color scale and these semantic categories, propose semantic tokens for hover/active/disabled" is tractable. "Design a color token system" is not yet.

### Contrast and accessibility checking

Deterministic tools (axe-core, Stark, Leonardo) compute contrast ratios and APG conformance. AI's role is to *interpret* and *prioritize* the output, not to compute it. A useful prompt pattern:

> Given this token build report and these failing contrast pairs, identify which failures affect production tokens vs. internal-only tokens, suggest the minimum token-value adjustments to bring failures into compliance, and flag any pairs where the failure suggests a structural problem (e.g., a semantic token aliasing the wrong primitive).

This is the kind of reasoning AI handles well — pattern-matching across a structured input, applying domain rules, surfacing structural concerns. It can't replace the deterministic check; it can make the output of the check actionable.

### Automated token audit

Specific audits where AI shines, given a full token catalogue plus the consuming codebase:

- **Orphaned primitives.** Primitives not aliased by any semantic token. Often safe to remove; sometimes a sign of a missing semantic.
- **Naming inconsistency.** `color/bg/primary` and `color-bg-secondary` in the same system. AI flags reliably.
- **Missing semantic coverage.** Common patterns the AI knows about (hover/active/disabled state coverage, focus indicators, error/warning/success/info parity) that the system lacks.
- **Tier discipline.** Primitives directly referenced by components rather than via semantic tokens. AI catches this from the codebase.
- **Description gaps.** Tokens without `$description` fields — AI can detect and even suggest descriptions, though human review is needed.

These audits are well-suited to a one-shot prompt with the full catalogue as context. They're low-stakes (worst case: AI suggests a non-fix) and high-leverage (catches drift that humans miss in big systems).

### Brand-book-to-tokens

Multimodal AI can extract raw values from a brand book PDF — colors with hex codes, type scales, spacing rhythms — reliably. The bottleneck is **semantic translation**: the brand book says "primary brand color is #0066CC"; the token system needs to know whether that color is intended as a CTA color, a navigation surface color, a branded accent, or all three. AI guesses based on common conventions and is right enough of the time to be useful as a draft, wrong enough that a designer must validate every assignment.

The workflow:

1. Multimodal AI extracts raw values from the brand book.
2. AI proposes a primitive token catalogue (color scales, spacing, type) — usually correct.
3. AI proposes semantic mappings — review every one; expect to revise 30–50%.
4. Human validates against design intent and existing product usage.

This collapses the 1–2 week brand-extraction phase to about a day of human curation over an AI draft.

---

## 2. AI in Figma — design operations

### Figma's native AI features

As of early 2026, Figma has shipped or previewed several AI features. Names and exact scope have shifted across releases, so verify against current Figma docs. The capabilities cluster:

- **Make Designs / First Draft / prompt-to-mockup.** Generate a low-fidelity layout from a text prompt. Useful for early exploration; **not useful for DS work** because outputs don't use the system's tokens or components and produce off-system designs that need to be either discarded or refactored.
- **Asset/image-to-design.** Convert screenshots or wireframes to editable Figma. Useful for capturing reference material; same limitation re: DS adherence.
- **Auto-arrange / smart auto-layout suggestions.** Helps individual designers; tangential to DS authoring.
- **Component-property assistance.** Suggesting variant names, prop types. Marginal utility — gets generic answers right and specific design-system answers wrong.

**The honest read:** Figma's native AI is aimed at designers exploring ideas, not at DS authors building system components. For DS work, native AI is rarely the leverage point. The leverage is the MCP layer, which exposes the file to external AI tools that can be steered with DS context.

### Figma MCP server (Dev Mode MCP)

Figma's Model Context Protocol server — public preview late 2024, GA through 2025 — exposes the structure of a Figma file to MCP-capable clients (Claude Code, Cursor, Windsurf, custom agents). The agent can read the file structure and request specific node context.

The tools the server typically exposes:

- `get_variable_defs` — pull the token catalog for a given file or selection
- `get_code` — generate a code translation of a selected node, using available context (Code Connect, Variables)
- `get_code_connect_map` — return the Figma-to-code mapping for components in scope
- `get_screenshot` — image of a selected node, for visual reference
- `get_metadata` — structural metadata about the file/node

The practical workflow, in increasing order of context maturity:

1. **Bare Figma MCP, no Code Connect, no DS metadata.** Agent reads the file, generates code that resembles the design but uses hardcoded values and invented component names. Useful for exploration, not for production.
2. **Figma MCP + Code Connect.** Agent maps Figma components to real production components. Generated code references actual imports and props. Useful for routine implementation; struggles with composition and custom logic.
3. **Figma MCP + Code Connect + custom DS MCP exposing component metadata.** Agent has the full DS context — components-as-data, token catalog, Code Connect map, plus structured metadata about composition rules. Generated code is system-compliant and increasingly reliable for both implementation and composition.

**The architectural insight:** Figma MCP alone is insufficient. It exposes whatever's in the Figma file, and a Figma file optimized for designers is not the same as a structured component contract. Curtis's caveat — "stochastic, incomplete, and imprecise" — applies. The leverage compounds when MCP is paired with a structured DS data layer.

### Figma Console MCP

A newer entrant: an MCP server that lets AI agents *write* into Figma — create design files, populate FigJam boards, build component instances, apply tokens, take screenshots, run console-style commands inside the Figma plugin sandbox. Where Dev Mode MCP exposes Figma to external AI for *reading*, Console MCP makes Figma a target for AI *generation*.

For DS work, Console MCP enables workflows that previously required custom plugins:

- **Generating exemplar pages** for documentation from component metadata.
- **Bulk-applying token migrations** across a library file.
- **Auto-arranging component sets** in a consistent grid for handoff.
- **Producing screenshot variants** for documentation across themes/locales.

Caveats: writing into Figma raises governance questions (who reviews AI-generated changes? do they go through branches?), and the tooling around AI-driven Figma writes is still maturing. Verify the specific Console MCP capability surface against current docs — this is one of the faster-moving areas.

### Limits of Figma AI for DS work

Where human judgment is still required:

- **Component decomposition decisions.** Should this be one component with five slots or five components? AI proposes based on convention; the right answer depends on consumer team capability and brand expression goals.
- **Naming taxonomy.** AI defaults to generic conventions; system-specific naming (matching the production codebase, matching client vocabulary) requires human direction.
- **Composition vs. configuration trade-offs.** When does flexibility belong as props vs. as composition with slots? Judgment call; AI guesses.
- **Brand expression.** Whether a button feels "on-brand" is not something AI evaluates well. It produces structurally correct but characterless outputs.
- **Cross-component consistency.** Does this new component fit alongside the existing 50? Requires holding the system's gestalt in mind, which AI does poorly across long contexts.

---

## 3. AI in component development

### AI coding assistants

The dominant AI coding assistants in 2026 — Claude Code, Cursor, Copilot, Windsurf — all support MCP and all are usable for DS component work. The differences in DS context:

- **MCP support.** All have it; the maturity and the configurability vary.
- **Long-context handling.** Component implementations benefit from having the full DS catalogue in context. Tools with longer context windows (and that handle them well) produce more consistent output across multiple components.
- **Tool-use depth.** Tools that can query the filesystem, run lint, run tests, and self-correct produce better output than tools that emit code blind.

For DS work, the choice of assistant matters less than the choice of context architecture. A Cursor session with full DS context outperforms a Claude Code session with only a screenshot, and vice versa.

### Specs CLI and components-as-data

Nathan Curtis's **Specs CLI** (DirectedEdges/specs on GitHub) operationalizes the components-as-data POV laid out in his "Components as Data" essay. The architecture:

- A component is defined as **structured YAML** — `anatomy`, `props`, `default`, `variants`, plus metadata.
- This data is the **source of truth**. Figma assets, code, and documentation are *outputs* generated from it.
- Specs CLI is the build tool that takes the YAML and produces (or assists in producing) Figma component sets, code scaffolds, and documentation.

The argument: components built independently in Figma and code drift apart. Components generated from a single data source stay aligned by construction.

**Maturity, as of early 2026:** Specs CLI is a recent and evolving project. It's usable; it's not yet a commodity tool with broad enterprise adoption. Practitioners using it report that the YAML-to-Figma pipeline works well for simpler components and requires more hand-tuning for complex ones; the YAML-to-code pipeline is more about generating consistent scaffolds than turn-key production code. Verify the current scope at the repo before committing a client to it.

The deeper point — and the reason this is in the prompt's "particular focus" — is that the components-as-data POV is the **architectural prerequisite for AI to do reliable DS work**. Without structured data describing what the component *is* (anatomy, intended composition, props with semantic meaning), AI tools have only artifacts (a Figma file, a code snippet) and have to infer intent from structure. Inference from artifacts is unreliable. Generation from structured data is reliable.

This applies whether or not Specs CLI is the specific tool used. The principle generalizes: any structured component data layer (Specs YAML, `.ai.json`, Wolosin's metadata schema, Adobe Spectrum's component descriptors) gives AI the contract to generate against. Without one, AI is guessing.

### Prompt strategies for token-compliant code

The pattern that produces the most reliable output:

1. **System prompt sets the frame.** "You are generating component code for a design system that targets WCAG 2.2 AA, uses CSS custom properties for tokens (no hardcoded values), and follows these naming conventions: [...]."
2. **Token catalog as context.** Provide the full token list (or at least the relevant subset) so the AI knows which tokens exist and their intended use.
3. **Component schema as context.** Provide the structured component data (props, variants, slots) so the AI generates the right interface.
4. **Production component imports as context.** Provide the import paths for adjacent components the new one might compose with.
5. **Concrete output specification.** "Generate the implementation as a single React component with TypeScript types matching the props above. Use only tokens; no hardcoded values. Implement keyboard handling per WAI-ARIA APG `dialog` pattern."

Without (1)–(4), output drifts. With them, output is consistent across runs.

### Variant generation

AI is reliably good at **expanding from a working base**. Given the rest state of a button, generating hover/active/focus/disabled states is tractable. Given a Default size, generating Small/Medium/Large is tractable. The constraint that makes this work: the AI has a specific working component to extend, not a blank slate.

The same principle applies to props: given a working component, "add a `loading` prop that shows a spinner and disables the button" produces reliable output. "Generate all the props this button might need" does not.

### AI for code review

AI is useful for catching specific classes of issue in generated or human-written code:

- **Hardcoded values.** "Find any color, spacing, or typography values not referenced via tokens." Reliable.
- **Missing accessibility attributes.** "Find buttons without accessible labels, form inputs without labels, images without alt text." Reliable.
- **Naming inconsistency.** "Find props that don't match the system's naming conventions." Reliable.
- **Token misuse.** "Find tokens applied at the wrong tier (primitive instead of semantic)." Reliable when the convention is documented.
- **APG conformance.** "Check this composite widget against the APG `combobox` pattern." Useful as a draft; needs human verification because AI hallucinates ARIA.

It is *not* yet reliable for:

- Composition correctness (does this component compose well with the rest?)
- Performance (is this implementation fast?)
- Security (does this introduce XSS, CSRF, etc.?)
- Cognitive accessibility (is this experience easy to use for someone with limited working memory?)

---

## 4. AI in documentation generation

### Generating usage guidelines

AI produces useful first drafts of:

- **Component descriptions.** Structural prose from anatomy + props.
- **Prop tables.** Trivial from schema.
- **State coverage.** "Document all the states this component supports and when each appears."
- **Examples.** Code snippets showing common usage.

It produces less useful drafts of:

- **When-to-use / when-not-to-use.** AI is risk-averse and produces excessive "consider whether..." hedges. Human edit pass cuts roughly half the prose.
- **Composition guidance.** Requires holding the system context; AI defaults to generic patterns.
- **Avoid-when patterns.** AI generates plausible avoid-whens but miscalibrates which are common in this specific system. Human curation required.

The pattern: **AI drafts; human edits.** Time savings of 60–80% are realistic. Quality is consistent because the drafts are consistent.

### Doc-in-sync maintenance

A specific high-leverage use: AI compares a component's current implementation against its current documentation, flags mismatches.

> The Button component now accepts a `loading` prop; the documentation does not mention it. Update the documentation.

This kind of incremental sync is well-suited to AI because it's pattern-matching against a specific delta. Practitioners using this in CI/PR workflows report meaningful reduction in doc drift, which is otherwise the failure mode that quietly accumulates over a year.

### Storybook and AI

AI can generate stories from component implementations — given the component file, it produces stories covering the major states and prop combinations. The output requires light editing (story names, knob/control configuration) but the time savings are real for libraries with many components.

For new components, the pattern that works: write the component, generate stories with AI, edit the story file. For existing libraries, AI can backfill stories en masse — useful when adopting Storybook into a library that wasn't previously Storybook-driven.

---

## 5. AI in design-to-development handoff

### Two paradigms

The fundamental architectural choice in design-to-code AI:

- **Screenshot-first.** AI receives a visual rendering and reproduces it in code. The simplest mental model; the lowest fidelity. Output looks like the design but uses invented component names, hardcoded values, and ad-hoc CSS. Useful for rapid prototyping; not for production DS work.
- **MCP-first (or context-first more broadly).** AI receives structured design context — variables, components, Code Connect mappings, component metadata — and generates code against the system's contracts. Output uses real tokens, imports real components, follows real conventions. Useful for production work; requires the system to expose context.

The practical trade-off: screenshot-first works against any system (including no system); MCP-first works only when the system has invested in the architecture. For an agency with a mature DS practice, MCP-first should be the default; screenshot-first is the exploratory tool.

### Code Connect

Figma's Code Connect maps Figma components to production code components. When set up, AI tools that consume Code Connect (via Figma MCP or directly) generate code that references actual production component imports and uses actual production prop names.

**Maturity, as of early 2026:** GA across React, Vue, SwiftUI, Jetpack Compose, and HTML; community implementations for other frameworks. Setup requires per-component manual mapping (one engineer-day per ~30–50 components, depending on complexity). The mapping lives in the engineering repo and must be maintained as the codebase evolves.

The integration with AI workflows is the main reason to invest in Code Connect today. Without Code Connect, an AI tool generating code from a Figma component has to guess at the component name and prop API. With Code Connect, the AI gets the right answer by construction.

### MCP servers in the DS architecture

The architectural picture for AI-assisted DS work involves several MCP servers, each contributing context:

- **Figma MCP** — design context (Variables, structure, screenshots, Code Connect map).
- **Specs CLI / components-as-data layer** — structured component definitions, anatomy, props, variants, intended composition.
- **Custom DS MCP server** — DS metadata, token catalog, governance rules, the `.ai.json` layer (or equivalent), component registry.
- **Engineering-repo MCP** (filesystem, Git, etc.) — the actual codebase the AI is generating into.

The full stack is rare in the wild today. Most teams have Figma MCP + a partial custom layer; the rigorous build (with Specs CLI or equivalent components-as-data) is a 2026-and-onward investment.

### Screenshot vs. full-context generation

The output difference, for the same Figma node:

- **Screenshot only.** Code that looks visually similar; uses hex codes; invents component names; flat CSS; no accessibility attributes beyond what's visible; no semantic HTML structure.
- **Full context** (Figma MCP + Code Connect + components-as-data + DS MCP). Code that imports real components; uses semantic tokens; matches naming conventions; includes correct ARIA from the component contract; structures HTML semantically per the documented anatomy.

The gap is large, and it grows with component complexity. Simple components (a styled box) are nearly equivalent. Complex components (a data table with sorting, filtering, accessibility, virtualization) diverge sharply — screenshot-only output is unusable for complex components; full-context output is often production-acceptable with light review.

**The minimum architecture for the workflow to work at all:**

1. **Components-as-data** (or equivalent structured component contract). Without this, AI doesn't know what the component *is* beyond what it can infer from the rendered artifact.
2. **DTCG-compliant tokens with descriptions.** Without this, AI doesn't know what tokens exist or which to apply.
3. **Code Connect or equivalent mapping.** Without this, AI doesn't know what production components exist.
4. **Component metadata** (`.ai.json`, Wolosin schema, or equivalent). Without this, AI doesn't know composition rules, when-to-use boundaries, or accessibility requirements.

A team that ships an MCP integration without these architectural prerequisites has built a fast path to inconsistent code. A team that ships them in order has built the substrate for AI to do real DS work.

---

## 6. AI in governance and ongoing maintenance

### Drift detection

Detecting when production code diverges from DS specifications is a real use case where AI is starting to be useful but isn't yet reliably productized. The shape of the workflow:

1. AI scans a consuming codebase against the DS component catalogue.
2. Identifies components implemented locally that should be using DS components.
3. Identifies DS components used in non-conforming ways (wrong props, wrong tokens, modified styling).
4. Produces a drift report.

This works in proof-of-concept and is appearing in some commercial tools. The accuracy is uneven — false positives are common — and the report typically needs human triage before becoming an actionable backlog. Worth piloting; not yet worth selling as a polished offering.

### Coverage analysis

A related use case: surveying a product to find UI patterns that aren't yet in the DS but probably should be. AI scans product files, clusters similar patterns, flags candidates for systematization.

This works better than drift detection because the output is suggestive (a candidate list) rather than declarative (a violation list). Useful as input to quarterly DS planning. Limited by AI's pattern-matching, which clusters by visual similarity and sometimes misses semantic equivalence (two visually different toast components that serve the same role).

### Changelog and versioning

AI-generated changelogs from git diffs are reliably useful — produces a draft changelog covering the changes, typically requires light editing for tone and to elevate the user-facing impact over the technical change.

Semver bump suggestions from a diff are also useful as drafts. AI can usually identify breaking changes (renamed props, removed components) but occasionally misses subtler breaks (changed default values, modified ARIA behavior). Human review of the suggestion is short and high-leverage.

### Contribution review

Using AI as a first-pass review on proposed components — checking against accessibility patterns, naming conventions, token compliance, structural standards — is feasible and is being adopted by some teams. The shape:

1. Contributor opens PR with a new component.
2. CI runs AI review against documented standards.
3. AI produces a report: passes, warnings, blocking issues.
4. Human reviewer uses the report as input to their review, not as a replacement.

This works when the standards are well-documented (so the AI has criteria to apply) and when the reviewer treats AI output as advisory. The failure mode is treating AI output as authoritative — AI hallucinates standards that don't exist and fails to apply standards that do.

The decision: **AI as gate or AI as advisory?** Most mature systems should default to **advisory**. A blocking gate that produces false positives erodes trust in the system; an advisory layer that surfaces candidates for human attention sustains it. As models improve, the balance shifts; today the balance favors advisory.

---

## 7. AI-ready DS architecture

### Components-as-data as the prerequisite

The thesis, sharpened: **AI-in-DS workflows fail or succeed on whether the component is defined as structured data.** This is Curtis's argument and it is the load-bearing claim of this entire document.

Why: AI models are pattern-matchers over their input. Given a Figma file, they pattern-match against visual layout. Given a code snippet, they pattern-match against syntax. Neither artifact carries the *intent* of the component — what it is, what it composes with, what it must do, what it must not do. Without intent, AI extrapolates. Extrapolation produces inconsistency at scale.

A structured component data layer makes intent explicit:

```yaml
component: Button
type: action
anatomy:
  - id: container
    type: container
  - id: leadingIcon
    type: slot
    optional: true
  - id: label
    type: text
  - id: trailingIcon
    type: slot
    optional: true
props:
  variant: [primary, secondary, tertiary, danger]
  size: [small, medium, large]
  disabled: boolean
  loading: boolean
default:
  variant: primary
  size: medium
metadata:
  apg_pattern: button
  required_label: true
  composition_rules:
    - cannot_contain: [Button, Link]
  avoid_when:
    - "Use Link for navigation"
    - "Use IconButton when only an icon is needed"
```

Given this, AI knows what a `Button` *is*, what it must contain, what it can't contain, what props it accepts, what defaults apply, and what conventions it follows. Generation against this contract is reliable. Generation without it is hopeful.

This is true whether the structured layer is YAML (Specs CLI's choice), JSON (Wolosin's schema), or a custom format. The format is less important than the existence.

### What the structured layer must contain

Minimum fields, drawing from Curtis (anatomy/props/default/variants), Wolosin's 12-field schema, and the practice's `.ai.json`:

- **Identity.** `id`, `type` (action, surface, navigation, feedback, input, etc.), `description`.
- **Anatomy.** Internal structure with named parts; types (container, slot, text, icon).
- **Props.** Name, type, allowed values, description, default.
- **Variants.** Discrete variant matrices that produce structurally different outputs.
- **Composition rules.** Cannot-contain, common-partners, parent constraints.
- **Usage metadata.** When-to-use, avoid-when, common misuse patterns.
- **Accessibility metadata.** APG pattern reference, required labels, keyboard behavior, ARIA roles set internally.
- **Token references.** Which tokens the component uses and at which leaf elements.

This layer is what an AI agent needs to generate reliable code, reliable docs, reliable Figma assets, and reliable governance checks. It is also what a human contributor needs to author a new component consistently with the rest of the system. **The structured layer serves AI and humans equivalently**, which is part of why it works.

### DTCG tokens as the parseable structure for the foundation layer

The token side of the architecture has stabilized around the W3C DTCG format — a JSON schema for tokens that's machine-parseable, type-aware, and supports the full range of design token types (color, dimension, duration, shadow, gradient, typography composite, etc.).

DTCG matters for AI because it gives the agent a structured contract for tokens equivalent to what components-as-data gives for components. An AI agent given a DTCG file knows:

- Which tokens exist
- Their types (color vs. dimension vs. composite)
- Their values (and through aliases, their resolution chains)
- Their descriptions (when authored)
- Their groupings (categories and hierarchies)

Generation against DTCG is reliable in the same way generation against components-as-data is reliable. The two layers compose: structured tokens + structured components = a substrate AI can generate against end-to-end.

### MCP server architecture for a DS

The shape of a complete DS-side MCP architecture, as it's emerging:

```
DS source files (components-as-data + DTCG tokens + metadata)
    │
    ├── built into → Figma library, code package, docs site (as outputs)
    │
    ├── exposed via Figma MCP → AI clients see the design surface
    │
    └── exposed via custom DS MCP → AI clients see the structured contract
```

The custom DS MCP server is what most teams haven't built yet. Its tools, conceptually:

- `list_components` — return the catalogue
- `get_component(id)` — return full structured data for one
- `search_components(query)` — find components matching intent
- `get_token_catalog()` — return tokens (with descriptions)
- `get_composition_rules(component_id)` — return what this composes with
- `get_usage_guidelines(component_id)` — return when-to-use / avoid-when
- `validate_implementation(code, component_id)` — check generated code against the contract

This is what "AI-ready DS architecture" looks like in 2026. Most teams have pieces of it; few have the whole stack. It's a 2026–2027 investment for shops that want to lead.

---

## 8. Current limits and honest assessment

### What ships and works today

- **AI as token-taxonomy critic.** Audit existing taxonomies for gaps and inconsistencies. Reliable.
- **AI for documentation drafts.** Component descriptions, prop tables, basic usage. 60–80% of the work; human edit pass required.
- **AI for variant generation from a working base.** Hover/active/disabled states, size variants. Reliable.
- **AI for code review against documented standards.** Token compliance, missing labels, naming consistency. Reliable when standards are explicit.
- **MCP-driven code generation with full DS context.** Production-acceptable for routine components when the DS architecture is in place. Increasingly reliable through 2025–2026.
- **AI changelog drafts from git diffs.** Reliable; light human edit required.
- **AI as advisory in PR review.** Useful first-pass; not yet trustworthy as an autonomous gate.
- **Brand-book extraction with multimodal AI.** Raw value extraction reliable; semantic mapping requires curation.

### What is aspirational

- **End-to-end Figma → production code with no human in the loop.** Demos exist; production reliability does not. Routine components get close; complex components don't.
- **AI authoring components from scratch (no design first).** Produces plausible-looking but inconsistent components that need significant rework.
- **AI-driven contribution gating.** Workable as advisory; not yet workable as authoritative.
- **AI-driven full-codebase drift detection.** Proof-of-concept maturity; not productized.
- **Cross-platform code generation that's natively idiomatic on each platform.** AI generates web well, native less well, Flutter unevenly. Specific to the model and the context provided.
- **Generative design that understands brand voice.** AI produces structurally correct but characterless output; brand judgment remains human.

### Quality and consistency issues

- **Naming drift across multiple AI generations.** Run the same prompt twice, get two different naming conventions. Mitigated by aggressive context (style guide, examples) but never eliminated.
- **Token drift.** AI applies tokens correctly when they're well-named and well-described; defaults to hardcoded values or invented tokens otherwise. Quality of the token system directly determines quality of AI output.
- **Hallucinated APG patterns.** AI confidently produces ARIA that's wrong. Always verify against the actual APG.
- **Over-engineering.** AI defaults to expansive prop APIs. Curate aggressively.
- **Composition errors.** AI struggles to keep cross-component consistency in mind across long generation sessions. Periodic review is necessary.

### Organizational and governance challenges

- **Review burden.** AI generates code faster than humans can carefully review. Trusting AI output too quickly leads to bugs that compound; reviewing every line conservatively erases the speed gain.
- **Attribution.** AI-generated code in a public OSS-licensed system raises licensing and attribution questions. Most agencies handle this case-by-case; few have policies.
- **Skill atrophy.** Engineers and designers who delegate routine work to AI may not develop the underlying skills. Real concern for junior practitioners; less so for senior ones who have the skills already.
- **Vendor lock-in.** Commitments to specific AI tools, MCP servers, or integrations create dependencies that may not age well as the tooling churns.
- **Cost.** Frontier AI tools used at scale across a team cost real money. Budgets need to anticipate this.

### What still requires human judgment

- **Brand expression.** What feels right is not what AI produces.
- **Strategic component decisions.** When does this pattern become a component? When does this component become a pattern? When does the system absorb this exception?
- **Governance decisions.** Who can contribute? What's our accessibility floor? When do we deprecate?
- **Stakeholder communication.** Translating system decisions to non-technical clients.
- **Cross-functional negotiation.** Brand vs. accessibility vs. engineering velocity vs. product timeline. AI can summarize the tradeoffs; the negotiation is human.
- **Quality calibration.** Is this component good enough to ship? AI doesn't have taste; humans do.

The leverage is real. The leverage is not unconditional. The condition is the architecture: structured tokens, structured components, structured metadata, exposed via MCP. Build that, and AI accelerates DS work meaningfully. Skip it, and AI produces output that looks like progress but isn't.

---

## References

Primary sources, current as of Jan 2026.

**Figma:**
- Figma AI features: <https://help.figma.com/hc/en-us/sections/24468570714007>
- Figma Dev Mode MCP server: <https://help.figma.com/hc/en-us/articles/32132100833559>
- Figma Code Connect: <https://www.figma.com/code-connect-docs/>

**MCP and components-as-data:**
- Anthropic MCP specification: <https://modelcontextprotocol.io/>
- Nathan Curtis — *Components as Data* (Sep 2025): <https://medium.com/@nathanacurtis/components-as-data-2be178777f21>
- Specs CLI: <https://github.com/DirectedEdges/specs>
- W3C DTCG specification: <https://design-tokens.github.io/community-group/format/>

**Practitioner sources:**
- Nathan Curtis — *Design Tokens* (Nov 2024) and ongoing EightShapes writing: <https://medium.com/eightshapes-llc>
- Diana Wolosin — Indeed component metadata work (Jun 2025); 12-field metadata schema
- Figma DS x AI (2025) — Figma's published thinking on AI integration
- Sam Anderson — *Design Systems are Infrastructure* (Nov 2024)

**AI coding assistants:**
- Claude Code: <https://docs.claude.com/en/docs/claude-code>
- Cursor: <https://cursor.com/>
- GitHub Copilot: <https://github.com/features/copilot>
- Windsurf: <https://codeium.com/windsurf>

**Token tooling:**
- Style Dictionary: <https://amzn.github.io/style-dictionary/>
- Tokens Studio: <https://tokens.studio/>
- Adobe Leonardo (color contrast): <https://leonardocolor.io/>

**Note on currency:** This area moves faster than any other DS topic in this vault. Specific feature surfaces, plan-tier capabilities, MCP tool sets, and AI assistant integration claims cited above reflect early 2026 state and may have evolved. The architectural patterns (components-as-data, DTCG tokens, structured metadata, MCP exposure) are more durable than the tool names attached to them. Verify before client-facing recommendation.

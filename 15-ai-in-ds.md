---
type: practice-area
title: AI in Design Systems
description: AI integration across the DS lifecycle. Components-as-data as architectural prerequisite. MCP, Figma MCP and Code Connect, three-level context maturity, the four-prerequisite minimum architecture.
tags: [extension, ai, mcp, components-as-data, code-connect]
timestamp: 2026-06-10
---

# 15 — AI in Design Systems Practice

> AI in design systems work compounds where the architecture is structured and fails where it isn't. Components-as-data, DTCG tokens, Code Connect, structured metadata exposed via MCP — these are not optional add-ons; they are the prerequisites that make AI tools produce reliable output instead of confident hallucinations. This file covers how AI integrates across the lifecycle and the architecture that makes the integration pay off. It also covers the limits, honestly, because the field is moving fast enough that confident assertions today will be inaccurate within months.
>
> Scope note: this file is the (a)-axis of the AI-in-DS split — AI features the design system *operates internally* (token critique, codegen, MCP-served metadata, drift detection). The sibling (b)-axis — AI features the design system *ships as patterns to consumers* (chat input, streaming response, citation, refusal, tool-call rendering) — lives in 25-ai-aware-patterns-and-conversational-ui. The third axis — adaptive interfaces that *reshape themselves* in real time around user, moment, and task — lives in 26-adaptive-interfaces-foundations and 27-adaptive-interfaces-implementation. All three share the same components-as-data substrate; they differ in what gets shipped on top of it. The three are easy to conflate in scoping conversations and meaningfully different in what they require to ship.

---

## A note on currency before anything else

This space rotates faster than any other DS topic in this vault. Specific feature names, MCP tool surfaces, plan-tier capabilities, and AI-assistant integrations cited below reflect the platform state as of early 2026 and may have evolved by the time anyone reads this. **Where claims are platform-state-dependent, we date them and flag the verification path.** The architectural shape — components-as-data, DTCG tokens, structured metadata exposed via MCP — is more durable than the tool names attached to it. Bet on the architecture, not on the tool.

---

## AI in token creation and validation

### AI as critic, not author

The most useful pattern is **AI as critic of existing taxonomy, not author of new taxonomy from scratch**. Asked to "generate a token taxonomy from scratch," current frontier models produce plausible but over-engineered output — too many tiers, redundant naming, semantic tokens that wrap one primitive each, conventions that don't match any actual codebase. Asked to "audit this token taxonomy for missing semantic coverage, redundant primitives, and naming inconsistencies," the same models produce useful surgical critique. We land on the cautious side here because author-mode is the failure mode — though some practitioner writing is more bullish about AI-driven taxonomy generation.

The workflow that works:

1. Human drafts the taxonomy (or feeds in an existing one).
2. AI receives the full taxonomy plus contextual brief — brand intent, target consumers, scale, theming dimensions.
3. AI returns a critique: gaps, inconsistencies, duplications, naming suggestions.
4. Human curates — about half to two-thirds of suggestions are useful; the rest are too cautious or miss the point of a deliberate choice.

For taxonomy *generation*, AI is best used to expand within a structure the human has decided. "Given this primitive scale and these semantic categories, propose semantic tokens for hover/active/disabled" is tractable. "Design a color token system" is not yet.

### AI-assisted contrast and accessibility checking

Deterministic tools (axe-core, Stark, Leonardo) compute contrast ratios. **AI's role is to interpret and prioritize the output, not to compute it.** A useful prompt:

> Given this token build report and these failing contrast pairs, identify which failures affect production tokens vs. internal-only tokens, suggest the minimum token-value adjustments to bring failures into compliance, and flag any pairs where the failure suggests a structural problem.

The token-pair architecture from 14-accessibility makes this much more tractable: the AI is reasoning about a contract (this pair must meet this ratio) rather than guessing intent.

A related capability is **expression tokens / math** — conditional logic and math-driven computation inside a variable's value. **Not part of the DTCG 2025.10 stable spec.** Tokens Studio's math syntax is the most-adopted implementation; Style Dictionary v4 preprocessors handle the same job at build time. The convergent practitioner discipline is **compute at authoring time, ship literals at runtime** — expression resolution is a build-time artefact, not a runtime contract. (See 22-token-architecture-extensions for the spec depth and the trade-off framing.) For AI agents specifically, this means agents reason about literal values at runtime — token permutation across modes runs in the build pipeline, and AI-driven contrast/regression checks consume the resolved literals.

### Automated token audits

Specific audits where AI is reliable, given a full token catalogue plus the consuming codebase:

- **Orphaned primitives.** Primitives not aliased by any semantic token. Often safe to remove; sometimes a sign of a missing semantic.
- **Naming inconsistency.** `color/bg/primary` and `color-bg-secondary` in the same system. AI flags reliably.
- **Missing semantic coverage.** Common patterns (hover/active/disabled state coverage, focus indicators, error/warning/success/info parity) the system lacks.
- **Tier discipline.** Primitives directly referenced by components rather than via semantic tokens.
- **Description gaps.** Tokens without `$description` fields — AI can detect and suggest descriptions, though human review is needed.
- **Hard-coded values in consuming code.** Hex codes, pixel values, magic numbers that should be aliased through tokens. Tools like **Design Lint** have evolved to include semantic understanding for this.

These audits are well-suited to one-shot prompts with the full catalogue as context. They're low-stakes (worst case: a non-fix suggestion) and high-leverage (catch drift that humans miss in big systems).

### Brand-book to token architecture

Multimodal AI can extract raw values from a brand book PDF — colors with hex codes, type scales, spacing rhythms — reliably. The bottleneck is **semantic translation**: the brand book says "primary brand color is `#0066CC`"; the token system needs to know whether that color is intended as a CTA color, a navigation surface color, a branded accent, or all three. AI guesses based on conventions and is right enough of the time to be useful as a draft, wrong enough that a designer must validate.

The workflow:

1. Multimodal AI extracts raw values from the brand book.
2. AI proposes a primitive token catalogue (color scales, spacing, type) — usually correct.
3. AI proposes semantic mappings — review every one; expect to revise 30–50%.
4. Human validates against design intent and existing product usage.

This collapses the 1–2 week brand-extraction phase to about a day of human curation over an AI draft. (See 02-design-foundations on the broader Foundations phase.)

---

## AI in Figma — design operations

### Figma's native AI features

Figma has shipped or previewed several AI features through 2025–2026. Names and exact scope have shifted across releases; **verify against current Figma docs before quoting specific maturity labels.** The capabilities cluster:

| Feature | Reported maturity (verify) | Practical DS use case |
|---|---|---|
| First Draft (formerly Make Designs) | Reported as GA | Generating new pattern ideas using system tokens — when configured to respect system context |
| Rename with AI | Reported as GA | Cleaning up layer naming debt across files; useful for bulk fixes |
| Visual Search | Reported as GA | Finding existing components via screenshot to prevent duplication |
| Figma Make | Reported as Beta | Prompt-to-prototype with token linkage |
| Smart Page Summaries | Reported as GA | Auto-generating overviews of dense documentation pages |

The labels above are reported in current research as the maturity state of these features; verify against current Figma documentation before client-facing recommendations.

The honest read: Figma's native AI is aimed at designers exploring ideas, not at DS authors building system components. The features that matter most for DS work are:

- **Rename with AI** — concretely useful for cleaning up legacy file naming.
- **Visual Search** — useful for component discovery, particularly for preventing duplicate component proposals.
- **First Draft** — useful only when paired with strong system constraints; without them, generates off-system designs.

For DS authoring, **the leverage is the MCP layer, not native AI.** Native AI helps individual designers; MCP exposes the system to external AI tools that can be steered with DS context.

### Figma MCP server (Dev Mode MCP)

Figma's Model Context Protocol server — public preview late 2024, GA through 2025 — exposes the structure of a Figma file to MCP-capable clients (Claude Code, Cursor, Windsurf, custom agents). The agent reads the file structure and requests specific node context.

The tools the server typically exposes:

- `get_variable_defs` — pull the token catalog
- `get_code` — generate a code translation of a selected node, using available context
- `get_code_connect_map` — return the Figma-to-code mapping for components in scope
- `get_screenshot` — image of a selected node, for visual reference
- `get_metadata` — structural metadata about the file/node

The official server is **primarily optimized for read-only operations** when used with personal access tokens. Advanced write capabilities require additional plugins or alternative servers.

### Figma Console MCP and write access

A separate MCP implementation, **Figma Console MCP** (developed by Southleft), extends the official capabilities by providing project-wide context and full **write access** through a "Desktop Bridge" plugin and a "bootloader" architecture. This allows AI agents to write directly to the Figma canvas — creating frames, components, and variables through natural language commands, applying token migrations across thousands of nodes, generating exemplar pages from component metadata.

For DS work, Console MCP enables workflows that previously required custom plugins:

- **Generating exemplar pages** for documentation from component metadata.
- **Bulk-applying token migrations** across a library file.
- **Auto-arranging component sets** in a consistent grid for handoff.
- **Producing screenshot variants** for documentation across themes/locales.

Caveats: writing into Figma raises governance questions (who reviews AI-generated changes? do they go through branches?), and the tooling around AI-driven Figma writes is still maturing. **Verify Console MCP's specific capability surface against current docs** — this is one of the faster-moving areas.

### Three context-maturity levels

The practical workflow with MCP, in increasing order of context maturity:

1. **Bare Figma MCP, no Code Connect, no DS metadata.** Agent reads the file, generates code that resembles the design but uses hardcoded values and invented component names. Useful for exploration; not for production.
2. **Figma MCP + Code Connect.** Agent maps Figma components to real production components. Generated code references actual imports and props. Useful for routine implementation; struggles with composition and custom logic.
3. **Figma MCP + Code Connect + custom DS MCP exposing component metadata.** Agent has the full DS context — components-as-data, token catalog, Code Connect map, plus structured metadata about composition rules. Generated code is system-compliant and increasingly reliable for both implementation and composition.

**The architectural insight:** Figma MCP alone is insufficient. It exposes whatever's in the Figma file, and a Figma file optimized for designers is not the same as a structured component contract. **The leverage compounds when MCP is paired with a structured DS data layer** — which is the load-bearing argument of §7 below.

### Limits of Figma AI for DS authoring

Where human judgment is still required:

- **Component decomposition decisions.** One component with five slots vs. five components? AI proposes based on convention; the right answer depends on consumer team capability and brand expression goals.
- **Naming taxonomy.** AI defaults to generic conventions; system-specific naming requires human direction.
- **Composition vs. configuration trade-offs.** When does flexibility belong as props vs. as composition with slots? Judgment call; AI guesses.
- **Brand expression.** Whether something feels "on-brand" is not something AI evaluates well. Structurally correct, characterless outputs.
- **Cross-component consistency.** Holding the system's gestalt across a long context is something AI does poorly.

(See 12-figma-practice for the broader Figma practice context.)

---

## AI in component development

### Components-as-data: Curtis's POV, sharpened

The thesis, sharpened: **AI-in-DS workflows fail or succeed on whether the component is defined as structured data.** Curtis's *Components as Data* essay is the canonical reference; 03-component-library already names this as the post-tokens architectural move.

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

Given this, AI knows what a `Button` *is*, what it must contain, what it can't contain, what props it accepts, what defaults apply, and what conventions it follows. **Generation against this contract is reliable. Generation without it is hopeful.**

This is true whether the structured layer is YAML (Specs CLI's choice), JSON (Wolosin's schema), or a custom format. **The format is less important than the existence.**

### Specs CLI

Nathan Curtis's **Specs CLI** (DirectedEdges/specs on GitHub) operationalizes the components-as-data POV. The architecture:

- A component is defined as **structured YAML** — anatomy, props, default, variants, metadata.
- This data is the **source of truth.** Figma assets, code, and documentation are *outputs* generated from it.
- Specs CLI is the build tool that takes the YAML and produces (or assists in producing) Figma component sets, code scaffolds, and documentation.

The workflow has several stages:

- `specs fetch` — retrieve raw variables, styles, and file data from Figma.
- `specs scan` — identify components and build a manifest of system assets.
- `specs generate` — build the machine-readable component specifications.

The CLI essentially translates the visual and variable logic of Figma into the structured data format that LLMs favor.

**Maturity, as of early 2026:** Specs CLI is a recent and evolving project. Usable; not yet a commodity tool with broad enterprise adoption. The YAML-to-Figma pipeline works well for simpler components and requires more hand-tuning for complex ones; the YAML-to-code pipeline is more about generating consistent scaffolds than turn-key production code. **Verify the current scope at the repo before committing a client to it.**

The deeper point — and the reason this is the architectural backbone of this file — is that Specs CLI is one tool *embodying* the components-as-data POV. Other implementations exist or are emerging (Wolosin's metadata schema, our practice's `.ai.json`). What matters is that **the structured data layer exists**, not which specific tool produces it.

### AI coding assistants

The dominant AI coding assistants in 2026 — Claude Code, Cursor, Copilot, Windsurf — all support MCP and all are usable for DS component work.

| Tool | Role | Integration |
|---|---|---|
| Claude Code | CLI-based agent for implementation | MCP (Figma, Storybook, custom DS servers) |
| Cursor | IDE for AI-driven development | MCP, Figma plugins |
| GitHub Copilot | Inline code generation | IDE extension |
| Windsurf | IDE-based agent | MCP |
| Specs CLI | Context generator (not an assistant itself) | Produces YAML/JSON manifests for assistants to consume |

The choice of assistant matters less than the choice of context architecture. **A Cursor session with full DS context outperforms a Claude Code session with only a screenshot, and vice versa.** Bet on the context.

### Prompt strategies for token-compliant code

The pattern that produces the most reliable output:

1. **System prompt sets the frame.** "You are generating component code for a design system that targets WCAG 2.2 AA, uses CSS custom properties for tokens (no hardcoded values), and follows these naming conventions: [...]."
2. **Token catalog as context.** Provide the full token list (or relevant subset) so the AI knows which tokens exist and their intended use.
3. **Component schema as context.** Provide the structured component data (props, variants, slots) so the AI generates the right interface.
4. **Production component imports as context.** Provide import paths for adjacent components the new one might compose with.
5. **Concrete output specification.** "Generate the implementation as a single React component with TypeScript types matching the props above. Use only tokens; no hardcoded values. Implement keyboard handling per WAI-ARIA APG `dialog` pattern."

Without (1)–(4), output drifts. With them, output is consistent across runs.

The shift in prompting style: rather than "implement a blue button," practitioners now prompt with system references — "Using the `Button` anatomy and the `color/action/primary` collection from our MCP context, implement a React component supporting a disabled state with `aria-label` for icons." The result is production-ready code rather than what practitioners increasingly call "AI slop" — code that looks correct but uses invented component names and hardcoded values.

### Variant generation

AI is reliably good at **expanding from a working base**. Given the rest state of a button, generating hover/active/focus/disabled states is tractable. Given a Default size, generating Small/Medium/Large is tractable. The constraint that makes this work: the AI has a specific working component to extend, not a blank slate.

The same principle applies to props: given a working component, "add a `loading` prop that shows a spinner and disables the button" produces reliable output. "Generate all the props this button might need" does not.

A related capability sometimes referenced is **"Smart Variant Adaptation"** — the pattern of generating responsive variants (mobile, tablet) automatically from a desktop base implementation. The underlying capability is plausible and useful if available; verify the specific feature naming before committing to it in client materials.

### AI for code review

AI is useful for catching specific classes of issue in generated or human-written code:

- **Hardcoded values.** "Find any color, spacing, or typography values not referenced via tokens." Reliable.
- **Missing accessibility attributes.** "Find buttons without accessible labels, form inputs without labels, images without alt text." Reliable. (Connects to 14-accessibility on automated a11y checks.)
- **Naming inconsistency.** "Find props that don't match the system's naming conventions." Reliable.
- **Token misuse.** "Find tokens applied at the wrong tier (primitive instead of semantic)." Reliable when the convention is documented.
- **APG conformance.** "Check this composite widget against the APG `combobox` pattern." Useful as a draft; needs human verification because **AI hallucinates ARIA**.

It is *not* yet reliable for:

- Composition correctness (does this component compose well with the rest?)
- Performance (is this implementation fast?)
- Security (does this introduce XSS, CSRF, etc.?)
- Cognitive accessibility (is the experience easy for users with limited working memory?)

---

## AI in documentation generation

### Generating usage guidelines

AI produces useful first drafts of:

- **Component descriptions.** Structural prose from anatomy + props.
- **Prop tables.** Trivial from schema.
- **State coverage.** "Document all the states this component supports and when each appears."
- **Examples.** Code snippets showing common usage.

It produces less useful drafts of:

- **When-to-use / when-not-to-use.** AI is risk-averse and produces excessive "consider whether..." hedges. Human edit pass cuts roughly half the prose.
- **Composition guidance.** Requires holding system context; AI defaults to generic patterns.
- **Avoid-when patterns.** AI generates plausible avoid-whens but miscalibrates which are common in this specific system.

The pattern: **AI drafts; human edits.** Time savings of 60–80% are realistic. Quality is consistent because the drafts are consistent.

| Documentation type | AI-assisted content | Reliability |
|---|---|---|
| Prop tables | Auto-generated from component schema | High |
| Usage examples | Code snippets from stories | High (context-aware) |
| Behavioral summaries | Drafted from anatomy and APG pattern | High with light review |
| Avoid-when / context notes | Drafted from system metadata | Moderate (requires curation) |
| Change logs | Summarized from commits and token diffs | High (automated) |

### Doc-in-sync maintenance

A specific high-leverage use: AI compares a component's current implementation against its current documentation and flags mismatches.

> The Button component now accepts a `loading` prop; the documentation does not mention it. Update the documentation.

This kind of incremental sync is well-suited to AI because it's pattern-matching against a specific delta. Practitioners using this in CI/PR workflows report meaningful reduction in doc drift, which is otherwise the failure mode that quietly accumulates over a year.

### Storybook and the AI component manifest

Storybook has become a critical node in the AI-ready DS. A Storybook capability worth noting is the **components manifest** (sometimes referenced as `experimentalComponentsManifest` in current research; verify the specific feature flag name against current Storybook docs) — a feature that generates a machine-readable package of component metadata: APIs with validated prop types, usage examples from stories, JSDoc descriptions, test suites that encode requirements.

By exposing this manifest through an MCP server, Storybook gives AI agents **curated, machine-readable context** about how a component is *actually* used in production stories — not how the AI guesses it should be. This prevents the agent from inventing patterns and produces higher-quality code with lower token costs (less context needed because the context is denser).

Whether `experimentalComponentsManifest` is the canonical name or not, the architecture is real and worth investing in: Storybook stories are an underused source of DS context for AI tools.

### Storybook story generation

AI can generate stories from component implementations — given the component file, it produces stories covering major states and prop combinations. Output requires light editing (story names, knob/control configuration); time savings are real for libraries with many components.

For new components: write the component, generate stories with AI, edit. For existing libraries that aren't yet on Storybook: AI can backfill stories en masse — useful for adoption.

---

## AI in design-to-development handoff

### Two paradigms

The fundamental architectural choice in design-to-code AI:

- **Screenshot-first.** AI receives a visual rendering and reproduces it in code. Simplest mental model; lowest fidelity. Output looks like the design but uses invented component names, hardcoded values, ad-hoc CSS. Useful for rapid prototyping; not for production DS work.
- **Context-first (MCP-driven).** AI receives structured design context — variables, components, Code Connect mappings, component metadata — and generates code against the system's contracts. Output uses real tokens, imports real components, follows real conventions. Useful for production work; requires the system to expose context.
- **Code-Connect-driven.** Goes further: every Figma component is mapped to a specific code component. AI generation reduces to "instantiate this component with these props." Highest fidelity; requires the heaviest setup investment.

| Approach | Mechanism | Quality |
|---|---|---|
| Screenshot-to-code | Visual inference from pixels (e.g., GPT-4o Vision) | Low to moderate; prone to "AI slop" and token misalignment |
| Context-aware code | Direct data extraction via MCP / Specs CLI | High; token-accurate, system-consistent |
| Code-Connect-driven | Linking to existing production components | Very high; near-zero translation |

**For an agency with a mature DS practice, MCP-first should be the default; screenshot-first is the exploratory tool.** Code-Connect-driven is the right target for engagements with longer time horizons and committed engineering investment.

### Code Connect

Figma's Code Connect is the primary mechanism for linking design components to production code. By 2026, GA across React, Vue, SwiftUI, Jetpack Compose, and HTML; community implementations for other frameworks. Setup requires per-component manual mapping (one engineer-day per 30–50 components, depending on complexity). The mapping lives in the engineering repo and must be maintained as the codebase evolves.

The integration with AI workflows is the main reason to invest in Code Connect today. Without it, an AI tool generating code from a Figma component has to guess at the component name and prop API. With it, the AI gets the right answer by construction.

A commonly cited figure is **~30% time recovery** for developers using Code Connect (likely originating in Figma's published material; attribute to source rather than asserting in client materials). The directional claim is consistent with practitioner reports; the specific number warrants attribution.

### The practical MCP workflow

The sequence most AI-assisted handoffs in 2026 use:

1. **Selection.** Engineer selects a frame in Figma.
2. **Context pull.** AI agent (via Figma MCP) fetches node variables, layout data, Code Connect links, screenshot.
3. **Validation.** Agent calls a Storybook MCP or DS MCP to find existing components matching selected patterns.
4. **Generation.** Agent generates implementation code, reusing existing components and tokens.
5. **Review.** Engineer reviews the snippet in their IDE and merges.

(See 12-figma-practice on the MCP server architecture and 05-development-support on the AI integration layer.)

### The minimum architecture

The four prerequisites that make context-first generation reliable:

1. **Components-as-data** (or equivalent structured component contract). Without this, AI doesn't know what the component *is* beyond what it can infer from the rendered artifact.
2. **DTCG-compliant tokens with descriptions.** Without this, AI doesn't know what tokens exist or which to apply.
3. **Code Connect or equivalent mapping.** Without this, AI doesn't know what production components exist.
4. **Component metadata** (`.ai.json`, Wolosin schema, or equivalent). Without this, AI doesn't know composition rules, when-to-use boundaries, or accessibility requirements.

A team that ships an MCP integration without these architectural prerequisites has built a fast path to inconsistent code. **A team that ships them in order has built the substrate for AI to do real DS work.**

---

## AI in governance and ongoing maintenance

### Drift detection

Detecting when production code diverges from DS specifications is a real use case where AI is starting to be useful but isn't yet reliably productized. Workflow:

1. AI scans a consuming codebase against the DS component catalogue.
2. Identifies components implemented locally that should be using DS components.
3. Identifies DS components used in non-conforming ways (wrong props, wrong tokens, modified styling).
4. Produces a drift report.

This works in proof-of-concept and is appearing in some commercial tools. Specific tooling sometimes referenced — "Instance Finder" and "Token Master" — should be verified as current named products before recommending; the underlying capability is real and useful regardless of the specific brand name. The accuracy is uneven — false positives common — and the report typically needs human triage before becoming an actionable backlog. **Worth piloting; not yet worth selling as a polished offering.**

### Coverage analysis

A related use case: surveying a product to find UI patterns that aren't yet in the DS but probably should be. AI scans product files, clusters similar patterns, flags candidates for systematization.

This works better than drift detection because the output is *suggestive* (a candidate list) rather than *declarative* (a violation list). Useful as input to quarterly DS planning. Limited by AI's pattern-matching, which clusters by visual similarity and sometimes misses semantic equivalence.

### Changelog and versioning

AI-generated changelogs from git diffs are reliably useful — produces a draft covering the changes, typically requires light editing for tone and to elevate user-facing impact over technical change.

Semver bump suggestions from a diff are also useful as drafts. AI usually identifies breaking changes (renamed props, removed components) but occasionally misses subtler breaks (changed default values, modified ARIA behavior). Human review of the suggestion is short and high-leverage.

### Contribution review

Using AI as a first-pass review on proposed components — checking against accessibility patterns, naming conventions, token compliance, structural standards — is feasible and being adopted by some teams. Shape:

1. Contributor opens PR with a new component.
2. CI runs AI review against documented standards.
3. AI produces a report: passes, warnings, blocking issues.
4. Human reviewer uses the report as input, not as a replacement.

This works when the standards are well-documented (so the AI has criteria to apply) and when the reviewer treats AI output as advisory. **The failure mode is treating AI output as authoritative** — AI hallucinates standards that don't exist and fails to apply standards that do.

The decision: **AI as gate or AI as advisory?** Most mature systems should default to **advisory**. A blocking gate that produces false positives erodes trust; an advisory layer that surfaces candidates for human attention sustains it. As models improve, the balance shifts; today the balance favors advisory. (See 14-accessibility on the same gate-vs-advisory question for a11y review.)

---

## AI-ready DS architecture

### Components-as-data is the prerequisite

**This is the load-bearing claim of the entire file.** AI-in-DS workflows fail or succeed on whether the component is defined as structured data. A structured component data layer makes intent explicit:

- **Anatomy.** Hierarchy of named parts; types (container, slot, text, icon).
- **Props.** Name, type, allowed values, description, default.
- **Variants.** Discrete variant matrices that produce structurally different outputs.
- **Composition rules.** Cannot-contain, common-partners, parent constraints.
- **Usage metadata.** When-to-use, avoid-when, common misuse patterns.
- **Accessibility metadata.** APG pattern reference, required labels, keyboard behavior, ARIA roles set internally.
- **Token references.** Which tokens the component uses at which leaf elements.

This layer is what an AI agent needs to generate reliable code, reliable docs, reliable Figma assets, and reliable governance checks. **It is also what a human contributor needs** to author a new component consistently with the rest of the system. The structured layer serves AI and humans equivalently, which is part of why it works.

Whether the format is YAML, JSON, or custom, what matters is that **the layer exists** and is the source of truth. Figma + code + docs + AI are all *outputs*.

### DTCG tokens as the parseable structure

The token side has stabilized around the **W3C DTCG format** — a JSON schema for tokens that's machine-parseable, type-aware, and supports the full range of token types (color, dimension, duration, shadow, gradient, typography composite, etc.).

DTCG matters for AI because it gives the agent a structured contract for tokens equivalent to what components-as-data gives for components. Generation against DTCG is reliable in the same way generation against components-as-data is reliable. **The two layers compose: structured tokens + structured components = a substrate AI can generate against end-to-end.**

(See 02-design-foundations for the broader token architecture and 12-figma-practice on the Figma-side of DTCG.)

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

This is what "AI-ready DS architecture" looks like in 2026. **Most teams have pieces of it; few have the whole stack.** It's a 2026–2027 investment for shops that want to lead. (See 05-development-support on the broader AI integration layer in our practice POV.)

### Semantic naming as compressed sentence

A reinforcing detail: token names like `surface/action/primary/rest` are AI-readable specifically because they read as compressed sentences. The semantic structure carries intent. **Visual names** (`blue-500`) **strip intent and force AI to extrapolate.** This is the same point made in 02-design-foundations on naming as compressed sentences — restated here because the AI-readability of the system depends on it.

---

## Current limits and honest assessment

### What ships and works today

- **AI as token-taxonomy critic.** Audit existing taxonomies for gaps and inconsistencies. Reliable.
- **AI for documentation drafts.** Component descriptions, prop tables, basic usage. 60–80% of the work; human edit pass required.
- **AI for variant generation from a working base.** Hover/active/disabled states, size variants. Reliable.
- **AI for code review against documented standards.** Token compliance, missing labels, naming consistency. Reliable when standards are explicit.
- **MCP-driven code generation with full DS context.** Production-acceptable for routine components when the DS architecture is in place.
- **AI changelog drafts from git diffs.** Reliable; light human edit required.
- **AI as advisory in PR review.** Useful first-pass; not yet trustworthy as autonomous gate.
- **Brand-book extraction with multimodal AI.** Raw value extraction reliable; semantic mapping requires curation.
- **Layer naming cleanup, visual search for component discovery.** Useful; well-validated.

### What is aspirational

- **End-to-end Figma → production code with no human in the loop.** Demos exist; production reliability does not. Routine components get close; complex components don't.
- **AI authoring components from scratch (no design first).** Plausible-looking but inconsistent components needing significant rework.
- **AI-driven contribution gating.** Workable as advisory; not yet workable as authoritative.
- **AI-driven full-codebase drift detection.** Proof-of-concept maturity; not productized.
- **Cross-platform code generation that's natively idiomatic on each platform.** AI generates web well, native less well, Flutter unevenly.
- **Generative design that understands brand voice.** Structurally correct but characterless output.
- **Full automated migration of legacy systems to new architectures.** *(External names this aspirational; we agree.)*
- **Autonomous decision-making on DS strategy.** Not on the table for the foreseeable future.

### Quality and consistency issues

- **AI slop.** UI that looks correct but is built with poor technical foundations. Without components-as-data, AI hallucinates props or relies on generic patterns that don't match the codebase.
- **Naming drift across multiple AI generations.** Run the same prompt twice, get two different naming conventions. Mitigated by aggressive context (style guide, examples) but never eliminated.
- **Token drift.** AI applies tokens correctly when they're well-named and well-described; defaults to hardcoded values or invented tokens otherwise. **Quality of the token system directly determines quality of AI output.**
- **Hallucinated APG patterns.** AI confidently produces ARIA that's wrong. Always verify against the actual APG.
- **Over-engineering.** AI defaults to expansive prop APIs. Curate aggressively.
- **Composition errors.** AI struggles to keep cross-component consistency in mind across long generation sessions. Periodic review necessary.
- **Token-cost economics.** If an agent is forced to load an entire massive design system into context for every task, costs and latency compound. The MCP-server architecture is partly a response to this — give the agent queryable access rather than dumping everything in context.

### Organizational and governance challenges

- **Review burden.** AI generates faster than humans can carefully review. Trusting too quickly leads to compounding bugs; reviewing every line conservatively erases the speed gain.
- **Attribution.** AI-generated code in OSS-licensed systems raises licensing and attribution questions. Most agencies handle case-by-case; few have policies.
- **Skill atrophy.** Engineers and designers who delegate routine work to AI may not develop the underlying skills. Real concern for junior practitioners; less so for senior ones with the skills already.
- **Vendor lock-in.** Commitments to specific AI tools, MCP servers, or integrations create dependencies that may not age well as tooling churns.
- **Cost.** Frontier AI tools used at scale across a team cost real money. Budgets need to anticipate this.
- **The flood-of-low-quality-contributions risk.** AI-assisted contribution lowers the friction of submitting components, which can flood the system with low-quality or redundant proposals if the gate isn't strong. The role of the human "system architect" — setting standards, reviewing logic, ensuring coherence — becomes more critical, not less.

### What still requires human judgment

- **Brand expression.** What feels right is not what AI produces.
- **Strategic component decisions.** When does this pattern become a component? When does this component become a pattern? When does the system absorb this exception?
- **Governance decisions.** Who can contribute? What's our accessibility floor? When do we deprecate?
- **Stakeholder communication.** Translating system decisions to non-technical clients.
- **Cross-functional negotiation.** Brand vs. accessibility vs. engineering velocity vs. timeline. AI can summarize the trade-offs; the negotiation is human.
- **Quality calibration.** Is this component good enough to ship? AI doesn't have taste; humans do.
- **The senior practitioner's value shift.** From "how to build" to "what to build and why." AI handles increasingly complex technical execution; the system architect sets the spirit and the standards.

---

## Failure modes

- **AI integration shipped without the architectural prerequisites.** Components-as-data missing, or DTCG tokens missing, or Code Connect missing. AI produces "AI slop" and the team blames the AI rather than the missing architecture.
- **Screenshot-first treated as production-ready.** Code generation without DS context becomes the default workflow; consuming products diverge from system standards because the generated code doesn't reference real components.
- **Figma MCP enabled without a structured DS data layer.** AI extracts whatever's in the Figma file; output is "stochastic, incomplete, and imprecise."
- **Specific feature names treated as stable.** Capabilities change names release-to-release; client materials become outdated faster than they can be updated.
- **AI as authoritative gate before models are trustworthy.** False positives erode contributor confidence; the gate becomes a barrier rather than a quality lever.
- **Token system without descriptions.** AI applies tokens by guessing intent; descriptions are the highest-leverage AI investment in the token layer (also valuable for human onboarding).
- **Visual names** (`blue-500`) **persisted into the AI era.** AI extrapolates from a meaningless name; output is plausible but wrong.
- **Hallucinated ARIA shipped without review.** AI confidently emits incorrect ARIA; review didn't catch it; users with assistive tech hit the failure.
- **Over-engineered prop APIs from AI generation.** Components shipped with 15 props that should have been 5 plus composition.
- **No human curation of AI-drafted documentation.** AI hedges land in published docs; reads as defensive and dilutes the practice's voice.
- **Token-cost runaway.** Every task loads the full DS into context; bills balloon; latency degrades; team workarounds with smaller context produce worse output.
- **Junior practitioners delegating without developing skills.** Skill atrophy; the next generation doesn't internalize the architecture and can't extend or debug it.
- **Vendor lock-in via tool-specific MCP integrations.** Custom integrations to a specific AI tool become legacy when the tool churns; portable architecture (DTCG, MCP standard, components-as-data) ages better.
- **Selling AI capabilities ahead of the architecture.** Client expects results AI can't deliver without the architecture they haven't invested in. Trust erodes.
- **AI contributions flooding without strong gates.** Low-quality or redundant components multiply; system coherence degrades; the system architect role becomes firefighting.
- **Native Figma AI features used as the leverage point** rather than the MCP layer. Designers explore on AI; designs don't use the system; rework cost compounds.

---

## Tensions and open questions

1. **The components-as-data adoption curve.** Specs CLI, Wolosin's metadata schema, and our own `.ai.json` all converge on the same architectural prerequisite. The practice should commit to one canonical shape (or named alternatives) for our engagements; we currently don't, and clients receive different recommendations from different leads. Worth productizing.

2. **AI as gate vs. advisory — when does the balance shift?** Today the balance favors advisory. As models improve and DS architecture matures, autonomous gating will become viable for specific check classes (token compliance, naming consistency, basic a11y). The practice needs a tracked POV that updates as the capability changes — not a fixed position locked into 2026.

3. **The minimum DS architecture for AI to be net-positive.** We've named four prerequisites (components-as-data, DTCG, Code Connect, metadata). The honest question is how much of this we ship in a 12–16 week MVP engagement vs. how much we ship across a longer arc. The "AI-ready DS" needs to be a deliverable category in our scoping, not an aspirational add-on.

4. **Specs CLI vs. internal `.ai.json` — when do we use which?** Specs CLI is the public, growing-adoption tool; `.ai.json` is internal POV with documentation and language we control. Both encode the same architectural layer. The practice needs a guideline on when to recommend which.

5. **AI in governance — moving from advisory to autonomous over time.** Drift detection, contribution review, changelog generation are all candidate areas. Each has a different threshold for autonomous use. We should track this per-area rather than a blanket policy.

6. **Vendor lock-in management.** Our practice currently uses Claude Code, which exposes specific MCP capabilities. Cursor users have different defaults. As we standardize internal practice, the question of "which assistant is the practice's default" becomes a real internal-policy question. Worth deciding rather than letting it emerge.

7. **The skill-atrophy risk for junior practitioners.** AI-assisted authoring is faster and lowers the cost of producing components. Juniors who delegate from day one don't develop the architectural intuition. Mitigation: deliberate "learn by hand" tracks for onboarding, AI as an assist after the basics are internalized. Currently not a productized policy.

8. **Token cost as a project line item.** Frontier AI tools used at scale across an engagement team produce real costs. Currently absorbed into agency overhead; should be transparently scoped on engagements with significant AI integration.

9. **The Figma Console MCP write-access governance question.** Allowing AI to write directly to Figma raises the question of who reviews AI-generated changes, whether they go through branches, whether they require human approval. Best practices for write-access governance are not yet established; the practice should pilot and document.

10. **The "MCP-without-DS-data" failure mode as a defensible POV.** Curtis's caveat — "stochastic, incomplete, and imprecise" — applies. Our practice can be the agency that names this clearly in pitches: AI-in-DS without the architecture is theatre. **This is a defensible commercial POV** that differentiates from agencies selling AI features without the substrate.

---

*Provenance: The components-as-data POV is from Nathan Curtis, *Components as Data* (Sep 2025, medium.com/@nathanacurtis/components-as-data-2be178777f21) and Specs CLI (github.com/DirectedEdges/specs); both are central references for this file. The MCP standard is from Anthropic (modelcontextprotocol.io). The Figma Dev Mode MCP server is a Figma product (help.figma.com/hc/en-us/articles/32132100833559); the figma-console MCP (Southleft) is a community implementation extending it with write capabilities. The W3C DTCG token format (design-tokens.github.io/community-group/format/) is the parseable structure underlying machine-readable tokens. Code Connect (figma.com/code-connect-docs/) is the Figma-side mapping between design components and production code components. The "stochastic, incomplete, and imprecise" caveat on Dev Mode MCP without structured component data is Curtis (2024) and is the practical core of the architectural-prerequisite argument. The `.ai.json` schema and four-layer AI stack are internal practice IP from AI-Compatible Design Systems (Feb 2025). Wolosin's 12-field component metadata schema (Indeed, Jun 2025) is a parallel structured-data implementation worth referencing alongside Specs CLI. Specific Figma AI feature claims (First Draft, Visual Search, Smart Page Summaries, Figma Make, Rename with AI), MCP-related capability claims (expression tokens, Smart Variant Adaptation, Instance Finder, Token Master, the Storybook components manifest), and reported figures (30% time recovery from Code Connect, 60–80% documentation-time savings, share of WCAG issues machine-detectable) are dated to 2025–2026 in current research and should be verified or attributed to source before client-facing recommendation. The three-level context-maturity framing (bare Figma MCP / + Code Connect / + custom DS MCP) and the four-prerequisite minimum architecture (components-as-data, DTCG, Code Connect, component metadata) are positions sharpened from internal practice work and are the central architectural recommendations of this file. The "AI as critic, not author" pattern, the screenshot-vs-context-vs-Code-Connect three-paradigm framing, and the gate-vs-advisory framing for AI in contribution review are practice POVs that connect to 14-accessibility on the same gate-vs-advisory question for a11y review. AI coding assistants (Claude Code, Cursor, GitHub Copilot, Windsurf) are dominant tools in 2026 but the vendor landscape rotates fast — bet on the architecture, not the tool. This file was synthesized from a dual-agent research run in May 2026 (see `_research/_archive/2026-05-05-ai-in-ds.md` for the editorial trail).*

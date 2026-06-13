---
type: practice-area
title: Figma Practice
description: Figma at professional depth. Library architecture, component construction, Variables, Dev Mode/Code Connect/MCP, branching, performance, deprecation.
tags: [extension, figma, code-connect, mcp]
timestamp: 2026-05-16
---

# 12 — Figma as the Design Systems Tool

> Figma is the tool we use on nearly every design systems engagement, which makes our fluency with it a competitive surface, not a checkbox. This file is what professional Figma practice looks like in 2026 — how we architect libraries, build components, manage tokens, hand off to engineering, and govern the system over time. It is not Figma 101. It assumes the reader knows the tool and skips to the trade-offs, the gaps, and the conventions that have stabilized into de facto standards.

---

## Why this is its own file

The rest of this vault is tool-agnostic by design. Components, tokens, governance, and adoption are concepts that translate across Sketch, Figma, Penpot, or whatever comes next. But Figma is the practical substrate for almost everything we ship in 2026, and the way we use it carries enough opinionated craft to warrant its own document. **The risk of leaving Figma practice implicit is that it gets re-derived per engagement.** Junior practitioners reinvent naming conventions; senior ones don't write down what they've internalized; clients absorb whatever the lead designer happens to do that month. This file is the corrective.

A note on currency: Figma ships changes constantly. Every specific limit (modes per collection, file size ceiling, plan-tier features) and every specific feature name in this document reflects platform state as of early 2026 and may have evolved. For client-facing recommendations, verify against the current Figma docs before locking in. The principles age more slowly than the specifics.

---

## Library architecture and organization

### Single library vs. multi-library

The split is not a matter of preference; it is a function of three forces — file weight, governance surface, and team topology — and the decision should be re-evaluated as those change.

**Consolidation works at smaller scale.** A single library makes sense when the system is under roughly 200 components, the maintainer team is one to three people with publish rights, and the consuming surface is one or two product lines. Consolidation eliminates the publish cascade — when a foundation token changes, every consuming file picks it up on a single library update, not a chain of three. The cost is governance flatness: anyone with edit rights can touch foundation tokens and component layouts in the same session, and there is no separation between people who should be working on raw values and people who should be working on component composition.

**Above that scale, the question is how to split, not whether.** The convention that has stabilized is a tiered decomposition:

1. **Foundations** — variables, type styles, effects. The slowest-moving, most consequential layer.
2. **Iconography and assets** — SVG library, illustrations, brand marks. Often updated independently of the component cadence.
3. **Core components** — buttons, inputs, cards, navigation primitives. Consumes foundations and assets.
4. **Patterns** — multi-component recipes (page headers, data tables, checkout flows). Consumes core components.
5. **Brand-specific overlays** (multi-brand portfolios only) — variable mode extensions or component variants that ride on the core.

Each tier publishes to the next. A token change in Foundations requires four sequential publishes before a product file sees it. We plan publish cadence around this — some clients absorb foundation publishes daily and stage downstream cascades to a sprint boundary; others batch the whole chain weekly. The right cadence is whatever consuming product teams can absorb without thrash.

| | Single library | Multi-library |
|---|---|---|
| Update propagation | Immediate | Cascading (multiple publishes) |
| File performance at scale | Degrades | Each file stays leaner |
| Permission scoping | Flat — all editors equal | Per-tier role separation possible |
| Onboarding friction | Lower | Higher (consumers enable multiple libraries) |
| Cross-file alias risk | None | Real — biggest stability risk |

**The cross-file alias risk is the single most under-discussed cost of going multi-library.** When a Component library aliases a Foundations variable, that alias survives only as long as the publishing chain stays intact. Renaming a foundation variable, deleting a collection, or moving variables between collections can break aliases across consumer files in ways that surface days later. Once a team has lived through this, they treat foundation variable names as a stable contract — additions are free; renames and deletions go through the deprecation cycle described later in this file. (See also 02-design-foundations on the broader token architecture.)

### Page structure inside a library

Within a library, page order communicates intent. A reader should be able to read pages top-to-bottom and understand the file's narrative without opening anything.

The convention that has stabilized:

1. **Cover** — file thumbnail, version, owner, status badge, links to external docs.
2. **Changelog** — recent changes, deprecations, link to release notes.
3. **--- Foundations ---** (separator) — colors, typography, spacing, motion.
4. **--- Components ---** (separator) — grouped by category (Inputs, Surfaces, Navigation, Feedback, Data Display).
5. **--- Internal ---** (separator) — `_`-prefixed pages: scratch, exploration, deprecated archive.

Separator pages (a page named `---` with empty canvas) are a hack but a useful one — they create a visual gap in Figma's page rail. Alternatives like emoji-prefixed page names work too but degrade in screenshots and search.

**The rule that gets forgotten:** internal pages must be excluded from publishing. Figma indexes everything on a published page into the consumer's asset panel unless the page is explicitly hidden. A scratch page accidentally published is the most common path to weird Frankenstein components surfacing in consumer libraries.

### Naming

Figma names appear in three places — the canvas, the consumer's asset panel, and (via Code Connect or DTCG export) the production codebase. A naming convention has to serve all three.

**Components.** Plain PascalCase for top-level components — `Button`, `InputField`, `NavigationBar`. **No namespace prefixes** (`DS/Button`) on top-level components — Figma doesn't need them, and they pollute Code Connect outputs. This has stabilized as de facto standard. Slashes in component names are reserved for sub-components.

**Internal sub-components.** Underscore-prefixed: `_Button/Icon`, `_Card/Header`. The underscore hides them from the consumer asset panel — they remain instantiable from within the parent component but consumers can't drag them out and detach them. **This is the single most important hygiene rule for a public component library:** anything that's a structural building block, not a publishable unit, gets `_`.

**Documentation/example components.** Period-prefixed: `.ButtonExample`, `.GuidelineHeader`. The period prefix hides from the asset panel *and* excludes from publishing — useful for in-file examples consumers shouldn't be able to drag out at all.

**Variants.** `Property=Value` syntax, with Title Case values for human readability: `Size=Small`, `Variant=Primary`. Code Connect and DTCG handle case translation downstream — keep Figma readable.

**Variables.** Slash-separated paths, lowercase, no spaces: `color/bg/primary`, `spacing/inline/md`. The slash creates Figma's folder grouping in the variable picker. **CamelCase belongs in code output, not in the Figma name itself** — that's what Code Syntax (covered in §Multi-platform below) is for. Mixing casings within variable names makes find-and-replace operations unsafe.

**Layers.** Inside a component, layer names matter because they survive across variants. Text layers especially must have **identical names across every variant** — if `Default` has a layer called `Label` and `Hover` has a layer called `Text`, consumer overrides reset when the variant flips. This is one of the most-encountered bugs in mid-maturity libraries and is the single most worth-stating convention when training a new contributor.

### Published vs. unpublished

Three categories belong in the file but not in the published payload:

- **Primitive variables.** Publish only the semantic layer. Forcing consumers through `color/bg/primary` rather than `blue/500` is the entire point of a semantic token system; exposing primitives invites deviations from the semantic logic.
- **Internal sub-components** (`_`-prefixed).
- **Scratch and archive pages.**

Figma's publishing modal lists every change on every publish. Maintainers should review this list every time. Unintended additions — a stale exploration component that got accidentally promoted — leak into consumer asset panels and are hard to retract once consumers have instances of them.

**Variable scoping is a separate lever from publishing.** Scoping restricts *where* in the UI a variable can be applied (a `border/radius/sm` variable scoped to "Corner radius" only won't show up in the typography size picker). Use scoping to prevent misapplication; use unpublishing to control discoverability. They're complementary, not redundant.

---

## Component architecture

### Variants vs. component properties

The decision rule, applied ruthlessly:

- **Use a variant** when the change is structural or visual in a way an engineer would write differently in code (a CSS class change, a different element type, a different layout). Size, density, primary/secondary, hover/pressed/disabled.
- **Use a component property** when the change is content (text, an icon, a slot) or a boolean toggle of an existing element (show icon, show secondary action).
- **Use an instance swap** when the change is one of a known set of nested components (which icon, which avatar size).

A button with 3 sizes × 4 styles × 4 states = 48 variants is correct. A button with 3 × 4 × 4 × 2 (icon-or-not) × 2 (trailing-icon-or-not) = 192 variants is malpractice. The last two dimensions are properties, not variants.

**The performance cost of variant matrices is real but is not the primary reason to avoid them.** The primary reason is editability: every cell of the matrix is its own canvas. A change to icon spacing requires touching 192 cells. Even with components-of-components, the matrix becomes its own maintenance burden that scales worse than the rest of the system.

**Misuse patterns we routinely encounter:**

- **A boolean property faked as a variant** (`HasIcon=True/False`) — doubles the matrix for nothing.
- **Variant values that should be a single property** — `Variant=PrimaryWithIcon`, `Variant=PrimaryNoIcon` collapses to `Variant=Primary` plus a boolean.
- **Property names that don't match code prop names** — slows handoff and breaks Code Connect's value mapping.
- **Layer name drift across variants** — text overrides reset on variant switch when layer names differ. This is the bug, every time.

### Nesting

Auto Layout nesting is the cheapest way to build flexible components and the most expensive way to build slow ones. Each nested Auto Layout frame is a node Figma's layout engine resolves on every render and on every property change.

**The empirical threshold practitioners cite is 4–5 levels of nesting.** Below that, fine. Above that, performance degrades visibly — properties panel lag, slow drag-resize, slow variant switches. The right response when a component requires deeper nesting is almost always to flatten using variable-driven padding and gap rather than wrapper frames. A frame with `padding-x = spacing/inline/md` and `gap = spacing/stack/sm` does work that previously required two wrapper frames.

A useful audit heuristic: open a component in the layers panel, expand all, count depth. If it exceeds 5, look for wrappers that exist solely to hold one child or apply a single property — those are the candidates to flatten.

### Base components and slots

The "base component" pattern — building a generic wrapper that specialized components instance-swap into — was the dominant flexibility pattern from roughly 2022 to 2024. It works but has a known tax: consumers can only swap one instance for another known instance, and adding multiple unpredictable items requires nesting more base components, which reintroduces the depth problem.

Figma's slot capability — matured through 2024–2025 — replaces most base-component patterns. We have not independently verified specific feature-launch dates or keyboard shortcuts cited in some sources; confirm against current Figma docs before training a team on a specific gesture. A slot is a designated drop zone inside a component where consumers can place arbitrary content (a button, an icon, raw text, multiple stacked elements) without detaching the parent. The parent still receives upstream updates; the slot content is per-instance.

**The architectural impact:** components that previously needed dozens of variants to cover content permutations (modals, dialogs, page headers, data table cells) collapse to a single component with one or two slots. The Modal stops needing 20 variants and becomes a frame with `header`, `body`, and `footer` slots.

**Where slots are weaker than the codebase analogy suggests:** Figma slots don't have the equivalent of named React children with type constraints. "Preferred Instances" — the maintainer-curated list of components Figma suggests when a consumer adds to a slot — is the closest mechanism, but it's a soft suggestion, not a constraint. Consumers can put anything in a slot. Documentation and review remain the primary governance lever.

(See 03-component-library for the broader composition vocabulary — block / area / slot / substitution — that this Figma capability operationalizes.)

### Detaching

Detachment rates are a diagnostic, not a target. Figma's library analytics surface detachment per component; a consistently high rate (we use >10% of instances as the rule of thumb) is a signal that the component doesn't fit how consumers need to use it. **The right response is almost never "tell consumers to stop detaching" — it's "fix the component."**

Common reasons consumers detach:

- A required content configuration the component doesn't support → add a slot or property.
- A one-off layout deviation for a specific screen → may be legitimately appropriate; not every screen should be systematized.
- The consumer wants to override styles (color, padding) the component doesn't expose → consider exposing them as variables, or accept the detachment if the override is genuinely one-off.

**A design principle worth holding:** even when the macro structure must be detached, foundation tokens should be applied at the atomic layer. Every fill references a color variable; every spacing value references a spacing variable. A detached button still inherits brand color updates because its fill points at `color/bg/primary`, not `#0066CC`. Detachment becomes much less destructive when variable bindings survive.

---

## Variables and token architecture

### Collection structure

The mature pattern is two or three tiers, kept in separate collections:

1. **Primitives** — raw values. `blue/500 = #0066CC`. One collection per resource type, or all primitives in a single `_primitives` collection.
2. **Semantics** — aliases that point at primitives. `color/bg/primary → blue/500`. This is the layer consumers and components reference.
3. **Component-specific** (optional, often skipped) — aliases at the component level. `button/bg/hover → color/bg/primary/hover`. Adds resolution power; adds variable count and Figma client memory pressure.

**Most teams do not need the component-specific tier.** The argument for it is "we want to retheme buttons without touching everything else"; in practice that requirement is rare enough that the overhead isn't worth it for systems under ~50 components. Larger systems with strong component ownership get more from it.

**Type discipline matters more than people realize.** Variables are typed as Color, Number, String, or Boolean. Number variables hold dimensionless values — `4` for `spacing/sm`, not `"4px"`. **Units belong in the variable name** (`duration-250ms`) **or in the consuming context, never in the value.** Percentages stored as decimals (`0.5` for 50%) compose with math; percentages stored as strings don't. Wrong types upstream are fixable but tedious — get them right at creation.

### Modes

Modes let a single semantic variable resolve differently based on context. Canonical use cases: theme (Light/Dark), brand (Brand A / Brand B), density (Compact/Comfortable). Less canonical but increasingly common: locale, contrast (WCAG AAA mode), motion (reduced).

**Plan tier limits matter.** Free and Professional plans have a hard cap on modes per collection (smaller); Organization and Enterprise plans raise it. Specific cap numbers we've seen cited (e.g., 10 on Professional, 20 on Organization/Enterprise) should be treated as plan- and date-dependent and confirmed against current Figma docs before designing around a number. Figma has revised these caps multiple times since Variables launched in mid-2023.

**Mode multiplication is a real cost.** A collection with `theme × brand × density = 2 × 3 × 2 = 12 modes` is unusable in practice — switching requires picking from a 12-item dropdown and the matrix becomes hard to validate. The right decomposition is usually **one mode dimension per collection** (one collection for theme, one for brand, one for density), letting frames inherit each. This is an underused pattern.

**Limits practitioners hit:**

- No conditional logic inside a variable definition (the "if dark then X else Y" pattern requires modes; you can't compute it in a single variable).
- Limited string concatenation, math expressions, and composite types in stable Figma. Teams who need these reach for Tokens Studio.
- Mode switches don't traverse instance boundaries cleanly in all edge cases — nested instances sometimes resolve to the wrong mode, particularly when an instance is placed in a frame whose mode doesn't match the source library's default.

### Composite types and expression tokens

Two newer capabilities sit at different stages of maturity: **composite/array types** (grouping shadow x/y/blur/spread/color into a single variable rather than five separate ones) and **expression tokens / math** (programmable conditional logic inside a variable, e.g. `if(is-dark, #FFF, #111)` or `{spacing-base} * 1.5`).

**Composite types are stable in DTCG 2025.10** (the W3C Design Tokens Format Module's first stable release, 28 October 2025, verified via `designtokens.org/tr/2025.10/format/`). They are implemented by Figma, Tokens Studio, Style Dictionary v4, Penpot, Sketch, Framer, and Terrazzo. The practitioner caveat is the property-level-aliasing fidelity gap: composite sub-properties that should be aliases to other tokens often round-trip as literal values across tools, breaking the alias relationship. The convergent discipline is to author composites as the source-of-truth representation and **flatten them at the build pipeline into per-platform atomic outputs.** Composites are fine to recommend; flatten at build, not at runtime. (See 22-token-architecture-extensions for the spec depth, 23-typography-tokenisation for typography composites specifically.)

**Expression tokens / math are not part of the DTCG stable spec.** Tokens Studio's math syntax is the most-adopted implementation; Style Dictionary v4 preprocessors handle the same job at build time. The compute-at-authoring-ship-literals discipline applies: math runs at authoring time, resolved literals ship to runtime. Watch the DTCG community group's Resolver Module for eventual standardisation. (See 22.)

### Multi-brand collection architecture

12-practice's one-mode-dimension-per-collection pattern extends into the multi-brand portfolio scale (5–20+ brands sharing a foundation) as a multi-collection architecture: a Global Foundations collection (primitives, read-only for brand teams), one Brand Semantic collection per brand (aliases to the global primitives, with the brand's themes as modes inside the collection), and a Components layer that consumes brand semantics through library swap. **Brand is a collection axis, not a mode axis** — modes work for theme and density, fail for brand because brand axes multiply rather than compose. See 24-tokens-at-scale.

A related capability sometimes referenced is **Extended Collections** — an Enterprise-exclusive feature for multi-brand portfolios that lets a base variable collection be extended with brand-specific overrides while inheriting structure and modes from the parent. We have not independently verified this either. If real, it materially changes the multi-brand token architecture pattern; if not yet stable, the parallel-collection pattern remains the right approach.

### Variable scoping

Scoping restricts where a variable surfaces in the UI. A spacing variable scoped to "Gap, Padding" won't appear in the corner radius picker. This is the lightest-weight governance lever Figma offers — set it at the variable level, applies everywhere.

**The under-used scoping is per-property:** scoping a color variable to "Frame fill" only, so it can't be applied as a stroke. For semantic colors with strong fill-vs-stroke conventions, this prevents drift. The ergonomic cost is that the scoping UI is buried and bulk-editing it is slow — a real gap in Figma's native tooling that Tokens Studio partially fills.

### Figma Variables vs. Tokens Studio

Current state of the trade-off:

| | Native Variables | Tokens Studio |
|---|---|---|
| Token types | Color, number, string, boolean (composites limited or emerging) | 20+ types covering full CSS surface area |
| Math, references, composition | Limited | Full expression engine |
| DTCG import/export | Native (improved through 2024–2025) | Established, well-tested |
| Style Dictionary integration | Via DTCG export | Direct, mature |
| Multi-brand, multi-mode | Native (within plan limits) | Possible, more complex setup |
| Plugin overhead | None | Real — slow load on large files |
| API for automation | Variables REST API | Plugin API only |

**The migration trend is real but partial.** Teams are moving from Tokens Studio to native Variables for the core color/spacing/typography work, where native is now sufficient. Tokens Studio remains the right tool for teams that need:

- Composite tokens (shadows, borders as single units), if Figma's native composite support isn't yet stable for the team's needs
- Math expressions (`{spacing.base} * 2`)
- Token types beyond what Variables natively support
- A more programmatic management surface for hundreds of tokens

A common hybrid: **native Variables for what designers interact with daily** (colors, spacing, type), **Tokens Studio for the engineering-side transformation pipeline** (composite shadows, motion, complex aliasing). Both can coexist if the source of truth is clearly designated; both as sources of truth simultaneously is chaos.

### Connecting to a code pipeline

The stabilized pipeline (See 02-design-foundations and 05-development-support for the broader pipeline architecture):

```
Figma Variables
  ↓ DTCG JSON export (native, or via Tokens Studio)
Tokens repository (W3C DTCG format)
  ↓ Style Dictionary
Platform outputs (CSS custom properties, SCSS, JS modules,
                  iOS Swift, Android XML/Kotlin, Dart for Flutter)
  ↓ CI/CD distribution (npm, GitHub Actions, API endpoint)
Consumer applications
```

**The DTCG format is now stable enough to commit to.** The W3C Design Tokens Community Group spec moved from long draft toward stable through 2024–2025; Figma's native export aligns to it. We still write custom Style Dictionary transforms for platform-specific needs (iOS color asset catalogs, Tailwind config), but the JSON intermediate is portable.

**Known gaps in the Variables-to-code pipeline:**

- Variable descriptions don't always survive the DTCG round-trip cleanly — descriptions are first-class in DTCG but Figma's export is not always lossless.
- Variable scoping doesn't translate to DTCG (it's a Figma-UI concern, no equivalent in tokens-as-data).
- Mode collections export as separate token sets; the consumer pipeline must decide how to reconcile them (one CSS file per theme, runtime switching via attribute selectors, etc.). Figma can't make this decision for you.
- **Bidirectional sync (code-to-Figma) remains weaker than Figma-to-code.** Most pipelines are one-way: Figma is the source of truth, code consumes.

---

## Design-to-development handoff

### Dev Mode

Dev Mode is a separate UI surface, not just a permission level. It surfaces variable references rather than computed values, exposes spacing measurements directly, and provides asset export controls. Engineers without edit access can work in Dev Mode without risk to the source.

**Where Dev Mode is strongest:** showing the variable behind a value (`color/bg/primary` rather than `#0066CC`), measuring spacing between elements without selecting both, and inspecting Auto Layout settings.

**Where it's structurally limited:** Dev Mode reads pixels, not intent. It can show that a frame is 240px wide; it cannot tell the engineer whether that width is fixed, derived from content, or a breakpoint constraint, unless the design uses Min/Max Width variables. It can show an Auto Layout configuration; it can't tell the engineer whether that configuration matches the production component's prop API. **These gaps are bridged by Code Connect, not by Dev Mode alone.**

**The structural advice for component authors:**

- Name component properties identically to code props (`size`, `variant`, `disabled`).
- Use values that match code values (lowercase strings, exact spelling).
- Apply variables at every leaf — no raw hex inside components.

An engineer reading Dev Mode against a well-built component should translate the property panel into JSX in one read.

### Code Connect

Code Connect links a Figma component to its production code counterpart. The maintainer writes a small mapping file (a `*.figma.tsx` or equivalent) declaring "this Figma component is this code component" plus a per-property mapping. When an engineer inspects the Figma component in Dev Mode, Code Connect surfaces the actual code snippet from the production repo — `<Button variant="primary" size="md">Save</Button>` — instead of a generic CSS dump. (See 05-development-support for the broader Code Connect role in our dev-pipeline POV.)

**Maturity, as of early 2026:** React, Vue, SwiftUI, Jetpack Compose, and HTML are first-class. Other frameworks are workable via the generic adapter or community implementations. Code Connect runs as a CLI in the engineering repo; a CI step keeps mappings in sync as code changes.

**Limitations practitioners hit:**

- **Per-property mapping is per-component manual work.** A 200-component library is several engineer-days of mapping. Scope this explicitly.
- **Slot mappings are supported but the syntax is more complex than simple props.**
- **The mapping file lives in the engineering repo,** which means the Figma library and the engineering repo must be coordinated — a Figma rename without a code mapping update breaks the link silently.
- **Code Connect only works for components that exist in production code.** Aspirational components in Figma that haven't been built yet have no link.

### The MCP server and agentic workflows

Figma's Model Context Protocol server (Dev Mode MCP) — public preview late 2024, GA through 2025 — exposes the structure of a Figma file to AI coding tools (Cursor, Claude Code, Windsurf). An AI agent given an MCP connection can pull variable definitions, the component structure, the Code Connect mappings, and a screenshot of a selected node, then produce code that references the right variables and the right code components.

The current sequence most agentic workflows use:

1. `get_variable_defs` — pull the token catalog
2. `get_code_connect_map` — find the component-to-code links
3. `get_code` — generate a code translation of the selected node, using the prior context
4. `get_screenshot` — visual reference for the agent to validate against

**Where this is strong:** for component implementation against a well-built library, the agent can produce correct code in one pass. **For component composition** (assembling existing components into a new screen), it's good but error-prone — the agent can confidently produce structurally-wrong code that compiles.

**Curtis's caution applies and we share it:** Figma MCP without a structured component data layer is "stochastic, incomplete, and imprecise" — the MCP exposes whatever's in the Figma file, and a Figma file optimized for designers is not the same as a structured component contract. Teams getting the most from MCP pair it with a `.ai.json` or component-registry layer that gives the agent explicit metadata about composition rules, props, and constraints. This is a defensible POV for our practice and is named in our AI-Compatible Design Systems materials. (See 03-component-library on `.ai.json` and 05-development-support on the AI integration layer.)

### Annotations

Figma's native annotation capability lets designers attach annotations to specific layers — focus order, ARIA roles, behavior notes — that Dev Mode surfaces in a separate panel. These have largely displaced the redline-plugin patterns that dominated prior workflow.

**Where native annotations work:** accessibility notes, behavior on interaction, links to external specs. They live in the file, survive copy-paste, and Dev Mode renders them cleanly.

**Where teams still reach for plugins:** generated specs for engineers who don't open Figma (deprecated in healthy workflows), redlining for PDF deliverables (rare in modern engagements), and stakeholder review processes that need export formats Figma doesn't natively produce. EightShapes Specs and similar tools survive in these residual cases.

For complex interaction states, some teams use **native Figma components styled as overlay markers** (absolute-positioned annotations that don't disrupt the auto-layout structure) to call out focus orders, ARIA roles, and accessibility notes directly on the canvas. This is a sensible workaround where native annotation density isn't sufficient.

### Living documentation

Documentation in two places:

- **Inside Figma:** every variable and component should have a description. Variable descriptions surface as tooltips in the picker; component descriptions surface in the asset panel. **This is the highest-ROI documentation a maintainer writes** — adjacent to the moment of decision. This aligns with our internal POV that every token carries a `$description` (see 02-design-foundations).
- **Outside Figma:** Storybook for engineers, Zeroheight or a custom site for designers, ADRs in the repo for decisions. The split is "what helps in the moment of use" (Figma descriptions) vs. "what helps in the moment of decision" (external docs).

Bidirectional sync between Figma and Zeroheight is now standard via API; Storybook integration via Code Connect closes the engineering-side loop. The remaining gap is decision documentation — why a component looks the way it does, what alternatives were considered. This consistently lives outside both surfaces, in ADR-style markdown in the engineering repo or a wiki, because neither Figma nor Storybook are good homes for prose. (See 04-documentation for our broader docs strategy and 07-governance-and-adoption on decision logs.)

---

## Multi-platform design

(See 11-mobile-and-cross-platform for the broader strategic context on iOS / Android / Flutter trade-offs; this section covers the Figma-side mechanics specifically.)

### Single workspace, multiple targets

The architectural decision is whether platforms share components or share only foundations. Three patterns, in order of common adoption:

1. **Shared foundations, platform-specific components.** A single Foundations library publishes to Web, iOS, and Android component libraries, each maintained independently. The dominant pattern for native-mobile shops where iOS and Android components must adhere to platform conventions.
2. **Shared foundations, shared core components, platform-specific patterns.** Common for Flutter or React Native shops where the rendering layer is unified and components like buttons can be one-source. Patterns (navigation, forms) still diverge per platform because interaction conventions diverge.
3. **Fully shared, platform-themed.** Rare. Works only when the brand prioritizes cross-platform visual identity over platform conventions and the consuming team accepts the friction with platform users.

**The decision should be explicit in Discovery, not emergent.** Letting it emerge produces hybrid systems where iOS feels like Android with rounded corners (or vice versa), and platform users notice. (See 11-mobile-and-cross-platform on the strategic native-vs-custom decision this connects to.)

### Platform-specific code syntax

Variables in Figma have a per-platform Code Syntax field (Web/iOS/Android). A single variable named `color/bg/primary` in Figma can render as `var(--color-bg-primary)` for Web, `Color.bgPrimary` for iOS Swift, and `R.color.bg_primary` for Android XML, all surfacing in Dev Mode based on the engineer's platform context.

**This is the right surface for platform translation.** The Figma name stays human-readable; platform-specific transformation lives in the syntax field; Dev Mode shows engineers what they need without forcing the maintainer to encode platform syntax in the variable name itself.

### Responsive vs. native scaling

Web responsive design in Figma uses Auto Layout's hug/fill behavior, Min/Max Width constraints, and breakpoint-mode variables. A component bound to `spacing/inline/md` whose value changes with mode (`md = 16` on Desktop, `md = 12` on Mobile) scales without redraw. With Min/Max Width set to breakpoint variables, components fluidly adapt within strict, system-defined boundaries — the design-tool analogue of CSS `clamp()` and min/max-width logic.

Native mobile scaling is a different model. iOS Dynamic Type and Android's text scaling don't map cleanly onto Figma's mode system — the user's runtime preference can't be predicted in design. **The convention is to design at the platform's default scale and document the semantic type role** (`title3`, `body`, `caption`) **so engineers map to the right platform type style.** Don't try to model every Dynamic Type setting in Figma; you'll spend time and miss what users actually do. (See 11-mobile-and-cross-platform on Dynamic Type and TextTheme.)

---

## Governance

### Branching

Figma's branching mirrors Git's mental model: a contributor creates a branch from main, makes changes in isolation, and proposes a merge that maintainers review with a visual diff. Available on Organization and Enterprise plans.

**What branching is good for:** isolated structural changes (refactoring a component, adding a new variant set, rebuilding a token collection) that would risk breakage if done on main.

**Limits practitioners hit:**

- **Concurrent branches that touch the same component or variable collection produce merge conflicts** the diff tool doesn't always resolve cleanly. Coordination by humans remains necessary.
- **Long-lived branches drift from main and become hard to merge.** Discipline is the same as Git: short-lived branches, frequent merges.
- **Variable changes are particularly conflict-prone** — two branches both adding to the same collection often need manual reconciliation.

### Library updates

Library publishing is the moment changes propagate from a maintainer to consumers. Figma surfaces an "update available" prompt in consuming files; consumers choose when to accept.

**The communication layer Figma doesn't provide is what changed, why, and what consumers need to do.** Figma's update modal lists components affected but doesn't surface migration guidance. We supplement with:

- Release notes (Notion, Slack, or a Markdown changelog file in the design repo)
- A `Changelog` page in the library file itself, updated each publish
- Automated Slack notifications via Figma's webhooks for major versions

(See 07-governance-and-adoption on our broader release-communications POV.)

### Contribution workflows

The conventional pattern in mature systems:

1. **Proposal.** A product designer identifies a recurring pattern not in the system. Submits via intake (Jira, Linear, Slack form) with screenshots and rationale.
2. **Triage.** Core team evaluates against criteria — frequency of use, generalizability, accessibility, brand alignment.
3. **Build, in branch.** If accepted, the proposer (or core team, depending on capacity) builds the component in a Figma branch using existing tokens.
4. **Review.** Core team reviews structure, naming, slots, accessibility, Code Connect readiness.
5. **Merge and publish.**
6. **Engineering implementation.** Component built in code, Code Connect mapped, shipped.

**The bottleneck is almost always step 4.** Mature systems publish their review criteria explicitly so contributors can self-check before submitting.

A useful overlay is a **RACI matrix** (Responsible / Accountable / Consulted / Informed) — proposer is Responsible, core team is Accountable, accessibility/brand reviewers are Consulted, consumers are Informed. RACI is the right way to talk to clients about the workflow when their organization already operates in those terms; the workflow steps above are the operational view.

### Audit and coverage

The questions a system needs to answer continuously:

- **What's in the library?** Component count, token count, variant counts. Figma's library analytics surface this.
- **What's used?** Insertion counts, instance counts per component. Surfaces in analytics.
- **What's detached?** Detachment rate per component. Diagnostic for component fit.
- **What's missing?** Hardest to answer in Figma. Requires looking at consumer files for repeated patterns the library doesn't cover. Some teams run quarterly audits; some use plugins (Design Lint, Clean Document) to scan files for non-token color usage as a proxy.

**Figma's native linting** — surfacing hardcoded values in real time during design and suggesting the correct semantic variable — is the highest-leverage audit lever. Teams that turn it on by default catch drift before it ships. The feature is sometimes named "Check Designs"; verify the specific feature name and capability set against current Figma docs, but the general capability is real and worth committing to.

A related capability sometimes referenced is **AI-driven visual search** for finding pre-existing components similar to a proposed new one, intended to reduce duplication. We have not independently verified this as a current named feature; the underlying capability is plausible and useful if available.

---

## Performance and maintenance

### When libraries become unwieldy

Thresholds where Figma performance degrades visibly:

- **~500–1000 components in a single library.** Asset panel slows; search becomes important.
- **~2000 variables in a single collection.** Variable picker noticeably lags.
- **File memory above ~1.5 GB.** Slow open, occasional save failures, unreliable plugins. **A ~2 GB hard ceiling is commonly cited but is plan- and feature-dependent and has changed over time** — treat it as a folkloric threshold rather than a precise spec.
- **More than ~10–15 published libraries enabled in a single consumer file.** Asset panel becomes hard to navigate; library switching slows.

These are not hard limits; they're points where teams typically begin to feel the pressure and start splitting.

### Keeping libraries performant

Interventions, in order of impact:

1. **Eliminate variant explosion.** Convert content-permutation variants to properties. Single highest-impact lever.
2. **Hide internal sub-components.** `_` prefix removes them from the published index; faster to publish, faster to load for consumers.
3. **Quarantine heavy assets.** Large SVG icon sets and complex illustrations belong in their own library. A file with 800 inline SVGs is slow regardless of how well-structured the rest is.
4. **Flatten Auto Layout depth.** Wrapper frames that exist to apply a single property are usually replaceable with a variable.
5. **Split when the above is done and pressure persists.** Don't split prematurely — multi-library tax (cascade publishing, alias risk) is real.

### Deprecation

Deleting a component breaks every instance in every consumer file that references it. The deprecation lifecycle that avoids this:

1. **Mark.** Rename with a deprecation prefix (`[Deprecated] Button-Old` or a more visible marker). Update the description. Existing instances continue to work; the visual marker tells anyone who lands on it that it's going away.
2. **Hide from publishing.** Move to an unpublished page or rename with `_` prefix. New instances can no longer be created from the asset panel; existing instances persist.
3. **Migration period.** Document the replacement, send release notes, give consumers a window (typically a sprint or two) to migrate.
4. **Sweep upstream remnants.** After the migration window, scan consumer files for remaining instances. Either migrate them in branch or detach (preserves the visual but breaks the link).
5. **Delete.** Only after step 4 confirms no live instances remain.

**The communication cost is the dominant cost.** A deprecation done in three weeks with explicit communication is fine; a deprecation done silently in a month produces bug reports for the next year.

### Migration to slot-based architecture

A specific case worth flagging: moving legacy base-component patterns to slot-based architecture is a major maintenance effort for systems with several years of history. Shape of this migration:

- **Build the slot-based replacement alongside the legacy component.** Don't try to convert in place — converting a frame to a slot fundamentally alters its property bindings and risks breaking consumer files.
- **Mark the legacy component deprecated, link to the replacement in the description.**
- **Provide a migration guide showing before/after for the most common usages.**
- **Accept that fully retiring the legacy will take longer than feels reasonable.** The real failure mode is forcing migration on a tight deadline and breaking consumers' work.

The parallel-then-deprecate pattern is the consensus. Conversion-mechanic specifics (e.g., the gesture to convert a frame to a slot) should be confirmed against current Figma docs before execution.

---

## Failure modes

- **The single-library file that should have been split.** Performance degrades; maintainers lose the ability to govern foundation tokens separately from component composition. Symptoms: properties panel lag, slow opens, conflict-prone branching.
- **Multi-library architecture without a publish discipline.** Consumers see "5 updates available" weekly and stop accepting them. The cascade is real, the communication is missing, adoption stalls.
- **Variant matrices used for content permutations.** 192-cell button matrices that should have been 48 cells with three properties. Editability collapses; performance suffers.
- **Layer name drift across variants.** Text overrides reset on variant switch. The bug, every time.
- **Primitives published to consumers.** Designers reach for `blue/500` instead of `color/bg/primary`. The semantic system erodes from below.
- **Variables typed as strings when they should be numbers.** Math doesn't compose; downstream pipelines need bespoke handling.
- **Slot replacements built but legacy not deprecated.** Both versions of a component live in the library; consumers pick at random; the system carries two answers to the same question.
- **Code Connect set up but mappings not maintained.** Engineering refactors the codebase; Figma renames a property; the link breaks silently. Engineers stop trusting the code snippet output.
- **MCP enabled without a structured component data layer.** AI agents produce confident, structurally-wrong code. Trust in the agent erodes; the team falls back to copy-paste.
- **Branching used as the only review gate, with no explicit criteria.** Reviews become subjective; merge times balloon; contributors stop submitting.
- **Detachment rates rising and ignored.** A component is broken-by-design and consumers route around it; the analytics surface this and no one looks.
- **Deprecation by deletion.** A component is removed and dozens of consumer files break overnight. Trust in the system collapses for a quarter.
- **Modes multiplied past usefulness.** A 12-mode collection no one understands; mode switching produces unpredictable results because cognitive load exceeds the team's capacity to validate.
- **Page hygiene neglected; scratch pages published.** Frankenstein components leak into consumer libraries; retraction is hard once instances exist.

---

## Tensions and open questions

1. **How aggressive should we be in moving clients off Tokens Studio?** Native Variables now cover the majority of designer-facing token needs, but Tokens Studio still wins for engineering-side transformation pipelines. The hybrid setup is operationally sound but introduces a "where is the source of truth?" question that mature clients can resolve and immature ones cannot. Worth a Discovery question.

2. **Native composite types and expression tokens — when do they land for our practice?** If Figma's emerging composite/array types and expression tokens (variously dated to 2025–2026) prove stable, they significantly reduce the gap to Tokens Studio and change our recommendation. Until we've validated through a pilot, we should hedge in client conversations. A practice-internal evaluation would be high-value.

3. **Code Connect adoption cost vs. payoff.** Per-property mapping is engineer-time we ask clients to fund. Some clients will see the ROI (engineering velocity, reduced design-code drift); some will balk at the upfront cost. We need a defensible ROI framing for Code Connect specifically — currently we sell it as part of "AI-readiness" without naming the engineering cost or the productivity payoff in concrete terms.

4. **The MCP-without-component-data problem.** Our POV — that MCP needs a structured data layer to be useful — is correct but is currently named in our AI-Compatible Design Systems doc rather than client-facing materials. If clients adopt MCP without our `.ai.json` POV, they'll get the failure mode we've predicted, blame the AI tools, and potentially blame the design system. Worth getting ahead of in pitch decks.

5. **How much do we standardize Figma practice across the agency?** A single naming convention, a single multi-library template, a single contribution workflow — would speed every engagement but constrains client-specific judgement. A "VML Figma practice template" is a productizable artifact we don't currently have. (See also 09-gaps on the practice's productization gaps.)

6. **The Figma-as-MCP question for our own knowledge.** This vault is markdown; eventually we plan to expose it via an MCP server. Figma files containing client design systems could be similarly exposed to AI tools doing component implementation. The infrastructure for this is increasingly available; our POV on it is not yet articulated.

---

*Provenance: The multi-library tiering pattern (Foundations / Iconography / Core Components / Patterns), the `_` and `.` naming-prefix conventions, the variants-vs-component-properties decision rule, the slot pattern replacing legacy base-component patterns, the 4–5-level Auto Layout nesting threshold, and the deprecation lifecycle (mark / hide / migrate / sweep / delete) are de facto industry standards as of early 2026, named consistently in current practitioner writing and platform documentation. The DTCG → Style Dictionary pipeline framing aligns with Mangialardi (Design Systems for Developers, 2021), Curtis (Design Tokens, Nov 2024), and the AI-Compatible Design Systems doc (Feb 2025). The MCP-as-pipeline framing and the "structured component data layer required" caution on Dev Mode MCP are from our internal AI-Compatible Design Systems POV (Feb 2025) and Curtis's "stochastic, incomplete, and imprecise" caveat (2024). The Figma Variables API, Code Connect, branching, and library analytics are platform features documented at help.figma.com; specific mode caps, file-size ceilings, and emerging features (composite types, expression tokens, Extended Collections, the "Check Designs" feature name, slot-conversion gestures) are dated to 2025–2026 in current research but should be verified against current Figma documentation before client-facing recommendation. The `.ai.json` schema reference is internal practice IP from AI-Compatible Design Systems (Feb 2025). Cross-platform Code Syntax handling and the `(See 11-mobile-and-cross-platform.)` framing connect to internal practice on multi-platform delivery. This file was synthesized from a dual-agent research run in May 2026 (see `_research/_archive/2026-05-05-figma-best-practices.md` for the editorial trail).*

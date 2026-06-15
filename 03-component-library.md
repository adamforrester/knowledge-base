---
type: practice-area
title: Component Library
description: Component model — anatomy, properties, layout, composition primitives, components-as-data. Web rendering target assumed; mobile in 11.
tags: [phase, components, components-as-data]
timestamp: 2026-06-15
---

# 03 — Component Library

> The most visible artifact of the system. Also the part most likely to be mistaken for the system itself. Components are the medium through which the foundation propagates and the brand expresses; they are not the system.

---

## What this phase is, and why it matters

A component library is the third layer down — it sits on top of the foundation tokens and below the patterns and templates that consuming products assemble. The library is the unit clients see, the unit they buy, and the unit they will judge the engagement against. So we ship components carefully — but the practice should resist the gravitational pull that treats more components as more system. By 2026, the most consequential component decisions are not "what to build" but **how to *define* what we build** — the shift from components-as-Figma-files to components-as-data is the load-bearing change of this phase.

The internal practice has unusually deep IP here: the **UI Components series** (Nov 2024 — six docs covering Naming/Metadata, Anatomy, Properties, Layout/Spacing, Composition) is the most operational component-building methodology any consultancy publishes internally. Reading it against Curtis's 2025 *Components as Data* and Wolosin's 2025 metadata schema, the practice's vocabulary is closely aligned with the field's frontier — the gap is articulating that alignment in client-facing materials.

**This file's component model assumes a web rendering target.** The composition primitives, Group/GroupItem patterns, and configure-and-compose framing translate to native iOS, Android, and Flutter, but the component implementations do not — each platform requires its own component layer built against its own paradigm. (See 11-mobile-and-cross-platform.)

## What actually happens in this phase

Five clusters of work, mostly sequential within a component but parallelizable across components.

### 1. Inventory, audit, and qualification

Done partly in Discovery; sharpened here.

- **Pattern-spotting**, both objective and aspirational. (Mall, 2023, Activities #5 + #10 — "8 of 8 cards have small sans-serif body" *and* "what do we want more of / less of?")
- **Group by purpose, not appearance.** Two cards that look similar may serve different purposes; consolidate by problem, not visual similarity. (Perez-Cruz citing Kholmatova, 2021.) Our internal scoping doc already names this rule.
- **Component qualification** — does this earn its place? Multi-Brand Governance (Apr 2025) names four criteria, which align with the practice's implicit rule:
  1. The problem it solves (clearly).
  2. How it differs from existing components.
  3. Reusability potential — across teams or brands.
  4. Technical feasibility and accessibility compliance.
- **Rule of three** (Mall, 2023, Activity #26): "If three or more teams need this component right now, it goes in the design system."

### 2. Component anatomy

Decompose the component into named parts. Practice IP from the UIC series: **five questions** that define anatomy.

- What are the **elements**? (Container, slots, text, icons, controls, decorations.)
- Which are **required**, which **optional**, and *why*?
  - **Always required** (e.g., button label).
  - **Required depending on a property** (e.g., icon required when `iconBefore` is true).
  - **Required depending on behavior** (e.g., loading spinner during async state).
- Are elements named on **four naming axes**: Physical (where it sits), Ordinal (which one), Abstract (what type), Logical (what role)?
- Is each element **content** or **component**? (Content: configurable text/image. Component: instance of another DS component, e.g., a Button inside a Toolbar.)
- Is the component **integrated** (parts hard-coded, theme-locked) or **composed** (parts are slots that consumers fill)?

Curtis's 2025 *Components as Data* converges precisely on this anatomy vocabulary, with `type: container | slot | text` as the formal shape — confirming the practice's UIC framework is on industry-leading footing. (Curtis is treated as near-internal-tier weight.)

### 3. Properties

How a single component varies. Practice IP: **six questions** that define properties.

- What do consumers need to vary?
- What's the **default**? Heuristic: Most common / most important / most prominent.
- What's the **property type**: boolean, enum, instance-swap, content slot?
- Does the property name read clearly, with no homonyms?
- What is **design–code parity** for each property? (Design-only / Code-only / Intentionally-different — name each explicitly.)
- What property combinations are possible? (Complete — all combinations supported; Partial — some illegal pairs; Conditional — some pairs depend on other props.)

A few high-value sub-frameworks from the UIC series:

- **The Facade pattern** — for components where one prop coordinates resize across subcomponents (e.g., a `density` prop that retunes padding in every nested child).
- **"Prop smell"** — too many props with overlapping intent signals an anatomy problem, not a properties problem. Refactor to anatomy or split the component before adding the eighth boolean.
- **Combination set patterns** — explicit naming for which prop combinations are legal. Reduces accidental rendering.

This level of operational precision on properties is rare in published external sources — neither Frost nor Couldwell engages with prop schemas at this depth. The UIC series is genuinely differentiated practice IP.

### 4. Layout and spacing

How the component lays itself out and behaves under variable content.

- **Sizing approaches**: hugging (content-driven), fixed-height, special-shape (e.g., circular avatar). Each comes with its own auto-layout pattern.
- **Nesting model** — where padding lives. Outer container? Inner content frame? Per-element? The decision affects whether a component "fills" or "hugs" cleanly.
- **Group / GroupItem pattern** — for collections (ListGroup, CheckboxGroup, Tabs, RadioButtonGroup). The group owns layout; items own content.
- **Density mapped to a token multiplier scale** (`0_25x ... 2x`) ties spacing back to foundation tokens and supports density theming.

### 5. Composition

How components combine. The UIC series treats this as the philosophical climax — and rightly so. Composition is where *brand* lives (per the AI-Compatible doc and Perez-Cruz 2021): two interfaces built from identical components can feel completely different based on how they're composed.

Practice taxonomy:

- **Block / Area / Slot / Substitution** — four named composition primitives. A block is a fixed layout. An area is a region with constraints but flexibility. A slot is a content insertion point. Substitution is replacing a default with an instance-swap.
- **Lockup** — multiple elements treated as one positionally (logo + product name).
- **Extension** subcomponents — explicit override paths built into the system.

Practice rules of thumb (UIC series, verbatim where named):

- **Don't supercomponent.** A god-object component that handles every possible variant via 14 props is a refactor signal.
- **Caution made-to-order.** Components built for a single team rarely scale across; pause before building.
- **DO composable parts.** Build smaller, slot-friendly pieces that consumers can assemble. Configure-and-Compose: common things AND uncommon things.
- **"Trust them. They won't make this."** When deciding whether to support a long-tail composition, weigh actual likelihood. If three teams over five years have asked, build it; otherwise, don't pre-build.

Six rationales the practice uses for composition decisions: **Expression, Efficiency, Delegation, Autonomy, Quality, Maintenance.** Workshop empirical data captured in the UIC series: success rates for "Configure" (100%), "Compose-1" (~80%), "Compose-2" (~50%) — meaning the more nesting required, the more failure-prone. This belongs in any consumer team's training.

### 6. The 2025+ shift: components as data

This is the biggest single change to component-library practice since Atomic Design — and Curtis's 2025 essay names it as the post-tokens architectural move.

- A component definition is structured data (YAML/JSON), platform-neutral.
- Top-level fields: `anatomy / props / default / variants`.
- **Figma is one target among many**, not the source of truth. The data is the source; Figma assets are *outputs*.
- Auto-generates: docs, code (multi-platform), Figma component sets, registry entries, AI-readable metadata.
- Catalog scale: simple components ~20–50 lines of YAML; complex components 500+; a `core.yaml` with 30–50 components is "10,000s of lines."
- The 2025 caveat (Curtis): some things data still can't capture well — motion / non-trivial interaction, accessibility (Figma is structurally weak here), non-visual configs (Alert autohide duration). Pair component data with structured handoff for these. (The structured handoff for motion is treated in 21-motion-spec-and-handoff; the accessibility parallel is in 17-accessibility-annotation-contract.)

This is the defensible POV the practice should be writing into 2026+ engagements: components shipped as a data layer that *generates* the Figma library, the code, the docs, the registry — not as a Figma file with code "to follow."

The Figma side of this — how components are actually built in Figma to be both designer-usable and Code-Connect-mappable, when to use variants vs. component properties, how to use slots, and the mechanics of multi-library architecture — is covered in 12-figma-practice. The internationalization side — how components must grow with content, mirror in RTL, and slot-shape locale-formatted output — is covered in 13-internationalization-and-rtl. The accessibility side — ARIA encapsulation, keyboard contracts, focus management, the per-component conformance declaration — is covered in 14-accessibility. The AI side — why components-as-data is the architectural prerequisite for reliable AI-driven code generation, documentation, and governance — is covered in 15-ai-in-ds. The adaptive-UI side — why headless primitives plus intent metadata are what an LLM can actually compose against, and why a closed catalogue of heavily-composed components is *less* adaptable to LLM composition than open primitive-level code — is covered in 27-adaptive-interfaces-implementation. The documentation side — the per-component template the components-as-data substrate produces, the generation-vs-authoring seam, the CI freshness check, the conformance dossier slot — is covered in 29-per-component-documentation-template; the commercial-default angle of that pipeline (the engineering investment, the per-component hours math, the migration playbook, the cluster relationship to AI-readiness) is covered in 30-generated-from-data-documentation.

### 7. AI-readable metadata layer

Wolosin's 12-field schema (Jun 2025) plus the practice's `.ai.json` (Feb 2025) converge on the per-component fields that AI agents need:

- `component_id`, `primary_purpose`, `semantic_role`
- `when_to_use` (positive selection)
- **`avoid_when` (negative selection — uniquely important; AI defaults to using whatever it finds)**
- `required_content`, `optional_content` (slot contracts)
- `common_partners` (composition graph)
- `trigger_keywords` (prompt-to-component mapping)
- `generation_priority` (tiebreaker for the model)
- `layout_behavior`, `responsive_support`
- `confidence_threshold`, `business_context`, `user_journey_stage`, `required_dependencies`, `conflicts_with`, `design_tokens_used`, per-variant `when_to_use`

The `.ai.json` is essentially Wolosin's schema serialized at component scope. Aggregated into a **component registry** (CLI-bundled or CDN-hosted), they enable keyword search, dependency resolution, and confidence-ranked AI selection. Generated **component cards** (markdown + JSON, <2000 tokens each) feed RAG pipelines.

## Our POV

The CareCentrix 2026 commercial standard runs Build (component library) as a 4–6 week phase (MVP) or 16-week phase (extended), with these activities:

- Component architecture (foundational elements → composite patterns → containers/layout structures).
- Component design — each component on the token foundation; themeable, accessible, adaptable.
- Design patterns — common patterns for internal, data-heavy tooling (a playbook for frequent interface challenges).
- Usage documentation — when/how to use each component, do/don't, annotated specs.
- Content guidelines — tone of voice, error message patterns, help text best practices.
- Component validation — validated with pilot teams in context, ideally via Storybook.

MVP component set (CareCentrix Option 1): Button (primary, secondary, destructive, disabled); Text input & text area (with error/warning/success validation states); Select / dropdown; Checkbox / checkbox list; Radio button / radio button list; Toggle; Alert / notification banner; Badge / status tag.

Extended set (Option 2): Modal / dialog with scrim; Data table (basic structure, column headers, row states); Pagination; Tooltip / popover; Search input; Tabs; Accordion; Loading spinner / skeleton loader.

**Practice-distinctive POVs in this phase:**

- **The UIC series methodology.** Anatomy-five-questions, properties-six-questions, layout patterns, composition primitives (block/area/slot/substitution + lockup + extension), configure-and-compose. This is the most operationally specific component methodology any consultancy publishes internally. We should be selling this explicitly in pitches — most consultancies sell "we'll build components"; we sell "here is how we decide *what a component is*."
- **Hierarchical Component Model.** Foundations → Components → Patterns → Templates → Pages. Atomic Design as mental model; Couldwell's foundations naming as practical layer; both compatible.
- **Component qualification gate.** Problem solved + differentiation + reusability + a11y feasibility (cf. Multi-Brand 2025). We use this implicitly; should make explicit as a deliverable.
- **Embedded engineering during component design.** Components ship to the consuming codebase as completed — not at the end. (CareCentrix 2026: "incremental handoff, not a moment.")
- **Pilot validation milestone** at the end of Build with the consuming engineering team.

**Gaps in our current commercial Component standard, honestly named:**

- **Components-as-data is not in our 2026 deliverables.** The practice's AI-Compatible doc reaches the data structure layer; CareCentrix-style proposals do not yet sell components as YAML/JSON definitions that generate Figma assets and code. This is the leading edge of practice and Curtis names it as the post-tokens move. By end of 2026 it should be a default deliverable for engagements scoped past MVP.
- **Motion specs in components are missing.** The component templates list states (rest/hover/active/disabled) but don't specify entrance/exit motion, transitions between states, or motion guidelines per component. Head's framework would slot in cleanly. The architectural treatment now lives in 18-motion-foundations; the per-component spec contract lives in 21-motion-spec-and-handoff.
- **`.ai.json` is in the AI-Compatible doc but not the commercial proposal.** We have the IP; we don't yet sell it. By end of 2026 every component shipped should ship with its `.ai.json` peer file as default deliverable.
- **Accessibility annotations are referenced but under-specified.** The UIC series explicitly excludes Accessibility (along with Behavior, Motion, Theming) from scope. This is honest scoping but it's also a gap — the practice's component-level a11y annotations (focus states, ARIA roles, keyboard interaction, screen-reader labels) need a documented standard.
- **Component contribution and deprecation policy.** What happens after launch — how does a new component enter the system, how does an old one leave? The UIC series doesn't address this; commercial proposals leave it to "ongoing maintenance." (See `07-governance-and-adoption.md` and `08-ongoing-maintenance.md`.)

## External perspectives

### Validate

- **Curtis's "Components as Data" (Sep 2025)** — directly validates the practice's UIC-series anatomy-and-properties vocabulary. The data shape (`anatomy / props / default / variants`) maps almost 1:1 to the UIC series. Near-internal-tier weight; this is the most important external alignment for the phase.
- **Frost's atomic taxonomy** (atoms / molecules / organisms / templates / pages) — won the industry as vocabulary even where teams don't fold their components by it. Our practice uses the words; this is the source.
- **Couldwell's Foundations Model** (foundations / components / patterns / templates / pages, with features/screens for products) — the cleaner working vocabulary than Frost's chemistry; explicitly invented as a friendlier alternative. Our internal "Hierarchical Component Model" combines both lineages.
- **Perez-Cruz on group-by-purpose** — directly validates the scoping doc's purpose-grouping rule.
- **Wolosin's 12-field metadata schema** (Jun 2025) — validates the `.ai.json` contents and extends with specific fields (`avoid_when`, `common_partners`, `trigger_keywords`, `generation_priority`) the practice should adopt.
- **Figma DS x AI (2025)** on higher-order blocks (cards, headers, carousels) as the right unit for AI generation — validates that we should register both atomic primitives *and* compositional units.
- **Figma DS x AI** on Code Connect / MCP — validates the Figma pipeline layer of the AI-Compatible stack.

### Challenge

- **Curtis on "Figma as output, not input."** The most challenging single claim from external sources. If Figma is the output of component data, the practice's "Figma source of truth" framing in CareCentrix 2026 is a 2024-tier position. The 2026+ position is: data is source, Figma is generated. This is the biggest single positioning evolution the practice should make in the next 12 months.
- **Curtis on "MCP Dev Mode is a trap."** Many in the industry treat Figma's Dev Mode MCP as the AI-readiness solution. Curtis says it's "a stochastic, incomplete, and imprecise component description biased towards one platform (like React) and framework (like Tailwind)." Practice should agree publicly: formalize the data first; MCP exposes the data, doesn't replace it.
- **Perez-Cruz on supercomponents.** The UIC series rule "Don't supercomponent" aligns directly. The challenge from Perez-Cruz is that pushing too far in the other direction (everything as small composable parts) is also a failure mode — components become so generic they don't serve any specific purpose well. The right answer is contextual.
- **Frost on dogmatic naming.** Frost explicitly approves teams renaming the levels (e.g., GE: "Principles, Basics, Components, Templates, Features, Applications"). Our practice's "foundational / composite / containers / layout" naming is a valid variation; we should not feel obligated to use Frost's vocabulary in client work.
- **Mangialardi on headless UI components.** Pushes against opinionated component libraries (Material UI as the cautionary example); recommends Headless UI patterns (Tailwind Labs) for cross-framework systems. Worth considering for clients with multi-framework codebases.

### Extend

- **Wolosin's `avoid_when` field** is uniquely important and should be adopted in `.ai.json` schema by default. AI defaults to using whatever it finds; negative selection rules prevent more mistakes than positive ones.
- **Wolosin's `common_partners` field** encodes composition logic — close to the practice's UIC composition primitives but in a machine-readable form. Adopt.
- **Wolosin's `trigger_keywords` field** is the explicit prompt-to-component map. Most missing field from our current `.ai.json` thinking.
- **Curtis's `generation_priority`** as a model tiebreaker.
- **Figma's "blocks" framing** — register both atomic components AND higher-order compositional units (cards, headers, carousels) so AI can generate from blocks. Our practice tends to scope only primitives.
- **Curtis's component pipeline** (Plan → Design → Specs → Code → Design Doc → Design Assets → Release) is a more granular sequencing than our embedded-handoff narrative; worth adopting as the operational framework.
- **Curtis's effort curve** (gradual through Plan→Code, slow decline through Doc, sharp rise at Release) is useful for stakeholder expectation-setting on per-component cost.
- **Mangialardi's manual-extraction-then-automation pattern** for the first sprint of token bindings to components — forces the naming negotiation, then automates.

## Tensions and open questions

1. **Components as Figma vs. components as data.** The practice is at a 2024-tier "Figma source of truth" position; Curtis (2025) and the AI cluster argue for "data source of truth, Figma generated." Working synthesis: through 2026, ship Figma as primary deliverable and `.ai.json` as parallel deliverable. By 2027, flip the positioning so data is the source. This is a positioning shift more than a tooling shift; the JSON exists either way.
2. **Integrated vs. composed components.** UIC series acknowledges this is not always cleanly resolved. Working rule: integrated components for the most-common shapes (Button) where the cost of slot configuration would exceed benefit; composed components for variable contexts (Card with content area) where consumers will need flexibility. Don't try to make every component fully composable — it's an over-rotation toward primitives.
3. **Distinct vs. consolidated state.** Hover-and-active vs. interactive (combined). Disabled-loading vs. nested-state. The UIC series leaves this as a judgment call. A defensible default: if two states have meaningfully different visuals or behaviors, keep them distinct; otherwise collapse.
4. **Promotion-by-reuse threshold.** Curtis's "two components" rule for promoting component-scoped tokens to semantic, plus Mall's "rule of three" for promoting components into the system, plus Mall's "if three or more teams need this." All point at the same logic at different layers (token, component, pattern). Practice should adopt a unified rule of three across all these decisions to keep team conversations clean.
5. **How many components in MVP?** CareCentrix Option 1 ships ~8 core components. InVision MVP (2020) recommends "*only three* component groups." Practice can defend 8 as appropriate scope for an enterprise internal-tooling client; 3 is right for a fast-moving product team. Discovery should determine which.
6. **Component-level accessibility annotations as standard deliverable.** Practice does not yet ship a documented accessibility-annotation standard per component. Worth defining: focus states, ARIA roles, keyboard interaction, screen-reader labels, error states with content guidance. This is the most under-articulated practice gap in the phase.
7. **Higher-order compositional blocks as registry entries.** Figma (2025) makes a strong case for cards, headers, carousels as the right unit for AI generation. The practice's UIC series stops at the component layer. Adding "block" or "pattern" entries to the `.ai.json` registry — with their own metadata — would close the gap.

## Per-component briefs

03 is the practice's POV on the *component model* — anatomy, properties, composition, the configure-and-compose framing, the decision rules that apply across components. The model is system-level; it tells us *how* to think about any component but stops short of telling us how to think about *this* component. The seam between system-level model and per-component reasoning is where every engagement currently re-derives the same field-truth study from scratch — what does Polaris do, what does Spectrum do, what does Material call this, where does Carbon land on the API.

The **components/** catalogue closes that seam. It is a flat directory of per-component briefs, each one a 15-section field-truth study of a single component: framing, anatomy, properties/API, states and variants, usage guidance, accessibility, content guidelines, motion, internationalization, naming, implementation notes, related components, field POV evolution, sources cited, and an embedded agent-consumable schema. Briefs are written in the same prose-led, opinionated, first-person-plural voice as the numbered files. They are not docs pages — that is what 29's template ships. They are the *upstream* artefact: the practice's opinionated default the docs page is built from and the engagement's `.ai.json` is seeded from. (See `components/index.md` for the catalogue and the seed target list of ~40 components across the seven categories.)

The §15 agent-consumable schema is what makes the catalogue load-bearing for the AI-readiness story. Per 30, the engagement's component data file is the source of truth in *its* codebase; per 15, the four-layer AI documentation stack assumes a per-component machine-readable layer exists. The brief's §15 is the seed an engagement copies and instantiates. Free-form YAML for the first ~5 briefs; the schema formalises after the shape has stabilised through real use.

The first brief is **Button** — deliberately, because it is the most-shipped, least-agreed-upon component and so the hardest test of the spine. It lands the practice's defaults on the questions every engagement re-litigates: the two-axis `intent` + `appearance` model over a single overloaded `variant` enum, native-disabled versus a focusable inactive state, and the loading contract. (See `components/button.md`.) The second brief is **Text Field** — the encapsulation-boundary and accessibility-wiring calibration: the bundled-props-vs-composed-slots tension resolving to a hybrid, how far to split the typed-input family (NumberField separate, email/url/tel as `type`+attributes), placeholder-is-not-a-label with a static top-label default, read-only versus disabled, and the `aria-describedby` helper+error chain. (See `components/text-field.md`.) The third brief is **Textarea** — the sizing-model and inherited-substrate calibration, and the first brief to stand explicitly on another: ~80% is the Text Field substrate, inherited rather than re-derived, and the contested 20% is the sizing model (vertical-default `resize`, auto-grow with bounded `maxRows`, `field-sizing: content`), soft-over-hard grapheme-counted `maxLength`, and the Enter-as-newline contract with submit-on-Enter as an opt-in. (See `components/textarea.md`.) The first two **foundation primitives** — **Divider** and **Icon** — prove the spine's depth scales to the component: a divider's states and motion sections collapse to a sentence because a one-pixel non-interactive rule has nothing to say there, and that is correctness, not omission. **Divider** is the catalogue's first **claude-only** brief (the convergent-primitive escape hatch in the research-workflow rule), landing the decorative-by-default separator decision. **Icon** began as a claude-only brief and was then **promoted to dual-agent** when the second pass reopened the one genuinely contested point — delivery — refining a flat "icon fonts are dead" into a design-language-dependent rule (tree-shaken inline SVG for fixed-stroke systems; variable WOFF2 fonts for multi-axis/optical-sizing sets; legacy ligature/PUA fonts dead); it also lands the decorative-by-default accessible-name matrix and the icon-only-button trap. The promotion is itself the worked example: claude-only is the default for convergent primitives, upgraded to dual-agent when a contested seam surfaces. (See `components/divider.md`, `components/icon.md`.) The fifth brief is **Select** — the native-vs-custom calibration and the first written across a live platform inflection: the native `<select>`-vs-custom-ARIA-listbox decision as a framework rather than a winner, the select-vs-combobox boundary (non-destructive type-ahead vs. destructive filtering), the `aria-activedescendant` focus contract, and the Popover API / CSS Anchor Positioning / `appearance: base-select` shift that is collapsing the trade the component was organised around — a worked example of writing a brief durably against a moving platform, flagging the unverified platform claims rather than baking them in. (See `components/select.md`.) The seventh brief is **Combobox** — the two-state-reconciliation calibration and the first to stand on *two* substrates at once (the text-field form-stack and select's overlay machinery, both inherited rather than re-derived): the destructive filter that separates it from Select, the `inputValue`-vs-`value` tension that drives nearly every combobox bug, `aria-autocomplete=list` with inline/both as opt-in traps, async debounce + `AbortController` race handling, the token-vs-checkbox multi-select split, and the ARIA 1.2 pattern (role on the input, not the deprecated 1.0 wrapper). (See `components/combobox.md`.) The eighth brief is **Checkbox** — the decomposition calibration and the first of the boolean/choice controls: it resolves the atomic-box / labelled-row / group question to a two-component public surface (`Checkbox` + `CheckboxGroup`) plus an exposed `Checkbox.Control` primitive — the text-field bundled-vs-composed hybrid applied to a control, with both research passes converging on it independently — and lands indeterminate-as-DOM-property, the whole-row hit target, `role=group` over `fieldset`, and the staged-vs-immediate checkbox-vs-switch boundary. It deliberately establishes the **selection-control decomposition** that Radio (group mandatory) and Switch (no group) will refine. (See `components/checkbox.md`.) The ninth brief is **Radio** — the same decomposition with one mutation (the group is mandatory; `RadioGroup` owns `name` + single value + validation), which both passes inherited without dispute; it resolves the roving-tabindex single-tab-stop keyboard model and the contested selection-follows-focus question (landing on follows-focus as the native-aligned default with explicit-selection as a documented opt-out), and lands no-deselect + the explicit "None", start-empty default selection, and the radio-vs-segmented-control boundary. (See `components/radio.md`.) The tenth brief is **Switch**, which **closes the selection-control decomposition arc** by removing the group entirely (checkbox optional, radio mandatory, switch none): it states the immediate-effect contract (the staged-vs-immediate boundary from the switch side), resolves the async/optimistic-update model (optimistic default plus a first-class pending/loading lock), the `role=switch`-vs-`aria-pressed` distinction, the label-leading settings-row pattern, and supported read-only. With Checkbox, Radio, and Switch complete, the practice now has one stated selection-control decomposition with all three group variations resolved. (See `components/switch.md`.) The eleventh brief is **Toggle Button** — a Button that carries a persistent binary pressed state (`role=button` + `aria-pressed`), which states the setting-vs-action/mode boundary with Switch, the persistent-`selected`-vs-transient-`:active` trap, and the constant-name + `aria-pressed` pattern; it is the atomic unit of a Toggle Button Group, which presented compactly is the **Segmented Control** (a dual-agent run in progress that closes the toggle-group boundary the form batch repeatedly referenced). (See `components/toggle-button.md`.) The twelfth brief is **Segmented Control** — the Toggle Button Group as a connected control, and the catalogue's most semantically contested component: it resolves a four-model ARIA fork by *purpose* (`role=group` + `aria-current` for the immediate view-switcher, `radiogroup` only for a deferred form input, `aria-pressed` for multi-select), which **refines the Radio brief's simplification** that segmented and radio share an a11y tree; it also lands the two visual paradigms (track-and-pill vs. connected buttons), the segmented-vs-tabs / -radio / -select boundaries, the 2–5-segment no-overflow rule, and `disallowEmptySelection`. (See `components/segmented-control.md`.) The thirteenth brief is **Slider** — the last standalone form control: one overloaded component (scalar|tuple value for single vs. range), the step/tick + IEEE-754 float-rounding math, the `aria-valuetext` and Arrow/Page/Home-End keyboard contract, and the headline slider-vs-NumberField precision boundary resolved via the bi-directionally-synced paired-input composite (also the accessibility escape hatch), plus the pointer-capture / thumb-overhang / thumb-collision implementation traps. (See `components/slider.md`.)

## Failure modes specific to this phase

- **Supercomponent.** A component grows 14 props, 6 boolean flags, 4 enum dimensions to handle every possible variant. Sign of an anatomy problem. (UIC: "Don't supercomponent.")
- **Atomic-only library, no blocks.** Buttons, inputs, icons — fine for humans who can compose. Generative AI struggles to assemble cohesive layouts from primitives alone. (Figma 2025.)
- **Components without `avoid_when`.** AI agents and junior designers default to using whatever's available. Without explicit negative selection rules, the wrong component gets chosen for the job.
- **Visual taxonomy without purpose taxonomy.** Two cards that look similar are filed as the same component; a year later one team's Card is doing four different jobs and can't change without breaking three others. (Perez-Cruz / Kholmatova.)
- **Made-to-order components.** A team requests a one-off component; the system team builds it; nobody else uses it. The system bloats with single-purpose entries.
- **Components that drift from tokens.** A component is built on tokens initially; six months later, ad-hoc hex values appear in variant overrides. (Curtis: "If I had a nickel for every time I detected a raw value in a stray variant when a token is needed, I'd be rich.")
- **Documentation lag.** Components ship; docs follow weeks later. Consumers either build wrong or wait, both of which damage adoption. (Couldwell: document as you go.)
- **No pilot validation.** Components built in isolation, never used by a real consuming team before launch. Surfaces wrong assumptions about prop combinations only after public release.
- **Component-level a11y as afterthought.** Focus states, ARIA, keyboard interaction added in remediation. The system inherits accessibility debt that any consumer also inherits.
- **Compose-2 ignored as a known failure rate.** Workshop data shows ~50% success on two-deep compositions; if the design assumes consumers will reliably nest, the system has a design problem, not a documentation problem.

---

*Provenance: The component anatomy five-questions, properties six-questions, layout/sizing patterns, Group/GroupItem pattern, density-as-multiplier, composition primitives (Block/Area/Slot/Substitution + Lockup + Extension), the configure-and-compose framing, the "Don't supercomponent / Caution made-to-order / DO composable parts" rules, the six rationales (Expression / Efficiency / Delegation / Autonomy / Quality / Maintenance), and the empirical workshop success rates (Configure 100% / Compose-1 ~80% / Compose-2 ~50%) are all internal practice IP from the UI Components series (Nov 2024). The `.ai.json` schema, component registry, and component cards are internal POV from AI-Compatible Design Systems (Feb 2025). The Hierarchical Component Model, MVP and extended component lists, and incremental-handoff positioning are from CareCentrix 2026 + VML library (2024–2026). Components-as-data (anatomy / props / default / variants), Figma-as-output, the Plan→Design→Specs→Code→Doc→Assets→Release pipeline, the effort curve, and the YAGNI-driven promotion rule are from Nathan Curtis (Components as Data Sep 2025; Operating Design Systems workshop Sep 2023), treated as near-internal-tier weight. The atomic taxonomy and "mental model not folder structure" framing are from Brad Frost (Atomic Design, 2016). The Foundations Model and Components/Patterns split are from Andrew Couldwell (Laying the Foundations, 2019). Group-by-purpose, supercomponent critique, and "your design system is your pantry, not your cookbook" are from Yesenia Perez-Cruz (Expressive Design Systems, 2021). The 12-field component metadata schema (with avoid_when, common_partners, trigger_keywords, generation_priority emphasized) is from Diana Wolosin (Indeed, Jun 2025). Higher-order blocks framing, Code Connect, and MCP-as-pipeline are from Figma DS x AI (2025). Headless UI architectural pattern is from Mangialardi (Design Systems for Developers, 2021). The four-criterion qualification process is from Multi-Brand Governance (Apr 2025). Rule of three is from Mall, 90 Days (2023).*

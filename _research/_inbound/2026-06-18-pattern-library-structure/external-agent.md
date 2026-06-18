# Pattern-library structure — external-agent pass

*Second independent pass for the meta-research run. Captured verbatim as the dual-agent audit record. Synthesis with `claude.md` is folded into `patterns/_schema.md` and `patterns/index.md`; see the run's reconciliation note / commit.*

---

## Architectural Validation of Design System Pattern Libraries: A Field-Truth Meta-Study

The codification of design knowledge has largely succeeded at the atomic and molecular levels of user interface design. Components—such as buttons, inputs, and dialogs—are well-defined, predictably scoped, and universally understood across the digital product industry. However, at the macro level of pattern libraries, the field lacks consensus and routinely devolves into architectural ambiguity. As systems scale to handle complex, multi-state user journeys, the boundaries between components, patterns, and foundational guidelines become highly contested.

This report provides an exhaustive, field-truth analysis of how leading design systems structure their pattern libraries as of mid-2026. The objective is to thoroughly validate, critique, and refine a proposed pattern library scaffolding—specifically evaluating the component-versus-pattern boundary, the taxonomic tiers, the documentation schema, and the candidate list. Crucially, this analysis addresses the practitioner's intent to optimize this architecture for machine consumption via a Model Context Protocol (MCP) server, recognizing that AI agents require deterministic, structured context rather than traditional human-targeted prose.

### Framing: The State of Pattern Libraries and the Definitional Schism

To understand why leading design systems disagree on what constitutes a pattern, one must trace the lineage of the term. The concept of the "design pattern" originated in architecture with Christopher Alexander before being adapted into software engineering and subsequently into human-computer interaction by researchers such as Jenifer Tidwell in Designing Interfaces. In its original academic and interaction-design lineage, a design pattern is a behavioral resolution to a recurring human-computer interaction problem. Platforms like UI-Patterns.com categorize these behavioral heuristics under cognitive umbrellas such as "Safe Exploration," "Satisficing," or "Deferred Choices".

However, modern design systems have largely deviated from this purely behavioral lineage, pivoting toward implementation and structural composition. The Nielsen Norman Group notes that while a component library specifies individual user interface elements, a pattern library specifies reusable groupings of those individual elements, such as a page header composed of a title, a breadcrumb, a search field, and primary actions. This shift from cognitive solutions to structural groupings has fractured the industry.

The field currently suffers from a definitional schism regarding how to categorize these groupings. Some systems categorize patterns structurally, focusing on the interface output itself, such as forms or data tables. Others categorize them functionally, focusing entirely on user intent, utilizing task-based groupings. Furthermore, some systems have abandoned the "pattern" moniker entirely, absorbing compositional logic into foundational layout guidelines or macro-components. This lack of consensus presents a significant architectural challenge when designing a meta-taxonomy intended to be universally applicable and machine-readable for artificial intelligence agents.

### The Field-Truth Survey: Structural Paradigms of Leading Systems

An exhaustive analysis of the industry's leading design systems reveals severe divergence in how pattern libraries are organized, titled, and scoped.

- **IBM Carbon (v11/v12)** — Top-level "Patterns." Defines patterns as "best practice solutions for how a user achieves a goal" combining components and templates. Highly structural categorization: Common actions, Dialogs, Empty states, Forms, Loading, Search.
- **Material Design 3 (M3)** — "Foundations > Layout." Abandons the standalone "Patterns" moniker. Groups compositional concepts under "Canonical Layouts" (Feed, List-detail, Supporting pane). Cross-cutting state/accessibility rules kept strictly within "Foundations."
- **GOV.UK Design System** — "Patterns." Strictly functional, task-driven taxonomy: "Ask users for…" (Names, Addresses, Dates), "Help users to…" (Navigate, Check answers, Complete multiple tasks), and "Pages" (Confirmation, Errors).
- **Atlassian Design System** — "Patterns." Defines patterns as the combination of "components and foundations to create consistent experiences." Strongly emphasizes structured, machine-readable schemas; invests heavily in AI context engines and MCP servers.
- **Microsoft Fluent 2** — "Patterns & Experience Patterns." Distinguishes Controls (UI elements) from Patterns (reusable recipes of multiple controls). Recently introduced AI-specific "Experience Patterns" detailing inline widget constraints versus side-by-side workspace orchestration.
- **Ant Design (v6.0)** — "Design Patterns." Encompasses function examples, templates (page-level), and business components (block-level). Features dynamic layout adaptations and native LLM integration via `llms.txt` exposing components to agents.
- **Adobe Spectrum (v2)** — Embedded in Components & Foundations. Does not elevate "Patterns" to a distinct top-level tier. Relies on detailed component documentation and robust token schemas. Design data exposed to AI via the Spectrum Design Data MCP server.
- **Shopify Polaris** — "Patterns vs Foundations." Separates abstract system rules (Foundations) from recurring compositional assemblies (Patterns), prioritizing merchant workflows and e-commerce-specific task resolutions.

The primary architectural disagreement is the cognitive framing of the taxonomy. Carbon and Fluent organize patterns around the interface output. GOV.UK organizes patterns around human intent, explicitly asking what the user is trying to accomplish. Material Design 3 dissolves the "Pattern" tier entirely, dispersing its concepts into responsive layout primitives and high-level component documentation.

### The Pattern-Versus-Component Boundary

The practitioner's proposed scaffolding defines a component as a "thing" with properties, states, variants, and an API, and a pattern as a recurring composition resolved via decision rules that owns cross-component orchestration and "does not ship as one importable thing."

This boundary is philosophically elegant but technically fragile in modern front-end architectures. The assertion that a pattern cannot ship as a single importable entity is rapidly being invalidated. Leading systems increasingly ship "macro-components" or "pro-components" that encapsulate complex orchestration logic, blurring the line. Ant Design ships ProForm and ProTable as importable, heavily abstracted components that manage internal state, validation, and layout. Microsoft Fluent provides advanced collection controls like Items repeater and Tree view that handle hierarchical list patterns natively. IBM Carbon is adopting Web Components to encapsulate broader logic. GOV.UK specifically notes that its "Step by step navigation" pattern is an exception because they do not provide the code for it in govuk-frontend—highlighting that usually they DO provide code for patterns.

Debated elements: **Card** is a Component (M3, Fluent) despite being compositional—it ships via a primary API. **Search** is a Component AND a Pattern (Carbon, GOV.UK)—the input field is a component, the type-ahead/empty-state/scope logic is a pattern. **Data Table** is universally a Component (Carbon, Ant) despite massive orchestration. **Dialog/Modal** is a Component (Atlassian) AND a Pattern (Carbon).

Therefore the boundary requires sharpening. The defining characteristic of a pattern is not its packaging or importability, but its **contextual dependency** and its role in dictating **business logic**. A component is agnostic to the user's ultimate goal; a `<Button>` does not care whether it sits in a checkout or a profile update. A pattern is a highly opinionated resolution to a specific user goal, contextualized by business logic, spatial layout, and temporal flow. For AI agents, maintaining the distinction based on opinionation and orchestration rather than code packaging is critical: an agent needs to understand that `<Wizard>` is the structural component, but the Multi-Step Checkout Pattern dictates the validation, data-persistence, and state decision rules within that structure.

### Validation and Critique of the Taxonomic Tiers

- **`cross-component-recipe`** is robust and aligns with the field (Fluent's "recipes"). Nomenclature is verbose and could be streamlined.
- **`state-convention` must be rejected as a pattern category.** Leading systems overwhelmingly categorize interaction/disabled states and generic accessibility orchestration as foundational guidelines. M3 places "Interaction states" under Foundations; Spectrum handles states as global token properties. Elevating a cross-cutting state rule to a "pattern" introduces taxonomic redundancy. For an MCP server, treating states as patterns will confuse agents applying global semantic modifiers to local components—token bloat and context conflicts.
- **`flow-and-shell` forcibly combines temporal interactions with spatial architectures.** Flows operate over time (sequential steps, data persistence, error recovery). Shells operate over space (persistent headers, sidebars, mainframes). Combining them obscures distinct design constraints.
- **`page-template` is problematic as a standalone pattern category.** It contradicts M3, which isolates these into "Canonical Layouts." Layouts define responsive grids and pane behaviors; patterns define the functional actions within those panes.

**The Defended Taxonomy:** a refined hybrid that excises foundational rules, separates temporal and spatial concerns, and borrows M3's structural clarity plus GOV.UK's goal-oriented framing:

1. **Compositions (Spatial Recipes)** — replaces cross-component-recipe. Localized, single-screen orchestrations. *Forms-as-a-system, Filtering, Search orchestration, Data Visualization, Complex Data Tables.*
2. **Flows (Temporal Journeys)** — extracted from flow-and-shell. Multi-step interactions requiring state persistence, error recovery, sequential navigation. *Multi-step wizards, Authentication, Destructive confirmations, Save/Resume, Onboarding.*
3. **Layouts & Shells (Structural Archetypes)** — replaces page-template + the spatial aspect of flow-and-shell. Responsive macro-architecture. *App shell, Global headers, Master-detail (List-detail), Feed layouts, Supporting pane layouts.*
4. **Foundations (Cross-Cutting Rules)** — replaces state-convention; removes these from the pattern library entirely. *Disabled state logic, Loading orchestration, Notifications orchestration, Theming, Accessibility.*

### Validation of the Pattern-Brief Spine

The ALWAYS / SCALES model is highly effective and maps accurately to Carbon and GOV.UK. "Decision rules" as a center of gravity excellently differentiates a pattern from a component: a component API dictates *how* to implement; decision rules dictate *whether* to.

For an MCP server the spine must be rigorously optimized to prevent context-window bloat. Unstructured-prose ingestion produces generic "UI slop" and consumes massive tokens (Atlassian observed 4–7M tokens, frequent hallucination). The agent-consumable schema cannot mirror the component schema: component schemas focus on props/types/event-handlers; pattern schemas must focus on dependencies, conditional rendering logic, and layout constraints. The spine must enforce **deterministic logic**: not "consider a radio group if there are only a few options" but `Rule: IF options <= 4, USE RadioGroup; IF options > 4, USE Select`. The composition section must use explicitly typed component references (`requires: [TextInput, Button, Tooltip]`) so an agent can fetch those API schemas before generating code.

### Validation of the Candidate Pattern List

**Compositions:** Rightly includes Forms-as-a-system, Filtering, Search, Overflow content, Data Visualization, Inline-edit, Bulk actions, Comparison/Pricing tables. Data Visualization needs deep guidance on color mapping and charting archetypes. **Miscategorized:** "Pagination vs Infinite Scroll" is behavioral, but pagination itself ships as a component; "Command Palette" increasingly ships as a single-import component. **Missing:** Empty States (zero-data, first-use, error recovery—heavily documented by Carbon/Atlassian); "Check Answers" (GOV.UK—review/amend before final submit); Status Trackers / progress indicators (long-running background processes).

**Flows:** Login/Auth, Multi-step wizard, Destructive confirmations, Save/Unsaved-changes, Progressive disclosure, Onboarding align perfectly. **Relocate to components:** Comment threads, Activity feeds (typically shipped as composite components). **Missing:** Eligibility / "Check a service is suitable" triage (GOV.UK—prevents deep-transaction failure); AI Conversational Flows (chat vs inline generative AI—Fluent Copilot guidelines).

**Layouts & Shells:** App shell, Global header, Master-detail, Dashboard, Settings, Error pages are correct. **Miscategorized:** "Responsive/adaptive layout" is a global foundational rule set, not a discrete layout pattern. **Missing:** Feed Layouts, Supporting Pane Layouts (M3 canonical layouts).

**Exiled to Foundations:** Disabled states, Read-only semantics, Loading orchestration, Notifications orchestration, Theming, Dark-mode, Internationalization/RTL. System-wide heuristics, not localized discrete patterns.

**Prioritized Validated Seed List:**
1. **Empty States** — low complexity, high impact; rules for replacing underlying layouts with state messaging.
2. **Search Orchestration** — moderate; active vs focused, type-ahead, scope filtering.
3. **Forms-as-a-system** — high complexity; deterministic validation flows, error recovery, required vs optional heuristics.
4. **List-Detail Layout** — structural backbone of enterprise software; canonical pane behaviors across breakpoints.
5. **Multi-step Temporal Flows** — wizard orchestration, progress persistence, step-by-step navigation.
6. **Destructive Confirmations** — risk mitigation; thresholds for inline alerts vs modal interruptions.

### The Agent-Consumability Angle and MCP Architecture

The MCP-server intent is the most critical variable. An architecture optimized solely for human reading fails under AI orchestration due to context-window bloat, token inefficiency, and unstructured ambiguity. Monolithic ingestion skyrockets token use while accuracy plummets (Atlassian: 4–7M tokens, hallucinatory generic UIs). Systems adopt schema-preserving tool compression in their MCP servers.

The taxonomy itself must act as an efficient indexing tool. With the defended taxonomy, the MCP server exposes a `list_patterns()` tool returning brief descriptions; on identifying the needed pattern, the agent calls `get_pattern_schema("multi-step-wizard")` to retrieve the deterministic decision rules and component dependencies on demand. This lazy-loading, combined with deterministic decision rules, delivers concentrated, relevant context and prevents the model from drowning in global state guidelines or irrelevant typography tokens.

### Conclusion

The instinct to separate patterns from components is correct, but the boundary predicated on code importability is outdated and incompatible with modern component architectures. Pivot to a taxonomy based on Compositions, Flows, and Layouts; strictly exile global state guidance into a separate Foundations directory. Enforce a deterministic, machine-readable schema within the ALWAYS/SCALES spine so the MCP server delivers high-fidelity, constrained context to authoring agents—bridging human design intent and reliable AI code generation.

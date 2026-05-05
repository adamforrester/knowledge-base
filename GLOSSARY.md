# Glossary

Vault-specific and practice-adjacent vocabulary. Common DS terms (token, component, variant) are assumed and not defined here. People and project names are not in this glossary; they appear in provenance footers and are searchable directly. Where a term is most fully developed in a particular file, the file is linked.

---

## A

**ACR (Accessibility Conformance Report)** — Public artifact stating a system's accessibility conformance, based on the VPAT template. The procurement-grade version of an "accessibility promise." (See 14-accessibility.)

**`.ai.json`** — Internal-tier component metadata schema from the practice's *AI-Compatible Design Systems* doc (Feb 2025). Per-component structured data including `component_id`, `primary_purpose`, `when_to_use`, `avoid_when`, slot contracts, and accessibility metadata. The practice's instantiation of components-as-data. (See 03-component-library, 15-ai-in-ds.)

**APCA (Accessible Perceptual Contrast Algorithm)** — Perceptual contrast model that more accurately predicts readability than WCAG 2.x's relative-luminance ratio. Candidate for WCAG 3; not yet a compliance standard as of early 2026. Use as internal target; cite WCAG 2.2 for compliance. (See 14-accessibility.)

**APG (ARIA Authoring Practices Guide)** — W3C's canonical pattern catalog for composite widgets (combobox, menu, tabs, listbox, dialog, treegrid, etc.). Components implementing composite patterns should conform to APG. (See 14-accessibility.)

**Atomic Design** — Brad Frost's mental-model framing (atoms / molecules / organisms / templates / pages). The practice treats this as a *mental model, not a folder structure*. (See 03-component-library.)

---

## B

**Bidi (bidirectional text)** — Mixed-direction text (Latin URL inside Arabic paragraph). The Unicode Bidi Algorithm (UAX #9) handles ordering; `<bdi>`, `dir="ltr"`, and `unicode-bidi: isolate` are the practical CSS/HTML controls. (See 13-internationalization-and-rtl.)

**Block / Area / Slot / Substitution** — Core composition primitives from the UIC series. With *Lockup* and *Extension* added, these form the practice's composition vocabulary. (See 03-component-library.)

---

## C

**Code Connect** — Figma feature linking design components to production code. When set up, Dev Mode shows the actual code snippet from the consuming repo instead of generic CSS. The substrate that lets AI generation reference real component imports. (See 12-figma-practice, 15-ai-in-ds.)

**Components-as-data** — Curtis's POV (Sep 2025) that a component is structured data (anatomy, props, default, variants), and Figma + code + docs are *outputs* generated from that data. The architectural prerequisite for reliable AI-driven DS work. (See 03-component-library, 15-ai-in-ds.)

**Composite token** — A token holding multiple values as a unit (e.g., a shadow as `[x, y, blur, spread, color]` rather than five separate tokens). Tokens Studio supports these natively; Figma Variables support is emerging. (See 02-design-foundations, 12-figma-practice.)

**Configure-and-Compose** — Practice framing for component flexibility: components should be both configurable (props handle the common cases) and composable (slots handle the uncommon ones). Workshop empirical data: ~100% success on Configure, ~80% on Compose-1, ~50% on Compose-2. (See 03-component-library.)

---

## D

**DTCG (Design Tokens Community Group, W3C)** — The W3C working group defining the standard JSON format for design tokens. The format moved from long draft toward stable through 2024–2025; Figma's native export aligns to it. The interchange format that lets tokens flow between tools without re-authoring. (See 02-design-foundations.)

---

## E

**EAA (European Accessibility Act)** — EU regulatory framework requiring digital accessibility for products and services sold in the EU. Enforceable since June 28, 2025. Materially raises the regulatory floor for EU-facing consumer products. (See 14-accessibility.)

**Embedded handoff** — Practice operating model: engineering joins from Discovery, components ship into the consuming codebase as they complete (not at the end). Differentiates from consultancies that ship a Figma file and walk away. (See 00-principles, 06-pilot-and-implementation.)

**EN 301 549** — EU's harmonised technical standard for accessibility, basis of EAA technical conformance, references WCAG 2.x. (See 14-accessibility.)

**Expression token** — A Figma Variable with conditional or computed logic (e.g., `if(is-dark, #FFF, #111)`). Reported as a 2026 capability; verify current Figma docs before recommending. (See 12-figma-practice, 15-ai-in-ds.)

---

## F

**Foundations Model** — Andrew Couldwell's framing (*Laying the Foundations*, 2019). The practice uses it for the foundation tokens layer beneath components and patterns. (See 02-design-foundations.)

**Four-layer AI stack** — Internal practice POV from *AI-Compatible Design Systems* (Feb 2025). The architecture layers an AI agent needs to engage with a DS reliably. (See 02-design-foundations, 05-development-support, 15-ai-in-ds.)

---

## G

**Group / GroupItem** — Component pattern from the UIC series for parent–child composition where the parent owns layout and styling and children are content slots. (See 03-component-library.)

---

## H

**Headless UI** — Architectural pattern (Tailwind Labs' Headless UI, Radix UI, React Aria): functionality (focus management, keyboard nav, ARIA) encapsulated in unstyled components; styling applied by the consumer. Mangialardi's recommendation for cross-framework systems. Counter-pattern to opinionated libraries like Material UI. (See 05-development-support.)

**Hierarchical Component Model** — Internal practice framing for organizing components by purpose and semantic role rather than visual category. (See 03-component-library.)

---

## I

**ICU MessageFormat** — Unicode/ICU standard for parameterized strings supporting pluralization, gender, and grammatical cases across locales. The replacement for string concatenation in i18n. (See 13-internationalization-and-rtl.)

**Influence Map** — Mall's Discovery artifact (90 Days Activity #3): green/yellow/red on supportive/undecided/opposed; thick/thin arrows on relational influence. The most useful single Discovery deliverable in the external corpus. (See 01-discovery-and-strategy.)

**Intl.* (JavaScript)** — The JS API for locale-aware formatting (`Intl.NumberFormat`, `Intl.DateTimeFormat`, `Intl.PluralRules`). The boundary the DS draws: the application uses `Intl.*` to produce formatted strings; DS components display them. (See 13-internationalization-and-rtl.)

---

## L

**Levers and dials** — Yesenia Perez-Cruz framing for system flexibility: levers are big choices (variant, density), dials are fine-grained (token overrides). (See 02-design-foundations.)

**Logical properties** — CSS properties that resolve to physical sides based on the document's writing mode and direction (`margin-inline-start`, `padding-inline-end`, `text-align: start`). The 2026 default for bidirectional layout. (See 13-internationalization-and-rtl.)

**Lockup** — Composition primitive: a fixed arrangement of multiple components treated as a unit (e.g., logo + tagline). (See 03-component-library.)

---

## M

**MCP (Model Context Protocol)** — Anthropic standard for connecting AI applications to external data sources via a server-and-tool-call protocol. Used in DS work to expose Figma context (Figma Dev Mode MCP), production code (Code Connect via MCP), and DS metadata (custom DS MCP servers) to AI coding assistants. (See 12-figma-practice, 15-ai-in-ds.)

**MCP-first vs. screenshot-first** — Practice POV on design-to-code AI: MCP-first gives the agent structured DS context and produces system-compliant code; screenshot-first infers from pixels and produces "AI slop." The architectural choice that determines whether AI generation is production-acceptable. (See 15-ai-in-ds.)

---

## N

**North Star (Mall / Watkins)** — Discovery artifact mapping the *organization's* mission, network, strategy, and vision. Mall's pointed instruction: write the company's North Star, not the design system's. The system aligns to the org, not the other way around. (See 01-discovery-and-strategy.)

**Noto** — Google's universal-coverage font family ("no tofu" project) covering virtually every Unicode script. The default fallback in multi-script font stacks. (See 13-internationalization-and-rtl.)

---

## O

**Opinionated library** — Architectural pattern (Material UI as canonical example): functionality and styling tightly coupled. Faster to start with, harder to brand-extend. Counter-pattern to Headless UI. (See 05-development-support.)

**Overlay (accessibility overlay)** — Third-party scripts that promise automated accessibility compliance via JavaScript injection. Increasingly the target of accessibility lawsuits because they conflict with assistive technologies and don't address structural issues. The practice's position: not a substitute for built-in accessibility. (See 14-accessibility.)

---

## P

**Pair tokens** — Color tokens that encode contrast as a property of the foreground/background *pair* (e.g., `color/text/on-surface-primary` validated at 4.5:1 against `color/surface/primary`). The token-layer architecture that makes contrast compliance enforceable at build time. Adobe Spectrum's pattern, generalized. (See 14-accessibility.)

**Pantry vs. cookbook** — Yesenia Perez-Cruz framing: "Your design system is your pantry, not your cookbook." Components are ingredients; products are the recipes that compose them. (See 03-component-library.)

**Phase model** — The vault's numbering reflects an engagement phase model: Discovery (01) → Foundations (02) → Components (03) → Documentation (04) → Dev Support (05) → Pilot (06) → Governance (07) → Maintenance (08). (See CLAUDE.md.)

**Pseudo-localization** — Test technique replacing strings with elongated, accented, bracketed text (`[Ĥéééļļļööö]`) to surface hardcoded strings and layout fragility. Bidi pseudo-locales also test direction. The cheapest layout-validation tool i18n provides. (See 13-internationalization-and-rtl.)

---

## R

**RACI (Responsible / Accountable / Consulted / Informed)** — Stakeholder-mapping convention for clarifying who does what in a workflow (contribution, governance, escalation). Useful when client orgs already operate in those terms. (See 12-figma-practice, 07-governance-and-adoption.)

**Roving tabindex** — Keyboard pattern for composite widgets (tabs, menus, toolbars): only one element of the composite is in the page tab order at a time; arrow keys navigate within. Counter-pattern to `aria-activedescendant`. (See 14-accessibility.)

**Rule of three** — Mall's heuristic for promoting patterns into the system: three independent uses justify systematization. (See 03-component-library.)

---

## S

**Six rationales** — Practice framing for composition decisions: Expression / Efficiency / Delegation / Autonomy / Quality / Maintenance. Used to justify whether a component should be configurable, composable, or both. (See 03-component-library.)

**Six Signs** — VML library Section 5. Practice diagnostic for opportunity recognition (when a client should invest in a design system). Strong for first executive conversations; less precise as a maturity instrument. (See 01-discovery-and-strategy.)

**Section 508** — US federal procurement accessibility standard, references WCAG. Used as a regulatory floor in regulated-industry engagements. (See 14-accessibility.)

**Specs CLI** — Curtis's tool (github.com/DirectedEdges/specs) operationalizing components-as-data. Generates structured component specs from Figma files and packages design intent for developer/AI consumption. (See 03-component-library, 15-ai-in-ds.)

**Style Dictionary** — Token transformation tool by Amazon. Canonical pipeline component: takes DTCG JSON and produces platform-specific outputs (CSS, SCSS, Swift, Kotlin, Dart). Mangialardi spent 60 pages on it. (See 02-design-foundations.)

**Substitution** — Composition primitive: replacing one component with another at the same slot position (e.g., swapping an `Avatar` for a custom element). (See 03-component-library.)

---

## T

**Theming dimensions (Curtis's seven)** — Curtis's catalog of dimensions a system may need to theme across, in ascending cost: Responsive, Light/Dark, Multi-brand, Campaigns, Design Generations, White Label, Density. (See 02-design-foundations.)

**Tokens Studio** — Figma plugin for token authoring, transformation, and DTCG export. Mature; widely used. Increasingly being replaced by native Figma Variables for daily designer work, retained for engineering-side transformation pipelines. (See 02-design-foundations, 12-figma-practice.)

---

## U

**UIC series** — The practice's *UI Components* series (Nov 2024, six docs covering Naming/Metadata, Anatomy, Properties, Layout/Spacing, Composition). The most operationally specific component-building methodology any consultancy publishes internally. Source of the anatomy five-questions, properties six-questions, layout patterns, composition primitives, and configure-and-compose framing. (See 03-component-library.)

---

## V

**VPAT (Voluntary Product Accessibility Template)** — Standard template for documenting accessibility conformance against WCAG/Section 508. Source format for the ACR (the public artifact). (See 14-accessibility.)

---

## W

**WCAG 2.2** — Web Content Accessibility Guidelines, current stable version as of early 2026. Adds Focus Appearance (2.4.11), Target Size Minimum (2.5.8), and other criteria over 2.1. Practice baseline for product-led work. (See 14-accessibility.)

**WCAG 3** — In working draft as of early 2026. Will likely incorporate APCA. Not yet a compliance standard. (See 14-accessibility.)

---

## Z

**Zeroheight** — Documentation platform that bidirectionally syncs with Figma. Common docs surface for designers; complements Storybook on the engineering side. (See 04-documentation, 12-figma-practice.)

---

*This glossary is incremental — add terms as new files introduce vocabulary. Don't define common DS terms; assume the reader.*

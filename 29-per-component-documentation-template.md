---
type: practice-area
title: Per-Component Documentation Template
description: The shape of a single component's documentation page — sectional spine, per-section depth, four-audience entry points, generation-vs-authoring seam, tooling decisions, anti-patterns, the version-zero schema the practice ships in week one.
tags: [extension, documentation, components, mdx, storybook, ai-json, mcp]
timestamp: 2026-06-14
---

# 29 — The Per-Component Documentation Template

> 04-documentation covers the strategy: docs as a parallel layer for humans and machines, the four-layer AI documentation stack, generated-from-data per Curtis Components-as-Data, the dedicated UX Designer role. This file is the *artefact* the strategy produces — the shape of a single component's documentation page. Without it, every engagement reinvents the IA, every component author makes their own choices about depth and order, and clients receive 60 pages with 60 slightly-different shapes. With it, every consumer learns the shape once and knows where to find what they need on every component thereafter. The template is an SOW deliverable; the version-zero schema below is what the practice should pull off the shelf in week one of the next engagement.

---

## 1. Why the per-component template is load-bearing

The template is the single artefact most likely to differentiate a *delivered* design system from a system that *survives*. The reason is operational, not pedagogical. Without a per-component template, every component-page author makes their own choices about what to include, in what order, with what depth. After 60 components a docs site has 60 slightly-different shapes. After the third consumer encounters a missing section on a third component, they stop relying on the docs site and either build wrong or build their own. Both are adoption failures and neither is recoverable post-handoff. The practice has named this gap in 09-gaps-and-open-questions §1.10 since the file was written, and it remains the most-likely-to-derail-quality-of-deliverable item on the list.

**Why the field defaults to "the IA emerges per component."** Consultancy engagements are time-boxed and component-driven; pages are typically written in the order components ship; whoever owns the first page sets the de facto template; subsequent authors copy-and-adapt. By the time anyone notices the inconsistency, ten components have shipped and retrofit is a 60-hour project no one scoped. A *prescriptive* template authored in week one, before the first component page is written, is the only way to avoid this. The template is a Discovery deliverable, not a Documentation deliverable — the discipline starts before content does.

**The authoring-cost / consumption-cost asymmetry.** Authoring a component page takes 3–8 hours per component, distributed by complexity (more for foundational primitives and form components; less for variants of established patterns; the range comes from converging two independent estimates with overlap in the middle). At 60 components that is a few hundred hours, paid once. Consumption is paid forever: every designer adopting the system, every engineer reaching for a component, every AI agent attempting code generation, every executive reviewing the dossier. The consumption cost dwarfs the authoring cost by orders of magnitude over a system's life. The template is the lever that lowers the consumption cost — every consumer learns the shape once, then knows where to find what they need on every component thereafter.

**The four-audience problem.** Component-page consumers split into four audiences with different access patterns:

- **Designers** scan for examples and do/don'ts; they want to see the component used correctly and incorrectly before they read any prose.
- **Developers** scan for the props table, the framework-specific code snippet, the Storybook story link.
- **AI agents** consume structured metadata — `.ai.json`, the schema embedded in MDX, description fields, the typed relationship graph — increasingly via the **Model Context Protocol** (MCP). Wolosin's research (Indeed, Jun 2025) reports that structured JSON via MCP is materially cheaper and more accurate than forcing an LLM to read unstructured Markdown — *(external)* cites this as up to 5× more efficient; we hold the figure as Wolosin-cited rather than asserting it as established.
- **Executives and auditors** consume the conformance dossier — accessibility evidence, version, deprecation status, adoption metrics where instrumented.

A template that surfaces each audience without forcing them to read the whole page is a four-axis problem. The shape that works in 2026 is **a stacked layout with strong anchor links and a per-page table of contents**, with a summary card at the top and the conformance dossier at the bottom. Designers and developers find their entry point in the summary card and live example; AI agents find their entry point in the structured metadata block; auditors find their entry point in the conformance dossier slot. The TOC handles the rest.

**The "trust the docs" cliff.** Trust is asymmetric: it takes weeks of consistent experience to build per consumer and minutes to lose. Once a consumer finds one wrong page — one out-of-date prop default, one component marked stable that's actually deprecated, one accessibility note that contradicts the live build — they stop trusting the entire site. The template is a contract that bounds where wrong-ness can live. If the props table is generated from the component data file, the props can never lie. If the accessibility section is `.ai.json`-derived and the schema is enforced in CI, the accessibility note can never lie about what the component does. The structural discipline is what makes single-source-of-truth generation tractable; without it, the source of truth fragments across the prose authors.

**The relationship to ACR / VPAT evidence.** Per 28-web-accessibility-implementation §8 and 14-accessibility, every component page is a per-component conformance dossier in microcosm. The consuming product's ACR aggregates per-component dossiers with application-level evidence; without the per-component dossier slot in the template, the consuming product's accessibility lead has to reverse-engineer it from the docs site. This is a real engagement-end cost the practice currently absorbs and could ship as a default deliverable instead. As GitHub Primer's accessibility annotations demonstrate, accessible components do not automatically guarantee accessible designs — the documentation must explicitly bridge the gap *(external)*. The template's accessibility section is what makes the bridge default.

**The brief is upstream of the docs page.** The template described in this file is the *output* — the artefact the practice ships to a client. The *input* is the per-component brief: the field-truth study that establishes what the component is, how the leading systems handle it, and what the practice's opinionated default is. The brief is the source the docs page authors draw from; the §15 schema embedded in the brief is the seed the engagement instantiates into its component data file (per 30). Without the brief, every engagement's docs page reinvents the field survey, the prop convergence analysis, and the accessibility decision tree from scratch. (See `components/index.md` for the catalogue.)

---

## 2. The template's sectional spine

The minimum viable set, in shipping order:

1. **Header** — name, brand-system version where the component was added or last meaningfully changed, status (stable / beta / deprecated), category (Foundations / Layout / Form / Navigation / Feedback / Data / Overlay).
2. **Summary card** — one-sentence purpose; primary use case; "see also" alternatives surfaced in the first paragraph rather than buried at the bottom.
3. **Live example** — the canonical configuration, interactive in Storybook, with a "view code" affordance. Examples-before-specs is the discipline.
4. **Purpose** — the intent layer; one or two paragraphs of declarative prose covering *what the component is for*.
5. **When to use** — the prescriptive layer; bulleted list of canonical use cases.
6. **When not to use** — the avoid-when layer; bulleted list with cross-links to the component-the-consumer-should-use-instead. The highest-leverage AI-consumer section.
7. **Anatomy** — labelled diagram of the component's structural parts, named to match the props vocabulary. Where slots exist, the slot semantics ("trigger," "content," "footer-action").
8. **Props / properties / API** — generated from the component data file. Sortable, searchable, with deprecation flags surfaced inline.
9. **States** — rest / hover / focus-visible / pressed / disabled / loading / error / empty / read-only as applicable. Per-state row with visible treatment, announced state, token transition, interaction model, and triggering condition.
10. **Variants** — visual variants (size, tone, density, emphasis) with the prop combinations that produce each. Distinct from states; variants are intentional design choices, states are runtime conditions.
11. **Examples** — multiple canonical configurations; one per typical use case; design-mode (Figma frame), live (Storybook), code-paste (MDX fenced block) per example.
12. **Do and don't** — side-by-side, paired by dimension, specific.
13. **Accessibility** — inline; not a separate page. Maps to the 17-accessibility-annotation-contract fields per concern.
14. **Content guidelines** — tone, error messages, empty-state copy, CTA labels. Per the UX Copywriter scope in 04-documentation.
15. **Composition and related components** — typed relationships (alternative to / composes with / supersedes / superseded by) rather than untyped "see also."
16. **Changelog** — per-component, semver-scoped, with deprecation announcements as first-class entries at the top.
17. **Conformance dossier** — automated test results, manual-AT walkthrough log links, contrast verification, SC-by-SC mapping for the WCAG 2.2 criteria the component participates in.

**Why the order.** The sequence is calibrated for how the four audiences actually move through the page. Designers find their entry point in the summary card and live example (positions 2–3) and rarely scroll past 12 (do/don't). Developers find their entry point in the props table and code examples (positions 8 and 11) and scroll up to 4–6 only when something is unclear. AI agents consume the entire page but rely on the structured metadata embedded in 4–7, 13, 15. Auditors enter at 17 (conformance dossier) and reference 13 (accessibility) for evidence detail. The order is opinionated and the practice should hold it.

**The order's exception: foundational primitives.** For tokens, layout primitives, and pure-utility components (a `VisuallyHidden` wrapper, a `Portal`, a generic `Box`/`Stack`/`Flex` as in Adobe Spectrum and Polaris), the props table *is* the answer to most questions and the prose layer is correspondingly thin. The template handles this via a **primitive variant** mode where the props table moves up to position 4, and sections 4–7 collapse to a one-paragraph purpose. The template still ships the slots; it acknowledges that for primitives the meaningful content lives in the props table.

### Component-type-specific extensions

Six component types have additional required slots; the template's metadata schema enforces them:

- **Form components** — validation logic, error-state messaging sequences, recovery flows; `aria-describedby` and `aria-errormessage` wiring; `:user-invalid` styling; autocomplete attribute mapping per WCAG 1.3.5 (see 28 §6).
- **Toast / snackbar / notification** — auto-dismiss timing, queue behaviour, `role="status"` vs. `role="alert"` decision, the per-toast accessible-name vs. body distinction.
- **Modal / dialog / drawer** — focus-trap and focus-return targets, `inert` scope, Escape behaviour, overlay-click behaviour, the relationship to `<dialog>` + `showModal()` (web) or platform-specific modal primitives (mobile). Z-index layering rules and scroll-lock mechanics where the surface escapes flow.
- **Tooltip and popover** — trigger model (hover / focus / click), persistence behaviour, dismissibility, the WCAG 1.4.13 contract.
- **Chart / data visualization** — encoding guidance (colour, position, size, shape, pattern), the colour-is-not-the-sole-carrier rule, axis and legend conventions, per-chart-type accessible name and description templates, sonification or table-fallback patterns. (This component type is itself a known practice gap per 09 §5.2 and is one of the genuine field-level absences.)
- **Composite / layout primitives** — slot semantics, composition rules ("a `Card` may contain at most one `CardHeader`, zero-or-more `CardBody`, and zero-or-one `CardFooter`"), the named relationships between the primitive and the components that compose with it.

Each extension is a *required slot* on the template for components of that type, not an optional add. Conditional rendering — driven by the component's typology field in the metadata schema — is what keeps the template from collapsing into generic-template-overfit (§7).

### Sections external sources name that the practice should consider

Worth weighing explicitly:

- **Architecture Decision Records (Mangialardi).** A typed list of "why X over Y" decisions — e.g., "we ship a `tone` prop rather than separate component variants because the brand changes faster than the structural shape." External argues for *linking* to an ADR repository to keep cognitive noise out of the consumption view; we argue this is engagement-shape-dependent: organisations with strong ADR culture inline a collapsed-by-default section, organisations without link out to a separate repo. The template carries the slot; the rendering decision is per-engagement *(both agents — held as a decision, not a default)*.
- **Version compatibility (Curtis).** A sub-table near the API specification ("This component requires `tokens@4.x` and `react@18+`"). Adopt as conditional; ship by default for portfolio engagements with multiple consumer products in flight; over-engineered for monorepo-pinned consumers *(external)*.
- **Anonymous user research notes.** Where the practice has the research, including it inline adds practitioner authority. Where the practice does not, the slot becomes embarrassing. Adopt only when the research exists.
- **Adoption metrics inline.** "Used by 14 surfaces; latest version adopted by 11; 3 surfaces on a deprecated prior major." Strong for systems with instrumented consumption; aspirational otherwise. Most engagements do not yet have token-usage telemetry — see 09 §1.24, which names this as an open practice gap. Adopt only when the instrumentation exists; otherwise the slot lies *(Claude — the honest framing)*.

### Sections that should be omitted by default

A short list of recurring noise:

- **Per-component "philosophy" sections** that recapitulate the system's overall principles. Move to system-wide pages.
- **Decorative changelog narratives** — "We made the button rounder, which feels more friendly." Either the changelog is structured per-version with semver and reasons, or it is removed.
- **Founder-letter framings.** No "From the Component Library Team:" intros.
- **Live performance dashboards inline.** Performance benchmarks belong on a system-wide observability page.
- **Marketing-tier preview imagery.** Hero shots that take 80% of the viewport do not help any of the four audiences.

---

## 3. Per-section depth — what each section actually contains

### Purpose, when-to-use, avoid-when

The intent layer carries more weight than any other prose section; it is the layer AI agents consume to choose between components, and the layer designers consume to decide whether to use the system at all.

**Purpose** is one or two paragraphs, declarative, *component-as-noun* in the topic sentence ("A button is an interactive control that triggers an action") followed by component-as-verb context ("Use a button when the user must take an action that progresses the primary task. Buttons emphasise commitment; links emphasise navigation."). Both framings matter — the noun framing anchors the type; the verb framing anchors the use *(both agents converge on the noun-and-verb framing)*.

**When to use** is a bulleted list of canonical use cases, typically 3–6 items. Each item is one line, prescriptive, and references a real surface or pattern when possible ("As the primary CTA on a form (e.g., Submit, Save, Continue)"). The discipline is specificity; "for actions" is too generic to be useful.

**When not to use** is the load-bearing section. Each item names the thing the consumer is tempted to use this component for, the reason to avoid it, and the component to use instead with a cross-link. *"Don't use a button for navigation between pages — use a link, which signals navigation rather than action and gets the right semantic on the web (`<a href>` rather than `<button>`)."* This pattern — temptation, reason, alternative — is the most-leverage rule the template can encode. Per Wolosin, AI agents with rich `avoid_when` data and cross-links to alternatives produce dramatically better component selection than agents working from `when_to_use` alone *(both agents)*.

**Every when-to-use must be paired with at least one avoid-when** *(external)*. The pairing forces the contract to be a binary logic gate for both human and AI consumers; without the pairing, the prescriptive layer is one-sided and the LLM has nothing to disambiguate against during component selection.

The avoid-when discipline carries through to `.ai.json` as the `avoid_when` array, with each entry a structured object: `{situation, reason, alternative}` where `alternative` is a typed reference to another component.

### Props / properties / API

Generated from the component data file in mature systems and hand-authored as a fallback. Either way, the most-consumed section by developers and the highest-stakes section for accuracy.

The discipline:

- **Per-prop row format.** Name, type signature, default, description, deprecation flag, version-introduced. The description field is one or two sentences, with examples for non-obvious props ("`tone` — controls the visual emphasis. `'default'` for typical use; `'brand'` for primary CTAs; `'critical'` for destructive actions"). The description is not just for human developers; it is scraped by AI coding assistants and is the primary semantic lever guiding the LLM during automated code generation. **Missing descriptions on API tables result directly in degraded AI outputs** *(external)* — making descriptions mandatory.
- **Type signatures shown verbatim from the source.** Generated; never hand-typed. Deviations between docs and source are the most-corrosive form of doc rot.
- **Defaults shown.** Both in the type signature and as a separate "Default" column.
- **Deprecation flag inline.** A `@deprecated` JSDoc comment on the prop produces a deprecation flag with the deprecation message and the prop-to-use-instead.
- **Required vs. optional split.** Standard sort puts required first, then optional, then deprecated.
- **Composition props split out.** Where a component takes a children slot, render-prop, or compound child, the section names the composition primitives separately rather than burying them in the props table. A `Tabs` component's API is *not* "the `Tabs` props"; it is "the `Tabs` props plus the `TabList`, `Tab`, `TabPanels`, `TabPanel` composition primitives." The template enforces the split.

The seam between "props the consumer sets" and "slots the consumer fills" is where most documentation falls down. Composition primitives need their own row format that names the slot, allowed children, required parent, and the slot's semantic role *(both agents)*.

### States

A standardised matrix covering the full spectrum of user interaction: rest, hover, focus, focus-visible, pressed/active, disabled, loading, error, empty, read-only. States that don't apply to the component type are *omitted*, not marked N/A — the metadata schema enforces "rest is always present; the rest are conditional on the component type."

The per-state row format *(external's framing is sharper; absorb it)*:

- **State name.**
- **Visual treatment** (a screenshot or Storybook story link).
- **Token transition** — the explicit token-to-token shift that produces the state ("`surface-brand-default → surface-brand-hover`"). This row is what aligns the docs with the actual token architecture rather than a hex-code change *(external)*.
- **Announced state** — what AT announces for this state (`aria-disabled="true"`, `aria-busy`, `aria-invalid`, `aria-current`).
- **Interaction model** — what the state allows (disabled does not receive focus; loading receives focus but ignores activation; error receives focus and AT announces the error message).
- **Triggering condition** — what causes the state (user input, prop change, async resolution).

The visible-vs-announced distinction is what the template makes explicit. Many existing systems collapse the two and ship wrong AT behaviour; the template forces the per-state announcement explicit.

### Examples

**Examples-before-specs** is the discipline *(both agents; consistent across high-quality public exemplars — Atlassian, Spectrum, Carbon)*. Consumers scan the live example first to confirm the component is what they think; they read prose only when the example is unclear.

The canonical example set per component-type:

- **Buttons, links, badges, tags** — one example per tone × emphasis combination; one with an icon adornment; one in disabled and loading state.
- **Form fields** — empty / filled / focused / error / disabled / loading / read-only; one with help text; one with autocomplete; one in a multi-field group with `<fieldset>`.
- **Cards** — minimal; with media; with action; with multiple actions; in a grid (composition).
- **Tables / data grids** — minimal data; sortable; with selection; with row-level actions; with pagination; with empty state.
- **Modals / dialogs** — confirm; form; informational; multi-step.
- **Toasts / notifications** — success; error; with action; queue behaviour.
- **Tooltips / popovers** — hover; focus; with rich content; on a disabled trigger.

The pattern: 4–8 examples per component, each demonstrating one specific axis the consumer might vary. More than 8 becomes an example dump; fewer than 4 leaves out canonical configurations.

**Per-example slots.** Each example carries a one-sentence caption explaining what the example demonstrates ("With an icon adornment — when the action benefits from a visual cue alongside the label"), a live render in Storybook, a code-paste fenced block, and a Figma frame link.

**Real data, not Lorem Ipsum** *(external — load-bearing rule)*. Default examples represent realistic payloads — actual product names, plausible user names, real-shape error messages. Lorem Ipsum hides truncation, wrapping, and overflow bugs that real strings expose. The template's example-authoring guidelines require realistic content.

**The Figma frame link** is the under-shipped slot in most existing systems — most link to the design library at the *system* level, not per-component-example level. Authoring the link is a 2-minute task per example; over 60 components × 6 examples it is ~12 hours of authoring that pays back permanently in designer-flow *(Claude)*.

### Do and don't

Side-by-side, paired by dimension, specific. The discipline:

- **Each "do" is paired with a "don't" on the same dimension.** "Do use 'Save' for the primary action when the action persists changes." paired with "Don't use 'Submit' when the action is not a form submission." The pair is what makes the row useful; a one-sided "do" is a tip, not a contract.
- **Specific over generic.** "Do use clear language" is noise. "Do label destructive actions with the consequence ('Delete account' rather than 'Delete')" is a rule.
- **Visual where possible.** A do/don't pair with screenshots of the actual usage costs more to produce and pays back proportionally — designers absorb visual examples 4–10× faster than prose. Each pair is marked with a green check (do) and a red cross (don't), leaving zero ambiguity *(external)*.
- **One pair per dimension; no multi-rule pairs.** A do that says three things and a don't that says four becomes a paragraph; the side-by-side discipline collapses.

The most common authoring failure is generic do/don'ts that could appear on any component page. The template's audit pass for do/don't asks: *if this pair were copy-pasted onto another component page, would it still make sense?* If yes, it is too generic; rewrite for specificity.

### Accessibility

Inline, mapping to the 17-accessibility-annotation-contract fields per concern. The accessibility section is *not* a free-form prose block — it is a structured table that produces both the human-readable docs and the `.ai.json` accessibility schema from the same source.

Per-row format:

- **Concern** — name mechanism, role, state, value, focus, ARIA relationships, focus-return, forced-colors survival, motion treatment, gesture alternative, live-region intent, APG keyboard model — the 17 concerns from the contract.
- **What the component does by default** — "Renders `<button>` so the role is automatic; the visible text is the accessible name."
- **What the consumer must specify** — "If the button is icon-only, the consumer provides `aria-label`; the system warns at the type level if a non-text-content button has neither a visible label nor `aria-label`."
- **AT-by-AT verification status** — "Verified on NVDA 2026.1 + Chrome, JAWS 2026 + Chrome, VoiceOver + Safari macOS, VoiceOver + Safari iOS, TalkBack + Chrome (Android). Last verified 2026-06-12." (The matrix per 28 §8.)
- **WCAG SC mapping** — the success criteria the component participates in (e.g., 1.4.4 Resize Text, 2.4.7 Focus Visible, 2.5.8 Target Size Minimum). The conformance dossier (slot 17) consumes this for ACR aggregation.

This is the section that closes the gap between "the design system documents accessibility" and "the consuming product's ACR has per-component evidence." Without this section's structural discipline, the dossier is a bespoke per-engagement artefact every time.

### Content guidelines

The seam with 04-documentation's UX Copywriter role. Per-component:

- **Tone for default copy.** Buttons say "Save," not "Submit changes" except in specific cases.
- **Error messages.** Patterns and templates ("[Field] [requirement that wasn't met]." → "Email must include an @ symbol.").
- **Empty-state copy.** "No results yet" rather than "Nothing here." Hierarchy: state, why, what the user can do.
- **CTA labels.** Verbs first, action-noun where the action's object is implicit ("Save changes" rather than "Save"; "Add member" rather than "Add").
- **Language for help text and tooltips** — declarative, second person, present tense.

The section is short on most components and substantive on form components, modals, and toasts. The audit pass asks: *if a copywriter on the consuming product team needed to localise this component's copy, would they have what they need?*

### Composition and related components

Typed relationships, not untyped "see also" *(both agents)*:

- **Alternative to** — components the consumer might confuse with this one. AI agents use this for disambiguation during component selection.
- **Composes with** — components that fit inside or around this one (`Card` composes with `CardHeader`, `CardBody`, `CardFooter`).
- **Composes within** — the inverse (`CardBody` composes within `Card`).
- **Supersedes** — components this one replaces.
- **Superseded by** — for deprecated components only. The "use this instead" pointer.

The graph layer is where the design system goes from "a list of components" to "a coherent vocabulary." Untyped "see also" loses the relationship semantics; AI agents in particular use the typed graph for recommendations.

### Changelog

Per-component, semver-scoped, structured. Per-version row: version, date, type (added / changed / deprecated / removed / fixed / security), description, migration link for breaking changes.

**Deprecation announcements at the top** *(external — sharp framing worth absorbing)*. They must not be buried in chronological order; they live at the top of the section and are highlighted before any adoption takes place. The deprecation also appears as a banner on the component page and as a flag on the prop or component itself.

The system-wide changelog is the aggregation; the per-component changelog is the per-consumer truth. Per-component capture is critical for patch-level changes that don't warrant a major system release broadcast but heavily affect downstream visual regression tests *(external)*.

---

## 4. The four-audience problem — what each audience needs

**Designers** — entry points: summary card, live example, do/don't.

- They confirm the component is the right tool by scanning the live example.
- They scan do/don't to understand the contract.
- They reach for the Figma frame link in the examples to pull the component into their working file.
- They occasionally reach for content guidelines and accessibility notes when reviewing a senior engineer's PR.
- They very rarely read the props table or the changelog.

The template optimises for designers via the early summary card and live example, plus the Figma frame link in every example as the seam.

**Developers** — entry points: props table, code-paste examples, Storybook story.

- They reach for the props table to find the prop they need.
- They copy a code example into their PR as the starting point.
- They reach for the Storybook story when they need to see edge-case behaviour.
- They consume the changelog when they need to reason about migration.
- They consume accessibility notes when reviewing their own PR before submission.

The template optimises for developers via the generated-from-data props table, framework-specific code snippets, the per-example "view code" affordance, and a sticky table of contents for rapid jumping past intent prose to API.

**AI agents** — entry point: structured metadata.

- They consume the entire page but their decisions hinge on the structured metadata block.
- The `.ai.json` schema embedded in MDX (or sidecar to it) is what the agent uses for component selection, increasingly via MCP.
- The `when_to_use` and `avoid_when` arrays are the highest-leverage sections.
- The accessibility schema fields are what the agent uses to generate ARIA, focus management, and forced-colors handling.
- The composition graph is what the agent uses to assemble components into patterns.

The template optimises for AI agents via the embedded `.ai.json` block, the structured accessibility table (which produces the `accessibility` schema field), and the typed composition graph (which produces the `relatedComponents` schema field). Concrete agents consuming this surface in mid-2026 include GitHub Copilot, Cursor, and Claude *(external)* — and the practice should design for the protocol (MCP) rather than any one client.

**Executives and auditors** — entry point: conformance dossier.

- They reach for the dossier to verify the component's accessibility evidence per WCAG SC.
- They reach for the version field to verify the component is current.
- They reach for the deprecation status to verify the component is supported.
- They occasionally reach for the changelog when scoping migration timelines.
- They rarely read the prose layer.

Where the system is properly instrumented, the dossier can pull dynamic adoption metrics (e.g., "Used by 14 surfaces; 11 on the latest version; 3 on a deprecated prior major"), giving immediate ROI visibility. Most engagements do not yet have token-usage telemetry to support this — see 09 §1.24, which names production-token-telemetry as an open practice gap. **Where the instrumentation does not exist, the slot is omitted rather than filled with fictional metrics.** Adoption-metrics-inline is conditional on instrumentation existing.

### The four-audience entry-point pattern

To serve all four audiences without forcing any one of them to read the whole page:

- **A summary table at the page apex** with version, accessibility status, framework availability, deprecation status — auditors scan this in seconds *(external)*.
- **A sticky table of contents** with anchors per slot — developers jump to API; designers jump to examples and do/don't *(external)*.
- **An audience-toggle on the TOC** (designer / developer / AI / auditor) that highlights the sections most relevant to the selected audience and dims the others — content stays accessible but the entry-point hierarchy is preserved per audience. This is the pattern that scales without fragmenting the page into four duplicated views *(Claude)*.

Implementation in 2026: Storybook's component-page architecture supports the TOC and anchors natively; the audience toggle is implementable in MDX via component meta-fields. In Zeroheight it is implemented via tagged sections and audience filters. In Knapsack it is built into the Code Connect rendering layer.

---

## 5. Generation, authoring, and the seam between them

The template's economic argument is that the generation seam is what makes it sustainable at scale. Per Curtis (*Components as Data*, Sep 2025) and 04-documentation's stance, mature systems treat the component data file as the source of truth and generate as much of the documentation as possible. The template names the seam explicitly.

### Generated sections

- **Props / properties / API** — generated from TypeScript types or framework-specific definitions. Storybook 9's auto-generated docs page is the baseline; Zeroheight's React Connect is the equivalent for hosted docs. *(Storybook 8 plus the 9.x line, with RSC support and SWC-based docgen, is the current technical stack as of mid-2026 — exact dates of the 9 release vary in citation; both agents reference the architecture without contesting it.)*
- **Default examples** — every prop produces a default via Storybook's controls; the canonical "minimal example" is a generated configuration.
- **Type signatures** — verbatim from the source.
- **Default values** — verbatim from the source.
- **Deprecation flags** — from `@deprecated` JSDoc on the prop.
- **Version-introduced metadata** — from a `since` JSDoc tag on the prop or component.
- **The Storybook story link** for each example — auto-generated from the story tree.

### Hand-authored sections

- **Purpose** — the intent layer; cannot be generated.
- **When to use / when not to use** — prescriptive prose; cannot be generated, though AI assistance during authoring is plausible (the generator suggests draft `avoid_when` entries based on adjacent components' usage).
- **Anatomy diagram** — design-tool-authored; the SVG or image asset, paired with labels matching the props vocabulary.
- **Do / don't** — pairs are authored; the discipline is specificity, which generation does not produce.
- **Content guidelines** — authored by the UX Copywriter.
- **Architecture decision records** — when included; authored once and rarely revisited.
- **Example captions** (one-sentence "what does this demonstrate") — authored.
- **Accessibility section's "what the component does by default" and "what the consumer must specify" rows** — authored, then validated against the implementation in CI.

### Generated-with-authoring-overlays

- **States** — the default state set is generated from the component data file's state declaration; per-state announced-state, token-transition, and interaction-model rows are authored, with the schema validating that every declared state has all rows filled.
- **Variants** — the default variant set is generated from the prop combinations; the visual treatment screenshot is authored or auto-captured.
- **Examples** — the canonical minimal example is generated; the additional examples per component-type are authored.
- **Changelog** — generated from commit history with `@semantic-release` or equivalent, with authored prose for breaking changes.
- **Conformance dossier** — automated test results generated from CI; manual-AT walkthrough log links authored; SC-by-SC mapping authored once and validated against test coverage.

### The CI freshness check

Per 04 §3 and the AI-Compatible Doc Ch. 7 pattern: the build fails if the component code changes but the docs do not. The conceptual ancestor is the dbt source-freshness pattern from data engineering — continuously monitor the delta between the component's code state and the documentation metadata, and fail the build when they drift *(external — the dbt analogue is sharp framing)*.

The mechanism:

- A pre-commit hook computes a hash of the component's authored doc fields (purpose, when-to-use, avoid-when, content guidelines, accessibility "what the consumer must specify" rows).
- The hash is stored alongside the component's source.
- On any change to the source, the hash is recomputed; if the hash matches the stored value, the docs were not updated and the commit fails with "Component changed; documentation hash unchanged. Update the docs or explicitly mark this change as documentation-irrelevant."
- The "explicitly mark" affordance is a `// docs: irrelevant` comment that the hook recognises; this prevents the hook from blocking trivial refactors.

The freshness check is the single highest-leverage piece of CI documentation infrastructure the practice can ship. It costs ~4 hours to implement per system and prevents the "60 pages, 12 of them out of date" failure mode permanently.

A second CI rule worth shipping: **per-section minimum-prose lengths**. The schema enforces minimum content per section (Purpose 50–500 words; When to use 3–8 bullets; Avoid-when 2–6 bullets with linked alternatives; etc.). Sections under the minimum fail the build with a specific error. This is the pickiest of the CI rules; it prevents the most common failure mode in shipping consultancy deliverables — every section heading present, the content under each heading a one-line placeholder *(Claude)*.

### The single-source-of-truth model

In a mature system, the component data file is the source. Each consumer of the docs (Storybook, MDX docs site, `.ai.json` registry, Figma library, the internal AI assistant's component catalog) derives from the source. The shape:

```
component-source/
├── Button.tsx                  // implementation
├── Button.types.ts             // types (consumed by docs and .ai.json)
├── Button.stories.tsx          // Storybook stories
├── Button.docs.mdx             // authored prose
├── Button.tokens.ts            // design tokens consumed
├── Button.ai.json              // AI metadata (generated + authored)
├── Button.a11y.json            // accessibility schema (generated + authored)
└── Button.test.tsx             // automated tests (feeds dossier)
```

The docs site, the `.ai.json` registry, and the per-component conformance dossier all derive from this set. A change to `Button.types.ts` triggers the freshness check on `Button.docs.mdx`; a change to `Button.test.tsx` updates the conformance dossier; a change to `Button.tokens.ts` updates the `.ai.json` `tokens` field automatically.

### Where authoring tooling falls short in 2026

- **Generated-from-data documentation is still not the default in most consultancy deliverables.** The architecture exists; the tooling exists; the practice does not yet ship it as a default. This is the gap between 04-documentation's stated direction and the commercial proposal's actual deliverables.
- **MDX 3 + Storybook 9 is the closest mature stack for a code-side docs site.** The remaining seam: design-side consumption (Figma library, Zeroheight) does not yet pull from the same source automatically; the design library is rebuilt from the data file on a separate cadence, which produces drift.
- **Complex multi-variable interactive states** (e.g., a datatable cell that is simultaneously selected, focused, and in a server-validation error state) often require manual scripting to render accurately in automated documentation. The practice generates base states algorithmically and hand-authors visual examples for the highly complex multi-variable edge cases *(external)*.
- **`.ai.json` is not yet a standard.** The schema is internal-tier IP for the practice; external sources (Wolosin, the AI-Compatible Doc) name it conceptually but no canonical schema has emerged in the field. The practice can ship its schema as a public artefact and claim the layer.
- **Zeroheight's API for generated content** has matured significantly through 2025–2026 but remains the design-side equivalent of "Storybook autodocs from 2022" — usable, opinionated, and constraining. For systems using Zeroheight, the practice's discipline is to use Zeroheight for the design-consumer surface and treat code-side docs (Storybook + MDX) as the authoritative source.
- **The Figma frame link per example** is the under-shipped slot. Authoring it is a 2-minute task per example that pays back permanently in designer-flow.

### The per-component template's relationship to system-wide IA

The per-component page lives at the leaves of a navigation tree:

```
Home
├── Getting started
├── Foundations (Color / Typography / Space / Motion)
├── Layout (Grid / Stack / Box)
├── Components
│   ├── Form (Button / TextField / ...)
│   ├── Navigation
│   ├── Feedback
│   ├── Data
│   ├── Overlay
│   └── ...
├── Patterns
├── Accessibility
└── Changelog
```

Search is the first-class navigation primitive at scale (per Couldwell and consistent across high-quality exemplars); category landing pages are second-class. The semantic tagging required by the template — categories, typed relationships, deprecation status — directly powers the global search mechanics; a search for "validation" can index Form layout components *and* the do/don't guidelines of the Text Input page that reference validation patterns, creating a coherent exploratory experience *(external — the search-tagging implication is worth absorbing)*.

The per-component template's job is to be findable from search, navigable from category, and readable per audience-entry-point. The system-wide IA's job is to compose category landing pages and the patterns layer; that is a separate template the practice should also encode but is out of this file's scope.

---

## 6. Tooling decisions and recommendations

### The default stack

For engineering-heavy systems with code-resident developers, **Storybook + MDX is the default**. The reasoning:

- Storybook's component-page architecture (8 with the 9.x line as the current major) ships built-in support for autodocs, addon-a11y, and the controls panel as a first-class authoring surface. RSC support and SWC-based docgen mean API tables are generated from TypeScript interfaces with minimal overhead *(external)*.
- MDX 3 supports the structured-frontmatter pattern that lets the per-component template's metadata schema live alongside prose.
- The CI integration (Chromatic for visual regression, axe-core via `@storybook/addon-a11y` for runtime accessibility, Storybook Test Runner for behaviour) is the most-mature stack for component-level CI in 2026.
- The cost is portability — the docs site is tightly coupled to Storybook's renderer. Migration to a different platform requires rewriting MDX-with-Storybook-component-imports, which is non-trivial.
- The cost is also authoring ergonomics for non-engineers. UX Designers and UX Copywriters often find MDX syntax, the local development environment, and the Git-based workflow hostile *(external)*. Without dedicated Design Systems Engineering support to bridge the gap, Storybook documentation devolves into raw, auto-generated API dumps without the hand-authored intent layer.

### Hosted alternatives

| Platform | Use case | Strengths | Trade-offs |
|---|---|---|---|
| **Zeroheight (4.x)** | Designer-heavy organisations; Figma as primary source of truth | Polished designer-led documentation; deeply integrated MCP features (LLMs read the styleguide via custom connectors); democratised CMS-style authoring | Struggles with complex automated code-generation pipelines compared to developer-centric tools |
| **Supernova (2026)** | Multi-brand ecosystems with complex token matrices | Deep structural customisation; powerful data-model engine; one component template can map dynamically to multiple distinct brand themes | Less mature Figma sync as of mid-2026 |
| **Knapsack (mid-2026)** | Enterprise-tier; multi-platform; ACR aggregation | Live-code integration — renders actual production components rather than static representations or isolated Storybook iframes; aligns with components-as-data; mathematically prevents component drift | Premium pricing; only justified for portfolio engagements past a threshold |
| **GitBook** | Legacy systems migrating off Notion / Confluence | Easy authoring, low setup | Yellow flag for systems with > 30 components; migration to Storybook + MDX is one of the more-frequent technical-debt items in the practice's portfolio |

### Self-hosted vs. SaaS

Self-hosted (Storybook deployed to internal infra; static MDX site behind a corporate VPN; on-prem Penpot for design library) is required for:

- Regulated clients (healthcare, finance, government) where component metadata must not leave the network.
- EAA-procurement clients where vendor lock-in is a procurement-tier concern.
- Clients with internal AI tools that need to query the design system from within the network without external API calls.

SaaS (Zeroheight hosted; Supernova hosted; Storybook deployed to Vercel) is the default for:

- Most agency-to-client engagements where the design system is shared with the consuming product team via the agency's docs platform.
- Engagements where the time-to-deploy of a hosted platform is worth the trade-off in portability.

The practice's discipline: **assume self-hosted is required until the client explicitly waives it.** Many clients will, but the conversation is procurement-grade and worth scoping deliberately.

### The decision framework

A client picks a docs platform based on five questions:

1. **Codebase culture.** Developers live in the codebase, system ships as code → Storybook + MDX. System is design-led with engineers as occasional consumers → hosted.
2. **Designer-engineer ratio.** > 2:1 designer-heavy → hosted. Roughly even → Storybook + MDX with hosted secondary surface. > 1:2 engineer-heavy → Storybook + MDX as primary, hosted optional.
3. **Budget tier.** Storybook + MDX is free; Zeroheight ~$5–15K/year for an org-tier subscription; Supernova comparable; Knapsack $30K+/year for enterprise. The free option is the best option for systems with < 4 consuming product teams.
4. **Regulatory constraint.** EAA, HIPAA, PCI, government → self-hosted, with the implication that the docs platform is part of the engagement's infrastructure scope, not an afterthought.
5. **Scale of consumer base.** < 5 consumer surfaces → either is fine. 5–20 surfaces → hosted with code-side mirror or vice versa. 20+ surfaces → enterprise tier (Knapsack) or self-hosted with custom tooling.

### Where the system can be portable

The component data file (per §5) is the portable layer. Each docs platform consumes the data file; each platform produces the docs site. A system that authors `Button.docs.mdx` with Storybook component imports is *not* portable; a system that authors `Button.metadata.json` plus `Button.docs.md` with no platform-specific dependencies is. **Separate the authoring source from the rendering platform** — the authoring source lives in the component repo, version-controlled, platform-neutral; the rendering platform is replaceable.

This is the single most important architectural decision in the docs strategy and is under-articulated in most existing engagements. The template's structural discipline is what makes the separation tractable.

---

## 7. Anti-patterns and failure modes

The recurring patterns the practice should explicitly avoid; each maps to a recoverable engagement scope item.

**Generic-template overfit.** Every component page has the same template, even when the template doesn't fit. A primitive `VisuallyHidden` wrapper has a 17-section page where 13 sections say "N/A." Consumers learn the template is performative rather than informative. The fix: the metadata schema declares per-section conditions (`appliesTo: ["interactive"]`, `appliesTo: ["form"]`, `appliesTo: ["composite"]`). Sections that don't apply to the component-type are *omitted*, not marked N/A. The "primitive variant" mode (per §2) is the codified version.

**Documentation-as-changelog.** The page is mostly history; the current usage is buried under "What's new in v3.4." The fix: changelog at slot 16, after the prescriptive layer. The header carries version-introduced and last-changed metadata as a compact summary; the full changelog is at the bottom. Consumers who want history can find it; consumers who want current usage are not blocked by it.

**Implicit-context prose.** Written for the original team; references shared abbreviations, internal Slack threads, "the original Figma file" without a link. Fails for new consumers and for AI agents that consume the page literally. The fix: every prose section is read by a consumer-not-on-the-team before merge. Every cross-reference is a link, every abbreviation is expanded on first use, every "as we discussed" is replaced with "see [linked source]." This is editorial review, not authoring.

**Zero-example pages.** Lots of prose, no live or pasteable examples. Designers and engineers leave; AI agents have nothing to anchor on. Faced with this, consumers resort to inspecting the production DOM to reverse-engineer the component *(external)*. The fix: the template enforces a minimum of one live example at slot 3 and one code-paste fenced block per example. The build fails if either is missing.

**Stale documentation.** 60 pages, 12 of them out of date. Trust collapses. The fix: the CI freshness check (per §5). Cost: ~4 hours per system. Pays back permanently.

**Tooling without authors.** Zeroheight subscription, no UX Designer hours scoped to fill it. Empty rooms with brand colours. The fix: the practice's commercial scope ties the docs platform to the UX Designer hours. The proposal cannot scope a docs platform without scoping the authoring labour. The proposal cannot scope authoring labour without scoping the platform.

**Six weeks of tooling, one week of content.** Per 04-documentation's failure-modes section. The team picks Zeroheight vs. Supernova vs. Knapsack for six weeks; spends one week writing the first three component pages; ships an empty platform. The fix: the platform decision is a Discovery deliverable, not a Documentation deliverable. The decision is made in week 1 against the framework in §6; authoring begins in week 2. The platform decision takes 2 hours, not 6 weeks.

**Accessibility as a separate page.** The visit pattern misses it. A consumer who doesn't visit the `/accessibility` page assumes accessibility is "handled" without knowing what is or isn't documented. The fix: accessibility inline at slot 13 of every component page; the system-wide accessibility page is the architecture and conformance reporting overview, not the per-component contract.

**Empty rooms.** Every section heading is present; the content under each heading is a one-line placeholder. Consumers see structure and conclude there is content; there isn't. The fix: per-section minimum-prose lengths enforced in CI (per §5).

**Dynamic adoption metrics that lie.** Telemetry-flavoured prose ("Used by 14 surfaces") shipped for systems without instrumentation produces fictional metrics that consumers and executives will eventually verify and lose trust over. The fix: adoption-metrics-inline is conditional on instrumentation existing. Where it doesn't, the slot is omitted, not filled. (See 09 §1.24 for the underlying telemetry gap.)

---

## 8. The practice's POV — what we ship, why, and the commercial framing

The template is a **default Documentation deliverable scoped in the SOW alongside the dedicated UX Designer role.** It is shipped as version 1.0 in week 1 of every engagement, populated through the engagement, and handed off as part of the system-wide deliverable.

### The version-zero shape — what we ship in week one

The actual template, ready to use, that an engagement pulls off the shelf:

```yaml
# component-template.yaml
sections:
  - id: header
    required: true
    fields: [name, version, status, category]

  - id: summary
    required: true
    minWords: 30
    maxWords: 80

  - id: liveExample
    required: true
    source: storybook
    captionRequired: true

  - id: purpose
    required: true
    minWords: 50
    maxWords: 500

  - id: whenToUse
    required: true
    minBullets: 3
    maxBullets: 8

  - id: avoidWhen
    required: true
    minBullets: 2
    maxBullets: 6
    schema:
      situation: string
      reason: string
      alternative: componentRef

  - id: anatomy
    required: true
    type: diagram
    labelMatchesProps: true

  - id: api
    required: true
    generated: true
    source: typescript

  - id: states
    required: conditional
    appliesTo: [interactive]
    perStateRows: [name, visual, tokenTransition, announced, interaction, trigger]

  - id: variants
    required: conditional
    appliesTo: [hasVisualVariants]
    generatedFromPropCombinations: true

  - id: examples
    required: true
    minExamples: 4
    maxExamples: 8
    perExampleSlots: [caption, live, code, figmaFrame]
    realData: true

  - id: doDont
    required: true
    minPairs: 2
    maxPairs: 8
    pairedByDimension: true
    visualMarking: [check, cross]

  - id: accessibility
    required: true
    schema: a11yContract
    perConcernRows: [concern, default, consumerSpecifies, atVerification, wcagSc]

  - id: contentGuidelines
    required: conditional
    appliesTo: [hasUserCopy]

  - id: relatedComponents
    required: true
    typedRelationships: [alternativeTo, composesWith, supersedes, supersededBy]

  - id: changelog
    required: true
    generated: true
    source: gitHistory
    semverScope: systemWide
    deprecationsAtTop: true

  - id: conformanceDossier
    required: true
    generatedSections: [automatedTests, contrast, scMapping]
    authoredSections: [manualWalkthroughs]

ciRules:
  - id: freshnessCheck
    description: Component code change without doc update fails build
    enabled: true

  - id: minProseLengths
    enabled: true

  - id: liveExampleMandatory
    enabled: true

  - id: figmaFrameLinkMandatory
    enabled: true
    appliesTo: [interactive, layout]

  - id: avoidWhenMandatory
    description: Every whenToUse must pair with at least one avoidWhen
    enabled: true
```

This is the template the practice ships in week 1. The engagement populates it; the client team inherits it. It is the version-zero artefact that closes 09 §1.10 and gives the practice a default Documentation deliverable to scope, defend, and improve over time.

### The commercial scoping unit

"Per-component-page authoring hours × component count × the UX Designer + UX Copywriter mix."

A typical breakdown for a 60-component system:

- **UX Designer authored sections** (purpose, when-to-use, avoid-when, anatomy, do/don't, accessibility "what the consumer must specify," content guidelines for components without separate copywriter scope, design rationale where included): **3–8 hours per component**, distributed by complexity. Primitives (icon, divider) at the low end; form components, modals, and data-grid at the high end. For a 60-component system this is ~180–480 hours of UX Designer time *(the range comes from converging two independent estimates with overlap in the middle; both ends are defensible)*.
- **UX Copywriter authored sections** (where the copywriter is a discrete role per CareCentrix-tier engagements): **0–2 hours per component**, with the distribution sharply skewed — pure-utility components have zero copywriter scope; form components, modals, and toasts have the most. Average: ~1 hour × 60 components = ~60 hours.
- **Engineering authored sections** (component data file definitions, types, examples, the CI freshness check setup, the conformance dossier integration): typically scoped under engineering hours rather than documentation hours; ~2 hours per component for the data file authoring. Average: ~120 hours.
- **Editorial review pass** (the read-by-consumer-not-on-team audit per anti-pattern "implicit context"): ~0.5 hours per component. Average: ~30 hours.
- **Template authoring at engagement start** (custom adaptation per client; the practice's template adjusted for the client's component vocabulary, brand voice, and tooling stack): ~16–40 hours.

Total documentation labour for 60 components: **~270–610 hours of UX Designer / UX Copywriter time, plus ~120 hours of engineering data-file authoring, plus the template-customisation cost.** The range is wide because component complexity varies and the labour-mix between UX Designer and UX Copywriter is engagement-shape-dependent. **Itemising the cost makes it defensible** — clients understand "60 components × per-complexity-bracket hours" better than "documentation pass" as a lump-sum line item. The practice's discipline is to scope documentation as an itemised unit, not a buffer.

### Defensible POV claims

The differentiators no external source articulates as a complete package in mid-2026:

1. **The template itself, with the 17-section spine.** External exemplars (Atlassian, Spectrum, Carbon, Polaris) each have their own template; none is published as a deliverable. The practice can publish ours as practice IP.
2. **The four-audience framing** (designer / developer / AI / auditor). External sources name three; the AI-as-first-class-consumer audience is current to 2024+ and the auditor-as-first-class is current to the 2025 EAA enforcement.
3. **The components-as-data substrate as the authoring source.** Curtis articulates the architecture; the practice can articulate the *engagement-scoped commercial deliverable* — the data file plus CI freshness check that the client team can run after handoff.
4. **The accessibility annotation contract as `.ai.json` fields.** Per 17 and 28; the practice can claim this as the seam between design-time annotation, AI-time consumption, and audit-time evidence aggregation.
5. **The conformance dossier slot.** The per-component dossier is the missing piece in most existing systems' ACR pipelines; the practice can ship it as a default and claim the layer.
6. **MCP-readiness as a default.** Per Wolosin (Indeed, Jun 2025), structured JSON via MCP is materially cheaper and more accurate than unstructured Markdown for AI consumption — Wolosin reports up to 5× efficiency improvement *(external — held as Wolosin-cited, not asserted)*. The practice's `.ai.json` schema, served via MCP, is the AI-consumer-ready surface.

### Where the template positions the practice against tooling vendors

Zeroheight, Supernova, and Knapsack ship templates. The practice's value is *not* the template alone — the practice's value is:

1. **The editorial discipline** that makes the template's content load-bearing rather than performative.
2. **The components-as-data architecture** that makes the template's prescriptive structure tractable at scale.
3. **The accessibility annotation contract** that makes the template's accessibility section closer to ACR-grade evidence than tooling-vendor accessibility blocks.
4. **The CI freshness check and per-section minimum-prose rules** that make the template enforce its own quality.

The vendor's value is the rendering and hosting layer. The practice's value is the editorial and architectural layer. Both are necessary; neither replaces the other. Engagements that buy a vendor template without the editorial discipline ship empty rooms; engagements that author with editorial discipline against a generic template ship strong content with weak structure. The practice's offer is both layers.

---

## See also

For the documentation strategy this template operationalises — the four-layer AI documentation stack, the human-plus-machine parallel layer, generated-from-data — see 04-documentation. For the *commercial-default angle* of this template — the engineering investment, the per-component hours redistribution, the migration playbook, the 5-question decision tree for when generation is justified, the phased-adoption pitch, the cluster relationship to AI-readiness — see 30-generated-from-data-documentation.

For the components-as-data substrate that underwrites the generation seam, see 03-component-library and 15-ai-in-ds.

For the accessibility annotation contract that the template's accessibility section implements, see 17-accessibility-annotation-contract. For the implementation depth underneath that contract, see 16-mobile-accessibility-implementation and 28-web-accessibility-implementation.

For the semver discipline the changelog section assumes at scale, see 24-tokens-at-scale.

For the practice gaps this file partially closes — the per-component template gap (§1.10), the engineering-onboarding-artefact gap (§1.7), AI-readiness as commercial default (§1.12) — see 09-gaps-and-open-questions.

---

## Provenance

Synthesis of the dual-agent research run filed 2026-06-13 (`_research/_inbound/2026-06-13-per-component-doc-template/`). Both agents converged substantively: the template's load-bearing role, the four-audience problem, the purpose-first-props-last discipline (with the foundational-primitives exception), avoid-when as the highest-leverage AI-consumer signal, examples-before-specs, do/don't paired by dimension, accessibility inline rather than on a global page, typed relationships over untyped "see also," per-component changelog plus system-wide, the generated-vs-authored seam with technical facts generated and intent authored, the CI freshness check, the single-source-of-truth model, Storybook + MDX as the engineering default with hosted alternatives (Zeroheight, Supernova, Knapsack), the same anti-patterns, and the commercial framing as a default SOW deliverable. Where they diverged, the synthesis applied judgement: external's MCP-named protocol framing and Wolosin's 5× efficiency claim are absorbed (held as Wolosin-cited, not asserted); external's token-transition row in States is the sharper format; external's "real data, not Lorem Ipsum" rule and the green-check / red-cross visual marking discipline for do/don't pairs are absorbed; external's deprecations-at-top-of-changelog framing is absorbed; external's dbt-source-freshness-as-conceptual-ancestor for the CI pattern is absorbed; the inline-vs-linked ADR question is held as a decision rather than a default (per the convergence/divergence read); the per-component hours range is held as 3–8 hours per UX Designer per component (overlapping the two independent estimates) rather than a single point; Storybook 9 release dating is softened to "the 8 plus 9.x line as the current major as of mid-2026" since neither agent has authoritative version-release-date verification; adoption-metrics-inline is held as conditional on instrumentation existing (Claude's framing) with 09 §1.24 named as the underlying gap; the 17-section spine and the version-zero YAML schema (Claude) are kept as the practice's prescriptive deliverable. Closes 09-gaps-and-open-questions §1.10 (per-component template), partially closes §1.7 (engineering-onboarding-artefact via the conformance dossier slot), partially closes §1.12 (AI-readiness as commercial default via the `.ai.json` and MCP-ready surface), and partially closes §1.4 / §1.6 / §1.10 in 04-documentation's own gaps inventory.

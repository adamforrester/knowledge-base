# The per-component documentation template — Claude run

> Research output, June 2026. Companion to the planned external-agent run on the same prompt. Audience: senior DS practitioner shaping the practice's default per-component documentation deliverable. Reference line: Storybook 8.6 / 9 (the latter shipped May 2026 with the new component-page architecture); MDX 3 (current); React 19; Zeroheight 4.x; Supernova 2026; Knapsack mid-2026 release. The template described below is what the practice should ship as a default in commercial Documentation deliverables — it is prescriptive on shape and slots, opinionated on order, and explicit about where the practice's POV diverges from tooling-vendor defaults.

---

## 1. Why the per-component template is load-bearing

The template is the single artefact most likely to differentiate a delivered design system from a *system that survives*. The reason is not pedagogical — it is operational. Without a per-component template, every component-page author makes their own choices about what to include, in what order, with what depth. After 60 components, a docs site has 60 slightly-different shapes. After the third consumer encounters a missing section on a third component, they stop relying on the docs site and either build wrong or build their own. Both are adoption failures and neither is recoverable post-handoff. The practice has named this gap in 09-gaps-and-open-questions §1.10 since the file was written, and it remains the most-likely-to-derail-quality-of-deliverable item on the list.

**Why the field defaults to "the IA emerges per component."** Consultancy engagements are time-boxed and component-driven; component pages are typically written in the order components ship; whoever owns the first page sets the de facto template; subsequent authors copy-and-adapt. By the time anyone notices the inconsistency, ten components have shipped and retrofit is a 60-hour project no one scoped. A *prescriptive* template authored in week one, before the first component page is written, is the only way to avoid this. The template is a Discovery deliverable, not a Documentation deliverable — the discipline starts before content does.

**The authoring-cost / consumption-cost asymmetry.** Authoring a component page takes 4–12 hours per component the first time (more for foundational primitives, less for variants of established patterns). At 60 components, that is a 240–720-hour authoring cost — paid once. Consumption is paid forever: every designer adopting the system, every engineer reaching for a component, every AI agent attempting code generation, every executive reviewing the dossier. The consumption cost dwarfs the authoring cost by orders of magnitude over a system's life. The template is the lever that lowers the consumption cost — every consumer learns the shape once, then knows where to find what they need on every component thereafter. Without the template, every consumer pays the "where does this live on this page" tax repeatedly.

**The four-audience problem.** Component-page consumers split into four audiences, each with different access patterns:

- **Designers** scan for examples and do/don'ts; they want to see the component used correctly and incorrectly before they read a single sentence of prose.
- **Developers** scan for the props table, the framework-specific code snippet, the Storybook story link.
- **AI agents** consume the structured metadata layer (`.ai.json`, the schema embedded in MDX, the description fields).
- **Executives and auditors** consume the conformance dossier — accessibility evidence, version, adoption metrics where instrumented, deprecation status.

A template that surfaces each audience without forcing them to read the whole page is a four-axis problem. The shape that works in 2026 is **a stacked layout with strong anchor links and a per-page table-of-contents shadowed by a summary card**. Designers and developers find their entry point in the summary card; AI agents find their entry point in the structured metadata block; auditors find their entry point in the conformance dossier slot. The TOC handles the rest.

**The "trust the docs" cliff.** Once a consumer finds one wrong page — one out-of-date prop default, one component marked stable that's actually deprecated, one accessibility note that contradicts the live build — they stop trusting the entire site. This is asymmetric: trust takes weeks to build per consumer and minutes to lose. The template is a contract that bounds where wrong-ness can live. If the props table is generated from the component data file, the props can never be wrong. If the accessibility section is `.ai.json`-derived and the same schema is enforced in CI, the accessibility note can never lie about what the component does. The template's structural discipline is what makes single-source-of-truth generation tractable; without it, the source of truth fragments across the prose authors.

**The relationship to ACR / VPAT evidence.** Per 28-web-accessibility-implementation §8 and 14-accessibility, every component page is a per-component conformance dossier in microcosm. A consuming product's ACR aggregates per-component dossiers with application-level evidence; without the per-component dossier slot in the template, the consuming product's accessibility lead has to reverse-engineer it from the docs site. This is a real engagement-end cost the practice currently absorbs and could ship as a default deliverable instead. The template's accessibility section is what makes this aggregation possible.

---

## 2. The template's sectional spine

The minimum viable set, in shipping order:

1. **Header** — name, brand-system version where the component was added or last meaningfully changed, status (stable / beta / deprecated), category (Foundations / Layout / Form / Navigation / Feedback / Data / Overlay).
2. **Summary card** — one-sentence purpose; primary use case; "see also" alternatives surfacing in the first paragraph rather than buried at the bottom.
3. **Live example** — the canonical configuration of the component, interactive in Storybook, with a "view code" affordance. Examples-before-specs is the discipline.
4. **Purpose** — the intent layer; one or two paragraphs of declarative prose covering *what the component is for*.
5. **When to use** — the prescriptive layer; bulleted list of canonical use cases.
6. **When not to use** — the avoid-when layer; bulleted list with cross-links to the component-the-consumer-should-use-instead. Negative selection is the highest-leverage AI-consumer section per 04-documentation and Wolosin's metadata loop.
7. **Anatomy** — labelled diagram of the component's structural parts, named to match the props vocabulary. Where slots exist, the slot semantics ("trigger," "content," "footer-action").
8. **Props / properties / API** — generated from the component data file. Sortable, searchable, with deprecation flags surfaced inline.
9. **States** — rest / hover / focus-visible / pressed / disabled / loading / error / empty / read-only as applicable. Per-state row with visible-state, announced-state, and the state's interaction model (e.g., "loading shows the spinner and disables interaction; the live region announces 'Loading…' followed by 'Loaded' on completion").
10. **Variants** — visual variants (size, tone, density, emphasis) with the prop combinations that produce each. Distinct from states; variants are intentional design choices, states are runtime conditions.
11. **Examples** — multiple canonical configurations; one per typical use case; design-mode (Figma frame), live (Storybook), code-paste (MDX fenced block) per example.
12. **Do and don't** — side-by-side, paired by dimension, specific.
13. **Accessibility** — inline; not a separate page. Maps to the 17-accessibility-annotation-contract fields per concern.
14. **Content guidelines** — tone, error messages, empty-state copy, CTA labels. Per the UX Copywriter scope in 04.
15. **Composition and related components** — typed relationships (alternative to / composes with / supersedes / superseded by) rather than untyped "see also."
16. **Changelog** — per-component, semver-scoped, with deprecation announcements as first-class entries.
17. **Conformance dossier** — automated test results, manual-AT walkthrough log links, contrast verification, SC-by-SC mapping for the WCAG 2.2 criteria the component participates in.

**Why the order.** Consumers scan top-to-bottom; the order is calibrated for how the four audiences actually move through the page. Designers find their entry point in the summary card and live example (positions 2–3) and rarely scroll past 12 (do/don't). Developers find their entry point in the props table and code examples (positions 8 and 11) and scroll up to 4–6 only when something is unclear. AI agents consume the entire page but rely on the structured metadata block embedded in 4–7, 13, 15. Auditors enter at 17 (conformance dossier) and reference 13 (accessibility) for evidence detail. The order is opinionated and the practice should hold it.

**The order's exception: foundational primitives.** For tokens, layout primitives, and pure-utility components (e.g., a `VisuallyHidden` wrapper, a `Portal`), the props table *is* the answer to most questions and the prose layer is correspondingly thin. The template handles this via a "primitive variant" mode where the props table moves up to position 4, and sections 4–7 collapse to a one-paragraph purpose. The template still ships all the slots; it just acknowledges that for primitives the meaningful content lives in the props table.

**Component-type-specific extensions.** Six component types have additional required slots:

- **Form components** — validation guidance (when a value is invalid, what the error string is, where the error appears), `aria-describedby` and `aria-errormessage` wiring, `:user-invalid` styling, autocomplete attribute mapping per WCAG 1.3.5 (see 28 §6).
- **Toast / snackbar / notification** — auto-dismiss timing, queue behaviour, `role="status"` vs. `role="alert"` decision, the per-toast accessible name vs. body distinction.
- **Modal / dialog / drawer** — focus-trap and focus-return targets, `inert` scope, Escape behaviour, overlay-click behaviour, the relationship to `<dialog>` + `showModal()` (web) or platform-specific modal primitives (mobile).
- **Tooltip and popover** — trigger model (hover, focus, click), persistence behaviour, dismissibility, the WCAG 1.4.13 contract.
- **Chart / data visualization** — encoding guidance (colour, position, size, shape, pattern), the colour-is-not-the-sole-carrier rule, axis and legend conventions, per-chart-type accessible name and description templates, sonification or table-fallback patterns. (This component type is a known practice gap per 09 §5.2 and is one of the genuine field-level absences.)
- **Composite / layout primitives** — slot semantics, composition rules ("a `Card` may contain at most one `CardHeader`, zero-or-more `CardBody`, and zero-or-one `CardFooter`"), the named relationships between the primitive and the components that compose with it.

Each extension is a *required slot* on the template for components of that type, not an optional add. The template's metadata schema enforces this.

**Sections external sources name that we should consider but may not adopt.** Worth weighing explicitly:

- **Design rationale / decision history (Mangialardi ADRs).** A short section explaining why a particular design decision was made — e.g., "we ship a `tone` prop with `default | brand | critical | success` rather than separate component variants because the brand changes faster than the structural shape." Strong argument for inclusion in the practice's template *as a collapsed-by-default section*. Designers and engineers consume it occasionally; AI agents consume it as part of `business_context`. Not a "philosophy" section; a typed list of "why X over Y" decisions.
- **Version compatibility (Curtis).** "This component requires `tokens@4.x` and `react@18+`." Useful for systems with multiple consumer versions in flight; over-engineered for consumer products where the system is monorepo-pinned. Adopt as conditional; ship by default for portfolio engagements with multiple consumer products.
- **Anonymous user research notes.** A very small set of systems include "what we learned testing this component with users" inline. Where the practice has the research, including it adds practitioner authority. Where the practice does not, the slot becomes embarrassing. Adopt only when the research exists.
- **Adoption metrics inline.** "Used by 14 surfaces; latest version adopted by 11; 3 surfaces on a deprecated prior major." Strong for systems with instrumented consumption; aspirational otherwise. Adopt only when the instrumentation exists; otherwise the slot lies.

**Sections that should be omitted by default.** A short list of recurring noise:

- **Per-component "philosophy" sections** that recapitulate the system's overall principles. Move to system-wide pages.
- **Decorative changelog narratives** — "We made the button rounder, which feels more friendly." Either the changelog is structured per-version with semver and reasons, or it is removed.
- **Founder-letter framings.** No "From the Component Library Team:" intros.
- **Live performance dashboards inline.** Performance benchmarks belong on a system-wide observability page, not per-component.
- **Marketing-tier preview imagery.** Hero shots that take 80% of the viewport do not help any of the four audiences.

---

## 3. Per-section depth — what each section actually contains

### Purpose, when-to-use, avoid-when

The intent layer carries more weight than any other prose section; it is the layer AI agents consume to choose between components, and the layer designers consume to decide whether to use the system at all.

- **Purpose** is one or two paragraphs, declarative, *component-as-noun* in the topic sentence ("A button is an interactive control that triggers an action") followed by component-as-verb context ("Use a button when the user must take an action that progresses the primary task. Buttons emphasise commitment; links emphasise navigation.") The seam between noun and verb framing is where the semantic context lives. Both framings matter — the noun framing anchors the type; the verb framing anchors the use.
- **When to use** is a bulleted list of canonical use cases, typically 3–6 items. Each item is one line, prescriptive, and references a real surface or pattern when possible ("As the primary CTA on a form (e.g., Submit, Save, Continue)"). The discipline is specificity; "for actions" is too generic to be useful.
- **When not to use** is the load-bearing section. Each item names the thing the consumer is tempted to use this component for, the reason to avoid it, and the component to use instead with a cross-link. *"Don't use a button for navigation between pages — use a link, which signals navigation rather than action and gets the right semantic on the web (`<a href>` rather than `<button>`)."* This pattern — the temptation, the reason, the alternative — is the most-leverage rule the template can encode. Per Wolosin, AI agents that have `avoid_when` data with cross-links to alternatives produce dramatically better component selection than agents working from `when_to_use` alone.

The avoid-when discipline carries through to `.ai.json` as the `avoid_when` array, with each entry as a structured object (`{situation: ..., reason: ..., alternative: "@components/Link"}`).

### Props / properties / API

This section is generated from the component data file in mature systems and hand-authored as a fallback. Either way, it is the most-consumed section by developers and the highest-stakes section for accuracy.

The discipline:

- **Per-prop row format.** Name, type signature, default, description, deprecation flag, version-introduced. The description field is one or two sentences, with examples for non-obvious props ("`tone` — controls the visual emphasis. `'default'` for typical use; `'brand'` for primary CTAs; `'critical'` for destructive actions").
- **Type signatures shown verbatim from the source.** Generated; never hand-typed. Deviations between the docs and the source are the most-corrosive form of doc rot.
- **Defaults shown.** If the prop is `tone: ToneVariant = 'default'`, the default is shown both in the type signature and as a separate "Default" column.
- **Deprecation flag inline.** A `@deprecated` JSDoc comment on the prop produces a deprecation flag in the row, with the deprecation message and the prop-to-use-instead.
- **Required vs. optional split.** A standard sort puts required props first, then optional, then deprecated.
- **Composition props split out.** Where a component takes a children slot, render-prop, or compound child, the section names the composition primitives separately rather than burying them in the props table. A `Tabs` component's API is *not* "the `Tabs` props"; it is "the `Tabs` props plus the `TabList`, `Tab`, `TabPanels`, `TabPanel` composition primitives." The template enforces the split.

The seam between "props the consumer sets" and "slots the consumer fills" is where most documentation falls down. Composition primitives need their own row format that names the slot, the allowed children, the required parent, and the slot's semantic role.

### States

The per-state row format:

- **State name** (rest, hover, focus-visible, pressed, disabled, loading, error, empty, read-only).
- **Visual treatment** (a screenshot or a Storybook story link showing the state).
- **Announced state** (what AT announces for this state — `aria-disabled`, `aria-busy`, `aria-invalid`, `aria-current`).
- **Interaction model** (what the state allows; e.g., disabled does not receive focus, loading receives focus but ignores activation, error receives focus and AT announces the error message).
- **Triggering condition** (what causes the state — user input, prop change, async resolution).

States that don't apply to the component-type are omitted; the template's metadata schema enforces "rest is always present; the rest are conditional on the component type."

The visible-vs-announced distinction is what the template makes explicit. Many existing systems collapse the two and produce wrong AT behaviour; the template forces the per-state announcement explicit.

### Examples

**Examples-before-specs** is the discipline. Per Figma DS x AI (2025) and consistent across high-quality public exemplars (Atlassian, Spectrum, Carbon), consumers scan the live example first to confirm the component is what they think; they read the prose only when the example is unclear. The template's positioning at slot 3 reflects this.

The canonical example set per component-type:

- **Buttons, links, badges, tags** — one example per tone + emphasis combination; one example with an icon adornment; one example in disabled and loading state.
- **Form fields** — empty / filled / focused / error / disabled / loading / read-only; one example with help text; one example with autocomplete; one example in a multi-field group with `<fieldset>`.
- **Cards** — minimal; with media; with action; with multiple actions; in a grid (composition).
- **Tables / data grids** — minimal data; sortable; with selection; with row-level actions; with pagination; with empty state.
- **Modals / dialogs** — confirm; form; informational; multi-step.
- **Toasts / notifications** — success; error; with action; queue behaviour.
- **Tooltips / popovers** — hover; focus; with rich content; on a disabled trigger.

The pattern: 4–8 examples per component, each demonstrating one specific axis the consumer might vary. More than 8 becomes an example dump; fewer than 4 leaves out canonical configurations the consumer needs.

**Per-example slots.** Each example carries a one-sentence caption explaining what the example demonstrates ("With an icon adornment — when the action benefits from a visual cue alongside the label"), a live render in Storybook, a code-paste fenced block, and a Figma frame link. The Figma frame link is the under-shipped slot in most systems and is the seam where designers transition from docs page to design tool.

### Do and don't

Side-by-side, paired by dimension, specific. The discipline:

- **Each "do" is paired with a "don't" on the same dimension.** "Do use 'Save' for the primary action when the action persists changes." paired with "Don't use 'Submit' when the action is not a form submission." The pair is what makes the row useful; a one-sided "do" is a tip, not a contract.
- **Specific over generic.** "Do use clear language" is noise. "Do label destructive actions with the consequence ('Delete account' rather than 'Delete')" is a rule.
- **Visual where possible.** A do/don't pair with screenshots of the actual usage costs more to produce and pays back proportionally — designers absorb visual examples 4–10× faster than prose.
- **One pair per dimension; no multi-rule pairs.** A do that says three things and a don't that says four becomes a paragraph; the side-by-side discipline collapses.

The most common authoring failure is generic do/don'ts that could appear on any component page. The template's audit pass for do/don't asks: *if this pair were copy-pasted onto another component page, would it still make sense?* If yes, it is too generic; rewrite for specificity.

### Accessibility

Inline, mapping to the 17-accessibility-annotation-contract fields per concern. The template's accessibility section is *not* a free-form prose block — it is a structured table that produces both the human-readable docs and the `.ai.json` accessibility schema from the same source.

Per-row format:

- **Concern** (name mechanism, role, state, value, focus, ARIA relationships, focus-return, forced-colors survival, motion treatment, gesture alternative, live-region intent, APG keyboard model — the 17 concerns from the contract).
- **What the component does by default.** "Renders `<button>` so the role is automatic; the visible text is the accessible name."
- **What the consumer must specify.** "If the button is icon-only, the consumer provides `aria-label`; the system warns at the type level if a non-text-content button has neither a visible label nor `aria-label`."
- **AT-by-AT verification status.** "Verified on NVDA 2026.1 + Chrome, JAWS 2026 + Chrome, VoiceOver + Safari macOS, VoiceOver + Safari iOS, TalkBack + Chrome (Android). Last verified 2026-06-12."
- **WCAG SC mapping.** The success criteria the component participates in (e.g., 1.4.4 Resize Text, 2.4.7 Focus Visible, 2.5.8 Target Size Minimum). The conformance dossier (slot 17) consumes this for ACR aggregation.

This is the section that closes the gap between "the design system documents accessibility" and "the consuming product's ACR has per-component evidence." The template makes it default; without it, the conformance dossier remains a per-engagement bespoke artefact.

### Content guidelines

The seam with 04-documentation's UX Copywriter role. Per-component:

- **Tone for default copy** — buttons say "Save," not "Submit changes" except in specific cases.
- **Error messages** — patterns and templates ("[Field] [requirement that wasn't met]." e.g., "Email must include an @ symbol.").
- **Empty-state copy** — "No results yet" rather than "Nothing here." Hierarchy: state, why the state, what the user can do.
- **CTA labels** — verbs first, action-noun where the action's object is implicit ("Save changes" rather than "Save"; "Add member" rather than "Add").
- **Language for help text and tooltips** — declarative, second person, present tense.

This section is short on most components and substantive on form components, modals, and toasts. The template's audit pass asks: *if a copywriter on the consuming product team needed to localise this component's copy, would they have what they need?*

### Composition and related components

Typed relationships, not untyped "see also":

- **Alternative to** — components the consumer might confuse with this one. Used by AI agents to disambiguate during component selection.
- **Composes with** — components that fit inside or around this one ("`Card` composes with `CardHeader`, `CardBody`, `CardFooter`").
- **Composes within** — the inverse ("`CardBody` composes within `Card`").
- **Supersedes** — components this one replaces. The deprecation history is a graph, not a linear list.
- **Superseded by** — for deprecated components only. The "use this instead" pointer.

The graph layer is where the design system goes from "a list of components" to "a coherent vocabulary." Untyped "see also" loses the relationship semantics and AI agents in particular use the typed graph for recommendations.

### Changelog

Per-component, semver-scoped, structured. Per-version row:

- **Version** (e.g., `4.2.0` for the system-wide release that included this change; per-component semver is over-engineered).
- **Date.**
- **Type** (added, changed, deprecated, removed, fixed, security).
- **Description.**
- **Migration link** for breaking changes.

Deprecation announcements are first-class entries with a target removal version and a migration path. The deprecation appears in the changelog *and* on the prop or component itself (a banner on the component page; deprecation flags inline on the prop row).

The system-wide changelog is the aggregation; the per-component changelog is the per-consumer truth.

---

## 4. The four-audience problem — what each audience needs

The template's slot order is calibrated to the four audiences' access patterns; the question this section answers is *what does each audience actually need to find on the page*, mapped against the slots.

**Designers** — entry points: summary card, live example, do/don't.

- They confirm the component is the right tool by scanning the live example.
- They scan do/don't to understand the contract.
- They reach for the Figma frame link in the examples to pull the component into their working file.
- They occasionally reach for content guidelines and accessibility notes when reviewing a senior engineer's PR.
- They very rarely read the props table or the changelog.

The template optimises for designers via the early summary card and live example; the Figma frame link in every example is the seam.

**Developers** — entry points: props table, code-paste examples, Storybook story.

- They reach for the props table to find the prop they need.
- They copy a code example into their PR as the starting point.
- They reach for the Storybook story when they need to see edge-case behaviour.
- They consume the changelog when they need to reason about migration.
- They consume accessibility notes when reviewing their own PR before submission.

The template optimises for developers via the generated-from-data props table, framework-specific code snippets, and the per-example "view code" affordance.

**AI agents** — entry point: structured metadata.

- They consume the entire page but their decisions hinge on the structured metadata block.
- The `.ai.json` schema embedded in MDX (or sidecar to it) is what the agent uses for component selection.
- The `when_to_use` and `avoid_when` arrays are the highest-leverage sections; per Wolosin's metadata loop, agents with rich `avoid_when` produce 60–80% fewer wrong-component-selection errors than agents with `when_to_use` only.
- The accessibility schema fields are what the agent uses to generate ARIA, focus management, and forced-colors handling.
- The composition graph is what the agent uses to assemble components into patterns.

The template optimises for AI agents via the embedded `.ai.json` block, the structured accessibility table (which produces the `accessibility` schema field), and the typed composition graph (which produces the `relatedComponents` schema field).

**Executives and auditors** — entry point: conformance dossier.

- They reach for the dossier to verify the component's accessibility evidence per WCAG SC.
- They reach for the version field to verify the component is current.
- They reach for the deprecation status to verify the component is supported.
- They occasionally reach for the changelog when scoping migration timelines.
- They rarely read the prose layer.

The template optimises for auditors via the dedicated conformance dossier slot at position 17, which aggregates the automated test results, manual-AT walkthrough log links, contrast verification, and SC-by-SC mapping.

**The shadowed-anchor pattern.** The way the template surfaces all four audiences without forcing any one of them to read the whole page: every section has an anchor link; the page's table-of-contents is shadowed by a small "audience" toggle (designer / developer / AI / auditor) that highlights the sections most relevant to the selected audience and dims the others. The toggle does not hide content — it dims it — so an audience can navigate to any section but the entry-point hierarchy is preserved per-audience. This is a Storybook-9-era pattern and is implementable in MDX via component meta-fields; in Zeroheight it is implemented via tagged sections and audience filters.

---

## 5. Generation, authoring, and the seam between them

The template's economic argument is that the generation seam is what makes it sustainable at scale. Per Curtis (*Components as Data*, Sep 2025) and 04-documentation's stance, mature systems treat the component data file as the source of truth and generate as much of the documentation as possible. The template names the seam explicitly.

### Generated sections

- **Props / properties / API** — generated from the TypeScript types or the framework-specific component definition. Storybook 9's auto-generated docs page is the baseline; Zeroheight's React Connect is the equivalent for hosted docs.
- **Default examples** — every prop produces a default example via Storybook's controls; the canonical "minimal example" is a generated configuration.
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
- **Design rationale** — when included; authored once and rarely revisited.
- **The example captions** (one-sentence "what does this demonstrate") — authored.
- **The accessibility section's "what the component does by default" and "what the consumer must specify" rows** — authored, then validated against the implementation in CI.

### Generated-with-authoring-overlays

- **States** — the default state set is generated from the component data file's state declaration; per-state announced-state and interaction-model are authored, with the schema validating that every declared state has both rows filled.
- **Variants** — the default variant set is generated from the prop combinations; the visual treatment screenshot is authored or auto-captured.
- **Examples** — the canonical minimal example is generated; the additional examples per component-type are authored.
- **Changelog** — generated from the commit history with `@semantic-release` or equivalent, with authored prose for breaking changes.
- **Conformance dossier** — automated test results generated from CI; manual-AT walkthrough log links authored; SC-by-SC mapping authored once and validated against test coverage.

### The CI freshness check

Per 04 §3 and the AI-Compatible Doc Ch. 7 pattern: the build fails if the component code changes but the docs do not.

The mechanism:

- A pre-commit hook computes a hash of the component's authored doc fields (purpose, when-to-use, avoid-when, content guidelines, accessibility "what the consumer must specify" rows).
- The hash is stored alongside the component's source.
- On any change to the source, the hash is recomputed; if the hash matches the stored value, the docs were not updated and the commit fails with "Component changed; documentation hash unchanged. Update the docs or explicitly mark this change as documentation-irrelevant."
- The "explicitly mark" affordance is a `// docs: irrelevant` comment that the hook recognises; this prevents the hook from blocking trivial refactors.

The freshness check is the single highest-leverage piece of CI accessibility / documentation infrastructure the practice can ship. It costs ~4 hours to implement per system and prevents the "60 pages, 12 of them out of date" failure mode permanently.

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

The docs site, the `.ai.json` registry, and the component-page conformance dossier all derive from this set. A change to `Button.types.ts` triggers the freshness check on `Button.docs.mdx`; a change to `Button.test.tsx` updates the conformance dossier; a change to `Button.tokens.ts` updates the `.ai.json` `tokens` field automatically.

### Where authoring tooling falls short in 2026

- **Generated-from-data documentation is still not the default in most consultancy deliverables.** The architecture exists; the tooling exists; the practice does not yet ship it as a default. This is the gap between 04-documentation's stated direction and the commercial proposal's actual deliverables.
- **MDX 3 + Storybook 9 is the closest mature stack for a code-side docs site.** The remaining seam: design-side consumption (Figma library, Zeroheight) does not yet pull from the same source automatically; the design library is rebuilt from the data file on a separate cadence, which produces drift.
- **`.ai.json` is not yet a standard.** The schema is internal-tier IP for the practice; external sources (Wolosin, the AI-Compatible Doc) name it conceptually but no canonical schema has emerged in the field. The practice can ship its schema as a public artefact and claim the layer.
- **Zeroheight's API for generated content** has matured significantly through 2025–2026 but remains the design-side equivalent of "Storybook autodocs from 2022" — usable, opinionated, and constraining. For systems using Zeroheight, the practice's discipline is to use Zeroheight for the design-consumer surface and treat code-side docs (Storybook + MDX) as the authoritative source.
- **The Figma frame link per example** is the under-shipped slot. Most systems link to the design library at the system level, not per-component-example level. Authoring the link is a 2-minute task per example; over 60 components × 6 examples, it is 12 hours of authoring that pays back permanently in designer-flow.

### The per-component template's relationship to system-wide IA

The per-component page is not the navigation surface; the system-wide IA is. The component page lives at the leaves of a navigation tree:

```
Home
├── Getting started
├── Foundations
│   ├── Color
│   ├── Typography
│   ├── Space
│   └── Motion
├── Layout
│   ├── Grid
│   ├── Stack
│   └── Box
├── Components
│   ├── Form
│   │   ├── Button
│   │   ├── TextField
│   │   └── ...
│   ├── Navigation
│   ├── Feedback
│   ├── Data
│   ├── Overlay
│   └── ...
├── Patterns
├── Accessibility
└── Changelog
```

Search is the first-class navigation primitive at scale (per Couldwell and consistent across high-quality exemplars); category landing pages are second-class. The per-component template's job is to be findable from search, navigable from category, and readable per audience-entry-point. The system-wide IA's job is to compose the category landing pages and patterns layer; that is a separate template the practice should also encode but is out of this file's scope.

---

## 6. Tooling decisions and recommendations

### The default stack

For engineering-heavy systems with code-resident developers, **Storybook 9 + MDX 3 is the default**. The reasoning:

- Storybook 9 (May 2026) ships the new component-page architecture with built-in support for autodocs, addon-a11y, and the controls panel as a first-class authoring surface.
- MDX 3 supports the structured-frontmatter pattern that lets the per-component template's metadata schema live alongside prose.
- The CI integration (Chromatic for visual regression, axe-core via `@storybook/addon-a11y` for runtime accessibility, Storybook Test Runner for behaviour) is the most-mature stack for component-level CI in 2026.
- The cost is portability — the docs site is tightly coupled to Storybook's renderer. Migration to a different platform requires rewriting MDX-with-Storybook-component-imports, which is non-trivial.

### Hosted alternatives

- **Zeroheight (4.x)** — the design-side default for designer-heavy organisations. Strong Figma integration, good for cross-disciplinary consumption, weak for code-resident developers. Use as a *secondary surface* synced from the source, not as the primary docs platform.
- **Supernova (2026)** — competitive with Zeroheight on the design-side; stronger token-management story; weaker Figma sync as of mid-2026 (verify per release). Choose over Zeroheight when token management is the practice's primary value and the design-side consumption is secondary.
- **Knapsack (mid-2026)** — the enterprise-tier option with Code Connect integration, multi-platform support, and the ACR aggregation layer the practice's conformance dossier slot depends on. Choose for portfolio engagements where the docs platform must serve 20+ consumer products.
- **GitBook** — historically used for design-system docs in earlier engagements; in 2026 it is a yellow flag for systems with > 30 components. Migration cost from GitBook to Storybook + MDX is one of the more-frequent technical-debt items in the practice's portfolio.

### Self-hosted vs. SaaS

Self-hosted (Storybook deployed to internal infra; static MDX site behind a corporate VPN; on-prem Penpot for design library) is required for:

- Regulated clients (healthcare, finance, government) where component metadata must not leave the network.
- EAA-procurement clients where vendor lock-in is a procurement-tier concern.
- Clients with internal AI tools that need to query the design system from within the network without external API calls.

SaaS (Zeroheight hosted; Supernova hosted; Storybook deployed to Vercel) is the default for:

- Most agency-to-client engagements where the design system is shared with the consuming product team via the agency's docs platform.
- Engagements where the time-to-deploy of a hosted platform is worth the trade-off in portability.

The practice's discipline: assume self-hosted is required *until the client explicitly waives it*. Many clients will, but the conversation is procurement-grade and worth scoping deliberately.

### The decision framework

A client picks a docs platform based on five questions:

1. **Codebase culture.** If developers live in the codebase and the system ships as code, Storybook + MDX is the answer. If the system is design-led with engineers as occasional consumers, hosted (Zeroheight / Supernova) is the answer.
2. **Designer-engineer ratio.** > 2:1 designer-heavy → hosted. Roughly even → Storybook + MDX with hosted secondary surface. > 1:2 engineer-heavy → Storybook + MDX as primary, hosted optional.
3. **Budget tier.** Storybook + MDX is free; Zeroheight is $5–15K/year for an org-tier subscription; Supernova is comparable; Knapsack is $30K+/year for enterprise-tier. The free option is the best option for systems with < 4 consuming product teams.
4. **Regulatory constraint.** EAA, HIPAA, PCI, government → self-hosted, with the implication that the docs platform is part of the engagement's infrastructure scope, not an afterthought.
5. **Scale of consumer base.** < 5 consumer surfaces → either option is fine. 5–20 surfaces → hosted with code-side mirror or vice versa. 20+ surfaces → enterprise tier (Knapsack) or self-hosted with custom tooling.

### Where the system can be portable

The component data file (per §5) is the portable layer. Each docs platform consumes the data file; each platform produces the docs site. A system that authors `Button.docs.mdx` with Storybook component imports is *not* portable; a system that authors `Button.metadata.json` plus `Button.docs.md` with no platform-specific dependencies is. The practice's discipline: **separate the authoring source from the rendering platform**. The authoring source lives in the component repo, version-controlled, platform-neutral. The rendering platform is replaceable.

This is the single most important architectural decision in the docs strategy and is under-articulated in most existing engagements. The template's structural discipline is what makes the separation tractable.

---

## 7. Anti-patterns and failure modes

The recurring patterns the practice should explicitly avoid; each maps to a recoverable engagement scope item.

### Generic-template overfit

Every component page has the same template, even when the template doesn't fit. A primitive `VisuallyHidden` wrapper has a 17-section page where 13 sections say "N/A" or "Not applicable to this component." Consumers learn the template is performative rather than informative.

The fix: the template's metadata schema declares per-section conditions (`appliesTo: ["interactive"]`, `appliesTo: ["form"]`, `appliesTo: ["composite"]`). Sections that don't apply to the component-type are *omitted*, not marked N/A. The "primitive variant" mode (per §2) is the codified version of this.

### Documentation-as-changelog

The page is mostly history; the current usage is buried under "What's new in v3.4." Consumers who need to use the component now have to scroll past the history to find the prescriptive layer.

The fix: changelog at slot 16, after the prescriptive layer. The header carries version-introduced and last-changed metadata as a compact summary; the full changelog is at the bottom. Consumers who want history can find it; consumers who want current usage are not blocked by it.

### Implicit-context prose

Written for the original team; references shared abbreviations, internal Slack threads, "the original Figma file" without a link. Fails for new consumers and for AI agents that consume the page literally.

The fix: every prose section is read by a consumer-not-on-the-team before merge. Specifically: every cross-reference is a link, every abbreviation is expanded on first use, every "as we discussed" is replaced with "see [linked source]." This is editorial review, not authoring; the practice's UX Designer ownership of docs strategy includes the audit pass.

### Zero-example pages

Lots of prose, no live or pasteable examples. Designers and engineers leave; AI agents have nothing to anchor on.

The fix: the template enforces a minimum of one live example at slot 3 and one code-paste fenced block per example. The build fails if either is missing. (This is the simplest CI rule; Storybook's auto-generated docs page enforces the live example automatically.)

### Stale documentation

60 pages, 12 of them out of date. Trust collapses.

The fix: the CI freshness check (per §5). Cost: ~4 hours per system. Pays back permanently.

### "Tooling without authors"

Zeroheight subscription, no UX Designer hours scoped to fill it. Empty rooms with brand colours.

The fix: the practice's commercial scope ties Zeroheight (or equivalent) to the UX Designer hours. The proposal cannot scope a docs platform without scoping the authoring labour. The proposal cannot scope authoring labour without scoping the platform. They go together; the scope template enforces it.

### "Six weeks of tooling, one week of content"

Per 04-documentation's failure-modes section. The team picks Zeroheight vs. Supernova vs. Knapsack for six weeks; spends one week writing the first three component pages; ships an empty platform.

The fix: the platform decision is a Discovery deliverable, not a Documentation deliverable. The decision is made in week 1 against the framework in §6; authoring begins in week 2. The practice's discipline: the platform decision takes 2 hours, not 6 weeks. Where the client has strong vendor preferences, those preferences are the decision; the practice does not litigate the choice.

### Accessibility as a separate page

The visit pattern misses it. A consumer who doesn't visit the `/accessibility` page assumes accessibility is "handled" without knowing what is or isn't documented.

The fix: accessibility inline at slot 13 of every component page; the system-wide accessibility page is the architecture and conformance reporting overview, not the per-component contract. Per 04 and 14, the practice already encodes this stance; the template makes it default.

### "The template is comprehensive; the prose is empty"

Every section heading is present; the content under each heading is a one-line placeholder. Consumers see structure and conclude there is content; there isn't.

The fix: the metadata schema enforces minimum prose lengths per section (Purpose: 50–500 words, When to use: 3–8 bullets, Avoid-when: 2–6 bullets with linked alternatives, etc.). Sections under the minimum fail the build with a specific error. This is the pickiest of the CI rules; it is also the one that prevents the most common failure mode in shipping consultancy deliverables.

---

## 8. The practice's POV — what we ship, why, and the commercial framing

The template is a **default Documentation deliverable scoped in the SOW alongside the dedicated UX Designer role.** It is shipped as version 1.0 in week 1 of every engagement, populated through the engagement, and handed off as part of the system-wide deliverable.

### What the practice ships

**Version 1.0 of the template per engagement** — the actual MDX template file (or the Zeroheight equivalent, or the Knapsack equivalent), pre-populated with the section headings, the metadata schema, the CI freshness check, and the per-section minimum-prose rules. Pulled off the shelf in week 1; populated through the engagement. The template is the practice's IP; the populated component pages are the client's deliverable.

**The commercial scoping unit** is "per-component-page authoring hours × component count × the UX Designer + UX Copywriter mix." A typical breakdown for a 60-component system on a CareCentrix-tier engagement:

- **UX Designer authored sections** (purpose, when-to-use, avoid-when, anatomy, do/don't, accessibility "what the consumer must specify," design rationale where included): 4–8 hours per component, scaling with component complexity. Average: 6 hours × 60 components = 360 hours.
- **UX Copywriter authored sections** (content guidelines, error messages, empty-state copy, CTA labels): 1–2 hours per component for components with copy concerns; 0 for pure-utility components. Average: ~1 hour × 60 components = 60 hours, with a sharper distribution.
- **Engineering authored sections** (component data file definitions, types, examples, the CI freshness check setup, the conformance dossier integration): typically scoped under engineering hours rather than documentation hours; ~2 hours per component for the data file authoring. Average: 2 hours × 60 components = 120 hours.
- **Editorial review pass** (the read-by-consumer-not-on-team audit per anti-pattern "implicit context"): 0.5 hours per component. Average: 30 hours.
- **Template authoring at engagement start** (custom adaptation per client; the practice's template adjusted for the client's component vocabulary, brand voice, and tooling stack): 16–40 hours.

Total documentation labour for 60 components: ~570–600 hours of UX Designer / UX Copywriter time, plus ~120 hours of engineering data-file authoring, plus the template-customisation cost. At blended UX rates, this is a substantive scope item — ~$60K–$100K depending on rates and engagement size — and is currently absorbed in many proposals as "documentation" without per-component itemisation. **Itemising it makes the cost defensible; clients understand "60 components × 6 hours" better than "documentation pass."**

### What the practice can claim publicly

The defensible POV differentiators that no external source articulates as a complete package in mid-2026:

1. **The template itself, with the 17-section spine.** External exemplars (Atlassian, Spectrum, Carbon, Polaris) each have their own template; none is published as a deliverable. The practice can publish ours as practice IP.
2. **The four-audience framing** (designer / developer / AI / auditor). External sources name three; the AI-as-first-class-consumer audience is current to 2024+ and the auditor-as-first-class is current to the 2025 EAA enforcement. The practice's framing of all four is timely.
3. **The components-as-data substrate as the authoring source.** Curtis articulates the architecture; the practice can articulate the *engagement-scoped commercial deliverable* — the Style Dictionary plus component data file plus CI freshness check that the client team can run after handoff.
4. **The accessibility annotation contract as `.ai.json` fields.** Per 17 and 28; the practice can claim this as the seam between design-time annotation, AI-time consumption, and audit-time evidence aggregation.
5. **The conformance dossier slot.** The per-component dossier is the missing piece in most existing systems' ACR pipelines; the practice can ship it as a default and claim the layer.

### Where the template positions the practice against tooling vendors

Zeroheight, Supernova, and Knapsack ship templates. The practice's value is *not* the template alone — the practice's value is:

1. **The editorial discipline** that makes the template's content load-bearing rather than performative.
2. **The components-as-data architecture** that makes the template's prescriptive structure tractable at scale.
3. **The accessibility annotation contract** that makes the template's accessibility section closer to ACR-grade evidence than existing tooling-vendor accessibility blocks.
4. **The CI freshness check and per-section minimum-prose rules** that make the template enforce its own quality.

The vendor's value is the rendering and hosting layer. The practice's value is the editorial and architectural layer. Both are necessary; neither replaces the other. Engagements that buy a vendor template without the editorial discipline ship empty rooms; engagements that author with editorial discipline against a generic template ship strong content with weak structure. The practice's offer is both layers.

### The version-zero shape

The actual template, ready to use, that an engagement could pull off the shelf:

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
    perStateRows: [name, visual, announced, interaction, trigger]

  - id: variants
    required: conditional
    appliesTo: [hasVisualVariants]
    generatedFromPropCombinations: true

  - id: examples
    required: true
    minExamples: 4
    maxExamples: 8
    perExampleSlots: [caption, live, code, figmaFrame]

  - id: doDont
    required: true
    minPairs: 2
    maxPairs: 8
    pairedByDimension: true

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
```

This is the template the practice ships in week 1. The engagement populates it; the client team inherits it. It is the version-zero artefact that closes 09 §1.10 and gives the practice a default Documentation deliverable to scope, defend, and improve over time.

---

## References

Primary sources (verified June 2026; URLs stable at time of writing):

- **Storybook docs** — `https://storybook.js.org/docs` for current MDX, autodocs, and component-page architecture. Storybook 9 release notes for the May 2026 changes.
- **MDX docs** — `https://mdxjs.com/` for MDX 3 syntax and frontmatter patterns.
- **Curtis, *Components as Data*** (Sep 2025) — the architectural argument for source-of-truth component data files.
- **Curtis, *Operating Design Systems*** (Sep 2023) — the documentation track in the major-release cadence.
- **Wolosin, "Design system metadata is training data"** (Indeed, Jun 2025) — the four-tier metadata loop.
- **Couldwell, *Laying the Foundations*** (2019) — "document as you go," the IKEA-without-instructions framing, name-match-across-design-and-code-and-docs.
- **Mangialardi, *Design Systems for Developers*** (2021) — ADRs and decision logs in the docs repo.
- **Figma DS x AI** (2025) — examples-before-specs, layer hygiene, AI as documentation consumer.
- **Mall, *90 Days of Design Systems*** (2023) — glossary as Discovery deliverable, Activity #25.
- **Zeroheight docs** — `https://zeroheight.com/help/` for the React Connect API and the audience-tagged sections pattern.
- **Supernova docs** — `https://supernova.io/docs` for the token-management-led approach.
- **Knapsack docs** — `https://knapsack.cloud/docs` for the enterprise-tier Code Connect and ACR aggregation.
- **Atlassian Design System** — `https://atlassian.design/components` as a public exemplar of consistent per-component templates.
- **Adobe Spectrum** — `https://spectrum.adobe.com/page/component-status/` for the conformance dossier pattern.
- **IBM Carbon** — `https://carbondesignsystem.com/components/overview/` for the strong typed relationships between components.
- **Shopify Polaris** — `https://polaris.shopify.com/components` for the editorial-discipline-led approach to per-component prose.
- **Material Web Components** — `https://material-web.dev/components/` for the spec-driven docs architecture.

Version-dependent claims dated above:

- Storybook 9 (May 2026) ships the new component-page architecture.
- MDX 3 is current; MDX 2 backwards-compatibility for legacy systems through 2026.
- Zeroheight 4.x with React Connect API mature.
- Knapsack mid-2026 release with enterprise-tier ACR aggregation.
- The Storybook a11y addon ships axe-core 4.10.x by default.
- TypeScript 5.4+ is assumed for the JSDoc-driven props-table generation.

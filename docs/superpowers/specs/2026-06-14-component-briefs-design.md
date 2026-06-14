# Component Briefs — Catalogue Design

**Status:** approved (brainstorm), pending implementation plan
**Date:** 2026-06-14
**Owner:** Adam Forrester

---

## 1. What this is

A new authoritative tier in the vault: a flat catalogue of per-component field-truth briefs at `components/`, sitting alongside the numbered files at vault root. Each brief is a single component's study — what the leading systems converge on, where they diverge, where the practice lands by default — written in the same prose-led, opinionated, first-person-plural voice as the numbered files. Briefs are the upstream artefact that feeds the per-component documentation page on a real engagement (29) and the practice's POV on the component model (03). They are not a docs page, not a spec, not a fillable form.

The catalogue exists because the vault has covered the *system-level* practice exhaustively — discovery, foundations, governance, AI, accessibility, motion, tokens, adaptive interfaces — but has nothing to reach for when a real engagement asks "we're shipping `Combobox`, what does the field say and what's our default?" Without the catalogue, every engagement re-derives that answer from scratch.

## 2. Directory and naming

- **Location:** `components/` at vault root, no underscore prefix. Signals authoritative tier.
- **File naming:** component slug, lowercase, hyphenated. `components/button.md`, `components/text-field.md`, `components/dialog.md`.
- **Flat structure:** no category subdirectories. Category lives in frontmatter (`category:`), which lets a brief belong to a category without committing the path and lets Obsidian/MCP queries filter by category later.
- **No numeric prefixes inside the directory.** Numbering catalogue entries by intake order is fragile; you reach for these by component name, not by sequence.

## 3. Brief shape — the 15-section spine

Every brief follows this sectional spine. Sections scale to component complexity — a brief on `Button` is longer than a brief on `Divider`, and that is correct. Voice and depth match the numbered files: prose-led, opinionated, citations to real systems.

1. **Framing** — what this component is, what it isn't, why systems disagree on it.
2. **Anatomy and parts** — structural model, named parts, slot vocabulary.
3. **Properties / API** — converged prop set across field leaders; divergences with reasoning.
4. **States and variants** — runtime states (rest / hover / focus-visible / pressed / disabled / loading / error / empty / read-only) vs. intentional variants (size / tone / density / emphasis); canonical matrix.
5. **Usage guidance** — when to use, when not to use, what to use instead.
6. **Accessibility** — component-specific concerns; cross-refs to 14 / 17 / 28 / 16 for general theory.
7. **Content guidelines** — labels, tone, error / empty / CTA copy patterns; cross-refs to 04.
8. **Motion and transition** — entry / exit, state transitions, reduce-motion contract; cross-refs to 18–21.
9. **Internationalization** — RTL behaviour, text expansion, locale concerns; cross-refs to 13.
10. **Naming** — what the field calls it; the practice's default; aliases consumers will reach for.
11. **Implementation notes** — framework-specific gotchas, prop-vs-slot decisions, headless-vs-opinionated tension.
12. **Related and alternative components** — typed relationships (`composes with` / `alternative to` / `supersedes` / `superseded by`).
13. **Field POV evolution** — how the leading systems' position has changed; recent shifts worth flagging.
14. **Sources cited** — field-leader systems referenced with version dates so the brief is re-auditable in 18 months.
15. **Agent-consumable schema** — a fenced YAML block representing the brief's structured content in the practice's opinionated `.ai.json` shape for this component. The schema is the seed an engagement instantiates into its actual component data file (per 30's components-as-data architecture); the brief is the source of truth, the schema is auditable against the prose. See §3.1 below.

### 3.1 The agent-consumable schema (§15)

This section is the bridge between the brief and the AI-consumer audience the vault has spent 15 / 25 / 29 / 30 specifying. The principle is the one 30 makes explicit: one source of truth wins. The brief is the source; the §15 schema is a structured projection of the prose, not a parallel artefact. If §3 (Properties / API) says a Button's `tone` prop has values `neutral | critical | success`, the §15 schema says the same thing in machine-consumable form. They cannot diverge; if they do, the brief has failed its self-review.

**What the schema covers.** A first-pass shape, free-form YAML, covering:

- **Identity** — `id`, `name`, `aliases`, `category`, `status`.
- **API** — props with `type`, `default`, `required`, `deprecated`, one-line `description`.
- **Composition** — `composes-with`, `alternative-to`, `supersedes`, `superseded-by` as typed arrays of component ids.
- **Accessibility** — `wcag-criteria` (the SC ids the component participates in), `aria-attributes`, `keyboard-model`, `focus-behavior`. Mirrors the 17-accessibility-annotation-contract per-concern shape.
- **States** — named runtime states with announced-state notes where relevant.
- **Variants** — named intentional variants with the prop combinations that produce each.
- **Content** — `label-pattern`, `error-pattern`, `empty-pattern` where applicable.

**Free-form first, formalise later.** The first ~5 briefs use free-form YAML and let the shape stabilise through real use. Once the shape has settled, the schema is formalised — versioned, validated in CI, lives at `components/_schema.md` (or `_schema.json` if that fits the eventual MCP server shape better). Pre-formalising before the briefs exist is exactly the trap 30 warns against: building the pipeline before the data has shape.

**Why this lives in the brief, not as a companion file.** A `components/<slug>.ai.json` paired with `<slug>.md` would split the source of truth, double maintenance, and require lockstep updates that nothing in the vault enforces. Embedding the schema as a fenced YAML block keeps the prose and the structured projection literally adjacent on the page — a reviewer reading section 3 and section 15 can see the divergence. For the eventual MCP server (per 15 §… and the longer-term plan), an extractor parsing fenced ` ```yaml schema ` blocks from `components/*.md` is a small piece of code; the file-coupling discipline is the harder part, and embedding solves it for free.

**Where the schema does and does not bind the engagement.** The §15 schema is the practice's *opinionated default*, not a contract a real engagement must adopt verbatim. Per 30, the engagement's component data file is the source of truth in *its* codebase; the brief's §15 is the seed the engagement copies and adapts. The brief documents what the practice would ship if starting from scratch; the engagement's reality (existing component model, framework choice, brand-specific extensions) overrides where it has to. This is the same principle the brief follows for all other sections.

### Frontmatter

Every brief carries:

```yaml
---
okf_version: "0.1"
type: component-brief
title: <Component Name>
description: <one-line hook>
tags: [components, <category>]
category: <Foundations | Layout | Form | Navigation | Feedback | Data | Overlay>
status: <draft | stable | superseded>
aliases: [<other names the field uses>]
last-audited: YYYY-MM-DD
timestamp: YYYY-MM-DD
---
```

`last-audited` is what makes section 14 actionable — it's the trigger for re-running the research when the field has moved.

### Cross-reference style

Inline as prose, matching CLAUDE.md convention: `(See 14-accessibility §3.)` Not Obsidian wikilinks, not relative markdown links.

## 4. Research workflow

Briefs use the existing `_research/` dual-agent workspace, with one workflow accommodation for component scope.

### Per-brief decision: dual-agent or claude-only

- **Dual-agent (default)** — for any component where the field is contested (Button-the-meta-component, Combobox, Dialog, Toast, Chart, Form composites). `_research/_inbound/YYYY-MM-DD-component-<slug>/` with `prompt.md`, `external-agent.md`, `claude.md`.
- **Claude-only (allowed)** — for components where the field genuinely converges (Divider, Spinner, simple primitives). `_research/_inbound/YYYY-MM-DD-component-<slug>/` with `prompt.md` and `claude.md`. The folder still exists for paper trail.

The choice is recorded by the contents of the research folder itself — presence of `external-agent.md` means dual-agent, absence means claude-only. The folder is the audit record; no frontmatter field is needed for this.

### New companion prompt template

`_research/_component-prompt-template.md` — purpose-built for component briefs. Differs from the existing `_prompt-template.md` (which targets ~3,000-word topic syntheses) by:

- Pre-filling the 14-section spine as the required output shape.
- Pre-filling the field-leader system list (web: Polaris, Spectrum, Material 3, Carbon, Primer, Atlassian, Hydrogen, Base Web; mobile: HIG, Material 3 mobile, Fluent).
- Framing the brief as a convergence/divergence study rather than a topic survey.
- Specifying that section 14 (Sources cited) include version dates for every system referenced.

The existing `_prompt-template.md` continues to be used for topic-level research that lands in numbered files.

### Synthesis path

Default is **Path B** per `_research/README.md` — direct from raw outputs into `components/<slug>.md`, no `_synthesis/` intermediate. The brief itself is the synthesis.

**Path A** (intermediate `_synthesis/` file) is used only when the dual-agent outputs diverge enough that explicit reconciliation needs its own document before the brief can be written. Per-run judgment call.

### Promotion checklist

Once a brief lands in `components/<slug>.md`:

1. Update its entry in `components/index.md` from "not yet briefed" to a link with one-line hook and status flag.
2. Add inline cross-references from numbered files where the component is now relevant. 03-component-library always; 14 / 17 / 28 / 18 / 13 / 04 conditionally based on the component.
3. The `_inbound/` folder for that component stays as audit record.

## 5. Scope and intake

The catalogue's value depends on *legible coverage*. The intake model:

- **Curated target list, freely re-ordered.** The full target set lives in `components/index.md` from day one with status flags (not-yet-briefed / draft / stable / superseded). Intake order is engagement-driven, but the gap is always visible.
- **Engagement need pulls a brief forward.** When a real engagement needs `Combobox`, that brief moves to the front of the queue.
- **No upfront bulk briefing.** Briefs are written when needed, not as a make-work project.

### Seed target list (~40 components)

**Foundations:** Icon, Avatar, Badge, Tag, Divider, Spinner, Skeleton

**Layout:** Box, Stack, Grid, Card, Section

**Form:** Button, Text Field, Textarea, Select, Combobox, Checkbox, Radio, Switch, Slider, Date Picker, File Upload, Form (composite)

**Navigation:** Link, Tabs, Breadcrumbs, Pagination, Menu, Side Navigation

**Feedback:** Toast, Banner / Alert, Progress, Empty State, Inline Message

**Data:** Table, List, Tree, Chart (composite)

**Overlay:** Dialog / Modal, Drawer, Popover, Tooltip

Mobile-only and platform-specific components (Action Sheet, Bottom Sheet, Segmented Control) are appended as the catalogue matures. The seed list is not fixed forever; it's the baseline coverage shape.

## 6. Indexing and cross-references

### `components/index.md`

Its own OKF root index. Frontmatter:

```yaml
---
okf_version: "0.1"
type: practice-area
title: Component Briefs
description: Field-truth studies of individual components — how the leading systems handle them, where they converge, where they diverge, and the practice's defaults.
tags: [index, components]
timestamp: YYYY-MM-DD
---
```

Structure:

1. **How this catalogue works** — short opening section (300–500 words) covering: what a brief is and isn't, the dual-agent / claude-only choice, the research folder convention, the promotion flow. This is the operational meta-doc; it lives here rather than as a numbered file because it describes the directory it sits in.
2. **The catalogue** — sectioned by the seven categories. Each entry one line: component name → one-line hook → status flag. Drafted/stable briefs link to their file; not-yet-briefed components are listed without a link with a `scope:` note describing what the brief will cover.

### Vault root `index.md`

A new section *Component briefs*, placed after *Extensions* and before *Vocabulary*. One line linking to `components/index.md` plus a one-line description. Not 40 individual links at root — the catalogue index does that work.

### Cross-references from numbered files

- **03-component-library** — new section near the end, *Per-component briefs*, that names the catalogue and links to `components/index.md`. The seam between system-level component model (03) and individual-component briefs (catalogue) is explicit.
- **29-per-component-documentation-template** — inline cross-reference noting that the catalogue is the *upstream* artefact a component brief feeds the delivered docs page.
- **30-generated-from-data-documentation** — inline cross-reference noting that the brief's §15 (Agent-consumable schema) is the *seed* an engagement instantiates into its actual component data file. The brief is the practice's opinionated default; the engagement's data file is its real source of truth.
- **15-ai-in-ds** — inline back-reference noting that the briefs are the AI-readable per-component layer the four-layer AI documentation stack assumes exists. The §15 schemas are what an MCP server eventually serves to agents.
- **25-ai-aware-patterns-and-conversational-ui** — back-reference *only when a brief lands that covers an AI-pattern component* (chat-message, citation, refusal-state, tool-call surface, streaming-response container). Not all briefs touch 25.
- **14, 17, 28, 18, 13, 04** — inline back-references added *only when a brief lands that's relevant*, per the existing convention. Not retrofitted upfront.
- **09-gaps-and-open-questions** — one-line update marker noting the catalogue exists, not a rewrite. As briefs land, parts of §1.10 close.

### Why the meta-doc is not a numbered file

There is a temptation to write `31-component-briefs.md` describing this whole design. I'm explicitly choosing against that. Numbered files are the practice's POV on *topics*; this is operational mechanics for a directory. It belongs at the top of `components/index.md`, not as a 25KB numbered file. Keeps the numbered surface clean and the meta-doc next to the thing it describes.

## 7. What this design explicitly does not do

- **Does not duplicate 29.** The brief is upstream of the docs page. The brief is field-truth and POV; the docs page is the artefact the practice ships to a client.
- **Does not re-litigate 03.** The brief is per-component; 03 is the system-level component model.
- **Does not re-state accessibility / motion / i18n theory.** Briefs cross-reference 14 / 17 / 28 / 16 / 18 / 13 for general theory and add only the component-specific concerns.
- **Does not introduce category subdirectories.** Category is metadata.
- **Does not prescribe brief length.** Briefs scale to component complexity.
- **Does not bulk-brief upfront.** Engagement need pulls briefs forward; the catalogue grows deliberately, not opportunistically.
- **Does not formalise the §15 schema before the briefs exist.** The first ~5 briefs use free-form YAML; the schema is formalised after the shape has stabilised through real use, not before.
- **Does not split source of truth between the brief and a companion `.ai.json` file.** The schema is embedded in the brief. One source, prose and structure adjacent on the page.

## 8. Open work for the implementation plan

The implementation plan should cover, in order:

1. Create `components/` directory and `components/index.md` skeleton with the seed target list and "How this catalogue works" preamble.
2. Create `_research/_component-prompt-template.md`. The template must require §15 (Agent-consumable schema) as part of the output and must specify free-form YAML for now.
3. Add the *Component briefs* section to vault root `index.md`.
4. Add the *Per-component briefs* cross-reference section to `03-component-library.md`.
5. Add the inline cross-reference in `29-per-component-documentation-template.md`.
6. Add the inline cross-reference in `30-generated-from-data-documentation.md` noting that the brief's §15 is the seed.
7. Add the inline cross-reference in `15-ai-in-ds.md` noting the catalogue's §15 schemas are the per-component layer the four-layer stack assumes.
8. Add the one-line marker in `09-gaps-and-open-questions.md` §1.10.
9. Commit the catalogue scaffolding as one editorial commit, separate from the first actual brief.
10. (Out of scope for this plan) Write the first brief — the component is to be chosen by Adam based on engagement need, and the act of writing it is itself the validation that the template works. After ~5 briefs, formalise the §15 schema as a separate task.

## 9. Voice and editorial discipline

Briefs are written like the numbered files, not like a docs site:

- Declarative and opinionated. Avoid hedging.
- Avoid bullet-point dumps where prose is doing the work.
- Citations in parens with source + version, e.g. `(Polaris 12.0, 2025)`, `(Material 3, 2024)`, `(Spectrum 2024.4)`.
- No emoji.
- Bolded lead-ins (`**Like this.**`) inside paragraphs are fine and match the existing style.
- First-person plural for the practice's POV; third person for what the field does.

The first brief written is the calibration point for the rest. Once the first brief feels right, the template — and the prompt template — can be tightened based on what was actually load-bearing.

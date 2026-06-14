# Component Briefs Catalogue — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the new authoritative `components/` catalogue tier in the vault: directory + index + companion prompt template + cross-references from numbered files. Out of scope: writing the first brief itself.

**Architecture:** Editorial work in a markdown vault. New flat directory `components/` at vault root with its own OKF-conformant `index.md`. New companion prompt template at `_research/_component-prompt-template.md`. Inline cross-references added to six numbered files (root `index.md`, 03, 09, 15, 29, 30). One commit per logical unit.

**Tech Stack:** Markdown + YAML frontmatter (Open Knowledge Format v0.1). Obsidian vault. No build step, no tests, no code. Verification = reading the file after editing.

**Reference:** Spec at `docs/superpowers/specs/2026-06-14-component-briefs-design.md`. Vault conventions in `CLAUDE.md` at the repo root.

---

## Editorial discipline (read first)

This plan is editorial, not code. Three rules carry throughout:

1. **Voice match.** Numbered files use first-person plural ("we", "our practice"), prose-led, opinionated, no emoji, no hedging. Bolded lead-ins (`**Like this.**`) inside paragraphs are fine. Read a recently-edited section in `29-per-component-documentation-template.md` if calibration is needed.
2. **Cross-reference style.** Inline as prose, e.g. `(See 14-accessibility §3.)` — never Obsidian wikilinks (`[[…]]`), never relative markdown links between numbered files. The vault root `index.md` is the only exception; it uses absolute markdown links because it's the navigation surface.
3. **Frontmatter scope.** Every file inside `components/` carries OKF v0.1 frontmatter. Files in `_research/` do not (per CLAUDE.md "Frontmatter is scoped to numbered files (and the root `index.md`). Underscore-prefixed directories — `_research/`, `_notes/`, `_source-text/` — stay frontmatter-free.").

---

## File map

What gets created or modified, and the responsibility of each:

**Created:**
- `components/index.md` — OKF root index for the catalogue tier. Carries the "How this catalogue works" preamble (300–500 words) and the seed target list with status flags.
- `_research/_component-prompt-template.md` — purpose-built prompt template for component-brief research runs. Mirrors the shape of `_research/_prompt-template.md` but pre-fills the 15-section brief spine, the field-leader systems list, and the §15 schema requirement.

**Modified (cross-references):**
- `index.md` (vault root) — new section *Component briefs* placed after *Extensions*, before *Vocabulary*.
- `03-component-library.md` — new H2 *Per-component briefs* near the end, between *Tensions and open questions* and *Failure modes specific to this phase*.
- `29-per-component-documentation-template.md` — short inline cross-reference noting the catalogue is the upstream artefact.
- `30-generated-from-data-documentation.md` — short inline cross-reference noting the brief's §15 is the seed.
- `15-ai-in-ds.md` — short inline cross-reference noting the catalogue's §15 schemas are the per-component layer the four-layer stack assumes.
- `09-gaps-and-open-questions.md` — one-line marker added to §1.10 noting the catalogue exists.

**Untouched in this plan (explicitly out of scope):**
- Any file inside `components/` other than `index.md`. The first actual brief is its own task, owner-assigned.
- 14-accessibility, 17-accessibility-annotation-contract, 28-web-accessibility-implementation, 18-motion-foundations, 13-internationalization-and-rtl, 04-documentation, 25-ai-aware-patterns-and-conversational-ui — these get back-references *only when an actual brief lands* per the spec's "not retrofitted upfront" rule.

---

## Task 1: Create `components/index.md`

**Files:**
- Create: `components/index.md`

- [ ] **Step 1.1: Create the directory and write the index file**

```bash
mkdir -p components
```

Then write the file. The full content is below — copy verbatim. The `timestamp` field is today's date in ISO format.

```markdown
---
okf_version: "0.1"
type: practice-area
title: Component Briefs
description: Field-truth studies of individual components — how the leading systems handle them, where they converge, where they diverge, and the practice's defaults. Upstream of the per-component docs page (29) and the practice's POV on the component model (03).
tags: [index, components]
timestamp: 2026-06-14
---

# Component Briefs

A flat catalogue of per-component field-truth briefs. Each brief is a single component's study — what the leading systems converge on, where they diverge, and where the practice lands by default. Briefs are the upstream artefact a real engagement uses to populate its per-component docs page (see 29-per-component-documentation-template) and to seed its component data file (see 30-generated-from-data-documentation §15 schemas). The catalogue is the practice's opinionated default; the engagement's reality overrides where it has to.

---

## How this catalogue works

**Brief shape.** Every brief follows a 15-section spine: framing, anatomy, properties/API, states and variants, usage guidance, accessibility, content guidelines, motion, internationalization, naming, implementation notes, related and alternative components, field POV evolution, sources cited, and an embedded agent-consumable schema. Sections scale to component complexity — a brief on `Button` will be longer than a brief on `Divider`, and that is correct. Voice and depth match the numbered files: prose-led, opinionated, citations to real systems with version dates.

**Research workflow.** Briefs use the existing `_research/` dual-agent workspace with a purpose-built prompt template at `_research/_component-prompt-template.md`. Dual-agent is the default for any component where the field is contested; claude-only is allowed for components where the field genuinely converges (Divider, Spinner, simple primitives). The choice is recorded by the contents of the research folder — presence of `external-agent.md` means dual-agent, absence means claude-only.

**Synthesis path.** Default is direct from raw outputs into `components/<slug>.md`. The brief itself is the synthesis. An intermediate `_research/_synthesis/` file is used only when dual-agent outputs diverge enough to need explicit reconciliation.

**Promotion.** When a brief lands: update its entry in this index from "not yet briefed" to a link with one-line hook and status flag; add inline cross-references from the numbered files where the component is now relevant (03 always; 14 / 17 / 28 / 16 / 18 / 13 / 04 / 25 / 30 conditionally); leave the `_inbound/` folder in place as audit record.

**The §15 schema.** Section 15 of every brief is a fenced YAML block — the practice's opinionated default `.ai.json` shape for the component. The schema is a structured projection of the prose, not a parallel artefact; if section 3 says `tone: neutral | critical | success`, the schema says the same thing in machine-consumable form. The first ~5 briefs use free-form YAML and let the shape stabilise through real use; once the shape has settled, the schema is formalised.

**Intake.** Engagement need pulls a brief forward. The seed target list below covers ~40 components across the seven categories. The list is the discipline; the order is the flexibility. Components without briefs are listed with a `scope:` note describing what the brief will cover.

---

## The catalogue

### Foundations

- **Icon** — *not yet briefed.* `scope: glyph sizing model, semantic vs. decorative split, accessible name vs. aria-hidden, the icon-only-button anti-pattern, the bicolour/duotone trend.`
- **Avatar** — *not yet briefed.* `scope: image vs. initials vs. fallback, group/stack composition, accessible name patterns, presence-indicator overlay.`
- **Badge** — *not yet briefed.* `scope: count vs. dot vs. status, the announcement contract, placement relative to host, color-as-sole-carrier failure.`
- **Tag** — *not yet briefed.* `scope: chip vs. tag vs. pill terminology, removable vs. static, multi-select interaction model, the tag-vs-badge boundary.`
- **Divider** — *not yet briefed.* `scope: presentational vs. semantic separator, vertical vs. horizontal, inset and full-bleed variants, the role="separator" decision.`
- **Spinner** — *not yet briefed.* `scope: indeterminate vs. determinate, when to use vs. skeleton, accessible loading announcement, the reduce-motion contract.`
- **Skeleton** — *not yet briefed.* `scope: shape-matched vs. block placeholders, animation discipline, accessibility (aria-busy on parent, hidden from AT), the spinner-vs-skeleton decision.`

### Layout

- **Box** — *not yet briefed.* `scope: the polymorphic primitive, prop-driven vs. style-driven, the as-prop contract, the box-as-escape-hatch trap.`
- **Stack** — *not yet briefed.* `scope: vertical vs. horizontal, gap vs. margin, divider-between, the alignment-and-justification matrix.`
- **Grid** — *not yet briefed.* `scope: container queries vs. viewport queries, named-track vs. auto-flow, the 12-column legacy, responsive prop shapes.`
- **Card** — *not yet briefed.* `scope: header / body / footer slot model, interactive-card vs. card-with-actions, the link-on-card-vs-button-in-card decision, elevation tokens.`
- **Section** — *not yet briefed.* `scope: structural vs. visual section, the heading-level contract, landmark roles, full-bleed vs. constrained.`

### Form

- **Button** — *not yet briefed.* `scope: tone / size / shape / emphasis matrix, the icon-button vs. icon-with-label boundary, loading state, link-vs-button semantics, destructive-action confirmation.`
- **Text Field** — *not yet briefed.* `scope: label / placeholder / helper / error stack, the autocomplete contract, prefix/suffix slots, password-reveal pattern, validation timing.`
- **Textarea** — *not yet briefed.* `scope: auto-resize behaviour, character counter, paste-handling, the textarea-vs-rich-text boundary.`
- **Select** — *not yet briefed.* `scope: native vs. custom, multi-select model, group/option structure, the select-vs-combobox decision.`
- **Combobox** — *not yet briefed.* `scope: ARIA 1.3 combobox pattern, async option loading, free-text vs. enumerated, multi-select, the popover positioning model.`
- **Checkbox** — *not yet briefed.* `scope: indeterminate state, group composition, the label-association contract, alignment with text.`
- **Radio** — *not yet briefed.* `scope: group as required unit, fieldset/legend pattern, the radio-vs-segmented-control decision.`
- **Switch** — *not yet briefed.* `scope: switch vs. checkbox semantics, the immediate-effect contract, accessible labelling, on/off vs. labelled-state.`
- **Slider** — *not yet briefed.* `scope: single-thumb vs. range, step model, keyboard increment, value-display pattern, the slider-vs-input decision.`
- **Date Picker** — *not yet briefed.* `scope: input vs. calendar, single vs. range, locale and RTL, the masked-input contract, accessibility patterns.`
- **File Upload** — *not yet briefed.* `scope: drag-and-drop vs. browse, multi-file, progress and error handling, accessibility, the file-list slot model.`
- **Form (composite)** — *not yet briefed.* `scope: the form as compositional unit, validation strategies, error summary pattern, submit-and-recovery flow, autofill contract.`

### Navigation

- **Link** — *not yet briefed.* `scope: link vs. button semantics, internal vs. external, visited state, focus visibility, the underline-discipline.`
- **Tabs** — *not yet briefed.* `scope: ARIA tabs pattern, manual vs. automatic activation, panel association, scroll/overflow handling, vertical orientation.`
- **Breadcrumbs** — *not yet briefed.* `scope: separator semantics, current-page convention, truncation/overflow, the breadcrumb-vs-back-button decision.`
- **Pagination** — *not yet briefed.* `scope: numbered vs. load-more vs. infinite, current-page announcement, the truncation pattern, accessibility.`
- **Menu** — *not yet briefed.* `scope: ARIA menu pattern, submenu navigation, the menu-vs-listbox-vs-combobox confusion, click-outside dismissal, focus management.`
- **Side Navigation** — *not yet briefed.* `scope: collapsed vs. expanded, multi-level structure, the active-state contract, mobile transformation, accessible landmark.`

### Feedback

- **Toast** — *not yet briefed.* `scope: role="status" vs. role="alert", auto-dismiss timing, queue behaviour, the accessible-name vs. body distinction, action-in-toast pattern.`
- **Banner / Alert** — *not yet briefed.* `scope: severity model, dismissibility, the inline-banner vs. page-banner distinction, action affordances, accessibility.`
- **Progress** — *not yet briefed.* `scope: determinate vs. indeterminate, accessible value announcement, the progress-vs-spinner decision, multi-step progress.`
- **Empty State** — *not yet briefed.* `scope: illustration / heading / body / action structure, the empty-vs-error vs. empty-vs-loading boundaries, content patterns.`
- **Inline Message** — *not yet briefed.* `scope: error vs. info vs. success, association with form fields, the live-region vs. static decision, content patterns.`

### Data

- **Table** — *not yet briefed.* `scope: column model, sort/filter/select, sticky headers, responsive transformation, virtualisation, accessibility patterns, the table-vs-list decision.`
- **List** — *not yet briefed.* `scope: ordered vs. unordered semantics, list-with-actions, the list-vs-table decision, virtualisation.`
- **Tree** — *not yet briefed.* `scope: ARIA tree pattern, multi-select, expand/collapse model, virtualisation, the tree-vs-nested-list decision.`
- **Chart (composite)** — *not yet briefed.* `scope: encoding rules, color-not-sole-carrier, axis and legend conventions, accessible name and description templates, sonification/table-fallback. (See 09-gaps-and-open-questions §5.2.)`

### Overlay

- **Dialog / Modal** — *not yet briefed.* `scope: focus-trap and return, inert scope, Escape and overlay-click behaviour, native <dialog>+showModal(), z-index and scroll-lock, the modal-vs-drawer decision.`
- **Drawer** — *not yet briefed.* `scope: edge-anchored placement, the drawer-vs-modal-vs-popover decision, focus management, mobile vs. desktop.`
- **Popover** — *not yet briefed.* `scope: trigger model, positioning (Floating UI / popover API), dismissibility, the popover-vs-tooltip-vs-menu boundaries.`
- **Tooltip** — *not yet briefed.* `scope: hover/focus trigger, the WCAG 1.4.13 contract, persistence and dismissibility, the tooltip-as-only-affordance anti-pattern.`

---

## Status flags

- *not yet briefed* — entry exists, no research run
- *draft* — `_research/_inbound/` folder exists, brief in `_synthesis/` or being authored
- *stable* — brief lives in `components/<slug>.md` and reflects current field state
- *superseded* — replaced by another brief; superseding slug noted inline
```

- [ ] **Step 1.2: Verify the file exists and the frontmatter validates**

Run: `head -10 components/index.md`
Expected: the `---`-delimited frontmatter block, then `# Component Briefs`. Confirm the seven `okf_version`, `type`, `title`, `description`, `tags`, `timestamp` fields are all present.

Run: `wc -l components/index.md`
Expected: between 100 and 130 lines.

- [ ] **Step 1.3: Commit**

```bash
git add components/index.md
git commit -m "Add components/ catalogue index with seed target list

Sets up the new authoritative tier per the component-briefs spec.
Index carries the 'How this catalogue works' preamble and the ~40-
component seed list across the seven categories, each entry with a
scope note describing what the brief will cover."
```

---

## Task 2: Create `_research/_component-prompt-template.md`

**Files:**
- Create: `_research/_component-prompt-template.md`

The companion template mirrors the shape of `_research/_prompt-template.md` (read it for calibration before writing) but is purpose-built for the 15-section component brief and pre-fills the field-leader systems.

- [ ] **Step 2.1: Write the template**

Create `_research/_component-prompt-template.md` with the following content:

```markdown
# Component-brief research prompt template

Use this template for component-brief research runs. The same prompt goes to both agents (the external one and Claude in this repo) when running dual-agent. For claude-only runs, the same template is used; only the external-agent output is omitted.

This is a companion to `_prompt-template.md`. The original template targets ~3,000-word topic surveys that land in numbered files. This template targets per-component briefs that land at `components/<slug>.md`.

---

## When to use which template

- **`_prompt-template.md`** — topic-level research that lands in a numbered file. Practice-area surveys (accessibility, motion, tokens, AI patterns).
- **`_component-prompt-template.md`** — single-component briefs that land in `components/<slug>.md`. Field-truth studies of one component.

If unsure, ask: is the output a numbered file or a component brief? That answers it.

---

## When to deviate

The 15-section spine is the contract. Deviation is rare, and is recorded in the synthesis. Reasons that justify deviation:

- **Foundational primitive** — for `Box`, `Stack`, `Divider`, sections 4 (states/variants) and 8 (motion) collapse to one paragraph each. The spine still ships; the depth scales.
- **Non-web component** — for components with no web equivalent (Action Sheet, Bottom Sheet on mobile), section 11 (implementation notes) shifts to platform-specific frameworks; section 9 (i18n) becomes platform-locale concerns.

For everything else, follow the spine.

---

## The template

Copy from this section. Replace `{{double-braced}}` placeholders. Remove any `[guidance: ...]` comments before sending.

```
You are researching the {{Component Name}} component for a senior
design systems practitioner at a digital agency. The output is a
field-truth study of how the leading design systems handle this
component — what they converge on, where they diverge, and what
the practice's opinionated default should be when starting from
scratch.

This is not an introductory guide. Assume the reader knows what a
{{component}} is, knows what a design system is, and has shipped
multiple component libraries. Explain the non-obvious — the prop
choices field leaders disagree on, the accessibility decisions that
are still contested, the implementation traps that recur across
codebases.

Field-leader systems to survey (web, unless the component is
mobile-first):

- Shopify Polaris
- Adobe Spectrum
- Google Material 3
- IBM Carbon
- GitHub Primer
- Atlassian Design System
- Shopify Hydrogen (where it diverges from Polaris)
- Base Web (Uber)

Mobile reference (where the component has a mobile dimension):

- Apple Human Interface Guidelines
- Material 3 (Compose / mobile)
- Microsoft Fluent

Cite each system referenced with a version date — e.g., (Polaris
12.0, 2025), (Material 3, 2024), (Spectrum 2024.4). Currency
matters; section 14 of the brief is the auditable record.

Output structure — follow this 15-section spine:

1. Framing — what this component is, what it isn't, why systems
   disagree on it.
2. Anatomy and parts — structural model, named parts, slot
   vocabulary.
3. Properties / API — converged prop set across field leaders;
   divergences with reasoning.
4. States and variants — runtime states (rest / hover / focus-
   visible / pressed / disabled / loading / error / empty / read-
   only) vs. intentional variants (size / tone / density /
   emphasis); canonical matrix.
5. Usage guidance — when to use, when not to use, what to use
   instead.
6. Accessibility — component-specific concerns. The reader has
   read 14-accessibility, 17-accessibility-annotation-contract,
   and 28-web-accessibility-implementation; do not re-state the
   theory; identify what is specific to this component (ARIA
   pattern, keyboard model, focus contract, AT announcements,
   the WCAG SC the component participates in).
7. Content guidelines — labels, tone, error / empty / CTA copy
   patterns.
8. Motion and transition — entry / exit, state transitions,
   reduce-motion contract.
9. Internationalization — RTL behaviour, text expansion, locale
   concerns.
10. Naming — what the field calls it; the practice's default;
    aliases consumers will reach for.
11. Implementation notes — framework-specific gotchas, prop-vs-
    slot decisions, headless-vs-opinionated tension.
12. Related and alternative components — typed relationships
    (composes with / alternative to / supersedes / superseded by).
13. Field POV evolution — how the leading systems' position has
    changed; recent shifts worth flagging.
14. Sources cited — every system referenced, with version dates.
15. Agent-consumable schema — a fenced YAML block representing
    the brief's structured content as the practice's opinionated
    `.ai.json` shape for this component. Free-form YAML; the
    schema is the structured projection of sections 1–13. Cover:
    identity (id, name, aliases, category, status), API (props
    with type/default/required/deprecated/description),
    composition (composes-with, alternative-to, supersedes,
    superseded-by), accessibility (wcag-criteria, aria-attributes,
    keyboard-model, focus-behavior), states, variants, content
    (label-pattern, error-pattern, empty-pattern). The schema
    must not contradict any prose section above; if it does, the
    prose wins and the schema is wrong.

Output format: Structured markdown. Use H2 headings that match
the numbered spine above. Synthesize findings — do not list
sources mechanically. Where the field has consensus, state it
clearly; where decisions are context-dependent, provide decision
frameworks rather than declaring a winner. Where claims depend on
current platform state — feature names, version flags, ARIA
attributes that recently changed — date them and note the
verification path.

Depth: Expert audience. Do not explain {{the basic concept of
this component}} — explain {{the non-obvious application or the
implementation trade-off that field leaders still disagree on}}.
```

---

## Filing a completed run

Same convention as `_prompt-template.md`:

```
_research/_inbound/YYYY-MM-DD-component-<slug>/
  prompt.md           the prompt verbatim
  external-agent.md   raw output from the other agent (dual-agent only)
  claude.md           Claude's run of the same prompt
```

Slug convention: lowercase, hyphenated, prefixed with `component-`. Examples: `2026-07-01-component-button`, `2026-07-12-component-text-field`, `2026-07-20-component-toast`.

The presence of `external-agent.md` records that the run was dual-agent; its absence records that the run was claude-only. No frontmatter field encodes this — the folder is the audit.

After the brief lands at `components/<slug>.md`, the `_inbound/` folder stays in place as audit record. If a `_synthesis/` intermediate was used, move it to `_research/_archive/` after promotion.

---

## What this template does not include

- **House voice.** The vault's first-person plural enters at the synthesis step (when writing the brief), not at the agent step.
- **Vault-specific cross-references.** The agents do not see numbered files; the brief author adds the `(See 14-accessibility §3.)`-style cross-references during synthesis.
- **The §15 schema's final shape.** Free-form YAML for the first ~5 briefs. The shape stabilises through real use; only then is the schema formalised into `components/_schema.md`.
```

- [ ] **Step 2.2: Verify the file exists and contains the 15-section spine**

Run: `wc -l _research/_component-prompt-template.md`
Expected: between 110 and 150 lines.

Run: `grep -c "^[0-9][0-9]*\\. " _research/_component-prompt-template.md`
Expected: at least 15 (the spine numbered list).

- [ ] **Step 2.3: Commit**

```bash
git add _research/_component-prompt-template.md
git commit -m "Add _research/_component-prompt-template.md

Companion to _prompt-template.md, purpose-built for component-brief
research runs. Pre-fills the 15-section spine, the field-leader
systems list, and the §15 agent-consumable schema requirement."
```

---

## Task 3: Add *Component briefs* section to vault root `index.md`

**Files:**
- Modify: `index.md` — insert a new section after *Extensions*, before *Vocabulary*.

The vault root index uses absolute markdown links (e.g., `/30-…`) per its existing convention. Match that style.

- [ ] **Step 3.1: Locate the insertion point**

Run: `grep -n "^## " index.md`
Expected output (approximately):
```
14:## Cross-cutting
20:## Engagement phases
31:## Gaps
35:## Extensions
59:## Vocabulary
63:## Working directories
```

The new section *Component briefs* goes between *Extensions* (which ends with the link to `30-…`) and *Vocabulary*.

- [ ] **Step 3.2: Edit the file**

Find the line `## Vocabulary` and insert the following block immediately above it (i.e., before the line `## Vocabulary`), preserving the blank-line spacing convention used elsewhere in the file:

```markdown
## Component briefs

* [Component Briefs Catalogue](/components/index.md) - Field-truth studies of individual components — how the leading systems handle them, where they converge, where they diverge, and the practice's defaults. Upstream of 29's docs page and 30's data file.

```

- [ ] **Step 3.3: Verify the section landed and the existing structure is intact**

Run: `grep -n "^## " index.md`
Expected: the new `## Component briefs` line appears between `## Extensions` and `## Vocabulary`. The other H2s are unchanged.

Run: `grep -A 1 "^## Component briefs" index.md`
Expected: the heading and the bullet linking to `/components/index.md`.

- [ ] **Step 3.4: Commit**

```bash
git add index.md
git commit -m "Add Component briefs section to vault root index

One-line link to components/index.md, placed between Extensions
and Vocabulary. The catalogue index does the per-component routing."
```

---

## Task 4: Add *Per-component briefs* section to `03-component-library.md`

**Files:**
- Modify: `03-component-library.md` — insert a new H2 between *Tensions and open questions* (currently line 195) and *Failure modes specific to this phase* (currently line 205).

03 is the practice's POV on the component model. The catalogue is the practice's POV on individual components. The seam between them needs to be explicit, in 03's own voice (first-person plural, prose-led, no bullet dump).

- [ ] **Step 4.1: Confirm the insertion point**

Run: `grep -n "^## " 03-component-library.md`
Expected: includes the lines `Tensions and open questions`, `Failure modes specific to this phase`. The new section sits between them.

- [ ] **Step 4.2: Edit the file**

Find the line that begins the *Failure modes specific to this phase* section (`## Failure modes specific to this phase`) and insert the following block immediately above it. Preserve a single blank line above and below the new H2.

```markdown
## Per-component briefs

03 is the practice's POV on the *component model* — anatomy, properties, composition, the configure-and-compose framing, the decision rules that apply across components. The model is system-level; it tells us *how* to think about any component but stops short of telling us how to think about *this* component. The seam between system-level model and per-component reasoning is where every engagement currently re-derives the same field-truth study from scratch — what does Polaris do, what does Spectrum do, what does Material call this, where does Carbon land on the API.

The **components/** catalogue closes that seam. It is a flat directory of per-component briefs, each one a 15-section field-truth study of a single component: framing, anatomy, properties/API, states and variants, usage guidance, accessibility, content guidelines, motion, internationalization, naming, implementation notes, related components, field POV evolution, sources cited, and an embedded agent-consumable schema. Briefs are written in the same prose-led, opinionated, first-person-plural voice as the numbered files. They are not docs pages — that is what 29's template ships. They are the *upstream* artefact: the practice's opinionated default the docs page is built from and the engagement's `.ai.json` is seeded from. (See `components/index.md` for the catalogue and the seed target list of ~40 components across the seven categories.)

The §15 agent-consumable schema is what makes the catalogue load-bearing for the AI-readiness story. Per 30, the engagement's component data file is the source of truth in *its* codebase; per 15, the four-layer AI documentation stack assumes a per-component machine-readable layer exists. The brief's §15 is the seed an engagement copies and instantiates. Free-form YAML for the first ~5 briefs; the schema formalises after the shape has stabilised through real use.

```

- [ ] **Step 4.3: Verify the section landed in the right place**

Run: `grep -n "^## " 03-component-library.md`
Expected: a new line `## Per-component briefs` appears after `## Tensions and open questions` and before `## Failure modes specific to this phase`.

Run: `grep -B 1 -A 1 "^## Per-component briefs" 03-component-library.md`
Expected: shows the section is sandwiched between the two adjacent H2s with appropriate whitespace.

- [ ] **Step 4.4: Update the file's `timestamp` frontmatter**

Open `03-component-library.md` and change the `timestamp:` field at the top of the file to `2026-06-14`.

- [ ] **Step 4.5: Commit**

```bash
git add 03-component-library.md
git commit -m "03: add Per-component briefs section linking to components/

The system-level component model (03) and the per-component briefs
(components/) sit on opposite sides of an explicit seam. The new H2
names that seam, points to the catalogue, and surfaces the §15
schema as the bridge to 15 and 30."
```

---

## Task 5: Add cross-reference in `29-per-component-documentation-template.md`

**Files:**
- Modify: `29-per-component-documentation-template.md` — short inline cross-reference noting the catalogue is the upstream artefact.

29 already covers the per-component *docs page* — the artefact the practice ships to a client. The brief is upstream of that docs page. The reference should be inline, single-paragraph, in 29's voice. The natural home is in §1 ("Why the per-component template is load-bearing"), which already establishes the docs page as load-bearing; the brief-as-upstream observation strengthens that argument.

- [ ] **Step 5.1: Locate the right paragraph**

Read `29-per-component-documentation-template.md` lines 15 to 36 (the §1 section). The last paragraph before the `---` separator is the one about the "trust the docs" cliff and the "relationship to ACR / VPAT evidence." The new paragraph follows that one and precedes the `---`.

- [ ] **Step 5.2: Find the exact insertion anchor**

Run: `grep -n "relationship to ACR / VPAT evidence" 29-per-component-documentation-template.md`
Expected: one line number around 34. The paragraph extends to the next blank line; insert immediately after that paragraph and before the `---` separator that ends §1.

- [ ] **Step 5.3: Add the inline reference**

After the final paragraph of §1 and before the `---` separator that closes §1, insert this paragraph (preserve a blank line above and below):

```markdown
**The brief is upstream of the docs page.** The template described in this file is the *output* — the artefact the practice ships to a client. The *input* is the per-component brief: the field-truth study that establishes what the component is, how the leading systems handle it, and what the practice's opinionated default is. The brief is the source the docs page authors draw from; the §15 schema embedded in the brief is the seed the engagement instantiates into its component data file (per 30). Without the brief, every engagement's docs page reinvents the field survey, the prop convergence analysis, and the accessibility decision tree from scratch. (See `components/index.md` for the catalogue.)

```

- [ ] **Step 5.4: Update the file's `timestamp` frontmatter**

Change the `timestamp:` field to `2026-06-14`.

- [ ] **Step 5.5: Verify**

Run: `grep -A 2 "The brief is upstream of the docs page" 29-per-component-documentation-template.md`
Expected: shows the new paragraph and the link to `components/index.md`.

- [ ] **Step 5.6: Commit**

```bash
git add 29-per-component-documentation-template.md
git commit -m "29: cross-reference the components/ catalogue as upstream

The per-component docs page (29) is the output; the per-component
brief (components/) is the input. New paragraph at the end of §1
makes the seam explicit and points to the catalogue."
```

---

## Task 6: Add cross-reference in `30-generated-from-data-documentation.md`

**Files:**
- Modify: `30-generated-from-data-documentation.md` — short inline cross-reference noting the brief's §15 is the seed for the engagement's component data file.

30 argues that the component data file is the source of truth in a real engagement. The brief's §15 is the practice's opinionated default that the engagement's data file derives from. Natural home: §1 ("The architecture in production"), where the source-of-truth argument is established.

- [ ] **Step 6.1: Locate the right paragraph**

Read `30-generated-from-data-documentation.md` §1 (lines 15 onward). The opening paragraph of §1 establishes "the component data file is the source of truth." The new paragraph attaches to that opening, before the `### Source-format choices` subheading begins.

- [ ] **Step 6.2: Find the exact insertion anchor**

Run: `grep -n "### Source-format choices" 30-generated-from-data-documentation.md`
Expected: one line number around 19. Insert the new paragraph immediately *before* that line, preserving a blank line above and below.

- [ ] **Step 6.3: Add the inline reference**

```markdown
**The data file's seed is the per-component brief.** Per 03's *Per-component briefs* section and `components/index.md`, every component in the practice's catalogue carries a §15 *Agent-consumable schema* — a free-form YAML block that is the structured projection of the brief's prose. The brief's §15 is not the engagement's source of truth (that is the engagement's component data file in its own codebase); it is the seed that data file is instantiated from. The brief documents what the practice would ship if starting from scratch; the engagement's reality — existing component model, framework choice, brand-specific extensions — overrides where it has to. The two-source-of-truth concern dissolves once the relationship is read this way: the brief is upstream and prescriptive; the engagement's data file is downstream and authoritative for that codebase.

```

- [ ] **Step 6.4: Update the file's `timestamp` frontmatter**

Change the `timestamp:` field to `2026-06-14`.

- [ ] **Step 6.5: Verify**

Run: `grep -A 1 "data file's seed is the per-component brief" 30-generated-from-data-documentation.md`
Expected: shows the new paragraph.

- [ ] **Step 6.6: Commit**

```bash
git add 30-generated-from-data-documentation.md
git commit -m "30: cross-reference the components/ briefs as the data-file seed

The brief's §15 schema is the practice's opinionated default; the
engagement's data file is downstream and authoritative for its
codebase. New paragraph in §1 makes the upstream/downstream
relationship explicit."
```

---

## Task 7: Add cross-reference in `15-ai-in-ds.md`

**Files:**
- Modify: `15-ai-in-ds.md` — short inline cross-reference noting the catalogue's §15 schemas are the per-component layer the four-layer AI documentation stack assumes.

15 establishes the four-layer AI documentation stack and the components-as-data prerequisite. The natural home for the cross-reference is the *AI-ready DS architecture* section (around line 416) — that section is where the per-component-machine-readable layer is described, and the catalogue's §15 schemas are exactly that layer.

- [ ] **Step 7.1: Locate the right paragraph**

Run: `grep -n "^## AI-ready DS architecture" 15-ai-in-ds.md`
Expected: one line number around 416.

Read the section starting at that line. Find the paragraph that introduces the per-component machine-readable layer (`.ai.json`, MCP-served, registry-style). The new paragraph attaches at the end of that subsection, before the next H2 or H3.

- [ ] **Step 7.2: Find an unambiguous insertion anchor**

Read 15-ai-in-ds.md from the line `## AI-ready DS architecture` to the next `^## ` heading. Identify the last paragraph of that section. Insert the new paragraph as the new last paragraph of the section, immediately above the next H2 (which is *Current limits and honest assessment*).

Run: `grep -n "^## Current limits and honest assessment" 15-ai-in-ds.md`
Expected: one line number around 474. The new paragraph goes immediately above this line, preserving a blank line above and below.

- [ ] **Step 7.3: Add the inline reference**

```markdown
**The components/ catalogue is the per-component layer the four-layer stack assumes.** Per 03's *Per-component briefs* section, every brief in `components/` carries a §15 *Agent-consumable schema* — a free-form YAML block that is the practice's opinionated default `.ai.json` shape for the component. When this vault is eventually exposed via MCP (per the long-term plan in CLAUDE.md), an extractor parsing those fenced YAML blocks from `components/*.md` is the per-component-registry surface an agent actually consumes. The catalogue is what makes the AI-readiness story materially testable per-component, not aspirationally per-system.

```

- [ ] **Step 7.4: Update the file's `timestamp` frontmatter**

Change the `timestamp:` field to `2026-06-14`.

- [ ] **Step 7.5: Verify**

Run: `grep -A 1 "catalogue is the per-component layer" 15-ai-in-ds.md`
Expected: shows the new paragraph.

- [ ] **Step 7.6: Commit**

```bash
git add 15-ai-in-ds.md
git commit -m "15: cross-reference the components/ catalogue as per-component layer

The four-layer AI documentation stack assumes a per-component
machine-readable layer; the catalogue's §15 schemas are exactly
that layer. New paragraph closes AI-ready DS architecture section."
```

---

## Task 8: Add marker in `09-gaps-and-open-questions.md` §1.10

**Files:**
- Modify: `09-gaps-and-open-questions.md` — append a one-line marker to §1.10 noting the catalogue exists.

§1.10 already records the closure of two related gaps (29 and 30 in June 2026). The marker for the catalogue is one more bullet of the same shape.

- [ ] **Step 8.1: Confirm the section structure**

Run: `sed -n '69,90p' 09-gaps-and-open-questions.md`
Expected: shows the §1.10 *Documentation IA and templates* section with its existing four bullets ending in the 30 commitment.

- [ ] **Step 8.2: Find the exact anchor**

Run: `grep -n "next engagement actually itemising the pipeline" 09-gaps-and-open-questions.md`
Expected: one line number around 73. The new bullet is appended after the bullet on that line (which is the last bullet of §1.10 today) and before the next H3 (`### 1.11 Glossary`).

- [ ] **Step 8.3: Append the marker**

Find the bullet ending with "absorbing it as overhead." (the last bullet of §1.10) and insert this new bullet immediately after it, preserving the existing bullet-list formatting:

```markdown
- **Per-component field-truth gap closed by `components/` catalogue (June 2026).** The new authoritative tier ships ~40 per-component briefs across the seven categories. Each brief is a 15-section field-truth study (framing / anatomy / properties / states / usage / accessibility / content / motion / i18n / naming / implementation / related / POV evolution / sources / agent-consumable schema). The §15 schema is the seed an engagement instantiates into its component data file (per 30). Briefs are written through the existing `_research/` dual-agent workflow with a purpose-built prompt template at `_research/_component-prompt-template.md`. The catalogue is the upstream artefact 29's docs page is built from. Intake is engagement-driven; gap visibility lives in `components/index.md`.
```

- [ ] **Step 8.4: Update the file's `timestamp` frontmatter**

Change the `timestamp:` field at the top of `09-gaps-and-open-questions.md` to `2026-06-14`.

- [ ] **Step 8.5: Verify**

Run: `grep -A 1 "field-truth gap closed by" 09-gaps-and-open-questions.md`
Expected: shows the new bullet.

Run: `sed -n '69,90p' 09-gaps-and-open-questions.md`
Expected: §1.10 now has five bullets; §1.11 *Glossary* still follows directly after.

- [ ] **Step 8.6: Commit**

```bash
git add 09-gaps-and-open-questions.md
git commit -m "09 §1.10: marker for the components/ catalogue

One-bullet closure marker matching the existing 29 and 30 markers.
Catalogue ships the per-component field-truth tier the gap names."
```

---

## Task 9: Final verification pass

- [ ] **Step 9.1: Confirm all eight commits landed**

Run: `git log --oneline -10`
Expected: the eight commits from Tasks 1–8 plus the spec commit (`Add component-briefs catalogue design spec`) at the head of the log, in this order (newest first):
1. `09 §1.10: marker for the components/ catalogue`
2. `15: cross-reference the components/ catalogue as per-component layer`
3. `30: cross-reference the components/ briefs as the data-file seed`
4. `29: cross-reference the components/ catalogue as upstream`
5. `03: add Per-component briefs section linking to components/`
6. `Add Component briefs section to vault root index`
7. `Add _research/_component-prompt-template.md`
8. `Add components/ catalogue index with seed target list`
9. `Add component-briefs catalogue design spec`

- [ ] **Step 9.2: Confirm the working tree is clean**

Run: `git status`
Expected: `On branch main` and `nothing to commit, working tree clean`.

- [ ] **Step 9.3: Confirm the catalogue is reachable from the vault root**

Run: `grep "components/index.md" index.md`
Expected: matches the line added in Task 3.

Run: `ls components/`
Expected: just `index.md`.

- [ ] **Step 9.4: Confirm cross-references resolve**

Run: `grep -l "components/index.md" *.md`
Expected: at least `index.md`, `03-component-library.md`, `29-per-component-documentation-template.md`. (15-ai-in-ds.md and 30-generated-from-data-documentation.md reference `components/` and the brief schema in prose; the explicit `components/index.md` link is in 03 and the root index, which is enough to make the catalogue navigable.)

- [ ] **Step 9.5: No commit needed for this task** — it's verification only.

---

## What this plan explicitly does not do (matches spec §7)

- Does not write any per-component brief. The first brief is owner-assigned, picked by engagement need, and is the calibration point for the rest.
- Does not formalise the §15 schema. Free-form YAML is the discipline for the first ~5 briefs; formalisation is its own future task.
- Does not retrofit cross-references into 14 / 17 / 28 / 16 / 18 / 13 / 04 / 25. Those land per-component when the relevant brief lands.
- Does not introduce category subdirectories under `components/`. Category lives in frontmatter.
- Does not push to remote. Commits are local until the user pushes.

## Follow-on work (out of scope here)

- **Write the first brief.** Owner-assigned. The act of writing it is the validation that the 15-section spine and the prompt template work in practice. After this brief lands, expect small revisions to both.
- **Formalise the §15 schema.** After ~5 briefs, the schema's stabilised shape moves to `components/_schema.md` (or `_schema.json`). Versioned. CI-enforceable when the vault gets a build step.
- **Bulk-brief the seed list.** Counter-recommended. Engagement need pulls briefs forward. The catalogue grows deliberately.

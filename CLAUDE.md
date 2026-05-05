# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal knowledge base on **design systems consulting**, maintained by Adam Forrester for day-to-day reference at VML (a global creative/experience/commerce agency). It is an Obsidian vault of long-form markdown — there is no code, no build, no tests. The vault is the product. The audience is one practitioner; the voice is opinionated and first-person plural ("we", "our practice"). Treat edits like editorial work, not code changes.

## Structure and conventions

Top-level files are numbered to imply both reading order and a phase model of a DS engagement:

- `00-` cross-cutting (principles, agency context, commercial model)
- `01–08` engagement phases: discovery → foundations → components → docs → dev support → pilot → governance → maintenance
- `09-` open questions / gaps in the practice's POV
- `10+` extension topics (CMS, mobile/cross-platform, …) — append, don't renumber

Numbering anomalies are intentional: `00`, `00b`, `00d` (no `00c`) reflect when files were added, not a missing entry. Don't "fix" the sequence.

Three supporting directories:
- `_source-text/` — raw `.txt` source material (external articles, internal decks, transcripts). Treat as read-only inputs; cite them when synthesising.
- `_notes/` — intermediate synthesis notes that fed the numbered files. Lower authority than the numbered files; useful as a paper trail.
- `_research/` — workspace for the dual-agent research workflow. Drafts, not authoritative. See `_research/README.md` for the convention.

`.obsidian/` is vault config — leave it alone unless asked.

## File index

One-line hooks for each numbered file. Use this to jump to the right file rather than reading them all.

- `00-principles-and-philosophy.md` — the practice's POV: the ten principles, where we converge with and diverge from the field.
- `00b-agency-context.md` — VML as agency context: how DS work fits the agency commercial reality, and the gap between "what good looks like" and the world we operate in.
- `00d-commercial-model.md` — how VML scopes, resources, and prices DS engagements. Working document, not fixed formula.
- `01-discovery-and-strategy.md` — Discovery phase: strategic alignment, audits, stakeholder mapping, maturity baseline, pilot scoring.
- `02-design-foundations.md` — tokens, theming, naming, the Figma → DTCG → Style Dictionary pipeline. The bedrock layer.
- `03-component-library.md` — component model: anatomy, properties, layout, composition primitives, components-as-data. Web rendering target assumed; mobile addressed in 11.
- `04-documentation.md` — docs strategy for two audiences (humans and machines). Storybook/MDX + machine-readable metadata + registries from one source.
- `05-development-support.md` — dev pipeline, Storybook, headless vs. opinionated, CI quality gates, MCP/AI integration, adoption enablement.
- `06-pilot-and-implementation.md` — running the pilot product team: validating the system in production, building the executive coalition for scale.
- `07-governance-and-adoption.md` — governance models, contribution flow, adoption mechanics. The phase that decides whether the system survives the engagement.
- `08-ongoing-maintenance.md` — post-launch operating model, retainer shapes, KPIs. The phase the practice sells the least and external sources flag as the biggest delivery gap.
- `09-gaps-and-open-questions.md` — practice gaps and unanswered questions across the corpus. Sourced inventory of what we don't yet have a POV on.
- `10-cms-and-platform-integration.md` — DS in CMS environments. The seam between component governance and content governance.
- `11-mobile-and-cross-platform.md` — iOS, Android, Flutter. Tokens as the shared layer; native vs. custom component decisions; platform-specific token delivery.
- `12-figma-practice.md` — Figma at professional depth. Library architecture, component construction, Variables, Dev Mode/Code Connect/MCP, branching, performance, deprecation. The tool-specific exception in an otherwise tool-agnostic vault.
- `13-internationalization-and-rtl.md` — i18n, l10n, and RTL as DS architecture. Logical properties, text expansion, multi-script typography, locale-aware tokens, RTL component mirroring, the DS/application boundary.
- `14-accessibility.md` — accessibility encoded into the DS architecture. Pair tokens for contrast, ARIA encapsulation, focus management, the four-layer model (tokens / components / docs / contribution gates), conformance reporting under EAA / Section 508.
- `15-ai-in-ds.md` — AI integration across the DS lifecycle. Components-as-data as the architectural prerequisite. MCP server architecture, Figma MCP and Code Connect, three-level context maturity, the four-prerequisite minimum architecture, honest assessment of what works vs. aspirational.

When new numbered files are added, add a hook here as well as cross-referencing from earlier files.

## Cross-reference style

References to other files are written inline as prose, e.g. `(See 01-discovery-and-strategy.)` — not as Obsidian `[[wikilinks]]` and not as relative markdown links. Match this style. When a new file is added, search for topics it now covers and add inline references from the relevant earlier files rather than retrofitting links into every file.

## File anatomy

Numbered files follow a consistent shape — preserve it when editing:

1. `# NN — Title` H1
2. A blockquote one-paragraph framing of why this file exists / the POV it takes
3. `---` separator
4. H2 sections, often opening with framing prose before any lists/tables
5. Heavy use of bolded lead-ins (`**Like this.**`) inside paragraphs
6. Citations in parens with source + year, e.g. `(InVision MVP, 2020)`, `(VML library)`, `(Sam Anderson, *Design Systems are Infrastructure*, Nov 2024)`

Voice is declarative and opinionated. Avoid hedging, avoid bullet-point dumps where prose is doing the work, avoid emoji. New content should sound like it was written by the same person.

## When asked to add or update content

- Prefer editing existing files over creating new ones. New top-level files are reserved for genuinely new phase/topic areas.
- When a new file is added (most recently `11-mobile-and-cross-platform.md`), audit the earlier numbered files for places the new topic was previously hand-waved or noted as out-of-scope, and add inline cross-references there.
- For substantial new claims, expect a `_source-text/` file to back them. If one doesn't exist, flag the claim as needing a source rather than inventing a citation.
- Don't rewrite tone. If the user asks to add a section, match the surrounding voice.

## Git and remote

The vault is a private git repo at `git@github.com:adamforrester/knowledge-base.git`, default branch `main`. Commits are editorial — make them when content is ready, not on every save. The user plans to eventually expose this vault via an MCP server.

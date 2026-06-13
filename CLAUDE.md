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

Three top-level navigation aids:
- `index.md` — the canonical file index. One-line hooks per numbered file, written as an OKF-conformant root index. Read this when you need to jump to the right file rather than scanning the directory.
- `GLOSSARY.md` — vault-specific and practice-adjacent vocabulary. Common DS terms not defined; reach for it when a term reads as internal-tier IP (`.ai.json`, Six Signs, components-as-data, four-layer AI stack, etc.).
- Frontmatter on every numbered file — `type`, `title`, `description`, `tags`, `timestamp`. Conforms to the Open Knowledge Format v0.1 (markdown + YAML frontmatter, no platform). When adding a new numbered file, add the same frontmatter shape and add an entry to `index.md` as well as the file index discipline below.

`.obsidian/` is vault config — leave it alone unless asked.

## File index discipline

`index.md` is the canonical list. When new numbered files are added, add a hook to `index.md` and add inline cross-references from earlier files where the new content is now relevant. Do not duplicate the index inside this file.

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

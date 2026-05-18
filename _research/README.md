# _research — incoming research workflow

Working directory for dual-agent research runs. The pattern: a single prompt is run against two agents independently (one external, one Claude in this repo); both raw outputs are captured here; we then synthesise a single draft that, once promoted, lands in a numbered top-level file.

This directory is editorial scratch space. Nothing here is authoritative until it's been synthesised and either folded into a numbered file or — if it's a new topic area — promoted to its own numbered file. Until then, treat `_research/` as drafts, not as the practice's POV.

---

## Structure

```
_research/
  _inbound/   raw agent outputs, untouched
  _synthesis/ reconciled drafts in progress
  _archive/   synthesis drafts that have already landed in numbered files
```

Underscore-prefixed folders match the convention of `_source-text/` and `_notes/` — keeps the numbered files prominent in the Obsidian file tree.

---

## Run convention

One research run = one dated topic folder under `_inbound/`:

```
_inbound/
  YYYY-MM-DD-topic-slug/
    prompt.md           the brief — identical for both agents
    external-agent.md   raw output from the other agent (pasted in)
    claude.md           Claude's run of the same prompt, in this repo
```

**Topic slug** matches the numbered-file convention (lowercase, hyphenated, no underscores), e.g. `2026-05-05-ai-component-codegen`.

**The prompt is identical for both agents.** That is the point of the dual-agent setup — same input, different reasoning paths, surface where they converge and where they diverge. Don't tweak the prompt between runs unless the run is being explicitly redone; in that case, supersede the whole folder rather than editing in place.

**For prompt drafting, use `_prompt-template.md`.** The template is informed by completed runs and standardizes the parts that should be consistent (audience, output format, depth) while leaving the topic-specific scope variable. Skip it only when the question is small enough to not need a full survey.

**Raw outputs are not edited.** No reformatting, no fixing typos, no trimming. We need to be able to audit which agent contributed which claim later, especially when they disagree. Edits happen in `_synthesis/` or directly in numbered files, not in `_inbound/`.

---

## Synthesis convention

Synthesis can happen two ways. Both are legitimate; pick by topic shape, not by habit.

**Path A — intermediate synthesis file.** A separate document in `_synthesis/` reconciles the raw outputs before anything lands in a numbered file:

```
_synthesis/
  YYYY-MM-DD-topic-slug.md
```

Use this when the two raw outputs diverge enough to need an explicit reconciliation pass, when the synthesis itself is the deliverable, or when the topic will land across multiple numbered files and the bridging logic warrants its own document. The May 2026 batch covering accessibility, AI-in-DS, Figma practice, and i18n/RTL used this path — see `_archive/` for the four resulting synthesis files.

**Path B — direct to numbered file.** When the two raw outputs converge cleanly, when the synthesis fits naturally inside one or more numbered files, or when the convergence/divergence reasoning is short enough to live in the numbered files' provenance footers, draft directly from raw outputs into the numbered files. The mobile a11y (May 13 → 16/17), motion (May 14 → 18/19/20/21), and tokens (May 15 → 22/23/24) batches used this path. The conversation transcript and the numbered files themselves are the audit trail; no intermediate file is created.

Either way, the synthesis should:

- Reconcile the two outputs — note where they agree (probably right), where they diverge (interesting), where one has something the other missed.
- Cite both agents inline when a claim is load-bearing, e.g. *(both agents)*, *(external only)*, *(Claude only)*.
- Match the voice and shape of the numbered files — opinionated, first-person plural, prose-led.
- Flag claims that need a `_source-text/` backing before they can be promoted.

---

## Promotion

When a synthesis is ready to land in the vault:

1. Edit it into the relevant numbered file (or, for a genuinely new topic area, promote to a new numbered file — `12-…`, `13-…`).
2. Add inline cross-references from earlier files where the new content is now relevant (same convention as when `11-mobile-and-cross-platform.md` was added — see `CLAUDE.md` for the cross-reference style).
3. **If Path A was used:** move the synthesis file from `_synthesis/` to `_archive/`. Don't delete — keeps a paper trail of what synthesis produced what numbered-file content. **If Path B was used:** the numbered files' provenance footers are the paper trail; nothing needs to move.

The `_inbound/` folder for that topic stays put as the audit record of where the synthesis came from, regardless of which path was used.

---

## What this directory is *not*

- Not a place for one-off Claude conversations or ad-hoc notes — those belong in `_notes/`.
- Not a replacement for `_source-text/` — that's external articles, decks, transcripts (read-only inputs). `_research/` is generated material.
- Not authoritative — content here is draft until promoted.

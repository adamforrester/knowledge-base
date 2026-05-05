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

**Raw outputs are not edited.** No reformatting, no fixing typos, no trimming. We need to be able to audit which agent contributed which claim later, especially when they disagree. Edits happen in `_synthesis/`, not `_inbound/`.

---

## Synthesis convention

Once both raw outputs are in place, synthesis goes here:

```
_synthesis/
  YYYY-MM-DD-topic-slug.md
```

The synthesis file is where the practice's voice enters. It should:

- Reconcile the two outputs — note where they agree (probably right), where they diverge (interesting), where one has something the other missed.
- Cite both agents inline when a claim is load-bearing, e.g. *(both agents)*, *(external only)*, *(Claude only)*.
- Match the voice and shape of the numbered files — opinionated, first-person plural, prose-led.
- Flag claims that need a `_source-text/` backing before they can be promoted.

---

## Promotion

When a synthesis is ready to land in the vault:

1. Edit it into the relevant numbered file (or, for a genuinely new topic area, promote to a new numbered file — `12-…`, `13-…`).
2. Add inline cross-references from earlier files where the new content is now relevant (same convention as when `11-mobile-and-cross-platform.md` was added — see `CLAUDE.md` for the cross-reference style).
3. Move the synthesis file from `_synthesis/` to `_archive/`. Don't delete — keeps a paper trail of what synthesis produced what numbered-file content.

The `_inbound/` folder for that topic stays put as the audit record of where the synthesis came from.

---

## What this directory is *not*

- Not a place for one-off Claude conversations or ad-hoc notes — those belong in `_notes/`.
- Not a replacement for `_source-text/` — that's external articles, decks, transcripts (read-only inputs). `_research/` is generated material.
- Not authoritative — content here is draft until promoted.

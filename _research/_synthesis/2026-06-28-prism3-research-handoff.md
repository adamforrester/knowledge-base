# Prism3 → KB research handoff (2026-06-28)

> A coordination index for the KB agent. The Prism3 token-engine work generated
> four dual-agent research runs and two direct edits to numbered files. This lists
> every KB gap encountered — **what's already in the vault, what's filed-but-not-
> promoted, and what has no home yet** — so nothing is lost in synthesis. This is
> not itself a single-topic synthesis; it's the promotion queue. Delete or move to
> `_archive/` once everything below is promoted.

---

## How to read this (context for the KB agent)

- **Each run is single-sided so far.** Per `_research/README.md` a run has
  `prompt.md` + `external-agent.md` + `claude.md`. Only **`claude.md`** exists for
  these four (the Prism3 work ran Claude in-repo, not the external agent). Two
  paths: (a) run the external agent on the same `prompt.md` and reconcile, or (b)
  accept `claude.md` as-is — it is **heavily primary-sourced** (Figma/W3C/Carbon/
  Utopia/Material/Bootstrap docs, cited inline with confidence flags) and was used
  to drive shipped engine decisions, so single-sourcing is low-risk here.
- **Voice on promotion:** house first-person-plural, declarative, citations in
  parens — same as the existing files. The `claude.md` outputs are neutral expert
  voice (per the convention); apply house voice when promoting.
- **New numbered file?** Only layout (§4 below) needs one. Add frontmatter +
  an `index.md` hook + inline cross-refs (per `CLAUDE.md`).
- **Source-text:** these runs cite primary URLs but created **no `_source-text/`
  files**. If you want source-text backing before promoting load-bearing claims,
  flag/capture; otherwise treat the cited run as the provenance.
- **Engineering context** (optional, for grounding): the consuming engine + its
  decisions live in the *prism3-tokens* repo at `Prism3/docs/00-progress.md` and
  `Prism3/docs/05-token-coverage-roadmap.md`. Not needed to promote, but it shows
  how each finding was applied.

---

## The queue

### 1. Figma Variables vs Styles + the code→Figma round-trip  ·  FILED, NOT PROMOTED
- **Run:** `_inbound/2026-06-28-figma-variables-styles-roundtrip/` (`prompt.md` + `claude.md`; `claude.md` has a §3a "Typography binding limitations").
- **Gap:** `12-figma-practice` covers Figma *Variables* well (collections, modes, scoping, Tokens-Studio trade-off) but has **no POV on Figma *Styles* as a separate object class**, on **code→Figma write-back** (REST Variables API is Enterprise-only read+write; Styles can only be created via the Plugin API), or on the **typography binding limits** (lineHeight/letterSpacing bind as px only; textDecoration/textCase not bindable → links/all-caps are separate styles; the 8 bindable text fields).
- **Promote to:** `12-figma-practice` — a "Variables vs Styles, and the code→Figma round-trip" section (styles = separate object class; the three-tier disposition variable/style-part/code-only; the materialization directive; the Enterprise write gate; update-in-place vs build-from-scratch by `VariableID`). Add the typography-binding limits either here or as a cross-ref into `23-typography-tokenisation`.
- **Cross-refs to add:** from `22-token-architecture-extensions` (composite round-trip fidelity), `23-typography-tokenisation` (the binding limits), and a back-ref from `12`'s existing Variables section.
- **Also flagged in prism3:** `05-token-coverage-roadmap` → "Cross-cutting: Figma round-trip" calls this KB write-up out as backlog.

### 2. Responsive type — mobile↔desktop sizing  ·  FILED + ALREADY PROMOTED (reconcile only)
- **Run:** `_inbound/2026-06-28-responsive-type-scaling/`.
- **Already in the vault:** a subsection **"How much to shrink — the mobile↔desktop relationship"** was added to `23-typography-tokenisation` (timestamp bumped to 2026-06-28). Core POV is landed: a flat shrink factor is the wrong model; bigger sizes shrink more; body stays constant; display converges to a ~40–48px mobile hero band (`160→48`, ≈Carbon `fluid-display-04`).
- **Remaining:** reconcile with `external-agent.md` if you run it; otherwise this is effectively done. Confirm the cited numbers if promoting any further detail.

### 3. Shadow / elevation tokens  ·  FILED + ALREADY PROMOTED (reconcile only)
- **Run:** `_inbound/2026-06-28-shadow-elevation-tokens/`.
- **Already in the vault:** a subsection **"Shadow tokens — shape, colour, and the elevation lever"** was added to `31-color-systems` after the existing lift-pattern section (timestamp bumped). Landed: six steps / two layers (key+ambient); tint-don't-use-pure-black; the two-axis surface+shadow split joined by a semantic `elevation.N`; softness as the generation lever.
- **Remaining:** reconcile external if run; otherwise done. (Note: it lives in `31-color-systems` since that already owned the lift pattern; if a dedicated elevation/foundations file is ever created, consider relocating.)

### 4. Layout — breakpoints + responsive grid  ·  FILED, NO HOME (needs a numbered file)
- **Run:** `_inbound/2026-06-28-layout-grid-breakpoints/` (filed today).
- **Gap:** the vault has **no layout/grid/breakpoint file at all** — the largest structural gap. Coverage is scattered (typography's container queries in `23`).
- **Promote to:** likely a **new numbered file** (e.g. a layout-foundations topic in the 10+ extension range, or a section in `02-design-foundations` if you prefer to keep it in foundations). Core POV: 5–6 t-shirt min-width breakpoints; the 12-col grid is a *design artifact* not the load-bearing code contract (CSS Grid + container queries do real layout); gutter/margin **alias the spacing scale**; fluid-first + a `container.max` cap + a narrow reading container (collapse the fluid-vs-fixed duplication); breakpoints as Figma modes in a separate collection.
- **If a new file:** add frontmatter + `index.md` hook + cross-refs from `23` (container queries vs breakpoints), `12-figma-practice` (breakpoints as modes), `13-internationalization-and-rtl` (which already mentions breakpoint/Direction modes).

---

## Lower-priority / optional gaps (encountered, not yet researched or filed)

- **Generated AI-readable token metadata (the `.ai.json` technique).** `31-color-systems §9` is the schema source for token descriptions. The engine extends it with: `meaning` distinct from `$description`; per-step colour-scale `intent`; a **bidirectional `aliased_by` reverse index computed transitively** (so a primitive shows every token that resolves to it, through multi-hop alias chains). Worth a short note in `31 §9` or `30-generated-from-data-documentation` as a practice technique. *No run yet.*
- **The "materialization directive" pattern.** A general token-architecture principle the engine uses: the **canonical value lives in `$value`; exporter-read transform data lives in `$extensions`** (e.g. line-height `px-from-ratio` for Figma, fluid `clamp()`, shadow effect-style modes), never in the prose/AI sidecar. Candidate addition to `22-token-architecture-extensions`. *No run yet.*

These two are optional and prism3-flavoured; include only if they earn vault-tier generality.

---

## Already-edited numbered files (for your audit)
- `23-typography-tokenisation.md` — added "How much to shrink — the mobile↔desktop relationship" (run #2). Timestamp 2026-06-28.
- `31-color-systems.md` — added "Shadow tokens — shape, colour, and the elevation lever" (run #3). Timestamp 2026-06-28.

## Status summary
| # | Topic | Filed | In vault | Action |
|---|---|---|---|---|
| 1 | Figma Variables vs Styles + round-trip | ✅ | ✗ | promote → `12-figma-practice` (+ cross-refs) |
| 2 | Responsive type sizing | ✅ | ✅ (`23`) | reconcile only |
| 3 | Shadow / elevation | ✅ | ✅ (`31`) | reconcile only |
| 4 | Layout / breakpoints / grid | ✅ | ✗ | **new file** (+ `index.md`, cross-refs) |
| 5 | AI-metadata technique | ✗ | partial (`31 §9`) | optional note |
| 6 | Materialization-directive principle | ✗ | ✗ | optional → `22` |

# Handoff prompt for the KB agent (paste into a fresh knowledge-base session)

---

You are the maintainer agent for the **knowledge-base** vault — a design-systems
consulting KB (an Obsidian vault of long-form markdown; the vault is the product).
Before touching anything, read **`CLAUDE.md`** (house conventions: numbering,
frontmatter/OKF, cross-reference style, file anatomy, voice) and
**`_research/README.md`** (the dual-agent research workflow and the promotion
discipline). Follow them exactly — this is editorial work, not code.

## Your task

Promote a batch of completed research into the vault. A coordination index has been
prepared at **`_research/_synthesis/2026-06-28-prism3-research-handoff.md`** — read
it first; **it is your work queue.** It catalogues four research runs under
`_research/_inbound/2026-06-28-*/` plus two edits already made, and for each topic
gives the gap, the target numbered file, and the cross-references to add.

## Context you must account for

- **The runs are single-sided.** Each `_inbound/2026-06-28-*/` folder has
  `prompt.md` + `claude.md` but **no `external-agent.md`** (the Prism3 work ran only
  the in-repo Claude side). You may either (a) run the external agent on the same
  `prompt.md` and reconcile both per the README, or (b) accept `claude.md` as the
  source — it is heavily primary-sourced (Figma/W3C/Carbon/Utopia/Material/Bootstrap
  docs, cited inline with confidence flags) and already drove shipped engine
  decisions, so single-sourcing is low-risk. State which path you took.
- **Two topics are already partly in the vault** — do not duplicate them: a
  "How much to shrink — the mobile↔desktop relationship" subsection in
  `23-typography-tokenisation`, and "Shadow tokens — shape, colour, and the
  elevation lever" in `31-color-systems`. Audit these; extend/reconcile only if the
  run has material they're missing.
- **Voice on promotion:** the `claude.md` outputs are neutral expert voice by
  convention; rewrite into the vault's house voice (declarative, first-person
  plural, prose-led, bolded lead-ins, citations in parens). Don't paste raw.
- **Source-text:** the runs cite primary URLs but created no `_source-text/` files.
  If you want source-text backing before promoting a load-bearing claim, capture it
  or flag the claim; otherwise treat the cited run as provenance.

## Do, in priority order

1. **Figma Variables vs Styles + the code→Figma round-trip** (run
   `2026-06-28-figma-variables-styles-roundtrip`) → promote into
   **`12-figma-practice`** as a new section: Figma *Styles* as a separate object
   class from Variables; the three-tier disposition (variable / style-part /
   code-only); the code→Figma write gate (REST Variables API is Enterprise-only;
   Styles can only be created via the Plugin API); update-in-place vs
   build-from-scratch by `VariableID`. Fold the run's **§3a typography binding
   limits** (lineHeight/letterSpacing bind as px only; textDecoration/textCase not
   bindable → links/all-caps are separate styles) here or as a cross-ref into
   `23-typography-tokenisation`. Add cross-refs from `22-token-architecture-
   extensions` (composite round-trip fidelity) and a back-ref from `12`'s Variables
   section.

2. **Layout — breakpoints + responsive grid** (run
   `2026-06-28-layout-grid-breakpoints`) → this has **no home**; create a **new
   numbered file** (a layout-foundations topic — pick the number per the numbering
   convention; the 10+ extension range or a foundations slot, your call). Core POV:
   5–6 t-shirt min-width breakpoints; the 12-col grid is a *design artifact*, not the
   load-bearing code contract (CSS Grid + container queries do real layout);
   gutter/margin **alias the spacing scale**; fluid-first + a `container.max` cap +
   a narrow reading container (the fluid-vs-fixed duplication is collapsed);
   breakpoints as Figma modes in a separate collection. Add an `index.md` hook and
   inline cross-refs from `23` (container queries vs breakpoints), `12-figma-
   practice` (breakpoints as modes), and `13-internationalization-and-rtl`
   (which already mentions breakpoint/Direction modes).

3. **Reconcile the two already-promoted topics** (runs `2026-06-28-responsive-type-
   scaling` and `2026-06-28-shadow-elevation-tokens`): audit the existing `23`/`31`
   subsections against the runs; add only what's missing. Likely no-ops.

4. **Optional, only if they earn vault-tier generality** (see handoff §"Lower-
   priority"): a note on the generated AI-readable metadata technique (the
   transitive `aliased_by` reverse index; `meaning` vs `$description`; per-step
   colour `intent`) into `31 §9` or `30-generated-from-data-documentation`; and the
   "materialization directive" principle (canonical value in `$value`, exporter
   transform data in `$extensions`, never the prose sidecar) into
   `22-token-architecture-extensions`. Skip if too prism3-specific.

## On completion

- Update the **`timestamp`** on every numbered file you touch; add the **`index.md`**
  entry for the new layout file.
- Move the handoff + any Path-A synthesis drafts to **`_research/_archive/`** once
  promoted; leave the `_inbound/` folders in place as the audit record.
- Report a short changelog: which files you edited/created, which cross-refs you
  added, which path (external vs claude-only) you took per run, and anything you
  deliberately did not promote (with the reason).

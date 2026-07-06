---
okf_version: "0.1"
type: schema
title: Component Brief §15 Schema
description: The locked shape for the agent-consumable schema embedded as section 15 of every component brief. Formalised after the first six briefs (Button, Text Field, Textarea, Divider, Icon, Select) once the free-form shape had stabilised through real use. Keys and ordering are locked; values stay free-form prose. The practice's opinionated default `.ai.json` projection of a component brief.
tags: [components, schema]
timestamp: 2026-07-06
---

# Component Brief §15 Schema

Every component brief ends with a §15 *agent-consumable schema* — a fenced YAML block that is the structured projection of the brief's prose (§§1–13). For the first six briefs that block was free-form, so the shape could stabilise through real use (the catalogue's stated plan; see `index.md`). It has now stabilised, and this file locks it.

**What "locked" means here:** the **top-level keys, their ordering, and the ALWAYS/SCALES rule** are fixed; **values stay free-form prose**. The schema is not strictly typed — a key's value can be a string, a list, a map, or nested prose, whichever carries the meaning. The discipline is structural consistency, not a rigid type system. (This is the "keys locked, values prose" decision; a future tightening to typed values is possible but deliberately deferred until the catalogue is larger.)

Because values are free-form, a **downstream implementation may reconcile a brief's recommended vocabulary without touching the locked keys** — the keys are the contract, the vocabulary is a value. This is the brief-upstream / engagement-data-downstream relationship (see 30) at the schema level: the brief records the field's terms; an implementation may settle on its own, and the reconciliation is recorded where it is authoritative — in the implementation. The worked example is Button: its `intent` / `appearance` vocabulary is reconciled by the Prism3 engine (`filled/outline/text` + `primary/neutral/destructive/accent`), noted in `button` §3 and specified in `Prism3/docs/20-interactive-color-system`. The `§15` keys are unchanged; only the values differ downstream.

The §15 block stays **complete and self-contained in every brief** — this file defines the shared shape they all conform to; it does not replace the per-brief block. A reader (human or agent) gets the full schema from any single brief.

---

## Canonical key order

The keys mirror the prose spine, so the schema reads as a clean projection of it. **ALWAYS** keys appear in every brief; **SCALES** keys appear only when the component has something substantive to encode there (a non-interactive primitive has no `motion`; a flat control has no `anatomy`).

1. **`identity`** — ALWAYS. `id`, `name`, `aliases` (list), `category`, `status`. (≈ §10 naming + frontmatter status.)
2. **`description`** — ALWAYS. One-paragraph "what it is / what it isn't / the boundaries it holds." (≈ §1 framing.)
3. **`anatomy`** — SCALES. Structural/geometric model where it carries weight (e.g. Icon's grid/stroke/optical metrics). (≈ §2.)
4. **`api`** — ALWAYS. The prop surface. May open with `inherits:` (the substrate it stands on — see below), `delivery`/`data-model`, then `props:` (each: `name`, `type`, `default`, `required`, `deprecated?`, `description`). (≈ §3.)
5. **`states`** — ALWAYS. `runtime:` (list); may carry `inherits:` and a component-specific list; `[]` for non-interactive primitives. (≈ §4.)
6. **`variants`** — ALWAYS. `size` plus the component's intentional axes. (≈ §4.)
7. **`accessibility`** — ALWAYS. `wcag-criteria` (list), `aria-attributes`, `keyboard-model`, `focus-behavior`; may carry `inherits:`. (≈ §6.)
8. **`content`** — ALWAYS. `label-pattern`, `error-pattern`, `empty-pattern`, plus component-specific patterns. (≈ §7.)
9. **`motion`** — SCALES. `enter`/`exit`, `reduce-motion`, platform notes. Omit for static primitives. (≈ §8.)
10. **`i18n`** — SCALES. `rtl`, locale concerns; may carry `inherits:`. (≈ §9.)
11. **`implementation`** — SCALES. Delivery, framework gotchas, the headless-vs-opinionated substrate. (≈ §11.)
12. **`composition`** — ALWAYS. `composes-with`, `alternative-to`, `supersedes`, `superseded-by` (each a list, or `null`). (≈ §12.)
13. **`notes`** — ALWAYS. `contested:` (list — the live decisions); optional `unverified:` (claims lacking `_source-text/` backing), `evolution`, `trap`, `emerging`, `inherited`. (≈ §13.)

---

## Two locked conventions

- **`inherits:`** — a first-class field on `api`, `states`, `accessibility`, and `i18n`. When a component stands on a shared substrate (the form family on `text-field`), it **names the substrate and does not re-derive it**. The schema records the *delta*, not a copy. This emerged in Textarea and Select and is load-bearing for the form category; it is now part of the locked shape. Example: `api: { inherits: text-field, props: [ ...only the new props... ] }`.
- **`notes.unverified:`** — the standing home for claims surfaced in research but lacking `_source-text/` backing (external-pass version numbers, vendor-roadmap claims, performance figures). Flagging is mandatory; a brief never silently launders an unverified claim into an asserted default.

---

## Conformance

All six launch briefs conform to this shape (retrofitted at formalisation). New briefs adopt it from the start. When a genuinely new key proves necessary across multiple components, add it here first (with an ALWAYS/SCALES designation and a spine mapping), then use it — the schema is itself versioned discipline, not an ad-hoc accretion.

A note on strictness: should the catalogue later need machine-validation, this file is where a typed schema (enums, required flags, controlled vocabularies) would be specified. That tightening is deferred deliberately — the current value is a consistent, readable shape across the catalogue, not a validator.

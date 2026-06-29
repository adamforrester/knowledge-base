---
type: practice-area
title: Layout, Grid, and Breakpoints
description: The layout foundation the vault was missing — five t-shirt min-width breakpoints (mobile-first, brand authors the values, ranges derive), the 12-column grid as a design artifact rather than the load-bearing code contract (CSS Grid + container queries do the real work), gutters and margins as aliases of the spacing scale rather than independent tokens, fluid-first containers with a max cap and a narrow reading width (the fluid-vs-fixed duplication collapsed), breakpoints encoded as Figma modes in a separate layout collection, and the two-knob generation lever (breakpoint floors + base column count) for the white-label engine.
tags: [extension, layout, grid, breakpoints, responsive, containers, tokens, dtcg, figma-modes]
timestamp: 2026-06-29
---

# 35 — Layout, Grid, and Breakpoints

> Layout is the foundation this vault had no file for — the largest structural gap in our token POV until now. Colour (31) and typography (23) each earned a deep-dive; breakpoints, the responsive grid, and containers were scattered across a container-queries note in 23 and a breakpoint-modes mention in 13, never assembled into a position. That is a problem, because layout is where the 2020–2026 platform shift is most under-absorbed: CSS Grid and container queries have quietly demoted the 12-column framework from a load-bearing primitive to a design artifact, and most token systems still ship a column grid as if components consume it. This file is the practice's settled view on the four decisions a layout token layer actually has to make — how many breakpoints and where, what the column grid is *for*, where gutters and margins come from, and how containers behave — plus the two knobs a white-label engine needs to generate all of it per brand.

---

## Why layout needs its own file

The systems we audit tokenise colour and spacing reliably, tokenise typography occasionally, and tokenise layout almost never. Breakpoints live as magic numbers in a media-query mixin; the grid is a Bootstrap habit nobody has revisited; gutters are hand-typed per layout. The cost is the same as everywhere else tokens are skipped — drift, per-brand re-litigation, and a Figma file whose breakpoints bear no documented relationship to the code's. The deeper reason layout is worth a position of its own is that the **right answer changed**. The 12-column grid was a real layout engine in the float-and-then-flexbox era; on the 2026 platform, CSS Grid and container queries do the structural work, and the column grid survives mainly as an alignment scaffold in Figma and a shared mental model. A token layer that doesn't internalise that ships the wrong contract — it tells component authors to consume column spans that the CSS no longer needs. This file fixes the position before the engine bakes it in.

## Breakpoints — five, t-shirt, mobile-first

Across a ten-system survey (Bootstrap 5, Tailwind, Material 3, IBM Carbon, Atlassian, Polaris, Primer, Fluent 2, Ant, Bulma) the count converges on **five or six**, the naming converges on **t-shirt** (`sm/md/lg/xl/2xl`), and the strategy converges overwhelmingly on **min-width / mobile-first** — only Material uses ranged window-size classes, and it does so because it drives discrete adaptive *layouts*, not interpolated type. The values cluster around real attractors: **~768 (tablet) is near-universal, ~1024 desktop, ~1200–1280 large, ~1440/1920 wide**; the least-converged value in the whole field is the small-mobile floor (systems variously anchor it at 0, 320, 480, 576, or 640).

| System | Count | Values (px) | Naming | Mobile-first? |
|---|---|---|---|---|
| Bootstrap 5 | 6 | 0 / 576 / 768 / 992 / 1200 / 1400 | t-shirt | yes |
| Tailwind | 5 | 640 / 768 / 1024 / 1280 / 1536 | t-shirt | yes |
| Material 3 | 5 | 0 / 600 / 840 / 1200 / 1600 | semantic (window classes) | ranged |
| IBM Carbon v11 | 5 | 320 / 672 / 1056 / 1312 / 1584 | t-shirt | yes |
| Atlassian | 6 | 0 / 480 / 768 / 1024 / 1440 / 1768 | t-shirt | yes |
| Polaris | 5 | 0 / 490 / 768 / 1040 / 1440 | t-shirt | yes |
| Primer | 6 | 320 / 544 / 768 / 1012 / 1280 / 1400 | t-shirt | yes |
| Ant | 6 | 576 / 768 / 992 / 1200 / 1600 (/1920) | t-shirt | yes |
| Bulma | 5 | 768 / 1024 / 1216 / 1408 | device | yes |

*(Bootstrap, Tailwind, Material 3, Carbon, Atlassian, Polaris, Primer, Ant, Bulma docs, 2026.)*

**The practice default: five min-width breakpoints — `sm 0 / md 768 / lg 1024 / xl 1440 / 2xl 1920`.** Brand authors *override the values*; the names stay constant across brands, and the ranges derive mechanically (each range ends one pixel below the next floor — `next − 1`), so we never store both a floor and a ceiling. We emit min-width floors and let the cascade do the rest. Two profiles flex the count without breaking the names: a **minimal three** (`sm / md / lg`) for simple brands, and a **comprehensive six** that prepends an `xs` small-mobile floor for data-dense products. Five is the anchor because it covers phone / tablet / laptop / desktop / wide without the over-granular low end some systems ship — a 390px-vs-430px split between two phones is a distinction the layout almost never needs to make.

## The 12-column grid — design artifact, not code contract

**Twelve columns is still the product default** (Bootstrap, Atlassian, Polaris, Primer, Bulma all ship it), with two deliberate outliers: IBM Carbon moved to **sixteen** at v11 (it was twelve at v10 — so the number is version-dependent, not a law) and Ant ships **twenty-four**, both dense-data choices for analytics-heavy UIs. Material runs a per-breakpoint **4 / 8 / 12**. Underneath the count, two schools: fixed-count-variable-span (Bootstrap, Carbon, Ant) versus variable-count-per-breakpoint (Material, and the Figma design-grid convention).

The more important finding is that the column grid **has shifted from a code primitive to a design artifact**. Tailwind never shipped a column framework at all; Polaris's and Atlassian's grids are thin CSS-Grid wrappers; modern layout is done with native **CSS Grid** (`grid-template-columns`, `subgrid`, `minmax()`) and **container queries**, not by consuming a twelve-class span system (Barker, *Is it time to ditch the design grid?*, 2021; Eckles, *Solutions to replace the 12-column grid*, 2020). The twelve-column grid endures as the **Figma layout-grid that designers align to** and the **4 / 8 / 12 ladder everyone reasons in** — a shared language, not an API. So the practice's position is: **emit the column grid as a design artifact, document "build with CSS Grid," and never assume components consume column spans.** Sixteen and twenty-four are available as opt-in dense-data profiles; twelve is the default mental model. For agency and marketing-tier work the point is sharper still — a rigid twelve-column rhythm reads as "product UI," and bespoke editorial work leans on freeform CSS Grid, so the column grid there is purely a Figma alignment aid.

## Gutters and margins alias the spacing scale

The single most useful finding in the whole layout survey: **gutters and margins are not independent tokens — they are aliases of the 8px spacing scale, keyed to breakpoint index.** Atlassian literally aliases `space.200 / 300 / 400` for its gutters; Material, Carbon's narrow mode, and the practice's own reference implementation all draw gutter and margin values straight from the spacing ramp. The values scale shallowly: **gutter 16 (mobile) → 24 → 32 (desktop)**, with **margins running a step larger at the top** (→ 40 / 48). Bootstrap's flat 24 and Carbon's gutter-as-a-mode (32 / 16 / 1) are the variations, but every value any of them ships is a multiple of the same 8px scale.

The architectural consequence is that we do **not** mint a parallel `gutter/*` and `margin/*` primitive tree. Gutter and margin are **semantic aliases into the existing spacing scale**, indexed by breakpoint — which means a brand that re-authors its spacing ramp gets a correct gutter/margin ladder for free, and the layout layer adds almost no new primitives. (See 22-token-architecture-extensions for the primitive → semantic aliasing discipline this applies, and 23 for the same move in typography.)

## Containers — fluid-first, a max cap, and a narrow reading width

The fluid-vs-fixed container question used to be a fork; in 2026 it is settled as **fluid-first with an opt-in max-width cap.** The legacy pattern — Bootstrap's and Bulma's stepped fixed `.container` (540 / 720 / 960 / 1140 / 1320) — has been superseded by one fluid container plus a single `max-width`. Systems that still expose both do so only as *modifiers* (`.container` vs `.container-fluid`), and **none of them ships a full parallel fluid-and-fixed token tree.** That last point is a hard-won lesson worth stating as a rule: a prior reference system in our portfolio shipped both a fluid container set *and* a fixed column-width set as parallel tokens, and the duplication was pure cost — two trees to keep in sync, two ways to express one decision. **Collapse it: one fluid container, one `container.max` cap, fixed-stepped as an opt-in modifier rather than a parallel tree.**

The one genuinely separate container is the **narrow reading container** — roughly **640–768px**, the width that holds long-form prose at the 65–75-character measure reading research wants. It is not a smaller version of the page container; it is a different pattern with a different job, and it earns its own token (`container.narrow ≈ 720`). So the container layer is three things, not a matrix: a fluid default, a `max` cap on it, and a narrow reading width. This connects to the fluid-type position in 23 — fluid type scales the text, the narrow container bounds the measure, and the two together are what make long-form reading hold up across viewports.

## Breakpoints as Figma modes

The community pattern for getting breakpoints into Figma is a **variable collection whose modes are the breakpoints** — and the discipline that makes it scale is the same one 12-figma-practice and 22 already name for theming: **one mode dimension per collection.** Breakpoints go in their own **layout collection** (modes = `sm … 2xl`), colour keeps its own light/dark collection, and they compose independently instead of multiplying into a combinatorial mode matrix. This is why the one-dimension-per-collection rule matters beyond theming — layout is another axis that would otherwise blow up the mode count. DTCG has no native concept of modes, so the breakpoint-keyed values live in `$extensions` and round-trip through Tokens Studio, which implements breakpoints as Figma modes directly (DTCG 2025.10; Tokens Studio docs, 2026). (See 12-figma-practice for modes and plan-tier mode caps, and 13-internationalization-and-rtl, which already treats Direction as a mode on the same principle — layout breakpoints are the same move for the responsive axis.)

## The generation lever — two knobs

For the white-label engine the question is which of this a brand authors and which the engine derives, and the answer is unusually clean: **two knobs.** A brand supplies its **breakpoint floor array** (the primary lever — the values, not the names) and a **base column count** (a mild lever — twelve by default, sixteen or twenty-four for dense-data brands), plus a single **`container.max`**. Everything else is derived: the t-shirt names are constant, the ranges fall out as `next − 1`, the gutter/margin ladder is read from the brand's existing spacing scale, the containers follow the fluid-first-plus-cap shape, the narrow reading width is fixed, and the Figma layout collection's modes are generated from the floor array. So the minimal input is `{ breakpoint floors[], base column count }` over the spacing scale the brand already has — and the engine produces the column ladder, the gutter/margin ladder, the ranges, the containers, and the Figma modes deterministically. (See 33-white-label-systems for the brand-generation-engine economics this feeds, and 24-tokens-at-scale for the multi-collection architecture it lands in.)

## Container queries vs. breakpoints — the division of labour

Breakpoints and container queries are complementary, not competing, and the boundary is worth stating because teams reach for the wrong one. **Breakpoints own the page shell** — the global responsive frame, the gutter/margin ladder, the column grid, the app-level layout shifts that depend on viewport width. **Container queries own component responsiveness** — a card, a sidebar widget, a media object that must adapt to *its container's* width regardless of where it sits, so the same component is portable from a 300px rail to a 1200px hero (`@container`, cross-browser since ~2023, in Tailwind v4 core). The token system serves both: the breakpoint floors for the shell, and the spacing/typography scales that components consume under their own container queries. Shipping only viewport breakpoints locks consumers into the page-as-context model the platform has moved past; shipping only container queries leaves the page shell with nothing to anchor to. (See 23-typography-tokenisation's fluid-type section for the typographic half of this — `cqi`-based fluid type is the container-query counterpart to viewport-relative `clamp()`.)

## Tensions and open questions

- **The small-mobile floor stays unconverged.** The field genuinely disagrees on the bottom breakpoint (0 vs 320 vs 480 vs 576 vs 640); we default the anchor to `sm 0` and treat a prepended `xs` as a per-brand profile rather than pretending there is a right answer.
- **Sixteen vs twelve vs twenty-four is a product-type decision, not a default.** We ship twelve as the design-artifact default and expose sixteen/twenty-four as dense-data profiles; we have not committed to a rule for *when* a brand crosses into needing them beyond "analytics-grade data tables."
- **DTCG has no modes, so breakpoint round-trip is `$extensions`-bound.** Until the Resolver Module standardises modes, breakpoint-as-mode is portable only through Tokens Studio's encoding, not natively across tools (see 22's note on the same gap for theming).

## See also

- **23-typography-tokenisation** — the fluid-type half of responsive layout: `clamp()`, `cqi` container-relative type, the rem-floor accessibility rule, and the mobile↔desktop sizing curve the narrow reading container complements.
- **12-figma-practice** — modes, plan-tier mode caps, and the variable architecture the breakpoint layout collection sits in.
- **13-internationalization-and-rtl** — Direction as a mode on the same one-dimension-per-collection principle; the RTL axis composes with the breakpoint axis.
- **22-token-architecture-extensions** — the primitive → semantic aliasing the gutter/margin-as-spacing-alias move depends on, and the one-mode-dimension-per-collection rule.
- **33-white-label-systems** / **24-tokens-at-scale** — the brand-generation engine and multi-collection architecture the two-knob lever feeds.

---

*Provenance: synthesised from the layout/grid/breakpoints research run in `_research/_inbound/2026-06-28-layout-grid-breakpoints/` (June 2026), single-sourced (Claude in-repo; no external-agent pass) and accepted on the strength of its primary-source survey. Breakpoint values, column counts, container max-widths, gutter/margin-as-spacing-alias, the Carbon 12→16 change, and the Figma-mode limits are sourced to the named systems' 2026 docs; the design-grid-as-artifact direction to Barker (2021) and Eckles (2020); DTCG-has-no-modes to the W3C Design Tokens Format Module 2025.10. The five-breakpoint default value set, the collapse of the fluid-vs-fixed duplication, the dropping of over-granular low breakpoints, and the two-knob generation lever are the practice's judgement calls, anchored to the survey. No `_source-text/` file was captured; the cited run is the provenance.*

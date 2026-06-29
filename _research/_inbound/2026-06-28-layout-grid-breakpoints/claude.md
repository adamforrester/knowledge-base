# Tokenizing Breakpoints & the Responsive Grid

*Claude's run of the dual-agent brief. Researched 2026-06-28 against primary docs
for Bootstrap 5, Tailwind, Material 3, IBM Carbon, Atlassian, Polaris, Primer,
Fluent, Ant, Bulma + the Figma-modes and DTCG material. Confidence: [S] sourced/
exact, [J] judgement.*

## TL;DR — recommendation

- **5 breakpoints, t-shirt, min-width/mobile-first** as default: `sm 0 · md 768 ·
  lg 1024 · xl 1440 · 2xl 1920` (the cross-system attractors). Brand authors the
  *values*; names are constant; ranges derive (`next−1`). Minimal (3) and
  comprehensive (6, prepend `xs`) profiles available.
- **12-col grid is a design artifact, not the code contract.** Modern layout is
  CSS Grid + container queries; the column grid survives as Figma layout-grid +
  the 4/8/12 design ladder. Emit it; document "build with CSS Grid."
- **Gutter/margin are NOT independent tokens — they alias the 8px spacing scale**
  (16→24→32 / 16→24→48), keyed to breakpoint index. (Atlassian/Prism2/M3 do this.)
- **Fluid-first + a `container.max` cap** (the 2026 default) + a `narrow`≈720
  reading container. **Collapse the fluid-vs-fixed duplication** Prism2 shipped;
  fixed-stepped is an opt-in modifier, not a parallel tree.
- **Breakpoints as Figma modes in a *separate* layout collection** (composes with
  colour light/dark independently).
- **Generation lever = two knobs:** the breakpoint floor array + the base column
  count (+ a `container.max`). Everything else derived.

---

## Comparison table

| System | BP count | Values (px) | Naming | Cols | Cols change/BP? | Gutter | Container max-widths | Real code grid? |
|---|---|---|---|---|---|---|---|---|
| **Bootstrap 5** [S] | 6 | 0/576/768/992/1200/1400 | t-shirt | 12 | no | 24 flat | 540/720/960/1140/1320 | flex 12-col |
| **Tailwind v4** [S] | 5 | 640/768/1024/1280/1536 | t-shirt | none | n/a | utility | snaps to BP | CSS-Grid utils + container queries in core |
| **Material 3** [S] | 5 | 0/600/840/1200/1600 (window classes) | semantic | 4/8/12/12/12 | **yes** | 16→24 | panes, not px | component grid |
| **IBM Carbon v11** [S] | 5 | 320/672/1056/1312/1584 | t-shirt | **16** (was 12 in v10) | no | 32/16/1 (mode) | 1584 | CSS-Grid 16-col |
| **Atlassian** [S] | 6 | 0/480/768/1024/1440/1768 | t-shirt | 12 | no | 16→32 (space tokens) | none fixed | CSS-Grid beta |
| **Polaris** [S] | 5 | 0/490/768/1040/1440 | t-shirt | 12 | per-prop | gap (4px base) | none | thin CSS-Grid |
| **Primer** [S] | 6 | 320/544/768/1012/1280/1400 | t-shirt | 12 | viewport-range | gutter/condensed/spacious | 544/768/1012/1280 | legacy 12 + modern Layout |
| **Fluent 2** [S] | 6 | 320/480/640/1024/1366/1920 | semantic | 12 (not tokenized) | n/a | "×4px" (qual.) | none | underspecified |
| **Ant** [S] | 6 | 576/768/992/1200/1600(/1920) | t-shirt | **24** | no | Row prop | none | 24-col Row/Col |
| **Bulma** [S] | 5 | 768/1024/1216/1408 | device | 12 | no | 32 | 960/1152/1344 | flex 12-col |
| **NB (ref)** | 2 | 0/1024 (+1920) | device | 4/12 | yes | 16→24 | 1920 + narrow 720 | tokens only |
| **Prism2 (ref)** | 6 | 0/390/768/1024/1440/1920 | t-shirt | 2/2/4/8/12/12 | yes | 16→32 | fluid + fixed columnwidth | tokens only (both) |

---

## Per-question synthesis (condensed)

**Q1 — breakpoints.** Count converges on **5–6**; ~768 (tablet) is near-universal, ~1024 desktop, ~1200–1280 large, ~1440/1920 wide; the small-mobile floor is the least-converged value (0/320/480/576/640). **t-shirt naming dominates**; min-width/mobile-first is the overwhelming default (only Material uses ranges, for discrete adaptive layouts). Emit min-width floors; derive ranges.

**Q2 — columns.** **12 is still the product default** (Bootstrap/Atlassian/Polaris/Primer/Bulma/Fluent). Outliers: Carbon v11 = **16** (was 12 in v10 — version-dependent), Ant = **24**, Material = **4/8/12**. Two schools: fixed-count-variable-span (Bootstrap/Carbon/Ant) vs variable-count-per-breakpoint (Material/NB/Prism2 — the Figma design-grid convention). Convergent: 12 + the 4/8/12 design ladder as the mental model; 16/24 are deliberate dense-data choices. Prism2's 2→2→4→8 lower steps are over-granular.

**Q3 — gutter/margin.** Scale shallowly: **16 mobile → 24 → 32 desktop** (Atlassian/Prism2/M3/NB); Bootstrap is flat 24; Carbon makes gutter a *mode* (32/16/1) not per-BP. Margins run a step larger at the top (→40/48). **Every value is a multiple of the 8px spacing scale** (Atlassian literally aliases `space.200/300/400/500`). The single most important finding: **gutter/margin are spacing-scale aliases, not independent tokens.**

**Q4 — fluid vs fixed (the parked decision).** Field default = **fluid-first with an opt-in fixed max-width cap**, not a choice between two. Bootstrap/Bulma's stepped-fixed `.container` (Bootstrap 540/720/960/1140/1320) is legacy; the modern equivalent is one fluid container + one `max-width`. Systems ship both only as *modifiers* (`.container` vs `.container-fluid`); **nobody ships Prism2's full fluid+fixed token duplication.** A **narrow/reading container ~640–768px** is a real separate pattern (NB `narrow 720`; 65–75ch measure).

**Q5 — is the 12-col grid still load-bearing?** **It's shifted from code primitive to design artifact.** Modern systems ship breakpoints + container max-widths + the spacing scale and let native CSS Grid + container queries do layout (Tailwind never shipped a column framework; Polaris/Atlassian grids are thin CSS-Grid wrappers). The 12-col endures as Figma alignment + the 4/8/12 mental model. Container queries (`@container`, cross-browser since ~2023, Tailwind v4 core) handle component responsiveness; breakpoints still own the page shell — complementary. For marketing/expressive (agency) work, rigid 12-col reads as "product UI"; bespoke work leans editorial CSS-Grid. **Emit the column grid as a design artifact; don't assume column-span consumption.**

**Q6 — validation set.** Bootstrap 5: BP 0/576/768/992/1200/1400, `.container` 540/720/960/1140/1320, 12 cols, 24px gutter flat. Carbon v11: BP 320/672/1056/1312/1584, 16 cols, margin 0/16/16/16/24, gutter 32 wide/16 narrow, max 1584.

**Q7 — Figma modes.** Established community pattern: a variable collection whose **modes = breakpoints**. Best practice: **separate collections per concern** (colour gets light/dark; layout/typography get breakpoint modes) so they compose independently without combinatorial explosion. Mode limits (2026): Pro 10 / Org 20 / Enterprise unlimited. DTCG has no native mode concept — use `$extensions`; Tokens Studio implements breakpoints as Figma modes.

**Q8 — generation lever.** Per-brand variables: **breakpoint values** (primary), base **column count** (mild), **container max** + narrow. Effectively universal (bake in): t-shirt names, the gutter/margin ladder shape (spacing aliases), fluid-first containers, the reading container. **Minimal input: { breakpoint floors[], base column count }** + the existing spacing scale + one container.max → derive the column ladder, gutter/margin ladder, ranges, Figma modes, narrow container.

---

## Recommendation (full)

5 t-shirt min-width breakpoints (`sm 0 / md 768 / lg 1024 / xl 1440 / 2xl 1920`),
brand overrides the values, count-aware names (≤5 anchor at sm; 6+ prepend xs).
12-col base (one knob; 16/24 niche) emitted as a 4/8/…base ladder = a Figma
layout-grid / design artifact, *not* the code contract. Gutter/margin alias the
8px spacing scale (16/24/32 · 16/24/48). Fluid-first + `container.max` cap +
`container.narrow ≈ 720`; collapse fluid-vs-fixed (no dual tree; fixed-stepped
deferred). Breakpoint-keyed values → a separate Figma layout collection (modes =
breakpoints). Lever = breakpoint floor array + base column count.

**Sourced:** breakpoint px, Bootstrap/Carbon tables, gutter/margin-as-spacing,
container max-widths, Figma mode limits, DTCG-has-no-modes, Carbon 12→16 change,
12-col-as-design-artifact direction. **Judgement:** the default value set,
collapsing fluid/fixed, dropping Prism2's low column steps, the two-knob lever.

## Sources
Bootstrap: getbootstrap.com/docs/5.3/layout/ · Tailwind: tailwindcss.com/docs/responsive-design · Material 3: m3.material.io/foundations/layout/applying-layout/window-size-classes · Carbon: carbondesignsystem.com/elements/2x-grid/ · Atlassian: atlassian.design/foundations/grid · Polaris: polaris.shopify.com/tokens/breakpoints · Primer: primer.style/product/primitives/size · Fluent: fluent2.microsoft.design/layout · Ant: ant.design/components/grid · Bulma: bulma.io/documentation/columns · POV: css-irl.info/is-it-time-to-ditch-the-design-grid/ (Barker 2021), moderncss.dev/solutions-to-replace-the-12-column-grid/ (Eckles 2020) · Figma modes: help.figma.com Modes-for-variables · DTCG: w3.org/community/design-tokens (stable 2025-10-28).

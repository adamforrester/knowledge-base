You are researching **how mature design systems tokenize breakpoints and the
responsive grid (layout)** for a senior design systems practitioner at a digital
agency. The output is a structured knowledge document.

This designs a white-label layout generator and resolves a parked decision (fluid
vs fixed grids). The vault currently has **no** dedicated layout/grid/breakpoint
file — coverage is scattered (typography's container queries). Cover product AND
marketing-expressive contexts.

This is not an introductory guide — assume the reader knows breakpoints, CSS Grid,
container queries, and design tokens. Explain the *model* and the *numbers*.

Research scope — verify against current primary docs; date version-dependent
claims; flag confidence.

1. **Breakpoint count, values, naming** — the actual px + names each system ships;
   what's convergent (5 vs 6); t-shirt vs device vs semantic; min-width vs range.
2. **Column count + how it changes across breakpoints** — is 12 still default;
   Material 4/8/12, Carbon 16, Ant 24; fixed-count-variable-span vs variable-count.
3. **Gutter + margin per breakpoint** — real values; do they scale; relationship
   to the spacing scale.
4. **Fluid vs fixed containers (the parked decision)** — fixed max-width-per-
   breakpoint vs fluid; which the field defaults to in 2026; do systems ship both;
   container max-widths + a narrow/reading container.
5. **Is a 12-col grid still load-bearing in 2026?** — with CSS Grid, subgrid, and
   container queries, has the classic column grid become a design artifact rather
   than the layout engine? Practitioner POV.
6. **Real numbers** — Bootstrap + Carbon full breakpoint/container/columns/gutter
   tables as a validation set.
7. **Breakpoints as Figma variable modes** — the modes-as-breakpoints pattern;
   separate collections per concern so theme × breakpoint compose.
8. **Generation lever** — the minimal input that derives breakpoints + grid; what
   varies per brand vs what's universal.

Output: comparison table across ≥8 systems (Bootstrap, Tailwind, Material 3,
Carbon, Atlassian, Polaris, Primer, Fluent, Ant, Bulma) first; then per-question
synthesis; then a concrete recommendation for a white-label generator (breakpoint
set, column model, gutter/margin, fluid vs fixed, container max-widths incl. a
narrow container, generation lever) with rationale + citations. Flag sourced vs
judgement.

Depth: Expert audience. Resolve the fluid-vs-fixed decision with evidence; give
numbers a generator can be validated against.

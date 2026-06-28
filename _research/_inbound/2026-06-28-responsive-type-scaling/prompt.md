You are researching **how responsive type systems set the relationship between
mobile and desktop font sizes** for a senior design systems practitioner at a
digital agency. The output is a structured knowledge document.

This validates (or replaces) a guessed model. A token engine derives fluid type
via `clamp(min, preferred, max)` where `min` is the mobile size and `max` the
desktop size, over a curated rem ladder. The first cut computed the mobile
endpoint as desktop × a flat per-group factor — a guess. We need the real basis:
is a flat factor even the right model, and what numbers do shipping systems use?

This is not an introductory guide — assume the reader knows fluid type, `clamp()`,
modular scales, and what a design token is. Explain the *model* and the *numbers*,
not the basics.

Research scope — cover all of the following; verify load-bearing claims against
current primary sources (system docs/source repos, Utopia, platform HIGs, WCAG);
date anything version-dependent and give the verification path.

1. **Flat factor vs dual-scale vs size-dependent shrink — which model?**

   - Does any major fluid-type system use a single uniform scale-down?
   - Utopia's dual-ratio model (calmer ratio at min viewport, punchier at max) and
     how it compresses hierarchy on mobile rather than scaling uniformly.
   - For a curated (non-ratio) ladder, the right analog: flat factor, size-dependent
     rung drop, or recomputing two scales.

2. **Utopia's concrete defaults** — min/max viewport, min/max ratio, base size, and
   the resulting mobile-vs-desktop size for body, a mid heading, a large display.

3. **Real numbers from shipping systems** — IBM Carbon (explicit per-step fluid
   min/max), Material 3, Apple HIG (Dynamic Type, iPad vs iPhone), Polaris/Primer/
   Atlassian where published. Tabulate mobile vs desktop px per role.

4. **Does body/UI stay constant across viewports, or bump slightly?**

5. **How much should a hero shrink?** — a 96–160px desktop hero becomes what on a
   360–400px phone? Concrete numbers + the line-count / readability rationale.

6. **Minimum readable floors on mobile** — body, caption, heading (WCAG / platform
   HIG / practitioner floors) that should bound the mobile endpoint.

Output format: structured markdown with a model recommendation first (flat factor
vs dual-scale vs size-dependent), then a concrete recommended mobile-endpoint
mapping for a curated ladder, with rationale and citations. Where the field has
consensus, state it; where it's a calibration choice, say so. Flag every place a
DS tool has a known gap. Date claims that depend on current platform state.
Include a references section linking to primary sources (Figma/Carbon/Utopia/
Apple HIG/WCAG/practitioner blogs).

Depth: Expert audience. Do not explain `clamp()` or modular scales — explain the
mobile↔desktop sizing relationship and why bigger sizes shrink more.

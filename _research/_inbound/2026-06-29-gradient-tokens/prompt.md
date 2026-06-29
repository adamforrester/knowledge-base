# Research brief — tokenizing gradients (DTCG, the field, and Figma)

*Filed 2026-06-29 from the Prism3 token-engine work, where gradients were the last
token category to build. Single-sided run (Claude in-repo); see `claude.md`.*

We need a decision-useful POV on gradient tokens for a design-token generation
engine and the consulting practice KB. Four questions:

1. **Are gradients composites?** Is `gradient` a composite type in DTCG, and what
   is the exact `$value` shape (stops? fields per stop)?
2. **DTCG support.** Does the DTCG gradient type encode the gradient KIND
   (linear/radial/conic) and ANGLE/direction, or is it stops-only? What is the
   spec's current (2025) state, and what are the open issues?
3. **What does the field do?** How do mature design systems tokenize gradients —
   Material, Carbon, Atlassian, Adobe Spectrum, Polaris, SLDS, Primer, Fluent,
   Tailwind, USWDS? Who abstains, who ships, and in what shape (CSS string vs
   decomposed composite vs utilities)? Are stops aliased to the colour ramp?
4. **How do gradients map to Figma?** Variables vs Styles; can a variable hold a
   gradient; what binds on a gradient stop; how does the code→Figma round-trip
   work; what is the colour-interpolation story (OKLCH vs sRGB)?

The deliverable feeds (a) the engine's gradient axis and (b) a KB POV on whether
and how a practice should tokenize gradients.

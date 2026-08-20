# Verification pass — Image

**Same provenance as the sibling folder, and the same caveat.** This is not a research transcript.
`components/image.md` was written first, from knowledge, with no research run behind it, and its §14
carried version-dated citations that had not been checked. A reviewer held the PR for the missing
`_inbound/` folder; the folder was the symptom and the unverified §14 was the defect.

This pass ran **after** the brief, against primary sources. `verification.md` records what was found
verbatim and what the brief had to change.

## Questions put to primary sources

The three the brief **rests on** — where being wrong moves a section:

1. **Is `alt=""` genuinely different from an omitted `alt`, and do screen readers fall back to the
   filename?** This is §6's whole contract and the reason §3 makes `alt` a *required prop with a
   permitted empty value* — deliberately stricter than HTML. If the two behave the same, that
   strictness has no justification and §3 should relax.

2. **Does `loading="lazy"` on an above-the-fold image measurably worsen LCP?** §11 calls it "the
   standing own-goal" and asserts a page made *measurably slower* by something that looks like an
   optimization. An assertion of a measured effect needs the measurement.

3. **Does Polaris ship `Thumbnail` as a component separate from `Image`?** §10 cites it as the thing
   we deliberately do *not* copy — treating thumbnail as a size rather than a component. If Polaris
   has since folded it in, §10's example is stale.

## Sources

- MDN → `Web/HTML/Reference/Elements/img`, for the `alt` contract
- web.dev → the LCP lazy-loading article, for the measurement
- `Shopify/polaris` → `polaris-react/src/components/Thumbnail/Thumbnail.tsx`, the TypeScript interface

Type definitions over docs pages where both exist, for the reason recorded in the Text folder's method
note: a page describes intent and can move; a shipped interface is what a consumer meets.

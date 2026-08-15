# Verification pass — Text

**This folder is not a research transcript, and saying so is the point.**

Every other `_inbound/` folder in this vault records a research run that *preceded* its brief: a prompt
was issued, an agent surveyed the field, and the brief was synthesised from the output. `claude.md`
is that output.

This one records something different and weaker. **`components/text.md` was written first, from
knowledge, with no research run behind it.** Its §14 "Sources cited" listed version-dated entries for
Polaris, Radix, Chakra, Spectrum, Base Web, Ant, Material and Carbon, formatted exactly like the
verified citations in every other brief — and none of them had been checked.

A reviewer held the PR because the folder was missing. The missing folder was the **symptom**; the
defect was a §14 that asserted verified-looking citations produced by no verification. This is the
same failure the vault's own `_schema.md` names — *a brief never silently launders an unverified claim
into an asserted default* — and it is the same shape as an earlier incident in the sibling repo, where
one unsourced citation sat between two sourced ones and the pattern implied it had been checked.

So this pass ran **after** the brief, against primary sources, to establish which of its claims were
true. `verification.md` records what was asked, what was found verbatim, and — the part that matters —
**what the brief got wrong and how it changed as a result.**

## Questions put to primary sources

The brief makes many claims. These are the ones it **rests on** — the ones where being wrong moves a
section rather than a sentence. Everything not on this list stays asserted-without-a-source and is
marked as such in the revised §14.

1. **Does Polaris ship `as` and `variant` as separate props on `Text`?** §3's entire argument — that
   the semantic element and the visual step are independent axes — cites Polaris as the reference API.
   If they are one prop, §3 loses its witness.

2. **Does Polaris *state the rationale* for the separation?** The brief claimed it does, in as many
   words. A design system demonstrating a decoupling and a design system *arguing* for one are
   different kinds of evidence, and §3 leaned on the second.

3. **Does Base Web ship per-style typography components?** §10 uses it as the counter-example — the
   third path that multiplies the API by the length of the ramp. If it ships a single `Text`, §10's
   three-way split collapses to two.

## Sources

Primary only, and source-of-truth over documentation where the two differ — a docs page describes
intent, a type definition describes what shipped:

- `Shopify/polaris` → `polaris-react/src/components/Text/Text.tsx` (the TypeScript interface)
- `uber/baseweb` → `src/typography/index.tsx` (the export list)

The published Polaris docs URL redirected to an API index and the component page 404'd, which is
itself worth recording: **the citation in the first draft pointed at a page that does not resolve.**

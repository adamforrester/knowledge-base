# Prompt — the behaviour half of the vanilla HTML/CSS projection

Run date: 2026-08-21. Filed for prism3 issue #882.

---

## A note on this brief, recorded rather than smoothed over

**No prompt was supplied for this run.** The requesting message said one had been "provided
separately" and none arrived. Rather than block, the brief below was **derived** from prism3 `#882`,
`docs/19` §3, and the requester's own framing of the gap. It is recorded here in full so that a
second agent can be run against the identical text later, and so that anyone auditing this run knows
the brief is reconstructed rather than issued.

**This is therefore a single-agent run.** The `_research/README.md` convention is one prompt against
two agents, and the corroboration that convention exists to produce is **absent here**. Every
finding below should be read at the confidence a single pass earns. The synthesis flags this again.

---

## What is already settled and must not be re-derived

`docs/19` §3 ranks the output targets, and the ranking was set by two independent research passes
with fetched URLs after the web-components lean was retired. **Rank 2 — a class-based skin over
platform-generated markup — is what ships.** AEM Edge Delivery (#1 platform) and Drupal (#2) both
render server-side HTML their platforms augment with classes.

Do not re-open the ranking. Do not re-open #252 (author-our-own vs wrap), which `19` §3 explicitly
parks and which now governs only ranks 5–6.

## The gap that is the question

`19` §3 says: *"Behaviour = framework-agnostic headless, and the author-our-own-vs-wrap fork (#252)
beneath it, now govern only ranks 5–6."*

So **behaviour is unanswered for the rank we actually ship.** #882 states the wall: vanilla HTML/CSS
has no expression for `dialog`'s focus trap, `menu`'s roving tabindex, `tabs`' keyboard model,
`select`'s listbox semantics — which is `docs/40` tranche 4 almost exactly, plus `select` reaching
back into tranche 1.

#882 offers three options:

1. A small vanilla behaviour layer shipped alongside the HTML/CSS.
2. Web components, at `19` §3 rank 6.
3. HTML/CSS plus a **documented behaviour contract** each framework target implements.

## Questions

1. **What do the two named platforms actually do for behaviour today?** Not what is possible — what
   AEM Edge Delivery and Drupal SDC natively expect. Does either have a per-component JS mechanism
   already?
2. **How much of tranche 4's behaviour is now platform rather than library?** `<dialog>`, the popover
   API, invoker commands, customizable `<select>`, native `<details>`. Baseline status and dates,
   not impressions.
3. **What is the prior art for option 1** — a class-based design system that also ships a small
   vanilla behaviour layer? How much of its catalogue needs JS, and how is behaviour bound to markup?
4. **What is the prior art for option 3** — a documented behaviour contract that separate
   implementations sign up to? Does anyone publish one machine-readably?
5. **If option 1 is chosen, does #252 reappear** in the vanilla layer — author our own, or wrap an
   existing framework-agnostic engine? Is there a vanilla-target engine to wrap at all?

## Method constraints

Fetch, don't recall. Every platform or browser-support claim needs a URL that was actually opened,
with the date. Where two sources disagree, record the disagreement rather than picking. Where a
claim rests on one source, say so in the claim.

## What matters most in the output

The requester is taking this to a developer partner. **Which questions the literature cannot answer
matters as much as the answers** — knowing what to bring to that conversation as an open decision is
the point.

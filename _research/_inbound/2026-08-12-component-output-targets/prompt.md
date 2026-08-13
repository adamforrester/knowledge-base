# Research intake — Prism3's component output targets, now that the platforms are named

> **Source:** commissioned from `prism3-tokens` #252 (comment of 2026-08-12), which parked the
> headless-behaviour decision pending this pass. Run against two agents per `_research/README.md`;
> this folder holds the brief and both raw outputs.

---

**Question.** What should Prism3's component output targets be, and in what order — given that the
delivery platforms are now named rather than abstract?

This supersedes the reasoning in `docs/19` §3 (prism3 repo), which set "web components primary, React
a thin wrapper" from deployment-neutrality in the abstract, before anyone had written down which
platforms we actually ship to. The owner's position is that the original direction came from research
that may not hold, so treat `19` §3 as a hypothesis under test, not a premise.

**The constraints, stated by the owner 2026-08-12:**

- AEM is the #1 delivery platform. Drupal is #2. Sitecore, Salesforce Page Designer and others are a distant third.
- React's primary use case is prototypes, not client site builds — the agency does not build many React sites.
- iOS / Flutter / Android native libraries are a possible later target.
- "It could be vanilla HTML and CSS for all I care."

**Read first, do not re-derive:** `docs/19` §3 (the lean under test), `docs/15` (deployment
neutrality), `docs/13`'s AEM mapping section ("the path is projection, not conversion"), `docs/27`
Idea 2 (the AEM phasing), `docs/38` (the arcs this feeds), and KB file 10 (CMS and Platform
Integration — AEM at depth, Drupal secondary). Also read #252's comment of 2026-08-12, which records
what has already been verified so you don't spend the pass re-checking npm.

**Answer these, in order:**

1. What does an AEM engagement actually consume? `27` Idea 2 says Phase 1 is a tokens clientlib plus a CSS skin over Core Components, zero custom components. Is that right, is it still current (SPA Editor deprecated Jan 2025; Edge Delivery as the 2025+ direction), and what is the real Phase-2 shape — web components via clientlib, HTL-native components, or something else? Same question for Drupal: theme libraries plus Twig, and where Single Directory Components (Drupal 10+) fit.
2. Does web-components-primary survive contact with those two platforms? State the case for and against honestly. If the answer is that CSS-over-server-rendered-markup is the primary projection and WC is secondary, say so — that is a legitimate finding, not a failure.
3. What is the minimum set of projections worth building, and in what order? Candidates: a CSS/token layer, AEM components, Drupal components, web components, React (prototypes), native mobile. Rank by commercial value against the stated platform priorities, not by technical elegance.
4. What does each projection demand of the definition layer? `13` notes an authorable CMS component needs a content model — which fields exist, which are required, which the author edits vs. which the system fixes — and that neither React nor WC forces you to state it. Which projections impose requirements `component-schema.ts` cannot currently express? This is the finding that feeds back into Arcs 1–3.
5. Only if WC survives question 2: revisit the headless-behaviour fork with the corrected facts in #252's comment (all three named candidates peer on react/react-dom; Zag's machines have no peers), plus the cross-root ARIA constraint — ARIA IDREF associations do not cross shadow-root boundaries, and Reference Target is prototyped in Chromium and WebKit but not shipped unflagged in any browser as of 2026-08-12.

**Method constraints:**

- Fetch, don't recall. A cited external fact is a claim like any other. This repo has already shipped one fabricated citation (a Style Dictionary issue asserted as open that was closed as completed); it was caught in review and the failure class is recorded in `docs/00-progress.md`. Every platform claim needs a URL that was actually opened, with the date.
- Platform claims about AEM, Drupal and Sitecore date fast. KB file 10's own currency note says to verify specific tooling claims against current docs before treating them as load-bearing. Do that.
- Where you find the KB or `docs/19` is wrong, say so plainly and name the file and section. That is the most valuable output of this pass.
- Deliverable: a findings file under `_research/` per that directory's convention, plus a recommendation with a stated confidence level and the specific evidence that would change it.

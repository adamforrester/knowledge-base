# Synthesis — component output targets (the #252 run)

> Reconciles the two raw outputs in `_research/_inbound/2026-08-12-component-output-targets/`.
> Path A was used because the run reaches a **reversal** of a standing architectural decision
> (`prism3 docs/19` §3, "web components primary"), and because the findings land across a prism3
> decision *and* at least two numbered files. Filed 2026-08-13.

---

## The headline: the reversal survives an independent second pass

The Claude side concluded *"Does web-components-primary survive? **No** — and that is a finding, not a failure."* The external side, run on the identical prompt and **without access to the prism3 repo**, reached the same conclusion independently: *"The architectural premise established in `docs/19` §3 … does not survive operational integration with enterprise content management systems."*

**That convergence is the most important output of this run.** A single agent overturning a standing decision was the reason issue #15 flagged this as needing a second pass; two independent agents reaching the same reversal, from different starting knowledge, is materially stronger evidence than one. The reversal should be treated as sound.

Both land in the same place on the replacement: **CSS-over-server-rendered-markup is the universal primitive**, with web components demoted to a secondary, leaf-level projection for self-contained interactive widgets.

## Where the two agree (high confidence)

Convergent findings, independently reached:

1. **The reversal itself** — WC-primary does not survive contact with AEM and Drupal.
2. **SPA Editor deprecated January 2025** (AEM as a Cloud Service 2025.01 and AEM 6.5.23), with the React/Angular/Vue SDKs frozen to P1/P2 security fixes only.
3. **Edge Delivery Services is Adobe's modern direction**, and its unit of consumption is the **block**: a co-located vanilla-JS module exporting `decorate(block)` plus an isolated stylesheet, over server-delivered semantic HTML — no framework, no hydration.
4. **Drupal SDC is core** (10.3+ / 11): `{name}.component.yml` + `{name}.twig` with co-located `.css`/`.js` auto-discovered, and a hard split between **typed props (JSON Schema validated)** and **unstructured slots**.
5. **Zag.js is the framework-neutral behaviour engine.** Radix and React Aria peer on `react`/`react-dom`, which would tether behaviour to the React runtime; Zag's machines have no framework peers and emit plain ARIA/`data-*` attribute dictionaries any host can consume.
6. **Cross-root ARIA is a genuine platform barrier.** IDREF-based associations (`aria-labelledby`, `aria-describedby`, `aria-controls`, `aria-activedescendant`, `<label for>`) do not resolve across a shadow boundary, Reference Target is not shipped unflagged anywhere, and it **cannot be polyfilled** — a script shim cannot grant the accessibility tree the ability to pierce encapsulation.
7. **The definition layer needs a content model.** CMS-authorable components require a statement of which fields exist, which are required, and which the author edits versus which the system computes — a thing neither React props nor WC attributes ever force you to write down.
8. **The build order**, ranked commercially rather than technically: CSS/token layer → AEM → Drupal → web components → React (prototypes only) → native mobile (deferred).

## Where the external pass goes further

Three additions worth adopting, none contradicted by the Claude side:

**Light DOM specifically, not just "WC secondary."** The sharper move is to name the culprit as **Shadow DOM**, not web components as such, and to recommend **Light DOM custom elements** driven by Zag machines. This resolves both failure modes at once: light-DOM IDs resolve natively (no cross-root ARIA problem) and global tokens cascade in (no `::part`/custom-property penetration tax).

**A concrete mechanism for why Shadow DOM breaks EDS.** EDS `decorate(block)` expects **direct light-DOM access** to parse child elements, manipulate table rows and rearrange nodes. Putting that structure inside a shadow root breaks the assumptions of the EDS boilerplate utilities. That is a specific, checkable reason rather than a general preference — and it is independent of the accessibility argument, so the two reinforce each other.

**The Universal Editor schema demands, concretely.** An authorable EDS block needs a model definition (`_block-name.json` / `component-models.json`) mapping authoring fields onto edge HTML table cells, plus two layout concepts a component schema does not normally carry — **element grouping** (several text fields into one cell container) and **field collapse** (image URL + asset reference + alt text into one media element) — plus `component-filters.json` to constrain which children an author may insert. This is the most actionable part of the run for the definition layer.

## Where to hold back — the verification gap

**Stated plainly because the prompt was explicit about it.** The brief required *"Fetch, don't recall … Every platform claim needs a URL that was actually opened, with the date,"* and cited a prior fabricated-citation incident as the reason. **The external output carries no URLs and no fetch dates.** It offers checkable identifiers — Chromium feature #5188237101891584, WebKit bug #290744, Mozilla bug #1769586, "origin trial 133–135, shipping estimated 152" — but nothing recording that those were opened. The `[cite: 7, 11, 12]` markers in its tables are artifacts, not references.

The practical reading:

- **Where the two passes overlap, treat it as verified** — the Claude side did carry fetch dates (2026-08-13) for the AEM/Drupal claims, and the external independently agrees.
- **Where the external is alone — especially the browser-status table — treat it as unverified** until someone opens those trackers. The Reference Target shipping estimate in particular is the kind of forward-looking version claim that ages badly and should not go into any KB file without a check.
- The external pass also **could not read the prism3 repo**, so it took `docs/19` §3 and the constraints from the prompt's summary rather than the source. That is *good* for independence on platform facts, but it means it did not verify the prism3-internal premises.

## What this changes in the vault (not yet promoted)

Two genuine gaps, filed rather than promoted — each is a real piece of work, not a line edit:

**1. `10-cms-and-platform-integration` has no Edge Delivery Services coverage at all.** The file is current and correct on the SPA Editor deprecation and the Universal Editor direction, and it already notes that Shadow DOM can interfere with Universal Editor click-target instrumentation. But its three AEM integration options are **Web Components / React-HTL / HTL-native** — EDS is not among them, and both passes now say EDS is the modern Phase-2 target. Relatedly, the file's own open question #1 (*"Web Components vs. HTL-native for new AEM work. Web Components are more portable and better positioned for the Universal Editor era"*) is the exact claim this run pushes back on.

**2. `28-web-accessibility-implementation` has no cross-root ARIA treatment.** It already documents the ARIA 1.3 **IDREF reflection properties** (`ariaDescribedByElements`, `ariaLabelledByElements`, `ariaOwnsElements`, `ariaControlsElements`), which is the adjacent element-reference machinery — but nothing on the shadow-boundary limitation, Reference Target, or the resulting light-DOM recommendation. Given how much of the field is shipping web components into design systems, "shadow DOM breaks IDREF association and you cannot polyfill it" is a vault-tier accessibility finding.

Both are worth a considered pass rather than a bolt-on, especially since the light-DOM conclusion bears on `05` (headless vs opinionated) and `03` (component architecture) too.

## Recommendation

- **Accept the reversal.** Two independent passes, same conclusion, with distinct supporting mechanisms (accessibility *and* EDS DOM manipulation). Prism3 should discard WC-primary from `docs/19` §3.
- **Adopt the light-DOM refinement** — it is strictly better than "WC secondary" and resolves both failure modes with one decision.
- **Verify the browser-status specifics** before any of it lands in a numbered file.
- **Promote the two vault gaps separately**, at KB-quality depth, rather than as an appendix to a prism3 decision.

# Research intake — how should a design system model "surface context" (inverse / on-color)?

> Standalone brief supplied 2026-08-20, feeding a design decision in the Prism3 engine repo.
> Findings report; the recommendation is explicitly one section among several, not the deliverable.

The full brief as given is reproduced below so both agents receive identical input.

---

**The decision.** A button (or checkbox, icon button, link…) sometimes sits on a dark hero band, a
brand-color section, or an image overlay, where its normal colors lose contrast. The tokens exist;
the open question is **where that context lives in the component API**. Four candidates:

1. A **variant axis** on the component — `surface: "default" | "inverse"`, doubling the matrix.
2. An **appearance/emphasis value** — folding `inverse` in beside `filled | outline | text`.
3. An **inherited cascade** — the component declares nothing; a container publishes surface context and children pick it up through CSS custom properties or equivalent.
4. A **theme mode** — inverse is another axis of the theme, like light/dark, resolved at the token layer.

The project currently has **three answers shipping simultaneously** — one component uses a variant
axis, one uses an inherited-cascade prop defaulting to `"inherit"`, one has nothing and relies on
per-instance overrides. That inconsistency prompted the research.

**What makes it hard.** Figma variables can vary *only* by mode, so option 3 may be inexpressible in a
Figma library even if right in code. Option 1 multiplies combinatorics (one component already projects
to 648 Figma variant members). Option 4 multiplies modes, crossed with any existing mode axis.

**Delivery platforms:** Adobe AEM Edge Delivery Services and Drupal Single Directory Components — both
server-render HTML and decorate it with classes. React is secondary.

**The questions**, each answered separately, discriminator being *what a developer types and what a
designer clicks* rather than how a system describes itself:

1. **Field survey** — Material 3, Carbon, Spectrum, Polaris, Primer, Fluent 2, Salesforce Lightning, Atlassian. Classify each into 1–4 or name a fifth. Cite the actual API: prop name, container component, token name, theme class. Official docs and public source, not blog posts.
2. **The container-cascade pattern, concretely** — how it works mechanically in CSS; documented failure modes: specificity, nested inversions, partial inversion, server-rendered markup where container and child are authored separately.
3. **The platform question, which matters most** — for EDS and SDC specifically, is there a documented idiomatic way for a container to publish styling context that descendants inherit *without each component declaring a prop*? Quote the docs. "No established pattern" is a finding, not a gap.
4. **Figma: is inverse a mode?** Any published system using Figma modes for surface context as distinct from light/dark? Documented mode ceilings, plan restrictions, how teams handle two crossing axes. Include Figma's own guidance.
5. **Cost and regret** — for systems choosing option 1, how much did the matrix grow, and is there public record of regret or migration? Equally, any record of a cascade failing at scale.
6. **Accessibility** — does surface context change what a component must guarantee under WCAG 2.2, particularly 1.4.11 and 1.4.3? Focus indicators are the sharp case: a three-color relationship that changes with surface. Published guidance for inverse or image backgrounds?
7. **Falsification** — what evidence would show option 3 is wrong? What would show option 1 is? Argue both.

**Output:** structured by question; every factual claim carries a URL and access date, with direct
quotation where load-bearing. Then, separately: **VERIFIED** / **INFERRED** / **COULD NOT VERIFY**,
the last being specific about what was searched and as valuable as the others. Finish with a
recommendation, the strongest argument against it, and what to measure to settle it empirically.

**Rules:** do not invent citations — a missing source is a finding, a fabricated one is a failure.
Report disagreement rather than averaging it. Where documentation and source code differ, **the source
code wins** — say so and cite both. Prefer primary sources.

# Research intake — surface context in white-label, multi-brand and owned-code design systems

> Brief supplied 2026-08-20. Follow-on to `2026-08-20-surface-context-modeling`, which surveyed eight
> first-party systems and did not address the white-label case. Reproduced verbatim so both agents
> receive identical input.

---

**The gap.** The previous pass surveyed Material 3, Carbon, Spectrum, Polaris, Primer, Fluent 2,
Atlassian and Salesforce Lightning on how a component adapts on a dark band, brand-colour section or
image overlay. **Every one of those systems controls its own surfaces.** This project cannot: it ships
a kit to a client who will build surfaces nobody has seen. One suggestive data point — **SLDS, the
surveyed system closest to a white-label model, ships two mechanisms simultaneously**, a
`.slds-theme_inverse` container *and* per-component `_inverse` modifiers, with a hand-maintained
`:not(.slds-button--neutral)` exclusion in the container stylesheet. That may be sloppiness; it may be
what happens when you cannot control the surfaces. **Determining which is a central question.**

**Delivery:** AEM Edge Delivery Services and Drupal SDC, both server-rendered HTML decorated with CSS
classes. The kit is rebranded and used by client organisations to build their own pages.

**The four candidate architectures:** (1) a variant axis on the component; (2) an appearance value
beside `filled | outline | text`; (3) an inherited cascade published by a container; (4) a theme mode
resolved at the token layer.

**The questions.**

1. **Multi-brand and white-label systems.** Survey systems built to be rebranded or to serve many brands from one codebase — suggested: Telefónica Mística, Volkswagen Group, Marriott or IHG, Mercado Libre (Andes), Zeta, ING, Santander. Replace any you cannot source and say which. For each: how is surface context handled, and **does the brand-theming layer and the surface-context layer use the same mechanism or different ones?** That second question is the one that matters — if both want to be "the thing that changes token values," they may collide.
2. **Owned-code / theming-first libraries — weight this heavily.** shadcn/ui, Radix Themes, Base Web, Panda CSS, StyleX (and Astryx if publicly documented). These ship code the consumer owns, which is structurally closest. For each: the theming primitive, how a *nested* context override works, and what happens when a consumer adds a component the library never shipped. Cite real source, including the actual CSS or config.
3. **The content-author experience — no prior report covered this.** In EDS and Drupal, what does a non-technical content author actually *do* to make a section inverted? Document the real authoring step. Then the harder half: **is there documentation of how components INSIDE that section are expected to consume the context?** Publishing may be documented; consuming may only be convention. If consumption is undocumented, say so plainly.
4. **The unanticipated-surface problem.** When a client builds a surface the authors never designed for — brand-colour band, photographic hero, video overlay — what do these systems tell them to do? Is there an extension point, an escape hatch, a documented "define your own context" path, or does the system not cover it?
5. **Extension and the name surface.** When a client adds their own component, how does it participate in surface context? Is there a documented contract — required custom properties, naming convention, lint rule — or is conformance left to inspection? Systems shipping an ESLint rule or token-usage gate are especially relevant; cite the rule.
6. **Cost of the token layer.** For options 3 or 4: how many tokens does the contextual layer add relative to the base semantic set? Any published figure or countable repository. If a system publishes its tokens, **count them and show your working.**
7. **Falsification.** What evidence would show a cascade is wrong *specifically for a white-label system* — as distinct from a first-party one? And what would show a variant axis is wrong for the same case? Argue both.

**Output:** structured by question, every claim with URL and access date and a verbatim quotation where
load-bearing. Where documentation is unavailable, **go to shipped code** and say so. Then **VERIFIED**
/ **INFERRED** / **COULD NOT VERIFY**, the last specific and neither padded nor omitted. Finish with a
recommendation for a white-label system and how it differs from a first-party one, the strongest
argument against it, and **whether the SLDS both-mechanisms pattern is a defect or an adaptation**,
with reasoning.

**Rules:** do not invent citations, token counts or API examples. Do not state numeric limits, plan
tiers or version thresholds without a source; if a figure is commonly cited but unsourceable, say
that. Where documentation and shipped code differ, code wins; cite both.

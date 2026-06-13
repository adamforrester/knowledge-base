You are researching the per-component documentation template — what a single component's documentation page contains, how it is structured, and what the practice should ship as a default deliverable on commercial design system engagements — for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: this is one of the more-frequently-named gaps in the practice's own self-assessment. The agency has architectural and tooling positions on documentation strategy (Storybook / MDX plus machine-readable metadata, four-layer AI documentation stack, generated-from-data per Curtis Components-as-Data, the four-tier metadata loop per Wolosin, accessibility annotation contract as `.ai.json` fields). What the practice does *not* yet ship is a prescriptive per-component documentation template — the standard shape every component page takes, with sectional discipline that scales across a 60-component system without becoming generic. Without it, every engagement reinvents the IA, every component author makes their own choices about how much to document, and clients receive 60 pages with 60 slightly-different shapes. The result is a docs site that looks comprehensive but reads as inconsistent, where consumers (designers, engineers, AI agents) cannot rely on finding a given piece of information in a given location. This research fills that gap. Cover the template as it should be in 2026 — Storybook 8 / MDX, machine-readable metadata as a default rather than aspirational, AI agents as a first-class consumer audience alongside humans, the components-as-data substrate that lets prose be generated where possible.

This is not an introductory documentation guide — assume the reader knows what a design system is, what Storybook is, what MDX is, what `.ai.json` and `AGENTS.md` are, what a component anatomy diagram is, and what the practice already encodes about documentation strategy in 04-documentation. Focus on the *template itself* — the sectional spine of a per-component doc page — at the level a senior DS lead can use to brief a UX Designer, ship to a client as a deliverable, and audit existing documentation against. Where decisions are context-dependent, give a decision framework rather than declaring a winner. Where the practice can claim defensible POV that external sources don't yet articulate, surface it.

Research scope — cover all of the following. Use these as the section spine of the output:

1. Why the per-component template is load-bearing

   - Why "the IA emerges naturally per component" is the documented anti-pattern across consultancy engagements.
   - The asymmetry between authoring cost (scales with component count) and consumption cost (scales with consumer count × use-frequency); why a standard template lowers both.
   - The four-audience problem: designers consuming the system, developers consuming components, AI agents consuming metadata, executives auditing the system. Each audience uses the page differently; each needs to find specific information at the same location across all components.
   - The "trust the docs" cliff: once a consumer finds one wrong page, they stop trusting the entire site. The template is a contract that bounds where wrong-ness can live.
   - The relationship to ACR/VPAT evidence — every component page is a per-component conformance dossier in microcosm.

2. The template's sectional spine

   - The minimum viable set: name / purpose / when-to-use / avoid-when / props (or properties / API) / states / accessibility / examples / do-don't / content / related / changelog. Where each section sits, why each is non-negotiable.
   - The order of sections — why "purpose first, props last" is the discipline that aligns with how consumers actually scan a page; the cases where this order breaks (foundational primitives where the props table is the answer to most questions).
   - Sections that are component-type-specific (form components need validation guidance; toast needs auto-dismiss; modal needs focus-trap notes; chart needs encoding guidance). How the template handles these — required slots vs. component-type extensions.
   - Sections external sources name that the practice should consider but may not adopt: design rationale / decision history (Mangialardi ADRs), version compatibility (Curtis), anonymous user research notes, consumer adoption metrics inline.
   - Sections that should be omitted by default: per-component "philosophy" sections, decorative changelog narratives, founder-letter framings. Why these accumulate noise.

3. Per-section depth — what each section actually contains

   For each section in the spine, specify what goes in it at the level a UX Designer can fill it in. Address at minimum:

   - **Purpose / when-to-use / avoid-when.** The intent layer. How prescriptive vs. how loose. Whether the language is component-as-noun ("a button is...") or component-as-verb ("use the button when..."). The avoid-when discipline as the highest-leverage section for AI consumers per the AI-Compatible doc and Wolosin's metadata loop.
   - **Props / properties / API.** Generated from data (Curtis) or hand-authored. Naming conventions, types, defaults, deprecated flags. The seam between "the props the consumer sets" and "the slots the consumer fills" — composition primitives need different treatment.
   - **States.** Rest / hover / focus / focus-visible / pressed / disabled / loading / error / empty / read-only. Visible vs. announced state. The per-state row format.
   - **Examples.** Examples-before-specs as a discipline (Figma DS x AI). Live (Storybook), code-paste (MDX fenced blocks), framework-specific snippets, design-mode (Figma frame). How many examples are enough; the canonical set per component-type.
   - **Do / don't.** Side-by-side. The discipline of pairing each "do" with an explicit "don't" for the same dimension. Why generic do/don'ts ("use clear language") accumulate noise vs. specific ones ("don't use Submit when the action is destructive").
   - **Accessibility.** Inline (per the practice's stance), not a separate page. The fields from 17-accessibility-annotation-contract: name mechanism, role, state, value, ARIA relationships, focus-return, forced-colors survival, APG keyboard model, motion treatment, gesture alternatives. Map each to the template row.
   - **Content guidelines.** Tone, error message patterns, empty-state copy, CTA labels. The seam with 04-documentation's UX Copywriter role.
   - **Related components.** The graph layer — what to use instead, what composes with this, what supersedes this. Why "see also" is informationally weaker than typed relationships ("alternative to," "composes with," "deprecated in favour of").
   - **Changelog.** Per-component, not just system-wide. SemVer per Curtis library tiers; the question of where deprecation announcements live.

4. The four-audience problem — what each audience needs

   - **Designers.** Examples and do/don'ts as the primary entry point. The Figma library link.
   - **Developers.** Code examples, props table, framework-specific snippets, the Storybook story.
   - **AI agents.** The `.ai.json` block with `when_to_use`, `avoid_when`, `business_context`, semantic prompt, accessibility schema. Description fields on every parameter.
   - **Executives.** The conformance dossier slot — accessibility evidence, version, adoption metrics where instrumented, deprecation status.
   - How the template surfaces each audience without forcing them to read the whole page; entry-point patterns (anchors, summary tables, search).

5. Generation, authoring, and the seam between them

   - Which sections are generated from the component data file (props, states, default examples, type signatures) vs. hand-authored (purpose, when-to-use, avoid-when, content guidelines).
   - The CI freshness check pattern: component code changes but metadata doesn't → build fails. Per AI-Compatible doc Ch.7.
   - The "single source of truth for X" model — components-as-data feeding Storybook, MDX, `.ai.json`, the docs site, the Figma library, all from one component definition.
   - Where authoring tooling falls short in 2026 — the gap between "we can generate this" and "we ship it generated by default."
   - The per-component template's relationship to the system-wide IA: how navigation, search, and category landing pages compose per-component pages into the consumer's flow.

6. Tooling decisions and recommendations

   - Storybook + MDX as the de-facto baseline for engineering-heavy systems. What Storybook 8 (and 9, where current) does well and where it falls short for documentation specifically.
   - Zeroheight, Supernova, Knapsack as the design-side or hosted alternatives. Trade-offs per consumer audience and engagement size.
   - Self-hosted vs. SaaS — portability concerns for regulated, on-prem, or EAA-procurement clients.
   - Decision framework for picking the docs platform per engagement: codebase culture, designer-engineer ratio, budget tier, regulatory constraint, scale of consumer base.
   - Where the system can be portable across docs platforms (the component data file is the source; each platform consumes it) vs. where it locks in.

7. Anti-patterns and failure modes

   - Generic-template overfit: every component page has the same template even when the template doesn't fit the component (a primitive icon doesn't need a "states" section).
   - Documentation-as-changelog: the page is mostly history, not current usage.
   - Implicit-context prose: written for the original team, references shared abbreviations and lore. Fails for new consumers and AI.
   - Zero-example pages: lots of prose, no live or pasteable examples. Designers and engineers leave.
   - Stale documentation: 60 pages, 12 of them out of date. Trust collapses.
   - "Tooling without authors": Zeroheight subscription, no UX Designer hours scoped to fill it. Empty rooms.
   - "Six weeks of tooling, one week of content" (per 04's failure-modes section).
   - Accessibility as a separate page: the visit pattern misses it.

8. The practice's POV — what we ship, why, and the commercial framing

   - The template as a default Documentation deliverable scoped in the SOW alongside the dedicated UX Designer role.
   - The relationship to scoping: a 60-component system × N hours per component template × the UX Designer + UX Copywriter mix, expressed as a unit cost.
   - What the practice can claim publicly: the template, the four-audience framing, the components-as-data substrate, the accessibility annotation as `.ai.json` fields, the conformance dossier slot.
   - Where the template positions the practice against tooling vendors (Zeroheight et al. ship templates; the practice's value is the editorial discipline and the components-as-data architecture, not the template alone).
   - The version-zero shape the practice ships in the next engagement — the actual template, ready to use, that an engagement could pull off the shelf.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where the field has clear consensus or one obvious choice, state it; where decisions are context-dependent, give a decision framework rather than declaring a winner. Flag tooling gaps that practitioners work around. Where claims depend on current platform state — Storybook version, MDX syntax, vendor product features, AI-tool capabilities — date them and note the verification path. Include a references section linking to primary sources (Storybook docs, Curtis on Components as Data and Operating Design Systems, Wolosin's metadata loop, Couldwell's Laying the Foundations, Mangialardi's Design Systems for Developers, Figma DS x AI, Mall's 90 Days of Design Systems, Zeroheight / Supernova / Knapsack docs, public exemplars like Atlassian Design System / Adobe Spectrum / Carbon / Polaris / Material Web).

Depth: Expert audience. Do not explain what a design system or Storybook is — explain what makes the per-component template load-bearing, why the field's existing exemplars succeed or fail, and what the practice should ship by default that closes the gap between "we have a docs site" and "every component page reads the same way and contains what every audience needs to find."

# Design-system teams as a discipline — at agency scale

The dominant body of DS-team literature is in-house product literature: Spotify's Encore, Atlassian Design System, Shopify Polaris, Airbnb's DLS-then-DLP, GitHub Primer, IBM Carbon, Adobe Spectrum, Microsoft Fluent, Material Design. The teams behind these systems persist for years, serve a single product (or a single product family), are budgeted on headcount, and have an indefinite horizon. Their team-building patterns are visible because their members write, speak, and post-mortem in public.

The agency reality is structurally different. Teams ramp up for an engagement, run for 6–24 months, hand off to a client team, and disband. The practice is a portfolio of engagements in different industries on different platforms with different commercial shapes, not a single product evolving over a decade. The people doing the work bill hours; the SOW shapes the headcount, not the other way around. The client may be the team within a year. Almost none of this is written down by senior agency-side practitioners — partly because agency-side IP is often treated as competitive and stays internal, partly because the cohort of senior agency-DS practitioners is much smaller than the in-house cohort, and partly because the work pattern (engagement after engagement) leaves less time for the kind of public reflection in-house DS leads have.

This document treats the DS team as a discipline of its own and reads the agency context as a structural difference, not as a degraded version of the in-house pattern. Eight sections in order: why the agency context matters; hiring and skill mix; the practitioner-count arc from one to a dedicated team; the agency-to-client handoff; internal rituals; career paths; distributed-team patterns; and burnout. The references section names the field's primary sources, with notes on which translate to agency contexts and which are in-house-product-shaped.

---

## 1. Why a DS team is a discipline of its own, and why the agency context changes the answer

### The discipline as discipline

A design-system practitioner is a stable, named professional role with a tacit-knowledge surface that does not collapse into "senior product designer" or "senior front-end engineer." The case for the discipline rests on five pieces of distinctive literacy that the role demands and that adjacent roles develop only incidentally.

**Tokens-as-architecture.** A design system is not a Figma library; it is a multi-tier token tree, a transformation pipeline, and a platform-specific rendering target. The DS practitioner reads tokens as architecture — primitive vs. semantic vs. component-tier composition, the alias graph, the resolved-value boundary across platforms, the DTCG specification's semantics, the Style Dictionary or Tokens Studio toolchain, the Generative Token pattern at portfolio scale. A senior product designer who has not done DS work can use tokens; a DS practitioner has internalised the token system as the load-bearing architectural primitive of every other deliverable.

**Components-as-contract.** A component in a DS context is not a UI element; it is an API surface (the prop matrix), a state machine (the variants and their transitions), a behavioural contract (focus, keyboard, AT semantics, motion), and a data shape (the components-as-data layer that AI surfaces and CMSes increasingly consume). The DS practitioner writes components for the consumer they have not met yet. The product designer writes components for the surface they're shipping.

**Governance-as-protocol.** A DS team enforces and evolves a contribution model — what comes from the team vs. what comes from product teams; how requests are triaged; how proposals become candidate components become released components; how breaking changes get released; how deprecation gets handled. None of this is invented per project; the field has converged on patterns (hub-and-spoke, federated, cyclical), and the practitioner reads governance as a designed protocol the same way they read APIs as designed protocols. Adjacent roles do governance reactively when forced; the DS practitioner does it intentionally as the discipline's central craft.

**Accessibility as stakeholder.** The DS practitioner reads assistive technology not as a constraint to comply with but as a stakeholder the system is built for. The four-engine × four-AT test matrix, ARIA 1.3 semantics, the user-preference media-query surface, focus-management patterns, the EAA / Section 508 conformance regime, the colour-pair contract for both WCAG and APCA — these are working knowledge, not a third-party audit produced once before launch.

**The field's vocabulary and lineage.** The discipline has a literature: Brad Frost on Atomic Design, Nathan Curtis on team models and contribution, Dan Mall on embedded design teams, Donella Meadows on systems thinking, Christopher Alexander on pattern language, the InVision Design Systems Handbook, the Design Systems Podcast back catalogue, and the increasingly large body of conference talks (Clarity, Config, Smashing, Into Design Systems, Frontside's earlier formats). A practitioner who can't situate their own work in this lineage is a generalist who has done some system work; one who can is a member of the discipline.

The discipline's identity formation is mostly lateral. DS practitioners come from product-design or front-end-engineering backgrounds with two to five years of system-adjacent experience, a moment of conversion (typically working with a senior DS lead who modelled the lens), and a deliberate investment in the field's literature and toolchain. The cohort is small. Estimates from the Design Systems Podcast community surveys and the periodic Sparkbox surveys put the dedicated-DS-practitioner population in the low tens of thousands globally (mid-2026), with senior practitioners (5+ years dedicated DS work) numbering in the low thousands. The senior population most agencies will hire from is small enough that hiring is a relationship-led process across the entire field, not a candidate-funnel process within the agency's geography.

### The agency vs. in-house structural difference

The dominant DS-team literature is in-house product literature, and the patterns it describes do not generalise cleanly to agency contexts. The differences are structural, not stylistic.

**Persistence vs. cycle.** An in-house DS team persists. The team that shipped Spectrum 1.0 in 2018 is the team that shipped Spectrum 2 in 2024 — same lead, much of the same core team, evolving under continuous architectural pressure. An agency DS team ramps up at engagement kickoff, runs for 6–24 months, and either disbands or rotates to the next engagement. The compounding asset is not the artefact (which lives at the client); it is the team's accumulated method, which has to survive disengagement intact.

**Single product vs. portfolio.** An in-house DS team optimises for one product (or one product family). The decisions accumulate against that product's constraints — its platform mix, its content surface, its localisation footprint, its internationalisation requirements, its commercial shape, its regulatory regime. An agency DS team rotates across radically different clients: a fintech under tight regulatory constraint, a CPG brand with seasonal campaign surges, a B2B SaaS in a portfolio acquisition, a media client with editorial workflow demands. The practitioner needs a *cross-engagement view* of the field that no in-house practitioner develops.

**Headcount budget vs. SOW budget.** An in-house DS team is funded as a cost centre with a permanent headcount. The headcount can flex slowly; it doesn't flex for the next quarter's roadmap. An agency DS team is funded by SOWs against client engagements, with hours as the unit of accounting. A senior practitioner can be 60% allocated to one engagement, 30% to another, and 10% on practice-internal work — and the allocation can shift mid-quarter as engagements close out or new ones open. The lead's scheduling-and-staffing surface is far more dynamic than an in-house lead's, and a meaningful fraction of the lead's time goes to the staffing problem itself.

**Authority over the consumer vs. authority over the contract.** An in-house DS team has standing relationships with the product teams that consume the system. The conversation is "we're shipping; can you adjust your work to land?" — and the consumer has the same employer. An agency DS team's "consumers" are the client's product teams, whose loyalty is to the client's commercial outcomes, not to the agency. The agency DS team's authority is not employer-derived; it is *contractual* (the SOW says they own the system) and *coalitional* (executive sponsors at the client back them). When the contract or the coalition wavers, agency DS teams lose authority faster than in-house teams.

**The "exit" problem.** An in-house DS team has no exit problem — the team is the team, indefinitely. An agency DS team has an exit problem at the centre of every engagement. The system has to outlast the agency. The team has to leave behind a *capable client team*, not just a maintainable artefact. This is the agency-DS practitioner's hardest problem, and it is the problem the in-house literature has nothing useful to say about.

### What the agency context demands

Given the structural differences, the agency-DS practitioner has to do things in-house practitioners don't. The demands compound across an engagement and across a career.

**Stand up the practice from cold inside three weeks.** Most agency engagements have a Discovery phase of one to four weeks. By the end, the practitioner is expected to deliver an audit, a maturity diagnostic, a Six Signs framing (or equivalent), an initial commercial pitch, an executive-stakeholder map, and a draft engagement architecture. None of this is a fresh problem to think through — the practitioner has done it before, in different industries, against different existing systems — but the pace requires *pattern recall*, not pattern invention. Senior agency practitioners maintain a private playbook; the playbook is the agency's method-IP, applied to each client's specifics.

**Leave a viable client team behind.** The handoff is the engagement's success metric. A handoff that produces a great system without a capable client team rots the system within a year. The practitioner's discipline is to plan the handoff from week one — identifying the client people who will inherit the system, designing the coaching arc that will up-skill them, building the executive coalition the client team will inherit, and timing the disengagement so the client team is operationally independent before the agency leaves. (See section 4 for the full treatment.) An in-house practitioner never does this work because there is no handoff.

**Translate practice IP across radically different contexts.** A senior agency practitioner has, over their career, run engagements for clients whose constraints have nothing in common with each other. A fintech's regulatory constraints (KYC, BSA/AML, GDPR, FINRA, FedRAMP) shape every authentication, audit-trail, and accessibility decision. A CPG brand's seasonal-campaign rhythm shapes how the system handles brand variation and how often it ships marketing-surface tokens. A B2B SaaS in private-equity portfolio context has explicit financial pressure on engineering velocity, which shapes governance and contribution. A media client's editorial workflow requires CMS integration depth most product DS teams never face. The practitioner has to translate the practice's *method* across these contexts without imposing a one-size-fits-all approach. The translation skill is what compounds; the artefacts don't.

**Carry the practice across engagements.** Each engagement is a context in which the practice's method gets tested, refined, and sometimes shifted. The senior practitioner who has run ten engagements has a richer method than one who has run three. The agency's compounding asset is the *senior practitioner population*, not the case studies. Hiring and retaining senior people is the practice's central commercial decision. (See sections 2 and 6.)

**Sustain the work across a multi-decade career under conditions that wear faster than in-house work.** Each engagement is a fresh stand-up, with all the cold-start cost that implies. Ten engagements over a decade is ten times "stand up the practice from cold," which is more wearing than one engagement that runs for a decade. (See section 8.)

The in-house product literature — Spotify, Atlassian, Shopify, Airbnb, IBM, Adobe, Microsoft, Google — is useful as field reference for the discipline's mechanics. It does not address the agency stand-up cost, the handoff problem, the cross-engagement translation skill, or the cold-start fatigue. The agency-side practitioner has to do those parts of the work without the literature's guidance.

---

## 2. Hiring and skill mix — building the agency-side DS team

### DS designer vs. product designer

The portfolio of a DS designer reads differently from the portfolio of a strong product designer. A senior product designer typically presents shipped surfaces — a redesigned checkout, a new onboarding flow, a refreshed dashboard. The work is end-state and consumer-facing. A DS designer's portfolio presents *systems* — a token architecture with its rationale, a component API and its invariants, a contribution model that survived adoption pressure, a Figma library architecture that didn't degrade after six months. The work is intermediate (it's consumed by other designers and engineers, not by end users) and architectural (its quality is judged by what it makes possible, not by what it shipped).

The literacy differences that matter, in priority order:

- **Token systems.** Reads tokens as a graph, not as a list. Understands primitive / semantic / component tiers, alias resolution, the platform-output boundary, theming as orthogonal axes (mode, density, brand, motion, contrast preference), the difference between a multi-collection model and a multi-mode model, and the conditions under which Generative Tokens make sense at portfolio scale. Has hands-on with at least one of Style Dictionary, Tokens Studio, or a similar pipeline; has authored token transforms.
- **Component anatomy.** Reads components as APIs. Distinguishes prop axes from variants, knows when a component should be polymorphic vs. when it should split, recognises composition primitives (Slot, AsChild, render-prop) as architectural decisions, sees the component documentation surface as part of the design.
- **Theming architecture.** Has shipped a system with at least two themes (mode is the typical one; brand is the next). Reads theming as a foundation problem, not a component problem. Knows where theming breaks (hard-coded values in components, alias collapse during build, missing per-script overrides for type, contrast inversion in dark mode).
- **Accessibility patterns at the system level.** Knows ARIA roles for composite widgets (combobox, listbox, menu, tablist, tree, grid), focus-management patterns (roving tabindex, focus-trap-on-modal, skip-to-content), the user-preference media-query surface, and the four-engine × four-AT test matrix as a working concept. Has shipped components that pass real AT testing, not just automated checks.
- **Governance.** Has been in a contribution-model setup, ideally as a maintainer. Knows the failure modes (every-team-contributes-everything; nothing-is-rejected; the-system-team-rejects-everything). Has views on the hub-and-spoke vs. federated trade-off. Reads the contribution model as a designed protocol, not as a hand-wave.
- **Motion as foundation.** Has tokenised at least a duration scale and an easing set. Knows the prefers-reduced-motion contract. Has views on the cross-platform spring-parameter mapping. The motion surface is the most-recent foundation tier to mature; designers who have shipped motion as a foundation are signal.
- **Colour science to a useful depth.** Reads colour in OkLCh, knows the WCAG vs. APCA distinction, has views on dark-mode lift patterns, knows the gamut-mapping situation. Doesn't need to be a colour scientist; does need to be literate enough not to mis-design contrast.
- **Type at system scale.** Reads typography as a token problem (composite typography tokens, modular scale, line-height as a multiplier, optical-size axis, font-loading discipline). Distinguishes typographic identity (the system's brand voice in type) from typographic UI (the workhorse text faces). Has views on the display + text + mono triad.

The mindset differences are subtler and harder to detect in interviews. A DS designer thinks at one remove from the surface — the question "what does this component need to be" becomes "what does the consumer need this component to be, what variants will they reach for, what extensions will they request, what failure modes will surface in the next year." A product designer can be trained to think this way; a DS designer has internalised the lens. The trained-vs-internalised distinction matters because the role's daily decisions are too frequent for the lens to be invoked deliberately each time.

A useful interview question: "Tell me about a component decision you made that was right at the time and wrong six months later. What changed, and what would you do differently?" Senior DS designers have multiple stories. Mid-level designers have one or two. Product designers without DS background often have zero — they haven't had their decisions tested against six months of consumer pressure.

The portfolio signal that matters most: **evidence of a system that survived its first year.** Pretty UI in a portfolio is not a DS signal. A system whose token architecture didn't break under a rebrand, whose contribution model survived a leadership change, whose components survived adoption by teams the system designer never met — these are signals. Few candidates can show this; the ones who can are the ones who have done DS work, not adjacent work that touched DS surfaces.

### The design technologist as a specific archetype

The design technologist (also titled design engineer, UI engineer, prototype engineer; the field has not converged on a single name as of mid-2026) is the highest-leverage hire on a DS team and the hardest to find. The role's composition is high design literacy + high engineering literacy + the *bridging instinct* — the disposition to translate between the two crafts in real time, in both directions, without losing fidelity in either.

The practical surface of the role:

- Builds prototypes that are production-shape — code that could be promoted, not throwaway click-throughs.
- Translates designs into framework-specific component APIs and back, fluently. The translation includes the parts that don't survive design naively (responsive behaviour, focus management, motion under load, edge-case data, AT navigation).
- Authors and maintains the system's component documentation infrastructure (Storybook setup, Code Connect mappings, MDX-or-equivalent authoring, the docs platform's custom components).
- Owns the boundary work between design-tool source and code source — Figma Variables to design tokens, Code Connect mappings, the schema layer if the system has one, MCP server endpoints if the system ships one.
- Often the team's "show, don't tell" voice — produces working examples that resolve debates faster than meetings could.

Where design technologists come from: almost never from CS programs or design programs. The cohort is self-taught hybrids — a designer who learned to ship code in production, an engineer who developed serious design literacy through years of UI work, an indie maker who built tools and got noticed, a person who started on the engineering side and rotated through design. The recognised individuals in the field — Una Kravets at Google, Adam Argyle at Google (formerly), Jhey Tompkins at GitHub, Sam Cox in his independent work, Pasquale D'Silva in product roles, Roman Komarov in CSS-platform work, Bramus van Damme at Google — are individuals more than archetypes. Each has a recognisable craft signature; none is interchangeable with the others.

Signals that matter when hiring:

- **A public artefact.** A blog, a CodePen catalogue, a GitHub presence, a conference talk, a Twitter thread that became a reference. The cohort writes and demos.
- **A built-or-maintained system.** Not just used — built. Token pipeline, component library, build infrastructure, tooling. The portfolio surface is "I made this work end-to-end," not "I touched this layer."
- **Engineering credibility on the system surface.** Can debug a CI failure in the system's pipeline; can read the design tool's plugin API; can architect an MCP server; can speak about variable-font byte economics or the colour-space pipeline at depth.
- **Design credibility on the system surface.** Can run a component design crit; can take a flat comp and reason about the prop matrix it implies; can author a Figma library that other designers don't break.
- **Bridging artefacts.** Tools they've built that translate between layers (a Figma plugin, a Storybook addon, a Code Connect template, a token sync utility). These artefacts are the bridging instinct made visible.

The role's compensation reality: design technologists at the senior level command compensation comparable to staff engineers, because the supply is small and the leverage is real. Agency budgets often struggle to fund this. The agency-DS lead's discipline: hire one design technologist, then one more if the engagement-portfolio justifies it; don't try to run a multi-person DS team without one. The dilution of trying to spread the bridging work across designers and engineers who don't have the role costs more than the design-technologist headcount does.

### What the DS lead actually owns

The DS lead is not a senior designer or a senior engineer. The lead is the practice's *commercial-and-craft hybrid*, and the role is misunderstood when it is treated as the senior-IC version of either contributing discipline.

What the lead spends time on across a typical week (rough breakdown for a senior agency lead with two active engagements):

- **Engagement scoping and pitching (15–25%).** Reading the next pitch, structuring the engagement architecture, sizing the team, drafting the pricing, writing the SOW with sales support, presenting to the client's executives. The lead is the agency's senior face on DS work; sales doesn't substitute. This time investment is invisible in the engagement budget but funds the next engagement.
- **Team coaching and 1:1s (15–20%).** Weekly or fortnightly 1:1s with team members, in-the-flow coaching during reviews and crit, mid-quarter career conversations, mentoring junior practitioners across engagements. The compounding asset of the practice is the team's seniority growth; the lead's coaching is the principal mechanism.
- **Governance decisions on contested work (10–15%).** Decisions that the team can't resolve internally — a contested API, a deprecation timeline, a dispute with a product team about contribution scope, a regression that touches the executive surface. The lead is the escalation point.
- **Executive coalition-building at the client (10–15%).** Standing relationships with the client's executive sponsors. Quarterly reads, pre-quarterly briefings, the occasional crisis call. This is the relationship surface the client team will inherit at handoff; the lead can't delegate it without weakening it.
- **Hiring (5–15%).** Always-on; spikes during ramp-up. Sourcing through the practitioner network, screening, leading interviews, debriefing.
- **External POV and practice IP (5–10%).** Conference talks, blog posts, white papers, internal practice training. The compounding intellectual asset of the practice is the lead's externally-visible thinking.
- **Occasional deep dive (5–10%).** A genuinely hard architectural call where the lead has to sit with the problem for a week. Many leads under-budget this and lose their craft edge over time.

What the lead's deliverables are: engagement architecture documents, team allocation plans, governance frameworks, the practice's POV documents, executive readouts. None of these are visual deliverables; the lead's craft has shifted to a higher altitude of artefact.

The reporting question: where does the DS lead sit in the agency's organisation? Three patterns work, none cleanly:

- **Reporting through design.** The most common pattern. Works when design leadership at the agency understands DS as a peer discipline rather than a sub-specialty of design. Fails when DS gets treated as "senior product design" and the lead's commercial-and-engineering surface doesn't get supported.
- **Reporting through engineering.** Works at agencies where engineering leadership has DS literacy. Fails at agencies where DS gets treated as "senior front-end engineering" and the design and governance surfaces atrophy.
- **Reporting through a cross-discipline practice or capability office.** The healthiest pattern when the agency has the structure for it. The DS practice is a peer to design, engineering, and strategy practices; the lead reports through the practice-leadership layer. Most large agencies converge here over time; smaller agencies often don't have the structural surface.

The lead almost never reports cleanly through a single contributing discipline because the role's surface is genuinely cross-disciplinary. Agency leadership that hires a DS lead and then treats them as a senior designer or senior engineer typically loses them within 18 months.

### The T-shape expected of a DS engineer

A DS engineer's T-shape has a deeper vertical and a wider horizontal than a product engineer's. The vertical: deep on a primary framework (typically the web stack — React, the modern build pipeline, TypeScript, the testing surface, accessibility implementation; or one of the major mobile platforms — SwiftUI, Compose, Flutter, React Native). The horizontal: enough literacy across the cross-platform surface to make architecture decisions about cross-platform tokens, native-platform translation patterns, and the cross-platform contract for components shipped from a single design source.

The system-specific tooling layer is itself substantial:

- **Storybook.** At least at the depth of authoring stories, configuring custom decorators, writing addons, and integrating with the system's testing pipeline. Storybook is the field's standard component-development surface; an engineer who hasn't shipped Storybook config and stories is at a real disadvantage.
- **Style Dictionary or equivalent.** Has authored transforms, has shipped multi-platform output, knows the DTCG specification at working depth.
- **Tokens Studio (or Figma Variables-to-Style-Dictionary tooling).** Has worked the design-tool-to-code seam. Knows where Figma Variables falls short of full DTCG composite types and what work-arounds the field uses.
- **The build and CI surface.** Visual-regression testing (Chromatic, Percy, Playwright, or equivalent), automated accessibility testing (axe-core, Pa11y), the package-publish pipeline, semantic-versioning automation, the changelog generator. The system's CI isn't a side concern; it's the system's quality gate.
- **The docs platform.** Storybook with Docs blocks, or Zeroheight, or Backlight, or a custom Next.js / Astro / Docusaurus docs site. The engineer needs to be able to extend it.
- **The AI / MCP layer.** As of mid-2026, this is increasingly common. Has thought about how the system exposes itself to AI clients (component metadata as structured data, MCP server endpoints, components-as-data architecture). The senior engineer has an opinion.

The engineer's literacy on design tooling matters more than is often recognised:

- **Figma at depth.** Can read a Figma file critically, knows Variables, knows Dev Mode and Code Connect, can author or maintain plugin-based tooling.
- **The design-to-code seam.** Knows where the seam breaks (composite typography tokens, theming dimensions Figma doesn't model, motion that doesn't survive Figma's prototyping, AT semantics that aren't expressible in the design tool).

What the practice should look for in a portfolio:

- **Library and tooling work, not application work.** A portfolio that shows shipped product features is product-engineering signal. A portfolio that shows a published component library, a token pipeline, a CLI tool, a Storybook addon, a Figma plugin, an MCP server is DS-engineering signal.
- **Open-source contribution at the system layer.** PRs to Style Dictionary, Storybook, the W3C DTCG repo, Radix, Material's codebases, Carbon's codebases. Strong signal of literacy and engagement with the field.
- **Cross-platform thinking.** Even if the candidate's depth is web-only, evidence that they've thought about how the work translates to mobile, native, or other targets.

### The supporting roles, and when each is justified

The agency-side DS team's supporting-role economics are different from in-house. In-house teams justify dedicated roles by long-term cost amortisation; agency teams justify them per engagement and have to size carefully.

**Design ops.** A coordination-and-process role typically justified once the practice as a whole reaches 8–10 people across active engagements. The dedicated design-ops practitioner owns calendars, retros, async-comms tooling, the engagement-onboarding process, the cross-engagement learning surface. Below the threshold, the lead owns these directly (and that's appropriate). Hiring design ops too early creates a coordinator without a coordination problem; too late creates a lead who is full-time on coordination instead of craft.

**Technical writer or UX copywriter.** The practice's commercial model names a 75-hour minimum scope; in practice this scope is rarely justified at engagements under three months. The role's value is real (system documentation voice, component usage guidance, error and empty-state copy patterns, content guidelines) but the role is typically the first cut when budget pressure surfaces. The pattern that works: a fractional technical writer attached to the practice rather than to specific engagements, time-boxed onto each engagement when the documentation surface justifies it. Below the threshold, the DS designer carries the writing.

**Accessibility specialist.** Rarely a full-time role at agency scale. The pattern that works: every senior DS practitioner is expected to have working accessibility literacy (WCAG 2.2, ARIA 1.3, the AT testing matrix, the focus-management patterns); one or two practitioners on the team have deeper depth (have done a11y audits as a billed deliverable, have shipped components against real AT testing, have read the EAA and Section 508 conformance regimes at depth). When an engagement has heavy accessibility demands (regulated industry, government, education), the practice can stand up an a11y specialist for the engagement; otherwise the deeper-depth practitioners cover the surface.

**Product manager for the system.** Rare in agency engagements. The DS lead carries the PM function — roadmapping, prioritisation, stakeholder management, release planning. In-house DS teams increasingly hire a dedicated PM (Atlassian, GitHub Primer, IBM Carbon, Adobe Spectrum all have DSPM roles); the agency commercial reality rarely supports a dedicated PM as a billable role. When it does, the lead's calendar opens up considerably and the practice's pace increases noticeably.

**Front-end / mobile platform specialists.** Justified when the engagement's surface area genuinely exceeds the team's coverage. A heavy iOS engagement justifies an iOS specialist; a Flutter engagement justifies a Flutter specialist. The pattern that fails: trying to deliver all platforms with web-only specialists. The engagement's quality drops on the under-staffed platform; the system's cross-platform credibility erodes.

The general shape: a small core team with deep generalists (DS lead, senior DS designer, senior DS engineer, design technologist), augmented with specialists as the engagement's surface demands. The core team can stand up an engagement; the specialists deepen the work. Trying to build a team primarily of specialists fails the engagement-pace requirement; trying to build a team primarily of generalists fails the engagement-depth requirement. The mix is the discipline.

---

## 3. The Part Timer → Allocated Individual → Dedicated Team arc

Nathan Curtis named the stages in *Team Models for Scaling a Design System* (EightShapes, 2017, with subsequent revisions). The agency-side practitioner has to make stage-transition calls without a clear playbook; the in-house literature describes the *destination* shapes (Solitary, Centralized, Federated, Cyclical) rather than the *transitions*. This section names the stages, the signals that mark a transition, the characteristic problems at each stage, and the patterns that work.

### Stage 0 — No DS practitioner

The pre-state. The engagement (or the client) has no dedicated DS practitioner. Symptoms visible from outside:

- Design debt visible in shipped product. Components reinvented per feature; spacing values hard-coded across views; type scales inconsistent across surfaces.
- Designers building "components" that don't ship. Figma libraries that exist but aren't consumed. Style guides that are PDFs no one has opened in six months.
- Engineering reinventing primitives per feature. Buttons re-implemented per screen with subtle differences. Form fields that don't share validation logic.
- A "design system" channel in Slack with no maintainer. Or a "ds-questions" channel where questions go unanswered.
- A request from the client for "a design system" without a clear definition of what that means or why now.

The intervention pattern: a Discovery engagement (typically one to four weeks) led by a senior DS practitioner. The deliverables: a Six Signs framing (or equivalent — what would qualify the work as a system rather than a UI kit), a maturity diagnostic (where the client is on the curve), an audit (token, component, accessibility, content as appropriate), a stakeholder map, and an initial commercial pitch shaped to the maturity. Discovery's purpose is partly to qualify the engagement (some clients are not ready for DS work) and partly to shape it (the engagement's commercial structure depends on what Discovery surfaces). Discovery is itself a billable engagement; the practice that runs Discovery for free trains clients to expect the front of an engagement to be unpaid.

### Stage 1 — Part Timer

A single DS practitioner working part-time inside the engagement, typically 20–40% allocation. The other 60–80% is on a different engagement, on a practice-internal initiative, or on bench time the agency is funding through utilisation slack.

What the part-timer can do:

- Author the initial token foundation (5–8 weeks of focused work for a fresh start).
- Stand up a starter component library (typically 8–15 components in 8–12 weeks, depending on platform and complexity).
- Run early governance — ad-hoc requests come in, the part-timer triages and answers as time permits.
- Establish the seed of the documentation site.
- Hold the executive-stakeholder relationships at the client.

What the part-timer cannot do:

- Sustain governance velocity past initial ramp. Requests pile up; SLAs slip; the system becomes a bottleneck.
- Run a contribution model. Other-team contributions need review and merge time the part-timer doesn't have.
- Cover multi-platform delivery. Web is plausible; web + mobile is not.
- Cover multi-brand work. The cognitive load of brand-switching is real.
- Coach a client team. Coaching is a sustained-attention activity.

The trap: a part-timer treated as a full-time DS lead. The engagement's expectations grow beyond the allocation; the part-timer over-extends; quality declines; the engagement starts reading the practice as failing. The lead's discipline: enforce the allocation explicitly, and pitch the escalation to allocated when the demand-vs-allocation gap is visible (typically within 8–12 weeks of stage start).

The escalation signals:

- **Ticket queue growing faster than draining.** The leading indicator. Two-week SLA on routine requests slipping to four, then six.
- **Governance decisions piling up.** Decisions that should take a day or two are taking weeks.
- **The part-timer's other engagement consuming the time.** The other engagement's pressure shifts; the DS work loses time first because it's not the primary commitment.
- **Client requests beyond the part-timer's hours.** "Can you also do mobile?" "Can you also lead the audit?" "Can you join the executive review?" — each request reasonable on its own; together exceeding the allocation.
- **Burnout signals from the part-timer.** The leading-indicator individual signal — declining responsiveness, declining work quality, declining engagement in retros.

### Stage 2 — Allocated Individual

A single DS practitioner working full-time (or near-full-time) on the engagement. The dominant agency stage; most engagements live here for months or longer. The allocated individual typically covers the Six Signs full set: foundations (tokens, theming, typography), components (the starter library and ongoing contribution), governance (the de-facto DS lead for the client), dev support (CI quality gates, the build pipeline, integration support for product teams), documentation (the docs site and component-level guidance), and the executive-stakeholder surface.

What the allocated individual can cover well:

- A single-platform engagement (web-only, or a single mobile platform).
- A single-brand system (no multi-brand theming demands beyond mode and density).
- A small-to-medium-sized product surface (one to three product teams consuming the system).
- Foundational work and a starter component library (40–80 components over six to twelve months).
- Initial governance, including light contribution work.
- The full documentation site at "good enough" quality.

What the allocated individual cannot cover:

- Sustained two-platform delivery. Web + mobile is too much for one practitioner past the initial three months.
- Enterprise-scale governance. Past four product teams the contribution velocity exceeds individual capacity.
- Multi-brand work. Each additional brand multiplies the foundations work and the component variation surface.
- A client team that is actively learning. Coaching is sustained-attention work that competes with the allocated individual's delivery work.

The risks at this stage:

- **The individual becomes the system.** Every decision routes through them; every architecture choice is in their head. The system fails to outlast them. When they're sick, on leave, or on vacation, the engagement stalls.
- **The system fails to outlast them.** The bus-factor problem. A senior allocated individual will die or quit or rotate eventually; if the system has been built around their tacit knowledge, the system rots.
- **Burnout.** The role's load is real. A single practitioner serving multiple product teams as their de facto DS lead, plus running governance, plus owning the docs surface, plus holding the executive coalition, is doing the work of two or three people. Some practitioners run this for years; many don't.
- **The "we'll just keep going" trap.** The engagement keeps growing in scope without the staffing growing. The lead has to push back proactively against the client's tendency to add scope to a competent practitioner without adding budget.

The escalation signals to dedicated team:

- **Multi-brand demand.** The client adds a second brand or sub-brand. The architectural surface doubles.
- **Multi-platform demand.** The client wants mobile in addition to web, or wants Flutter in addition to web + native iOS/Android.
- **Enterprise governance demand.** The contribution surface exceeds individual capacity. Multiple product teams contributing weekly; the review queue not draining.
- **Retention risk on the allocated individual.** The individual signals fatigue; the practice can either lose them or escalate to a team that distributes the load.
- **Client team starting to participate.** When the client begins forming its own DS function, the engagement's coaching surface opens up and a single practitioner can't cover both delivery and coaching.

### Stage 3 — Dedicated Team

A small team — typically three to six people — working sustained on the engagement. The shape that produces Curtis-1:2-ratio-supportable systems at meaningful surface area. The typical mix:

- **DS lead (1).** Owns engagement architecture, executive coalition, governance escalation, team coaching, hiring within the engagement.
- **Senior DS designer (1).** Owns design-side foundations, component library design direction, the design-tool surface.
- **DS engineers (1–2).** Own the build pipeline, CI, the implementation of the component library, integration support.
- **Design technologist (0–1).** When justified, the bridging role between the designers and engineers. Higher-leverage at this stage than at allocated-individual.
- **Specialist scope as needed.** Design ops if 8+ people on the broader practice; technical writer if the docs surface demands it; accessibility specialist for short engagements with regulated demands.

What changes at this stage:

- **The practice is no longer person-bound.** Decisions are made through the team, not through one head. The team can absorb individual departures (with cost, but not catastrophe).
- **The system can outlast the engagement.** The client team, if it's been forming in parallel, can take over from a multi-person team more credibly than from a single individual.
- **Governance becomes a team practice.** Contribution review is shared; SLAs hold under load; the system's pace doesn't depend on one person's calendar.
- **Coaching capacity opens up.** With multiple people, coaching the client team becomes feasible without sacrificing delivery velocity.

The new risks:

- **Coordination overhead.** Three to six people coordinating around shared work is itself an overhead. Sync meetings, review queues, the cross-functional surface — none of these are free. The lead's time on coordination grows.
- **Team-internal disagreements becoming engagement risk.** When two senior practitioners disagree about an architectural decision, the disagreement can leak to the client and undermine the team's authority. The lead has to manage these disagreements visibly without dampening healthy crit.
- **The lead becoming a manager instead of a craftsperson.** At three or four direct reports, the lead's calendar fills with management work. Senior leads who haven't structured for this lose their craft edge.
- **The "everyone is busy" failure mode.** The team's work doubles in scope as it gains capacity; sometimes capacity grows faster than scope, leaving the team with idle time and the lead scrambling for billable work to keep utilisation up.

### Stage 4 — Embedded Multi-Team

Past three product teams or beyond a certain organisational scale, the practice pattern shifts again. Embedded DS practitioners attach to specific product teams (one designer + one engineer per high-value product team, typically); a coordinating central group owns the foundations and the cross-team governance; the contribution model becomes federated. This is the Curtis Federated model in operational terms.

The agency variant: a core DS practice team plus per-product-team embeds. The agency staffs the central team; the embeds may be agency or client. The pattern is rare in agency engagements — most engagements don't reach this scale. When they do, the practice's role is typically to *stand the federated model up* and *hand it off* to client leadership, not to operate it indefinitely. Operating a federated model at agency scale is uneconomical (the per-team embed billing doesn't pay back fast enough; the client's product teams are usually the right consumers, so they should staff the embeds).

When this stage applies:

- Enterprise client engagements past 200–500 people in product organisations. The system has to serve more product teams than a central group can.
- Multi-product portfolios where central governance can't keep up with the per-product velocity.
- Multi-brand or multi-business-unit organisations where each unit has its own DS variant.

The agency's discipline: identify when the engagement is approaching this scale, plan the transition, work with client leadership to staff the embeds, and shift the agency's role from operator to coach.

### Stage transition signals and the failure mode

The general signals practitioners watch for:

- **Velocity divergence.** Demand for DS work growing faster than the team's delivery velocity. This is the fundamental signal; everything else is a consequence.
- **Lead time growth.** Time-from-request-to-delivery slipping. A two-week SLA becoming a six-week SLA is a stage-transition signal.
- **Staffing tension.** The team or the lead expressing real concern about workload, retention, or quality slipping under pressure.
- **Client appetite.** The client's willingness to fund the next stage. The lead's commercial discipline: surface the appetite and shape the next SOW before the current one strains.

The failure mode that's worth naming explicitly: **stages get added when work scales, but the people don't grow with them.** A part-timer becomes "the allocated individual" without being given the upgrade in seniority and authority the role demands. The allocated individual becomes "the lead of the dedicated team" without ever doing the lead's training. The transitions in title don't correspond to the transitions in work, and the engagement breaks at the seams.

The practice's leverage: anticipate the next stage and pitch it before the current stage breaks. The senior lead should be able to forecast the stage transitions for an active engagement six to twelve months ahead, with named conditions (these things have to happen; if they do, escalate; if they don't, hold). The forecast becomes part of the quarterly executive readout at the client; the escalation is then a planned commercial moment, not a crisis.

---

## 4. The agency-to-client team handoff — the practice's constant problem

The handoff is the agency-DS practitioner's hardest single problem, and the in-house DS literature is structurally silent on it because in-house teams don't have one. The agency ramps up a DS team, runs the engagement, ships a maintainable system, and is supposed to leave a maintainable team behind. The "leaves a maintainable team behind" half is where engagements most commonly fail. The system reverts to drift within a year of agency departure because the client has the artefact but not the discipline.

This section treats the handoff as a four-component activity (client team identity, discipline transfer, artefact transfer, relationship transfer), names the financial shape of a successful handoff, and lists the failure modes the practice has lived through.

### What the handoff actually consists of

#### The client team's identity

Who, by name and role, is the client's DS team going to be? The handoff begins with this question. If the engagement reaches month nine without an answer, the engagement is heading for a failure-mode handoff.

The pattern that works:

- **Client-team-formation begins in week one.** The Discovery engagement's deliverables include a recommendation for the client's DS team shape. The recommendation names roles (DS lead, DS designer, DS engineer at minimum) and the staffing question (existing-internal-talent, internal-promotion, external-hire). The lead engages with the client's HR and design/engineering leadership to shape the staffing plan.
- **Staffing happens in the engagement's first quarter.** Existing internal talent gets identified and rotated into DS work; external hires get sourced. The agency may help with the hiring (interview support, referrals through the practitioner network); the staffing decision sits with the client.
- **The client team works alongside the agency team from the start.** Not "the client team gets briefed at the end" — the client team is a peer working group from quarter one. Shadowing, paired contribution, shared retros, joint design crit, joint code review.
- **The client lead is named early and supported visibly.** The agency lead introduces the client lead to the executive coalition by month three or four; the client lead carries an increasing share of the executive surface from there.

The pattern that fails: the agency staffs the engagement, runs it for six to nine months, then looks up and realises the client has not staffed up because the agency was doing the work. The handoff date arrives and the system has nowhere to go. The agency's reflexive fix — compress the handoff into the last six weeks — almost always fails. Six weeks is not enough time to onboard a client team into the discipline of a system the agency has been building for nine months.

The client team's identity has to be a *deliverable* of the engagement, not an artefact the agency hopes will materialise.

#### The discipline transfer

The system itself is one set of artefacts; the *discipline of operating the system* is a different set of competencies. The discipline transfer is what most fails to happen, and it's what the "client has the artefact but not the discipline" failure mode is about.

The competencies that have to transfer:

- **Tokens-as-architecture thinking.** The client team has to internalise the alias graph, the resolution boundaries, the platform-output discipline. They have to be able to make token-architecture decisions without the agency in the room.
- **Components-as-contract thinking.** The client team has to read components as APIs and reason about props, variants, behavioural contracts, and the consumer's perspective. They have to feel the pressure not to ship a "feature complete" component that breaks composition rules a year later.
- **Governance as practice.** The client team has to run the contribution model — triage, review, decide, communicate — under load, without the agency lead's escalation safety net.
- **The failure modes the agency has lived through.** The client team has to *know what doesn't work*, ideally without having to discover each failure independently. The senior agency practitioner has a private catalogue of these (the "we tried this once and the system rotted" anti-patterns); transferring the catalogue is part of the coaching.

Coaching is not training. The distinction matters. Training transfers facts and procedures: "here is how the build pipeline works." Coaching transfers judgement: "here is how I reason about whether to deprecate this component now or in the next major." Training is necessary but insufficient; coaching is what produces a client team that can operate the system, not just maintain it.

The pattern that works, in stages:

- **Shadowing first.** The client team observes — present in design crits, present in code reviews, present in governance escalations, present in executive readouts. They don't drive; they listen and ask. Typical duration: two to three months from client-team-staffing.
- **Paired contribution second.** The client team contributes alongside the agency team. A client designer and an agency designer co-design a component; a client engineer and an agency engineer co-implement. The agency partner reviews; the client partner is on the byline. Typical duration: three to six months.
- **Client-led contribution third with agency review.** The client team owns a component or a foundation deliverable end-to-end; the agency reviews before the merge. Typical duration: three to six months. By the end of this stage, the client team has shipped enough of the system to feel ownership.
- **Independence with agency consultation as a retainer.** The agency leaves; the retainer relationship continues. The client team owns the system day-to-day; the agency consults on architectural questions, governance escalations, and the next major release.

The whole arc takes 12–18 months from client-team-staffing to agency-departure, in a healthy engagement. Agencies that try to compress it to six or nine months almost universally produce handoffs that drift.

#### The artefact transfer

The system itself, the documentation, the build pipeline, the governance bodies, the contribution process, the comms channels. Already covered in 04, 05, 07 in the practice's existing material; here only insofar as it interacts with the team transfer.

What matters for handoff:

- **The artefacts are the client's from day one.** Not "the agency owns and licenses." The client owns. The agency's IP is the *method*, not any client's *instance*. (See section 4.2 below.)
- **The artefacts have to be operable by the client team without agency presence.** The Storybook config that only the agency engineer knows how to debug is a handoff failure waiting to happen. The Figma library that depends on an agency designer's plugin setup is a failure mode. The build pipeline that has tribal-knowledge dependencies is a failure mode.
- **The documentation has to teach, not just describe.** A docs site that explains *what* the components do is descriptive. A docs site that explains *how to think about* extending them, *when to* deprecate them, *why* the API is shaped the way it is — that's the docs site that supports a client team operating the system.

#### The relationship transfer

The agency team has spent months building executive coalition at the client; the client DS team has to inherit that coalition, not rebuild it.

The pattern that works:

- **Joint executive presentations through the engagement.** The agency lead presents alongside the client lead from month three or four. The agency lead introduces the client lead as the long-term owner. By month nine or ten, the client lead is the primary presenter; the agency lead is supporting.
- **Explicit coalition-passing in the last quarter.** The agency lead has individual conversations with each executive sponsor to introduce them to the client lead as the new primary relationship. These are real conversations, not email introductions. They include the executive's perspective on the system's progress, on the client lead's standing, and on what continued sponsorship looks like.
- **Named executive sponsors paired with client leads.** Each executive at the client has a named primary contact in the client DS team. The pairing survives the agency's departure.

The pattern that fails: the agency lead holds the executive relationships unilaterally, then "introduces" the client lead in the last month. The executive sponsorship is performative thereafter; the client lead doesn't have the standing the agency lead built.

### The financial shape of a successful handoff

A successful handoff is a *transition from project revenue to retainer revenue*, not a commercial loss. The retainer pays for:

- **Governance review.** Quarterly architectural reviews of the client's DS work; the agency lead reads the work and consults on direction.
- **Escalation consultation.** When the client team hits an architectural or governance call they can't resolve, they have an agency lead to consult. Hourly billing or retained hours; either works.
- **Major-release support.** When the client plans a major version of the system, the agency comes back for a defined engagement to support the architectural lift.
- **Adjacent engagement scoping.** When the client expands the system's surface (new platform, new brand, new product), the agency is the natural first call for the expansion engagement.

The retainer compounds across years if the client team thrives. A successful handoff produces a long-term relationship that pays the agency more in aggregate, over a five-to-ten-year horizon, than continuing the project work would have. The agency that recognises this dynamic structures its engagement model around the handoff being a feature, not a bug.

The agency that doesn't recognise this dynamic treats the handoff as revenue loss and resists it. The result is the failure modes named below.

### The failure modes

Three failure modes show up repeatedly in agency-DS handoffs.

#### "We'll just stay another quarter"

The client team isn't ready. The agency stays. The agency's incentive (continued engagement revenue) and the client's incentive (continued comfort with the system being someone else's problem) both work against the handoff. Senior practitioners have to push back against both their own commercial instinct and the client's request.

The pattern that prevents it:

- The handoff timeline is committed to in the SOW from engagement start. The end-date is a *deliverable*, not a soft target.
- The lead's quarterly readouts to the executive sponsors include progress on client-team readiness. When readiness slips, the readout names it; the executive sponsorship can correct the staffing or the timeline can extend, but the slip is visible.
- The agency lead has the discipline to refuse the extension when the client's request is "stay another quarter so we don't have to staff up." The right answer is: "No. We'll help you staff up, but we're going to leave on the timeline."

The senior lead's commercial discipline matters more here than at any other moment. The lead who agrees to one extension finds themselves agreeing to four; the engagement extends indefinitely; the client team never forms; and when the agency finally leaves (three years later than planned), the system has no operator and rots faster than it would have at the original handoff date.

#### "Agency owns the artefacts, client owns the operations"

A bizarre but real failure mode where the agency treats the system as IP and refuses to fully transfer it. Sometimes this comes from the agency's commercial team trying to lock in long-term licensing; sometimes from the agency's legal team mis-applying IP-protection patterns to client work; sometimes from the senior lead not understanding that the client owns the work the client paid for.

The practice's discipline: **the client owns the system from day one.** The agency's IP is the practice's *method*, not any client's instance. The method is what compounds across engagements; the instance is the client's. This has to be stated in the SOW; it has to be modelled in the engagement; it has to be reinforced when commercial pressure pushes the other way.

The agency that operates this discipline has stronger long-term commercial outcomes (retainers across many clients) than the agency that tries to lock in artefact-licensing on individual clients (which produces resentment, then attrition, then replacement by a competitor).

#### "No client team"

The client never staffed up because the agency was doing the work. The handoff date arrives and the system has nowhere to go; the engagement extends on emergency staffing, drifts, or the system rots.

The agency's discipline: client-team formation is a *deliverable* of the engagement. The lack of client staffing is a deliverable blocker. The lead names this in the executive readout. The client either staffs up or the engagement renegotiates the scope and timeline; "we'll just keep going" is not an option.

In practice, the agencies that don't enforce this discipline find themselves running engagements where the client never staffs up and the agency is operating the client's DS function indefinitely as a quasi-outsourcer. The pattern can be commercially profitable in the short term and is almost always a strategic loss. The agency's reputation suffers (clients in the network notice that the agency's "design systems" engagements don't end and the systems don't survive the agency's eventual departure); the agency's senior practitioners burn out (they're stuck on the same engagement for years); the agency's competitive position erodes (the next client's RFP includes "we want you to leave us with a capable team," and the agency that can demonstrate this wins).

---

## 5. Internal team rituals — the daily and weekly cadence of a working DS team

DS-internal rituals are distinct from external governance comms. External comms is *how the system communicates with consumers*: release notes, contribution-process documentation, the docs site, the broadcast Slack channel, the executive readout. Internal rituals are *how the team coordinates internally to do the work*: standups, design crit, code review, retros, architecture office hours.

The agency-DS team's internal cadence has to work across timezones (often), across two contributing disciplines (design and engineering, plus design technology if the team has it), and across the engagement's lifecycle (ramp-up, steady-state, handoff). The patterns below are what works at agency scale; in-house teams converge on similar shapes but with different time-of-day and meeting-density choices.

### The daily pattern

**Asynchronous standups via Slack thread.** First thing in the day, each team member posts: what I did yesterday, what I'm doing today, blockers. The thread is timezone-friendly (each person posts at the start of their working day) and artefact-leaving (you can scroll back a week and see the team's velocity). The pattern that fails: synchronous standups across mismatched timezones, where the meeting time is nobody's preferred working hour and the meeting becomes a status performance.

**Live design review or live engineering review, twice a week.** Thirty minutes each. The team workshops in-progress work together — not for status, for craft. A designer brings a component variation problem; the team reads the work, asks questions, surfaces the failure modes the designer hasn't yet seen. An engineer brings an API design; the team reasons about the prop matrix and the future-state implications. The discipline: this is *crit*, not status. The lead's job is to model the crit voice (rigorous, kind, specific) and make sure junior practitioners feel safe contributing.

**The lead's open office hours, twice a week.** One to two hours per session. The lead is available for ad-hoc questions from anyone in the broader practice (the engagement team, other engagement teams, design and engineering colleagues at the agency who want DS perspective on something). The office hours are blocking time on the lead's calendar — the team knows the slots; non-team members can drop in. The lead's discipline is to keep the time un-overbooked; the surface area exists for relationships and unscheduled help, and over-scheduling collapses the value.

**Weekly system sync with client design and engineering leads.** Thirty to forty-five minutes. Agenda-light, blocker-and-decision-led. The agency lead and the client design lead and the client engineering lead align on the week's priorities, surface blockers, and take any decisions that need joint resolution. The meeting's discipline: it is *not* a status meeting (status is in writing); it is a decision-and-blocker forum. When the meeting becomes a status meeting, it has lost its purpose.

### The weekly pattern

**The team retro.** Sixty to ninety minutes, weekly or fortnightly. The only meeting with no client present. The place where craft conversations happen without performance pressure — what's wearing the team down, what's working, what's getting in the way. The retro's discipline: the lead does not dominate. The retro is for the team's voice; the lead's job is to listen and follow up.

The retro shape that works at agency scale: ten minutes for "what worked this week," ten minutes for "what didn't work," ten minutes for "what we'd change," twenty to forty minutes for whatever surfaced, ten minutes for action items. Async retros (a Slack thread or a Notion page) work as a complement but not as a replacement; the synchronous time matters because some conversations only happen face-to-face (or video-to-video).

**The component review, weekly.** Where contributed work — both team-internal and from the client team or product teams — is critiqued before it lands in the system. The review is the system's quality gate; the discipline of running it well is part of the team's craft. The agency-side pattern: component review is open to client practitioners and to product-team consumers. The transparency builds the contribution culture; the secret review fails the contribution model.

**The roadmap session.** Where the next four to six weeks of work are sequenced with the client. The agency lead and the client product owner (or PM equivalent) align on what's coming, in what order, with what trade-offs. The session is decision-oriented: leaving without decisions made is a failure mode.

**Architecture office hours.** The lead's longer-form thinking time, often co-working with one or two practitioners on a hard architectural call. Two to three hours, weekly. The discipline: this time is for the work that doesn't fit in an hour-long meeting — the redesign of the token primitive layer, the multi-brand contribution model, the migration plan to the next major release.

### The monthly pattern

**The system release cycle.** Typically every two weeks at agency engagements; major release every four to six weeks. The release cadence is a ritual itself — release notes generated and reviewed, the changelog published, the broadcast channel updated, the docs site refreshed. Release weeks have a predictable rhythm that the team can plan around.

**The exec readout.** Where the executive coalition gets its refreshed view of progress and risk. Thirty to forty-five minutes, monthly or quarterly depending on the engagement. The format that works: metrics-led (adoption, contribution velocity, system health), narrative-led (what we shipped, what we're working on, what we're worried about), and strategic-led (where we'll be in three months, what decisions need exec input). The discipline: don't bury risk. The execs would rather hear about the contributing-team-resistance problem in month four than discover it in month nine.

**The "external POV" session.** Where the team writes or refreshes practice-IP — case studies, blog posts, conference talk drafts, white papers. The discipline: the external POV is a team output, not a lead-only output. Senior practitioners speak and write; mid-level practitioners co-author; junior practitioners observe and learn. The compounding asset of the practice is the externally-visible thinking; the team that doesn't produce it doesn't compound.

### Documentation as a ritual, not a phase

The discipline that distinguishes mature DS teams from immature ones: documentation is written *during* contribution, not *after*. A component contribution that doesn't include its docs is incomplete. An ADR (architecture decision record) is written for every load-bearing architectural decision *as the decision is made*, not retrospectively. Release notes are generated from PR metadata, not hand-authored.

The pattern that fails: documentation as a separate phase at the end of the engagement. The team accumulates a documentation debt; the debt grows faster than the team can pay it down; the docs site reaches a partial-coverage stable state where some components are documented well and others are barely listed; the consumer experience degrades.

The pattern that works: documentation acceptance as part of the merge gate. The PR template includes a docs checklist (component docs page complete; usage examples included; a11y notes complete; design tokens used documented; failure modes named). The PR doesn't merge without the checklist. The lead's discipline is to enforce this even when the engagement is under delivery pressure; the practitioner's discipline is to write the docs while the implementation is fresh, not to defer them.

The compounding effect: a year of disciplined doc-as-you-go produces a docs site that *teaches*. A year of deferred documentation produces a docs site that *describes the components that managed to get documented*.

### The "team voice" question

How the team writes — PR descriptions, Slack threads, ADRs, docs prose, release notes — is the team's *external face*. Senior teams develop a recognisable voice over time. The voice carries the team's craft; it's part of what makes the team's work feel like one team's work, not a collection of individual contributions.

Most agency teams have a tonal hole here that surfaces when the team scales. Three writers' voices on the same docs page is a system smell. The team's coaching surface should include voice — what's the tone of a docs page, what's the shape of an ADR, what's the structure of a release note. The lead's discipline is to coach toward voice without micromanaging; the senior practitioners' discipline is to model the voice in their own writing and to give voice-feedback in PR review.

The voice question is under-discussed in the DS-team literature. In-house teams develop voice as a function of long tenure together; agency teams have to develop it more deliberately because the tenure is shorter and the writers turn over more.

---

## 6. Career paths in DS — IC vs. lead, principal track, what comes next

The DS career path is not yet a settled question — the role is too young at agency scale to have a 20-year career arc in the way that, say, "senior front-end engineer" or "senior product designer" has. The dedicated DS practitioner cohort first formed in the mid-2010s (Atomic Design 2013, the InVision Design Systems Handbook 2017, the first wave of named in-house systems shipping 2014–2018); the agency-side dedicated practitioner cohort is younger still. Many of the career-path patterns are being invented in real time. This section names what the field knows in 2026 and what is still being figured out.

### DS designer career path

Junior DS designer → DS designer → senior DS designer → principal DS designer or DS lead.

**Junior DS designer.** Has product design experience and is rotating into system work for the first time. Spends the first six to twelve months learning the literacy (tokens, components, governance, accessibility patterns). The junior practitioner's deliverables are component-level — designs a component or two, contributes to documentation, participates in crit. The lead's job is to coach.

**DS designer.** Has shipped DS work and has the working literacy. Owns components end-to-end; participates in foundations work; can take an architectural component through design crit credibly. Two to four years in.

**Senior DS designer.** Owns foundations work (token tier design, theming architecture, motion-as-foundation if the system has it). Co-leads contribution governance. Mentors junior practitioners. Reads the engagement's design surface as a coherent whole. Four to seven years in.

**Branching point at senior.** Two tracks open up:

- **Principal IC track.** Deep craft, principal-level systems thinking, occasional consulting on other engagements, architectural-decision authority. The principal designer is the team's design-architectural authority — when a hard architectural decision arrives, the principal is consulted. The role is hands-on; the principal still designs.
- **Lead track.** Engagement architecture, team leadership, commercial responsibility, less hands-on design. The lead's deliverables are at engagement and team altitude (see section 2 on what the lead actually owns).

The two tracks pay similarly at senior+. The field has not yet articulated the principal IC track for DS designers as cleanly as engineering has — there is no consensus title, no consensus level matrix, no consensus expectation set. The result: senior DS designers who don't want to manage often find themselves drifting into lead roles by default, and burning out within two or three years because they're doing work they don't want to do. The agency that supports a real principal IC track retains senior designers; the agency that doesn't loses them.

### DS engineer career path

Junior DS engineer → DS engineer → senior DS engineer → principal DS engineer or staff DS engineer.

**Junior DS engineer.** Has front-end (or mobile-platform) experience and is rotating into system work. Learns the system's pipeline, the testing infrastructure, the docs platform. Ships components against existing architecture. Six to twelve months.

**DS engineer.** Has the working literacy. Ships components, contributes to the build pipeline, participates in API design discussions. Two to four years in.

**Senior DS engineer.** Owns the build and CI pipeline, contributes to API architecture, mentors junior engineers, runs code review with authority. Four to seven years in.

**Principal or staff DS engineer.** The IC engineering track is more developed than the design equivalent. The field has clearer signals:

- The engineer who owns the build pipeline at engagement-architectural depth.
- The engineer who designs the API architecture for the component library.
- The engineer who operates as the team's architectural authority on hard implementation calls.
- The engineer who builds the system's tooling (CLI, Storybook addons, MCP server, schema-validation framework).
- The engineer who is read by other engineers in the practice as the one to consult on hard problems.

The principal/staff DS engineer track maps reasonably onto general front-end staff-engineer tracks, with the system-specific specialisation. Compensation is competitive with general staff-engineer roles, sometimes premium given the supply scarcity.

### Design technologist career path

Less clear. The role is typically titled differently per organisation (design engineer, UI engineer, design technologist, prototype engineer, design technologist, design engineer); the senior track is often invented per-person rather than described as a path.

The recognised individuals at the high end — Una Kravets, Adam Argyle, Jhey Tompkins, Sam Cox, Pasquale D'Silva, Roman Komarov, Bramus van Damme, Sara Soueidan in her independent work — are individuals more than archetypes. Each has built a recognisable craft signature; the senior career emerges from the individual work, not from a pre-defined ladder.

The pattern that's emerging in 2024–2026:

- **Mid-level design technologist.** Has the bridging instinct and shipped both design and code work. Two to four years in. Often titled inconsistently; "design engineer" is the most common in 2026.
- **Senior design technologist.** Has shipped a system or major tool that demonstrates the craft. Recognised within their organisation as the bridge person.
- **Principal design technologist.** Recognised externally — has a public artefact (writing, talks, open-source work) and is consulted across organisations. The cohort is small.

The compensation question: design technologists at the senior level command compensation comparable to staff engineers, because the supply is small and the leverage is real. Agencies often struggle to fund this; the agency that does fund it retains the role's holder, who then becomes a force multiplier across engagements.

### DS lead career path

What's beyond DS lead?

- **Practice lead.** Manages multiple DS leads in a global practice. The role is structural at large agencies (VML, R/GA, Frog, EPAM, Thoughtworks, Capgemini Invent's design practices) and rare at smaller firms. The work shifts from engagement architecture to practice strategy.
- **Director or VP of DS at the agency level.** Above practice lead. The role spans the agency's overall DS posture — pitch leadership across regions, hiring strategy, the practice's competitive positioning. Few agencies have this role explicitly; it tends to be carried by the most senior practitioner.
- **CTO-adjacent or CDO-adjacent roles** where DS is one input among many. Rare but documented — senior DS leads moving into broader technology or design leadership roles where the systems lens applies across the organisation's craft.
- **Founding or co-founding a DS-focused agency or product.** Several recognised independents (Rangle.io's DS practice, Sparkbox, Knapsack-the-product, Backlight-the-product, Specify) are former agency-DS leads who left to build something more focused.
- **Returning to in-house leadership** as a head of design or VP of engineering with a systems lens. The senior DS lead's cross-engagement experience makes them a strong candidate for in-house leadership roles where breadth of context is valuable.

The pattern: senior DS practitioners are valuable in many roles. The lead-of-leads career inside any single agency is small and competitive. The career that compounds beyond a single agency is the one that produces externally-visible work — the writing, the conferences, the open-source contribution, the network of past clients and colleagues. The agency that supports this externally-visible work retains its senior leads; the agency that doesn't produces leads who eventually leave to build their visibility elsewhere.

### Where DS people go after DS

The field's outflow is real. Senior DS practitioners who have done the discipline for five to ten years often move on. Common destinations:

- **Product leadership at clients they've worked with.** A senior DS lead who ran the engagement well at a client is sometimes hired by that client into a head-of-design or head-of-engineering role. The cross-pollination is healthy for the field; the agency loses a senior practitioner but gains a long-term ally inside the client.
- **In-house DS leadership at product companies.** The natural transition. The senior agency lead becomes the in-house DS lead at a product company, often with a meaningful compensation increase. The agency's loss is the field's distribution — these practitioners shape in-house DS practices for the next phase of their careers.
- **Founding their own consultancies.** Smaller, more focused. The DS lead who has run engagements at scale knows what they want to do differently and starts a smaller practice. The cohort is large enough to be visible (Sparkbox, Knapsack the consultancy, the various individual-DS-consultant practices that show up at conferences).
- **Engineering or design-engineering roles** where systems thinking applies. Some senior DS practitioners move into broader tooling roles — developer-experience engineering, design-tools engineering, the AI-tooling layer. The systems lens transfers.
- **Teaching, speaking, writing as primary work.** Practitioners who have built the externally-visible voice often scale it down from agency engagement work toward teaching, conference speaking, writing. The cohort is small but recognised (Brad Frost is the most-named example; Dan Mall, Nathan Curtis, Stéphanie Walter, and others have varying degrees of this rebalancing).

The agency's discipline given the outflow: structure the role so people don't burn out and leave the field; structure the practice so senior people leaving doesn't crater operations. The field's compensating dynamic: agency alumni often come back as clients, partners, or referral sources. The agency that treats senior departures as relationship-end loses the network value; the agency that treats them as relationship-evolution gains it.

### The compensation question

Agency-side DS people are typically paid less than in-house DS people at high-paying tech companies, for the same reason agency designers and engineers are generally paid less: agency revenue per head is lower than top-tier product company revenue per head. The compensation gap can be material — a senior DS engineer at a top-tier in-house DS practice might earn 1.5x to 2.5x what the same engineer would at a global agency.

The compensating advantages, when honestly considered:

- **Variety.** Agency practitioners work across industries, platforms, and brands. The breadth is real; ten engagements across a decade is more variety than ten years inside one product organisation.
- **Breadth of practice.** Agency practitioners see more failure modes than in-house practitioners. The cross-engagement learning compounds into a senior practitioner whose context is wider than any in-house peer's.
- **The practice's intellectual rhythm.** The agency-DS calendar is meaningfully different from the in-house calendar. Engagement starts and ends produce natural reflection points; in-house calendars are continuous.
- **The ability to influence multiple companies' DS practices over a career.** A senior agency practitioner has visibly shaped five to ten organisations' systems by mid-career; an in-house peer has shaped one or two.

The retention pattern: pay competitively for the agency tier (not below market for the agency cohort, even if below the top in-house tier), invest visibly in growth (conference attendance budget, training, principal-track development, external speaking opportunities, sabbaticals), make the practice a place where senior people *want* to stay. The agency that invests in retention keeps the practitioners whose cross-engagement learning is the practice's compounding asset; the agency that doesn't invest finds itself constantly hiring at the senior level and losing the compounding to the field.

A specific compensation pattern worth naming: **senior practitioners' externally-visible work is itself compensation.** The conference talk paid for in agency time, the open-source contribution allowed during work hours, the blog post written under the agency's banner — these are part of the practitioner's portfolio and visible to the next employer. The agency that allows and encourages this work is paying in a currency that retains; the agency that locks it down is paying only in cash and is competing on cash with the top-tier in-house tier, which it will lose.

---

## 7. Distributed and global team patterns

The agency reality is global. VML and similar global agencies (R/GA, EPAM, Capgemini, Thoughtworks, Frog, Designit) staff DS engagements across timezones — US East and US West, EU West and EU Central, Latin America (especially Argentina, Brazil, Mexico), India (Bangalore, Pune, Hyderabad), Asia-Pacific (Singapore, Sydney, Tokyo). The team-building patterns that work are timezone-aware in ways the in-house literature mostly ignores.

### Two-timezone overlap as a minimum

A DS team needs at least a 2–4 hour daily overlap window between its core members for real-time coordination. Without it, the loop time on hard decisions stretches to days; the team's pace drops below what the engagement can sustain.

The pattern that fails: 12-hour-offset handoff teams with zero overlap. "We work US hours, they work India hours, we hand off at end of day" sounds like it works. In practice, the loop time on a contested decision is two days minimum (the US team raises it; the India team responds the next morning India time, which is the US team's evening; the US team responds the next morning US time, which is the India team's evening). Two days for one round-trip on a decision that should take an hour.

The pattern that works: paired timezones with a daily synchronous window for the team's hardest work.

- **US East + EU West.** Five-hour overlap (10am ET = 3pm UK = 4pm CET). Lots of room for real-time coordination.
- **EU + India.** Three to four-hour overlap (2pm CET = 6:30pm IST). Tighter but workable.
- **US West + LATAM.** Three to five-hour overlap depending on country (10am PT = 1pm Buenos Aires = 12pm São Paulo).
- **US East + LATAM.** Easier; same hemisphere.
- **The hard cases.** US West + India, US East + Asia-Pacific, EU + Asia-Pacific. Two-hour overlap windows exist but are at edge-of-day for both sides; the team has to be deliberate.

When the team spans more than two timezones, the pattern becomes "core hours" — a 2–3 hour daily window that everyone is expected to be available within, even if it's an inconvenient time of day for some. The discipline: rotate the inconvenience. If the US team always gets their preferred hours and the India team always works late, the India team's experience degrades; eventually the senior India practitioner leaves and the practice's distribution breaks.

### Asynchronous as the dominant mode

Most coordination happens in writing — Slack, GitHub, Jira, Linear, Notion, Figma comments, ADRs. The synchronous windows are reserved for work that genuinely needs synchrony:

- Contested decisions where the disagreement is faster to resolve face-to-face than in writing.
- Pair-debugging, where the back-and-forth is real-time-natural.
- Design crit on novel work, where the visual and spatial discussion benefits from real-time.
- Executive readouts, where the relationship surface requires presence.
- Retros, where psychological safety benefits from synchronous space.

Senior teams over-invest in asynchronous writing quality and under-invest in meetings; junior teams do the opposite. The senior team's PR descriptions are detailed enough that no follow-up meeting is needed. The senior team's ADRs are written enough that the decision survives the writer's eventual departure. The senior team's Slack threads end with explicit decisions, not with implicit conclusions.

The discipline that produces this: the lead models writing-quality. The lead's PR descriptions are detailed; the lead's Slack-thread responses are complete; the lead's ADRs teach. Senior practitioners follow the modelling; junior practitioners learn from it. The team's writing quality is a function of the lead's writing quality plus a function of how much the lead invests in coaching it.

### Documentation as the team's memory

The async-dominant pattern only works if decisions are captured, not just made. The team's memory has to live in the writing, not in the meeting attendees' heads.

- **ADRs for load-bearing decisions.** The decision, the alternatives considered, the trade-offs, the people in the room. A new team member can read the ADR catalogue and understand why the system is shaped the way it is.
- **RFCs for proposals.** Before a major change lands, an RFC proposes it. The RFC is reviewed asynchronously; the comments produce the discussion that an in-person meeting would have produced. The RFC plus its comments is the artefact; the meeting (if any) is supplementary.
- **Recorded retrospectives.** The retro produces an artefact (a Notion page, a Slack thread, a Linear cycle review). The artefact captures what was discussed and what was committed to. New team members can read the retro history and learn the team's culture.
- **Architecture notes.** Beyond the formal ADRs, the team writes down architectural reasoning — design principles, mental models, the team's tacit assumptions. The senior practitioner who eventually leaves takes their tacit knowledge with them unless the team writes it down; the team that writes it down survives senior departures.

The agency-side pattern that wins: a single source for the team's memory (Notion, Linear with rich descriptions, a Confluence-equivalent), with discipline about what goes there and what doesn't. The pattern that fails: a fragmented memory across Slack messages, Google Docs, Figma comments, email threads. The fragmentation is comfortable in the moment and lethal over time; new team members can't onboard, and senior practitioners' knowledge doesn't compound into the team's shared understanding.

### "Follow-the-sun" rarely works for DS

Follow-the-sun (work moves around the globe; one team finishes, the next picks up; 24/7 progress on the same work item) is occasionally proposed for DS engagements because it sounds like it should work and because operations functions in the same agency may already be running it.

It rarely works for DS work. The reason is structural: DS work is *mostly serial*. A component goes through:

- Design exploration.
- Design crit.
- API design.
- Engineering review.
- Implementation.
- Accessibility review.
- Documentation.
- Visual-regression review.
- Release.

The dependencies are real. The accessibility review can't happen before the implementation; the implementation can't happen before the API design; the API design can't happen before the design crit. Follow-the-sun assumes the work is parallelisable across timezones; DS work, mostly, isn't.

The pattern that emerged in agency practice: paired timezones with overlapping core hours, not full follow-the-sun. The team works a normal day in their primary timezone, with the overlap window for the synchronous coordination. The async work happens in the writing. The "the next team picks up where the last one left off" pattern, when it does work, works for *parallel* work — multiple components in progress simultaneously, with clear handoff at component boundaries — not for serial work on a single component.

### Cross-cultural patterns

A team spanning US, EU, India, LATAM has cultural differences in directness, hierarchy, conflict, time perception, meeting expectations, and craft norms. The senior practitioner's read: don't try to flatten the culture; do build in mechanisms that make all voices land.

Examples of mechanisms that work:

- **Written-first decisions.** The proposal is written before the meeting; the meeting reviews the proposal. Non-native English speakers and non-extroverts have time to compose. The decision is captured in writing as it's made.
- **Explicit invitations to opinion.** Some cultures require the senior to ask before the junior speaks. The lead's discipline is to ask explicitly: "X, what do you think?" rather than waiting for the junior to volunteer.
- **Retros that explicitly surface "what wasn't said in this meeting."** The retro asks: who didn't speak, what was held back, what feedback would be uncomfortable to give in real-time. The team's psychological safety improves when the surface for held-back feedback is named.
- **Working hours that respect timezone preferences.** Don't schedule the EU + India sync at 9pm IST; don't schedule the US East + EU sync at 6am ET. The lead's calendaring discipline is real work.
- **Recognising holiday calendars.** The Indian team's Diwali is not a casual day off; the LATAM team's Carnaval and Easter periods are real; the European August is real. The agency's calendar that ignores regional holidays signals which culture is the default; the calendar that respects them signals that the team is genuinely distributed.

A specific anti-pattern worth naming: **the "always-on senior" trap.** Senior practitioners working across global teams often default to extending their own day to cover every overlap — early morning calls with EU, late evening calls with India. The trap is sustainable for a quarter, not a year.

The discipline: a *senior in each timezone* doing the same role, with explicit rotation. The agency's compounding asset is having senior people in each region; an agency that has only one senior carries the senior into burnout.

The pattern in practice for global agencies: the practice has at least two senior practitioners per major timezone region. The senior in EU runs EU-led engagements; the senior in India runs India-led engagements (often serving Asia-Pacific clients); the senior in the US runs US-led engagements. Cross-region engagements have a senior on each side, with explicit hand-off. The structural redundancy is real cost; the alternative (one senior carrying global exposure) is real-cost-plus-burnout-plus-attrition.

---

## 8. Team health and the burnout patterns specific to DS work

DS work has burnout patterns that the broader design and engineering fields don't fully share. The patterns compound over time; senior practitioners who haven't named them often burn out without understanding why. This section names the patterns, the mitigations that work, the early-warning signals, and the hard call about when to disband.

### The "everyone's customer" load

A DS practitioner is the customer-facing role for every product team in the organisation. The ticket queue is constant. The prioritisation is contested every time — every product team thinks their request is the most urgent. The answer is "we'll get to that" far more than the practitioner wants. Saying no is a daily activity.

The role's emotional surface is wider than a product designer's or product engineer's. A product designer serves their product's users (or, more often, the product's stakeholders). A product engineer serves their product's surface. A DS practitioner serves *every product team*, every product designer, every product engineer, every executive sponsor, every consumer of the system. Senior DS practitioners often describe the role as being in customer-support mode for years.

The mitigation that works:

- **Triage discipline.** The team has a stated SLA for responses (24h for an acknowledgment; one to two weeks for routine work; defined escalation path for urgent). The discipline buys the team space; the lack of discipline produces a queue that never drains.
- **Saying no with structure.** "We can't do that this quarter; here's the queue; here's how it could be prioritised; here's what would have to change for it to land sooner." The structured no is sustainable; the unstructured no produces antagonism.
- **Visible governance.** The contribution model is documented; the prioritisation framework is documented; the team's capacity is communicated. The product teams may not like the answers, but they understand them.
- **Distributing the customer load across the team.** Not every conversation has to go through the lead. The senior team can rotate the "who answers the urgent Slack" responsibility; the lead is the escalation point, not the always-on responder.

### The "never finished" load

A DS practice is never done. There is always more to tokenise, more to document, more to automate, more to govern. The work is structurally incomplete; the practitioner who needs the satisfaction of closure burns out faster than the practitioner who is at peace with the discipline being a *craft*, not a *project*.

The product designer who ships a feature gets the satisfaction of the launch. The product engineer who ships a release gets the satisfaction of the release. The DS practitioner ships releases too, but the system itself never closes. Version 2.0 ships; version 2.1 follows; the foundations work that needed doing in 1.0 still needs doing; the components added in 2.0 will need refining in 3.0. The horizon is indefinite.

The mitigation that works:

- **Explicit milestones.** Within the indefinite horizon, the team carves out closeable milestones. The release of version 2.0; the completion of the multi-brand theming work; the rollout of the AI-readability layer. These milestones have endings the team can celebrate.
- **External POV outputs.** A conference talk is a closeable artefact. A blog post lands. A case study completes. The senior practitioner who feels the never-finished load at engagement scale gets the satisfaction of closure at the field-contribution scale.
- **Reframing the discipline as craft.** The senior practitioner learns to read the work as ongoing craft, like a chef reading their kitchen as ongoing craft, like a musician reading their instrument as ongoing practice. The reframing isn't trivial; the practitioner who can't reach it eventually leaves the field.

### The "invisible improvement" load

The DS team's biggest wins are usually invisible — a design system that *prevents* a redesign, *avoids* a regression, *short-circuits* a feature-flag rollout, *catches* an accessibility bug before it ships. The work product is often the absence of work; the recognition for absence-of-work is structurally lower than for visibly-shipped work.

The product designer who shipped the redesigned checkout gets the recognition for the checkout. The DS designer whose token system *prevented* a mid-project rebrand-induced redesign gets nothing visible — the rebrand happened and the system absorbed it, which looks from the outside like nothing happened.

Senior practitioners learn to advocate for themselves; junior practitioners often don't and feel under-valued. The pattern that works:

- **Metrics that surface invisible value.** Adoption metrics (how many product teams are using the system); contribution-velocity metrics (how fast contributions are landing); regression-prevention metrics (how many bugs the system caught before they shipped); accessibility metrics (how the system's accessibility coverage compares to the field). The metrics make invisible work visible.
- **Storytelling discipline.** The lead and the senior practitioners write up the wins explicitly. "We avoided a six-month redesign because the token system absorbed the rebrand"; "the contribution model meant that the new product team was productive on day one"; "the accessibility audit passed because the system's components passed it before the audit started." The stories accumulate into the practice's external POV.
- **Coaching practitioners on self-advocacy.** Junior practitioners often need explicit coaching to advocate for their work in performance reviews and in executive surfaces. The lead's job includes this coaching.

### The agency-specific load

The agency-side DS practitioner starts a new engagement every six to eighteen months. The relationship-building, executive-coalition-forming, audit, foundation-laying, governance-establishing work is *repeated* per engagement.

The compounding learning is real — the senior practitioner who has done ten engagements has a rich method that no in-house practitioner develops. The compounding fatigue is also real. Ten engagements over a decade is ten times "stand up the practice from cold," which is more exhausting than one engagement that runs for a decade. The cold-start cost is mostly social — re-establishing trust with new executive sponsors, learning a new client culture, re-litigating the case for DS work that the previous engagement had already resolved.

The mitigation that works:

- **Engagement spacing.** A senior practitioner doesn't run back-to-back engagements without breathing room. The agency that sequences engagements with two-to-four-week gaps between major engagements (filled with practice-internal work, training, or sabbatical) retains practitioners; the agency that runs them back-to-back-to-back loses them.
- **Practice-internal work between engagements.** White papers, conference talks, training, internal tooling, mentorship. The senior practitioner who has produced something visible to the field after each engagement experiences the engagement as part of a career arc, not as the same engagement repeated forever.
- **Explicit engagement variety.** The lead's staffing discipline includes variety — a senior who has just done a heavy regulated-industry engagement gets a CPG or media engagement next, not another regulated one. The variety keeps the work fresh.

### What works overall to mitigate

- **Sabbaticals.** Every 18–24 months, two to four weeks, paid, the agency commits to coverage. The sabbatical is not a vacation; it is a structural rest that interrupts the cumulative load. Agencies that ship sabbaticals as a benefit retain senior practitioners materially better than those that don't. The cost is real (two to four weeks of senior coverage by other practitioners); the alternative cost (senior attrition every two to three years) is much higher.
- **The structured IC-vs-lead choice.** The practice supports both tracks; the practitioner who doesn't want to manage doesn't have to. The IC who is forced into management burns out; the IC who is supported in IC craft retains.
- **The cross-engagement portfolio rhythm.** The practitioner doesn't always-on the same client; rotates across the practice's engagements with explicit transitions. The transition rhythm matters; constant exposure to one client erodes faster than rotation does.
- **The "external POV" ritual.** The team writes, speaks, contributes to the field. The work that compounds beyond the engagement and feels visibly *theirs*, not the client's. The senior practitioner whose only work is invisible client work eventually wonders what they have to show for the decade; the senior practitioner who has a portfolio of public artefacts has an answer.
- **The strong retro discipline.** What's wearing on the team is named, not endured. The retro that surfaces fatigue early gives the lead time to act; the retro that doesn't (or that the team doesn't have) leaves the lead discovering attrition only when someone resigns.

### The signals that a team is in trouble

Leading indicators, before resignations:

- **Pull-request throughput declining without scope changing.** The team is working as hard but shipping less. Energy is going somewhere — into rework, into unproductive disagreement, into avoidance.
- **Documentation quality declining.** A leading indicator of fatigue. People defer documentation when they're tired; the docs site is the canary.
- **Team-internal conflicts becoming personal.** Healthy crit is depersonalised; conflict that personalises is fatigue or unresolved structural problems leaking out.
- **The lead skipping retros to "save time."** The lead is the team's reflection surface; the lead who can't make time for retros is the lead who isn't doing the work that prevents burnout.
- **Senior people quietly looking elsewhere.** LinkedIn updates, conference talks at competitors, side projects that look like portfolio-building. The lead's network usually picks this up before the resignation lands.
- **Fewer informal interactions.** Lunch conversations stop; Slack-channel chatter declines; the team becomes purely transactional.

The practice's early-warning system:

- **Monthly 1:1s with the lead.** Not status meetings; relationship meetings. The practitioner can talk about anything, including dissatisfaction with the work.
- **Quarterly team-pulse surveys.** Anonymous, short, structured around the questions that matter (workload sustainability, growth opportunities, satisfaction with the work, intent to stay).
- **The agency's HR or people-ops surface feeding back to the lead.** Not as surveillance; as collaboration. HR sees patterns the lead doesn't see (compensation comparisons, exit-interview themes, cross-agency benchmarks).

### The hard call — when to disband

Some engagements should end. The client isn't ready for ongoing DS work; the budget has shifted; the strategic priority has moved; the engagement was the wrong fit from the beginning. The lead's discipline that prevents burnout: not staffing dying engagements with senior practitioners out of inertia.

Signals that an engagement should wind down:

- The executive coalition has dissolved. The original sponsor left; the new leadership doesn't see DS as a priority.
- The client team isn't forming and shows no sign of forming. The handoff trajectory is broken.
- The product teams aren't adopting. The system is shipping but no one is consuming it.
- The work has become purely maintenance with no architectural progress. The engagement has reached "we maintain a Figma library and a Storybook" and isn't going anywhere.
- The team is unhappy and the unhappiness is engagement-specific.

The lead's responsibility: read the engagement's health, recommend a wind-down before it becomes a death-march, protect the team's energy for the next engagement that deserves it. The wind-down is itself a piece of work — a defined exit, a documented system state, a graceful handoff (even if the client team isn't ready, the artefacts have to be left in operable shape), a final readout to the executive surface.

The pattern that fails: the lead avoids the hard call because the engagement is billable. The team continues; the energy degrades; senior practitioners leave; the practice's reputation at the client (and in the client's network) suffers; the wind-down eventually happens anyway, but in worse shape.

The senior lead who can read engagement health and call wind-downs proactively is the lead who builds a sustainable practice. The lead who can't is the lead whose practice burns through senior practitioners.

---

## References

The agency-side DS-team-as-discipline literature is sparse; most of the field's published material is in-house product literature. The references below are partitioned by what generalises to agency contexts and what doesn't.

### Primary field references — directly applicable

- **Nathan Curtis, *Team Models for Scaling a Design System* (EightShapes, 2017, with subsequent revisions).** The canonical naming of Solitary, Centralized, Federated, and Cyclical. The 1:2 ratio. The Part Timer → Allocated Individual → Dedicated Team arc. https://medium.com/eightshapes-llc/team-models-for-scaling-a-design-system-2cf9d03be6a0
- **Nathan Curtis, EightShapes' broader catalogue.** Decades of writing on contribution models, governance, role definitions, and team structure. Skews in-house but most translates. https://medium.com/@nathanacurtis
- **Brad Frost, *Atomic Design* (2013, with subsequent online updates).** The team chapter and the broader articulation of how systems get built and governed. Translates to agency contexts because Frost's own background is consulting; agency-applicable material runs throughout. https://atomicdesign.bradfrost.com/
- **Brad Frost's broader writing.** The blog, the *Frostapalooza* talks, the *DS Hours* sessions. Heavy agency-side experience visible. https://bradfrost.com/
- **Dan Mall, *Design That Scales* (2024) and earlier writing on embedded design teams.** The canonical agency-side perspective on DS team structure; Mall's background at SuperFriendly is directly agency. https://danmall.com/
- **InVision Design Systems Handbook (2017, online).** Slightly dated but foundational. Multiple authors including agency-side practitioners. https://www.designbetter.co/design-systems-handbook
- **Design Systems Podcast (Sparkbox / Knapsack hosts, ongoing).** Many episodes feature agency-DS leads; the back catalogue is substantial. https://thedesignsystem.guide/podcast / search the podcast archive
- **Design Systems Conference (Clarity, the leading dedicated conference).** Many talks address team and discipline questions. https://www.clarityconf.com/
- **Into Design Systems (newsletter and conference).** Active community surface; agency-DS practitioners speak regularly. https://www.intodesignsystems.com/
- **Sparkbox's writing on DS engagements.** Agency that has been running DS engagements since the early 2010s; case-study writing addresses the team and handoff questions directly. https://sparkbox.com/foundry
- **EPAM (formerly Pivotal Labs and various predecessors), Thoughtworks, Capgemini Invent.** Large consulting firms with DS practices; their published case studies and engineering blog posts surface team patterns when read carefully.

### Primary field references — useful but in-house product–shaped

The following are valuable for the DS-team mechanics but require translation for agency contexts:

- **Atlassian Design System team retros and writing.** Long-form public reflection. https://atlassian.design/
- **Shopify Polaris team writing.** Particularly the era after the team scaled past 30 people. https://polaris.shopify.com/
- **GitHub Primer team writing.** Primer's evolution is documented in multiple posts. https://primer.style/
- **IBM Carbon team writing and conference talks.** Adobe-scale practitioner pool. https://carbondesignsystem.com/
- **Adobe Spectrum team retros.** Particularly the cross-platform coordination stories. https://spectrum.adobe.com/
- **Material Design's evolution from M2 to M3.** The team scaling story is partly public. https://m3.material.io/
- **Microsoft Fluent's writing.** Rare but high-quality; the cross-OS team coordination stories are worth reading. https://fluent2.microsoft.design/

### Design technologist / design engineering

The role is distributed across many individual voices. These are the names worth following as of mid-2026:

- **Una Kravets (Google, web platform).** Writing and talks across CSS, design tooling, and DS infrastructure. https://una.im/
- **Adam Argyle (formerly Google, now independent / various).** CSS platform work that intersects with DS frequently. https://nerdy.dev/
- **Jhey Tompkins (GitHub, formerly various).** UI engineering at the design-engineering boundary. https://twitter.com/jh3yy
- **Sam Cox (independent).** Independent design engineer; widely read. Various platforms.
- **Pasquale D'Silva (independent / various product roles).** Motion and product design at the design-engineering boundary.
- **Roman Komarov (independent).** Deep CSS platform work. https://kizu.dev/
- **Bramus van Damme (Google).** CSS platform writing including DS-relevant features. https://www.bram.us/
- **Sara Soueidan (independent).** Front-end and accessibility writing at deep technical depth. https://www.sarasoueidan.com/

### Team and operations references (broader)

Outside DS specifically but applicable to the team-and-discipline questions:

- **Will Larson, *An Elegant Puzzle* (Stripe Press, 2019).** Engineering leadership at scale; many of the staffing-and-team-dynamics patterns translate. https://lethain.com/elegant-puzzle/
- **Camille Fournier, *The Manager's Path* (O'Reilly, 2017).** IC-vs-lead track decisions, principal-track structure. Engineering-flavoured but transferable.
- **The Engineering Manager Slack and adjacent communities.** Practitioner conversation that occasionally surfaces DS-relevant patterns.
- **The Design Leadership Forum and adjacent communities.** Senior-design-leader peer networks where agency-DS discussion happens.

### Agency-side practitioner blogs and writing

Sparser than the in-house equivalents but worth tracking:

- **Sparkbox's blog and case studies.** https://sparkbox.com/foundry
- **Knapsack's blog (the consultancy and the product).** https://www.knapsack.cloud/blog
- **Various individual agency-DS leads who blog or maintain Substack publications.** The cohort is small enough that following the field's conferences and the Design Systems Podcast catches most active voices.

### Verification notes

- All "as of mid-2026" claims about practitioner-population sizes, conference rosters, and named individuals should be re-checked against the current state of the field. The cohort changes; the named individuals move between roles; new conferences and communities form.
- Curtis's *Team Models for Scaling a Design System* is dated 2017; the model has held up well but the staffing-thresholds in the post (when to escalate from one stage to another) have shifted as the field has matured. Read with the current 2026 staffing reality (typically one practitioner per 8–12 product engineers consuming the system) in mind, not the 2017 numbers.
- The InVision Design Systems Handbook (2017) is still circulating but has not been substantially updated. Specific tooling references (Sketch as the design tool, etc.) are dated; the team and process material is mostly current.
- Specific compensation claims (in-house vs. agency tier; 1.5x to 2.5x ratio) reflect mid-2026 industry observation and vary materially by region. Verify against current compensation surveys (Levels.fyi, Glassdoor, the Design Salary Survey, the Design Tool Survey's compensation breakouts) before treating as load-bearing in client conversations.

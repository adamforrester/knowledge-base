---
type: practice-area
title: Governance and Adoption
description: Governance models, contribution flow, adoption mechanics. The phase that decides whether the system survives the engagement.
tags: [phase, governance, adoption, contribution]
timestamp: 2026-06-10
---

# 07 — Governance & Adoption

> The phase that decides whether the system survives the engagement. Governance is the operating model that keeps the system trustworthy as it grows; adoption is the work of moving the system from "available" to "default." Both are the responsibility of the practice — not artifacts to hand off.

---

## What this phase is, and why it matters

By the time a system reaches this phase, the technical architecture is largely set. What's not set is **who decides what changes**, **how contributions enter the system**, **how consumers stay current**, and **how the team that owns the system relates to the teams that use it**. These are organizational design decisions, not technical decisions, and they determine whether the system compounds or decays after the consultancy walks away.

Across every external source from Frost (2016) through Curtis (2023) through Anderson (2024), the consensus is clear: *adoption is the hardest part*. Internal practice docs echo this verbatim: *"Getting people to use the design system is often cited as the hardest part."* (DS-Scoping, 2026.) But the practice's commercial scoping spends the majority of engagement budget on Discovery → Foundations → Components, with Governance and Adoption sized as a sliver at the end (Thrive 2024 — "Run" phase) or absent entirely (CareCentrix 2026 — engagement ends at handoff). This is the most consequential commercial mismatch in the practice's current model.

The 2024+ reframe makes this gap even more acute. If a design system is **infrastructure** (Anderson, Nov 2024), then governance is operations and adoption is the SLA — non-negotiable, ongoing, funded. The "system as product" framing has produced a generation of well-built, under-adopted systems. Governance for the infrastructure era requires versioning, contracts, observability, and an explicit operating model — none of which fit cleanly into a 4-week phase at the end of a 16-week engagement.

## What actually happens in this phase

Six clusters of work, mostly continuous through the system's life.

### 1. Choosing the governance model

Three (or four) named approaches, with strong cross-source consensus on the trade-offs:

| Model | Definition | Strengths | Blind spots |
|---|---|---|---|
| **Solitary** | One person maintains the system. | Coherent vision; fast decisions. | No bandwidth; no continuity if person leaves. Stage 1 only. |
| **Centralized (Core)** | A funded, dedicated team builds and maintains the system. | Clear ownership and accountability; consistent quality. | Can disconnect from product reality; bottlenecks contributions. |
| **Federated** | Distributed contributors across product teams co-decide. | Fast contribution; strong product-context awareness. | Inconsistency; chaos without a backbone. Curtis: "Pure federation is chaos." |
| **Cyclical / Hybrid** | Centralized core + structured federated contribution. | Combines centralized backbone with product-context contribution. | Hard to operate; requires explicit contribution criteria. Most teams reach this; few start here. |

Curtis's decision rule, and the field's emerging consensus: **Solitary → Central → Federated, in stages.** "Start with core group to setup tools and form ways-of-working. Then gradually grow to engage a community." (Curtis, *Operating Design Systems*, Sep 2023.) Pure federation is a *destination*, not a starting point.

The internal practice's stance: **centralized is preferred, with explicit contribution channels.** This aligns with the field. The deck is honest about centralized blind spots (lack of day-to-day product context, low product-designer participation, no influence on product tradeoffs) — which is the right framing, *as long as the contribution model is paired with the recommendation.*

### 2. Team structure and capacity

Curtis's near-internal-tier guidance is the sharpest in the field. Adopt:

- **Designer-to-developer ratio: 1:2** ("Mine is 1:2.")
- **50% capacity floor** for designers and devs assigned to the system. Below that, the work doesn't compound.
- **Specialists negotiable** — content strategy, accessibility, performance, SEO can be partial.
- **Three lead roles** (Client lead / Design lead / Tech lead) plus PM as minimum.
- **Minimum maker pairs:** 1 UX + 1 UI designer paired; 1 lead + 1 production developer paired; 1 QA; 1 PM; ideally 1 content strategist.
- **Stages of getting to a core team:** Part Timers → Allocated Individuals → Dedicated Team. Most clients are stuck at Allocated Individuals; the engagement should prepare the org to fund a Dedicated Team. (See 00e §The Part Timer → Allocated Individual → Dedicated Team arc, which operationalises each stage's risks, escalation signals, and the Stage 4 federated variant for the rare large-scale engagement.)

The internal practice's commercial model in CareCentrix 2026:
- Project Lead (Design Director, 25%)
- Design Systems Lead (50%)
- UX Designer (100%)
- UI Designer (100%)
- Delivery Lead (PM, 50%)
- UX Copywriter (75 hours)
- Accessibility Specialist (10 hours)

This is a 5-person production core plus 2 specialists. Scaled appropriately for a 12–24 week engagement; less clear how it converts to the client's ongoing 3–8 person team after handoff.

Curtis's library tier model is a useful overlay on team structure for multi-brand or multi-platform clients:

- **Core foundation** (tokens) — DS team owns.
- **Core library** (cross-team UI components) — DS team owns.
- **Shared libraries** (BU/platform/feature kits) — contributors maintain with DS team help.
- **Team library** — team-identified maintainers.
- **Team project file** — single team members, not a library.

### 3. Communities of practice

Three named groups, complementary:

- **Steering Committee** — directors, VPs. Makes resourcing and direction decisions. Meets quarterly or semi-annually.
- **Extended Design Group** (Ambassadors / Champions / Guild / Critique) — designers from product teams, embedded in their teams, liaising with the core. Sprout Social's pattern; Couldwell's recommended posture. Adopted by Etsy, GOV.UK, others.
- **Extended Developer Group** — front-end engineers from product teams, same role.

Couldwell on Ambassadors selection: *"We seek out people who are not only passionate about design systems but also those who are systems thinkers, willing to stand up for good design and advocate for best practices."* (Sprout Social via Ben Lister.)

The Ambassadors program is one of the most under-utilized governance patterns in agency-led engagements. The practice currently does not productize it. It would close a real gap — most clients lose adoption momentum within 6 months because there's no embedded liaison structure.

### 4. Contribution model

Curtis's contribution framework is the most operational in the field. Practice should adopt verbatim:

**Contribution definition** (precise): "Design, code, or documentation of a fix, enhancement, or new feature by someone NOT on the core team made available for others to use." Tangible / Useful / Federated / Released. *Contributions ≠ Participation* — reviewing PRs, attending meetings, asking questions are participation, not contribution.

**Contribution scale:**
- Fix
- Small Enhancement
- Large Enhancement
- New Feature
- Catalog Wide
- New Catalog

The largest two ("Catalog Wide," "New Catalog") are **driven by the system team, not the contributor.** This is a critical clarification — federation has limits.

**Contribution criteria** (eight named):
- **Shared Need** — 1–5 scale; 1 means "keep it local," 4–5 means "let's get started."
- **Timing** — 3 months for full release; 6 weeks system-spec'd / locally-built; 2 weeks for build-yourself with consultation.
- **Responsibility** — who does which step.
- **Availability** — 1 week "let's go"; 1 month "set milestones"; 3 months "discuss commitments"; 1 year "discuss another time."
- **Capability** — does the contributor have the skill?
- **Direction** — consistent with how the system is growing?
- **Cost** — relative to shared impact.
- **Relative Value** — vs. other current work.

**Contributor onboarding (six-step):**
1. Start with a conversation, not a form.
2. Prep with what they need to know, not more.
3. Provide templates and outline with them.
4. Refer to most-similar existing examples.
5. Listen for what they believe they can do.
6. Build cadence, check in, avoid stalls.

Multi-Brand Governance (Apr 2025) extends this with a process layer:

**9-step intake:** Initial inquiry → Communication channel → Assessment and guidance → Qualification review (cross-brand reusability, alignment, feasibility, scalability) → Prototyping → Review and approval → Prioritization → Formal development and testing → Documentation and release.

**10-step component testing:** Content (lengthy / i18n) → Accessibility → Cross-browser/device → Responsive → Functionality unit tests → Stress test (common, edge, stress) → Internal code review → Internal design review → Application trial → QA.

**7-step contribution workflow:** Proposal → Design/dev specs → Peer review → Cross-brand testing → Documentation → Final approval → Distribution & announcement.

These together are the most complete contribution operating model published. The practice should ship them as default — they translate immediately into client-team operating instructions.

**Governance weight should track blast radius at the token layer specifically.** A primitive token change cascades to every brand and every consuming codebase; a semantic change cascades to every component in one brand; a component-token change cascades to one component. The right RACI by token tier (central team owns primitives; brand lead owns semantics; product team owns component tokens) makes friction proportional to consequence. **Primitive changes pass through a Cascade Report in CI** that lists every brand and component affected; semantic and component changes pass through lighter review. See 24-tokens-at-scale for the full operational layer.

### 5. Adoption tactics

A list, not a recipe — the right combination depends on org size and culture:

- **Practice Pilot** (rehearse internally before going live) — see `06-pilot-and-implementation.md`.
- **Shared-vocabulary glossary** — Mall's Activity #25.
- **Joining pilot sprint planning** — DS-side designer/eng embedded in pilot team meetings.
- **First stakeholder update** at end of Discovery, with synthesis report.
- **Design System Coverage Map** with statuses (Live / In Use / In Progress / In Planning) — one of the practice's strongest internal artifacts; visible evidence of reach.
- **Recurring Office Hours** — semi-monthly default. Curtis: "Slack + Office Hours ≠ communications plan" — necessary but not sufficient.
- **Slack release announcements** — `#system-design`, `#system-dev`, `#system-[ambassadors]` channels.
- **Onboarding integration** — HTML/CSS for designers, Figma for engineers, Git for designers, Storybook for designers. (Adoption is literacy.)
- **Sprint demo cadence** — every 2 weeks. Curtis: audience grows from 8–15 to 40–80 over time; demos can become the system's social fabric.
- **Quarterly training events** + semi-annual planning + release events with rolling "release coming / new feature spotlight / deep dive" cadence.
- **Roadshow** — go to consuming teams, present, answer questions.
- **Praise patterns** — @ mentions in Slack (multiple times), doc-page byline, email release announcement, release history line item, demo to large groups, "expert" promotion.
- **"Systems Week"** — periodically dedicate one week of every three to internal-only work (breaking changes, global functionality, renames). Internal practice's named cadence.
- **Cross-disciplinary onboarding** — teach Figma to engineers, Git to designers. (Internal scoping doc.)

### 6. Communication structure

Curtis names this explicitly as a major-release initiative track. Operationalize:

- **Core team Slack** (private) — `#system-core`.
- **Public design Slack** — `#system-design` for releases + design help.
- **Public dev Slack** — `#system-dev` for releases + tech help.
- **Ambassador Slack** — `#system-ambassadors` for the embedded group.
- **Special-topic channels** — `#system-ux-patterns`, `#system-tokens`, etc., as the system grows.
- **Sprint demo every 2 weeks** — open invitation, recorded, posted.
- **Release events** with rolling "Major release is coming / New feature spotlight / Deep Dive" cadence.
- **Quarterly training events.**
- **Semi-annual planning** (with surveys + interviews + must/should/could/shouldn't matrix scoring + workshop validation).
- **Org-wide updates** monthly or quarterly.
- **Weekly stakeholder update** to executive sponsors using Mall's three-section template (*What We Did / Where We're Headed / How You Can Help*).

### 7. The leadership-incentives reframe (2025+)

Figma's *Design Leaders* ebook (Apr 2025) adds a leadership-level reframe the practice should absorb:

> "The teams struggling for greater alignment — that's usually a structural problem based on the incentives that go all the way up to the top." — Hugo Raymond, Figma

Misalignment between designers and developers — and between the system and consuming teams — is a *structural incentives* problem, not a tooling problem. The leadership-level conversation: are design debt, technical debt, and product debt weighted equally in the org? If not, governance friction is a symptom of misweighted debts.

Practical implications for the practice:

- **Survey stats as exec openers.** "80% of developers think their business would benefit from working more closely with designers" / "92% of designers and 91% of developers say there's room for improvement in handoff."
- **GitHub's "shift left" doctrine** — engineers enter design discussions during ideation, not at handoff.
- **Joint dev+design "Ready for Dev" approval** as a governance gate.
- **Linear's leadership stance** — *"We push direct responsibility onto the team, giving them the freedom to make decisions, while setting a standard for them to meet."* — leadership sets the bar, not the tactics.
- **ServiceNow's reframe:** *"Maybe we have to reframe handoff as no longer being a handoff. We are working together until this thing gets to a level of completeness and quality that we feel it's ready to ship."*

## Our POV

The internal practice has a richer Governance & Adoption POV than the commercial proposals reflect. The VML library covers governance models, contribution workflows, communication strategy, and measurement. CareCentrix 2026 commercial scope ends at handoff with no Governance phase priced. Thrive 2024 has a "Run" phase covering Adoption & Integration / Support / Communication / Feedback / Contribution but doesn't price it.

**Practice-distinctive POVs in this phase:**

- **Centralized-with-contribution model** as the default recommendation, with explicit awareness of centralized blind spots.
- **Coverage Map** with Live / In Use / In Progress / In Planning statuses — visible evidence of reach.
- **Systems Week** cadence — 1 week internal work per 3 weeks pilot work.
- **SemVer (MAJOR.MINOR.PATCH)** for library and individual components.
- **Cross-disciplinary onboarding** as adoption fuel (HTML/CSS for designers, Figma for engineers, Git for designers).
- **3–8 person team at 20–30 hrs/week** as the post-handoff target team.
- **Multi-brand governance models** named (centralized / federated / distributed) with awareness of contextual fit.

**Gaps in our current commercial Governance & Adoption standard, honestly named:**

- **Governance & Adoption is not commercially priced post-handoff.** This is the single biggest structural gap. The practice ships the system; the client runs it. The first 6 months of "running it" is where most systems decay. We should sell a Run-phase retainer, support tier, or governance subscription.
- **Curtis's contribution criteria and scale are not in commercial deliverables.** The 8-factor criteria, the 6-step onboarding, the contribution-vs-participation distinction, the contribution scale (Fix → New Catalog) — all available IP but not yet packaged.
- **The Ambassadors program is not productized.** Couldwell's Guardians/Ambassadors/Lead pattern; Sprout Social's program; GOV.UK's working group. The practice could ship a "design your Ambassadors program" workshop as part of every engagement.
- **Library tiers are not in our scoping conversation.** Curtis's Core foundation / Core library / Shared / Team library / Team project file structure is the right answer for any multi-team client. We should articulate it during scoping.
- **Communication architecture is implicit.** Slack channel structure, sprint demo cadence, release event cadence, ambassador rituals — none of these are spelled out as deliverables. Should be — they are the operating model.
- **No explicit pilot-to-broader-rollout sequencing.** Section 7 of the VML library reads as an unfinished outline ("Roadmap example, Backlog example w/ t-shirt sizing, Sprint Timeline, Request intake flow"). The practice has flagged this as a known gap; closing it is high-priority.
- **No leadership-incentives conversation in commercial discovery.** Figma Design Leaders' "structural incentives all the way to the top" reframe is the most useful discovery question for executive conversations the practice doesn't yet ask.
- **No "trust as production constraint" framing for AI-era governance.** Obello's framing — indemnification, brand-safe generation, auditability, permissioning — needs to enter our governance POV explicitly for AI-using clients.
- **AI-pattern governance is a separate gate from component governance.** When the system ships consumer-facing AI patterns, the governance contract extends to disclosure language, refusal copy, citation correctness, approval workflows for tool calls, and the regulatory disclosure regime (EU AI Act Article 50, US state laws). Twilio Paste's PIA-before-shipping requirement is the cleanest published instance of this gate. Our current governance offering treats components as the unit of governance; for AI patterns, the unit is the *behaviour*, not the component. (See 25-ai-aware-patterns-and-conversational-ui.)
- **Multi-brand technical governance under-articulated.** Practice has multi-brand at the token / theming layer; the multi-brand source (Apr 2025) covers process governance but skips technical governance. Practice's combined POV is unique but not yet documented coherently.

## External perspectives

### Validate

- **Curtis's contribution model** (definition, scale, criteria, 6-step onboarding) — directly aligns with the practice's intent and operationalizes it. Near-internal-tier weight.
- **Curtis's team structure** (1:2 designer:dev, 50% floor, lead structure, library tiers, communities of practice) — the most rigorous external framework; aligns with internal practice principles.
- **Couldwell's Guardians/Ambassadors/Lead model** — three-tier governance that maps to the practice's preferred centralized + contribution structure.
- **Couldwell's "educate, not enforce"** stance — the right governance posture; aligns with internal "library of solved problems" framing.
- **Idean's "make tools, not rules"** — same posture, different phrasing. Useful slogan.
- **Multi-Brand Governance (Apr 2025)** on the 9-step intake / 4-criterion qualification / 10-step testing / 7-step contribution. Process layer; complements internal technical governance.
- **Frost on makers/users distinction** — the right governance scaffolding for the system team's relationship with consuming teams.
- **Anderson's "DS as infrastructure" reframe** — implies governance is operations; needs SLA-grade thinking.

### Challenge

- **Curtis on "pure federation is chaos."** Pushes against any client (or internal materials) leaning too far toward distributed contribution without a centralized backbone. *"No central foundation, curators or maintainers... that is the chaos that leads to consistency, quality and maintainability"* (sarcastic).
- **Curtis on "Catalog-wide and new-catalog work is system-team driven, not contributor."** Pushes back on the assumption that contributions can scale to anything. There are limits to federation.
- **Curtis on NPS** — "not well-respected in the design community." Use SUS for product ease-of-use, especially with open-ended follow-up.
- **Curtis on "Slack + Office Hours ≠ communications plan."** Pushes against the easy "we'll do office hours" answer. Real adoption requires structured, scheduled, varied communication.
- **Hugo Raymond / Figma Design Leaders on "structural incentives all the way to the top."** Misalignment is a leadership problem, not a tooling problem. The most useful single reframe for executive conversations.
- **Figma Design Leaders on "shift left."** Engineers should enter design discussions during ideation, not at handoff. Pushes against the practice's residual "handoff" framing even when we say "incremental handoff."
- **Frost on neglect.** *"The biggest existential threat to any system is neglect."* (Schleifer/Airbnb, in Frost.) Most systems die from under-maintenance, not from poor design. Governance is the maintenance contract.
- **Idean (Audrey Hacq) on org-readiness:** *"If the maturity of the organization is low... then the design system is not the main solution, or the only one."* Practice should treat this as a discovery diagnostic; some clients aren't ready for governance, and we should name it.

### Extend

- **Adopt Curtis's contribution scale and criteria verbatim** as part of the practice's governance offering. They productize cleanly.
- **Productize the Ambassadors program** as a workshop or 4–6 week consulting engagement post-Launch.
- **Adopt library tiers (Core foundation / Core library / Shared / Team library)** as the scoping conversation for any multi-team client.
- **Adopt Curtis's six measurement themes** (Productivity / Coverage / Satisfaction / Consistency / Quality / Efficiency) as the measurement framework. (See `08-ongoing-maintenance.md`.)
- **Adopt Curtis's three coverage definitions awareness** — he names three competing industry definitions (didoo, Morningstar, Veriff) without picking one. Practice should pick one and acknowledge alternatives.
- **Adopt Mall's weekly stakeholder update template** (*What We Did / Where We're Headed / How You Can Help*) as default executive cadence.
- **Adopt the "structural incentives" reframe** for executive Discovery conversations.
- **Adopt the "shift left" doctrine** explicitly — engineers in design discussions from ideation.
- **Adopt the "v1" release framing** (Duolingo) — explicit permission to ship imperfect things and iterate.
- **Adopt the "trust as production constraint" framing** (Obello) for AI-using clients.

## Tensions and open questions

1. **Governance scoped commercially or after handoff.** Today: not scoped. Should it be? Yes, in three forms: a Run-phase retainer (ongoing core-team support), an Ambassadors program offering (4–6 week embedded coaching), or a quarterly governance review (one-shot per quarter, productized). The practice currently sells the build; the keep-alive is value the practice creates and gives away.
2. **Centralized vs. cyclical at handoff.** The internal practice prefers Centralized with contribution. Curtis's stages model says cyclical/federated is the eventual destination. At handoff, where should the client be? Working synthesis: Centralized at handoff with documented contribution path, expecting the client to evolve toward cyclical at month 9–12. Set this expectation explicitly.
3. **Top-down mandate vs. bottom-up groundswell.** Both work; sequencing matters. Bottom-up to evidence (the pilot does this); top-down to scale (the executive coalition does this). Tessa Rodes (IBM Cloud, via InVision MVP): *"Groundswell efforts can get you halfway there, but it's hard to reach true consistency without a clear directive from the top."*
4. **Contribution-vs-participation, in practice.** Curtis is precise: contributions are tangible/useful/federated/released; everything else is participation. Most teams blur this and over-claim contribution as a metric. Practice should adopt the precise definition and use it for measurement.
5. **Coverage definition.** Curtis names three industry definitions without picking one. Practice should pick: *proportion of pages/screens using system components vs. team-made* (Morningstar's definition) is the most actionable. Pick, document, measure.
6. **How much governance is enough.** Small org with 30 engineers vs. enterprise with 3,000. Governance models scale differently. The 9-step intake is overkill for a 30-engineer org; office hours alone won't work for 3,000. Practice should articulate decision rules for sizing.
7. **Versioning practice.** SemVer for the library is field-standard. Per-component versioning is also possible (Curtis's library tiers each have their own cadence). Practice should commit to one approach as default and document the rare cases where the alternative is appropriate.
8. **Deprecation policy.** *How* a component leaves the system gracefully is under-articulated. Salesforce's `Sass-Deprecate` library is one option; explicit `_legacy` suffix is another. Either way, deprecation needs a documented timeline (typically: announce → marked deprecated → final removal in N months) and a migration codemod where feasible.
9. **AI-era governance: trust as constraint.** Obello's framing — indemnification, brand-safe generation, auditability, permissioning. None of this is in current internal materials. Should be — clients are starting to ask.

## Failure modes specific to this phase

- **No governance model.** System ships; nobody knows who decides what. Conflicts pile up; consumers fork; system fragments.
- **Centralized model without contribution path.** Everything flows through the core team; bottleneck; consumers stop trying.
- **Federation as starting point.** No backbone; distributed teams contribute incoherent components; system fragments. Curtis: "chaos."
- **Coalition of one.** Single executive sponsor; sponsor moves; system orphaned in 18 months.
- **Slack + Office Hours as the entire communication plan.** Necessary but not sufficient. Sprint demos, training events, release events, roadshow all needed.
- **No Ambassadors / embedded-liaison structure.** Core team has no eyes/ears in product teams; loses product-context awareness; misses adoption opportunities.
- **Contribution = participation conflation.** "We had 200 contributions this quarter" — most of which were comments on Slack. Real contribution count is low; measurement misleads.
- **Catalog-wide refactors expected from contributors.** Federated teams can't ship system-wide refactors; they get attempted, fail, and damage trust.
- **No "no" criteria for contributions.** Everything proposed is accepted; system bloats with single-team needs.
- **Coverage Map missing or stale.** Stakeholders can't see reach; ROI can't be defended; investment shrinks.
- **Versioning ad-hoc.** No SemVer, no changelog discipline; consumers can't tell what's safe to upgrade.
- **No deprecation strategy.** Old components linger; new components added on top; system grows without removing.
- **Governance ends when engagement ends.** Practice walks away; client team has the contribution model on a slide but never operates it. Adoption decays within a quarter.
- **Org isn't ready.** Engagement assumes collaboration culture that doesn't exist. (Hacq, Idean, 2019 — should be a Discovery diagnostic.)
- **AI-era governance ignored.** No indemnification policy, no brand-safety enforcement, no AI activity logging. AI-using consumers generate off-brand outputs; legal flags it; system loses standing.

---

*Provenance: Centralized model preferred with explicit awareness of blind spots, three-governance-models naming (centralized / federated / distributed), 4 governance best practices (clear roles / intake / version control / regular reviews), 3-8 person team at 20-30 hrs/week, SemVer for library and components, Systems Week cadence, Cross-disciplinary onboarding, Coverage Map with Live/In-Use/In-Progress/In-Planning statuses, and the multi-brand governance overview are internal POV from VML library (2024-2026) and DS-Scoping (2026). The CareCentrix 2026 team composition (5-person production core + 2 specialists) is internal POV from the 2026 pitch. The contribution definition (tangible/useful/federated/released), contribution-vs-participation distinction, contribution scale (Fix → New Catalog), 8 contribution criteria (shared need / timing / responsibility / availability / capability / direction / cost / relative value), 6-step contributor onboarding ("conversation, not a form"), library tiers (Core foundation / Core library / Shared / Team / Team project file), communities of practice (Steering Committee / Extended Design / Extended Developer), 1:2 designer-to-dev ratio, 50% capacity floor, Solitary → Central → Federated stages, and "Slack + Office Hours ≠ communications plan" are from Nathan Curtis (Operating Design Systems, Sep 2023), treated as near-internal-tier weight. The 9-step intake / 4-criterion qualification / 10-step testing / 7-step contribution workflow process layer is from Multi-Brand Governance (Apr 2025). The Guardians/Ambassadors/Lead three-tier governance model and "educate, not enforce" posture are from Andrew Couldwell (Laying the Foundations, 2019). "Make tools, not rules" is from Idean (Hack the Design System, 2019). The "structural incentives all the way to the top" reframe, GitHub's shift-left doctrine, Linear's "set the standard, push responsibility to the team," ServiceNow's "no longer being a handoff" reframe, Duolingo's "v1" release framing, and the 80%/92%/91%/55% survey stats are from Figma's Design Leaders ebook (Apr 2025). "Borrow, don't build" the pilot, executive coalition of 1-3, and Tessa Rodes' top-down/groundswell quote are from InVision MVP (2020). The launch-and-forget failure mode and 5-level maturity ladder are from InVision Benchmarking (2020). The makers/users distinction, three change types (modify/add/retire), and "biggest existential threat is neglect" are from Brad Frost (Atomic Design, 2016). "Trust as production constraint" framing for AI-era governance is from Obello State of AI Design (2026). The "DS as infrastructure" reframe driving operations-grade governance is from Sam Anderson (Nov 2024). The org-readiness diagnostic ("if maturity of organization is low... DS is not the main solution") is from Audrey Hacq (Idean, 2019).*

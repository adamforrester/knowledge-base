---
type: practice-area
title: Ongoing Maintenance
description: Post-launch operating model, retainer shapes, KPIs. The phase the practice sells the least and external sources flag as the biggest delivery gap.
tags: [phase, maintenance, retainer, kpis]
timestamp: 2026-05-05
---

# 08 — Ongoing Maintenance

> Most design systems die quietly, not loudly. They are launched, used briefly, then neglected — outpaced by the products that consume them, until the consuming teams forget they exist. Maintenance is the work of preventing that. It is also the phase the practice currently sells the least, and where every external source from Frost (2016) to Anderson (2024) names the largest gap between consultancy delivery and durable client outcomes.

---

## What this phase is, and why it matters

If a design system is **infrastructure** (Anderson, Nov 2024), maintenance is operations: versioning, observability, deprecation, contribution intake, measurement, communication, and continuous improvement of the system itself. Infrastructure that isn't operated is infrastructure that is failing, slowly. The practice currently delivers the system and frames maintenance as "the client's responsibility" — and that framing is the most consequential commercial gap in the engagement model.

Three reasons this matters now:

1. **Adoption is the only scoreboard, and adoption is a maintenance metric.** Coverage trends down quarter over quarter without active maintenance — products evolve faster than the system if no one funds the catch-up. (See `00-principles-and-philosophy.md` Principle 1.)
2. **AI consumers age systems faster than human consumers.** A token without a description, a component without `avoid_when`, a metadata file that hasn't been refreshed since the component last changed — each is a silent failure point that compounds across every AI-generated artifact downstream. (Wolosin, Jun 2025; AI-Compatible Design Systems, Feb 2025.)
3. **Brand evolves; products evolve; tools evolve.** A system frozen at handoff is already legacy by month 6. The 2024–2026 tooling shifts (Figma Variables modes, DTCG, MCP, Code Connect, Components-as-Data) make any 2023-tier system materially older every quarter it doesn't update.

Frost's epigraph (quoting Schleifer at Airbnb) is the right framing: *"The biggest existential threat to any system is neglect."*

## What actually happens in this phase

Six clusters of work. All are continuous.

### 1. Initiative types and rhythm

Curtis names five initiative types — each with a distinct personality and skill profile (*Operating Design Systems*, Sep 2023):

- **Scaling** — make more of what you already have. Predictable to plan and estimate.
- **Refactoring** — improve what's already made. Often impacts the entire catalog. Challenges mindsets; invokes API and naming reconsiderations. *Not for all designers and developers.*
- **Expanding** — make something new. Discovery and exploration; unpredictable.
- **Servicing** — support who you make things for. Core team would rather "make stuff." Needs attention and perseverance.
- **Operating** — run and manage how you do things. Once architected, predictable to execute.

A healthy maintenance year mixes all five. A team that only does Scaling and Expanding is feeding a Feature Ceiling; a team that only does Servicing is firefighting. Curtis's pattern recognition here is sharper than anything in the practice's internal docs and should be adopted.

The **Feature Ceiling** is Curtis's diagnostic for systems whose UI-component growth plateaus over time. Three responses, in order:

- *"Demand justifies more."* Federate or expand core team.
- *"Our system isn't just UI components."* Expand into Service (onboarding, plugins, sparring critique) and Community (foundations, contribution).
- *"Our system has grown unwieldy."* Refactor.

Most clients hit the ceiling at month 9–12. Practice should anticipate and prepare them.

### 2. Versioning, deprecation, and breaking change

Versioning practice (cross-source consensus):

- **SemVer (MAJOR.MINOR.PATCH)** for the library and individual components.
- **Each library tier versions independently** (Curtis's library tiers — Core foundation, Core library, Shared, Team).
- **Changelog discipline** — every release has a changelog entry; changelog is published and searchable.
- **Asymmetric package taper** (Curtis): code packages taper *slowly* across past versions; design assets diminish *sharply*. This drives different deprecation strategies for code vs. Figma assets.

Deprecation lifecycle:

1. **Announce** — release notes, deprecation warning in code, doc page banner. Set a removal date.
2. **Soft-deprecate** — component still works, but consoles a warning; docs flagged; new uses discouraged.
3. **Migration support** — codemod (where automatable), migration guide, office-hours support.
4. **Final removal** — typically N months after announcement. Default: 6 months for major changes.

Generation tokens (Curtis): naming legacy tokens with `_legacy` prefix to coexist with current generation (e.g., `DS2_0` alongside `DS3_0`). Useful pattern for migrations.

The practice's commercial materials name SemVer but do not yet ship a deprecation playbook. Should — clients ask for it the moment they have to deprecate their first component.

### 3. Communication cadence

Curtis's operational cadence is the most concrete in the field:

- **Sprint demo every 2 weeks** — open invitation, recorded.
- **Quarterly training events.**
- **Semi-annual planning** (with surveys + interviews + must/should/could/shouldn't matrix scoring + workshop validation: "We will / We might / We won't").
- **Release events** with rolling "Major release is coming / New feature spotlight / Deep Dive" cadence.
- **Org-wide updates** monthly or quarterly.
- **Slack channels** structured: `#system-core` (private), `#system-design`, `#system-dev`, `#system-ambassadors`, special-topic channels.

Audience growth pattern (Curtis): demos start at 8–15 people, can grow to 40–80 over time. Demos can become the system's social fabric.

The internal scoping doc names some of this implicitly ("regular stakeholder updates," "monitor adoption with quantitative metrics") but does not articulate the cadence as a maintenance contract. Should.

### 4. Measurement framework

Curtis's six measurement themes are the most complete the field has produced. Practice should adopt:

| Theme | Key Question | Examples | Data collection |
|---|---|---|---|
| **Productivity** | How much did the (core/contributor) team make? | # components, # doc pages, # releases, # fixes | Project management, component code tagging |
| **Coverage** | Is the system being used? Who? How much? | # of products using; % of page applying system; lifecycle status by adopter | Automated package.json audits, automated component tracking, downloads |
| **Satisfaction** | How satisfied are internal/external customers? | NPS, SUS, complaint frequency | Surveys, polls, sentiment analysis |
| **Consistency** | Is the experience consistent? On-brand? | Visual / content / interactive cohesiveness | Manual product/page audits |
| **Quality** | Are products more performant? Accessible? Usable? | Accessibility scoring, usability testing, performance metrics | Manual audits, automated scoring tools, controlled studies |
| **Efficiency** | How much time was saved? Faster-to-market? | % dev time reduced, # days reduced, % CSS reduced, average turnaround | Employee reviews, system v product codebase comparison |

Curtis's notes:

- **NPS is "not well-respected in the design community."** Use SUS for product ease-of-use, with open-ended follow-up.
- **Coverage definition is contested.** Three competing industry definitions (didoo: proportion sourced from system; Morningstar: proportion of a page using system vs. team-made; Veriff: components in use across all repos). Practice should pick one — *Morningstar's "% of page applying system"* is the most actionable — and acknowledge the alternatives.

The internal practice's ROI calculator (VML library) gives concrete component-level efficiency numbers (Button: 67.7% efficiency gain; Dynamic menu: 81%) — the kind of evidence Curtis's measurement framework collects systematically. Together they form the start of a defensible measurement methodology the practice could publish.

### 5. AI-era maintenance

Three new maintenance concerns that legacy materials don't address:

**Metadata freshness tracking.** AI-Compatible Design Systems (Feb 2025): a CI check that fails the build if a component file changes but `.ai.json` doesn't. Without this, metadata silently drifts from reality and AI consumers produce wrong outputs at scale.

**AI activity as diagnostic data.** Figma DS x AI (2025): track how AI interprets components, log where it breaks rules or invents workarounds. Each rejected or heavily-modified AI output signals a metadata, instruction, or composition gap. The maintenance flywheel: instrument AI consumption → log drift → prioritize DS updates → measure if drift drops.

**Brand evolves, retraining required.** Obello (2026): *"What may have felt right six months ago might feel tone-deaf in the present moment."* As brand voice and visual identity evolve, the system's encoded brand rules need to evolve too. This is qualitative judgment, not a CI check.

The practice's claim: the maintenance phase post-handoff should include **periodic quarterly evaluation against a standard prompt suite** — testing whether the system is still producing on-brand AI output. The AI-Compatible doc names a 5-dimension brand-alignment rubric (Token Compliance / Component Correctness / Composition Quality / Accessibility / Design Language Fidelity, scored 1–5) — this is the right instrument.

### 6. Continuous improvement loops

Curtis's planning lifecycle (semi-annual; useful at any cadence):

1. **Solicit** — surveys + interviews ("imagine a year from now, the system failed — what's the evidence?")
2. **Score** — must / should / could / shouldn't matrix.
3. **Validate** — workshop with stakeholders ("We will / We might / We won't").
4. **Implement** — communicate + prepare in Jira/Asana with `[Component] [StepType]` ticket titles.

Communication is constant, with a fixed three-section template (Mall, 90 Days Activity #28/#41): **What We Did / Where We're Headed / How You Can Help.**

Two distinct user groups must be optimized for (VML library; Curtis):

1. **System users** — the designers and developers consuming the system.
2. **End users** — people using the products built with the system.

When the two diverge, name the tradeoff out loud. (See `00-principles-and-philosophy.md` Principle 8.)

## Our POV

The internal practice's Performing & Optimizing macro-phase (Section 4 Phase 3 of the VML library) covers:

- Adoption & Integration Strategy — ensure consumer teams understand AND continue to effectively utilize.
- Support consumer teams — ongoing assistance.
- Communication strategy — releases, changes, feedback, roadshows, onboarding.
- Collect Feedback — designers, developers, stakeholders.
- Contribution Process — proposals from team members.

The internal scoping doc Stage 5 (Governance) and Stage 6 (Adoption) cover:

- Versioning (SemVer for library and components).
- Systems Week (1 week internal per 3 weeks pilot).
- Coverage Map (Live / In Use / In Progress / In Planning).
- Office hours, Slack channels, onboarding integration.
- Quantitative metrics (consistency, efficiency, quality, satisfaction, reusability, maintainability, time saved).
- Qualitative beta sentiment.

CareCentrix 2026 commercially: maintenance is largely **out of scope.** Engagement ends at handoff. Supporting roles framed as bucket-of-hours that can be added.

Thrive 2024 commercially: "Run" phase covers Adoption & Integration / Support / Communication / Feedback / Contribution but isn't priced.

**Practice-distinctive POVs in this phase:**

- **Performing & Optimizing as a named phase.** The framework recognizes ongoing maintenance as a distinct stage; the field consensus aligns.
- **ROI calculator with concrete numbers** (Button 67.7%, Dynamic menu 81%). Most consultancies cite anecdotes; we cite math.
- **Coverage Map with explicit statuses** (Live / In Use / In Progress / In Planning). Strong adoption-evidence artifact.
- **Systems Week** cadence — names the discipline that internal-only maintenance work needs.
- **Two user groups** (system users + end users) framing — useful tradeoff vocabulary.
- **5-dimension brand-alignment rubric** for AI-era brand fidelity (AI-Compatible Design Systems, Feb 2025).
- **Periodic quarterly AI evaluation** against a standard prompt suite — the right maintenance ritual for AI-using clients.

**Gaps in our current commercial Ongoing Maintenance standard, honestly named:**

- **The phase is not commercially priced.** Single biggest gap. No retainer, support tier, governance subscription, or quarterly review offering is currently part of the practice's productized service stack. This is the work the practice should be selling — and isn't.
- **No measurement framework as deliverable.** KPIs are mentioned in Discovery; measurement methodology, dashboards, instruments are not produced. Curtis's six themes is a ready-made framework — adopt and ship.
- **No deprecation playbook.** SemVer named; deprecation lifecycle not documented. Codemods (the practice has the capability; doesn't yet productize it) would close a real gap.
- **No "what to log when AI consumes the system" playbook.** AI activity as diagnostic data (Figma 2025) is the right framing; the practice's commercial materials don't articulate what to instrument or how.
- **No org-wide measurement reporting cadence.** Monthly / quarterly governance review is named in the multi-brand source; not productized in our offerings.
- **No release retrospective process.** Curtis names sprint demo and release events; doesn't articulate retrospective. Practice could ship structured release retrospectives as a deliverable.
- **No formal contribution-intake operating procedure** post-handoff. Curtis's six-step onboarding and 9-step intake exist as IP; not yet shipped as part of "we'll set up your contribution model" engagement.
- **No coverage definition committed.** Three industry definitions; practice hasn't picked one. Should.

## External perspectives

### Validate

- **Curtis's six measurement themes** (Productivity / Coverage / Satisfaction / Consistency / Quality / Efficiency) — the most complete measurement framework the field has produced. Validates the internal practice's intuition; operationalizes it. Near-internal-tier weight.
- **Curtis's five initiative types** (Scaling / Refactoring / Expanding / Servicing / Operating) — gives maintenance work a vocabulary the practice doesn't yet have.
- **Curtis on the Feature Ceiling** — names the diagnostic the practice has been observing without naming.
- **Curtis on planning lifecycle** (Solicit / Score / Validate / Implement) — operational planning rhythm.
- **Curtis on communication cadence** (sprint demo every 2 weeks; quarterly training; semi-annual planning; release event rolling cadence) — directly usable as the practice's recommended client cadence.
- **Frost on neglect** — *"The biggest existential threat to any system is neglect."* (Schleifer, in Frost.) The right framing.
- **Frost's three change types** (modify / add / retire) — the right governance scaffolding for ongoing change.
- **Couldwell** (*Laying the Foundations*, 2019) Ch.11 — diplomacy is as important as the pixels. The leadership half of maintenance.
- **Couldwell** — "A design system is a marathon, not a sprint."
- **AI-Compatible Design Systems** (Feb 2025) on metadata freshness tracking — internal POV; CI gate that fails the build if `.ai.json` lags component code.
- **Figma DS x AI (2025)** on AI activity as diagnostic data — the maintenance flywheel for AI-era systems.
- **Anderson** (Nov 2024) — DS as infrastructure implies maintenance is operations, not janitorial work.
- **Multi-Brand Governance** (Apr 2025) — quarterly cross-brand audits as a maintenance pattern.

### Challenge

- **Curtis on NPS** — "not well-respected in the design community." Use SUS instead. Practice should not lead with NPS in measurement.
- **Curtis on coverage definitions** — three competing definitions exist; practice should pick one. We default to vague.
- **Curtis on "Catalog-wide and new-catalog work is system-team driven, not contributor."** Pushes against the assumption that contributions can scale to catalog-level work; system-wide refactors are core-team work.
- **Curtis on initiative-type personality fit** — Refactoring "challenges mindsets to learn new ways" and is "not for all designers and developers." Staffing maintenance against initiative type matters more than headcount.
- **Frost on "ask forgiveness, not permission."** Sometimes maintenance gets stuck in governance; the right move is to ship and document. Anti-perfectionism at the maintenance layer.
- **Couldwell on "guidelines are no good in your head."** Stale documentation is silent failure. Maintenance includes maintaining docs.
- **Obello on brand-evolution-requires-retraining** — pushes the practice to treat brand rule sets as living documents, not one-time captures.
- **Idean on org-readiness** — Hacq's caveat: a system can't fix an org that isn't ready to maintain it. Practice should diagnose maintenance-readiness during Discovery; some clients shouldn't start until they're staffed for keep-alive.

### Extend

- **Curtis's six measurement themes** as the practice's measurement methodology. Adopt and publish.
- **Curtis's five initiative types** as the practice's vocabulary for maintenance work.
- **Curtis's Feature Ceiling diagnostic** for client conversations at month 9–12.
- **Curtis's `[Component] [StepType]` ticket titling** as project-management hygiene.
- **Curtis's planning lifecycle** (Solicit / Score / Validate / Implement) as the practice's recommended quarterly cadence.
- **Mall's three-section weekly stakeholder update** template as the executive cadence.
- **Asymmetric package taper** awareness — different deprecation strategies for code (slow taper) vs. Figma (sharp diminish).
- **Generation tokens** (`_legacy`, `DS2_0`/`DS3_0`) for migrations.
- **AI evaluation rubric** (5 dimensions, 1–5 scale) as periodic quarterly evaluation instrument for AI-using clients.
- **Codemods** as default deliverable for major version migrations. Practice has the capability; should ship it.
- **Release retrospectives** as a structured deliverable.
- **Salesforce's `Sass-Deprecate` library** (or equivalent) as deprecation tooling pattern.
- **Quarterly governance review** as a productized offering — one-shot per quarter, fixed scope, fixed price.

## Tensions and open questions

1. **What does the practice sell after handoff?** Today: not much. Three productizable offerings:
   - **Run-phase retainer** — embedded core-team support for 6–12 months post-Launch.
   - **Quarterly governance review** — one-shot per quarter; measurement, contribution review, roadmap update, brand-alignment audit.
   - **Ambassadors program** — 4–6 week embedded coaching for the client's emerging Ambassadors team.
   Which is right depends on the client. Practice needs all three articulated and priced.
2. **Coverage definition.** Three industry definitions; practice should commit. Working synthesis: Morningstar's *"% of pages applying system components"* is the most actionable measurement; Veriff's *"components in use across all repos"* is the most comprehensive but engineering-heavy; didoo's *"proportion sourced from system"* is intermediate. Pick Morningstar as default; provide alternatives by client context.
3. **NPS or SUS.** Curtis prefers SUS. Most clients reach for NPS by default. Practice should pick SUS with open-ended follow-up.
4. **Deprecation timeline default.** No published consensus. Working synthesis: 6 months for major component deprecations; 3 months for token deprecations (with `_legacy` overlap); shorter for documented bugs/security fixes.
5. **AI evaluation cadence.** Quarterly is reasonable for stable systems; monthly for systems undergoing brand evolution or heavy AI use. Worth being explicit per client.
6. **Maintenance-readiness as a Discovery diagnostic.** Practice should add a Discovery question: *Is the org committed to funding the system after handoff? What's the planned headcount, what's the budget, who's the named owner?* If the answer is "we'll figure it out later," that's a yellow flag — system is unlikely to survive year 1.
7. **The role of the consultancy after handoff.** Practice could be the long-term governance partner (multi-year retainer), the periodic auditor (quarterly review), or the migration consultant (called back for major version migrations every 2–3 years). Different revenue shapes; practice should articulate which is the default offering.
8. **AI maintenance as commercial work.** Quarterly AI brand-alignment evaluation is value the practice can deliver and clients can fund. Not yet productized.

## Failure modes specific to this phase

- **No staffed maintenance.** System ships; client's planned headcount never materializes; system stops shipping releases within a quarter. Single most common failure mode.
- **Maintenance as cleanup, not work.** Treated as residual/janitorial; not funded; not respected. The team that does it leaves; the system decays.
- **No versioning discipline.** Releases shipped without changelogs; consumers don't know what changed; trust erodes; consumers stop upgrading.
- **No deprecation lifecycle.** Components linger forever; system grows without removing; codebase fragments; new component adoption slows because the catalog is overwhelming.
- **Coverage stat unmeasured.** ROI cannot be defended; investment cuts when budget tightens.
- **NPS as primary metric.** Vague signal; easy to game; doesn't drive action.
- **No release retrospectives.** Same mistakes ship every quarter; team doesn't learn.
- **AI metadata stale.** `.ai.json` files date from initial build; components evolved; AI consumers produce outputs from old metadata; off-brand drift goes undetected.
- **Brand evolves; system doesn't.** Six months after the brand refresh, the system still ships old colors; consuming products fork to keep up.
- **Feature Ceiling unrecognized.** Component growth plateaus at month 9–12; team doesn't recognize the pattern; instead piles on more components; system grows unwieldy.
- **Office Hours becomes the entire support model.** Curtis: *"Slack + Office Hours ≠ communications plan."* Without sprint demos, training events, release events, the system loses social oxygen.
- **Ambassadors program never launched.** Promised in handoff; never staffed; the bridge between core team and product teams never gets built.
- **Codemods unwritten for breaking changes.** Migrations stall on consuming teams; old version lingers indefinitely.
- **No maintenance-readiness diagnostic in Discovery.** Engagement begins with a client who can't afford the system after handoff. Practice ships it; client can't operate it; trust erodes; future engagements harder to win.

---

*Provenance: The Performing & Optimizing macro-phase, Coverage Map with Live/In-Use/In-Progress/In-Planning statuses, SemVer for library and components, Systems Week cadence, two-user-groups framing (system users + end users), and ROI calculator math (Button 67.7%, Dynamic menu 81%) are internal POV from VML library (2024-2026) and DS-Scoping (2026). The 5-dimension brand-alignment rubric for AI-era brand fidelity, metadata freshness tracking via CI, and quarterly AI evaluation against a standard prompt suite are internal POV from AI-Compatible Design Systems (Feb 2025). The five initiative types (Scaling / Refactoring / Expanding / Servicing / Operating), Feature Ceiling diagnostic, six measurement themes (Productivity / Coverage / Satisfaction / Consistency / Quality / Efficiency), three contested coverage definitions (didoo / Morningstar / Veriff), asymmetric package taper, generation tokens (`_legacy`, `DS2_0`/`DS3_0`), planning lifecycle (Solicit / Score / Validate / Implement), `[Component] [StepType]` ticket titling, sprint demo / quarterly training / semi-annual planning / release event cadence, and "Slack + Office Hours ≠ communications plan" / "NPS not well-respected" are from Nathan Curtis (Operating Design Systems, Sep 2023; Design Tokens, Nov 2024), treated as near-internal-tier weight. The deprecation patterns (Sass-Deprecate library) and ten qualities of a maintainable system are from Brad Frost (Atomic Design, 2016, Ch.5). "A design system is a marathon, not a sprint" and "guidelines are no good in your head" are from Andrew Couldwell (Laying the Foundations, 2019, Ch.11). "Make tools, not rules" is from Idean (Hack the Design System, 2019). The "DS as infrastructure implies operations-grade maintenance" reframe is from Sam Anderson (Nov 2024). AI activity as diagnostic data is from Figma DS x AI (2025). Brand-evolution-requires-retraining is from Obello State of AI Design (2026). The three-section weekly stakeholder update template (What We Did / Where We're Headed / How You Can Help) is from Dan Mall (Design System in 90 Days 2nd Ed., 2023). Quarterly cross-brand audits are from Multi-Brand Governance (Apr 2025). Org-readiness diagnostic is from Audrey Hacq (Idean, 2019).*

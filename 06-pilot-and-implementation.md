---
type: practice-area
title: Pilot and Implementation
description: Running the pilot product team — validating the system in production and building the executive coalition for scale.
tags: [phase, pilot, adoption, executive-coalition]
timestamp: 2026-05-05
---

# 06 — Pilot & Implementation

> The hinge between "the system exists" and "the system is used." A well-run pilot validates the system in production conditions with a real consuming team and converts evidence into the executive coalition that scales adoption. A poorly-run pilot — or no pilot at all — produces a system that ships and is forgotten.

---

## What this phase is, and why it matters

By the time components are built and documentation is in place, the practice's instinct is to "launch." That instinct is wrong. A system launched with no consuming team committed is the canonical failure mode in every external source from 2017 to 2026: *"Too often, teams put months or years of work into their design system, 'launch' it, and then wonder why no one uses it."* (InVision Benchmarking, 2020.)

The pilot is the rehearsal — a real team using a real subset of the system on real product work, with the system team alongside, generating evidence of value before broad rollout. A pilot done well produces three durable outputs:

1. **Validated components and patterns** in production conditions, surfacing real prop combinations, real edge cases, real performance issues.
2. **Adoption evidence** for the executive coalition — quantitative and qualitative — that converts the system from "design team initiative" to "company infrastructure."
3. **A pre-trained champion team** who become the first ambassadors when broader rollout begins.

The internal practice currently names "pilot validation with engineering" as a milestone in CareCentrix 2026 timelines — but does not yet articulate a methodology for what makes the pilot successful, how to choose the pilot product, or what the exit criteria are. This is the most consequential gap in the practice's commercial scoping for this phase.

## What actually happens in this phase

Six clusters of work, mostly sequential.

### 1. Pilot product selection

Mall's eight-factor scoring rubric (90 Days Activity #7) is the field's most validated approach — and it converges precisely with the practice's own scoping doc. Score every product on the roadmap 0–10 against:

1. **Potential for common components.** Will this product use components that several others will also need?
2. **Potential for common patterns.** Same question, at the pattern level.
3. **High-value elements.** Heart-of-product moments, even if uncommon.
4. **Technical feasibility.** Can the consuming codebase actually adopt the system within the pilot window?
5. **Available champion.** Is there a senior person on this team who actively wants the system?
6. **Scope fits a 3–4 week pilot timeframe.** Not a multi-quarter epic.
7. **Technical independence.** Decoupled from legacy systems / shared dependencies that would block adoption.
8. **Marketing potential.** Will success here excite other teams?

Score, prioritize, pick one. (Maybe two, never three.)

The complementary heuristic from InVision MVP (2020): **borrow, don't build** the pilot. Choose a product that has an in-flight redesign or a new product version with budget and a champion already in place. Don't manufacture momentum that doesn't exist. When picking among similar candidates, choose the *most complex* one — surfacing real complexity early is more valuable than easy wins.

### 2. The Practice Pilot (rare; valuable)

Mall's *Practice Pilot* (90 Days Activity #24) — *before* the real pilot, run a fake one using a third-party design system (e.g., Material Design) with the system team and a feature team. Rehearse:

- The handoff between system designer and feature designer.
- The contribution flow.
- The component-request intake.
- The release and announcement cadence.
- The Slack / office-hours support pattern.

Costs days. Catches process bugs that would otherwise surface mid-real-pilot. Almost no consultancy does this. The practice should productize it as a 3–5 day workshop offering, scoped between Discovery and Build.

### 3. Pilot scope and team alignment

Per the internal scoping doc and InVision MVP (2020), pilot MVP scope has three parts — not just one:

1. **A starter component collection.** All Foundations sections (color, type, spacing, etc.) plus *only three component groups*. (Buttons recommended as one of the three — button states surface real complexity.) Each group needs at minimum: definition, dos and don'ts, accessibility/compliance rules.
2. **A user base.** 1–3 executive sponsors plus a developer fanbase. Not "all engineers in the company"; a specific small group.
3. **A contribution plan.** One written answer to: "How will people contribute changes or new components?" Don't overbake it. It's part of MVP, not after.

Most consultancy proposals scope only the first part. The InVision MVP framing makes the second and third parts non-negotiable. The practice should scope all three.

The pilot **team alignment** activities (cf. CareCentrix 2026 milestones):

- Pilot validation kickoff.
- Embedded engineering presence in the pilot team (one DS-side engineer paired with the consuming team's engineers).
- Pilot Team Collaboration Plans (the scoping doc names this) — gauging interest, capacity, expected hours per week from the consuming team.
- Component Implementation Roadmap blocking realistic timeframes per component.

### 4. Major-release milestones

Curtis's *Operating Design Systems* workshop (Sep 2023) names a four-stage milestone progression — the sharpest articulation in the field:

| Milestone | Definition | Quantity | Quality | Stability |
|---|---|---|---|---|
| **Commit** | Plan, design language, technical architecture committed. | — | — | — |
| **Alpha** | A few features through the entire process to prove "how to build." | 2–4 components | Low | Moderate |
| **Beta** | Enough features at sufficient stability for early adopters (the pilot team). | 10–15 | High | High |
| **Launch** | A major release of all features available generally. | 20–30 | Full | Full |

The pilot operates between Beta and Launch — the consuming team adopts the Beta, surfaces issues, and the system iterates toward Launch. This is the structure the practice should adopt for any engagement scoped past MVP.

### 5. Pilot evidence collection

The pilot's primary deliverable is *evidence*, not the deployed feature. What to collect:

**Quantitative (through the pilot window):**
- Time-to-first-component-shipped (from the consuming team's perspective).
- Number of components used vs. ignored.
- Defects introduced vs. caught by the system.
- Velocity comparison (pre- and post-system) for similar work.
- Token compliance % in the pilot codebase.
- Accessibility conformance vs. baseline.
- Any specific KPI committed in Discovery (See `01-discovery-and-strategy.md`).

**Qualitative:**
- Consuming-team designer and engineer interviews — what felt easier, what felt harder, what surprised them.
- "How much easier / less frustrating / more efficient" sentiment per consuming-team member (InVision MVP, 2020 — beta sentiment template).
- Specific stories: the moment the system saved hours, the moment it got in the way.

This evidence becomes the **synthesis report for the executive coalition** that scales adoption. Mall's three-section weekly stakeholder update template (*What We Did / Where We're Headed / How You Can Help*) carries this through the pilot window with a fixed cadence.

### 6. Pilot exit criteria and rollout sequencing

Most engagements treat "pilot complete" as "the calendar window ended." The right question is whether the pilot's evidence supports broader rollout. Practice should articulate exit criteria explicitly:

**Pilot succeeds when:**
- The consuming team is using the system as default for new work.
- Time-to-component is trending down.
- The team's engineers and designers report (in interviews) that the system reduced friction.
- The system survived at least one component request from the team that turned into a contribution back.
- An identified second pilot team is committed to adopting next.

**Pilot is failing when:**
- The consuming team is bypassing the system to ship faster.
- Components are being forked or hardcoded.
- Engineering velocity is the same or worse.
- The champion has changed roles or lost interest.

**Pilot is incomplete when:**
- The above signals are mixed and the system team has not surfaced clear evidence either way.

Failure mode for failing/incomplete pilots: shipping anyway. The right move is to extend the pilot window or pause and triage — not to declare "Launch" against the calendar.

After Launch, Curtis's **warranty period** kicks in: rapid releases of fixes, priority enhancements, integration support. This is the "launch tail" that converts early adopters into ambassadors. Often unscoped commercially; should be a clearly-priced add.

## Our POV

The CareCentrix 2026 commercial standard names a **pilot validation milestone** at the end of Build:

- "Pilot validation with engineering" appears in both Option 1 (12–16 weeks) and Option 2 (16–24 weeks) timelines.
- "Backoffice Portal POC" is discussed as the likely primary pilot target in the discovery questions.
- The consuming team validates components in context, ideally via Storybook.

The Thrive 2024 deck implicitly describes piloted-then-scaled adoption (Ford, T-Mobile case studies) but does not articulate a pilot methodology.

**Practice-distinctive POVs in this phase:**

- **Pilot validation with engineering as a named milestone**, not a catch-all "go live."
- **Embedded engineering during pilot** — DS-side engineers paired with consuming team's engineers.
- **Storybook as the validation surface** — pilot team interacts with components in their actual development environment, not in a Figma file.
- **Discovery identifies the pilot target.** The 10 procurement discovery questions include "What is the current status of the Backoffice Portal POC — is it actively in development, and will it serve as the primary pilot target?" — naming pilot as a Discovery decision, not a Build afterthought.
- **Option 2 explicitly creates "system-wide readiness, broader organizational adoption, and long-term scalability"** — the recognition that Launch is not the end of the engagement.

**Gaps in our current commercial Pilot & Implementation standard, honestly named:**

- **No pilot scoring framework in deliverables.** The internal scoping doc names eight-factor scoring; CareCentrix-style proposals don't ship a scored pilot decision. Should — gives the client confidence the choice is rigorous.
- **No Practice Pilot offering.** Mall's pre-pilot rehearsal is rare and valuable; productizing it as a 3–5 day workshop would differentiate.
- **MVP scoping covers components only.** The InVision three-part MVP (collection + user base + contribution plan) is not yet how the practice scopes Discovery+Foundations+Build. The user base and contribution plan should appear as deliverables in Discovery and Build, not deferred to "after handoff."
- **No alpha/beta/launch milestone progression.** Curtis's Commit → Alpha → Beta → Launch with quantity/quality/stability dimensions is sharper than our current "Pilot validation → Handoff." Adopt.
- **No documented pilot exit criteria.** "Pilot validation with engineering" is named; what makes it succeed or fail is not. Most consequential single gap in this phase. Define and ship.
- **No warranty period framing or pricing.** Curtis's post-launch fast-fix window is implicit in our commercial model but not named or priced. Should be a default add-on (fixed-price 4–6 week warranty after Launch).
- **No measurement plan during pilot.** Practice doesn't ship a pilot measurement framework as a deliverable. KPIs are mentioned in Discovery; no operational plan to collect them during pilot.
- **Synthesis-to-coalition handoff under-articulated.** Mall's stakeholder synthesis report at end of Discovery becomes the first executive coalition artifact; the pilot synthesis report at Launch becomes the next one. Practice doesn't yet ship either as default.

## External perspectives

### Validate

- **Mall's eight-factor pilot scoring** (90 Days Activity #7, 2023) — converges with the internal scoping doc's eight-factor scoring. Strong cross-validation.
- **Mall's "rule of three"** for components at pilot scope — "if three or more teams need this component right now, it goes in the design system" (Activity #26).
- **InVision MVP's three-part scope** (collection + user base + contribution plan) — extends the practice's pilot thinking.
- **InVision Benchmarking (2020)** on the launch-and-forget failure mode — validates the practice's emphasis on adoption.
- **InVision MVP "borrow the pilot, don't build it"** — choose products with existing momentum.
- **Curtis's Commit → Alpha → Beta → Launch milestones** with quantity/quality/stability progression — operational structure the practice should adopt.
- **Curtis's warranty period** post-Launch — names the implicit fast-fix window.
- **Frost** (*Atomic Design*, 2016) on "make a thing → show it's useful → make it official" — the canonical three-step adoption arc; the pilot is the "show it's useful" step.

### Challenge

- **InVision MVP's "borrow, don't build."** Pushes against the consultancy instinct to scope every system from scratch. The right pilot is one with momentum *and* budget *and* a champion already in place — not one we manufactured.
- **Mall's "Practice Pilot" before real pilot.** Pushes against the assumption that the system team has rehearsed the workflows. Most haven't.
- **Mall on "pilot evidence is the deliverable."** Pushes against the assumption that the deployed feature is the deliverable. The feature is the *vehicle*; the evidence is the deliverable.
- **InVision MVP on developer-first user base.** "Save 100 developers one hour of work, and you've done miracles." Most consultancy proposals (including ours) center designers as the primary pilot audience. The leverage is on the engineering side.
- **Couldwell** (*Laying the Foundations*, 2019) on **MVP-first stance.** "You might not get it right the first time, so consider getting to an MVP — or a beta launch phase — as fast as possible." Constraint as feature.

### Extend

- **The Practice Pilot** as a productizable workshop offering (3–5 days). Pre-real-pilot rehearsal using Material or another reference system.
- **Curtis's milestone progression** (Commit / Alpha / Beta / Launch with Quantity / Quality / Stability scales). Sharper than our current single "pilot validation" milestone.
- **InVision's three-part MVP definition** (collection + user base + contribution plan). Reshape commercial scoping to include all three.
- **Pilot exit criteria as an explicit document.** The practice should ship a one-page "pilot exit criteria" artifact that the consuming team and DS team agree to at pilot kickoff. Forces the conversation.
- **Pilot synthesis report** as a default deliverable (mirrors Mall's Discovery synthesis report). One artifact for Discovery synthesis at the start; one for Pilot synthesis at the end.
- **Warranty period as default** post-Launch scope. 4–6 weeks of priority response on fixes, integration questions, contribution support.
- **Beta sentiment template** (InVision MVP) — "How much easier / less frustrating / more efficient" beta-user surveys. Lightweight, qualitative, persuasive.

## Tensions and open questions

1. **One pilot or two.** A single pilot reduces complexity; two pilots stress the system more and produce more diverse evidence. For most engagements, one is right. For multi-platform / multi-brand engagements, two may be warranted.
2. **Pilot duration.** The internal scoping doc names "3–4 week" pilot windows. Mall agrees. Reality: most enterprise pilots run 6–8 weeks because the consuming team has its own velocity. Practice should negotiate the *evidence* scope rather than the calendar — define what evidence is sufficient and end when it's collected.
3. **Pilot success without champion change.** The biggest single risk to pilot success is champion turnover. The practice does not yet build "champion redundancy" into the pilot plan — what if the named champion is reassigned mid-pilot? This is worth a discovery question.
4. **Public Launch vs. Quiet Launch.** Some engagements benefit from a public launch event (training, press, internal blog, all-hands demo). Others benefit from a quiet beta-to-launch transition. Public launches generate more adoption energy but risk over-promising; quiet launches are safer but generate less momentum. Discovery determines.
5. **What goes in the V1.** Couldwell: "Cut corners on the scope of the feature, but never the polish or the fun." Duolingo's "v1" framing — releases are explicitly marked v1, freeing the team from launch perfectionism (Figma Design Leaders 2025). Practice should adopt v1 framing — sets honest expectations and creates momentum for v2.
6. **Pilot to scale transition.** What signals the system is ready for broader rollout? Practice doesn't have published criteria. Working synthesis: at least one second pilot team committed; first pilot's contributions accepted into the system; pilot's velocity-and-quality data trending positive at four weeks; explicit executive sponsor green-light for scale.
7. **What if the pilot fails.** The worst-case the practice's commercial materials don't address: pilot evidence shows the system isn't producing value. Working synthesis: extend the pilot, triage the gaps, or — rarely — pause the engagement and renegotiate scope. Pretending a failed pilot succeeded is the worst outcome.
8. **Adoption Enablement scoped commercially.** Curtis names Adoption Enablement as a discrete initiative track (Roadshow, Getting Started, Training, Office Hours, Slack, Releases). Practice doesn't yet sell this as a discrete deliverable. Should — clients are willing to pay for adoption support; we're leaving value on the table.

## Failure modes specific to this phase

- **No pilot.** System launches against a calendar; consuming teams aren't invested; adoption stalls. Single most common failure mode in the field.
- **Pilot picked by volunteer.** The team that volunteered may not be the team that should pilot — they may be small, low-leverage, or not representative. Scoring is not optional.
- **Pilot too small.** Three components, one team, two weeks; produces no evidence either way.
- **Pilot too large.** A whole product redesign; the system team can't keep up with consuming-team requests; pilot stalls.
- **Champion changes mid-pilot.** No backup; champion leaves the team; pilot loses oxygen.
- **No evidence collected.** Pilot ends; no quant data, no qualitative interviews. No basis for executive coalition.
- **Pilot designs not shipped to production.** Consuming team treats pilot as side project; never deploys. System never tested in real conditions.
- **Pilot synthesis not produced.** No artifact for the executive coalition; the pilot's value is invisible to stakeholders.
- **Premature Launch.** Calendar says Launch; evidence says incomplete. Ship anyway. Adoption stalls and never recovers.
- **No warranty period.** Engagement ends at Launch; consuming team has questions, bugs, integration issues; no support. Trust erodes; consumers go back to bespoke.
- **Pilot metrics not aligned with Discovery KPIs.** Pilot collects whatever's easy; Discovery's committed KPIs go unmeasured. Engagement can't defend its outcomes.
- **Adoption Enablement skipped.** No roadshow, no training, no office hours. The system "exists" but consumers don't know how to use it.

---

*Provenance: The pilot validation milestone, embedded engineering during pilot, Storybook as validation surface, and Discovery-determines-pilot-target framing are internal POV from CareCentrix 2026. Eight-factor pilot scoring, Component Implementation Roadmap, and Pilot Team Collaboration Plans are from DS-Scoping (2026). The eight-factor pilot scoring rubric, Practice Pilot (Activity #24), rule of three (Activity #26), stakeholder synthesis report (Activity #27), and weekly stakeholder update template (Activity #28) are from Dan Mall (Design System in 90 Days 2nd Ed., 2023). The three-part MVP definition (collection + user base + contribution plan), "borrow don't build" the pilot, "save 100 developers an hour" framing, and beta sentiment template are from InVision MVP (2020). The launch-and-forget failure mode is from InVision Benchmarking (2020). The Commit / Alpha / Beta / Launch milestones with Quantity / Quality / Stability progression and the warranty period framing are from Nathan Curtis (Operating Design Systems, Sep 2023), treated as near-internal-tier weight. "Cut corners on scope, never polish or fun" and "v1" framing are from Colleen MacDonald (Duolingo, in Figma Design Leaders 2025). MVP-first stance is from Andrew Couldwell (Laying the Foundations, 2019). The "make a thing → show it's useful → make it official" three-step adoption arc is from Brad Frost (Atomic Design, 2016).*

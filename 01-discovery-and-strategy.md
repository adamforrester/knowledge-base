# 01 — Discovery & Strategy

> The phase that determines whether the engagement succeeds. Most failed design systems fail here — not in components, not in tooling, not in handoff. They fail because nobody did the work to know what the organization actually needed, who would actually use it, who would actually decide, and what was actually true about the existing landscape.

---

## What this phase is, and why it matters

Discovery & Strategy is the work of replacing assumptions with evidence and replacing wishful alignment with negotiated alignment. It produces three things:

1. **A defensible scope** — informed by what exists, what's broken, and what's politically possible.
2. **A coalition** — at least one executive sponsor, a pilot product team, and a working coalition of designers/engineers who are committed before launch, not after.
3. **A working strategic frame** — a North Star, draft principles, a maturity baseline, and a prioritized opportunity map.

The practice's own 2026 scoping doc opens with the right premise: a DS is a "living product with distinct, evolving stages." Discovery is the stage that decides whether the product has a market. We routinely under-invest in it because clients perceive it as "talking, not building" — an expectation we should be willing to push back on. The InVision Benchmarking guide (2020) names the failure mode directly: *"Too often, teams put months or years of work into their design system, 'launch' it, and then wonder why no one uses it. If they skip steps (e.g. try to scale a system without first doing the necessary discovery work and audits), then the design system won't gain traction and will ultimately fail."*

Mall's 2023 update is sharper still: of the 90-day playbook, roughly the first 30 days are Discovery activities. Foundations and Components don't begin until alignment, evidence, and a pilot have been secured.

---

## What actually happens in this phase

There is broad cross-source agreement on the activities, even where the artifact names differ. The strongest synthesis is six clusters of work, run roughly in parallel rather than strictly sequentially:

### 1. Strategic alignment (the North Star)

Before designing anything, define why the system exists for *this* organization, who it serves, and how its success will be judged.

- **Mission, network, strategy, vision.** Mall's "Assemble the North Star" (Activity #1, borrowed from Watkins' *The First 90 Days*) — what (mission + goal), who (audiences served), how (strategic priorities), why (vision + incentives). Mall's pointed instruction: **write *the company's* North Star, not the design system's.** The system aligns to the org, not the other way around.
- **Three to five opinionated design principles** — drafted as hypotheses in this phase, expected to be rewritten retrospectively after the pilot. (See `00-principles-and-philosophy.md` Principle 10.)
- **Initial KPIs** — committed at kickoff, not at handoff. Adoption %, time-to-component, defect rate, brand consistency score, accessibility conformance. The rigor of this list will determine whether the engagement can defend itself a year out.
- **Ecosystem positioning** — a diagram showing where the DS sits in the broader stack: CMS, CRM, DAM, build pipelines, marketing automation, app shells, code repositories. (Scoping doc; Mall 90 Days Activity #11.) Prevents the system from being mis-scoped against tools it will need to integrate with.

### 2. Audits and inventory

The objective baseline. What exists, what is duplicated, what is broken, what is unused.

- **Interface inventory** — UXPin's five-part framework (2017) is still the cleanest checklist: Patterns, Colors, Typography, Icons, Space. Walk the codebase and the screens; count appearances; surface anomalies. ("62 shades of gray" remains the canonical example of how this work generates buy-in.)
- **Asset and code audit** — every existing Figma library, design file, code library, plugin, token export. Categorize by *visual* (which look alike) *and* by *purpose* (the *why* behind their existence) — the second axis is what reveals which patterns belong in the system. (Scoping doc.)
- **Audit of digital products and experiences** — review of how products are actually used by end users. Identifies UX pain, accessibility issues, and which patterns are bearing real weight vs. which are decorative. (VML library, Section 4.)
- **Pattern-spotting, both objective and aspirational.** Mall splits this into Activity #5 (objective: "8 of 8 cards have small sans-serif body") and Activity #10 (aspirational: "what would we like to see *more* of and *less* of?"). The future system isn't only in your code today; the audit must capture both signals.

### 3. Stakeholder mapping and interviews

The organizational substrate. Who decides, who blocks, who champions, who consumes.

- **Stakeholder identification at three tiers** (Scoping doc): designers/engineers/PMs/writers (15–20 customer interviews, ~30–45 min each); leadership (~10 leader interviews); end users (5–10 interviews about the broader product context, *not* the DS).
- **The Influence Map** (Mall, 90 Days Activity #3) — green/yellow/red on supportive/undecided/opposed; thick/thin arrows on relational influence. Distinct from the org chart, layered on top of it. This artifact is the most useful single Discovery deliverable in the external corpus and one we should adopt by default.
- **Influence/interest 2x2** (VML library) — High influence/high interest (brand leads, design leads, tech leads, product leads, DS team); High influence/low interest (executive sponsors, cross-org leaders); Low influence/high interest (developers, junior designers, PMs). Drives engagement priority and update cadence per quadrant.
- **Interviews that are not about the design system.** Mall's explicit guidance — and our practice should adopt it. Asking leaders about the design system invites theater; asking them about the org's future, their priorities, and their frustrations produces signal we can position the system against. The system gets named at the end of the conversation, not the beginning.

### 4. Maturity baseline and readiness assessment

Where is this organization on the curve, and what's realistic?

- **Six Signs** (VML library Section 5) — our practice's diagnostic for *opportunity recognition*. Strong for the first executive conversation; less precise as a maturity instrument.
- **Chaos / Silos / Integration** (VML library, ~line 604) — three-stage maturity heuristic; useful internally but coarse for client diagnosis.
- **InVision's five-level ladder** (Benchmarking, 2020) — Nascent → Basic → Integrated → Distributed → Optimized. Each level has a behavioral checklist and "level-up" resources. The most-cited industry benchmark; productizable as a "Where are you?" workshop.
- **Paavan's 0–4 scale** (Design System Canvas, 2022) — more compact, suited to a single workshop session. 0 = bespoke per product → 4 = fully documented DS with dedicated team integrated into all workflows.

The practice does not currently sell maturity assessment as a discrete offering. It should — see `09-gaps`.

### 5. Pilot identification and scoring

Which product team goes first, and why.

- **VML's eight-factor pilot scoring** (Scoping doc): common components, common patterns, business value, technical feasibility, available champion, scope (3–4 week pilot timeframe fit), technical independence (decoupled from legacy), marketing potential.
- **Mall's identical eight-factor scorecard** (90 Days Activity #7) — the convergence with our scoping doc is striking and probably not coincidental; either we adopted it from Mall or we both adopted it from a common source. Either way, the scorecard is well-validated and should be a default Discovery artifact.
- **MVP "borrow, don't build" heuristic** (InVision MVP, 2020) — choose a pilot product that has an in-flight redesign or new product version with budget and a champion already in place. Don't manufacture momentum that doesn't exist. The complementary heuristic: when picking among similar candidates, choose the *most complex* one — surfacing real complexity early is more valuable than easy wins.
- **The Practice Pilot** (Mall, 90 Days Activity #24) — *before* the real pilot, run a fake one using a third-party system (Material) with the DS team and a feature team. Rehearse the handoff, the contribution flow, the meetings. Costs days; saves weeks. We should productize this.

### 6. Initial buy-in / executive coalition

Discovery's payoff. The buy-in artifact, the synthesis presentation, the move from research to commitment.

- **Synthesis report** (Mall, 90 Days Activity #27) — cover slide, "what's happening," "what we heard," "a draft plan with measurement," "stay informed," appendix with anonymized quotes. Distributed as PDF + email + Loom. Email matters because it forwards.
- **The 7-beat presentation narrative** (UXPin, 2017): inventory process → inconsistencies per category → numbers → cost translation (hours × salary) and UX harm → DS as the answer → ongoing managing team → clear "yes." Still the cleanest sales arc in the literature; pair it with our case-study metrics.
- **Coalition of 1–3 sponsors** (InVision MVP, 2020) — never one. Leaders with most to gain: the product leader of the pilot product, a design leader with budget, a frontend dev leader who's used a DS before. Frame impact in *their* metrics. Tessa Rodes' IBM Cloud lesson: "Groundswell efforts can get you halfway there, but it's hard to reach true consistency without a clear directive from the top." Bottom-up to evidence, top-down to scale.
- **Weekly stakeholder update** (Mall Activity #28/41) on a fixed three-section template — *What We Did / Where We're Headed / How You Can Help.* A communication ritual, not a deliverable.

---

## Our POV

The practice's discovery motion has three signature artifacts.

### The 20 Strategic Discovery Questions (VML library)

The most complete single artifact in our internal materials for this phase. Used in early strategic conversations to drive structure:

1. What is important to our organization at the highest level?
2. What design and code assets do we have at our disposal?
3. Who is important to our design system effort?
4. What work is coming up soon for our teams?
5. What unofficial systems already exist in design and code, even if they're not intentional or documented?
6. Which teams have upcoming needs that a design system could solve?
7. Which teams have the most immediate interface needs that can most effectively grow our design system?
8. Which teams should we and have we talked to?
9. Which stakeholders should we and have we talked to?
10. What opportunities already exist for systemization and scaling in the near future?
11. How can a design system fit seamlessly into the larger ecosystem of our organization's tools and technologies?
12. What end user problems and opportunities could a design system address?
13. What needs, desires, and concerns do our stakeholders have? What do they share?
14. What components do product or feature teams need now or soon?
15. What is our repeatable process for working on products and features?
16. What shared language can we start to use?
17. What components will we start with?
18. What information do our consumers need from a reference website?
19. When will we be working on each component?
20. How does our team make decisions?

These are *strategic* questions for internal alignment — they assume the engagement has begun. They are not yet a *procurement* discovery instrument.

### The 10 Procurement Discovery Questions (CareCentrix 2026)

Our 2026 sales motion has separated out a tighter, structured procurement-readiness instrument used *before* the engagement begins, in four categories:

**Tools & Licensing** — existing Figma license? brand fonts licensed for digital? existing icon library?
**Stakeholders & Process** — day-to-day POC? approval authority for design direction? engineering availability for alignment + handoff?
**Brand & Content** — existing brand guidelines and assets at start? content guidelines from existing materials or stakeholder interviews required?
**Technical Context** — existing design files / UI kits / component libraries to be aware of? status of the pilot target (e.g., the Backoffice Portal POC) — actively in development?

These two instruments serve different jobs. The 20 questions are for the first weeks of the engagement; the 10 are for the proposal/scoping conversation that decides whether there is an engagement. The practice should be explicit about that separation in its materials.

### The Six Signs Diagnostic (VML library)

Our practice's own opportunity-recognition framework, used in pitches, RFPs, and exec conversations. (Listed in `00-principles-and-philosophy.md`; will not repeat.) Functionally, the Six Signs play the same role for our practice that the Maturity Ladder plays for InVision — but as an *opportunity* lens, not a *level* lens. We should consider whether to fuse them into one diagnostic that does both jobs.

### Our methodology shape

Our 2026 client-facing motion (CareCentrix) compresses Discovery into ~4 weeks at the front of a 12–24 week engagement, with these activities:

- Brand onboarding (review existing brand guidelines/assets).
- Application audit (inventory components, patterns, inconsistencies, redundancies).
- Stakeholder alignment (tools, Figma setup, ways of working).
- Definition sessions (working sessions to surface requirements, priorities, open questions).
- Component backlog (prioritized inventory based on application needs and usage frequency).
- Define design direction (visual language aligned to brand, validated through high-fidelity mockups).
- North star (why the system exists, who it serves, principles).

Discovery deliverables in our 2026 commercial standard:

- Application audit report
- Prioritized component backlog
- Design principles (3–5 opinionated, decision-making principles)
- High-fidelity mockups demonstrating the approved design direction
- Figma environment configured (variables, styles, documentation tooling)

A senior practitioner should notice: **the influence map, the interview synthesis report, the maturity baseline, the pilot scoring artifact, and the executive coalition strategy are not in our 2026 commercial discovery deliverables.** We sell discovery as alignment; we underbuy the people-and-politics work that determines whether alignment will hold. This is the most important practice-level gap in the phase.

---

## External perspectives

### Validate

- **Mall's 8-factor pilot scoring** (2023) ≈ our 8-factor pilot scoring (2026). Strong cross-source consensus.
- **The North Star activity** (Mall) ≈ our "Assemble the North Star" task (Scoping doc). Both borrow from Watkins.
- **Two-tier interview model** (Mall: customers + stakeholders + end users; us: designers/engineers/PMs/writers + leaders + end users). Identical structure; nearly identical sample sizes.
- **Audit-as-buy-in tactic** (UXPin 2017, our case study work). Numbers persuade — "62 shades of gray" works because it converts to a concrete cost translation.
- **Discovery as where alignment happens** (CareCentrix 2026; Mall 2023). Universal across sources.

### Challenge

- **Discovery questions about the org, not the system** (Mall, 2023). Our 20 questions are mostly about the system. Mall's interview script is mostly about the company. The shift would tighten our research and reduce theater.
- **The Influence Map vs. the Influence/Interest 2x2.** Both are useful. The 2x2 is for prioritizing engagement; the Influence Map is for *predicting outcomes*. We have the first; we don't routinely produce the second. Adopt.
- **Maturity ladder as a sold artifact.** External sources have strong, productizable maturity instruments (InVision 5-level, Paavan 0–4). Our Six Signs / Chaos-Silos-Integration is coarser. We should productize a "Where are you on the design systems curve?" workshop as either a sales-stage artifact or a paid 1–2 day diagnostic engagement.
- **The Practice Pilot.** Almost no consultancy does this. Running a fake pilot on Material before the real one would close most of the handoff/coordination gaps that surface mid-engagement. Worth piloting (so to speak) on our next engagement.
- **Three-part MVP scoping** (InVision MVP, 2020). Our discovery scopes the collection. MVP includes the user base (1–3 sponsors + dev fanbase) *and* the contribution plan as part of MVP, not after. Our procurement structure should reflect this — the user base and contribution plan should appear as deliverables in Discovery and Foundations, not be deferred to "after handoff."
- **Borrow, don't build** (InVision MVP). Our internal Prism position implies the same principle, but our discovery conversations don't always recommend borrowing as a starting move for clients. We should — most clients don't need bespoke foundations on day one. (See `00-principles-and-philosophy.md`.)

### Extend

- **The Design System Canvas** (Paavan, 2022). A 10-box, 60–90 minute kickoff workshop with a sponsor and a few key stakeholders. Boxes: Problem / Existing Assets / Maturity Level / New Resources (assets + processes) / Affected Products / Consumers / Maintainers / Champions / Scope / Adoption Strategy / Costs. Productizable as a paid kickoff session.
- **Glossary as Discovery deliverable** (Mall Activity #25). Component, Component Library, Design System, Governance, Guidelines, Pattern, Pilot, Reference Site, UI Kit. Each definition signals "this is what we've agreed to call this thing." Most of our engagements treat glossary as a docs appendix; making it a Discovery negotiation prevents the three-systems-in-one outcome.
- **Naming and logo as a Discovery / Foundations activity** (Mall Activities #43–49). Named systems are adopted at higher rates. Adds maybe one designer-week of work; pays off for the lifetime of the system.
- **Developer-first user research** (InVision MVP, 2020). "What types of things do you find yourself building again and again? Where do you spend the most time? Which meetings or messages feel redundant?" Asked of developers *before* announcing the system — "guerilla marketing through user research." Developer adoption is the leverage point for ROI; our Discovery scripts should weight engineers as primary research subjects, not secondary.
- **The "magic wand" and "fast forward" prompts** (Mall). "If you had a magic wand and could change one thing about how things work here, what would it be?" / "Fast forward a year — everyone is thrilled. How did that happen?" / "Fast forward a year — total failure. Why did it fail?" The pre-mortem questions surface political risk that direct questions don't.

---

## Tensions and open questions

Where the field — and our practice — has not yet settled.

1. **Top-down vs. bottom-up sequencing.** Our docs lean bottom-up (groundswell, prove value, expand). Tessa Rodes (IBM Cloud, via InVision MVP) argues consistency at scale ultimately requires a top-down mandate. The synthesis: bottom-up to *evidence*; top-down to *scale*. Discovery should produce both — the pilot evidence and the executive coalition that will mandate adoption when the evidence is in. Whether we sequence those activities serially or run them in parallel from week 1 is engagement-dependent.

2. **Principles up-front or retrospective.** UXPin (2017) and InVision Handbook (2018) draft principles in Foundations; Mall (2023) extracts them retrospectively from real pilot decisions. The pragmatic answer: draft a working set in Discovery; treat them as hypotheses; rewrite from evidence after the pilot. Anything aspirational that didn't get reached for during the pilot should be deleted, not preserved.

3. **Borrow vs. curate vs. collect.** UXPin recommends inventorying everything then standardizing. InVision MVP recommends starting from your most polished product (curate over collect). Mall recommends collecting *both* objective and aspirational patterns in parallel. The synthesis: collect objective patterns to ground the system; curate from the most polished product to set the *quality* bar; use the gap between them as the system's roadmap.

4. **How much Discovery is enough.** Our 2026 commercial standard caps Discovery at ~4 weeks. Mall's 90 Days uses ~30 days of the 90 — a third — almost entirely for Discovery. The right answer is org-readiness-dependent: a Nascent organization needs more discovery than an Integrated one. This argues for a maturity-baseline-first model: assess maturity in week 1; size Discovery investment to maturity. We do not yet do this.

5. **Discovery for whom.** The single most useful evolution in the external corpus has been the shift from "designer-led" to "developer-led" Discovery. Our Discovery questions still center the design conversation. Whether the practice should re-weight is an open POV question.

6. **Pilot definition and exit criteria.** "Pilot validation with engineering" appears in our 2026 milestones. What makes a pilot *successful*? What makes it *failing*? What is the exit criterion that promotes a pattern from pilot to canonical? We do not have published criteria. (See `09-gaps`.)

7. **The "Selling DS" boundary.** Our internal library treats Discovery and selling as overlapping — the Six Signs, the discovery questions, the case studies all serve both jobs. This is fine internally; with mature clients it becomes a tell that the practice has not yet separated *what we believe* from *how we pitch*. A mature 2027+ Discovery offering should look more like a paid diagnostic engagement and less like an extended pitch.

---

## Failure modes specific to this phase

- **"We already know the answer."** Skipping discovery in favor of starting components on day one. Common when a design lead already has a vision and treats discovery as obstacle. Symptom: the system launches and the engineering team rebuilds it from scratch.
- **Discovery as theater.** Going through the motions — running interviews, producing a deck — without changing scope based on findings. Symptom: the proposal that emerges from Discovery is the same proposal that went into it.
- **Org-chart mapping instead of influence mapping.** Treating reporting lines as power lines. Symptom: the wrong sponsor is invested; the right blocker is unaddressed.
- **Designer-only research.** Talking only to designers about a system that engineers will spend the most time using. Symptom: the system is beautiful and unused.
- **No pilot scoring; pilot is "whoever volunteered."** A self-selected pilot is a pilot whose champion may not survive procurement. Symptom: the pilot stalls when the champion changes roles.
- **Principles written for the deck, not for the team.** Symptom: the principles are not referenced in any later disagreement; they are documentation, not decision tools.
- **Maturity not assessed.** The practice ships the same engagement to a Nascent org and an Integrated org. Symptom: the Nascent org is overwhelmed; the Integrated org is bored.
- **Coalition of one.** Single executive sponsor. Symptom: the sponsor moves orgs and the system is orphaned in 18 months.
- **No glossary.** Symptom: nine months in, "pattern," "template," and "page" mean different things to design, engineering, and content. The system is three systems.

---

*Provenance: the 20 Strategic Discovery Questions, 8-factor pilot scoring, Six Signs, Chaos/Silos/Integration model, and the 10 Procurement Discovery Questions are internal POV from VML library (2024–2026) and CareCentrix 2026 pitch. The Influence Map, Practice Pilot, retrospective principles, glossary-as-Discovery, magic-wand questions, three-part MVP definition, and Design System Canvas are external (Mall 2023; InVision MVP 2020; Paavan 2022; UXPin 2017) and are noted as adoption candidates rather than current practice.*

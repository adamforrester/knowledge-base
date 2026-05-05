# Notes: External sources — Principles & Discovery focus

Synthesis of six external design-systems sources, scoped to (a) cross-cutting principles / philosophy and (b) Discovery & Strategy methodology. These notes feed the first two files of the 10-file knowledge base.

---

## Per-doc reading log

### 1. *Design System in 90 Days, 2nd Ed.* — Dan Mall, Design System University, 2023
- **Lines:** 4,486
- **Read:** ToC + intro (lines 1–565), Activities 1–13 in detail (the Discovery arc, lines 565–1850), Activity 25 (Glossary, ~2360–2440), Activity 27 (Stakeholder synthesis, ~2510–2620), Activity 31–33 (Reference site / coverage / collaboration plan), Activity 39–42 (component pilot wrap, principles extraction, ~3540–3725). Skimmed Activities 14–24 and 43–52.
- **Summary:** A 52-activity, 90-day playbook for kicking off (or restarting) a design system inside an enterprise. Built around the "Design System in 90 Days Canvas" (a FigJam template) and the DACI decision framework. The first ~30 days are nearly all Discovery: North Star alignment, asset audit, influence mapping, stakeholder + customer + end-user interviews, ecosystem visualization, pilot team scoring, glossary, and synthesis report.
- **Authority:** High. Mall is one of the field's most cited practitioners (former Sparkbox, runs Design System University, frequent Brad Frost collaborator). Tactical, opinionated, scripted to the point of providing email and interview templates.

### 2. *Design Systems Handbook* — Marco Suarez, Jina Anne, Katie Sylor-Miller, Diana Mounter, Roy Stanfield (InVision), 2018 (referenced and re-used through 2020)
- **Lines:** 7,389
- **Read:** Chapter 1 "Introducing Design Systems" (lines 1–770), Chapter 2 start "Designing Your Design System" (1080–1310 — team models, customer interviewing, visual audit), Chapter 3 "Foundations" / guiding principles (2300–2500), Chapter 5 "Design principles" section (5600–5780), Process section after that. Skimmed code-level chapters.
- **Summary:** Foundational handbook. Defines a design system as "a collection of reusable components, guided by clear standards, that can be assembled together to build any number of applications." Establishes the Standards + Components binary, debunks myths, walks through team models (solitary / centralized / federated), foundational principles (consistent / self-contained / reusable / accessible / robust), and the role of design principles, process, and voice.
- **Authority:** High. The canonical text most practitioners cite as their introduction to the discipline. Authors are from Airbnb, Salesforce, Etsy, GitHub, IBM.

### 3. *Design System Canvas* — Paavan, designsystemcanvas.com, 2022
- **Lines:** 44 (read fully)
- **Summary:** A single one-page template (Lean Canvas / Business Model Canvas analog) with 10 boxes: Problem, Existing Assets, Maturity Level (0–4 scale), New Resources (assets + processes), Affected Products, Consumers, Maintainers, Champions, Scope, Adoption Strategy, Costs. Designed to garner buy-in and structure planning in one workshop session.
- **Authority:** Medium. Indie / community artifact, but elegant. Most useful as a *meeting tool* — not a methodology in itself.

### 4. *The Actionable Guide to Starting Your Design System: The 100-Point Process Checklist* — Marcin Treder, UXPin, 2017
- **Lines:** 1,040 (read fully)
- **Summary:** A literal checklist organized as inventory → support → team → key decisions → first sprints (color, type, icons, space, first pattern). Practical, tool-prescriptive (UXPin-flavored), strongly weighted toward the "interface inventory" as the lever to win buy-in.
- **Authority:** Medium-high but dated. 2017-era thinking — pre-tokens-as-default, pre-Figma-dominant, pre-the-system-is-a-product framing. Still excellent for the buy-in narrative pattern.

### 5. *Building an MVP Design System* — Rebecca Kerr / Marci Pasenello et al., InVision, 2020
- **Lines:** 1,073 (read fully)
- **Summary:** Reframes "minimum viable" for design systems. Three-part definition (Foundations/Components + Design/Engineering use + Guidelines/Governance), two-thirds of which is "people." Prescribes "borrow, don't build" (steal from existing momentum/products), build a developer fanbase first, prepare 1–3 executive sponsors, keep contribution simple, ship and iterate.
- **Authority:** Medium-high. Less rigorous than 90 Days but the *people-not-just-collection* framing is one of the most useful counter-intuitions in the literature.

### 6. *Guide to Benchmarking Your Design System* — Eli Woolery, Marci Pasenello et al., InVision, 2020
- **Lines:** 792 (read fully)
- **Summary:** Introduces the Maslow-style hierarchy / 5-level maturity model: **Nascent → Basic → Integrated → Distributed → Optimized**. Each level has a behavioral checklist and "level-up" resources. Companion data: from InVision's *New Design Frontier* survey, only 5.5% of orgs were "Visionaries"; 50% of Visionaries had dedicated DS teams vs. 16% of Producers. Warns against scaling without doing "the necessary discovery work and audits."
- **Authority:** Medium-high. The maturity ladder has become the most-cited industry benchmark.

---

## Principles & philosophy — themes across external sources

### Theme 1: A design system is a *product*, not a project
- "A design system is a process and therefore is simultaneously always ready and never done." — Treder, UXPin, 2017.
- "Remember that a design system is a product so staff it like a product instead of a project; you want people committed to maintaining and evolving it." — InVision Handbook, 2018.
- "A leaf blower is a tool, but the Toro PowerJet F700 is a product. Naming something elevates it." — Mall, 90 Days, 2023.
- 90 Days frames a 3-stage journey: **tool → product → practice**. The end state is "the way we do things" — onboarding-level habit (Mall, 2023, intro lines 317–334).

### Theme 2: People are two-thirds of the system
- InVision's diagram (re-used in MVP and Benchmark guides, 2020): Foundations + Components are "a collection of"; Design + Engineering are "used by both"; Guidelines + Governance are "controlled with." Two of those three columns are people-and-process.
- "A collection is a powerful asset, but it's only one third of a design system… People bring it to life." — InVision MVP, 2020.
- "Making the design system isn't the hardest part: getting people to use it is." — Mall, 90 Days, 2023.

### Theme 3: Bespoke design doesn't scale (the industrial-revolution analogy)
- InVision Handbook (2018) and Benchmarking guide (2020) both open with the 1968 NATO software-crisis / component-based-development story. Design is now where software was 50 years ago.
- "Scaling design through hiring, without putting standards in place, is a myth… Every new hire increases the design entropy." — Treder, UXPin, 2017.

### Theme 4: Five technical guiding principles (InVision Handbook, 2018)
A successful design system is: **consistent, self-contained, reusable, accessible, robust.** These are restated almost verbatim in many later docs. They're technology-agnostic foundations, not aesthetic principles.

### Theme 5: Design *principles* are decision-making infrastructure
- Principles "act as a reusable standard for designers to measure their work. They replace subjective ideals with a shared understanding of what design must do." — Suarez et al., InVision, 2018.
- Mall's twist (2023, Activity #42): extract principles *retrospectively* from the decisions you actually made during the first pilot — "Look for the decision points. When the team came to a disagreement, what kind of criteria did you use to resolve it?" Examples: "Rank breaks ties," "Majority rules," "Accessibility above all," "Whomever cares the most wins."
- Etsy's process (referenced by InVision): collect raw data via discussion/survey/interview, then refine.

### Theme 6: Shared vocabulary precedes shared work
- Mall makes Activity #25 a glossary covering: Component, Component Library, Design System, Governance, Guidelines, Pattern, Pilot, Reference Site, UI Kit. Each definition signals either "this is what this means" or "this is what we've agreed to call this thing." (90 Days, 2023, lines 2360–2400).
- Without shared vocabulary, Figma layer names will diverge from BEM markup will diverge from Storybook stories — and you don't have one system, you have three.

### Theme 7: Common failure modes
- "Too often, teams put months or years of work into their design system, 'launch' it, and then wonder why no one uses it. If they skip steps (e.g. try to scale a system without first doing the necessary discovery work and audits), then the design system won't gain traction and will ultimately fail." — InVision Benchmarking, 2020.
- Mall warns about teams on their "third or fourth try" — usually because adoption was treated as a downstream problem (90 Days, 2023, intro).
- InVision MVP (2020) lists the typical excuses: no resources, no time, no confidence — and reframes each as evidence the system is *more* needed, not less.
- Design system not used by the product team is "dead and useless." — Treder, 2017.

### Theme 8: Myths to debunk early
InVision Handbook (2018) lists three common objections you'll need to neutralize when selling the system:
1. **"Too limiting"** → Reality: bespoke solutions create the very debt the system fixes; the system absorbs new solutions, doesn't lock them out.
2. **"Loss of creativity"** → Reality: interdependence makes style updates trivial-effort/high-impact; a redesign that used to take weeks now takes an afternoon.
3. **"One and done"** → Reality: a design system is *living*; the work is maintenance and evolution, not delivery.

---

## Discovery & Strategy — methodologies

### Verbatim discovery / stakeholder interview questions

**Mall's stakeholder interview script (90 Days, 2023, Activity #13).** Five sections, intentionally *not about the design system*:

> *Introduction:* role, tenure, journey at company.
> *Work & Workflow:* day in the life; priorities; current workflow; what's working / could be improved; "if you had a magic wand and could change one thing about how things work here, what would it be?"; current projects; what should/shouldn't use the design system.
> *Tools & Technologies:* what they use regularly, irregularly, love, hate; forced vs. chosen.
> *Hopes & Fears:* prior DS experience; how they heard of yours; will it help; what makes them nervous/skeptical; what makes them excited/eager/curious.
> *Outcome:* "Fast forward a year — everyone is thrilled with the design system. How did that happen?" / "Fast forward a year — total failure. Why did it fail?"
> *Wrap Up:* what should we tell you; how involved do you want to be (collaborator / informed / steer clear); advice; "what questions should we be asking you that we aren't?"

He runs the same script for *potential customers* (designers/engineers/PMs/writers, Activity #6) and *end users* (Activity #12) with light variation. Aim 15–20 customer interviews, ~10 stakeholder interviews, 5–10 (up to 30) end users.

**InVision MVP developer-research questions (2020):**
> What types of things do you find yourself building again and again? Walk me through your workflow from the moment specs arrive. Where do you spend the most time? Which meetings or messages feel redundant? What's the most frustrating part of the process? How do you find the compliance guidelines, assets, details you need?

The framing matters: ask developers diagnostic questions *before* announcing the system; "guerilla marketing through user research."

### Audit / inventory checklists

**UXPin (Treder, 2017) — five-part interface inventory:**
- **Patterns:** screenshots from each product, categorized by frontend modular architecture if it exists.
- **Colors:** traverse code, list every variable + every CSS color, count appearances, organize by hue, count anomalies (UXPin found 116 color variables and 62 shades of gray).
- **Typography:** browser-console walk; build typographic scale h1→small; tie to Sass mixins.
- **Icons:** identify libraries, mark inconsistencies, document implementation methods (inline SVG vs data-URL vs icon font).
- **Space:** grids, paddings.

**Mall (90 Days, 2023) — pattern-spotting audit (Activity #5 + #10):**
- Activity #5 is purely *objective* — group similar components, count what's common ("8 of 8 cards have small sans-serif body").
- Activity #10 is purely *subjective* — "what would we like to see *more* of and *less* of at this organization?"
- The two halves become the base for component abstraction in Activity #34.

**InVision Handbook (2018):** two parallel inventories — visual attributes (color/spacing/type) for the visual language, and UI elements (buttons/cards/modals) for the component library. Recommends CSS Stats and Sketch-Style-Inventory plugin.

### Stakeholder mapping

**Mall's "Influence Map" (90 Days, 2023, Activity #3):**
> "This is different than an org chart. You're identifying the critical decision makers and the individuals within their departments that influence and challenge design system efforts."
- Green = supportive, Yellow = undecided, Red = opposed.
- Thick arrows = strong influence; thin = weak.
- Layered on top of the formal org chart. Used to drive the interview list.

### Readiness / maturity ladders

**InVision Benchmarking, 2020 — five-level model with behavior checklists:**

| Level | Posture | Tells |
|---|---|---|
| **Nascent** | Just getting started | Auditing products; rough plan; starter team model (guild); deploying tools |
| **Basic** | Components exist, not integrated | Dev/design have separate components; basic UI kit; initial token-like definitions; iterating; emerging governance |
| **Integrated** | Design + code aligned | Components reflect both; update processes; contribution checklist; release cadence; conflict-detection processes |
| **Distributed** | Scaled across teams/sub-brands | Multiple sub-systems; public; decentralized contribution; core/sub-system governance |
| **Optimized** | Automated and measured | Custom workflows eliminate manual sync; usage analytics; gap visibility; incentives (stickers, leaderboards, perf reviews) |

The ladder rests on a Maslow analogy: skipping levels causes the failure ("no one uses it") most teams blame on adoption.

**Design System Canvas (Paavan, 2022) — 0–4 maturity scale:**
> 0 — Each product is bespoke, nothing reused.
> 1 — Foundations (color, type) in place.
> 2 — Some reusable components with light docs, outside codebase.
> 3 — Most components linked to a library with documentation; DS is a core part of design workflow.
> 4 — Fully documented DS with dedicated team and detailed roadmap; usage integrated into all workflows.

This is more compact than InVision's five-level ladder and arguably more useful for a one-hour kickoff workshop.

**InVision *New Design Frontier* design-maturity model (2019, referenced 2020):** Producers (41%) → Connectors (21%) → Architects (21%) → Scientists (12%) → Visionaries (5.5%). 50% of Visionaries had dedicated DS teams; 16% of Producers did.

### Kickoff / alignment activities

**Mall's "Assemble the North Star" (90 Days, 2023, Activity #1)** — borrowed from Michael D. Watkins' *The First 90 Days*:
> "Mission, network, strategy, and vision define the strategic direction for a business. They provide the what, who, how, and why necessary to powerfully align action in complex organizations."
- **What:** mission + goal
- **Who:** who we serve
- **How:** strategic priorities
- **Why:** vision + incentives

The DS team's first job is to write *the company's* North Star, not the design system's, so the system can be aligned to it.

**Treder's "Establish Key Rules and Principles" sprint (UXPin, 2017):** decide before sprint 1:
1. From scratch or treat one product as the foundation?
2. Existing tech stack or new?
3. Distribution: one team/product first or across the portfolio?
4. KPIs of the system?
5. Design principles?
6. Communicate decisions to entire company.

**90 Days "Practice Pilot" (Activity #24):** before going live, run an internal practice pilot using an existing third-party design system (e.g., Material) so the team experiences the workflows and tools without political risk. Then extract principles retroactively (#42).

### Buy-in / executive narrative tactics

**UXPin presentation-for-stakeholders template (Treder, 2017, lines 387–413).** A 7-beat narrative:
1. Describe the inventory process.
2. Present key inconsistencies per category.
3. Focus on **numbers** ("62 shades of gray, 16 types of buttons, 5 icon libraries").
4. Translate to cost (hours × average salary) and to UX harm.
5. Propose the design system as the answer.
6. Frame as ongoing, requiring a small managing team.
7. Get a clear "yes."

**InVision MVP "executive coalition" approach (2020):**
- Don't ask for the dream; ask for support of *an experiment*.
- Build a coalition of 1–3 sponsors across product / design / business — never one pillar.
- Find leaders with most to gain: the product leader of your pilot product, a design leader with budget/sway, a frontend dev leader who's used a DS before.
- Frame impact in *their* metrics: PMs care about quality + speed for future iterations; design leaders about big-picture UX time and consistency; dev leaders about speed and reduced frustration.
- Sample script: *"We're already spending X developer hours and X designer hours to get X product out the door. If we invest just 5% more energy and add the work we do into a reusable system, we could save ourselves half the time down the road."*
- IBM Cloud case (Tessa Rodes, 2020): they latched onto a top-down VP directive ("everything must use Carbon 10 within a year") to unlock momentum: *"Groundswell efforts can get you halfway there, but it's hard to reach true consistency without a clear directive from the top."*

**Mall's stakeholder synthesis report (90 Days, 2023, Activity #27)** — the formal buy-in artifact:
- Cover slide (designed-up to tease quality)
- *What's happening?* — recap of activities since last update
- *What we heard* — 1–2 paragraph prose on themes
- *A draft plan* — what we'll do + how we'll measure
- *Stay informed* — async update channels
- *Appendix* — one slide per theme, anonymized quotes

> "Email is important because it can be easily forwarded to others." (Mall) — distribute as PDF + email + a Loom recording walking through it.

Then start a *weekly* stakeholder update cadence (Activity #28 / #41) with a fixed three-section template: **What We Did / Where We're Headed / How You Can Help.**

### ROI / business-case methods

The external corpus is surprisingly thin on rigorous ROI math — they mostly point to outcomes and case studies rather than formulas.

- **UXPin's "hours × salary" framing (2017):** the most explicit. Quantify duplicate-pattern maintenance time, multiply by average salary, present.
- **InVision MVP "developers as ROI multiplier" (2020):** "Save a designer one hour of work, and you've done well. Save 100 developers one hour of work, and you've done miracles." Rationale to build for developers first.
- **Sparkbox study referenced by Mall (2023):** "Yes, Design Systems Do Improve Developer Efficiency and Design Consistency." Cited in Activity #39 (usability test).
- **InVision Benchmarking (2020):** "some teams see gains of 25% or more" in product development efficiency at Distributed/Optimized levels.
- **MVP case study, RealSelf:** "Radiance saves us upwards of 1,250 salaried hours per year, by reducing frustration and rework between groups."
- **MVP case study, IBM iX (Joe Galliford):** a junior designer using a templated DSM reached "50% increase in workflow efficiency" within months.

The *post-MVP measurement* loop (InVision MVP, 2020): collect numbers (time saved, eliminated meetings/tasks/emails) and sentiments (how much easier/less frustrating/more efficient the work felt) from beta users; compile and project to broader scale; "tell leaders what you need" with that data.

### MVP scoping logic (InVision MVP, 2020)

The clearest scoping methodology in the corpus.

**Borrow, don't build:**
- Take advantage of an in-flight brand redesign or new product version (already approved/funded).
- Draw from your most fully-baked product — broad consensus exists; choose the most complex use case when picking between similar candidates.
- If neither, use Material as base.

**Sized scope cap:**
- All Foundations sections (color, type, spacing, etc.).
- *Only three* component groups. (Buttons recommended as one of the three because button states surface real complexity.)
- Each component group needs at minimum: a definition, dos and don'ts, accessibility/compliance rules.

**The two-thirds people rule:**
- MVP is not the collection. MVP includes:
  1. A starter collection (above).
  2. A user base (1–3 executive sponsors + a developer fanbase).
  3. A contribution plan (one written answer to: "How will people contribute changes or new components?").
- Don't overbake the contribution plan. It's also MVP.

**Mall's pilot-team scoring model (90 Days, 2023, Activity #7).** Score every product on the roadmap 0–10 against:
1. Potential for common components.
2. Potential for common patterns.
3. High-value elements (heart-of-product even if uncommon).
4. Technical feasibility.
5. Available champion.
6. Scope fits 3–4 week pilot timeframe.
7. Technical independence (decoupled from legacy).
8. Marketing potential (will it excite others).

Then prioritize. The output is *which teams to partner with first* — not which components to build.

**Mall's "rule of three" (Activity #26):** "If three or more teams need this component right now, it goes in the design system." Adapted from Goldfinger: *"Once is happenstance, twice is coincidence, three times a pattern."*

### Design System Canvas (Paavan, 2022) — the 10 boxes

A one-page workshop tool (Lean Canvas analog). Walk a stakeholder group through:
1. **Problem** — what problems do you face with current bespoke approach?
2. **Existing Assets** — component libs, style guides, marketing assets that could fold in?
3. **Maturity Level** — 0–4 (see ladder above).
4. **New Resources** (4a assets, 4b processes) — what's needed to move up one level?
5. **Affected Products** — which products tangibly benefit?
6. **Consumers** — who uses the system?
7a. **Maintainers** — who maintains it? 7b. **Champions** — who evangelizes?
8. **Scope** — what's feasible and realistic?
9. **Adoption Strategy** — what needs to happen for consumers to adopt? Who owns that?
10. **Costs** — team capacity, time, money.

Best used: as an output of a 60-90 minute kickoff with a sponsor and a few key stakeholders — not as an internal team artifact.

---

## Where external thinking has evolved (2017 → 2020 → 2023)

| Dimension | 2017 (UXPin Actionable) | 2020 (InVision MVP/Benchmark) | 2023 (Mall 90 Days) |
|---|---|---|---|
| **Primary framing** | Inventory → kill inconsistency | Hierarchy of needs; people are 2/3 | Practice (habit), not project |
| **Adoption model** | Communicate decisions to company | Executive coalition + dev fanbase | Influence map + pilot scoring |
| **First sprints** | Color, type, icons, space, first pattern | Borrow a starter collection, ship MVP | Hot-Potato component pilot with a real team |
| **Definition of "system"** | Patterns + decisions + principles | Foundations + Components × Design + Engineering × Guidelines + Governance | Same 3-part definition, plus stages: tool / product / practice |
| **Tooling assumed** | Sass/LESS, Sketch, UXPin | DSM, Storybook, Sketch | Figma, Storybook, Github, Loom |
| **Team size** | Build inventory solo OK; small multidisciplinary team | 1–3 executive sponsors, lightweight | 3–8 dedicated, 20–30 hrs/week |
| **Risk model** | Risk = inconsistency cost | Risk = skipping discovery | Risk = adoption (people don't use it) |
| **Principles** | Drafted up-front to align team | Drafted from research with users | Extracted *retrospectively* from real decisions |

**Net shift:** earlier writing assumed the hard part was *making* the system; later writing assumes the hard part is *getting people to use it*. By 2023 Mall is essentially writing a change-management playbook with a design system as the medium.

---

## Where external sources conflict with each other

1. **When to write principles.** UXPin (2017) and InVision Handbook (2018) advise drafting principles up-front to align the team. Mall (2023) explicitly inverts this — principles emerge retrospectively from the decisions you actually made on the first pilot, because principles invented in a vacuum tend to be aspirational and unused. *Resolution: do both — draft a working set early, treat them as hypotheses, and rewrite them after the first real pilot.*
2. **Solo or team-only?** UXPin (2017): "It takes one committed person to kick off the process." Mall (2023): "If you're a freelancer or a lone designer/engineer/product person, don't be surprised if what you find here feels a bit too overwhelming." *Resolution: solo can run the inventory and the buy-in narrative; the system itself needs a multidisciplinary team to ship.*
3. **Build top-down or bottom-up?** InVision MVP (2020) Tessa Rodes: groundswell stalls without top-down directive. Mall (2023) and Treder (2017): start scrappy, prove it on a pilot, expand. *Resolution: start bottom-up to generate evidence; convert to a top-down mandate at the buy-in moment using that evidence.*
4. **Should you "borrow" from open source?** InVision MVP (2020) actively recommends starting from Material. Mall (2023) and InVision Handbook (2018) are skeptical — generic systems carry generic decisions that may misrepresent the brand. *Resolution: borrow patterns and structure (atomic decomposition, naming, token shapes); don't borrow style.*
5. **Pilot scoring vs. canvas.** Mall's 8-factor pilot scorecard is empirical and quantitative. The Paavan Canvas is qualitative, single-meeting, broad-stroke. *Resolution: Canvas for sponsor alignment, Scorecard for team selection.*
6. **Components: collect or curate?** UXPin (2017) says inventory everything then standardize. Mall (2023) Activity #5 + #10 says collect existing patterns *and* aspirational ones in parallel — the future system isn't in your code today. InVision MVP (2020) says start from your most polished product (curate over collect).

---

## Notable quotes (with source + year)

- "A design system is a process and therefore is simultaneously always ready and never done." — Treder, UXPin, 2017.
- "Design system not used by the product team is dead and useless." — Treder, UXPin, 2017.
- "A design system is a collection of reusable components, guided by clear standards, that can be assembled together to build any number of applications." — Suarez, InVision Handbook, 2018.
- "Standards govern the purpose, style, and usage of these components. Together, you equip your product team with a system that is easy to use, and you give them an understanding that clearly links the what with the why." — InVision Handbook, 2018.
- "Principles are important for design systems primarily for describing how it was created, and how the makers of it would intend it to be used." — Rich Fulcher, Google (in InVision Handbook, 2018).
- "Design principles act as a reusable standard for designers to measure their work. They replace subjective ideals with a shared understanding of what design must do for users. Just as guardrails keep you safe and on the road, design principles keep teams on the path to achieving their vision." — Suarez et al., InVision, 2018.
- "A design system is a product so staff it like a product instead of a project; you want people committed to maintaining and evolving it." — InVision Handbook, 2018.
- "A collection is only one third of a design system… People bring it to life." — InVision MVP, 2020.
- "Save a designer one hour of work, and you've done well. Save 100 developers one hour of work, and you've done miracles." — InVision MVP, 2020.
- "Groundswell efforts can get you halfway there, but it's hard to reach true consistency without a clear directive from the top." — Tessa Rodes (IBM Cloud), in InVision MVP, 2020.
- "Talking to devs on their turf helps you avoid looking like the designer coming down from an ivory tower to hand them a thing they don't want." — Scott Arnold (Motorola Solutions), in InVision MVP, 2020.
- "Too often, teams put months or years of work into their design system, 'launch' it, and then wonder why no one uses it. If they skip steps (e.g. try to scale a system without first doing the necessary discovery work and audits), then the design system won't gain traction and will ultimately fail." — InVision Benchmarking, 2020.
- "Making the design system isn't the hardest part: getting people to use it is." — Mall, 90 Days, 2023.
- "If three or more teams need this component right now, it goes in the design system." — Mall, 90 Days, 2023.
- "A leaf blower is a tool, but the Toro PowerJet F700 is a product. Naming something elevates it." — Mall, 90 Days, 2023.
- "Once is happenstance, twice is coincidence, three times a pattern." — adapted from Ian Fleming's *Goldfinger*, in Mall, 90 Days, 2023.
- "These barriers are normal. Start anyway." — InVision MVP, 2020.

---

## Topics for the gaps file

These external sources surface concerns that VML internal practice docs *might* not address (worth checking against `notes-internal-strategy-and-scoping.md`):

1. **The Influence Map as a distinct artifact from the org chart.** Mall treats stakeholder-relationship dynamics (green/yellow/red, thick/thin arrows) as a deliverable. Most internal strategy decks default to org-chart thinking.
2. **Practice Pilot before real pilot** — running a fake pilot on a third-party DS (Material) to rehearse the workflows. Cheap; almost never done.
3. **Glossary as an alignment activity** — Mall's Activity #25. Internal docs often have glossaries-as-appendix; this treats glossary as a *negotiation* between disciplines.
4. **Retrospective extraction of principles** rather than upfront declaration. Likely to challenge any internal POV that wants principles written in the proposal.
5. **MVP as a 3-part scope (collection + user base + contribution plan)**, not a 1-part scope (collection). Most consultancy proposals scope only the collection.
6. **"Borrow, don't build"** as a starting heuristic — likely uncomfortable for a consultancy whose value is making custom things, but honest about how the best clients actually start.
7. **Developer-first user research.** Most VML proposals likely position designers and brand as the primary audience. The MVP guide flips that: developers are the leverage point because they're more numerous, more expensive, and more underserved.
8. **Weekly stakeholder update cadence** with a fixed template. A communication ritual, not a deliverable.
9. **The "Hot Potato" handoff process** (Mall, Activities #21, #34, #36) — designers and engineers iterate in tight loops on the same component, rather than throwing over the wall. Worth seeing if VML has an analog.
10. **Maturity benchmarking as a sales / consulting hook.** InVision's 5-level ladder and Paavan's 0–4 scale are excellent diagnostic tools for the first executive meeting; a consultancy could productize a "where are you?" workshop.
11. **Naming and logo work as an explicit phase** (Mall, Activities #43–49). The system needs to *feel* like a product with an identity to be adopted — branding is part of the methodology, not vanity.
12. **Office Hours and Systems Week** as adoption rituals (Mall, Activities #45, #48). Sustained habit-building, not one-time launch.
13. **Stakeholder interviews not about the design system.** Mall's explicit guidance: ask leaders about the *org's* future, not the system, so the system can be positioned afterward. Most discovery scripts get this backwards.
14. **The "magic wand" and "fast forward / sink the ship" questions** as standard discovery prompts.
15. **Ecosystem/architecture diagram of all tools-and-acronyms** as a Discovery deliverable (90 Days Activity #11). Forces clarity on where the DS actually fits — CMS, CRM, DAM, build pipelines.
16. **ROI is anecdotal across the entire corpus.** A defensible ROI calculator (perhaps based on Sparkbox's methodology) is a genuine gap the VML POV could fill.
17. **The "imposter syndrome" framing** (InVision Benchmarking) — even Optimized teams feel behind. Useful for setting client expectations honestly.

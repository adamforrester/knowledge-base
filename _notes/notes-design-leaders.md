# Notes: Design Leaders ebook (Apr 2025)

## Source meta
- **Title:** *The design leader's guide to redefining handoff*
- **Publisher:** Figma (figma.com/reports)
- **Length:** 24 pages / ~821 lines of extracted text
- **Date:** April 2025
- **Authorship:** Figma editorial, drawing on interviews with leaders and practitioners at Linear, Duolingo, GitHub, ServiceNow, Crunchyroll, Spotify, Razorpay, Peloton, and Figma itself.
- **Format:** Three-chapter ebook framed as guidance for design leaders, anchored by survey statistics and pull-quotes from named leaders.
- **Summary:** Argues that "handoff" is the wrong mental model for modern, iterative product development. Reframes the design-development relationship as a continuous collaboration that leaders must actively shape through team structure, incentives, communication norms, and explicit defaults. While the ebook's surface topic is handoff, the underlying argument is fundamentally about *organizational design*: how leaders set up incentives, rituals, and culture so that craft can compound rather than decay.

## Thesis / overall framing
The ebook's core claim: handoff problems are *structural problems*, not interpersonal ones. Misalignment between designers and developers reflects misaligned incentives that "go all the way up to the top" (Hugo Raymond, Figma). Therefore the fix is not better Figma file hygiene — it's leadership work: aligning incentives, restructuring proximity (sit them together, design reviews, shift left), and articulating non-negotiables and quality bars.

Three chapters frame the leadership intervention:
1. **Unlock collaboration with curiosity** — change the mindset (me vs. we; assume best intent; cross-discipline literacy without forcing designers to code).
2. **Communicate early and often** — restructure when developers enter the process (GitHub's "shift left" doctrine; pair designing).
3. **Choose your defaults** — leaders must take an explicit position on scope alignment, when to break vs. reuse system patterns, "pencils down" criteria, and team-level non-negotiables.

The closing reframe (Amy Lokey, ServiceNow): *"Maybe we have to reframe handoff as no longer being a handoff. We are working together until this thing gets to a level of completeness and quality that we feel it's ready to ship."*

## Key extractions

### The numbers (useful for executive narrative)
- **80%** of developers think their business would benefit from designers and developers working more closely together.
- **92%** of designers and **91%** of developers say there's room for improvement in handoff.
- **55%** of developers think improving the design-dev relationship would yield faster time to market.
- **55%** of front-end developers want to be brought into the design process earlier.
- **49%** of developers cite differences in priorities/motivations as a top challenge.
- **47%** of developers cite designers' lack of understanding of the development process.

### Structural / leadership diagnoses
- Misalignment is structural, not personal. "The teams struggling for greater alignment — that's usually a structural problem based on the incentives that go all the way up to the top." (Hugo Raymond)
- Engineers are incentivized to grow JavaScript depth over CSS; what designers care about is rarely what developers are evaluated on, unless they sit in front-end specialist roles (which are rare).
- Design debt, technical debt, and product debt are not weighed equally in most orgs — leadership has not had the conversation. This is the gating problem behind most collaboration friction.
- "Companies that are well known for their craft tend to shine from both an engineering and design standpoint." (Roshan Bhalla) — Craft is a *paired* output, not a design-only output.

### Mindset shift: "me vs. we"
- Lauren Byrne: replace "me vs. we" with shared problem space. Without it, teams over-negotiate ("argue for 120% so you can back down to 100%").
- Jake Albaugh: "We start with 'How far do I need to pitch?' so that we work back to 'What am I going for?'" — a symptom of broken trust.
- Noga Mann: "It's not about pushing back — it's bringing things up for discussion."
- "You can't manufacture trust, but you can assume best intent."

### Cross-discipline literacy (without forced coding)
- Designers don't need to code; they need to understand how design choices impact engineering effort. (Aleksander Djordjevic, Spotify)
- Tactical: designers shadow developers during QA bug-fixing; designers review PRs; developers join design discussions and even do "design riffs."
- Noga Mann: "We're really trying to encourage people not to read too much into their role definition, and that it's okay to cross those boundaries."

### Shift left (GitHub)
- GitHub formalizes the doctrine that engineers should enter the product development process *during ideation*, not at handoff.
- Mechanism: design reviews where developers are tagged into design discussions almost daily.
- Result (Reza Rahman): "We don't really have a single handoff anymore — we have a continuous collaboration."

### Context as the unit of efficiency
- Sharing intent early lets developers independently make trade-offs. Roshan Bhalla: "Even if we're missing pieces during implementation, we have enough context to make trade-offs independently."
- Example: a designer explaining *why* they want toggle functionality lets a developer suggest a dropdown alternative without round-tripping — saves days.

### Non-negotiables
- Designers must explicitly articulate which elements are non-negotiable and why. Pair an "ideal" version with a "realistic" version to surface the trade-off space.
- When too many things are non-negotiable, ask "Where else can I take from?" rather than weakening any single element.

### Defaults a leader must set (Chapter 3)
1. **How to align on scope** — one-way vs. two-way door framework; cross-functional tiebreakers (PM, PMM); "above the line" vs. "below the line" with fast-follow.
2. **When to make or break patterns** — map design and code libraries to each other; joint reviews; intentional, documented departures from the system.
3. **What "pencils down" means** — joint dev+design approval; criteria for post-dev changes; sync vs. async (formal handoff meeting vs. "Ready for Dev" status).
4. **Which beliefs are strongly held** — team-level principles (GitHub's shift-left; Duolingo's company handbook; ServiceNow's GenAI evolution).

### Duolingo case study (operational details worth stealing)
- Prototype early and dogfood with the engineering team.
- Shared visual language: brand colors named after animals ("Oh, this is eel"), so Figma label maps directly to the code token. Reduces translation friction.
- Treat releases as "v1" — frees the team from launch perfectionism. "Cut corners on the scope of the feature, but never the polish or the fun."

### GenAI-era handoff (Amy Lokey, ServiceNow)
- Linear handoff fails because of "organic unpredictability" of LLM outputs — must see live in production.
- Implications: ensure devs understand design intent at the interaction level; pair design; embrace fluid, evolving designs.

## Phase-tagged findings (canonical 8 phases)

- **Discovery & Strategy** — The ebook's strongest material is here. Position the design system / collaboration work to executives as a *structural incentives problem*, not a tooling problem. The conversation about design debt vs. tech debt vs. product debt being weighted unequally is a leadership-level discovery question. Survey stats (80% / 92% / 91% / 55%) are ready-made for executive decks. Frame collaboration ROI as: higher quality products + faster time to market + improved organizational culture.

- **Design Foundations** — Naming conventions matter operationally: Duolingo's animal-named brand colors collapse the design-to-code translation step. Foundations should be designed for *bidirectional readability* between Figma and code.

- **Component Library** — "Map design and code libraries to each other to avoid hidden costs and reduce redundant work." Joint design+dev reviews drive visibility into what already exists. The decision rule for reuse vs. new pattern is a leadership artifact, not a designer judgment call.

- **Documentation** — Dev Mode annotations replace handoff meetings (Oliver Dumoulin, Peloton: "Before Figma, we needed extra meetings for handoff... Now, we handle much of that asynchronously through Dev Mode."). Designer prototypes/videos document *intent* for components that don't yet exist in the system.

- **Development Support** — Compare-changes and version history give devs transparency on file churn (Saurav Rastogi, Razorpay) and let them "freeze" a file to scope work. "Ready for Dev" status as an asynchronous handoff bridge. Pair designing where feasible.

- **Pilot & Implementation** — Duolingo Math as a pilot model: nascent product, fluid process, prototype-first, dogfood internally, ship simple v1s to test market resonance, iterate. The pilot's job is to prove the collaborative motion, not the feature.

- **Governance & Adoption** — Team structure is the lever: "A lot of it is down to how you structure your teams — bringing designers operationally closer to engineers and having those conversations regularly." (Reza Rahman) Design reviews as the recurring governance ritual. Joint approval for "Ready for Dev" is a governance gate. Be intentional and documented when bypassing system patterns.

- **Ongoing Maintenance** — Karri Saarinen (Linear CEO): "We push direct responsibility onto the team, giving them the freedom to make decisions, while setting a standard for them to meet." Leadership sets the bar, not the tactics. Operationalize values via artifacts (Duolingo's company handbook). Iterate principles as tools change (ServiceNow updating its process for GenAI). The "v1" framing for shipped features keeps maintenance and iteration emotionally on equal footing with launch.

## Selling design systems content (cross-cutting)

This is the strongest extractable material for the *selling* theme.

**Reframe the problem upward.** The most quotable insight for an exec audience: collaboration friction is a *structural incentives* problem visible all the way to the C-suite. If a design leader is asking executives to fund a system, the parallel argument is: *we are not currently weighing design debt, tech debt, and product debt equally, and that imbalance is what's preventing collaboration from compounding into craft*.

**Use the survey stats as opening evidence.** "80% of developers think their business would benefit from working more closely with designers" is a stronger executive opener than any internal anecdote. Pair with "92% of designers and 91% of developers see room for improvement" — near-universal agreement collapses the "is this a real problem?" debate.

**ROI framing.** Three benefit categories the ebook puts in an exec-friendly order: (1) higher quality products, (2) faster time to market (55% of devs say improving the relationship would deliver this), (3) improved organizational culture. Avoid leading with culture — lead with quality and speed, treat culture as the compounding effect.

**Cost framing.** Colleen MacDonald (Duolingo): "It's expensive to build something, so you want to build it right." Design and tech debt accrue subtly — "a few pixels off here, inconsistent spacing there" — and erode morale. A single sentence executives understand.

**Structural asks to make of leadership.**
- Align design debt, tech debt, and product debt as equal-weight conversations.
- Restructure team proximity (sit designers near engineers; recurring design reviews with engineers tagged in).
- Adopt a shift-left doctrine: engineers participate during ideation.
- Set explicit defaults at the leadership level for scope, pattern reuse, "pencils down," and quality bar.

**The "no handoff" reframe** is itself a sales tactic. Naming the old model ("handoff") as obsolete and offering "continuous collaboration" as the new model gives executives a clean before/after narrative.

**What this ebook is *not*.** It is not a financial ROI playbook. There are no dollar figures, no productivity benchmarks, no maturity model. Its sale is a leadership-philosophy sale, not a budget sale. Pair with sources that quantify ROI when building an executive deck.

## Notable verbatim quotes

- "The teams struggling for greater alignment — that's usually a structural problem based on the incentives that go all the way up to the top." — Hugo Raymond, Designer Advocate, Figma
- "There's a whole conversation still to be had about design debt, technical debt, and product debt." — Hugo Raymond
- "Maybe we have to reframe handoff as no longer being a handoff. We are working together until this thing gets to a level of completeness and quality that we feel it's ready to ship." — Amy Lokey, CXO, ServiceNow
- "We don't really have a single handoff anymore — we have a continuous collaboration." — Reza Rahman, Senior Staff Engineer, GitHub
- "It's more about competencies than roles. You're trying to find ways to inspire curiosity in each other's discipline." — Hugo Raymond
- "What you end up doing is arguing for 120% so that you can hopefully back down to 100%, instead of just being like, 'What is 100% for us together?'" — Jake Albaugh, Developer Advocate, Figma
- "It's not about pushing back — it's bringing things up for discussion." — Noga Mann, Engineering Manager, Figma
- "We push direct responsibility onto the team, giving them the freedom to make decisions, while setting a standard for them to meet." — Karri Saarinen, CEO, Linear
- "Even if we're missing pieces during implementation, we have enough context to make trade-offs independently." — Meaza Abate, Engineering Manager, Figma
- "It's expensive to build something, so you want to build it right." — Colleen MacDonald, Product Designer, Duolingo
- "Companies that are well known for their craft tend to shine from both an engineering and design standpoint." — Roshan Bhalla, Software Engineer, Figma
- "We tend to cut corners on the scope of the feature, but never the polish or the fun." — Colleen MacDonald, Duolingo
- "Communication is always the big part — getting people on the same page about what we are trying to do, and how we are going to do it." — Jori Lallo, Co-founder, Linear
- "Before Figma, we needed extra meetings for handoff and collaborative discussions about interaction states and component behaviors. Now, we handle much of that asynchronously through Dev Mode." — Oliver Dumoulin, Staff Design Systems Engineer, Peloton

## Topics for the gaps file

- **Quantified ROI** — The ebook leans entirely on survey percentages and qualitative quotes. No dollar values, no time-saved benchmarks, no maturity-stage cost curves. Need a complementary source for hard ROI numbers when selling DS work.
- **Org-design specifics** — Asserts "structural incentive problem" but doesn't prescribe org models (centralized, federated, hub-and-spoke). Need a source on DS team topologies and reporting lines.
- **How to actually run the design-debt vs. tech-debt vs. product-debt conversation** — Hugo Raymond names this as the gating leadership conversation but the ebook does not script it. Worth developing a meeting-agenda or framework artifact.
- **Pattern-break governance mechanics** — The ebook says "be intentional when bypassing established patterns — share reasoning and acknowledge the departure." Doesn't specify the artifact (RFC? exception log? variant proposal?). Gap: a documented exception/contribution flow.
- **Shift-left implementation cost** — GitHub says engineers are tagged into design discussions "almost daily." This implies real engineering capacity. No discussion of how to fund that time, who pays for it, or how to measure whether the investment is paying off.
- **Pair designing operating model** — Mentioned several times as ideal but no guidance on cadence, when it's worth the cost, or how to scale it beyond the small-team case (Duolingo Math).
- **Quality-bar articulation** — Linear and Duolingo both reference a "standard" or "quality bar" but neither is described in operational terms. Gap: how does a leader actually write down and socialize a quality bar?
- **Executive narrative templates** — The ebook gives raw materials (stats, quotes, reframes) but no pre-built deck structure for taking these to a CFO/COO. Worth synthesizing.
- **Measurement** — No KPIs proposed for "continuous collaboration." How would a leader know it's working beyond vibes? Gap.
- **GenAI handoff specifics** — Amy Lokey flags GenAI as breaking linear handoff but the ebook only sketches the implication. Deeper source needed on what design systems for GenAI-driven products look like.

You are researching design-system teams as a discipline — hiring,
team-building, internal rituals, career paths, distributed-team
patterns, the agency-to-client handoff, and burnout — for a senior
design systems practitioner leading the practice at a global creative
agency. The output is a structured knowledge document that will be
promoted to a numbered file in the practitioner's vault
(`00e-team-and-discipline.md`), positioned as a cross-cutting
foundation alongside 00 Principles, 00b Agency Context, and 00d
Commercial Model.

The practice's existing team-structure content is split across two
files. `00d-commercial-model.md` covers roles, hours, minimum-viable-
team shapes, and the CareCentrix engagement reference. `07-governance-
and-adoption.md` covers governance models, the Curtis 1:2 ratio, lead-
role definitions, contribution models, communities of practice, and
external comms structure. That split is governance-leaning. The
*team-as-discipline* layer — what a DS practitioner *is*, how the
discipline grows from one person into a core team, what the work
actually feels like day-to-day, how the team survives the engagement
ending, where careers go — is currently underdeveloped. Most
DS-team literature is in-house-product-shaped (Spotify, Atlassian,
Shopify, Airbnb, GitHub Primer, IBM Carbon, Adobe Spectrum, Microsoft
Fluent). The agency reality is structurally different: teams ramp up
for an engagement, hand off, and disband; the practice is a portfolio
of engagements, not a single product; the people doing the work bill
hours; the client may be the team in a year. This research must
account for those structural differences, not assume the in-house
patterns generalise.

This is not an introductory guide — assume the reader is the practice
lead, has read the existing 00d and 07 material, knows the field's
team models (Solitary / Centralized / Federated / Cyclical from Nathan
Curtis's *Team Models for Scaling a Design System*; Bjarte Karlsen's
roles canon; Brad Frost's *Atomic Design* team chapter; the
Design-Systems-Handbook treatment from InVision), knows the Curtis
1:2 ratio, and is fluent in the standard role vocabulary (DS lead, DS
designer, DS engineer, design technologist, design ops, DS product
manager, technical writer, accessibility specialist). Don't explain
what a community of practice is, what a hub-and-spoke model is, what a
"contribution model" is, what governance is — explain the *agency-side
applications* of those concepts, where the in-house playbook fails to
generalise to agency engagements, what the senior agency practitioner
actually has to figure out that the in-house literature doesn't
address, and what tools and patterns work at agency scale.

Research scope — cover all of the following:

1. Why a DS team is a discipline of its own, and why the agency
   context changes the answer

- The case that "DS team" is a stable, named discipline rather than a
  staffing arrangement assembled per engagement. What makes someone a
  DS practitioner vs. a generalist designer or engineer who happens
  to be on a system project. The discipline's tacit-knowledge surface:
  understanding tokens-as-architecture, components-as-contract,
  governance-as-protocol, AT-as-stakeholder, the field's vocabulary
  and lineage. The discipline's identity formation: where DS
  practitioners come from (most commonly product-design or front-end-
  engineering backgrounds with a few years of system work), how they
  develop the lens, what distinguishes a senior DS lead from a senior
  product designer who has touched system work.
- Why the agency context changes the team-building answer materially.
  In-house teams persist; agency teams ramp up and disband. In-house
  teams have a single product to serve; agency teams serve a portfolio
  of clients in different industries on different platforms with
  different commercial shapes. In-house teams are budgeted on
  headcount; agency teams are budgeted on hours and SOWs. The
  dominant DS-team literature (Curtis, Brad Frost, Spotify,
  Atlassian, Shopify, Airbnb, IBM, Adobe) is in-house product
  literature; the agency-side gap is real and growing.
- What the agency reality actually demands: people who can stand up a
  DS practice from cold inside three weeks, who can leave behind a
  client team capable of running it, who can move to the next
  engagement without the system rotting. People who have a
  cross-engagement view of the field that no in-house practitioner
  develops. People who can translate practice-IP across radically
  different client contexts (a fintech with strict regulatory
  constraints, a CPG brand with seasonal campaign surges, a B2B SaaS
  in a portfolio acquisition). Why this is harder to build a team
  for than the in-house version, and why the practice's compounding
  asset is the team itself, not the artefacts the team produces.

2. Hiring and skill mix — building the agency-side DS team

- What makes a strong DS designer vs. a strong product designer. The
  literacy differences (token systems, component anatomy, theming
  architecture, accessibility patterns, governance, motion as
  foundation, color science to a useful depth, type at system scale).
  The mindset differences (designing for consumers, not for users
  directly; designing for resilience and reuse, not for a single
  surface; designing for a roadmap, not for a sprint). The portfolio
  signals (case studies showing system thinking, not pretty UI;
  evidence of engineering empathy and code literacy; evidence of
  having shipped something that *survived* its first year).
- The design technologist as a specific archetype. The role's
  composition (high design literacy + high engineering literacy + the
  bridging instinct), where it sits in the team (typically reporting
  through design but with embedded relationships in engineering), why
  it's the highest-leverage hire on a DS team and the hardest to find.
  The cohort: design technologists rarely come from CS programs or
  design programs — they're typically self-taught hybrids who landed
  here. What signals the design technologist tier (built or maintained
  a system, understands token pipelines, can debug a CI failure,
  speaks Figma plugin development or MCP-server architecture).
- What the DS lead actually owns. The lead is not a senior designer
  or a senior engineer — the lead is the practice's commercial-and-
  craft hybrid. What the lead spends time on across a typical week
  (engagement scoping and pitching, team coaching, governance
  decisions on contested work, executive coalition-building at the
  client, hiring, mentorship, the occasional deep dive). What the
  lead's deliverables are (engagement architecture, team allocation,
  governance frameworks, the practice's external POV). Why the lead
  almost never reports through a single discipline (design, engineering,
  product) and what reporting structure works in agency settings.
- The "T-shape" expected of a DS engineer. Strong on a primary
  framework (typically React + the broader web stack, or one of the
  major mobile platforms), reasonably literate across the
  cross-platform surface (the other web frameworks, native iOS,
  Android, RN, Flutter at sufficient depth to make architecture
  decisions), and deep on the system-specific tooling (Storybook,
  Style Dictionary, Tokens Studio, the build pipeline, the CI surface,
  the docs platform, the AI/MCP layer). The engineer's literacy on
  design tooling matters too (Figma at depth, Code Connect, Variables,
  Dev Mode). What the practice should look for in a portfolio (not
  general full-stack work; specifically library-and-tooling work).
- The supporting roles and when each is justified. Design ops (when
  the engagement size justifies a dedicated coordination role —
  typically past 8–10 people on the practice). Technical writer or UX
  copywriter (75-hour minimum scope per the practice's commercial
  model, but rarely justified at smaller engagements; ranges in size
  by content surface complexity). Accessibility specialist (rarely a
  full-time role at agency scale; typically a literacy that the
  whole team holds with one or two people having deeper depth).
  Product manager for the system (rare in agency engagements; usually
  the DS lead carries the PM function). The shape: small core team
  with deep generalists, augmented with specialists as the surface
  demands.

3. The Part Timer → Allocated Individual → Dedicated Team arc

- The arc as it appears in 07: stages are *named* but not
  *operationalised*. The agency-side practitioner has to make
  stage-transition calls without a clear playbook. This section names
  the stages, the signals that mark a stage transition, the
  characteristic problems at each stage, and the patterns that work.
- **Stage 0 — No DS practitioner.** What the engagement looks like
  before the practice is involved. Typical signals: design debt
  visible in the product, designers building components that don't
  ship, engineering reinventing primitives per feature, the existence
  of a "design system" channel in Slack with no maintainer. The
  intervention pattern: a Discovery engagement with the practice
  (1–4 weeks), Six Signs framing, maturity diagnostic, audit, the
  initial commercial pitch.
- **Stage 1 — Part Timer.** A single DS practitioner working part-time
  inside the engagement (typically 20–40% allocation). What the part-
  timer can and cannot do. What signals the engagement needs more
  (typically: ticket queue growing faster than the part-timer can
  drain it, governance decisions piling up, the part-timer's other
  engagement consuming the time). The trap: a part-timer treated as
  a full-time DS lead. The escalation pattern: ramp to allocated.
- **Stage 2 — Allocated Individual.** A single DS practitioner
  working full-time on the engagement. The dominant agency stage —
  most engagements live here for months or longer. What the allocated
  individual covers (the Six Signs full set; foundations, components,
  governance, dev support, documentation; the de-facto DS lead for
  the client). What they cannot cover (sustained two-platform delivery,
  enterprise-scale governance, multi-brand work). The risks (the
  individual becomes the system; the system fails to outlast them;
  burnout). The escalation signals (multi-brand demand, multi-
  platform demand, enterprise governance demand, retention risk,
  client team starting to participate).
- **Stage 3 — Dedicated Team.** A small team (typically 3–6 people)
  working sustained on the engagement. The shape that produces
  Curtis-1:2-ratio-supportable systems. The typical mix (DS lead
  + DS designer + 1–2 DS engineers + design technologist; design ops
  if 8+ people on the broader practice; specialist scope as needed).
  What changes at this stage (the practice is no longer person-bound;
  the system can outlast individual departures; governance becomes a
  team practice). The new risks (coordination overhead, team-internal
  disagreements becoming engagement risk, the lead becoming a manager
  instead of a craftsperson).
- **Stage 4 — Embedded Multi-Team.** Past three teams, the practice
  pattern shifts again. Embedded DS practitioners across product
  teams; a coordinating central group; the federated model. The
  agency variant: a core practice team plus per-product-team
  embeds. Rare in agency engagements — most engagements don't reach
  this scale; when they do, the practice's role is typically to
  stand the model up and hand it off to client leadership.
- The signals practitioners look for to escalate, and the signals
  that distinguish a real escalation from a tactical surge. The
  failure mode: stages get added when the work scales, but the
  *people doing the work* don't get up-skilled or replaced. The
  practice's leverage: anticipating the next stage and pitching it
  before the current stage breaks.

4. The agency-to-client team handoff — the practice's constant problem

- The handoff is the practice's hardest single problem. The agency
  ramps up a DS team, runs the engagement, ships a maintainable
  system, leaves a maintainable team behind. The "leaves a
  maintainable team behind" half is where engagements most commonly
  fail; the system reverts to drift within a year of agency departure
  because the client has the artefact but not the discipline.
- What the handoff actually consists of:

  - **The client team's identity.** Who the client's DS practitioners
    are (titles, reporting line, allocation, peer support). The
    handoff fails when the client team is not formed before the
    agency departs; the agency's reflexive fix (compress the handoff
    into the last six weeks) almost always fails. The pattern that
    works: client-team-formation begins on day one of the engagement
    and is the second deliverable after Discovery.
  - **The discipline transfer.** The agency team coaches the client
    team in DS thinking (tokens-as-architecture, governance as
    practice, RACI in contribution, the failure modes the agency
    has lived through). Coaching is not training. The practice's
    pattern: shadowing first, paired contribution second, client-led
    contribution third with agency review, then independence with
    agency consultation as a retainer.
  - **The artefact transfer.** The system itself, the documentation,
    the build pipeline, the governance bodies, the contribution
    process, the comms channels. Already covered in 04, 05, 07; here
    only insofar as it interacts with the team transfer.
  - **The relationship transfer.** The agency team has spent months
    building executive coalition at the client; the client DS team
    has to inherit that coalition, not rebuild it. The pattern: joint
    executive presentations through the engagement, with the agency
    lead introducing the client lead as the long-term owner; explicit
    coalition-passing in the last quarter; named executive sponsors
    paired with client leads.

- The financial shape of a successful handoff. The practice retains a
  retainer relationship (08-ongoing-maintenance), not a hands-on team
  presence. The retainer pays for governance review, escalation
  consultation, and the next-engagement scoping. The handoff is not a
  commercial loss — it's a transition from project revenue to
  retainer revenue, and the retainer compounds across years if the
  client team thrives.
- The failure modes:

  - **The "we'll just stay another quarter" pattern.** The client
    team isn't ready, the agency stays. The agency's incentive
    (continued engagement revenue) and the client's incentive
    (continued comfort with the system being someone else's problem)
    both work against the handoff. Senior practitioners have to push
    back against both their own commercial instinct and the client's
    request to stay.
  - **The "agency owns the artefacts, client owns the operations"
    pattern.** A bizarre but real failure mode where the agency
    treats the system as IP and refuses to fully transfer it. The
    practice's discipline: the client owns the system from day one.
    The agency's IP is the practice's *method*, not any client's
    instance.
  - **The "no client team" pattern.** The client never staffed up
    because the agency was doing the work. The handoff date arrives
    and the system has nowhere to go; the engagement extends on
    emergency staffing, drifts, or the system rots. The agency's
    discipline: the engagement scope explicitly includes client-
    team formation, and the lack of staffing is a deliverable
    blocker.

5. Internal team rituals — the daily and weekly cadence of a working
   DS team

- DS-internal rituals are distinct from external governance comms
  (which 07 covers). External comms is *how the system communicates
  with consumers*. Internal rituals are *how the team coordinates
  internally to do the work*.
- The daily pattern that works at agency scale. Asynchronous standups
  via Slack thread first thing in the day (timezone-friendly,
  artefact-leaving). The 30-minute "live design review" or
  "live engineering review" twice a week where the team workshops
  in-progress work together — not for status, for craft. The lead's
  open-office hours (typically 1–2 hours, twice a week) for ad-hoc
  questions from the broader practice. The "system sync" weekly with
  client design and engineering leads (typically 30–45 minutes,
  agenda-light, blocker-and-decision-led).
- The weekly pattern. The team retro (60–90 minutes, the only meeting
  with no client present, the place where craft conversations happen
  without performance pressure). The component review (where contributed
  work is critiqued before it lands in the system; typically Tuesdays).
  The roadmap session (where the next 4–6 weeks of work are sequenced
  with the client). The "architecture office hours" (the lead's
  longer-form thinking time, often co-working with one or two
  practitioners on a hard architectural call).
- The monthly pattern. The system's release cycle (typically every
  two weeks at agency engagements; major release every 4–6 weeks).
  The exec readout (where the executive coalition gets its
  refreshed view of progress and risk; typically 30 minutes,
  metrics-led). The "external POV" session (where the team writes
  or refreshes practice-IP — case studies, white papers, conference
  talks).
- Documentation as a ritual, not a phase. Component documentation
  written during contribution, not after. ADRs (Architecture
  Decision Records) for every load-bearing decision (per the
  practice's existing pattern). Release notes generated from PR
  metadata, not hand-authored. Why the discipline of document-as-
  you-go is the discipline that survives the engagement.
- The "team voice" question. How the team writes (PR descriptions,
  Slack threads, ADRs, docs prose) is the team's external face.
  Senior teams develop a recognisable voice over time; the lead's
  job is to coach toward voice without micromanaging. Most agency
  teams have a tonal hole here that surfaces when the team scales —
  three writers' voices on the same docs page is a system smell.

6. Career paths in DS — IC vs. lead, principal track, what comes next

- The DS career path is not yet a settled question — the role is too
  young at agency scale to have a 20-year career arc. What the field
  knows:

  - **DS designer career path.** Junior DS designer → DS designer →
    senior DS designer → principal DS designer / DS lead. The
    branching point at senior: do you go to the IC track (deep
    craft, principal-level systems thinking, occasional consulting,
    architectural-decision authority) or the lead track (engagement
    architecture, team leadership, commercial responsibility, less
    hands-on design). The two tracks pay similarly at senior+; the
    field has not yet articulated the principal IC track as
    cleanly as engineering has.
  - **DS engineer career path.** Junior DS engineer → DS engineer →
    senior DS engineer → principal DS engineer / staff DS engineer.
    The principal IC engineering track is more developed than the
    design equivalent; the field has clearer signals (the engineer
    who owns the build pipeline, the engineer who designs the API
    architecture, the engineer who operates as the team's
    architectural authority).
  - **Design technologist career path.** Less clear. The role is
    typically titled differently per organisation (design engineer,
    UI engineer, design technologist, prototype engineer, design
    technologist) and the senior track is often invented per-
    person rather than described as a path. The field's high-end
    examples (Roman Komarov, Adam Argyle, Sam Cox, Pasquale
    D'Silva, Jhey Tompkins) are individuals more than archetypes.
  - **DS lead career path.** What's beyond DS lead? Practice lead
    (managing multiple DS leads in a global practice). Director of
    DS at the agency level. CTO-adjacent or CDO-adjacent roles
    where DS is one input among many. Founding or co-founding a
    DS-focused agency or product. Returning to in-house product
    leadership as a head of design or VP of engineering with a
    systems lens. The pattern: senior DS practitioners are
    valuable in many roles; the lead-of-leads career is small and
    competitive.

- Where DS people go after DS. The field's outflow is real: senior
  DS practitioners who have done the discipline for 5+ years often
  move on. Common destinations: product leadership at clients
  they've worked with; founding their own DS-focused consultancies;
  in-house DS leadership at product companies; engineering or
  design-engineering roles where systems thinking applies; teaching,
  speaking, writing as primary work. The pattern: the discipline is
  intense; senior practitioners often want to do something different
  after a decade. The agency's discipline: structure the role so
  burnout doesn't drive people out, and structure the practice so
  senior people leaving doesn't crater the practice.
- The compensation question. Agency-side DS people are typically
  paid less than in-house DS people at high-paying tech companies,
  for the same reason agency designers and engineers are paid less:
  agency revenue per head is lower than top-tier product company
  revenue per head. The compensating advantages: variety, breadth,
  the practice's intellectual rhythm, the ability to influence
  multiple companies' DS practices over a career. The retention
  pattern: pay competitively for the agency tier, invest visibly
  in growth (conference attendance, training, principal-track
  development, external speaking opportunities), make the practice
  a place where senior people *want* to stay.

7. Distributed and global team patterns

- The agency reality is global: VML and similar global agencies
  staff DS engagements across time zones (US, EU, Latin America,
  India, the Pacific). What works:

  - **Two-timezone overlap as a minimum.** A DS team needs at least
    a 2–4 hour daily overlap window between its core members for
    real-time coordination. The pattern that fails: 12-hour-offset
    handoff teams with zero overlap; the loop time on hard
    decisions stretches to days. The pattern that works: paired
    timezones (US East + EU West; EU + India; US West + LATAM)
    with a daily synchronous window for the team's hardest work.
  - **Asynchronous as the dominant mode.** Most coordination
    happens in writing — Slack, GitHub, Jira, Linear, Notion,
    Figma comments, ADRs. The synchronous windows are reserved for
    work that genuinely needs synchrony (contested decisions,
    pair-debugging, design crit on novel work). Senior teams
    over-invest in asynchronous writing quality and under-invest
    in meetings; junior teams do the opposite.
  - **Documentation as the team's memory.** The async-dominant
    pattern only works if decisions are captured, not just made.
    ADRs, RFCs, recorded retrospectives, written architecture
    notes. The team's memory is in the writing; meetings that
    don't produce writing have not happened.
  - **The "follow-the-sun" pattern at agency scale.** Rarely works
    for DS work. Follow-the-sun assumes the work is parallelisable
    across timezones (a customer-support ticket queue, a defect
    triage queue). DS work is mostly serial — a component goes
    through design crit, engineering review, accessibility review,
    documentation, and release — with strong sequential
    dependencies. The pattern that emerged in agency practice:
    paired timezones with overlapping core hours, not full follow-
    the-sun.

- Cross-cultural patterns. A team spanning US, EU, India, LATAM has
  cultural differences in directness, hierarchy, conflict, time
  perception, and meeting expectations. The senior practitioner's
  read: don't try to flatten the culture; do build in mechanisms
  that make all voices land. Examples: written-first decisions
  (gives non-native English speakers and non-extroverts time to
  compose), explicit invitations to opinion (some cultures require
  the senior to ask), retros that explicitly surface "what wasn't
  said in this meeting."
- The "always-on senior" trap. Senior practitioners working across
  global teams often default to extending their own day to cover
  every overlap — early morning calls with EU, late evening calls
  with India. The trap is sustainable for a quarter, not a year.
  The discipline: a *senior in each timezone* doing the same role,
  with explicit rotation. The agency's compounding asset is having
  senior people in each region; an agency that has only one
  senior carries the senior into burnout.

8. Team health and the burnout patterns specific to DS work

- DS work has burnout patterns the broader design and engineering
  fields don't fully share. The patterns:

  - **The "everyone's customer" load.** A DS practitioner is the
    customer-facing role for every product team in the
    organisation. The ticket queue is constant; the prioritisation
    is contested every time; the answer is "we'll get to that"
    far more than the practitioner wants. The role's emotional
    surface is wider than a product designer's or product
    engineer's; senior DS practitioners often describe the role
    as being in customer-support mode for years.
  - **The "never finished" load.** A DS practice is never done.
    There is always more to tokenise, more to document, more to
    automate, more to govern. The work is structurally
    incomplete; the practitioner who needs the satisfaction of
    closure burns out faster than the practitioner who is at
    peace with the discipline being a craft, not a project.
  - **The "invisible improvement" load.** The DS team's biggest
    wins are usually invisible — a design system that *prevents*
    a redesign, *avoids* a regression, *short-circuits* a
    feature-flag rollout. The work product is often the absence
    of work; the recognition for this kind of work is structurally
    lower than for visibly-shipped work. Senior practitioners
    learn to advocate for themselves; junior practitioners often
    don't and feel under-valued.
  - **The agency-specific load.** The agency-side DS practitioner
    starts a new engagement every 6–18 months. The relationship-
    building, executive-coalition-forming, audit, foundation-
    laying, governance-establishing work is *repeated* per
    engagement. The compounding learning is real; the compounding
    fatigue is also real. Ten engagements over a decade is ten
    times "stand up the practice from cold," which is more
    exhausting than one engagement that runs for a decade.

- What works to mitigate. Sabbaticals (every 18–24 months, 2–4
  weeks, paid, the agency commits to coverage). The structured
  IC-vs-lead choice (the practice supports both tracks; the
  practitioner who doesn't want to manage doesn't have to). The
  cross-engagement portfolio rhythm (the practitioner doesn't
  always-on the same client; rotates across the practice's
  engagements with explicit transitions). The "external POV"
  ritual (the team writes, speaks, contributes to the field —
  produces work that compounds beyond the engagement and feels
  visibly *theirs*, not the client's). The strong retro discipline
  (what's wearing on the team is named, not endured).
- The signals that a team is in trouble. Pull-request-throughput
  declining without scope changing. Documentation quality
  declining (a leading indicator of fatigue). Team-internal
  conflicts becoming personal. The lead skipping retros to "save
  time." Senior people quietly looking elsewhere. The practice's
  early warning system: monthly 1:1s with the lead, quarterly
  team-pulse surveys, the agency's HR or people-ops surface
  feeding back to the lead.
- The hard call: when to disband. Some engagements should end. The
  client isn't ready for ongoing DS work; the budget has shifted;
  the strategic priority has moved. The discipline that prevents
  burnout: not staffing dying engagements with senior practitioners
  out of inertia. The lead's responsibility: read the engagement's
  health, recommend a wind-down before it becomes a death-march,
  protect the team's energy for the next engagement that deserves
  it.

Output format: Structured markdown. Use section headings that match
the numbered scope above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather
than declaring a winner. Flag where the in-house product literature
fails to generalise to agency engagements, and what the agency
practitioner has to figure out without guidance from the dominant
field references. Where claims depend on current state — practice
patterns at named agencies, named individuals, named conferences,
named tooling — date them and note the verification path. Include a
references section linking to primary sources (Nathan Curtis's
EightShapes writing, especially *Team Models for Scaling a Design
System*; Brad Frost's *Atomic Design* team chapter; the InVision
*Design Systems Handbook*; the *Design Systems Podcast*; conference
talks from Clarity / Config / Smashing / Into Design Systems where
the agency-side DS team is a topic; Sparkbox, Pivotal-now-EPAM,
Thoughtworks, and other agency-DS-practitioner case studies; the
in-house DS team retros that *do* surface relevant patterns —
Spotify, Atlassian, Shopify Polaris, IBM Carbon, Adobe Spectrum,
Material Design — even though the dominant lens is in-house product
work; Dan Mall's writing on team structure and embedded design;
Una Kravets / Jhey Tompkins / Adam Argyle / Sam Cox writing on the
design-technologist role; agency-side practitioner blogs and Medium
posts where they exist).

Depth: Expert audience. Do not explain what a community of practice
is, what hub-and-spoke means, what the Curtis 1:2 ratio is, what
"governance" means, what a contribution model is, what an ADR is —
explain what the agency-side DS practitioner has to do that the
in-house literature doesn't address, where the field's dominant
references break down outside in-house product contexts, what works
at agency scale, and what compounds across an agency-DS career.

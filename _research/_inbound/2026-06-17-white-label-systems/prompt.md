You are researching white-label design systems as an engagement type — the
practitioner-facing discipline of architecting, scoping, and operating a DS
that ships to multiple unknown future brands or that serves as a
foundation-plus-starter for bespoke client work — for a senior design
systems practitioner leading the practice at a global creative agency.
The output is a structured knowledge document that will be promoted to a
numbered file in the practitioner's vault (`33-white-label-systems.md`),
positioned as an extension topic alongside 22 (token architecture
extensions), 24 (tokens at scale), 26/27 (adaptive interfaces), 30
(generated-from-data documentation), 31 (color systems), 32 (auditing
design systems), 34 (MCPs for DS practice).

This run is the *engagement-type* half of the white-label question — the
shaping, scoping, pricing, and operating discipline. The architectural
primitive that white-label-for-resellers depends on (the brand-generation
engine, the OKLCH-derived semantic layer, the Theme Schema as a contract,
the Generative Token pattern at portfolio scale) is substantially closed
by 24-tokens-at-scale (§White-label-and-reseller-scenarios + §The
Generative Token pattern). The internal context for VML's white-label
kit (Prism2 — what it is, what it isn't yet, the technology-team-adoption
gap) is closed by 00b-agency-context (§The white-label kit). The
commercial tension (does Prism2 reduce estimates or raise quality for
the same estimate; current position is "scope at standard hours") is
closed by 00d-commercial-model (§The white-label kit question). What is
*not* closed is the engagement-shaping and operating discipline that sits
above those primitives — when to recommend white-label as a shape; how to
scope it; how to price it; how to operate it; how to staff it; how to
hand it off; and how to resolve the Prism positioning conflict (09 §3.2)
that has been open across the corpus for the full life of this knowledge
base.

The practice has working knowledge here — Prism2 exists and is in active
use as a Figma kit; 24's Generative Token pattern is articulated; the
Multi-Brand Governance source (Apr 2025) gives a process layer; 00b /
00d give the agency context. But the integration is missing. White-label
content is split across 00b (Prism2 as VML's white-label kit), 00d (white-
label kit commercial question), 02 §6 (white-label as Curtis's seventh
theming dimension — "extensive customization at any decision level,
highest cost"), 24 §White-label-and-reseller-scenarios (the unknown-
brand-list architecture problem with brand-generation-engine framing),
and 09 §3.2 (Prism positioning conflict — DS vs. UI Kit). White-label-
as-an-engagement-type is not articulated; this run closes that gap.

This is not an introductory guide — assume the reader is the practice
lead, has read 00b / 00d / 02 / 24 / 30 / 32 / 34 in the practice's
vault, knows what a token tree is, knows what OKLCH is, knows what a
Theme Schema is (the JSON contract per 24 specifying which values a
brand must provide), knows what the Generative Token pattern is (5–10
primitives produce a brand's full semantic layer mechanically per 24
+ Adobe Spectrum / IBM Carbon precedent), knows what headless-component
architecture is (Radix UI, React Aria, Headless UI, Reach UI as the
canonical examples — primitives that own behaviour and a11y but ship
unstyled, with consumers owning the visual layer), knows what Material
Design / Polaris / Carbon are, and knows the practice's commercial
shapes from 00d (Pattern 1–5, the role table, the phase hour ranges,
the run-phase pricing gap). Don't explain what tokens are, what
multi-brand theming is, what Style Dictionary is, what Figma Variables
are, what a contribution model is, what BCP47 / IETF locales are, what
DTCG is — explain how the practice should *operate* the white-label
engagement type as a discipline at agency scale, where each architectural
choice (the engine, the schema, the headless-vs-opinionated split)
shapes the SOW and the team, where the field's white-label tooling has
known gaps that practitioners work around, what the two white-label
shapes are and when to recommend each, how Prism2 is positioned against
them, and how the commercial shape differs from the practice's standard
build-and-handoff pattern.

Research scope — cover all of the following:

1. White-label as an engagement type — meta-framing and altitude

- The case that white-label-DS is a *distinct engagement type*, not a
  variant of multi-brand or a feature of a generic DS. Multi-brand is
  the architecture (per 24 — multi-collection-not-multi-mode for brand,
  Brand Semantic collections, the seven theming dimensions per 02 §6);
  white-label is the *shape of the engagement* the practice signs and
  delivers. The architecture and the engagement-shape are different
  axes; the practice that articulates only the architecture under-
  scopes the engagement.
- Where white-label sits relative to 00b / 00d / 02 / 24 / 30 / 32 / 34.
  00b names the kit (Prism2); 00d names the commercial question; 02
  names white-label as the seventh theming dimension; 24 names the
  architecture (Generative Token, Theme Schema as contract); 30 prices
  the AI-readiness layer; 32 prices the audit; 34 prices the workstation
  MCPs. White-label-as-engagement-type is the *fourth productisation
  companion* alongside 30 / 32 / 34 — same template (workstation-vs-
  engagement-vs-portfolio billing distinction explicit; cost-of-not-
  having articulated; synthesis-ready operational artefact shipped),
  different slice of practice IP.
- Why the engagement-type framing matters commercially. The agency
  that pitches "we'll build you a multi-brand design system" prices
  the architecture and skips the engagement shape (no SOW for brand-
  onboarding, no retainer for engine maintenance, no per-brand
  pricing model). The agency that pitches "we'll build you a white-
  label design system" prices the architecture *and* the engagement
  shape (the engine as a Phase 2 deliverable; the brand-onboarding
  runbook as a deliverable; the recurring brand-onboarding revenue
  as a retainer line; the per-brand SOW shape as a productised
  template). The framing is what unlocks the commercial wedge.
- The miscategorisation cost worth naming. The practice that conflates
  white-label with multi-brand under-prices both. The practice that
  conflates white-label-for-resellers with white-label-as-starter
  ships the wrong architecture for the brief — building a brand-
  generation engine for a starter library that doesn't need one
  (over-engineering, sunk cost), or shipping a starter library to a
  reseller-platform client (under-engineering, doesn't scale past
  three resellers). Articulating the two shapes is what prevents
  both miscategorisations.

2. The two white-label shapes — for-resellers vs. as-starter

- **White-label-for-resellers.** One product, N reseller-supplied
  brand inputs. The reseller signs up; supplies a minimum brand
  set (logo, primary color, typeface, voice tone — the Theme Schema
  contract per 24); the system generates the rest. The end-user
  product is structurally the same across resellers; the brand
  layer is what varies. Examples in the field: Shopify's theme
  marketplace; Mailchimp's email-template themes; B2B SaaS platforms
  shipping to embedded white-label clients (Stripe Connect's
  Embedded Components, Plaid's Link, ChannelEngine, ShipStation).
  Architecturally: brand-generation engine + Theme Schema contract +
  semantic-layer tokens + reseller onboarding pipeline. Commercially:
  recurring brand-onboarding revenue (per-reseller fee on signup;
  per-reseller monthly retainer for engine access).
- **White-label-as-starter.** Foundation + starter library that
  accelerates the early stages of a *bespoke* client engagement.
  The agency ships an internal kit (Prism2 as the practice's
  example); each engagement starts from the kit; client-specific
  customisation diverges from the kit during the engagement; the
  end-state is a bespoke client system that started from the kit
  but isn't bound to it. Examples in the field: most agency-
  internal kits (IBM Garage's starter, Pentagram's brand-system
  template, the practice's Prism2). Architecturally: starter token
  set + starter component library + starter documentation pattern +
  agency-internal governance for the kit's own evolution. Commercially:
  the kit reduces engagement startup cost (foundations exist;
  components don't start from zero); the kit doesn't generate
  recurring revenue from clients (it's an agency-internal asset).
- The conflation cost. White-label-for-resellers needs the brand-
  generation engine because the brand list is unknown at architecture
  time and grows over the product's lifetime; the engine is a
  load-bearing investment. White-label-as-starter does *not* need the
  engine — each engagement's brand is known at architecture time
  (it's the client's brand) and the kit-to-bespoke transition happens
  during the engagement. Building the engine for a starter library
  is over-engineering. Shipping a starter library to a reseller
  platform doesn't scale past three or four resellers.
- The decision questions. Is the brand list known at architecture
  time? (No → for-resellers.) Does the system serve a single product
  with multiple brand instances or multiple products from a single
  brand foundation? (Single product, multiple brands → for-resellers;
  multiple products, single foundation → as-starter.) Is the recurring
  revenue from brand-onboarding the engagement's commercial premise,
  or is the kit reducing per-engagement startup cost? (Recurring
  revenue → for-resellers; startup-cost reduction → as-starter.) Each
  pair of answers points to one shape.
- The hybrid case. Some engagements ship a starter that *includes*
  a partial brand-generation engine — the kit comes with OKLCH
  semantic-layer derivation but ships to one client at a time. The
  hybrid is real but should be the conscious decision, not the
  unstated default. The practice's discipline: pick the shape, name
  it explicitly in the SOW, deliver against the picked shape.

3. The architecture decision tree — when does the engine pay back

- The brand-generation engine is a load-bearing investment for white-
  label-for-resellers. Building it is the dominant cost (a one-time
  investment per portfolio that amortises across resellers; per 24
  + Adobe Spectrum / IBM Carbon precedent). The decision tree:
  when is the engine warranted, and when is the system better
  shipped without it?
- The minimum brand-defining input set. The Theme Schema contract
  (per 24) specifies which values a brand must provide. The minimum
  set: primary color (the OKLCH-derived ramp seed); a neutral hue
  (the gray ramp seed); a typeface stack (the brand voice in type);
  a brand radius (the form-factor distinguisher); a brand density
  (the brand's spacing rhythm). Five primitives is the floor. Adding
  a sixth (a logo URI, a brand-voice tone parameter for assistant
  copy) expands the input set without expanding the engine
  meaningfully. Going below five (only a primary color, only a
  logo) under-determines the brand and produces visually
  indistinguishable resellers — the brand layer collapses.
- The reseller-count payback curve. Building the engine is meaningful
  one-time investment (~150–300 hours of senior DS engineering
  + ~80–120 hours of senior design — the engine itself, the
  schema validation, the onboarding pipeline, the per-reseller QA
  surface). Per-reseller cost without the engine is roughly the
  same as a single-brand bespoke build (the brand layer is hand-
  crafted; the foundations are reused). With the engine, per-
  reseller cost drops to ~10% of the first reseller's cost (per
  Spectrum / Carbon's reported numbers; verify the claim per the
  source-text discipline). The break-even point is roughly five
  resellers — below that, the engine is over-engineered; above
  that, the engine pays back through the engagement and becomes
  recurring-revenue infrastructure.
- The architecture decision tree should ship as a synthesis-ready
  artefact in the file. Five questions; each answer points to engine
  or no-engine. (Sketch shape, not prescription — the agent can
  refine.) Q1: Is the brand list known at architecture time? (Yes →
  no engine, hand-craft each brand.) Q2: How many brands at launch
  and within 18 months? (≤4 → no engine; ≥5 → engine.) Q3: Is the
  per-brand onboarding cost a commercial constraint (recurring
  revenue depends on it being low)? (Yes → engine; no → optional.)
  Q4: Does the brand layer need to vary on more than four primitives
  (color + neutral + type + radius + density)? (Yes → engine
  warranted; no → manual works.) Q5: Will the engine be maintained
  by a dedicated engineer post-handoff, or does it need to be
  client-self-service? (Self-service → engine + brand-validation
  tooling; dedicated engineer → engine + lighter validation.)
- Build-vs-buy for the engine. The vendors are starting to ship
  this layer — Specify, Knapsack, Supernova, Backlight all have
  primitives-to-semantic-layer derivation. As of mid-2026 none is
  fully sufficient for white-label-for-resellers at portfolio scale
  (the validation surface is thin; the per-brand QA surface is
  thinner; the onboarding pipeline is custom regardless). The
  practice's bet: native vendor support lands in 2026–2027; until
  then, the engine is custom work. The bridge investment is
  meaningful but bounded.

4. Headless-vs-opinionated for white-label — the visual-vs-behaviour
   layer decision

- White-label products face a tension: resellers (and bespoke
  clients on starter foundations) want to override surface
  elements (visual layer — color, type, spacing, radius, motion)
  without overriding behaviour (interaction layer — keyboard model,
  focus management, a11y semantics, error states, validation
  contracts). Headless-component architecture is the modern answer
  (Radix UI, React Aria, Headless UI, Reach UI as the canonical
  examples).
- The split. **Behaviour layer (system-owned, non-negotiable).**
  Keyboard model, focus trap, focus restoration, ARIA semantics,
  state machine for composite widgets, a11y contracts, RTL handling,
  i18n contracts (not content; the rendering contract). The system
  owns this. Resellers cannot override it. **Visual layer (reseller-
  owned, negotiable within the schema).** Color, typography,
  spacing, radius, motion duration / easing, iconography, surface
  elevation. Resellers can override these via the Theme Schema.
  The system *renders* what the schema says; the system doesn't
  *design* per reseller.
- Why the split matters for white-label specifically. A reseller
  that can override the keyboard model breaks accessibility across
  the platform — the reseller has neither the expertise nor the
  testing surface to do this safely. A reseller that can override
  the visual layer expresses brand without compromising the
  platform's contract. The split is what makes white-label-for-
  resellers commercially viable: the platform retains a11y
  conformance liability; the reseller retains brand expression.
- The headless-component implementation pattern. The system ships
  a component library where each component is composed of a
  headless behavioural primitive (Radix's `Dialog` primitive,
  React Aria's `useDialog` hook) and a visual layer that consumes
  the Theme Schema. The agency builds the visual layer once
  against the engine; the engine generates the per-reseller
  visual rendering. The behavioural primitive is shared; the
  visual layer is generated.
- The opinionated-component case. White-label-as-starter doesn't
  necessarily need headless. The starter ships components with
  visual defaults; the bespoke engagement modifies the visual
  layer during the engagement. Opinionated components are fine
  for as-starter because the visual modification happens at design
  time (in Figma), not at runtime (per reseller). The headless
  discipline is over-engineering for as-starter — adds complexity
  without commensurate benefit.
- The hybrid. Some engagements ship a starter with headless
  primitives where the bespoke engagement is expected to need
  cross-product brand variation later. The hybrid is the conscious
  bet on future needs; should be priced as such.
- The 2026 tooling reality. Radix UI, React Aria (Adobe's),
  Headless UI (Tailwind's), Reach UI (in maintenance mode),
  Ariakit, Park UI (built on Ark UI which wraps headless logic
  for cross-framework use). The practice's default for new headless
  white-label work is Radix UI for React engagements, React Aria
  for cross-framework engagements where Radix's React-only
  surface is a constraint, Ark UI for engagements that need
  Vue / Solid / Svelte alongside React. Verify the framework's
  current state per project; the headless-library landscape
  evolves quarterly.

5. The commercial shape of white-label engagements

- The two shapes price differently. The synthesis-ready artefact:
  a comparison table laying out the SOW shape, retainer pattern,
  and onboarding pricing for each white-label shape side by side.
  (Sketch shape, not prescription — the agent can refine.)
- **White-label-for-resellers commercial shape.** The Build SOW
  prices the engine + the schema + the first three resellers as
  the engineering proof point. Roughly: foundations (~150 hours);
  engine + schema (~150–300 hours); reference component library
  (~250–400 hours); per-reseller onboarding pipeline (~80–150
  hours); first three reseller brand integrations (~80–160 hours
  total, ~30–60 hours each). The Run SOW is a recurring brand-
  onboarding retainer: per-reseller signup fee ($5–25k depending
  on brand complexity); per-reseller monthly retainer for engine
  access ($1–5k/month); engine maintenance retainer (~20–40
  hours/month covering schema evolution, engine bug fixes, new
  reseller onboarding support). The recurring revenue is the
  commercial premise.
- **White-label-as-starter commercial shape.** The starter is
  agency-internal IP; clients don't pay for the starter directly.
  The engagement prices the bespoke build at standard hours (per
  00d's current Prism2 position — "scope at standard hours; the
  kit is a quality and consistency accelerator, not a line-item
  reduction"). The compression is in the foundations / token /
  initial-component-design phases; the audit / handoff / dev-
  support phases don't compress. The agency's commercial benefit
  is internal velocity (more engagements per practitioner per
  year because startup cost drops), not per-engagement revenue.
- The retainer pattern for for-resellers. The retainer covers
  three commitments: brand-onboarding SLA (a new reseller is
  onboarded within X days of contract signature); engine
  availability SLA (the engine is up 99.x% of the time and
  generates valid output); schema-evolution coordination (the
  schema may evolve; resellers may need to migrate; the retainer
  covers the migration coordination). The SLAs are how the
  retainer gets priced — without them, the retainer is "we'll
  help when you need it" which doesn't bind to a number.
- The brand-onboarding pricing model — the load-bearing decision.
  Per-reseller signup fees vary widely in the field. The
  practice's discipline: tier the brand by complexity (simple
  brand = primary color + logo + typeface = $5k; standard brand
  = adds neutral hue + radius + density = $12k; complex brand =
  adds custom motion + custom iconography + custom voice = $25k+).
  The complexity tier maps to the engine's input-set scope (per
  §3); the more inputs, the more brand-validation work; the
  higher the fee.
- How for-resellers connects to 00d's run-phase gap and §1.1's
  pricing-after-handoff gap. The recurring brand-onboarding
  retainer is the most concrete answer to 00d's "the run phase
  is unpriced" gap that the practice has surfaced. White-label-
  for-resellers engagements *force* the run-phase pricing question
  because the engine doesn't operate without ongoing maintenance.
  The practice that articulates the for-resellers retainer pattern
  has a productised retainer-phase shape that generalises to
  bespoke engagements (Run-phase retainer per 00d), not just to
  white-label.
- Where for-resellers fits in 00d's Pattern 1–5. None of the
  five patterns fits cleanly. The practice should add a sixth
  pattern: **Pattern 6 — White-label / reseller platform.** The
  hour ranges are higher than Pattern 1–5 because the engine
  is a heavier lift; the deliverable shape is different (engine
  + schema + reference library, not a single client's library);
  the commercial shape includes a recurring retainer that
  Pattern 1–5 doesn't.

6. Prism positioning closure — resolving 09 §3.2

- The conflict. 09 §3.2 names the unresolved positioning question:
  Prism is alternately called a "design system" (in some VML
  internal materials) and an "internal UI Kit and set of tools"
  (in others). The deck says DSes are *not* UI Kits. The conflict
  has been open across the corpus for the full life of this
  knowledge base.
- The resolution this file lands. **Prism2 is properly described
  as a white-label-as-starter foundation + starter library, not
  a finished design system.** Prism2 is *not* white-label-for-
  resellers — there's no brand-generation engine, no Theme Schema
  contract validating arbitrary future brands, no per-reseller
  onboarding pipeline. Prism2 ships a token foundation, a Figma
  component kit, and a coded counterpart in development; it
  accelerates the early stages of a bespoke client engagement;
  it doesn't operate as a multi-brand reseller platform.
- The technology-team-adoption gap as the load-bearing constraint.
  Per 00b: Prism2 is "primarily realized as a Figma component
  kit" with "a React component library (in development/evolution)";
  it is "not formally adopted by VML's technology teams — which
  limits its use on engagements where design and dev need to be
  tightly integrated." This is what holds Prism2 in the as-starter
  shape; it cannot become for-resellers without technology-team
  adoption (the engine, the schema, the onboarding pipeline are
  all engineering work that requires technology-team commitment).
- The Prism2 → Prism3 implication. If the practice wants Prism to
  evolve toward white-label-for-resellers (recurring revenue from
  reseller platforms; agency-level repeatable brand-onboarding
  capability), Prism3 needs the engine + schema + pipeline
  layers that Prism2 lacks. This is a meaningful investment
  (~300–500 hours of senior engineering plus ~150–250 hours of
  senior design — the engine, the schema, the validation surface,
  the per-reseller QA surface, the onboarding documentation,
  the runbook for the agency's own brand-onboarding team). The
  payback shape is the recurring brand-onboarding revenue per §5.
- The right answer for now. Don't try to make Prism2 do white-
  label-for-resellers. Position Prism2 as white-label-as-starter
  honestly; price engagements that use Prism2 at standard hours
  (per 00d's current position); track the first ~5–10 engagements
  where Prism2 is formally used to build the empirical case for
  the kit's actual time savings. If the data supports white-
  label-for-resellers as a future practice direction, scope
  Prism3 against it explicitly.
- The client conversation that the closure unlocks. Per 00b's
  current language: *"We have an internal foundation that means
  we're starting from a more mature baseline than a from-scratch
  build."* The closure adds the engagement-shape clarification:
  *"Prism2 is our white-label-as-starter foundation — it
  accelerates the early stages of your bespoke build. It is not
  a multi-tenant reseller platform; if you need that, the
  engagement is a different shape and a different price."* The
  clarification prevents the conflation that has caused the
  positioning conflict to persist.

7. Team, governance, failure modes, AI-readiness, and the See-also

- **The team shape for white-label-for-resellers engagements.** The
  Build phase team includes a senior DS architect (engine + schema +
  composition rules); a senior DS engineer (engine implementation,
  per-platform output); a senior visual designer (the reference
  brand and the brand-validation tooling); a senior accessibility
  specialist (the behaviour layer's a11y contract; the cross-engine
  matrix per 28); a project manager. The Run phase team is smaller —
  an engine maintainer (typically 0.5 FTE for a portfolio of 10–30
  resellers); a brand-onboarding designer (typically 0.5 FTE for
  the first wave; scales with the reseller list); a part-time
  accessibility specialist (per-reseller validation as resellers
  onboard).
- **The team shape for white-label-as-starter engagements.** Smaller
  on the agency side because the engagement is a single client's
  bespoke build with the kit accelerator. Standard 00d team
  composition (senior visual designer + senior UX designer + design
  technologist + PM + part-time accessibility specialist) plus an
  agency-internal kit maintainer (typically 0.25 FTE across all
  engagements that use the kit, supporting kit evolution and
  cross-engagement learnings).
- **Governance for the kit (or engine) itself.** White-label-as-
  starter requires agency-internal kit governance — who owns the
  kit's evolution; how do per-engagement learnings get back to the
  kit; how do breaking changes to the kit propagate to engagements
  using earlier kit versions; how is kit version pinning handled
  per 24's brand version pinning pattern. White-label-for-resellers
  requires both kit/engine governance *and* schema governance —
  the schema is the API resellers code against; schema changes are
  breaking changes for resellers; deprecation windows per 24 §
  Deprecation-as-a-window apply.
- **The brand-onboarding runbook as practice IP.** For-resellers
  engagements ship a runbook the agency's brand-onboarding team
  follows for each new reseller. The runbook covers: the input-
  collection meeting (typically 1–2 hours with the reseller's
  brand owner; capture primary color, neutral, typeface, radius,
  density, voice tone); the engine invocation (typically 2–4 hours
  of senior DS engineer time); the per-reseller QA pass (typically
  4–8 hours; verifies the engine's output meets contrast / a11y /
  visual quality bars); the reseller-facing handoff (typically 1
  hour; gives the reseller their brand assets, the platform-level
  documentation, the support contract details). Total per-reseller:
  ~10–16 hours of agency time; pricing tiered per §5.
- **Failure modes specific to white-label.** **Brand-validation
  drift.** The engine's output passes contrast / a11y rules at
  onboarding time; the schema evolves; the previously-validated
  brand drifts out of conformance. Continuous validation (per 32 §5
  + 24 §Cross-brand drift) is load-bearing. **The engine outpaces
  the system.** The engine ships features (new theming dimensions,
  new schema fields) faster than the reference component library
  consumes them; resellers see options the components don't render.
  **Reseller customisation outpaces the architecture.** A reseller
  asks for an override the schema doesn't support; the agency makes
  a one-off custom build for the reseller; the one-off doesn't fold
  back into the engine; the architecture splits. **Brand-onboarding
  SLA missed.** The runbook's hour estimate is wrong (a complex
  brand needed 30 hours, not 10); the SLA breaks; the recurring-
  retainer commercial shape is at risk. **The kit-vs-bespoke
  divergence (as-starter specific).** A bespoke engagement modifies
  the kit's tokens and components; the engagement ships; the
  modifications don't fold back into the kit; the kit's version
  drifts from the actual fielded systems. **The "starter became a
  product" failure mode.** The agency's internal kit evolves to
  the point that it's almost a finished system; clients are
  charged for engagements that mostly ship the kit unchanged; the
  agency's commercial value-add is unclear. The discipline: when
  the kit covers >70% of an engagement's needs, the engagement is
  a thin-bespoke shape (priced lower than full bespoke; honestly
  named).
- **AI-readiness for the engine.** The engine that generates
  per-reseller token sets should also generate per-reseller
  `.ai.json` registries (per 30) — every reseller's brand has its
  own AI-readable layer because every reseller's components inherit
  the reseller-specific token semantic layer. The engine's
  output set: token JSON, CSS / Swift / Kotlin output, MDX docs,
  `.ai.json` per component. Per 30's pipeline framing applied to
  white-label.
- **MCP for white-label.** Per 34 — the per-engagement custom DS
  MCP server applies to white-label but with a wrinkle: for-
  resellers engagements may ship a *per-reseller* MCP surface where
  each reseller's MCP exposes their brand's token catalogue +
  component contract. The engine generates the MCP server's
  configuration alongside the brand assets. The MCP layer becomes
  the structured surface AI clients (whether the reseller's
  internal AI tooling, or the platform's first-party AI features)
  consume. As of mid-2026 no white-label platform ships per-
  reseller MCP natively; the practice's bet: this lands in
  2026–2027 alongside vendor-native MCP per 34 §5.
- **The See-also.** 00b (Prism2 framing → 33 §6 closes the
  positioning); 00d (white-label kit commercial question → 33 §5
  articulates the answer); 02 §6 (white-label as Curtis's seventh
  theming dimension → 33 productisation); 24 (Generative Token
  pattern → 33 §3 architecture decision tree); 30 (AI-readiness
  pipeline → 33 §7 white-label AI layer); 32 (audit → continuous
  brand-validation per 33 §7 failure modes); 34 (workstation MCPs
  → 33 §7 per-reseller MCP). Also 07 (governance), 08 (run phase),
  17 (a11y contract — the behaviour-layer non-negotiable per
  §4), 28 (web a11y — the cross-engine matrix the platform owns).

Output format: Structured markdown. Use H2 section headings that match
the seven-section spine above. Synthesize findings — do not list
sources mechanically. Where the field has consensus, state it clearly;
where decisions are context-dependent, provide decision frameworks
rather than declaring a winner. Two synthesis-ready artefacts must
ship: the architecture decision tree (per §3 — five questions, engine-
vs-no-engine outcomes) and the for-resellers vs. as-starter comparison
table (per §5 — SOW shape, retainer pattern, onboarding pricing side
by side). Flag where white-label tooling has known gaps (vendor-
native MCP for per-reseller surfaces; native engine support in
Specify / Knapsack / Supernova; the 2026 headless-library landscape's
quarterly evolution). Where claims depend on current state — vendor
positioning, platform pricing, library framework support — date them
and note the verification path. Include a references section linking
to primary sources (Adobe Spectrum's brand-derivation docs; IBM
Carbon's contrast-pinned palette docs; Radix UI / React Aria / Ark
UI / Ariakit documentation; Stripe Connect Embedded Components;
Shopify Polaris's white-label variant; Mailchimp's email-template
themes; the Multi-Brand Governance source from Apr 2025; the
practitioner writing on white-label DS work — Brad Frost, Nathan
Curtis if they've written, Andrew Couldwell's *Laying the
Foundations* on token foundations, the EightShapes catalogue
where multi-tenant DS surfaces, the ZURB / Treder writing on
agency starter kits).

Depth: Expert audience. Do not explain what tokens are, what
multi-brand theming is, what Style Dictionary is, what Figma
Variables are, what a contribution model is, what BCP47 is, what
DTCG is, what OKLCH is, what a Theme Schema is at the basic level —
explain how the practice operates the white-label engagement type
as a discipline at agency scale, where each architectural choice
shapes the SOW and the team, where the field's white-label tooling
has known gaps, what the two white-label shapes are and when to
recommend each, how Prism2 is positioned against them, and how the
commercial shape differs from the practice's standard build-and-
handoff pattern.

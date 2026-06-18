# White-label design systems as an engagement type — the agency-scale shaping discipline

The white-label DS conversation in this vault has been split across five files for the entire life of the corpus. 00b names the kit (Prism2 — what it is, what it isn't yet, the technology-team-adoption gap that holds it where it is). 00d names the commercial question ("does the kit reduce estimates or raise quality at the same estimate"; current position is "scope at standard hours, treat the kit as a quality accelerator, not a line-item reduction"). 02 §6 names white-label as the seventh theming dimension in Curtis's hierarchy — *extensive customisation at any decision level, highest cost.* 24 §White-label-and-reseller-scenarios names the architecture (Theme Schema as contract; brand-generation engine as the practice-default for unknown-brand-list scenarios; the Generative Token pattern as the most-promising direction). 09 §3.2 names the unresolved positioning conflict — Prism is alternately called a design system and a UI Kit; the working POV ("white-label foundations + starter library") is stated but not operationalised.

The architecture half of the white-label question is closed. The engagement-shaping half — when to recommend white-label as a shape, how to scope it, how to price it, how to operate it, how to staff it, how to hand it off, how to resolve the Prism positioning question — is not. This file closes that gap. Seven sections in order: why white-label is a distinct engagement type and not a variant of multi-brand; the two white-label shapes (for-resellers vs. as-starter) the practice should articulate explicitly; the architecture decision tree for when the brand-generation engine pays back; the headless-vs-opinionated split that makes white-label-for-resellers commercially viable; the commercial shape of white-label engagements as the fourth productisation companion to 30 / 32 / 34; the Prism positioning closure; and the team, governance, failure-mode, and AI-readiness layers that the engagement shape forces.

A note on altitude before anything else. White-label content evolves slowly compared to MCP tooling (per 34) but faster than token-architecture fundamentals (per 22 / 24). Specific tooling claims about the headless-component landscape, vendor-native engine support, and per-reseller MCP surfaces below reflect mid-2026 platform state; verify against current docs before treating any specific tool name as load-bearing in client work. The architectural shape — two engagement shapes, the engine-vs-no-engine decision, the headless visual-vs-behaviour split, the run-phase recurring-revenue pattern — is more durable than the tools attached to it. Bet on the architecture, not on the tool.

---

## 1. White-label as a distinct engagement type — meta-framing and altitude

### Architecture and engagement-shape are different axes

The practice's existing material treats white-label primarily as an *architectural* question — the seventh theming dimension per Curtis (02 §6); the unknown-brand-list scenario per 24 §White-label-and-reseller; the Generative Token pattern per 24. All correct, all load-bearing. None of it answers the question that determines whether an engagement succeeds: *what is the shape of the engagement the practice signs and delivers, and how does the practice scope, price, staff, and operate it?*

The shape is a different axis from the architecture. A multi-brand engagement (T-Mobile/Metro, Ford/Lincoln per 02) and a white-label-for-resellers engagement (a SaaS platform shipping to dozens of unknown future resellers) can use the *same* multi-collection token architecture and the *same* Generative Token pattern at the primitive layer. They are nevertheless different engagements. The multi-brand engagement scopes the brand list at architecture time and prices the build against the known brand count; the white-label engagement scopes the brand-generation contract at architecture time and prices the recurring brand-onboarding capability against the projected reseller count. The first is a one-time delivery; the second is a delivery plus recurring infrastructure. The architecture is similar; the engagement is different.

The practice that articulates only the architecture under-scopes the engagement. The proposal lists token tiers and component specifications and ships against them; it does not articulate the brand-onboarding runbook, the per-reseller pricing tier, the engine-maintenance retainer, the schema-evolution coordination, the SLAs that define what "the engine works" means commercially. The result is a build that delivers the architecture and does not deliver the operating capability the client needs to run the platform. The client either funds the operating capability themselves (badly, because they don't know the runbook the practice never shipped) or pays the practice a second time for capabilities that should have been in scope from day one.

### The fourth productisation companion

This file is the **fourth productisation companion** in the pattern that 30 / 32 / 34 established. Each productises a different facet of practice IP; each commits the workstation-vs-engagement-vs-portfolio billing distinction explicitly; each ships a synthesis-ready operational artefact.

- **30** (generated-from-data documentation) productises the AI-readiness pipeline — workstation effort to specify; per-engagement effort to ship; portfolio effort to amortise the MCP server.
- **32** (auditing design systems) productises the audit engagement — workstation effort to run scanners; per-engagement effort to deliver the audit; portfolio effort to operate the continuous-audit pipeline.
- **34** (MCPs for DS practice) productises the workstation MCP stack — career-amortised general-purpose IP; per-engagement custom DS MCP for billable productisation.
- **33** (this file, white-label DS as engagement type) productises the **multi-brand IP that 24 architects** — agency-internal kit governance for as-starter; per-engagement engine + schema + onboarding pipeline for for-resellers; portfolio recurring brand-onboarding revenue as the run-phase commercial premise.

The synthesis-ready artefacts in this file are two: the architecture decision tree per §3 (five questions, engine-vs-no-engine) and the for-resellers vs. as-starter comparison table per §5 (SOW shape, retainer pattern, onboarding pricing side by side). Both are operational tools the practice carries into scoping conversations.

### Why the engagement-type framing matters commercially

The agency that pitches *"we'll build you a multi-brand design system"* prices the architecture and skips the engagement shape. No SOW for brand-onboarding; no retainer for engine maintenance; no per-brand pricing model; no SLA for the engine's availability. The proposal closes against the build hours; the build ships; the operating capability is missing; the relationship goes one of two ways — the client struggles to operate the platform and churns, or the client pays the practice a second time for the operating capability that was always going to be needed.

The agency that pitches *"we'll build you a white-label design system"* prices both. The engine and schema are itemised in the build SOW (typically as Phase 2 deliverables, after foundations); the brand-onboarding runbook is itemised as a deliverable; the recurring brand-onboarding retainer is itemised as a Run-phase line; the per-brand SOW shape is itemised as a productised template. The framing is what unlocks the commercial wedge — and what closes the run-phase pricing gap (per 00d §The Run-Phase Pricing Gap; per 09 §1.1's pricing-after-handoff) on this engagement type specifically.

White-label-for-resellers is the practice's clearest example of an engagement that *forces* the run-phase pricing question. The engine doesn't operate without ongoing maintenance; the schema doesn't evolve without coordination; the resellers don't onboard without the runbook. The Run phase is not optional. The agency that has articulated the for-resellers retainer pattern has a productised retainer-phase shape that generalises — the same shape applies, with adjustments, to bespoke engagements where the practice wants to ship a Run-phase retainer (per 00d's three productisable post-Build offerings).

### The miscategorisation costs to name

Two miscategorisations show up in agency proposals and shape this file's structure.

**Conflating white-label with multi-brand.** Multi-brand systems handle a known brand list at the *theming* layer (per 02). Architecturally similar; commercially different. The agency that conflates the two prices the multi-brand build and skips the operating layer that white-label needs — the engine, the schema, the runbook, the retainer.

**Conflating white-label-for-resellers with white-label-as-starter.** This is the load-bearing miscategorisation that this file's §2 closes. For-resellers ships an engine because the brand list is unknown at architecture time and grows over the product's lifetime; the engine is a one-time investment that amortises across resellers. As-starter ships a foundation + starter library because each engagement's brand is known at architecture time (it's the client's brand) and the kit-to-bespoke transition happens during the engagement; no engine is needed. Building the engine for a starter library is over-engineering — sunk cost the practice never recovers. Shipping a starter library to a reseller-platform client is under-engineering — the architecture doesn't scale past three or four resellers, and the platform's commercial premise (recurring revenue from onboarding) breaks. Articulating the two shapes is what prevents both miscategorisations.

---

## 2. The two white-label shapes — for-resellers vs. as-starter

### White-label-for-resellers

One product, N reseller-supplied brand inputs. The reseller signs up; supplies a minimum brand set (logo, primary color, typeface, voice tone — the Theme Schema contract per 24); the system generates the rest. The end-user product is structurally the same across resellers; the brand layer is what varies.

**Field examples.** Shopify's theme marketplace (each merchant supplies a small brand set; Shopify generates the rendered storefront). Mailchimp's email-template themes (each customer supplies brand color and logo; Mailchimp generates the per-template rendering). Stripe Connect's Embedded Components (each platform supplies brand tokens; Stripe renders the Checkout / Connect components inside the platform). Plaid Link (each financial platform supplies a small brand surface; Plaid renders the connection flow). ChannelEngine, ShipStation, and most B2B SaaS platforms shipping embedded white-label flows. The shared shape: *one platform, an arbitrary number of brand-instances.*

**Architecturally.** Brand-generation engine + Theme Schema contract + semantic-layer tokens + reseller-onboarding pipeline. Per 24's Generative Token pattern, the engine derives most of the brand's semantic layer from a small primitive set (5–10 tokens) via standardised computation — OKLCH-derived ramps from the primary color; contrast-pinned text-on-background pairs; density-aware spacing tokens generated from the brand's chosen density step. The schema is a JSON contract resellers code against; the engine validates against the schema; the validated brand becomes a per-reseller token set the platform consumes.

**Commercially.** Recurring brand-onboarding revenue. Per-reseller signup fee tied to brand complexity; per-reseller monthly retainer for engine access and schema-evolution coordination; engine-maintenance retainer covering schema evolution and reseller-onboarding support. The Run phase is not optional; the engine doesn't operate without it. The recurring revenue is the engagement's commercial premise — it is what makes the engineering investment in the engine pay back across the portfolio.

### White-label-as-starter

Foundation + starter library that accelerates the early stages of a *bespoke* client engagement. The agency ships an internal kit; each engagement starts from the kit; client-specific customisation diverges from the kit during the engagement; the end-state is a bespoke client system that started from the kit but isn't bound to it.

**Field examples.** Most agency-internal kits — IBM Garage's starter, Pentagram's brand-system templates, the practice's Prism2, the EightShapes Sub Atomic + Atomic + Molecule scaffolds Curtis ships, ZURB Foundation as the historical example. Some open-source starter libraries serve the same role for in-house teams (Tailwind UI as a starter; shadcn/ui as a more recent example; Material UI's `unstyled` mode used as a starter foundation). The shared shape: *one engagement at a time, the kit is the starting point not the ending point.*

**Architecturally.** Starter token set + starter component library + starter documentation pattern + agency-internal governance for the kit's own evolution. The kit ships opinionated defaults — a Prism2-style visual baseline, a documented contribution pattern, an `.ai.json` registry shape that subsequent engagements instantiate against (per 30). No brand-generation engine; no Theme Schema contract for arbitrary future brands; no per-reseller onboarding pipeline. The kit is one starting point that diverges per engagement.

**Commercially.** The starter is agency-internal IP; clients don't pay for the starter directly. The engagement prices the bespoke build at standard hours (per 00d's current Prism2 position — "scope at standard hours; the kit is a quality and consistency accelerator, not a line-item reduction"). The compression is in the foundations / token / initial-component-design phases; the audit / handoff / dev-support phases don't compress regardless of kit availability. The agency's commercial benefit is internal velocity — more engagements per practitioner per year because startup cost drops — not per-engagement revenue.

### The conflation cost

White-label-for-resellers needs the engine because the brand list is unknown at architecture time and grows over the product's lifetime; the engine is a load-bearing investment that pays back across the reseller portfolio. White-label-as-starter does *not* need the engine; each engagement's brand is known at architecture time (it's the client's brand) and the kit-to-bespoke transition happens during the engagement.

Building the engine for a starter library is over-engineering. The starter library serves one engagement at a time; the engine's per-reseller payback shape is irrelevant; the engineering effort (typically 150–300 hours senior DS engineering plus 80–120 hours senior design — see §3) is sunk cost the practice never recovers. Worse, the engine ties the kit to a specific token-derivation discipline that the bespoke engagement may not want; the engagement spends its first weeks fighting the engine instead of starting from a clean kit.

Shipping a starter library to a reseller-platform client is under-engineering. The starter ships components the agency designed once; resellers need rendering options the components don't expose; the agency tries to add reseller-customisation surfaces ad-hoc; the architecture splits between starter-shaped components and engine-shaped components; per-reseller onboarding cost stays at first-reseller scale (no compounding payback); the platform's commercial premise (recurring brand-onboarding revenue from a growing reseller list) breaks. The agency that under-prices a for-resellers engagement against an as-starter shape ships an architecture that doesn't scale and a commercial model that doesn't pay back.

### The decision questions

Three questions point to one shape:

1. **Is the brand list known at architecture time?** If no (the platform ships to unknown future resellers), the shape is for-resellers. If yes (the engagement is a single client's bespoke build, even when the client has multi-brand needs internally), the shape is as-starter — or the architecture is multi-brand, not white-label per se.
2. **Does the system serve a single product with multiple brand instances or multiple products from a single brand foundation?** Single product, multiple brands → for-resellers. Multiple products, single foundation → as-starter (the foundation is the practice's kit; products are bespoke engagements).
3. **Is recurring revenue from brand-onboarding the engagement's commercial premise, or is the kit reducing per-engagement startup cost?** Recurring revenue → for-resellers. Startup-cost reduction → as-starter.

Each pair of answers points to one shape. The practice's discipline is to ask all three questions in scoping; if the answers conflict, the engagement is a hybrid (see below) and the conflict surfaces the conscious decision the practice has to make.

### The hybrid case

Some engagements ship a starter that *includes* a partial brand-generation engine — the kit comes with OKLCH semantic-layer derivation, but ships to one client at a time. This is real and worth naming. It's typically the right shape when the practice has a strong opinion that the client will need cross-product brand variation later (a brand portfolio expanding from one product to several; an acquisition strategy that adds brand instances to the foundation over the system's lifetime). The hybrid is a conscious bet on future needs; it should be priced as such — the engine's engineering effort doesn't pay back on the first engagement, but the practice is wagering that future engagements with the same client (or in the same portfolio) will amortise the investment.

The discipline: if the engagement is hybrid, name it explicitly in the SOW. *"This is a starter library with engine primitives included for projected future multi-product use; the engine is a discounted line item ($X) reflecting partial first-engagement amortisation; future engagements drawing on the engine will reflect lower foundation costs accordingly."* The naming forces the conversation about what the future engagements actually are; without it, the engine becomes a sunk cost the agency absorbed without recognition.

---

## 3. The architecture decision tree — when does the engine pay back

### The engine as the load-bearing investment

The brand-generation engine is the load-bearing investment for white-label-for-resellers. Building it is the dominant cost — a one-time investment per portfolio that amortises across resellers per 24 + the Adobe Spectrum / IBM Carbon precedent. The decision tree this section commits is *when is the engine warranted, and when is the system better shipped without it*. The decision is what determines whether the engagement is for-resellers (engine in scope) or as-starter (engine not in scope) at architecture time.

### The minimum brand-defining input set

The Theme Schema contract specifies which values a brand must provide. The minimum set is **five primitives**:

1. **Primary color** — the OKLCH-derived ramp seed. The engine generates the primary's full lightness ramp (50 / 100 / 200 / ... / 900) via OKLCH lightness adjustments, contrast-pins the text-on-primary pairs to WCAG / APCA thresholds, derives accent semantics by formula.
2. **Neutral hue** — the gray-ramp seed. Same OKLCH-derived ramp logic; neutrals carry the brand's temperature (warm gray, cool gray, true gray).
3. **Typeface stack** — the brand voice in type. Per 23 — primary type role, display type role, code/UI role; the multi-script fallbacks via DTCG modes.
4. **Brand radius** — the form-factor distinguisher. Sharp (0px) reads industrial; soft (16–24px) reads consumer; the brand radius scales the entire component library's corner system.
5. **Brand density** — the brand's spacing rhythm. Compact / cozy / comfortable; the density step parameterises the spacing scale per 22.

Five primitives is the floor. Adding a sixth (a logo URI, a brand-voice tone parameter for assistant copy per 25 / 26 / 27) expands the input set without expanding the engine meaningfully. Adding a seventh (custom motion duration / easing per 18-21; custom iconography family) starts to expand the engine's surface; the engineering effort grows non-linearly because each new primitive interacts with the existing primitives' output. Going below five (only a primary color, only a logo) under-determines the brand and produces visually indistinguishable resellers — the brand layer collapses, and the commercial premise (resellers feel branded) breaks.

The practice's discipline: start at five; expand to six on a strong reseller-side need; resist the seventh-and-beyond expansion until the engagement has shipped and the field-truth shows the input set is genuinely insufficient. Premature schema expansion locks the engine into engineering complexity the resellers don't actually want.

### The reseller-count payback curve

Building the engine is meaningful one-time investment:

- **Engine implementation.** ~150–300 hours of senior DS engineering. The OKLCH transforms, the contrast-pinning logic, the schema validation, the per-platform output (web CSS, iOS Swift, Android Kotlin per 11), the cross-platform fidelity check per 24 §Validation.
- **Schema design and documentation.** ~40–80 hours of senior DS architect time. The Theme Schema as a JSON contract; the schema versioning discipline (per 24's deprecation-as-a-window pattern applied to schema evolution); the schema documentation resellers code against.
- **Reference component library.** ~250–400 hours of senior visual + UX design plus engineering. The component set rendered against the engine's reference brand; the components consume the engine's output and demonstrate that the brand-generation works end-to-end.
- **Onboarding pipeline.** ~80–150 hours. The brand-input collection tooling (a form, a CLI, a Figma plugin — practice's choice); the engine invocation flow; the per-reseller QA pipeline; the reseller-facing handoff package generation.
- **First three reseller integrations as the engineering proof point.** ~80–160 hours total, ~30–60 hours per reseller. The first three resellers are the engine's stress test — the agency learns where the schema is under-determined, where the engine's output needs human override, where the QA pass catches issues the engine can't.

Total engine + first-three-resellers Build cost: roughly **600–1,090 hours**, depending on engagement complexity and the practice's experience level. This is the wedge.

Per-reseller cost *without* the engine is roughly the same as a single-brand bespoke build — the brand layer is hand-crafted; the foundations are reused but the components are re-themed manually. Call this 100–250 hours per reseller depending on complexity (the lower end for simple brands, the higher end for complex brands with bespoke iconography or motion).

Per-reseller cost *with* the engine drops to roughly **10% of the first reseller's cost** per the Adobe Spectrum and IBM Carbon precedents (10–25 hours per reseller for the onboarding work — the brand-input meeting, the engine invocation, the QA pass, the handoff). Verify the 10% figure against current Spectrum / Carbon documentation before quoting in client work; the figure is widely cited but not trivially verified against a single primary source.

The break-even point: **roughly five resellers**. Below five, the per-reseller savings don't pay back the engine's build cost; the agency would have been better off hand-crafting each brand. Above five, the engine pays back through the engagement and becomes recurring-revenue infrastructure — every additional reseller after the break-even is high-margin revenue against minimal incremental cost.

### The decision tree

Five questions; each answer points toward engine or no-engine. The tree commits as a synthesis-ready artefact the practice carries into scoping conversations.

```
Q1. Is the brand list known at architecture time?
    Yes → No engine. Hand-craft each brand (or use multi-brand
          architecture per 24 if brand count >2).
    No  → Continue to Q2.

Q2. How many brands at launch and within 18 months of launch?
    ≤4 → No engine. Hand-craft is cheaper than the engine's amortisation
         curve at this scale.
    ≥5 → Continue to Q3.

Q3. Is per-brand onboarding cost a commercial constraint?
    (i.e., does recurring revenue from brand-onboarding depend on the
    onboarding cost being low?)
    Yes → Engine. Manual onboarding doesn't sustain the recurring-revenue
          model; the engine is the commercial premise.
    No  → Continue to Q4.

Q4. Does the brand layer need to vary on more than four primitives?
    (Color + neutral + type + radius + density is the floor; any
    additional axis — custom motion, custom iconography, custom voice
    surface for AI assistants — pushes toward engine.)
    Yes → Engine warranted. The variation surface is too wide for hand-
          craft to be consistent.
    No  → Continue to Q5.

Q5. Will the engine be maintained by a dedicated engineer post-handoff,
    or does it need to be reseller-self-service?
    Self-service → Engine + heavy brand-validation tooling. Resellers
                   onboard without agency intervention; the validation
                   surface has to catch every error the runbook would
                   have caught.
    Dedicated     → Engine + lighter validation. The engineer's review
                   catches what the validation misses; the validation
                   doesn't have to be production-grade for every edge.
```

Three or more "engine" answers across Q1-Q5 → ship the engine. Two or fewer → don't.

### Build-vs-buy for the engine

The vendors are starting to ship this layer. **Specify** has primitives-to-semantic-layer derivation; **Knapsack** exposes design-token automation that approaches engine functionality; **Supernova** has positioned itself as "AI-ready design systems" with brand-derivation surfaces (verify against current Supernova framing per §1.28d's open verification flag); **Backlight** has a brand-derivation flow; **Tokens Studio** has the graph engine that custom MCP wrappers (per 34 §5) expose to AI clients for engine-shaped audits.

As of mid-2026, none is fully sufficient for white-label-for-resellers at portfolio scale. The shared gaps:

- **Validation surface is thin.** Vendors expose the derivation logic but don't ship the per-brand QA surface that catches contrast regressions across modes, content-shift regressions on the per-platform output, motion regressions where the brand's chosen motion duration breaks one of the system's interaction patterns. The QA layer is custom regardless.
- **Onboarding pipeline is custom.** Vendors expose the brand-input surface but don't integrate with the agency's brand-onboarding runbook (the input-collection meeting, the engine invocation, the handoff package generation). The pipeline is custom regardless.
- **Per-reseller MCP surface is custom.** Per 34 §5 — vendors don't ship per-reseller MCP servers exposing each reseller's structured contract. White-label-for-resellers engagements that want per-reseller AI-readiness ship custom MCP wrapping per reseller (or per reseller cohort).

The practice's bet: native vendor support lands in 2026–2027; the AI-readiness commercial pressure is real and the engineering work is bounded. Until then, the engine is custom work — meaningful but bounded; bridge investment, not the long-term answer.

---

## 4. Headless-vs-opinionated for white-label

### The visual-vs-behaviour layer split

White-label products face a tension: resellers (and bespoke clients on starter foundations) want to override surface elements (visual layer — color, typography, spacing, radius, motion) without overriding behaviour (interaction layer — keyboard model, focus management, ARIA semantics, error states, validation contracts). The headless-component architecture is the modern answer.

**The split that works:**

| Layer | Owner | Reseller authority | Examples |
|---|---|---|---|
| **Behaviour** | System (non-negotiable) | None | Keyboard model, focus trap, focus restoration, ARIA semantics, state machine for composite widgets, RTL handling, i18n rendering contract, a11y-name computation |
| **Visual** | Reseller (bounded by Theme Schema) | Bounded | Color, typography, spacing, radius, motion duration / easing, iconography selection, surface elevation |

The behaviour layer carries the platform's accessibility liability; the system owns it absolutely and resellers cannot override it. The visual layer carries the reseller's brand expression; the reseller authors against it within the bounds the schema defines.

### Why the split matters for white-label specifically

The split is what makes white-label-for-resellers commercially viable.

A reseller that can override the keyboard model breaks accessibility across the platform. The reseller has neither the expertise (most reseller brand teams aren't accessibility specialists) nor the testing surface (the four-engine × four-AT matrix per 32 §2.3 + 28's web-accessibility-implementation framing requires dedicated tooling and dedicated time) to do this safely. If the reseller modifies focus management to suit a brand expression, the platform-level a11y conformance breaks; the platform is liable; the reseller is not. The economic and legal asymmetry forces the system to retain behaviour.

A reseller that can override the visual layer expresses brand without compromising the platform's contract. The reseller's brand color, typeface, radius, and density all flow through the engine's output into the rendered components; the reseller's brand is visible; the platform's behaviour is preserved. The split is what allows resellers to feel branded without inheriting accessibility liability.

The split also clarifies the reseller's economic relationship to the platform. The platform charges for the operating capability (the engine, the schema, the validation, the SLAs); the reseller pays for brand expression. Both sides understand what they're paying for.

### The headless-component implementation pattern

The system ships a component library where each component is composed of two layers:

- **A headless behavioural primitive.** Radix UI's `Dialog` primitive, React Aria's `useDialog` hook, Ariakit's `Dialog` component, Ark UI's `Dialog` machine. The primitive owns the keyboard model, the focus trap, the ARIA semantics, the state machine. It ships unstyled; consumers cannot override the primitive's behaviour.
- **A visual layer that consumes the Theme Schema.** The agency builds the visual layer once against the engine's reference brand; the engine generates per-reseller visual rendering by substituting the reseller's brand tokens for the reference brand's tokens. The visual layer is parameterised against the schema's primitives — color tokens flow from the engine's OKLCH-derived ramp; spacing tokens flow from the brand's density step; radius tokens flow from the brand's radius primitive; typography tokens flow from the brand's typeface stack.

The component the platform ships is the composition. The behavioural primitive is shared across all resellers; the visual rendering is per-reseller. Resellers modify the visual layer's parameters by modifying their schema input; resellers cannot modify the behavioural primitive at all.

### The opinionated-component case for as-starter

White-label-as-starter doesn't necessarily need headless. The starter ships components with visual defaults; the bespoke engagement modifies the visual layer during the engagement. Opinionated components work for as-starter because the visual modification happens at design time (in Figma; in the engagement's component code) rather than at runtime (per reseller, automatically). The headless discipline is over-engineering for as-starter — adds complexity without commensurate benefit.

The practice's discipline for as-starter (Prism2 specifically): keep the kit's components opinionated. The kit ships with the agency's reference visual baseline; engagements modify the baseline during the engagement; the kit's value is in the architectural shape (the token tier discipline; the documentation pattern; the contribution model) more than in the visual specifics. Going headless on the kit introduces architectural complexity that the typical as-starter engagement doesn't benefit from.

### The hybrid

Some engagements ship a starter with headless primitives where the bespoke engagement is expected to need cross-product brand variation later. The hybrid is the conscious bet on future needs; should be priced as such.

The pattern: Prism2 today ships opinionated components (per the as-starter shape); a hypothetical Prism3 could ship headless primitives + a thin opinionated layer (per a hybrid shape that supports both as-starter use *and* per-engagement reseller-platform shipping). The hybrid is real but should be a deliberate practice direction, not the unstated default. Going hybrid means the kit's complexity rises; the maintenance burden rises; the agency is investing in a future commercial capability (white-label-for-resellers) the practice may or may not actually want to ship.

### The 2026 tooling reality

The headless-component landscape evolves quarterly; specific framework support shifts. Mid-2026 reality:

- **Radix UI.** The dominant choice for React-based engagements. Comprehensive primitive surface; mature a11y semantics; large community. The practice's default for new headless white-label work in React.
- **React Aria (Adobe).** The cross-framework alternative. Adobe's research-backed a11y model; framework-agnostic core (`react-aria`) with React-specific bindings (`react-aria-components`); pairs with Adobe Spectrum if the practice wants the visual layer prebuilt. Default for engagements where the practice wants Adobe's a11y rigor explicitly.
- **Headless UI (Tailwind Labs).** Lighter than Radix; stronger pairing with Tailwind. Adequate for engagements that have committed to Tailwind for the visual layer.
- **Ariakit.** Mature, comprehensive, less commercially backed than Radix or React Aria. Reasonable choice when team familiarity favours it; the documentation is excellent.
- **Ark UI / Park UI.** Cross-framework headless logic (built on Zag.js state machines) with Vue, Solid, Svelte, React support. Default for engagements that need cross-framework primitives — mainly those shipping to multiple JS frameworks simultaneously (less common, but the right answer when needed).
- **Reach UI.** In maintenance mode; not recommended for new work.

Verify the framework's current state per project; the headless-library landscape has historically shifted faster than other DS-tooling layers. The architectural shape (behaviour layer in the headless primitive; visual layer parameterised against the Theme Schema) is durable across whichever library wins the next round.

---

## 5. The commercial shape of white-label engagements

### Two shapes price differently

The synthesis-ready artefact for this section is a comparison table laying out the SOW shape, retainer pattern, and onboarding pricing for the two white-label shapes side by side. This is the second of the file's two synthesis-ready artefacts (after §3's decision tree).

| Dimension | White-label-for-resellers | White-label-as-starter |
|---|---|---|
| **Build SOW shape** | Foundations (~150 hrs) + Engine + Schema (~150–300 hrs) + Reference component library (~250–400 hrs) + Onboarding pipeline (~80–150 hrs) + First 3 reseller integrations (~80–160 hrs total). Total: **600–1,090 hrs**. | Standard 00d Pattern 1–5 hours per engagement; the kit doesn't change the SOW shape but compresses foundation / token / initial-component-design phases. Per 00d: standard build at **300–700 hrs** depending on pattern. |
| **Run SOW shape** | Recurring brand-onboarding retainer + engine-maintenance retainer + per-reseller signup fees. Total typical Run: **~30–80 hrs/month** plus **per-reseller signup fees**. | Optional retainer per 00d's three productisable post-Build offerings (Run-phase retainer, quarterly governance review, Ambassadors program). Kit doesn't directly affect Run. |
| **Onboarding pricing model** | Per-reseller signup fee tiered by brand complexity: simple = $5k; standard = $12k; complex = $25k+. Plus per-reseller monthly retainer for engine access ($1–5k/month). | N/A — the kit is agency-internal; clients don't onboard against it. |
| **Retainer SLAs** | Brand-onboarding SLA (new reseller onboarded within X days); engine availability SLA (engine generates valid output 99.x%); schema-evolution coordination (schema changes coordinated across resellers within the deprecation window per 24). | Standard retainer SLA per 00d's Run-phase retainer (response time, monthly hours, governance facilitation). |
| **Commercial premise** | **Recurring brand-onboarding revenue.** The engine + schema + retainer is the commercial wedge; without it, the platform doesn't operate and the agency's revenue stops at Build. | **Internal velocity.** The kit reduces per-engagement startup cost across the practice; the agency's commercial benefit is more engagements per practitioner per year, not direct kit revenue from clients. |
| **IP transfer at handoff** | Engine + schema + reference library transfer to the client per 32 §1's failure-mode catalogue (the client owns the system instance from day one). The brand-onboarding runbook may transfer or stay agency-internal depending on contract. | The kit stays agency-internal; the engagement's deliverable transfers to the client (engagement-specific tokens, components, documentation). The kit-side IP is the agency's. |
| **00d Pattern fit** | None of Pattern 1–5 fits cleanly. Add **Pattern 6 — White-label / reseller platform**. | Existing Pattern 1–5 with kit acceleration. Most often Pattern 1 (Product-support component build) or Pattern 5 (Brand → Digital extension). |

### Build SOW shape for for-resellers

The Build SOW prices six discrete deliverables. Each itemised explicitly so the client sees what they're paying for and the practice can defend the hours when scoping conversations push back.

1. **Foundations.** ~150 hours. Token primitives — primitive color (per 31), spacing scale (per 22), motion primitives (per 18-21), iconography baseline. The same foundations that any DS build needs.
2. **Engine + Schema.** ~150–300 hours. The OKLCH transforms; the contrast-pinning logic; the schema design and validation; the cross-platform output discipline. The dominant engineering line item.
3. **Reference component library.** ~250–400 hours. The component set rendered against the engine's reference brand. The library demonstrates the engine works; the library is what resellers' implementations will look like with their own tokens.
4. **Onboarding pipeline.** ~80–150 hours. The brand-input collection tooling (form / CLI / Figma plugin); the engine invocation flow; the per-reseller QA pipeline; the handoff package generation. The pipeline is the practice's productised standardisation surface — it's how the runbook executes.
5. **First three reseller integrations.** ~80–160 hours total. The engine's stress test; the practice learns where the schema is under-determined and where the engine's output needs human override before the reseller-onboarding cadence accelerates.
6. **Documentation and `.ai.json` registry.** ~60–100 hours. Per 30 — the AI-readability layer for the platform. Each reseller's `.ai.json` is generated by the engine alongside the brand assets (per §7); the documentation pattern uses 29's per-component template instantiated against the engine's reference brand.

Total Build: roughly **770–1,160 hours** depending on engagement complexity and reseller count at launch.

### Run SOW shape for for-resellers

The Run SOW prices three commitments and the recurring revenue model.

1. **Brand-onboarding retainer.** ~10–30 hours/month for the brand-onboarding designer (scaling with the reseller list — first wave at 0.25 FTE; mid-portfolio at 0.5 FTE; mature portfolio at 1 FTE depending on reseller count). Covers per-reseller input-collection meetings, engine invocation, QA pass, handoff. The runbook makes this work scalable; without the runbook, every reseller is bespoke and the retainer doesn't operate.
2. **Engine-maintenance retainer.** ~20–40 hours/month for the engine maintainer. Covers schema evolution (new fields requested by resellers, deprecated fields aged out per 24's deprecation window); engine bug fixes; per-platform output regression testing; new framework / platform support as the system extends.
3. **Per-reseller signup fees.** Tiered by brand complexity:
   - **Simple brand** (primary color + logo + typeface): **$5k**.
   - **Standard brand** (adds neutral hue + radius + density): **$12k**.
   - **Complex brand** (adds custom motion + custom iconography + bespoke voice surface for AI assistants): **$25k+**.

Per-reseller monthly retainer for engine access: **$1–5k/month** depending on reseller scale and the platform's pricing model (some platforms charge end-customer fees that subsume the retainer; others keep the retainer separate). The retainer model is negotiated in the platform-agency contract; the per-reseller pricing is the platform's commercial decision and the agency typically advises rather than dictates.

### The retainer SLAs as the load-bearing decision

Without SLAs, the retainer is "we'll help when you need it" — which doesn't bind to a number and which the client can't price against the recurring revenue. The SLAs are how the retainer becomes a commercial commitment.

The three SLAs that have to be in the contract:

1. **Brand-onboarding SLA.** A new reseller is onboarded — engine invocation complete, QA pass complete, handoff package delivered — within **X business days** of contract signature (typically 5–10 days for a standard brand; 10–15 for a complex brand). The SLA defines what the reseller can expect; the agency's runbook capacity has to support it; if the runbook can't, the agency renegotiates the SLA, not the runbook.
2. **Engine-availability SLA.** The engine generates valid output for X.X% of invocation requests in any 30-day window (typically 99.5–99.9%). Defines what "the engine works" means; the validation tooling per §3 has to support it.
3. **Schema-evolution coordination SLA.** Schema changes are announced **N business days in advance** (typically 30–60), coexist with deprecated fields for **M deprecation cycles** (typically 2–3 release cycles per 24's deprecation window), and migration guidance is published with the announcement. The SLA prevents the agency from making schema changes that strand resellers; it forces the agency to plan schema evolution as a practice rather than as ad-hoc engineering.

The SLAs are negotiable per engagement; the practice's discipline is to start at these defaults and renegotiate only against documented constraints.

### The brand-onboarding pricing model — the load-bearing pricing decision

Per-reseller signup fees vary widely in the field. The practice's discipline: tier the brand by complexity; the complexity tier maps to the engine's input-set scope per §3; the more inputs, the more brand-validation work; the higher the fee.

The three tiers are calibrated against the engine's input set:

- **Simple** (3 inputs: primary color + logo + typeface). $5k. Engine invocation is straightforward; QA pass is short (~2 hours); handoff is light. Profitable at $5k with 8–10 hours of agency time.
- **Standard** (5 inputs: simple + neutral + radius + density). $12k. Engine invocation is straightforward but schema validation has more edges; QA pass is longer (~4–6 hours); handoff is standard. Profitable at $12k with 12–16 hours of agency time.
- **Complex** (7+ inputs: standard + custom motion + custom iconography + voice surface for AI assistants per 25 / 26 / 27). $25k+. Engine invocation may require per-reseller engine extension; QA pass is longest (~8–12 hours); handoff includes bespoke documentation. Profitable at $25k with 20–30 hours of agency time, with reasonable margin for the per-engagement escalation.

The tiers compose: a reseller can move from simple to complex over time; the per-tier upgrade fee is the difference plus a $2–3k upgrade-coordination fee. The model creates a glide path the platform's commercial team uses to grow account value over reseller lifecycle.

### How for-resellers connects to 00d's run-phase pricing gap

White-label-for-resellers is the practice's clearest example of an engagement that *forces* the run-phase pricing question. The engine doesn't operate without ongoing maintenance. The schema doesn't evolve without coordination. The resellers don't onboard without the runbook. The Run phase is not optional — the engagement's commercial premise depends on it.

The retainer pattern that for-resellers articulates generalises. The same shape — three discrete commitments (brand-onboarding / engine-maintenance / schema-coordination), each with an explicit SLA, each with an hour estimate, all priced as a recurring monthly retainer — applies with adjustments to bespoke engagements where the practice wants to ship a Run-phase retainer per 00d's three productisable post-Build offerings. The bespoke version names different commitments (system-evolution coordination, governance facilitation, per-component contribution review) but the *shape* — three commitments, three SLAs, three hour estimates, recurring retainer — is portable.

The practice that has shipped a for-resellers retainer once has the shape internalised. Pitching the bespoke retainer becomes easier because the agency has lived through the retainer-pricing conversation in a forcing context (where the client had no choice but to engage the question). Pitching becomes more credible because the practice can reference the for-resellers retainer as evidence the model works.

### Pattern 6 — White-label / reseller platform

The practice should add a sixth pattern to 00d's Pattern 1–5:

**Pattern 6 — White-label / reseller platform.** A platform shipping to multiple unknown future resellers via a brand-generation engine. Pattern 6 is structurally different from Pattern 1–5 because it includes a recurring Run-phase retainer that the existing patterns treat as optional. The Run phase is the engagement's commercial premise.

**Phase scope.** Discovery + Foundations + Engine + Schema + Reference component library + Onboarding pipeline + Documentation + AI-readiness + Build-side validation. Run-phase: brand-onboarding retainer, engine-maintenance retainer, schema-coordination retainer.

**Hour ranges.**
- Build (engine + schema + reference library + onboarding pipeline + first 3 resellers): **770–1,160 hrs**.
- Run (per month): **30–80 hrs**.
- Per-reseller signup fee: **$5–25k+** depending on complexity tier.

**What is almost always out of scope:** Reseller-side product development (the agency builds the platform's white-label capability; the platform's product team uses the capability for product surfaces); brand acquisition / brand-design work for individual resellers (resellers supply brand inputs; the agency doesn't design reseller brands).

**Key complexity drivers.** Reseller count at launch and projected within 18 months (drives engine break-even calculation); brand complexity tier mix (drives runbook hour estimates); per-platform output count (web only is cheapest; cross-platform output adds engineering effort); regulatory surface (some platforms ship to regulated industries — healthcare, financial services — where per-reseller validation has to clear regulatory thresholds, raising QA hours significantly).

---

## 6. Prism positioning closure — resolving 09 §3.2

### The conflict

09 §3.2 has named the unresolved positioning question for the full life of this knowledge base. Prism is alternately called a "design system" (in some VML internal materials) and an "internal UI Kit and set of tools" (in others). The deck says DSes are *not* UI Kits. The conflict has been open across the corpus.

### The resolution this file lands

**Prism2 is properly described as a white-label-as-starter foundation + starter library, not a finished design system, and not a multi-tenant white-label-for-resellers platform.**

The reasons are operational. Prism2 ships:

- A token foundation with 219+ semantic tokens (per 00b) — the foundation is mature.
- A Figma component kit with multi-theme support (light/dark/wireframe) and components built on Figma Variables and auto-layout — the design-tool side is mature.
- A React component library "in development/evolution" (per 00b) — the coded counterpart is partial.
- An accelerator for the early stages of bespoke client engagements (per 00b's "starting from a more mature baseline") — the engagement role is established.

Prism2 does *not* ship:

- A brand-generation engine that derives reseller brands from primitive inputs.
- A Theme Schema contract validating arbitrary future brands against the engine's output discipline.
- A per-reseller onboarding pipeline that operates without bespoke per-reseller agency intervention.
- A multi-tenant rendering capability that lets a single platform serve N resellers from one kit instance.

The features Prism2 ships position it as a **starter**. The features it does not ship position it as **not for-resellers**. The two-shape framing per §2 lets the practice describe Prism2 without contradiction: it's a white-label kit because the agency is white-label-shaped — agency-internal, brand-agnostic, designed to apply across many brands over time — but it's *as-starter*, not *for-resellers*. The two halves of "white-label" are different shapes; Prism2 is one shape and not the other.

### The technology-team-adoption gap as the load-bearing constraint

Per 00b: Prism2 is "primarily realized as a Figma component kit" with "a React component library (in development/evolution)"; it is "not formally adopted by VML's technology teams — which limits its use on engagements where design and dev need to be tightly integrated."

This is the load-bearing constraint that holds Prism2 in the as-starter shape. Prism2 cannot become for-resellers without technology-team adoption. The reasons:

- **The engine is engineering work.** Building the OKLCH transforms, the contrast-pinning logic, the schema validation — all live in the React component library and its build pipeline. Without technology-team commitment to ship and maintain that pipeline, the engine doesn't exist in the codebase the practice can actually deliver.
- **The schema is engineering work.** The Theme Schema is a JSON contract that lives in the React library's distribution; resellers code against it; the contract evolves with technology-team coordination. Without that commitment, schema evolution is ad-hoc and the for-resellers operating model breaks.
- **The onboarding pipeline is engineering work.** Engine invocation, per-platform output generation, per-reseller asset emission — engineering tooling, not Figma-side authoring. Without technology-team ownership, the pipeline is hand-rolled per engagement and doesn't scale.

The technology-team-adoption gap is the gatekeeper between Prism2 (as-starter) and a hypothetical Prism3 (for-resellers). The gap is documented in 00b and remains the practice's most consequential structural constraint on white-label evolution.

### The Prism2 → Prism3 implication

If the practice wants Prism to evolve toward white-label-for-resellers — recurring revenue from reseller platforms; agency-level repeatable brand-onboarding capability; a productised platform offering rather than a per-engagement accelerator — Prism3 needs the engine + schema + pipeline layers that Prism2 lacks.

The investment is meaningful:

- **~300–500 hours of senior engineering** for the engine, the schema, the validation surface, the per-platform output, the cross-platform fidelity check.
- **~150–250 hours of senior design** for the reference brand, the brand-validation tooling, the per-reseller QA surface, the onboarding documentation, the runbook.
- **Technology-team commitment** to maintain the pipeline post-launch — without it, the investment decays within twelve months.

Total Prism3 investment: roughly **450–750 hours** plus standing technology-team capacity.

The payback shape is the recurring brand-onboarding revenue per §5 — a Prism3-shaped offering positions the agency to bid Pattern 6 (White-label / reseller platform) engagements directly with a productised platform rather than building each engagement's engine from scratch. The first reseller-platform engagement amortises the Prism3 investment partially; the second amortises it further; from the third on, the platform investment is paid back and every additional engagement is high-margin.

The decision is a strategic bet on the practice's commercial direction over the next 24–36 months. Building Prism3 in 2026 positions the practice for 2027–2028 reseller-platform engagements. Not building it forfeits that wedge — the practice continues to bid Pattern 1–5 engagements and ad-hoc reseller-platform builds without a productised differentiator. The decision is the practice lead's; the strategic analysis above is the practice's input.

### The right answer for now

Don't try to make Prism2 do white-label-for-resellers. Position Prism2 as white-label-as-starter honestly; price engagements that use Prism2 at standard hours per 00d's current position; track the first ~5–10 engagements where Prism2 is formally used to build the empirical case for the kit's actual time savings.

If the data supports white-label-for-resellers as a future practice direction — if reseller-platform engagements appear in the pipeline; if the agency's commercial team starts seeing platform-shaped briefs; if the technology team signals willingness to commit to the engineering layer — scope Prism3 against the §6 framing explicitly. Don't drift toward for-resellers without the explicit decision.

### The client conversation the closure unlocks

Per 00b's current language: *"We have an internal foundation that means we're starting from a more mature baseline than a from-scratch build."* Honest and useful for as-starter engagements.

The closure adds the engagement-shape clarification: *"Prism2 is our white-label-as-starter foundation — it accelerates the early stages of your bespoke build. It is not a multi-tenant reseller platform; if your brief includes shipping to multiple unknown future resellers via a brand-generation capability, the engagement is a different shape — Pattern 6 — and a different price. We can scope either; we shouldn't conflate them."*

The clarification prevents the conflation that has caused 09 §3.2's positioning conflict to persist. Account leads who know the two shapes can ask the right scoping questions early; clients who hear the two shapes know which one their brief is asking for; the practice's commercial model has two distinct entry points instead of one ambiguous one. The positioning conflict closes because the framing is no longer ambiguous — Prism2 is one shape, the hypothetical Prism3 is the other shape, and the practice articulates both.

---

## 7. Team, governance, failure modes, AI-readiness, and the See-also

### Team shape for white-label-for-resellers

The Build phase team includes a senior DS architect (engine + schema + composition rules); a senior DS engineer (engine implementation; per-platform output; cross-platform fidelity); a senior visual designer (the reference brand; the brand-validation tooling); a senior accessibility specialist (the behaviour layer's a11y contract; the cross-engine matrix per 28); a project manager. Roughly: 5-person production core plus PM coverage, scoped at ~60–80% allocation across the 12–24 week Build.

The Run phase team is smaller and shifts roles. An engine maintainer (typically 0.5 FTE for a portfolio of 10–30 resellers; scales with reseller count); a brand-onboarding designer (typically 0.5 FTE for the first wave of resellers; scales toward 1 FTE as reseller count grows past 20); a part-time accessibility specialist (per-reseller validation as resellers onboard, ~5–15 hours per reseller depending on complexity tier); a project manager (typically 0.25 FTE for ongoing coordination). The Run team is the agency's brand-onboarding capacity; its hour estimates determine the retainer's cost basis.

### Team shape for white-label-as-starter

Smaller on the agency side because the engagement is a single client's bespoke build with the kit accelerator. Standard 00d team composition (senior visual designer + senior UX designer + design technologist + PM + part-time accessibility specialist) plus an **agency-internal kit maintainer** typically allocated 0.25 FTE across all engagements that use the kit, supporting kit evolution and cross-engagement learnings.

The kit maintainer role is the as-starter shape's distinctive staffing line. Without the maintainer, the kit decays — engagements modify the kit's tokens and components; the modifications don't fold back; the kit drifts from fielded systems; new engagements start from a kit that's increasingly stale. With the maintainer, kit evolution is a standing capacity; cross-engagement learnings get back into the kit; the kit's compounding asset value persists.

### Governance for the kit (or engine) itself

**As-starter kit governance.** Agency-internal. Who owns the kit's evolution (the kit maintainer with the practice lead's review). How per-engagement learnings get back to the kit (a quarterly retro across active engagements; a documented contribution flow for engagement teams to propose kit changes). How breaking changes to the kit propagate to engagements using earlier kit versions (kit version pinning per 24's brand version pinning pattern; explicit migration windows when the kit ships a major release). The discipline mirrors 24's federated governance — local engagement autonomy within the kit's global constraints.

**For-resellers engine + schema governance.** Agency-internal *and* reseller-coordinated. The schema is the API resellers code against; schema changes are breaking changes for resellers; the deprecation window per 24 §Deprecation-as-a-window applies. The change-review process per 24 — Token PRs against the schema, technical validation + design review + impact analysis (Cascade Report) — applies with the addition of a reseller-impact analysis step. A schema change that affects all resellers requires an explicit migration window; a schema change that affects new resellers only can land faster but still announces in advance.

The reseller-impact analysis is the for-resellers-specific addition. Before a schema change lands, the engine simulates the change against every existing reseller's brand input; the simulation surfaces which resellers' generated assets shift; the change-review process either accepts the shift (because all affected resellers are in the migration window) or scopes the change down (to avoid affecting resellers with active SLA commitments). The Cascade Report's portfolio analogue applied to the reseller list.

### The brand-onboarding runbook as practice IP

For-resellers engagements ship a runbook the agency's brand-onboarding team follows for each new reseller. The runbook is itself practice IP — it compounds the brand-onboarding team's per-reseller capacity; it standardises the per-reseller experience; it documents the failure modes and the recovery patterns.

**Runbook contents:**

1. **Input-collection meeting.** Typically 1–2 hours with the reseller's brand owner. Capture primary color (in OKLCH or HEX with conversion path); neutral hue; typeface stack with foundry licensing confirmed; brand radius; brand density; voice tone parameter for AI-surface copy if the platform ships AI features per 25 / 26 / 27. The meeting follows a documented script; the reseller's brand owner leaves with confirmed inputs.
2. **Engine invocation.** Typically 2–4 hours of senior DS engineer time. The engineer runs the engine with the captured inputs; the engine produces the per-reseller token JSON, per-platform output (web CSS, iOS Swift, Android Kotlin), MDX docs, `.ai.json` registry per component (per 30); the engineer reviews the engine's output for schema-validation pass.
3. **Per-reseller QA pass.** Typically 4–8 hours depending on complexity tier. Verifies engine output meets contrast / a11y / visual quality bars; spot-checks rendered components against the reference; runs scanner-MCP-based a11y checks per 34 §4 across a sample of components in the per-reseller rendering; flags any engine-output edges for the engine maintainer's review.
4. **Reseller-facing handoff.** Typically 1 hour. Delivers the reseller their brand assets (the token JSON, the per-platform output files, the rendered component preview), the platform-level documentation (where the engine's documentation differs from the reference), and the support contract details (how to reach the brand-onboarding team; what the SLAs cover; what's out of scope).

Total per-reseller: **~10–16 hours of agency time** for a standard-tier brand. Pricing tiered per §5.

The runbook is also the practice's standardisation surface — every brand-onboarding designer follows the same script; cross-onboarding consistency is high; the failure modes are caught at runbook checkpoints rather than discovered ad-hoc per reseller. New brand-onboarding designers onboard against the runbook in roughly two weeks; without the runbook, onboarding to the role takes months and per-reseller variance is high.

### Failure modes specific to white-label

**Brand-validation drift.** The engine's output passes contrast / a11y rules at onboarding time; the schema evolves over time (new fields, new constraints, new validation logic); the previously-validated brand drifts out of conformance because the validation logic that approved it no longer applies. Continuous validation per 32 §5 + 24 §Cross-brand drift is load-bearing — every reseller's brand re-validates on every schema release; drift surfaces are caught at the schema-evolution coordination step.

**The engine outpaces the system.** The engine ships features (new theming dimensions, new schema fields, new derivation logic) faster than the reference component library consumes them; resellers see options the components don't render. The discipline: engine releases gate on reference-library consumption — the engine doesn't ship a new schema field unless the reference library demonstrates the field's behaviour, end-to-end. The pattern that fails: the engine team ships ambitious schema expansions that the reference library team can't keep up with; resellers get a contract that promises rendering the system can't actually deliver.

**Reseller customisation outpaces the architecture.** A reseller asks for an override the schema doesn't support; the agency makes a one-off custom build for the reseller; the one-off doesn't fold back into the engine; the architecture splits between engine-shaped resellers and one-off-shaped resellers; over time, the engine becomes a technicality and the reality is per-reseller bespoke work. The discipline: a documented "schema-extension request" process where reseller-side asks evaluate against the schema; legitimate extensions land in the schema for all resellers; one-off requests escalate to the practice lead with explicit pricing premium; the agency does not silently absorb schema-bypassing custom work.

**Brand-onboarding SLA missed.** The runbook's hour estimate is wrong (a complex brand needed 30 hours, not the priced 15); the SLA breaks; the recurring-retainer commercial shape is at risk because the cost of fulfilling the retainer exceeds the retainer's revenue. The discipline: the brand-complexity tier per §5 has to be calibrated against actual engagement data; the first 5–10 reseller onboardings are the calibration set; tiering refines per the data; resellers that don't fit the tiers get explicit pricing premium rather than absorbing the cost.

**The kit-vs-bespoke divergence (as-starter specific).** A bespoke engagement modifies the kit's tokens and components; the engagement ships; the modifications don't fold back into the kit; the kit's version drifts from the actual fielded systems. The discipline: a quarterly kit retro across active engagements per the as-starter governance pattern; the retro is the moment cross-engagement learnings either fold back or are explicitly rejected; the kit maintainer prosecutes the fold-back work.

**The "starter became a product" failure mode.** The agency's internal kit evolves to the point that it's almost a finished system; clients are charged for engagements that mostly ship the kit unchanged; the agency's commercial value-add is unclear. The discipline: when the kit covers >70% of an engagement's needs, the engagement is a thin-bespoke shape — priced lower than full bespoke (because most of the work is configuration not creation); honestly named in the SOW so the client understands they're paying for engineering judgment and integration, not creation; positioned as a *kit configuration* engagement rather than a custom build. The agency that pretends a thin-bespoke engagement is a full bespoke build is mispricing and the client will eventually figure out the mispricing.

### AI-readiness for the engine

The engine that generates per-reseller token sets should also generate per-reseller `.ai.json` registries per 30. Every reseller's brand has its own AI-readable layer because every reseller's components inherit the reseller-specific token semantic layer; the AI client that knows reseller A's brand cannot reason about reseller B's components without reseller B's AI-readable surface.

The engine's full output set per reseller:

- **Token JSON** — the reseller's per-platform token files (DTCG-conformant per 22 / 24).
- **CSS / Swift / Kotlin / framework-specific output** — the per-platform rendering of the tokens.
- **MDX docs** — the reseller's per-component documentation, instantiated against 29's per-component template with the reseller's brand visible.
- **`.ai.json` per component** — the AI-readable layer per 30; each reseller has its own registry; AI clients consume the registry to reason about the reseller's component contract.
- **Code Connect mappings** — the design-to-code bindings between Figma components and code components, per the reseller's brand.

The engine generates all five outputs from the schema input. Per 30's pipeline framing — what is generated vs. what is authored — the entire per-reseller surface is generated; the engine is the practice's most aggressive expression of the generated-from-data discipline. There is no per-reseller authoring overhead; every reseller's documentation, code, AI surface, and design-tool binding flows from one schema input through one engine.

### MCP for white-label

Per 34 — the per-engagement custom DS MCP server applies to white-label, with a wrinkle: for-resellers engagements may ship a *per-reseller* MCP surface where each reseller's MCP exposes their brand's token catalogue + component contract.

The practitioner's AI client connects to a **platform-level MCP** (the engine's structured contract; the schema; the cross-reseller composition rules) plus a **per-reseller MCP** (the specific reseller's brand-rendered components-as-data). The composition is what the practitioner uses to reason about both the platform's invariants and the reseller's specific instantiation.

The engine generates the MCP server's configuration alongside the brand assets — the per-reseller MCP shape is the schema-derived MCP shape with the reseller's brand applied; the AI client sees a structured surface that names the reseller's components, exposes the reseller's tokens, surfaces the reseller's usage guidelines (where the schema permits per-reseller usage variations).

As of mid-2026, no white-label platform ships per-reseller MCP natively. The practice's bet, consistent with 34 §5: this lands in 2026–2027 alongside vendor-native MCP surfaces from Specify / Knapsack / Supernova / Backlight. Until then, per-reseller MCP is custom wrapping work — bounded but not free.

### See also

- **00b** (agency context) — Prism2 framing → 33 §6 closes the positioning. The technology-team-adoption gap is the load-bearing constraint that holds Prism2 in the as-starter shape.
- **00d** (commercial model) — white-label kit commercial question → 33 §5 articulates the answer. The Run-phase pricing gap closes for white-label-for-resellers via the recurring brand-onboarding retainer.
- **02 §6** (design foundations / theming dimensions) — white-label as Curtis's seventh theming dimension → 33 productises it as an engagement type rather than only an architectural axis.
- **24** (tokens at scale) — the Generative Token pattern, the Theme Schema as contract, multi-collection-not-multi-mode for brand → 33 §3 architecture decision tree applies the architecture to the engagement-shaping question.
- **30** (generated-from-data documentation) — AI-readiness pipeline → 33 §7 white-label AI layer applies the pipeline per-reseller.
- **32** (auditing design systems) — continuous validation pipeline → 33 §7 brand-validation drift failure mode + per-reseller validation as the audit's white-label extension.
- **34** (MCPs for DS practice) — workstation MCP stack + custom DS MCP server → 33 §7 per-reseller MCP shape extends the custom DS MCP server's surface to the per-reseller axis.
- **07** (governance and adoption) — contribution flow + governance → 33 §7 schema governance applies the contribution model to the for-resellers schema.
- **08** (ongoing maintenance) — Run phase → 33 §5 articulates white-label-for-resellers' recurring retainer as the practice's clearest Run-phase shape.
- **17** (a11y annotation contract) → 33 §4 behaviour layer's a11y contract is the non-negotiable system-owned surface in the headless split.
- **28** (web a11y implementation) → 33 §4 cross-engine × cross-AT matrix is the platform's accessibility test surface that resellers cannot override.

---

## References

The white-label DS literature is sparse — most public writing focuses on the multi-brand architecture without articulating the engagement shape. References below are organised by section.

### White-label architecture and Generative Token precedent

- **Adobe Spectrum's brand derivation** — `spectrum.adobe.com`. The light/dark math; the OKLCH-derived ramp logic; the contrast-pinned palette discipline. Verify the canonical documentation page; Spectrum's docs are reorganised periodically.
- **IBM Carbon's contrast-pinned palettes** — `carbondesignsystem.com`. The foreground / background pair contract; the per-mode contrast-pinning across the full palette.
- **Tokens Studio's graph engine** — `tokens.studio`. The dependency-graph view that the brand-generation engine's MCP wrapper exposes to AI clients per 34 §5.
- **Style Dictionary** — `styledictionary.com`. v4 / v5 resolver and dependency-graph surfaces; the build pipeline that produces per-platform output for the engine.

### Headless-component libraries

- **Radix UI** — `radix-ui.com`. The dominant React-headless choice as of mid-2026.
- **React Aria (Adobe)** — `react-spectrum.adobe.com/react-aria`. The cross-framework headless logic with Adobe's a11y rigor.
- **Headless UI (Tailwind Labs)** — `headlessui.com`. Lighter; pairs with Tailwind.
- **Ariakit** — `ariakit.org`. Comprehensive headless logic; well-documented.
- **Ark UI / Park UI** — `ark-ui.com`, `park-ui.com`. Cross-framework headless logic via Zag.js state machines.
- **Reach UI** — `reach.tech`. In maintenance; not recommended for new work.

### Embedded white-label / reseller platforms

- **Stripe Connect Embedded Components** — `docs.stripe.com/connect/embedded-components`. The canonical embedded-platform white-label surface; verify current capability against the live docs.
- **Plaid Link** — `plaid.com/docs/link`. Bank-connection white-label surface; brand-tokenisation surface for embedded use.
- **Shopify themes / Polaris** — `shopify.dev/docs/api/themes`, `polaris.shopify.com`. The merchant-side white-label theme architecture; the platform-side Polaris design system.
- **Mailchimp's email-template themes** — verify current developer documentation; Mailchimp's theme architecture has shifted with the Intuit acquisition.
- **ChannelEngine, ShipStation, BigCommerce stencil themes** — varying levels of white-label tokenisation; useful comparative references.

### Multi-brand DS governance and the architectural primitives

- **Multi-Brand Governance source (Apr 2025)** — internal source material referenced in 24. Verify the canonical citation against the practice's source-text directory.
- **EightShapes catalogue (Nathan Curtis)** — `medium.com/@nathanacurtis`. The seven theming dimensions per 02 §6; the components-as-data writing per 03 / 24; the multi-brand theming sequence per 02. White-label-specific writing is sparser but adjacent material informs the architectural approach.
- **Couldwell, *Laying the Foundations* (2019)** — token foundations, naming, structure. Pre-Variables and pre-DTCG; architecturally portable but the implementation details are dated.
- **Brad Frost** — `bradfrost.com`. Occasional white-label-relevant posts; multi-brand theming writing where it exists.
- **Marcin Treder / UXPin** — historical writing on agency starter kits and design-system maturity. Pre-2020 vintage; cite the patterns, not the snapshots.

### Vendor design-token platforms (engine-relevant)

- **Specify** — `specifyapp.com`. Primitives-to-semantic-layer derivation; verify current capability surface and pricing.
- **Knapsack** — `knapsack.cloud`. Design-token automation approaching engine functionality.
- **Supernova** — `supernova.io`. "AI-ready design systems" positioning per §1.28d; verify current framing.
- **Backlight** — `backlight.dev`. Brand-derivation flow; mid-2026 vendor.
- **Tokens Studio** — `tokens.studio`. Already cited above; the graph engine.

### Verification notes

- All "as of mid-2026" claims about headless-library landscape, vendor-native engine support, per-reseller MCP availability, and platform pricing reflect mid-2026 platform state. Verify against current docs before treating any specific claim as load-bearing in client work.
- The "10% of the first reseller's cost" figure (per Adobe Spectrum / IBM Carbon precedents) is widely cited in the field but not trivially verified against a single primary source. Verify against current Spectrum / Carbon documentation before quoting in client work; this is a §1.30-residual flag for the next housekeeping pass.
- Vendor-native engine support from Specify / Knapsack / Supernova / Backlight is the practice's bet for 2026–2027; track quarterly.
- The Theme Schema contract and the brand-generation engine architecture have a year of field application at portfolio scale (since 24 landed in May 2026). The practice's first ~3–5 reseller-platform engagements should track actual engine-vs-no-engine break-even points; the five-reseller break-even per §3 is an observation-grounded estimate, not an empirically-verified one. Refine in next file revision once empirical data exists.
- The brand-onboarding pricing tiers per §5 ($5k / $12k / $25k+) are practitioner-observation calibrated, not market-research-validated. Verify against actual reseller-platform engagement pricing data as it accumulates; the tier model may shift with the data.

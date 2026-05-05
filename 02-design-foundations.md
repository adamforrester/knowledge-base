# 02 — Design Foundations

> The floor of the system. Decisions about color, typography, space, shape, motion, accessibility — encoded as tokens, named with intent, made readable to humans and machines. Foundations done well make every downstream decision cheaper; done poorly, every downstream decision is a fight.

---

## What this phase is, and why it matters

Foundations are the layer at which *intent* gets encoded. A pixel value chosen ad-hoc in a button file is a styling decision; the same value expressed as `surface-elevated-rest` and bound to a description is a *named decision* that scales. The whole system rests on whether this naming is rigorous, complete, and shared.

This phase is also the most leveraged decision point in the engagement. Token architecture decisions made in week 4 of Discovery propagate through every component, every theme, every brand, every consumer codebase, and — increasingly — every AI-generated artifact for the system's lifetime. Re-architecting tokens at month 18 is the single most expensive corrective work a DS team can undertake. Get it right early or pay later, indefinitely.

Three things that have changed since 2019, which most legacy materials don't reflect:

1. **W3C DTCG** is now the de-facto interchange standard. `$value`/`$type`/`$description` JSON is what tools should read and write.
2. **Figma Variables and modes** have replaced Sass-variable thinking as the design-tool source of truth — and made multi-theme architecture practical for the first time.
3. **Tokens are now machine-readable contracts**, not just shared values. AI agents, code generators, MCP servers, design-to-code tools all consume tokens; tokens without descriptions or with chaotic naming break those consumers silently.

The internal practice's W3C DTCG-compliant, primitive/semantic, multi-theme-from-day-one stance reflects all three shifts. Foundations work that doesn't is already legacy.

## What actually happens in this phase

Six clusters of work, run roughly in parallel. Discovery deliverables flow into all of them.

### 1. Strategic infrastructure (carried over from Discovery)
- **3–5 opinionated design principles** — drafted as hypotheses in Discovery; revisited here as decision tools that govern foundation choices. Mall's correction stands: principles will be rewritten retrospectively after the first pilot.
- **Initial KPIs** — committed at kickoff, measured continuously. Adoption %, time-to-component, accessibility conformance, brand consistency score, defect rate.
- **The system's name and identity.** A named system is adopted at higher rates than an unnamed library. (Mall, 90 Days Activities #43–49.) This is a Foundations-phase activity, not vanity.

### 2. The visual foundation primitives
- **Color** — accessible palettes structured for theming. Numeric scales (Couldwell: 50/60/70 with two digits to allow 5% half-steps), named neither poetically nor by hex. Group colors by **role** within a background context (foreground/background/border/divider/state) rather than enumerating 300 individual variables. (Lyft's "15 pinks" remains the cautionary tale — Perez-Cruz, 2021.)
- **Typography** — type scale via modular ratio (not handpicked). Heading/body/UI families. Multiple breakpoints. Density variants if the product spans data-dense and breathing-room contexts.
- **Space** — scale on a base unit (4px or 8px most common). Numbered intervals (`0_25x`, `0_5x`, `1x`, `1_25x`, `2x`...) preferred over T-shirt sizes — they handle "between sizes" cleanly where T-shirt and increment do not (Curtis, *Design Tokens*, Nov 2024).
- **Shape** — radius, border weights. Often overlooked; encodes "feel" more than designers credit it.
- **Elevation / shadow** — composite tokens with structured DTCG values referencing color and offset primitives.
- **Iconography** — robust library; flag licensing early (a recurring CareCentrix-style discovery question for a reason).
- **Motion** — *the foundation primitive most legacy materials skip*. Tokens for **duration** and **easing** belong alongside color, type, and space. Three custom easing curves (in / out / in-out) is the minimum viable system. Carbon's *productive vs. expressive* split (utility vs. marketing) is a clean way to handle the consistency-vs-expression tension at the motion layer (Head, 2020).

### 3. Token architecture and naming

The single most consequential set of decisions in the engagement. Curtis's three-tier taxonomy has won industry consensus and should be the practice's default:

| Tier | Definition | Used for |
|---|---|---|
| **Generic / Reference** | A value with no intent — `color-blue-50`, `space-1x` | Build the palette; rarely consumed directly by components |
| **Semantic** | Intent-bearing decision reusable across 2+ components — `text-primary`, `surface-elevated-rest`, `space-inline-md` | The vast majority of component bindings |
| **Component** | A token used for only one component — `button-primary-background-hover` | When theming demands per-component override and no semantic exists |
| **Composite** (DTCG) | Token whose value is a structured object referencing other tokens — typography, shadow, border | Multi-property visual decisions |

Naming principles (Curtis, *Design Tokens*, Nov 2024 — high-weight):

- **Avoid homonyms.** `display` is ambiguous. `surface-display-large` and `text-display-xl` both use `display` differently and confuse consumers.
- **Balance flexibility and specificity.** Generics favor composition; semantics favor reuse. Offer both.
- **Avoid premature optimization** — YAGNI as governance. Needed by 1 team? Don't add to Core. Needed across 7+ teams in 3+ business groups? Add it.
- **Start within, then promote across.** Component tokens stay component-scoped until 2+ components share the concept. *Then* promote to semantic.
- **Names are levels, not strings.** `system / category / property / variant / mode` (or similar) is the shape — reads as a compressed sentence (AI-Compatible Design Systems, Feb 2025): `ds-color-action-primary-surface-rest` encodes namespace/category/usage/hierarchy/element/state.
- **Tokens ≠ Variables.** Curtis's matrix is essential: tokens are versioned, multi-format, deliberately named for scale; variables are local, single-format, often chaotically named. Figma Variables become tokens *only* when treated with the discipline tokens require.

### 4. Theming
Multi-theme from day one. Defining only "light" and adding "dark" later means re-architecting every binding. Internal practice standard is to define `data-theme` (or equivalent) attribute switching, with theme-specific token values mapped semantically.

Curtis's seven theming dimensions (in ascending cost):

1. **Responsive** (mobile/tablet/desktop) — almost universal.
2. **Light/Dark mode** — table stakes by 2025.
3. **Multi-brand** (A/B/C — like T-Mobile/Metro or Ford/Lincoln) — common in enterprise.
4. **Campaigns** — temporary brand extension for marketing.
5. **Design generations** — DS2_0 / DS3_0 alongside, for migrations.
6. **White label** — extensive customization at any decision level. Highest cost.
7. **Density** (compact / cozy / comfortable) — often forgotten; matters for data-dense UIs.

Strategy: "Define the customer problems, and work back from there." Don't theme dimensions you can't justify.

**Surface as the unit of inheritance.** Components inherit their theme context from a parent surface — they're rarely themed individually. This prevents 200 components from each owning explicit dark-mode logic.

### 5. Code-side delivery pipeline

Foundations are not "done" until they reach engineers in their actual frameworks. The architecture has stabilized:

```
Figma Variables (with descriptions)
    ↓ (DTCG export — Token Forge / Tokens Studio)
Tokens (DTCG JSON, source of truth)
    ↓ (Style Dictionary)
Platform deliverables (CSS custom properties, SCSS, JS modules, TS types, iOS Swift, Android XML)
    ↓ (GitHub Actions — copycat-action or equivalent)
Consuming applications
```

This pipeline is what Mangialardi's *Design Systems for Developers* (2021) lays out, what Curtis presents in his Tokens deck, and what the AI-Compatible doc names as the bedrock of an AI-readable foundation. Most pitches show "tokens" as a Figma-side concern and don't articulate this. Internal practice should articulate it explicitly — it is what differentiates a system that reaches engineers from one that lives in a design file.

**The mobile rendering targets are not a footnote.** iOS Swift and Android XML are listed above as platform deliverables, but on a mobile DS engagement the Style Dictionary mobile transforms — Swift enums, Kotlin objects for Compose, Dart constants for Flutter — are the entire load-bearing pipeline, not an extension to a primarily web one. Token architecture decisions taken in this phase determine whether a future mobile or cross-platform extension is mechanical or a rebuild. (See 11-mobile-and-cross-platform.)

The Figma-side mechanics that feed this pipeline — Variables collection structure, primitive vs. semantic tier discipline, modes for theme/brand/density, scoping, the trade-off with Tokens Studio, and the known gaps in the DTCG round-trip — are covered in their own file. (See 12-figma-practice.)

### 6. AI-readiness layer (post-2024 standard)
- **Every token carries a `$description`.** AI-Compatible Design Systems (Feb 2025) names this as the highest-ROI single action for AI compatibility. The same description is equally valuable to junior designers.
- **Semantic naming as compressed sentence.** `surface / action / primary / rest` reads cleanly to humans and to agents.

(See 15-ai-in-ds for how DTCG tokens combine with components-as-data and structured metadata to make the system queryable by AI agents — and why the architecture, not the tool, is the durable bet.)
- **`$extensions.figma`** with `scopes` (`TEXT_FILL`, `STROKE_COLOR`) tells agents where a token is valid.
- **Multi-theme from day one** so AI output is automatically theme-compatible.

## Our POV

The CareCentrix 2026 commercial standard runs Foundations as a **4-week phase** following a 4-week Discovery, with these activities:

- Figma setup as source of truth (Variables, styles, documentation tooling).
- Naming & architecture (token naming standards; primitive/semantic structure).
- Color (full palette: primary, secondary, neutral, semantic, status; documented usage rules; WCAG-compliant contrast).
- Typography (scales across heading/body, multiple breakpoints, density levels).
- Spacing (scales spanning data-dense to breathing-room interfaces — "consistency without rigidity").
- Design tokens (color, type, spacing core; everything foundational encoded as W3C DTCG-compliant variables — "ready for consumption as your stack evolves").
- Style guide (digital style guide in Figma covering all foundational elements with usage doc).

Deliverables: color system with semantic usage, typography system with breakpoint guidance, spacing system with density variants, complete W3C DTCG-compliant token set in Figma Variables (color, typography, spacing, border, radius, shadow, grid, motion), digital style guide in Figma, accessibility standards documentation (contrast ratios, type minimums, focus state specs).

**Practice-distinctive POVs in this phase:**

- **W3C DTCG as a procurement-grade commitment.** We name the standard explicitly — Thrive (Sep 2024) talked about tokens generally; CareCentrix (Mar 2026) names DTCG. This is a real differentiator vs. consultancies that ship Figma Variables and call it done.
- **"Big levers and small dials"** as our internal vocabulary for design language (Scoping doc; aligns with Perez-Cruz's *levers and dials* though we use slightly different phrasing). Big levers = scale, density, weight. Small dials = specific typography, spacing, color values. Naming this distinction out loud structures most stakeholder reviews and keeps debates at the right altitude.
- **Embedded engineering from day one.** The token pipeline is co-designed with the consuming team — not handed off as a Figma file with the assumption engineers will figure it out.
- **Multi-theme from day one** (light/dark/wireframe; brand themes for multi-brand clients; density variants where the product spans contexts).

**Gaps in our current commercial Foundations standard, honestly named:**

- **Motion is on the token list but not in our methodology.** CareCentrix lists motion in the token set but the practice does not yet ship motion principles, motion audits, easing studies, or productive/expressive splits as foundational deliverables. Adopting Head's framework would be straightforward and would close a real gap.
- **No purpose-grouped color discipline.** We tend to enumerate palettes; Perez-Cruz's "color groups by background context" approach (15 pinks → 4 contexts) is more defensible. Adopt.
- **Token descriptions are aspirational in our current pitches.** They appear in the AI-Compatible doc as the highest-ROI single action; they don't appear as a default deliverable in CareCentrix-style proposals. This needs to flip — descriptions should be a default Foundations deliverable, not an AI add-on.
- **Code-side pipeline is implied, not articulated.** Style Dictionary, DTCG export, GitHub Actions distribution — these are standard, but our pitches don't show them as engineering deliverables. We sell Figma; we don't sell the pipeline. Adding a single "code delivery architecture" slide to the methodology would materially strengthen the procurement conversation with technology stakeholders.

## External perspectives

### Validate

- **Curtis on three-tier token taxonomy** (Generic / Semantic / Component + Composite). High-weight near-internal source. Curtis's tokens-vs-variables matrix and YAGNI naming principles align cleanly with our internal stance.
- **Curtis on theming dimensions** — seven dimensions ordered by cost (responsive → density → light/dark → multi-brand → campaigns → generations → white label) gives us a defensible structure for theming conversations.
- **Couldwell** (*Laying the Foundations*, 2019) on numeric scales, semantic-over-poetic naming, and the primitive→semantic two-tier split — pre-DTCG but the logic survives essentially verbatim into modern token thinking.
- **Frost** (*Atomic Design*, 2016) on the "subatomic" framing — *with the caveat* that this is a post-Frost industry/VML extension. Frost's atoms are HTML elements; tokens-as-subatomic is a useful overlay we own.
- **AI cluster** (Figma DS x AI 2025; Wolosin 2025) on tokens as machine-readable contracts with descriptions of intent. Validates the AI-Compatible doc's central token claim.
- **Sam Anderson** (*Design Systems are Infrastructure*, Nov 2024) implicitly: foundations are the infrastructure layer, the substrate that must work for everything above it.

### Challenge

- **Curtis on "Figma Variables ≠ tokens."** Many client teams (and many of our pitches) treat them as synonymous. Curtis's matrix is a useful pushback. Figma Variables become tokens only when treated with the discipline of versioning, multi-format export, and deliberate naming. Practical implication: if a client's "design system" is "we use Figma Variables," they have variables, not tokens. The conversation should name this gap.
- **Perez-Cruz on "levers and dials."** Useful vocabulary we should adopt verbatim. Our "big levers / small dials" language is similar but less crisp. *Size, scale, density, weight* as the four named global levers gives stakeholder reviews a shared frame.
- **Perez-Cruz on color groups vs. color enumeration.** Pushes against the default "300 hex tokens" approach. Color groups (light/dark/bright/muted) mapped to background contexts is more defensible than per-shade naming.
- **Head on motion as foundation primitive.** External pushback against the legacy view (which our pitches still default to) that motion is a component-level concern. Motion belongs in the same tier as color/type/space.
- **AI cluster on tokens-with-descriptions.** External 2025 sources have caught up to our internal AI-Compatible POV. Token descriptions are no longer a forward POV — they're table stakes.

### Extend

- **Curtis token "levels" decomposition** (system / theme / domain / group / component / element / category / concept / property / variant / state / scale / mode) gives a more rigorous vocabulary for naming hierarchies than our current internal materials. Worth adopting.
- **Perez-Cruz on "tokens, roles, values"** as a theming model — tokens are codes, roles are systematic usage, values vary by theme. Same architecture as our primitive/semantic split but the "roles" layer is a useful semantic frame for client communication.
- **Curtis on "Inverse conundrum"** — a specific pitfall in token promotion: button label inverse, checkbox check inverse, badge success icon inverse all *look* like a shared semantic but should usually stay component-scoped. Worth naming explicitly in our token guidance.
- **Curtis on density tokens** — compact / cozy / comfortable mapped to a multiplier scale (`0_5x`, `1x`, `1_25x`). Often overlooked; matters for data-dense enterprise UIs (CareCentrix's exact context).
- **Curtis on generation tokens** — `_legacy` prefix for tokens coexisting alongside current generation. Useful pattern for migrations the practice has not yet articulated.
- **Wolosin's 4-tier metadata loop** (structured metadata / Figma-native / React-native / cross-link) extends our 4-layer AI stack with more granularity on *where* metadata lives.
- **Mangialardi's GitHub Actions delivery pattern** (`copycat-action` distributing token deliverables to consumer repos) is a concrete engineering deliverable our pitches don't yet show.

## Tensions and open questions

1. **Manual extraction vs. automation.** Mangialardi (2021) argues for manual extraction early to force designer-developer collaboration and create the "API contract." Curtis-era automation tools (Tokens Studio, Specify, Figma Variables → DTCG export) have matured significantly since. Working synthesis: manual on the first sprint to negotiate the naming taxonomy; automate everything from sprint 2 onward. Naming is the negotiation; the JSON shouldn't be.
2. **Figma Variables modes vs. CSS custom properties at runtime.** Figma's Variables modes drive a particular theming model (each component carries mode metadata). Web/native apps usually theme via attribute switching at the root. The two are compatible but not identical, and the practice has not yet articulated how to reconcile them when the design tool's mental model and the runtime mental model diverge. Worth a POV. (See 12-figma-practice on the Figma side and 13-internationalization-and-rtl on multi-locale modes specifically.)
3. **"Tokens stop at component boundaries" vs. component tokens.** Curtis is explicit: component tokens exist when theming demands per-component override that no semantic supports. Many practitioners (and some of our materials) avoid component tokens to keep the system "clean." Curtis's argument is the right one — refusing component tokens forces over-promoted semantics that misrepresent intent. Our internal POV should explicitly endorse component tokens for theming, not avoid them.
4. **Motion-as-foundation, where it lives in the methodology.** Head's framework (principles → building blocks → choreography) is sound but our 4-week Foundations phase doesn't have time for a motion audit + study + token set + named effects library at the same depth as color/type/space. Pragmatic path: ship motion principles + duration tokens + 3 easing curves in MVP; defer named effects library to extended scope.
5. **Color-by-role vs. color-by-shade.** The Perez-Cruz approach (color groups + role binding) and the Curtis approach (numeric scale + semantic mapping) are largely compatible but emphasize different artifacts. The practice should pick one as the default for client-facing work and note the alternative as a stylistic choice, not present both as equally good.
6. **DTCG adoption velocity.** The W3C Design Tokens Community Group spec is still evolving (as of 2026, draft). Tooling support varies. Internal POV commits to DTCG; some clients' engineering stacks may push back. Working synthesis: lead with DTCG; have a fallback path for clients whose stack doesn't yet consume it (Style Dictionary outputs CSS custom properties / SCSS / TS regardless of source format).
7. **AI-compatibility now or later.** Internal AI-Compatible doc treats AI-readiness as a parallel layer. External 2025–2026 consensus (Figma DS x AI; Anderson; Wolosin) increasingly treats it as table stakes for any new system. The practice's commercial proposals don't yet default to shipping the AI layer; this should flip by end of 2026.

## Failure modes specific to this phase

- **62 shades of gray.** No semantic layer. Every product reaches into the primitive palette directly. Every brand refresh becomes a six-month migration. (UXPin's classic example, 2017.)
- **Tokens defined, never described.** A token without a `$description` is a value that humans and machines must guess at. Adoption stalls because consumers don't know which token applies when. Worse for AI: the agent will compose plausibly-named tokens incorrectly because it has no signal of intent.
- **Light-only architecture.** Dark mode added later requires reaching into every binding. Multi-theme from day one is materially cheaper than retrofitting.
- **Visual taxonomy without role mapping.** "Blue" is named; "primary action" is not. Refactoring brand color downstream becomes impossible without breaking text and icons too.
- **Tokens that don't reach engineers.** A Figma Variables setup with no Style Dictionary, no DTCG export, no CI delivery — the tokens "exist" but engineers can't consume them, so they hardcode. Within months, the design tokens and the production codebase have diverged.
- **Motion as afterthought.** Designers freelance animation per component, or skip it for lack of time. The product feels static and inconsistent. (Head, 2020.)
- **Levers without dials, or dials without levers.** A team that picks specific values without setting global levers gets arbitrariness. A team that sets levers without committing to dials gets vague guidance and downstream divergence. (Perez-Cruz, 2021.)
- **Component tokens refused on principle.** The system over-promotes inverse and semantic tokens to avoid "polluting" the namespace; the result is a shallow semantic layer that misrepresents real component-specific theming needs. (Curtis's "inverse conundrum.")
- **Naming taxonomy chosen before the team has tried it.** Naming is the negotiation; if the team adopts a taxonomy without working through it on real components, they will rewrite it after the first pilot — but only after thousands of bindings already use the original.
- **Foundation work treated as design-only.** No engineering presence in the token decisions. Engineers get handed a JSON file at the end and discover that half the names don't map to their build pipeline. The pipeline is foundation work.

---

*Provenance: Token taxonomy (three-tier + composite), naming principles (avoid homonyms, balance flexibility/specificity, YAGNI, start within then promote across), tokens vs. variables matrix, theming dimensions, levels decomposition, surface as inheritance unit, density and generation tokens are from Nathan Curtis (EightShapes — *Design Tokens* Nov 2024 + *Components as Data* Sep 2025 + *Operating Design Systems* workshop Sep 2023), treated as near-internal-tier weight. Numeric color scales and primitive→semantic two-tier model are from Andrew Couldwell (*Laying the Foundations*, 2019). "Levers and dials" vocabulary, color-by-role, unity-vs-cohesion are from Yesenia Perez-Cruz (*Expressive Design Systems*, 2021). Motion as foundation primitive (principles → building blocks → choreography), three-easing-curve minimum, and productive vs. expressive split are from Val Head (*Animation in Design Systems*, 2020). Token pipeline architecture and Style Dictionary as canonical tool are from Michael Mangialardi (*Design Systems for Developers*, 2021) plus Curtis. Token descriptions as highest-ROI AI action, semantic naming as compressed sentence, and `$extensions.figma` scopes are internal POV (AI-Compatible Design Systems, Feb 2025) reinforced by Figma DS x AI (2025), Wolosin (Jun 2025), and Sam Anderson's infrastructure thesis (Nov 2024). The 4-week Foundations phase, "big levers/small dials" framing, and W3C DTCG procurement standard are internal POV from CareCentrix 2026 + DS-Scoping (2026) + VML library (2024–2026).*

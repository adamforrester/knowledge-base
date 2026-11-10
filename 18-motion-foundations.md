---
type: practice-area
title: Motion Foundations
description: Motion as a first-class foundation primitive. Three tiers — token primitives and roles, motion patterns, components — with spring storage, the spatial/effects split, brand-curve guardrails, decision frameworks, a minimum viable pattern set, reduce-motion as substitution, performance budget.
tags: [extension, motion, foundations, tokens, patterns, reduce-motion]
timestamp: 2026-11-04
---

# 18 — Motion Foundations

> Motion is the foundation primitive our practice has named on every token list and shipped on almost none. This file is what motion looks like when it stops being a per-screen design choice and starts being a system primitive — the principles, tokens, motion patterns, choreography vocabulary, performance budget, and reduce-motion contract that a design system encodes once so that downstream products don't improvise it a thousand times. The implementation depth lives in 19 (web) and 20 (mobile); the designer-to-developer spec gap lives in 21.

---

## Why motion belongs at the foundation tier

The legacy framing — the one our pitch decks still default to — treats motion as a component-level concern. A button has a hover transition. A modal slides in. A toast fades out. Each component owns its motion, each engineer picks the duration, and the result is what we tell clients we don't ship: a product that *feels* different in every flow because no two screens share an easing curve.

The argument for treating motion as a foundation primitive is the same as for color and space: **consistency only emerges when the values are centralised and the choices are constrained.** A `duration/medium` token used across every entrance animation in the system is not an aesthetic preference; it is an architectural decision that makes downstream consistency cheap. The cost asymmetry is identical to accessibility — pay it once at the foundation layer, or pay it indefinitely at the application layer (see 02-design-foundations and 14-accessibility for the parallel arguments).

Head's 2020 framing — *principles → building blocks → choreography* — already lives in our methodology as a citation. The 2025–2026 field has moved past it on three specifics. First, the token tier has matured and grown a tier above it: durations and easings are no longer enough on their own, springs have a stable storage form, and multi-property motion has moved out of tokens into a separate motion pattern tier. Second, choreography has acquired a real vocabulary: AnimatePresence on web, ExitingPersistence on mobile, View Transitions across both, shared-element transitions per framework. Third, the AI-coding-agent era has made the cost of un-tokenised motion concrete: agents asked to add an animation will hallucinate a duration and an easing curve every single time unless the system gives them named tokens and patterns to compose from.

**What goes wrong when motion is per-screen, not systemic.** The product accumulates a long tail of one-off durations — 180ms here, 220ms there, 350ms for the hero — none of which are wrong but none of which feel like the same product. State changes inside a flow have inconsistent rhythm: a button responds in 150ms, the panel it opens animates in over 400ms, the toast that confirms the action fades out over 600ms. The whole sequence reads as three unrelated motions stapled together. The fix is not better design taste applied per screen; it is tokens and patterns applied at the system level.

---

## Motion principles and brand personality

A motion principle is decidable. "Motion should feel responsive" is not a principle; it is a feeling. "Interactive elements respond within 100ms; transitions that move the user's spatial frame complete within 400ms; ambient motion is paused when the page is not in focus" — those are principles. A reviewer can hold a component against them and say yes or no.

The convergent shape across mature systems in 2026 is a small set (typically four to six) of principles, each of which:

- Names a behaviour, not a vibe.
- Is decidable in review — you can tell whether a given animation honours it.
- Encodes the brand's personality in a way that survives translation across platforms.

Atlassian's *Human / Clarity / Accessible / Performant* is the canonical four-principle set in the field. IBM Carbon's *productive vs. expressive* split sits underneath it as a categorisation, not a principle — and that distinction matters.

**The productive/expressive split.** Productive motion is the motion of utility — buttons reacting, panels opening, sheets dismissing. It is short, calm, and disposable; the user is meant to move through it, not look at it. Expressive motion is the motion of brand — onboarding, hero moments, marketing pages, celebratory states. It is longer, more deliberate, and meant to be noticed. The split is load-bearing because the same easing curve cannot do both: a productive curve applied to a hero moment feels mean; an expressive curve applied to a button feels broken. **A mature motion system ships both, as two schemes over one set of semantic roles** — productive and expressive modes, not parallel names (see the easing tokens below) — and the principles tell consumers which scheme to reach for in which context.

**Where the field has diverged.** Material treats motion as continuous (every transition implies a physical relationship), while Apple's HIG treats motion as conditional (motion should defer to clarity, and reduce-motion is treated as first-class). Neither is wrong; both reflect the host platform's broader stance. A multi-platform DS resolves this by writing principles that are platform-neutral and letting the per-platform implementation files (19, 20) handle the spelling.

**Brand personality without preciousness.** The temptation in agency work is to design every motion as a brand expression. The discipline is the inverse: most motion is productive, anonymous, and the brand shows up in the *expressive* layer — the hero, the empty state, the moment of success — where the user has bandwidth to notice it. A brand that expresses itself in every button transition is a brand that has confused decoration with identity.

---

## Three tiers: tokens, patterns, components

Our May 2026 position was a three-tier *token* model — primitive, semantic, component — with composite tokens bundling duration, easing and the animated properties into a single name. The October 2026 research run corrected the shape, not the ambition. **A motion system has three tiers, but only the first of them is tokens:**

| Tier | What it holds | Where it lives |
|---|---|---|
| **1. Tokens — primitives and roles** | Single scalars and curves: durations, easing curves, springs, distances, with semantic roles aliasing primitives and a `reduced` twin for each value | The token namespace (DTCG `duration`, `cubicBezier`, `transition`; springs in `$extensions`) |
| **2. Motion patterns** | Named, multi-property motion decisions — dialog enter, sheet by edge, expand/collapse — as tracks that reference tokens, plus choreography, a reduced-motion substitute and behavioural rules | A structured spec per pattern, serialised as a sibling file to the tokens; generated into code recipes and Figma custom animation styles |
| **3. Components** | A choice of pattern per phase (`enter: pop`, `exit: pop`), and nothing else | The component's data file (see 30) |

**Why the pattern tier is not tokens.** The field arrives here by several independent routes. Material ships transition *classes* (shared axis, fade-through, container transform) rather than tokens; Fluent 2 ships motion atoms and presence components in code; Carbon is moving from primitives toward named surfaces; and the DTCG community discussion on springs (issue #429) dropped named patterns as "a naming convention, not a type" (October 2026 research run, both agents). Atlassian is the outlier: its early-access `motion.popup.enter.{top,bottom,left,right}` tokens bundle duration, curve, keyframes and fill in one token (`@atlaskit/tokens` 20.6.0). That is a pattern living in the token namespace, and it shows why the separation matters — a DTCG composite can carry one duration and one easing and bind no property, so anything with more than one property has outgrown the token layer. Eddie Lou reaches the same three levels from practice — token, pattern, behavioural — and argues that patterns "are more than the sum of their tokens" (Eddie Lou, *Motion belongs in the design system*, 2026). That is corroboration of the shape, not evidence for it.

**What this replaces.** The component tier of motion *tokens* (`motion/modal/enter/duration`) goes. A component that needs its own motion picks a pattern, and if no pattern fits, that is a signal to author a new pattern rather than a component override. Composite motion tokens are **demoted** to single-property conveniences in the shape of DTCG `transition` and Primer's `motion.transition.{hover, stateChange, enter, exit}` — a duration and a timing function, nothing more. Multi-property motion moves to patterns. Where the rest of the vault says "composite motion token" for something like `motion/modal/enter`, read "pattern" (see 21-motion-spec-and-handoff for the handoff consequence).

---

## Tier 1 — Motion tokens: primitives and roles

**The token tier we had in May is on target.** The October run tested it against the field and against a real brand inventory of about 105 production animations, and every gap the inventory surfaced turned out to be a pattern field or a deliberate exclusion, not a missing token type (October 2026 research run). What follows keeps that tier, tightens spring storage, and adds two small token families.

### Duration tokens

Every mature system ships a duration scale, and the scales converge on a working range of roughly 100–400ms with longer steps for hero and ambient motion. Carbon ships six (70–700ms); Material 3 ships sixteen (50–1000ms) (October 2026 research run, both agents). **The primitive scale runs six to ten steps, with our own names and values** — names do not travel between systems ("fast" is 70ms in Carbon and 150ms in Fluent), so borrowing them buys nothing for a brand-portable system.

Above the scale sits a small semantic role tier. The convergent shape is roughly:

- An *instant* role (50–100ms) — interactive feedback, button presses, hover states.
- A *short* role (150–250ms) — micro-transitions, state changes, single-property animations.
- A *medium* role (300–400ms) — entrance and exit animations, panel openings.
- A *long* role (500–700ms) — orchestrated sequences, full-screen transitions, hero moments.

Consumers choose among four roles, give or take one. More than six and they stop choosing meaningfully; fewer than three and the system cannot distinguish a button press from a page transition. Every role carries a **reduced twin** (see the reduce-motion section below).

**Dynamic duration scales** are an emerging refinement. Material 3's *Expressive* update (2024) introduced the idea that motion duration should scale with the distance the animation traverses — a panel sliding 100px should not take the same time as one sliding 600px. This can be encoded at the token layer (`duration/spatial-short`, `duration/spatial-medium`) or expressed as a function of distance. The implementation files (19, 20) treat the per-platform spelling; the principle at the foundation layer is that not every animation should have a fixed clock.

### Easing tokens

Easing comes as a small set of roles crossed with an intensity axis. The roles separate the *enter* curve (decelerating — the element settles into place) from the *exit* curve (accelerating — the element gets out of the way) from the *standard* curve used for in-place transitions:

```
easing/enter      → decelerating curve, ease-out family
easing/exit       → accelerating curve, ease-in family
easing/standard   → symmetric, ease-in-out family
easing/emphasised → an expressive curve for the brand-expressive layer
```

The intensity axis is the industry's personality lever: Carbon's productive × expressive, Material 3's standard × emphasized, Fluent's Min/Mid/Max, Atlassian's practical × bold (October 2026 research run, both agents). **We encode that lever as a scheme, not as a parallel set of names** — `productive` and `expressive` modes on the semantic easing and spring collections, so a pattern references `easing/enter` and inherits whichever scheme is active. That maps one-to-one onto Material 3's `MotionScheme` on Android and onto Figma variable modes. A numeric "tempo" multiplier across the whole system is a practice invention no surveyed system documents; if we adopt one, it scales primitives only.

**Calm easing as an accessibility token, not just a vibe.** Easing curves with abrupt onsets or harsh decelerations are more likely to cause discomfort in motion-sensitive users even without reduce-motion enabled. The DS should encode a *calm* easing variant for any animation that travels a long distance or is involuntary (auto-advancing carousels, pop-ups not triggered by the user). See 14-accessibility for the architectural treatment; the foundation-layer point is that this is a token decision, not a per-component judgement call.

### Brand-defined curves

No surveyed system publishes guardrails for brand-authored curves; Material 3 (`MotionScheme` is a public interface) and Apple (a custom `Spring`) are the only formal routes to brand physics (October 2026 research run, both agents). We allow brand curves, in an `easing.brand.*` primitive namespace that semantic roles may alias, gated twice. **These gates are practice positions, not cited standards.**

- **Shape.** Role compatibility (an alias of `easing/exit` must accelerate; one of `easing/enter` must decelerate). Overshoot only on spatial properties, at a bounce of about 0.4 or less — Apple's WWDC23 guidance is to be cautious above roughly 0.4, and Material 3 never lets a spatial damping ratio fall below 0.6 — and never on opacity or colour. A non-overshooting reduced twin. Recorded provenance.
- **Permission.** Which patterns may reference a brand curve. Utility and state-change patterns may not: a heavy overshoot that delights on a 400ms modal reads as a glitch on a 50ms checkbox.

Shape stops a bad curve existing; permission stops a good curve landing in the wrong place. A curve that fails a shape check is rejected by the generator. One that passes but is referenced from a forbidden pattern is a lint error, not a silent fallback.

### Spring tokens

**Springs are the default for interactive motion.** A spring conveys the physical reality that the user is interacting with — an element responds to a gesture by being pushed, not by being scheduled. Curves are still right for non-interactive, deterministic transitions; springs are right for anything driven by direct manipulation.

**Few systems tokenise springs at all.** Material 3 is the only design system that ships springs as tokens; Apple ships springs as platform presets (`.smooth`, `.snappy`, `.bouncy`), not as a system's tokens; web-first systems either have no springs or bake one into a `linear()` string (October 2026 research run; ledger-verified against the androidx source and Apple's documentation).

**Store springs as damping ratio and stiffness at mass 1.** That is exactly what Material 3's generated `ExpressiveMotionTokens.kt` and `StandardMotionTokens.kt` publish (for example DefaultSpatial: damping 0.8, stiffness 380), and exactly what Compose's `spring(dampingRatio, stiffness)` takes, with mass implicitly 1 (androidx source, verified 2026-10-14). The form converts losslessly to every other target except baked `linear()`: to mass/stiffness/damping by setting m = 1 and c = 2ζ√k; to SwiftUI's duration + bounce by d ≈ 2π/√k and bounce = 1 − ζ for ζ ≤ 1. Storing mass, stiffness and damping instead adds a degree of freedom nobody tunes and that both Compose and Figma throw away. **The claim that mature systems store mass/stiffness/damping as their primary spring tokens failed verification**; m/k/c is a platform-API form (SwiftUI, Reanimated, Flutter, Figma prototype springs), not a token-storage convention.

**Emit springs in duration + bounce form as well**, with a declared settling tolerance, for Figma, SwiftUI and motion libraries. The duration in that form is perceptual, and what counts as "settled" is unresolved in the DTCG spring discussion (#429), so the tolerance has to be stated rather than assumed.

**The spatial / effects split.** We replace the May set of three perceptual presets (snappy, gentle, bouncy) with Material 3's grid: {fast, default, slow} × {spatial, effects}. **Spatial** springs move things — position, scale, size, rotation — and may overshoot within the shape guardrail. **Effects** springs change things in place — opacity, colour — and are always critically damped (ζ = 1). The split earns its place three ways: it gives per-property easing a default (spatial properties take the spatial spring, opacity and colour the effects one), it gives reduced motion a default substitution rule (below), and it maps one-to-one onto Material 3's `MotionScheme`. The tokens stay named by perceptual outcome; the mapping table in 20 is the per-platform spelling.

**Overdamped springs (ζ > 1) are out.** Figma cannot represent them — its bounce floors at 0 — and UI tokens do not use them.

### Distance tokens

Lou puts distance and displacement at the token level, and the field shows it in two systems: Spectrum ships component-scoped distance tokens (`--spectrum-tooltip-animation-distance` at 5px, re-aliased to `spacing-75`), and Atlassian bakes distance into its keyframe names (`SlideInBottom8px` in, `SlideOutBottom4px` out) (October 2026 research run, verified against `@spectrum-css/tokens` 16.0.2 and `@atlaskit/tokens` 20.6.0). The evidence is thin but real. We add a short **motion distance scale** — three or four steps aliasing the spacing scale — consumed by pattern tracks. The enter/exit asymmetry (Atlassian's 8px in, 4px out) is encoded in the pattern, not as separate tokens.

*Decision rule:* a distance that recurs across patterns is a token; one unique to a pattern is a literal in that pattern's track. Reduced motion sets distance to zero, which is what makes a spatial track droppable without a separate twin.

### Decay tokens — optional

Deceleration rate and a rubber-band factor are tokenisable, but generated only when a brand's inventory includes custom flick surfaces. Most systems never need them.

---

## Tier 2 — Motion patterns

A **motion pattern** is a named motion decision with its own identity — "dialog enter", "sheet from bottom", "expand" — that references tokens and is picked by components. It is the layer that was missing from our model, and the place where four of the five gaps the brand inventory surfaced (brand curves aside) actually belong: scroll-triggered reveals, physics beyond presets, per-property easing and out-and-back pulses (October 2026 research run).

### What a pattern specifies

- **`phase`** — enter, exit, state change, reposition, navigate.
- **`tracks[]`** — one per animated property: `{property, from, to, distance?, duration | spring, easing, delay, layout?}`. Per-property timing is the normal case (Material's fade is 150ms in and 75ms out; Atlassian's popup enters over 150ms with an 8px slide and exits over 100ms with a 4px one), so tracks, not a single duration, are the unit.
- **`choreography`** — stagger interval, order and a total cap. Carbon's guidance — 20ms between items within a 500ms total — is the default.
- **`direction`** — axis, and whether the motion reverses on back navigation.
- **Behavioural fields** (below).

Exit is faster than enter by default. A pattern's timing is always a token reference; a literal in a track is the exception that has to justify itself.

### Behavioural rules as fields

Lou calls the behavioural level "the least documented layer … and the most important" (Lou, 2026). The way to make it real in a generated system is to make every rule a field the generator emits and the code honours, not a paragraph in the docs.

- **`interruptible`** — true means a spring primitive and velocity retargeting on platforms that offer it; false allows a timed curve. This is how a pattern declares physics intent without putting velocity in a token.
- **`skipOnRapidRepeat`** — when the same trigger fires again inside the pattern's duration (a user mashing a toggle, paging quickly), jump to the end state rather than queue. Lou names the rule; Reanimated's jump-to-end behaviour under reduced motion shows the mechanism exists. *Practice position.*
- **`reducedMotion`** — required. Either substitute tracks, or `essential: true` with a recorded reason.
- **`lowPower`** — what the pattern becomes when the platform reports animations disabled for non-accessibility reasons; Android's `areAnimatorsEnabled()` is false under Battery Saver. Default: the same as reduced. *Practice position.*
- **`iterations`** — finite by default. Anything infinite names its WCAG 2.2.2 pause/stop/hide control, since auto-playing motion beside other content that runs past five seconds requires one.

### Per-property easing and pulses are pattern tracks

Both exceed a flat token. The tempting fallback — a CSS `@keyframes` block in the component, tokenising only the total duration — hides the internal timing from Figma, from agents and from review, which is the handoff failure 21 exists to fix, in a new place. **Model both as tracks.** A pulse is a pattern with amplitude, property, duration and easing, a direction mode (alternate or mirror), finite iterations within five seconds, and a reduced fallback. Tracks also match Figma Motion's entry model, Fluent's `Collapse` (separate size and opacity durations) and Material's spatial/effects rule.

### Where patterns live

Not in the token namespace. A pattern is a structured spec per pattern, serialised as a sibling file that references tokens, and **it is the source of truth**. Per-platform code recipes and Figma custom animation styles are both *generated* from it — Figma Motion is good enough to render a pattern, not to own one (see 21-motion-spec-and-handoff for the Figma vehicle and its limits). Spring and pattern data travel in DTCG `$extensions`, since a `$type` outside the spec's list is non-conformant; if the DTCG spring discussion lands on `{bounce, duration}`, we add a transform.

### A minimum viable pattern set

Ordered by how many components each unblocks and by dependency (October 2026 research run, reconciled from both agents):

1. **Fade (enter / exit).** Tooltips, popovers, skeleton-to-content — and the universal reduced-motion substitute, so it comes first.
2. **State change / press.** Hover, focus, press, toggle, tab indicator. Effects-only, plus a small spatial spring on press. Mostly composite transitions; the cheapest pattern and the first test of the brand-curve permission guardrail.
3. **Pop / scale-fade (enter / exit).** Menus, selects, comboboxes, anchored popovers. Scale from about 0.95 to 1 plus fade, spatial/effects split, the first user of the distance scale.
4. **Dialog (enter / exit).** Scrim on effects, panel on spatial, exit faster than enter.
5. **Sheet / drawer (enter / exit, by edge).** Spring-driven and interruptible — the first pattern where `interruptible` changes the code.
6. **Expand / collapse.** Accordion, disclosure, tree. Separate size and opacity tracks; the declared layout exception (see the performance section).
7. **Toast (enter, exit, reposition).** Stack reflow is the first choreography case.
8. **Page / view transition.** Shared axis plus fade-through, mapped onto View Transitions on the web and the native navigation transitions (see 19, 20).
9. **Container transform / shared element.** Last of the transitions, because every platform now provides the mechanism; the system supplies timing and the reduced substitute.
10. **Pulse / attention** (finite), once 2.2.2 handling is in place.
11. **Progress / loading loop** (shimmer, spinner). The first infinite loop, so it ships only with an explicit pause or reduced-motion stop and a recorded 2.2.2 reading. Whether a loading indicator counts as essential under 2.2.2 is not yet settled (see 09), so we do not state a default.

Stagger is a choreography field on expand/collapse, toast and page transition, not a pattern of its own.

---

## Tier 3 — Components

A component picks a pattern per phase and passes runtime inputs — the gesture's velocity, the trigger's origin — to it. It does not own durations, easings or reduced-motion logic. That constraint is what makes the AI-agent argument work: an agent asked to "animate the modal entrance" with only primitive tokens available will pick three of them and pick differently each time; an agent pointed at the dialog pattern gets the whole choreography from one name (see 15-ai-in-ds for the broader components-as-data argument). In May we made that argument for composite tokens. It holds, one tier up.

**Pattern or component motion?** If the motion is inseparable from the component's structure — a toggle's thumb, a checkbox's tick drawing on — it belongs to the component and is specified there. Everything else is a pattern reference.

---

## Choreography and orchestration

Choreography is the cross-component layer of motion. A single button transition is not choreography; the coordinated entrance of a panel, its contents, and its dismiss button *is*.

The vocabulary the field has converged on:

- **Sequence** — animations that happen in order, one after another.
- **Stagger** — sequence with a fixed delay between siblings (a list of cards entering one at a time).
- **Parallel** — animations that happen simultaneously across multiple elements.
- **Follow-through** — an animation that continues briefly after the triggering element has settled, suggesting weight.
- **Anticipation** — a small inverse motion before the main motion, suggesting an element is preparing.
- **Settle** — the final phase of an animation where overshoot resolves.

**What gets tokenised vs. what lives in the pattern.** Stagger applied inconsistently is visibly inconsistent, so the interval is a token; the iteration — which sibling goes when, and the total cap — is a choreography field on the pattern, done at runtime by the component library (Carbon's 20ms within a 500ms total is the default). Sequence and parallel are choreography *primitives*, expressed as track delays inside a pattern, not as tokens. Follow-through and anticipation show up in expressive motion and rarely in productive motion; where a system needs them, they are tracks in an expressive pattern.

**Shared element transitions** — the same component visually persisting across a route change (a card on a list page becoming the hero on a detail page) — are the choreography pattern most consistently underspecified at the system level. They depend on per-platform primitives (SwiftUI's `matchedGeometryEffect`, Compose's `SharedTransitionLayout`, Flutter's `Hero`, the web's View Transitions API) but the *intent* is the same across platforms. The DS should name the shared-element pattern at the foundation layer; the implementation files (19, 20) document the spelling.

---

## Reduce-motion as a system contract

The architectural treatment lives in 14-accessibility. The foundation-layer responsibility is to encode reduce-motion such that no individual engineer has to remember it. **The contract is: every motion token has a reduced twin, every motion pattern declares its reduced form, and every consuming component reaches motion through patterns and tokens, never through hardcoded values.** When both halves hold, the system honours reduce-motion automatically. When either half breaks, individual engineers carry the burden — and they will get it wrong.

**The 2024–2026 refinement to our earlier position.** Our existing 14-accessibility material describes the reduce-motion fallback as collapsing durations to 0ms and easings to `step-end`. The field has moved on from that blanket treatment. The current convergent position is *informational vs. vestibular*:

- **Vestibular triggers** — large-scale translation, scaling, parallax, 3D rotation, infinite-spin — should be eliminated or replaced with a cross-fade.
- **Informational motion** — short fades, focus-state transitions, progress indicators — can be preserved at reduced amplitude or unchanged.

**Reduced motion is a substitution of properties, not just a change of values.** Our May position encoded the reduced variant per token. That is necessary and not sufficient: a token twin can make a slide shorter, but it cannot turn a slide into a fade. The systems that do this well encode it per pattern — Fluent v9 replaces an atom's keyframes with a per-atom `reducedMotion` form, Reanimated documents `BounceIn` → `FadeIn` substitution per animation, and Apple's `prefersCrossFadeTransitions` tells the app *what* to substitute (October 2026 research run). So the work splits along the reduced-motion decision framework below:

- **Value twins live in the token tier** — a `reduced` mode on the semantic motion collections: shorter durations, no overshoot, zero distance.
- **Property substitution lives in the pattern tier** — the required `reducedMotion` field. The default rule follows the spatial/effects split: spatial tracks (translate, scale, size, path, rotation) are dropped or replaced by an opacity cross-fade; effects tracks (opacity, colour) stay, at reduced duration. `essential: true` exempts a pattern, with a recorded reason.
- **Finer platform signals are a runtime choice** — iOS's cross-fade preference picks the pattern's substitute; Android's animator scale of zero and Battery Saver are honoured through `lowPower`.

The spatial/effects → reduced-motion mapping is our inference, not a cited standard; no source states it. It is defensible because WCAG's definition of motion animation excludes opacity and colour changes, which is the normative basis for substituting a fade rather than removing everything. Removing everything is the failure the global 0.01ms reset produces: context is lost and elements pop.

**Near-zero, not zero.** Where reduced motion collapses a track, collapse it to a near-zero duration rather than removing the animation, so that code waiting on a transition-end event keeps working. The global reset in 19 uses 0.01ms for the same reason; what the pattern tier replaces is the reset's *global* reach, not its near-zero value. The rationale is sound; the claim that a named system does exactly this is unverified and we do not cite it.

**WCAG criteria the tiers operationalise.** 2.3.3 Animation from Interactions (AAA) is the criterion design systems actually build to even when they do not claim AAA. 2.2.2 Pause, Stop, Hide (A) governs any auto-playing motion that runs past five seconds beside other content, which is why `iterations` is finite by default. 2.3.1 Three Flashes or Below Threshold (A) bears on cyclical patterns: a pulse or loop whose duration tokens could resolve to more than three flashes a second is a defect a CI check can catch cheaply. That check is not yet built (see 09).

**A 2026 gotcha to encode explicitly.** Browsers' View Transitions API does not respect `prefers-reduced-motion` automatically (see 19 for the spelling). Our system contract has to make this explicit: every view transition is wrapped in the reduce-motion check at the system layer, so consumers can't accidentally ship a forced animation. This is a small but load-bearing pattern.

The downstream relationship to other accessibility motion settings — Reduce Transparency, Differentiate Without Color, the broader vestibular consensus — is treated in 14. Motion is one channel among several; the system should not over-claim that respecting reduce-motion is sufficient on its own.

---

## Performance and the cost of motion

A design system that ships motion without a performance budget is shipping a regression vector. The budget is decidable, not aspirational.

**The web budget** is set by INP (Interaction to Next Paint, the Core Web Vital that replaced FID in 2024) and the LoAF API (Long Animation Frames, 2024). The architectural rule is that motion runs on the compositor thread — `transform` and `opacity` only — and never on properties that trigger layout or paint. The spelling lives in 19; the foundation-layer commitment is that the system tokens themselves only encode compositor-safe animations. A pattern that animates `height: auto` without saying so is a system failure, not a consumer failure.

**The mobile budget** is set by frame rate (60Hz baseline, 120Hz on modern hardware) and the per-platform threading model. SwiftUI and Compose handle this on a UI thread separate from app logic; Flutter has a single UI isolate that benefits from light animation work; React Native splits work across JS thread and UI thread, with Reanimated's worklets moving animations to the UI thread. The system contract is the same as on web: tokens only encode animations the platform's compositor can run cheaply.

**Encoding safety as a property.** Patterns declare which properties they animate, track by track, so safety is visible in the spec rather than discovered in a profiler. The default is `transform` and `opacity` only. **Layout animation is a declared exception, not a silent breach.** "Never animate height, width, padding or margin" is the right rule for transitions in general and the wrong rule for expand/collapse, where a change of size *is* the motion — Fluent's `Collapse` gives size its own track and duration. So a track may set `layout: true`, only in a pattern whose purpose is a size change, and it is budgeted and instant under reduced motion. The technique is per platform: animate size on small subtrees; on the web, `interpolate-size: allow-keywords` animates to `auto` but ships only in Chromium (Chrome 129+; Firefox and Safari not implemented, MDN browser-compat-data, 2026-10-14), so a measure-then-animate path or a clip/transform reveal is the portable route (see 19). Layout tracks are where a performance budget actually bites.

**The 120Hz consideration.** Modern devices ship 120Hz displays as standard. A motion that drops frames on 60Hz is jank; the same motion on 120Hz looks broken because the user's expectation of smoothness has been recalibrated. The system should treat 120Hz as the design target, not the high-end exception.

---

## Decision frameworks

**Token, pattern or out of scope?** A token is a single scalar or curve reused across contexts. A pattern has more than one property, a phase, choreography, a reduced substitute or a behavioural rule. Out of scope means the motion depends on continuous input (scroll position, gesture velocity) or is authored as an asset.

**Spring or curve for a pattern?** A spring when the motion is user-initiated, interruptible or must feel physical. A curve when it is system-initiated, fixed-length, synced with other timed media, or targets CSS-only consumers for whom `linear()`'s fixed duration is acceptable. Effects tracks inside a spring pattern can still take a curve.

**Where does a reduced-motion alternative live?** A value-only change (shorter, no overshoot, zero distance) is a token mode. A property change (movement replaced by a fade) is a pattern field. A finer platform signal (iOS's cross-fade preference) is the runtime picking the pattern's substitute.

**May this animate layout?** Only in a pattern whose purpose is a size change (expand/collapse, toast stack reflow), declared with `layout: true`, budgeted, and instant under reduced motion. Everywhere else, transform and opacity.

**Which Figma vehicle?** Variables for anything a mode should switch; a custom animation style for a named pattern designers apply; an animated component when the motion is inseparable from the component's structure; prototype transitions only for flows, with literal values until Figma binds variables there (see 21).

---

## Out of scope, by decision

Say so in the system docs, so the absence reads as a decision rather than an omission.

- **Continuous scroll-linked and parallax motion.** Scroll-*triggered* reveals are a pattern with a mandatory static fallback and reduced motion off. Continuous parallax is bespoke build work: CSS scroll-driven animation (`animation-timeline` with `scroll()` and `view()`) ships in Chrome 115+ and Safari 26 but is Firefox Nightly only and not Baseline as of 2026-10-14, Figma Motion has no scroll timeline, and WCAG's Understanding document for 2.3.3 names parallax as the canonical vestibular trigger. The tokenisable parts — magnitudes, easing across the range, a parallax ratio ceiling — live in the pattern spec.
- **Physics beyond presets as tokens.** Gesture coupling, velocity, snap points and rubber-banding beyond a factor are implementation. The pattern declares intent through `interruptible`; tokens hold only the resting spring. Very bouncy springs are a governance problem, not an encoding one.
- **Initial velocity in any token.** A design token cannot know how fast a user's thumb was moving; velocity is a runtime input.
- **Illustrative and brand-moment animation.** Lottie/dotLottie or Rive assets reference our colour and timing tokens; the token system does not produce them (see 21 for the handoff layers).
- **Overdamped springs** (ζ > 1).
- **Infinite loops by default.**
- **The operating model** — a named motion owner, system-level motion review, testing with motion-sensitive users, frame and battery budgets (Lou, 2026). These are governance, not tokens. The system can support them — emit a per-pattern performance class, flag `layout: true` tracks, list every infinite loop — but cannot supply them. Their home is 07-governance-and-adoption and 08-ongoing-maintenance.

---

## Where motion sits relative to the rest of the system

| Concern | Owner | Reference |
|---|---|---|
| Motion tiers: tokens, patterns, components | This file | 18 |
| Pattern spec as handoff artefact; Figma Motion as a generated target | 21-motion-spec-and-handoff | 21 |
| Motion in Figma Variables, Style Dictionary pipeline | 02-design-foundations | 02 |
| Per-component motion behaviour | 03-component-library | 03 |
| Reduce-motion architectural treatment | 14-accessibility | 14 |
| Mobile platform motion implementation | 20-motion-implementation-mobile | 20 |
| Web platform motion implementation | 19-motion-implementation-web | 19 |
| Designer-to-developer micro-interaction spec | 21-motion-spec-and-handoff | 21 |
| AI coding agents and motion tokens and patterns | 15-ai-in-ds + this file | 15, 18 |
| Motion ownership, review, and performance budgets as operating model | 07-governance-and-adoption, 08-ongoing-maintenance | 07, 08 |

---

## Failure modes to watch

- **Motion tokens on the list but unused.** The system ships duration and easing tokens. Components hardcode their own values. The token layer becomes documentation rather than constraint. (See 02 — this is the practice's existing gap, now more concrete.)
- **One-tier tokens.** Primitives mapped directly to component use, no semantic layer. Every consumer picks their own duration from a list of literals. Consistency collapses at scale.
- **Productive curves applied to expressive moments.** The brand is supposed to show up in a hero animation; instead it gets the same `easing/standard` as a button. The expressive scheme is missing, or a pattern hardcodes a productive curve instead of referencing a role that the scheme resolves.
- **Reduce-motion at the duration layer only.** Durations collapse to 0ms but easings and properties remain, so the animation snaps in a way that still triggers vestibular sensitivity. The contract is value twins per token *and* property substitution per pattern, not a global flag.
- **Springs simulated with curves.** A designer specs a "bouncy" interaction; the engineer approximates it with a long ease-out. The result is consistently wrong because the field-converged answer to interactive motion is a spring, and springs do not approximate from curves cleanly. (See 19, 20 for the platform spellings.)
- **Multi-property motion squeezed into a token.** A composite token is asked to carry a scale, a fade and a slide with different timings, and either carries one of them or becomes a vendor-specific bundle no pipeline can read. The motion has outgrown the token tier; it is a pattern.
- **Figma treated as the source of truth for patterns.** Custom animation styles are authored by hand in the library file and drift from code. Figma Motion renders patterns well; it should be generated from the pattern spec, not edited as the master (see 21).
- **Springs stored in a form nobody tunes.** A spring stored as mass, stiffness and damping looks more complete than damping ratio and stiffness, adds a parameter every target discards, and invites three people to tune it three ways.
- **Brand curves without permission.** A brand's overshooting curve is aliased into `easing/standard` and lands on every checkbox. Shape guardrails passed; permission was never checked.
- **AI agents producing unique durations every time.** An agent asked to add an animation generates `transition: all 0.18s ease`. Without patterns and role tokens in its context, this is the default failure mode and it accumulates faster than any human review can catch it.

---

## Tensions and open questions

1. **Productive vs. expressive as parallel token sets, or as a single set with overrides — resolved (November 2026).** Our May lean was parallel sets. The October 2026 research run converged on the other answer: the personality lever is a **scheme or mode on the semantic tier**, and patterns reference roles and inherit. It is what Material 3's `MotionScheme` and Carbon's productive/expressive matrix both amount to, it maps onto Figma variable modes, and it keeps one set of role names. The enforceability argument for parallel sets is now carried by the brand-curve permission guardrail instead: what stops an expressive curve landing on a checkbox is a lint rule on the pattern, not a separate namespace.

2. **Spring tokens as perceptual or physical.** The token name is perceptual (`spring/default-spatial`); the stored value is physical (damping ratio and stiffness), and each platform spells it differently. The risk is that the perceptual name drifts away from the physical implementation across platforms — the same spring on iOS and on Android ends up feeling different. One part of this is still open: whether Figma's spring duration is perceptual or settling time (see 09). The mitigation is the dual-vocabulary discipline in 20 (see the cross-platform spring parameter mapping table). The practice should ship a calibration test alongside the tokens, not just the names.

3. **Composite tokens vs. component-internal motion — resolved (November 2026).** The May answer was to ship composite tokens for the choreography-heavy components. The pattern tier replaces that: choreography-heavy motion is a pattern, composite tokens shrink back to single-property conveniences, and the minimum viable pattern set above is the list of what to build first. The open edge is the threshold for authoring a new pattern rather than a component-owned motion; the rule of three referenced in 03 is the working answer.

4. **Where motion principles get reviewed.** Principles only enforce if someone applies them. The DS team can ship the principle "interactive elements respond within 100ms" and the consuming product still ships a 350ms button feedback because no one held the work against the principle. Governance treatment lives in 07; the foundation-layer commitment is that principles are written in a form that can be reviewed — decidable, not aspirational.

5. **Distance tokens: alias spacing or own steps.** The distance scale aliases spacing in the recommendation above, but whether it should alias one-to-one or hold its own steps is untested against a real brand inventory (see 09).

6. **Practice positions awaiting evidence.** The overshoot cap, the brand-curve permission guardrail, `skipOnRapidRepeat`, `lowPower`, the tempo multiplier and the spatial/effects → reduced-motion mapping are positions we hold, not standards we can cite. They should be presented to clients that way until engagement use gives us evidence for or against them.

7. **Dynamic duration scales as system, not as Material-3-specific feature.** Material 3's distance-aware durations are the most actionable specific instance of this idea, but the broader principle — that not all motion has a fixed clock — applies across platforms. The practice has not yet decided whether to encode this at the token layer (additional tokens for spatial-aware durations) or as a runtime function (durations as a function of distance). Either works; the choice depends on how aggressively the DS wants to enforce vs. enable.

---

## See also

- **02-design-foundations** — where motion is named alongside color, type, space as a foundation primitive, and where the practice acknowledges the methodology gap this file partially closes.
- **03-component-library** — where motion specs were flagged as missing from component templates.
- **07-governance-and-adoption, 08-ongoing-maintenance** — the motion operating model (ownership, review, budgets) that tokens and patterns support but cannot supply.
- **14-accessibility** — reduce-motion architectural treatment, the four-layer model that this file's tokens slot into.
- **15-ai-in-ds** — named motion tokens and patterns as a prerequisite for trustworthy AI-assisted authoring.
- **19-motion-implementation-web** — CSS / WAAPI / View Transitions, the `linear()` spring revolution, library landscape, INP/LoAF, AI-agent guardrails for web motion.
- **20-motion-implementation-mobile** — primitives, springs, shared element transitions, Lottie vs. Rive, threading model, reduce-motion per framework.
- **21-motion-spec-and-handoff** — the designer-to-developer micro-interaction spec gap, what Figma Motion can and cannot specify, the pattern spec as the canonical handoff format.

---

*Provenance: Motion as foundation primitive, the principles → building blocks → choreography frame, three-easing-curve minimum, and productive vs. expressive split are from Val Head (*Animation in Design Systems*, 2020), already present in 02-design-foundations. The three-tier token taxonomy with composite tokens, the spring-as-perceptual-token discipline, the productive vs. expressive as parallel sets, the four-principle convergent shape (Human / Clarity / Accessible / Performant), and the AI-agent failure mode argument are synthesised from IBM Carbon (Productive vs. Expressive Motion, 2023–2024), Atlassian Design System (Motion principles, 2024), Material 3 Expressive (2024), the dual-agent research outputs in `_research/_inbound/2026-05-14-motion-foundations-and-spec/`, and Token Studio's composite-token treatment (2024–2025). The informational vs. vestibular reduce-motion refinement is from the dual-agent research outputs (May 2026), refining the earlier blanket position in 14-accessibility. The 120Hz design target framing and INP / LoAF performance budget are from the web implementation research output (May 2026). Performance-safety-as-property at the token layer is internal POV synthesised across the three research outputs. Token tiers, three-tier model, and composite tokens are aligned with Nathan Curtis (EightShapes — *Design Tokens* Nov 2024 + *Components as Data* Sep 2025). The November 2026 revision — the three tiers as tokens / patterns / components, composite tokens demoted to single-property transitions, spring storage as damping ratio + stiffness at mass 1 with duration + bounce emission, the spatial/effects split, distance and optional decay tokens, the brand-curve shape and permission guardrails, behavioural rules as pattern fields, reduced motion as property substitution, the layout exception, the decision frameworks, the out-of-scope list and the minimum viable pattern set — is promoted from `_research/_archive/2026-10-14-motion-tokens-and-figma-motion.md`, which reconciles the dual-agent run in `_research/_inbound/2026-10-14-motion-tokens-and-figma-motion/` and its 2026-11-04 second external half. Only claims that passed the synthesis's verification ledger are carried; the rejected ones (mass/stiffness/damping as the field's storage convention, Spectrum spring tokens, mode-swapped reduced styles, among others) are recorded there. Material 3 spring values are from the androidx `ExpressiveMotionTokens.kt` / `MotionScheme.kt` source; Spectrum and Atlassian distance and popup tokens from `@spectrum-css/tokens` 16.0.2 and `@atlaskit/tokens` 20.6.0; the bounce caution line from Apple (WWDC23, *Animate with springs*); browser support from MDN browser-compat-data (2026-10-14). The token / pattern / behavioural levels, the behavioural rules and the operating-model list are from Eddie Lou (*Motion belongs in the design system*, 2026, `_source-text/ext-motion-in-design-systems-lou.txt`), used as practitioner corroboration, not evidence. Positions flagged as practice positions in the text are ours.*

# 18 — Motion Foundations

> Motion is the foundation primitive our practice has named on every token list and shipped on almost none. This file is what motion looks like when it stops being a per-screen design choice and starts being a system primitive — the principles, tokens, choreography vocabulary, performance budget, and reduce-motion contract that a design system encodes once so that downstream products don't improvise it a thousand times. The implementation depth lives in 19 (web) and 20 (mobile); the designer-to-developer spec gap lives in 21.

---

## Why motion belongs at the foundation tier

The legacy framing — the one our pitch decks still default to — treats motion as a component-level concern. A button has a hover transition. A modal slides in. A toast fades out. Each component owns its motion, each engineer picks the duration, and the result is what we tell clients we don't ship: a product that *feels* different in every flow because no two screens share an easing curve.

The argument for treating motion as a foundation primitive is the same as for color and space: **consistency only emerges when the values are centralised and the choices are constrained.** A `duration/medium` token used across every entrance animation in the system is not an aesthetic preference; it is an architectural decision that makes downstream consistency cheap. The cost asymmetry is identical to accessibility — pay it once at the foundation layer, or pay it indefinitely at the application layer (see 02-design-foundations and 14-accessibility for the parallel arguments).

Head's 2020 framing — *principles → building blocks → choreography* — already lives in our methodology as a citation. The 2025–2026 field has moved past it on three specifics. First, the token tier has matured: durations and easings are no longer enough on their own — spring tokens and composite motion tokens are now standard. Second, choreography has acquired a real vocabulary: AnimatePresence on web, ExitingPersistence on mobile, View Transitions across both, shared-element transitions per framework. Third, the AI-coding-agent era has made the cost of un-tokenised motion concrete: agents asked to add an animation will hallucinate a duration and an easing curve every single time unless the system gives them named tokens to compose from.

**What goes wrong when motion is per-screen, not systemic.** The product accumulates a long tail of one-off durations — 180ms here, 220ms there, 350ms for the hero — none of which are wrong but none of which feel like the same product. State changes inside a flow have inconsistent rhythm: a button responds in 150ms, the panel it opens animates in over 400ms, the toast that confirms the action fades out over 600ms. The whole sequence reads as three unrelated motions stapled together. The fix is not better design taste applied per screen; it is choreography tokens applied at the system level.

---

## Motion principles and brand personality

A motion principle is decidable. "Motion should feel responsive" is not a principle; it is a feeling. "Interactive elements respond within 100ms; transitions that move the user's spatial frame complete within 400ms; ambient motion is paused when the page is not in focus" — those are principles. A reviewer can hold a component against them and say yes or no.

The convergent shape across mature systems in 2026 is a small set (typically four to six) of principles, each of which:

- Names a behaviour, not a vibe.
- Is decidable in review — you can tell whether a given animation honours it.
- Encodes the brand's personality in a way that survives translation across platforms.

Atlassian's *Human / Clarity / Accessible / Performant* is the canonical four-principle set in the field. IBM Carbon's *productive vs. expressive* split sits underneath it as a categorisation, not a principle — and that distinction matters.

**The productive/expressive split.** Productive motion is the motion of utility — buttons reacting, panels opening, sheets dismissing. It is short, calm, and disposable; the user is meant to move through it, not look at it. Expressive motion is the motion of brand — onboarding, hero moments, marketing pages, celebratory states. It is longer, more deliberate, and meant to be noticed. The split is load-bearing because the same easing curve cannot do both: a productive curve applied to a hero moment feels mean; an expressive curve applied to a button feels broken. **A mature motion system ships two parallel token sets, one productive and one expressive**, and the principles tell consumers which set to reach for in which context.

**Where the field has diverged.** Material treats motion as continuous (every transition implies a physical relationship), while Apple's HIG treats motion as conditional (motion should defer to clarity, and reduce-motion is treated as first-class). Neither is wrong; both reflect the host platform's broader stance. A multi-platform DS resolves this by writing principles that are platform-neutral and letting the per-platform implementation files (19, 20) handle the spelling.

**Brand personality without preciousness.** The temptation in agency work is to design every motion as a brand expression. The discipline is the inverse: most motion is productive, anonymous, and the brand shows up in the *expressive* layer — the hero, the empty state, the moment of success — where the user has bandwidth to notice it. A brand that expresses itself in every button transition is a brand that has confused decoration with identity.

---

## Motion tokens

The 2025–2026 token tier looks like this:

| Tier | What it holds | Naming convention |
|---|---|---|
| Primitive | Raw values: `200ms`, `cubic-bezier(0.2, 0, 0.4, 1)`, spring `{ stiffness: 200, damping: 25, mass: 1 }` | Literal, not semantic. `duration-200`, `easing-decel-standard`, `spring-snappy-base` |
| Semantic | Role-based: `duration/short`, `easing/enter`, `spring/snappy` | Names a use, not a value |
| Component | Per-component overrides: `motion/modal/enter/duration`, `motion/toast/exit/easing` | Used only when a component's motion legitimately diverges from the semantic default |

**Three tiers is the convergent recommendation; two is a defensible compromise.** A system that ships only one tier of motion tokens (primitives mapped 1:1 to component use) reproduces the original problem at the token layer — every component picks its own duration from a shared list. The semantic tier is what makes the system enforceable: when a designer says "this should use the standard exit", the engineer reaches for `duration/exit` and `easing/exit`, not for the underlying numbers.

### Duration tokens

The convergent set of durations across IBM Carbon, Material 3, Atlassian, and Polaris is roughly:

- An *instant* tier (50–100ms) — interactive feedback, button presses, hover states.
- A *short* tier (150–250ms) — micro-transitions, state changes, single-property animations.
- A *medium* tier (300–400ms) — entrance and exit animations, panel openings.
- A *long* tier (500–700ms) — orchestrated sequences, full-screen transitions, hero moments.

A system needs four duration tokens, give or take one. More than six and consumers stop choosing meaningfully; fewer than three and the system cannot distinguish a button press from a page transition.

**Dynamic duration scales** are an emerging refinement. Material 3's *Expressive* update (2024) introduced the idea that motion duration should scale with the distance the animation traverses — a panel sliding 100px should not take the same time as one sliding 600px. This can be encoded at the token layer (`duration/spatial-short`, `duration/spatial-medium`) or expressed as a function of distance. The implementation files (19, 20) treat the per-platform spelling; the principle at the foundation layer is that not every animation should have a fixed clock.

### Easing tokens

The Head minimum was *three custom easing curves: in, out, in-out*. The 2026 field has stabilised on a slightly larger set, separating the *enter* curve (decelerating — the element settles into place) from the *exit* curve (accelerating — the element gets out of the way) from the *standard* curve used for in-place transitions.

```
easing/enter      → decelerating curve, ease-out family
easing/exit       → accelerating curve, ease-in family
easing/standard   → symmetric, ease-in-out family
easing/emphasised → an expressive curve for the brand-expressive layer
```

This is the productive set. The expressive set typically adds a curve with overshoot or anticipation that would feel wrong on a routine button transition.

**Calm easing as an accessibility token, not just a vibe.** Easing curves with abrupt onsets or harsh decelerations are more likely to cause discomfort in motion-sensitive users even without reduce-motion enabled. The DS should encode a *calm* easing variant for any animation that travels a long distance or is involuntary (auto-advancing carousels, pop-ups not triggered by the user). See 14-accessibility for the architectural treatment; the foundation-layer point is that this is a token decision, not a per-component judgement call.

### Spring tokens

This is the largest update to the field since Head wrote. **Springs are the new default for interactive motion.** A spring conveys the physical reality that the user is interacting with — an element responds to a gesture by being pushed, not by being scheduled. Curves are still right for non-interactive, deterministic transitions (a modal opening on a button click, a page transition); springs are right for anything driven by direct manipulation (a card being dragged, a sheet being pulled up, a button pressed and released).

The cross-platform spring vocabulary divergence is documented in 20-motion-implementation-mobile. At the foundation layer, what matters is that the system tokenises springs by *perceptual outcome*, not by physical parameter:

```
spring/snappy   → fast settle, no overshoot — for buttons, taps, small state changes
spring/gentle   → natural feel, subtle settling — for panels, sheets, drawers
spring/bouncy   → overshoot — for playful expressive moments, success states
```

The underlying parameters (stiffness/damping/mass on Compose, Flutter, Reanimated; duration/bounce on SwiftUI; the `linear()` easing string on web) are platform-specific concerns documented in 19 and 20. The token name is the contract; the parameter is the implementation.

### Composite motion tokens

A composite motion token is a single name that bundles duration, easing, and the property being animated. Examples:

```
motion/modal/enter       → duration/medium + easing/enter, property: opacity + transform
motion/toast/exit        → duration/short + easing/exit, property: opacity + transform-y
motion/page/transition   → duration/long + spring/gentle, property: transform-x
```

This is the layer at which AI coding agents become trustworthy. An agent asked to "animate the modal entrance" with only primitive tokens available will pick three of them — and pick differently each time. An agent given a composite `motion/modal/enter` token uses one name and gets the entire choreography correct. Composite tokens are the difference between a motion system that survives AI-assisted authoring and one that does not (see 15-ai-in-ds for the broader components-as-data argument).

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

**What gets tokenised vs. what stays per-component.** The system should ship a `stagger/standard` token (typically 30–60ms between siblings) because stagger applied inconsistently is visibly inconsistent. Sequence and parallel are choreography *primitives* and are usually expressed in code, not tokens. Follow-through and anticipation are component-level concerns that show up in expressive motion and rarely in productive motion.

**Shared element transitions** — the same component visually persisting across a route change (a card on a list page becoming the hero on a detail page) — are the choreography pattern most consistently underspecified at the system level. They depend on per-platform primitives (SwiftUI's `matchedGeometryEffect`, Compose's `SharedTransitionLayout`, Flutter's `Hero`, the web's View Transitions API) but the *intent* is the same across platforms. The DS should name the shared-element pattern at the foundation layer; the implementation files (19, 20) document the spelling.

---

## Reduce-motion as a system contract

The architectural treatment lives in 14-accessibility. The foundation-layer responsibility is to encode reduce-motion such that no individual engineer has to remember it. **The contract is: every motion token has a reduce-motion variant, and every consuming component reaches motion through tokens, never through hardcoded values.** When both halves hold, the system honours reduce-motion automatically. When either half breaks, individual engineers carry the burden — and they will get it wrong.

**The 2024–2026 refinement to our earlier position.** Our existing 14-accessibility material describes the reduce-motion fallback as collapsing durations to 0ms and easings to `step-end`. The field has moved on from that blanket treatment. The current convergent position is *informational vs. vestibular*:

- **Vestibular triggers** — large-scale translation, scaling, parallax, 3D rotation, infinite-spin — should be eliminated or replaced with a cross-fade.
- **Informational motion** — short fades, focus-state transitions, progress indicators — can be preserved at reduced amplitude or unchanged.

The DS encodes this as a per-token decision rather than a global flag. A `motion/page/transition` token's reduce-motion variant cross-fades; a `motion/button/hover` token's reduce-motion variant is unchanged. The variant is the contract; consumers don't write the logic.

**A 2026 gotcha to encode explicitly.** Browsers' View Transitions API does not respect `prefers-reduced-motion` automatically (see 19 for the spelling). Our system contract has to make this explicit: every view transition is wrapped in the reduce-motion check at the system layer, so consumers can't accidentally ship a forced animation. This is a small but load-bearing pattern.

The downstream relationship to other accessibility motion settings — Reduce Transparency, Differentiate Without Color, the broader vestibular consensus — is treated in 14. Motion is one channel among several; the system should not over-claim that respecting reduce-motion is sufficient on its own.

---

## Performance and the cost of motion

A design system that ships motion without a performance budget is shipping a regression vector. The budget is decidable, not aspirational.

**The web budget** is set by INP (Interaction to Next Paint, the Core Web Vital that replaced FID in 2024) and the LoAF API (Long Animation Frames, 2024). The architectural rule is that motion runs on the compositor thread — `transform` and `opacity` only — and never on properties that trigger layout or paint. The spelling lives in 19; the foundation-layer commitment is that the system tokens themselves only encode compositor-safe animations. A `motion/list/expand` token that animates `height: auto` is a token-layer failure, not a consumer failure.

**The mobile budget** is set by frame rate (60Hz baseline, 120Hz on modern hardware) and the per-platform threading model. SwiftUI and Compose handle this on a UI thread separate from app logic; Flutter has a single UI isolate that benefits from light animation work; React Native splits work across JS thread and UI thread, with Reanimated's worklets moving animations to the UI thread. The system contract is the same as on web: tokens only encode animations the platform's compositor can run cheaply.

**Encoding safety as a property.** Composite motion tokens should declare which properties they animate. A `motion/*/safe` set animates `transform` and `opacity` only; a `motion/*/heavy` set animates `width`, `height`, `box-shadow`, or other layout-triggering properties and is opt-in for specific use cases. The default token set should be safe by construction. Heavy tokens exist because the field of motion is not always cheap, but the system makes the cost visible at the token name.

**The 120Hz consideration.** Modern devices ship 120Hz displays as standard. A motion that drops frames on 60Hz is jank; the same motion on 120Hz looks broken because the user's expectation of smoothness has been recalibrated. The system should treat 120Hz as the design target, not the high-end exception.

---

## Where motion sits relative to the rest of the system

| Concern | Owner | Reference |
|---|---|---|
| Token taxonomy (three-tier + composite) | This file | 18 |
| Motion in Figma Variables, Style Dictionary pipeline | 02-design-foundations | 02 |
| Per-component motion behaviour | 03-component-library | 03 |
| Reduce-motion architectural treatment | 14-accessibility | 14 |
| Mobile platform motion implementation | 20-motion-implementation-mobile | 20 |
| Web platform motion implementation | 19-motion-implementation-web | 19 |
| Designer-to-developer micro-interaction spec | 21-motion-spec-and-handoff | 21 |
| AI coding agents and motion tokens | 15-ai-in-ds + this file | 15, 18 |

---

## Failure modes to watch

- **Motion tokens on the list but unused.** The system ships duration and easing tokens. Components hardcode their own values. The token layer becomes documentation rather than constraint. (See 02 — this is the practice's existing gap, now more concrete.)
- **One-tier tokens.** Primitives mapped directly to component use, no semantic layer. Every consumer picks their own duration from a list of literals. Consistency collapses at scale.
- **Productive curves applied to expressive moments.** The brand is supposed to show up in a hero animation; instead it gets the same `easing/standard` as a button. The expressive layer is missing or is treated as overrides rather than a parallel token set.
- **Reduce-motion at the duration layer only.** Durations collapse to 0ms but easings and properties remain, so the animation snaps in a way that still triggers vestibular sensitivity. The contract should be per-token, not global.
- **Springs simulated with curves.** A designer specs a "bouncy" interaction; the engineer approximates it with a long ease-out. The result is consistently wrong because the field-converged answer to interactive motion is a spring, and springs do not approximate from curves cleanly. (See 19, 20 for the platform spellings.)
- **AI agents producing unique durations every time.** An agent asked to add an animation generates `transition: all 0.18s ease`. Without composite motion tokens, this is the default failure mode and it accumulates faster than any human review can catch it.

---

## Tensions and open questions

1. **Productive vs. expressive as parallel token sets, or as a single set with overrides.** Atlassian and Carbon ship two parallel sets; Material 3 ships one set and treats the expressive variant as a mode. The practice should pick one. The case for parallel sets is enforceability — a productive curve cannot accidentally appear in an expressive context. The case for overrides is simplicity. Lean parallel, but the choice is not yet a practice default.

2. **Spring tokens as perceptual or physical.** The token name is perceptual (`spring/snappy`); the underlying parameters are physical and platform-specific. The risk is that the perceptual name drifts away from the physical implementation across platforms — `spring/snappy` on iOS and `spring/snappy` on Android end up feeling different. The mitigation is the dual-vocabulary discipline in 20 (see the cross-platform spring parameter mapping table). The practice should ship a calibration test alongside the tokens, not just the names.

3. **Composite tokens vs. component-internal motion.** The argument for composite tokens is AI-agent legibility and cross-component consistency. The argument against is that the composite layer is a lot of tokens for not-much-flexibility — most components animate the same handful of properties. The pragmatic answer is to ship composites for the choreography-heavy components (modals, sheets, toasts, list reveals, route transitions) and leave the rest to compose from primitives and semantics. The threshold is roughly the same as for component promotion (the rule of three referenced in 03).

4. **Where motion principles get reviewed.** Principles only enforce if someone applies them. The DS team can ship the principle "interactive elements respond within 100ms" and the consuming product still ships a 350ms button feedback because no one held the work against the principle. Governance treatment lives in 07; the foundation-layer commitment is that principles are written in a form that can be reviewed — decidable, not aspirational.

5. **Dynamic duration scales as system, not as Material-3-specific feature.** Material 3's distance-aware durations are the most actionable specific instance of this idea, but the broader principle — that not all motion has a fixed clock — applies across platforms. The practice has not yet decided whether to encode this at the token layer (additional tokens for spatial-aware durations) or as a runtime function (durations as a function of distance). Either works; the choice depends on how aggressively the DS wants to enforce vs. enable.

---

## See also

- **02-design-foundations** — where motion is named alongside color, type, space as a foundation primitive, and where the practice acknowledges the methodology gap this file partially closes.
- **03-component-library** — where motion specs were flagged as missing from component templates.
- **14-accessibility** — reduce-motion architectural treatment, the four-layer model that this file's tokens slot into.
- **15-ai-in-ds** — composite motion tokens as a prerequisite for trustworthy AI-assisted authoring.
- **19-motion-implementation-web** — CSS / WAAPI / View Transitions, the `linear()` spring revolution, library landscape, INP/LoAF, AI-agent guardrails for web motion.
- **20-motion-implementation-mobile** — primitives, springs, shared element transitions, Lottie vs. Rive, threading model, reduce-motion per framework.
- **21-motion-spec-and-handoff** — the designer-to-developer micro-interaction spec gap, the tooling landscape, the recommended canonical format.

---

*Provenance: Motion as foundation primitive, the principles → building blocks → choreography frame, three-easing-curve minimum, and productive vs. expressive split are from Val Head (*Animation in Design Systems*, 2020), already present in 02-design-foundations. The three-tier token taxonomy with composite tokens, the spring-as-perceptual-token discipline, the productive vs. expressive as parallel sets, the four-principle convergent shape (Human / Clarity / Accessible / Performant), and the AI-agent failure mode argument are synthesised from IBM Carbon (Productive vs. Expressive Motion, 2023–2024), Atlassian Design System (Motion principles, 2024), Material 3 Expressive (2024), the dual-agent research outputs in `_research/_inbound/2026-05-14-motion-foundations-and-spec/`, and Token Studio's composite-token treatment (2024–2025). The informational vs. vestibular reduce-motion refinement is from the dual-agent research outputs (May 2026), refining the earlier blanket position in 14-accessibility. The 120Hz design target framing and INP / LoAF performance budget are from the web implementation research output (May 2026). Performance-safety-as-property at the token layer is internal POV synthesised across the three research outputs. Token tiers, three-tier model, and composite tokens are aligned with Nathan Curtis (EightShapes — *Design Tokens* Nov 2024 + *Components as Data* Sep 2025).*

# Motion as a design system foundation, and the micro-interaction handoff gap

> Research run, Claude half of a dual-agent pair. Drafted 2026-05-14. The frame is a senior DS lead at an agency shipping for web, iOS, Android, and cross-platform. Motion is a foundation we have not yet treated as one; the micro-interaction spec workflow is the secondary, load-bearing concern.

---

## 1. Why motion is a design system concern, not an application concern

The argument for centralising motion at the system layer is the same argument that won for colour a decade ago and for spacing five years after that. Motion is a perceptual property of the brand and the interface, not a screen-level design decision. When it is left to product teams, it accumulates as a hundred small inconsistencies — three durations that should be one, four different easing curves on what looks like the same interaction, modals that slide on Android and fade on web for no defensible reason — and these inconsistencies are not legible to the team that created them because each one was locally reasonable. The cost is invisible until a user moves between two surfaces of the same brand and feels, without being able to name, that something is wrong.

**What goes wrong specifically.** Per-product motion produces three failure modes the consulting practice should be able to diagnose at a glance. First, drift between platforms: the iOS app's sheet has a spring response that the web's modal does not, because the iOS team used UIKit defaults and the web team used a 200ms ease-out. Both look fine in isolation. Together they look like two products. Second, drift inside a platform: the same product ships a 150ms duration for one tab transition and 300ms for another, often because two designers worked at different times and neither saw the other's spec. Third, accessibility regression: reduce-motion gets respected on the components engineers thought about and missed everywhere else, because there is no system contract that makes it the default. Each of these is recoverable as a one-off; together they describe a system that has no motion layer.

**The cost asymmetry.** Retrofitting motion consistency after the fact is more expensive than retrofitting colour, because motion lives in code paths (transition definitions, animation orchestration, scroll-driven effects) that are not as easily refactored as a CSS variable swap. A token rename across a codebase is a codemod; a duration rationalisation is often an audit of every `transition:` declaration, every `animate()` call, every `withTiming()` in Reanimated, every implicit animation in SwiftUI. The practice's experience with token retrofits applies — but worse, because motion has no `--motion-duration-md` shaped variable in most production codebases today. Baking the four-layer model (tokens / components / docs / contribution gates, see 14-accessibility) into motion from the first foundations sprint is meaningfully cheaper than producing motion as a deliverable two years in.

The practice's POV should therefore be that motion is a foundation, on the same tier as colour, spacing, and type, and that the foundation work belongs in the same phase as the rest of `02-design-foundations`. Anything weaker than that produces the per-product drift the engagement was meant to prevent.

---

## 2. Motion principles and brand personality

Motion principles are the part of a motion system most teams skip and most consulting decks include. A principle is useful only if it is specific enough to decide a contested choice. "Motion should feel natural" decides nothing. "Motion should respond to the gesture that initiated it within 100ms and resolve within 300ms unless the user is being shown new content" decides whether a tab transition is 150ms ease-out or a 450ms spring. The test for whether a principle is good is whether a designer holding two options can pick between them by reading it.

**Productive vs. expressive as the load-bearing distinction.** The field has converged on a two-mode model since Material 3 made it explicit in 2023, though Apple has carried the same distinction in less codified form since iOS 7. Productive motion is for transitions that move the user through known tasks — switching tabs, opening a panel, navigating between routes — and is characterised by short durations (typically 150–250ms), simple eases (standard or emphasised, not bouncy), and minimal stagger. Expressive motion is for moments where the system is communicating state or personality — onboarding moments, success states, illustrative empty states, the pull-to-refresh moment — and tolerates longer durations (300–600ms), springs with visible overshoot, and choreographed sequences. The system encodes the distinction by labelling tokens and patterns explicitly: `duration.productive.md`, `duration.expressive.lg`, `easing.productive.standard`, `easing.expressive.emphasised`. Designers reach for the productive set by default and the expressive set when justified.

**Brand personality without preciousness.** Brand-expressive motion fails when it is a designer's pet flourish; it succeeds when the brand's underlying attributes — playful, restrained, technical, warm — are encoded into a small set of decisions that compound across the product. A restrained brand should ship a productive easing curve closer to `ease-out` with no overshoot and avoid springs entirely outside hero moments. A playful brand should have a productive curve that already has a hint of asymmetry (a gentle overshoot or a slow-out) and a spring vocabulary that gets reached for more often. The test is whether the brand's motion is recognisable in a five-second blind clip of an interaction — if it is not, the motion is not doing brand work. If it is showy enough to be recognisable but not consistent enough to be used everywhere, the motion is preciousness, not personality.

**Where the field has converged and diverged.** Convergence: the productive/expressive split, the use of a small (5–8) duration scale, standard ease-out as the default productive curve, springs reserved for expressive moments, reduce-motion as a first-class concern. Divergence: how aggressively to use springs in productive motion (Apple's iOS spring defaults are more aggressive than Material 3's), whether to expose mathematical spring parameters (`mass`, `stiffness`, `damping`) as tokens or only their visual equivalents (`bouncy`, `snappy`, `gentle`), and whether motion principles get documented as prose, as numbered rules, or as a decision matrix. Material's motion documentation (M3, updated 2024) is the most thorough public artefact; Apple's HIG motion sections are the most aesthetically opinionated but the least systematic; IBM Carbon and Atlassian's motion docs are the strongest examples of mid-sized systems publishing useful principles without overproducing the artefact.

---

## 3. Motion tokens

The token layer is where motion stops being a slide deck and becomes infrastructure. The same DTCG 2025 specification that covers colour and spacing has had a `duration` type since the 2024 draft and a `cubicBezier` type alongside it; both are stable enough to ship in production token pipelines today (verified DTCG draft, 2025-Q1). Spring tokens are not yet in the DTCG spec and require a custom type or a structured object — a known gap, flagged below.

**Duration tokens.** The field has converged on a small scale, typically 5–7 named values from roughly 50ms to 1000ms, on a roughly geometric progression. Material 3 ships `short1–4` (50/100/150/200ms), `medium1–4` (250/300/350/400ms), `long1–4` (450/500/550/600ms), `extraLong1–4` (700/800/900/1000ms) — sixteen values, more than most systems need but useful as a public reference. Carbon ships a tighter scale (`fast-01` through `slow-02`). The practice's recommendation should be a 6–8 step scale, named semantically (`duration.instant`, `duration.fast`, `duration.medium`, `duration.slow`, `duration.deliberate`) with productive/expressive variants where the durations diverge.

The semantic vs. literal naming question matters. Literal names (`duration.150`) tell a designer what they are getting but couple the token to its current value; semantic names (`duration.fast`) let you re-tune the scale without renaming. The mature pattern, paralleling the colour token tiers, is a two-tier system: a numeric base scale (`duration.100` = 100ms, `duration.200` = 200ms) and a semantic alias layer (`duration.productive.standard` = `duration.200`) that components reference. Designers and engineers using the system reach for the semantic layer; the base scale exists for the rare component that needs to bind to a specific value.

**Easing tokens.** Standard curves are `cubicBezier` tokens. The field has converged on a small set of named curves, broadly mapping to:

- `linear` — used almost only for progress indicators and continuous animations
- `standard` / `ease-in-out` — for things appearing and leaving in sequence
- `decelerate` / `ease-out` — for things arriving on screen (the most common productive curve)
- `accelerate` / `ease-in` — for things leaving the screen
- `emphasised` — Material's signature asymmetric curve (`cubic-bezier(0.2, 0.0, 0, 1.0)` in M3), used for productive motion that needs more presence
- `expressive` / `overshoot` — curves with a hint of overshoot, used for expressive moments where a spring would be overkill

Custom curves are appropriate when the brand demands a distinctive motion signature and the team can commit to maintaining it. Most systems do not need them; the default Material or Apple curves do not read as off-brand in the way default colours do. If the brand requires a custom curve, ship it as a single token (`easing.brand.signature`) and use it sparingly so it remains legible.

**Spring tokens vs. timing-curve tokens.** Springs and curves are not interchangeable. A curve is a function of time; a spring is a function of physical state (position, velocity, mass, stiffness, damping). Springs handle interruption gracefully — if a user grabs a sheet mid-animation, a spring continues from the current velocity, where a curve has to restart or reverse awkwardly. The rule: use a spring when the animation is gesture-driven or likely to be interrupted; use a curve when the animation is fire-and-forget and the duration is bounded.

Expressing springs as tokens is harder than curves. The two viable approaches:

1. **Visual-parameter tokens.** Apple's SwiftUI `Spring(duration:bounce:)` API (iOS 17+, 2023) is the model — express a spring as a duration and a bounce parameter, both of which are designer-legible. This translates to web via Framer Motion's `visualDuration` API (added late 2024) and to React Native via Reanimated 3's similar visual-spring helpers. The token shape is `{ "type": "spring", "duration": 400, "bounce": 0.2 }`.
2. **Physics-parameter tokens.** `{ "mass": 1, "stiffness": 200, "damping": 20 }`. Closer to the implementation, less legible to designers, harder to translate across platforms because each engine's spring solver is slightly different.

The practice's recommendation should be the visual-parameter approach as the public token contract, with physics parameters available as an escape hatch for components that have already been tuned to specific values.

**Composite motion tokens.** Material 3 introduced the idea of a "motion scheme" — a bundle of duration + easing + (optionally) spring parameters that get applied as a unit. The composite token shape is something like:

```json
{
  "motion.productive.standard": {
    "duration": "{duration.200}",
    "easing": "{easing.standard}",
    "properties": ["opacity", "transform"]
  }
}
```

Composite tokens are useful when components consistently animate the same property set with the same timing — modals fading and scaling, sheets translating and fading, items entering with stagger. They become harmful when they over-constrain, forcing components to either accept all the bundled parameters or none of them. The practical pattern is to ship composites for the five or six canonical motion patterns (enter, exit, container transform, shared axis, fade-through, emphasised) and leave the atomic duration/easing tokens available for components that compose their own.

---

## 4. Choreography and orchestration

Choreography is the part of motion that lives above the token layer and below the component. It is also the part most systems do not document, which produces the per-product drift discussed in section 1.

**Vocabulary the field uses.** The accepted terms map reasonably well across platforms, with platform-specific words layered on top:

- **Sequence** — animations that run one after another
- **Parallel** — animations that run at the same time
- **Stagger** — a sequence with a fixed delay between siblings (the canonical list-entrance pattern)
- **Cascade** — stagger with delay-per-depth across a tree, not per-sibling
- **Anticipation** — a small counter-movement before the main movement, used sparingly in expressive moments
- **Settle** — a spring's resolution behaviour, the period between visible overshoot and rest
- **Follow-through** — secondary elements that complete their animation slightly after the primary
- **Shared element** — an element that persists across a transition and animates between two positions/sizes
- **Container transform** — Material's name for shared-element transitions where the container itself morphs
- **Shared axis** — a transition that implies forward/backward motion along an axis
- **Fade-through** — an exit-then-enter transition for unrelated content

The vocabulary is worth standardising in the docs because designers and engineers currently use these terms interchangeably and inconsistently. Carbon, Material, and Polaris all publish glossaries; the practice should ship its own as part of the motion foundation.

**System level vs. component level.** The rule is similar to spacing: encode at the system what is shared across components, leave to the component what is intrinsic to it. Shared at system: the stagger delay (typically 25–50ms between siblings), the standard enter/exit choreography, the container-transform pattern, the route-transition pattern. Component-local: how a switch's thumb moves between positions, how a checkbox's check draws, how a chip's selection state animates. The component is responsible for its own internal motion; the system is responsible for how the component participates in larger transitions.

**Transitions.** Three scales, each with different system implications:

1. **State transitions** (hover, focus, pressed, selected). Almost always sub-200ms, typically `ease-out`, fire-and-forget. The system should ship these as part of the interaction-state foundation, not as standalone motion tokens.
2. **Route transitions** (within an app or product). Material's shared-axis and container-transform patterns are the most thoroughly specified examples; iOS's default navigation push and modal-presentation are the most aesthetically successful. The system should standardise on a small set (forward/backward, modal up, modal-replace, shared-element) and document when each applies.
3. **Screen-to-screen transitions** in marketing or onboarding contexts. The expressive end of the system, often hand-choreographed; the foundation provides the easing and duration vocabulary, the component layer composes.

**When motion defers vs. composes.** A component's motion is its own when it is self-contained — a tooltip's appearance, a switch's toggle, a tab indicator's slide. A component's motion belongs to the system when it participates in a larger transition — a list item that enters as part of a stagger, a card that morphs into a detail view, a sheet whose backdrop fades while the sheet itself springs in. The composition layer is where most systems are weakest, because it is the layer where the encoding requires the most architectural work (orchestration primitives, layout-animation support, shared-element machinery). React's `motion` library (formerly Framer Motion, renamed late 2024 under Vercel's stewardship), iOS's `matchedGeometryEffect`, Android's `SharedTransitionLayout` (added in Compose 1.7, 2024), and Flutter's `Hero` are the platform-native primitives the system has to compose with.

---

## 5. Reduce-motion as a system contract

Reduce-motion is where the four-layer accessibility model pays off most visibly. The contract the system should encode is that every motion primitive — every token-consuming animation — checks the user setting by default, not because the engineer remembered to.

**The encoding.** At the token layer, the duration scale collapses to either zero or a very short value when the reduce-motion setting is on. Most implementations zero out durations and rely on the component to provide a fallback presentation (a cross-fade, a snap, a state change without transition). The mechanism varies by platform:

- **Web.** A `@media (prefers-reduced-motion: reduce)` block in the token output that overrides duration tokens to `0.01ms` (zero confuses some animation APIs; `0.01ms` is the conventional safe value). Motion-library wrappers (Framer Motion's `MotionConfig reducedMotion="user"`, since 2023) consume the same setting and short-circuit at the API level. Both belong in the system — the CSS variable handles raw transitions, the wrapper handles JS-driven animations.
- **iOS.** `UIAccessibility.isReduceMotionEnabled` and `accessibilityReduceMotion` environment value in SwiftUI. The system's motion primitives (SwiftUI `withAnimation` wrappers, UIKit transition wrappers) check this before applying.
- **Android.** `Settings.Global.ANIMATOR_DURATION_SCALE` and `Settings.Global.TRANSITION_ANIMATION_SCALE`; in Compose, the `LocalAccessibilityManager` exposes reduce-motion state. Compose-side motion wrappers consume it.
- **React Native / Flutter.** Both expose the system setting; Reanimated 3 has a `ReducedMotionConfig` (since v3.5, 2024); Flutter's `MediaQuery.disableAnimationsOf` is the canonical hook.

**What replaces the motion.** The field has converged on three replacement patterns, used in roughly this priority order:

1. **Cross-fade** — for transitions whose purpose was to communicate change. Replaces translate-and-fade, container transform, shared axis.
2. **Snap (no transition)** — for transitions whose purpose was decorative. Replaces stagger, hover micro-animations, decorative state transitions.
3. **Shortened duration** — for transitions whose absence would be confusing (a sheet appearing instantaneously can read as a flash; a 100ms fade reads as instant but reduces vestibular load). Used sparingly; some accessibility specialists argue against it, because it does not actually reduce motion, just shortens it.

Apple's HIG (updated 2024 for visionOS but also covering iOS) prefers cross-fade as the universal replacement; Material 3 documents per-pattern replacements with cross-fade as the default. The practice should standardise on cross-fade as the default replacement and document explicit per-pattern overrides where cross-fade is wrong (e.g., a progress bar should not cross-fade; it should stop animating but keep showing progress).

**Relationship to other accessibility motion settings.** Reduce-motion is one of three settings the system should be aware of:

- `prefers-reduced-motion` / Reduce Motion — addresses vestibular triggers (parallax, large-area movement, spinning, zooming). This is the dominant setting and the one the system should encode at the token layer.
- `prefers-reduced-transparency` / Reduce Transparency — addresses readability over translucent backgrounds. Not strictly motion but often handled in the same layer because both settings hint at "the user wants a less expressive UI." The system should respect this in components that use translucent surfaces (sheets, navigation bars) by switching to opaque fills.
- `prefers-contrast` / Differentiate Without Color — orthogonal to motion but often grouped in accessibility settings UIs. Affects motion only insofar as motion sometimes carries information that should also be communicated by state change or icon.

The system's responsibility is to encode the setting check at the token and component layer; the application's responsibility is to make case-by-case decisions where the system cannot. Scroll-driven effects, parallax in marketing pages, autoplaying video — these are application-layer concerns the system should document but not own.

---

## 6. Performance and the cost of motion

Motion is the most performance-sensitive part of the design system. The cost is not the motion itself but what the motion forces the renderer to do.

**The budget.** A safe motion budget is 60fps on the target platforms, with no dropped frames during transitions, on the 25th-percentile target device. The web's CWV INP metric (which fully replaced FID in March 2024) is the proxy most teams track; an animation that pushes INP over 200ms is failing the budget regardless of how it looks on the designer's M-series laptop.

**Web specifics.** The compositor-friendly properties — `opacity`, `transform`, `filter` (with caveats), and the newer view-transition primitives — are cheap because they do not invalidate layout or paint. Animating `top`, `left`, `width`, `height`, `margin`, anything that forces layout, is expensive. The system should encode this distinction in component motion APIs:

- Components that animate `transform` and `opacity` are "safe" and can be used freely.
- Components that animate layout (a panel widening, a list item growing) need to declare it and accept a performance budget.
- `will-change` should not be a system-level hint applied to every animatable element; it is a per-component declaration that the component should remove once the animation is done. Systems that ship `will-change: transform` as a class default produce GPU memory pressure that is invisible until the page has fifty animated elements.

The View Transitions API (stable in Chrome 111+, Safari 18.2, Firefox behind a flag as of early 2026) deserves explicit treatment. Same-document view transitions are production-ready for shared-element style transitions; cross-document transitions are still rolling out (Chrome shipped late 2024; Safari support landed in 18.2, January 2026). For systems shipping today, view-transitions are a progressive enhancement, not a baseline.

CLS (Cumulative Layout Shift) is a motion-adjacent concern: a transition that causes layout to shift on entry — a stagger that pushes content down as items load, an expanding section that re-flows the page — counts against CLS. The system should standardise on reserving space before animating in, or animating from a layout-stable initial state.

**Mobile specifics.** The 60Hz vs. 120Hz divide affects how springs feel. A spring tuned to look right on 60Hz can feel mushy on 120Hz ProMotion or Android variable-refresh displays; a spring tuned for 120Hz can feel snappy-to-the-point-of-jittery on 60Hz. The mitigation is either to tune for visual duration rather than physics parameters (the visual-spring API approach mentioned in section 3) or to ship two spring tokens and select at runtime, which is more complexity than most systems want.

Jank on lower-end devices is the failure mode the design team typically does not see. The Android budget at the 25th percentile is meaningfully tighter than at the 50th; Compose's `LaunchedEffect`-driven animations can drop frames on low-end devices if the work runs on the main thread. The system should document which animations are safe and which require profiling, and component APIs should make heavy animations opt-in.

**Encoding "safe" vs. "heavy" as a property.** A useful pattern: tag each motion pattern with a performance class.

- `motion.class.safe` — compositor-only, GPU-accelerated, no layout work
- `motion.class.moderate` — minor paint or layout but bounded
- `motion.class.heavy` — full layout animation, blur filters, complex SVG, scroll-driven effects

This belongs in the metadata/registry layer alongside component metadata (see 04-documentation). Engineers consume the property to know whether an animation can be used in a list of 100 items or only as a one-off. Designers see the property in the docs and learn the difference.

---

## 7. The micro-interaction handoff problem

This is where the workflow gap most often shows up. Figma's prototype features have improved steadily through 2025 — `Smart Animate` covering more properties, `Variables` driving conditional animations, interactive components handling state transitions — but it remains inadequate for spec'ing a micro-interaction at the level a developer can implement from. The gap is not a tooling oversight; it is a fundamental mismatch between Figma's model (frames with declarative differences, interpolated by a tween) and the implementation model (properties animated over time with named curves, often interruptible, often gesture-driven).

**What Figma still cannot do as of May 2026.** Figma cannot express:

- A named easing curve. Smart Animate offers a small set of curves (`ease`, `ease-in`, `ease-out`, `ease-in-out`, `linear`, `gentle`, `quick`, `bouncy`, `slow`) but they do not map cleanly to the system's named tokens; there is no way to bind a transition to `motion.easing.emphasised`.
- A spring with mass / stiffness / damping or visual duration / bounce. Smart Animate's `bouncy` preset is the closest, and it is opaque.
- Stagger across siblings (designers fake it by animating each frame individually).
- A transition that is interruptible — Figma's transitions always run to completion.
- A reduce-motion variant in any first-class way (designers ship two prototypes or annotate).
- Choreography across multiple components without putting them all in one frame.
- Scroll-driven animation in a way that maps to platform implementations.

Figma's roadmap (publicly discussed at Config 2025, June 2025) flagged motion as an investment area, with `Variables`-driven animation as the bridge; the practitioner-visible improvements through Q1 2026 have been incremental rather than structural. **Verification path: Figma changelog, monitored quarterly.**

**What this costs in practice.** The motion that ships is whatever the developer improvised, because the developer is the last person in the chain who has to make a decision. The designer can show a Lottie reference or a screen recording; the developer translates it to whatever animation library the codebase uses, and the result is rarely what the designer pictured. The cost is hours per micro-interaction in PR review and revision, plus the cumulative drift discussed in section 1.

**Historical workarounds, and what each loses.**

- **Written specs in a doc.** Reliable, version-controllable, terrible at communicating timing. A 350ms duration in a spec doc means nothing without seeing it.
- **Video reference / screen recording.** Communicates timing well, communicates nothing about the parameter values. A developer cannot tell from a video whether a spring has bounce 0.3 or 0.4.
- **Lottie files.** Strong for illustrative animations and one-off expressive motion. Weak for state-driven interactions because Lottie is a baked timeline, not a state machine. A button press animation as a Lottie is the wrong tool.
- **Code prototypes (CodePen, Framer Sites, etc.).** The most accurate fidelity, the highest authoring cost, and the least reusable across designers. Some teams have an "interaction designer" who codes prototypes; most do not.
- **"Ask the designer."** The default, the cheapest, the most lossy. Survives only because the alternatives have not been good enough.

**Current consensus.** Partially solved, trending towards solved. The honest read on the field as of May 2026:

- Figma alone is not sufficient and the community has accepted this.
- The combination of Figma (for layout and state) + a motion-specific tool (for timing and easing) + a written spec table is what most senior teams are converging on.
- The motion-specific tools have improved meaningfully: Rive (state machines, on the web and natively, 2024–2025 updates), Jitter (browser-based motion design with shareable specs, growth through 2024), Linear's Marker (acquired and integrated into Linear, 2025), and Origami Studio (still maintained by Meta though unstable in adoption). None has won the category.
- The motion-library side has also matured: Framer Motion's rebrand to `motion` (late 2024) reflects its broader scope; Reanimated 3.x is the iOS/Android standard for cross-platform; SwiftUI and Compose now both have first-class spring APIs that designers can reference by visual parameters. The gap between what designers can spec and what engineers can implement has narrowed from a chasm to a seam.

**What a sufficient spec contains.** This is worth standardising as a checklist:

1. **Trigger.** What causes the animation to start (hover, click, focus, scroll, gesture, state change, mount).
2. **Properties animated.** Which CSS / SwiftUI / Compose properties change. Named, not implied.
3. **From state and to state.** The start and end values for each property.
4. **Timing.** Duration in ms, by reference to the system token if possible.
5. **Easing.** Curve name (system token reference) or spring parameters.
6. **Choreography.** If multiple properties or elements: their relative order, any stagger, any follow-through.
7. **Interruption behaviour.** What happens if the trigger reverses or a new trigger fires (reverse, restart, continue from current state).
8. **End state behaviour.** Where the element rests; whether it is still interactive; whether any properties (like `will-change`) need clearing.
9. **Reduce-motion behaviour.** What this animation becomes when the user has reduce-motion on (typically a reference to a system fallback pattern).
10. **Performance class.** Safe, moderate, or heavy, per section 6.

A spec with all ten fields is implementable by any competent engineer without back-and-forth. A spec missing any of the last four (interruption, end state, reduce-motion, performance class) is where most production motion bugs live.

---

## 8. Tools and workflow for motion spec

Below is the candidate landscape as of May 2026, not a recommendation. The synthesis run can decide what the practice standardises on.

**Prototype-focused tools.**

- **Figma prototype mode.** Universal, designer-accessible, weak at parameter exposure (see section 7). Handoff artefact: Dev Mode inspection that shows duration and easing preset names, not values that map to system tokens. Engineers can consume the layout and state spec but typically not the motion.
- **Framer (the product, not the library).** Stronger motion fidelity than Figma because it is built on the same animation primitives as the `motion` library. Adoption has been niche since the company refocused on Sites in 2023; useful for teams that have it. Handoff: real CSS / React snippets, which engineers can adapt.
- **ProtoPie.** Best-in-class for sensor-driven and conditional prototypes. Adopted in larger product orgs (Samsung, Microsoft surfaces) and in automotive. Handoff: a `.pie` file plus video; the parameter values are inspectable inside ProtoPie but the file is not directly engineer-consumable. Pricing changed in 2024 to per-seat enterprise; verification path: protopie.io/pricing.

**Animation-focused tools.**

- **Rive.** State-machine driven, exports to runtimes for web, iOS, Android, React Native, Flutter, Unity. Strong for components with internal state animations (a toggle, an expanding card, a complex loader). Designer-accessible after a learning curve. Handoff: `.riv` file plus a runtime call that drives the state machine from app state. The most interesting tool in the category through 2024–2025.
- **Lottie + LottieFiles.** Universal runtime support, designer-accessible via After Effects + Bodymovin or via LottieFiles' newer browser editor. Strong for one-off illustrative motion; weak for state-driven interactions. Handoff: a `.json` file. Adobe's stewardship of After Effects has stalled feature work; LottieFiles is the practical centre of gravity.
- **Jitter.** Browser-based motion design tool, aimed at marketing and product motion. Designer-accessible, lighter than Rive. Handoff: video or animated SVG; less directly engineer-consumable. Verified active development through Q1 2026.

**Video / reference tools.**

- **Screen capture (QuickTime, CleanShot, Loom).** Universal. Handoff: a video file. Communicates timing, not parameters. Default fallback when nothing else works.
- **Principle, Flow, Tumult Hype.** Older generation, niche maintenance. Worth flagging only because some teams still use Principle for iOS-style motion exploration.

**Code-focused tools.**

- **Storybook with interactions and play functions.** The engineer-side spec artefact. A Storybook story with an animation running, parameters declared in code, is the most precise spec a system can ship. Designer-accessible via the deployed Storybook URL, not the source. Handoff: the source is the spec.
- **CodeSandbox / StackBlitz prototypes.** Useful for hero moments that need to be authored in code. Designer-accessible via preview, not authoring. Handoff: runnable code.
- **Framer Motion / `motion` documentation site.** Not a tool per se, but the de facto reference for parameter values; teams routinely link to motion.dev examples as part of a spec.

**Trade-offs.**

| Category | Fidelity | Designer effort | Engineer-consumable | Reusable across team |
|---|---|---|---|---|
| Figma prototypes | Low for motion | Low | Low | High |
| Framer (product) | High | Medium | Medium-high | Medium |
| ProtoPie | High for conditional | High | Low (video) | Medium |
| Rive | High for state-driven | Medium-high | High (runtime) | High |
| Lottie | High for illustrative | Medium | High (runtime) | High |
| Screen capture | Low | Very low | Very low | Low |
| Storybook | Maximum | High | Maximum | High |

**Patterns from teams that have closed the gap.** The teams shipping consistent motion (Linear, Stripe, Vercel, Material's reference apps, Atlassian) have converged on a similar pattern, with variations:

- A motion-token layer in the design system, consumed by both Figma (as variables and prototype settings) and code (as CSS variables and JS objects).
- Component-level motion lives in Storybook, with story-level parameters that designers can scrub.
- One-off expressive motion is built either in Rive (if state-driven) or coded directly in the production codebase, with the engineer pairing with the designer.
- A spec template — usually a Notion or Figma page — that captures the ten fields from section 7 for any micro-interaction not already covered by a component default.
- A weekly or per-feature motion review where the designer and the implementing engineer watch the production build side-by-side with the prototype.

**Patterns that have not worked.** A single "motion tool of record" mandated for all motion specs; standalone motion spec documents not linked to a running prototype or build; Lottie as a state-machine substitute; expecting Figma alone to cover the gap.

**What a system might standardise on, framed as a decision.** Not a recommendation, but a decision framework:

- If the team's products are predominantly state-driven UI (consumer apps, complex web apps), Rive is the strongest candidate for component-level motion that exceeds Figma's reach, with Lottie reserved for illustrations and Storybook as the engineering spec.
- If the team is predominantly content-driven (marketing, editorial, brand sites), Lottie + coded prototypes + the production codebase's animation library is the more honest stack.
- If the team is cross-platform with shared product surfaces, the canonical motion spec format should be the system's token references plus a structured spec sheet (the ten fields), with platform-specific code prototypes as the highest-fidelity artefact and Storybook as the web-side source of truth.
- Across all cases, the practice's POV should be that the spec is the contract, not the tool — the system standardises on the ten-field spec format and the token layer, and tooling is a per-engagement decision.

A reasonable default for a new engagement: Figma for layout and state, Storybook with `motion` (or platform equivalent) for the engineering-side spec, Rive for state-driven components that exceed Figma, Lottie for illustration, and a written ten-field spec for anything that does not fit cleanly into the above.

---

## References

Primary platform documentation:

- Material 3 motion documentation — m3.material.io/styles/motion (current as of 2025, accessed for this run May 2026)
- Apple Human Interface Guidelines — Motion section — developer.apple.com/design/human-interface-guidelines/motion (updated 2024 for visionOS)
- Android / Compose motion documentation — developer.android.com/develop/ui/compose/animation (Compose 1.7+, 2024)
- W3C CSS Easing Functions Level 2 — www.w3.org/TR/css-easing-2/ (Candidate Recommendation, 2024)
- W3C CSS View Transitions Module Level 1 and Level 2 — www.w3.org/TR/css-view-transitions-1/, /-2/ (Level 1 stable, Level 2 still in flux as of early 2026)
- W3C Web Animations API — www.w3.org/TR/web-animations-1/
- MDN `prefers-reduced-motion` — developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion

Token / spec:

- Design Tokens Community Group format specification, including `duration` and `cubicBezier` types — design-tokens.github.io/community-group/format/ (draft, 2025-Q1)

Design system motion documentation:

- IBM Carbon motion guidelines — carbondesignsystem.com/guidelines/motion/
- Atlassian Design System — motion — atlassian.design/foundations/motion
- Shopify Polaris motion — polaris.shopify.com/design/motion
- Salesforce Lightning Design System — motion — lightningdesignsystem.com/guidelines/motion/
- Adobe Spectrum — animation — spectrum.adobe.com/page/motion/

Motion libraries:

- motion (formerly Framer Motion) — motion.dev (rebranded under Vercel stewardship, late 2024)
- React Native Reanimated 3.x — docs.swmansion.com/react-native-reanimated
- SwiftUI animation and Spring APIs — Apple developer docs, iOS 17+ (2023)
- Jetpack Compose animation APIs — Android developer docs
- Flutter animation and motion — docs.flutter.dev/ui/animations

Tools:

- Rive — rive.app (state-machine motion tooling, runtimes for web/iOS/Android/RN/Flutter/Unity)
- LottieFiles + Lottie spec — lottiefiles.com, airbnb.io/lottie
- ProtoPie — protopie.io
- Jitter — jitter.video
- Framer (product) — framer.com

Practitioner writing:

- Issara Willenskomer, "UX in Motion" series (the IDEO-adjacent body of work that introduced the productive/expressive framing to a wider audience)
- Pasquale D'Silva, motion design writing (Khan Academy / Elepath era pieces, foundational)
- Val Head, *Designing Interface Animation* (Rosenfeld, 2016) and ongoing writing — still the most thorough single book on the topic
- Rachel Nabors, motion writing for Smashing Magazine and W3C contributions
- Nathan Curtis, EightShapes — multiple essays on motion tokens and choreography in design systems
- Sam Anderson, *Design Systems are Infrastructure* and follow-up writing on motion as a system primitive (referenced elsewhere in the vault)

Verification paths flagged in the body:

- Figma motion roadmap — Figma changelog and Config keynote announcements, monitored quarterly
- View Transitions API browser support — caniuse.com/view-transitions
- DTCG spec status — design-tokens.github.io/community-group/format/
- ProtoPie pricing — protopie.io/pricing
- Motion library version claims — package changelogs (motion, reanimated)

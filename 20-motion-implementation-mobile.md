# 20 — Motion Implementation: Mobile

> Mobile motion in 2026 is four frameworks that have converged on declarative, value-driven animation and diverged on almost everything underneath. Springs are the default; the spring vocabulary is different in every framework. Shared element transitions exist everywhere; the spelling is different everywhere. This file is the cross-framework comparison a DS team needs to ship motion that feels like the same product across SwiftUI, UIKit, Jetpack Compose, Flutter, and React Native — and the reference an AI coding agent needs to write idiomatic motion code in each.

---

## Where the frameworks have converged

The 2023 view of mobile motion was four divergent stories. The 2026 view is one shared mental model with four spellings.

The convergence:

- **Declarative animation is the default authoring model** across SwiftUI, Compose, Flutter (implicit widgets), and React Native (Reanimated v3+). Imperative animation (UIView animation blocks, manual `AnimationController`) is the legacy path; new code lives in the declarative layer.
- **Springs are the default for interactive motion.** Curves remain right for deterministic, non-interactive transitions; springs are the field-converged answer for anything driven by direct manipulation.
- **Shared element transitions exist as a first-class primitive in all four frameworks** — a 2024 development that meaningfully closes the cross-platform gap.
- **Reduce-motion is a system-level setting that each framework exposes through a queryable API.** The DS contract is the same as on web: query once, gate the animation, never per-engineer.
- **120Hz is the design target.** SwiftUI's `ProMotion` integration, Compose's `LTPO`-aware rendering, Flutter's 120Hz support, and React Native's Reanimated worklets all assume modern displays.

The divergence (which the rest of this file documents) is in primitives, spring vocabularies, threading models, and shared-element specifics. The DS team's job is to express motion at a layer above the divergence and let the per-framework files spell it out underneath.

---

## Animation primitives by framework

| Framework | Primary surface | Mental model | Threading |
|---|---|---|---|
| SwiftUI | `.animation(_:value:)`, `withAnimation`, `Animation.spring(...)` | Declarative, value-driven — animations respond to state changes | Main thread for state; render server for execution |
| UIKit | `UIView.animate(...)`, `UIViewPropertyAnimator` | Imperative; legacy but still required for some surfaces | Main thread; Core Animation off-thread for execution |
| Jetpack Compose | `animate*AsState`, `updateTransition`, `Animatable`, `AnimatedVisibility` | Declarative, value-driven; composables recompose on animated state change | Compose's frame loop; off the UI thread for most work |
| Flutter | Implicit widgets (`AnimatedContainer`, `AnimatedOpacity`); explicit (`AnimationController` + `Tween`) | Declarative implicit; explicit when you need full control of the controller | Single UI isolate; animations run on the same thread as the rest of the app |
| React Native (Reanimated 3+) | `useSharedValue`, `useAnimatedStyle`, `withTiming`, `withSpring` | Declarative on the JS side; the animation itself runs as a worklet on the UI thread | UI-thread worklets — the JS thread is bypassed for animation frames |

**SwiftUI** is the most declarative of the set. A state change triggers a recomputation; wrapping the change in `withAnimation` interpolates from old to new. The defaults (the `.default` animation) are unopinionated; production motion uses explicit `.spring`, `.easeOut`, or custom animations.

**UIKit** remains the right tool for some surfaces (`UICollectionView` layouts, complex gesture-driven transitions, anything pre-iOS 15 in scope). Most new DS work uses SwiftUI; the practice should still document the UIKit spelling because legacy work persists.

**Compose** is structurally similar to SwiftUI but with a slightly different primitives split — `animate*AsState` for single-value animations (`animateColorAsState`, `animateDpAsState`), `updateTransition` for multi-value coordinated animation, `Animatable` for fine-grained control. The 2024 addition of `SharedTransitionLayout` is the most significant Compose motion update since 1.0.

**Flutter** ships two parallel APIs: implicit widgets (the lowest-friction path; `AnimatedContainer` interpolates its properties automatically on change) and explicit `AnimationController`-driven animation (for anything implicit can't handle). The implicit/explicit split is uniquely Flutter; the other frameworks fold both into one declarative surface.

**React Native** is the one to watch — its 2026 default is Reanimated 3+, whose worklets compile JS animation code to native code that runs on the UI thread. The old "JS thread blocks the animation" failure mode that defined RN motion through ~2022 is largely solved by Reanimated, but only if the team has actually adopted it. Legacy `Animated` API on the JS thread is still in shipping codebases; the DS should require Reanimated for any motion work.

---

## Spring and physics

The single biggest cross-framework comparison the DS team has to internalise. **Springs are the default; springs are spelled differently in every framework.**

| Framework | Spring API | Parameters | Notes |
|---|---|---|---|
| SwiftUI | `.spring(duration:bounce:)` (iOS 17+) | `duration`, `bounce` (perceptual) | Apple moved to perceptual parameters in iOS 17. Older `response`/`dampingFraction` API still works. |
| SwiftUI (older) | `.interactiveSpring`, `.spring(response:dampingFraction:blendDuration:)` | `response`, `dampingFraction` | Pre-iOS-17. Still common in production code. |
| Compose | `spring(dampingRatio:stiffness:)` | `dampingRatio` (0.0–2.0), `stiffness` (Float) | Classical physics parameters. |
| Flutter | `SpringSimulation(SpringDescription(mass:stiffness:damping))` | `mass`, `stiffness`, `damping` | Most explicit; least token-friendly without abstraction. |
| Reanimated (RN) | `withSpring(value, { mass, stiffness, damping, velocity })` or `withSpring(value, { duration, dampingRatio })` | Either classical or perceptual, depending on version | Reanimated 3.7+ supports both vocabularies. |

The same perceptual outcome — "snappy, settles quickly, no overshoot" — requires different parameters in each framework. The token contract in 18 names the outcome (`spring/snappy`); this file spells it.

**Cross-platform spring calibration table.** Approximate parameter mappings for the three semantic spring tokens (these are starting values; perceptual calibration on device is required):

| Token | SwiftUI (perceptual) | Compose | Flutter | Reanimated |
|---|---|---|---|---|
| spring/snappy | `.spring(duration: 0.3, bounce: 0.0)` | `spring(dampingRatio = 1.0f, stiffness = 1500f)` | `mass: 1, stiffness: 200, damping: 25` | `withSpring(val, { stiffness: 200, damping: 25, mass: 1 })` |
| spring/gentle | `.spring(duration: 0.5, bounce: 0.15)` | `spring(dampingRatio = 0.8f, stiffness = 700f)` | `mass: 1, stiffness: 100, damping: 15` | `withSpring(val, { stiffness: 100, damping: 15, mass: 1 })` |
| spring/bouncy | `.spring(duration: 0.6, bounce: 0.4)` | `spring(dampingRatio = 0.5f, stiffness = 500f)` | `mass: 1, stiffness: 150, damping: 10` | `withSpring(val, { stiffness: 150, damping: 10, mass: 1 })` |

**The discipline.** The token name is the contract. The parameters are the implementation. The practice ships side-by-side reference videos of each spring on each framework so designers can confirm the perceptual mapping holds. Without this calibration step, `spring/snappy` on iOS and `spring/snappy` on Android drift and the cross-platform consistency claim collapses.

**Why springs are the default in 2026.** Springs are interruptible by construction — a new state mid-animation continues from current physics state rather than restarting. Curves are not; a curve interrupted mid-flight either restarts or snaps. For any motion driven by direct manipulation (drag, swipe, pull), springs are the only correct primitive. For deterministic transitions (modal opens, route changes), curves remain right.

---

## Choreography and orchestration

### Sequence, stagger, parallel

| Pattern | SwiftUI | Compose | Flutter | RN (Reanimated) |
|---|---|---|---|---|
| Sequence | `withAnimation` with delays; or `Animation.delay(_:)` | `updateTransition` with `keyframes` | `TweenSequence`; or chained `AnimationController` | `withSequence(...)` |
| Stagger | Manual via `.animation(.delay(...))` per index | `updateTransition` with per-child delay | `AnimatedList`, or manual per-item delay | Manual per-index delay |
| Parallel | Multiple `withAnimation` blocks on independent state | `updateTransition` runs all children in parallel by default | Multiple `AnimationController`s | Multiple `useAnimatedStyle` calls |

Stagger remains a manual computation in all four frameworks. The DS-level commitment is the same as on web: ship a `stagger/standard` token and let consumers compute delays from `index * stagger`.

### Shared element transitions

The 2024 development that closed the most painful cross-platform gap.

| Framework | API | Notes |
|---|---|---|
| SwiftUI | `matchedGeometryEffect(id:in:)` | Mature since iOS 14; the canonical reference implementation. |
| Compose | `SharedTransitionLayout` + `sharedElement` modifier (1.7.0, July 2024) | The 2024 long-awaited primitive. Requires opt-in to `Modifier.sharedBounds` semantics. |
| Flutter | `Hero` widget | Long-standing; route-bound; less flexible than `matchedGeometryEffect`. The `flutter_animate` plus shared-element-transition libraries close some of the flexibility gap. |
| React Native | `sharedTransitionTag` (Reanimated 3+); `react-native-shared-element` (older) | Reanimated 3+ is the convergent answer for new work. |

**The DS-level pattern.** Name the shared-element transition at the system layer (`SharedHero`, `SharedCard`). The implementation is per-framework but the intent is consistent. AI coding agents asked to implement "the card-to-detail shared transition" can reach for the correct primitive per framework if the system documents the intent at the foundation layer.

### Route transitions

| Framework | Idiomatic 2026 path |
|---|---|
| SwiftUI | `NavigationStack` + custom transition modifiers; `.navigationTransition` (iOS 18) |
| Compose | Navigation Compose's `enterTransition` / `exitTransition` |
| Flutter | `PageRoute` subclasses; `PageRouteBuilder` with custom transitions |
| React Native | React Navigation 7's `transitionSpec` and screen options; Expo Router for App-Router-style routing |

Each framework's navigation library is the right tool; the DS provides the motion tokens and the navigation library composes them. The DS should not ship its own router.

---

## Implicit vs. explicit animation patterns

Two of the frameworks model this split explicitly; the other two fold it into one surface.

- **SwiftUI** — One surface. `withAnimation` is the universal mechanism; the engineer composes implicit-feeling code (`@State` change → animation) without a separate API.
- **Compose** — Two surfaces. `animate*AsState` is implicit (Compose handles interpolation when the value changes); `updateTransition` and `Animatable` are explicit (you control the animation lifecycle).
- **Flutter** — Two surfaces, named explicitly. Implicit widgets (`AnimatedContainer`, `AnimatedOpacity`) animate on property change with zero controller code; explicit animation requires an `AnimationController` and a `Tween`. The DS should default to implicit for any motion that maps cleanly to a single property change.
- **React Native (Reanimated)** — One surface. `useSharedValue` + `useAnimatedStyle` is the universal pattern; the worklet-based execution means animations are declarative on the JS side and imperative-fast on the UI side.

**The rule.** Reach for implicit when the motion is a function of state. Reach for explicit when the motion needs runtime control (gestures, interruption to a different target, scrubbing). On SwiftUI and RN, this is one mental shift; on Compose and Flutter, it is a different API.

**Interruption.** Springs handle interruption natively across all four frameworks. Curves on SwiftUI and Compose handle interruption by interpolating from current value to new target with a new animation — usually correct. Curves on Flutter via `AnimationController` need explicit handling; the controller's `value` becomes the new animation's `begin`. Reanimated handles it via `withSpring`'s velocity-aware behaviour. **A DS that ships interactive motion must specify interruption behaviour at the spec layer** (see 21); the framework primitives differ enough that omitting interruption from the spec produces inconsistent results.

---

## Lottie and Rive integration

The 2026 boundary is the same as on web: Lottie for playback, Rive for interactive state.

| Framework | Lottie runtime | Rive runtime | Notes |
|---|---|---|---|
| SwiftUI / UIKit | `lottie-ios` (Airbnb) | `rive-ios` | Lottie is mature; Rive runtime is small relative to the iOS app baseline |
| Compose | `lottie-compose` (Airbnb) | `rive-android` | Same shape; Rive's state-machine API maps cleanly to Compose state |
| Flutter | `lottie` package | `rive` package | Flutter's Rive runtime is the most-documented of the set; designers and engineers share vocabulary cleanly |
| React Native | `lottie-react-native` | `rive-react-native` | Rive RN runtime has historically lagged; check current version before scoping |

**The 2026 decision rule.** Use Rive for any motion that needs to respond to app state (icons that transition through hover/pressed/loading/success; controls whose motion identity is part of the brand). Use Lottie for deterministic playback (onboarding illustrations, branded loaders, marketing motion). Use neither if the motion can be expressed with framework primitives — both runtimes add binary size, and Rive's runtime is non-trivial.

**When hand-coded animation is the right answer:**

- Anything that needs to interpolate based on runtime-computed values (drag offsets, scroll position).
- Anything that participates in the system's motion-token contract — Rive motion is parameterised inside the `.riv` file and does not naturally consume CSS-variable-style tokens.
- Anything that needs to interact with the framework's gesture system in tightly-coupled ways.

**The Lottie feature-parity gap.** Not all Lottie features render on all platforms. The Airbnb runtime documentation publishes a compatibility matrix; the practice should consult it before any client commits to a Lottie animation in the brand language. Common failure modes: text layers, masks, mattes, certain effects. The pragmatic mitigation is to use the LottieFiles preview-on-target tool before signing off.

---

## Reduce-motion per framework

Detailed architectural treatment is in 14-accessibility and 16-mobile-accessibility-implementation. The motion-specific spelling:

| Framework | Detection API | Notes |
|---|---|---|
| SwiftUI | `@Environment(\.accessibilityReduceMotion)` | Reactive; updates on system setting change |
| UIKit | `UIAccessibility.isReduceMotionEnabled` + `reduceMotionStatusDidChangeNotification` | Notification-based |
| Compose | `LocalConfiguration.current.fontScale` is *not* this; use `AccessibilityManager.isAnimationDisabled` (Compose 1.7+) | Or check via `LocalAccessibilityManager` |
| Flutter | `MediaQuery.disableAnimationsOf(context)` | Reactive |
| React Native | `AccessibilityInfo.isReduceMotionEnabled()` | Async; subscribe to `reduceMotionChanged` for updates |

**Framework defaults.** Some framework defaults already respect reduce-motion (SwiftUI's `.spring(.default)` shortens in reduce-motion contexts; UIKit's `UIView.animate` does not — engineers must gate manually). The DS contract is that *every* animation gates on the system setting, regardless of whether the framework default would handle it. This makes the contract uniform across frameworks and removes the per-framework reasoning burden from individual engineers.

---

## Performance characteristics

| Framework | Frame rate target | Common drop causes | Profiling tool |
|---|---|---|---|
| SwiftUI | 60Hz baseline; 120Hz on ProMotion devices | Excessive view rebuilds inside animation, AttributeGraph cycles | Instruments — SwiftUI template, Animation Hitches template |
| UIKit | 60Hz baseline; 120Hz on ProMotion | Off-screen rendering, large `cornerRadius` with `clipsToBounds`, expensive layer effects | Instruments — Core Animation template |
| Compose | 60Hz baseline; 120Hz on LTPO devices | Recomposition storms, expensive Layout passes in animated subtrees | Android Studio Layout Inspector, Macrobenchmark, Compose Recomposition Counts |
| Flutter | 60Hz baseline; 120Hz on supported devices | Heavy build methods, oversized shaders, jank on Skia/Impeller transition | Flutter DevTools, Performance Overlay |
| React Native | 60Hz baseline; 120Hz reaches via Reanimated worklets | JS-thread animation (legacy `Animated`), bridge serialisation overhead | Flipper, Reanimated DevTools |

**The JS-thread / UI-thread distinction in React Native.** The single biggest performance lever on RN is whether motion runs on the JS thread (legacy `Animated`) or the UI thread (Reanimated worklets). On the JS thread, any JS work — even unrelated React rendering — blocks the animation. On the UI thread, animations run independently of JS work. The DS should require Reanimated for any motion work; the practice should specify Reanimated as a non-negotiable for new RN engagements.

**Threading on Compose and SwiftUI.** Both frameworks separate animation state from animation execution. State changes happen on the main thread; the framework's render engine interpolates and rasterises off-thread. The implication: cheap state changes drive expensive-looking animations without main-thread cost, *provided the animated value doesn't trigger a re-layout cascade.*

**The 120Hz design target.** All four frameworks now support 120Hz on modern hardware. The baseline performance budget is 120Hz, not 60Hz. A motion that lands at 60fps on a 120Hz display reads as broken in the same way a motion that lands at 30fps on a 60Hz display would have read three years ago. The DS should validate motion on a 120Hz device before signing off.

**Compositor vs. layout properties.** The web's compositor-safe-properties discipline has rough mobile equivalents:

- **iOS / SwiftUI / UIKit** — opacity and transform (translation, scale, rotation) run on the render server / Core Animation off the main thread. Layout-affecting properties (frame, size) trigger main-thread layout.
- **Compose** — `graphicsLayer` modifier moves expensive properties off the main thread. Use `graphicsLayer { translationX = … }` for animated translation rather than animating `Modifier.offset`.
- **Flutter** — implicit widgets that animate opacity and transforms are cheap; widgets that animate layout (`AnimatedSize`) trigger relayout each frame.
- **React Native (Reanimated)** — worklets running on the UI thread can animate any property cheaply; the JS-thread-based `Animated` API has the same compositor-property constraint as the web.

---

## The spec-to-code bridge per framework

Detailed treatment in 21. The mobile-specific notes:

**Motion tokens as the primary handoff.** Same as on web. A motion spec that names `spring/snappy` and a trigger collapses to one line of framework code that reads the token from the platform's token surface (Style Dictionary outputs, or the framework's design-token integration).

**Lottie remains the canonical artefact for branded playback motion.** All four frameworks have mature Lottie runtimes; the artefact is portable across them.

**Rive is the right artefact for interactive motion components on mobile.** The 2026 case for Rive on mobile is stronger than on web because the runtime cost is a smaller fraction of the app's binary size, and the interactive motion identity Rive ships maps cleanly to the system-icon and animated-control use cases that recur in mobile DS work.

**AI coding agents and mobile motion.** The cross-framework spring-vocabulary divergence is exactly the kind of thing AI agents get wrong without explicit guardrails. An agent producing Compose code from a generic motion brief will pick `spring(0.8f, 1500f)` from training-data defaults rather than the system's `spring/snappy` mapping. The fix is to surface the per-framework spring parameter table (above) in the agent's context (`AGENTS.md`, `CLAUDE.md`, MCP). With this surfaced, agents produce framework-idiomatic motion that respects the system's tokens.

**The Figma → mobile motion pipeline.** Figma's MCP server surfaces motion variables to AI agents (2025–2026). For mobile specifically, the gap that remains is the Figma → native-spring-parameter translation — the perceptual spring token in Figma needs to land as the right `(dampingRatio, stiffness)` on Compose, the right `(duration, bounce)` on SwiftUI, etc. This is the calibration step the practice has to own until Figma's tooling closes it.

---

## Failure modes to watch

- **Spring parameters copied verbatim across frameworks.** The same `(stiffness: 200, damping: 25)` produces different perceptual outcomes on Compose, Flutter, and Reanimated. The token name is portable; the parameters are not.
- **Lottie used for interactive motion.** Lottie is a playback format; interactive Lottie is a hack. Rive is the 2026 answer.
- **Legacy RN `Animated` API on the JS thread.** Any motion shipping through `Animated` (not `react-native-reanimated`) is on the wrong thread and will jank under any JS-thread contention. The DS should require Reanimated.
- **SwiftUI `.animation(_:)` without a value parameter.** The implicit `.animation(_:)` modifier (without `value:`) is deprecated and animates every state change — including unrelated ones. New code uses `.animation(_:value:)` with a specific value to scope the animation.
- **Compose recomposition storms inside animated subtrees.** An animation that triggers recomposition of a large subtree on every frame is the most common Compose jank source. The fix is `Modifier.graphicsLayer { … }` for transforms, which doesn't trigger recomposition.
- **Flutter heavy `build()` methods inside `AnimatedBuilder`.** A common Flutter performance footgun. The animation runs every frame; if the `build()` inside `AnimatedBuilder` is expensive, every frame is expensive.
- **AI agents picking native springs from training-data defaults.** Without the system's spring parameter table in agent context, agents produce parameters that work but are off-brand. Compounds across components.
- **Reduce-motion checked only on app launch.** The system setting can change while the app is running; the DS should subscribe to the change notification on every framework (SwiftUI's `@Environment` does this automatically; UIKit and RN require explicit subscription).

---

## Tensions and open questions

1. **Cross-framework spring calibration as an explicit practice deliverable.** The mapping table in this file is a starting point; the practice should ship calibration videos (the same spring on each framework, side-by-side) with every motion-tokenised DS engagement. This is currently a gap.

2. **Reanimated as a required RN dependency.** The argument for requiring it: legacy `Animated` is structurally wrong for 2026 motion. The argument against: it adds a non-trivial dependency to the RN bundle. The practice should default to requiring it for any RN engagement where motion is part of the success criteria and document the exception when it isn't.

3. **Rive as cross-platform motion artefact vs. per-framework hand-coding.** Rive's pitch is one artefact across all four frameworks. The trade-off is binary size, runtime version skew across platforms, and the loss of token-driven motion identity (Rive parameters live inside the `.riv` file, not the system's token surface). For interactive iconography and motion-as-component, Rive wins. For animation that should compose from system tokens, hand-coded animation per framework wins.

4. **Compose Multiplatform's motion story on iOS.** Compose MPP can render on iOS; motion in CMP on iOS uses Compose's spring vocabulary, not SwiftUI's. The cross-platform consistency claim of CMP works only if the team accepts that iOS motion will be authored in Compose's idiom rather than SwiftUI's. Whether this is a Hill or a strength depends on the engagement; flagged also in 09 §1.18.

5. **The motion-token surface on each framework.** SwiftUI consumes design tokens through Swift constants or extensions; Compose through Material's theming system or a custom `CompositionLocal`; Flutter through `ThemeData` or a custom inherited widget; RN through context or a token package. None of these is wrong; none is consistent across frameworks. The practice should ship a Style Dictionary output per framework for motion tokens, the same way it does for color and type.

6. **Shared element transitions as system-level abstraction.** Each framework has the primitive (post-2024); none has named the *system pattern* yet. The practice should ship "SharedHero" and "SharedCard" as cross-framework named patterns with per-framework implementations. This is a near-term opportunity.

---

## See also

- **18-motion-foundations** — the spring token vocabulary (snappy/gentle/bouncy) and the perceptual-vs-physical token discipline this file implements.
- **19-motion-implementation-web** — the web-side parallel; the cross-platform calibration this file's spring tables anchor.
- **21-motion-spec-and-handoff** — the designer-to-engineer spec contract; Rive `.riv` files as the canonical interactive-motion handoff.
- **11-mobile-and-cross-platform** — platform context, framework choice rationale.
- **14-accessibility** and **16-mobile-accessibility-implementation** — reduce-motion architectural treatment and per-framework accessibility implementation.
- **15-ai-in-ds** — AI agents and the components-as-data / token-context prerequisite.

---

*Provenance: Cross-framework primitives, the spring parameter mapping table, shared-element transition convergence (matchedGeometryEffect / SharedTransitionLayout / Hero / sharedTransitionTag), the implicit/explicit split per framework, threading and 120Hz treatment, per-framework reduce-motion detection APIs, and the Rive/Lottie 2026 boundary are synthesised from the dual-agent research outputs in `_research/_inbound/2026-05-14-motion-implementation-mobile/` (May 2026). The 2024 SwiftUI perceptual spring (`duration:bounce:`) is from Apple's SwiftUI 5 release notes (WWDC 2023). Compose `SharedTransitionLayout` is from Compose 1.7.0 (July 2024). The cross-framework calibration argument and the failure modes section are internal POV. The Reanimated-as-required argument is internal POV building on the research output's strong recommendation. Apple HIG motion guidance, Material 3 motion documentation, Flutter animation documentation, and Reanimated 3.x documentation are the primary per-framework references.*

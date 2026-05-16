# Motion implementation on mobile — cross-framework

> Implementation-level synthesis of mobile motion across SwiftUI/UIKit, Jetpack Compose, Flutter, and React Native. Audience: a senior DS lead translating a designer's motion spec into idiomatic, performant code in four runtimes. The architectural case for motion as a system foundation is researched separately; reduce-motion architecture is in `16-mobile-accessibility-implementation`. Version-dated where it matters; verification path is the references section.

---

## 1. Animation primitives by framework

The four frameworks split cleanly along two axes: **declarative vs. imperative** (what the engineer writes), and **value-driven vs. state-driven** (what triggers the animation). SwiftUI, Compose, and Flutter's implicit widgets are declarative and state-driven. UIKit, Flutter's explicit controllers, and React Native's `Animated` are imperative and value-driven. Reanimated 3 (now Reanimated 4 in late 2025) is a hybrid: declarative shared values on the UI thread with worklet-based callbacks.

### SwiftUI

SwiftUI's two animation surfaces are `.animation(_:value:)` and `withAnimation { … }`. The mental model is: state changes, the view recomputes, and any properties that differ between the old and new view tree are interpolated according to the animation curve attached to the relevant value. There is no animation object the engineer holds; the animation is a transient property of a state transition.

The defaults are unusually good. `withAnimation` with no argument uses a smooth spring (post-iOS 17 this is the perceptual spring family — `.smooth`, `.snappy`, `.bouncy` — which are response/dampingFraction springs with sensible defaults). For 90% of "this property should ease to its new value" cases, `withAnimation { state = newValue }` is correct and complete.

Engineers must override when: (a) they need explicit control over interruption — SwiftUI animations are interruptible by default but the new animation's curve replaces the old, which is sometimes wrong; (b) they need a keyframed timeline (`KeyframeAnimator`, iOS 17+); (c) they need a custom timing curve that isn't expressible as a spring. The `Animation.timingCurve(_:_:_:_:)` cubic-bezier API exists but is the escape hatch, not the idiom.

### UIKit

UIKit's two animation surfaces are the block-based `UIView.animate(withDuration:…)` family and `UIViewPropertyAnimator`. The block API is imperative — set properties inside the block, the runtime captures the start/end values and interpolates. `UIViewPropertyAnimator` is the modern variant: an animator object you can pause, scrub, reverse, and chain. Anything interactive (gesture-driven sheet dismissal, scrub-to-rewind) routes through `UIViewPropertyAnimator` or its predecessor `UIPercentDrivenInteractiveTransition`.

`CABasicAnimation` and `CAKeyframeAnimation` on `CALayer` sit beneath UIKit and are where you reach when you need to animate properties the view layer doesn't expose (mask paths, shadow paths, stroke positions) or when you need an explicit `CADisplayLink`-driven curve. The cost is that Core Animation animations are presentation-layer only — the model layer doesn't change, so on completion you must commit the final value yourself.

Defaults are not good. `UIView.animate` defaults to ease-in-out at 0.25s; this is a 1990s curve that nothing modern uses. Any DS-grade UIKit work overrides with `UISpringTimingParameters` or a custom `UICubicTimingParameters`. Spring support was added to `UIView.animate` in iOS 9 (`usingSpringWithDamping`) but the modern path is `UIViewPropertyAnimator(duration:timingParameters:)` with a `UISpringTimingParameters(dampingRatio:initialVelocity:)`.

### Jetpack Compose

Compose's three primary surfaces are `animate*AsState` (e.g. `animateFloatAsState`, `animateColorAsState`, `animateDpAsState`), `updateTransition` (state-machine-based animation of multiple properties to a coordinated end state), and `Animatable` (the imperative escape hatch, owns a value and exposes `animateTo` / `snapTo` / `stop`).

`animate*AsState` is the implicit/state-driven idiom. You write `val alpha by animateFloatAsState(targetValue = if (visible) 1f else 0f)` and the value animates whenever the target changes. `updateTransition` is the multi-property variant — when you need three properties to animate to coordinated end values driven by one state. `Animatable` is what gestures and complex interruption stories actually use under the hood.

There is also `AnimatedVisibility` and `AnimatedContent` for entrance/exit and content swapping. These are wrappers that compose `updateTransition` with appropriate `EnterTransition` / `ExitTransition` defaults. `Crossfade` is the simplest of these and is fine for fade swaps.

Compose's defaults moved to spring-based in Compose 1.4 (early 2023). `animate*AsState` defaults to a `spring()` with the visibility-threshold-aware dampingRatio of `Spring.DampingRatioNoBouncy` and `Spring.StiffnessMedium`. This is sensible. The Material 3 motion library (`MotionScheme`, introduced as expressive motion in late 2024 / early 2025) provides a tokenised spring set that ships with the design system.

### Flutter

Flutter's split is the cleanest of the four: **implicit widgets** (`AnimatedContainer`, `AnimatedOpacity`, `AnimatedAlign`, `AnimatedDefaultTextStyle`, and the rest of the `Animated*` family) and **explicit animation** (`AnimationController` + `Animation<T>` + `AnimatedBuilder`/`AnimatedWidget`).

Implicit widgets are pure declarative: change a property on the widget, supply a `duration` and `curve`, and Flutter interpolates between the old and new value. Internally this is a `Tween` driven by an `AnimationController`, but the engineer doesn't manage the controller.

Explicit animation is for everything else. The pattern is: a `StatefulWidget` with a `SingleTickerProviderStateMixin`, an `AnimationController` owned by the state, one or more `Tween` or `CurvedAnimation` objects driving derived values, and an `AnimatedBuilder` rebuilding the subtree on each tick. This is more ceremony than any other framework, but it's also the most explicit: you hold the controller, you know exactly when it ticks, you can `.forward()`, `.reverse()`, `.repeat()`, `.fling()`, and chain via `await controller.forward()` because controllers return futures that complete on animation end.

Defaults: Flutter has no opinionated default curve. `AnimatedContainer` defaults to `Curves.linear`, which is wrong for almost everything. DS-grade Flutter wraps `Animated*` widgets with project-default curves and durations. Material 3 motion in Flutter (via `flutter_animate` or the `material` library's `MotionScheme` analogue) is improving but is not yet on parity with Compose's tokenised motion.

### React Native

Two surfaces, both libraries: `Animated` (in React Native core) and Reanimated (Software Mansion, now version 4 — released October 2025). In 2026, Reanimated has won decisively for any DS-grade work. `Animated` is still acceptable for opacity-only fades and trivial cases, but anything gesture-driven, anything interruptible, anything that needs to feel native runs Reanimated.

The mental model is fundamentally different from the other three frameworks because of React Native's bridge architecture. `Animated` runs on the JS thread and either commits values to native every frame (slow, drops frames under JS load) or uses `useNativeDriver: true` to serialise the animation and run it on the UI thread (fast, but limited to layout-independent properties: `transform`, `opacity`).

Reanimated rewrites this. **Shared values** (`useSharedValue`) are mutable references that live in a parallel JS runtime on the UI thread (a "worklet" runtime). **Worklets** are JS functions marked with `'worklet'` that run on the UI thread. Animation primitives — `withTiming`, `withSpring`, `withDecay`, `withSequence`, `withDelay`, `withRepeat` — are worklet-compatible drivers that animate shared values without touching the JS thread. `useAnimatedStyle` derives a style object from shared values on the UI thread and applies it to the view. The result: 60/120fps animations that don't drop frames when the JS thread is blocked.

The defaults: `withTiming` defaults to 300ms `Easing.inOut(Easing.quad)`; `withSpring` defaults to a reasonably damped spring. Neither is great as a DS default; both need to be wrapped behind tokenised wrappers.

### Cross-framework comparison

| Concern | SwiftUI | UIKit | Compose | Flutter | RN (Reanimated) |
|---|---|---|---|---|---|
| Declarative? | Yes | No | Yes | Both | Yes |
| Default driver | Spring | Ease-in-out 0.25s | Spring (since 1.4) | Linear | Timing 300ms |
| Idiomatic implicit | `withAnimation` / `.animation(_:value:)` | n/a | `animate*AsState` | `Animated*` widgets | `useAnimatedStyle` over `useSharedValue` |
| Idiomatic explicit | `KeyframeAnimator` / `Animatable` | `UIViewPropertyAnimator` | `Animatable` / `updateTransition` | `AnimationController` | `withSequence` / worklets |
| Thread story | UI thread, GPU compositing | UI thread, Core Animation | UI thread, RenderThread | UI thread, Skia/Impeller | UI thread via worklets |
| Default curve quality | Excellent (iOS 17 perceptual) | Poor | Good | Poor | Adequate |

**Where the field has converged:** four of the five surfaces are declarative and state-driven by default. UIKit is the holdout, retained mainly for interactive transitions, legacy code, and `UICollectionView` choreography. The declarative shape is now the idiom.

### Mental-model differences that bite

The thing senior engineers underestimate when crossing frameworks is the difference in **when the animation value is read**. SwiftUI reads animated values during `body` evaluation, which means an animated value is a *function of view identity and state at that frame*. Compose reads them during composition, which is roughly equivalent. Flutter's implicit widgets read them during `build`. UIKit's `UIView.animate` doesn't "read" anything — it reflects model-layer property changes into presentation-layer interpolations. Reanimated reads on the UI thread via the worklet runtime, side-stepping the React render cycle entirely.

The practical consequence: when you build a DS-grade motion-aware component, the boundary between "this property is animated" and "this property triggers a recomposition that animates" is different per framework. In Compose, expensive recompositions during animation are the dominant performance problem and the idiom is to push animated reads down to `Modifier.graphicsLayer { … }` so they never trigger composition. In SwiftUI, the equivalent is keeping the animated property as a small leaf state, not bubbling it up. In Flutter, use `AnimatedBuilder` to scope rebuilds. In Reanimated, reads inside `useAnimatedStyle` never touch React at all — they're free. This is the single biggest performance lever in each framework and it manifests differently in each.

---

## 2. Spring and physics

The convergence in the last five years is that springs replaced cubic-bezier curves as the default for state-change animation. The reason is well-rehearsed: springs are interruption-friendly (they preserve velocity across state changes), they're parameterised by perceptual qualities (bouncy/snappy/smooth) rather than abstract curve coefficients, and they handle distance-invariant timing better than fixed-duration tweens.

### Parameterisations

The four frameworks expose three different parameterisations of the same underlying damped harmonic oscillator:

**SwiftUI** uses **response / dampingFraction** (sometimes called the Apple parameterisation). `response` is roughly the period of one oscillation in seconds — how long the spring "feels" — and `dampingFraction` (0..1) is how quickly it settles. iOS 17 introduced the **perceptual spring family**: `.smooth` (no bounce, ~0.5s response), `.snappy` (slight bounce, faster), `.bouncy` (visible bounce). These are the modern idiom. The legacy `.spring(response:dampingFraction:blendDuration:)` and `.interactiveSpring()` still work.

**Compose** uses **dampingRatio / stiffness**. `Spring.DampingRatioNoBouncy = 1f`, `Spring.DampingRatioLowBouncy = 0.75f`, `Spring.DampingRatioMediumBouncy = 0.5f`, `Spring.DampingRatioHighBouncy = 0.2f`. `Spring.StiffnessLow / Medium / High / VeryHigh` cover the speed axis. Material 3 expressive motion (2024–2025) ships a `MotionScheme` with `standard`/`expressive` token sets, each providing fast/default/slow springs.

**Flutter** uses **SpringDescription(mass, stiffness, damping)**, the physics-textbook parameterisation. `SpringSimulation(SpringDescription(mass: 1.0, stiffness: 100.0, damping: 10.0), startPosition, endPosition, velocity)` drives a controller via `controller.animateWith(simulation)`. Flutter is the most physically literal of the four and the least convenient for designers — `mass: 1, stiffness: 100, damping: 10` is not a readable spec.

**React Native (Reanimated)** uses two overloads: a Compose-like `stiffness / damping / mass` triple, and an Apple-like `duration / dampingRatio` pair. Reanimated 3 added the duration-based overload explicitly to ease iOS-Android-RN parity. Defaults: `stiffness: 100, damping: 10, mass: 1` — physically equivalent to Flutter's default.

### Cross-framework comparison table

| Framework | Parameterisation | Perceptual presets | Physical parameters |
|---|---|---|---|
| SwiftUI | response / dampingFraction | `.smooth`, `.snappy`, `.bouncy` (iOS 17+) | Yes via `.interpolatingSpring(mass:stiffness:damping:initialVelocity:)` |
| UIKit | dampingRatio / initialVelocity (`UISpringTimingParameters`) | None | Yes |
| Compose | dampingRatio / stiffness | `Spring.*` constants + `MotionScheme` tokens (2024+) | Yes via `spring(visibilityThreshold:)` |
| Flutter | mass / stiffness / damping | None in core; `flutter_animate` provides presets | Yes (this is the only API) |
| Reanimated | Either dampingRatio/duration OR stiffness/damping/mass | None | Yes |

### Cross-framework standardisation

For a multi-framework DS, the practical advice is to **tokenise springs at the perceptual level** (smooth / snappy / bouncy / expressive — or whatever set your motion design lead settles on) and provide a per-framework adapter that resolves each token to the framework's native parameterisation. Don't try to ship a single `(mass, stiffness, damping)` triple across all four — it works mathematically but is brittle when one framework's runtime damps differently, and it ignores SwiftUI's perceptual presets which are genuinely better than a literal physical match.

A reasonable convergence:

| Token | SwiftUI | Compose | Flutter | Reanimated |
|---|---|---|---|---|
| `motion.spring.smooth` | `.smooth` | `spring(0.9f, StiffnessMedium)` | `SpringDescription(1, 200, 26)` | `{ damping: 26, stiffness: 200, mass: 1 }` |
| `motion.spring.snappy` | `.snappy` | `spring(0.85f, StiffnessMediumLow)` | `SpringDescription(1, 300, 30)` | `{ damping: 30, stiffness: 300, mass: 1 }` |
| `motion.spring.bouncy` | `.bouncy` | `spring(0.55f, StiffnessMediumLow)` | `SpringDescription(1, 180, 12)` | `{ damping: 12, stiffness: 180, mass: 1 }` |

(Numerical values approximate; calibrate against your reference motion in each runtime — the cross-platform feel is never bit-identical and trying to make it so produces uniformly worse motion in every framework.)

### Where the field has converged

Material 3 expressive motion (2024), Apple's perceptual spring family (iOS 17, 2023), Reanimated 3's duration/dampingRatio overload (2023), and Compose's `MotionScheme` (2025) all moved the same direction: a small named set of springs exposed as tokens, with physical parameters available as the escape hatch. The DS-grade implementation in 2026 follows this convergence rather than fighting it.

### The case for springs as default

The argument that finally won: **fixed-duration tweens lie about distance.** A 300ms ease-out animating 8px and 800px takes the same time, which means the 8px case is glacial and the 800px case is rushed. A spring sized by perceptual response handles both well — the 8px case settles in under a third of a second because there isn't far to go; the 800px case takes proportionally longer because there is. Velocity preservation under interruption follows for free: a spring evaluates from `(currentValue, currentVelocity)` to `(targetValue, 0)`, so a new spring picked up mid-flight just changes the target.

The remaining role of cubic-bezier curves is for **deterministic motion that must sync to external timing** — a server-driven progress bar, a video-scrubber, an audio waveform. Anything synced to a clock that isn't the animation's own should use timed curves; everything else should use springs. Across the four frameworks, this is now consensus.

---

## 3. Choreography and orchestration

Choreography splits into three concerns: sequencing/stagger within a screen, shared-element/hero transitions between screens, and route transitions themselves.

### Sequencing and stagger

**SwiftUI**'s idiom for stagger is per-element animation delays plus `transition` modifiers, or the iOS 17+ `PhaseAnimator` / `KeyframeAnimator` for choreographed sequences. For a list of cards entering, the convention is `.transition(.opacity.combined(with: .offset(y: 10)))` on each card, and the parent `withAnimation` driving the state change — the implicit per-element entry is itself implicitly staggered if you key the cards by identity and insert them sequentially, but explicit stagger needs explicit `.animation(.spring().delay(Double(index) * 0.05))`. `PhaseAnimator` (iOS 17) is the cleanest path for "go through these N phases in sequence".

**UIKit**'s idiom is `UIView.animateKeyframes` for choreographed timelines, or chained `UIViewPropertyAnimator` instances via `addCompletion`. `UICollectionView`'s `performBatchUpdates` plus layout-driven transitions handles list stagger when you let the layout do the animating. For DS-grade UIKit stagger, the typical pattern is a small `Choreographer` helper that owns an array of animators and starts them with offsets.

**Compose** uses `AnimatedVisibility` with `enter`/`exit` transitions for individual elements, and the parent's recomposition naturally produces stagger when items are added incrementally. For explicit stagger, the idiom is `delayMillis` on the spring or tween, parameterised by index. `LazyColumn` and `LazyRow` animate item additions/removals via `animateItemPlacement()` (now `Modifier.animateItem()` since Compose 1.7, mid-2024). For multi-property coordinated transitions, `updateTransition` with multiple `animate*` extension calls on the transition is the idiom.

**Flutter**'s idiom for staggered animations is documented as the "staggered animation" pattern: a single `AnimationController` with multiple `CurvedAnimation`s using `Interval(begin, end, curve: …)` to map sub-ranges of the controller's 0..1 to different property animations. One controller, many tweens, each gated by an interval. This is more verbose than the other three but very explicit about timing.

**React Native / Reanimated** sequences via `withSequence(withTiming(...), withTiming(...))` and `withDelay(delayMs, withTiming(...))`. Stagger is index-based delay on `withDelay`. `Layout` animations and the `entering`/`exiting` props on `Animated.View` (Reanimated 3+) handle list entrance choreography declaratively — `entering={FadeIn.delay(index * 50)}`.

### Shared-element / hero transitions

This is where the frameworks diverged most until recently, and where 2024–2025 produced significant convergence.

**SwiftUI**: `matchedGeometryEffect(id:in:)` is the primitive, available since iOS 14. Two views in different parts of the hierarchy share an ID and a `Namespace`; when one is removed and the other inserted, SwiftUI interpolates the geometry between them. Works well within a single view; works less well across `NavigationStack` boundaries until the iOS 18 (2024) `navigationTransition(.zoom(sourceID:in:))` API, which finally bridged matched-geometry into navigation transitions properly.

**UIKit**: `UIViewControllerAnimatedTransitioning` is the primitive. You snapshot the source view, position it over the destination, animate the snapshot to the destination's frame, and reveal the destination. The infrastructure is verbose; production code typically uses `Hero` (the Swift library) or builds a small custom transition coordinator. iOS 18's `UINavigationController` zoom transition (system-provided) is the modern idiom for the common case.

**Compose**: `SharedTransitionLayout` and `Modifier.sharedElement(...)` shipped stable in Compose 1.7 (mid-2024). This was the major missing piece in Compose's animation story for years. The pattern is: wrap a region in `SharedTransitionLayout`, give matched elements a shared key, and call `sharedElement(rememberSharedContentState(key), animatedVisibilityScope)` on each. The integration with Navigation Compose's `composable` destinations works via `AnimatedContentScope`. As of 2026, this is the canonical Compose pattern.

**Flutter**: `Hero` is the original and still the idiom. Wrap source and destination with `Hero(tag: 'same-tag', child: ...)` and Flutter's `Navigator` handles the rest. The implementation is older than Compose's and well-debugged; it works across all `Navigator` transitions out of the box. The flightShuttleBuilder hook lets you customise the in-flight widget. The constraint: matched elements must be identifiable by an `Object` tag (typically a string or UUID) and the source must be present in the source route's widget tree.

**React Native**: historically the weakest of the four. `react-native-shared-element` (an unofficial library, Wojtek Trzcinski / IjzerenHein) bridges native iOS/Android shared-element transition APIs. In 2024–2025, Reanimated's shared transitions API (`SharedTransition`, experimental) moved this in-tree, but as of early 2026 it's still labelled experimental and most production code uses `react-native-shared-element` with `react-navigation`'s shared element bindings, or builds a custom solution using Reanimated's `measure` + absolute positioning. This is the framework where the DS lead has to do the most work.

### Route / screen transitions

| Framework | Primitive | Library role |
|---|---|---|
| SwiftUI | `NavigationStack` + `navigationTransition` (iOS 18+) | First-party; transitions customisable from iOS 18 |
| UIKit | `UIViewControllerAnimatedTransitioning` | First-party but verbose; libraries like `Hero` for the common case |
| Compose | `composable(enterTransition = …, exitTransition = …)` in Navigation Compose | Navigation Compose owns it; transitions are `EnterTransition`/`ExitTransition` |
| Flutter | `PageRouteBuilder` / `PageTransitionsTheme` | First-party; `Navigator 2.0` / `go_router` both delegate transitions to `PageRoute` |
| React Native | `react-navigation`'s `cardStyleInterpolator` / `transitionSpec` | Navigation library owns it; Reanimated 3+ enables custom interpolators on UI thread |

The cross-framework lesson: **don't standardise route transitions as part of the DS** — standardise them per-platform, because the navigation library is the authoritative owner and platform conventions (iOS push-from-right, Android shared-axis, Material 3 container transform) differ on purpose. The DS owns the durations and curves; the navigation library owns the geometry.

### Choreography as a DS concern

The cross-framework standardisation worth investing in is the **vocabulary** of choreography, not the implementation. A DS motion spec that names patterns — `enter.stagger.cascade`, `exit.dismiss.together`, `transition.contained.expand` — and provides per-framework implementations against those names is what scales. Don't write four cookbooks; write one vocabulary and four adapters.

The traps:
- **Cross-fade ≠ shared-element transition.** A common mistake on RN is approximating shared transitions with a cross-fade and a position interpolation. It looks broken on devices with high refresh rates because the eye reads the discontinuity. Use a real shared-element implementation or accept that the transition will be a stack push, not a hero.
- **Stagger delays accumulate.** A 50ms-per-item stagger across 20 items is a one-second cascade — too slow. Decay the delay (`min(50 * index, 400)`) or use a curve-based stagger function. Every framework gives you the loop; none gives you the perceptual decay.
- **Choreographed exit before enter is universally wrong.** Cross-framework, the convention is that exit and enter overlap by ~50% — pure-sequential animation (exit completes, then enter starts) reads as broken on every platform. Wire this into the DS adapter, not into each component.

---

## 4. Implicit vs. explicit animation patterns

The decision framework that holds across all four frameworks:

- **Reach for implicit when** the animation is a side effect of a state change, animates a single property or small coordinated set, has no interactive interruption requirement, and doesn't need to be reversed or scrubbed.
- **Reach for explicit when** you need timeline control, gesture-driven scrubbing, interruption with custom blending, choreographed multi-property timelines, or animations that need to be paused/resumed/reversed under user control.

The 80/20 rule: probably 80% of DS-grade motion is implicit; the 20% that's explicit is also the 80% of the engineering cost.

### Interruption stories

**SwiftUI**: interruption is automatic and usually correct. If a `withAnimation` block runs while a previous animation is in flight, the new animation takes over from the current presentation value, and if both use springs, velocity is preserved. The failure mode is when the two animations use different curve families (spring → ease) — velocity is lost and you get a visible discontinuity. The fix is to always use springs for interruptible state.

**UIKit**: interruption is manual unless you use `UIViewPropertyAnimator`, which exposes `pauseAnimation()`, `fractionComplete`, and `continueAnimation(withTimingParameters:durationFactor:)`. `UIView.animate` blocks fight each other — the second block starts a new animation but the first doesn't gracefully hand off; CALayer presentation values may snap. For interruptible UIKit motion, `UIViewPropertyAnimator` is mandatory.

**Compose**: `Animatable` handles interruption correctly — `animateTo` while another `animateTo` is in flight cancels the previous and continues with current velocity. `animate*AsState` is built on `Animatable` so inherits this. The failure mode is mixing `animate*AsState` with manual state mutations on the same property — recomposition order can produce jumps. The fix is to keep one source of truth per animated property.

**Flutter**: `AnimationController` interruption is explicit — `controller.stop()` then `controller.animateTo(newTarget)`. Velocity is not preserved by default; you have to read the controller's current velocity (which the `AnimationController` exposes via `velocity`) and pass it to the next `SpringSimulation` if you want continuity. This is more bookkeeping than the other three, but it's also the most explicit. Implicit widgets (`AnimatedContainer` and friends) handle interruption automatically.

**React Native / Reanimated**: `cancelAnimation(sharedValue)` cancels an in-flight animation; the next `withSpring` reads the current velocity from the cancelled animation and uses it as the starting velocity (since Reanimated 2.x, this is the default). This is the same correct behaviour as SwiftUI's springs. The failure mode: mixing `withTiming` and `withSpring` on the same value loses velocity at the handoff.

### Motion and gesture handling

**SwiftUI**: gestures and animation integrate via `@GestureState` and `interactiveSpring()`. The `DragGesture` updates a `GestureState` which drives view properties; on end, `withAnimation` settles to the target.

**UIKit**: `UIPanGestureRecognizer` updating view properties directly is the simple path; for snap-to-position-with-velocity, use `UIDynamicAnimator` or `UIViewPropertyAnimator` with `UISpringTimingParameters(dampingRatio:initialVelocity:)` passing the gesture's terminal velocity.

**Compose**: `Modifier.draggable`/`Modifier.pointerInput` plus `Animatable`. The pattern is `coroutineScope.launch { animatable.snapTo(dragValue) }` during drag, then `animatable.animateTo(snapTarget, initialVelocity = …)` on release.

**Flutter**: `GestureDetector` with `onPanUpdate` driving an `AnimationController.value`, then `controller.fling(velocity: …)` or `controller.animateWith(SpringSimulation(...))` on release.

**Reanimated**: `useAnimatedGestureHandler` (deprecated) or the newer `Gesture.Pan()` from `react-native-gesture-handler` 2.x, with worklet callbacks updating shared values. Because both gesture handling and animation run on the UI thread, gesture-driven animations are smooth even under JS load. This is Reanimated's biggest competitive advantage over the legacy `Animated` library.

### When implicit is wrong

A subtle failure mode shared by all four frameworks: implicit animation hides timing dependencies. If two implicitly-animated properties depend on the same state but are read by different widgets/views/composables, they animate independently and can desync visually. The fix is to lift the animation into an explicit driver (one `Animatable`, one `AnimationController`, one shared value) and derive both properties from it. The smell is "two animations that should look coordinated but don't quite line up." Every senior engineer who has shipped motion on these frameworks has been bitten by this; the cross-framework rule is **one driver per coordinated set of properties, even if you have to write more code to get there.**

---

## 5. Lottie and Rive integration

Lottie has been the default vector animation runtime for nearly a decade; Rive is the upstart that's been pushing into Lottie's territory since around 2022 and as of 2026 is a serious contender for any new DS work.

### Runtime support

**Lottie** ships first-party runtimes for iOS (`lottie-ios`, Airbnb), Android (`lottie-android`), React Native (`lottie-react-native`), and Flutter (`lottie` package, community-maintained but mature). The iOS and Android runtimes are written by Airbnb; the RN and Flutter ones are community-maintained but production-grade. For Compose, `lottie-compose` (Airbnb) wraps `lottie-android` with a Composable API. For SwiftUI, `LottieView` (Airbnb) wraps `lottie-ios`. All runtimes support After Effects export via the Bodymovin plugin and a subset of After Effects features (the unsupported-features list is long and is the constant source of "the designer's file doesn't look right in the app" tickets).

**Rive** ships first-party runtimes for iOS (`rive-ios`), Android (`rive-android`), React Native (`rive-react-native`), Flutter (`rive` package). Rive's pitch is interactivity (state machines), small file sizes, and a designer tool that's better than After Effects + Bodymovin for the kinds of UI motion DS work actually needs. Rive files are designed to be UI animations, not film effects; the state-machine model lets the runtime drive animations from app state without baking every variant.

### Trade-offs in 2026

| Concern | Lottie | Rive |
|---|---|---|
| File size | Larger; JSON-based, can be hundreds of KB | Smaller; binary `.riv` format, often <50KB |
| Interactivity | Limited; pause/play/scrub/segment | First-class; state machines, inputs, listeners |
| Designer tool | After Effects (general-purpose, expensive, complex) | Rive editor (purpose-built, free tier, simpler) |
| Runtime cost | Higher; JSON parsing + Skia-style rasterisation | Lower; native renderer per platform |
| Designer pool | Huge; any motion designer | Smaller but growing |
| Format stability | Mature; AE features evolve, Bodymovin lags | Younger; format updates more frequent |
| Vector-only? | Yes | Vector + mesh deformation + bone rigs |

The honest 2026 read: Rive is better for **UI motion that responds to state** (toggle states, progress indicators, illustration that reacts to user input). Lottie is better for **canonical brand motion that's the same every time** (splash, hero illustrations, marketing-driven decorative motion). Most DS work has both kinds.

### Hand-coded vs. exported asset — decision framework

Use exported assets (Lottie/Rive) when:
- Motion is illustrative or decorative (a celebration burst, a loading scene)
- The motion is designer-authored and won't survive translation into engineer-readable spec
- The same motion ships across all four frameworks and bit-identical playback matters
- Brand wants control over a specific look that's expensive to hand-code

Use hand-coded animation when:
- Motion is functional and tightly coupled to component state (button press, sheet present, list reorder)
- Motion needs to respond to gesture velocity or interruption
- Motion is parameterised by tokens (duration, curve, distance) that the DS owns
- The animation is small and routine — a 200ms fade does not need a Lottie file

The boundary: anything that's *system motion* (responds to system state, owned by the DS) should be hand-coded. Anything that's *brand motion* (authored by a motion designer, illustrative) should be exported. The line gets blurry for transitions like onboarding screens, where the answer is usually Lottie/Rive even if it could be hand-coded, because the iteration cost on the designer side dominates.

Framework-by-framework: all four runtimes are mature enough that the decision is not framework-bound. The exception is **React Native + Rive**: `rive-react-native` is younger than the other Rive runtimes and the New Architecture / Fabric integration was stabilised through 2024–2025; pin a known-good version and test the upgrade path before committing the DS.

### Practical integration notes per framework

**SwiftUI**: `LottieView` (Airbnb, since 2023's lottie-ios 4.x) is the native SwiftUI wrapper; for `rive-ios` the SwiftUI surface is `RiveViewModel` + `RiveViewRepresentable`. The lifecycle gotcha is that both runtimes hold animation state on a non-Combine `ObservableObject` — wiring state-machine inputs from SwiftUI requires careful `@StateObject` ownership.

**UIKit**: `AnimationView` (Lottie) and `RiveView` (Rive) are first-class `UIView` subclasses; integration is the most mature path for both runtimes. View controller transitions can drive Lottie/Rive scrub via `setProgress(_:animated:)`.

**Compose**: `lottie-compose`'s `LottieAnimation` composable is mature; `rive-android` exposes a `RiveAnimationView` that you wrap in `AndroidView`. For state-machine-driven Rive in Compose, the `rive-android` 9.x API improved Compose integration substantially.

**Flutter**: `lottie` (xvrh) and `rive` (Rive team) packages both work but differ in completeness — Flutter's Lottie support has historical gaps for certain AE features (masks, mattes); Rive on Flutter is more complete because Flutter is one of Rive's primary platforms.

**React Native**: as noted, the New Architecture story stabilised in 2024–2025. The other gotcha is that both Lottie and Rive RN packages historically had iOS/Android renderer differences — animations that rendered perfectly on iOS dropped a layer or rasterised text wrong on Android. Test both platforms with the actual designer-authored file before committing.

---

## 6. Reduce-motion respect per framework

The architecture is covered in `14-accessibility.md` and `16-mobile-accessibility-implementation.md`. The framework-specific spelling:

**SwiftUI**: `@Environment(\.accessibilityReduceMotion) var reduceMotion`. Gate animations with `reduceMotion ? .none : .smooth`. Many built-in transitions (`NavigationStack` defaults, `.transition` modifiers) honour the setting automatically; explicit `withAnimation` does not.

**UIKit**: `UIAccessibility.isReduceMotionEnabled` plus the `UIAccessibility.reduceMotionStatusDidChangeNotification` for live updates. UIKit honours the setting on system transitions (e.g. cross-dissolve replacement of slide-push); custom `UIViewControllerAnimatedTransitioning` must check it explicitly.

**Jetpack Compose**: `LocalAccessibilityManager.current` exposes the manager; the canonical check is `LocalView.current.context.getSystemService(AccessibilityManager::class.java).isAnimationsEnabled` — wrap behind a `@Composable fun rememberReduceMotion(): Boolean`. As of Compose 1.6+, the framework respects `Settings.Global.ANIMATOR_DURATION_SCALE` in some animation APIs (`animate*AsState` reads it when constructing default specs), but for choreographed `updateTransition` work the engineer must read it.

**Flutter**: `MediaQuery.of(context).disableAnimations` (Flutter 2.10+, late 2022). Implicit widgets in Flutter do **not** automatically honour this — the DS lead must wrap them. `flutter_animate` and the Material library have begun gating animations on it as of Flutter 3.13+, but coverage is incomplete; treat it as something to wire by hand.

**React Native**: `AccessibilityInfo.isReduceMotionEnabled()` plus `AccessibilityInfo.addEventListener('reduceMotionChanged', …)`. Reanimated does **not** automatically honour the setting; every `withTiming` / `withSpring` must be gated. The convention is a `useReduceMotion()` hook that returns a boolean and a wrapped `withTimingMaybe(value, config)` that short-circuits to `value` when reduce-motion is on.

In every framework, the pattern is the same: **read the setting, branch on it, return either the animated value or the target value directly.** Don't return a "0ms animation" — that still emits an animation event and on some screen readers produces an audible cue. Return the value directly.

---

## 7. Performance characteristics

### Frame rate targets

**iOS**: 60Hz baseline, ProMotion 120Hz on iPhone Pro from iPhone 13 Pro (2021) onwards, iPad Pro from 2017. Apple's animation APIs target the device's actual refresh rate automatically; CADisplayLink-driven custom animation should query `preferredFramesPerSecond` (deprecated) or use `CADisplayLink.preferredFrameRateRange` (iOS 15+).

**Android**: 60Hz baseline, 90/120/144Hz on most flagships since 2020. Android's choreographer dispatches frames at the display rate; Compose and Views animation APIs target the device rate. Note: Android 15 (2024) introduced `Window.setFrameRate()` for app-side hints, but most DS work doesn't need it.

**Cross-platform**: Flutter targets the device's native refresh rate via its own ticker. React Native + Reanimated targets the device rate as long as the animation runs on the UI thread; legacy `Animated` without `useNativeDriver` is capped by JS-thread throughput, typically dropping to 30–45fps under load.

### Dropped-frame causes

**SwiftUI**: layout invalidation cascades. A small state change that invalidates a large subtree's `body` recomputation drops frames even if the animation itself is cheap. Profiling: Instruments → Animation Hitches, SwiftUI tooling in Xcode 15+.

**UIKit**: off-screen rendering (rasterisation triggered by `shouldRasterize`, masking, shadows without `shadowPath`), main-thread blocking from synchronous I/O. Profiling: Instruments → Core Animation, Time Profiler.

**Compose**: recomposition cost on the animated frame, especially when animation drives values used by many composables. Read animated values as late as possible (inside `Modifier.graphicsLayer { translationY = offset.value }` rather than as parameters that trigger recomposition). Profiling: Android Studio's Layout Inspector + Compose recomposition counts, Macrobenchmark for jank.

**Flutter**: shader compilation jank (especially first-run after install — Skia historically; Impeller from Flutter 3.10+ mitigates this on iOS and from 3.27+ on Android), large widget rebuilds during animation, `setState` in animation listeners rebuilding the whole subtree (use `AnimatedBuilder` or `ValueListenableBuilder` to scope rebuilds). Profiling: DevTools → Performance, raster thread vs. UI thread separation.

**React Native (legacy Animated)**: JS-thread bridge serialisation; any animation without `useNativeDriver` drops frames when the JS thread is busy. `useNativeDriver` limits you to layout-independent properties.

**React Native (Reanimated)**: the issue moves from frame-rate to glitches at the worklet/JS boundary. Anything that crosses back to the JS thread (a callback to React, a `runOnJS`) blocks until the JS thread responds. Profiling: React Native Performance Monitor, Flipper plugin (deprecated 2024; now React Native DevTools), platform profilers underneath.

### Compositor / rasteriser story

**iOS**: Core Animation drives a GPU compositor. Layer-backed views animate on the GPU at native refresh rate when the animated properties are GPU-friendly (transform, opacity, position, bounds with non-mask content). Anything that requires re-rasterising the layer (text content changes, mask path animations on complex shapes) is expensive.

**Android**: RenderThread plus the GPU; from Android 5.0 onwards, the RenderThread can drive animations independently of the UI thread. Compose targets RenderThread for `graphicsLayer` properties; non-`graphicsLayer` modifiers force re-layout.

**Flutter**: Skia (pre-Impeller) or Impeller. Impeller pre-compiles shaders, eliminating the first-frame jank that plagued earlier Flutter. The raster thread takes the layer tree from the UI thread and rasterises; the only animations that are cheap are the ones that don't require new rasterisation (transform, opacity on `RepaintBoundary`-wrapped subtrees).

**React Native**: with Reanimated, animations driven by `useAnimatedStyle` and applied via the new architecture (Fabric, 2024+) commit values directly to the native shadow tree on the UI thread. The cost is roughly the platform-native cost (Core Animation on iOS, RenderThread on Android) plus a thin worklet-runtime overhead.

The general rule across all four frameworks: **animate transforms and opacity, not layout-driving properties**. Width/height/padding/margin animations force layout passes that cascade through the tree. Translate/scale/rotate/opacity animations are GPU-cheap.

### Common performance budget

A reasonable DS-grade budget across all four frameworks:

- Per-frame animation work: under 8ms on a mid-range device (target 120Hz devices well under 4ms, with the understanding that the device itself negotiates the actual rate)
- First-frame jank on screen entry: zero dropped frames after warm-up; one tolerated on cold start
- Concurrent animations: a screen running 5–10 simultaneous animations (list entrance + button feedback + scroll-driven hero) should stay within budget
- Lottie/Rive playback: budget separately; running a 200KB Lottie at full quality plus the rest of the UI animation costs more than the sum suggests

Cross-framework, the components most likely to exceed budget are: gradients with animated stops (rasterise every frame), shadow animations without precomputed shadow paths, blur effects (especially backdrop blur on Android pre-12 and Compose pre-1.6), and any animation that modifies text content rather than text transform.

### 60Hz vs. 120Hz convergence

By mid-2025, 120Hz is mainstream on flagship Android (Samsung S-series, Pixel 8 Pro+) and on iPhone Pro models. The DS implication is that **motion designed for 60Hz looks under-fluid on 120Hz devices**. Springs scale naturally — they generate more intermediate frames at higher refresh rates. Cubic-bezier curves don't scale as well — they sample more frames but the perceptual quality plateaus. This is one more vote for spring-as-default; the 120Hz transition has effectively retired fixed-duration tweens from new DS-grade work.

---

## 8. The spec-to-code bridge per framework

### What the engineer consumes

A motion spec at the DS-grade level is typically:
- A name / token (e.g. `motion.spring.snappy`)
- A duration or perceptual response
- A curve or spring parameters
- The properties animated (opacity, transform, position, scale)
- The trigger (state change, gesture, navigation event)
- Any delay or stagger relative to other elements

What the engineer actually consumes in each framework:

**SwiftUI**: a Swift `Animation` constant from a `Motion` enum or struct, applied to `withAnimation` or `.animation(_:value:)`. The token resolves to `.smooth`, `.snappy`, or a custom spring.

**UIKit**: a `UISpringTimingParameters` or `UITimingCurveProvider` from a motion catalogue, plus a duration. Used to construct `UIViewPropertyAnimator`s.

**Compose**: a `SpringSpec<T>` / `TweenSpec<T>` from the `MotionScheme` or DS-owned motion tokens, passed as the `animationSpec` parameter to `animate*AsState`, `updateTransition`, or `Animatable.animateTo`.

**Flutter**: a `Curve` + `Duration` pair, or a `SpringDescription`, from a `MotionTokens` class. Used to construct `CurvedAnimation`s or `SpringSimulation`s.

**React Native (Reanimated)**: an object literal — `{ duration: 300, easing: Easing.bezier(...) }` for `withTiming`, `{ damping, stiffness, mass }` or `{ duration, dampingRatio }` for `withSpring` — from a motion tokens module.

The cross-framework convention worth standardising: **the same token name resolves in each framework, the parameters are calibrated per framework rather than mechanically translated.**

### Lottie and Rive as canonical handoff

The pitch is real: a `.lottie` or `.riv` file is the only motion artefact that is genuinely identical across all four frameworks. For brand motion — illustration, splash, decorative — this is the right answer.

Where it doesn't work:
- **State-driven UI motion** (button press, toggle, sheet present). The motion needs to respond to interruption, gesture, and state in ways that an exported asset can't. Rive's state machines push at this boundary but for tight UI feedback, native APIs win.
- **Motion parameterised by DS tokens**. If the duration is supposed to be `motion.duration.short` and the curve `motion.spring.snappy`, the exported asset has those baked in; changing the token requires re-exporting.
- **Performance-critical motion**. The runtime cost of Lottie/Rive is a fraction of native animation but it's not zero, and for motion that runs constantly (loading indicator, scroll-driven hero) the native path is cheaper.

### AI code generation in 2026

The state of the art as of early-to-mid 2026:

- **Claude Code / Cursor / Codeium**: given a motion spec in prose, can produce competent first-draft animation code in all four frameworks. They are reliable for the common cases (fade-in on appear, spring on press, list item entrance) and unreliable for the harder cases (interruption-correct spring chains, gesture-driven scrubbing, choreographed multi-property timelines with custom phase intervals). The DS-grade workflow is: token catalogue exists, engineer asks the AI to wire a component using token X, AI produces code that uses the named token, engineer reviews.
- **Figma Make** (Figma's code-generation product): produces React/React Native and SwiftUI code with motion, including basic spring/transition matching from Figma's prototype interactions. As of 2026, the output is closer to scaffolding than production code, and the motion fidelity drops fast outside the cases Figma's prototype mode itself supports.
- **Figma Code Connect + MCP**: where mappings exist between Figma components and code components, the AI generation respects the DS component boundary. This is the main lever for shifting AI motion generation from "guesses what's probably right" to "uses the actual DS components and their motion tokens."

### Where automation has landed by 2026

Automated:
- Translating a named token (e.g. `motion.spring.snappy`) into framework-specific application code.
- Generating boilerplate `useAnimatedStyle` / `withAnimation` / `AnimatedContainer` wrappers around state changes.
- Exporting Lottie/Rive and dropping the playback widget into all four frameworks.

Still manual:
- Calibrating spring parameters perceptually across frameworks so the same token feels right in each.
- Choreographing multi-element timelines with custom stagger.
- Wiring gesture-driven interruption with velocity continuity.
- Deciding when to use a Lottie/Rive asset vs. hand-code.

The honest 2026 read: the bridge from designer intent to per-framework motion code is partially automated for the easy cases and unchanged for the hard ones. The DS investment that pays off is the **motion token catalogue with framework adapters** — once that exists, both AI tooling and engineers consume it the same way.

### What a useful motion spec looks like

The motion spec that minimises rework across four frameworks contains:

1. **A named token**, not raw parameters. `motion.spring.snappy`, not `damping: 26, stiffness: 200`.
2. **The trigger condition** — state transition, gesture release, mount/unmount, route push. This tells the engineer whether to use implicit or explicit animation.
3. **The properties animated** — explicitly listed, with the start and end values either literal or token-referenced.
4. **Reduce-motion behaviour** — does the motion turn off, shorten, or persist? The spec must answer this; the engineer cannot infer it.
5. **Interruption behaviour** — what happens if the user gestures or navigates mid-animation. Most specs ignore this and produce bugs; a serious DS spec answers it.
6. **A reference recording** — a short screen capture (15s, 60fps) showing the motion on a real device, not a designer's prototype. The reference is the ground truth when the engineer's implementation in any framework needs to be calibrated.

A spec without those six fields is a wishlist; a spec with them is a contract. Across four frameworks, the contract format is the artefact that scales — the framework-specific code is downstream of it.

### Where the DS lead actually spends their time

Across multi-framework mobile DS work in 2026, the motion budget is roughly:

- 20% authoring the token catalogue and framework adapters (one-time investment, then maintenance)
- 30% Lottie/Rive integration and the per-platform calibration of those assets
- 30% gesture and interruption work — the part AI doesn't help with
- 10% accessibility / reduce-motion wiring
- 10% performance debugging — usually one or two components that miss the budget

The high-leverage investments are the token catalogue and a small library of choreography primitives (the named stagger / hero / transition shapes) wired to the four framework adapters. Everything else is downstream of those.



---

## References

- Apple, **Human Interface Guidelines — Motion**, 2024–2025 revision. https://developer.apple.com/design/human-interface-guidelines/motion
- Apple, **SwiftUI Animation documentation**, iOS 17 / 18 / 19. https://developer.apple.com/documentation/swiftui/animation
- Apple, **UIViewPropertyAnimator** reference. https://developer.apple.com/documentation/uikit/uiviewpropertyanimator
- Apple, **`matchedGeometryEffect` and `navigationTransition`**, WWDC 2020 / 2024 sessions.
- Google, **Material Design 3 — Motion**, 2024 expressive motion update. https://m3.material.io/styles/motion
- Google, **Jetpack Compose animation documentation**. https://developer.android.com/jetpack/compose/animation
- Google, **SharedTransitionLayout** — introduced stable in Compose 1.7.0, August 2024. https://developer.android.com/develop/ui/compose/animation/shared-elements
- Google, **MotionScheme and expressive motion tokens**, Material 3 release notes, late 2024 / early 2025.
- Flutter team, **Animation and motion widgets**, **AnimationController**, **Hero**, **SpringSimulation**. https://docs.flutter.dev/ui/animations
- Flutter team, **Impeller renderer** — default on iOS from Flutter 3.10 (May 2023), default on Android from Flutter 3.27 (December 2024). https://docs.flutter.dev/perf/impeller
- Software Mansion, **Reanimated 3** (released January 2023), **Reanimated 4** (released October 2025) docs. https://docs.swmansion.com/react-native-reanimated/
- Software Mansion, **react-native-gesture-handler** v2 docs. https://docs.swmansion.com/react-native-gesture-handler/
- Software Mansion, **Reanimated Shared Transitions** (experimental). https://docs.swmansion.com/react-native-reanimated/docs/shared-element-transitions/overview
- Wojciech Trzcinski, **react-native-shared-element**. https://github.com/IjzerenHein/react-native-shared-element
- Airbnb, **Lottie** docs, iOS / Android / React Native / Flutter runtimes. https://airbnb.io/lottie/
- Rive, **Rive runtime documentation**, iOS / Android / Flutter / React Native. https://rive.app/docs
- Apple, **`accessibilityReduceMotion`** environment value. https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion
- Apple, **`UIAccessibility.isReduceMotionEnabled`**. https://developer.apple.com/documentation/uikit/uiaccessibility/1615133-isreducemotionenabled
- Android, **AccessibilityManager.isAnimationsEnabled** (API 33+) and `Settings.Global.ANIMATOR_DURATION_SCALE`. https://developer.android.com/reference/android/view/accessibility/AccessibilityManager
- Flutter, **MediaQueryData.disableAnimations**, since Flutter 2.10. https://api.flutter.dev/flutter/widgets/MediaQueryData/disableAnimations.html
- React Native, **AccessibilityInfo.isReduceMotionEnabled**. https://reactnative.dev/docs/accessibilityinfo
- Figma, **Code Connect** and **MCP server** documentation, 2024–2026. https://www.figma.com/developers/api
- Practitioner write-ups: Chris Brown / Janum Trivedi on SwiftUI spring tuning; Jaime Cely / Stéphane Mathis on Reanimated gestures; Filip Hracek (Flutter) on AnimationController patterns; Doris Liu (Compose) on `Animatable` interruption semantics — search by name + topic for current write-ups (these authors update frequently).


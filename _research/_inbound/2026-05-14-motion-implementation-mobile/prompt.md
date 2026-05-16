You are researching motion implementation on mobile for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our practice ships mobile design systems across SwiftUI / UIKit (iOS), Jetpack Compose (Android), Flutter, and React Native. We need cross-framework depth on motion implementation — enough to translate a designer's motion spec into idiomatic, performant code in each framework, plus the cross-framework comparison. Bound on this research: moderate depth per framework (the consulting value is in the comparison and the cross-framework conventions, not a per-framework cookbook). The architectural treatment of motion as a system foundation is being researched separately; this prompt covers implementation only. Reduce-motion respect is covered in our existing accessibility work (16-mobile-accessibility-implementation); cover only the motion-specific spelling per framework, not the broader accessibility architecture.

This is not an introductory motion guide — assume the reader knows what easing is, what a spring is, what implicit vs. explicit animation means at a high level, and what a screen reader is. Explain mobile motion at the level a senior engineer or DS lead needs to ship motion that is consistent, performant, and brand-aligned across a multi-framework mobile component library.

Research scope — cover all of the following. Use these as the section spine of the output. For each section, address all four frameworks (SwiftUI / UIKit, Jetpack Compose, Flutter, React Native) and highlight the cross-framework comparison.

1. Animation primitives by framework

   - The core animation surface each framework exposes (SwiftUI's `.animation` and `withAnimation`, UIKit's `UIView.animate` and `UIViewPropertyAnimator`, Compose's `animate*AsState` and `updateTransition`, Flutter's implicit / explicit animation widgets, React Native's `Animated` and Reanimated 3).
   - The mental model in each: declarative vs. imperative, value-driven vs. state-driven, JS-thread vs. UI-thread.
   - Where each framework's defaults are good and where engineers must override them.

2. Spring and physics

   - Spring APIs by framework — SwiftUI `.spring()`, Compose `spring()`, Flutter `SpringSimulation`, React Native Reanimated's `withSpring`.
   - Cross-framework comparison of spring parameter conventions (response/damping vs. stiffness/damping vs. mass/stiffness/damping). Where parameter naming and defaults diverge.
   - The case for springs as the default in modern mobile motion and where the field has converged.

3. Choreography and orchestration

   - Patterns for sequencing entrance/exit, stagger, parallel animations in each framework.
   - Shared element transitions / hero transitions per framework (SwiftUI's `matchedGeometryEffect`, Compose's `SharedTransitionLayout` introduced in 2024, Flutter's `Hero` widget, React Native's `react-native-shared-element` / Reanimated's shared transitions).
   - Route / screen transitions per framework and the role of the navigation library in each.

4. Implicit vs. explicit animation patterns

   - When to reach for implicit animation (state changes, single properties) vs. explicit orchestration (timelines, gestures, interruption).
   - The interruption story per framework — what happens when an animation is interrupted by a new state change, gesture, or route transition.
   - The relationship between motion and gesture handling per framework.

5. Lottie and Rive integration

   - Native runtime support per framework — what each framework gives, what each requires.
   - The trade-offs between Lottie and Rive in 2026 (file size, interactivity, designer tooling, runtime cost).
   - When the right answer is hand-coded animation vs. exported asset, framework by framework.

6. Reduce-motion respect per framework

   - The per-framework primitive for detecting the system setting (covered in detail in 16-mobile-accessibility-implementation; here just summarise the spelling).
   - The pattern for gating animations on the setting in each framework.
   - Where the framework defaults already respect the setting and where engineers must wire it up.

7. Performance characteristics

   - The performance profile per framework — frame rate, dropped-frame causes, profiling tools.
   - The JS-thread / UI-thread distinction in React Native (where Reanimated changes the story).
   - The compositor / rasteriser story per framework and what makes motion cheap vs. expensive.
   - The 60Hz vs. 120Hz target story per platform.

8. The spec-to-code bridge per framework

   - What an engineer actually consumes from a designer's motion spec in each framework.
   - The role of Lottie and Rive as the canonical handoff artefact, where it works, where it doesn't.
   - The role of AI code generation (Claude Code, Cursor, Figma Make) in producing framework-specific animation code from designer intent.
   - Where the spec-to-code translation is still manual and where it has been automated in 2026.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Use cross-framework comparison tables where they help the reader. Where there's clear consensus across the four frameworks, state it; where they diverge meaningfully, give the comparison. Where decisions are context-dependent, give a decision framework. Where claims depend on framework / version state — feature names, version numbers, recent additions like Compose's `SharedTransitionLayout` — date them and note the verification path. Include a references section linking to primary sources (Apple HIG and SwiftUI/UIKit animation docs, Material motion docs, Android Compose animation docs, Flutter animation docs, React Native and Reanimated docs, Lottie and Rive docs, practitioner write-ups).

Depth: Expert audience. Do not explain what an animation API is or what a spring does — explain the cross-framework comparison, what's idiomatic per framework in 2026, where the platforms have converged or diverged, and what a multi-framework design system should standardise on.

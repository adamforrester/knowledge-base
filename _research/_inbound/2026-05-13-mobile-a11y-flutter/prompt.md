You are researching mobile accessibility implementation in Flutter for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our teams ship native and cross-platform mobile work and must annotate accessibility requirements in Figma in a way that developers can implement faithfully. We already have an architectural position on accessibility as a design system concern (pair tokens, ARIA encapsulation, four-layer model, conformance reporting). What we lack is the platform-specific implementation depth that closes the gap between "the system encodes accessibility" and "this screen ships to WCAG 2.2 AA on a real device with real assistive tech." This research fills that gap for Flutter. We already have a Claude-side research run on Flutter screen-reader accessibility specifically; this prompt deliberately broadens the scope to the full mobile accessibility surface (focus, text scaling, system inversions, motion preferences, gesture alternatives, the annotation contract) and will be paired with that earlier run.

This is not an introductory accessibility guide — assume the reader knows WCAG 2.2, the difference between role/name/state, what a screen reader is, and what a design system is. Explain Flutter's accessibility primitives at the level a senior engineer or design systems lead would need to make implementation and annotation decisions.

Research scope — cover all of the following. Use these as the section spine of the output:

1. The accessibility primitives Flutter exposes

   - The core API surface for semantics (name, role, value, state, grouping, decorative exclusion) and how it maps to TalkBack and VoiceOver via the engine.
   - What's automatic vs. opt-in for built-in Material/Cupertino widgets.
   - The mental model a developer needs (render-tree semantics, MergeSemantics/ExcludeSemantics, SemanticsConfiguration, the role of GestureDetector).
   - Common pitfalls and anti-patterns specific to Flutter.

2. Focus and traversal

   - Screen-reader swipe order: how it's determined, how it's overridden (sortKey, OrdinalSortKey).
   - Hardware keyboard support including iOS Full Keyboard Access state and known regressions.
   - Switch Control / Switch Access behaviour.
   - Modal trapping in DialogRoute, focus return after Navigator.pop on iOS, autofocus on route change.
   - FocusNode / FocusScope / FocusTraversalPolicy primitives.

3. Text scaling and reflow

   - How Flutter respects system text-size settings via MediaQuery.textScaler.
   - Behaviour at 200%+ scaling: truncation, reflow, icon-with-text pairs, fixed-height containers.
   - What breaks by default and what Flutter gives you to fix it.

4. System contrast, color, and motion preferences

   - Detecting and respecting: iOS Smart Invert / Increase Contrast / Differentiate Without Color / Reduce Transparency, Android high-contrast text and forced colors, dark mode.
   - Reduce Motion equivalents and how they reach Flutter.
   - How to exclude images/icons from Smart Invert correctly.
   - Where Flutter supports these natively and where the team has to wire it up.

5. Tap targets, gestures, and input alternatives

   - Minimum target enforcement (44pt iOS / 48dp Android) and meetsGuideline matchers.
   - Providing alternatives to drag, long-press, multi-finger, and motion-actuated gestures (WCAG 2.5.7, 2.5.4).
   - Custom-gesture accessibility actions for screen-reader users (onIncrease/onDecrease, custom actions).

6. Live regions, announcements, and dynamic content

   - liveRegion cross-platform behaviour and reliability.
   - SemanticsService.sendAnnouncement (and the deprecated announce), when not to use them.
   - Status messages, loading states, error announcements.

7. Testing, tooling, and conformance evidence

   - Widget test APIs: meetsGuideline matchers, SemanticsController, simulatedAccessibilityTraversal.
   - In-app debug overlays (accessibility_tools package, showSemanticsDebugger), Accessibility Scanner, Xcode Accessibility Inspector.
   - Manual testing workflow on real Android + iOS devices.
   - What evidence can be generated for an ACR/VPAT and what cannot.

8. The Figma annotation contract

   - Given everything above, what must a designer specify in Figma so a Flutter developer can implement it without guessing? Address at minimum: accessible name, role, state, traversal order, dynamic-type behaviour, behaviour under Smart Invert / forced colors, gesture alternative, live-region intent.
   - Where Flutter's defaults make annotation unnecessary, say so. Where the defaults are wrong or absent, the annotation is load-bearing — call this out.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where Flutter has clear consensus or one obvious choice, state it; where decisions are context-dependent, give a decision framework rather than declaring a winner. Flag framework or tooling gaps that practitioners work around. Where claims depend on platform/framework version state — feature names, version numbers, deprecation cycles, issue numbers — date them and note the verification path (issue tracker, release notes, docs URL). Include a references section linking to primary sources (Flutter docs, Material/Cupertino guidelines, Apple HIG, Android accessibility docs, WCAG, W3C WCAG2Mobile, Flutter GitHub issues, practitioner write-ups, open-source reference apps like Wonderous).

Depth: Expert audience. Do not explain what a screen reader does or what WCAG is — explain how Flutter's primitives expose the right semantics, where they fall short, and what a designer must specify so an engineer can close the gap.

You are researching mobile accessibility implementation in Jetpack Compose for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our teams ship native and cross-platform mobile work and must annotate accessibility requirements in Figma in a way that developers can implement faithfully. We already have an architectural position on accessibility as a design system concern (pair tokens, ARIA encapsulation, four-layer model, conformance reporting). What we lack is the platform-specific implementation depth that closes the gap between "the system encodes accessibility" and "this screen ships to WCAG 2.2 AA on a real device with real assistive tech." This research fills that gap for Jetpack Compose. Cover Compose's `Modifier.semantics { }` model, mergeDescendants and clearAndSetSemantics behaviour, View-system interop where applicable, and Compose's relationship to AccessibilityNodeInfo. Cover both Material 3 components and custom-built ones.

This is not an introductory accessibility guide — assume the reader knows WCAG 2.2, the difference between role/name/state, what a screen reader is, and what a design system is. Explain Compose's accessibility primitives at the level a senior engineer or design systems lead would need to make implementation and annotation decisions.

Research scope — cover all of the following. Use these as the section spine of the output:

1. The accessibility primitives Compose exposes

   - The core API surface: Modifier.semantics, SemanticsProperties (contentDescription, role, stateDescription, liveRegion, etc.), SemanticsActions, mergeDescendants, clearAndSetSemantics.
   - What's automatic vs. opt-in for Material 3 / Material You components.
   - The mental model: how Compose builds its SemanticsNode tree, how it maps to AccessibilityNodeInfo for TalkBack and to the platform's accessibility services.
   - Common pitfalls and anti-patterns specific to Compose (e.g., missing roles on Box-with-clickable, contentDescription on decorative images, modifier order).

2. Focus and traversal

   - TalkBack swipe order: how it's determined, how it's overridden (traversalIndex, isTraversalGroup).
   - Hardware keyboard support and Compose's FocusRequester / FocusManager / FocusModifier APIs.
   - Switch Access behaviour.
   - Modal trapping in Dialog/AlertDialog/BottomSheet, focus return after dismiss, initial focus on screen entry.
   - Compose Navigation interactions with focus and accessibility.

3. Text scaling and reflow

   - How Compose respects Android fontScale and the user's display-size setting.
   - Behaviour at 200%+ scaling: truncation, reflow, icon-with-text pairs, fixed-height containers.
   - sp vs. dp conventions and what goes wrong when teams mix them.
   - What breaks by default and what Compose gives you to fix it.

4. System contrast, color, and motion preferences

   - Detecting and respecting Android's high-contrast text setting, forced colors (Android 14+ where applicable), color inversion, dark mode.
   - Reduce Motion equivalents on Android and how they reach Compose (animations should defer to system settings).
   - Where Compose / Material 3 supports these natively and where the team has to wire it up.

5. Tap targets, gestures, and input alternatives

   - Minimum touch target (48dp) and minimumInteractiveComponentSize, how Material 3 enforces it.
   - Providing alternatives to drag, long-press, multi-finger, and motion-actuated gestures (WCAG 2.5.7, 2.5.4).
   - Custom accessibility actions (CustomAccessibilityAction, SemanticsActions for scroll, expand, dismiss).

6. Live regions, announcements, and dynamic content

   - SemanticsProperties.liveRegion (Polite vs. Assertive) behaviour with TalkBack.
   - View.announceForAccessibility and its discouraged status, modern Compose equivalents.
   - Status messages, loading states, error announcements.

7. Testing, tooling, and conformance evidence

   - Compose test APIs: SemanticsMatcher, onNodeWithContentDescription, assertions on semantics tree.
   - Espresso/UIAutomator integration where relevant.
   - Accessibility Scanner, Android Studio's Layout Inspector + accessibility checks, Lint accessibility rules.
   - Manual testing workflow on real devices with TalkBack and Switch Access.
   - What evidence can be generated for an ACR/VPAT and what cannot.

8. The Figma annotation contract

   - Given everything above, what must a designer specify in Figma so a Compose developer can implement it without guessing? Address at minimum: accessible name, role, state, traversal order, dynamic-type/fontScale behaviour, behaviour under inversion / forced colors, gesture alternative, live-region intent.
   - Where Compose's defaults make annotation unnecessary, say so. Where the defaults are wrong or absent, the annotation is load-bearing — call this out.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where Compose has clear consensus or one obvious choice, state it; where decisions are context-dependent, give a decision framework rather than declaring a winner. Flag framework or tooling gaps that practitioners work around. Where claims depend on platform/framework version state — feature names, version numbers, deprecation cycles, issue numbers — date them and note the verification path (issue tracker, release notes, docs URL). Include a references section linking to primary sources (Android developer docs, Compose docs, Material 3 docs, Android accessibility guidance, WCAG, W3C WCAG2Mobile, Compose issue tracker, practitioner write-ups, open-source reference apps).

Depth: Expert audience. Do not explain what a screen reader does or what WCAG is — explain how Compose's primitives expose the right semantics, where they fall short, and what a designer must specify so an engineer can close the gap.

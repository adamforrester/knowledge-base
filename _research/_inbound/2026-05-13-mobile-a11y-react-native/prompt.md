You are researching mobile accessibility implementation in React Native for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our teams ship native and cross-platform mobile work and must annotate accessibility requirements in Figma in a way that developers can implement faithfully. We already have an architectural position on accessibility as a design system concern (pair tokens, ARIA encapsulation, four-layer model, conformance reporting). What we lack is the platform-specific implementation depth that closes the gap between "the system encodes accessibility" and "this screen ships to WCAG 2.2 AA on a real device with real assistive tech." This research fills that gap for React Native. Cover the `accessibilityLabel` / `accessibilityHint` / `accessibilityRole` / `accessibilityState` / `accessibilityValue` prop surface, the Android–iOS prop and behaviour divergence, the New Architecture's effect on accessibility (Fabric / TurboModules), and Expo's surface where relevant.

This is not an introductory accessibility guide — assume the reader knows WCAG 2.2, the difference between role/name/state, what a screen reader is, and what a design system is. Explain React Native's accessibility primitives at the level a senior engineer or design systems lead would need to make implementation and annotation decisions.

Research scope — cover all of the following. Use these as the section spine of the output:

1. The accessibility primitives React Native exposes

   - The core prop surface: accessible, accessibilityLabel, accessibilityHint, accessibilityRole, accessibilityState, accessibilityValue, accessibilityActions, accessibilityElementsHidden (iOS), importantForAccessibility (Android), accessibilityViewIsModal (iOS), accessibilityLiveRegion (Android).
   - The mental model: how RN bridges to native accessibility trees on each platform, how Pressable/Touchable* compose accessibility, how the New Architecture affects this.
   - What's automatic vs. opt-in for built-in components (Pressable, Text, TextInput, Switch, FlatList).
   - Common pitfalls and anti-patterns specific to RN (nested Touchables, View with onPress missing role, accessible=true grouping behaviour, Text not being focusable on Android by default).

2. Focus and traversal

   - Screen-reader swipe order: how it's determined, how it's overridden (importantForAccessibility on Android, accessibilityElements on iOS via setAccessibilityElements not directly exposed).
   - Hardware keyboard support on iOS (Full Keyboard Access), Android, and where RN falls short — focusable prop, hasTVPreferredFocus, nextFocus* props.
   - Switch Control / Switch Access behaviour.
   - Modal trapping (Modal component, accessibilityViewIsModal on iOS), focus return after close.
   - AccessibilityInfo.setAccessibilityFocus and ref-based focus management.
   - The TV / focus-system pattern (react-native-tvos lineage) and how RN's keyboard support has evolved from it.

3. Text scaling and reflow

   - allowFontScaling, maxFontSizeMultiplier, and the conventions teams set globally.
   - How RN maps to iOS Dynamic Type and Android fontScale; the divergence.
   - Behaviour at 200%+ scaling: truncation, reflow, icon-with-text pairs, fixed-height containers.
   - What breaks by default and what RN gives you to fix it.

4. System contrast, color, and motion preferences

   - AccessibilityInfo APIs: isReduceMotionEnabled, isReduceTransparencyEnabled, isInvertColorsEnabled (iOS), isHighTextContrastEnabled (Android), isBoldTextEnabled, isGrayscaleEnabled.
   - useColorScheme and dark mode interplay.
   - Smart Invert and how to exclude images (no first-class API — workarounds via native modules or platform-specific code).
   - Where RN supports these natively and where the team has to wire it up.

5. Tap targets, gestures, and input alternatives

   - Minimum target enforcement (44pt iOS / 48dp Android), hitSlop, Pressable's pressRetentionOffset.
   - Providing alternatives to drag, long-press, multi-finger, and motion-actuated gestures (WCAG 2.5.7, 2.5.4).
   - accessibilityActions and the onAccessibilityAction handler for custom screen-reader gestures.

6. Live regions, announcements, and dynamic content

   - accessibilityLiveRegion (Android) and its iOS gap.
   - AccessibilityInfo.announceForAccessibility (Android-good, iOS-quirky) vs. .announceForAccessibilityWithOptions (iOS).
   - Status messages, loading states, error announcements; what's reliable cross-platform vs. what needs platform branching.

7. Testing, tooling, and conformance evidence

   - Jest + @testing-library/react-native accessibility queries (getByRole, getByA11yState, getByA11yValue, getByA11yLabel).
   - Detox / Appium / Maestro for end-to-end accessibility traversal.
   - eslint-plugin-react-native-a11y and other lint coverage.
   - Manual testing workflow on real Android + iOS devices.
   - What evidence can be generated for an ACR/VPAT and what cannot, including the "we shipped one codebase but two ACRs" question.

8. The Figma annotation contract

   - Given everything above, what must a designer specify in Figma so an RN developer can implement it without guessing? Address at minimum: accessible name, role, state, traversal order, dynamic-type/fontScale behaviour, behaviour under inversion / forced colors / increase contrast, Reduce Motion behaviour, gesture alternative, live-region intent.
   - Where RN's defaults make annotation unnecessary, say so. Where the defaults differ between iOS and Android, call out which annotation covers which platform.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where RN has clear consensus or one obvious choice, state it; where decisions are context-dependent, give a decision framework rather than declaring a winner. Flag framework or tooling gaps that practitioners work around. Where claims depend on RN version / New Architecture / Expo SDK state — feature names, version numbers, deprecation cycles, issue numbers — date them and note the verification path (issue tracker, release notes, docs URL). Include a references section linking to primary sources (React Native docs, Expo docs, Apple HIG, Android accessibility docs, WCAG, W3C WCAG2Mobile, RN GitHub issues, practitioner write-ups, open-source reference apps).

Depth: Expert audience. Do not explain what a screen reader does or what WCAG is — explain how React Native's primitives expose the right semantics, where they fall short, and what a designer must specify so an engineer can close the gap.

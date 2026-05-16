You are researching mobile accessibility implementation in SwiftUI and UIKit for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our teams ship native and cross-platform mobile work and must annotate accessibility requirements in Figma in a way that developers can implement faithfully. We already have an architectural position on accessibility as a design system concern (pair tokens, ARIA encapsulation, four-layer model, conformance reporting). What we lack is the platform-specific implementation depth that closes the gap between "the system encodes accessibility" and "this screen ships to WCAG 2.2 AA on a real device with real assistive tech." This research fills that gap for iOS (and iPad/Catalyst where relevant). Cover both SwiftUI and UIKit — most production iOS codebases are still mixed, and design systems often need to support both. Treat hardware keyboard / Full Keyboard Access on iPad as in-scope.

This is not an introductory accessibility guide — assume the reader knows WCAG 2.2, the difference between role/name/state, what a screen reader is, and what a design system is. Explain SwiftUI's and UIKit's accessibility primitives at the level a senior engineer or design systems lead would need to make implementation and annotation decisions.

Research scope — cover all of the following. Use these as the section spine of the output:

1. The accessibility primitives SwiftUI and UIKit expose

   - SwiftUI: the `.accessibility*` modifier surface (label, value, hint, traits, addTraits/removeTraits, accessibilityElement(children:), accessibilityHidden, accessibilityRepresentation, accessibilityChildren).
   - UIKit: the UIAccessibility informal protocol (accessibilityLabel, accessibilityValue, accessibilityHint, accessibilityTraits, isAccessibilityElement, accessibilityElements, accessibilityCustomActions).
   - The mental model: how UIKit's element flattening works, how SwiftUI maps to the accessibility tree, where the two approaches diverge.
   - What's automatic vs. opt-in for built-in controls (SwiftUI Button, Toggle, Picker, TextField; UIKit UIButton, UISwitch, UISegmentedControl, etc.).
   - Common pitfalls and anti-patterns (custom controls drawn with shapes, gesture-only views, decorative SF Symbols).

2. Focus and traversal

   - VoiceOver swipe order: how it's determined, how it's overridden (accessibilitySortPriority, accessibilityElements ordering, sortPriority in SwiftUI).
   - Hardware keyboard / Full Keyboard Access on iPad and iOS — focusable APIs, focusEffect, FocusState in SwiftUI; canBecomeFocused / preferredFocusEnvironments in UIKit.
   - Switch Control behaviour.
   - Modal trapping in sheets, alerts, fullScreenCover; focus return after dismiss; initial focus on screen appear (UIAccessibility.post(notification:argument:)).
   - SwiftUI NavigationStack / TabView interactions with accessibility focus.

2. Focus and traversal — continued

   - Differences between accessibility focus (VoiceOver) and keyboard focus (Full Keyboard Access) and where SwiftUI conflates them.

3. Text scaling and reflow

   - Dynamic Type: how SwiftUI's Font.body / textStyle hooks into it; how UIKit's UIFontMetrics + UIFont.preferredFont(forTextStyle:) does.
   - Behaviour at AX accessibility sizes (AX1–AX5): truncation, reflow, icon-with-text pairs, fixed-height containers.
   - When to allow scaling vs. cap it; conventions around adjustsFontForContentSizeCategory.
   - What breaks by default and what the frameworks give you to fix it.

4. System contrast, color, and motion preferences

   - Smart Invert, Classic Invert, Increase Contrast, Differentiate Without Color, Reduce Transparency — detection APIs (UIAccessibility.is*Enabled, accessibilityInvertColors environment, @Environment in SwiftUI).
   - Dark mode interplay and trait collections.
   - Reduce Motion and Prefer Cross-Fade Transitions detection and how to wire animations to defer to them.
   - How to exclude images from Smart Invert (accessibilityIgnoresInvertColors).
   - Where SwiftUI / UIKit handle these natively vs. require explicit code.

5. Tap targets, gestures, and input alternatives

   - 44×44 pt minimum target enforcement on iOS, and how SwiftUI's frame minimums and UIKit's hit-test expansion (hitTest override, pointInside) interact with this.
   - Providing alternatives to drag, long-press, multi-finger, and motion-actuated gestures (WCAG 2.5.7, 2.5.4).
   - accessibilityCustomActions (UIKit) and .accessibilityAction (SwiftUI) for screen-reader users to invoke custom gestures.

6. Live regions, announcements, and dynamic content

   - SwiftUI: AccessibilityNotification.Announcement, accessibilityRespondsToUserInteraction.
   - UIKit: UIAccessibility.post(notification: .announcement, argument:), .layoutChanged, .screenChanged, .pageScrolled.
   - When each notification type is appropriate; ordering and queueing behaviour.
   - Status messages, loading states, error announcements.

7. Testing, tooling, and conformance evidence

   - XCUITest accessibility APIs, accessibility identifiers vs. labels.
   - Xcode Accessibility Inspector (Audit + Inspect modes), accessibility audits in unit tests (XCUIApplication.performAccessibilityAudit, Xcode 15+).
   - SwiftUI accessibility previews (.accessibilityRepresentation in previews, AccessibilityInspector).
   - Manual testing workflow on real device with VoiceOver, Voice Control, Switch Control, Full Keyboard Access.
   - What evidence can be generated for an ACR/VPAT and what cannot.

8. The Figma annotation contract

   - Given everything above, what must a designer specify in Figma so an iOS developer (SwiftUI or UIKit) can implement it without guessing? Address at minimum: accessible name, role/traits, state, traversal order, Dynamic Type behaviour, behaviour under Smart Invert / Increase Contrast, Reduce Motion behaviour, gesture alternative, accessibility-announcement intent.
   - Where the frameworks' defaults make annotation unnecessary, say so. Where defaults are wrong or absent, the annotation is load-bearing — call this out.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where there's clear consensus or one obvious choice, state it; where decisions are context-dependent, give a decision framework rather than declaring a winner. Flag framework or tooling gaps that practitioners work around. Where claims depend on platform/framework version state — feature names, iOS/Xcode version numbers, deprecation cycles, FB or rdar references — date them and note the verification path (release notes, docs URL, WWDC session). Include a references section linking to primary sources (Apple HIG, Apple Developer accessibility docs, SwiftUI/UIKit reference, WWDC sessions, WCAG, W3C WCAG2Mobile, practitioner write-ups, open-source reference apps).

Depth: Expert audience. Do not explain what a screen reader does or what WCAG is — explain how SwiftUI's and UIKit's primitives expose the right semantics, where they fall short, and what a designer must specify so an engineer can close the gap.

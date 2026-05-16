# 16 — Mobile Accessibility Implementation

> Our position on accessibility as a design system concern is in 14-accessibility — pair tokens, ARIA encapsulation, the four-layer model, conformance reporting under EAA and Section 508. That file is what the system must encode. This file is what the framework actually does with it. The gap between the architectural intent and the device behaviour is where most apps quietly lose WCAG conformance, and it is platform-specific in ways that 14 cannot speak to. Mobile is the case where that gap is largest. We cover Flutter, Jetpack Compose, SwiftUI and UIKit (treated together because production iOS codebases mix them), and React Native — the four frameworks our teams actually ship in.

---

## The four frameworks at a glance

Each framework owns the accessibility tree differently, and the difference is the most useful thing to internalise before we get into the per-concern detail.

**Flutter** generates a render-layer semantics tree that is engine-owned and platform-independent. Each `RenderObject` describes a `SemanticsConfiguration`; during `flushSemantics` the framework walks the tree and emits a `SemanticsNode` tree which is then shipped across the engine boundary to TalkBack and VoiceOver. Layout-only widgets (`Container`, `Padding`, `Row`) emit no semantic node and merge into their nearest ancestor or descendant. The mental model that catches people out: `GestureDetector` is layout-only. Wrapping arbitrary children in a `GestureDetector` produces something visible to a sighted user but invisible to the accessibility tree unless wrapped in `Semantics(button: true, label: ...)` or replaced with a real `*Button` widget.

**Jetpack Compose** builds two parallel trees during composition and layout — the UI tree describing what to draw, and a Semantics Tree describing what it means. The Semantics Tree exists for accessibility services, autofill, and tests. The translation layer (`AndroidComposeView`) maps `SemanticsNode` objects to `AccessibilityNodeInfo` for TalkBack, using `Role` properties to populate the `className` field — `Role.Button` becomes `android.widget.Button` to the OS even though no actual `Button` view exists. The mental model: if a custom composable is built out of `Box` and `Canvas` without a defined role, it is either generic or invisible to TalkBack.

**SwiftUI and UIKit** are different paradigms running on the same accessibility API. UIKit treats accessibility as an informal protocol on `NSObject`; every `UIView` has accessibility properties that must be set imperatively and kept in sync with the visual state. SwiftUI integrates accessibility into its declarative engine — modifiers participate in the `AttributeGraph` and re-evaluate alongside the view they describe, so the accessibility tree updates as a side effect of state changes. Most production iOS codebases mix the two: SwiftUI for new screens, UIKit for `UICollectionView` and other surfaces where its imperative control over the accessibility hierarchy is still more mature than SwiftUI's reactive equivalent. Our practice treats them as one platform with two implementation languages, not two platforms.

**React Native** is a thin abstraction over both native accessibility trees. The prop surface — `accessibilityLabel`, `accessibilityHint`, `accessibilityRole`, `accessibilityState`, `accessibilityValue` — is unified across iOS and Android in the JavaScript layer, but the behaviour underneath diverges materially. `accessibilityLiveRegion` only exists on Android. `accessibilityViewIsModal` only on iOS. `accessibilityElementsHidden` is iOS; `importantForAccessibility` is Android. The mental model: the JS prop is a single surface; the implementation behind it is two different stories, and an engineer who treats them as one will fail in different ways on each platform. The New Architecture (Fabric) doesn't change the prop surface but does collapse the bridge latency that previously caused stale accessibility labels during rapid state updates.

| Framework | Accessibility tree | Customisation primitive | Where the cost of mistakes lives |
|---|---|---|---|
| Flutter | Engine-owned, platform-independent, single source | `Semantics`, `MergeSemantics`, `ExcludeSemantics` | `CustomPainter`, `GestureDetector`, `PlatformView` |
| Compose | Parallel to UI tree, reactive, maps to Android | `Modifier.semantics { }`, `mergeDescendants`, `clearAndSetSemantics` | Custom `Box` + `clickable` without a `Role` |
| SwiftUI | Reactive, part of `AttributeGraph` | `.accessibility*` modifiers, `accessibilityRepresentation` | Custom-drawn views, focus-state desync |
| UIKit | Imperative protocol on `NSObject` | `accessibility*` properties, `UIAccessibilityContainer` | Manual state sync, custom `hitTest` |
| React Native | Two trees, unified prop surface | Cross-platform props, `AccessibilityInfo` API | iOS-Android divergence at the same prop |

The single most important property of this table is that no framework lets us avoid the work — they shift *where* the work lives. Compose and SwiftUI make defaults better; Flutter centralises the model; UIKit gives the most control with the most discipline required; React Native lets one team write one codebase but produces two different accessibility experiences underneath.

---

## Semantic primitives

Every framework exposes the same four-pillar contract: name, role, state, value. (See 14-accessibility for the architectural treatment of these as a system contract.) The implementation depth is where the contract becomes load-bearing.

**Name** is the accessible string read by the screen reader. Flutter's `Semantics(label: ...)`, Compose's `contentDescription`, SwiftUI's `.accessibilityLabel(_:)`, UIKit's `accessibilityLabel`, RN's `accessibilityLabel`. The rule that holds across all four: do not include the role word ("button," "image") in the label, because the platform appends it automatically and "Cart button button" is what users actually hear. Equally consistent: empty labels are worse than missing labels, because the framework will fall back to something usable when nothing is set but will respect an empty string as intentional.

**Role** is the only primitive where the frameworks diverge meaningfully in spelling.

- **Flutter** uses flags on `Semantics` (`button: true`, `header: true`, `checked: true`) plus the newer `SemanticsRole` enum introduced in 3.32 (May 2025) covering `tab`, `tabBar`, `dialog`, `alertDialog`, `table`, `list`, `listItem`, `form`, `tooltip`, `progressBar`, `radioGroup`, `menu`, `comboBox`, `status`, `alert`. As of Flutter 3.32 the role API maps to ARIA roles on web fully; iOS and Android translation is being wired up incrementally. Combine roles with the older boolean flags for full mobile coverage.
- **Compose** uses `Role` values within `Modifier.semantics { role = Role.Button }`. The translation populates the underlying `AccessibilityNodeInfo` className, so TalkBack says "Button" or "Check box" as expected. Material 3 components set the role automatically; custom interactive composables must set it explicitly.
- **SwiftUI and UIKit** use traits, not roles. `UIAccessibilityTraits` is a bitmask — an element can be `.button` and `.selected` and `.adjustable` at once. SwiftUI's `.accessibilityAddTraits(.isButton)` and `.accessibilityRemoveTraits(...)` modify the same bitmask. The `.isToggle` trait (iOS 17+) is the modern way to express a custom toggle's role.
- **React Native** uses string-valued `accessibilityRole` — `button`, `link`, `header`, `image`, `search`, `radio`, etc. The string is translated to the platform's native traits or className at the bridge layer.

**State** covers the dynamic properties: selected, checked, disabled, expanded, busy, toggled. Compose splits this further into `stateDescription` (a developer-controlled localised string read *before* the description, e.g. "Connecting") and the structured `selected`/`enabled` properties. Flutter uses `Semantics(toggled: ..., checked: ..., enabled: ...)`. SwiftUI and UIKit fold state into traits and `accessibilityValue`. RN exposes a single `accessibilityState` object covering `disabled`, `selected`, `checked`, `busy`, `expanded`.

The decision framework for designers: if the state is meaningfully named in the design (selected/unselected, expanded/collapsed), it needs an annotation. If it is purely visual (hover, pressed transient), the framework usually handles it.

**Value** is the current magnitude of a control — slider percentage, progress count, page-of-N for carousels. Flutter, Compose, SwiftUI, UIKit, and RN all support a `value` (or `accessibilityValue`) string or object. The interesting cross-framework consensus is on carousels: a horizontal `PageView` (Flutter), `HorizontalPager` (Compose), `TabView` (SwiftUI), or `FlatList` (RN) all default to a screen-reader experience where horizontal swipe is consumed by VoiceOver/TalkBack and the user cannot flip pages. The fix is the same in every framework: expose `onIncrease`/`onDecrease` actions (Flutter), `accessibilityActions` (RN), `.accessibilityAdjustableAction` (SwiftUI), `SemanticsActions.PageUp`/`PageDown` (Compose), and announce the value as "Page 2 of 5". This is the single highest-yield carousel annotation our practice should require by default.

### Merging and clearing

Every framework has the same problem and the same set of levers: control granularity. A card with title, subtitle, price, and a favourite button should be one swipe-stop for the screen reader (announce the whole card, then a custom action for the button), not four (title, subtitle, price, button) — but it depends on whether the button is the primary affordance or a sibling. The lever shapes differ:

- **Flutter** uses `MergeSemantics` and `ExcludeSemantics`. `MergeSemantics(child: ...)` collapses descendants into one focus stop; `ExcludeSemantics` removes a subtree from the accessibility tree entirely. The interactive primitives (`clickable` equivalents) typically merge automatically.
- **Compose** uses `Modifier.semantics(mergeDescendants = true)` for explicit merging and `Modifier.clearAndSetSemantics { }` for the more aggressive "wipe descendants and replace with my description" pattern. `clickable` and `toggleable` set `mergeDescendants = true` by default, which is why a Material 3 `Button` with an `Icon` and a `Text` is one focus stop.
- **SwiftUI** uses `.accessibilityElement(children: .ignore | .combine | .contain)`. `.combine` concatenates child labels into one element; `.contain` creates a container the user can "enter" to interact with children individually; `.ignore` hides the children.
- **UIKit** uses the `isAccessibilityElement` flag and the `UIAccessibilityContainer` protocol. `isAccessibilityElement = true` on a parent hides its subviews from the accessibility tree; `false` lets them through; full container behaviour requires implementing the protocol and managing an `accessibilityElements` array.
- **React Native** uses `accessible={true}` on a parent to collapse children into one focus stop — with the well-documented iOS pitfall that nested touchables inside an `accessible={true}` parent become unreachable to VoiceOver.

The cross-framework rule we should annotate against: **compound rows merge, custom-drawn controls clear and replace, decorative graphics exclude.** Designers don't need to know the framework spelling. They need to mark a card "this is one announcement, plus an Action for the favourite button," and engineers implement the spelling correctly.

### Custom-painted graphics are the universal hole

Charts, signature pads, sparklines, custom progress indicators, anything that goes through `CustomPainter` (Flutter), `Canvas` (Compose), `Drawing` modifiers (SwiftUI), or `drawRect` (UIKit) is invisible to the accessibility tree by default. Every framework has a way to fix it — `CustomPainter.semanticsBuilder`, `Modifier.semantics { contentDescription = ... }` wrapping a `Canvas`, `accessibilityChildren` (SwiftUI's synthetic-children API, the most expressive of the four), `UIAccessibilityElement` synthetic children in UIKit — but the fix is opt-in. Our practice's default position: if it is rendered as pixels and not as a real component, the design system requires an explicit accessible representation. For data viz the practical pattern is a `Semantics(label: 'Chart: revenue rose from $100k to $250k over Q1')` wrapper plus a tabular `DataTable` alternative reachable from the chart.

---

## Focus and traversal

Three distinct concerns that frameworks tend to conflate at their peril: **screen-reader traversal order** (the sequence VoiceOver/TalkBack walks when the user swipes right), **hardware keyboard focus** (where the system focus moves when the user presses Tab), and **focus management around route and modal transitions** (what happens when a screen pushes, a dialog opens, a dialog closes).

### Screen-reader traversal order

Default is reading order — top-to-bottom, left-to-right, RTL-aware. (See 13-internationalization-and-rtl for the directionality layer.) Every framework needs an escape hatch for cases where the visual layout diverges from logical reading order — responsive reflows, circular layouts, content rearranged via `Stack`/`ZStack`.

- **Flutter** uses `Semantics(sortKey: OrdinalSortKey(n))`. This is screen-reader-only; keyboard focus order is controlled separately by `FocusTraversalPolicy`.
- **Compose** uses `Modifier.semantics { isTraversalGroup = true; traversalIndex = n }`. `isTraversalGroup` defines a container that's visited as a unit; `traversalIndex` sorts within it. Material Surfaces and scrollable containers default to `isTraversalGroup = true`. Renamed from earlier spellings in Compose UI 1.5.
- **SwiftUI** uses `.accessibilitySortPriority(_:)`. Local to the parent; higher priority comes first.
- **UIKit** sets an `accessibilityElements` array on a container. This is the most powerful escape hatch — and the easiest to break, because the array is manually maintained and silently overrides everything else.
- **React Native** has the weakest story. The default is render-tree order; overrides require either `importantForAccessibility` on Android, the experimental `experimental_accessibilityOrder` (RN 0.77.x, 2024) on iOS, or restructuring the JSX. Our practice: in RN, prefer restructuring the tree over relying on traversal-override props, because the experimental APIs ship and unship and aren't reliable to bake into a design system.

The clock-face example is the canonical test case: a circular layout where numbers 1–12 are placed visually around a circle. Default traversal will walk them top-to-bottom and produce nonsense; an explicit traversal index per number produces clockwise (or whatever) order. Designers should be able to mark traversal-order overrides as a numbered path on the Figma frame.

### Hardware keyboard and Full Keyboard Access

This is the single area where mobile accessibility frameworks differ most by maturity, and the iOS Full Keyboard Access story is the consequential one.

- **Flutter**'s focus system (`FocusManager`, `FocusScopeNode`, `FocusNode`, `FocusTraversalGroup`, `FocusTraversalPolicy`) is rich, and Android Switch Access / external keyboards work via standard traversal. iOS Full Keyboard Access support — the long-standing gap that for years blocked WCAG 2.1.1 conformance on iOS Flutter apps — was finally landed in the engine in early 2025 (issue #76497 closed via engine PR #56842 and framework #159811). Regressions continue to surface; our practice: confirm the target Flutter version includes the FKA fixes before claiming iOS keyboard conformance.
- **Compose**'s `FocusRequester` / `FocusManager` / `Modifier.focusable()` model is straightforward, and hardware keyboard support on Android is mature. The Compose-on-iOS story (via Compose Multiplatform) is newer and we should not assume parity.
- **SwiftUI** introduced `@FocusState` for keyboard focus and `@AccessibilityFocusState` for VoiceOver focus. Both work; the gap is that they are two separate focus systems and SwiftUI itself sometimes conflates them. `@FocusState` is the keyboard's — VoiceOver users moving the screen reader cursor do not move keyboard focus, and vice versa. Annotating a focus order in Figma without specifying which system we mean is a recipe for divergent implementation. iPadOS Full Keyboard Access works.
- **UIKit** has `UIFocusSystem`, `canBecomeFocused`, `preferredFocusEnvironments`. The model originally came from tvOS but covers iPad keyboard navigation. More work to set up than SwiftUI, more reliable when set up.
- **React Native**'s hardware-keyboard story is weaker than the others. `focusable` (Android), `nextFocusForward`/`nextFocusDown`/`nextFocusLeft`/`nextFocusRight` (Android, TV), `AccessibilityInfo.setAccessibilityFocus(reactTag)` (both platforms, screen-reader focus only). iOS Full Keyboard Access traversal is largely whatever the underlying native views give us; teams that need explicit keyboard support typically reach for `react-native-tvos` patterns or a native module.

The annotation that designers must make: **on iPadOS and tablet Android, every primary action and form field must be reachable by Tab.** Visual focus rings need to be styleable; the design system should ship them as a token. (See 14-accessibility's focus-indicator treatment.)

### Modal trapping and focus return

All four frameworks trap focus inside modals correctly when their native modal primitives are used. The universal failure mode is focus return: when a dialog dismisses, where does accessibility focus go?

- **Flutter**: `DialogRoute` traps with `closedLoop` traversal; focus *should* return to the dismissing widget but on iOS this is broken (open issue #107069, longstanding). Workaround: hold a `FocusNode` on the trigger, call `node.requestFocus()` after `await Navigator.pop(...)`.
- **Compose**: handles this well as of `material3:1.3.0`+. Before that, focus often landed at the top of the screen.
- **SwiftUI**: focus return on sheet/cover dismiss is system-managed in iOS 17+ and reliable; in earlier iOS or with custom `Overlay` modals, manual `@AccessibilityFocusState` management on the trigger is required.
- **UIKit**: post a `UIAccessibility.layoutChanged` notification with the trigger element as the argument after dismiss.
- **React Native**: focus return is absent by default. `AccessibilityInfo.setAccessibilityFocus(findNodeHandle(triggerRef.current))` on close is the standard pattern.

The right design-system position: focus return is non-optional. We treat it as a contract on every modal, and ship a "ModalTrigger" pattern in the system that wires it up correctly per framework.

A second failure that is universal: pseudo-modals built out of overlays (a `Box` with a translucent background covering the screen) do not trap focus by default in any framework. Whatever the framework, the design system's modal primitive must use the framework's actual modal API or wire focus trapping explicitly. We don't ship "looks like a modal but isn't one."

---

## Text scaling and reflow

(See 14-accessibility for the architectural treatment of typographic scaling as a system concern and the recommended ramps. This section covers the framework primitives.)

All four frameworks have the same conceptual model — read the system text-size setting, scale text accordingly — and the same failure mode: containers with fixed heights overflow when the user scales text past about 130%, and again past 200%, and again at iOS AX accessibility sizes.

- **Flutter** exposes the system scale via `MediaQuery.textScalerOf(context)`. The newer `TextScaler` API (3.16, late 2023) replaced the older `textScaleFactor` with a non-linear scaler that matches iOS Dynamic Type's AX sizes. Designers should never see `MediaQuery(textScaler: TextScaler.noScaling)` in production code; capping text scaling is a WCAG 1.4.4 failure unless the cap is generous (1.5×+).
- **Compose** uses `sp` (scale-independent pixels) for font sizes and `dp` for layout. Non-linear font scaling matching Android 14's curve landed in Compose UI 1.6 (2024). Reflow patterns rely on `BoxWithConstraints` or computed branching off `LocalConfiguration.current.fontScale`.
- **SwiftUI** uses the `dynamicTypeSize` environment value (`.large`, `.xLarge`, … `.accessibility1` through `.accessibility5`). Custom fonts must be declared as `.font(.custom(name, size: 16, relativeTo: .body))` to participate in Dynamic Type scaling. The HStack-to-VStack reflow pattern at AX1+ is idiomatic and well-documented.
- **UIKit** uses `UIFontMetrics.default.scaledFont(for:)` for custom fonts and the `adjustsFontForContentSizeCategory` flag. Auto Layout constraints can activate or deactivate based on `traitCollection.preferredContentSizeCategory`.
- **React Native** has `allowFontScaling` (default `true`) and `maxFontSizeMultiplier` on `Text` and `TextInput`. The two-platform divergence: iOS Dynamic Type and Android `fontScale` use different curves and different user-facing controls, so the same `maxFontSizeMultiplier = 2` lets a user reach roughly 32sp on iOS and 28sp on Android. Reflow is manual — listen to `useWindowDimensions().fontScale` and conditionally swap layouts.

Two consistent failure modes worth calling out for designers:

**Icon-with-text horizontal pairs break first.** Header layouts and navigation bars typically place an icon next to a label in a row. At AX1+ or 200%+ scaling, the row either truncates the label or squeezes it into an illegible column. The annotation requirement: every icon-text pair needs a documented reflow strategy (wrap to two lines, drop the icon, switch to a vertical stack, hide the label and keep the tooltip).

**Fixed-height containers are a trap.** A 48dp button with a single line of 14sp text works at default scaling and breaks at AX2. Buttons, list rows, app bars, tab bars — anything we treat as a fixed-height design primitive — needs to be a `minHeight`, not a `height`. This is a design-system architecture question, not just an implementation one. (See 14-accessibility.)

The design-system rule: **we ship components that respect the system text-size setting, and we test them at the maximum value.** `maxFontSizeMultiplier` capping is a tool of last resort, used only on a per-component basis with documented rationale, never globally.

---

## System preferences: contrast, color, motion, inversion

This is where iOS leads in API breadth and Android catches up unevenly, and where the cross-platform frameworks expose iOS APIs more reliably than Android's.

### Contrast and color

iOS exposes "Increase Contrast," "Differentiate Without Color," "Reduce Transparency," "Bold Text," "Smart Invert," and "Classic Invert" — five separate accessibility preferences that a design system must respect.

- **Flutter** has `MediaQueryData.highContrast`, `.boldText`, `.disableAnimations`, `.accessibleNavigation`, `.invertColors`. Coverage on iOS is more complete than on Android; "Increase Contrast" detection on Android is patchy without writing a platform channel.
- **Compose** has `LocalConfiguration` for some of this and gaps for the rest. The high-contrast text setting on Android has no first-class Compose API as of 1.8.x; teams typically build a `CompositionLocal` (`LocalHighContrastEnabled`) wired up via `AccessibilityManager.isHighTextContrastEnabled` from the platform.
- **SwiftUI** has `@Environment(\.accessibilityContrast)`, `\.accessibilityReduceMotion`, `\.accessibilityReduceTransparency`, `\.accessibilityDifferentiateWithoutColor`. UIKit has `traitCollection.accessibilityContrast` and the `UIAccessibility.is*Enabled` family. Full and reliable.
- **React Native** has `AccessibilityInfo.isReduceMotionEnabled()`, `.isReduceTransparencyEnabled()`, `.isBoldTextEnabled()`, `.isInvertColorsEnabled()`, `.isHighTextContrastEnabled()`. The iOS coverage is full; the Android coverage is real but not all settings map cleanly.

The design system position (and a strong cross-link to 14-accessibility's pair-token treatment): we ship a high-contrast token set that swaps in when "Increase Contrast" / "High Text Contrast" is active. Our color token semantics include a contrast variant by default. This means engineers don't have to reach for the API at all — the theme system handles it — and designers annotate the alternate color only when it diverges from the default high-contrast swap.

### Reduce Motion

All four frameworks expose the system setting. The design-system rule is consistent across all of them: animations that move content laterally, scale, or simulate physics should defer to the user setting. Cross-fades are always safe. The annotation requirement: every transition needs a "with Reduce Motion" alternative, even if it's just "skip the animation and snap to end state."

- Flutter: `MediaQuery.of(context).disableAnimations` and `accessibleNavigation`. Most built-in animations check this automatically.
- Compose: animations should respect `Settings.Global.ANIMATOR_DURATION_SCALE == 0f`; Compose's own animation APIs do this in 1.2+.
- SwiftUI: `@Environment(\.accessibilityReduceMotion)` and gate `withAnimation { }` on it.
- UIKit: `UIAccessibility.isReduceMotionEnabled`.
- React Native: `AccessibilityInfo.isReduceMotionEnabled()` plus `reanimated`'s `useReducedMotion` hook for animations in Reanimated 3.6+.

### Smart Invert and forced colors

This is the messy one. iOS "Smart Invert" inverts the UI but leaves images and media alone — *if* the app excludes them. "Classic Invert" inverts everything. The detection API (`UIAccessibility.isInvertColorsEnabled`) returns true for both and cannot distinguish them, which means our practice has to treat them as the same case: assume Smart Invert and make sure media is excluded.

- Flutter: detection works; exclusion requires a platform channel — there is no sanctioned framework-level API for excluding a widget from Smart Invert.
- Compose / Android: forced colors mode was added to AndroidX as a system-level accessibility setting; Compose has no first-class API as of 1.8.x. Teams build a `CompositionLocal` if the design system needs it.
- SwiftUI / UIKit: `.accessibilityIgnoresInvertColors(true)` (SwiftUI) and `accessibilityIgnoresInvertColors` (UIKit) cleanly mark an image or view as exempt. This is the only framework with a first-class fix.
- React Native: `accessibilityIgnoresInvertColors` prop exists, with the documented quirk that it doesn't reliably work on `<Image>` directly and must be applied to a wrapper `<View>`.

The cross-framework position our practice should hold: **every illustrative image, photo, and chart in the design system carries an "exclude from invert" annotation by default.** Brand-coloured icons should also be excluded if their meaning depends on hue. Decorative shapes that are pure UI chrome should *not* be excluded — they should invert with the rest of the UI.

### Bold Text

iOS only. `UIAccessibility.isBoldTextEnabled` (UIKit), `@Environment(\.legibilityWeight)` (SwiftUI), `MediaQueryData.boldText` (Flutter), `AccessibilityInfo.isBoldTextEnabled()` (RN). System fonts respond automatically; custom fonts need a heavier alternate weight wired up. The token-system position: every font role in the design system has a Bold-Text variant.

---

## Tap targets, gestures, and input alternatives

This is the area where all four frameworks converge most closely.

**Minimum target sizes** are 44pt on iOS, 48dp on Android. WCAG 2.5.5 Level AAA was 44 CSS px; WCAG 2.5.8 Level AA (added in 2.2) is 24 CSS px, which is below both native minimums — so platform conventions are the binding constraint for us, not WCAG. Our practice: 48dp / 44pt, enforced.

- Flutter: `meetsGuideline(androidTapTargetGuideline)` and `meetsGuideline(iOSTapTargetGuideline)` for tests; visually small controls (like a small `Checkbox`) get expanded touch bounds automatically by Material's `materialTapTargetSize`.
- Compose: Material 3's `LocalMinimumInteractiveComponentSize` expands semantic bounds to 48dp even for visually smaller components. `Modifier.minimumInteractiveComponentSize()` for custom widgets.
- SwiftUI: `.contentShape(Rectangle())` plus `.frame(minWidth: 44, minHeight: 44)` is the idiom; SwiftUI does not enforce the minimum automatically the way Material 3 does.
- UIKit: override `point(inside:with:)` or `hitTest(_:with:)` to expand the interactive area beyond the visual bounds.
- RN: `hitSlop` on the touchable component is the standard tool.

**Gesture alternatives** under WCAG 2.5.7 (Dragging Movements, 2.2 AA) require that drag-only and multi-finger gestures have single-pointer alternatives. The framework primitive is consistent: a screen-reader user reaches gestures via the rotor (iOS) or local context menu (Android).

- Flutter: `Semantics(onIncrease: ..., onDecrease: ..., customSemanticsActions: ...)` for drag, swipe, long-press alternatives.
- Compose: `customActions` semantic property; standard `SemanticsActions` for scroll, expand, dismiss.
- SwiftUI: `.accessibilityAction(named:handler:)`, `.accessibilityActions { }` block, `.accessibilityAdjustableAction` for increment/decrement.
- UIKit: `UIAccessibilityCustomAction` array on the view.
- RN: `accessibilityActions` array with `onAccessibilityAction` handler.

The annotation requirement: **every gesture-only interaction in the design needs a named alternative action.** Swipe-to-delete → "Delete" action. Long-press-for-context → "Show options" action. Drag-to-reorder → "Move up" / "Move down" actions. The label is what the screen reader announces in the rotor menu; designers write it.

**Magic Tap and Escape** (iOS only) deserve a mention. Two-finger double-tap (Magic Tap) typically triggers the primary action on screen — play/pause music, start/end a call. Two-finger scrub (Escape) dismisses modals. Both are conventions VoiceOver users rely on. Where a screen has an obvious primary action, the design system should wire Magic Tap up. Escape should be wired on every modal as belt-and-braces alongside the close button.

---

## Live regions and announcements

The cross-framework conclusion: prefer implicit live regions for status updates; use imperative announcements sparingly and never for safety-critical messaging.

- **Flutter**: `Semantics(liveRegion: true, child: Text(statusMessage))` for inline updates. `SemanticsService.sendAnnouncement(message, textDirection)` for decoupled announcements (replaced the older `SemanticsService.announce`, deprecated after v3.35). The cross-platform divergence: `liveRegion` works on Android automatically; on iOS, `liveRegion` historically mapped to `UIAccessibilityTraitUpdatesFrequently` (which doesn't announce), then was patched to queue announcements on iOS ≥ 11.
- **Compose**: `Modifier.semantics { liveRegion = LiveRegionMode.Polite }` (or `.Assertive`). `View.announceForAccessibility` is the legacy imperative path and is deprecated in newer Android versions.
- **SwiftUI**: `AccessibilityNotification.Announcement` (iOS 17+) with priority levels. For older iOS, drop to `UIAccessibility.post(notification: .announcement, argument:)`.
- **UIKit**: `UIAccessibility.post(notification: .announcement, argument:)`, `.layoutChanged`, `.screenChanged`, `.pageScrolled`. Each notification has subtly different semantics; `.screenChanged` re-anchors VoiceOver focus to a new element.
- **React Native**: `accessibilityLiveRegion` (Android only) with `none`/`polite`/`assertive`. `AccessibilityInfo.announceForAccessibility` (iOS reliable; Android disruptive — TalkBack flushes its queue). The newer `announceForAccessibilityWithOptions` on iOS allows queue priority.

The universal failure mode: announcements triggered at the same instant as a screen transition get dropped. Every framework has some version of this bug; the workaround is to defer the announcement (200–400ms) after the transition completes.

The polite-vs-assertive decision:

- **Polite** for everything that isn't an emergency. Form-field count, search-results-updated, item-added-to-cart, save-completed. Almost everything in a design system is polite.
- **Assertive** for safety-critical or actively-required user attention — form submission errors that block the user, session-expired alerts, validation that prevents proceeding. Reserve for cases where interruption is justified.

The design-system position: dynamic regions in components carry a "polite" / "assertive" annotation, and the default is polite. We don't ship "assertive on everything" defaults; the interruption cost is too high.

---

## Testing and conformance evidence

Every framework has test APIs that cover roughly the same surface — labels, roles, tap targets, contrast, basic traversal — and none of them can substitute for manual testing with real assistive tech on real hardware. Our practice treats automated tests as a regression net, not a conformance proof.

- **Flutter**: `meetsGuideline(androidTapTargetGuideline)`, `meetsGuideline(iOSTapTargetGuideline)`, `meetsGuideline(labeledTapTargetGuideline)`, `meetsGuideline(textContrastGuideline)`. `tester.semantics` exposes a `SemanticsController` with `simulatedAccessibilityTraversal` for asserting traversal order. The `accessibility_tools` package provides an in-app debug overlay that flags issues at design time and is the easiest "shift-left" tool.
- **Compose**: `SemanticsMatcher`, `onNodeWithContentDescription`, `assertHasClickAction`, accessibility checks integrated via `enableAccessibilityChecks()` in Compose 1.8+. Lint rules in AndroidX flag missing content descriptions. Accessibility Scanner is the on-device Android tool.
- **SwiftUI / UIKit**: `XCUIApplication.performAccessibilityAudit()` (Xcode 15+, iOS 17+) covers contrast, Dynamic Type, element detection, hit-region size, sufficient element description, and trait correctness. Accessibility Inspector is the live-tree inspection tool. SwiftUI previews have accessibility preview modes.
- **React Native**: `@testing-library/react-native` for unit tests with `getByRole`, `getByA11yState`, `getByA11yLabel`. `eslint-plugin-react-native-a11y` for lint. Detox / Appium / Maestro for E2E (these depend on accessibility identifiers, so good labels yield good tests for free — this is one of the strongest arguments for setting them properly).

**Manual testing** is non-negotiable. Our practice: every release walks the top user journeys on a physical Android device with TalkBack and a physical iOS device with VoiceOver. Hardware keyboard testing is added when the app targets iPad or Android tablets. Switch Control / Switch Access pass is added when the contract requires it.

**Conformance evidence** for ACR / VPAT is the question agencies face most. Three positions worth holding:

- Automated tests do not generate VPAT-grade evidence. They generate regression protection. The VPAT comes from manual audit results, documented per-criterion.
- Cross-platform apps need separate VPATs per platform. A React Native or Flutter codebase shipped to iOS and Android passes WCAG criteria differently on each; one document conflating them is misleading.
- WCAG 2.2 AA is the realistic target across all four frameworks today, with the caveat that several framework gaps (heading levels on iOS, listbox virtualization with custom pickers, platform-view focus on iOS WebView) are worth documenting explicitly in the "remarks" column of the VPAT rather than claiming silent conformance.

---

## Failure modes

The recurring failures across all four sets of source material. Treat as a release checklist.

**Gesture-only controls with no role.** An icon with `onTap` (Flutter), `clickable` on a `Box` (Compose), `onTapGesture` (SwiftUI), or `onPress` on a `View` (RN) that does not declare a role is invisible to screen readers and untestable via Appium-class tools. Every interactive element in the system needs a role.

**Decorative images not excluded.** An image with no semantic intent that the framework treats as content-bearing makes the screen reader announce file paths, asset names, or "image" with no description. The design system marks every image as content or decoration explicitly.

**Modal focus return missing.** A dialog dismisses, accessibility focus jumps to the top of the screen, the user is lost. The ModalTrigger pattern in the design system wires focus return per framework.

**`accessible={true}` on a React Native parent with nested touchables.** Children become unreachable on iOS VoiceOver. Either the parent is not `accessible={true}` and each child is independently focusable, or the children are not interactive.

**`Stack` / `ZStack` stealing focus.** Stacked layouts can land focus on a backgrounded element, especially on iOS 16+ in Flutter (#113377, now fixed but only on newer Flutter versions). When a design uses stacking for visual effect, the design system should validate which layer is actually focusable.

**Custom-painted graphics invisible to assistive tech.** Charts, sparklines, signature pads, custom progress indicators — all of them need an accessible representation. The design system requires one before the component ships.

**`allowFontScaling` globally disabled "for design fidelity."** A WCAG 1.4.4 failure. The design system caps scaling per-component with documented rationale, never globally.

**Live-region announcements during transitions getting dropped.** Defer announcements 200–400ms after a route change.

**Smart Invert exclusions missing on photos and illustrative imagery.** Photos become inverted into surrealist negatives. The design system carries the exclusion annotation by default on all media.

**Headings declared but no level.** Flutter's `headingLevel` is web-only as of 3.32. SwiftUI's heading trait has no level. Mobile screen readers don't navigate by heading level on iOS the way they do on web — so the design system should mark headings semantically but not bake heading-level navigation into the mobile experience contract.

---

## Tensions and open questions

**Heading levels on iOS.** The native concept of `accessibilityHeading` with levels exists in iOS but Flutter doesn't wire `headingLevel` to it (open issue #155928, #97894 — verify at time of writing). SwiftUI's heading trait has no level. The design system can mark headings semantically and rely on logical reading order, and flag the level gap in the VPAT — but the practice should not require heading-level navigation as a contract on mobile until the framework support catches up.

**SwiftUI's focus-system conflation.** `@FocusState` and `@AccessibilityFocusState` are separate, but practitioners regularly conflate them, and SwiftUI's own documentation is ambiguous on which one wins when both are bound. Our annotation contract should specify which focus system a focus order applies to: keyboard, screen-reader, or both.

**One ACR or two?** Cross-platform apps (Flutter, React Native) ship one codebase to two platforms. The realistic position is two ACRs — one per platform — because the accessibility tree implementations diverge. Agency clients sometimes ask for one document covering both; we should educate before agreeing.

**Smart Invert detection.** No public API in any framework distinguishes Smart Invert from Classic Invert. The pragmatic position is to treat them as the same — assume Smart Invert, exclude media — but we should track whether the platforms ever expose the distinction. As of the date of this synthesis, they do not.

**`SemanticsRole` / role enums.** Flutter 3.32's `SemanticsRole`, SwiftUI's `.isToggle` (iOS 17+) and similar new traits, and Compose's expanded `Role` values are useful on the platforms where they translate fully. On platforms where translation is incomplete (Flutter `SemanticsRole` is web-first; iOS catch-up is incremental), the older boolean flags are still load-bearing. Our practice: combine the new role API with the legacy flag for full coverage; don't bet a contract on the new API alone.

**Compose Multiplatform's accessibility story on iOS.** Compose on iOS via Compose Multiplatform is newer than Compose on Android and we should not assume parity with the native frameworks. For projects considering CMP for iOS, accessibility should be a release-blocking validation, not a checkbox.

**React Native's New Architecture (Fabric) on accessibility.** Fabric's synchronous JSI-based commits remove the bridge latency that previously caused stale labels during rapid state updates. The prop surface is unchanged; the implementation underneath is better. Practitioner reports of "label not updating immediately after state change" should largely disappear on Fabric. We have not yet field-tested this at scale.

---

## See also

The Figma annotation contract — what designers specify so engineers can implement these primitives faithfully — is its own file (See 17-accessibility-annotation-contract.) That contract is currently mobile-scoped; web extension is a known gap.

For the architectural treatment of accessibility as a system concern — pair tokens, ARIA encapsulation, the four-layer model, conformance reporting — see 14-accessibility.

For the mobile context this file sits inside — tokens as the shared layer, native vs. custom component decisions, platform-specific token delivery — see 11-mobile-and-cross-platform.

For directionality, RTL focus order, and locale-aware behaviour that overlaps with mobile accessibility — see 13-internationalization-and-rtl.

---

## Provenance

Synthesised from four dual-agent research runs filed 2026-05-13 covering Flutter, Jetpack Compose, SwiftUI + UIKit, and React Native. Each run paired an external agent's expert output with an independent Claude run against the same prompt. Source files are in `_research/_inbound/2026-05-13-mobile-a11y-*/`. The original Flutter source (screen-reader-only, narrower scope) was filed as the Flutter run's external-agent output and supplemented by a broader Claude run. Version-specific claims about Flutter, Compose, SwiftUI, UIKit, and React Native APIs are dated to the synthesis date; verification path for load-bearing version claims is the framework's release notes and issue tracker — re-check before using in client-facing conformance documentation.

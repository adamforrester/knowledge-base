# Mobile Accessibility in SwiftUI and UIKit — Claude run

> Research scope: implementation depth for iOS (including iPad / Catalyst hardware keyboard) across SwiftUI and UIKit, with the goal of closing the gap between an accessibility-encoded design system and a screen that ships to WCAG 2.2 AA on a real device. Version baseline: iOS 17 / Xcode 15 as the stable floor; iOS 18 (WWDC 2024) where it materially changes the picture. Dated where load-bearing.

---

## 1. The accessibility primitives SwiftUI and UIKit expose

### UIKit: UIAccessibility as an informal protocol on UIView

UIKit's accessibility surface is the `UIAccessibility` informal protocol on `NSObject` (in practice, on `UIView` and `UIAccessibilityElement`). Every view has the following addressable properties: `isAccessibilityElement`, `accessibilityLabel`, `accessibilityValue`, `accessibilityHint`, `accessibilityTraits`, `accessibilityIdentifier`, `accessibilityElements`, `accessibilityCustomActions`, `accessibilityCustomRotors`, `accessibilityActivationPoint`, `accessibilityFrame`, `accessibilityLanguage`, plus the `accessibilityContainerType` and (iOS 17+) `accessibilityAttributedLabel/Value/Hint` variants for marking pronunciation, language, or text attributes.

The model is the **accessibility element tree** — a parallel tree alongside the view hierarchy. A `UIView` is either itself an accessibility element (`isAccessibilityElement == true`) or it is a container whose `accessibilityElements` (or, by default, eligible descendants) become children in the tree. Controls (`UIButton`, `UISwitch`, `UISegmentedControl`, `UITextField`, `UISlider`, `UIStepper`, `UITableViewCell`) opt themselves in and supply sensible defaults for label/traits/value. Plain `UIView`, `UIImageView`, `UILabel` are leaf elements when they have content; container views (`UIStackView`, `UIScrollView`, plain wrapping `UIView`s) are not elements themselves — their descendants are.

The crucial UIKit-specific behaviour is **flattening**. When you set `isAccessibilityElement = true` on a container, VoiceOver treats it as a single leaf and its descendants disappear from the tree. This is the standard way to merge a card or row into one swipe-stop: set the container's label to a synthesised string, set `isAccessibilityElement = true`, and the children become invisible to AT.

### SwiftUI: a declarative tree of modifiers

SwiftUI builds its accessibility tree from view modifiers, not from view-class state. The relevant surface:

- **Naming and description**: `.accessibilityLabel`, `.accessibilityValue`, `.accessibilityHint`, `.accessibilityInputLabels` (for Voice Control alternative names).
- **Semantics**: `.accessibilityAddTraits` / `.accessibilityRemoveTraits` against the `AccessibilityTraits` option-set (`.isButton`, `.isHeader`, `.isSelected`, `.isLink`, `.updatesFrequently`, `.playsSound`, `.causesPageTurn`, `.allowsDirectInteraction`, etc.).
- **Tree shaping**: `.accessibilityElement(children:)` with `.ignore` (flatten and own the label), `.combine` (concatenate descendants into one element), `.contain` (act as a container, keep children navigable).
- **Hiding**: `.accessibilityHidden(true)`.
- **Substitution**: `.accessibilityRepresentation { … }` (iOS 14+) — declare a *semantic* equivalent that AT sees in place of the rendered view. The canonical case is a custom-drawn slider that visually renders shapes but semantically `accessibilityRepresentation`s a `Slider`.
- **Child augmentation**: `.accessibilityChildren { … }` (iOS 15+) — declare additional virtual children when a view's drawn content has structure VoiceOver can't otherwise see (e.g. a `Canvas`-drawn chart with logical data points).
- **Actions**: `.accessibilityAction(named:)`, `.accessibilityAction(.magicTap) / .escape / .default`, `.accessibilityAdjustableAction`, `.accessibilityScrollAction`.
- **Order / containers**: `.accessibilitySortPriority(_:)`, `.accessibilityElement()` with `.contain`, `.accessibilityRotor(_:)` for custom rotors.

### Mental model and divergence

In UIKit, the developer maintains a parallel data structure that *describes* the view. In SwiftUI, the developer composes modifiers and SwiftUI generates the accessibility tree. The two diverge in three important places:

1. **Default semantics.** SwiftUI's high-level controls (`Button`, `Toggle`, `Picker`, `Stepper`, `TextField`, `Slider`, `Link`, `NavigationLink`, `Menu`) carry correct role, state and value automatically and *also* respond to the right gesture from VoiceOver, Voice Control, and Switch Control without further work. UIKit controls do too, but anything you draw yourself in UIKit (a `UIView` subclass with `draw(_:)`) is invisible by default; in SwiftUI, the equivalent (a `Shape`, `Path`, `Canvas`) is also invisible *but you can attach semantics declaratively without subclassing*.
2. **Container model.** UIKit asks "is this the element, or do you want me to look at its children?" SwiftUI asks "for this subtree, do you want the children combined, ignored, or kept separate?" The mental shift matters when you port code: UIKit's `isAccessibilityElement = true` corresponds to SwiftUI's `.accessibilityElement(children: .ignore)` *plus* `.accessibilityLabel(...)`.
3. **Composition leakage.** In SwiftUI, modifiers applied higher up the tree don't necessarily override modifiers applied lower — the *innermost* `.accessibilityLabel` typically wins on a leaf, and `.accessibilityElement(children:)` reshapes who the leaf is. This is the source of most "why doesn't this label apply?" bugs; the cure is to be explicit about where the element boundary is.

### What's automatic, what's opt-in

| Control | UIKit default | SwiftUI default |
| --- | --- | --- |
| Button / `UIButton` | Label from title, `.button` trait | Label from content, `.isButton` |
| Toggle / `UISwitch` | "Switch button", value "1"/"0" | Label, `.isToggle` (iOS 17+) / "Switch button", state announced |
| Picker / segmented | Selected segment announced | Selected option announced |
| TextField | Label = placeholder if no separate label set | Label from `Text` label, value from binding |
| Slider | Value announced, adjustable | Adjustable, value announced |
| Tappable `Image` / `Shape` | Invisible unless made an element | Invisible unless `.accessibilityLabel` + button-y wrapping |
| Decorative SF Symbol | Picked up as element with symbol name (bad) | Same; use `.accessibilityHidden(true)` |
| Custom-drawn control | Invisible | Invisible |

### Common pitfalls

- **Custom controls drawn with shapes/Canvas** that ship with no `accessibilityRepresentation` and no manual label/trait. This is the single biggest source of regression when designers ask for non-standard styling.
- **Gesture-only views** — `.onTapGesture` on a `VStack` does *not* add `.isButton`; VoiceOver users get no affordance and no action. The cure is to wrap in `Button` or add `.accessibilityAddTraits(.isButton)` + an `.accessibilityAction`.
- **Decorative SF Symbols** announced as "star.fill, image" because the developer did not hide them. SwiftUI: `.accessibilityHidden(true)`. UIKit: set the parent button's label and leave the image with `isAccessibilityElement = false`.
- **Concatenated labels** built by joining strings without `.accessibilityElement(children: .combine)`, which produces correct strings but loses the structural opportunity to use `.accessibilityValue` for the dynamic part.
- **Header inflation** — every section title marked `.isHeader` is fine, but only when the title is genuinely a heading; turning every bold word into a header destroys the rotor.

---

## 2. Focus and traversal

### VoiceOver swipe order

VoiceOver's swipe order is, by default, a **geometric reading order** approximated from the accessibility frames of elements: top-to-bottom, leading-to-trailing (right-to-left in RTL locales). This is *not* the view hierarchy order, which is a common source of confusion when a developer rearranges z-order but VoiceOver order remains visually-driven.

To override:

- **UIKit** — set `accessibilityElements` on the container to an explicit array. The array order *is* the swipe order. There's no per-element priority API; you reorder by rewriting the array. For deeply nested containers you may need to flatten on the container by overriding `accessibilityElements` to return a curated list (and ensure `isAccessibilityElement` is `false` on the container itself).
- **SwiftUI** — use `.accessibilitySortPriority(_:)` (higher values come first within the same container). For larger reorderings, wrap a region in `.accessibilityElement(children: .contain)` to make it an explicit container, then apply sort priorities to its members. SwiftUI does not let you express "this element is at index N globally"; you express relative priority within a container, which is usually enough.

### Hardware keyboard and Full Keyboard Access on iPad / iOS

Full Keyboard Access (FKA) is the iOS accessibility feature (Settings → Accessibility → Keyboards → Full Keyboard Access) that draws a visible focus ring and lets the user Tab through interactive elements. It's a separate focus engine from VoiceOver's element tree, though it largely reuses the same accessibility semantics.

UIKit's hooks:

- `canBecomeFocused` / `isFocused` (originally tvOS, now used by FKA).
- `preferredFocusEnvironments` on a `UIFocusEnvironment` (view controller or view) to drive initial focus.
- `UIFocusGuide` to bridge gaps the focus engine can't reach (e.g. wrap-around behaviours, or a focus path across two siblings the geometric algorithm doesn't connect).
- `UIFocusUpdateContext` in `didUpdateFocus(in:with:)` to observe and react to focus changes.

SwiftUI's hooks:

- `@FocusState` (iOS 15+) — a property wrapper that binds to a focusable region and lets you read or set the focused field/value.
- `.focusable(_:interactions:)` — declares a view focusable, with `interactions` (iOS 17+) telling SwiftUI whether the view participates in activation, edit, or both.
- `.focused($state)` / `.focused($state, equals: …)` — connects a view to a `FocusState` binding.
- `.focusEffect` (iOS 17+) for custom focus indicators where the default ring is wrong.
- `.focusSection()` and `.focusScope(_:)` to define focus groups (originally tvOS; useful on iPad).
- `.defaultFocus($state, value, priority:)` to declare initial focus when a region appears.

The most-missed gotcha: **`Button` is FKA-focusable; a `Color`/`Shape` with `.onTapGesture` is not.** A custom-styled tap target in SwiftUI gets keyboard focus only if it's a `Button` (or `.focusable(true)` is added explicitly with an `.accessibilityAction`). Designers who specify non-button-looking interactive surfaces must annotate them as interactive.

### Switch Control

Switch Control walks the same element tree as VoiceOver but groups it for item-mode scanning. Two specific concerns for design systems:

- **Element grouping.** Switch Control benefits from coarse grouping — a card as a single stop is faster to navigate than five children. The same `.accessibilityElement(children: .combine)` / `isAccessibilityElement = true` that helps VoiceOver also helps Switch Control.
- **Custom actions.** Switch Control surfaces `accessibilityCustomActions` in the action menu. Long-press or swipe-to-delete that has no custom-action equivalent is invisible to Switch Control users (and to VoiceOver users).

### Modal trapping and focus return

Sheets, alerts, and `fullScreenCover` automatically trap accessibility focus inside the modal in both UIKit (`UIViewController.presentationController`) and SwiftUI (`.sheet`, `.alert`, `.fullScreenCover`). What does *not* always happen automatically is:

- **Initial focus** on a specific element when the modal appears. UIKit: post `UIAccessibility.post(notification: .screenChanged, argument: <view>)` after the modal becomes visible. SwiftUI: `@FocusState` with a `task { focused = .someField }` after a small delay, or `AccessibilityFocusState` (iOS 15+) for VoiceOver focus specifically.
- **Focus return** to the triggering element on dismiss. UIKit: capture the previously-focused element, dismiss, then `.screenChanged` to that element. SwiftUI: this works for `@FocusState` in many cases but is unreliable for `AccessibilityFocusState` across sheet boundaries — practitioners commonly post a `screenChanged` notification via a small UIKit bridge.

`AccessibilityFocusState` (iOS 15+) is SwiftUI's first-party VoiceOver focus API. It is *separate* from `FocusState` and works only for VoiceOver — this is the principal place where SwiftUI does *not* conflate the two focus models. The trap is that `AccessibilityFocusState` does not always reliably move VoiceOver focus on initial appearance of a modal in earlier 15.x / 16.x releases; FB10584322-style reports recurred through iOS 16. As of iOS 17 the behaviour is improved but not bulletproof; the workaround remains a UIKit-bridged `screenChanged` post.

### NavigationStack and TabView

`NavigationStack` (iOS 16+) places initial accessibility focus on the back-button equivalent or the first element of the destination view, depending on push vs. presented context. This is usually correct. The known weak spot is a destination view that *itself* has dynamic content loaded after appear: VoiceOver lands on whatever was there at first paint. The fix is to explicitly post an announcement or move focus once content has loaded.

`TabView` switches: VoiceOver focus stays on the tab bar by default after a tab switch (you confirm the change, but the new tab's content is not announced). This is intentional and consistent with the platform; most apps don't override it.

### Accessibility focus vs. keyboard focus — where SwiftUI conflates them

The clean separation:

- **VoiceOver focus** = where the green/black ring is for screen-reader users; driven by the accessibility tree.
- **Keyboard focus** (FKA) = where the visible blue focus ring is for sighted keyboard users; driven by the focus environment.

In SwiftUI, the conflation surfaces are:

- `.focusable(_:)` makes a view focusable for *both* keyboard and VoiceOver in some contexts and only one in others, depending on whether the view is also a control. The `interactions:` parameter (iOS 17+) helps; before that, the behaviour was ambiguous.
- `@FocusState` is keyboard/hardware-focus state. `AccessibilityFocusState` is VoiceOver focus state. They are *not* synonyms; setting one does not move the other. Code that treats them interchangeably will mis-focus on either VoiceOver or FKA depending on which test was last run.
- `.accessibilityFocused($state)` (the modifier counterpart of `AccessibilityFocusState`) is the right tool when you specifically need to announce something or move VO focus on a state change.

The practical heuristic: if the user moves it with a swipe or rotor, it's VoiceOver focus; if they move it with Tab on a keyboard, it's FKA. Different bindings, different APIs.

---

## 3. Text scaling and reflow

### Dynamic Type, the platform model

iOS exposes a single user preference (`UIContentSizeCategory` / `DynamicTypeSize` in SwiftUI) on a scale from `xSmall` through `xxxLarge` and then the five accessibility sizes `AX1`–`AX5`. The text styles (`largeTitle`, `title`, `body`, `caption`, etc.) are size classes that scale against this preference. Apple's HIG promises legible text at all sizes up to AX5 in system controls; everything you build inherits this *only if* you opt in.

### SwiftUI

Text using `.font(.body)`, `.font(.title)`, etc., scales automatically. `Font.system(size: 17)` does *not* scale; use `Font.system(.body)` or `.system(size: 17, relativeTo: .body)` for a fixed visual baseline that still respects Dynamic Type. The environment exposes `@Environment(\.dynamicTypeSize)` (iOS 15+) which returns a `DynamicTypeSize` you can compare (`>= .accessibility1`). `.dynamicTypeSize(_:)` lets you constrain a subtree's scaling (e.g. `.dynamicTypeSize(...(.accessibility3))` to cap at AX3); this is the right tool for tight chrome where layout breaks at AX5.

`ScaledMetric` (iOS 14+) lets numeric values (icon sizes, paddings, frame sizes) scale alongside Dynamic Type: `@ScaledMetric var iconSize: CGFloat = 24`. This is the SwiftUI equivalent of `UIFontMetrics.scaledValue(for:)`.

### UIKit

Use `UIFont.preferredFont(forTextStyle:)` to fetch a Dynamic-Type-aware font, and set `adjustsFontForContentSizeCategory = true` on the label/text field/text view. For custom fonts, use `UIFontMetrics(forTextStyle:).scaledFont(for: <your font>)` and set `adjustsFontForContentSizeCategory = true`. For scaling non-text values (icon size, row height), `UIFontMetrics.default.scaledValue(for: <base>)`.

`UIContentSizeCategoryAdjusting` is the protocol that controls auto-adjustment; it's on `UILabel`, `UITextField`, `UITextView`. Custom views need to observe `UIContentSizeCategory.didChangeNotification` and re-layout.

### What breaks at AX1–AX5

The pathological cases, in rough order of frequency:

1. **Fixed-height containers.** A `frame(height: 44)` for a 44-pt button is fine at default size; at AX5, body text needs ~60 pt of vertical room and the label clips. Cure: drop fixed heights, use min-height with `.frame(minHeight: 44)`.
2. **Horizontal icon-with-text pairs** that overflow the line at AX5 and either truncate or push the icon off-screen. Cure: switch to vertical layout above a threshold (`if dynamicTypeSize >= .accessibility1 { VStack { … } } else { HStack { … } }`). The HIG calls this pattern out specifically.
3. **Tab bars and navigation bars** with custom labels. The system handles its own, but a custom tab-bar item with a fixed `font(.caption)` won't reflow. Cure: rely on `Label` + `.labelStyle(.iconOnly)` when content overflows, or use `accessibilityLabel` to preserve naming while hiding visual text.
4. **Truncation by default.** `Text` defaults to single-line truncation in many container contexts. Add `.lineLimit(nil)` or `.lineLimit(2)` deliberately, and verify at AX5.
5. **Stacks of `HStack`s** where one column should reflow into a vertical layout — `ViewThatFits` (iOS 16+) is the canonical primitive for this; below 16, manual breakpoints.

### Cap or not cap

The defensible default is *don't cap.* Capping below AX5 fails WCAG 1.4.4 (Resize text, 200%) if you cap too low, and harms low-vision users. The legitimate cap-points are:

- **Tab-bar / navigation-bar / chrome** where AX sizes destroy the design — cap at AX1 or AX2 if reflowing isn't possible, and only on the chrome, not on content.
- **Marketing splash screens** with hand-tuned typography — cap at AX2 with a documented decision and a CTA that does *not* cap.

Anywhere you cap, document why. ACR/VPAT auditors and accessibility leads will ask.

### What the frameworks give you for free vs. need explicit code

| Concern | Free | Needs code |
| --- | --- | --- |
| Text styles scaling | Yes if you use `.font(.body)` / `preferredFont(forTextStyle:)` | Custom fonts (`scaledFont(for:)`); fixed `.system(size:)` |
| Icon sizes scaling | No | `ScaledMetric` / `UIFontMetrics.scaledValue` |
| Line height / spacing | Mostly | Custom paragraph styles |
| Layout reflow at AX | No | Manual `dynamicTypeSize` branches or `ViewThatFits` |
| Truncation prevention | No | `.lineLimit(nil)`, drop fixed heights |

---

## 4. System contrast, color, and motion preferences

### Detection APIs

UIKit exposes a set of static `UIAccessibility.is*Enabled` properties and matching `…DidChangeNotification`s. SwiftUI mirrors most of them via `@Environment` keys. Cross-reference:

| Preference | UIKit | SwiftUI environment |
| --- | --- | --- |
| Reduce Motion | `UIAccessibility.isReduceMotionEnabled` | `\.accessibilityReduceMotion` |
| Prefer Cross-Fade Transitions | `UIAccessibility.prefersCrossFadeTransitions` (iOS 14+) | (no first-party key — bridge from UIKit) |
| Reduce Transparency | `UIAccessibility.isReduceTransparencyEnabled` | `\.accessibilityReduceTransparency` |
| Increase Contrast (Darker System Colors) | `UIAccessibility.isDarkerSystemColorsEnabled` | `\.accessibilityShowButtonShapes` (related), `\.colorSchemeContrast` (`.standard` / `.increased`) |
| Differentiate Without Color | `UIAccessibility.shouldDifferentiateWithoutColor` | `\.accessibilityDifferentiateWithoutColor` |
| Invert Colors (Smart/Classic) | `UIAccessibility.isInvertColorsEnabled` | `\.accessibilityInvertColors` |
| Bold Text | `UIAccessibility.isBoldTextEnabled` | (no first-party key as of iOS 17 — bridge) |
| On/Off Labels (toggle 1/0) | `UIAccessibility.isOnOffSwitchLabelsEnabled` | (no first-party key — bridge) |
| VoiceOver running | `UIAccessibility.isVoiceOverRunning` | `\.accessibilityVoiceOverEnabled` |
| Switch Control running | `UIAccessibility.isSwitchControlRunning` | `\.accessibilitySwitchControlEnabled` |

The gaps in SwiftUI's environment coverage (Bold Text, OnOff Switch Labels, prefersCrossFadeTransitions) are well-known practitioner pain points; the workaround is a small `UIKit` observer that publishes into a SwiftUI `ObservableObject`.

### Dark mode interplay

Dark mode is *not* an accessibility setting; it's an aesthetic preference. But it interacts with accessibility because Increase Contrast applies on top of either light or dark scheme, producing four trait permutations (light/standard, light/increased, dark/standard, dark/increased). UIKit's `UITraitCollection` exposes both `userInterfaceStyle` and `accessibilityContrast`. Color assets in `.xcassets` support all four variants directly — use them rather than branching in code.

SwiftUI reads them via `\.colorScheme` and `\.colorSchemeContrast`. The standard pattern is to define semantic colors in the asset catalog with all four variants and reference them by name; explicit branching in views is a sign your token system is leaking into application code.

### Reduce Motion and Prefer Cross-Fade Transitions

Reduce Motion is a user request to avoid parallax, large translations, springy/bouncy animations, and anything that triggers vestibular discomfort. The contract isn't "no animation" — a brief cross-fade or opacity change is generally acceptable.

SwiftUI: `@Environment(\.accessibilityReduceMotion) private var reduceMotion` and gate animations:

```swift
.animation(reduceMotion ? .none : .spring(), value: state)
// or
.transition(reduceMotion ? .opacity : .move(edge: .leading))
```

UIKit: check `UIAccessibility.isReduceMotionEnabled` before `UIView.animate` calls with spring damping / non-trivial translation. For transition styles, swap `UIView.AnimationOptions.transitionCrossDissolve` in.

`prefersCrossFadeTransitions` (iOS 14+) is a *narrower* preference users can enable to specifically request cross-fade over slide transitions on push/pop. Apps that respect Reduce Motion mostly satisfy this for free, but if you've built custom transitions you should branch on this too.

### Smart Invert and `accessibilityIgnoresInvertColors`

Smart Invert inverts the UI but leaves images, media, and views explicitly marked as not to be inverted. The mark:

- UIKit: `view.accessibilityIgnoresInvertColors = true` on `UIImageView`s and any view with photographic or chrome that mustn't invert.
- SwiftUI: `.accessibilityIgnoresInvertColors(true)` on `Image` and any wrapper.

A common annotation: every photographic image and every brand-color element should be marked. Decorative system colors should *not* be marked (they're meant to invert). This is one of the design-system contracts that is dead easy to forget; tooling-level lints (a custom SwiftLint rule, for example) help.

### Differentiate Without Color

This preference asks UI to convey state by something other than colour alone — shape, label, icon. Mandatory in any pattern that uses color as the *only* signal (red/green status badges, chart series differentiated by color only). The detection API is `\.accessibilityDifferentiateWithoutColor` (SwiftUI) / `UIAccessibility.shouldDifferentiateWithoutColor` (UIKit), and the response is to render an additional shape or text label when it's `true`. Note: WCAG 1.4.1 requires this *unconditionally* for sighted-non-screen-reader users — the iOS preference is not a justification for color-only signaling when off; it's a stronger signal when on.

### What's native vs. explicit

- **Native:** Dynamic Type for system controls, Smart Invert behaviour on non-photographic content, Bold Text on system fonts, dark mode contrast in `.xcassets`, system colour adaptation (`UIColor.label` and friends; `Color.primary`, `Color.accentColor`).
- **Explicit:** Reduce Motion, Differentiate Without Color, Increase Contrast (custom drawn views), Smart Invert on photographs, custom transitions, custom fonts.

---

## 5. Tap targets, gestures, and input alternatives

### The 44×44 pt minimum

Apple's HIG specifies 44×44 pt as the minimum tap target. This is *not enforced* by either framework — you can ship a 16-point button and it will compile. WCAG 2.5.5 (AAA) asks 44×44 CSS px; WCAG 2.5.8 (AA, added in 2.2) asks 24×24 CSS px. The iOS HIG number is more conservative than WCAG 2.2 AA. Both numbers refer to *effective* hit area, not visual size — a 24-point icon centered in a 44-point hit area is compliant.

SwiftUI: `Button` defaults to a hit area sized to its content; a small icon-only button needs `.frame(minWidth: 44, minHeight: 44)` or `.contentShape(Rectangle())` on a wrapping view of the right size. `.contentShape` is the right primitive when the *visual* should stay small but the *hit area* should be larger — the shape is what receives gestures.

UIKit: `UIButton`'s hit area is by default its bounds. Two approaches:

1. Increase `bounds` and use `contentEdgeInsets` / `imageEdgeInsets` (deprecated in iOS 15 in favour of `UIButton.Configuration`) to keep the visual centered in a larger frame.
2. Override `point(inside:with:)` on the button (or `hitTest(_:with:)` on a parent) to enlarge the hit region beyond the visual bounds. This is the iPhone-stalwart trick for crowded toolbars but should be used sparingly because it can shadow neighbouring hits.

### Gesture alternatives — WCAG 2.5.4 and 2.5.7

WCAG 2.5.7 (Dragging Movements, AA in 2.2) requires that any drag operation has a single-pointer alternative that isn't itself a drag. WCAG 2.5.4 (Motion Actuation, A) requires the same for motion-triggered actions (shake to undo). WCAG 2.5.1 (Pointer Gestures, A) for multi-finger/path-based gestures.

The iOS-specific mappings:

- **Drag to reorder / swipe-to-delete on lists** — `EditButton` (SwiftUI) and `UITableViewCell` edit mode satisfy 2.5.7 because they expose reordering and deletion as single taps. *In addition*, swipe-to-delete actions should be exposed as `accessibilityCustomActions` (UIKit) / `.accessibilityAction(named:)` (SwiftUI) so VoiceOver and Switch Control users can invoke them — this also covers 2.5.1 for the swipe gesture itself.
- **Long-press menus** — `.contextMenu` (SwiftUI) and `UIContextMenuInteraction` (UIKit) are correctly exposed to VoiceOver as a custom action by default. If you build a custom long-press menu yourself, you must add the custom action manually.
- **Shake to undo** — provide an Undo button. `UIResponder.motionEnded` is fine, but it cannot be the only path.
- **Pinch / rotate / pan on images** — buttons for "zoom in / zoom out / reset" are the standard alternative.

The single-most-missed annotation is *the custom action label*. A drag gesture exposed as a custom action needs a clear short verb-noun phrase: "Reorder", "Delete", "Mark as read".

### `accessibilityCustomActions` and `.accessibilityAction`

The UIKit and SwiftUI APIs are equivalent in semantics, with minor syntactic difference. The model is: each custom action is a (name, handler) pair; VoiceOver users open the actions menu (rotor → Actions) and select. Practical rules:

- Keep action labels short (one or two words). They're spoken every time the user opens the menu.
- Don't duplicate the primary tap — the activation gesture is its own thing. Custom actions are for *additional* operations the gesture path doesn't cover.
- Group them on the *container element*, not on each child, when the actions apply to the row/card as a whole.

---

## 6. Live regions, announcements, and dynamic content

### The notification model

UIKit's `UIAccessibility.post(notification:argument:)` covers four cases:

- `.announcement` — interrupt VoiceOver with a string to speak. Use sparingly.
- `.layoutChanged` — the layout has changed; the argument (if a view) becomes the new VoiceOver focus. Use for in-place content changes (a new error message, a filter applied).
- `.screenChanged` — a major screen change; resets the cursor and (with argument) moves focus. Use for modal presentation/dismissal and large nav transitions.
- `.pageScrolled` — the content has scrolled; argument is a description string ("Page 2 of 7"). Use for paged content.

Ordering and queueing: announcements are *not* queued reliably. If you post two announcements in quick succession the second often interrupts the first. The iOS 17 addition `AccessibilityNotification.Announcement(_:)` accepts a priority via `AccessibilityNotification.AnnouncementPriority` (`.low`, `.default`, `.high`) which addresses *some* of this, but practitioners still see flakiness on actual devices; a defensive pattern is to debounce announcements and only post when the user-relevant change has settled.

### SwiftUI

`AccessibilityNotification.Announcement("Saved")` posts an announcement, equivalent to UIKit's `.announcement`. The iOS 17 SwiftUI surface (`.accessibilityRespondsToUserInteraction`, the `AnnouncementPriority` types) is still maturing; pre-17 SwiftUI projects often bridge to UIKit's `UIAccessibility.post` because they need fine control. There is no first-party SwiftUI equivalent to `.layoutChanged` with a focus-target argument — you bridge via UIKit when you need to move focus along with the announcement, or you use `.accessibilityFocused($state)` for the focus shift and post an announcement separately.

### Status messages, loading, errors

The WCAG 4.1.3 (Status Messages, AA) requirement maps to the *announcement* pattern in iOS — there's no `aria-live="polite"` equivalent, only the imperative post. Decision framework:

- **Inline error appearing on a field after blur** — `.layoutChanged` with the error view as the argument (UIKit) or `AccessibilityFocusState` moved to the field with `accessibilityValue` updated to include the error (SwiftUI). The error text should be associated with the field via `accessibilityLabel`/`accessibilityValue`, not announced separately, so VoiceOver users re-encountering the field hear it.
- **Toast / banner notification** — `.announcement` with the body text. Keep brief.
- **Loading state appearing** — `.announcement` "Loading…" *only if* the user initiated the action and a delay is expected. Don't announce every fetch.
- **Loading state resolving to content** — `.screenChanged` with the first content element as focus target, or `.layoutChanged` if the rest of the screen is preserved.
- **Page navigation in a paged scroll view** — `.pageScrolled`.

A common anti-pattern: announcing every change that *visually* appears (skeleton loaders, micro-animations). Most are noise to a VoiceOver user; only announce when the *information* changes.

---

## 7. Testing, tooling, and conformance evidence

### XCUITest accessibility APIs

XCUITest queries the same accessibility tree VoiceOver does. The query API (`app.buttons["Save"]`, `app.textFields.element`) matches by *accessibility label* unless you've supplied a separate `accessibilityIdentifier`. The discipline that matters at scale:

- **`accessibilityIdentifier` for tests, `accessibilityLabel` for users.** Identifiers are non-localised, non-user-visible strings (`saveButton`, `loginFlow.email`). Labels are the human-readable name. Mixing them — using English labels in test code — breaks localisation testing.
- **XCUIElement traits expose what the user gets**: `.exists`, `.isHittable`, `.isEnabled`. They map to `isAccessibilityElement` plus geometric in-bounds.

### Accessibility Inspector and audits

The Xcode Accessibility Inspector ships with two modes: **Inspect** (point at an element to read its properties) and **Audit** (run a battery of automated checks on the current screen and flag issues). Audit categories include hit-region size, contrast (which is approximate — relies on rendered pixels), label presence, dynamic type response, element overlap.

The major addition in Xcode 15 / iOS 17 (WWDC 2023 session 10035 "Perform accessibility audits for your app") is `XCUIApplication.performAccessibilityAudit()` — runnable from a unit test, producing `XCUIAccessibilityAuditIssue` objects with categories you can assert against:

```swift
try app.performAccessibilityAudit(for: [.contrast, .dynamicType, .elementDetection, .hitRegion, .sufficientElementDescription, .trait]) { issue in
    return shouldIgnore(issue) // return true to suppress
}
```

This is the first credible CI hook for iOS accessibility, and the right place to enforce a regression bar. It catches a known subset (mostly geometric and naming), not the full WCAG surface — it does not test focus order, custom actions, announcement appropriateness, or screen-reader experience holistically.

### SwiftUI accessibility previews

SwiftUI's preview system can render in any Dynamic Type size (`.previewLayout`, `.environment(\.dynamicTypeSize, .accessibility5)`), in dark mode, with Increase Contrast, and with `.environment(\.accessibilityReduceMotion, true)`. The Accessibility Inspector pane in Xcode preview (Xcode 15+) shows the resolved label/value/traits per element — useful for catching missing labels at design-review time.

`.accessibilityRepresentation` works in previews and the Inspector will show the represented element rather than the rendered one, which is the right behaviour for verifying that a custom-drawn control reads as its semantic equivalent.

### Manual testing — the irreplaceable layer

Automated audits flag the cheap classes of bug. Conformance to WCAG 2.2 AA requires manual verification of:

- **VoiceOver flow** on a real device with the screen actually off (or screen-curtain enabled). Headphones on, eyes closed for at least one major flow.
- **Voice Control** ("Show numbers", "Show grid", named control invocation) — verifies labels are usable as voice commands and that `.accessibilityInputLabels` covers synonym needs.
- **Switch Control** — at minimum verify group navigation makes sense and custom actions are reachable.
- **Full Keyboard Access on iPad** — Tab order, custom focus rings on non-default styled controls, Esc / Cmd-W / Cmd-, behaviour.
- **Dynamic Type at AX5** — every screen, no exceptions, on the narrowest target device.
- **Smart Invert + Dark mode + Increase Contrast** — at least a spot check.

### Evidence for ACR / VPAT

What audits can generate as evidence:

- Pass/fail per `performAccessibilityAudit` category, per screen, dated.
- Inspector audit summaries (exportable as Markdown / PDF reports).
- Test-run videos with VoiceOver overlay (Settings → Accessibility → VoiceOver → Captions Panel for transcript).
- XCUITest results showing element labels and identifiers, demonstrating that programmatic identification (WCAG 4.1.2) is in place.

What audits cannot establish:

- Subjective quality of announcements (1.3.1, 4.1.3 require judgment).
- Focus order correctness (2.4.3) beyond geometric.
- Whether custom actions cover all gesture paths (2.5.1, 2.5.7).
- Whether colour-only signaling is supplemented (1.4.1) — automated contrast can flag but not confirm meaningfulness.
- Whether announcements at the right semantic moment (status vs. screen change).

This map is what to put in the test plan that accompanies the VPAT: "for these criteria, we run `performAccessibilityAudit`; for these, manual VoiceOver pass on listed devices; for these, structured review of design tokens and code."

---

## 8. The Figma annotation contract

Given everything above, here's the minimum a designer must specify in Figma for an iOS engineer to implement without guessing. The contract is per-element; not every element needs every field, but when a field is needed and missing, the engineer guesses.

### Per-element annotations

**Accessible name.** The text VoiceOver / Voice Control will speak. Required when:
- The visible label is an icon (no surrounding text).
- The label is decorative or visually abbreviated ("→", "•••").
- The same component appears multiple times with the same visible label and disambiguation is needed ("Delete *Project Atlas*").
When the visible text *is* the accessible name (a button labelled "Save"), the framework default is correct and the annotation can say "name: visible label". Make this the explicit default convention so silence in the annotation means "use the visible label".

**Role / traits.** The semantic kind of element: button, link, header, tab, toggle, search field, adjustable (slider/stepper). Engineers know what `Button` and `Toggle` are; the load-bearing annotations are:
- "treat as button" on a non-button-shaped tappable surface (a `VStack` with `.onTapGesture`).
- "treat as header" on visually-bold-but-not-actually-a-header text that *should* be a header in the rotor.
- "treat as adjustable" on a custom slider.
- "link, not button" when the tap exits the app or opens a web URL.
SwiftUI's `Button` and UIKit's `UIButton` carry `.isButton` automatically. Annotate only when the element is *not* the obvious framework primitive.

**State.** The current value or selection. Three cases:
- **Selected / unselected** — for toggles, segmented controls, tabs, list selection. Required if the visual state is the only signal.
- **Expanded / collapsed** — for disclosure rows, accordions. The framework does not annotate this automatically; specify which trait (`.isSelected`, custom trait combined with value) and what the announcement reads ("Expanded" / "Collapsed").
- **Validation / error state** — required state, error state, focus state. Annotate the relationship: "error text is part of the field's accessibility value" vs. "error is announced as a status message on appearance".

**Traversal order.** The VoiceOver swipe order through the screen, numbered. Required when:
- The geometric order is wrong (visually-overlapping elements, popovers, custom layouts where a logical group spans rows).
- A group of elements should be flattened into a single stop (a card, a row, a toolbar). Annotate the *grouping* and the *combined label*.
- Z-ordered elements (FABs, toasts) need a defined position in the order.
Where geometric order is correct (a vertical stack of controls), state "default order" and move on.

**Dynamic Type behaviour.** Per surface, specify:
- **Scales freely up to AX5**, with reflow direction (horizontal pair becomes vertical at AX1+, etc.).
- **Scales freely, no reflow needed** — for plain text blocks.
- **Caps at AX-N** with explicit justification (the navigation bar, the marketing splash). Engineers must implement the cap explicitly; this is not the default.
- **Specific Dynamic Type style** (`.body`, `.title3`, `.caption`) — required when token-to-style mapping isn't obvious. Tie this to the type token in the design system.

**Behaviour under Smart Invert.** Per image / non-text element:
- **Inverts** (default for UI chrome) — no annotation needed.
- **Does not invert** (photographic content, brand-coloured marks) — annotate "ignore invert colors". This produces `accessibilityIgnoresInvertColors = true`.

**Behaviour under Increase Contrast.** Per surface that uses colour or transparency:
- **Standard variant** for default state.
- **Increased-contrast variant** for `accessibilityContrast == .increased`. Annotate the alternative tokens (typically a higher-contrast colour pair and reduced/removed transparency). If the design uses only semantic system colours and asset-catalog Increase Contrast variants, this can be a one-line system-level annotation rather than per-element.

**Reduce Motion behaviour.** Per animation / transition:
- **Always animate** — never; this is non-compliant.
- **Animate fully by default, cross-fade under Reduce Motion** — the most common case; annotate the fallback transition (opacity, no spring).
- **Skip entirely under Reduce Motion** — for parallax, large translations, decorative animation.
- **No animation** — no annotation needed.

**Gesture alternatives.** Per non-tap gesture:
- For **drag / swipe** (reorder, swipe-to-delete): specify the custom action label and what it does. Annotate where in the rotor it appears.
- For **long-press menus**: annotate "exposed as accessibility custom action `<verb-noun>`" if it's not a `.contextMenu` or `UIContextMenuInteraction`.
- For **pinch / rotate / pan**: annotate the button-based alternative (zoom in/out/reset).
- For **shake**: annotate the on-screen Undo button.

**Accessibility-announcement intent.** Per dynamic content change:
- **No announcement** — purely visual change (a hover affordance).
- **Polite announcement on appearance** ("Saved", "1 result") — annotate the string and that this is `.announcement` / `AccessibilityNotification.Announcement`.
- **Move focus to** (modal opening, navigation, content replaced) — annotate the target element and that this is `.screenChanged`.
- **Layout changed, focus optionally moved** (inline error appearing) — annotate `.layoutChanged` and the focus target if any.
- **Page change** — annotate `.pageScrolled` with the descriptor string ("Page N of M").

### Where defaults are load-bearing — and where annotation is load-bearing

**Defaults are right, annotation can be silent:**
- A `Button`, `Toggle`, `Picker`, `TextField`, `Slider` in either framework: role, value, activation behaviour are all correct out of the box.
- Tap target sized to a visible 44×44 pt button: hit area is the button's bounds.
- Text styled with system text styles in supported font: Dynamic Type scales for free.
- System colours (`Color.primary`, `UIColor.label`, named assets with all four variants): adapt to dark mode and Increase Contrast.

**Defaults are wrong or absent, annotation is load-bearing:**
- Any custom-drawn control (Shape, Canvas, custom `UIView`).
- Any tap-gesture-on-a-non-button surface.
- Any decorative icon next to a labelled control (must be hidden from AT).
- Any hit area smaller than the visual or smaller than 44×44 pt.
- Any non-standard reading order, especially across cards, rows, modals.
- Any modal whose initial focus should not be the framework default.
- Any inline error, loading state, or status banner that must be announced.
- Any drag / long-press / multi-finger / motion gesture.
- Any photograph or brand-coloured mark that must not invert.
- Any animation that should defer to Reduce Motion.
- Any text that uses a custom font and should still scale with Dynamic Type.
- Any text-with-icon pair that must reflow at AX sizes.
- Any container that should flatten into a single VoiceOver stop.

The shape of the contract, in other words: **the annotation describes the deltas from framework defaults**. If a design uses standard system controls, system colours, system text styles, default tap targets, default reading order, and no custom gestures or animations, the annotation footprint is small. The more custom the design, the more load-bearing the annotation — and the more an under-specified Figma file becomes a delivery risk.

---

## References

Apple primary sources:

- Apple Human Interface Guidelines — Accessibility. https://developer.apple.com/design/human-interface-guidelines/accessibility (consulted 2026; periodically revised in line with iOS releases).
- Apple Developer — Accessibility on iOS. https://developer.apple.com/accessibility/ios/
- Apple Developer — UIAccessibility. https://developer.apple.com/documentation/uikit/uiaccessibility
- Apple Developer — SwiftUI Accessibility. https://developer.apple.com/documentation/swiftui/view-accessibility
- Apple Developer — `UIAccessibility.Notification`. https://developer.apple.com/documentation/uikit/uiaccessibility/notification
- Apple Developer — `AccessibilityNotification.Announcement`. https://developer.apple.com/documentation/accessibility/accessibilitynotification/announcement
- Apple Developer — `UIFontMetrics` / Dynamic Type. https://developer.apple.com/documentation/uikit/uifontmetrics
- Apple Developer — `ScaledMetric`. https://developer.apple.com/documentation/swiftui/scaledmetric
- Apple Developer — Full Keyboard Access user guide. https://support.apple.com/en-us/HT212742
- Apple Developer — `XCUIApplication.performAccessibilityAudit(for:)`. https://developer.apple.com/documentation/xctest/xcuiapplication/performaccessibilityaudit

WWDC sessions (selected, dated):

- WWDC 2019, Session 254 — "Accessibility in SwiftUI". https://developer.apple.com/videos/play/wwdc2019/254/
- WWDC 2020, Session 10119 — "App accessibility for switch control". https://developer.apple.com/videos/play/wwdc2020/10119/
- WWDC 2021, Session 10119 — "SwiftUI Accessibility: Beyond the basics".
- WWDC 2022, Session 10153 — "Build accessible apps with SwiftUI and UIKit".
- WWDC 2023, Session 10035 — "Perform accessibility audits for your app" (introduces `performAccessibilityAudit`).
- WWDC 2023, Session 10036 — "Build accessible experiences in visionOS / iOS" (Announcement priorities introduced).
- WWDC 2024, Session 10073 — "Catch up on accessibility in SwiftUI".

W3C and standards:

- WCAG 2.2 Recommendation (W3C, October 2023). https://www.w3.org/TR/WCAG22/
- W3C — Mobile Accessibility: How WCAG 2.x and Other W3C/WAI Guidelines Apply to Mobile (Working Note). https://www.w3.org/TR/mobile-accessibility-mapping/
- W3C — WCAG2ICT.
- EN 301 549 v3.2.1 (European harmonised accessibility standard referencing WCAG 2.1 / 2.2).

Practitioner write-ups and reference apps:

- Rob Whitaker — *Developing Inclusive Mobile Apps*. (Apress, 2020.)
- Mobile A11y / `mobilea11y.com` — practitioner reference, iOS pattern catalogue.
- Daniel Devesa Derksen-Staats — *Developing Accessible iOS Apps* (Apress 2021); blog at https://www.devesa.es.
- Sommer Panage's accessibility talks (Twitter Mobile/Square engineering). 
- Apple's open-source sample code — Fruta, Food Truck, Backyard Birds (SwiftUI sample apps with reasonable but not exhaustive a11y).
- A11yWatch / Deque axe DevTools for Mobile — third-party automated scanners; treat as supplementary to `performAccessibilityAudit`.
- iA11y Slack community / iOS Accessibility GitHub topic — active practitioner discussion of FBs and workarounds.

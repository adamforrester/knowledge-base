# Mobile accessibility in React Native

A practitioner's reference for a senior design systems lead at a digital agency that ships React Native alongside native iOS, native Android, and Flutter. Covers React Native's accessibility prop surface, the iOS / Android behavioural divergence underneath it, the effect of the New Architecture (Fabric, TurboModules) on how accessibility is wired, and where Expo's managed surface differs from bare RN. Aimed at closing the gap between an architectural position on accessibility (pair tokens, ARIA encapsulation, four-layer model) and the implementation depth needed to ship a screen to WCAG 2.2 AA on a real device with real assistive tech.

Version baseline at time of writing (May 2026): React Native 0.79 (current stable), with the New Architecture on by default since 0.76 (October 2024). Expo SDK 53 (current stable). New Architecture defaults assumed unless explicitly noted. Where a behaviour depends on RN version, Expo SDK, or AT version (VoiceOver / TalkBack), it is dated inline.

---

## 1. The accessibility primitives React Native exposes

### The mental model: one prop API, two native trees

The thing to understand before anything else is that React Native does not implement its own accessibility tree. **Every accessibility prop on a `<View>` or `<Pressable>` is a translation layer to the underlying platform's accessibility API** — UIAccessibility on iOS, the AccessibilityNodeInfo / AccessibilityDelegate machinery on Android. The JS prop is the same; the runtime behaviour is whatever VoiceOver or TalkBack does with the resulting native node. This is the source of every behavioural divergence in this document.

Under the old (Paper) renderer, accessibility props were applied by mutating shadow views on the main thread after layout. Under Fabric (the New Architecture renderer, default since 0.76 in October 2024), the C++ shadow tree carries accessibility props as first-class state and applies them when the host view is mounted or updated. **The net effect for product engineers is that accessibility updates are more synchronous and more consistent under Fabric** — particularly around `accessibilityState` flipping mid-interaction, which under Paper occasionally lost announcements because the state change and the focus event raced. Fabric's synchronous commits make this race much rarer. It is not zero; TalkBack 14.x in particular still drops state announcements on rapidly-toggled `selected` states (see RN issue #43098 family, verified open as of early 2026).

TurboModules — the rewritten native module system, also default on the New Architecture — matters less directly for accessibility. The relevant TurboModule is `AccessibilityInfo`, which is now generated from a TypeScript spec and uses JSI rather than the bridge. The practical effect: `AccessibilityInfo.isScreenReaderEnabled()` and the related queries are now synchronous-callable from JS without a round-trip, which makes it tractable to branch render trees on AT state without flashing.

### The core prop surface

The props every RN developer working on accessibility will touch:

- `accessible` — boolean. When true on a `View`, the OS treats the view *and its descendants* as a single accessibility element. This is the grouping switch. It is implicitly true on `Pressable`, `Touchable*`, `Text` (iOS only — see below), `TextInput`, `Switch`, `Image` (with `accessible` set). Setting it on a parent View collapses children into a single focus stop with a single name — useful for card components, dangerous for anything with nested interactives.
- `accessibilityLabel` — the accessible name. Maps to `UIAccessibility.accessibilityLabel` (iOS) and `setContentDescription` (Android). Overrides whatever the OS would have computed (e.g., from `Text` children). Required wherever the visible label is missing, ambiguous, or icon-only.
- `accessibilityHint` — supplementary description of what happens when the element is activated. Maps cleanly to VoiceOver's hint. On Android there is no native equivalent; React Native appends the hint to the content description, which TalkBack reads after a pause if the user lingers on the element. The behaviour is approximately right but not identical.
- `accessibilityRole` — the role string. RN exposes a curated set (`button`, `link`, `image`, `header`, `search`, `summary`, `adjustable`, `imagebutton`, `keyboardkey`, `text`, `none`, `radio`, `radiogroup`, `tab`, `tablist`, `togglebutton`, `switch`, `checkbox`, `progressbar`, `scrollbar`, `spinbutton`, `menu`, `menuitem`, `menubar`, `combobox`, `alert`, `timer`, `toolbar`, `list`). The mapping to native traits is opinionated; not every role maps cleanly to both platforms. `adjustable` maps to UIAccessibilityTraitAdjustable on iOS (enabling the swipe-up / swipe-down gesture in VoiceOver) and to a `RangeInfo`-equipped node on Android. `header` becomes a heading trait on iOS and `AccessibilityNodeInfo.setHeading(true)` on Android. `summary` is iOS-only in any meaningful sense; on Android it has no visible effect.
- `accessibilityState` — an object of `{ disabled, selected, checked, busy, expanded }`. Maps to native traits/states. `checked` accepts `true | false | 'mixed'`. `busy` maps to `aria-busy`-ish behaviour: on Android it sets a busy state, on iOS it is approximated by an "in progress" trait. **Do not rely on `busy` alone for loading announcements** — it is inconsistent (see live regions, section 6).
- `accessibilityValue` — `{ min, max, now, text }`. Drives the adjustable trait's value reading. If `text` is provided, screen readers read that string verbatim; otherwise they compute "X of Y" from min/max/now. Required for any custom slider, stepper, or rating component built without using the `Slider` primitive.
- `accessibilityActions` + `onAccessibilityAction` — declarative custom AT gestures. RN exposes a fixed set of action names: `activate`, `increment`, `decrement`, `longpress`, `magicTap` (iOS-only — two-finger double-tap), `escape` (iOS-only — two-finger z-scrub). You can also define custom-named actions which surface in VoiceOver's rotor and TalkBack's local context menu. **This is the single most underused primitive in the RN a11y surface** — every drag, every swipe-to-dismiss, every long-press menu should have an accessibility action equivalent and almost none do in practice.
- `accessibilityElementsHidden` (iOS) and `importantForAccessibility` (Android) — siblings, not equivalents. `accessibilityElementsHidden={true}` hides the element and its subtree from VoiceOver. `importantForAccessibility="no-hide-descendants"` does the same on Android. `importantForAccessibility="no"` hides only the element itself, not descendants — there is no iOS equivalent for that distinction. To hide a subtree cross-platform, set both. RN does not provide a single `hidden` prop that does the right thing on both.
- `accessibilityViewIsModal` (iOS) — when true, VoiceOver ignores everything outside this view's subtree. There is no Android equivalent at the prop level; you have to use `importantForAccessibility="no-hide-descendants"` on every sibling subtree, or rely on `Modal` semantics.
- `accessibilityLiveRegion` (Android) — `'none' | 'polite' | 'assertive'`. Announces content changes within the region. There is no iOS prop equivalent — on iOS you use `AccessibilityInfo.announceForAccessibility` imperatively (see section 6).
- `accessibilityLanguage` (iOS) — BCP-47 language tag, tells VoiceOver to switch voices for this subtree. No Android prop equivalent; Android handles this via `setLanguage` on a SpannableString, which RN does not expose.
- `accessibilityIgnoresInvertColors` (iOS) — excludes a view from Smart Invert. Critical for photographic and brand imagery. No Android equivalent because Android's color inversion is implemented in the display compositor and cannot be opted out of per-view.

### What is automatic versus opt-in for built-in components

`Pressable` and the legacy `Touchable*` family auto-set `accessible={true}` and infer `accessibilityRole="button"` when given an `onPress`. **A `<View>` with `onTouchEnd` or `onResponderRelease` does not.** This is the most common RN a11y bug in the wild — engineers wire up tap handling on a View and end up with an invisible interactive that no screen reader announces. Use `Pressable`.

`Text` is always exposed as an accessibility element on iOS and is focusable by VoiceOver. **On Android, `Text` is not focusable by TalkBack by default** unless it has an `onPress` or is wrapped in an `accessible` View. This is an architectural choice in the Android view system: TextView is only an accessibility node if it has interaction. For static body copy this is usually fine; for headings and labels that you want TalkBack to land on, set `accessibilityRole="header"` (which makes the node focusable) or wrap in `accessible`.

`TextInput` is handled correctly out of the box: it exposes a `textfield` trait, the placeholder participates in the accessible name in the absence of a label, the keyboard type and autocomplete hints map to the platform's input semantics. The one trap: `placeholder` is not a label. Always provide an `accessibilityLabel` or a visible `<Text>` label associated by proximity in the visual layout.

`Switch` is the correctly-built case study: it maps to UISwitch on iOS and SwitchCompat on Android, both of which have full native accessibility wiring. The role, state, and value-change announcements all work without any developer intervention. **This is what a built-in primitive should look like**; almost every custom design system "toggle" component ships worse a11y than the platform default.

`FlatList` and `SectionList` expose list semantics on Android (the parent gets a CollectionInfo node, items get CollectionItemInfo). On iOS the list semantics are weaker — VoiceOver does not announce "row 3 of 12" the way it does for native UITableView. If list-position context matters to your AT users, you must supply it via `accessibilityLabel` ("Message 3 of 12: ...").

### Common RN-specific pitfalls

- **Nested Touchables.** A `Pressable` inside another `Pressable` produces two accessible elements that overlap. VoiceOver will land on the outer one and never reach the inner. The fix is structural: either flatten to one interactive, or set the outer `accessible={false}` and rely on the inner's semantics (but then the outer's `onPress` becomes inaccessible).
- **`accessible={true}` as a grouping pattern.** Setting `accessible={true}` on a View collapses descendants. This is what you want for a card with internal `<Text>` nodes that should read as one element. It is *not* what you want if the card has internal interactives — those become unreachable. The rule of thumb: group only leaf-level elements.
- **`accessibilityRole="text"` on Android is a no-op for body copy.** Don't use it as a hack to force TalkBack focus; use `accessibilityRole="header"` if it's a heading, or wrap in `accessible`.
- **`accessibilityLabel` overrides `Text` children silently.** A `<Pressable accessibilityLabel="Submit"><Text>Submit form</Text></Pressable>` will read as "Submit" — the inner text is discarded. This is a frequent source of stale labels when the visible text is updated but the prop is not.
- **`onPress` plus role mismatch.** A `Pressable` styled as a checkbox but left at the default `button` role will be announced as a button. Set `accessibilityRole="checkbox"` and `accessibilityState={{ checked }}` explicitly.

---

## 2. Focus and traversal

### Screen-reader swipe order

The default swipe order on both platforms follows the view hierarchy's geometric layout — top-to-bottom, leading-to-trailing. **There is no `tabIndex` equivalent in RN.** Order is determined by what the native accessibility tree reports, which is determined by JSX hierarchy plus absolute positioning. Two implications:

- Visual reordering with `position: 'absolute'` or `flexDirection: 'row-reverse'` can desync visual order from accessibility order. Always test the actual AT swipe sequence on both platforms — the iOS and Android hit-test heuristics differ subtly, especially for overlapping z-indices.
- Components that visually re-flow (a column on mobile that becomes a row on tablet) need to be JSX-reordered, not just style-reordered, to keep AT order matching visual order.

To override traversal:

- **Android.** `importantForAccessibility="no"` removes an element from traversal entirely; there is no native "put this element here in the order" API exposed by RN. To force a specific order you can use `accessibilityTraversalBefore` and `accessibilityTraversalAfter` props — these were added to RN in 0.71 (early 2023) and map to `setTraversalBefore` / `setTraversalAfter` on the AccessibilityNodeInfo. They are not widely known and have rough edges; they take view IDs (set via `nativeID`), and they only work on Android.
- **iOS.** The native API is `accessibilityElements` on a container view, where you pass an ordered array of subviews. **RN does not expose this directly.** The workaround is a third-party native module or — more commonly — restructuring JSX to match the desired order. There is a long-running issue (RN #14785, opened 2017, still open as of 2026) requesting first-class support. Practitioners route around this; large RN apps with complex z-stacked UIs (overlays, drag handles) typically write a thin native module to set `accessibilityElements` manually.

### Hardware keyboard support

iOS Full Keyboard Access landed in iOS 14 (2020) and matured through iOS 16. For a React Native view to participate, the underlying UIView must set `isAccessibilityElement` and respond to focus. RN's default views do this correctly for `Pressable` and `Touchable*`; custom-built interactives often don't. The relevant prop is `focusable={true}` on `Pressable`, which maps to `canBecomeFocused` on iOS and `setFocusable` on Android. **On iOS, `focusable` was effectively a TV-platform vestige until RN 0.73 (late 2023) made it apply to Full Keyboard Access as well.** Apps shipping RN < 0.73 still need workarounds.

Android keyboard focus has worked for longer (since the early Android days, via the View focus system) but RN historically routed around it. The `nextFocusUp`, `nextFocusDown`, `nextFocusLeft`, `nextFocusRight`, and `nextFocusForward` props on `Pressable` map directly to Android's nextFocusXxx system. These are accepted on iOS too as of RN 0.71 but only meaningful for TV / VisionOS / Full Keyboard Access scenarios. `hasTVPreferredFocus` is the original TV-platform prop and is now the canonical way to set initial focus on both TV-OS and (less commonly) on Full Keyboard Access.

The lineage to be aware of: **RN's hardware focus story is downstream of react-native-tvos.** Douglas Lowder's tvOS fork carried the focus engine for years; much of what shipped into mainline RN 0.71–0.73 for keyboard focus was retrofitted from that work. The behaviour is therefore TV-shaped — directional focus, with an emphasis on D-pad-like navigation — rather than a flat tab order. For most screens this is invisible; for screens with non-orthogonal layouts (overlays, floating buttons) you may find focus jumps in surprising directions.

### Switch Control and Switch Access

iOS Switch Control and Android Switch Access traverse the same accessibility tree as VoiceOver / TalkBack respectively. **If VoiceOver swipe order is right, Switch Control order is almost always right too.** The behavioural divergence is around grouping: Switch Control's "item mode" navigates by accessibility element, while "group mode" navigates by sibling groups, which respects `accessible={true}` containers. A card with `accessible={true}` and three internal items reads as one element in VoiceOver but as a four-item group in Switch Control. There is no RN prop to override this; the grouping is fixed by `accessible`.

### Modal trapping

`<Modal>` from `react-native` sets `accessibilityViewIsModal={true}` on iOS automatically. On Android, the underlying Dialog view stops accessibility traversal from reaching the views behind it (Android's window-level focus model handles this for you). The known iOS quirk: if your Modal is animated in from an off-screen position with a non-zero animation, VoiceOver may briefly focus the underlying screen before the modal applies. The fix is to call `AccessibilityInfo.setAccessibilityFocus(reactTag)` on the modal's first focusable element in the modal's `onShow` handler.

**Focus return after close is not automatic on either platform.** When the modal dismisses, VoiceOver / TalkBack focus jumps to wherever the layout-engine puts it, which is usually the top of the screen. To return focus to the trigger element you must save a ref to the trigger before opening, then call `AccessibilityInfo.setAccessibilityFocus` on its node-handle after dismiss. This is rote work that every modal-using RN app re-implements; there is no library standard.

### Programmatic focus

`AccessibilityInfo.setAccessibilityFocus(reactTag)` moves AT focus to a specific element. The reactTag comes from `findNodeHandle(ref.current)`. **The timing is fragile**: call it too early (before the view is laid out) and it no-ops silently. The reliable pattern is to call it in an `InteractionManager.runAfterInteractions` or, more pragmatically, with a short `setTimeout(..., 100)` after the view becomes visible. On Android, the analogous API was previously `sendAccessibilityEvent` with `TYPE_VIEW_ACCESSIBILITY_FOCUSED`; RN unified these under `setAccessibilityFocus` from 0.66 onward. The cross-platform behaviour is now consistent at the API level but timing-sensitive.

---

## 3. Text scaling and reflow

### The two prop surfaces

RN exposes `allowFontScaling` (boolean, default `true`) and `maxFontSizeMultiplier` (number, default no cap) on `Text` and `TextInput`. Both can be set globally by mutating the static defaults: `Text.defaultProps = { ...Text.defaultProps, maxFontSizeMultiplier: 1.5 }`. **Almost every team caps scaling somewhere — and almost every cap is wrong.** A 1.5× cap fails WCAG 1.4.4 (text resize to 200%); a no-cap policy breaks layouts at iOS's 310% AX5 setting. The defensible position is no cap on body copy and headlines, a cap (around 1.3×) only on numeric labels in space-constrained UI (badges, tab labels), and a cap *never* applied silently — it must be a deliberate per-component decision.

### The platform divergence

iOS Dynamic Type has eleven steps (xSmall, Small, Medium, Large, xLarge, xxLarge, xxxLarge, plus five accessibility sizes AX1–AX5). The scaling factor at AX5 is approximately 3.1× the base size. **iOS Dynamic Type scaling is applied automatically by UIKit** when the underlying text uses `preferredFont(forTextStyle:)`. RN does not by default — RN's text scaling reads the system content size category and applies a multiplier, but it does not map text styles to Apple's semantic styles (`body`, `headline`, `footnote`, etc.). The effect: an RN app responds to Dynamic Type but does not get Apple's curated scaling curve. For most apps this is fine; for apps targeting accessibility-first iOS users, the curve mismatch is visible.

Android `fontScale` is a single multiplier from 0.85 to 1.30 in stock Android, but the OEM range can go higher (Samsung One UI exposes "Huge" at ~1.6×). Android applies fontScale to `sp` units automatically; RN font sizes are in unitless dp-equivalents that get scaled when `allowFontScaling` is on. Android does *not* have AX-tier sizes the way iOS does.

The implication for cross-platform design: **the maximum reasonable scaling target is iOS AX5 (~3.1×), not Android fontScale 1.3×.** Designing for AX5 means designing for the Android case for free; designing only for 200% leaves AX users on iOS with broken layouts.

### What breaks at large scale

- **Fixed-height containers.** Buttons with `height: 44` clip ascenders at 200%+. Use `minHeight` and let the container grow.
- **Icon + text pairs.** Icons at fixed sizes look stunted next to 3× text. Either scale icons proportionally with `PixelRatio.getFontScale()` (or `useWindowDimensions`'s `fontScale`) or commit to fixed-size icons and design for that.
- **Truncation.** `numberOfLines={1}` on a header that exceeds the viewport at AX5 produces an ellipsis where the design wanted reflow. The accessibility-correct default is `numberOfLines={undefined}` and a layout that reflows.
- **Tab bars and bottom navigation.** Text labels at AX5 don't fit in a tab bar. The native iOS behaviour is to switch tab bars to a vertical layout at large sizes; RN's typical custom bottom-tab implementations don't do this. Either commit to icon-only tabs at large scale (with `accessibilityLabel` providing the name) or implement the vertical fallback.
- **`TextInput` with fixed width.** Form fields styled at fixed pixel widths overflow horizontally at large scale. Use percentage or flex widths.

`PixelRatio.getFontScale()` is the canonical way to read the user's font-scale preference from JS. Use it for sizing things that aren't text (icons, spacing in text-adjacent contexts) but should grow with text — not just for text itself, which scales automatically.

---

## 4. System contrast, color, and motion preferences

### The AccessibilityInfo query surface

The cross-platform queries on `AccessibilityInfo`:

- `isScreenReaderEnabled` — VoiceOver / TalkBack on. Both platforms.
- `isReduceMotionEnabled` — Both platforms. iOS reads "Reduce Motion"; Android reads "Remove animations" (the system-wide animation scale = 0, in effect).
- `isBoldTextEnabled` — Both platforms, though Android exposure has been less reliable historically (added properly in RN 0.65).
- `isGrayscaleEnabled` — iOS, Android (via system color filters since RN 0.68).
- `isReduceTransparencyEnabled` — iOS only. Android has no equivalent system setting.
- `isInvertColorsEnabled` — iOS only. Reflects "Classic Invert" specifically — Smart Invert is **not** queryable.
- `isHighTextContrastEnabled` — Android only. Reflects the "High contrast text" developer-options-tier setting.

Each has a matching event (`'change'` event on a per-flag basis via `addEventListener`). Subscribe at the root and propagate via context if you intend to branch render output on AT state.

### useColorScheme and dark mode interplay

`useColorScheme()` returns `'light' | 'dark' | null` and updates reactively. Dark mode is not strictly an accessibility feature, but it is the closest RN gets to a contrast-preference API. iOS and Android both implement it; there is no "high contrast theme" hook beyond Android's `isHighTextContrastEnabled`.

**RN has no equivalent to the CSS `prefers-contrast: more` media query**, which iOS exposes natively (Increase Contrast) and Android exposes via the high-text-contrast flag. For an iOS-correct "Increase Contrast" response, you have to write a small native module to read `UIAccessibility.isDarkerSystemColorsEnabled`. This is one of the most glaring gaps in the cross-platform a11y surface — practitioners ship native modules or simply ignore it. Expo's `expo-system-ui` does not cover this either, as of SDK 53.

### Smart Invert exclusion

Smart Invert (iOS, since iOS 11) inverts colors except for images and media. **It cannot be queried from RN.** The only thing you can do is mark specific views to be excluded from inversion entirely via `accessibilityIgnoresInvertColors={true}`. This works for Classic Invert; for Smart Invert, photographic content is excluded automatically by the OS when the underlying view is identified as an image. RN's `<Image>` does the right thing here; backgrounds with `ImageBackground` may not depending on how they're composited.

On Android, color inversion is a display-level filter applied in the compositor. There is no per-view exclusion API. The accessibility-correct response is to ensure your brand imagery still reads correctly inverted, which usually means avoiding inversion-fragile color combinations (red/green pairs) and committing to inversion-resilient marks.

### What you have to wire up

In aggregate, the RN team must wire:

- A root-level `AccessibilityProvider` that subscribes to the relevant `AccessibilityInfo` flags and provides them via context.
- A motion-token resolver that returns durations of zero when `isReduceMotionEnabled` is true. This must be applied to every `Animated`, `Reanimated`, `LayoutAnimation`, and `Easing` use site. There is no global "respect reduce motion" switch in RN's animation libraries — Reanimated 3.6+ added a `useReducedMotion` hook (verified in changelog, late 2023) but using it is opt-in.
- A theme resolver that branches on `useColorScheme()` for dark mode and on `isHighTextContrastEnabled` / `isBoldTextEnabled` for contrast-tier branches.
- Native modules (or a maintained library — `react-native-accessibility-engine` is one) to fill the gaps around iOS Increase Contrast, Differentiate Without Color, and other absent query APIs.

---

## 5. Tap targets, gestures, and input alternatives

### Minimum target enforcement

WCAG 2.5.5 (AAA) calls for 44×44 CSS px; WCAG 2.5.8 (AA, 2.2) calls for 24×24 with exceptions. Apple HIG calls for 44pt; Material calls for 48dp. **None of these are enforced by React Native at the component level.** A `Pressable` with `style={{ width: 16, height: 16 }}` is a 16-pixel tap target.

The recovery mechanism is `hitSlop` — an object `{ top, right, bottom, left }` that extends the touch region beyond the visual bounds without changing the layout box. `hitSlop={{ top: 12, right: 12, bottom: 12, left: 12 }}` on a 24px icon button produces a 48px effective target. This is the standard RN pattern. **The trap: hitSlop expands the *touch* region, but it does not change the *accessibility frame* on iOS or the *click bounds* on Android.** A user with low motor control finding the target by exploration with VoiceOver still gets the 24px frame. For a true accessible target, the visual or layout size must meet the threshold; hitSlop is a pointer-input affordance, not an accessibility one.

`Pressable`'s `pressRetentionOffset` is a related but different prop: it controls how far the user can drag *after* pressing before the press is canceled. Default 50dp on all sides. Tuning this matters for list items where the press should commit even if the user's finger drifts during the press; it is not an accessibility primitive.

### Gesture alternatives (WCAG 2.5.7, 2.5.4)

WCAG 2.5.7 requires that any drag operation has a non-drag alternative; 2.5.4 requires motion-actuated functions have a UI alternative. RN's surface for this:

- `accessibilityActions` + `onAccessibilityAction`. Declare custom actions and handle them. For a swipe-to-delete row, declare an `'activate'` for the row's primary action and a custom `{ name: 'delete', label: 'Delete' }` for the swipe action. VoiceOver surfaces these in the rotor; TalkBack surfaces them in the local context menu.
- `magicTap` (iOS only) — the two-finger double-tap, conventionally mapped to a screen's primary action (play/pause, answer call). Implement this on the screen's root view for screens with a clear primary action.
- `escape` (iOS only) — the two-finger Z-scrub, conventionally maps to dismiss. Implement on Modals.

**Almost no design system component library wires these up out of the box.** A `SwipeableListItem` component should ship with `accessibilityActions` for the swipe actions; very few do. This is a clear DS opportunity: encapsulate the AT alternative inside the same component that ships the gesture, so consumers cannot ship the gesture without the alternative.

For motion-actuated actions (shake to undo, tilt to scroll), the WCAG-correct response is to provide a UI button that does the same thing and to support disabling the motion gesture entirely. RN's surface here is `DeviceEventEmitter` and accelerometer / device-motion libraries; there is no a11y-specific prop. The DS-level guarantee is that any shake-to-X has a button-X next to it.

---

## 6. Live regions, announcements, and dynamic content

### Cross-platform asymmetry

This is the most painful corner of RN accessibility. **There is no single API that reliably announces a content change on both platforms.**

- **Android.** `accessibilityLiveRegion="polite"` or `"assertive"` on a `<View>` or `<Text>` causes TalkBack to announce content changes within that view as it updates. Reliable and idiomatic.
- **iOS.** No prop. The canonical API is `AccessibilityInfo.announceForAccessibility(message: string)` for fire-and-forget announcements, and `AccessibilityInfo.announceForAccessibilityWithOptions(message, { queue: boolean })` (added in RN 0.69, mid-2022) for queued announcements that respect VoiceOver's speech queue.

The cross-platform pattern that works:

```js
function announce(message) {
  if (Platform.OS === 'ios') {
    AccessibilityInfo.announceForAccessibilityWithOptions(message, { queue: true });
  } else {
    AccessibilityInfo.announceForAccessibility(message);
  }
}
```

Plus the corresponding `accessibilityLiveRegion` on Android-side views for content that updates passively (no imperative trigger).

### Reliability of announcements

VoiceOver routinely drops `announceForAccessibility` calls if VoiceOver is mid-utterance. The `queue: true` option helps but is not bulletproof. The empirical reliability hierarchy, from most to least reliable:

1. Focus moving to a new element with an accessible name (always announces).
2. Android `accessibilityLiveRegion` on a visible text node updating.
3. iOS `announceForAccessibilityWithOptions` with `queue: true`.
4. iOS `announceForAccessibility` without options.
5. `accessibilityState={{ busy: true }}` (inconsistent on both platforms).

For status messages where the announcement is essential (form-submit success, error toast), the most reliable pattern is to **move accessibility focus to the new element** rather than rely on announcement APIs. A toast that appears with `accessibilityLiveRegion="assertive"` and a programmatic `setAccessibilityFocus` on iOS achieves the best cross-platform reliability.

### Loading states

`accessibilityState={{ busy: true }}` is the declarative way to mark a region as loading. In practice it under-delivers — TalkBack often says nothing, VoiceOver says "loading" only when the user focuses the busy element. **A reliable loading announcement requires explicit `announceForAccessibility('Loading')` and `announceForAccessibility('Loaded')` calls** on transitions, or focus management onto a status element. Treat `busy` as a hint to AT, not a guarantee.

---

## 7. Testing, tooling, and conformance evidence

### Unit / component-level

`@testing-library/react-native` is the standard. The relevant queries:

- `getByRole('button', { name: 'Submit' })` — checks both role and name. Updated API since v11 (early 2023); older codebases will have `getByA11yRole` and `getByA11yLabel` separately. Both still work, but `getByRole` is the recommended path going forward.
- `getByA11yState({ checked: true })` — asserts on state object.
- `getByA11yValue({ now: 50 })` — asserts on adjustable values.
- `getByA11yHint`, `getByA11yLabel` — present but considered lower-confidence checks (name is the user-facing contract; label is one source of name).

These queries inspect the React tree's accessibility props, not the rendered native accessibility tree. **This is a limitation worth being clear about.** A test that passes `getByRole('button')` confirms that the prop is set; it does not confirm that VoiceOver or TalkBack will announce the element as a button. The prop-to-AT mapping is itself the contract being tested at the platform level, not at the JS level.

### End-to-end accessibility traversal

- **Detox** — RN's first-party-adjacent e2e framework. Supports accessibility-id matching (`by.id`) and partial label matching, but does not natively simulate VoiceOver / TalkBack traversal. You can drive the app via accessibility identifiers, but you cannot assert that "the screen-reader swipe order matches X." For that you fall to platform-level tooling.
- **Maestro** — newer, YAML-driven, less ceremony than Detox. Same fundamental limit: it drives via accessibility identifiers but does not simulate AT.
- **Appium** — does have an `accessibility_id` locator strategy and, on iOS, can use the XCUITest backend to inspect the accessibility tree the way Accessibility Inspector does. The most powerful and the most operationally heavy of the three.
- **iOS Accessibility Inspector** (Xcode) — required for any serious iOS conformance work. Audit tab catches missing labels, contrast issues, and small hit-targets in the running app. Use this on the actual built RN app, not just in unit tests.
- **Android Accessibility Scanner** (Google Play Store app) — equivalent for Android. Runs a one-shot audit on whatever's currently on screen.

### Lint coverage

`eslint-plugin-react-native-a11y` covers static lint rules for the prop surface — flagging `Pressable` without `accessibilityLabel`, role mismatches, etc. It is less comprehensive than `eslint-plugin-jsx-a11y` (the web equivalent) but worth the install. Maintenance has been slow; verify the plugin is keeping up with new RN prop additions (it lagged on `accessibilityActions` for ~18 months after RN exposed it).

### Manual testing

The non-negotiable parts of an RN accessibility test pass:

1. VoiceOver on a real iPhone, with the rotor. Swipe-traverse every screen; activate every interactive; check focus order, names, hints, state.
2. TalkBack on a real Android device. Same traversal, plus check `accessibilityLiveRegion` updates fire.
3. Dynamic Type at AX5 on iPhone; Android fontScale at 1.3× plus an OEM-extended scale (Samsung Huge if a Samsung device is in the fleet).
4. Switch Control on iPhone, item-mode and group-mode. Confirm every interactive is reachable.
5. Smart Invert on. Check no images / charts are inverted incorrectly.
6. Reduce Motion on. Verify animations are disabled or reduced.

Emulator / simulator testing is not sufficient — VoiceOver in the iOS Simulator has different behaviour to real-device VoiceOver, especially around rotor and announcements.

### Conformance evidence and the two-ACR question

A React Native app is one codebase shipping to two operating systems. **It produces two ACRs / VPATs, not one.** WCAG 2.2 itself is platform-agnostic, but the conformance claims are platform-specific because the AT environment is platform-specific: an SC 4.1.2 (Name, Role, Value) claim on iOS is about VoiceOver behaviour, on Android it's about TalkBack behaviour, and those are different runtimes.

Practically: one document, two columns ("iOS" and "Android"), or two documents with shared section numbering. The temptation is to claim "the React Native app conforms" — don't. The platform behaviours diverge enough (live regions, modal trapping, focus order, hint behaviour) that monolithic claims will fail audit.

What can be auto-evidenced:

- Component-level role/name/state assertions via testing-library tests.
- Lint coverage as a process check.
- iOS Accessibility Inspector audit reports and Android Accessibility Scanner reports per build (these can be CI-integrated; the Android one is harder to script than the iOS one).

What cannot be auto-evidenced:

- Live region announcement reliability (manual only).
- Cross-platform AT behaviour parity (manual only).
- Gesture alternative completeness (manual review against design).
- Conformance under user-selected accessibility preferences (manual matrix).

The honest position for an agency producing a VPAT for an RN app is that the automated evidence covers the structural conformance (SC 4.1.2 mostly, parts of 1.3.1) and that the behavioural conformance (1.3.4 orientation, 1.4.3 contrast in dynamic states, 2.1.x keyboard, 4.1.3 status messages) requires manual sign-off per platform.

---

## 8. The Figma annotation contract

This is the contract the practice needs the most. The question is: what must a designer specify in a Figma file so that an RN engineer can implement it without guessing — and what is safe to leave unspecified because RN's defaults handle it?

### Required for every interactive

- **Accessible name.** If different from the visible label, annotate it. Icon-only buttons must have a name. For text-with-icon buttons, the visible text is usually sufficient and no annotation is needed.
- **Role.** Only annotate when not the default. A `Pressable` with `onPress` defaults to `button`. Annotate when the component is a checkbox, switch, radio, tab, link, header, or adjustable. The role is identical on both platforms — one annotation covers both.
- **State.** When the component has states (`checked`, `selected`, `disabled`, `expanded`, `busy`), specify which states map to which native state. This is one annotation per state, cross-platform.
- **Value.** For any adjustable / slider / stepper / rating, specify min, max, current, and the value-text format ("$50" not "50"). The `accessibilityValue.text` annotation is essential whenever the numeric value isn't a useful announcement on its own.
- **Hint, if non-obvious.** Annotate only when the result of activation isn't conveyed by name + context. **Note that on Android the hint is appended to the label**, so a long hint pollutes the announcement; keep hints short ("Returns to the previous screen") and never put critical information in a hint.

### Required for every screen

- **Traversal order.** If the visual order does not match the JSX order, annotate the intended traversal sequence (numbered overlays in Figma work well). Call out where the order differs by platform — RN's Android `accessibilityTraversalBefore`/`After` is exposed; iOS requires a native module. If the order can't be guaranteed identical between platforms, the designer needs to know that.
- **Focus order on modal open / close.** Annotate which element should receive focus when the modal opens and which element should receive it on close. Both require explicit RN code; neither is automatic.
- **Live region intent.** For any region that updates dynamically — toast, status, loading, error — annotate whether the announcement should be `polite` or `assertive` (or "none"). On Android this becomes `accessibilityLiveRegion`; on iOS this becomes an `announceForAccessibility` call. Annotation covers both, but call out that iOS announcements are less reliable so essential messages must move focus.
- **Loading state semantics.** Distinguish "spinner is decorative, content will appear" from "this region is currently busy; announce loading." The former is `accessibilityElementsHidden` on the spinner; the latter is `accessibilityState={{ busy: true }}` plus an explicit announce-on-start / announce-on-end pair.

### Required for every component with motion or gesture

- **Reduce Motion behaviour.** For every animated transition, specify the reduced-motion alternative: instant snap, crossfade, or no animation at all. This is two design states, not one.
- **Gesture alternative.** For every drag, swipe, long-press, pinch, or motion-actuated action, specify the equivalent `accessibilityAction`'s name and label. If the action is destructive (delete-on-swipe), specify the confirmation flow under AT. Default annotation pattern: "Custom action: `delete` / 'Delete message'."

### Required for every component with text or color

- **Dynamic-type behaviour.** Specify the scaling cap (or "no cap"), reflow behaviour at AX5, and truncation policy. Annotate which dimensions are fixed vs. fluid. For numeric labels in tight space (badge counts, tab labels), specify a cap explicitly with reasoning.
- **Inversion / Smart Invert behaviour.** For brand imagery, photographic content, and color-meaningful UI (status colors, charts), annotate whether `accessibilityIgnoresInvertColors` is set. Default is `false`; specify `true` only where the inverted appearance would mislead.
- **High contrast / Bold Text behaviour.** Specify how typography responds to system bold text (usually: it just works because RN forwards the trait; sometimes custom fonts ignore it). For Increase Contrast on iOS, specify which color tokens shift (or document that the system has no Increase Contrast response and accept the SC 1.4.6 risk).

### Where to *not* annotate

- **Default Pressable / Touchable behaviour.** Don't annotate `accessible={true}` or `accessibilityRole="button"` on a Pressable with onPress — it's the default.
- **Switch, TextInput, standard FlatList.** The platform primitives handle role, state, and focus correctly. Annotate only when overriding.
- **Standard Text rendering.** Don't annotate fontScale on body copy; it scales automatically.
- **Hint where the name is self-describing.** "Submit" doesn't need "Submits the form" as a hint; it's redundant noise.

### Platform-divergence call-outs in annotations

The annotations that *must* call out platform divergence:

- **Hint behaviour.** iOS reads on lingering; Android appends to label. The annotation must note "iOS hint" if the team wants the iOS-only behaviour, otherwise expect Android to read it inline.
- **Live region.** Android-native via prop; iOS imperative announce. The annotation can be platform-neutral if the team agrees on the cross-platform helper; otherwise annotate the iOS announcement string separately.
- **Modal trapping.** iOS via `accessibilityViewIsModal`; Android via window-level. Same behavioural outcome; designer doesn't need to know unless the modal is non-standard (e.g., a half-sheet that isn't using `<Modal>`).
- **Traversal override.** Android possible declaratively; iOS requires native module. The designer should know if a layout requires an iOS native-module dependency to ship as designed.

The shape of the annotation library to build: **a Figma component set of accessibility annotation stamps, one per concern**, with platform divergence baked into the variants. A "Live Region" stamp with `polite | assertive | none` and a sub-note "iOS uses announceForAccessibility; ensure focus moves for critical." A "Custom Action" stamp with `name` and `label`. A "Reduce Motion" stamp with the reduced-motion variant attached. Used systematically, these compress the designer/developer contract into a small, learnable vocabulary that survives across products.

---

## References

Primary sources:

- React Native Accessibility docs — `https://reactnative.dev/docs/accessibility` (verified against 0.79, May 2026).
- React Native AccessibilityInfo docs — `https://reactnative.dev/docs/accessibilityinfo`.
- React Native New Architecture docs — `https://reactnative.dev/docs/the-new-architecture/landing-page` (Fabric / TurboModules rollout, default since 0.76, Oct 2024).
- Expo SDK 53 docs, specifically `expo-system-ui` and `expo-localization` — `https://docs.expo.dev/versions/v53.0.0/`.
- Apple Human Interface Guidelines — Accessibility — `https://developer.apple.com/design/human-interface-guidelines/accessibility`.
- Apple UIAccessibility programming guide — `https://developer.apple.com/documentation/uikit/accessibility_for_uikit`.
- Android Accessibility developer docs — `https://developer.android.com/guide/topics/ui/accessibility`.
- Android AccessibilityNodeInfo reference — `https://developer.android.com/reference/android/view/accessibility/AccessibilityNodeInfo`.
- WCAG 2.2 — `https://www.w3.org/TR/WCAG22/`.
- W3C Mobile Accessibility: How WCAG 2 and Other W3C Documents Apply — `https://www.w3.org/TR/mobile-accessibility-mapping/`.

React Native issues and PRs of interest (verify status before citing in published work):

- RN #14785 — Expose `accessibilityElements` on iOS (open since 2017).
- RN #43098 family — TalkBack state-change announcement drops on rapid toggles.
- RN #34424 — `accessibilityTraversalBefore` / `After` rollout (Android) — landed in 0.71.
- Reanimated `useReducedMotion` hook — added in Reanimated 3.6 (late 2023), confirm against current changelog.

Practitioner references:

- Catalin Miron, *React Native Accessibility* — practitioner blog series with platform-divergence write-ups.
- Formidable / Nearform engineering blogs on RN accessibility in production apps.
- Shopify's `restyle` and accessibility internals — referenced in Shopify engineering blog posts on Shop / Shop Pay RN modules.
- `eslint-plugin-react-native-a11y` — repo and rule docs.
- `react-native-accessibility-engine` — library for runtime accessibility assertions (verify maintenance status before adoption).

Tooling docs:

- Xcode Accessibility Inspector — `https://developer.apple.com/library/archive/documentation/Accessibility/Conceptual/AccessibilityMacOSX/OSXAXTestingApps.html`.
- Android Accessibility Scanner (Play Store).
- `@testing-library/react-native` queries — `https://callstack.github.io/react-native-testing-library/docs/api-queries`.
- Detox accessibility matchers — `https://wix.github.io/Detox/docs/api/matchers/`.
- Maestro accessibility commands — `https://maestro.mobile.dev/`.

Cross-references inside the vault:

- `14-accessibility.md` for the architectural model (four-layer, pair tokens, conformance reporting).
- `11-mobile-and-cross-platform.md` for the wider cross-platform stance (RN as one option alongside native and Flutter).
- `12-figma-practice.md` for the Figma annotation library precedent and the Code Connect / MCP context the annotation stamps fit into.

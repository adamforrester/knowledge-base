# Mobile accessibility in Jetpack Compose — Claude run

> Research output, May 2026. Companion document to the SwiftUI/UIKit, Flutter, and React Native runs of the same date. Intended audience: senior DS practitioner producing platform-implementation guidance and a Figma annotation contract. Compose version references target the Compose BOM `2026.01.xx` / Compose UI `1.8.x` (the line current at time of writing); Material 3 `1.4.x`; AndroidX Core `1.15.x`; minSdk assumed 24 unless stated. Where a primitive's behaviour shifted, the shift is dated.

---

## 1. The accessibility primitives Compose exposes

Compose's accessibility model is a tree of `SemanticsNode`s built in parallel with the composition tree. Every composable can contribute or modify semantics through `Modifier.semantics { }` (or its merging variant `Modifier.semantics(mergeDescendants = true) { }`). The compiler-driven nature of Compose means there is no opaque "view tag" you can interrogate — the semantics tree *is* the accessibility surface. Compose then translates that tree into `AccessibilityNodeInfo` objects on demand, driven by the platform `AccessibilityDelegate` installed on the host `AndroidComposeView`. TalkBack, Switch Access, Voice Access, and any other `AccessibilityService` consume those nodes through the standard Android pipeline. Mental model: **the SemanticsNode tree is to AssistiveTech what the LayoutNode tree is to the renderer** — independent, declarative, and recomposed.

**The core API surface.** `Modifier.semantics { ... }` accepts a `SemanticsPropertyReceiver` builder. Inside it you set `SemanticsProperties` — the canonical ones in `androidx.compose.ui.semantics.SemanticsProperties`:

- **`contentDescription`** — the accessible name when there is no visible text. Setting this on a node that *also* has a `text` property merges them (TalkBack reads both, usually badly); prefer one or the other.
- **`text`** / **`editableText`** — what TalkBack reads as the node's text content. `BasicText` sets this automatically; `TextField` sets `editableText`.
- **`role`** — `Role.Button`, `Role.Checkbox`, `Role.Switch`, `Role.RadioButton`, `Role.Tab`, `Role.Image`, `Role.DropdownList`. The role is announced by TalkBack ("Submit, Button. Double tap to activate.") and changes what gestures Switch Access exposes. **Compose has no `Role.Link`, no `Role.Heading`, no `Role.Slider` as of 1.8.x** — sliders are inferred from `ProgressBarRangeInfo` + `SemanticsActions.SetProgress`; headings use the `heading()` extension which sets an internal flag rather than a `Role`.
- **`stateDescription`** — overrides the platform-default state announcement. Use this when "checked / not checked" is wrong for your component (e.g. a toggle that means "on / off / auto"). Pair-token analogue: stateDescription is the *content layer*; toggleableState is the *semantic layer*.
- **`liveRegion`** — `LiveRegionMode.Polite` or `LiveRegionMode.Assertive`. Marks the node so changes to its text are announced without focus moving.
- **`heading()`** — flags a node as a heading so TalkBack's heading-navigation gesture can jump to it. There is no `headingLevel`; Compose has no h1/h2 distinction.
- **`paneTitle`** — for non-Activity screen regions that should be announced as "panes" when they appear (e.g. detail panes in two-pane layouts).
- **`testTag`** — a stable identifier used by Compose test rules. Not surfaced to TalkBack, but it leaks into `AccessibilityNodeInfo.viewIdResourceName` when `testTagsAsResourceId` is set on the semantics modifier — useful for UIAutomator-based E2E tests that also do a11y assertions.
- **`invisibleToUser()`** — removes the node from the semantics tree for AssistiveTech while keeping it visible visually. Use for visual-only badges that are already announced via a parent's contentDescription.
- **`error(message)`** — surfaces an error state on a `TextField` so TalkBack announces "Invalid entry, email format expected" rather than just the field name. The Material 3 `OutlinedTextField` does **not** wire this automatically from `isError = true`; you must set it.

**SemanticsActions** are how Compose tells AssistiveTech what verbs a node supports. The framework provides standard ones — `OnClick`, `OnLongClick`, `ScrollBy`, `PageUp`/`PageDown`, `Expand`, `Collapse`, `Dismiss`, `SetProgress`, `SetSelection`, `CopyText`, `PasteText`, `RequestFocus` — and a free-form `CustomAccessibilityActions` list. Standard actions wire into TalkBack's local context menu ("Actions" rotor) and into Switch Access's menu. Custom actions show up as labelled entries in the same menus. This is the only way to expose actions that aren't tap/long-tap to AssistiveTech.

**`mergeDescendants` vs. `clearAndSetSemantics`.**

- `mergeDescendants = true` says "treat me and everything under me as one accessible node". TalkBack focuses the parent once; the parent's announced text concatenates the descendants' text/contentDescription in tree order. This is the right default for compound widgets: a card with a title, body, and CTA chip should be one merged node, not three swipe stops.
- `clearAndSetSemantics { ... }` is more aggressive: it replaces descendants' semantics entirely with what you put in the lambda. Use it when descendants have semantics you actively don't want — e.g. a custom rating bar where each star is a clickable but you want the whole row announced as "Rating, three of five stars".

The two are not interchangeable. `mergeDescendants` is additive (parent absorbs children's semantics); `clearAndSetSemantics` is destructive (children are erased from the tree). A common pitfall: using `clearAndSetSemantics` on a button-with-icon and forgetting to put `role = Role.Button` and an `onClick` action back — the result is a non-actionable label.

**What's automatic in Material 3.** Material 3 (1.4.x) components ship with sensible defaults, but the surface is uneven:

- `Button`, `OutlinedButton`, `TextButton`, `FilledTonalButton`, `ElevatedButton` — set `Role.Button`, merge descendants, announce text content. *Automatic.*
- `IconButton` — sets `Role.Button` and `onClick`, but the `Icon` inside requires a `contentDescription`. Passing `contentDescription = null` to `Icon` marks it decorative; passing a string sets the accessible name. **The compiler does not warn if you pass `""` (empty string)** — this is a frequent silent failure.
- `Checkbox`, `Switch`, `RadioButton`, `TriStateCheckbox` — set role, `toggleableState`, and merge with the adjacent label *only if you use the `Row(Modifier.toggleable(...))` pattern*. A naive `Row { Checkbox(...); Text("Label") }` will produce two separate swipe stops and the label won't toggle on tap.
- `Slider`, `RangeSlider` — set `ProgressBarRangeInfo` and `SetProgress` action. TalkBack announces the value as a percentage by default; override with `stateDescription` to announce a unit ("4 hours").
- `TopAppBar`, `BottomAppBar`, `NavigationBar`, `NavigationRail`, `NavigationDrawer` — items merge correctly; the bar itself does not get a `paneTitle` automatically. Add one if the bar represents a region the user might navigate to.
- `AlertDialog`, `ModalBottomSheet`, `DatePicker`, `TimePicker` — modal scrim is enforced; focus moves into the dialog on open; on dismiss, focus returns to the launcher. (See §2 — there are caveats.)
- `LazyColumn`, `LazyRow`, `LazyVerticalGrid` — set scroll semantics automatically; items get correct positional info (`collectionInfo`) so TalkBack can announce "item 3 of 12".
- `Card`, `Surface`, `ListItem` — `ListItem` merges descendants; `Card` does not merge by default. If you build a tappable card from `Card { ... }` plus `Modifier.clickable`, you must add `mergeDescendants = true` or each child becomes its own swipe stop.

**Mental model for how the tree maps to AccessibilityNodeInfo.** Compose composes → builds a `SemanticsOwner` tree → on AT request, the `AndroidComposeViewAccessibilityDelegateCompat` walks the tree, prunes `invisibleToUser()` nodes, applies `mergeDescendants`, and emits `AccessibilityNodeInfo` objects with `className` derived from `Role`, `text`/`contentDescription` derived from semantics, `actions` derived from `SemanticsActions`. The mapping happens lazily and is cached; semantic changes trigger `notifyAccessibilityEvent` calls. There is no 1:1 between composables and nodes — many composables (e.g. `Spacer`, decorative `Box`) emit no semantics at all and are invisible to AT.

**Common pitfalls.**

- **Box + clickable, no role.** `Box(Modifier.clickable { })` is announced as "Double tap to activate" with no role. TalkBack users hear nothing about what they're activating. Always add `Modifier.semantics { role = Role.Button }` or use a `Button`.
- **contentDescription on decorative images.** Passing a non-null `contentDescription` to a decorative `Icon` or `Image` creates a swipe stop with no useful information. Use `null` (treated as decorative) explicitly.
- **Modifier order matters.** `Modifier.semantics { }.clickable { }` and `Modifier.clickable { }.semantics { }` produce different node structures — `clickable` injects its own semantics layer. The canonical order is **`clickable` first, `semantics` last** when overriding, because the later semantics modifier wins for conflicting properties.
- **State announcements lost on recomposition.** A node that announces a count ("5 unread") needs the count in its `contentDescription` *or* in a `liveRegion`-marked descendant. Just changing the visible text does not announce; TalkBack only re-reads when focus moves.
- **Merging too aggressively.** A long article with `mergeDescendants = true` at the root becomes a single 4000-word swipe stop. Merge at the *component* level, not the screen level.
- **Custom touch handlers with no semantics.** Drawing your own swipe-to-dismiss on a `Modifier.pointerInput { }` and forgetting `CustomAccessibilityActions` gives AT users no path to the action. See §5.

---

## 2. Focus and traversal

Compose has two distinct focus systems that occasionally collide: **input focus** (used by keyboards, D-pads, the TextField cursor) governed by `FocusRequester` / `FocusManager` / `Modifier.focusable` / `Modifier.focusRequester`, and **accessibility focus** (the green TalkBack rectangle, Switch Access highlight) governed by the semantics tree and the platform AT service. They are *not* the same thing. A node can have AT focus but not input focus, and vice versa.

**TalkBack swipe order.** Default traversal is geometric: top-to-bottom, then left-to-right (mirrored under RTL). Compose computes this from the laid-out bounds of each `SemanticsNode`. The order can go wrong in three common cases:

1. **Overlapping or staggered layouts** (e.g. cards with absolute offsets, Pinterest-style staggered grids) — geometric order produces visually surprising swipe sequences.
2. **Z-ordered content** — a sticky header drawn after the list still appears in the list's tree position, so it's announced after the list content rather than first.
3. **RTL with mixed-script content** — bidi runs occasionally invert in ways the geometric heuristic doesn't match.

**Overrides:**

- `Modifier.semantics { traversalIndex = -1f }` — lower indices come first within a traversal group. Negative values pull a node to the front. *Use sparingly* — it's a maintenance hazard at scale.
- `Modifier.semantics { isTraversalGroup = true }` — declares this node and its descendants as a group that traversal completes before moving on. Critical for things like cards in a grid: without it, TalkBack may swipe from card 1 title → card 2 title → card 1 body → card 2 body. With it, card 1 is completed before moving to card 2. **`isTraversalGroup` was renamed from `isContainer` in Compose UI 1.5; older docs and Stack Overflow answers still reference `isContainer`.**
- `Modifier.semantics { traversalIndex = X; isTraversalGroup = true }` together let you build named traversal regions (header / content / footer) and reorder them.

**Hardware keyboard support.** Anything users can tap with TalkBack should also be focusable by Tab/Shift-Tab/D-pad. Compose's `Modifier.focusable()` makes a node focusable; `Modifier.clickable { }` implicitly adds focusable + indication. **The big asymmetry**: `Modifier.semantics { onClick { } }` makes a node AT-actionable but **does not make it keyboard-focusable**. Many teams discover this when they ship a "custom button" that works with TalkBack but a Bluetooth-keyboard user can't reach it. Fix: also apply `Modifier.focusable()` or, better, `Modifier.clickable { }` (which gives you both).

`FocusRequester` is the imperative escape hatch for "move focus to this specific node now":

```kotlin
val firstFieldFocus = remember { FocusRequester() }
LaunchedEffect(Unit) { firstFieldFocus.requestFocus() }
// ...
TextField(modifier = Modifier.focusRequester(firstFieldFocus), ...)
```

`FocusManager` (from `LocalFocusManager.current`) provides `moveFocus(FocusDirection.Next)` etc. and `clearFocus()`. For multi-step forms, `KeyboardActions(onNext = { focusManager.moveFocus(FocusDirection.Down) })` is the idiomatic wiring.

**Switch Access** uses the same semantics tree as TalkBack but with different gestures (linear scan via single-switch, or row/column scan via two-switch). Critical implication: every meaningful action — including non-tap ones like "delete this row" via swipe — must be reachable via a `SemanticsAction` (either standard or `CustomAccessibilityActions`). A swipe-to-dismiss without a custom action is invisible to Switch Access users. This is the most-violated WCAG 2.5.7 (Dragging Movements, WCAG 2.2 AA) requirement in mobile work.

**Modal trapping.** `Dialog`, `AlertDialog`, `ModalBottomSheet`, `BasicAlertDialog` all implement focus trapping at the AT layer — TalkBack swipe will not escape the modal scrim, and Switch Access scan is constrained. Compose 1.6+ also handles **initial focus** for `AlertDialog` (focus lands on the dialog content, typically the first focusable). For custom modals built from `Popup` or `Surface`, **focus trapping is not automatic** — you must:

1. Set `Modifier.semantics { isTraversalGroup = true; paneTitle = "..." }` on the modal root.
2. Use `BackHandler` to intercept back-press for dismissal.
3. Save the previously-focused node and restore on dismiss via `FocusRequester`.
4. Optionally call `Modifier.focusGroup()` to constrain hardware-keyboard tabbing.

**Focus return after dismiss.** Material 3 dialogs return focus to the launcher correctly as of `material3:1.2.0` (Feb 2024); bottom sheets returned focus inconsistently until `material3:1.3.0`. For long-lived bugs, verify against issuetracker.google.com — search component:"Jetpack Compose - UI" with keyword "focus return".

**Compose Navigation and accessibility.** `NavHost` does not automatically announce destination changes. When a user navigates from List to Detail, TalkBack stays silent unless the new screen sets a `paneTitle` on its root (which then announces "Detail pane shown"). For full-screen navigation, the idiomatic fix is:

```kotlin
Column(Modifier.semantics { paneTitle = stringResource(R.string.detail_title) }) { ... }
```

There is no Compose-native equivalent of UIKit's `UIAccessibility.post(notification: .screenChanged)`. The pane-title mechanism is the closest substitute and behaves correctly with TalkBack as of Compose UI 1.6.

---

## 3. Text scaling and reflow

Android exposes two independent user-controlled scaling axes: **fontScale** (Settings → Display → Font size, 0.85x–2.0x in stock Android; some OEMs go to 2.5x) and **display density / display size** (Settings → Display → Display size, which scales `dp` itself). Compose respects both by default — `sp` is multiplied by `fontScale * density`, `dp` is multiplied by `density` only. **Mixing them is the single most common bug**: any text rendered in `dp`-derived sizing (e.g. hard-coded line heights, fixed `Modifier.height(20.dp)` on text containers) freezes at 100% font scaling, clipping content the moment a user enlarges text.

**What breaks at 200%+.**

- **Fixed-height rows.** `Modifier.height(48.dp)` on a row containing text will clip the second line. Use `Modifier.heightIn(min = 48.dp)` or just let the content drive height.
- **Single-line truncation.** `Text(..., maxLines = 1, overflow = TextOverflow.Ellipsis)` at default font size shows "Submit application", at 200% shows "Subm…". For tappable controls this fails WCAG 1.4.4 (Resize Text).
- **Icon-with-text pairs.** Toolbar buttons with a 24dp icon and 12sp label often have the icon centred vertically against a fixed-height bar. At large scales, the label wraps below the icon (which Compose does correctly if you use `Column`) but the bar height was fixed.
- **Horizontal layouts with tight spacing.** Tab rows, segmented controls — at 200%, labels overlap or wrap mid-word. Material 3's `ScrollableTabRow` handles this; `TabRow` (fixed) does not.
- **Bottom navigation labels.** Material 3 `NavigationBar` wraps labels to two lines silently and crops the third. Test with German strings + 200% scaling — this is where most production builds break.

**What Compose gives you to fix it.**

- **`sp` for everything text-like.** Including line height: `lineHeight = 24.sp`, not `24.dp`. The compiler does not enforce this; Lint has a rule (`SpUsage`) that warns on `Text(fontSize = 14.dp)`.
- **`nonScaledSp` and `TextUnit.fontScaleConverter`** — Compose UI 1.6 (Jan 2024) introduced non-linear font scaling on Android 14+ to prevent runaway growth on already-large fonts. Material 3 typography opts in by default; custom typography does too if you use `TextStyle(fontSize = X.sp)`. To opt *out* (e.g. for a logo) use `fontSize = TextUnit(14f, TextUnitType.Sp)` with the legacy linear path or wrap in a `CompositionLocalProvider(LocalDensity provides ...)`.
- **`Modifier.heightIn(min = ...)`** for tap targets — sets a minimum without freezing growth.
- **`BoxWithConstraints`** for responsive layouts that need to know the scaled size at composition time.
- **`AnnotatedString` with inline content** for icon-in-text — the inline icon scales with the text.

**Verification path.** Set Settings → Display → Font size to maximum and Settings → Display → Display size to maximum *simultaneously*. The combined scaling factor is often 2.5–3x and is where most regressions surface. The Android Studio Layout Inspector → Configuration variants → Font scale dropdown supports preview-time testing in Compose Previews via `@Preview(fontScale = 2.0f)`.

---

## 4. System contrast, color, and motion preferences

**Dark mode.** `isSystemInDarkTheme()` reads `Configuration.uiMode`. Material 3's `MaterialTheme(colorScheme = if (darkTheme) darkColorScheme() else lightColorScheme())` is the idiomatic wiring. **Dynamic color** (Material You, Android 12+) pulls a wallpaper-derived palette via `dynamicLightColorScheme(LocalContext.current)` / `dynamicDarkColorScheme`. Dynamic color does *not* guarantee WCAG contrast against your tokens — it derives a tonal palette but does not solve "body text on container has 3.8:1 ratio". You must test with the system colour-extractor's worst-case wallpapers.

**High-contrast text.** `Settings.Secure.getInt(resolver, "high_text_contrast_enabled", 0)` exposes the user's preference. **Compose has no first-class API for this** as of UI 1.8 — you read it via `LocalContext.current` or build a wrapper composable. When set, the canonical response is to ensure all body text hits 7:1 (WCAG AAA) against its background and to thicken outlines on form controls. Material 3 does not adjust its tokens automatically; this is a system-integration gap that practitioners work around with a `LocalHighContrastEnabled` composition local. Track resolution via the Compose issue tracker — issue `b/186859272` and follow-ons.

**Forced colors / colour inversion.** Android does not have a true equivalent of Windows' `forced-colors: active` (CSS Media Queries Level 5) or iOS's "Smart Invert" with `accessibilityIgnoresInvertColors`. What Android offers:

- **Colour inversion** (Settings → Accessibility → Colour inversion) — inverts the entire display including images. Compose has no opt-out at the framework level; for media that must not invert (logos, photos), the workaround is to render via a `SurfaceView` or set `View.setAccessibilityHeading` style flags that some OEMs respect, but coverage is patchy.
- **Colour correction / grayscale** — for users with colour-vision differences. Compose's behaviour here is "passive": if your tokens encode meaning via colour alone (e.g. green = pass, red = fail with no icon), the meaning is lost. WCAG 1.4.1 (Use of Color) is a design-time concern, not a Compose-runtime one.
- **Android 14 forced-dark** — `android:forceDarkAllowed="false"` in the manifest opts an Activity out of system-level forced dark; Compose components themed via Material 3 should set this to avoid double-inversion artefacts.

**Reduce motion equivalents.** Android exposes `Settings.Global.ANIMATOR_DURATION_SCALE`, `TRANSITION_ANIMATION_SCALE`, `WINDOW_ANIMATION_SCALE`. When the user sets "Remove animations" (Settings → Accessibility → Remove animations) all three go to 0. Compose's `Animatable`, `animate*AsState`, and `AnimatedVisibility` respect `AnimatorDurationScale` partially — finite durations are shortened, but custom physics-based animations (`spring()`) need explicit gating:

```kotlin
val context = LocalContext.current
val reduceMotion = remember {
    Settings.Global.getFloat(context.contentResolver,
        Settings.Global.ANIMATOR_DURATION_SCALE, 1f) == 0f
}
```

There is no `LocalReduceMotion` composition local in Compose UI 1.8; this is an ecosystem gap. Accompanist had a draft proposal; it stalled. Most production teams build their own `ReduceMotionAware` wrapper around `AnimatedVisibility`.

**Where Material 3 helps and where it doesn't.**

- **Helps**: dark theme via `darkColorScheme`, dynamic colour, ripple disabled when animations disabled (since `material3:1.2.0`), tonal elevation respects dark mode.
- **Doesn't**: high-contrast text override, colour-inversion opt-outs, reduce-motion gating for `Snackbar` swipe animation, decorative motion in `LinearProgressIndicator(indeterminate = true)` (it keeps moving regardless of system setting — `b/239482977`-class issue).

---

## 5. Tap targets, gestures, and input alternatives

**Minimum touch target.** WCAG 2.5.5 (AAA) requires 44×44 CSS px; WCAG 2.5.8 (AA, new in 2.2) requires 24×24 CSS px. Material 3 enforces **48×48 dp** as a hard minimum via `LocalMinimumInteractiveComponentSize` (renamed from `LocalMinimumTouchTargetEnforcement` in `material3:1.2.0`, Feb 2024). All Material 3 interactive components — `IconButton`, `Checkbox`, `Switch`, `RadioButton`, `Slider` thumb — expand their *touch* bounds to 48dp even when their visual bounds are smaller. The visual size remains as designed; only the hit region grows. This is invisible to AT but real for finger input.

**Opting out.** `CompositionLocalProvider(LocalMinimumInteractiveComponentSize provides Dp.Unspecified) { ... }` disables enforcement. Practitioners do this for dense layouts (a 24dp dismiss "x" in a chip). **It is almost always wrong** — the WCAG 2.5.8 floor is 24×24 dp and most "dense" affordances drop below this if you disable enforcement. Reserve for cases where adjacent targets would overlap (e.g. side-by-side text decorations in a rich-text editor) and ensure spacing.

For custom components: do not rely on visual size. Use `Modifier.size(minimumInteractiveComponentSize)` from `androidx.compose.material3.tokens` if available, or `Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)`.

**Gesture alternatives — WCAG 2.5.7 (Dragging Movements) and 2.5.4 (Motion Actuation).**

WCAG 2.5.7 (new in 2.2 AA) requires that any functionality operated via a dragging movement also be operable via a single pointer click without dragging — unless dragging is essential (drawing, signature). In Compose terms, this means every `Modifier.draggable`, `Modifier.swipeable` (deprecated; replaced by `AnchoredDraggable`), every `SwipeToDismissBox`, every reorderable list, every long-press-to-drag must have a button alternative.

- **`SwipeToDismissBox`** (Material 3, `material3:1.2.0+`) handles swipe-to-delete in lists. It does **not** automatically expose a "Delete" action to AT; you must add a `CustomAccessibilityAction("Delete", action = { onDelete(); true })` via `Modifier.semantics`.
- **Reorderable lists** — there is no first-party Material 3 reorderable list as of `1.4.x`. Practitioners use `androidx.compose.foundation` with `LazyColumn` + drag handles, or external libraries (e.g. `sh.calvin.reorderable`). Either way, expose "Move up" / "Move down" custom actions; do not assume the drag handle alone is sufficient.
- **Pull-to-refresh** — Material 3 `PullToRefreshBox` requires a tap alternative. Common pattern: a refresh action in the top app bar that also triggers the refresh.

WCAG 2.5.4 (Motion Actuation) covers shake-to-undo and tilt-to-scroll. Compose has no built-in motion-actuated gestures; if a team adds one via `SensorManager`, an in-UI alternative is required.

**Custom accessibility actions.**

```kotlin
Modifier.semantics {
    customActions = listOf(
        CustomAccessibilityAction("Mark as read") { markRead(); true },
        CustomAccessibilityAction("Delete") { delete(); true },
        CustomAccessibilityAction("Archive") { archive(); true }
    )
}
```

These appear in TalkBack's local context menu (swipe up then right) and Switch Access's menu. The string label is the announcement — keep it short and verb-first. The boolean return value tells AT whether the action succeeded; `false` results in TalkBack saying "Unable to perform action". For scroll, expand/collapse, and dismiss — prefer the **standard** `SemanticsActions` (`scrollBy`, `expand`, `collapse`, `dismiss`) so AT can route them through standard gestures rather than the action menu.

---

## 6. Live regions, announcements, and dynamic content

**`SemanticsProperties.liveRegion`.** Setting `Modifier.semantics { liveRegion = LiveRegionMode.Polite }` on a node tells TalkBack to announce changes to that node's text without moving focus. `LiveRegionMode.Assertive` interrupts current speech. The mechanism is text-change-driven: TalkBack diffs the node's accessible text on recomposition and announces the new value.

**What works:**

- A snackbar/banner with `liveRegion = Polite` announces "Saved" without stealing focus.
- A counter that changes from "5 unread" to "6 unread" announces the new value.
- A status message ("Loading…" → "Loaded 12 results") announces transitions.

**What doesn't:**

- **Initial appearance.** A node that appears with text already in it does not announce — only *changes* to text are announced. Workaround: emit empty text first, then update on next composition.
- **Long text changes.** Very long live-region updates are throttled or truncated by TalkBack; chunk announcements.
- **Multiple simultaneous live regions** — TalkBack interleaves them unpredictably. Architect one canonical "status" live region per screen.

**`View.announceForAccessibility` and modernity.** The classic Android API `View.announceForAccessibility(CharSequence)` is **deprecated as of Android 16 (API 36)**, dated 2025, with the deprecation message recommending live regions instead. The rationale: announcements bypass the focus model, are unrecoverable (no way to repeat them), and don't survive the user navigating away and back. Compose teams still using it for "Saved!" toasts should migrate to a `liveRegion = Assertive` host composable.

**Compose's modern equivalent.** There is no `Modifier.announce(...)` API in Compose UI 1.8.x. The canonical pattern is a hidden live-region holder:

```kotlin
@Composable
fun AnnouncementHost(message: String) {
    Box(
        Modifier
            .size(1.dp)
            .semantics {
                liveRegion = LiveRegionMode.Polite
                contentDescription = message
                invisibleToUser() // wait — see note
            }
    )
}
```

Note: `invisibleToUser()` removes the node from the tree, which defeats the live region. The pattern instead uses a 1dp box with `liveRegion` set and minimal visual presence; clip via `Modifier.alpha(0f)` if needed, but understand that fully invisible (`alpha = 0f` *plus* not laid out) can be pruned by the platform. Test on a real device.

For one-shot announcements that need to fire outside recomposition (e.g. "Form submitted" after a network round-trip), the bridge to platform `View.announceForAccessibility` is still the practical option, with awareness it's deprecated. The Compose team has signalled an API is coming — track issue `b/239098947` and the `androidx.compose.ui.platform` package release notes.

**Loading and error states.**

- **Loading** — `LinearProgressIndicator` and `CircularProgressIndicator` expose `progressBarRangeInfo`. For indeterminate progress, AT announces "Loading" once on focus. Use a live region for "Loaded 12 of 50" updates.
- **Errors** — `TextField` with `isError = true` should also set `Modifier.semantics { error("Email is required") }` so TalkBack announces the error on focus rather than just "Edit box, invalid".
- **Form-level errors** — a banner at the top of a form that lists field errors should be a polite live region and should also be focused programmatically when it appears (via `FocusRequester`), so keyboard users land there.

---

## 7. Testing, tooling, and conformance evidence

**Compose test APIs.** `androidx.compose.ui.test` provides:

- `composeTestRule.onNodeWithContentDescription("Submit")`, `onNodeWithText`, `onNodeWithTag` — selectors.
- `assert(hasContentDescription(...))`, `assert(hasClickAction())`, `assert(hasRole(Role.Button))`, `assert(isToggleable())`, `assert(isOn())`.
- `SemanticsMatcher` for custom predicates: `SemanticsMatcher.expectValue(SemanticsProperties.LiveRegion, LiveRegionMode.Polite)`.
- `printToLog()` for dumping the semantics tree — invaluable when debugging "TalkBack reads the wrong thing".

These verify **structural** accessibility — that nodes have roles, names, states, actions — but they cannot verify that TalkBack *actually announces correctly*. A test that asserts `hasContentDescription("Submit")` will pass even if `clearAndSetSemantics` upstream wiped the role, making the announcement "Submit" rather than "Submit, button".

**Espresso / UIAutomator.** For end-to-end flows that mix Compose and Views, `UiAutomator` interrogates `AccessibilityNodeInfo` directly. Set `Modifier.semantics { testTagsAsResourceId = true }` at the screen root so `testTag("submit_button")` appears as `viewIdResourceName = "submit_button"`, which `UiAutomator` can query. This is the bridge between Compose semantics and the platform AT tree for E2E testing.

**Accessibility Scanner (Google app).** Runs heuristics on the live UI: contrast checks, touch-target size, missing labels, redundant descriptions. Useful as a quick sanity check; **not sufficient for conformance** — it doesn't test traversal, live regions, or custom actions. Run it as a smoke test, not as the audit.

**Android Studio integration.**

- **Layout Inspector** (Hedgehog/Iguana/Jellyfish 2024–2025) shows the semantics tree alongside the composition tree. Filter for "semantics" to see what AT sees.
- **Accessibility checks in instrumented tests** — `AccessibilityChecks.enable()` (from `accessibility-test-framework`) runs heuristics on every Espresso interaction. Wire it into your CI baseline.
- **Lint rules** — `ContentDescription`, `ClickableViewAccessibility`, `LabelFor`, `SpUsage`. Compose-specific lint coverage has grown but still misses common Compose pitfalls (missing role on clickable Box, empty contentDescription).

**Manual workflow on real devices.**

1. Enable TalkBack (Settings → Accessibility → TalkBack). Use a Pixel reference device — OEM skins (Samsung One UI, Xiaomi MIUI) sometimes intercept gestures differently.
2. Volume-up-and-down chord toggles TalkBack on/off — essential for fast iteration.
3. Navigate every screen with swipe-right and swipe-left only — verify traversal makes sense.
4. Enable "Speak passwords" off and "Audio focus" on to test in realistic conditions.
5. Repeat with Switch Access (USB keyboard plugged in, scan mode), then with Voice Access.
6. Repeat at 200% font scale and largest display size.
7. Repeat under dark mode and (if applicable) high-contrast text.

**ACR/VPAT evidence.** What the toolchain can produce:

- **Yes**: structural assertions (every interactive element has a name and role), automated contrast reports (via Accessibility Scanner CSV export or the Espresso a11y framework), test logs proving custom actions exist.
- **No**: experiential evidence that traversal is sensible, that live-region announcements are timely, that error messages are helpful. **Manual TalkBack walkthroughs with video capture remain the only credible evidence** for these — the engineering team running the audit, ideally alongside a screen-reader user. WCAG 2.2 SC 4.1.3 (Status Messages) is the prime example: there is no automated way to prove "the user knew the form was submitted".

For VPAT/ACR documents, structure evidence per success criterion: cite the test (automated or manual), the build version tested, the device/OS, and the assistive tech version. Compose UI version and Material 3 version both matter; Compose 1.6 → 1.7 → 1.8 each shipped accessibility fixes that change conformance posture.

---

## 8. The Figma annotation contract

Compose's defaults are good *for Material 3 components used canonically*. The annotation surface a designer must provide for a Compose engineer collapses sharply when the design is "Material 3 components composed in Material 3 patterns". It expands when the design is "custom layout, custom gestures, custom motion, brand typography overriding Material 3 type scale". The annotation contract below assumes a design system bridging both modes.

**For every interactive element, annotate:**

- **Accessible name.** If the visible text is the name, mark "name = visible text" — *no annotation required*, Compose handles this for Buttons, Tabs, ListItems, etc.
  - If the visible text differs from what should be announced (e.g. icon-only "X" → "Close"), annotate the explicit string.
  - If the name is composed dynamically ("Unread, 5 messages"), annotate the *template* with parameter slots.
- **Role.** If using a Material 3 component, annotate the component name (`M3.Button`, `M3.Switch`, `M3.TextField`) — role is implied. For custom-composed elements (e.g. a "card" that's actually a button), annotate the role explicitly: `role = Button` / `role = Tab` / `role = Heading`. Note where Compose lacks a role (`Link`, `Slider`-as-data-input) so the engineer knows to compose semantics manually.
- **State.** Annotate states the system must announce: checked/unchecked, expanded/collapsed, selected/unselected, busy/idle, error/valid. For non-binary states (e.g. a tri-state filter), supply the `stateDescription` strings explicitly. *Material 3 components handle binary states without annotation*; ternary states are always load-bearing annotations.
- **Traversal order.** Annotate only where geometric order is wrong — staggered grids, sticky elements, asymmetric two-column layouts. Most screens don't need this. When required, annotate as a numbered overlay AND name the traversal groups (e.g. "Header group", "Content group", "Footer group") so the engineer maps groups to `isTraversalGroup` directly.
- **Dynamic-type / fontScale behaviour.** This is the area where annotations are most often missing and most often load-bearing.
  - Annotate which text styles use the M3 type scale (no action) vs. custom type (engineer must verify scaling).
  - Annotate which elements must remain on one line vs. allowed to wrap. Default: allow wrap; explicit single-line is the annotation.
  - Annotate which containers must grow vertically with text. Default: grow; fixed-height is the load-bearing annotation.
  - Annotate behaviour at 200% scale for key screens (navigation, hero CTAs) — ideally provide a redline at 200%.
- **Behaviour under inversion / forced colors.** Compose has no automatic opt-out, so:
  - Annotate images/illustrations that must *not* invert (logos, brand photography) — engineer knows this requires a `SurfaceView` workaround or that the design must tolerate inversion.
  - Annotate where colour is the sole carrier of meaning (status pills, chart legends) — engineer must add an icon or label, not just rely on colour. This is design feedback, not engineering annotation.
- **Gesture alternative.** Required for any swipe, long-press-and-drag, reorder, or motion-actuated interaction. The annotation specifies the *button-or-menu alternative* (e.g. "Long-press card → opens action sheet with Move/Delete/Archive" — implemented as `CustomAccessibilityActions`). If you don't annotate, the engineer either guesses (variable quality) or omits (WCAG 2.5.7 fail).
- **Live-region intent.** Annotate dynamic regions with intent:
  - `live = Polite` for status updates, count changes, "Saved" confirmations.
  - `live = Assertive` only for errors that must interrupt (rare — over-use destroys the experience).
  - Specify what the *announcement string* should be — often different from the visible text ("Validation failed" rather than "✕ 3 errors").
- **Focus behaviour on entry.** For screens with an obvious first target (a form's first field, a modal's primary action), annotate "initial focus = this element". Engineer wires `FocusRequester`. Without annotation, focus lands on the first traversable node, which is usually the back button or app bar.

**Where Compose's defaults make annotation unnecessary:**

- M3 Button, IconButton (with `contentDescription` on the icon), Checkbox, Switch, RadioButton, Slider, TextField, TopAppBar with title, BottomSheet, AlertDialog — role, state, traversal, focus trapping, and minimum tap target are all automatic.
- LazyColumn / LazyRow with M3 ListItem children — collection info, traversal, scroll actions automatic.
- Material typography (display/headline/title/body/label) — fontScale handled.

**Where the defaults are wrong or absent — annotation is load-bearing:**

- Anything using a custom `Modifier.clickable` on a non-Material container (Box, Surface without role).
- Any non-text icon (always annotate `contentDescription` or "decorative").
- Any state that isn't binary (tri-state, custom step).
- Any traversal that isn't top-to-bottom-left-to-right.
- Any gesture beyond tap and standard scroll.
- Any colour-encoded meaning.
- Any dynamic content that updates without focus moving.
- Any modal not built from M3 Dialog/BottomSheet.
- Any motion that's load-bearing for understanding (an animation that conveys "moved to folder").

**Annotation packaging.** In Figma, the most durable shape we've seen is a per-frame "Accessibility" annotation layer with three columns: Element / Property / Value. Properties are drawn from the controlled vocabulary above (`accessibleName`, `role`, `state`, `traversalIndex`, `customActions`, `liveRegion`, `initialFocus`). The vocabulary maps 1:1 to Compose's `SemanticsProperties` — the goal is that an engineer can copy the value into the corresponding `Modifier.semantics { }` block without translation. Where the value diverges per platform (e.g. live-region semantics differ subtly on iOS), the annotation should call this out and the platform implementations should each consume the rows relevant to them. This is the seam the four-platform research set (Compose, SwiftUI/UIKit, Flutter, React Native) is designed to align.

---

## References

Primary sources (verified May 2026; URLs stable at time of writing):

- Android Developers — Accessibility in Compose: `https://developer.android.com/jetpack/compose/accessibility`
- Android Developers — Semantics in Compose: `https://developer.android.com/develop/ui/compose/accessibility/semantics`
- Android Developers — Custom accessibility actions: `https://developer.android.com/develop/ui/compose/accessibility/custom-actions`
- Android Developers — Focus in Compose: `https://developer.android.com/develop/ui/compose/touch-input/focus`
- Android Developers — Testing accessibility: `https://developer.android.com/develop/ui/compose/testing/accessibility`
- Material 3 (Compose) component reference: `https://developer.android.com/jetpack/compose/designsystems/material3`
- Material 3 spec — Accessibility: `https://m3.material.io/foundations/accessible-design/overview`
- Android Developers — TalkBack: `https://support.google.com/accessibility/android/answer/6283677`
- Android Developers — Accessibility Scanner: `https://support.google.com/accessibility/android/answer/6376570`
- Android Developers — Principles for improving app accessibility: `https://developer.android.com/guide/topics/ui/accessibility/principles`
- AndroidX release notes — Compose UI: `https://developer.android.com/jetpack/androidx/releases/compose-ui`
- AndroidX release notes — Compose Material 3: `https://developer.android.com/jetpack/androidx/releases/compose-material3`
- Non-linear font scaling (Android 14+): `https://developer.android.com/about/versions/14/features#non-linear-font-scaling`
- W3C — WCAG 2.2: `https://www.w3.org/TR/WCAG22/`
- W3C — Mobile Accessibility (WCAG2Mobile): `https://www.w3.org/TR/mobile-accessibility-mapping/`
- W3C — WAI Authoring Practices on focus and live regions: `https://www.w3.org/WAI/ARIA/apg/`
- Compose issue tracker: `https://issuetracker.google.com/issues?q=componentid:589987` (Jetpack Compose — UI)
- Reference apps: Google's `Now in Android` (`https://github.com/android/nowinandroid`) — semantics usage in production, accessibility test patterns. JetNews (`https://github.com/android/compose-samples`) — smaller-scale traversal and live-region examples.
- Practitioner write-ups: Jose Alcérreca, "Compose accessibility under the hood" (Android Developers Medium, 2023, revisited 2025); Chris Banes' blog on focus and traversal; Florina Muntenescu's talks at Droidcon (2023–2025) on semantics.

Version-dependent claims dated above:

- `LocalMinimumInteractiveComponentSize` rename: `material3:1.2.0` (Feb 2024).
- `isTraversalGroup` rename from `isContainer`: Compose UI 1.5 (mid-2023).
- Non-linear font scaling: Compose UI 1.6 (Jan 2024), runtime requires Android 14 (API 34).
- `View.announceForAccessibility` deprecation: Android 16 (API 36), 2025.
- BottomSheet focus return fix: `material3:1.3.0`.
- Compose BOM `2026.01.xx` / Compose UI `1.8.x` / Material 3 `1.4.x` as the reference line for this document.

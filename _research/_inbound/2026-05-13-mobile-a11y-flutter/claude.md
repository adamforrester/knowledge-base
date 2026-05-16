# Mobile accessibility implementation in Flutter

> Research note for the design systems practice. Companion to an earlier Claude run focused narrowly on Flutter screen-reader behaviour; this one widens the surface to the full mobile a11y stack — focus, text scaling, system inversions, motion, gestures, the annotation contract — at a depth a senior engineer or DS lead can act on. Flutter version baseline is the stable channel as of May 2026 (3.27.x / 3.29.x line); Dart 3.6+. Where the API has shifted recently I date the claim.

---

## 1. The accessibility primitives Flutter exposes

Flutter does not delegate accessibility to native widgets. The engine maintains a parallel **semantics tree** — a pruned, annotated mirror of the render tree — and pushes it across the platform channel to the OS accessibility services: TalkBack on Android (via `AccessibilityNodeProvider` on a `FlutterView`/`FlutterSurfaceView`), VoiceOver on iOS (via `UIAccessibility` on the `FlutterViewController`), and AT-SPI / AccessKit on desktop. The implication that every senior engineer needs to internalise: **there is no `UILabel` or `TextView` to introspect**. Whatever VoiceOver reads is whatever the semantics tree said. Empty or wrong semantics is invisible; there is no native fallback.

**The API surface.** Semantics are produced by `RenderObject.describeSemanticsConfiguration` and exposed to widget authors through the `Semantics` widget, which writes into a `SemanticsConfiguration`. The configuration's properties cluster into:

- **Identity and labelling**: `label`, `value`, `increasedValue`, `decreasedValue`, `hint`, `tooltip`, `identifier` (added 3.19, exposes a non-localised testing ID separate from `label`).
- **Role-ish flags**: `button`, `link`, `header`, `image`, `textField`, `slider`, `checked`, `selected`, `toggled`, `enabled`, `focused`, `inMutuallyExclusiveGroup`, `liveRegion`. Flutter does not have a free-form "role" string the way ARIA does; roles are a fixed enum of `SemanticsFlag`s that the engine translates into the platform's native trait/role on the other side. As of the Flutter 3.27 work on the new `SemanticsRole` API (landed late 2025, see `flutter/flutter#134701` and the `role:` parameter on `Semantics`), there is now an explicit role enum that more cleanly maps to AccessKit / TalkBack roles, but the flag-based traits still drive most behaviour.
- **Actions**: `onTap`, `onLongPress`, `onScrollLeft/Right/Up/Down`, `onIncrease`, `onDecrease`, `onCopy`, `onCut`, `onPaste`, `onDidGainAccessibilityFocus`, `onDidLoseAccessibilityFocus`, `onDismiss`, and an extensible `customSemanticsActions` map. Actions are how a screen-reader user invokes behaviour without the underlying gesture — see §5.
- **Structure**: `container`, `explicitChildNodes`, `excludeSemantics`, `mergeAllDescendantsIntoThisNode`, `scopesRoute`, `namesRoute`, `sortKey`.

**Automatic vs. opt-in.** Material and Cupertino widgets are mostly correctly semanticised out of the box. `ElevatedButton`, `TextButton`, `IconButton`, `Switch`, `Checkbox`, `Slider`, `TextField`, `AppBar`, `Tab`, `Chip`, `ListTile`, `BottomNavigationBar`, `NavigationRail`, `NavigationBar`, `Stepper`, `ExpansionTile` all set the right flag + label + action triplet. `Text` becomes a leaf semantics node automatically. `Image` and `Icon` honour their `semanticLabel` if provided — and crucially **do not become semantics nodes at all if you don't provide one**, which is the right default (decorative until proven otherwise) but trips engineers expecting an empty `alt`-equivalent. `Hero`, `AnimatedSwitcher`, and most layout primitives (`Padding`, `Column`, `Row`, `Stack`) are semantically transparent.

What you have to wire up yourself: anything built on `GestureDetector` or `InkWell` with no underlying Material widget; anything where the visible label and the accessible label diverge (icon-only buttons, badges, status indicators using colour); anything that aggregates several leaf nodes into one announcement; anything dynamic (live regions, error messages, loading state); and almost all of the `CustomPaint` / `Canvas` surface — pixels are inherently invisible to assistive tech.

**The mental model.** Three operations dominate day-to-day work:

1. **Add semantics** — wrap with `Semantics(label: …, button: true, onTap: …, child: …)`. Or, more often, use the `excludeFromSemantics: false` knob on a high-level widget.
2. **Merge semantics** — `MergeSemantics` collapses a subtree into a single node so the screen reader announces it as one item. Used for a `Row(children: [Icon, Text])` representing one button, or a card with title + subtitle + meta that should be read as one swipe stop.
3. **Suppress semantics** — `ExcludeSemantics` removes a subtree entirely. Used for purely decorative imagery, redundant overlays, or skeleton loaders.

`Semantics(container: true, explicitChildNodes: true)` is the escape hatch when the default flattening is wrong: it forces the framework to keep child nodes visible to AT rather than merging them up.

**Pitfalls specific to Flutter.**

- **`GestureDetector` is silent by default.** It does not produce a semantics node. A `GestureDetector` wrapping a `Container` with text is a tap target that VoiceOver doesn't know is tappable. Either use `InkWell`/`Material` button widgets, or wrap with `Semantics(button: true, onTap: …)`.
- **`Tooltip` adds a semantics hint but not a label.** Useful for IconButton-with-tooltip, but the tooltip text becomes a hint, not the accessible name.
- **`Visibility(visible: false)` keeps semantics by default** unless you also set `maintainSemantics: false`. The same applies to `Offstage` and `IgnorePointer` (which ignores pointers but not semantics — use `ExcludeSemantics` or `IgnorePointer(ignoring: true, child: ExcludeSemantics(...))`).
- **Custom widgets with `Listener` or raw pointer handling** never produce semantics. `Listener` is below `GestureDetector` in the stack and is purely a render-tree affordance.
- **`Text.rich` / `TextSpan` semantics.** Inline links built with `TextSpan(recognizer: TapGestureRecognizer())` produce no semantics action by default. Use `WidgetSpan` wrapping a `Semantics(link: true, …)` or the `MouseRegion`/`Link` widget. The `link` flag exists but is under-used.
- **`Hero` flights** can briefly produce duplicate semantics nodes during the animation — usually benign, occasionally produces a stutter announcement.
- **`Scrollable` regions inside non-scrollable parents** sometimes get their scroll actions stripped if a parent overrides semantics. Watch for missing "swipe up to scroll" affordances in TalkBack inside complex sheets.
- **`SliverAppBar` collapse state** does not announce — engineers must wire a `Semantics(value: …)` if the collapse is semantically meaningful (e.g. a search field appearing on scroll).

---

## 2. Focus and traversal

Flutter has two distinct focus systems that engineers routinely conflate: **input focus** (keyboard / D-pad, governed by `FocusNode`, `FocusScope`, `FocusTraversalPolicy`) and **accessibility focus** (the screen reader's reading cursor, governed by the semantics tree's traversal order and `SortKey`s). They overlap but are not the same — TalkBack can swipe to a node that does not have keyboard focus, and the focused `TextField` is not necessarily the one the screen reader is reading.

**Screen-reader traversal order.** By default the semantics tree is walked in **paint order**, top-to-bottom, left-to-right (right-to-left in RTL locales, automatically). For grid- or stack-based layouts where paint order doesn't match reading order — e.g. a `Stack` where a badge is painted last but should be read mid-card — wrap nodes with `Semantics(sortKey: OrdinalSortKey(n))`. Within a sibling group, `OrdinalSortKey` sorts ascending. `SemanticsSortKey` is the abstract base; you can write a custom one but in practice `OrdinalSortKey` is what teams use. Sort keys only sort *within* a sibling group; you cannot jump nodes across parents. If you need cross-parent reordering you have to restructure the tree or use `Semantics(container: true)` to introduce a new sibling group.

**Hardware keyboard support.** `Focus`, `FocusScope`, `FocusableActionDetector`, and `Shortcuts`/`Actions` cover most needs. Tab order is governed by `FocusTraversalPolicy` — the default is `ReadingOrderTraversalPolicy` (reading order), with `OrderedTraversalPolicy` available for explicit ordering via `FocusTraversalOrder`. `WidgetsApp` / `MaterialApp` install a default focus traversal at the top.

iOS **Full Keyboard Access** (FKA) — Apple's hardware-keyboard substitute for switch users introduced in iOS 13.4, materially enhanced in iOS 15/16 — has been historically poor in Flutter. The yellow focus rectangle FKA draws around the focused element relies on `UIAccessibilityElement` focus visuals; Flutter's engine has had to synthesise this and it has lagged. As of Flutter 3.22 (May 2024) and the work tracked in `flutter/flutter#108131`, FKA traversal is functional for standard Material widgets, but the focus ring is drawn by Flutter, not iOS, and so does not always match the system style or honour Increase Contrast. Custom widgets that don't expose proper semantics actions are skipped. **Verify on every release** — this surface regressed twice between 3.13 and 3.19. The verification path: physical iPad with Magic Keyboard, Settings → Accessibility → Keyboards → Full Keyboard Access → On.

Android hardware-keyboard support is more robust because Flutter renders the focus indicator itself in both platforms and Android's expectations are looser. D-pad navigation on Android TV / Chromebook generally works for Material widgets; custom widgets need explicit `Focus` wrapping.

**Switch Control / Switch Access.** Both platforms expose switch-driven traversal as essentially a serialised walk of the semantics tree with the same sort order as the screen reader. If swipe order is correct in TalkBack/VoiceOver it will generally be correct under Switch Access / Switch Control. Group navigation on iOS depends on the parent-child structure of the semantics tree — flat trees produce flat switch traversal, which is exhausting on long screens. **`Semantics(container: true, explicitChildNodes: true)`** to create hierarchical groups (cards, list rows, sections) is the lever. There is no Flutter API to mark a "switch group" beyond standard semantics nesting.

**Modal trapping and focus return.** `showDialog`, `showModalBottomSheet`, and `DialogRoute` push a route with `scopesRoute: true` and a `namesRoute` label. The engine notifies the OS that a route changed, which on iOS produces the "screen changed" announcement and on Android the equivalent window-state-changed event. Focus is trapped inside the modal by `FocusScope`. On `Navigator.pop`, focus *should* return to the element that opened the modal — and in practice this works on Android but has had repeated regressions on iOS where VoiceOver focus jumps to the top of the underlying screen instead of the trigger. Tracked across several issues (notably `flutter/flutter#118481` and follow-ups); the workaround teams use is to grab a `GlobalKey` on the trigger and call `SemanticsService.announce` or manually request focus on the trigger's `FocusNode` in the `.then()` of `showDialog`. Always test return focus on a real iPhone with VoiceOver, not just simulator.

**Autofocus on route change.** `autofocus: true` on a `Focus` / `TextField` / `FocusableActionDetector` works for input focus but does not move the screen reader's accessibility cursor. To move VoiceOver/TalkBack focus on route entry, the canonical trick is:

```dart
final key = GlobalKey();
// after build:
SchedulerBinding.instance.addPostFrameCallback((_) {
  final ctx = key.currentContext;
  if (ctx != null) {
    ctx.findRenderObject()?.sendSemanticsEvent(const FocusSemanticEvent());
  }
});
```

This sends a `FocusSemanticEvent` to the platform, which moves the AT cursor. Behaviour on TalkBack has been less reliable than VoiceOver historically; if a route is auto-announcing its name via `namesRoute`, an explicit focus event can produce a double-announcement.

**Primitives summary.** `FocusNode` is the per-widget input-focus handle. `FocusScope` defines a focus boundary (modals, route content). `FocusTraversalPolicy` (with `FocusTraversalGroup` and `FocusTraversalOrder`) controls Tab order. `FocusableActionDetector` is the high-level "I am a focusable thing with hover, focus, and shortcut handling" widget worth defaulting to for custom interactive components. None of these touch the semantics tree directly — they govern keyboard, not assistive tech.

---

## 3. Text scaling and reflow

Flutter exposes the system text scale via `MediaQuery.textScalerOf(context)`, which returns a `TextScaler` — added in Flutter 3.16 (Nov 2023) to replace the deprecated `textScaleFactor` double. `TextScaler` is necessary because iOS and Android no longer scale linearly: iOS Dynamic Type at the larger accessibility sizes (AX1–AX5) is non-linear, and `textScaleFactor` could not represent it faithfully. `TextScaler.scale(double fontSize)` returns the scaled size; `TextScaler.linear(2.0)` constructs a linear 2× scaler for testing.

**Defaults.** Every `Text` widget reads `MediaQuery.textScaler` and scales accordingly. Material widgets that render text (buttons, app bars, list tiles) inherit this. `RichText` honours it. The `Text(textScaler: …)` parameter overrides it locally — this is the right place to *clamp* scaling on individual widgets that genuinely cannot scale further, not to disable it globally.

**What breaks at ≥200%.** Mostly the same things that break in any framework, plus some Flutter-specific failure modes:

- **Fixed-height containers.** `Container(height: 48, child: Text(…))` clips at large scales. Replace with `ConstrainedBox(constraints: BoxConstraints(minHeight: 48))` and let intrinsic height take over.
- **`Row` with `Text` children and no `Expanded`/`Flexible`.** Overflows horizontally. Either wrap text in `Expanded`, set `softWrap: true`, or switch to `Wrap`.
- **Icon-with-text pairs.** Icons do not scale with `textScaler` — they scale with their own `size` parameter. Visual mismatch between a 24dp icon and a 200% scaled label. Pair the icon's `IconTheme.size` to `IconTheme.of(context).size * textScaler.scale(1.0)` if you want them to grow together. Material 3 default icons do not do this; opt in per component.
- **`SizedBox` constraining text.** Replace with `ConstrainedBox` + intrinsic sizing.
- **`OverflowBox` / `FittedBox`.** `FittedBox(fit: BoxFit.scaleDown)` is occasionally the right answer for tightly-constrained chrome (status bars, badge counters) but it should never be the default for body content — it defeats the user's preference.
- **`TextOverflow.ellipsis` with `maxLines: 1`.** Common in cards and list rows. At 200%+ this hides content; consider `maxLines: 2` minimum, and allow `TextOverflow.visible` for primary content.
- **Pixel-precise layouts (8-point grid + fixed heights).** The design system's spacing tokens must allow content to push against them; rows expand vertically rather than truncating.

**Cupertino.** `CupertinoTextField`, `CupertinoButton`, etc. respect `textScaler` the same way. iOS's Dynamic Type categories (`UIContentSizeCategory`) reach Flutter via the platform channel and are translated into the `TextScaler`; you do not get the category enum directly. If you need to behave differently at AX1+ you have to threshold on the scaled size of a known reference (e.g. `if (MediaQuery.textScalerOf(context).scale(17) > 28)`).

**What Flutter gives you.** `MediaQueryData.textScaler`, `MediaQuery.textScalerOf`, `DefaultTextStyle.merge`, and the `textScaler:` parameter on `Text`/`RichText` for local overrides. `meetsGuideline` test matchers do not check text scaling — you must build widget tests that pump with a forced `MediaQuery` at 2× and 3× and assert no overflow. `accessibility_tools` (community package, see §7) includes a "large text" toggle in its overlay.

**WCAG 2.2 SC 1.4.4 (Resize Text)** mandates 200% without loss of content. WCAG 2.2 SC 1.4.10 (Reflow) is desktop-centric (320 CSS pixels) but the spirit applies: a 320pt-wide mobile viewport at 200% text should still be usable. The practical mobile target is **200% iOS Dynamic Type (AX2) and 200% Android font size** — both feasible in a Flutter app if the layout system uses intrinsic sizing throughout.

---

## 4. System contrast, color, and motion preferences

This is the area where Flutter's defaults are thinnest. The engine exposes most signals through `MediaQuery`, but Material widgets do not all act on them, and several iOS-specific signals only landed in 2024–2025.

`MediaQueryData` exposes:

- `platformBrightness` — dark mode. Honoured by `ThemeData` if you pass `darkTheme` to `MaterialApp`.
- `highContrast` — iOS Increase Contrast and Android high-contrast text. Available on both platforms via the engine since Flutter 3.7 (Jan 2023). Material widgets do **not** automatically switch to high-contrast colours; you have to provide a separate `highContrastTheme` and `highContrastDarkTheme` on `MaterialApp` and Flutter will pick them when the flag is set.
- `disableAnimations` — Reduce Motion on iOS, "Remove animations" on Android. Available since Flutter 1.17 but most Flutter animations (including `Hero`, `PageRouteBuilder`, `AnimatedContainer`) **do not honour this automatically**. You must check it and short-circuit your durations to `Duration.zero`. Material page transitions do honour it as of Flutter 3.16+ on the predictive-back transition specifically; older `MaterialPageRoute` does not.
- `invertColors` — iOS Classic Invert. Note: this is *Classic Invert*, not *Smart Invert*. Flutter has no signal for Smart Invert; Smart Invert is handled entirely by iOS at the rendering layer, after Flutter has drawn (see below).
- `boldText` — iOS Bold Text. Honoured by `Text` when wrapped in a `MaterialApp` since 3.13; verify your custom `TextStyle`s respect it by checking `MediaQuery.boldTextOf(context)` and adjusting `fontWeight`.
- `accessibleNavigation` — `true` when a screen reader, switch control, or guided access is active. Useful for branching behaviour (e.g. disable swipe-only gestures, see §5).
- `onOffSwitchLabels` — Android-only signal that the user has enabled "on/off labels" for switches.

What is **not** in `MediaQuery` and matters: iOS Differentiate Without Color, iOS Reduce Transparency, Android forced-colors / "high contrast text" specifically (the `highContrast` MediaQuery captures the boolean but not the colour scheme), Android colour-correction modes, and the new Android 14+ "force dark" override.

**Smart Invert on iOS.** Smart Invert (Settings → Accessibility → Display & Text Size → Smart Invert) inverts colours globally *except* on images, video, and elements marked `accessibilityIgnoresInvertColors`. Because Flutter renders to a single `CAEAGLLayer` / `CAMetalLayer` surface, iOS by default inverts the entire Flutter view, which destroys photos and brand-coloured icons. The fix is `UIAccessibility.accessibilityIgnoresInvertColors = YES` on the relevant view, but Flutter renders everything into one view — you cannot mark a sub-region. The Flutter-side workaround landed in 3.13 as the `Semantics.image: true` flag triggering `accessibilityIgnoresInvertColors` on a per-semantics-node basis where supported, but coverage is partial. The honest answer practitioners ship: **provide a manual "match system" theme that detects Smart Invert and serves uninverted colours**. There is no clean MediaQuery signal for Smart Invert specifically — the engine cannot distinguish it from Classic Invert reliably. Some teams detect via `UIAccessibilityIsInvertColorsEnabled` through a platform channel; this is a workaround, not a sanctioned API. Issue tracker: `flutter/flutter#41775` (open as of writing).

**Android forced-colors / high contrast.** Android 14 introduced a stronger high-contrast text mode and improvements to the colour-inversion accessibility setting. Flutter's `highContrast` MediaQuery flips, but there is no equivalent of CSS `forced-colors` media query that hands you a palette. You implement the high-contrast palette yourself in `ThemeData.highContrastDarkTheme`. Material 3's `ColorScheme.highContrastDark` constructor (Flutter 3.19+) gives you a starting palette but it is generic; brand work overrides it.

**Reduce Motion plumbing.**

```dart
final reduce = MediaQuery.disableAnimationsOf(context);
AnimatedContainer(
  duration: reduce ? Duration.zero : const Duration(milliseconds: 240),
  child: …,
);
```

Apply this at the `Theme.of(context).pageTransitionsTheme` level for global route transitions, and on every custom `AnimationController`. A widely-used pattern is to wrap `Tween.animate` calls in a helper that respects the flag. Lottie animations need explicit handling — they don't read the MediaQuery on their own.

**Where Flutter handles it, where you wire it.**

| Signal | Auto-respected by Flutter | You must wire |
|---|---|---|
| Dark mode | Yes, via `darkTheme` | Custom themes |
| Bold text | Mostly (3.13+) | Custom `TextStyle`s |
| Reduce motion | No (except newer page transitions) | All custom animations, Lottie, Hero |
| Increase contrast | Flag exposed; theming manual | `highContrastTheme` palette |
| Differentiate without color | No signal | Always add icon/text/pattern alongside colour |
| Reduce transparency | No signal | Manual; consider `BackdropFilter` thresholds |
| Smart Invert (iOS) | Partial via `Semantics.image` | Manual theme branch, platform channel for detection |
| Classic Invert (iOS) | Yes (`invertColors`) | Rarely useful |
| Forced colors (Android) | Flag only | Manual palette |
| Larger text | Yes via `textScaler` | Layout intrinsics |

The unstated rule: **never encode meaning in colour alone**. Status pills get an icon and a label, errors get an icon and red colour and a textual prefix ("Error: …"), required-field markers get both an asterisk and the word "required" in the accessible name. The system contrast / colour preferences then become a styling concern, not a meaning-conveyance concern.

---

## 5. Tap targets, gestures, and input alternatives

**Minimum target sizes.** Material 3 spec is 48×48dp, Apple HIG is 44×44pt. Flutter's `meetsGuideline` matchers in `flutter_test` enforce both:

- `meetsGuideline(androidTapTargetGuideline)` — 48dp.
- `meetsGuideline(iOSTapTargetGuideline)` — 44pt.
- `meetsGuideline(textContrastGuideline)` — WCAG AA contrast.
- `meetsGuideline(labeledTapTargetGuideline)` — every tappable semantics node has a non-empty label.

These run against a `SemanticsHandle` produced by `tester.ensureSemantics()`. They are the closest thing Flutter has to an automated a11y gate (see §7). Caveat: they measure semantic node bounding boxes, so a 24×24 `IconButton` inside a 48dp wrapper passes if and only if the semantics node is sized to the wrapper. `IconButton` does this correctly (default `splashRadius` + tap target is 48dp). `GestureDetector` does not — its semantics node, if one exists, is sized to the painted child. Always test custom buttons against the matcher.

**The 48dp Material default.** `IconButton`, `Checkbox`, `Radio`, and `Switch` enforce a 48dp tap target via the ambient `MaterialTapTargetSize.padded` (the default). If a designer wants tighter visual spacing, the right move is to keep the 48dp tap region and reduce visual chrome, not shrink the hit area. `MaterialTapTargetSize.shrinkWrap` exists but its only legitimate use is dense data tables where every row is a tap target.

**Drag, long-press, multi-finger, motion gestures.** WCAG 2.2 SC 2.5.7 (Dragging Movements, AA) and 2.5.4 (Motion Actuation, A) and the long-standing 2.5.1 (Pointer Gestures, A) all demand alternatives. In Flutter:

- **Drag** (e.g. `Dismissible`, `ReorderableListView`, sliders, swipe-to-action) — must have a non-drag alternative. `Slider` exposes `onIncrease`/`onDecrease` semantics actions automatically, so screen-reader users adjust by swiping up/down on the slider node. `Dismissible` exposes no such alternative — engineers must add a context menu, action button, or `customSemanticsAction` ("delete item"). `ReorderableListView` is the worst offender: drag-to-reorder is invisible to AT by default. The accepted pattern is `Semantics(customSemanticsActions: {CustomSemanticsAction(label: 'Move up'): () => …, CustomSemanticsAction(label: 'Move down'): () => …}, child: …)` on each row.
- **Long-press** — almost always also exposes a tap or a kebab/overflow menu; ensure parity. `onLongPress` does *not* automatically expose a semantics action; you must either route it through `Semantics(onLongPress: …)` or — better — provide an explicit secondary affordance.
- **Multi-finger gestures** — pinch-zoom, two-finger rotate, three-finger swipe. WCAG requires a single-pointer alternative. Pinch-zoom on an image: provide +/− buttons; `InteractiveViewer` does not provide them by default.
- **Motion-actuated gestures** — shake to undo, tilt to scroll. WCAG 2.5.4 requires a UI alternative and the ability to disable. Flutter has no high-level motion-gesture API; if a team built one on `sensors_plus`, they own the disable affordance.

**`MediaQuery.accessibleNavigation`** is the right flag to branch on for "screen reader / switch / VoiceOver is active — disable swipe-only gestures". It's true when any of TalkBack, VoiceOver, Switch Control, Switch Access, or Guided Access is on.

**Custom-gesture accessibility actions.** The high-leverage primitives:

- `onIncrease` / `onDecrease` — for any value-bearing widget. Sliders, steppers, rating widgets, paginated carousels. Surface them; both VoiceOver (one-finger swipe up/down on the focused element) and TalkBack (volume keys or two-finger swipe) consume them.
- `customSemanticsActions` — a `Map<CustomSemanticsAction, VoidCallback>`. Each action gets a label and appears in VoiceOver's rotor / TalkBack's local context menu. Use for "Delete", "Archive", "Mark as read", "Move up", "Move down".
- `onDismiss` — surfaces VoiceOver's two-finger Z-scrub or TalkBack's back gesture as a programmatic dismiss. Wire on every modal and snackbar.
- `onCopy`, `onCut`, `onPaste` — for custom rich text or content surfaces. Most teams don't bother because they use `SelectableText`, which wires these automatically.

---

## 6. Live regions, announcements, and dynamic content

The semantics primitive is `Semantics(liveRegion: true, child: Text(message))`. When the node's label changes, the engine emits a live-region event to the platform: `UIAccessibilityNotification.announcement` on iOS, `AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED` with `CONTENT_CHANGE_TYPE_TEXT` on Android. TalkBack reads the change with politeness ~= polite; VoiceOver reads it interruptively. There is **no `assertive` vs `polite` distinction in Flutter's API** — and this is a real gap. ARIA's `aria-live=assertive|polite` does not have a Flutter equivalent. Practitioners route critical messages through `SemanticsService.announce` (which is more reliably interruptive) and informational changes through `liveRegion: true`.

**Reliability on each platform.** TalkBack consumes `liveRegion` changes reasonably reliably, but **only when the node remains in the tree** through the label change. If you mount and immediately update a live region, the engine sometimes drops the first event. Mount the region with an empty string, then update on the next frame. VoiceOver is more unpredictable — `liveRegion` works for some node configurations and silently drops on others, particularly when the live-region node is also marked as a header or button. The community workaround: keep live regions as pure `Text` leaves, no buttons, no extra flags.

**`SemanticsService.sendAnnouncement` / `SemanticsService.announce`.** `announce(String message, TextDirection)` is the older API and is **deprecated in favour of `sendAnnouncement`** (renamed for clarity around 3.22, with `Assertiveness` enum added; verify against your channel's `services` library). The new signature:

```dart
SemanticsService.announce(
  'Form submitted',
  TextDirection.ltr,
  assertiveness: Assertiveness.assertive,
);
```

`Assertiveness.polite` queues the announcement behind whatever the screen reader is currently reading; `Assertiveness.assertive` interrupts. **When not to use it.** Don't use it for content already visible on screen — the user will hear it twice when they swipe to it. Don't use it to re-announce focus after `Navigator.pop` (handle properly via `FocusSemanticEvent` per §2). Don't use it for high-frequency events (typing into a search field that filters a list — let the count update via `liveRegion` instead). Don't use it to substitute for a real semantics structure (i.e. don't `announce("Submit button enabled")` instead of setting `Semantics(button: true, enabled: true)` correctly).

**Status messages.** WCAG 2.2 SC 4.1.3 (Status Messages, AA). Loading states, success toasts, error summaries. The right pattern: a single live region per screen at a known location (often invisible to sighted users, or co-located with the toast). When a status fires, write its message into the region. Snackbars: `SnackBar` automatically announces its content on Android (TalkBack reads `Toast`-style content) but reliability is platform-version-dependent. Verify on real devices; do not assume.

**Loading states.** A skeleton loader with no semantics is invisible — the user has no signal that content is pending. Wrap the skeleton in `Semantics(label: 'Loading', liveRegion: true, child: …)` and on transition to loaded, update the same node's label to something terminal ("Loaded 12 results") so the change is announced.

**Error announcements.** Forms with field-level errors: each error message should be inside a live region adjacent to the field, *and* the field's accessible name should incorporate the error ("Email — error: invalid format"). The latter ensures the error is read when the user refocuses the field.

---

## 7. Testing, tooling, and conformance evidence

**Widget test APIs.** `flutter_test` ships:

- `tester.ensureSemantics()` returns a `SemanticsHandle`; releases on dispose.
- `meetsGuideline(...)` matchers per §5.
- `SemanticsController` (via `tester.semantics`) — query the semantics tree directly. `find.semantics.byLabel('Submit')`, `tester.semantics.find(find.byType(Foo))`, etc.
- `simulatedAccessibilityTraversal()` — added Flutter 3.10 (May 2023). Returns an `Iterable<SemanticsNode>` in the order a screen reader would visit them. Useful for asserting reading order: `expect(tester.semantics.simulatedAccessibilityTraversal().map((n) => n.label), ['Title', 'Subtitle', 'Action']);`. Caveat: it simulates Flutter's *intended* traversal, not what TalkBack/VoiceOver actually do on device — useful as a regression guard, not a substitute for device testing.
- `findsAtLeastNSemantics`, custom matchers around `SemanticsNode` for fine-grained assertions.

**Test-suite shape that works.** Every component test exercises (a) the `meetsGuideline` quartet (Android tap, iOS tap, contrast, labeled tap), (b) a simulated traversal asserting reading order, (c) state transitions firing the correct semantics actions, (d) text-scaler 2× and 3× pumps asserting no overflow. This is the most under-invested-in piece of test coverage in most Flutter codebases, and it's tractable — these tests run in milliseconds, no device farm needed.

**In-app debug overlays.**

- `showSemanticsDebugger: true` on `MaterialApp` overlays semantic node bounds and labels on every widget. The default Flutter primitive; ugly but truthful.
- **`accessibility_tools`** (pub.dev package by Jeroen Meijer / Code & Coffee, actively maintained as of 2026). Adds a floating overlay that detects issues live: missing labels, low contrast, tap targets too small, mis-ordered semantics. Drop into the `MaterialApp.builder` in debug mode. This is the single highest-leverage debug aid for Flutter a11y; it surfaces the kinds of issues that would otherwise only show up under manual testing.
- **`flutter_a11y`** and similar packages exist; coverage varies.

**Platform tooling.**

- **Android: Accessibility Scanner** (Google Play, separate app). Run on the running Flutter app; produces a structured report flagging tap-target size, contrast, missing labels, etc. Treats Flutter as a black-box View, so the issues it reports are real but the suggested fixes are Android-View-centric.
- **Android: TalkBack developer settings + Layout Inspector** — limited visibility into Flutter's semantics tree from native tooling.
- **iOS: Xcode Accessibility Inspector** — connects to the running app, walks the accessibility tree, lets you trigger Audit. Catches missing labels, traits, and hit-test issues. The audit run is the closest thing to an automated WCAG check on iOS.
- **iOS: Voice Control + VoiceOver + Full Keyboard Access** as user-side checks.

**Manual testing workflow** (the actual day-to-day). Per release candidate, per supported platform, per representative device class:

1. TalkBack on a physical Android (mid-tier, e.g. Pixel 6a) — swipe through every reachable screen state. Note: simulator behaviour differs.
2. VoiceOver on a physical iPhone (SE class device for performance, and a larger Pro for layout). Verify rotor actions, custom actions, and modal focus return.
3. Text size at maximum (200% Android, AX5 iOS). Capture screenshots.
4. Dark mode + High contrast + Reduce Motion + Smart Invert. Capture screenshots.
5. Hardware keyboard + Full Keyboard Access (iPad with Magic Keyboard). Tab through every screen, verify focus indicators, verify trap behaviour in modals.
6. Switch Control / Switch Access — at minimum a Tab-equivalent walk.

**Evidence for ACR / VPAT.** What you can credibly produce:

- Automated: widget-test results (`meetsGuideline` quartet, simulated traversal assertions), CI-runnable on every PR.
- Semi-automated: Accessibility Scanner reports, Xcode Accessibility Inspector audit exports.
- Manual: device-test logs per platform with WCAG SC mapping, recorded screen captures with TalkBack/VoiceOver audio.
- Architectural: the design-system layer's pair tokens, contract docs, and four-layer model (see vault file 14) — these support conformance claims about the *system*, distinct from the *product* claims.

**What cannot be evidenced by automation.** Anything involving comprehension or judgement: SC 1.3.1 (Info and Relationships) beyond structural sniff-tests, SC 2.4.6 (Headings and Labels) for *meaningfulness*, SC 1.4.5 (Images of Text), SC 3.3.2 (Labels or Instructions) for *helpfulness*. These require human review and should be scoped into the QA cycle, not delegated to tools.

---

## 8. The Figma annotation contract

Given everything above, the contract between designer and Flutter engineer needs to cover the cases where defaults are wrong or absent. The principle: **annotate where the engineer would have to guess**. Don't annotate where Flutter does the right thing automatically — it dilutes the signal.

A useful test: if a senior Flutter engineer would write the same code regardless of the annotation, the annotation is noise. If two equally competent engineers would write different code without it, it's load-bearing.

**Per interactive element**, the designer specifies:

1. **Accessible name** — the string a screen reader announces. Default to the visible label; explicitly call out when they diverge (icon-only buttons, badges, glyph-bearing chrome). Always annotate icon-only controls. *Load-bearing because Flutter's `IconButton` has no label by default.*
2. **Role** — button / link / header / image / tab / textfield / slider / checkbox / switch / radio / progressbar / live region / decorative. If the role matches the Material/Cupertino widget choice, the engineer reads it from the widget. If the visual is custom (a card that acts as a button, a div that acts as a link), the role is load-bearing. Always annotate "this is a button" on any clickable non-button visual.
3. **State** — selected / pressed / expanded / disabled / checked / busy. Especially for components with custom visual state (a chip that means "filter applied", a tab indicator). For Material widgets state is automatic; for custom widgets it is not.
4. **Value / range / increment** — for sliders, steppers, ratings, paginated carousels. Specify the announceable value format ("3 of 5 stars", "Page 2 of 7") and the increment step. *Load-bearing — Flutter's `Slider` exposes a numeric value by default; if the design wants a labelled one, annotate.*
5. **Traversal order** — only when paint order is wrong for reading order. Default is paint order; annotate the override (e.g. "read badge before title", "skip decorative chrome"). Use ordinal numbers on the Figma frame.

**Per screen / region**, the designer specifies:

6. **Landmark / region structure** — header, navigation, main, footer (where applicable). On mobile the practical surface is "is this a heading?" — annotate H1 / section headings explicitly. Flutter does not auto-assign heading roles to `Text` based on style.
7. **Modal / route behaviour** — focus return target, autofocus target on open, dismissal gesture alternatives. *Load-bearing because of the iOS focus-return regression.*
8. **Live region intent** — which areas update in place and should announce. Annotate the region, the message format, and the assertiveness (polite vs. assertive). The toast/snackbar pattern is usually polite; form-submission errors and connection-lost banners are assertive.

**Per layout**, the designer specifies:

9. **Dynamic-type behaviour** — for each text-bearing component, "scales up freely" or "clamps at Nx with truncation" with the rationale. Default to "scales up freely with intrinsic height". Annotate the exceptions — usually navigation and chrome. *Load-bearing because the default in many design files is fixed heights.*
10. **Behaviour under Smart Invert / forced colors** — which images and icons should be excluded from inversion (logos, photos, brand-coloured glyphs that carry meaning). Which colour pairs are "do not invert" vs "invert is fine". For most app surfaces the inversion is fine; the exceptions are the load-bearing annotations.
11. **High-contrast palette** — for branded surfaces, provide a high-contrast variant (often a darker outline, higher-weight text, more saturated focus indicators). If you don't provide one, the engineer falls back to Material's default, which may not match the brand.
12. **Focus indicator** — visible focus ring spec (colour, thickness, offset, behaviour against various backgrounds). *Load-bearing because Flutter draws its own focus rings and the default is rarely brand-aligned.*

**Per gesture**, the designer specifies:

13. **Gesture alternative** — for any drag, long-press, multi-finger, or motion-actuated interaction, the alternative path. Swipe-to-delete needs a tap-to-reveal-action or a custom semantics action labelled "Delete". Drag-to-reorder needs move-up / move-down custom actions. Pinch-to-zoom needs +/− buttons.
14. **Custom semantics actions** — labelled actions surfaced in the rotor / context menu. List them: "Edit", "Delete", "Mark as favourite". *Load-bearing — these don't exist unless you specify them.*

**Per motion-bearing element**, the designer specifies:

15. **Reduce-motion behaviour** — for each transition, what happens when Reduce Motion is on. Default: cross-fade or instant. Annotate the few cases where motion is informational (a slide animation that conveys direction) and a non-motion equivalent is needed.

**Where Flutter's defaults make annotation unnecessary.**

- Standard Material/Cupertino widgets with visible text labels — the framework gets accessible name and role right.
- `Text` widgets — read automatically.
- `Image.network` with provided `semanticLabel` — annotation flows from `alt` text.
- Text scaling for `Text` widgets within `Column`/`Row` with `Flexible`/`Expanded` — works out of the box.
- Dark mode for components themed via `ThemeData` — works out of the box.

**Where the defaults are wrong or absent and annotation is load-bearing.**

- Any `GestureDetector`-based custom tap surface (no semantics by default).
- Icon-only `IconButton` (no name unless `tooltip` or `Semantics(label: …)`).
- Card-as-button patterns (Flutter has no idiom; engineers must wire `Semantics(button: true)` and `InkWell`).
- Reorderable lists (no AT alternative by default).
- Smart Invert exclusion (no clean Flutter API).
- Modal focus return on iOS (regression-prone).
- Reduce-motion respect on custom animations (must be wired per controller).
- Status messages and live regions (no `aria-live` analogue; assertiveness only via `SemanticsService.announce`).
- Forced-colors / high-contrast palette (manual theme).
- Custom focus indicators (Flutter draws its own).

The artefact form that has worked best in practice is an **annotation layer** inside the Figma file: a separate page or pinned frame per screen, with numbered markers referring to a single shared table that lists name, role, state, traversal, dynamic-type, invert behaviour, gesture alternative, and live-region intent. The same numbering scheme appears in the engineering tickets, the Storybook story (or Flutter widgetbook story), and the widget test names. This makes the annotation contract bidirectional: a missing test in CI maps to a missing or unimplemented annotation, not just a missing test.

---

## References

Primary sources (verify against current channel; versions noted inline).

- Flutter documentation — Accessibility: https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility
- Flutter API — `Semantics` widget: https://api.flutter.dev/flutter/widgets/Semantics-class.html
- Flutter API — `MergeSemantics` / `ExcludeSemantics` / `BlockSemantics`: https://api.flutter.dev/flutter/widgets/MergeSemantics-class.html
- Flutter API — `SemanticsService`: https://api.flutter.dev/flutter/semantics/SemanticsService-class.html
- Flutter API — `MediaQueryData` (text scaler, high contrast, disable animations, bold text, accessible navigation): https://api.flutter.dev/flutter/widgets/MediaQueryData-class.html
- Flutter API — `TextScaler`: https://api.flutter.dev/flutter/painting/TextScaler-class.html (added 3.16, Nov 2023).
- Flutter API — `FocusNode`, `FocusScope`, `FocusTraversalPolicy`, `FocusableActionDetector`: https://api.flutter.dev/flutter/widgets/FocusNode-class.html
- Flutter API — `meetsGuideline` matchers and `accessibilityGuideline`: https://api.flutter.dev/flutter/flutter_test/AccessibilityGuideline-class.html
- Flutter API — `SemanticsController.simulatedAccessibilityTraversal`: https://api.flutter.dev/flutter/flutter_test/SemanticsController/simulatedAccessibilityTraversal.html (added 3.10, May 2023).
- Flutter cookbook — Testing accessibility: https://docs.flutter.dev/cookbook/testing/widget/a11y
- Material 3 — Accessibility: https://m3.material.io/foundations/accessibility/overview
- Apple Human Interface Guidelines — Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
- Apple — Full Keyboard Access (iOS Settings → Accessibility → Keyboards → Full Keyboard Access).
- Android — Accessibility developer guide: https://developer.android.com/guide/topics/ui/accessibility
- Android — Accessibility Scanner: https://support.google.com/accessibility/android/answer/6376570
- WCAG 2.2: https://www.w3.org/TR/WCAG22/ — esp. SC 1.4.4, 1.4.10, 1.4.11, 1.4.12, 2.1.1, 2.4.3, 2.4.7, 2.5.1, 2.5.4, 2.5.5, 2.5.7, 2.5.8, 4.1.3.
- W3C Mobile Accessibility (WCAG2Mobile): https://www.w3.org/TR/mobile-accessibility-mapping/
- Flutter GitHub — known iOS focus-return issues around `Navigator.pop`: `flutter/flutter#118481` and related.
- Flutter GitHub — Smart Invert handling: `flutter/flutter#41775` (open as of writing).
- Flutter GitHub — Full Keyboard Access traversal: `flutter/flutter#108131`.
- `accessibility_tools` package: https://pub.dev/packages/accessibility_tools — debug overlay surfacing missing labels, contrast, tap targets, ordering.
- Wonderous (gskinner) — open-source Flutter reference app with above-average a11y treatment: https://github.com/gskinnerTeam/flutter-wonderous-app
- Flutter team blog — "Building accessible Flutter apps" (verify date; check `medium.com/flutter` and `docs.flutter.dev` release notes).
- Vault cross-references: `14-accessibility.md` (architectural position, four-layer model, pair tokens, conformance under EAA / Section 508), `11-mobile-and-cross-platform.md` (Flutter as cross-platform target, tokens as shared layer), `12-figma-practice.md` (annotation conventions inside Figma libraries), `13-internationalization-and-rtl.md` (RTL mirroring and logical properties as adjacent concerns).

# Motion pattern timing benchmark — Claude run (2026-11-19)

Raw output of the Claude half of a research run. The brief is `prompt.md` in this folder. The run answers the open sub-questions in KB issues #61 (reference timing per pattern track) and #62 (reference easing curves and curve strength). The external half has not been run yet.

**Method.** Primary sources only, every URL accessed **2026-11-19**. Three kinds of evidence, labelled on every number:

- **[G] guidance**: a design-system documentation page that states a value or rule.
- **[T] token**: a published token package (npm, or the system's own token source).
- **[C] code**: the system's own shipped component code (npm build or source repository). A [C] value is what the component does, not what the guidance tells others to do. Where [G] or [T] and [C] disagree, both are given.
- **[X] derived**: a number this run computed from a stated value, with the formula shown. Never presented as documented.

Several documentation sites render client-side and could not be read: m3.material.io, fluent2.microsoft.design (numbers), spectrum.adobe.com (numbers), primer.style (motion page), polaris.shopify.com (redirects to shopify.dev), and the Apple HIG HTML (read through its JSON endpoint instead). For Material 3 that matters most, so its values come from Google's own implementations: androidx Compose Material 3, Material Web, and the Material Components for Android docs. **No m3.material.io guidance value is quoted anywhere in this file.**

Source IDs in square brackets after a value (for example `S52`) resolve to the Sources list at the end, which carries each URL and its access date.

**Spring periods.** Material 3 and Apple publish springs, not durations. Where a row needs a comparable time, the run gives the undamped period T = 2π/√k at mass 1, the same mapping 18-motion-foundations uses for duration + bounce. That is a perceptual pace, not a settling time, and is marked [X]. Two derived values per M3 slot (standard scheme / expressive scheme):

| M3 slot | Standard ζ, k | T [X] | Expressive ζ, k | T [X] |
|---|---|---|---|---|
| FastSpatial | 0.9, 1400 | 168ms | 0.6, 800 | 222ms |
| DefaultSpatial | 0.9, 700 | 237ms | 0.8, 380 | 322ms |
| SlowSpatial | 0.9, 300 | 363ms | 0.8, 200 | 444ms |
| FastEffects | 1.0, 3800 | 102ms | 1.0, 3800 | 102ms |
| DefaultEffects | 1.0, 1600 | 157ms | 1.0, 1600 | 157ms |
| SlowEffects | 1.0, 800 | 222ms | 1.0, 800 | 222ms |

ζ and k from `StandardMotionTokens.kt` and `ExpressiveMotionTokens.kt` [T] S3; MDC-Android publishes the same standard values [G] S1. `MaterialTheme` defaults to `MotionScheme.standard()` [C] S4.

---

## 1. Per-pattern timing and easing

### 1.1 Micro state change (hover, focus, selected, toggle)

| System | Value | Kind | Source |
|---|---|---|---|
| Material 3 | Hover overlay 15ms linear; nav bar indicator colour DefaultEffects spring (T 157ms [X]); switch thumb FastSpatial spring (T 168ms [X]); focus ring 600ms emphasised (`duration-long4`, split 25% grow / 75% shrink) | [C] | S20, S13, S9, S22 |
| Carbon | `fast-01` 70ms "Micro-interactions such as button and toggle"; button and toggle ship 70ms; tabs colour and border 70ms `standard productive` (0.2, 0, 0.38, 0.9) | [T] [C] | S32, S38, S36, S37 |
| Carbon guidance | "Do micro-interactions fall within a static duration ranging from 90–120 ms?"; micro-interactions use ease-out on user input | [G] | S30 |
| Atlassian | List item hover 50ms; list item selected 100ms; button hover 150ms; input and toggle 150ms; all `out.practical` (0.4, 1, 0.6, 1) | [T] | S52 |
| Atlassian guidance | Interactions 50–150ms; `xxshort` 50ms "High-frequency interactions (e.g. list item hover)" | [G] | S50, S51 |
| Fluent 2 | Button 100ms (`durationFaster`) `curveEasyEase` (0.33, 0, 0.67, 1); switch 200ms (`durationNormal`) easyEase | [C] | S68, S67 |
| Apple | Not stated. HIG: "In apps, generally avoid adding motion to UI interactions that occur frequently." | [G] | S80 |
| Polaris | Checkbox and radio border 100ms `ease-out` (0.19, 0.91, 0.38, 1); checked icon 150ms ease-out | [C] | S91 |
| Spectrum | Button and action button 130ms (`duration-100`) ease-in-out; switch colour 160ms (`duration-200`) ease-in-out | [C] | S109, S108 |
| Primer | Token `transition.hover` = 100ms (`micro`) + `ease` (0.25, 0.1, 0.25, 1); `stateChange` = 200ms + `easeInOut` (0.6, 0, 0.2, 1) | [T] | S120 |
| Primer code | Button 80ms cubic-bezier(0.65, 0, 0.35, 1); toggle switch 80ms cubic-bezier(0.5, 1, 0.89, 1) | [C] | S121, S125 |
| IBM | Not stated | — | S41 |

### 1.2 Fade

| System | Value | Kind | Source |
|---|---|---|---|
| Material 3 | `MaterialFade`: in 150ms, out 75ms, linear, with a secondary scale | [G] | S1 |
| | **Discrepancy:** that table names the attributes `motionDurationShort2` / `Short1`, which M3's own tokens set to 100ms / 50ms. The 150/75 column matches the older Material Components theme. 18-motion-foundations currently cites "Material's fade is 150ms in and 75ms out" | [G] vs [T] | S1, S2 |
| | Compose M3 fades (menu, tooltip, snackbar alpha) use the FastEffects spring both ways (T 102ms [X]) | [C] | S6, S5, S7 |
| Carbon | `fast-02` 110ms "Micro-interactions such as fade in. Subtle entrance or exit of small UI elements." | [T] | S32 |
| Atlassian | Fade rides with the surface (popup 150 in / 100 out; modal 250 / 200); icon fade 250ms in `out.bold` (0, 0.4, 0, 1), 250ms out `in.practical` (0.6, 0, 0.8, 0.6); fast icon fade 50ms | [T] | S52 |
| Fluent 2 | `Fade`: 200ms both ways, `curveEasyEase`; `FadeSnappy` 150ms; `FadeRelaxed` 250ms | [C] | S62 |
| Apple | Not stated. SwiftUI `easeInOut` and `easeOut` default to 0.35s (generic, not fade-specific) | [C] | S82 |
| Polaris | Backdrop fade-in 200ms | [C] | S91 |
| Spectrum | Not stated separately (fades ride with each overlay; see 1.7) | — | S102–S106 |
| Primer | Not stated separately | — | S120 |
| IBM | Not stated | — | S41 |

### 1.3 Crossfade (content swap in place)

| System | Value | Kind | Source |
|---|---|---|---|
| Material 3 | Fade through: 300ms, documented default easing cubic-bezier(0.4, 0, 0.2, 1) (`FastOutSlowIn`, the legacy standard curve), against an attribute (`motionEasingStandard`) the same page sets to (0.2, 0, 0, 1); see §7 | [G] | S1 |
| Carbon | Not stated | — | S30, S32 |
| Atlassian | Icon swap: `iconography-enter-fade` / `exit-fade` 250ms; `cycle-up` 400ms cubic-bezier(0.65, 0, 0.35, 1) with a 100% slide | [T] | S52 |
| Fluent 2 | Guidance: top-level navigation uses "a quick fade transition"; no number | [G] | S60 |
| Apple | Not stated (HIG visionOS: "Consider using fades when you need to relocate an object") | [G] | S80 |
| Polaris, Spectrum, Primer, IBM | Not stated | — | S91, S101, S120, S41 |

### 1.4 Indicator move (tab, segmented)

| System | Value | Kind | Source |
|---|---|---|---|
| Material 3 | Compose tab indicator DefaultSpatial spring (T 237ms [X]); Material Web tab indicator 250ms emphasised (approximated there as cubic-bezier(0.3, 0, 0, 1)) | [C] | S8, S19, S16 |
| Carbon | No sliding indicator; tab border and colour change 70ms `standard productive` | [C] | S37 |
| Atlassian | `tab-indicator-enter` 150ms `out.bold` + 8px slide + fade; `exit` 100ms `in.practical` + 8px | [T] | S52 |
| Fluent 2 | Tab indicator transform 300ms (`durationSlow`) `curveDecelerateMax` (0.1, 0.9, 0.2, 1) | [C] | S66 |
| Apple | Not stated | — | S80 |
| Polaris | Not stated | — | S91 |
| Spectrum | Tabs indicator transform 130ms ease-in-out token (0.45, 0, 0.4, 1) | [C] | S107 |
| Primer | Segmented control indicator (`inset`) 200ms `easeInOut` (0.6, 0, 0.2, 1) | [C] | S126 |
| IBM | Not stated | — | S41 |

### 1.5 Reveal on view (scroll-triggered)

**Not stated by any system surveyed.** No reveal-on-view duration, distance or easing appears in Material 3 (S1–S23), Carbon (S30–S33), Atlassian (S50–S52), Fluent (S60–S62), Apple (S80), Polaris (S90–S91), Spectrum (S101), Primer (S120) or IBM (S41). Primer's dialog uses `animation-timeline: scroll(self)`, but only to show a border when the body scrolls, not as a reveal (S122).

### 1.6 Line draw (stroke or path draw)

| System | Value | Kind | Source |
|---|---|---|---|
| Material 3 | Compose checkbox check draw uses DefaultSpatial spring (T 237ms [X]) | [C] | S12 |
| Polaris | Checkbox checkmark path animation 150ms linear | [C] | S91 |
| Carbon, Atlassian, Fluent, Apple, Spectrum, Primer, IBM | Not stated | — | S30–S33, S52, S62, S80, S101, S120, S41 |

### 1.7 Surface and sheet enter and exit

Values are enter / exit. Easing follows each duration where it differs.

| System | Surface | Enter | Exit | Kind | Source |
|---|---|---|---|---|---|
| Material 3 | Dialog (Material Web) | 500ms emphasised; 50px slide; scrim 500ms linear | 150ms emphasised-accelerate (0.3, 0, 0.8, 0.15) | [C] | S17 |
| | Menu (Material Web) | 500ms emphasised; items stagger, see 1.11 | 150ms emphasised-accelerate | [C] | S18 |
| | Menu, tooltip (Compose) | Scale 0.8→1 FastSpatial (T 168ms [X]) + alpha FastEffects (T 102ms [X]) | Same specs reversed | [C] | S6, S5 |
| | Snackbar (Compose) | Alpha FastEffects + scale FastSpatial | Same | [C] | S7 |
| | Bottom sheet, nav drawer (Compose) | DefaultSpatial spring (T 237ms [X]) | FastEffects spring (T 102ms [X]) | [C] | S11, S10 |
| | Sheet tween fallback (Compose) | 300ms `FastOutSlowInEasing` | — | [C] | S11 |
| | Container transform (MDC) | 300ms | 250ms | [G] | S1 |
| Carbon | Modal | 240ms (`moderate-02`) `entrance expressive` (0, 0, 0.3, 1); container 24px slide | 240ms `exit expressive` (0.4, 0.14, 1, 1) | [C] | S34 |
| | Tooltip, popover (`contextual` surface) | 110ms (`fast-02`) `entrance expressive`, scale 0.96→1 | 110ms `exit expressive` | [T] | S33 |
| | Toast | `moderate-02` 240ms "Expansion, system communication, toast" | Not stated | [T] | S32 |
| | Background dimming | `slow-02` 700ms | Not stated | [T] | S32 |
| Atlassian | Popup (menu, popover) | 150ms `out.practical`, 8px slide + fade | 100ms `in.practical`, 4px + fade | [T] | S52 |
| | Modal | 250ms `inout.bold` (0.4, 0, 0, 1), scale 95→100% | 200ms `in.practical`, scale 100→95% | [T] | S52 |
| | Flag (toast) | 250ms `out.bold`, 50% slide + fade | 200ms `in.practical`, 15% slide | [T] | S52 |
| | Blanket (scrim) | 250ms `inout.bold` | 200ms `in.practical` | [T] | S52 |
| | Panel, side nav | 200ms `out-expo` (0.16, 1, 0.3, 1), 100% slide | 200ms `out-quart` (0.25, 1, 0.5, 1) | [T] | S52 |
| | Panel content | 150ms `out.practical` | 50ms `in.practical` | [T] | S52 |
| Fluent 2 | Dialog | 250ms (`durationGentle`) `curveDecelerateMid` (0, 0, 0, 1), scale 0.85→1 | 250ms `curveAccelerateMin` (0.8, 0, 0.78, 1) | [C] | S64 |
| | Dialog backdrop | `FadeRelaxed` 250ms | 250ms | [C] | S64, S62 |
| | Drawer, by size | small 250, medium 300, large 400, full 500ms; `curveDecelerateMid` | Same durations; `curveAccelerateMin` | [C] | S65 |
| | `Scale` (generic) | 250ms `curveDecelerateMax`, from 0.9 | 200ms `curveAccelerateMax` (0.9, 0.1, 1, 0.2) | [C] | S62 |
| | `Slide` (generic) | 200ms `curveDecelerateMid` | 200ms `curveAccelerateMid` (1, 0, 1, 1) | [C] | S62 |
| Apple | System presentations | Not stated. SwiftUI `Animation.default` is a spring, response 0.55, damping 1.0 (iOS 17 and later) | — | [C] | S81 |
| Polaris | Modal | 200ms `ease` (0.25, 0.1, 0.25, 1), fade-up | Not stated separately | [C] | S91 |
| | Popover | 100ms `ease` | Not stated separately | [C] | S91 |
| | Tooltip | 50ms `ease-out` after a 100ms delay | No exit animation found | [C] | S91 |
| | Toast | 400ms `ease-out` | 200ms `ease-in` (0.42, 0, 1, 1) | [C] | S91 |
| | Sheet | 300ms `ease` | Not stated separately | [C] | S91 |
| Spectrum | Modal | 250ms (`duration-500`) ease-out (0, 0, 0.4, 1) after 160ms delay; 20–25px slide | 130ms (`duration-100`) | [C] | S104 |
| | Underlay (scrim) | 300ms ease-out | 190ms ease-in (0.5, 0, 1, 1) after 160ms delay | [C] | S105 |
| | Tray (bottom sheet) | 250ms cubic-bezier(0, 0, 0.4, 1) after 160ms delay | 130ms cubic-bezier(0.5, 0, 1, 1) | [C] | S106 |
| | Tooltip | 130ms ease-in-out, 4–5px distance | 130ms ease-in-out | [C] | S102, S101 |
| Primer | Tokens | `transition.enter` = 300ms (`medium`) + `easeOut` (0.3, 0.8, 0.6, 1) | `transition.exit` = 200ms (`short`) + `easeIn` (0.7, 0.1, 0.75, 0.9), "Shorter than enter to feel snappy" | [T] | S120 |
| | Dialog (code) | 200ms scale 0.5→1 + fade, cubic-bezier(0.33, 1, 0.68, 1); side sheets 250ms | No exit animation found | [C] | S122 |
| | Overlay, tooltip (code) | Overlay 200ms (0.33, 1, 0.68, 1); tooltip 100ms ease-in | No exit animation found | [C] | S123, S124 |
| IBM | — | Not stated | Not stated | — | S41 |

**Primer's components do not use Primer's own semantic motion tokens.** The tokens say 300ms in and 200ms out; the shipped dialog is 200ms in with no exit, and the button is 80ms where `transition.hover` is 100ms (S120 vs S121–S124).

### 1.8 Expand / collapse

| System | Height (size) track | Chevron | Kind | Source |
|---|---|---|---|---|
| Material 3 | Not stated in any M3 source read. Material Web dialog container height: 500ms emphasised open, 150ms emphasised-accelerate close | Not stated | [C] | S17 |
| Carbon | `disclosure` surface ("Accordion, table-row expand"): 150ms (`moderate-01`), enter easing `entrance productive` (0, 0, 0.38, 0.9), exit easing `exit productive` (0.2, 0, 1, 0.9), block size and opacity together | — | [T] | S33 |
| Carbon code | Accordion wrapper: `all` 110ms `entrance productive` (max-block-size, opacity), both directions. Token and code differ (150 vs 110ms) | 110ms `standard productive` | [C] | S35 |
| Atlassian | Not stated | Not stated | — | S51, S52 |
| Fluent 2 | `Collapse` (used by Accordion): 200ms (`durationNormal`) `curveEasyEaseMax` (0.8, 0, 0.2, 1) both ways; size and opacity tracks default to the same duration | Not stated | [C] | S62, S69 |
| Apple | Not stated | Not stated | — | S80 |
| Polaris | `Collapsible`: max-height 100ms `ease-out` | — | [C] | S91 |
| Spectrum | Accordion CSS carries no transition | — | [C] | S101 |
| Primer | `transition.stateChange` = 200ms + `easeInOut` (`move`), usage lists "expand-collapse", "accordion"; `easing.move` rule: "Use if an element moves or morphs on screen" | — | [T] | S120 |
| IBM | Not stated | — | — | S41 |
| Carbon choreography | "a data table row expansion and a dropdown should share the same motion style and easing"; durations "differ slightly based on component size"; no value | — | [G] | S31 |

### 1.9 Carousel step

| System | Value | Kind | Source |
|---|---|---|---|
| Material 3 | Compose carousel snap: `spring(stiffness = Spring.StiffnessMediumLow)` = 400, damping default 1.0 (T 314ms [X]) | [C] | S14, S15 |
| Fluent 2 | Carousel on Embla, `duration` 25 in Embla's own unit (not milliseconds) | [C] | S70 |
| Carbon, Atlassian, Apple, Polaris, Spectrum, Primer, IBM | Not stated | — | S30–S33, S52, S80, S91, S101, S120, S41 |

### 1.10 Settle after release (snap, fling settle)

| System | Value | Kind | Source |
|---|---|---|---|
| Material 3 | Sheet and drawer settle: DefaultSpatial spring (T 237ms [X]); drawer anchored-drag fallback tween 256ms; MDC: "Spring for animations that partially cover the screen like a bottom sheet or nav drawer" | [C] [G] | S11, S10, S1 |
| Apple | `interactiveSpring` defaults response 0.15, damping 0.86; `spring(response:dampingFraction:)` defaults 0.5, 0.825; `.smooth` / `.snappy` / `.bouncy` duration 0.5 with bounce 0 / 0.15 / 0.3 | [C] | S85, S84, S83 |
| Carbon, Atlassian, Fluent, Polaris, Spectrum, Primer, IBM | Not stated | — | S30–S33, S52, S62, S91, S101, S120, S41 |

### 1.11 Stagger

| System | Interval | Cap or item duration | Kind | Source |
|---|---|---|---|---|
| Material 3 | Material Web menu open: items fade 250ms each, interval (500 − 250) / item count; close: 150ms total, items 50ms | 500ms total open | [C] | S18 |
| Carbon | 20ms ("staggering the entrance of table content by 20 ms") | "within 500 ms" total | [G] | S31 |
| Fluent 2 | `Stagger` default item delay 100ms (`durationFaster`) | Item 200ms (`durationNormal`) | [C] | S62 |
| Atlassian, Apple, Polaris, Spectrum, Primer, IBM | Not stated | Not stated | — | S52, S80, S91, S101, S120, S41 |

---

## 2. Exit versus enter

Ratio = exit duration / enter duration, for pairs a system ships as a matched enter and exit. Spring pairs use the derived period and are marked [X].

| System | Pair | Ratio | Kind | Source |
|---|---|---|---|---|
| Material 3 | Material Web dialog 500 / 150; menu 500 / 150 | 0.30 | [C] | S17, S18 |
| | MDC fade 150 / 75 | 0.50 | [G] | S1 |
| | MDC container transform 300 / 250 | 0.83 | [G] | S1 |
| | Compose sheet, drawer DefaultSpatial / FastEffects | ≈0.43 [X] | [C] | S11, S10 |
| | Compose menu, tooltip, snackbar | 1.0 (same spring both ways) | [C] | S6, S5, S7 |
| Material 1 (2014, archived; source of the draft's curves) | "Elements entering the screen occur over 225ms / Elements leaving the screen occur over 195ms" | 0.87 | [G] | S25 |
| Carbon | Modal 240 / 240; contextual 110 / 110; disclosure 150 / 150 | 1.0 (easing changes, duration does not) | [C] [T] | S34, S33 |
| Atlassian | Popup, avatar, label, form message, tab indicator 150 / 100 | 0.67 | [T] | S52 |
| | Modal, flag, blanket, spotlight 250 / 200 | 0.80 | [T] | S52 |
| | Panel content 150 / 50 | 0.33 | [T] | S52 |
| | Panel, side nav, icon fade | 1.0 | [T] | S52 |
| | Rule: "Exits should be shorter, faster, and less dramatic. Use a practical easing curve and reduce the duration by 50ms or 100ms compared to the entrance." | absolute, not a ratio | [G] | S51 |
| | Rule: "Make exit motion faster than entrances so dismissed elements don't block someone's workflow." | — | [G] | S50 |
| Fluent 2 | `Scale` 250 / 200; `ScaleSnappy` 200 / 150; `ScaleRelaxed` 300 / 250 | 0.80 / 0.75 / 0.83 | [C] | S62 |
| | Dialog, drawer, `Fade`, `Slide`, `Collapse` | 1.0 ("Defaults to the `duration` param for symmetry") | [C] | S64, S65, S62 |
| Apple | Not stated | — | — | S80 |
| Polaris | Toast 400 / 200 | 0.50 | [C] | S91 |
| Spectrum | Modal 250 / 130; tray 250 / 130 | 0.52 | [C] | S104, S106 |
| | Underlay 300 / 190 | 0.63 | [C] | S105 |
| | Tooltip | 1.0 | [C] | S102 |
| Primer | Tokens 300 / 200 | 0.67 | [T] | S120 |
| IBM | Not stated | — | — | S41 |

**Reading.** Of the deliberately asymmetric pairs, most land between 0.5 and 0.83. Two sit lower: Material Web's dialog and menu at 0.30, and Atlassian's panel content at 0.33. Atlassian is the only system that states the rule, and it states it as an absolute cut of 50 or 100ms, not a ratio. Carbon and Fluent's dialog, drawer and collapse ship **symmetric durations** and express the asymmetry through the curve alone. The existing 18 citation of Atlassian's popup (0.67) and Material's fade (0.5) sits inside this spread.

---

## 3. Reduced motion

| System | What happens | Kind | Source |
|---|---|---|---|
| Material 3 | Material Web: tab indicator swaps to an opacity change; focus ring `animation: none`. Compose M3: no component-level rule found in the sources read | [C] | S19, S22 |
| Carbon | Component CSS sets `transition: none` / `animation: none` under `prefers-reduced-motion: reduce` (modal, toggle, accordion, overflow menu). Guidance: "Always provide alternatives for interface state transitions" | [C] [G] | S34–S36, S39, S30 |
| Atlassian | "Respect reduced motion settings. Currently, when reduced motion is active, motion is off and instant." | [G] | S50 |
| Fluent 2 | Motion atoms default to a 1ms duration under reduced motion; an atom can declare its own `reducedMotion` keyframes and params. Component CSS uses 0.01ms (button, switch, tab indicator) | [C] | S63, S68, S67, S66 |
| Apple | `accessibilityReduceMotion`: "UI should avoid large animations, especially those that simulate the third dimension." `prefersCrossFadeTransitions` reports Reduce Motion plus Prefer Cross-Fade Transitions. HIG: "Make motion optional." | [C] [G] | S86, S87, S80 |
| Polaris | Tooltip `animation: none`; no other reduced-motion rule in the compiled CSS | [C] | S91 |
| Spectrum | Guidance: "motion over large surface areas needs to support browser and system settings for reduced motion." None of the 13 component stylesheets checked has a reduced-motion query | [G] [C] | S100, S102–S110 |
| Primer | Token rule: "MUST respect prefers-reduced-motion." Overlay and tooltip animate only under `no-preference`; toggle switch `transition: none` | [T] [C] | S120, S123–S125 |
| IBM | Not stated | — | S41 |

**Reading.** Three treatments appear: **off** (Carbon, Atlassian, Polaris, Primer: no animation), **near-zero** (Fluent: 1ms atoms, 0.01ms CSS, which keeps end events firing), and **substitute** (Material Web's tab indicator becomes a fade; Apple's cross-fade preference; Fluent's per-atom override). No system surveyed publishes a reduced *duration* value, such as a shortened but non-zero fade. 18's position (spatial tracks dropped or cross-faded, effects tracks kept at reduced duration) is not contradicted, but no surveyed system does the "kept at reduced duration" half.

---

## 4. Press feedback

| System | Press down | Release | Press scale | Kind | Source |
|---|---|---|---|---|---|
| Material 3 | Ripple fade-in 105ms; grow 450ms `standard` (0.2, 0, 0, 1) from scale 0.2; touch delay 150ms | Fade-out 375ms linear; minimum press 225ms | Not stated | [C] | S20 |
| | MDC: animate the button's shape or size with FastSpatial and its colour with FastEffects | Same springs | Not stated | [G] | S1 |
| | Switch handle (Material Web): grows 250ms `standard`; travel 300ms cubic-bezier(0.175, 0.885, 0.32, 1.275), commented "custom to perform the overshoot" | — | — | [C] | S21 |
| Carbon | Button background, shadow, border, outline 70ms `entrance productive` | Same (single CSS transition) | Not stated | [C] | S38 |
| Atlassian | Button pressed 150ms `out.practical`; list item pressed 100ms. Guidance: `xshort` 100ms "Subtle pressed states", `short` 150ms "emphasised hover and pressed states" | Same token | Not stated | [T] [G] | S52, S51 |
| Fluent 2 | Button 100ms easyEase | Same | Not stated | [C] | S68 |
| Apple | Not stated. HIG: "Aim for brevity and precision in feedback animations." | — | Not stated | [G] | S80 |
| Polaris | No transition on button found | — | Not stated | [C] | S91 |
| Spectrum | Button 130ms ease-in-out | Same | Not stated | [C] | S109 |
| Primer | Button 80ms cubic-bezier(0.65, 0, 0.35, 1); hover state duration 80ms | Same | Not stated | [C] | S121 |
| IBM | Not stated | — | — | — | S41 |

**Reading.** Press feedback spans **70–150ms** where stated (Carbon 70, Primer 80, Fluent 100, Material Web 105, Spectrum 130, Atlassian 100–150). **Only Material distinguishes press-down from release**, and its release is slower (375ms) than its press (105ms), the opposite of an exit-faster rule. **No system surveyed states a press-scale value.** MVP pattern 2's "small spatial spring on press" has no published reference value; Material's FastSpatial spring for "shape/size" is the nearest (S1).

---

## 5. Easing strength (for #62)

### 5.1 Current curves per system and scheme

| System | Scheme | Enter | Exit | Standard (in place) | Source |
|---|---|---|---|---|---|
| Material 3 | Standard | (0, 0, 0, 1) | (0.3, 0, 1, 1) | (0.2, 0, 0, 1) | S2, S1 |
| | Emphasised | (0.05, 0.7, 0.1, 1) | (0.3, 0, 0.8, 0.15) | path curve (MDC), approximated (0.3, 0, 0, 1) on web | S2, S1, S16 |
| | Legacy | (0, 0, 0.2, 1) | (0.4, 0, 1, 1) | (0.4, 0, 0.2, 1) | S2 |
| Carbon | Productive | (0, 0, 0.38, 0.9) | (0.2, 0, 1, 0.9) | (0.2, 0, 0.38, 0.9) | S32 |
| | Expressive | (0, 0, 0.3, 1) | (0.4, 0.14, 1, 1) | (0.4, 0.14, 0.3, 1) | S32 |
| Atlassian | Practical | `out.practical` (0.4, 1, 0.6, 1) | `in.practical` (0.6, 0, 0.8, 0.6) | — | S52 |
| | Bold | `out.bold` (0, 0.4, 0, 1) | — | `inout.bold` (0.4, 0, 0, 1) | S52 |
| | Also | `out-expo` (0.16, 1, 0.3, 1), `out-quart` (0.25, 1, 0.5, 1), `spring` as baked `linear()` | | | S52 |
| Fluent 2 | Max / Mid / Min | Decelerate (0.1, 0.9, 0.2, 1) / (0, 0, 0, 1) / (0.33, 0, 0.1, 1) | Accelerate (0.9, 0.1, 1, 0.2) / (1, 0, 1, 1) / (0.8, 0, 0.78, 1) | EasyEase (0.33, 0, 0.67, 1); EasyEaseMax (0.8, 0, 0.2, 1) | S61 |
| Apple | — | Not stated as curves; SwiftUI ships springs (`.smooth`, `.snappy`, `.bouncy`) and CSS-like named curves | | | S81–S83 |
| Polaris | One set | `ease-out` (0.19, 0.91, 0.38, 1) | `ease-in` (0.42, 0, 1, 1) | `ease-in-out` (0.42, 0, 0.58, 1); `ease` (0.25, 0.1, 0.25, 1) | S90 |
| Spectrum | One set | `ease-out` (0, 0, 0.4, 1) | `ease-in` (0.5, 0, 1, 1) | `ease-in-out` (0.45, 0, 0.4, 1) | S101 |
| Primer | One set | `easeOut` (0.3, 0.8, 0.6, 1) | `easeIn` (0.7, 0.1, 0.75, 0.9) | `easeInOut` (0.6, 0, 0.2, 1); `ease` for hover | S120 |
| IBM | — | Not stated (classic principles: "Avoid long exponential eases as elements settle into place") | | | S41 |

### 5.2 A comparable strength number [X]

No system publishes a strength measure. To compare curves, this run evaluated each cubic-bezier numerically: **for an enter curve, the progress reached at 25% of the duration** (higher means the element arrives sooner, a stronger deceleration); **for an exit curve, the progress at 50% of the duration** (lower means the element lingers and then leaves, a stronger acceleration). Computed by bisection on the curve's x(t); the script is not part of the record. These are our numbers, not the systems'.

**Enter, progress at 25% / 50% of time** [X]

| Curve | 25% | 50% |
|---|---|---|
| Fluent decelerateMax (0.1, 0.9, 0.2, 1) | 0.85 | 0.97 |
| M3 emphasised decelerate (0.05, 0.7, 0.1, 1) | 0.83 | 0.95 |
| Atlassian out-expo (0.16, 1, 0.3, 1) | 0.83 | 0.97 |
| Atlassian out.bold (0, 0.4, 0, 1) | 0.79 | 0.93 |
| Polaris ease-out (0.19, 0.91, 0.38, 1) | 0.74 | 0.94 |
| M3 standard decelerate = Fluent decelerateMid (0, 0, 0, 1) | 0.69 | 0.89 |
| Atlassian out-quart (0.25, 1, 0.5, 1) | 0.69 | 0.93 |
| **Draft enter = M3 legacy decelerate (0, 0, 0.2, 1)** | **0.58** | **0.84** |
| Primer dialog/overlay code (0.33, 1, 0.68, 1) | 0.58 | 0.87 |
| Atlassian out.practical (0.4, 1, 0.6, 1) | 0.55 | 0.88 |
| Primer easeOut token (0.3, 0.8, 0.6, 1) | 0.53 | 0.83 |
| Carbon entrance expressive (0, 0, 0.3, 1) | 0.52 | 0.81 |
| Spectrum ease-out (0, 0, 0.4, 1) | 0.46 | 0.77 |
| Carbon entrance productive (0, 0, 0.38, 0.9) | 0.44 | 0.73 |
| Fluent decelerateMin (0.33, 0, 0.1, 1) | 0.40 | 0.83 |
| CSS `ease-out` (0, 0, 0.58, 1), for reference | 0.38 | 0.68 |

**Exit, progress at 50% / 75% of time** [X]

| Curve | 50% | 75% |
|---|---|---|
| Fluent accelerateMax (0.9, 0.1, 1, 0.2) | 0.08 | 0.17 |
| Fluent accelerateMid (1, 0, 1, 1) | 0.11 | 0.31 |
| M3 emphasised accelerate (0.3, 0, 0.8, 0.15) | 0.15 | 0.41 |
| Atlassian in.practical (0.6, 0, 0.8, 0.6) | 0.19 | 0.50 |
| Fluent accelerateMin (0.8, 0, 0.78, 1) | 0.19 | 0.57 |
| Primer easeIn (0.7, 0.1, 0.75, 0.9) | 0.26 | 0.65 |
| Spectrum ease-in (0.5, 0, 1, 1) | 0.28 | 0.59 |
| Polaris ease-in = CSS `ease-in` (0.42, 0, 1, 1) | 0.32 | 0.62 |
| **Draft exit = M3 legacy accelerate (0.4, 0, 1, 1)** | **0.32** | **0.63** |
| M3 standard accelerate (0.3, 0, 1, 1) | 0.37 | 0.67 |
| Carbon exit productive (0.2, 0, 1, 0.9) | 0.38 | 0.66 |
| Carbon exit expressive (0.4, 0.14, 1, 1) | 0.39 | 0.67 |

**Standard (in place), progress at 25 / 50 / 75%** [X]: M3 standard (0.2, 0, 0, 1), the draft's default, 0.61 / 0.88 / 0.98, which is closer to an enter curve than to a symmetric ease; Atlassian inout.bold 0.41 / 0.86 / 0.97; Carbon productive 0.31 / 0.68 / 0.91; Carbon expressive 0.26 / 0.75 / 0.95; M3 legacy standard 0.24 / 0.78 / 0.96; Fluent easyEase 0.16 / 0.50 / 0.84; Spectrum 0.14 / 0.61 / 0.93; Polaris ease-in-out 0.13 / 0.50 / 0.87; Primer easeInOut 0.10 / 0.70 / 0.96; Fluent easyEaseMax 0.05 / 0.50 / 0.95.

### 5.3 What the evidence says on #62's four questions

1. **Strength.** The draft's enter (legacy decelerate, 0.58 at 25%) and exit (legacy accelerate, 0.32 at 50%) both sit **mid-field**, not at the soft end.
   - **Enter.** Softer than M3 standard and emphasised decelerate, Fluent decelerateMax and Mid, Atlassian out.bold, out-expo and out-quart, and Polaris ease-out. Level with Primer's dialog curve and Atlassian out.practical. Stronger than Carbon (both schemes), Spectrum, Primer's token and Fluent decelerateMin.
   - **Exit.** Softer than all three Fluent accelerate curves, M3 emphasised accelerate, Atlassian in.practical, Primer easeIn and Spectrum ease-in. Level with Polaris and CSS ease-in. Stronger than M3 standard accelerate and both Carbon exits.

   "Softer than several systems' current curves" holds; "softer than the field" does not. **One trap:** M3's own current *standard* accelerate (0.3, 0, 1, 1) is softer than the legacy accelerate it replaced (0.37 vs 0.32 at 50%), so moving the exit to M3 standard would weaken it. A strength rule the shape gate could check falls naturally out of 5.2, as a floor on enter progress at 25% and a ceiling on exit progress at 50%. Where to put the floor and ceiling is a P-step decision; the field's enter range is 0.40–0.85 and its exit range 0.08–0.39.
2. **Mixing generations.** Google's own sources mix them, though partly through stale documentation. MDC-Android's transition tables list `FastOutSlowIn` (0.4, 0, 0.2, 1) as the default easing for container transform, shared axis and fade through, against the attribute `motionEasingStandard`, which the same page's curve table sets to (0.2, 0, 0, 1) (S1). That is the same stale-column pattern as the fade durations in §1.2. Compose M3 still ships the three legacy curves in `MotionTokens` (S2) and uses `FastOutSlowInEasing` for its sheet tween fallback (S11). Material Web uses M3 curves only (S16). The legacy curves are the Material 1 deceleration, acceleration and standard curves of 2014, there named `LinearOutSlowIn`, `FastOutLinearIn` and `FastOutSlowIn` (S25). No source calls the mix a defect, and none recommends it.
3. **Height track easing.** The field splits:
   - **In-place curve:** Primer, whose `stateChange` uses `easeInOut` and whose `move` usage lists expand-collapse (S120), and Fluent, whose `Collapse` uses `curveEasyEaseMax` both ways (S62).
   - **Enter and exit curves:** Carbon's `disclosure` surface (`entrance` / `exit productive`, S33, and `entrance productive` in its accordion CSS, S35); Polaris's `Collapsible` (`ease-out`, S91); and Material Web's dialog container height (emphasised open, emphasised-accelerate close, S17).

   The KB's inference that a height track takes `easing/standard` matches two of five systems that state anything. It is defensible, not convergent.
4. **Expressive scheme.** Systems that ship a second intensity: Material 3 (standard and expressive motion schemes, plus emphasised curves), Carbon (productive and expressive), Atlassian (practical and bold) and Fluent (Max / Mid / Min, plus Snappy and Relaxed variants). Apple ships perceptual spring presets rather than schemes. **Polaris, Spectrum and Primer ship one set with no expressive scheme.** 18's "a mature motion system ships both" therefore describes four of the eight systems surveyed.

---

## 6. What the evidence says on #61's six questions

Evidence only. Mapping a pattern onto 18's roles (instant 50–100, short 150–250, medium 300–400, long 500–700) is the P step's call.

1. **Duration per MVP pattern track, field spread:**
   - Fade: 75–250ms.
   - State or press: 15–200ms, with presses at 70–150ms.
   - Pop (menu or popover) enter: 100–250ms, or 500ms on Material Web.
   - Dialog enter: 200–500ms; dialog exit: 130–250ms.
   - Sheet or drawer enter: 200–500ms, by size in Fluent.
   - Expand/collapse: 100–240ms.
   - Toast enter: 240–400ms.

   The per-system values are in §1.
2. **Exit ratio:** §2. Asymmetric pairs run 0.30–0.87, mostly 0.5–0.83. Atlassian states an absolute cut (−50 or −100ms). Carbon and parts of Fluent are symmetric.
3. **Tooltip hide:** M3 Compose reverses the same springs (alpha T 102ms [X], S5). Carbon `contextual` 110ms with exit expressive easing (S33). Atlassian popup exit 100ms (S52). Spectrum 130ms ease-in-out, symmetric (S102). MDC fade-out 75ms (S1). Polaris and Primer ship no exit animation (S91, S124). Fluent and Apple: not stated.
4. **Press:** §4. No press-scale value anywhere. Only Material separates press from release, and its release is slower.
5. **Expand/collapse duration:** Polaris 100, Carbon 110 (code) or 150 (token), Primer 200, Fluent 200ms (§1.8). Atlassian, Spectrum, Apple and IBM: not stated. M3: not stated in the sources read.
6. **Distance-scaled drawers:** One system implements size-scaled durations: Fluent's drawer, at 250 / 300 / 400 / 500ms for small, medium, large and full (S65). Others state the principle without numbers:
   - MDC: "duration should increase as the area/traversal of an animation increases" (S1).
   - Carbon: "the larger the change in distance (traveled) or size (scaling) of the element, the longer the animation takes" (S30).
   - Fluent 2: "Give larger elements more time to animate than smaller elements" (S60).
   - Material 1: tablet durations "about 30% longer than on mobile" (S25).
   - IBM's `@ibm/motion` (0.3.1, 2018, pre-release) computes duration from distance and element size (S42).

   Atlassian's panel (200ms for a 100% slide) and Spectrum's tray (250ms) are fixed. One derived note [X]: a linear spring's settling time does not depend on travel distance, so M3's spring-driven sheets do not distance-scale by themselves.

---

## 7. Open and unverified register

- **m3.material.io was not read** (client-rendered). Whether its easing-and-duration guidance states per-pattern durations, an exit rule or an expand/collapse value is UNVERIFIED. Every M3 value above is implementation or MDC-Android documentation.
- **MDC fade 150/75 vs M3 tokens 100/50** (§1.2). It is UNVERIFIED which one current M3 guidance intends. 18-motion-foundations quotes 150/75. The same page's transition tables also give container transform, shared axis and fade through durations (300 / 250ms) and the easing `FastOutSlowIn` from the older theme, so all MDC transition defaults in this file carry the same caveat.
- **Fluent 2, Spectrum and Primer documentation pages** rendered without values, so their [G] guidance numbers, if any, are UNVERIFIED. Their [T] and [C] values are verified.
- **Atlassian's applying-motion page** labels some table columns in a way that conflicts with its own prose: the dropdown row reads as if the 150ms value were the exit. The token package (S52) is unambiguous, and this run uses it.
- **Atlassian motion is early access**, behind a feature flag "on a limited set of components" (S50). Values may move.
- **Carbon token vs code**: disclosure 150ms in `surfaces.tokens.json` vs 110ms in the accordion stylesheet (S33 vs S35).
- **Primer tokens vs code**: the semantic tokens are not used by the dialog, button or tooltip components read (§1.7).
- **Polaris React** (`@shopify/polaris` 13.9.5) is the source read. Whether Polaris's newer web components use the same values is UNVERIFIED.
- **Fluent's carousel duration** is in Embla's unit; no millisecond equivalent is stated (S70).
- **The spring periods** (T = 2π/√k) are a perceptual pace, not a settling time. A settling time needs a stated tolerance (see 18 §Spring tokens).

---

## Sources

All accessed 2026-11-19.

**Material 3 / Google**
- S1 MDC-Android, Motion.md: https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md
- S2 androidx, `MotionTokens.kt`: https://github.com/androidx/androidx/blob/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens/MotionTokens.kt
- S3 androidx, `StandardMotionTokens.kt` and `ExpressiveMotionTokens.kt`: https://github.com/androidx/androidx/tree/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens
- S4 androidx, `MotionScheme.kt` and `MaterialTheme.kt`: https://github.com/androidx/androidx/tree/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3
- S5 androidx, `Tooltip.kt` (same directory as S4)
- S6 androidx, `Menu.kt` (same directory as S4)
- S7 androidx, `SnackbarHost.kt` (same directory as S4)
- S8 androidx, `TabRow.kt` (same directory as S4)
- S9 androidx, `Switch.kt` (same directory as S4)
- S10 androidx, `NavigationDrawer.kt` (same directory as S4)
- S11 androidx, `BottomSheetScaffold.kt`, `ModalBottomSheet.kt`, `SheetDefaults.kt` (same directory as S4)
- S12 androidx, `Checkbox.kt` (same directory as S4)
- S13 androidx, `NavigationBar.kt` (same directory as S4)
- S14 androidx, `carousel/Carousel.kt`: https://github.com/androidx/androidx/blob/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/carousel/Carousel.kt
- S15 Android reference, Compose `Spring`: https://developer.android.com/reference/kotlin/androidx/compose/animation/core/Spring
- S16 Material Web, `internal/motion/animation.ts`: https://github.com/material-components/material-web/blob/main/internal/motion/animation.ts
- S17 Material Web, `dialog/internal/animations.ts`: https://github.com/material-components/material-web/blob/main/dialog/internal/animations.ts
- S18 Material Web, `menu/internal/menu.ts`: https://github.com/material-components/material-web/blob/main/menu/internal/menu.ts
- S19 Material Web, `tabs/internal/tab.ts`: https://github.com/material-components/material-web/blob/main/tabs/internal/tab.ts
- S20 Material Web, `ripple/internal/ripple.ts` and `_ripple.scss`: https://github.com/material-components/material-web/tree/main/ripple/internal
- S21 Material Web, `switch/internal/_handle.scss`: https://github.com/material-components/material-web/blob/main/switch/internal/_handle.scss
- S22 Material Web, `focus/internal/_focus-ring.scss` and `tokens/_md-comp-focus-ring.scss`: https://github.com/material-components/material-web/tree/main/focus/internal
- S23 Material Web, `tokens/versions/v0_192/_md-sys-motion.scss`: https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-motion.scss
- S24 M3, Easing and duration (client-rendered; not read): https://m3.material.io/styles/motion/easing-and-duration/applying-easing-and-duration
- S25 Material 1 (archived), Duration and easing: https://m1.material.io/motion/duration-easing.html

**Carbon and IBM**
- S30 Carbon, Motion overview: https://carbondesignsystem.com/elements/motion/overview/
- S31 Carbon, Choreography: https://carbondesignsystem.com/elements/motion/choreography/
- S32 `@carbon/motion` 11.57.0, `tokens/motion.tokens.json`: https://unpkg.com/@carbon/motion@11.57.0/tokens/motion.tokens.json
- S33 `@carbon/motion` 11.57.0, `tokens/surfaces.tokens.json`: https://unpkg.com/@carbon/motion@11.57.0/tokens/surfaces.tokens.json
- S34 `@carbon/styles` 1.120.0, modal: https://unpkg.com/@carbon/styles@1.120.0/scss/components/modal/_modal.scss
- S35 `@carbon/styles` 1.120.0, accordion: https://unpkg.com/@carbon/styles@1.120.0/scss/components/accordion/_accordion.scss
- S36 `@carbon/styles` 1.120.0, toggle: https://unpkg.com/@carbon/styles@1.120.0/scss/components/toggle/_toggle.scss
- S37 `@carbon/styles` 1.120.0, tabs: https://unpkg.com/@carbon/styles@1.120.0/scss/components/tabs/_tabs.scss
- S38 `@carbon/styles` 1.120.0, button mixins: https://unpkg.com/@carbon/styles@1.120.0/scss/components/button/_mixins.scss
- S39 `@carbon/styles` 1.120.0, overflow menu: https://unpkg.com/@carbon/styles@1.120.0/scss/components/overflow-menu/_overflow-menu.scss
- S40 `@carbon/styles` 1.120.0, loading: https://unpkg.com/@carbon/styles@1.120.0/scss/components/loading/_loading.scss
- S41 IBM Design Language, Animation (overview, classic principles, tips and techniques): https://www.ibm.com/design/language/animation/overview/ ; https://www.ibm.com/design/language/animation/classic-principles/ ; https://www.ibm.com/design/language/animation/tips-and-techniques/
- S42 `@ibm/motion` 0.3.1 (published 2018-02-18), README and `dist/getDuration.js`: https://unpkg.com/@ibm/motion@0.3.1/README.md

**Atlassian**
- S50 Atlassian, Motion: https://atlassian.design/foundations/motion
- S51 Atlassian, Applying motion: https://atlassian.design/foundations/motion/applying-motion
- S52 `@atlaskit/tokens` 20.14.0, `atlassian-motion` theme: https://unpkg.com/@atlaskit/tokens@20.14.0/dist/cjs/artifacts/themes/atlassian-motion.js

**Fluent 2**
- S60 Fluent 2, Motion: https://fluent2.microsoft.design/motion
- S61 Fluent tokens, `durations.ts` and `curves.ts`: https://github.com/microsoft/fluentui/tree/master/packages/tokens/src/global
- S62 `@fluentui/react-motion-components-preview` 0.15.10 (Fade, Scale, Slide, Collapse, Stagger): https://unpkg.com/@fluentui/react-motion-components-preview@0.15.10/lib/components/
- S63 `@fluentui/react-motion` 9.16.5, `hooks/useAnimateAtoms.js`: https://unpkg.com/@fluentui/react-motion@9.16.5/lib/hooks/useAnimateAtoms.js
- S64 `@fluentui/react-dialog` 9.18.6, `DialogSurfaceMotion.js` and `DialogBackdropMotion.js`: https://unpkg.com/@fluentui/react-dialog@9.18.6/lib/components/DialogSurfaceMotion.js
- S65 `@fluentui/react-drawer` 9.13.5, `shared/drawerMotions.js`: https://unpkg.com/@fluentui/react-drawer@9.13.5/lib/shared/drawerMotions.js
- S66 `@fluentui/react-tabs` 9.12.6, `useTabAnimatedIndicator.styles.raw.js`: https://unpkg.com/@fluentui/react-tabs@9.12.6/lib/components/Tab/useTabAnimatedIndicator.styles.raw.js
- S67 `@fluentui/react-switch` 9.7.7, `useSwitchStyles.styles.raw.js`: https://unpkg.com/@fluentui/react-switch@9.7.7/lib/components/Switch/useSwitchStyles.styles.raw.js
- S68 `@fluentui/react-button` 9.11.3, `useButtonStyles.styles.raw.js`: https://unpkg.com/@fluentui/react-button@9.11.3/lib/components/Button/useButtonStyles.styles.raw.js
- S69 `@fluentui/react-accordion` 9.12.5, `useAccordionPanel.js`: https://unpkg.com/@fluentui/react-accordion@9.12.5/lib/components/AccordionPanel/useAccordionPanel.js
- S70 `@fluentui/react-carousel` 9.9.16, `useEmblaCarousel.js`: https://unpkg.com/@fluentui/react-carousel@9.9.16/lib/components/useEmblaCarousel.js

**Apple**
- S80 HIG, Motion (read through the JSON endpoint): https://developer.apple.com/design/human-interface-guidelines/motion
- S81 SwiftUI `Animation.default`: https://developer.apple.com/documentation/swiftui/animation/default
- S82 SwiftUI `Animation.easeInOut` and `easeOut`: https://developer.apple.com/documentation/swiftui/animation/easeinout ; https://developer.apple.com/documentation/swiftui/animation/easeout
- S83 SwiftUI `smooth(duration:extraBounce:)`, `snappy(duration:extraBounce:)`, `bouncy(duration:extraBounce:)`: https://developer.apple.com/documentation/swiftui/animation/snappy(duration:extrabounce:)
- S84 SwiftUI `spring(response:dampingFraction:blendDuration:)`: https://developer.apple.com/documentation/swiftui/animation/spring(response:dampingfraction:blendduration:)
- S85 SwiftUI `interactiveSpring(response:dampingFraction:blendDuration:)`: https://developer.apple.com/documentation/swiftui/animation/interactivespring(response:dampingfraction:blendduration:)
- S86 SwiftUI `accessibilityReduceMotion`: https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion
- S87 UIKit `prefersCrossFadeTransitions`: https://developer.apple.com/documentation/uikit/uiaccessibility/preferscrossfadetransitions

**Polaris**
- S90 Polaris tokens, `motion.ts`: https://github.com/Shopify/polaris/blob/main/polaris-tokens/src/themes/base/motion.ts
- S91 `@shopify/polaris` 13.9.5, `build/esm/styles.css`: https://unpkg.com/@shopify/polaris@13.9.5/build/esm/styles.css
- S92 Polaris tokens page (redirects to shopify.dev; not read): https://polaris.shopify.com/tokens/motion

**Spectrum**
- S100 Spectrum, Motion (client-rendered; one sentence read): https://spectrum.adobe.com/page/motion/
- S101 `@spectrum-css/tokens` 16.0.2: https://unpkg.com/@spectrum-css/tokens@16.0.2/dist/css/index.css
- S102 `@spectrum-css/tooltip` 7.2.0: https://unpkg.com/@spectrum-css/tooltip@7.2.0/dist/index.css
- S103 `@spectrum-css/popover` 8.3.0: https://unpkg.com/@spectrum-css/popover@8.3.0/dist/index.css
- S104 `@spectrum-css/modal` 7.2.0: https://unpkg.com/@spectrum-css/modal@7.2.0/dist/index.css
- S105 `@spectrum-css/underlay` 6.2.0: https://unpkg.com/@spectrum-css/underlay@6.2.0/dist/index.css
- S106 `@spectrum-css/tray` 5.2.0: https://unpkg.com/@spectrum-css/tray@5.2.0/dist/index.css
- S107 `@spectrum-css/tabs` 6.2.0: https://unpkg.com/@spectrum-css/tabs@6.2.0/dist/index.css
- S108 `@spectrum-css/switch` 6.2.0: https://unpkg.com/@spectrum-css/switch@6.2.0/dist/index.css
- S109 `@spectrum-css/button` 14.2.0 and `@spectrum-css/actionbutton` 7.2.0: https://unpkg.com/@spectrum-css/button@14.2.0/dist/index.css
- S110 `@spectrum-css/progresscircle` 5.2.0: https://unpkg.com/@spectrum-css/progresscircle@5.2.0/dist/index.css

**Primer**
- S120 `@primer/primitives` 11.10.0: `src/tokens/base/motion/easing.json5`, `timing.json5`, `src/tokens/functional/motion/motion.json5`, `dist/css/functional/motion/motion.css`: https://unpkg.com/@primer/primitives@11.10.0/src/tokens/functional/motion/motion.json5
- S121 `@primer/react` 38.46.0, ButtonBase CSS: https://unpkg.com/@primer/react@38.46.0/dist/Button/ButtonBase-c8dab214.css
- S122 `@primer/react` 38.46.0, Dialog CSS: https://unpkg.com/@primer/react@38.46.0/dist/Dialog/Dialog-b7da369a.css
- S123 `@primer/react` 38.46.0, Overlay CSS: https://unpkg.com/@primer/react@38.46.0/dist/Overlay/Overlay-214d10dd.css
- S124 `@primer/react` 38.46.0, TooltipV2 CSS: https://unpkg.com/@primer/react@38.46.0/dist/TooltipV2/Tooltip-dd983e5b.css
- S125 `@primer/react` 38.46.0, ToggleSwitch CSS: https://unpkg.com/@primer/react@38.46.0/dist/ToggleSwitch/ToggleSwitch-b5866af6.css
- S126 `@primer/react` 38.46.0, SegmentedControl CSS: https://unpkg.com/@primer/react@38.46.0/dist/SegmentedControl/SegmentedControl-99b8e34e.css
- S127 Primer, Motion primitives page (rendered without values): https://primer.style/foundations/primitives/motion

---

## Compact table: pattern × system → duration / curve

For the Prism3 motion presets work. Cells are enter / exit where they differ. "n/s" means not stated. Curves are abbreviated as in §5.1: M3 `emph` = emphasised, `emph-acc` = emphasised accelerate, `std` = standard; Carbon `ent`/`exit` with `prod`/`expr`; Atlassian `out.prac`, `in.prac`, `out.bold`, `inout.bold`. Springs give the derived period T [X]. Sources are in §1–§4.

| Pattern | Material 3 | Carbon | Atlassian | Fluent 2 | Apple | Polaris | Spectrum | Primer | IBM |
|---|---|---|---|---|---|---|---|---|---|
| Micro state change | hover 15ms linear; colour DefaultEffects spring T157 | 70ms std prod | 50–150ms out.prac | 100ms easyEase | n/s | 100ms ease-out | 130ms ease-in-out | token 100ms ease; code 80ms (0.65,0,0.35,1) | n/s |
| Fade | MDC 150 / 75 linear (M3 tokens 100 / 50); Compose FastEffects T102 | 110ms | rides surface; icon 250 / 250 | 200ms easyEase | n/s | 200ms (backdrop) | n/s | n/s | n/s |
| Crossfade | fade through 300ms (0.4,0,0.2,1) | n/s | icon 250ms; cycle 400ms (0.65,0,0.35,1) | n/s | n/s | n/s | n/s | n/s | n/s |
| Indicator move | DefaultSpatial T237; web 250ms emph | 70ms colour only | 150 out.bold / 100 in.prac | 300ms decelMax | n/s | n/s | 130ms ease-in-out | 200ms easeInOut | n/s |
| Reveal on view | n/s | n/s | n/s | n/s | n/s | n/s | n/s | n/s | n/s |
| Line draw | DefaultSpatial T237 | n/s | n/s | n/s | n/s | 150ms linear | n/s | n/s | n/s |
| Dialog | web 500 emph / 150 emph-acc | 240 ent expr / 240 exit expr | 250 inout.bold / 200 in.prac | 250 decelMid / 250 accelMin | n/s | 200ms ease | 250 ease-out (+160 delay) / 130 | token 300 easeOut / 200 easeIn; code 200 (0.33,1,0.68,1) / none | n/s |
| Menu, popover | web 500 emph / 150 emph-acc; Compose FastSpatial T168 + FastEffects T102 | 110 ent expr / exit expr | 150 out.prac / 100 in.prac | n/s (generic `Scale` 250 decelMax / 200 accelMax) | n/s | 100ms ease | n/s | overlay 200 (0.33,1,0.68,1) / none | n/s |
| Tooltip | FastSpatial + FastEffects, both ways | 110 ent expr / exit expr | 150 / 100 | n/s | n/s | 50ms ease-out after 100ms / none | 130 / 130 ease-in-out | 100ms ease-in / none | n/s |
| Toast | Compose FastEffects + FastSpatial | 240ms | 250 out.bold / 200 in.prac | n/s | n/s | 400 ease-out / 200 ease-in | n/s | n/s | n/s |
| Sheet, drawer | DefaultSpatial T237 / FastEffects T102 | n/s | 200 out-expo / 200 out-quart | 250–500 by size, decelMid / accelMin | n/s | 300ms ease | tray 250 (+160) / 130 | side sheet 250 (0.33,1,0.68,1) | n/s |
| Expand / collapse | n/s | token 150 ent / exit prod; code 110 ent prod | n/s | 200ms easyEaseMax | n/s | 100ms ease-out | none | 200ms easeInOut | n/s |
| Carousel step | spring k400 ζ1, T314 | n/s | n/s | Embla 25 (not ms) | n/s | n/s | n/s | n/s | n/s |
| Settle after release | DefaultSpatial T237 | n/s | n/s | n/s | interactiveSpring 0.15 / 0.86 | n/s | n/s | n/s | n/s |
| Stagger | web menu: (500 − 250) / n | 20ms within 500ms | n/s | 100ms delay, 200ms item | n/s | n/s | n/s | n/s | n/s |
| Exit / enter ratio | 0.30–0.83; 1.0 for Compose menu springs | 1.0 | 0.33–0.80; rule −50 or −100ms | 0.75–1.0 | n/s | 0.50 | 0.52–0.63 | 0.67 | n/s |
| Reduced motion | substitute (web tabs) or none | off | off, instant | 1ms atom; 0.01ms CSS | avoid large / 3D; cross-fade pref | off (tooltip) | n/s in CSS | off (no-preference gate) | n/s |
| Press | 105 down / 375 release | 70ms ent prod | 100–150ms out.prac | 100ms easyEase | n/s | n/s | 130ms ease-in-out | 80ms | n/s |

# Motion tokens, motion patterns and Figma Motion — Claude run (2026-10-14)

Raw output of the Claude half of the dual-agent run. The prompt is `prompt.md` in this folder, unedited. The section spine follows the prompt's seven numbered scope items. After them come a section on what this run supersedes in the May 2026 runs and in `21-motion-spec-and-handoff`, an open/unverified register, and references.

**Method.** We researched four scope clusters in parallel against primary sources only:

- design-system repositories and published packages;
- the Figma help center, the Plugin API docs, the `@figma/plugin-typings` package, and the Figma MCP docs;
- the W3C DTCG report and its GitHub issues;
- WCAG 2.2 and its Understanding documents;
- MDN, plus MDN's browser-compat-data JSON;
- Apple's documentation JSON endpoints and WWDC session pages;
- the Android reference pages and AOSP/androidx source;
- the Reanimated and Style Dictionary docs and source.

Every URL was accessed on **2026-10-14**. A few sources render client-side and could not be read directly: m3.material.io, the Fluent Storybook, and Apple's HTML pages. In those cases we read the underlying source repository or the JSON endpoint instead, and say so. Anything we could not confirm against a primary page is marked **UNVERIFIED**.

Some claims come from the owner's live Figma Plugin API spike rather than from a document. Those are cited as *(live API test, 2026-10-14)*.

---

## 1. What mature design systems ship as motion tokens today

### The survey, compressed

| System | Durations | Easing | Springs | Composites / patterns in the token layer | Naming |
|---|---|---|---|---|---|
| **Material 3** (Compose + Material Web) | 16 steps: Short1–4 = 50–200ms, Medium1–4 = 250–400, Long1–4 = 450–600, ExtraLong1–4 = 700–1000 | 10 curves: Emphasized / Standard / Legacy, each × base / accelerate / decelerate, plus Linear | **Yes.** 6 slots, {fast, default, slow} × {spatial, effects}, each a (dampingRatio, stiffness) pair. There are two schemes, standard and expressive. | `MotionScheme` is a public interface, so a brand can implement its own | Semantic tier + ordinal |
| **Carbon** | 6: `fast-01` 70, `fast-02` 110, `moderate-01` 150, `moderate-02` 240, `slow-01` 400, `slow-02` 700 | 3 × 2 matrix: {standard, entrance, exit} × {productive, expressive} | No | New "surfaces" on `main`: `disclosure`, `contextual`, `expand`, `invoke`, each pairing a duration with enter/exit easings and keyframes, with custom surfaces accepted. Source is now authored as DTCG JSON. | Semantic tier + ordinal |
| **Fluent 2** | 8: UltraFast 50, Faster 100, Fast 150, Normal 200, Gentle 250, Slow 300, Slower 400, UltraSlow 500 | 9: Accelerate / Decelerate × Max / Mid / Min, EasyEase / EasyEaseMax, Linear | No | Not in tokens. Patterns live in code (see 2). | Speed adjectives; direction × intensity |
| **Atlassian** (early access) | 8: instant 0, xxshort 50, xshort 100, short 150, medium 200, long 250, xlong 400, xxlong 600 | 4 named curves, *practical* and *bold* families, plus `easing-spring` as a baked CSS `linear()` of about 65 points with roughly 2.4% overshoot | Baked only | **Yes.** Component-level composite tokens such as `motion.popup.enter.bottom`, which is 150ms + practical-out + keyframes `SlideInBottom8px` and `FadeIn0to100`. Keyframe tokens also exist. | Context.type.direction |
| **Polaris** | 12, literal: `motion-duration-0` … `-500` in 50ms steps, plus `-5000` | 5. Named after the CSS keywords, but `ease-out` is a custom curve (0.19, 0.91, 0.38, 1). | No | Keyframe tokens: `bounce`, `fade-in`, `pulse`, `spin`, `appear-above`, `appear-below` | Literal |
| **Spectrum** (Spectrum CSS tokens) | 14: `duration-0`, `-100` … `-1000`, `-2000`, `-4000`, `-6000` (0 to 3000ms) | 4 | No | No. The Spectrum 2 data package (`@adobe/spectrum-tokens` 15.5.0) has **no motion tokens at all**; whether this is deliberate is UNVERIFIED. | Ordinal |
| **Primer** | Base tier 0–1000ms; semantic `micro / short / medium / long` = 100 / 200 / 300 / 500 | Base 5; semantic `hover / enter / exit / move / linear` | No | **Yes.** `motion.transition.{hover, stateChange, enter, exit}` = duration + timing function, with machine-readable `usage` and `rules` metadata on every token | Base literal, semantic role |
| **Apple** (SwiftUI) | No token scale | Platform curves | **Yes.** `.smooth` (bounce 0), `.snappy` (0.15), `.bouncy` (0.3), all with duration 0.5 and tunable through `extraBounce`; four `Spring` initialisers | Platform primitives (`matchedGeometryEffect`, `NavigationTransition.zoom`) | Perceptual preset names |
| **Compose** (platform) | n/a | `CubicBezierEasing`, custom `Easing` | `spring(dampingRatio, stiffness)` with constants; mass is implicitly 1 | `AnimationSpec` family | Physical constants |

We also checked Base Web (17 literal timing steps), SLDS 1 (adverb-named durations such as `PROMPTLY` and `SLOWLY`, with no easing in the aliases file) and Open Props (5-step easing families, plus `--ease-spring-1..5` as baked `linear()` curves).

### Where the field has converged

**A duration scale of 6–16 steps, with the working range at 100–400ms.** Every system has a scale. Ceilings vary: 500ms (Fluent), 600ms (Atlassian), 700ms (Carbon), up to 1000ms or more (M3, Spectrum, Primer). Above roughly 400ms, steps exist for dimming, hero moments and ambient motion, not routine UI.

**Four easing roles, often crossed with a second intensity axis.** The roles are standard/move, enter/decelerate, exit/accelerate and linear. The intensity axis is the same idea with different names:

- Carbon: productive × expressive
- M3: standard × emphasized
- Fluent: Min / Mid / Max
- Atlassian: practical × bold

That intensity axis is the industry's de facto **personality lever**, and it is the closest thing to what our model calls role tiers (default / enter / exit / emphasized). Our model is on target here.

**Semantic names over literal names, with literal primitives kept underneath.** Polaris, Base Web and Primer's base tier keep ms-literal names below a semantic layer, which is the three-tier shape already in 18.

**Composites are emerging, but they are not uniform.** Four systems now bundle duration with easing:

- the DTCG `transition` type;
- Primer `motion.transition.*`;
- Carbon surfaces;
- Atlassian `motion.<component>.<phase>`.

Only Atlassian and Carbon go further and add keyframes, which pushes the composite toward a *pattern*.

### Where it diverges

**Springs as first-class tokens.** Only Material 3 tokenises springs, and it does so directly from generated token files (`StandardMotionTokens.kt` and `ExpressiveMotionTokens.kt`, header "VERSION: v0_14_0, GENERATED CODE"). Apple ships spring presets at platform level. Every web system surveyed either has no springs or bakes them into `linear()` (Atlassian, Open Props), which loses interruptibility (see 4 and 6). Our three spring presets already put us ahead of every web-first system and level with M3 in kind, though not in coverage.

**The values behind shared names.** "Fast" is 70ms in Carbon, 150ms in Fluent, and 50–200ms across M3's Short tier. Names do not travel between systems, which matters for brand-portable generation: our names should be ours, not borrowed.

**Investment direction.** Atlassian is building motion up: early access, a feature flag, and old variables "soon deprecated". Spectrum 2's token data has dropped it. Carbon is moving from primitives toward recipes.

### Brand-defined curves vs. presets

Only two systems formally let a brand supply its own physics:

- **M3.** `MotionScheme` is an interface, and the source says the built-ins "can be used as-is or customized". The M3 Expressive blog shows a custom "playful" scheme.
- **Apple.** Presets plus a fully custom `Spring`.

Carbon accepts custom surfaces, but only built from its fixed primitives. Everyone else ships fixed values that can be overridden only as raw token values, with no guardrails. **No system we found publishes guardrails for brand-authored curves.** This is a gap the practice can fill (see 4).

### How springs are parameterised, and converting between models

| Form | Who uses it | Relationship to mass / stiffness / damping |
|---|---|---|
| dampingRatio ζ + stiffness k (mass = 1 implicit) | Compose, M3 tokens, **our model** | ω₀ = √k; c = 2ζ√k |
| duration + bounce | SwiftUI `Spring(duration:bounce:)`, Motion (`visualDuration` + `bounce`), Reanimated (`duration` + `dampingRatio`), **Figma Motion (bounce only)** | k = (2π / d)²·m; for bounce ≥ 0, ζ = 1 − bounce |
| response + dampingFraction | SwiftUI `Spring(response:dampingRatio:)`, `Animation.spring(response:dampingFraction:)` | k = (2π / response)²·m; c = 4π·ζ·m / response |
| mass + stiffness + damping | SwiftUI, Reanimated physics mode, Figma *prototype* custom spring, most JS libraries | native |
| settlingDuration + dampingRatio + epsilon | SwiftUI | depends on the cutoff tolerance |
| baked `linear()` samples | Atlassian, Open Props, Figma Dev Mode export (reported in DTCG #429) | **not invertible** |

**Sources for the conversions.**

- **Verified.** Apple documents bounce on a −1 to 1 range: 0 is critically damped, 1 is undamped, negative is overdamped. Apple also calls duration "perceptual … approximately equal to the settling duration" (Apple `Spring` docs).
- **Verified.** Compose's simulation source sets `naturalFreq = sqrt(stiffness)` and `c = 2·naturalFreq·dampingRatio`, so Compose and M3 assume mass = 1.
- **Verified.** Figma's `physicalSpringToNormalized` returns bounce = 1 − ζ *(live API test, 2026-10-14)*. DTCG #429 commenters report the same relationship.
- **Derived.** The WWDC23 "Animate with springs" session shows a conversion snippet, but its damping line as rendered in the transcript does not reduce to critical damping at bounce 0. The physics-consistent form in the table is our derivation, consistent with Apple's documented semantics. It is **UNVERIFIED as Apple's exact internal implementation**.

**Worked conversion: M3's spring tokens in duration + bounce terms.** Duration is computed as 2π/√k (mass 1) and bounce as 1 − ζ. This is the conversion our pipeline needs for Figma and SwiftUI.

| M3 token | ζ / k | ≈ duration (s) | bounce |
|---|---|---|---|
| Expressive FastSpatial | 0.6 / 800 | 0.222 | 0.40 |
| Expressive DefaultSpatial | 0.8 / 380 | 0.322 | 0.20 |
| Expressive SlowSpatial | 0.8 / 200 | 0.444 | 0.20 |
| Standard Fast / Default / Slow Spatial | 0.9 / 1400, 700, 300 | 0.168 / 0.237 / 0.363 | 0.10 |
| Effects Fast / Default / Slow (both schemes) | 1.0 / 3800, 1600, 800 | 0.102 / 0.157 / 0.222 | 0 |

Two things follow.

**ζ + k is lossless; duration + bounce is lossy at the edges.** Our source format (ζ + k) converts without loss into every other form except baked `linear()`. Going the other way, Figma's normalised bounce runs only 0–1 *(live API test)*, so it cannot represent **overdamped** springs (ζ > 1). Apple can, through negative bounce. Our model should either forbid ζ > 1 or accept that Figma clamps it.

**Duration + bounce is the perceptual form designers tune by eye.** The field is converging on it as the authoring surface: SwiftUI, Motion, Reanimated's duration mode, Figma Motion, and the shape proposed in DTCG #429. ζ + k remains the most portable storage format.

---

## 2. Pattern-level motion: presets for components and transitions

### Do systems ship named patterns?

Yes, but almost always **as code, not as tokens**.

**Material** (MDC Android `Motion.md`). Four transition classes form an interaction-type taxonomy:

| Pattern | Use |
|---|---|
| `MaterialContainerTransform` | container → container |
| `MaterialSharedAxis` (X / Y / Z) | spatially or navigationally related screens |
| `MaterialFadeThrough` | unrelated destinations |
| `MaterialFade` | in-screen enter and exit: dialogs, menus, snackbars, FABs |

Each pattern is a primary provider plus a secondary provider:

- shared-axis X/Y = slide + fade-through
- shared-axis Z = scale + fade-through
- fade-through = fade + scale
- fade = fade + scale

Defaults:

- **Container transform.** 300ms enter (`motionDurationLong1`) and 250ms return (`motionDurationMedium2`). Fade mode `IN` (or `THROUGH`), fit mode `AUTO`, scrim `#52000000`. Exposed thresholds cover fade, scale, scale-mask and shape-mask.
- **Fade.** 150ms in and 75ms out, linear.
- **Shared-axis direction pairing is manual.** The developer must reverse it on back.

**Fluent UI React v9** has the most explicit pattern layer in the survey.

- `@fluentui/react-motion` provides `createMotionComponent` (one-way) and `createPresenceComponent` (enter/exit pair).
- `react-motion-components-preview` ships **atoms**: blur, fade, rotate, scale, slide.
- It also ships **presence components**: Blur, Collapse, Fade, Rotate, Scale, Slide, plus `choreography/Stagger`.
- An atom specifies direction, duration, easing, delay, translate out/in values, and keyframe reversal on exit.
- `Collapse` specifies separate size and opacity durations for enter and exit, a `staggerDelay` between size and opacity, `orientation`, and `outSize`.
- **Tempo is expressed as named variants**, not multipliers: `CollapseSnappy` (durationFast), `CollapseRelaxed` (durationSlower), `CollapseDelayed` (opacity trails size).
- The preview package is reported as not production-ready (UNVERIFIED on a rendered page).

**Carbon** treats choreography as written guidance, not code:

- paths follow the grid and never run diagonally;
- the same semantic style applies across components (a table-row expand and a dropdown open share productive / entrance-standard easing but differ in duration by size);
- stagger is 20ms within a 500ms total;
- entrance order is fixed: shell → body → dynamic data → primary action → data viz.

The new "surfaces" on `main` move Carbon toward code recipes (UNVERIFIED whether they have shipped in a release).

**Atlassian** is the one system that puts patterns *in the token layer*. `motion.popup.enter.bottom`, `motion.flag.reposition` and `motion.sidenav.exit.left` each bundle duration, curve, keyframes and fill.

**Platform primitives.** Patterns are increasingly provided by the platform itself:

- **SwiftUI:** `matchedGeometryEffect` and `NavigationTransition.zoom(sourceID:in:)` (iOS 18).
- **Compose:** `SharedTransitionLayout` with `Modifier.sharedElement()` (hero) and `Modifier.sharedBounds()` (container transform, with `resizeMode`).
- **Web:** the View Transitions API (`view-transition-name` / `-class`, cross-document `@view-transition`, and transition types via `:active-view-transition-type()`). The default is a cross-fade.

A system's job on these platforms is to supply the *tokens and the pattern parameters*, not to re-implement the mechanism.

### What a pattern specifies

Across Material, Fluent, Atlassian and Carbon, a pattern definition reduces to a stable set of fields:

1. **Trigger / phase:** enter, exit, state change, reposition, navigate.
2. **Animated properties.** Each property has from/to values (opacity 0→1; translate 8px from bottom; scale 0.92→1) and its own timing. Fluent's `Collapse` and Material's primary/secondary split both encode per-property timing.
3. **Timing reference:** a duration token plus an easing token, or a spring token.
4. **Asymmetry:** exit faster than enter (Material fade 150/75; Atlassian "exits are faster").
5. **Choreography:** stagger interval, ordering, and a total-time cap.
6. **Direction semantics:** axis, and whether direction reverses on back.
7. **Reduced-motion alternative** (Fluent's `reducedMotion`; see 5).

This is close to the eight-field spec in 21. The difference is that a pattern binds those fields **once per interaction type**, not once per component instance.

### How patterns stay brand-tunable

Two levers exist in the field. Neither is a global tempo multiplier.

**Scheme swap.**

- M3 `standard` vs `expressive` (or a custom `MotionScheme`), chosen at product level.
- Carbon productive vs expressive curve families.

The pattern references a *role* ("fast spatial spring", "entrance easing") and the scheme resolves it. This lets one pattern library serve many brands without re-authoring.

**Named tempo variants** (Fluent's Snappy / Relaxed). These suit a component library but multiply surface area.

**No system documents a global duration multiplier as a brand lever.** The only multipliers in the field are *user* settings: Android's `ANIMATOR_DURATION_SCALE` and Compose's `MotionDurationScale`. A brand "tempo" multiplier is therefore a practice invention. If we adopt one, it should scale the **duration scale primitives** (and spring stiffness by 1/tempo²). It should not touch per-pattern values, so that patterns inherit the change through aliases.

### Which layer should patterns live in?

| Layer | Holds | Field evidence |
|---|---|---|
| Token primitives | duration, easing, spring values | universal |
| Token semantic / scheme | roles (enter, exit, emphasized; spatial vs effects), resolved per scheme or mode | M3, Carbon, Fluent, Atlassian, Primer |
| **Motion pattern layer** | recipes: properties, distances, scale, opacity, per-property timing, stagger, reduced-motion alternative | MDC transition classes, Fluent atoms and presence components, Carbon surfaces, Atlassian composite tokens |
| Component | which pattern it uses and any override | Fluent `CollapseSnappy`; Material "fade for dialogs" |

**Consensus: a separate motion pattern layer** sitting between tokens and components. Atlassian is the outlier that collapses patterns into the token namespace, and it is in early access with "frequent breaking changes".

DTCG #429 reached the same conclusion from the format side: named patterns were dropped as "a naming convention, not a type". The practical reading is that a pattern is a **structured spec that references tokens**. It can be serialised as JSON next to the tokens and rendered into code and into Figma, but it should not be expected to fit a DTCG token type.

---

## 3. Figma's native motion tooling, late 2026

All claims in this section are dated 2026-10-14. This area changes monthly. **Verification path:**

- `npm pack @figma/plugin-typings`, currently 1.141.0, published 2026-10-05. Grep `plugin-api.d.ts` for `VariableResolvedDataType`, `MotionEasing`, `VariableScope`, `SimpleTransition` and `CustomAnimationStyle`.
- The Plugin API changelog: Update 133 (2026-08-05) and Update 140 (2026-09-30).
- The Figma Learn articles listed in References.

**Where Figma's own pages disagree, prefer the help center and the changelogs.** The launch blog and figma.com/motion still say "custom styles coming soon" and list pre-Lottie export formats.

### Status and availability

- **Launch.** "Introducing Figma Motion: Your canvas now has a timeline" (Figma blog, **2026-06-24**) says "Motion is in open beta". Figma presented it as a Config 2026 headline (Config recap post).
- **Still open beta.** Every Motion help article still carries the beta banner. **No GA date found** (UNVERIFIED).
- **Plan availability is inconsistent across Figma's pages.**
  - The help center says Motion, presets, easing and animated components are available "on any plan" to can-edit users.
  - The blog says Starter gets "limited exports", and that "full design system integration and the Figma agent for motion require paid plans".
  - Exports above 1920×1080 or above 30fps are paid-only.
  - Dev Mode handoff needs a paid plan and a Full or Dev seat.
- **Sept 30, 2026 update** (official forum, Product Updates): custom animation styles, audio, text animations, and Lottie export.

### What the timeline and data model express

**Timeline.** It has keyframes, independent keyframe tracks, auto-keyframing while the playhead moves, scrubbing, drag-to-retime, and time-stamped comments.

**Keyframe model** (Plugin API, Beta):

- `ManualKeyframeInput {timelinePosition, easing, value}`.
- Track operations are SET, OFFSET and SCALE.
- Value types are FLOAT, COLOR, TEXT_DATA, VECTOR, BOOL, and several geometry types.
- Keyframeable fields include:
  - geometry: corner radii, stroke weights, width and height, opacity, translation, rotation, scale, **path trim**;
  - auto-layout spacing and padding, and grid gaps;
  - indexed fills, strokes and effects, plus effect sub-fields (offset, radius, spread, noise and others);
  - component-property tracks.
- **All times are in seconds** in the API.

**First-party animation definitions.** `figma.motion.figmaAnimationStyles()` returns `AvailableAnimationStyle[]` with `name`, `styleId` and `props`. The live API test returned **Opacity, Position, Scale, Rotation, Size, Path, TextStagger** *(live API test, 2026-10-14)*.

Figma's docs do not enumerate these names, so they rest on the live test only. Figma's public pages describe the UI presets as "fade, move, and scale" (blog) or "Fade, Rotate, Scale, and Resize" (figma.com/motion). The Sept 30 forum post announces text animation per character, word or line, which is consistent with TextStagger. Path trim is consistent with Path.

**Composite presets.** In the UI, several presets can be applied at once (help: "Animation presets").

**Custom animation styles** (Plugin API Update 140, 2026-09-30):

- `figma.createCustomAnimationStyle()`, `getLocalCustomAnimationStylesAsync()`.
- `node.animationStyles` returns FIGMA or CUSTOM entries; `applyAnimationStyle(id, {type: 'CUSTOM'})`.
- `CustomAnimationStyle` is "a reusable, ordered group of Figma-provided animation styles". It has `animationEntries`, `addAnimationEntryAsync(styleId, props?)` and `removeAnimationEntry(id)`, plus the usual publishable-style members: `key`, `remote`, `getPublishStatusAsync()`, `description`, `documentationLinks`.
- **The style itself carries only `timelineOffset`.** Duration and easing live on each entry.
- **Library styles are read-only.** Entries can be edited only on local styles; calls on remote (library) styles throw.

**Publishing.** The forum post says: "Publish animation styles to your libraries so every file draws from the same sets." Animated components can be published, and instances can edit duration and properties only at the main component.

**Versioning semantics for animation styles beyond ordinary library publishing are undocumented (UNVERIFIED).** That includes what happens to instances when an entry is removed upstream, and whether entry IDs are stable across publishes.

### TIMING and EASING variables

**API surface.** Introduced in Plugin API Update 133 (2026-08-05):

```
VariableResolvedDataType = "BOOLEAN" | "COLOR" | "EASING" | "FLOAT" | "STRING" | "TIMING"
```

**TIMING** is a number stored in **seconds**. The UI shows milliseconds; the help center defines Timing as "Duration in milliseconds", e.g. `500ms`. Confirmed by the help center, the typings, and *(live API test, 2026-10-14)*.

**EASING** is a `MotionEasing` with a `type` from:

- `EASE_IN`, `EASE_OUT`, `EASE_IN_AND_OUT`, `LINEAR`
- `EASE_IN_BACK`, `EASE_OUT_BACK`, `EASE_IN_AND_OUT_BACK`
- `CUSTOM_CUBIC_BEZIER`, carrying `{x1, y1, x2, y2}`
- `GENTLE`, `QUICK`, `BOUNCY`, `SLOW` (built-in springs)
- `CUSTOM_SPRING`, carrying `NormalizedSpring {bounce: 0–1}`
- **`HOLD`**, a step/hold that prototypes lack

**Conversion helper.** `figma.motion.physicalSpringToNormalized({mass, stiffness, damping})` returns bounce, where bounce = 1 − ζ *(live API test; Plugin API figma-motion page)*.

**What binds.** The help center says:

- "Timing variables can be applied to a preset animation's delay and duration in Figma Motion."
- "Easing variables can be applied to animation presets and keyframes."

The typings agree: keyframe `easing?: MotionEasing | VariableAlias`, and `AnimationStylePropValue` includes `VariableAlias`. **Custom animation style entries bind too** *(live API test)*.

Whether TIMING can bind to a manual keyframe's `timelinePosition` is UNVERIFIED. The typings give it as a plain number.

**What does not bind: prototype reaction transitions.**

- `SimpleTransition` and `DirectionalTransition` take `easing: Easing` (the older prototype type, whose spring is *physical* `{mass, stiffness, damping, initialVelocity}`) and `duration: number`. Neither accepts a `VariableAlias` (typings; *live API test*).
- The forum request to apply variables to prototype animation speed has had no staff update since July 2024.
- figma.com/motion lists "smooth screen-to-screen transitions" as *coming soon*. Motion has not yet replaced prototype transitions.

**Scopes.** `VariableScope` in typings 1.141.0 has no timing or easing scopes; all 23 values are FLOAT, COLOR or STRING scopes. Scopes cannot be set on TIMING or EASING *(live API test)*. Note that scopes only filter UI pickers anyway; they never prevented binding.

**Modes.** The launch blog shows switching mode at page level so "every animation referencing that variable updates at once". The help article does not address modes for motion variables explicitly. A July 2026 community thread shows teams using Standard / Expressive / Smooth modes; that is community practice, not documentation.

**REST API.** The Variables types page still lists `resolvedType` as `BOOLEAN | FLOAT | STRING | COLOR` only. **REST support for TIMING and EASING is undocumented.** Treat it as unsupported until tested: GET `/v1/files/:key/variables/local` on a file that contains motion variables.

This matters for any pipeline that syncs through REST rather than a plugin.

### Handoff surfaces

**Dev Mode.** The Inspect panel has a **Motion tab** with a read-only timeline and a Code section. The code target defaults to CSS, with React and JSON options. The blog and the hub article also claim motion.dev; the dedicated handoff article lists only CSS, React and JSON (verify in the live panel). **No SwiftUI or Compose output found** (UNVERIFIED / apparently not offered).

**MCP server.** `get_motion_context` returns "keyframe animation data for an animated node so agents can faithfully recreate motion in code". Per the live tool schema, that means an animated-node inventory, keyframe tracks with easing, pre-computed CSS `@keyframes` and motion.dev snippets, and timeline coordination hints. An `export_video` tool (MP4 only) appears in the live toolset but not on the public tools page.

**Code Connect for motion.** No primary source mentions it (UNVERIFIED / not offered).

**Export.** MP4, WebM, GIF, SVG, **Lottie** (raw JSON, one animation per file) and **dotLottie** (multiple animations). Lottie limits: shaders, video and angular gradients rasterise; shadows, noise and glass export only partially (first frame).

### How a token pipeline should map onto Figma Motion

| Our token | Figma target | Notes |
|---|---|---|
| Duration scale (ms) | TIMING variables | **Write seconds through the API.** The UI shows ms. An off-by-1000 bug here is the most likely pipeline defect. |
| Duration semantic roles | TIMING variables aliasing primitives | Aliasing works like other variable types. Confirm cross-collection aliasing for TIMING in a spike (UNVERIFIED). |
| Reduced-motion duration twins | A **mode** on the semantic collection (e.g. `default` / `reduced`) | Modes switch every bound animation at once (blog). Twins-as-modes is cleaner than twins-as-separate-tokens in Figma, but code still needs them addressable (see 5). |
| Cubic-bezier curves | EASING `CUSTOM_CUBIC_BEZIER` | Lossless. Y may overshoot (DTCG and CSS both allow it); confirm Figma accepts y outside 0–1 (UNVERIFIED). |
| Easing roles (default / enter / exit / emphasized) | EASING variables aliasing the primitive curves | Brand personality = modes on this collection (e.g. `productive` / `expressive`). |
| Springs (ζ, k) | EASING `CUSTOM_SPRING {bounce}` **plus** a paired TIMING variable for perceptual duration | Figma stores only bounce, so **stiffness has no home in the easing value**. Emit duration ≈ 2π/√k as a sibling TIMING token and bind both. Whether Figma's spring duration means perceptual or settling time is **UNVERIFIED**; test against `Spring(duration:bounce:)` playback. ζ > 1 cannot be represented. |
| Composite transition (duration + easing) | **No variable type.** Closest vehicle is a custom animation style entry with bound TIMING + EASING. | See below. |
| Scopes | None available for TIMING/EASING | Accept picker noise. Rely on naming and collection structure instead. |
| Prototype transitions | **Not bindable** | Writing prototypes from tokens means the pipeline must write literal values and re-run on token change. Prototype springs are *physical* (mass / stiffness / damping), so they need the inverse conversion. |
| Publishing | Variables publish through libraries as usual | Motion variables are not readable through REST (above), so the sync must be plugin-side. |

### Are custom animation styles a sound vehicle for system motion patterns?

**Yes, as the Figma-side rendering of a pattern, with clear limits.** It should not be the pattern's source of truth.

**What fits:**

- a named, published, reusable group of first-party animations ("Dialog enter" = Opacity + Scale + Position entries);
- each entry's duration and easing bound to our TIMING and EASING variables, so scheme and mode switching flows through;
- a per-entry offset, which gives per-property timing and simple stagger within one style.

**What it cannot carry:**

1. **Trigger semantics.** On mount, on scroll into view, after another animation: Motion is timeline-based, not event-based.
2. **Interruption or velocity behaviour.**
3. **Reduced-motion alternatives as a structural pair.** A mode can swap values, but it cannot swap a Position entry for an Opacity entry. A separate "Dialog enter / reduced" style would be needed, and a designer must pick it manually.
4. **Choreography across components.** Each style applies to a node.
5. **Scroll or progress timelines.**
6. **Anything outside the first-party definitions** (no custom property tracks inside a style).
7. **Overrides on library styles.** Remote styles are read-only, so the only way to tune per-file is detaching.

**Versioning.** Behaviour is undocumented beyond ordinary library publishing. Treat a breaking change to a pattern style (removing an entry) as a library major and test what consumer instances do before relying on it.

**Prototypes.** Custom animation styles do not drive prototype transitions, so an interactive prototype of "Dialog enter" still uses the unbound Smart Animate path.

**Recommendation.** Author patterns in our structured pattern spec, then *generate* both the code recipe and the Figma custom animation style from it. Generating Figma styles is newly possible since 2026-09-30.

### Where other tools fit

- **Lottie / dotLottie.** Now a native Figma Motion export target, with the limits above. dotLottie state machines (inputs, states, transitions) are portable across web, iOS, Android, Flutter and RN runtimes, but the LottieFiles docs say they are "still in development". Plain Lottie JSON drops state machines and themes. **Use for illustration and brand moments, not component motion.**
- **Rive.** Still the answer for **state-driven, interactive, runtime-parameterised** motion (state machines plus data binding / view models). The only Figma route is copy-as-SVG; no Figma Motion import found (UNVERIFIED).
- **Jitter and ProtoPie.** Both have Figma import plugins (Jitter's rebuilt Feb 2025; ProtoPie needs 9.5.0+). Neither carries Figma Motion timelines (UNVERIFIED). ProtoPie remains the strongest tool for **conditional, sensor- and variable-driven prototypes**, which Figma prototypes still cannot bind to motion tokens.
- **Code-first.** motion.dev (MIT; a Dev Mode and MCP export target), SwiftUI previews, Compose previews and Storybook remain the **reference implementation** for springs with interruption, decay, gesture-coupled and scroll-driven motion. Figma can now *describe* much more, but it cannot *demonstrate* these.

---

## 4. The hard cases: what tokens can and can't carry

The inventory of about 105 production animations from a real brand surfaced five shapes our model cannot express. For each we cover the field state and our recommendation.

### Brand-defined easing curves

**Format latitude is total.**

- DTCG `cubicBezier` is `[P1x, P1y, P2x, P2y]`, with x in [0, 1] and **y any real number**.
- CSS Easing allows the same, and `linear()` can express any monotone-in-time curve, including multi-bounce.
- Figma's EASING accepts custom cubic-bezier *(live API test)*.

**No system publishes numeric guardrails for brand curves.** The nearest primary guidance:

- **Apple (WWDC23).** Be "cautious about using values higher than around 0.4" bounce; default to 0 when unsure.
- **M3 encodes guardrails structurally.** Effects springs are always ζ = 1, and spatial ζ never drops below 0.6 even in expressive.
- **Carbon.** None of its curves overshoot. Avoid "unnatural, distracting, or purely decorative" easing.

**Recommendation.** Admit brand curves as **primitives** in a dedicated `easing.brand.*` namespace that semantic roles may alias. Gate them in the generator with practice guardrails. **These are practice positions, not cited standards.**

1. **Role compatibility.** An `exit` alias must accelerate (front-loaded slope low); an `enter` alias must decelerate.
2. **Overshoot cap.** Overshoot only on spatial properties. Cap overshoot so it is equivalent to bounce ≈ 0.4 or less, matching Apple's line. Overshoot on opacity or colour is never allowed, matching M3's effects rule.
3. **Reduced-motion twin.** Every brand curve has a non-overshooting twin.
4. **Provenance.** Curves fitted from a brand's After Effects or Lottie assets carry a source note.

### Scroll-linked and progress-driven motion

**CSS.**

- `animation-timeline` (`scroll()`, `view()`) and `animation-range` ship in **Chrome 115+ and Safari 26**. **Firefox is Nightly only.**
- MDN marks them "Limited availability", **not Baseline**, as of 2026-10-14, and recommends gating with `@supports (animation-timeline: view())`.
- Re-check Firefox release notes and the MDN BCD `animation-timeline.json` before quoting.

**Native.**

- **SwiftUI.** `scrollTransition` / `ScrollTransitionPhase` and `visualEffect` (iOS 17); `onScrollGeometryChange` / `ScrollGeometry` (iOS 18).
- **Compose.** The animation docs recommend deferred-read modifiers (`graphicsLayer {}`); scroll-state-driven patterns are UNVERIFIED in this run.

**Figma Motion has no scroll timeline.** Prototype scroll behaviours are not motion-token bindable.

**WCAG.** The Understanding doc for 2.3.3 names **parallax** and scroll-moved elements as the canonical vestibular triggers.

**Recommendation: a pattern spec, not tokens.** What *is* tokenisable: the effect magnitudes (scale 0.9→1, opacity 0→1, translate distance), the easing applied across the range, and a **parallax ratio ceiling**. The timeline binding, the range (`entry 0% cover 40%`) and the fallback are pattern-level fields.

A scroll-linked pattern must declare:

- its non-scroll fallback (static, or a one-shot reveal on intersection);
- its reduced-motion behaviour, which is **off** by default, given WCAG's explicit naming of parallax.

Declare **continuous parallax as out of scope** for the generated system. It is a bespoke-build feature, not a token.

### Physics beyond spring presets

**Very bouncy springs.** These are representable in every format. ζ down to about 0.2 is Compose's `DampingRatioHighBouncy`; the value is read from the Compose reference and its full constant list is partially UNVERIFIED. The issue is governance, not encoding.

**Recommendation.** Extend the spring set from three presets to a **spatial / effects split**, borrowed from M3. Effects springs are always ζ = 1. Add at most one `expressive`-tier spatial spring with low ζ, behind the overshoot guardrail.

**Inertia / decay after a flick.** Each platform exposes one or two parameters:

- Compose `exponentialDecay(frictionMultiplier = 1f, absVelocityThreshold = 0.1f)` and `splineBasedDecay` (whose parameters are UNVERIFIED);
- Reanimated `withDecay` (`deceleration` 0.998, `rubberBandFactor` 0.6);
- Motion `type: "inertia"` (`power` 0.8, `timeConstant` 700, `bounceStiffness` 500, `bounceDamping` 10);
- React Native ScrollView `decelerationRate` (normal 0.998 iOS / 0.985 Android).

The 0.998 figure is stated on React Native's page as matching UIKit; Apple's own page does not print the raw value (UNVERIFIED there).

**Tokenisable:** a deceleration rate and a rubber-band factor. **Not tokenisable:** the gesture coupling, the velocity source and snap points.

**Recommendation.** Add an optional `motion.decay.{normal, fast}` pair only if a brand's inventory includes custom flick surfaces (carousels, sheets). Otherwise defer to the platform defaults, which are already tuned.

**Interruptible, velocity-preserving motion.** This is an **implementation property**, not a token.

- SwiftUI springs retarget with preserved velocity: "uses the velocity it had when it was retargeted as the initial velocity" (WWDC23).
- Compose springs guarantee velocity continuity (Compose customize docs).
- `UIViewPropertyAnimator` is interruptible, scrubbable and reversible.
- CSS transitions and `linear()` are not velocity-preserving. This is our inference from the CSS model; no single primary sentence states it.

The token's role is to **declare intent**: a pattern field `interruptible: true` tells each platform to use a spring primitive rather than a timed curve.

### Per-property easing within one transition

**Every runtime supports it:**

- CSS comma lists in `transition-timing-function`, mapped index-wise to `transition-property`;
- WAAPI per-keyframe `easing`;
- Motion per-value `transition`;
- Compose per-`animate*AsState` specs, formalised by M3 as **spatial vs effects**;
- Figma per-entry easing inside a custom animation style.

**The DTCG `transition` type carries a single `timingFunction` and no property binding.** The spec's own issue note and #103 question its usefulness for exactly this reason.

**Recommendation.** Do not stretch the composite token. Model per-property easing in the **pattern spec** as a list of `{property, from, to, duration, easing | spring, delay}` tracks. That matches Fluent `Collapse`, Material's primary/secondary providers and Figma's entry model.

The spatial/effects split gives a cheap default rule: spatial properties use the spatial spring or curve; opacity and colour use the effects one.

### Out-and-back (pulse / yo-yo)

**Every runtime has it:**

- CSS `animation-direction: alternate` with an iteration count (standard behaviour; MDN not re-fetched this run);
- Compose `repeatable` / `infiniteRepeatable(…, RepeatMode.Reverse)`;
- SwiftUI `repeatForever(autoreverses:)`, `PhaseAnimator` and `KeyframeAnimator(repeating:)` (iOS 17);
- Reanimated `withRepeat(anim, n, reverse = true)`;
- Motion `repeatType: "reverse" | "mirror"`.

**No token format has it.** DTCG #429 deferred keyframes.

**Recommendation.** A pulse is a **pattern** with fields amplitude, property, duration and easing (or spring), direction mode (alternate / mirror), iteration count (finite by default), and a reduced-motion fallback.

**WCAG 2.2.2 makes iteration count load-bearing.** Anything that loops for more than 5 seconds alongside other content needs pause/stop/hide. The generator should default pulses to finite iterations of no more than 5 seconds total, and flag infinite ones.

---

## 5. Reduced motion and accessibility as architecture

### The normative floor

**WCAG 2.2 SC 2.2.2 Pause, Stop, Hide (A).** Motion that starts automatically, lasts more than 5 seconds, and runs in parallel with other content needs a pause, stop or hide mechanism. There is **no 5-second exception for auto-updating content**. Sufficient techniques include G4, SCR33, G11, G152, SCR22, G186 and G191.

**SC 2.3.3 Animation from Interactions (AAA).** "Motion animation triggered by interaction can be disabled, unless the animation is essential."

- Motion animation is defined as "addition of steps between conditions to create the illusion of movement or to give a sense of a smooth transition".
- **Colour, blur and opacity changes that do not alter perceived size, shape or position are excluded.** That exclusion is the normative basis for *substituting a fade* rather than removing all motion.

**C39** gives two strategies:

- **subtractive:** `prefers-reduced-motion: reduce` removes motion;
- **additive:** `no-preference` adds motion on top of static defaults.

**SC 2.3.1 Three Flashes (A)** is the flash floor; Atlassian and Fluent both cite it. We did not separately fetch it this run.

**What systems operationalise.** Few systems claim AAA, but 2.3.3 is the criterion design systems actually build to:

- Carbon's v12 accessibility spike (#22686, closed 2026-07-22): no parallax, no excessive bounce, under 1 second, reduced-motion fallbacks, a site-wide toggle;
- Atlassian: reduced motion is "off and instant";
- Spectrum: large-area motion must honour the setting;
- Fluent's design guidance.

### How systems encode the alternative

**Fluent UI React v9** is the strongest architecture in the field.

- Every motion atom has an optional `reducedMotion?: Partial<AtomCore>`. Keyframes given there *replace* the normal ones.
- **If none is given, duration is overridden to 1ms.**
- Detection uses `matchMedia("(prefers-reduced-motion: reduce)")` with a live listener.

So: per-pattern substitution, with a safe instant default.

**Reanimated** sets the policy per animation:

- a `ReduceMotion` enum of `System` (the default), `Always` and `Never`;
- under reduce, timing and spring animations jump to the end, and exiting and shared transitions are skipped;
- the documented substitution is `BounceIn` → `FadeIn.reduceMotion(ReduceMotion.Never)`;
- `useReducedMotion()` reads the setting **at app start only**.

**Apple** has two layers:

- `accessibilityReduceMotion` / `UIAccessibility.isReduceMotionEnabled` tells you **whether** to reduce;
- `UIAccessibility.prefersCrossFadeTransitions` (iOS 14+) tells you **what** to substitute.

The SwiftUI environment equivalent for cross-fade is UNVERIFIED. The HIG says: make motion optional, let people cancel motion, and on visionOS avoid peripheral motion, world rotation and sustained oscillation around 0.2 Hz.

**Android** works through scales, not a boolean:

- `ANIMATOR_DURATION_SCALE` and `TRANSITION_ANIMATION_SCALE`; 0 ends animations immediately;
- `ValueAnimator.areAnimatorsEnabled()` (API 26) is also false under **Battery Saver**, a non-accessibility source of "no motion";
- Compose `MotionDurationScale` multiplies durations.

Two points are UNVERIFIED: that the "Remove animations" toggle writes the scales to 0, and that Compose honours the system scale.

**React Native.** `AccessibilityInfo.isReduceMotionEnabled()` also reports true when Android's transition scale is "Animation off". `prefersCrossFadeTransitions()` is iOS-only.

**Web.** `prefers-reduced-motion` is Baseline widely available (since Jan 2020), with a `Sec-CH-Prefers-Reduced-Motion` client hint for servers. Chrome's View Transitions guidance notes that "reduced motion" does not mean "no motion". Media Queries 5 siblings: `prefers-reduced-transparency`, and `prefers-reduced-data` (open fingerprinting issue).

### Mapping to tokens, Figma and code

Our model's reduced-motion **duration twins** are necessary but not sufficient. The field evidence (Fluent, Reanimated, Apple's cross-fade preference, WCAG's definition) says the alternative is a **substitution of properties**, not only a change of value.

| Layer | Reduced-motion encoding |
|---|---|
| Token primitives | Unchanged. |
| Token semantic | `reduced` **mode** on durations (collapse spatial durations; keep short effects durations) and easings (non-overshooting twins). Springs: effects-only ζ = 1. In code these are addressable as twins; in Figma they are a mode. |
| Pattern | **Required `reducedMotion` field per pattern.** Default rule: spatial tracks (translate, scale, size, path, rotation) are dropped or replaced by an opacity cross-fade; effects tracks (opacity, colour) stay with reduced duration. `essential: true` exempts with justification (progress indicators, for example). |
| Component | Inherits from the pattern. Override only with a recorded reason. |
| Runtime | Web: additive C39 pattern where feasible. iOS: honour `prefersCrossFadeTransitions` by picking the cross-fade substitute. Android: respect scale 0 and `areAnimatorsEnabled()`. RN: `ReduceMotion.System` default, with explicit `FadeIn` substitutes. |
| Figma | A `reduced` mode on motion variables handles value twins. **Property substitution needs a separate "/ reduced" custom animation style** per pattern, because a mode cannot swap an entry's animation type. This is a Figma gap to document, not to solve. |

**Mapping M3's spatial/effects split onto reduced motion is our inference.** No source states it. But it aligns exactly with WCAG 2.3.3's exclusion of opacity and colour, which makes it a defensible practice default.

**Vestibular triggers to flag in the generator:**

- large-area scale or zoom, and panning (MDN);
- parallax and scroll-moved elements (WCAG 2.3.3 Understanding; Carbon);
- large-area sweeps and rapid oscillation (Atlassian);
- peripheral motion, world rotation, about 0.2 Hz oscillation (Apple HIG, visionOS);
- spins, which Polaris ships as a keyframe token.

Whether Apple's iOS HIG names zoom, spin and parallax explicitly is UNVERIFIED.

---

## 6. Platform delivery

### The format layer: DTCG as of 2026-10-14

**Design Tokens Format Module 2025.10** is a *Final Community Group Report*, dated **28 October 2025**. It is described as stable, but it is a CG report, not a W3C Recommendation. Motion types:

- **`duration`:** an object `{ "value": number, "unit": "ms" | "s" }`.
- **`cubicBezier`:** `[x1, y1, x2, y2]`, with x in [0, 1] and y unrestricted.
- **`transition`** (composite): `duration`, `delay`, `timingFunction`, each a value or an alias. The spec carries a non-normative note questioning whether `transition` is useful, since it binds no property and no start or end states.

There is **no spring, steps, linear(), keyframe or animation type**, normative or in "additional types".

**Community activity:**

- **#158**, "Animation description by solely Bezier Curve is inadequate" (open since 2022). A July 2026 maintainer comment says the animation module is "next on the roadmap" and that springs are clearly wanted. The open question is which math to standardise.
- **#429**, "Motion beyond `transition`" (opened 2026-06-28, active through 2026-08-29). It narrowed to a `spring` type of `{bounce, duration}`, with optional physics and a fallback cubicBezier or sampled `linear()`. Keyframes were deferred, and named patterns dropped as "a naming convention, not a type".
  - The unresolved blocker is **the definition of "stopped"**. The same spring measures 780ms or 1380ms depending on the cutoff, so the spec must pin tolerance, method and reference.
  - A contributor invited a draft. No timeline.
- **#103**, "Transition type feedback" (open, last activity 2023). It asks to rename `timingFunction` to `easing`, notes that `steps()` is inexpressible, and requests per-keyframe easing and spring/bounce/elastic presets.
- **#342** proposes bare-number durations; a maintainer recommended against it for compatibility with 2025.10.
- No dedicated issue exists for `steps()` or `linear()` easing.

**Reading.** A DTCG spring type is likely to land in the shape **`{bounce, duration}`**, which is the same shape as SwiftUI, Motion and Figma. It is not landing soon. If we store springs as ζ + k now, we should also be able to *emit* `{bounce, duration}` with a declared settling-tolerance convention, so that migration is a transform, not a re-model.

### The transform layer: Style Dictionary and Tokens Studio

**Style Dictionary v5.6.1** has three built-in motion transforms: `time/seconds`, `cubicBezier/css` (which also handles a transition's `timingFunction`) and `transition/css/shorthand`. **They are only in the css, scss and less transform groups.** The js, android, compose, ios, ios-swift, flutter and react-native groups have **no motion transforms**.

The source has two specific defects:

- `time/seconds` filters on `$type === 'time'`, **not DTCG `duration`**, and assumes a bare ms number;
- `transition/css/shorthand` carries `// TODO: add support for DTCG duration object value type`.

**DTCG 2025.10 duration objects therefore do not round-trip through stock Style Dictionary.** Re-check on the next SD release.

**Tokens Studio.** Its 24 token types include no duration, easing, transition or motion type, and sd-transforms has no motion transforms.

**The workaround the field uses** (and we should use): custom transforms per platform, keyed on DTCG `$type` plus an `$extensions` namespace for spring and pattern data. Our generator already owns the transform layer, so this is a cost we already pay rather than a new dependency.

### Per-platform delivery

**CSS.**

- Durations become `ms` custom properties and curves become `cubic-bezier()`.
- **Springs reach CSS only as sampled `linear()`.** `linear()` has been Baseline widely available since **December 2023** (Chrome 113, Firefox 112, Safari 17.2).
- CSS Easing Level 2 (ED, 23 Feb 2026) specifies **no `spring()` function**.
- Generators: the Archibald/Argyle linear-easing generator (also in Chrome DevTools since 114), and a perceptual-duration + bounce spring generator at kvin.me (author attribution UNVERIFIED). The latter emits the easing plus a *separate, longer* duration: 500ms perceptual at 30% bounce gave 0.8333s.

Costs of the `linear()` route:

- a fixed duration that must be emitted as a **paired token**;
- no velocity preservation on interruption;
- precision that depends on the number of stops;
- a non-invertible result.

**Emit the spring source parameters alongside** (as JS or JSON) for JS-driven runtimes such as motion.dev, whose `spring()` takes `visualDuration` + `bounce` or stiffness/damping/mass.

**iOS / SwiftUI.**

- Emit `Spring(duration:bounce:)` (perceptual), or `Spring(mass:stiffness:damping:)` for exactness.
- Curves become `Animation.timingCurve(…)`; durations become `TimeInterval` seconds.
- Springs are SwiftUI's default animation and retarget with velocity.
- UIKit's `UIViewPropertyAnimator` takes `dampingRatio` directly.

**Android / Compose.**

- Emit `spring(dampingRatio, stiffness)`. This is **our storage format verbatim**, and M3 itself generates its springs this way.
- Curves become `CubicBezierEasing`; durations become `tween(durationMillis, …)`.
- For M3-based apps, the highest-leverage output is a **custom `MotionScheme` implementation** that maps our semantic springs onto M3's six slots. That flows our brand motion into every Material component without touching components.

**React Native / Reanimated 4.**

- `withSpring` takes physics (`mass`, `stiffness`, `damping`) **or** `duration` + `dampingRatio`; the duration form wins if both are set.
- Reanimated's `duration` is perceptual, and the actual run is 1.5×.
- `withTiming` takes `Easing.bezier(…)`.
- `reduceMotion` is per animation.
- Emit the physics form for parity with Compose.

**Flutter** (not in scope, noted). `SpringDescription(mass, stiffness, damping)` takes the physics form. We did not verify it this run.

### Where stock tooling falls short, summarised

| Gap | Where | Workaround |
|---|---|---|
| No spring type | DTCG 2025.10 | `$extensions` spring object; plan for a `{bounce, duration}` migration (#429) |
| No pattern / keyframe type | DTCG (deferred in #429) | Pattern spec as a sibling JSON file referencing tokens |
| `transition` has one easing, no property binding | DTCG | Pattern tracks |
| Duration object not consumed | Style Dictionary 5.6.1 `time/seconds`, `transition/css/shorthand` | Custom transform |
| No native motion output | SD transform groups beyond CSS | Custom formats per platform |
| No motion token types | Tokens Studio | Bypass; write Figma variables from our generator |
| TIMING/EASING not in REST | Figma REST Variables API | Plugin-side sync |
| Prototype transitions unbindable | Figma | Write literal values; re-sync on change |
| Springs as baked curves | CSS | `linear()` + paired duration + source params for JS runtimes |

---

## 7. Recommendations for a generated token system

### Verdict on the current model

The model is **on target at the token tier and ahead of most of the field on springs**. It has a duration scale with semantic roles and reduced twins, named cubic-beziers with a role tier, ζ + k springs, and duration + easing composites.

It is **missing a pattern tier**, and that is where four of the five inventory gaps actually belong.

### Keep

- **The duration scale plus semantic roles.** Keep the step count in the 6–10 range. Our names are ours; do not borrow Carbon's or Fluent's numbers.
- **Named curves plus the role tier** (default / enter / exit / emphasized). This matches the field's four-role convergence; "emphasized" is our intensity axis.
- **ζ + k as the spring storage format.** It is lossless to every target except baked `linear()`, and identical to Compose and M3's generated tokens.
- **Reduced-motion duration twins.** Reframe them as a `reduced` mode in Figma and as addressable twins in code.
- **Composite transitions, demoted.** Keep them as convenience aliases for single-property cases, mirroring Primer's `motion.transition.*`. Stop expecting them to carry multi-property motion; that moves to patterns.

### Add (in priority order)

1. **A motion pattern tier.** A structured spec per pattern:
   - `phase`;
   - `tracks[]` of `{property, from, to, duration | spring, easing, delay}`;
   - `choreography` (stagger, order, total cap);
   - `direction` (axis, reverse-on-back);
   - `interruptible`;
   - `reducedMotion` (substitute tracks, or `essential` with reason);
   - `platformHints`.

   It is generated into code recipes per platform and into Figma **custom animation styles**, with entries bound to our TIMING and EASING variables. It is serialised outside DTCG, as a sibling file referencing tokens. That is the shape Fluent, Material and Carbon surfaces converge on, and the shape DTCG #429 explicitly declined to standardise.

2. **The spatial vs. effects spring split.** Change the three presets into {fast, default, slow} × {spatial, effects}, with effects always ζ = 1. This gives per-property easing a default rule, gives reduced motion a default rule, and maps 1:1 onto M3 `MotionScheme`.

3. **A scheme or mode lever for personality**, e.g. `productive` / `expressive`. Implement it as modes on the semantic easing and spring collections, in the shape of M3 `MotionScheme` and Carbon productive/expressive. This is the brand-tunable lever. A **global tempo multiplier is optional** and is a practice invention; if added, it scales primitives only, with stiffness ∝ 1/tempo².

4. **A brand curve namespace with generator guardrails**, as in 4: role-shape checks, overshoot only on spatial properties at no more than bounce ≈ 0.4, a non-overshooting reduced twin, and source provenance.

5. **Spring emission in duration + bounce form** with a declared settling convention. It is needed for Figma (bounce + paired TIMING), SwiftUI, Motion and the likely DTCG shape. Document the cutoff tolerance used.

6. **Optional decay tokens** (`deceleration`, `rubberBand`). Generate them only when the brand inventory includes custom flick surfaces.

### Declare out of scope

These are explicitly not token-layer concerns. Say so in the system docs so the absence reads as a decision.

- **Continuous scroll-linked and parallax motion.** Scroll-*triggered* reveals are a pattern with a mandatory static fallback and reduced-motion off. Continuous parallax is bespoke. CSS support is not Baseline (Firefox), and WCAG names parallax as the canonical trigger.
- **Gesture-coupled physics** (drag, fling, snap points, rubber-banding beyond a factor). This is implementation; the pattern declares intent via `interruptible`.
- **Illustrative and brand-moment animation.** That is Lottie/dotLottie (now exportable from Figma Motion) or Rive for interactive state machines. Our system supplies colour and timing tokens these assets *should* reference, but does not generate them.
- **Infinite loops by default.** Pulses are finite patterns. Infinite loops need an explicit 2.2.2 control.
- **Overdamped springs (ζ > 1).** Figma cannot represent them, and the field does not use them in UI tokens.

### Decision frameworks where context matters

**Where should a reduced-motion alternative live?**

- *Value-only change* (shorter, no overshoot): a token mode.
- *Property change* (movement → fade): a pattern field.
- *Platform offers a finer signal* (iOS cross-fade): runtime picks the pattern's substitute.

**Should a motion be a token, a pattern or out of scope?**

- **Token:** a single scalar or curve reused across contexts.
- **Pattern:** more than one property, has a phase, or needs choreography or a reduced substitute.
- **Out of scope:** depends on continuous input (scroll position, gesture velocity), *or* it is authored as an asset.

**Spring vs. curve for a given pattern.** Use a **spring** if the motion is user-initiated, can be interrupted, or must feel physical. Use a **curve** if it is system-initiated, fixed-length, must sync with other timed media, or targets CSS-only consumers where `linear()`'s fixed duration is acceptable.

**Figma-side vehicle.**

- **Variables:** anything a mode should switch.
- **Custom animation style:** a named pattern designers apply.
- **Animated component:** when the motion is inseparable from the component's structure.
- **Prototype transitions:** only for flows. Accept literal values until Figma binds variables there.

### A minimum viable motion pattern set

These are ordered by coverage of a typical component library and by how many components each unblocks.

1. **Fade (enter / exit).** Tooltips, popovers, toasts, skeleton-to-content. It is also the universal reduced-motion substitute, so build it first.
2. **Pop / scale-fade (enter / exit).** Menus, popovers, selects, comboboxes: anchored surfaces. Scale about 0.95→1 plus fade, effects/spatial split.
3. **Dialog (enter / exit).** Modal and scrim choreography (scrim effects, panel spatial), with an exit faster than the enter.
4. **Slide / sheet (enter / exit, by edge).** Drawers, bottom sheets, side navigation. Spring-driven and interruptible.
5. **Expand / collapse.** Accordion, disclosure, tree. Separate size and opacity tracks, after Fluent `Collapse`.
6. **Toast / notification (enter, exit, reposition).** Stack reflow is the first choreography case.
7. **State change / press feedback.** Buttons, switches, checkboxes, tabs indicator. Effects-only plus a small spatial spring.
8. **Page / view transition.** Shared axis plus fade-through, mapping onto View Transitions, Compose and SwiftUI navigation transitions.
9. **Container transform / shared element.** Last, because every platform now provides the mechanism (`sharedBounds`, `.zoom`, View Transitions). The system supplies only timing and the reduced substitute.
10. **Pulse / attention** (finite). Only once 2.2.2 handling is in place.

**Stagger** is a choreography field on patterns 5, 6 and 8, not a pattern of its own. Use Carbon's figures as the default: 20ms interval within a 500ms total.

---

## What this run supersedes

Things have changed since the May 2026 runs (`_research/_inbound/2026-05-14-motion-foundations-and-spec/`, `-implementation-web/`, `-implementation-mobile/`) and `21-motion-spec-and-handoff`. Synthesis should treat the following as superseded.

1. **"Figma is structurally inadequate for spec'ing micro-interactions"** (21, §"Why Figma is currently inadequate"; May foundations run). **Superseded in large part.** Figma Motion (open beta from 2026-06-24) adds a timeline, keyframes, first-party animation definitions, publishable custom animation styles (2026-09-30), and TIMING/EASING variables that bind to them. Figma can now *specify* timed and spring motion with token-bound values.

   What remains true:
   - no trigger semantics;
   - no interruption model;
   - no scroll timeline;
   - prototype transitions are not variable-bindable;
   - no cross-component choreography.

   The diagnosis should narrow from "structurally inadequate" to "adequate for specifying timed motion; inadequate for behaviour".

2. **"Easing is a closed set of presets"** (21, point 3). **Superseded.** EASING supports custom cubic-bezier, built-in and custom springs, and HOLD, all bindable to variables.

3. **"Reduce-motion does not exist as a model"** (21, point 4). **Partially superseded.** Variable modes can now carry reduced value twins. Property substitution still needs a separate style.

4. **"The Figma MCP server's motion variables surface … surfaces tokens to agents but does not yet surface per-component motion specs"** (21). **Superseded.** `get_motion_context` returns keyframe tracks, easing and pre-computed CSS/motion.dev per animated node.

   The May external run's claim of a "70% reduction in design-to-dev cycle" was never sourced and should not be carried forward.

5. **"Dev Mode … shows duration and easing preset names, not values"** (May foundations run). **Superseded.** The Motion tab emits CSS, React and JSON. SwiftUI and Compose are still absent.

6. **"The DTCG motion module is at draft-final stage as of May 2026"** (May web run, external). **Incorrect then and now.** DTCG 2025.10 (Oct 2025) is final with only `duration`, `cubicBezier` and `transition`. Springs are "next on the roadmap" (#158, Jul 2026) with no draft.

7. **Pattern A vs. Pattern B** (21). **Not superseded, but the bridge has moved.** 21 said a plugin emitting Pattern B from Figma authoring "does not yet exist". The Plugin API can now *write* custom animation styles and read keyframes, so the reverse direction (generating Figma Motion from a Pattern B spec) is buildable today.

   We recommend Pattern B as source, generated into Figma. This strengthens 21's recommendation rather than reversing it.

8. **The Lottie vs. Rive boundary** (21, 19, 20). It holds, with one addition: Figma Motion now exports Lottie/dotLottie natively, which moves simple Lottie authoring into Figma.

---

## Open and unverified items

- The first-party definition names (Opacity, Position, Scale, Rotation, Size, Path, TextStagger) rest on the live API test only; Figma's docs do not enumerate them.
- Whether TIMING can bind to keyframe `timelinePosition`.
- Whether Figma EASING accepts cubic-bezier y outside [0, 1].
- Whether Figma's spring duration is perceptual or settling time.
- Cross-collection aliasing for TIMING/EASING.
- REST API support for TIMING/EASING (undocumented).
- Library versioning semantics for custom animation styles.
- Figma Motion GA date; plan availability (Figma's pages conflict).
- motion.dev as a Dev Mode target (Figma's pages conflict).
- M3 spec-page text, including whether easing/duration tokens are formally "legacy", and the published ms equivalents for springs. m3.material.io would not render, so values here come from source code.
- Carbon surfaces: shipped in a release, or `main` only.
- Spectrum 2's absence of motion tokens: deliberate or gap.
- Compose `StiffnessHigh` and `StiffnessMediumHigh` values on the reference page; `splineBasedDecay` parameters.
- Android "Remove animations" writing animator scales to 0; Compose `MotionDurationScale` honouring the system scale.
- A SwiftUI environment key for cross-fade preference.
- `UIScrollView.DecelerationRate.normal` = 0.998 on Apple's own page.
- Apple's exact spring conversion (our formula is derived; the WWDC snippet as rendered appears garbled).
- Polaris and GOV.UK reduced-motion implementation.
- Author attribution of the kvin.me spring generator.
- **Practice positions, not cited standards:** the overshoot cap for brand curves, the global tempo multiplier, and the spatial/effects → reduced-motion mapping.

---

## References

All accessed 2026-10-14.

**Figma**
- Introducing Figma Motion (blog, 2026-06-24): https://www.figma.com/blog/introducing-figma-motion/
- Config 2026 recap: https://www.figma.com/blog/config-2026-recap/
- Figma Motion marketing page: https://www.figma.com/motion/
- Explore Figma Motion (help): https://help.figma.com/hc/en-us/articles/41274629073303
- Animation presets (help): https://help.figma.com/hc/en-us/articles/41307886266135
- Easing in Figma Motion (help): https://help.figma.com/hc/en-us/articles/41414048690839
- Animated components (help): https://help.figma.com/hc/en-us/articles/41307940738967
- Export animations (help): https://help.figma.com/hc/en-us/articles/41307983648407
- Dev Mode motion handoff (help): https://help.figma.com/hc/en-us/articles/41296356954263
- Variables guide (help; Timing/Easing definitions and binding targets): https://help.figma.com/hc/en-us/articles/14506821864087
- Prototype easing and spring animations (help): https://help.figma.com/hc/en-us/articles/360051748654
- Product update, custom styles / audio / text / Lottie (forum, 2026-09-30): https://forum.figma.com/product-updates-3/motion-adds-custom-styles-audio-text-animations-and-lottie-export-58554
- Plugin API, Motion types: https://developers.figma.com/docs/plugins/api/Motion/
- Plugin API, `figma.motion`: https://developers.figma.com/docs/plugins/api/figma-motion/
- Plugin API, `figmaAnimationStyles`: https://developers.figma.com/docs/plugins/api/properties/figma-motion-figmaanimationstyles/
- Plugin API, `CustomAnimationStyle`: https://developers.figma.com/docs/plugins/api/CustomAnimationStyle/
- Plugin API, `VariableResolvedDataType`: https://developers.figma.com/docs/plugins/api/VariableResolvedDataType/
- Plugin API, `VariableScope`: https://developers.figma.com/docs/plugins/api/VariableScope/
- Plugin API, `Transition`: https://developers.figma.com/docs/plugins/api/Transition/
- Plugin API Update 133 (2026-08-05): https://developers.figma.com/docs/plugins/updates/2026/08/05/version-1-update-133/
- Plugin API Update 140 (2026-09-30): https://developers.figma.com/docs/plugins/updates/2026/09/30/version-1-update-140/
- REST API variables types: https://developers.figma.com/docs/rest-api/variables-types/
- MCP server tools: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/
- `@figma/plugin-typings` 1.141.0 (npm)

**DTCG and CSS**
- Design Tokens Format Module 2025.10: https://www.designtokens.org/tr/2025.10/format/
- DTCG #158: https://github.com/design-tokens/community-group/issues/158
- DTCG #103: https://github.com/design-tokens/community-group/issues/103
- DTCG #429: https://github.com/design-tokens/community-group/issues/429
- DTCG #342: https://github.com/design-tokens/community-group/issues/342
- CSS Easing Level 2 (ED): https://drafts.csswg.org/css-easing-2/
- MDN `linear()`: https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function/linear
- MDN `animation-timeline`: https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline
- MDN BCD `easing-function.json`, `animation-timeline.json`, `animation-range.json`: https://github.com/mdn/browser-compat-data
- MDN `transition-timing-function`: https://developer.mozilla.org/en-US/docs/Web/CSS/transition-timing-function
- MDN WAAPI keyframe formats: https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Keyframe_Formats
- MDN View Transition API: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
- MDN `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Media Queries Level 5: https://drafts.csswg.org/mediaqueries-5/
- Chrome, CSS `linear()` easing: https://developer.chrome.com/docs/css-ui/css-linear-easing-function
- Chrome, same-document view transitions: https://developer.chrome.com/docs/web-platform/view-transitions/same-document
- Linear easing generator: https://linear-easing-generator.netlify.app/
- CSS spring easing generator: https://www.kvin.me/css-springs

**Tooling**
- Style Dictionary predefined transforms: https://styledictionary.com/reference/hooks/transforms/predefined/
- Style Dictionary transform groups: https://styledictionary.com/reference/hooks/transform-groups/predefined/
- Style Dictionary transforms source: https://github.com/style-dictionary/style-dictionary/blob/main/lib/common/transforms.js
- Tokens Studio token types: https://docs.tokens.studio/manage-tokens/token-types
- Tokens Studio sd-transforms: https://github.com/tokens-studio/sd-transforms
- Motion (motion.dev): https://motion.dev/ ; https://motion.dev/docs/spring ; https://motion.dev/docs/react-transitions
- LottieFiles, Figma Motion export: https://docs.lottiefiles.com/en/integrations/figma/04_figma-to-lottie/figma-motion-export
- dotLottie state machines: https://docs.lottiefiles.com/en/format/dotlottie/interactivity/state-machines
- Rive, copy and paste from Figma: https://rive.app/blog/copy-and-paste-from-figma-to-rive
- Rive data binding: https://rive.app/docs/editor/data-binding/migration-guide
- Jitter Figma plugin: https://jitter.video/changelog/2025-02-26-all-new-figma-plugin/
- ProtoPie Figma import: https://www.protopie.io/learn/docs/import/importing-from-figma

**Design systems**
- Material Compose motion tokens (`ExpressiveMotionTokens.kt`, `StandardMotionTokens.kt`, `MotionTokens.kt`, `MotionScheme.kt`): https://github.com/androidx/androidx/tree/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3
- Material Web motion tokens: https://github.com/material-components/material-web/blob/main/tokens/versions/v0_192/_md-sys-motion.scss
- MDC Android Motion.md: https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md
- M3 motion overview (client-rendered; partially read): https://m3.material.io/styles/motion/overview/how-it-works
- M3 Expressive motion theming: https://m3.material.io/blog/m3-expressive-motion-theming
- Carbon motion overview: https://carbondesignsystem.com/elements/motion/overview/
- Carbon choreography: https://carbondesignsystem.com/elements/motion/choreography/
- Carbon motion package (DTCG source, surfaces): https://github.com/carbon-design-system/carbon/tree/main/packages/motion/src
- Carbon #22686, motion accessibility: https://github.com/carbon-design-system/carbon/issues/22686
- Fluent 2 motion: https://fluent2.microsoft.design/motion
- Fluent tokens, durations and curves: https://github.com/microsoft/fluentui/tree/master/packages/tokens/src/global
- Fluent react-motion: https://github.com/microsoft/fluentui/tree/master/packages/react-components/react-motion/library
- Fluent motion components preview: https://github.com/microsoft/fluentui/tree/master/packages/react-components/react-motion-components-preview/library/src
- Atlassian motion: https://atlassian.design/foundations/motion
- Atlassian tokens, `atlassian-motion` theme: https://unpkg.com/@atlaskit/tokens@20.6.0/dist/cjs/artifacts/themes/atlassian-motion.js
- Polaris motion tokens: https://github.com/Shopify/polaris/blob/main/polaris-tokens/src/themes/base/motion.ts
- Spectrum motion: https://spectrum.adobe.com/page/motion/
- Spectrum CSS tokens 16.0.2: https://unpkg.com/@spectrum-css/tokens@16.0.2/dist/css/index.css
- Primer motion primitives: https://github.com/primer/primitives/tree/main/src/tokens
- SLDS durations: https://github.com/salesforce-ux/design-system/blob/master/design-tokens/aliases/duration.yml
- Base Web animation: https://github.com/uber/baseweb/blob/main/src/themes/shared/animation.ts
- Open Props easing: https://github.com/argyleink/open-props/blob/main/src/props.easing.js

**Apple**
- SwiftUI `Spring`: https://developer.apple.com/documentation/swiftui/spring
- WWDC23, Animate with springs: https://developer.apple.com/videos/play/wwdc2023/10158/
- `matchedGeometryEffect`: https://developer.apple.com/documentation/swiftui/view/matchedgeometryeffect(id:in:properties:anchor:issource:)
- `NavigationTransition` and `.zoom`: https://developer.apple.com/documentation/swiftui/navigationtransition
- `scrollTransition`: https://developer.apple.com/documentation/swiftui/view/scrolltransition(_:axis:transition:)
- `visualEffect`: https://developer.apple.com/documentation/swiftui/view/visualeffect(_:)
- `ScrollGeometry`: https://developer.apple.com/documentation/swiftui/scrollgeometry
- `repeatForever(autoreverses:)`: https://developer.apple.com/documentation/swiftui/animation/repeatforever(autoreverses:)
- `PhaseAnimator`: https://developer.apple.com/documentation/swiftui/phaseanimator
- `KeyframeAnimator`: https://developer.apple.com/documentation/swiftui/keyframeanimator
- `UIViewPropertyAnimator`: https://developer.apple.com/documentation/uikit/uiviewpropertyanimator
- `accessibilityReduceMotion`: https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion
- `isReduceMotionEnabled`: https://developer.apple.com/documentation/uikit/uiaccessibility/isreducemotionenabled
- `prefersCrossFadeTransitions`: https://developer.apple.com/documentation/uikit/uiaccessibility/prefersCrossFadeTransitions
- HIG Motion: https://developer.apple.com/design/human-interface-guidelines/motion

**Android**
- Compose `Spring` constants: https://developer.android.com/reference/kotlin/androidx/compose/animation/core/Spring
- Compose `SpringSimulation` source: https://github.com/androidx/androidx/blob/androidx-main/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/SpringSimulation.kt
- Compose animation customize: https://developer.android.com/develop/ui/compose/animation/customize
- Compose animation quick guide: https://developer.android.com/develop/ui/compose/animation/quick-guide
- Compose shared elements: https://developer.android.com/develop/ui/compose/animation/shared-elements
- Compose `DecayAnimationSpec` source: https://android.googlesource.com/platform/frameworks/support/+/androidx-main/compose/animation/animation-core/src/commonMain/kotlin/androidx/compose/animation/core/DecayAnimationSpec.kt
- `MotionDurationScale`: https://developer.android.com/reference/kotlin/androidx/compose/ui/MotionDurationScale
- `Settings.Global`: https://developer.android.com/reference/android/provider/Settings.Global
- `ValueAnimator`: https://developer.android.com/reference/android/animation/ValueAnimator

**React Native**
- `AccessibilityInfo`: https://reactnative.dev/docs/accessibilityinfo
- `ScrollView` `decelerationRate`: https://reactnative.dev/docs/scrollview
- Reanimated `withSpring`: https://docs.swmansion.com/react-native-reanimated/docs/animations/withSpring/
- Reanimated `withDecay`: https://docs.swmansion.com/react-native-reanimated/docs/animations/withDecay/
- Reanimated `withRepeat`: https://docs.swmansion.com/react-native-reanimated/docs/animations/withRepeat/
- Reanimated accessibility: https://docs.swmansion.com/react-native-reanimated/docs/guides/accessibility/

**WCAG**
- Understanding 2.2.2 Pause, Stop, Hide: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
- Understanding 2.3.3 Animation from Interactions: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
- Technique C39: https://www.w3.org/WAI/WCAG22/Techniques/css/C39

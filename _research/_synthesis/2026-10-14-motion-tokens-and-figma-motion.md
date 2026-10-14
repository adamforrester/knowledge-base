# Synthesis — motion tokens, motion patterns and Figma Motion (the 2026-10-14 run)

> Reconciles the two raw outputs in `_research/_inbound/2026-10-14-motion-tokens-and-figma-motion/` (`claude.md` and `external-agent.md`, against the identical `prompt.md`), with Eddie Lou's practitioner piece (`_source-text/ext-motion-in-design-systems-lou.txt`) as a third, non-evidential view. Path A was used because the run reverses a standing diagnosis in `21-motion-spec-and-handoff` ("Figma is structurally inadequate for motion"), because the external half carries several claims that fail verification and need an explicit ledger, and because the result lands across 18, 21 and the generated token model rather than in one file. Filed 2026-10-14. Draft, not the practice's POV until promoted.

---

## The headline

**Both halves agree on the architecture, and it is the right one.** A motion system has three tiers: token primitives and semantic roles, a separate **motion pattern** tier that references those tokens, and components that pick a pattern. Figma Motion is now good enough to *render* that model — TIMING and EASING variables for the token tier, custom animation styles for the pattern tier — but not to be its source of truth. The pattern spec is the source; Figma styles and code recipes are both generated from it. Lou arrives at the same three levels from practice (token, pattern, behavioural), which is corroboration of the shape, not evidence for it.

**Where they part company, the Claude half is right more often, and for a structural reason.** It read the Plugin API typings, the generated Material token source and the platform docs, and it ran a live API test. The external half writes fluently but carries no URLs or fetch dates, and several of its most quotable claims — "mature systems store mass/stiffness/damping as tier-1", "Material 3 springs are mass/stiffness/damping", "Spectrum 3D spring tokens", "variable modes can bind reduced-motion modes to alternative animation styles" — fail against primary sources. Where the external half stands alone it should be read as hypothesis. The verification ledger below is the record.

**What the external half adds that is worth keeping** is mostly framing: the explicit permission contract on brand curves (scope them away from utility components by lint), the insistence that velocity is a runtime input and never a token, and a clean statement that spatial motion should prefer springs while effects use curves. Those survive and are folded in.

---

## Verification ledger

Every external-only claim the brief flagged, checked on 2026-10-14. "Verified" means opened on a primary source today; anything else does not carry forward as fact.

| External-agent claim | Verdict | What the primary source says |
|---|---|---|
| Plugin API "Update 133 (Aug 5)" added TIMING and EASING | **Verified** | Update 133, 2026-08-05: adds `"EASING"` (stores `MotionEasing`) and `"TIMING"` (plain numbers in seconds) as variable resolved types. The update page itself does not mention `CUSTOM_SPRING` or `physicalSpringToNormalized`; those are on the Motion and `figma.motion` reference pages. |
| "Update 140 (Sep 30)" shipped custom animation styles | **Verified** | Update 140, 2026-09-30: `CustomAnimationStyle`, `figma.createCustomAnimationStyle()`, `getLocalCustomAnimationStylesAsync()`, `animationEntries`, `addAnimationEntryAsync()`, `removeAnimationEntry()`; `animationStyles` now returns FIGMA or CUSTOM; `applyAnimationStyle()` accepts `{type: "CUSTOM"}`. |
| `figma.motion.playheadPosition` | **Verified** (but not from those updates) | A read-only `number \| undefined` in seconds on the `figma.motion` reference page and in `@figma/plugin-typings` 1.141.0. Neither Update 133 nor 140 introduces it. |
| `node.applyManualKeyframeTrack()` | **Verified** | Present in typings 1.141.0 (`applyManualKeyframeTrack(field, track)`, with `removeManualKeyframeTrack`). |
| `physicalSpringToNormalized()` "accepts true mass, stiffness and damping, converting them natively" | **Verified as a helper; framing wrong** | It takes `{mass, stiffness, damping}` and returns one number, `bounce` in 0–1 (bounce = 1 − ζ, live API test). Stiffness is discarded. It is a lossy projection, not a native physics input. |
| Custom animation styles "encapsulate configured variables, timings and keyframed property manipulations" | **Wrong in detail** | The style is "a reusable Motion animation defined in the file": an ordered list of entries, each a *Figma-provided* animation added by `styleId`. The reference page does not describe keyframes inside a style. Entries can be edited only on local styles; calls on a library style throw. |
| "Material 3 springs are mass/stiffness/damping" | **Wrong** | M3's generated `ExpressiveMotionTokens.kt` / `StandardMotionTokens.kt` publish `…Damping` and `…Stiffness` pairs (e.g. DefaultSpatial 0.8 / 380). `MotionScheme.kt` passes them as `dampingRatio =` and `stiffness =` to Compose `spring()`. No mass; Compose assumes mass 1. |
| "Mature systems increasingly store mass/stiffness/damping as tier-1" | **Unsupported, and contradicted** | No surveyed design system stores m/k/c as tokens. The only system that tokenises springs (M3) stores damping ratio + stiffness. Apple ships presets in duration + bounce terms. Web systems bake springs into `linear()`. m/k/c is a *platform API* form (SwiftUI, Reanimated, Figma prototype springs), not a token-storage convention. |
| SwiftUI bounce ranges −1 to 1 | **Verified** | Apple `Spring.init(duration:bounce:)`: "0 indicates no bounces (a critically damped spring), positive values … up to a maximum of 1.0 (undamped oscillation), and negative values indicate overdamped springs with a minimum value of -1.0." |
| Figma variable modes "bind reduced-motion modes to alternative custom animation styles" | **Wrong** | Variables cannot hold styles: the variables help article states "styles cannot be used in other styles or variables." Modes switch the *values* of TIMING and EASING variables ("switch the mode at the page level, and every animation referencing that variable updates at once", launch blog, 2026-06-24). A mode cannot swap one animation style, or one entry type, for another. |
| Spectrum "3D spring tokens (focus, feel, speed)" and durations "Instant, Noticeable, Lingering" | **Unverified; not found** | The Spectrum motion page says "Motion in Spectrum 2 is still being developed" and names no springs. `@spectrum-css/tokens` 16.0.2 ships ordinal `animation-duration-0…6000`, four eases, and no spring tokens; `@adobe/spectrum-tokens` 15.5.0 has no motion tokens at all. Drop both claims. |
| Atlassian `motion.popup.enter` bundles | **Verified with a correction** | `@atlaskit/tokens` 20.6.0 (early access) names are directional: `motion.popup.enter.{top,bottom,left,right}` and `motion.popup.exit.*`. `--ds-popup-enter-bottom` = `150ms cubic-bezier(0.4, 1, 0.6, 1) SlideInBottom8px backwards, 150ms … FadeIn0to100 backwards`; exit is 100ms with a 4px slide. Duration, curve, keyframes and fill in one token — the substance of the claim holds. |
| Apple presets "Snappy, Bouncy, Popover" | **Partly wrong** | `.smooth`, `.snappy`, `.bouncy` are SwiftUI presets. "Popover" is not a spring preset. |
| Scroll motion via "CSS `@scroll-timeline`" | **Outdated** | The `@scroll-timeline` at-rule belongs to an abandoned earlier draft. The shipping surface is `animation-timeline` with `scroll()` / `view()`, `animation-range`, and the `scroll-timeline` / `view-timeline` properties. |
| MVP table: "Drawer/Accordion: expand bounding box height/width" | **Self-contradiction** | The same output forbids animating height, width, padding and margin. Resolved under §4 below: expand/collapse is the one pattern where layout change *is* the motion, so it becomes a declared, budgeted exception rather than a silent breach. |
| "Motion envelope: meaning, method, permission", attributed to "practitioners" | **Unsourced** | Useful framing, no citation. Keep the idea (we use the permission half for brand curves); do not quote it as field terminology. |
| WCAG table rows for 1.4.11 and "Boolean variables tied to loop play states" | **Out of scope / unverified** | 1.4.11 is contrast, not motion. No Figma source says Motion loop state binds to a boolean variable. Drop. |

The external half also says Figma was inadequate "prior to the latter half of 2026". Motion launched in open beta on 2026-06-24 and is still beta; the variables and styles that matter for tokens arrived on 2026-08-05 and 2026-09-30.

---

## 1. What mature design systems ship as motion tokens today

**Convergence (both agents).** Every system ships a duration scale; easing comes as a small set of roles (standard, enter/decelerate, exit/accelerate, linear) crossed with an intensity axis (Carbon productive × expressive, M3 standard × emphasized, Fluent Min/Mid/Max, Atlassian practical × bold). Semantic names sit over literal primitives. Carbon's six durations (70–700ms) and M3's sixteen (50–1000ms) are reported identically by both halves. That intensity axis is the industry's personality lever, and it is what our role tier already is.

**Divergence: who tokenises springs.** The external half frames the field as "physics-first" (M3, Apple) versus "curve-first" (Carbon, Fluent). That is half right. M3 is the *only* design system that ships springs as tokens, and it does so as {fast, default, slow} × {spatial, effects} pairs of damping ratio and stiffness. Apple ships springs at platform level as presets, not as a system's tokens. Every web-first system either has no springs or bakes one into `linear()` (Atlassian, Open Props). The Claude half is right: **our three spring presets already put us ahead of every web system and level with M3 in kind, not in coverage.**

**Divergence: how springs are stored.** The external half's "consensus on mass/stiffness/damping as tier-1" is the run's most consequential error, because it would push us to re-model. It is contradicted by the one system that tokenises springs (M3: ζ + k) and by the platform that generates them (Compose: `spring(dampingRatio, stiffness)`, mass implicitly 1). Our model — **damping ratio + stiffness at mass 1** — is identical to M3's generated tokens and to Compose verbatim. It converts losslessly to every other form (m/k/c by setting m = 1 and c = 2ζ√k; duration + bounce by d ≈ 2π/√k and bounce = 1 − ζ for ζ ≤ 1) except baked `linear()`. Storing m/k/c instead would add a degree of freedom nobody tunes and that Compose and Figma both throw away. **Keep ζ + k.**

**Conversion maths.** Both halves give the same relationships (k = (2π/R)²·m; c = 2ζ√(km)), and they agree with the Claude half's derived table. The Claude half's caveat stands: the duration in duration + bounce is *perceptual*, and the definition of "settled" is unresolved (DTCG #429). Emit it with a declared tolerance.

**Brand curves.** Both halves agree that no system publishes numeric guardrails for brand-authored curves; M3 (`MotionScheme` is a public interface) and Apple (custom `Spring`) are the only formal routes to brand physics. The external half's "the safest and most prevalent approach restricts developers to predefined presets" describes product teams, not brands, and does not conflict.

**Distance is a token in two systems, hidden in one (verified this pass; neither agent surfaced it).** Spectrum ships component-scoped distance tokens: `--spectrum-tooltip-animation-distance` (5px, re-aliased to `spacing-75`) and `--spectrum-dialog-confirm-entry-animation-distance` (20px / 25px across scales). Atlassian bakes distance into keyframe names (`SlideInBottom8px` in, `SlideOutBottom4px` out). Lou names "distance and displacement values" as a token-level primitive. The field evidence for Lou's position is thin but real, and it bears on the closing section.

---

## 2. Pattern-level motion

**Convergence (both agents, and Lou).** Patterns are a distinct layer between tokens and components. The external half calls it the "Motion Layer" and argues it from code reuse (a `<Dropdown>` and a `<Combobox>` should inherit the same entrance without duplication); the Claude half argues it from the field (MDC transition classes, Fluent atoms and presence components, Carbon surfaces) and from DTCG #429, which dropped named patterns as "a naming convention, not a type". Lou: patterns "are more than the sum of their tokens … motion decisions with their own identity". Three routes, one answer.

**What a pattern specifies.** Both halves list the same fields — animated properties with from/to values, a distance or scale envelope, timing by token reference, choreography and stagger. The Claude half adds asymmetry (exit faster than enter: Material fade 150/75ms, Atlassian 150/100ms with an 8px-in / 4px-out distance), direction semantics, and a required reduced-motion field. Take the Claude half's seven-field list as the base and add Lou's behavioural rules as fields (closing section).

**Brand tunability.** Superficially the halves disagree — the external half proposes a global "tempo" lever, the Claude half says no system documents a global duration multiplier — but read closely, the external half's lever is "swapping the alias context", which is a scheme or mode swap. That is exactly what the Claude half recommends (M3 standard/expressive or a custom `MotionScheme`, Carbon productive/expressive). **Converged: the lever is a scheme/mode on the semantic tier; patterns reference roles and inherit.** A numeric tempo multiplier remains a practice invention; if adopted, it scales primitives only (stiffness ∝ 1/tempo²).

**Where patterns live.** Converged: not in the token namespace. Atlassian is the outlier, in early access. The external half's warning that DTCG cannot express keyframed choreography and the Claude half's "a structured spec that references tokens, serialised as a sibling file" are the same position.

---

## 3. Figma's native motion tooling, late 2026

**Converged and verified.** Figma Motion (open beta since 2026-06-24) has a timeline, keyframes, first-party animation definitions, and since 2026-09-30 publishable custom animation styles. TIMING variables store seconds (the UI shows ms); EASING stores `MotionEasing` — named curves, back curves, custom cubic-bezier, four built-in springs, `CUSTOM_SPRING {bounce}` and `HOLD`. Both bind to animation-style properties and keyframe easing. The external half's pipeline sketch (durations → TIMING, curves and springs → EASING, patterns → custom animation styles) matches the Claude half's mapping table.

**What the external half gets wrong, and why it matters for the generator.**

1. **Springs lose stiffness on the way in.** `CUSTOM_SPRING` holds only bounce; `physicalSpringToNormalized` is a projection. The Claude half's fix is the right one: emit duration ≈ 2π/√k as a **paired TIMING variable** and bind both. ζ > 1 cannot be represented (bounce floors at 0), so either forbid overdamped springs or accept the clamp.
2. **Styles are groups of first-party animations, not keyframe containers.** A "Dialog enter" style is Opacity + Scale + Position entries, each with duration and easing bound to our variables and an offset. Anything outside the first-party definitions (Opacity, Position, Scale, Rotation, Size, Path, TextStagger — live API test only; Figma's docs do not enumerate them) cannot go in a style.
3. **Modes cannot swap styles.** See the ledger. Reduced-motion *values* are a mode; reduced-motion *substitution* is a separate "/ reduced" style.

**Not bindable (Claude only, verified by live test and typings).** Prototype reaction transitions take literal `duration` and an older `Easing` whose spring is physical `{mass, stiffness, damping, initialVelocity}`. The external half does not mention the prototype gap at all. Any pipeline that writes prototypes must write literal values, convert ζ + k to m/k/c, and re-sync on token change.

**Other limits (Claude only).** No scopes for TIMING or EASING; REST support for both is undocumented, so sync must be plugin-side; library styles are read-only and their versioning semantics beyond ordinary publishing are undocumented. The external half's "rigid envelope" point — a style applied to a node structured differently may fail — is plausible and untested; carry it as a spike item, not a fact.

**Agent application.** The external half's picture of an agent applying styles across hundreds of components through the Figma MCP `use_figma` tool and `applyManualKeyframeTrack` is technically possible (both APIs exist) but describes an unproven workflow. It is the right direction for 34; it is not yet evidence.

**Other tools.** Converged: Rive for state-driven runtime motion, Lottie/dotLottie for illustrative and brand moments (now a native Figma Motion export), ProtoPie for conditional prototypes, code previews as the reference implementation for anything interruptible or gesture-coupled.

---

## 4. The hard cases

**Brand-defined curves.** Converged on "allow, with guardrails". The two halves contribute different guardrails and both are needed. The Claude half's are **shape** guardrails: role compatibility (an exit alias must accelerate, an enter alias decelerate), overshoot only on spatial properties at no more than bounce ≈ 0.4 (Apple WWDC23's caution line; M3 never lets spatial ζ fall below 0.6), a non-overshooting reduced twin, and provenance. The external half's is a **permission** guardrail: brand curves live in a scoped namespace and are lint-blocked from utility components (a heavy overshoot that delights on a 400ms modal reads as a glitch on a 50ms checkbox). Shape stops a bad curve existing; permission stops a good curve landing in the wrong place. Both are practice positions, not cited standards.

**Scroll-linked and progress-driven motion.** Converged: not tokens. The external half says "out of scope for primitive tokens, handle through pattern specs and layout components"; the Claude half says "a pattern spec, not tokens", with magnitudes and a parallax ceiling tokenisable and continuous parallax declared out of scope. Same answer. The Claude half's platform state is the current one: `animation-timeline` ships in Chrome 115+ and Safari 26, Firefox Nightly only, MDN "Limited availability", not Baseline, as of 2026-10-14. Figma Motion has no scroll timeline. WCAG's Understanding doc for 2.3.3 names parallax as the canonical vestibular trigger, so scroll patterns default to off under reduced motion.

**Physics beyond presets.** Converged: tokens define the resting spring; velocity is a runtime input. The external half states this most cleanly ("a design token cannot know how fast a user's thumb was moving"). The Claude half adds the useful corollary: interruptibility is an *intent* a pattern can declare (`interruptible: true` → use a spring primitive, not a timed curve), and decay is tokenisable only as a deceleration rate and rubber-band factor, worth generating only when a brand has custom flick surfaces. Very bouncy springs are a governance problem, not an encoding one.

**Per-property easing and pulses.** Converged: both exceed a flat token. The external half falls back to "a CSS `@keyframes` block in the component layer, tokenising only the total duration"; the Claude half models both as **pattern tracks** — `{property, from, to, duration | spring, easing, delay}` for per-property timing, and amplitude, direction mode, finite iteration count and a reduced fallback for pulses. The Claude half is right: the external fallback hides the internal timing from Figma, from agents and from review, which is the 21 failure mode in a new place. Pattern tracks also match Figma's entry model, Fluent's `Collapse`, Material's primary/secondary split and the M3 spatial/effects rule. WCAG 2.2.2 makes iteration count load-bearing: anything looping past 5 seconds beside other content needs pause/stop/hide, so pulses default finite.

**The layout-animation contradiction.** The external half's rule (never animate height, width, padding, margin) is sound for transitions in general and it is wrong for expand/collapse, where a change of size *is* the motion. The field accepts this: Fluent's `Collapse` has its own size track and duration. The resolution is to make layout animation a **declared exception** in the pattern spec — a track that sets `layout: true` — with a choice of technique per platform: animate size on small subtrees; on the web, `interpolate-size: allow-keywords` animates to `auto` but ships only in Chrome 129+ (Firefox and Safari not implemented, MDN BCD, 2026-10-14), so a JS measure-then-animate path or a clip/transform reveal is the portable route. Reduced motion collapses it to instant. Lou's performance-budget point lands here: layout tracks are where a budget actually bites.

---

## 5. Reduced motion and accessibility

**Converged.** Twins and substitution beat zeroing; WCAG 2.2.2 (A) governs auto-playing loops past 5 seconds; 2.3.3 (AAA) is the criterion systems actually build to even when they do not claim AAA; vestibular triggers are large spatial movement, parallax, depth scaling and rotation. The external half's criticism of the global 0.01ms reset — context lost, elements pop — is fair and matches the Claude half's reading that WCAG excludes opacity and colour changes from "motion animation", which is the normative basis for substituting a fade rather than removing everything.

**Where the Claude half goes further, and is right.** Reduced motion is a **property substitution**, not a value change. Fluent v9 (per-atom `reducedMotion` replacing keyframes, 1ms default), Reanimated (`ReduceMotion` per animation, documented `BounceIn` → `FadeIn` substitution) and Apple (`prefersCrossFadeTransitions` saying *what* to substitute) all encode it per pattern. Our duration twins are necessary but not sufficient. The spatial/effects split gives a default substitution rule: drop or replace spatial tracks, keep effects tracks at reduced duration. That mapping is our inference, aligned with WCAG's exclusion.

**Figma mapping, corrected.** Value twins → a `reduced` mode on the semantic motion collections. Property substitution → a separate "/ reduced" custom animation style per pattern, picked manually. The external half's "modes bind to alternative styles" is not possible. This is a Figma gap to document, not to solve.

**Non-accessibility sources of "no motion".** The Claude half notes Android's `areAnimatorsEnabled()` is false under Battery Saver. That gives Lou's "when the device is under performance pressure" rule a concrete platform hook.

---

## 6. Platform delivery

**Converged.** DTCG has `duration`, `cubicBezier` and `transition` and no spring or pattern type; springs reach CSS only as sampled `linear()`; Compose takes `spring(dampingRatio, stiffness)`; SwiftUI takes several forms; Style Dictionary needs custom transforms.

**Where the Claude half is more precise.** DTCG 2025.10 is a Final Community Group Report (28 Oct 2025), not a draft; #429 narrowed a spring proposal to `{bounce, duration}` with "stopped" as the unresolved blocker; keyframes were deferred. Stock Style Dictionary 5.6.1's `time/seconds` filters on `$type === 'time'`, not DTCG `duration`, so DTCG duration objects do not round-trip; motion transforms exist only in the CSS-family groups. The external half recommends custom `$type` values (`custom-spring`, `motion-composite`); a `$type` outside the spec's list is non-conformant, and `$extensions` is the sanctioned place for vendor data. Use `$extensions` for spring and pattern data, as the Claude half says, and plan a transform to `{bounce, duration}` if #429 lands in that shape.

**Native.** The external half's route of emitting m/k/c into SwiftUI is valid but unnecessary given ζ + k storage; `Spring(duration:bounce:)` or `Spring(mass: 1, stiffness:, damping:)` are both one transform away. For M3-based Android apps the highest-leverage output is a custom `MotionScheme` (Claude only), which flows brand motion into every Material component.

---

## 7. Recommendations

The two halves' recommendation sections agree on the shape — keep the token tier, add springs and patterns, declare scroll and velocity out of scope — and disagree on spring storage, where the external half's "encode exclusively as mass/stiffness/damping" fails verification. The reconciled recommendations, with Lou's behavioural layer folded in, are the next section.

---

## What this means for a generated token system

The current model — a duration scale with semantic roles and reduced twins, named cubic-beziers with a role tier, three springs as damping ratio + stiffness at mass 1, and duration + easing composites — is **on target at the token tier**. What it lacks is a pattern tier, and that is where four of the five inventory gaps belong. The brand inventory of about 105 production animations is the test: every gap it surfaced is either a pattern field or a deliberate exclusion, not a missing token type.

### Keep

- **The duration scale and semantic roles.** 6–10 steps, our own names and values.
- **Named curves and the role tier** (default, enter, exit, emphasized). "Emphasized" is our intensity axis.
- **Springs as damping ratio + stiffness at mass 1.** Identical to M3's generated tokens and Compose verbatim; lossless to every target except baked `linear()`. Do not move to m/k/c.
- **Reduced-motion duration twins**, reframed as a `reduced` mode in Figma and addressable twins in code.
- **Composite transitions, demoted** to single-property conveniences in the shape of DTCG `transition` and Primer `motion.transition.*`. Multi-property motion moves to patterns.

### Add

**1. A motion pattern tier.** A structured spec per pattern, serialised as a sibling file that references tokens (not a DTCG type), generated into per-platform code recipes and into Figma custom animation styles. Fields:

- `phase` — enter, exit, state change, reposition, navigate;
- `tracks[]` — `{property, from, to, distance?, duration | spring, easing, delay, layout?}`;
- `choreography` — stagger interval, order, total cap (Carbon's 20ms within 500ms as default);
- `direction` — axis, reverse on back;
- the behavioural fields below.

**2. Behavioural rules as pattern fields.** Lou's behavioural level is "the least documented layer … and the most important"; the way to make it real in a generated system is to make every rule a field the generator emits and the code honours, not a paragraph in the docs.

- `interruptible` — true means a spring primitive and velocity retargeting on platforms that offer it; false allows a timed curve.
- `skipOnRapidRepeat` — when the same trigger fires again inside the pattern's duration (a user mashing a toggle, paging quickly), jump to the end state rather than queue. Lou names this; Reanimated's jump-to-end behaviour under reduce shows the mechanism exists. Practice position, not a cited standard.
- `reducedMotion` — required. Either substitute tracks (default: spatial tracks dropped or replaced by an opacity cross-fade, effects tracks kept at reduced duration) or `essential: true` with a recorded reason.
- `lowPower` — what the pattern becomes when the platform reports animations disabled for non-accessibility reasons (Android Battery Saver). Default: same as reduced.
- `iterations` — finite by default; anything infinite must name its 2.2.2 control.

**3. Distance and displacement tokens.** Lou puts them at the token level; Spectrum and Atlassian show the field doing it either as component-scoped tokens or baked into keyframes. We should add a short **motion distance scale** (three or four steps) that aliases the spacing scale, consumed by pattern tracks, with the enter/exit asymmetry encoded in the pattern (Atlassian: 8px in, 4px out), not as separate tokens. *Decision rule:* if a distance recurs across patterns, it is a token; if it is unique to one pattern, it is a literal in that pattern's track. Reduced motion sets distance to zero, which is what makes the spatial track droppable without a separate twin.

**4. The spatial / effects spring split.** Replace the three presets with {fast, default, slow} × {spatial, effects}, effects always ζ = 1. It gives per-property easing a default (spatial properties take the spatial spring, opacity and colour the effects one), gives reduced motion a default, and maps 1:1 onto M3's `MotionScheme`.

**5. A scheme or mode lever for personality** — `productive` / `expressive`, as modes on the semantic easing and spring collections. This is the brand lever both halves converged on. A numeric tempo multiplier is optional and scales primitives only.

**6. Brand-defined curves with guardrails.** A `easing.brand.*` primitive namespace that semantic roles may alias, gated in the generator by shape (role compatibility; overshoot only on spatial properties at bounce ≈ 0.4 or less; never on opacity or colour; a non-overshooting reduced twin; provenance) and by permission (which patterns may reference a brand curve; utility and state-change patterns may not). *Decision rule:* a brand curve that fails a shape check is rejected; one that passes but is referenced from a forbidden pattern is a lint error, not a silent fallback.

**7. Pattern styles in Figma.** Each pattern generates a custom animation style ("Dialog / enter") whose entries are the first-party Opacity, Position, Scale and Size animations, with every entry's duration and easing bound to our TIMING and EASING variables and per-entry offsets for per-property timing and in-style stagger. Each pattern with a property-substituting reduced form also generates "Dialog / enter / reduced". Springs emit as `CUSTOM_SPRING {bounce}` **plus** a paired TIMING variable for perceptual duration. The generator writes TIMING in seconds (the likeliest off-by-1000 defect) and syncs plugin-side, since REST does not document motion variables. Prototype transitions get literal values on each sync.

**8. Spring emission in duration + bounce form** with a declared settling tolerance, for Figma, SwiftUI, Motion and the likely DTCG shape.

**9. Per-property easing and pulses as pattern tracks**, not composite tokens. A pulse is a pattern with amplitude, property, duration and easing, direction mode (alternate or mirror), finite iterations within 5 seconds, and a reduced fallback.

**10. Optional decay tokens** (`deceleration`, `rubberBand`), generated only when a brand's inventory includes custom flick surfaces.

### Out of scope

Say so in the system docs, so the absence reads as a decision.

- **Continuous scroll-linked and parallax motion.** Scroll-*triggered* reveals are a pattern with a mandatory static fallback and reduced-motion off. Continuous parallax is bespoke build work. CSS support is not Baseline and WCAG names parallax as the canonical trigger. Tokenisable parts — magnitudes, easing across the range, a parallax ratio ceiling — live in the pattern spec.
- **Physics beyond presets as tokens.** Gesture coupling, velocity, snap points and rubber-banding beyond a factor are implementation. The pattern declares intent through `interruptible`; tokens hold only the resting spring.
- **Initial velocity in any token.** Both halves agree; it is a runtime input.
- **Illustrative and brand-moment animation.** Lottie/dotLottie or Rive assets reference our colour and timing tokens; the generator does not produce them.
- **Overdamped springs (ζ > 1).** Figma cannot represent them and UI tokens do not use them.
- **Infinite loops by default.**
- **The operating model Lou describes** — a named motion owner, system-level motion review, testing with motion-sensitive users, frame and battery budgets. These are governance, not tokens. The generator can support them (emit a per-pattern performance class, flag `layout: true` tracks, list every infinite loop) but cannot supply them. They belong in 07 and 08 at promotion.

### Decision frameworks

**Token, pattern or out of scope?** A token is a single scalar or curve reused across contexts. A pattern has more than one property, a phase, choreography, a reduced substitute or a behavioural rule. Out of scope means it depends on continuous input (scroll position, gesture velocity) or is authored as an asset.

**Spring or curve for a pattern?** A spring when the motion is user-initiated, interruptible or must feel physical. A curve when it is system-initiated, fixed-length, synced with other timed media, or targets CSS-only consumers where `linear()`'s fixed duration is acceptable. Effects tracks inside a spring pattern can still take a curve.

**Where does a reduced-motion alternative live?** A value-only change (shorter, no overshoot, zero distance) is a token mode. A property change (movement to fade) is a pattern field. A finer platform signal (iOS cross-fade preference) is the runtime picking the pattern's substitute.

**May this animate layout?** Only in a pattern whose purpose is a size change (expand/collapse, toast stack reflow), declared with `layout: true`, budgeted, and instant under reduced motion. Everywhere else, transform and opacity.

**Which Figma vehicle?** Variables for anything a mode should switch; a custom animation style for a named pattern designers apply; an animated component when the motion is inseparable from the component's structure; prototype transitions only for flows, with literal values until Figma binds variables there.

### A minimum viable pattern set

Reconciled from the Claude half's ten and the external half's six, ordered by how many components each unblocks and by dependency.

1. **Fade (enter / exit).** Tooltips, popovers, skeleton-to-content — and the universal reduced-motion substitute, so it comes first.
2. **State change / press.** Hover, focus, press, toggle, tab indicator. Effects-only plus a small spatial spring on press. The external half ranks it first and it is the cheapest; it is mostly composite transitions and the first test of the permission guardrail.
3. **Pop / scale-fade (enter / exit).** Menus, selects, comboboxes, anchored popovers. Scale ≈ 0.95 → 1 plus fade, spatial/effects split, first user of the distance scale.
4. **Dialog (enter / exit).** Scrim on effects, panel on spatial, exit faster than enter.
5. **Sheet / drawer (enter / exit, by edge).** Spring-driven and interruptible; the first pattern where `interruptible` changes the code.
6. **Expand / collapse.** Accordion, disclosure, tree. Separate size and opacity tracks; the declared layout exception.
7. **Toast (enter, exit, reposition).** Stack reflow is the first choreography case.
8. **Page / view transition.** Shared axis plus fade-through, mapped onto View Transitions and the native navigation transitions.
9. **Container transform / shared element.** Last of the transitions, because every platform now provides the mechanism; the system supplies timing and the reduced substitute.
10. **Pulse / attention** (finite), once 2.2.2 handling is in place.
11. **Progress / loading loop** (shimmer, spinner). The external half includes it; it is the first infinite loop, so it ships only with an explicit pause or reduced-motion stop and a recorded 2.2.2 reading. Whether a loading indicator counts as essential under 2.2.2 needs checking against the Understanding doc before we state a default.

Stagger is a choreography field on 6, 7 and 8, not a pattern.

---

## What this run supersedes in `21-motion-spec-and-handoff`

At promotion, the following conclusions of 21 should be revised. Points 1, 2 and 6 of 21's inadequacy list (Smart Animate's tweening model, no trigger, no cross-component choreography) still hold, and so does the Pattern B recommendation.

1. **"Figma is structurally inadequate for spec'ing micro-interactions"** (the framing blockquote, the frontmatter `description`, and the section "Why Figma is currently inadequate"). **Superseded in large part.** Figma can now specify timed and spring motion with token-bound values through the timeline, custom animation styles and TIMING/EASING variables. The diagnosis narrows to *adequate for specifying timed motion; inadequate for behaviour* — no triggers, no interruption model, no scroll timeline, no cross-component choreography, and prototype transitions not variable-bindable.
2. **"Easing is a closed set of presets"** (point 3). **Superseded.** EASING carries custom cubic-bezier, back curves, built-in and custom springs, and HOLD, all bindable.
3. **"Reduce-motion does not exist as a model"** (point 4). **Partly superseded.** Modes carry reduced value twins. Property substitution still needs a separate style; that remains a documented gap.
4. **"Springs are not a primitive"** (point 5, which describes a single 2024 Smart Animate spring preset). **Superseded.** `CUSTOM_SPRING` and four built-in springs are bindable easing values. The residual gap is that only bounce is stored, so stiffness travels as a paired TIMING variable.
5. **"The Figma MCP server's motion variables surface … does not yet surface per-component motion specs"** (How AI changes this). **Superseded.** `get_motion_context` returns keyframe tracks, easing and pre-computed CSS and motion.dev per animated node.
6. **"The bridge is a Figma plugin that emits Pattern B from Pattern A authoring … does not yet exist"** (open question 1). **Reframed.** The useful bridge now runs the other way: the Plugin API can write custom animation styles and bind them, so generating Figma Motion *from* a Pattern B spec is buildable today. This strengthens 21's Pattern B recommendation.
7. **"The composite token already encodes duration, easing, and the properties animated, and reduce-motion fallback"** (the `motion/modal/enter` example under "Motion tokens themselves as a spec"). **Refined.** A DTCG composite carries one duration and one easing and binds no property. What 21 calls a composite token is, in this run's vocabulary, a **pattern** that references tokens. The four-field annotation still works; it references a pattern, not a token.

The May external run's "70% reduction in design-to-dev cycle" and "DTCG motion module at draft-final stage" were never sourced and remain excluded.

---

## Open items and spikes before promotion

- Whether Figma's spring duration is perceptual or settling time (test against `Spring(duration:bounce:)` playback).
- Whether TIMING can bind to a manual keyframe's `timelinePosition`; whether EASING accepts cubic-bezier y outside [0, 1]; cross-collection aliasing for TIMING and EASING.
- REST support for TIMING and EASING (GET local variables on a file that contains them).
- Library versioning of custom animation styles: what consumer instances do when an upstream entry is removed.
- The external half's "rigid envelope" failure when a style is applied to a differently structured node.
- WCAG 2.2.2's treatment of loading indicators, before pattern 11 ships a default.
- Whether the distance scale should alias spacing one-to-one or hold its own steps; test against the brand inventory.
- **Practice positions, not cited standards:** the overshoot cap, the permission guardrail, `skipOnRapidRepeat`, `lowPower`, the tempo multiplier, and the spatial/effects → reduced-motion mapping.

## Sources opened in this synthesis pass (2026-10-14)

Beyond the references in `claude.md`, which this pass relies on where it agrees:

- Figma Plugin API Update 133: https://developers.figma.com/docs/plugins/updates/2026/08/05/version-1-update-133/
- Figma Plugin API Update 140: https://developers.figma.com/docs/plugins/updates/2026/09/30/version-1-update-140/
- `figma.motion` reference: https://developers.figma.com/docs/plugins/api/figma-motion/
- Motion types reference: https://developers.figma.com/docs/plugins/api/Motion/
- `CustomAnimationStyle` reference: https://developers.figma.com/docs/plugins/api/CustomAnimationStyle/
- `@figma/plugin-typings` 1.141.0, `plugin-api.d.ts` (`playheadPosition`, `applyManualKeyframeTrack`)
- Figma help, variables guide: https://help.figma.com/hc/en-us/articles/14506821864087
- Figma blog, Introducing Figma Motion (2026-06-24): https://www.figma.com/blog/introducing-figma-motion/
- Apple, `Spring.init(duration:bounce:)` (documentation JSON): https://developer.apple.com/documentation/swiftui/spring/init(duration:bounce:)
- androidx `ExpressiveMotionTokens.kt` and `MotionScheme.kt`: https://github.com/androidx/androidx/tree/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3
- Spectrum motion: https://spectrum.adobe.com/page/motion/
- `@spectrum-css/tokens` 16.0.2: https://unpkg.com/@spectrum-css/tokens@16.0.2/dist/css/index.css
- `@atlaskit/tokens` 20.6.0, `atlassian-motion` theme and token names: https://unpkg.com/@atlaskit/tokens@20.6.0/
- MDN browser-compat-data, `interpolate-size`: https://github.com/mdn/browser-compat-data/blob/main/css/properties/interpolate-size.json
- Eddie Lou, "Motion belongs in the design system" (2026), `_source-text/ext-motion-in-design-systems-lou.txt` — practitioner view, not evidence.

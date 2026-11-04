---
type: practice-area
title: Motion Spec and Handoff
description: The designer-to-developer micro-interaction spec gap. Figma Motion as of late 2026 — adequate for timed motion, inadequate for behaviour — the eight-field sufficient spec, the layered handoff contract, the pattern spec as source with Figma generated from it.
tags: [extension, motion, handoff, figma, spec, patterns]
timestamp: 2026-11-04
---

# 21 — Motion Spec and Designer–Developer Handoff

> Motion has been the part of the design system designers could not reliably hand off. The result is the motion equivalent of the accessibility annotation problem (17): whatever ends up in production is whatever the engineer improvised, sometimes informed by a Loom video and a Slack message. Figma Motion (open beta since June 2026) has closed half of that gap — it can now specify timed and spring motion against bound token values — and left the other half open: it still cannot specify behaviour. This file is what a sufficient motion spec contains, what Figma and the other candidate tools actually produce, and what the practice standardises on as the canonical handoff artefact: a pattern spec that references tokens, from which Figma and code are both generated.

---

## Why this is its own file

The motion foundation layer (18) and the per-platform implementation layers (19, 20) assume that designers and engineers agree on what motion to ship. That assumption has been wrong for the entire history of digital product design. Until mid-2026 the tool most designers worked in could not specify motion at all: Smart Animate was good enough to communicate the general feel of a transition but not good enough to specify it, and what shipped was the developer's best interpretation of a 7-second video clip, modulated by whether the designer was in the same Slack channel.

**Our position as of November 2026: Figma is adequate for specifying timed motion and inadequate for specifying behaviour.** Figma Motion can now carry durations, curves and springs bound to token variables, and group first-party animations into reusable styles. It still has no triggers, no interruption model, no scroll timeline, no cross-component choreography, and prototype transitions that cannot bind to variables. This replaces our May 2026 diagnosis that Figma was "structurally inadequate for spec'ing micro-interactions", which was right when written and was overtaken by Figma's June–September 2026 releases (see the section below).

This is the same handoff failure mode that 17-accessibility-annotation-contract addresses for accessibility, and the structural fix is parallel: encode the spec as a contract the designer fills in and the engineer implements, rather than as a video the engineer interprets. Motion is harder than accessibility on this dimension because the spec includes time as a first-class dimension and most design tools were not built for it. The field has produced a half-dozen partial answers, and Figma has now become one of the better ones; this file's job is to surface them honestly and recommend what the practice standardises on as the engineering target while the tooling matures.

---

## What a sufficient micro-interaction spec contains

The motion of any single interaction is a function of six values. A spec that omits any of these forces the engineer to fill in the gap by guessing.

| Field | What it answers | Example |
|---|---|---|
| **Trigger** | What user or system action initiates the motion? | `onClick`, `onHover`, `onMount`, `onRouteChange`, `onIntersect` |
| **Properties** | Which CSS / view properties change? | `opacity`, `transform-x`, `scale`, `background-color` |
| **From → To values** | The start and end state of each property. | `opacity: 0 → 1`, `translateX: -16px → 0` |
| **Duration or spring** | How long, or under what physics? | `duration/medium` (300ms) **or** `spring/snappy` |
| **Easing** (if duration) | Which curve? | `easing/enter` — or the literal Bezier if non-tokenised |
| **Reduce-motion behaviour** | What does this animation become for users with `prefers-reduced-motion: reduce`? | Cross-fade only, or no motion, or shortened duration |

Two additional fields apply to compound interactions:

- **Choreography** — if multiple elements animate, what is their relationship? (Sequence, stagger interval, parallel, follow-through.)
- **Interruption** — what happens if the user triggers a new state mid-animation? (Cancel, reverse, settle to current position then animate to new state.)

**A motion spec that contains these eight fields is implementable in any framework without further questions.** A motion spec that contains fewer is interpretation, not specification.

The practice's current motion specs — when they exist at all — typically contain trigger, duration, and a video. Properties, easing, reduce-motion, and interruption are inferred. This is the gap.

---

## What Figma can and cannot specify (November 2026)

The diagnosis matters because the remediation depends on it. Figma's limits are not failures of imagination; they follow from how the tool models design. That model changed in 2026, and our diagnosis changes with it.

**What changed, dated.** Figma Motion launched in open beta on 2026-06-24 with a timeline, keyframes and first-party animation definitions; it is still beta (Figma blog, *Introducing Figma Motion*, June 2026). Plugin API Update 133 (2026-08-05) added `TIMING` and `EASING` as variable types: TIMING stores plain numbers in seconds (the UI shows milliseconds), and EASING stores a `MotionEasing` — named curves, back curves, custom cubic-bezier, four built-in springs, a custom spring and `HOLD`. Plugin API Update 140 (2026-09-30) added custom animation styles: a reusable Motion animation defined in the file, publishable through a library, created and edited from plugins (`figma.createCustomAnimationStyle()`, `addAnimationEntryAsync()`, `applyAnimationStyle()`). Animation-style properties and keyframe easing both bind to TIMING and EASING variables, and switching a mode at page level updates every animation that references the variable (Figma Plugin API reference and Update 133 / 140 pages, verified 2026-10-14).

**Where our May diagnosis still holds.**

1. **Smart Animate matches by layer name and interpolates.** Prototype transitions remain a layout-tweening model. Motion now has a proper timeline beside it, but the prototype path has not changed.
2. **There is no notion of "trigger".** Neither prototypes nor Motion model "this animates on mount", "this animates on scroll into view", or "this animates after another animation finishes" as a declared trigger.
3. **Choreography across components is not addressable.** A style orchestrates entries on one node; coordinating five components is still five overlapping pieces of work.

**Where it no longer holds.**

4. **Easing is no longer a closed set of presets.** EASING variables carry custom cubic-bezier, back curves, springs and hold, all bindable to our tokens.
5. **Springs are a primitive.** The four built-in springs and `CUSTOM_SPRING` are bindable easing values. The residual gap: a custom spring stores only a normalised bounce (0–1). The helper `physicalSpringToNormalized()` takes mass, stiffness and damping and returns that one number, discarding stiffness — a lossy projection, not a physics input. Stiffness therefore has to travel as a paired TIMING variable carrying the spring's perceptual duration, and overdamped springs (ζ > 1) cannot be represented at all.
6. **Reduce-motion exists as values, not as substitution.** A `reduced` mode on the motion collections carries value twins — shorter durations, no overshoot. A mode cannot swap one animation style for another: variables cannot hold styles, and modes switch values, not entries. So a reduced form that changes *properties* (a slide becoming a fade) is a separate "/ reduced" style, picked by hand. That is a gap to document, not to solve.

**New limits the May diagnosis did not name.**

- **Prototype transitions are not bindable.** They take literal durations and an older easing type whose spring is physical `{mass, stiffness, damping, initialVelocity}`. Any pipeline that writes prototypes writes literal values and re-syncs on token change.
- **Styles are groups of first-party animations, not keyframe containers.** A "Dialog / enter" style is Opacity, Scale and Position entries, each with its own duration, easing and offset. Anything outside Figma's first-party animation set cannot go in a style.
- **No scopes for TIMING or EASING, and REST support is undocumented**, so sync is plugin-side for now.
- **Library styles are read-only in consuming files**, and what happens to consumer instances when an upstream entry is removed is undocumented.
- **No scroll timeline.**

**What follows for the practice.** Figma Motion is good enough to *render* a motion system — TIMING and EASING variables for the token tier, custom animation styles for the pattern tier (see 18-motion-foundations) — but not to be its source of truth. Its behaviour gaps are exactly the fields a pattern spec carries and a style cannot: `interruptible`, `skipOnRapidRepeat`, the reduced substitute, iteration limits. So the pattern spec stays the source, and Figma is a generated target alongside code.

---

## The candidate tooling landscape

What follows is the current shape of the field, ordered roughly by adoption. None of these is the answer. The practice's job is to pick the artefact engineers will actually receive and standardise on it.

### Prototype-focused tools

**Figma prototypes (+ Smart Animate).** The default for flows. Communicates feel, fails on specifics, and its transitions still take literal values that cannot bind to tokens. Where it does work: simple state transitions between two well-defined layouts. Where it doesn't: anything with springs, choreography, or interruption.

**Figma Motion (open beta, June 2026).** The timeline, first-party animations, TIMING and EASING variables and custom animation styles described above. For timed and spring motion on a single component it is now a real specification surface — token-bound, reusable and publishable — and the right place for designers to *see* a system's motion patterns. Its exports include Lottie/dotLottie for illustrative motion. Where it doesn't reach: behaviour (triggers, interruption, scroll, cross-component choreography). We generate its styles from the pattern spec rather than authoring them by hand (see the bridge below).

**Framer.** Stronger prototyping engine than Figma, with proper easing, springs, and overrides. The handoff artefact is a runnable React component (Framer is now a React framework as well as a prototyping tool). For React shops, Framer prototypes can sometimes be lifted directly. For non-React shops, the engineer still translates.

**ProtoPie.** Best-in-class for sensor-driven and complex-trigger interactions (tilt, sound, time-based). Niche but high-fidelity. The handoff is a video plus the ProtoPie file; engineers do not consume ProtoPie files directly.

### Animation-focused tools

**LottieFiles / After Effects → Lottie.** The canonical 2018–2024 answer for character animation, branded loaders, and decorative motion. The handoff is a Lottie JSON file that the engineer drops into a runtime player. Where it works: deterministic, playback-only animation. Where it doesn't: anything interactive or state-driven, and (a 2026 caveat) the format ships a lot of bytes per kilobyte of motion.

**Rive.** The 2024–2026 successor for interactive animation. Designers build a state machine in the Rive editor; engineers integrate the runtime and drive the state machine from app state. The handoff is a `.riv` file plus a list of state machine inputs. This is the closest the field has to a "motion component" handoff — the designer ships an interactive artefact, the engineer integrates it without re-implementing the motion. Where it works: icons, illustrations, controls with motion identity (a heart that fills, a hamburger that morphs to a close, a button that transitions through loading and success). Where it doesn't: motion that needs to drive arbitrary layout (Rive does not own page transitions or layout-affecting animations).

**Jitter, Phase, Cavalry.** Web-native motion tools producing exportable assets. Newer entrants; none has emerged as the default. Worth monitoring; not yet a standardisation target.

### Video-focused

**Loom / Quicktime / After Effects exports.** The fallback when nothing else works. Adequate for communicating intent, useless as a spec. The cost is that engineers extract timing from frame-counting and easing from eyeballing, which is exactly the gap this file argues should be closed.

### Code-focused

**Storybook with motion examples.** The engineer-authored answer to the gap. A motion-component example in Storybook is, by definition, an implementable spec — the code *is* the spec. Where this works: shared component library motion, where the canonical implementation lives in the DS itself. Where it doesn't: product-specific motion the DS team did not author, which is most micro-interactions.

**Codepen / Stackblitz references.** A designer or developer prototypes a single interaction in code as the spec. High fidelity, low reusability, and depends on the design team having a developer who can produce code-as-spec — which most agency design teams do not.

### Token-focused

**Motion tokens and patterns as a spec.** A spec that says "the modal uses the dialog enter pattern" delegates the actual specification to the pattern definition. This is the most undervalued option in the field. **Where motion is systematised (see 18), most micro-interactions need only a pattern reference, a trigger, and a reduce-motion note.** The pattern already encodes the tracks — each property's from/to values, duration or spring, easing and delay — plus choreography, the reduced substitute and behavioural rules, all by token reference. The annotation collapses to four fields, not eight.

Our May version of this argument said the *composite token* did that work. It cannot: a DTCG composite carries one duration and one easing and binds no property. What we were describing is what 18 now calls a **motion pattern**, a tier above tokens. The argument survives the correction intact: **the motion spec problem is partially a motion system problem.** Components that pick named patterns do not need a full per-interaction spec; they need an annotation pointing to the pattern. Components whose motion legitimately diverges from the pattern set need full specs, but that set is small — and when the same divergence recurs, it is a new pattern.

---

## A practical handoff contract

The recommendation, given the state of the tooling, is a layered contract:

**Layer 1 — pattern reference.** For any motion that is a standard motion pattern (which should be most of them, by design), the spec is a single line:

```yaml
trigger: onMount
motion: dialog/enter
reduce-motion: defined in pattern
```

This is sufficient because the `dialog/enter` pattern already encodes its tracks, timing by token reference, choreography, and reduced substitute. The engineer reaches for the pattern; the pattern is already correct. In Figma, the designer applies the generated "Dialog / enter" custom animation style, and the reference is the same name.

**Layer 2 — full spec, when motion diverges from the pattern set.** For motion that genuinely needs a custom spec — a unique hero animation, a brand-expressive moment, an experimental interaction — the spec contains the eight fields above. Format options below.

**Layer 3 — Rive runtime, when motion is component-shaped.** For interactive icons, animated controls, and motion-as-component artefacts, the handoff is a `.riv` file plus the state machine input list. The engineer integrates the runtime; the designer owns the motion identity.

**Layer 4 — Lottie playback, when motion is deterministic and decorative.** For onboarding illustrations, branded loaders, and playback-only motion that is not interactive, Lottie remains the right artefact in 2026. The DS should publish guidance on file size budgets, runtime version, and the Lottie features supported by each platform's player (not all Lottie features work in all platforms; this is a frequent failure mode).

**Layer 5 — video plus narrative, only as fallback.** When none of the above applies, video is the fallback, and the spec must include written notes covering the eight fields. Video without notes is not a spec.

This contract works because it routes most motion to Layer 1 (where the pattern does the specification work), routes interactive motion to Layer 3 (where Rive does the work), and reserves the bespoke-spec burden for the small number of cases where it is genuinely required.

---

## Format for the full spec (Layer 2)

Two viable formats, parallel to the Pattern A / Pattern B distinction in 17-accessibility-annotation-contract. (The naming collision is unfortunate: Pattern A and Pattern B are *handoff formats*; a *motion pattern* is the tier in 18. A motion pattern spec is a Pattern B file.)

**Pattern A — Figma layer annotations.** The spec lives in Figma as a structured set of layer notes or comments, one per animatable element. Pros: lives where the design lives, easy for designers to update. Cons: hard to surface in code, hard to version, depends on a Figma plugin or convention.

**Pattern B — motion spec file alongside the component.** The spec lives in the codebase or the DS docs site as a YAML or JSON file, one per component. Pros: versioned, surfaceable in MCP context for AI coding agents, machine-readable. Cons: requires designers to author outside Figma, or requires a Figma → file pipeline.

```yaml
pattern: dialog/enter
phase: enter
tracks:
  - { target: scrim, property: opacity, from: 0, to: 1,
      duration: duration/short, easing: easing/enter }
  - { target: panel, property: opacity, from: 0, to: 1,
      spring: spring/default-effects, delay: 50ms }
  - { target: panel, property: translateY, from: distance/sm, to: 0,
      spring: spring/default-spatial, delay: 50ms }
interruptible: true
skipOnRapidRepeat: true
reducedMotion:
  substitute: drop-spatial   # panel translateY removed; opacity tracks kept, reduced duration
lowPower: same-as-reduced
iterations: 1
```

A component's own file then holds only the reference — `motion: { enter: dialog/enter, exit: dialog/exit }` — plus any Layer 2 spec for motion no pattern covers, in the same track shape.

**The practice's recommendation: Pattern B, with the same rationale as 17.** A motion spec file alongside the component is the artefact MCP servers can surface to AI coding agents, the artefact CI can validate, and the artefact engineers can reference without leaving the codebase.

**The bridge now runs from the file to Figma, not the other way.** Our May position was that the missing piece was a Figma plugin to emit Pattern B from Pattern A authoring. Figma Motion reversed the economics: the Plugin API can create custom animation styles, add first-party entries, and bind every entry's duration and easing to TIMING and EASING variables, so **generating Figma Motion from a Pattern B spec is buildable today.** Each pattern becomes a custom animation style ("Dialog / enter") whose entries are Opacity, Position, Scale and Size animations with per-entry offsets for per-property timing and stagger; each pattern with a property-substituting reduced form also becomes "Dialog / enter / reduced"; springs emit as a custom spring (bounce) plus a paired TIMING variable for perceptual duration. Two defects to guard against in any such generator: TIMING is stored in seconds, which makes off-by-a-thousand the likeliest bug, and prototype transitions need literal values rewritten on every token change. This strengthens the Pattern B recommendation: designers see and apply the system's motion in Figma, and the file stays the source.

---

## What works, what doesn't, in 2026

**What works:**

- Motion that is a named pattern composed from tokens; spec collapses to a pattern reference.
- Figma Motion custom animation styles *generated from* the pattern spec, with durations and easings bound to TIMING and EASING variables, for designers to see and apply.
- Interactive iconography handed off as Rive `.riv` files.
- Lottie for decorative, playback-only motion (with file-size discipline).
- Code-as-spec for motion that lives in the DS itself, surfaced via Storybook.

**What partially works:**

- Smart Animate for communicating feel between two designers who already share vocabulary.
- Figma Motion as the authoring surface for a new pattern's timing, provided the behavioural fields are then written into the spec file.
- Framer prototypes lifted into React when the team is React-aligned and Framer-fluent.
- Video plus written notes when the notes are actually written.

**What does not work:**

- Smart Animate as a spec for an engineer in a different framework, different team, or different time zone.
- Video without written notes.
- Per-engineer reconstruction from a Loom clip and a Slack message — the current default.

The practice should explicitly ban the last failure mode and route every motion task to one of the four layers above.

---

## How AI changes this

The 2026 shift the field is undercounting: **AI coding agents will produce motion code whether or not the spec is good.** An agent given a Figma file and a vague prompt will generate animation code; the code will work; the motion will be wrong in subtle ways that compound across the product. The fix is upstream — the agent must consume motion tokens and motion patterns (15, 18) as part of its context. When it does, agent-generated motion converges on the system's motion identity. When it doesn't, agent-generated motion fragments faster than human-authored motion ever did.

**This makes Pattern B (machine-readable spec files) more valuable than it would have been pre-AI.** An MCP server surfacing a motion spec file alongside the component schema lets an agent produce framework-specific motion code that respects the spec. The agent is not the customer of the spec; the agent is the implementer the spec was always written for.

**The Figma MCP server now surfaces motion per node.** Its `get_motion_context` tool returns keyframe tracks and easing for an animated node, with pre-computed CSS `@keyframes` and motion.dev snippets (Figma MCP tool schema, October 2026). That supersedes our May note that the server surfaced motion variables but not per-component motion. It does not change the recommendation: what the agent recovers from Figma is the *rendered* pattern, without the behavioural fields a style cannot hold. An agent working from the Pattern B file gets those; an agent working from Figma alone gets timing and has to guess the rest. The practice standardises on the file and treats the MCP surface as a convenience for motion that has no pattern yet.

---

## Failure modes to watch

- **Spec as Loom video.** The default, and the failure mode this file exists to address. Engineers reconstruct timing from frame-counting; result is inconsistent with the rest of the system.
- **Spec as Smart Animate prototype.** Better than video, still inadequate. The prototype's easing is not the runtime's easing; the engineer ships an approximation that compounds across components.
- **Rive used for decorative motion.** The 200KB+ WASM runtime is overkill for a single decorative loader; Lottie or CSS is the right tool. Rive is for interactive, state-driven motion.
- **Lottie used for interactive motion.** The reverse failure. Lottie is a playback format; interactive Lottie is a workaround. Rive is the 2026 answer.
- **Patterns skipped because designers don't think in tokens.** The whole layered contract above depends on the designer being able to reference `dialog/enter` in the spec. Generated Figma animation styles help — the designer applies "Dialog / enter" rather than remembering a name — but only if the styles are generated, not hand-made. If the designer's mental model is "300ms ease-out", the system has to translate, and the translation is where errors accumulate. (Designer enablement on motion tokens and patterns is a real workstream, not an assumption.)
- **Figma Motion styles edited as the master.** A designer adjusts the "Dialog / enter" style in the library file; the change never reaches the pattern spec or code, and the next generator run silently overwrites it. Figma renders patterns; the file owns them.
- **Reduced motion expected from a mode alone.** The team sets up a `reduced` mode on the motion variables and assumes reduced motion is handled. The mode shortens durations; it cannot turn a slide into a fade. The "/ reduced" style, and the pattern field behind it, are still needed.
- **TIMING written in milliseconds.** Figma stores TIMING in seconds and shows milliseconds; a pipeline that writes `300` produces a five-minute animation.
- **AI agent generates motion without consuming the spec.** The agent does not check whether the spec file exists; it improvises. The fix is at the agent's prompt and context, not at the spec.

---

## Tensions and open questions

1. **Pattern A vs. Pattern B as the practice default — reframed (November 2026).** Pattern A is where designers want to work; Pattern B is where engineers and agents need the data. In May we said the bridge was a Figma plugin emitting Pattern B from Pattern A authoring, which did not exist. The useful bridge now runs the other way — Pattern B generates Figma Motion styles — and it is buildable on today's Plugin API. What stays open is the round trip: when a designer wants a *new* pattern, they still author it somewhere, and authoring it in Figma means the behavioural fields have to be added in the file afterwards. Several mechanics of the generated path are untested — whether TIMING can bind a manual keyframe's position, whether EASING accepts cubic-bezier values outside [0, 1], cross-collection aliasing for TIMING and EASING, REST support for both, library versioning of custom styles, and whether a style applied to a differently structured node fails (see 09).

2. **The Rive runtime cost on small systems.** ~200KB of WASM is acceptable for a product with 10+ interactive motion components; it is excessive for a product with 1–2. The DS should publish a decision rule (rough threshold: Rive becomes worth it past three interactive motion components, or one mission-critical one).

3. **Motion specs in the AGENTS.md / CLAUDE.md surface.** AI coding agents consume their context from these files (and from MCP servers). The practice has not yet decided whether motion specs are surfaced inline in agent context, or fetched on demand from a separate file. Both work; the trade-off is context-window cost vs. lookup latency.

4. **The web extension of this file.** The mobile-implementation pair (20) makes the case that motion specs are most acute on mobile because frameworks diverge most. The web pair (19) suggests motion specs on web are converging on a smaller set of primitives (CSS / WAAPI / View Transitions) where the spec maps more directly to code. The handoff contract above is platform-neutral; the *acuteness* of the gap varies by platform. The practice should be honest about this in client conversations.

5. **Whether to include interruption in every spec.** The eight-field full spec lists interruption as one of the fields. In practice, most micro-interactions are not interrupted, and over-specifying interruption is a tax on the designer for little engineering value. Argument for: encoding it makes implementation deterministic. Argument against: most motion does not need it. Lean toward including it for any motion driven by direct manipulation (gesture-driven sheets, dragged cards) and omitting for triggered animations (modal opens, route changes).

6. **Figma's spring duration.** We emit springs to Figma as bounce plus a paired perceptual duration. Whether Figma's spring duration means perceptual duration or settling time is untested against SwiftUI's `Spring(duration:bounce:)` playback; until it is, cross-tool calibration of springs carries an unknown.

7. **Code Connect for motion components.** Figma's Code Connect maps Figma components to code components. It does not yet map Figma motion to code motion. The Figma 2026 roadmap includes motion variables in Code Connect; the practice should track it, though the generated-styles bridge above no longer depends on it.

---

## See also

- **17-accessibility-annotation-contract** — the architectural parallel to this file. Same handoff failure mode, same Pattern A vs. Pattern B distinction, same recommendation toward machine-readable artefacts.
- **18-motion-foundations** — the token and pattern tiers this file's Layer 1 spec depends on, the minimum viable pattern set, and the decision frameworks (including which Figma vehicle carries what). The motion spec problem is partially a motion system problem.
- **15-ai-in-ds** — components-as-data and the architectural prerequisites for AI-consumable motion specs.
- **12-figma-practice** — Figma-specific surface for designer authoring; the Figma Motion limits are described in this file.
- **19-motion-implementation-web** — what an engineer consumes from this spec on the web side, including AI-agent guardrails for motion code.
- **20-motion-implementation-mobile** — what an engineer consumes from this spec on the mobile side, and the per-framework Rive and Lottie integration.
- **03-component-library** — the components-as-data argument and the existing gap where motion specs were flagged as missing from component templates.

---

*Provenance: The original (May 2026) Figma inadequacy diagnosis, the eight-field sufficient spec, the layered handoff contract, and Pattern A / Pattern B as the format choice are synthesised from the dual-agent research outputs in `_research/_inbound/2026-05-14-motion-foundations-and-spec/` (May 2026), Uber's uSpec AI agent reporting (2025), Token Studio's composite-token treatment (2024–2025), and the Figma MCP server's motion-variables surface (2025–2026). The "spec problem is partially a token problem" argument is internal POV building on 18 and 15. The Rive vs. Lottie 2026 boundary is from the web (`_research/_inbound/2026-05-14-motion-implementation-web/`) and mobile (`_research/_inbound/2026-05-14-motion-implementation-mobile/`) research outputs. The architectural parallel to 17 (annotation contract) is internal POV from the prior mobile-accessibility synthesis. The AI-agent argument that motion-token-aware agents produce better motion is from the foundations and web research outputs. The November 2026 revision — the narrowed Figma position (adequate for timed motion, inadequate for behaviour), the dated Figma Motion capabilities and limits, the pattern reference replacing the composite-token reference, the reversed Pattern B → Figma bridge, the `get_motion_context` update, and the new failure modes — is promoted from `_research/_synthesis/2026-10-14-motion-tokens-and-figma-motion.md` (its section "What this run supersedes in 21"), which reconciles `_research/_inbound/2026-10-14-motion-tokens-and-figma-motion/` and carries the verification ledger. Figma capabilities are from the Figma blog (*Introducing Figma Motion*, 2026-06-24), Plugin API Updates 133 (2026-08-05) and 140 (2026-09-30), the `figma.motion`, Motion types and `CustomAnimationStyle` reference pages, `@figma/plugin-typings` 1.141.0, the Figma variables help article, and a live plugin API test, all checked 2026-10-14. External-agent claims that failed the ledger — modes binding reduced-motion styles, styles as keyframe containers, `physicalSpringToNormalized` as a native physics input, Bezier-only springs, a Dev Mode motion export tab — are excluded.*

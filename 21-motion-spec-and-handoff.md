---
type: practice-area
title: Motion Spec and Handoff
description: The designer-to-developer micro-interaction spec gap. Why Figma is structurally inadequate for motion, the eight-field sufficient spec, the layered handoff contract, Pattern A vs. Pattern B.
tags: [extension, motion, handoff, figma, spec]
timestamp: 2026-05-16
---

# 21 — Motion Spec and Designer–Developer Handoff

> Motion is the part of the design system designers cannot reliably hand off in Figma. The result is the motion equivalent of the accessibility annotation problem (17): whatever ends up in production is whatever the engineer improvised, sometimes informed by a Loom video and a Slack message. This file is what a sufficient motion spec contains, what the candidate tools actually produce, and what the practice should standardise on as the canonical handoff artefact — recognising that the field has not yet converged on a single answer.

---

## Why this is its own file

The motion foundation layer (18) and the per-platform implementation layers (19, 20) assume that designers and engineers agree on what motion to ship. That assumption is wrong in 2026 — and it has been wrong for the entire history of digital product design. **Figma is structurally inadequate for spec'ing micro-interactions.** Smart Animate is good enough to communicate the general feel of a transition but not good enough to specify it; its timing, easing, and trigger semantics are not a faithful representation of any production runtime. What ships is the developer's best interpretation of a 7-second video clip, modulated by whether the designer is in the same Slack channel.

This is the same handoff failure mode that 17-accessibility-annotation-contract addresses for accessibility, and the structural fix is parallel: encode the spec as a contract the designer fills in and the engineer implements, rather than as a video the engineer interprets. Motion is harder than accessibility on this dimension because the spec includes time as a first-class dimension and most design tools were not built for it. The field has produced a half-dozen partial answers; this file's job is to surface them honestly and recommend what the practice should standardise on as the engineering target while the tooling matures.

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

## Why Figma is currently inadequate

The diagnosis matters because the remediation depends on it. Figma's limitations are not failures of imagination; they are structural consequences of how the tool models design.

1. **Smart Animate matches by layer name and interpolates.** This is a layout-tweening model, not an animation model. It cannot express overshoot, spring physics, anticipation, follow-through, or any animation whose start and end positions are not both static layouts.

2. **There is no notion of "trigger".** A Figma prototype navigates between frames; it does not model "this element animates on mount", "this animates on scroll into view", or "this animates after a 200ms delay following another animation".

3. **Easing is a closed set of presets.** The Bezier curves Figma exposes are not the curves any modern runtime ships. The visual approximation in the prototype is not the timing the user will see in production.

4. **Reduce-motion does not exist as a model.** Figma cannot express "this animation has an alternate form for users who have requested reduced motion."

5. **Springs are not a primitive.** The 2024 introduction of *Smart Animate Spring* added a single preset; it is not a tokenised spring system and not a faithful approximation of any production framework's spring.

6. **Choreography across components is not addressable.** Figma's prototype model is frame-to-frame; a complex orchestration across five components requires five overlapping interactions and the result is brittle.

These are not bugs; they are the consequence of a tool optimised for static layout. The field's response has been a long tail of workarounds, none of which has stabilised as the standard.

---

## The candidate tooling landscape

What follows is the current shape of the field, ordered roughly by adoption. None of these is the answer. The practice's job is to pick the artefact engineers will actually receive and standardise on it.

### Prototype-focused tools

**Figma prototypes (+ Smart Animate).** The default. Communicates feel, fails on specifics. The engineer ends up watching the prototype and writing the animation by feel. Where it does work: simple state transitions between two well-defined layouts. Where it doesn't: anything with springs, choreography, or interruption.

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

**Motion tokens themselves as a spec.** A spec that says "the modal uses `motion/modal/enter`" delegates the actual specification to the token definition. This is the most undervalued option in the field. **Where motion is tokenised (see 18), most micro-interactions need only a token reference, a trigger, and a reduce-motion note.** The composite token already encodes duration, easing, and the properties animated. The annotation collapses to four fields, not eight.

This is the architectural payoff of motion tokens that 18 argues for, and it is the answer the field has not yet collectively recognised: **the motion spec problem is partially a motion token problem.** Components that compose from named tokens do not need full per-interaction spec; they need an annotation pointing to the token. Components whose motion legitimately diverges from the token set need full specs, but that set is small.

---

## A practical handoff contract

The recommendation, given the state of the tooling, is a layered contract:

**Layer 1 — token reference.** For any motion that is a standard composition of motion tokens (which should be most of them, by design), the spec is a single line:

```yaml
trigger: onMount
motion: motion/modal/enter
reduce-motion: defined in token
```

This is sufficient because `motion/modal/enter` already encodes duration, easing, properties animated, and reduce-motion fallback. The engineer reaches for the token; the token is already correct.

**Layer 2 — full spec, when motion diverges from the token set.** For motion that genuinely needs a custom spec — a unique hero animation, a brand-expressive moment, an experimental interaction — the spec contains the eight fields above. Format options below.

**Layer 3 — Rive runtime, when motion is component-shaped.** For interactive icons, animated controls, and motion-as-component artefacts, the handoff is a `.riv` file plus the state machine input list. The engineer integrates the runtime; the designer owns the motion identity.

**Layer 4 — Lottie playback, when motion is deterministic and decorative.** For onboarding illustrations, branded loaders, and playback-only motion that is not interactive, Lottie remains the right artefact in 2026. The DS should publish guidance on file size budgets, runtime version, and the Lottie features supported by each platform's player (not all Lottie features work in all platforms; this is a frequent failure mode).

**Layer 5 — video plus narrative, only as fallback.** When none of the above applies, video is the fallback, and the spec must include written notes covering the eight fields. Video without notes is not a spec.

This contract works because it routes 80% of motion to Layer 1 (where the token does the specification work), routes interactive motion to Layer 3 (where Rive does the work), and reserves the bespoke-spec burden for the small number of cases where it is genuinely required.

---

## Format for the full spec (Layer 2)

Two viable formats, parallel to the Pattern A / Pattern B distinction in 17-accessibility-annotation-contract.

**Pattern A — Figma layer annotations.** The spec lives in Figma as a structured set of layer notes or comments, one per animatable element. Pros: lives where the design lives, easy for designers to update. Cons: hard to surface in code, hard to version, depends on a Figma plugin or convention.

**Pattern B — motion spec file alongside the component.** The spec lives in the codebase or the DS docs site as a YAML or JSON file, one per component. Pros: versioned, surfaceable in MCP context for AI coding agents, machine-readable. Cons: requires designers to author outside Figma, or requires a Figma → file pipeline.

```yaml
component: Modal
interactions:
  - id: enter
    trigger: open
    properties:
      - { property: opacity, from: 0, to: 1 }
      - { property: translateY, from: 16px, to: 0 }
    timing: { token: motion/modal/enter }
    reduce-motion: cross-fade
    choreography:
      backdrop: { delay: 0, duration: token }
      panel: { delay: 50ms, duration: token }
  - id: exit
    trigger: close
    properties:
      - { property: opacity, from: 1, to: 0 }
    timing: { token: motion/modal/exit }
    interruption: cancel-and-reverse
```

**The practice's recommendation: Pattern B, with the same rationale as 17.** A motion spec file alongside the component is the artefact MCP servers can surface to AI coding agents, the artefact CI can validate, and the artefact engineers can reference without leaving the codebase. Designers author it either directly or through a Figma plugin that emits the file — the same architectural pattern as the AI-readable component metadata in 15.

---

## What works, what doesn't, in 2026

**What works:**

- Motion that is tokenised and composed from named tokens; spec collapses to a token reference.
- Interactive iconography handed off as Rive `.riv` files.
- Lottie for decorative, playback-only motion (with file-size discipline).
- Code-as-spec for motion that lives in the DS itself, surfaced via Storybook.

**What partially works:**

- Smart Animate for communicating feel between two designers who already share vocabulary.
- Framer prototypes lifted into React when the team is React-aligned and Framer-fluent.
- Video plus written notes when the notes are actually written.

**What does not work:**

- Smart Animate as a spec for an engineer in a different framework, different team, or different time zone.
- Video without written notes.
- Per-engineer reconstruction from a Loom clip and a Slack message — the current default.

The practice should explicitly ban the last failure mode and route every motion task to one of the four layers above.

---

## How AI changes this

The 2026 shift the field is undercounting: **AI coding agents will produce motion code whether or not the spec is good.** An agent given a Figma file and a vague prompt will generate animation code; the code will work; the motion will be wrong in subtle ways that compound across the product. The fix is upstream — the agent must consume motion tokens (18) and composite motion tokens (15, 18) as part of its context. When it does, agent-generated motion converges on the system's motion identity. When it doesn't, agent-generated motion fragments faster than human-authored motion ever did.

**This makes Pattern B (machine-readable spec files) more valuable than it would have been pre-AI.** An MCP server surfacing a motion spec file alongside the component schema lets an agent produce framework-specific motion code that respects the spec. The agent is not the customer of the spec; the agent is the implementer the spec was always written for.

The Figma MCP server's *motion variables* surface (2025–2026) is the field's first attempt at this pipeline. It surfaces tokens to agents but does not yet surface per-component motion specs. The gap is well-understood by Figma and likely to close; the practice should standardise on a file format that survives the closure.

---

## Failure modes to watch

- **Spec as Loom video.** The default, and the failure mode this file exists to address. Engineers reconstruct timing from frame-counting; result is inconsistent with the rest of the system.
- **Spec as Smart Animate prototype.** Better than video, still inadequate. The prototype's easing is not the runtime's easing; the engineer ships an approximation that compounds across components.
- **Rive used for decorative motion.** The 200KB+ WASM runtime is overkill for a single decorative loader; Lottie or CSS is the right tool. Rive is for interactive, state-driven motion.
- **Lottie used for interactive motion.** The reverse failure. Lottie is a playback format; interactive Lottie is a workaround. Rive is the 2026 answer.
- **Composite tokens skipped because designers don't think in tokens.** The whole layered contract above depends on the designer being able to reference `motion/modal/enter` in the spec. If the designer's mental model is "300ms ease-out", the system has to translate, and the translation is where errors accumulate. (Designer enablement on motion tokens is a real workstream, not an assumption.)
- **AI agent generates motion without consuming the spec.** The agent does not check whether the spec file exists; it improvises. The fix is at the agent's prompt and context, not at the spec.

---

## Tensions and open questions

1. **Pattern A vs. Pattern B as the practice default.** Pattern A is where designers want to work; Pattern B is where engineers and agents need the data. The bridge is a Figma plugin that emits Pattern B from Pattern A authoring. The plugin does not yet exist as a turnkey product, and the practice would have to build or commission it.

2. **The Rive runtime cost on small systems.** ~200KB of WASM is acceptable for a product with 10+ interactive motion components; it is excessive for a product with 1–2. The DS should publish a decision rule (rough threshold: Rive becomes worth it past three interactive motion components, or one mission-critical one).

3. **Motion specs in the AGENTS.md / CLAUDE.md surface.** AI coding agents consume their context from these files (and from MCP servers). The practice has not yet decided whether motion specs are surfaced inline in agent context, or fetched on demand from a separate file. Both work; the trade-off is context-window cost vs. lookup latency.

4. **The web extension of this file.** The mobile-implementation pair (20) makes the case that motion specs are most acute on mobile because frameworks diverge most. The web pair (19) suggests motion specs on web are converging on a smaller set of primitives (CSS / WAAPI / View Transitions) where the spec maps more directly to code. The handoff contract above is platform-neutral; the *acuteness* of the gap varies by platform. The practice should be honest about this in client conversations.

5. **Whether to include interruption in every spec.** The eight-field full spec lists interruption as one of the fields. In practice, most micro-interactions are not interrupted, and over-specifying interruption is a tax on the designer for little engineering value. Argument for: encoding it makes implementation deterministic. Argument against: most motion does not need it. Lean toward including it for any motion driven by direct manipulation (gesture-driven sheets, dragged cards) and omitting for triggered animations (modal opens, route changes).

6. **Code Connect for motion components.** Figma's Code Connect maps Figma components to code components. It does not yet map Figma motion to code motion. The Figma 2026 roadmap includes motion variables in Code Connect; the practice should track this as the most likely path to closing the gap inside Figma rather than around it.

---

## See also

- **17-accessibility-annotation-contract** — the architectural parallel to this file. Same handoff failure mode, same Pattern A vs. Pattern B distinction, same recommendation toward machine-readable artefacts.
- **18-motion-foundations** — the token layer this file's Layer 1 spec depends on. The motion spec problem is partially a motion token problem.
- **15-ai-in-ds** — components-as-data and the architectural prerequisites for AI-consumable motion specs.
- **12-figma-practice** — Figma-specific surface for designer authoring of motion specs, and the limits this file describes.
- **19-motion-implementation-web** — what an engineer consumes from this spec on the web side, including AI-agent guardrails for motion code.
- **20-motion-implementation-mobile** — what an engineer consumes from this spec on the mobile side, and the per-framework Rive and Lottie integration.
- **03-component-library** — the components-as-data argument and the existing gap where motion specs were flagged as missing from component templates.

---

*Provenance: The Figma inadequacy diagnosis, the eight-field sufficient spec, the layered handoff contract, and Pattern A / Pattern B as the format choice are synthesised from the dual-agent research outputs in `_research/_inbound/2026-05-14-motion-foundations-and-spec/` (May 2026), Uber's uSpec AI agent reporting (2025), Token Studio's composite-token treatment (2024–2025), and the Figma MCP server's motion-variables surface (2025–2026). The "spec problem is partially a token problem" argument is internal POV building on 18 and 15. The Rive vs. Lottie 2026 boundary is from the web (`_research/_inbound/2026-05-14-motion-implementation-web/`) and mobile (`_research/_inbound/2026-05-14-motion-implementation-mobile/`) research outputs. The architectural parallel to 17 (annotation contract) is internal POV from the prior mobile-accessibility synthesis. The AI-agent argument that motion-token-aware agents produce better motion is from the foundations and web research outputs.*

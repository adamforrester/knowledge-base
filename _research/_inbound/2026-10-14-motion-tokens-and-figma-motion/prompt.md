You are researching how a design system should encode motion as tokens and reusable patterns, and how that system should integrate with Figma's native motion tooling as it exists in late 2026, for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our practice generates design-system token layers from a small brand input and writes them into Figma and code. Motion today ships as duration tokens (a value scale plus semantic roles and reduced-motion twins), named cubic-bezier easing curves with a role tier above them (default, enter, exit, emphasized), three spring presets expressed as damping ratio and stiffness, and composite transition tokens (duration + easing). An earlier research run (May 2026) concluded that Figma was structurally inadequate for motion. That has since changed: Figma now ships a motion timeline with first-party animation definitions, local reusable "custom animation styles" composed from those definitions, and TIMING and EASING variable types that animation styles and keyframes can bind to. A real brand's motion inventory (about 105 production animations) also surfaced gaps our token model cannot express: brand-defined easing curves, scroll- or progress-driven motion, physics beyond a few spring presets (very bouncy springs, inertia/decay), per-property easing within one transition, and out-and-back pulses. We want to know whether our model is on target, what to add, and what to deliberately leave out.

This is not an introductory motion guide. Assume the reader knows easing curves, springs, stagger, choreography, productive vs. expressive motion, reduced motion, and DTCG tokens. Explain at the level needed to make architectural decisions about a token model and its Figma integration.

Research scope — cover all of the following. Use these as the section spine of the output:

1. What mature design systems ship as motion tokens today

   - Duration, easing, spring and composite/transition tokens across Material 3 (including its spring-based motion physics), Carbon, Fluent 2, Atlassian, Polaris, Spectrum, Apple HIG/SwiftUI and others you can verify. What they name, how many steps, semantic vs. literal naming.
   - Where the field has converged and where it still diverges. Whether systems let a brand define its own curves, or only choose among presets.
   - How springs are parameterized (damping ratio + stiffness, response + damping fraction, duration + bounce) and how systems convert between those models.

2. Pattern-level motion: presets for components and transitions

   - Whether systems ship named motion patterns tied to components or interaction types (dialog enter/exit, drawer/sheet slide, toast, menu, accordion expand, page transition, shared-element/container transform), and what a pattern specifies (properties, distances, scale, opacity, duration/easing tokens, choreography/stagger).
   - How those patterns are documented and handed off, and how they stay brand-tunable (a tempo or personality lever) without per-pattern re-authoring.
   - Whether a pattern library belongs in the token layer, the component layer, or a separate motion layer.

3. Figma's native motion tooling, late 2026

   - What Figma Motion can express: the timeline, first-party animation definitions, local custom animation styles, keyframes, and what TIMING and EASING variables can bind to (and cannot, e.g. prototype transitions). Date every claim and give the verification path; this area changes quickly.
   - How a token pipeline should map onto it: durations, curves, springs (Figma stores a normalized bounce), role aliases, modes, publishing and scoping limits.
   - Whether reusable custom animation styles are a sound vehicle for system-level motion patterns (e.g. "Dialog enter"), and their limits (what they can't express, how they version and publish through libraries).
   - How other tools (Rive, Lottie, Jitter, ProtoPie, code-first tools) fit alongside Figma for what Figma can't express.

4. The hard cases: what tokens can and can't carry

   - Brand-defined easing curves: how systems allow them safely (naming, guardrails, accessibility).
   - Scroll-linked and progress-driven motion (parallax ratios, scroll-triggered reveals, scroll-timeline animations): should these be tokens, pattern specs, or out of scope? What do CSS scroll-driven animations and native platforms offer?
   - Physics beyond spring presets: very bouncy springs, inertia/decay after a flick, interruptible and velocity-preserving motion. What is tokenizable and what is implementation.
   - Per-property easing within one transition, and out-and-back (pulse/yo-yo) motion: how systems express these, if at all.

5. Reduced motion and accessibility as architecture

   - How systems encode reduced-motion alternatives (twins, substitution of fades for movement, zeroed durations, exemptions for essential motion) and how that maps into Figma modes and code.
   - WCAG 2.2 criteria relevant to motion (2.2.2, 2.3.3) and how systems operationalize them; vestibular-safe guidance.

6. Platform delivery

   - How motion tokens reach CSS (including linear() for springs), iOS/SwiftUI, Android/Compose and React Native; where stock Style Dictionary and DTCG fall short (DTCG has cubicBezier and duration but no spring or composite pattern type), and how teams work around it.
   - What the DTCG spec and its community discussions say about springs, transitions and motion composites as of late 2026.

7. Recommendations for a generated token system

   - Given the model described in the context paragraph, what to keep, what to add (e.g. brand curves, pattern styles, more spring parameters), and what to explicitly declare out of scope, with decision frameworks rather than a single winner where context matters.
   - What a minimum viable "motion pattern" set looks like for a component library (which patterns, in what order).

Output format: Structured markdown. Use section headings that match the numbered scope above. Synthesize findings — do not list sources mechanically. Where the field has consensus, state it clearly; where decisions are context-dependent, provide decision frameworks rather than declaring a winner. Flag areas where DS tools (Figma, Style Dictionary, DTCG, code pipelines) have known gaps that practitioners work around. Where claims depend on current platform state — feature names, API availability, version numbers, browser support — date them and note the verification path. Include a references section linking to primary sources (design system docs, Figma help center and Plugin API docs, W3C DTCG drafts and issues, WCAG, MDN, Apple and Android developer docs, practitioner write-ups).

Depth: Expert audience. Do not explain what an easing curve or a spring is — explain how systems encode, tune, hand off and deliver them, and where the current tooling breaks.

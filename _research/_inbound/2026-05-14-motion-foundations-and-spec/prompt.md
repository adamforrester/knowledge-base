You are researching motion as a design system concern for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our practice ships design systems for consumer and enterprise products across web, iOS, Android, and cross-platform mobile. Motion appears in our token lists but we don't yet treat it as a first-class foundation — no shared motion principles, no easing studies, no productive-vs-expressive split, no choreography vocabulary. Two separate but related concerns sit underneath this. The first is the architecture: how motion is encoded into the system so consumers can't get it wrong, parallel to how we encode contrast (pair tokens), spacing (scale tokens), and accessibility (the four-layer model). The second is the workflow gap: designers cannot reliably spec micro-interactions in Figma today, which means the motion that ends up in production is whatever the developer improvises. We want both addressed in one piece of research.

This is not an introductory motion guide — assume the reader knows what an easing curve is, what stagger means, what a spring is, the difference between productive and expressive motion at a high level, and what reduce-motion as a system setting does. Explain motion at the level a senior design systems lead would need to make architectural and workflow decisions.

Research scope — cover all of the following. Use these as the section spine of the output:

1. Why motion is a design system concern, not an application concern

   - The case for centralising motion at the system layer rather than letting it accumulate per-product.
   - What goes wrong when motion is treated as a per-screen design choice instead of a system primitive.
   - The cost asymmetry between baking motion into the system early vs. retrofitting consistency later.

2. Motion principles and brand personality

   - How motion principles are articulated and what makes a good one (specific, decidable, brand-aligned).
   - The productive vs. expressive motion split — what each means, when each applies, how the system encodes the distinction.
   - How motion encodes brand personality without being arbitrary or precious.
   - Examples of how mature design systems have done this — and how the field has converged or diverged.

3. Motion tokens

   - Duration tokens — what set of durations a system should ship, how they should be named (semantic vs. literal), and where the field has converged.
   - Easing tokens — standard curves, custom curves, when each is appropriate; the math vs. the names.
   - Spring tokens vs. timing-curve tokens — when to use a spring, when to use a curve; how to express springs as tokens.
   - Composite motion tokens (duration + easing + properties as a unit) and how they map to component animations.

4. Choreography and orchestration

   - The vocabulary the field uses (sequence, stagger, parallel, follow-through, anticipation, settle, etc.).
   - How choreography is encoded at the system level vs. left to the component.
   - Patterns for transitions between states, between routes, between screens.
   - When motion should defer to the component vs. compose across multiple components.

5. Reduce-motion as a system contract

   - How the design system encodes "this animation respects user setting" so that no individual engineer has to remember it.
   - The cross-platform consensus on what to replace motion with (cross-fades vs. snaps vs. shortened durations).
   - The relationship between reduce-motion and other accessibility motion settings (Reduce Transparency, Differentiate Without Color, prefers-reduced-motion media query).
   - Where the design system's responsibility ends and the application's begins.

6. Performance and the cost of motion

   - The performance budget for motion in a design system — frame rate, layout vs. paint vs. compositor work, GPU implications.
   - The web-specific concerns (INP, CLS, paint flashing, will-change misuse).
   - The mobile-specific concerns (60Hz vs. 120Hz, dropped frames during transitions, jank on lower-end devices).
   - How a system should encode "this animation is safe" vs. "this animation is heavy" as a property, not a hope.

7. The micro-interaction handoff problem

   - Why Figma is currently inadequate for spec'ing micro-interactions (the gap and what it costs in practice).
   - The historical workarounds — written specs, video reference, Lottie files, code prototypes, "ask the designer."
   - The field's current consensus on whether this is solved, partially solved, or unsolved.
   - What a sufficient spec for a micro-interaction actually contains (timing, easing, properties animated, trigger, end state, reduce-motion behaviour).

8. Tools and workflow for motion spec

   - The candidate tools designers reach for today — prototype-focused, animation-focused, video-focused, code-focused. Cover the landscape; do not constrain to specific tools.
   - The trade-offs of each category (fidelity vs. effort, reusability vs. one-off, designer-accessible vs. developer-accessible).
   - The handoff artefact each tool produces and what an engineer can actually consume from it.
   - Patterns from teams that have closed this gap — what tooling stack works, what doesn't, what is emerging.
   - What a design system should standardise on as the canonical motion-spec format, given the trade-offs.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where the field has clear consensus, state it; where decisions are context-dependent (brand personality, performance budget, tooling stack), give a decision framework rather than declaring a winner. Flag tooling gaps that practitioners work around. Where claims depend on platform / tool / framework state — feature names, version numbers, vendor pricing, capability claims — date them and note the verification path. Include a references section linking to primary sources (Material motion docs, Apple HIG motion sections, w3c CSS animation specs, framework animation docs, practitioner write-ups by recognised motion designers and DS leads, open-source motion-library docs).

Depth: Expert audience. Do not explain what easing is or what reduce-motion does — explain how a design system encodes motion as a foundation, where the field has converged, what tooling actually works for designer-to-developer micro-interaction spec'ing, and what a practice should standardise on.

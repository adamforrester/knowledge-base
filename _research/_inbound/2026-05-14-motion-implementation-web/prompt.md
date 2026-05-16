You are researching motion implementation on the web for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: most production motion ships on web. Our practice writes design systems whose components animate, transition, and respond to interaction across React, Vue, vanilla, and increasingly AI-generated codebases. We need to give engineers enough depth to implement motion idiomatically and performantly without producing an animation-library cookbook. The bound on this research is: enough to translate a designer's motion spec into idiomatic, performant code in a modern web component, plus the performance gotchas, plus the library landscape. Not exhaustive animation API documentation.

This is not an introductory motion guide — assume the reader knows CSS transitions, basic easing curves, what `requestAnimationFrame` does, and the difference between layout-paint-compositor work. Explain web motion implementation at the level a senior engineer or DS lead needs to ship motion that is consistent, performant, and accessible across a component library.

Research scope — cover all of the following. Use these as the section spine of the output:

1. The primitive layer

   - CSS transitions, CSS animations, the Web Animations API — what each does, where each is appropriate, where the boundaries between them sit in 2026.
   - When to reach for one vs. another for design-system components (transitions for state, keyframes for entrance/exit, WAAPI for orchestration).
   - The current state of CSS Houdini animation worklets and whether they have crossed the threshold of practical use.
   - View Transitions API (cross-document and same-document) — what it gives a DS, what it doesn't, the browser-support state.

2. The library landscape

   - The named libraries practitioners reach for — Framer Motion, GSAP, Motion One, animejs, React Spring, Theatre.js, anime.js, Lottie web, Rive web. Comment on each's positioning and trade-offs.
   - The decision framework: when to ship native primitives only, when to bring in a library, when to pick a spring library vs. a timing library, when to use Lottie/Rive runtime players vs. hand-coded animation.
   - Library trends in 2026 — what's growing, what's stagnating, what's being absorbed into the platform.

3. Spring physics on web

   - Why spring physics matters for component motion (interruption, natural feel, gesture-driven).
   - The current implementation surface — React Spring, Motion One's spring, Framer Motion's spring, native CSS not-yet-shipping spring-easing-function.
   - Spring parameters as tokens — stiffness, damping, mass, velocity — and what good defaults look like.
   - When spring physics is the wrong choice (deterministic transitions, brand-driven choreography).

4. Choreography and orchestration in production

   - The patterns the field has converged on for sequencing entrance/exit of related elements (`AnimatePresence`, `LayoutGroup`, stagger configuration).
   - Route transitions in modern web frameworks (Next.js App Router, React Router, Nuxt, SvelteKit) — what's idiomatic in 2026.
   - The performance and accessibility implications of route transitions.

5. Reduce-motion implementation

   - The `prefers-reduced-motion` media query at the CSS layer.
   - The JS-side equivalents (`window.matchMedia`, library-level support).
   - How the system encodes "respect reduce-motion" so individual engineers don't have to remember (CSS variables, library defaults, helpers).
   - Cross-link only — assume the architectural treatment is covered elsewhere; cover only the web implementation specifics.

6. Performance — what actually matters

   - Compositor-only properties (transform, opacity) vs. layout-triggering properties — the current state in 2026 with modern browsers.
   - `will-change` — when it helps, when it hurts, the documented pitfalls.
   - INP (Interaction to Next Paint, replaced FID in 2024) and how motion affects it.
   - Long animation frames (the LoAF API, 2024) and what they expose.
   - The performance budget a design system should encode at the component level.

7. SVG and canvas animation

   - When SVG animation is the right tool (vector graphics, illustrations, branded loaders).
   - Lottie vs. Rive vs. hand-coded SVG — the trade-offs in 2026.
   - Canvas-based animation for data viz and high-density rendering — the boundary with WebGL.

8. The bridge between designer spec and code

   - What an engineer actually consumes from a designer's motion spec (timing, easing, properties, trigger, end state, reduce-motion fallback).
   - The tooling that produces engineer-consumable artefacts — Lottie JSON, Rive runtime files, CSS variables exported from design tools, code-as-spec patterns.
   - Where the spec-to-code translation is still manual and where it has been automated in 2026.
   - The role of AI code generation in motion implementation (Cursor, Claude Code, Figma Make) — what works, what doesn't.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where the field has clear consensus, state it; where decisions are context-dependent (library choice, performance/feature trade-offs), give a decision framework rather than declaring a winner. Flag platform / library gaps that practitioners work around. Where claims depend on browser / spec / library state — feature names, version numbers, browser-support percentages, library trajectories — date them and note the verification path (caniuse.com, MDN, library changelog). Include a references section linking to primary sources (CSS specs, Web Animations API spec, library docs, MDN, Chrome / WebKit / Firefox release notes, practitioner write-ups, performance documentation).

Depth: Expert audience. Do not explain what a CSS transition is or what easing is — explain what's idiomatic in 2026 web component animation, what the library landscape actually looks like, where the performance pitfalls live, and what design system engineers should standardise on.

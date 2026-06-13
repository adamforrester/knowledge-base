---
type: practice-area
title: Motion Implementation - Web
description: Web motion in 2026. CSS / WAAPI / View Transitions primitives, the linear() spring revolution, library landscape (Motion / GSAP / Rive / Lottie), INP / LoAF / compositor-only performance.
tags: [extension, motion, web, css, view-transitions, performance]
timestamp: 2026-05-16
---

# 19 — Motion Implementation: Web

> Motion on the web in 2026 has stopped being an animation-library decision and become a primitive-layer decision. CSS, WAAPI, and the View Transitions API can do most of what teams reached for Framer Motion or GSAP to do three years ago — and they can do it on the compositor thread, off the main thread, without paying an INP cost. This file is the web spelling of the motion tokens, principles, and choreography defined in 18: which primitives produce which token, which libraries are still worth their weight, and which performance gotchas are now load-bearing.

---

## What changed on web since 2023

The mental model engineers held in 2023 — "CSS for simple state, JS library for anything orchestrated, Lottie for branded motion" — is wrong for 2026. Three platform shifts compress the library footprint:

1. **The `linear()` easing function** (Baseline 2024) makes spring physics expressible as a CSS string. A spring animation that previously required React Spring or Framer Motion can now run as a pure CSS transition with no JavaScript on the main thread.
2. **The View Transitions API** (same-document Baseline 2024; cross-document shipping in Chromium and Safari 18.2+ as of May 2026) makes shared-element and route transitions a browser primitive rather than a library feature.
3. **WAAPI** (Web Animations API) is now Baseline Newly Available — full support in Chrome 111+, Safari 18+, Firefox 133+. The "JS animation that runs on the compositor" pattern no longer needs a library wrapper for most use cases.

The downstream consequence: the answer to "which library should we use" is increasingly "do you need one." Motion that previously required a 30KB runtime can now ship as a few CSS variables and a `transition` declaration.

This is good news for INP. It is also a re-architecture of how DS teams think about motion, because the *enforcement layer* moves from library defaults (the library shipped accessible motion if the engineer configured it) to platform defaults (the platform ships some motion accessibly and not other motion — see the View Transitions reduce-motion gotcha below).

---

## The primitive layer

| Primitive | When it's the right tool | Where it falls down |
|---|---|---|
| CSS transitions | Hover, focus, simple state toggles, single-property animation between two values | No support for orchestration, no callback when complete, no runtime control |
| CSS keyframes | Loading spinners, ambient motion, multi-step deterministic animation | No mid-flight control, no interpolation based on runtime values |
| WAAPI (`Element.animate()`) | Orchestrated animation, runtime-computed values, animations that need callbacks or playback control | Verbose for simple state changes; not declarative in JSX |
| View Transitions API | Same-document state transitions, cross-document route transitions, shared-element transitions across pages | Browser-managed snapshot; harder to override mid-flight; reduce-motion not automatic |
| CSS Houdini Paint API | High-performance custom backgrounds, generative brand patterns | Limited to Chromium and Safari; not used for component-level micro-interactions |

The 2026 default is to **reach for CSS first and add JavaScript only when CSS demonstrably cannot do the job.** This is the inverse of the 2020 default. Where a library is reached for, it is reached for orchestration (sequencing across multiple unrelated DOM elements with runtime-computed values) — not for the underlying animation, which the platform now runs.

---

## The library landscape

| Library | 2026 position | When to reach for it |
|---|---|---|
| Motion (formerly Framer Motion, v12+) | The standard for React-aligned shops. Rewrote core in v12 (2024–2025) as a WAAPI wrapper — animations run on the compositor, not in the React render loop. | React component libraries that want declarative `<motion.div>` syntax and AnimatePresence/LayoutGroup for orchestration. |
| GSAP | The specialist's tool. Sub-millisecond precision, robust interruption, the canonical answer for scroll-driven and timeline-heavy work. | Scrollytelling, marketing pages, data viz, anything where the motion *is* the product. Not the right choice for component-library motion. |
| Motion One | Tiny (~3.8KB), WAAPI wrapper, framework-agnostic. | Vanilla or non-React contexts where Motion is overkill but CSS isn't enough. |
| React Spring | Spring-physics library, runtime physics rather than baked `linear()` curves. | Gesture-driven interactions where springs need to adjust mid-flight; mostly superseded by Motion v12 for component-library use. |
| Lottie (web) | Still the answer for decorative, deterministic playback motion. | Onboarding illustrations, branded loaders, marketing motion. |
| Rive (web) | The 2024–2026 successor to Lottie for interactive iconography. ~200KB WASM runtime. | Stateful icons, interactive controls with motion identity, anything driven by app state. |
| Theatre.js | Editor-as-authoring-tool for complex orchestrated animation. | Designer-led complex timeline work, rare in DS contexts. |
| anime.js / animejs | Legacy general-purpose animation library; largely superseded. | Maintenance of existing code. New work should look elsewhere. |

**The decision framework:**

- Single-property state change → CSS transition. No library.
- Multi-property deterministic animation with no mid-flight control → CSS keyframes or WAAPI. No library.
- Orchestrated entrance/exit across multiple elements with declarative API → Motion (React) or Motion One (vanilla).
- Gesture-driven motion with mid-flight physics adjustment → Motion (which now includes spring physics) or React Spring.
- Cross-page route transitions or shared elements → View Transitions API. No library.
- Interactive iconography or motion-as-component → Rive runtime.
- Deterministic decorative playback → Lottie runtime.
- Scrollytelling, timeline-heavy, or sub-millisecond precision required → GSAP.

**The library tax.** Every library bundle is a tax on initial load and on the engineer's mental model. Three years ago a 30KB animation library was unremarkable; in 2026, with INP as a Core Web Vital and the platform doing more of the work natively, every library imported needs to justify its weight. The default DS posture should be that motion is shipped without a library, and libraries are added when a specific orchestration need outstrips the platform.

---

## Spring physics on web

The largest implementation change since the existing 02-design-foundations and 14-accessibility material was written: **springs on web are now a CSS string, not a JavaScript runtime.**

The `linear()` easing function takes a list of stops and interpolates between them. A spring physics curve, sampled at a high enough resolution and baked at build time, becomes a string the browser can run on the compositor thread. A spring that previously required `useSpring` from React Spring (with its main-thread cost) now runs as:

```css
--easing-spring-snappy: linear(0, 0.45, 0.82, 1.05, 1.08, 1.02, 1);

.button {
  transition: transform 300ms var(--easing-spring-snappy);
}
```

The CSS Spring Easing Generator (csstools.github.io) and similar tooling produce these strings from physical parameters (stiffness, damping, mass). The result is a token-friendly artefact:

```css
--motion-spring-snappy: linear(...);
--motion-spring-gentle: linear(...);
--motion-spring-bouncy: linear(...);
```

This is the implementation layer for the spring tokens 18 defines. The token name is perceptual; the CSS string is the implementation.

**Where `linear()` is the wrong tool:**

- Gesture-driven motion where the spring needs to adjust mid-flight based on velocity. A baked curve cannot respond to a new gesture target. This is where Motion's `useSpring` and React Spring remain right.
- Interruption that needs to settle to current position and animate to a new target. A `linear()` transition cannot do this cleanly because CSS transitions interpolate from current computed value; springs need physics state.

**The cross-platform discipline.** Spring tokens defined as `linear()` strings on web and as native springs on mobile (see 20) must feel the same. The mapping is calibration, not direct translation — the parameters that produce a "snappy" spring in SwiftUI are not the same numbers that produce a "snappy" `linear()` curve. The practice should ship visual reference videos alongside the token definitions, so designers and engineers can validate that the perceptual outcome matches across platforms.

---

## Choreography and orchestration in production

Choreography on web in 2026 is split between three patterns:

**Within-component orchestration → AnimatePresence + LayoutGroup (Motion) or hand-rolled WAAPI.** A modal that animates its backdrop and its panel with a 50ms stagger lives inside the component. Motion's `AnimatePresence` and `LayoutGroup` are the convergent React pattern; the vanilla equivalent is a WAAPI sequence with `getAnimations()` to coordinate.

**Same-page state transitions → View Transitions API (same-document).** A filter change that reorders cards, an accordion that expands, a list that reflows — the View Transitions API lets the browser snapshot the before-state, mutate the DOM, snapshot the after-state, and interpolate. This is the right tool for any transition where the engineer would previously have animated `transform` manually across many elements.

```javascript
document.startViewTransition(() => {
  updateDOM();
});
```

**Cross-page transitions → View Transitions API (cross-document).** Shipping in Chromium and Safari 18.2+; not yet in Firefox as of May 2026. Same opt-in mechanism; works across MPA route changes. This is the closest the platform has come to "shared element transitions" as a browser primitive.

```css
@view-transition { navigation: auto; }

.hero-image {
  view-transition-name: hero-42;
}
```

**The stagger primitive.** Stagger remains a token-and-formula pattern, not a library feature. The DS should ship a `stagger/standard` token (typically 30–60ms) and consumers compute delays as `calc(var(--index) * var(--motion-stagger-standard))`. This works in both CSS transitions and WAAPI sequences. AI coding agents reach for magic numbers (`delay: 0.2s`) when this token is absent; with it, they reach for the token.

**Route transitions in modern frameworks.** Next.js App Router, React Router 7, Nuxt, SvelteKit all now have first-class support for the View Transitions API, removing the need for a framework-specific route-transition library in most cases. The framework-specific spelling matters (Next.js exposes `useViewTransition`; SvelteKit handles it at the routing layer); the underlying API is the same.

---

## Reduce-motion implementation on web

The architectural treatment is in 14-accessibility; the foundation-layer commitment is in 18. The web-specific implementation patterns are:

**CSS layer — the convergent pattern.**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

This is the blanket fallback. It is also the *wrong* default per the informational-vs-vestibular refinement in 18. The DS should encode per-token reduce-motion variants rather than a global override:

```css
:root {
  --motion-duration-medium: 300ms;
  --motion-duration-medium-reduced: 0ms;
}

@media (prefers-reduced-motion: reduce) {
  :root { --motion-duration-medium: var(--motion-duration-medium-reduced); }
}
```

Consumers use `var(--motion-duration-medium)` and the right value is selected automatically. This is the system contract 18 describes.

**The View Transitions reduce-motion gotcha.** `document.startViewTransition()` does *not* automatically respect `prefers-reduced-motion`. If the engineer calls it, the browser runs the transition regardless of the user's setting. The DS must wrap every call site in a check:

```javascript
const safeViewTransition = (callback) => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !document.startViewTransition) {
    callback();
    return;
  }
  document.startViewTransition(callback);
};
```

This is the kind of pattern that needs to ship at the system level — exposed as a helper from the DS — so individual engineers cannot accidentally bypass it. This is a 2026-specific platform gap that 14-accessibility's earlier treatment did not anticipate.

**JS-side detection.** For libraries and JS-driven animation, `window.matchMedia('(prefers-reduced-motion: reduce)').matches` is the primitive. Motion and Framer Motion respect it via their `MotionConfig` provider; engineers must wire this at the application root.

---

## Performance — what actually matters

The 2026 budget is set by INP and LoAF. Both expose motion-related regressions in ways the older RAIL / FID model did not.

**Compositor-only properties.** `transform` and `opacity` are compositor-safe across all modern browsers. `filter` is compositor-safe in Chromium and Safari but not always in Firefox. Everything else triggers layout or paint and is per-frame expensive on the main thread.

**The implication for DS components.** A `Drawer` that animates `width: 0 → 400px` triggers layout on every frame. The convergent alternative is to render the drawer at full size, translate it offscreen with `transform: translateX(-100%)`, and animate the transform. This is a 2015 pattern that still gets violated regularly, especially in AI-generated code where agents reach for the property name that matches the visible behaviour rather than the property that is cheap.

**`will-change` discipline.** `will-change: transform` hints to the browser that an element will be animated, prompting layer promotion. Used universally, it leads to GPU memory bloat and can crash mobile browsers. The 2026 discipline is to apply `will-change` *only during* the active animation — typically by adding it on `mousedown` or `animationstart` and removing it on `animationend`. The library answer is to let Motion or WAAPI manage this; the manual answer is a small `useWillChange` helper. The DS should publish whichever pattern matches the consuming codebase's style.

**INP and motion.** INP measures the time between a user interaction and the next paint. Motion that runs on the main thread (a heavy `requestAnimationFrame` loop, an unoptimised React state update inside an animation) directly inflates INP. Motion on the compositor (CSS transitions, WAAPI on transform/opacity, Motion v12) does not affect INP because the main thread is free to paint.

**LoAF API.** Long Animation Frames is the 2024 successor to Long Tasks. It exposes frames where the browser spent more than 50ms doing work — typically a sign of layout thrash inside an animation. The DS can recommend that consuming products instrument LoAF in dev mode to catch motion regressions:

```javascript
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 50) {
      console.warn('Long animation frame:', entry);
    }
  }
}).observe({ type: 'long-animation-frame', buffered: true });
```

**The 120Hz target.** Most modern devices ship 120Hz displays. A 60Hz-budgeted animation looks broken at 120Hz because the user has been recalibrated by every other surface they interact with. The implication for the system is that the performance budget is no longer "60fps" — it is "matches the device's refresh rate, including 120Hz." This raises the bar on every property except `transform` and `opacity`.

---

## SVG and canvas

**SVG animation in the View Transitions era.** SVG elements are DOM nodes; they participate in View Transitions. Assigning `view-transition-name` to a `<path>` lets the browser interpolate it across page changes, *provided the path has the same number of points on both sides.* This last caveat is non-trivial — a logo that morphs across pages needs its source SVG paths to be topologically compatible.

**SVG for system iconography.** SVG remains the right format for icons in a DS — small, theme-able via CSS variables, accessible to screen readers. Motion on SVG icons (a chevron rotating, a hamburger morphing) should use CSS transitions on `transform`, never on path data, for compositor safety.

**Canvas and WebGL for asset-integrated motion.** Rive's web runtime renders via WebGL, bypassing the DOM's layout engine entirely. This is the right tool for motion that is dense (thousands of particles), high-frequency (data visualisation, generative art), or interactive in ways the DOM cannot cheaply express (a button morphing through five states with sub-pixel precision).

**The WASM tax.** Rive's web runtime is ~200KB gzipped because it ships a full rendering engine in WebAssembly. The threshold the practice should use: Rive becomes worth its weight past three interactive motion components, or one mission-critical one. Below that threshold, SVG + CSS is the right answer.

---

## The spec-to-code bridge on web

The detailed treatment lives in 21. The web-specific notes:

**Motion tokens as the primary handoff.** A motion spec that names `motion/modal/enter` and a trigger collapses to a CSS variable reference in code. The engineer does not implement the motion; the engineer references the token. This is the architectural payoff of 18.

**Lottie on web in 2026.** The `lottie-web` runtime remains the canonical player. The 2024 introduction of the `.lottie` format (compressed) reduces the file-size cost meaningfully. The dotLottie player (`@lottiefiles/dotlottie-web`) is the 2026-recommended runtime for new work.

**Rive on web.** `@rive-app/canvas` is the canonical web runtime. The handoff artefact is the `.riv` file plus a list of state-machine inputs the engineer wires to app state.

**AI coding agents and web motion.** Agents (Claude Code, Cursor, Copilot) reliably produce structurally correct CSS and WAAPI motion code, and reliably produce *wrong* motion values when the system does not provide tokens. The pattern that works: surface motion tokens in `AGENTS.md` / `CLAUDE.md` and in the MCP server's context. The pattern that fails: leave the agent to pick durations and easings from training-data defaults. With composite motion tokens available, agents converge on the system's motion identity; without them, the system fragments.

**The Figma MCP motion-variables surface.** Figma's MCP server (2025–2026) surfaces motion variables to AI agents, allowing the agent to query "what is the enter motion for a modal" and receive a token reference. This is the closest the field has come to the seamless designer-to-agent-to-code pipeline 21 argues for. The practice should track Figma's motion-spec roadmap closely — when Code Connect adds motion mapping, the contract in 21 collapses to a tooling integration rather than a manual artefact.

---

## Failure modes to watch

- **Library imported by reflex.** Engineers reach for Motion or GSAP when CSS would do. The result is a 30KB tax on a single hover transition.
- **`will-change` applied permanently.** A `will-change: transform` declaration in the base stylesheet promotes every element to its own GPU layer. Memory bloat, mobile crashes.
- **Animation on layout-triggering properties.** `width`, `height`, `top`, `left`, `box-shadow`, `background-color`. Compositor sits idle; main thread thrashes. INP inflates.
- **View Transitions used without reduce-motion wrapping.** Browser runs the transition regardless of the user's setting. Accessibility regression, frequent compliance finding.
- **Spring physics simulated with long ease-out.** Engineer received a "bouncy" spec and approximated with a 600ms ease-out. The result is not a spring; it is a slow ease that the user reads as latency.
- **AI agent generates magic-number durations.** `transition: all 0.18s ease`, `transition: all 0.22s ease`. Compounds across components. Fix is composite motion tokens in agent context.
- **`document.startViewTransition()` swallowed by frameworks without reduce-motion checks.** Next.js App Router and similar frameworks expose view-transition hooks; the DS-supplied helper is the correct path, not the framework's raw hook.
- **Stagger as magic numbers.** Engineer sees `delay: 0.05s` in one component, `delay: 0.08s` in another. The token would have prevented it.

---

## Tensions and open questions

1. **Motion v12 (WAAPI-backed Framer Motion) as the React default.** The library is the closest thing the React ecosystem has to a standard, and its WAAPI rewrite addresses the main-thread cost that motivated half the field's "do we need a library" introspection. The case for: orchestration, AnimatePresence, LayoutGroup, gesture handling. The case against: 30KB+ on initial bundle, and the system can do most of it natively. The practice's default is likely to be "Motion for React-aligned engagements where orchestration is genuine; CSS-only for static marketing-tier components" — but the decision is per-engagement, not standard.

2. **GSAP licensing trajectory.** GSAP relicensed in 2024 to bring previously-paid plugins into the free Club. The library remains best-in-class for scrollytelling and complex timelines. The question is whether agency work with this depth justifies the bundle weight; the convergent answer is yes for marketing surfaces, no for product surfaces.

3. **Spring physics: baked `linear()` strings vs. runtime libraries.** The argument for baked: zero main-thread cost, tokenisable, deterministic. The argument for runtime: mid-flight adjustment, interruption handling, gesture responsiveness. The practice's default should be baked for tokens; runtime only when the interaction is genuinely gesture-driven.

4. **View Transitions browser support gap.** Firefox shipped same-document support but not cross-document as of May 2026. For multi-page route transitions targeting Firefox users, the API is not yet a complete answer. The mitigation is progressive enhancement — feature-detect and fall back to instant navigation, which is what happens by default. The practice should still document this gap explicitly when motion is part of a project's success criteria.

5. **The shift from library defaults to platform defaults as the enforcement layer.** Three years ago, accessibility-aware motion required configuring the library. In 2026, accessibility-aware motion requires configuring the *platform* through CSS variables and the per-token reduce-motion variants. This shifts the maintenance burden to the DS team and away from individual engineers. It also makes the DS more load-bearing — a bug in the system's reduce-motion contract is now everyone's bug.

6. **AI-agent motion as the dominant authoring path.** By the end of 2026, more component motion is being authored by AI agents than by humans on most agency projects. The implication for the system is that motion tokens, composite motion tokens, and the agent's context surface (AGENTS.md, CLAUDE.md, MCP) become the primary enforcement layer. The practice's existing investment in components-as-data (15) is the prerequisite; this file's tokens are the second-layer prerequisite.

---

## See also

- **18-motion-foundations** — the token taxonomy, principles, and reduce-motion contract this file implements.
- **20-motion-implementation-mobile** — the mobile-side parallel; the spring parameter mapping table that calibrates web spring tokens against mobile.
- **21-motion-spec-and-handoff** — the designer-to-engineer spec contract this file's tokens consume.
- **14-accessibility** — the reduce-motion architectural treatment; the View Transitions gotcha refines its current position.
- **15-ai-in-ds** — AI coding agents and the components-as-data prerequisite.
- **05-development-support** — Storybook, CI quality gates, and where motion regressions should be caught.

---

*Provenance: The CSS / WAAPI / View Transitions primitive treatment, the `linear()` spring discipline, the View Transitions reduce-motion gotcha, the WASM-tax threshold for Rive, the INP / LoAF performance budget, the Motion v12 WAAPI repositioning, the 120Hz target framing, and the AI-coding-agent argument are synthesised from the dual-agent research outputs in `_research/_inbound/2026-05-14-motion-implementation-web/` (May 2026). The "library imported by reflex" failure mode and the platform-defaults-as-enforcement framing are internal POV. INP as Core Web Vital (2024) and LoAF API (2024) are from web.dev and the W3C Web Performance Working Group documentation. The MCP motion-variables surface is from Figma's 2025–2026 product documentation. Cross-references to spring perceptual tokens, composite motion tokens, and the reduce-motion per-token contract are aligned with 18-motion-foundations.*

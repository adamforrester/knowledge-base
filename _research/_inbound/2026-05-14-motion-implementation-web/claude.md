# Motion Implementation on the Web

A practitioner's reference for senior design systems engineers shipping motion across a component library on the web. Covers the primitive layer (CSS, WAAPI, View Transitions), the library landscape, spring physics, orchestration patterns, reduce-motion enforcement, performance under the post-2024 metric regime (INP, LoAF), SVG/canvas/Lottie/Rive, and the bridge between a designer's motion spec and idiomatic code. Audience is fluent in CSS transitions, easing curves, `requestAnimationFrame`, and the layout-paint-composite distinction; the goal is to translate a motion spec into performant, accessible, consistent code, not to teach animation fundamentals. State of play as of May 2026.

---

## 1. The primitive layer

### CSS transitions, CSS animations, WAAPI — where the boundaries sit in 2026

The three primitives have stable, distinct roles in 2026, and the boundaries have hardened rather than blurred. A senior DS engineer should standardise where each belongs:

**CSS transitions** are for state change. A button changing from rest to hover, a menu opening from `aria-expanded="false"` to `true`, a checkbox flipping checked. The trigger is a property change; the runtime is declarative; the cost model is well-understood. Transitions are the right primitive for any component motion driven by a state that the DOM already represents. With `transition-behavior: allow-discrete` (Baseline 2024 across Chromium, Safari 17.4+, Firefox 129+), transitions can now animate to and from `display: none` and other discrete properties — closing the long-standing gap that pushed engineers into JavaScript for entry/exit animations.

**CSS animations** (keyframes) are for choreographed motion that is not driven by state — entrance/exit loops, attention-getters, looping decorative motion, indeterminate loaders. They are also the right primitive for entrance animations where the element appears in the DOM and runs a fixed sequence. The `@starting-style` rule (Baseline 2024) lets entry animations work without JavaScript bootstrapping — define the from-state in `@starting-style` and the to-state in the base ruleset, and the transition runs on insertion.

**The Web Animations API (WAAPI)** is for orchestration: motion that needs to be paused, reversed, sequenced, interrupted, or composed with user input. `Element.animate()` returns an `Animation` object that exposes `play()`, `pause()`, `reverse()`, `cancel()`, `finished` (a promise), and `commitStyles()`. The decisive WAAPI capability for DS work is **`ScrollTimeline` and `ViewTimeline`** (Baseline 2024 in Chromium, Safari Technology Preview shipping, Firefox in nightly behind a flag as of early 2026) — scroll-driven animations declared in CSS or WAAPI without a `scroll` listener on the main thread. This is the first time scroll-linked motion has had a compositor-friendly primitive.

The decision rule for DS components: **transitions for state, keyframes for fire-and-forget entry/exit, WAAPI for anything controlled.** A `Toast` that slides in, waits, and slides out under JS control is WAAPI. A `Drawer` that opens on a state change is a transition. A `Spinner` is a keyframe animation. Pushing all three into a JS library — even a good one — is over-engineering for the typical DS component surface.

### Houdini animation worklets

The verdict on Houdini animation worklets has not changed: they are still not practically usable. `CSS.animationWorklet` shipped behind a flag in Chromium in 2019, never reached cross-browser parity, and the spec has not been actively progressed since 2022. Firefox and Safari have declined to implement. As of May 2026 the worklet API is effectively a Chromium experiment that has not crossed the threshold for production use; treat it as not available. The work that worklets were meant to enable — off-main-thread custom animation — has largely been absorbed by scroll-driven animations and view transitions, which solve the most common pain points without requiring a custom worklet.

The wider Houdini surface (`CSS.paintWorklet`, `CSS.registerProperty`, `CSS.layoutWorklet`) has had uneven outcomes: `registerProperty` is universally supported and useful for animating gradients and custom properties with type information; `paintWorklet` is Chromium-only and niche; `layoutWorklet` is dead. `registerProperty` is the only piece a DS engineer should rely on.

### View Transitions API

The View Transitions API is the most consequential addition to web motion in this cycle and is finally crossing the line into DS-grade usability.

**Same-document view transitions** (`document.startViewTransition()`) are Baseline 2024: Chromium since 111, Safari 18 (September 2024), Firefox 129 (August 2024). The mental model is that the browser snapshots the old state, runs your DOM mutation, snapshots the new state, and crossfades or morphs between them using pseudo-elements (`::view-transition-old`, `::view-transition-new`) that the developer can style. The default is a crossfade; named elements with `view-transition-name` morph between positions.

**Cross-document view transitions** (`@view-transition` in CSS, navigating between pages in a multi-page app) shipped in Chromium 126 (June 2024). Safari and Firefox have not yet shipped cross-document transitions as of May 2026; Safari has signalled support but no release. This is the gating constraint: cross-document is Chromium-only in 2026, so a DS that wants page transitions on a MPA needs a fallback or needs to accept Chromium-only behaviour. Same-document transitions are the practical bet for SPA route changes.

What the API gives a DS: a primitive for layout-aware morphing that was previously only available through `FLIP` techniques in JS libraries (Framer Motion's `LayoutGroup`, GSAP's Flip plugin). What it doesn't give: gesture-driven interruption, springs, or fine-grained per-property control. The pseudo-elements animate through standard CSS animations, so a `view-transition` is composed with an animation, not a richer motion model. Most DS engineers will use it as a building block, not a complete solution.

The accessibility note that matters: `@media (prefers-reduced-motion: reduce)` automatically skips the visual transition and applies the DOM mutation instantly — the browser handles this, the engineer does not need to opt out. Same for cross-document.

---

## 2. The library landscape

The library landscape is more concentrated and more honest than it was three years ago. The shape in 2026:

**Motion (formerly Framer Motion).** Renamed in 2024 when the library separated from Framer Inc. and became the umbrella project for both the React-flavoured library (now `motion/react`) and the lightweight Motion One core (`motion`). It is the dominant React motion library by a wide margin, and the React API is now built on top of the same core that powers the framework-agnostic version. The trade-off is bundle size — `motion/react` is the heaviest of the common options at roughly 40–50KB minified+gzipped for the full surface, though tree-shaking and the new `motion-mini` import paths cut this substantially for components that use only basic animations. Choose Motion when you need `AnimatePresence`, `LayoutGroup`/shared layout, gesture handling, or springs in a React component library and don't want to assemble that surface yourself.

**GSAP** went fully free (including formerly commercial plugins: SplitText, MorphSVG, ScrollTrigger, Flip, DrawSVG) in May 2024 after the Webflow acquisition. This shifted the calculus significantly. GSAP is now the default for: timeline-based choreography, complex SVG morphing, scroll-driven sequences that exceed what CSS scroll-driven animations can express, brand-led marketing-page motion. It is not idiomatic inside a React or Vue component library — its imperative timeline model fights component lifecycle — but for the choreographed-motion layer that sits *on top of* a DS (landing pages, hero sections, branded interactions), GSAP is the safest bet. The previous commercial pressure to avoid GSAP for "core" product motion has evaporated.

**Motion One** (the core that Motion is built on) is the right pick when you want WAAPI-based animation without React, with a small footprint (~3–4KB for the core), and with reasonable springs. It is the framework-agnostic option that mostly replaces what `animejs` used to be hired for.

**anime.js** v4 shipped in early 2025 as a substantial rewrite — modular imports, ESM-first, improved TypeScript types, a cleaner timeline API. It is no longer the most popular framework-agnostic option (Motion One has taken that crown) but it is a credible alternative, particularly for engineers who want a more imperative, sequence-driven mental model than Motion One offers.

**React Spring** has stagnated. It was the dominant spring-physics library for React for several years; in 2026 it is still maintained but no longer the default choice — Motion's spring implementation is good enough, and most teams don't want two animation libraries in their bundle. Reach for React Spring only if you have an existing codebase that uses it or you need its specific imperative API (`useSpringRef`, `useChain`).

**Theatre.js** is alive but niche. Useful when designers need to author motion in a timeline editor and export to runtime — typically for brand-led, story-driven sites — but rarely the right tool inside a product DS.

**Lottie web** (Airbnb's runtime + the `lottie-web` library) is the established choice for designer-authored vector animations exported from After Effects. The `dotlottie` format (Lottie Animation Community, 2023) and the `dotlottie-web` runtime are smaller and better-typed than the original `lottie-web`, and most teams using Lottie in 2026 have migrated. The unsolved problems with Lottie haven't gone away: variable performance with complex compositions, no built-in interactivity, weak runtime control, and effects (blurs, masks) that render differently or not at all across runtimes.

**Rive web** has displaced Lottie for new work in many shops, particularly where the animation needs to respond to state or user input. Rive's state machine model — the animation has inputs (booleans, numbers, triggers) that drive transitions between states — maps cleanly onto component-driven UI, and the runtime is smaller and more predictable than Lottie's. The trade-offs: Rive's authoring tool (Rive Editor) is the only practical path in, designers have to learn it, and there is no "export from After Effects" workflow. For brand-led one-shot animations Lottie/dotLottie still wins on tooling familiarity; for interactive component-level illustrations Rive wins on runtime model.

### The decision framework

A defensible decision rule for DS work:

- **Ship native primitives only** when the motion surface is state-driven, the choreography is simple, and there is no need for interruption, springs, or shared-element morphing. Most DS components in a typical product (`Button`, `Input`, `Tooltip`, `Drawer`, `Tabs`) fit here. View Transitions API plus CSS transitions covers most of this surface in 2026, where it didn't in 2023.
- **Bring in a library** when you need orchestration (`AnimatePresence` semantics — animating exit of components that are about to unmount), shared-layout morphing across DOM trees that view transitions can't address, or springs that need to interrupt gracefully under gesture.
- **Pick a spring library over a timing library** when motion is gesture-driven, interruptible, or where "natural feel" is the brand attribute. Pick a timing library when motion is choreographed, deterministic, and the brand calls for crisp linearity (Apple-style) rather than springy (Material-style).
- **Use Lottie/Rive runtime players** when the animation is authored by a motion designer in a tool that exports to that format and re-implementing it in code would lose fidelity or take too long. The break-even is roughly: anything under ~5 keyframes is faster to hand-code; anything that involves layered illustration, particle systems, or hand-drawn morphing belongs in Lottie/Rive.

### Library trends in 2026

What's growing: Motion (as the consolidated brand), Rive, view-transitions adoption (replacing custom FLIP libraries), CSS scroll-driven animations (replacing ScrollTrigger for the common cases). What's stagnating: React Spring, the older Framer Motion v6/v7 codebases, Lottie's hand-written non-dotLottie format. What's being absorbed into the platform: shared-element morphing (view transitions), scroll-linked motion (scroll-driven animations), discrete property transitions (`allow-discrete`), entry animations (`@starting-style`).

The honest read for 2026: **the platform has clawed back a meaningful chunk of what JS motion libraries used to be required for.** A new DS in 2026 should default to native primitives and reach for Motion only when the surface genuinely needs it — the calculus has flipped from "always bring a library" to "justify the library."

---

## 3. Spring physics on web

### Why springs matter for component motion

Spring physics matters because three properties of springs map onto interactive component motion better than any timing-based curve:

1. **Interruptibility.** A spring has a current position and velocity. When the target changes mid-flight, the spring continues from where it is with its current momentum, and resolves to the new target naturally. A timing-based animation either snaps, restarts, or has to be unwound by hand. For gesture-driven motion (a drawer that the user can grab and throw), springs are not optional — they are the only sane model.
2. **Velocity continuity.** A spring's perceived "feel" is governed by physics, not by an arbitrary curve. Motion-designer feedback like "this should feel weightier" maps to mass; "this should overshoot more" maps to damping. The parameter space is small and intuitive.
3. **Deterministic enough.** Despite being physics-based, springs converge to a deterministic resting state given the same parameters and starting conditions, so they pass visual regression testing with care.

### The current implementation surface

- **Motion (`motion/react` and `motion`)** — the de facto reference implementation for springs in React. Configurable via `type: "spring"` with `stiffness`, `damping`, `mass`, optional `velocity`, and the friendly aliases `bounce` and `duration` (added in 2023, useful for designers). Motion One's core has the same physics model.
- **React Spring** — older, more imperative API, still works, but the default for new projects has shifted to Motion.
- **GSAP** — has an `Elastic` ease and a `CustomBounce` but is not a true spring-physics engine in the interruptible sense; for spring-feel-with-gesture, GSAP is not the right pick.
- **`linear()` easing function (CSS)** — Baseline 2023 across all major browsers. Not a spring engine, but it lets you express a spring-shaped curve as a series of interpolated points (`linear(0, 0.05, 0.2, 0.5, 0.8, 1.0, 1.1, 1.05, 1.0)`), and tools like Linear Easing Generator produce CSS-ready output from spring parameters. This is the right path for "spring-shaped" entry/exit on declarative state changes where you don't need true interruptibility.
- **CSS `spring()` / `linear-easing-function` proposals** — the CSS Working Group has had a `spring(mass, stiffness, damping, velocity)` proposal on the table since 2022; it has not progressed to implementation. As of May 2026 no browser has shipped a spring easing function. The `linear()` workaround is what to use.

### Spring parameters as tokens

A spring is fully specified by three to four numbers. That makes it tokenisable in the same way an easing curve is — and a DS that takes motion seriously should ship spring tokens alongside duration and easing tokens. A defensible default set:

- `motion.spring.gentle`: stiffness 120, damping 14, mass 1 — for routine UI transitions (drawer open, tooltip appear).
- `motion.spring.snappy`: stiffness 300, damping 20, mass 1 — for button feedback, toggle states.
- `motion.spring.bouncy`: stiffness 200, damping 10, mass 1 — for delightful/emphasis motion; use sparingly.
- `motion.spring.stiff`: stiffness 400, damping 30, mass 1 — for utilitarian, near-instantaneous state changes.

The token tier should be semantic, not numeric — components reference `motion.spring.snappy`, not `stiffness: 300, damping: 20`. This is the same architectural argument that applies to color tokens: leaking the primitive numbers across the codebase makes the system unfixable.

(For the wider treatment of motion tokens, easing, and duration tiers, see `00-foundations-motion` and the spec-side research; this section covers only the web implementation.)

### When springs are the wrong choice

Springs are the wrong choice when motion is:

- **Deterministic by brand requirement.** A brand whose motion language is crisp linear ease-outs and tight cubic-béziers will be undermined by springs. Apple's motion language sits here.
- **Choreographed against a beat or another animation.** Springs don't have a precise end time; you can't sync a spring to a video, an audio cue, or another component's animation without forcing it. Use a timing function with a known duration.
- **Required to be visually identical to a static design spec.** A motion designer who hands over keyframes at specific timestamps expects timing-based motion; translating it to a spring will lose fidelity.
- **A loading or progress indicator.** Springs converge; a loader must continue indefinitely or until a known event. Use keyframes.

---

## 4. Choreography and orchestration in production

### Sequencing entrance and exit of related elements

The field has converged on a small number of patterns, and the names have stabilised even where the underlying implementations differ.

**`AnimatePresence` (or its equivalent).** The problem this solves is that React (and Vue, Svelte, etc.) unmount components synchronously — by the time you want to animate a component's exit, it is no longer in the DOM. `AnimatePresence` is the canonical solution: a wrapper that defers unmount until the exit animation completes. Motion's `AnimatePresence` is the reference; equivalents exist in `auto-animate` (FormKit), Vue's built-in `<Transition>`, and Svelte's `out:` directives. **A DS that animates exit needs this primitive somewhere in its stack** — there is no way to do it cleanly with raw CSS in React because the component is gone before the transition has a chance to fire. (`transition-behavior: allow-discrete` plus `@starting-style` is the framework-free path, but it relies on the element staying in the DOM with `display: none`, which doesn't help when the framework unmounts it.)

**`LayoutGroup` and shared-element morphing.** When an element moves between two parts of a layout (a card expanding into a detail view, a tab indicator sliding between tabs), the common pattern is FLIP — measure the from-state, perform the mutation, measure the to-state, apply an inverse transform, and animate to zero. Motion's `LayoutGroup` and `layoutId` automate this. GSAP's Flip plugin does the same imperatively. View Transitions API, where supported, replaces this entirely for the common cases (same-document shared morphing). In 2026 the question is: does view-transitions cover your case? If yes, prefer it. If no (gesture-interruptible, spring-driven, controlled), reach for the library primitive.

**Stagger.** Sequencing motion across siblings (list items appearing in series, dashboard cards loading in) is well-served by both library primitives (Motion's `staggerChildren` on a parent variant, GSAP's `stagger` parameter on timelines) and by CSS's `animation-delay: calc(var(--i) * 50ms)` pattern. The CSS version is fine for fire-and-forget; the library version is necessary if you need to interrupt or reverse.

### Route transitions in modern frameworks

The picture in 2026:

- **Next.js App Router.** The idiomatic answer has shifted from "use Framer Motion + a layout file" to "use the View Transitions API where it works, fall back to Framer Motion's `AnimatePresence` for Safari/Firefox cross-document gaps." Next.js 15 (October 2024) and 15.x added experimental view-transitions integration; by Next 16 (early 2026) the support is stable. Same-document transitions work everywhere; cross-document still Chromium-only.
- **React Router 7 (formerly Remix).** `useViewTransitionState` and the `viewTransition` prop on `<Link>` are first-class as of v7 (late 2024). This is the cleanest route-transition story in the React ecosystem because the router has direct control over the navigation lifecycle.
- **SvelteKit.** Same-document view transitions are idiomatic via `onNavigate` hooks; cross-document via `@view-transition`. The SvelteKit team has consistently led on this.
- **Nuxt.** Vue's built-in `<Transition>` and Nuxt's page transitions still work; view-transitions support is available via `<NuxtPage :transition>` in Nuxt 3.10+.

### Performance and accessibility implications

Route transitions are the most performance-sensitive motion a DS will ship because they are the moment the user is waiting for new content. Two specific risks:

1. **Blocking input during the transition.** A 300ms transition that disables clicks is a 300ms INP penalty if the user tries to interact. Keep route transitions short (≤300ms for incoming content), and never block input during the transition — the new page should be interactive as soon as it has painted, even if the visual transition is still running.
2. **Layout thrash from competing animations.** A route transition that animates a card's position while the destination page is also laying out can produce visible jank. The fix is to ensure the destination is laid out *before* the transition begins (view transitions handle this by snapshotting), and to keep route-transition animations to `transform` and `opacity` only.

`prefers-reduced-motion` is the gate. The native View Transitions API handles this automatically — under reduce-motion the browser does the mutation without the visual transition. Library-based route transitions need an explicit check. A DS that ships a route-transition helper should default to "respect reduce-motion" and provide an explicit override only for engineers who have a specific reason to ignore it.

---

## 5. Reduce-motion implementation

The architectural treatment lives elsewhere; this section is the web specifics.

### CSS layer

`@media (prefers-reduced-motion: reduce)` is universally supported and the right primary mechanism. Two patterns are common:

**Reset everything in a global rule:**

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

This is the "safety net" pattern: it catches everything, but it disables motion uniformly rather than allowing essential motion to persist. It is the right default but should not be the only mechanism.

**Token-mediated motion:**

```css
:root {
  --motion-duration-md: 250ms;
}
@media (prefers-reduced-motion: reduce) {
  :root {
    --motion-duration-md: 0ms;
  }
}
.component { transition: opacity var(--motion-duration-md); }
```

This is the architectural pattern. Components reference duration and easing tokens; the tokens collapse to zero or near-zero under reduce-motion at the root. Engineers writing components never have to think about reduce-motion individually — they think about it once, at the token layer. This is the same architectural argument as accessibility-by-default colour pairs (see `14-accessibility`).

### JS layer

`window.matchMedia('(prefers-reduced-motion: reduce)')` returns a `MediaQueryList` that is `addEventListener`-compatible. The DS should expose this as a hook in every framework it supports:

```ts
// React
export function usePrefersReducedMotion() {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const mq = matchMedia('(prefers-reduced-motion: reduce)');
    setReduced(mq.matches);
    const handler = (e: MediaQueryListEvent) => setReduced(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, []);
  return reduced;
}
```

Motion has `useReducedMotion()` built-in and respects the preference automatically in many of its components — `motion.div` with a `transition` will collapse durations under reduce-motion by default. GSAP has `gsap.matchMedia()` which exposes the same. Anime.js and Motion One leave it to the engineer. Whichever library the DS adopts, the rule is: **the DS's motion helpers should respect reduce-motion by default; opting out is an explicit, justified choice.**

### Encoding "respect reduce-motion" so engineers don't have to remember

Three patterns work together:

1. **Token collapse at the CSS layer.** Duration tokens become 0 under reduce-motion. This handles transitions and `animation-duration`-driven keyframes without per-component work.
2. **Library defaults.** Whatever motion library the DS adopts, configure it to honour reduce-motion at the wrapper layer — not at each call site. If using Motion, wrap once in a `MotionConfig reducedMotion="user"`. If using GSAP, register a `gsap.matchMedia()` at app start.
3. **Linting.** A custom ESLint rule or a Stylelint rule that flags hardcoded `transition-duration` values (anything not a CSS variable) catches the case where an engineer drops a `0.3s` literal into a component. This is the same pattern as token-compliance linting for colours.

The cross-cutting note: reduce-motion is not "no motion." Opacity fades and very short cross-fades are typically allowed; what is disallowed is *vestibular*-triggering motion — parallax, scale-from-zero, large translations, autoplay video, sustained rotation. A DS that collapses every duration to 0 will pass `prefers-reduced-motion` checks but will produce abrupt, jarring interfaces. A more nuanced approach is to collapse durations but preserve a 50–100ms opacity fade for state changes, so the interface still has perceptual continuity. Motion's `reducedMotion="user"` mode does this by default.

---

## 6. Performance — what actually matters

### Compositor-only properties in 2026

The core rule has not changed: `transform`, `opacity`, and `filter` animate on the compositor thread and avoid layout/paint; everything else doesn't. What has changed is the surface that can be moved onto the compositor. `clip-path` (Chromium 120+, January 2024, with compositor support; Safari and Firefox following), `background-color` (compositor-accelerated in Chromium 116+ when on a layer), and CSS scroll-driven animations (compositor-driven by design) are all now first-class.

**The rule for DS components:** animate `transform` and `opacity` first. Reach for `clip-path` for reveal effects only after verifying compositor acceleration in DevTools. Avoid animating `width`, `height`, `top`, `left`, `margin`, or anything that triggers layout — these are the persistent footgun. `height: auto` to `height: <fixed>` remains one of the most common DS mistakes (animating a content-driven height triggers layout on every frame); the modern fix is `grid-template-rows: 0fr` to `1fr` (Baseline 2023) or `calc-size(auto)` (Chromium 127+, May 2024; in spec finalisation, Safari/Firefox not yet shipped as of May 2026).

### `will-change` — when it helps, when it hurts

`will-change` promotes an element to its own compositor layer in advance of animation. The pitfalls are well-documented and worth repeating:

- **Don't apply it permanently.** A `will-change: transform` on every card in a list is the canonical mistake — it consumes GPU memory, raises composite cost, and produces no benefit when the element isn't actually animating. Add it just before the animation starts (`element.style.willChange = 'transform'`), remove it when the animation ends (`'auto'`).
- **Don't apply it to elements that already animate.** `transform`, `opacity`, and `filter` animations already promote to a layer in modern browsers without `will-change`. Adding it is redundant.
- **It is a hint, not a guarantee.** The browser can decline to promote; `transform: translateZ(0)` (the historical hack) is more aggressive but has the same downsides.

The honest verdict in 2026: `will-change` is rarely necessary for routine DS motion. Reach for it when profiling shows a specific composite-layer thrash on animation start; otherwise let the browser decide.

### INP and motion

Interaction to Next Paint (INP) replaced First Input Delay (FID) as a Core Web Vital in March 2024. INP measures the longest interaction latency a user experiences during their session — from input (click, tap, keypress) to the next paint. Google's threshold for "good" is ≤200ms; "needs improvement" is 200–500ms; "poor" is >500ms.

Motion intersects INP in two ways:

1. **Motion that runs on the main thread blocks paint.** A click handler that triggers a JS animation that does layout work (animating `height: auto`, running React state updates inside a `requestAnimationFrame` loop) extends the time from input to paint and pushes INP up. The mitigation is to move animation work onto the compositor (`transform`/`opacity`) and to keep the JS handler short — let the animation start on the next frame, don't block the paint waiting for the animation to begin.
2. **Animation triggered by hover/focus doesn't affect INP** in the way a click animation does, because hover/focus aren't measured as INP interactions (only click, tap, and keypress are). But they still affect perceived smoothness and show up in LoAF.

**The DS rule:** any animation that fires on a measurable interaction (click, tap, keypress) must be compositor-only and must not be preceded by JS work that takes more than a frame. Animating a drawer open on click should be `transform: translateX(-100%)` to `0`, not a React state update that re-renders 200 nested components and then animates them.

### Long Animation Frames (LoAF API)

The LoAF API (shipped Chromium 123, April 2024; Safari following in 18.4, March 2025; Firefox in nightly behind a flag) exposes long animation frames — frames that take longer than 50ms to render. It is the successor to long-task-API observability for the rendering pipeline and is what should be wired into RUM (real-user monitoring) for motion-heavy DS work.

```ts
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 50) {
      // entry.scripts — which scripts contributed
      // entry.renderStart, entry.styleAndLayoutStart — timing breakdown
      // entry.blockingDuration — how much of the frame was blocked
    }
  }
}).observe({ type: 'long-animation-frame', buffered: true });
```

What LoAF gives a DS: per-frame attribution of where rendering time was spent. The `scripts` array tells you which user scripts ran during the frame; `styleAndLayoutStart` minus `renderStart` tells you whether the time was in JS or in style/layout. This is the first time RUM has been able to attribute jank to specific scripts in production.

Practical use: ship LoAF observation in the DS's analytics integration, attribute long frames to component instances where possible, and surface a per-component motion-performance budget (e.g., "the `DataTable` row-expand animation produced LoAF events on 4% of sessions").

### Performance budget at the component level

A defensible budget the DS can encode:

- **Component animations are compositor-only by default.** Linting / CI catches `transition` or `animation` on layout-triggering properties.
- **Animation duration ≤ 400ms for state changes; ≤ 600ms for entrances; ≤ 250ms for exits.** Longer than this produces sluggish-feeling interfaces and increases the INP risk envelope.
- **No JavaScript-driven animation on click/tap/keypress unless it is hand-off to the compositor within one frame.** Inline `requestAnimationFrame` loops that drive layout properties are banned.
- **Scroll-linked motion uses `scroll-timeline` (CSS or WAAPI), not scroll listeners.** This is testable: a Lighthouse audit or custom check can detect main-thread scroll listeners attached to animation handlers.
- **Lottie/Rive compositions over 50KB or over 10 simultaneous layers get a perf review.** Both runtimes have well-known cliffs at higher complexity.

These are budgets the DS encodes once and consuming product teams inherit — the same architectural argument as token-compliance and accessibility-by-default.

---

## 7. SVG and canvas animation

### When SVG is the right tool

SVG is the right tool when the asset is vector, the asset is illustrative or brand, and the animation is shape-driven (path morphing, stroke drawing, gradient transitions). Loaders, branded mascots, illustrated empty states, and animated icons fit here. SMIL (the in-SVG animation syntax) is deprecated in spirit but still works; the practical animation surface for SVG in 2026 is **CSS animations on SVG attributes** (`stroke-dashoffset`, `transform`, `opacity`), **WAAPI on SVG elements**, or **a library** (GSAP's MorphSVG and DrawSVG are the gold standard for path morphing; Motion handles transforms cleanly).

The technical note: SVG transforms in 2026 work via standard CSS `transform` on SVG elements in all major browsers (Chromium, Safari 16+, Firefox 113+), so the historical pain of "SVG has its own transform attribute" is mostly behind us. `transform-origin` on SVG elements is well-supported. The remaining gap is `transform-box: fill-box` (rare older browser bugs), which is worth checking if rotation centres look wrong.

### Lottie vs. Rive vs. hand-coded SVG

The honest trade-off matrix in 2026:

| Need                                                | Recommend           |
|-----------------------------------------------------|---------------------|
| Designer-authored from AE, ship as one-shot animation | Lottie / dotLottie |
| Designer-authored, interactive, state-driven        | Rive                |
| Brand-led icon set with subtle motion               | Hand-coded SVG + CSS / Motion |
| Branded loader (≤2KB)                               | Hand-coded SVG + CSS |
| Marketing-page hero animation                       | Lottie or GSAP-driven SVG |
| In-product micro-animation tied to state            | Rive or hand-coded |

The "hand-coded" option is more attractive than it used to be because the tooling for vector animation in CSS has matured (`@property`-typed custom properties, `linear()` easing, scroll-driven animations), and the runtime cost is zero — no Lottie/Rive runtime bundle.

Lottie's known weak spots in 2026 (still): variable rendering of mask groups across runtimes, weak fidelity on certain AE effects (motion blur, complex track mattes), and unpredictable performance on compositions with heavy layer counts. dotLottie improves the file format but not the underlying rendering. Rive's known weak spots: smaller designer ecosystem, no AE import path, single-vendor risk (the format and tooling are tied to Rive Inc.).

### Canvas and the WebGL boundary

Canvas (2D) is the right tool when the content is non-DOM, non-vector, and high-density — data visualisation with thousands of marks, particle systems, sprite-driven animation, custom shaders for image processing. The boundary with WebGL (and WebGPU, which is now Baseline in Chromium 113+ and Safari 26 / 2026, with Firefox tracking) is:

- **Canvas 2D** for 2D data viz, simple particle systems (up to a few thousand particles), and rendering that doesn't need shaders. The API is approachable and the perf is usually adequate.
- **WebGL** when you need shaders, when you're rendering 10k+ marks per frame, or when you need GPU-driven layout (instanced rendering). The library landscape (three.js for 3D, regl/Pixi.js for 2D-on-WebGL, deck.gl for geospatial) is mature.
- **WebGPU** when you need compute shaders, when WebGL's limitations bite, or when targeting the next generation of high-performance web visualisations. As of 2026 WebGPU is shipped in Chromium and Safari (since macOS 26, 2026) but not yet in Firefox stable; the practical use case for DS work is still narrow.

For a DS, the rule is: canvas/WebGL is rarely the right tool for component-level UI. It belongs in data-viz components (`Chart`, `Sparkline`, `Map`) and in specialised primitives (`SignaturePad`, `ColorPicker`). Don't reach for canvas because CSS animation is "too slow" — the right answer there is almost always to move work to the compositor.

---

## 8. The bridge between designer spec and code

### What an engineer actually consumes

A motion spec that is implementable without follow-up clarifies six things:

1. **Trigger.** What initiates the motion — a state change (`open`/`closed`), a user action (`click`, `hover`, `focus`), an entry into the viewport, a route change, a programmatic event.
2. **Properties.** Which CSS properties change — `transform`, `opacity`, `color`, `clip-path`. With from-values and to-values, or referencing the rest/active states the engineer can read from the design.
3. **Timing.** Duration, delay, and where applicable, the timeline (when does property A start relative to property B). For springs, the parameters (`stiffness`, `damping`, `mass`).
4. **Easing.** Either a named curve (`ease-out`, `linear`), a cubic-bezier (`cubic-bezier(0.2, 0, 0, 1)`), or a spring specification. Referenced as a token where possible.
5. **End state and idle state.** What does the element look like when motion is not running. Designers often forget this for loops and interrupted motion.
6. **Reduce-motion fallback.** What happens under `prefers-reduced-motion: reduce`. The default the DS should encode is "collapse duration to ~0 but preserve opacity continuity"; the spec should call out any deviation.

A motion spec missing any of these is incomplete and will be implemented inconsistently across engineers. (For the full treatment of motion specification — token tiers, design-tool authoring conventions, sign-off rituals — see the motion-foundations research and `00-foundations-motion` when promoted.)

### Tooling that produces engineer-consumable artefacts

The current options:

- **CSS variables exported from Figma.** Variables → tokens pipeline (Tokens Studio, Figma Variables, Specify, Supernova) can carry motion tokens — duration, easing, spring parameters — into the codebase as DTCG-format JSON. The DTCG motion module is at draft-final stage as of May 2026 (spec activity in CSS/DTCG working group through 2025) and is the format to target; some teams are still on Tokens Studio's older motion structure.
- **Lottie JSON / dotLottie.** Direct export from After Effects via Bodymovin. Engineer consumes via `lottie-web` or `@dotlottie/web-component`. Spec content is in the file; engineer adds wiring (autoplay, loop, controls).
- **Rive runtime files (.riv).** Export from Rive Editor. Engineer consumes via `@rive-app/canvas` or the WebGL runtime, wires state-machine inputs to component props.
- **Code-as-spec.** A pattern where the design system ships a Storybook story or a code snippet as the authoritative spec for a given motion; designers reference the live implementation rather than re-specifying. This is the pattern that scales when the DS has matured.

### Where translation is still manual

In 2026, the manual gap remains in:

- **Choreography across multiple elements.** Lottie/Rive handle this within a single composition but not when the choreography crosses component boundaries (a card flying into a sheet from another part of the page). This is still hand-built.
- **Gesture-driven motion.** Designers can specify the resting and active states; the velocity-mapping, interruption behaviour, and rubber-banding all happen in code. Tools haven't caught up.
- **Spring parameters from After Effects.** AE has its own bouncy/elastic eases that don't map directly to spring physics; engineers translate by eye.
- **View-transition naming.** Designers don't typically annotate which elements should morph between which states; engineers infer from the design intent.

What has been automated since the 2023 cycle: token export, scroll-linked motion (now declarative), basic state-driven entry/exit (now declarative via `@starting-style` and `allow-discrete`), shared-element morphing for simple cases (View Transitions API).

### The role of AI code generation

The honest read in 2026:

**Cursor / Claude Code / Windsurf / Copilot** are competent at the primitive layer: writing a CSS transition or keyframe animation given a spec, scaffolding a Motion `<motion.div>` with the right props, adding `prefers-reduced-motion` guards. They are middling at orchestration: chaining `AnimatePresence` with `LayoutGroup` is the kind of thing they get 70% right and require fixing. They are weak at performance reasoning — they will happily animate `height: auto` if asked, and they will reach for libraries when native primitives would suffice.

**Figma Make** and similar Figma-to-code tools produce static markup well; their motion output in 2026 is still primitive (CSS transitions, simple `@keyframes`), with no native support for view transitions or spring physics. The handoff still requires an engineer pass for anything beyond fades and slides.

**Where AI helps most for motion work in 2026:** writing the boilerplate (reduce-motion hooks, token plumbing, framework-specific wrappers), translating between libraries (rewriting React Spring to Motion), and generating Storybook stories. **Where it doesn't help yet:** choosing between primitive and library, sizing performance budgets, and orchestrating motion across components.

The pragmatic stance for a DS team: AI is a productivity multiplier for the boilerplate, not yet a replacement for the judgement calls. Design system engineers should treat AI-generated motion code as a first draft and apply the same review standard they would to a junior engineer's PR — particularly checking for the layout-triggering animation patterns that AI gets wrong consistently.

---

## References

Primary specifications, browser-support data, and library documentation are cited inline above where they support specific claims. Verification paths:

- **CSS Transitions Level 2** (W3C Editor's Draft, including `transition-behavior: allow-discrete`) — w3.org/TR/css-transitions-2/
- **CSS Animations Level 2** (`@starting-style`) — drafts.csswg.org/css-animations-2/
- **Web Animations API** (WAAPI) — drafts.csswg.org/web-animations-1/ — verify against MDN's Browser Compatibility Data at developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API
- **View Transitions API** Level 1 (same-document) and Level 2 (cross-document) — drafts.csswg.org/css-view-transitions-1/ and -2/ — browser-support state at caniuse.com/view-transitions
- **CSS scroll-driven animations** (`scroll-timeline`, `view-timeline`) — drafts.csswg.org/scroll-animations-1/ — caniuse.com/css-scroll-timeline
- **`linear()` easing function** — drafts.csswg.org/css-easing-2/ — Linear Easing Generator: linear-easing-generator.netlify.app
- **`@property` and registered custom properties** — drafts.css-houdini.org/css-properties-values-api/
- **`calc-size()`** — drafts.csswg.org/css-values-5/ — Chromium release notes, May 2024
- **INP (Interaction to Next Paint)** — web.dev/articles/inp — March 2024 Core Web Vital promotion
- **LoAF (Long Animation Frames API)** — developer.chrome.com/docs/web-platform/long-animation-frames — Chromium 123, April 2024
- **Motion (formerly Framer Motion)** — motion.dev — changelog at github.com/motiondivision/motion
- **GSAP** — gsap.com — Webflow acquisition and free-plugin announcement, May 2024
- **Motion One** — motion.dev/docs/quick-start — github.com/motiondivision/motion
- **anime.js v4** — animejs.com — changelog for v4 rewrite, January 2025
- **React Spring** — react-spring.dev
- **Lottie / dotLottie** — lottiefiles.com/dotlottie — Lottie Animation Community
- **Rive** — rive.app/docs/runtimes/web
- **Next.js view-transitions integration** — nextjs.org/docs (App Router, view transitions section, v15+)
- **React Router viewTransition** — reactrouter.com/en/main/route/view-transition (v7)
- **`prefers-reduced-motion`** — developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion — WCAG 2.2 SC 2.3.3
- **DTCG motion module** — design-tokens.github.io/community-group/format/ — working group activity through 2025
- **WebGPU** — gpuweb.github.io/gpuweb/ — caniuse.com/webgpu

Browser-support claims in this document are accurate to caniuse.com and MDN BCD as of May 2026; verify version numbers against those sources before relying on them in a specific codebase.

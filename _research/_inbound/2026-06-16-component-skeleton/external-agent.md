# Skeleton — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/skeleton.md`; version numbers and the aria-busy/status AT specifics flagged unverified. The two passes converged almost completely; the external pass supplied the decisive SSR/RSC auto-derive-collapse reconciliation, the Adrian Roselli dual-node a11y citation, and sharp implementation detail (GPU shimmer, CSS-token binding, the SkeletonPage deprecation).*

---

The Skeleton Primitive: Layout-Reserving Architecture and Perceived Performance

## 1. Framing
The Skeleton is the terminal loading state of a data-container machine, executing a strict layout-reserving contract. The loading triad: Spinner (abstract activity, no dimensions), Progress (measurable %), Skeleton (content-shaped placeholder for an initial/complete-section load). The defining contract is CLS neutralization — the Skeleton mimics the exact shape/dimensions/typography metrics of incoming content (text lines, avatar circles, image rectangles), pre-allocating the bounding box so the document flow stabilizes; it leverages perceived performance (the layout reads as resolved, awaiting the final paint). The "mismatch trap": if a skeleton reserves 300x200 but the content resolves to 300x450, the app incurs a severe layout shift at resolution — a poorly calibrated skeleton is demonstrably WORSE than no indicator (a jarring double-paint jump). Field leaders diverge into the auto-derivation model (MUI/React Aria — infer dimensions from wrapped children) vs the explicit composition model (Polaris/Carbon/Fluent — hand-built skeleton screens from atomic primitives), balancing ergonomics/boilerplate against DOM rendering predictability in SSR.

## 2. Anatomy
The bounding container = the async orchestrator + the aria-busy region (the swap substrate flipping aria-busy true->false; + a visually-hidden role=status/alert live-region node). The visual primitives = presentational scaffolding, stripped of borders/shadows/content: text line (a rectangle with height mapped to the line-height token; final line truncated to 60-80% width to mimic ragged-right reading); circular/avatar (50% border-radius mapped to the avatar token); rectangular/rounded (configurable aspect ratios 16:9/4:3, surface radius tokens). The animation overlay = the base color (low-contrast neutral, gray-200 light / gray-800 dark) + the highlight sweep (a shimmer = a CSS pseudo-element linear gradient sweeping negative->positive offset across the X-axis, simulating a light reflection).

## 3. Properties / API
variant/shape (text/circular/rectangular/rounded). width/height (text auto/100% + hard height; image/card explicit). animation/active (pulse/wave/none/boolean — Ant active boolean, MUI typed). rows/lines (Ant paragraph={{rows:4}} auto-truncates the last line). loading/isLoaded (the orchestrator; Chakra v3 migrated isLoaded->loading for the standard negative/positive pattern). The major divergence — auto-derivation (MUI v5/React Aria: Skeleton wraps children; if no explicit dims, injects a transparent overlay absolutely-positioned to the children's boundaries; React Aria @react-spectrum/s2 replaces text/images/icons with a shimmer when isLoading — drastically reduces boilerplate but introduces severe SSR risk: unstable layout jumps if children rely on intrinsic sizing not yet calculated on the initial paint) vs hand-built (Polaris/Carbon/Fluent: discrete SkeletonBodyText/SkeletonThumbnail/SkeletonItem; Fluent enforces a Skeleton wrapper + SkeletonItem child where the wrapper handles animation sync and items dictate shape; higher effort + double-maintenance, but guarantees structural parity, zero CLS, and circumvents hydration mismatches).

## 4. States and Variants
No interactive states (no hover/focus/active) — purely async transitions. A binary loading:true->false machine; on the flip, the DOM swaps skeleton nodes for data nodes. Advanced impls use the inherited anti-flash timing (delay-before-show 150-200ms — prevents painting if the fetch resolves instantly; min-display 500ms once mounted — prevents subliminal flicker). Variant strategy: primitive model (MUI/Chakra — a single <Skeleton variant> altering morphology; maximizes flexibility, transfers cognitive burden to the dev) vs per-component model (Carbon/Polaris — pre-composed SkeletonDisplayText/SkeletonBodyText/SkeletonText/SkeletonPlaceholder). Macro: full-page compositions (Polaris's DEPRECATED SkeletonPage) — the field is shifting AWAY from monolithic skeleton screens (too rigid for dense modular UIs) toward atomic layout components (Stacks/Grids) populated with primitive Skeletons.

## 5. Usage Guidance
"Skeleton fatigue" — indiscriminate use yields a chaotic array of pulsing gray boxes that fails to reassure. Skeleton for initial loads where the layout is KNOWN (dashboards, data tables — replace grid rows; the system has the wireframe). Spinner if the layout is unknown or a minimal inline micro-interaction (button submit). Progress if the task is measurable/determinate. The cardinal rule — strict structural parity to avoid the mismatch trap: a hardcoded 200px skeleton for a dynamic gallery, when a 600px image loads, pushes everything 400px down the Y-axis — destroying the perceived-performance gains. Solution: constrain incoming content to aspect ratios (AspectRatioBox), apply the exact aspect-ratio tokens to the skeleton wrapper, locking the footprint before the payload transfers. "Don't skeleton everything": don't render a primitive for every microscopic icon/badge/metadata string (clutter + GPU degradation from uncoordinated gradients); abstract a complex card (title + subtitle + 3 tags + author lockup) to one avatar circle + two text lines + one rectangle (macro-structure over micro-detail).

## 6. Accessibility
The most contested/historically mishandled pattern. Skeletons are visually dominant but semantically vacant — pure presentational scaffolding. WAI-ARIA has no role="skeleton"; practitioners historically misused aria-busy on individual visual shapes. Per Adrian Roselli's foundational research, the compliant practice treats skeleton nodes as non-existent to AT: every box/shimmer/SVG wrapped in aria-hidden="true" — the absolute "never-read-the-boxes" rule (a blind user on JAWS/NVDA/VoiceOver never hears "graphic, gray box, graphic, gray box"). The correct implementation isolates visual from semantic via a dual-node architecture: (1) the Live Region — a visually hidden sr-only node with role="status" (or role="alert" for urgent) carrying the localized announcement string; (2) the Busy Container — the parent wrapper with aria-busy="true". On resolution: aria-busy flips to false, the aria-hidden skeleton nodes unmount + real data mounts, and focus is programmatically managed if the load was an explicit user action (a modal) OR the live region naturally quiets. Addresses WCAG 4.1.2 (Name/Role/Value) + 4.1.3 (Status Messages — exposing the dynamic content change without forcing a focus shift).

## 7. Content Guidelines
Defined by intentional absence of content — a structural vessel. Absolute prohibition of faux content: never "Loading…" text inside a box or overlaid on a shimmer; the placeholder stays abstract; any textual announcement is handled exclusively by the visually-hidden role=status node. Shape-match for content sizing: text-skeleton lengths reflect the anticipated average character length; paragraph skeletons use a randomized/stepped line-length (100%/100%/80%/40%) to simulate ragged-right typography (a uniform block of 100% bars looks unnatural on swap). The loaded announcement must be explicitly descriptive ("Loading transaction history for September" / "Fetching user profile details"), not a generic "Loading".

## 8. Motion
The animation indicates progress/momentum and reduces perceived wait. Shimmer/wave (a linear gradient moving along the X-axis — the premium experience, simulating light over a 3D wireframe, implying reading directionality) — but requires strict GPU compositing (animating background-position or transform:translateX across many nodes causes layout thrashing/repaint penalties on low-end mobile unless confined via will-change:transform). Pulse (a continuous opacity transition 0.4<->1.0 on the wrapper/staggered) — cheaper, less complex, but lacks directional momentum (a static "breathing" feel, reads slower). Static (a flat block). The reduce-motion architectural difference from Spinner: a Spinner relies entirely on motion — a frozen spinner implies a crash, so it must substitute its identity (text/dotted pulse). A Skeleton's information is the GEOMETRIC SHAPE, not the motion — so under prefers-reduced-motion:reduce the system simply DROPS the shimmer/pulse, reverting to a static skeleton (the shape maintains the CLS contract + communicates the loading state). The content-swap transition must be immediate or an extremely rapid crossfade (<=150ms); long fade-outs artificially lock the user out of data already arrived/parsed in memory.

## 9. Internationalization
RTL animation mirroring (critical): the shimmer/wave natively travels left->right (translateX(-100%) to translateX(200%)) to map LTR reading; in RTL (Arabic/Hebrew) the transform sweep MUST flip its vector (right->left) — failing to mirror creates cognitive dissonance. Shape layout mirroring: asymmetrical arrangements (avatar left, text right) mirror their flex/grid via CSS logical properties (margin-inline-start, padding-inline-end) — zero JS. Dark mode contrast calibration: dark mode relies on elevation (lighter surfaces = closer); the skeleton base maps to a surface/surface-container-highest token (not a generic dark gray), the highlight to a low-opacity white overlay; saturated/luminous hues create optical strain.

## 10. Naming
Skeleton (MUI/Chakra/Ant/Fluent/Base Web — the undisputed standard, denotes the bare-bones structural framework). IBM Carbon: SkeletonText/SkeletonPlaceholder (Skeleton prefix + semantic nodes, the hand-built model). Material 3 (Compose): Modifier.placeholder (treats loading as a modifier on an existing node — "Placeholder" for temporary spatial occupancy). Default: Skeleton (mandatory). Shimmer = the animation type / keyframe definition, not the component. Ghost = avoid (conflated with Button variant="ghost").

## 11. Implementation Notes
The auto-derive-vs-Skeleton-Screen AST trap (the most severe hazard): auto-derive (React Aria/newer MUI) renders children invisibly (visibility:hidden) to let the layout engine calculate the BoundingClientRect, then absolutely-positions the skeleton over those boundaries — this breaks catastrophically in SSR/RSC: on the initial server pass the dimensions of client-side assets (un-fetched images, intrinsic typography) are unknown, so the auto-derived skeleton collapses to a 0x0 box, ships, hydrates, and immediately triggers a massive CLS as the browser finally calculates — defeating the foundational purpose. The architectural verdict: explicitly defined dimensions (height=24px width=100%) or explicit hand-built skeleton screens are the ONLY mathematically safe way to guarantee zero layout shift in SSR/RSC. Modern impls eschew fixed px for text heights, binding to typography tokens via CSS custom properties (.skeleton-text { height: var(--typography-body-line-height); border-radius: var(--border-radius-sm); background-color: var(--surface-container-high); }). Fluent/Chakra v3 inject the shimmer gradient start/end colors via CSS variables, bypassing React's style engine so the GPU handles transitions without re-renders. Anti-flash via a useLoadingDelays hook (150ms delay; if isLoaded before, never mount; if breached, mount + min 500ms). The Skeleton is inherently opinionated/theme-bound (it must mimic the host's exact radii/shadows/grids) — ship it opinionated, not just a headless wrapper.

## 12. Related and Alternative Components
Spinner (sibling): shape-agnostic infinite busy indicator; boundary = layout knowledge (Spinner for minimal inline/unknown payloads, Skeleton for initial full-page/section). Progress (sibling): determinate/measurable; inherits the same anti-flash + aria-busy regional logic, communicates a % rather than a spatial footprint. Empty State (terminal state): the container's state when loading succeeds but the payload is zero; the Skeleton is the same container's state WHILE fetching. Data/Card/Image (hosts): Skeletons are the temporary structural surrogate; the skeleton's border-radius/padding/aspect-ratio must be imported from the Card/Data Table token definitions for a 1:1 shape match. Toast (live-region pattern): Skeletons lightly reuse the visually-hidden role=status injection to broadcast announcements without stealing focus.

## 13. Field POV Evolution
2016-2019 CSR era: Skeletons as aesthetic enhancements; blind <Skeleton isLoaded={data}> wrapping, DOM thrashing as components mounted/calculated/unmounted; the debate was Shimmer vs Pulse. 2020-present: Google's Core Web Vitals strictly penalized CLS, evolving the Skeleton into a strict mathematical layout-reservation contract (shape-match from guideline to dogmatic requirement). The accessibility community campaigned against the aria-busy-on-individual-nodes misuse; the modern consensus = the aria-hidden wrapper around the boxes + the aria-busy live region on the parent. Robust prefers-reduced-motion handling forced distinguishing structural loaders (Skeletons — drop to static, geometry is the information) from motion loaders (Spinners — must substitute identity). With RSC/streaming HTML, Skeletons are increasingly embedded directly into the initial server HTML payload as Suspense boundaries/fallbacks, pushing layout parity away from client-side JS into robust CSS Grid architecture.

## 14. Sources cited
MUI v4/v5 (variant text/circular/rectangular, infer-from-children, pulse/wave/false). Ant Design v3/v6 (active boolean, Skeleton.Image/Avatar, rows). IBM Carbon (React/Web Components; SkeletonText/SkeletonPlaceholder/SkeletonIcon). Shopify Polaris (deprecated SkeletonPage -> modular composition; SkeletonBodyText/SkeletonThumbnail). GitHub Primer (SkeletonText/SkeletonAvatar; CSS modules behind feature flags). Chakra UI v1-v3 (isLoaded->loading; CSS-variable gradient colors). Microsoft Fluent UI v3 (Skeleton + SkeletonItem). Base Web (rows/animation/width/height; dynamic sub-elements). React Aria / Spectrum (<Skeleton isLoading> wrapper auto-derivation). Google Material 3 (Compose Modifier.placeholder). Adrian Roselli + WAI-ARIA APG (the aria-hidden + role=status dual-node architecture).

## 15. Agent-consumable schema

```yaml
identity:
  name: Skeleton
  aliases: [Placeholder, Shimmer (animation only), SkeletonText, SkeletonAvatar]
  type: Foundations / Loading Primitive
  contract: content-shaped layout-reserving placeholder (CLS neutralizer)
description: >
  A structural placeholder mimicking the physical geometry of incoming data to
  reserve document layout, neutralize CLS, and maximize perceived performance
  during initial or known-topology loading states.
anatomy: [aria-busy region (container), visually-hidden role=status live-region, aria-hidden skeleton-wrapper, geometric primitives (text/circle/rectangle), animation overlay (shimmer/pulse)]
api:
  variant: [text, circular, rectangular, rounded]
  width: [string, number]
  height: [string, number]
  animation: [pulse, wave, none]
  rows: number
  loading: boolean
accessibility:
  hidden_scaffolding: visual skeleton nodes MUST carry aria-hidden=true
  busy_region: the parent data container MUST carry aria-busy=true while loading
  announcement: a visually hidden node MUST carry role=status with a descriptive string
  reduced_motion: Skeleton MUST drop to a static variant without motion (unlike Spinner)
content:
  guidelines: zero actual text/content (pure scaffolding); shape must have strict mathematical parity with the resolved content
motion: {shimmer: 'linear gradient sweep (transform:translateX, GPU)', pulse: 'opacity oscillation', fallback: 'static for prefers-reduced-motion'}
i18n: {rtl_mirroring: 'shimmer vectors + asymmetric geometric layouts MUST mirror horizontally in RTL'}
implementation:
  cls_contract: skeleton footprint MUST identically match the resolved node BoundingClientRect
  anti_flash: INHERITS Progress/Spinner 150ms delay-before-show + 500ms min-display
  auto_derive_risk: SSR/RSC hydration mismatch (0x0 collapse) when inferring sizing from unpainted children -> use explicit dimensions / hand-built screens
composition: [Skeleton -> Data Host (Card/List/Table), Skeleton -> Live Region (status)]
notes:
  unverified: auto-inference in RSC streaming may require explicit CSS min-height fallbacks to prevent CLS during chunk resolution
```

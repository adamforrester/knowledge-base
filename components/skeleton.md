---
okf_version: "0.1"
type: component-brief
title: Skeleton
description: The Foundations loading primitive that closes the three-loading-patterns triad (Progress/Spinner/Skeleton) — the content-shaped placeholder for an initial load, reserving the layout to neutralize CLS. A field-truth study of the layout-reserving/CLS contract (the Spinner opposite) + the shape-match/mismatch trap, the three-loading-patterns decision, the reduce-motion drop-to-static (the Spinner difference — the cue is the shape, not the motion), the aria-hidden-boxes + aria-busy-region + status dual-node accessibility, the variant model + the SSR-unsafe auto-derive vs CLS-safe hand-built/explicit, the anti-flash, and the shimmer-vs-pulse-vs-static animation — with the practice's defaults.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [placeholder, shimmer, ghost, skeleton-text, skeleton-avatar, skeleton-image, loading-placeholder]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Skeleton

> A Skeleton is a **content-shaped placeholder for an initial load** — flat gray shapes mimicking the layout and dimensions of incoming content (text lines, avatar circles, image/card rectangles). It **closes the three-loading-patterns triad** Progress and Spinner anchored: **Progress** (a value contract / measurable / longer), **Spinner** (minimal inline indeterminate, *no shape*), **Skeleton** (an *initial* known-layout load, *reserving the layout*). It inherits the **anti-flash (delay/min-display) + `aria-busy` region pattern from Progress/Spinner** (see progress, spinner) and lightly the **"Loading" live-region announcement from Toast** (see toast); it is also the **loading terminal state** of the data-container machine Empty State described (`loading → {content | empty | error}`; see empty-state). Two things define it. **The layout-reserving / CLS contract (the Spinner opposite):** it matches the final content's shape *and dimensions* so the swap is shift-free — neutralizing Cumulative Layout Shift and shortening the *perceived* wait. Its corollary is the **mismatch trap** — a skeleton whose size doesn't match the real content causes a **worse double-paint jump than no skeleton at all**. And **the reduce-motion difference from Spinner:** the cue is the **shape, not the motion**, so `prefers-reduced-motion` can simply **drop the shimmer to static** (no substitution) — the cleanest reduce-motion case in the loading family.

---

## 1. Framing

A Skeleton executes a **layout-reserving contract**: it pre-allocates the bounding box of the anticipated DOM so the document flow stays stable during fetch/render, leveraging perceived performance (the structure reads as resolved, only the paint is pending). It inherits the **anti-flash + `aria-busy` region substrate from Progress/Spinner** (see progress, spinner) and lightly the **Toast "Loading" announcement** (see toast).

What it *isn't*: a **Spinner** (no shape; minimal/inline/short/unknown-layout — see spinner), a **Progress** bar (a value/measurable task — see progress), or an **Empty State** (the *empty* terminal state — Skeleton is the *loading* one of the same container machine; see empty-state). Why systems disagree: the variant model, the **auto-derive-vs-hand-built** authoring trade (which the SSR collapse decides — §3/§11), and the shimmer-vs-pulse animation.

## 2. Anatomy and parts
Synthetic anatomy — it exists only to mimic spatial footprint, stripped of borders/shadows/content/interactivity:
- **bounding container** — the async orchestrator + the **`aria-busy` region** (the parent the content will fill; flips `aria-busy` true→false on resolution).
- **live-region node** — a visually-hidden `role="status"` element carrying the announcement (§6) — the only thing AT hears.
- **placeholder shapes** (presentational scaffolding, `aria-hidden`): a **text line** (a bar with `height` = the typography line-height token; multi-line with a **shorter last line** — a stepped 100%/100%/80%/40% width to mimic ragged-right text), a **circle** (avatar, 50% radius mapped to the avatar token), a **rectangle/rounded** (image/card/thumbnail/button, an aspect-ratio + the surface radius token).
- **animation overlay** — a **base** fill (low-contrast neutral — gray-200 light / a `surface-container-highest` token dark) + a **highlight sweep** (a gradient pseudo-element traversing the X-axis for the shimmer).

## 3. Properties / API
- **`variant` / `shape`** — text / circular / rectangular / rounded (MUI/Chakra/Fluent); or per-component skeletons (`SkeletonText`/`SkeletonAvatar`/`SkeletonImage`/`SkeletonButton` — Carbon/Polaris/Primer/Ant).
- **`width` / `height`** — explicit CSS dimensions (text defaults to 100% width + a hard height); **bind height to the typography token** (`var(--typography-body-line-height)`), not a fixed px.
- **`rows` / `lines`** — the text-block line count (Ant `paragraph={{rows}}` auto-truncates the last line; Base Web `rows`).
- **`animation`** — pulse / wave(shimmer) / none(false) (MUI; Ant's `active` boolean).
- **`loading` / `isLoaded`** — the orchestrator that triggers the swap (Chakra migrated `isLoaded`→`loading` for the standard negative/positive boolean).
- **The auto-derive vs hand-built schism (the load-bearing API call):** **auto-derive** (MUI/React Aria — wrap the real children, render them hidden, infer the box, overlay the skeleton) cuts boilerplate but is **SSR/RSC-unsafe** (§11); **hand-built / explicit** (Polaris/Carbon/Fluent — discrete `SkeletonItem`s composed into a wireframe, or explicit `width`/`height`) costs double-maintenance but **guarantees zero CLS + no hydration mismatch**. The practice default leans **explicit/hand-built for CLS safety**, with auto-derive as a CSR-only convenience.

## 4. States and variants
- **States:** **loading** (the only state — shown, then **swaps** to the real content on resolution) + the inherited anti-flash *delayed* / *min-display-locked* windows. A binary `loading: true→false` machine.
- **Variants:**
  - **shape:** text (lines) / circular (avatar) / rectangular / rounded (image/card).
  - **primitive (`variant` prop) vs per-component** (`SkeletonText`/`Avatar`/…) — the cognitive-burden-on-the-dev vs pre-composed trade.
  - **the skeleton screen** (a composed layout) — *but the field is shifting away from monolithic full-page skeletons* (Polaris deprecated `SkeletonPage`) toward **atomic primitives composed into Stacks/Grids** (more resilient to dense, responsive UIs).
  - **animation:** shimmer/wave / pulse / static.

## 5. Usage guidance
- **Use a Skeleton** for an **initial page/section load where the layout is known** — dashboards, data tables (skeleton rows), lists, cards, profile headers, feeds, an image into a known box. It sets the grid, reserves the real estate, and primes the user.
- **Don't use a Skeleton for:**
  - A **minimal inline / short / unknown-layout wait** → a **Spinner** (a button, a dropdown — you can't shape-match a single control's brief wait; applying a skeleton to an unknown layout *guarantees* a shift — see spinner).
  - A **measurable/longer task** → a **Progress** bar (see progress).
  - The **empty result** → an **Empty State** (Skeleton is the *loading* state; see empty-state).
- **Decision frameworks:**
  - **The shape-match rule (cardinal):** physically mimic the real content's typography/padding/dimensions. The classic trap: a fixed `height: 200px` skeleton for a gallery whose 600px image then **shoves everything 400px down the Y-axis**. The fix: constrain the incoming content to an **aspect ratio** (an `AspectRatioBox`) and apply the *same* aspect-ratio token to the skeleton, locking the footprint before the payload transfers. A mismatched skeleton is **worse than none**.
  - **Don't-skeleton-everything (skeleton fatigue):** a chaotic field of pulsing boxes gives no reassurance (and burns GPU on uncoordinated gradients). **Abstract** a complex card (title + subtitle + 3 badges + author lockup) to its **macro-structure** — one avatar circle, two text lines, one rectangle — not a placeholder per icon/badge.
  - **The anti-flash rules (inherited):** **delay before showing** (~150–200ms — a fast load shows nothing) + **minimum display time** (~500ms once shown) so it doesn't strobe.

## 6. Accessibility
The most historically mishandled loading a11y — the skeleton is **visually dominant but semantically vacant**.

- **The skeleton boxes are NOT content — `aria-hidden="true"` (the "never-read-the-boxes" rule).** Every shape/shimmer/SVG placeholder is wrapped `aria-hidden` so a screen reader never announces "graphic, gray box, graphic, gray box" (auditory pollution). (Adrian Roselli's research established this against the common misuse of `aria-busy` on the individual visual nodes.)
- **The dual-node architecture (the practice default):** isolate the *visual* from the *semantic*. **(1) A live region** — a visually-hidden `role="status"` (or `alert` for urgent) node carrying the announcement string. **(2) The busy container** — the parent wrapping the whole loading section carries **`aria-busy="true"`**. (This is the same `aria-busy`-region pattern Spinner/Progress use, reused.)
- **The load-complete sequence:** `aria-busy` flips to `false`, the `aria-hidden` skeleton nodes unmount and the real content mounts in their place, and the live region (now quiet) or a "Loaded" status confirms the swap. **Don't move focus** to the newly-loaded content unless the load was an explicit user action (a modal open); preserve the user's focus.
- **Reduce-motion — DROP to static (the Spinner difference):** the skeleton's information is the **shape**, so `prefers-reduced-motion: reduce` simply **stops the shimmer/pulse** → a static skeleton (still communicates loading, still holds the CLS contract). No substitution — unlike Spinner, whose motion *is* the cue. The cleanest reduce-motion case in the family.
- **WCAG SCs:** 4.1.2 (name/role/value — the loading mechanism has a role), 4.1.3 (Status Messages — the dynamic content change announced without a focus shift), 1.1.1 (the skeleton is decorative — `aria-hidden`), 2.3.3/2.2.2 (the shimmer + reduce-motion); plus Core Web Vitals (CLS) as the engineering metric. (The lightest a11y of the loading family — there's nothing to read.)

## 7. Content guidelines
- **The skeleton has no content — never fake it.** No "Loading…" text inside a box, no lorem-ipsum, no labels an SR could read; the shapes stay abstract + `aria-hidden`. Any textual announcement goes in the visually-hidden `role="status"` node, decoupled from the geometry.
- **Shape-match the text** — text-skeleton line lengths reflect the real payload's average; use the **stepped ragged-right pattern** (100%/100%/80%/40%), not a uniform block of full-width bars (which looks unnatural on swap).
- **The loaded announcement is descriptive** — "Loading transaction history for September" / "Fetching user profile", not a bare "Loading" (tells the AT user *which* container is blocking + what's coming).

## 8. Motion and transition
- **Shimmer (wave) vs pulse vs static:** **shimmer** = a linear-gradient highlight sweeping the X-axis (premium, implies reading-direction momentum) — but **must be GPU-composited** (`transform: translateX` / `will-change: transform`; animating `background-position` across many nodes thrashes layout/repaints on low-end mobile). **pulse** = a whole-skeleton opacity oscillation (0.4↔1.0) — cheaper, but a static "breathing" feel that reads slower. **static** = flat.
- **The reduce-motion DROP (the Spinner difference)** — under `prefers-reduced-motion: reduce`, **stop the animation → static** (the shape is the cue; no substitute, unlike Spinner). The cleanest reduce-motion case in the loading family.
- **The content-swap** — when data resolves, an **immediate or ≤150ms crossfade**; avoid long dramatic fades (they lock the user out of data that's already parsed in memory). The shape-match means no layout jump.
- (See spinner §8, progress §8, 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL — the shimmer sweep vector flips** (an LTR `translateX(-100%→200%)` becomes right-to-left), matching RTL momentum; and **asymmetric shape layouts mirror** (a leading avatar + trailing text lines flips) via **CSS logical properties** (`margin-inline-start`, `padding-inline-end`) — zero JS.
- **Text-line skeletons** suggest the (often expanded) localized text length — don't hardcode widths that mismatch the translated content (the mismatch trap in i18n form).
- **Dark mode** — the base maps to a `surface`/`surface-container-highest` token (elevation: lighter = closer), the highlight to a low-opacity white; never saturated/luminous hues (optical strain, contrast). (See 13-internationalization-and-rtl.)

## 10. Naming
**`Skeleton`** is the undisputed standard (MUI, Ant, Carbon, Polaris, Primer, Chakra, Fluent, Base Web) — for both the primitive and the per-component family; **`Placeholder`** is Material 3 Compose's framing (`Modifier.placeholder` — a modifier on an existing node). **The practice default: `Skeleton`** as the primitive (`variant: text | circular | rectangular`, `width`/`height`/`lines`/`animation`/`loading`) with **per-component skeletons** (`Skeleton.Text`/`.Avatar`/`.Image`) for common shapes, composed into **atomic skeleton layouts** (over a monolithic full-page component). **`Shimmer`** names the *animation type / keyframe*, not the component; **`Ghost`** is avoided (it collides with `Button variant="ghost"`). Aliases to map: `Placeholder`, `Shimmer`, `Ghost`, `SkeletonText`, `SkeletonAvatar`, `SkeletonImage`, `LoadingPlaceholder`.

## 11. Implementation notes
- **The SSR/RSC auto-derive collapse (the sharpest trap, and what decides the auto-vs-hand-built trade):** auto-derive renders the children hidden (`visibility:hidden`), measures the `BoundingClientRect`, and overlays the skeleton — but **on the server the dimensions of un-fetched images / intrinsic typography are unknown, so the auto-derived skeleton collapses to a 0×0 box**, ships, hydrates, and **then** triggers a massive CLS as the browser finally measures — defeating the whole purpose. **Verdict: explicit dimensions (`height="24px"`/`width="100%"`) or hand-built skeleton screens are the only CLS-safe option in SSR/RSC.** Auto-derive is a CSR-only convenience.
- **Shape-match-the-final-layout (CLS)** — the skeleton's box must equal the real content's; constrain media to an aspect ratio and mirror it on the skeleton (§5). Bind text-skeleton `height` to the **typography line-height token** (`var(--typography-body-line-height)`) so it scales with the type ramp.
- **The dual-node a11y wiring** — `aria-hidden` the shapes; `aria-busy` on the region + a pre-existing visually-hidden `role="status"`; flip on resolution (§6).
- **The anti-flash timers (inherited)** — a `delay` (~150–200ms; render nothing if resolved first) + a `minDisplay` (~500ms once shown); a shared `useLoadingDelays` hook with the Spinner/Progress.
- **The shimmer via GPU + CSS-variable colors** — animate `transform` (not `background-position`) under `will-change`; inject the gradient start/end colors as CSS variables so the GPU handles the animation without React re-renders. **Reduce-motion → disable (static)** (§8).
- **Streaming/Suspense** — increasingly the skeleton is the **Suspense fallback streamed in the initial server HTML** (React Server Components), pushing layout parity into robust CSS Grid rather than client JS — which *requires* the explicit-dimensions discipline (the auto-derive collapse).
- **Ship it opinionated, not headless** — the value is mimicking the host system's exact radii/shadows/grid; the skeleton is a theme-bound visual component (the timing/`aria-busy` logic is the shared headless part). Don't hand-roll — MUI/Ant/Carbon/Polaris/Primer/Chakra `Skeleton`.

## 12. Related and alternative components
- **Stands on:** the **anti-flash (delay/min-display) + `aria-busy` region pattern** inherited from Progress/Spinner (see progress, spinner), and lightly the **live-region pattern** from Toast (the "Loading" announcement — see toast).
- **Alternative to / boundary with:** **Spinner** (the minimal no-shape inline busy indicator — the Skeleton-vs-Spinner core call; see spinner), **Progress** (the value/measurable sibling — see progress), **Empty State** (the *empty* terminal state — Skeleton is the *loading* one of the same data-container machine; see empty-state).
- **Composed by / hosts:** the **Data / Card / List / Image** components whose initial-load state is a skeleton (Table renders skeleton rows, a Card a skeleton, an Image a skeleton box) — the skeleton must import the host's radius/padding/aspect-ratio tokens for a 1:1 match (see card for the loading-card host, table for the loading-rows host, list/image when briefed).

(A Foundations loading primitive that **closes the three-loading-patterns triad** (Progress / Spinner / Skeleton) — the content-shaped, layout-reserving (CLS) placeholder for an initial known-layout load, inheriting the anti-flash + `aria-busy` region substrate, with the cleanest reduce-motion case in the family (drop-to-static, because the cue is the shape not the motion). The loading terminal state of the data-container machine Empty State described. See progress/spinner for the loading siblings + the inherited substrate, empty-state for the empty terminal state, card for the loading-card host, table for the loading-rows host, list when briefed, toast for the "Loading" live-region touch. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The CSR-era aesthetic → the CLS engineering contract.** 2016–2019 treated skeletons as a visual nicety (the debate was shimmer-vs-pulse) and let the DOM thrash; **Google's Core Web Vitals (CLS, ~2020)** turned the layout-reservation purpose into a dogmatic engineering requirement — the shape-match rule went from guideline to mandate.
2. **Skeleton-over-spinner for initial loads** — shape-matched skeleton screens replaced the centered spinner on a blank page for initial structured loads (better perceived performance + no CLS); the spinner retreated to inline/micro-interactions.
3. **The `aria-hidden`-boxes + `aria-busy`-region + status settling** (Roselli) — over the systemic misuse of `aria-busy` on individual visual nodes.
4. **The reduce-motion-drop-to-static** — recognised as distinct from Spinner (the shape is the cue, so the animation can be removed entirely, no substitution).
5. **SSR/RSC + streaming** — the auto-derive collapse pushed the field toward explicit-dimension / hand-built skeletons embedded as **Suspense fallbacks in the server HTML**; and away from monolithic full-page skeletons (Polaris's deprecated `SkeletonPage`) toward atomic composition.

## 14. Sources cited
(Conservative; reconcile with external.) **MUI** — `Skeleton` (text/circular/rectangular/rounded, infer-from-children, pulse/wave/false) (2024–2026); **Ant Design** — `Skeleton` (avatar/title/paragraph/`active` + `Skeleton.Image`/`Button`/`Input`/`Avatar`/`Node`, `rows`) (2024–2026); **IBM Carbon** — `SkeletonText`/`SkeletonPlaceholder`/`SkeletonIcon` + the DataTable skeleton (2024–2026); **Shopify Polaris** — `SkeletonBodyText`/`SkeletonDisplayText`/`SkeletonThumbnail` (and the *deprecated* `SkeletonPage` → atomic composition) (2024–2026); **GitHub Primer** — `SkeletonText`/`SkeletonAvatar`/`SkeletonBox` (2024–2026); **Chakra UI** — `Skeleton`/`SkeletonCircle`/`SkeletonText` (`isLoaded`→`loading`; CSS-variable gradient colors) (2024–2026); **Microsoft Fluent** — `Skeleton`/`SkeletonItem` (the wrapper-synchronizes-animation, item-dictates-shape) (2024–2026); **Adobe Spectrum / React Aria** — `Skeleton`/`isLoading` (auto-derivation) (2024–2026); **Google Material 3** — `Modifier.placeholder` (Compose) (2024–2026); **Base Web (Uber)** — `Skeleton` (`rows`/`animation`) (2024); **Adrian Roselli** — the `aria-hidden` + dual-node (`role=status` + `aria-busy`) skeleton-accessibility research; **WAI-ARIA APG** — no formal skeleton pattern (`aria-hidden` + `aria-busy` + the status role); the inherited Progress/Spinner anti-flash/`aria-busy` substrate (see progress, spinner) + the Toast live-region pattern (see toast). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.2, 4.1.3, 1.1.1, 2.3.3, 2.2.2; Core Web Vitals (CLS).

## 15. Agent-consumable schema

```yaml
identity:
  id: skeleton
  name: Skeleton
  aliases: [placeholder, shimmer, ghost, skeleton-text, skeleton-avatar, skeleton-image, loading-placeholder]
  category: foundations
  status: stable
description: >
  The content-shaped placeholder for an initial load — flat gray shapes mimicking
  the incoming content's layout/DIMENSIONS to RESERVE the layout (neutralize CLS)
  + shorten perceived wait. Closes the three-loading-patterns triad (Progress/
  Spinner/Skeleton); the loading terminal state of the data-container machine (vs
  Empty State's empty). Inherits the anti-flash + aria-busy region substrate from
  Progress/Spinner. NOT a Spinner (no shape, inline/short/unknown), NOT a Progress
  bar (value/measurable), NOT an Empty State (empty terminal state).
anatomy:
  parts:
    - "bounding container (async orchestrator + the aria-busy region; flips true->false on resolution)"
    - "live-region node (visually-hidden role=status — the only thing AT hears)"
    - "placeholder shapes (aria-hidden): text line (height = line-height token; multi-line, shorter last line, stepped 100/100/80/40 widths) / circle (avatar, 50% radius) / rectangle-rounded (image/card, aspect-ratio + surface radius)"
    - "animation overlay (base fill gray-200 light / surface-container-highest dark + a highlight sweep gradient)"
api:
  inherits: [progress/spinner (anti-flash delay/min-display + aria-busy region), toast (live-region 'Loading' announcement)]
  props:
    - {name: variant/shape, type: enum, values: [text, circular, rectangular, rounded], description: "or per-component SkeletonText/Avatar/Image/Button"}
    - {name: width/height, type: "string|number", description: "explicit; bind text height to var(--typography-line-height) not fixed px"}
    - {name: rows/lines, type: number, description: "text-block count; auto-truncates last line"}
    - {name: animation, type: enum, values: [pulse, wave/shimmer, none]}
    - {name: loading/isLoaded, type: boolean, description: "the swap orchestrator (Chakra isLoaded->loading)"}
  schism: "AUTO-DERIVE (MUI/React Aria — wrap children, measure, overlay; boilerplate-light but SSR/RSC-UNSAFE) vs HAND-BUILT/EXPLICIT (Polaris/Carbon/Fluent — discrete SkeletonItems / explicit dims; double-maintenance but ZERO CLS + no hydration mismatch). Practice default: explicit/hand-built for CLS safety; auto-derive CSR-only"
states:
  runtime: "loading (the only state — shown -> swaps to content) + inherited anti-flash delayed/min-display windows; binary loading:true->false"
variants:
  shape: [text, circular, rectangular, rounded]
  model: "primitive (variant prop) vs per-component (SkeletonText/Avatar/…)"
  composition: "atomic primitives in Stacks/Grids (field shifting AWAY from monolithic full-page skeletons — Polaris deprecated SkeletonPage)"
  animation: [shimmer/wave, pulse, static]
accessibility:
  wcag-criteria: ["4.1.2", "4.1.3", "1.1.1", "2.3.3", "2.2.2"]
  cwv: "CLS (Core Web Vitals) — the engineering metric"
  never-read-the-boxes: "the skeleton shapes are NOT content -> aria-hidden=true on every shape/shimmer (don't announce 'graphic, gray box…'; Roselli) — over the common aria-busy-on-individual-nodes misuse"
  dual-node: "(1) live region: visually-hidden role=status (or alert) with the announcement; (2) busy container: the parent section carries aria-busy=true (the aria-busy-region pattern reused from Spinner/Progress)"
  load-complete: "aria-busy false; aria-hidden skeletons unmount + content mounts in place; live region confirms; DON'T move focus unless an explicit user action (modal); preserve focus"
  reduce-motion: "DROP to static (the cue is the SHAPE, not the motion — no substitution, unlike Spinner) — the cleanest reduce-motion case in the family"
content:
  no-content: "NEVER fake content (no 'Loading…' inside a box, no lorem-ipsum/labels — shapes blank + aria-hidden); announcement goes in the role=status node"
  shape-match-text: "line lengths reflect the real payload; stepped ragged-right (100/100/80/40), not uniform full-width bars"
  loaded-announcement: "DESCRIPTIVE ('Loading transaction history for September'), not bare 'Loading'"
motion:
  shimmer: "linear-gradient X-axis sweep (premium, momentum) — MUST be GPU-composited (transform/will-change, not background-position — thrashes on low-end mobile)"
  pulse: "opacity oscillation 0.4<->1.0 (cheaper, 'breathing', reads slower)"
  reduce-motion: "DROP to static (no substitution — the Spinner difference)"
  swap: "immediate or <=150ms crossfade; avoid long fades (locks the user out of already-parsed data)"
i18n:
  rtl: "shimmer sweep VECTOR flips (LTR translateX(-100%->200%) -> R-to-L) + asymmetric shape layouts mirror via logical properties (margin-inline-start)"
  text-lines: "suggest the expanded localized length; don't hardcode mismatching widths"
  dark-mode: "base = surface/surface-container-highest token (elevation), highlight = low-opacity white; never saturated hues"
implementation:
  - "SSR/RSC AUTO-DERIVE COLLAPSE (the sharpest trap): auto-derive measures hidden children, but server-side un-fetched image/typography dims are unknown -> collapses to a 0x0 box -> ships -> hydrates -> massive CLS, defeating the purpose. VERDICT: explicit dimensions (height=24px/width=100%) or hand-built skeleton screens are the ONLY CLS-safe option in SSR/RSC; auto-derive is CSR-only"
  - "shape-match-the-final-layout: skeleton box == real content's; constrain media to an aspect ratio + mirror on the skeleton (AspectRatioBox); bind text height to var(--typography-line-height)"
  - "dual-node a11y: aria-hidden the shapes + aria-busy region + pre-existing role=status; flip on resolution"
  - "anti-flash (inherited): delay ~150-200ms (render nothing if resolved first) + minDisplay ~500ms; shared useLoadingDelays hook"
  - "shimmer via GPU transform/will-change + CSS-variable gradient colors (bypass React re-renders); reduce-motion -> disable (static)"
  - "STREAMING/Suspense: skeleton as the Suspense fallback streamed in the server HTML (RSC) -> requires explicit dimensions; layout parity in CSS Grid not client JS"
  - "ship OPINIONATED (theme-bound — mimics host radii/shadows/grid), not headless; don't hand-roll — MUI/Ant/Carbon/Polaris/Primer/Chakra Skeleton"
composition:
  stands-on: [progress/spinner (anti-flash + aria-busy region), toast (live-region 'Loading')]
  alternative-to: [spinner (no-shape minimal/inline/short — the core call), progress (value/measurable), empty-state (the empty terminal state — Skeleton is loading)]
  composed-by: [data/table (skeleton rows), card, list, image — must import the host's radius/padding/aspect-ratio tokens for a 1:1 match]
notes:
  contested:
    - "auto-derive (boilerplate-light, SSR-unsafe) vs hand-built/explicit (CLS-safe) — the SSR collapse decides it for explicit"
    - "primitive+variant vs per-component skeletons; monolithic skeleton-page (deprecated) vs atomic composition"
    - "shimmer vs pulse vs static; how closely to shape-match (fidelity vs effort)"
  trap:
    - "SHAPE MISMATCH (skeleton not matching the real content -> a worse double-paint jump than none; the fixed-200px-image classic)"
    - "letting the SR read the boxes (must aria-hidden) / aria-busy on individual nodes (Roselli — wrong; use the region)"
    - "auto-derive in SSR/RSC (0x0 server collapse -> CLS)"
    - "skeleton for an unknown-layout/inline/short wait (-> Spinner) or an empty result (-> Empty State); skeleton-everything (fatigue); flashing for a fast load (anti-flash)"
    - "faking content; shimmer not GPU-composited (mobile jank); long content-swap fade (locks out parsed data)"
  inherited: "Progress/Spinner's anti-flash (delay/min-display) + aria-busy region pattern; Toast's live-region 'Loading' announcement"
  role-in-family: "a Foundations loading primitive that CLOSES the three-loading-patterns triad (Progress/Spinner/Skeleton) — the content-shaped layout-reserving (CLS) placeholder for an initial known-layout load; the loading terminal state of the data-container machine; the cleanest reduce-motion case (drop-to-static)"
  evolution: "CSR aesthetic -> CLS engineering contract (Core Web Vitals); skeleton-over-spinner for initial loads; aria-hidden+aria-busy+status settling (Roselli); reduce-motion-drop-to-static; SSR/RSC streaming -> explicit-dims/hand-built + Suspense fallbacks, away from monolithic skeleton-pages"
  unverified:
    - "external 2026 version numbers"
    - "the aria-busy/status AT behaviour specifics — verify against current screen readers"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-skeleton/` (16 June 2026), a Foundations loading primitive that **closes the three-loading-patterns triad** (Progress / Spinner / Skeleton) — the content-shaped, layout-reserving (CLS) placeholder for an initial known-layout load. It stands on the anti-flash (delay/min-display) + `aria-busy` region substrate inherited from Progress/Spinner and lightly the Toast "Loading" live-region announcement, and is the loading terminal state of the data-container machine Empty State described. The two passes converged almost completely — the layout-reserving/CLS contract (the Spinner opposite) + the shape-match/mismatch trap, the three-loading-patterns decision, the reduce-motion drop-to-static (the Spinner difference — the cue is the shape, not the motion), the `aria-hidden`-boxes + `aria-busy`-region + status dual-node accessibility, the variant model, the anti-flash, and the shimmer-vs-pulse-vs-static animation. The external pass supplied the decisive reconciliation of the auto-derive-vs-hand-built trade — the **SSR/RSC auto-derivation collapse** (auto-derive measures hidden children, but server-side dimensions are unknown so it collapses to a 0×0 box, hydrates, and triggers a massive CLS, defeating the purpose → **explicit dimensions / hand-built are the only CLS-safe option in SSR/RSC**) — plus the **Adrian Roselli dual-node a11y** citation (the authoritative `aria-hidden`-boxes + `aria-busy`-region pattern, over the `aria-busy`-on-individual-nodes misuse), the stepped ragged-right text pattern (100/100/80/40), the GPU `will-change`/`transform` shimmer (vs `background-position` mobile jank), the line-height-token binding, the `AspectRatioBox` CLS fix for media, the don't-skeleton-everything abstraction rule, the shift away from monolithic `SkeletonPage` toward atomic composition, the streaming/Suspense-fallback embedding, Material 3's `Modifier.placeholder`, and the descriptive loaded-announcement. Claude-pass contributions: the framing as the triad-closing layout-reserving primitive, the reduce-motion-drop distinction from Spinner, and the substrate map. The 2026 version numbers and the `aria-busy`/status AT specifics are flagged unverified. Conformant to `components/_schema.md`. The thirty-first brief — and with Progress, Spinner, and Skeleton all stable, the three-loading-patterns triad is complete.*

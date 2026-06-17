---
okf_version: "0.1"
type: component-brief
title: Spinner
description: The minimal indeterminate inline busy indicator — one corner of the three-loading-patterns triad (Progress/Spinner/Skeleton), inheriting Progress's anti-flash + reduce-motion substrate and composed by Button's loading state. A field-truth study of the no-value contract (the Progress-vs-Spinner boundary), the separate-primitive-vs-CircularProgress-variant decision (Material 3 fractured it out in May 2025), the accessibility announcement (role=status + Loading vs progressbar-indeterminate vs aria-busy + the never-unlabeled rule), the button-loading composition (the disabled-vs-aria-disabled focus trap + width-preservation), the anti-flash + reduce-motion substitution, the disableShrink CPU-jank fix, the RTL force-clockwise rule, and inline-vs-overlay placement — with the practice's defaults.
tags: [components, foundations]
category: Foundations
status: stable
aliases: [loading, inline-loading, circular-progress, progress-circle, spin, loader, busy-indicator, activity-indicator]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Spinner

> A Spinner is the **minimal, indeterminate, inline busy indicator** — a small rotating mark that says "working, duration unknown" under a strict **no-value contract** (no `aria-valuenow`). It is one corner of the **three-loading-patterns triad** the Progress brief anchored: **Progress** (a value contract / measurable / longer / large area), **Spinner** (minimal inline, ~200ms–5s, no value), **Skeleton** (a content-shaped placeholder that reserves layout to prevent CLS). It **inherits the anti-flash (delay/min-display) + reduce-motion-substitution + indeterminate-busy contract from Progress** (Spinner is the no-value inline sibling), and lightly the **"Loading" live-region announcement from Toast** (`role=status`, not focus). Its single most common use is **composition by Button's loading state**. The architectural call it forces — the **Spinner-vs-indeterminate-`CircularProgress` overlap** (visually identical) — has a recent, decisive answer: **Material 3 (May 2025) fractured the spinner *out* of indeterminate progress into a separate "Loading indicator"**, validating shipping `Spinner` as a **distinct primitive** (constrained to inline/small/no-value) so a button loader is never mistaken for a `progressbar` that needs a value contract.

---

## 1. Framing

A Spinner indicates system busyness or a suspended state awaiting resolution — *not* a measurable transition toward a known endpoint. It inherits the **anti-flash + reduce-motion + indeterminate-busy substrate from Progress** (see progress) and lightly the **"Loading" live-region announcement from Toast** (see toast), and is **composed by Button's loading state** (see button).

The defining contract is **no value** — a Spinner never carries `aria-valuenow`; it's pure "busy". The architectural question it forces — visually identical to an indeterminate `CircularProgress` — is whether to ship it separately: **Material 3's May 2025 Expressive Update split the "Loading indicator" out as a distinct primitive** (older systems folded it into `CircularProgress`/`ProgressCircle` via an `isIndeterminate` toggle). **The practice ships a separate `Spinner`** — decoupling it stops developers mapping value contracts onto inline button loaders and reduces malformed-`progressbar`-ARIA violations.

What it *isn't*: a **Progress bar** (a measurable/longer task with a value — see progress; the semantic contract differs entirely — progress implies eventual completion, a spinner implies busyness), or a **Skeleton** (a content-shaped placeholder for an *initial* load — see skeleton; a spinner is structurally agnostic and gives no shape). Why systems disagree: separate-primitive-vs-variant, the announcement model, and inline-vs-overlay placement.

## 2. Anatomy and parts
- **visual indicator (head + track)** — an `<svg>` of a faint background circle (**track**) + a foreground animated stroke (**head**/active indicator); SVG universally replaced GIFs/`border-radius` hacks (perfect HiDPI scaling + `currentColor` inheritance). Base Web/Chakra expose `TrackPath`/`ActivePath` subcomponents for deep overrides.
- **accessible wrapper** — the SVG is silent alone, so it's wrapped in a `role="status"`/`aria-live="polite"` container managing the announcement (§6).
- **optional label / description** — an adjacent text slot (Ant's `description`, deprecating `tip`); often **visually-hidden** in dense layouts but exposed to AT (§6).
- **overlay / mask (contextual)** — for the block case, a `position:relative` wrapper + an absolute scrim dimming the wrapped content + a centred spinner (Ant `Spin` embedded/`fullscreen` mode), converting the inline primitive into a blocking layout element (§5).

## 3. Properties / API
- **`size`** — a strict t-shirt scale (S/M/L — Spectrum) or numeric px/rem (MUI); the semantic scale is the recommended default (button-sized → page-sized).
- **`color`** — **`currentColor`** by default (inherits the parent text colour — white in a primary button, the text colour inline); **`staticColor`** (white/black — Spectrum) for over-imagery/video where theme tokens fail contrast; track-vs-head treatment.
- **`thickness`** — the stroke-width (often tied to `size`; Chakra exposes it).
- **`label` / `aria-label`** — the accessible name (default "Loading"); **never omit** (§6); replaces legacy `tip`.
- **`labelPosition`** — before/after/above/below (Fluent — flex-direction).
- **`delay`** — the anti-flash defer (~200–500ms — Ant/Fluent treat it as a first-class prop, §5/§11).
- **`spinning`** — the overlay/embedded toggle (Ant — wraps content with the mask).
- **API divide:** Base Web's exhaustive `overrides` (drill into `Svg`/`TrackPath`) for multi-tenant brand expression vs Spectrum's locked-down API (only `staticColor`) for strict consistency.
- (No `value`/`min`/`max` — the no-value contract; if you need a value, it's a **Progress**.)

## 4. States and variants
- **States:** **spinning** (the only state — present or not; presentational, no hover/focus/pressed) + the inherited anti-flash *delayed* and *min-display-locked* windows (§5). (Carbon's `InlineLoading` adds a **success/error end state** — the spinner resolving to a checkmark/error mark.)
- **Variants:**
  - **bare / inline** — an inline-flex element beside typography (Carbon `InlineLoading` for create/update/delete row actions); preserves line-height, no artificial padding.
  - **nested / overlay** — wraps content with a dimming mask (Ant `Spin`); `fullscreen` expands it to a page-blocking loader (merges the visual cue with modal-overlay interaction-blocking).
  - **static-color** — over full-bleed imagery/video (Spectrum `staticColor`).
  - **button-loading** — the most common (§5).
  - **size** (xs→lg), **with-label / bare**.

## 5. Usage guidance
- **The time-based decision (Material 3's heuristic — the core rule):**
  - **<200ms** → **no indicator** (optimistic update; a sub-200ms spinner strobes and *degrades* perceived performance).
  - **200ms–5s** → **Spinner** (the indeterminate loop manages psychological wait without computing progress).
  - **>5s** → a **determinate Progress bar** (an endless spinner past ~5s reads as stalled/crashed and raises anxiety).
- **Don't use a Spinner for:** a **measurable/longer task** (→ Progress — and per M3, **don't morph a spinner into a determinate progress bar** — they're different primitives; an indeterminate *Progress* may morph to determinate *within the Progress component*, but the *Spinner* doesn't become a bar), or an **initial content load** with a known layout (→ Skeleton — it reserves shape + prevents CLS; a spinner gives no shape).
- **The button-loading use (the most common):** a Button morphs to a Spinner — **width-preserving** (don't let the button shrink when the label unmounts — §11), the button **inactive during load** (prevent double-submit), the label kept ("Saving…") or replaced. Critically, use **`aria-disabled` not native `disabled`** (§6).
- **Don't over-spin** — Primer warns against many simultaneous spinners (a 20-widget dashboard shouldn't fire 20 spinners on mount — use one Skeleton for the layout, reserve the Spinner for granular user-triggered micro-interactions). Respect the anti-flash delay so fast ops show nothing.

## 6. Accessibility
- **The announcement (the contested point) — three methods:**
  - **`role="status"` + a visually-hidden "Loading"** — the **APG-recommended** pattern: a polite live region announces once without stealing focus (mirrors the Toast pattern). **The practice default for a standalone/inline spinner.**
  - **`role="progressbar"` (indeterminate, no `aria-valuenow`)** — technically permitted but apt only when it's truly *indeterminate progress*; for a pure status indicator it can make some SRs persistently announce the missing value (cognitive noise). Don't use on a minimal button spinner.
  - **`aria-busy="true"` on the region** + the SVG `aria-hidden` (Primer's stance — the spinner is decorative; the *region* signals busy, halting partial-DOM-update announcements until done, with an external `aria-live` for the status). **The practice default for the overlay/region case.**
- **NEVER an unlabeled spinner** — a bare animated SVG is **silent to AT** (a sighted user sees motion; an SR user gets nothing). It must carry an accessible name ("Loading" / contextual "Loading status checks").
- **The loading-button focus trap (sharp, recurring):** native **`disabled`** removes the button from the accessibility tree and **throws focus to `document.body`** — so a visually-impaired user who activates a button that instantly disables is violently disoriented. The fix (USWDS, increasingly the default): **`aria-disabled="true"`** (keeps the button focusable + in the focus order) + **JS-suppress the `onClick`** to prevent the double-submit. The practice default for any loading button.
- **Reduce-motion can't remove the only cue** — the rotation *is* the busy signal, so `prefers-reduced-motion: reduce` **substitutes** (a slow opacity pulse, or a static indicator + a low-frequency text ellipsis), never deletes — a frozen spinner reads as a crash (Primer: make it *subtle*, don't remove). Inherited from Progress's indeterminate case.
- **Non-text contrast** — the indicator must meet **3:1** against its background (WCAG 1.4.11) to be perceivable (the `staticColor` variant exists for this over imagery).
- **WCAG SCs:** 4.1.3 (Status Messages — the "Loading" announcement), 1.4.11 (non-text contrast), 2.3.3/2.2.2 (motion — reduce-motion), 1.1.1 (the visually-hidden name / `aria-hidden` SVG), plus the Button's SCs (the `aria-disabled` focus retention) for the in-button case.

## 7. Content guidelines
- **Never unlabeled** — always an accessible name, visually-hidden if dense (§6).
- **High specificity over generic "Loading…"** — "Loading status checks", "Processing transaction" — reassures the user the system is doing the exact requested task (lowers abandonment).
- **Sentence case** — "Updating profile", not title case (reads as a conversational status, lower cognitive load).
- **Don't progressively over-spin the label** — chaining "Fetching… → Parsing… → Rendering…" floods the `aria-live` queue; a **single holistic status** for the component's lifecycle. Announce **completion** ("Loaded"/the result) for region/longer cases.
- **In-button** — keep the label ("Saving…") or replace it, but the accessible name persists so the button has a name while loading.

## 8. Motion and transition
The rotation *is* the spinner — typically a **continuous 360° `transform: rotate`** of the SVG **plus** an animated **`stroke-dasharray`/`stroke-dashoffset`** (the arc grows/shrinks, chasing its tail — the organic loop). Keep the rotate on the **GPU** (`transform`, not layout). **The CPU main-thread-jank trap:** the `stroke-dasharray` animation is computed by the layout/paint engine and **drops frames or freezes under heavy main-thread load** (parsing a big JSON payload, rendering a large React tree) — exactly when the spinner most needs to look alive. **MUI's `disableShrink`** mitigates it: drop the expensive dash animation, leaving only the cheap GPU `rotate` (the practice should expose/default this under load). Appear/disappear is a quick fade (the anti-flash delay/min-display governs *whether* it shows). Under `prefers-reduced-motion: reduce`, **substitute** with a slow opacity pulse / static indicator (§6) — never a frozen ring. (See progress §8, 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL — force clockwise** (Spectrum's explicit rule): the spinner must **not** mirror to counter-clockwise. A clock/wheel rotating clockwise is a universal forward-time/ongoing-process metaphor; counter-clockwise reads as **undo / backward**, creating cognitive dissonance. (Most layout mirrors automatically via logical properties — the rotation is the deliberate exception.)
- **`labelPosition`** flips logically — an `after` label renders to the *left* of the spinner in an RTL (Arabic) layout, via the flex container respecting `dir`.
- **The label localizes** (short); **`currentColor`** is theme/locale-neutral (the spinner adopts the localized container's colour). (See 13-internationalization-and-rtl.)

## 10. Naming
The field splits on the separate-primitive question: **`Spinner`** (Polaris, Primer, Fluent, Chakra, Base Web) and **`Spin`** (Ant — with the mask) ship it separately; **`Loading indicator`** (Material 3, separated May 2025) / **`Inline loading`** (Carbon — names the action/position); **`CircularProgress`** (MUI, `variant="indeterminate"`) / **`ProgressCircle`** (Spectrum, `isIndeterminate`) fold it into the progress family. **The practice default: a separate `Spinner`** — it disambiguates from the Progress family, signalling "indeterminate busyness, no value props"; merging into `CircularProgress` blurs the measurable-vs-blocking boundary. Aliases `Loader`/`ActivityIndicator` (React Native) are acceptable but less descriptive. The determinate/value case is **`Progress`** (see progress). Aliases to map: `Loading`, `InlineLoading`, `CircularProgress`, `ProgressCircle`, `Spin`, `Loader`, `BusyIndicator`, `ActivityIndicator`.

## 11. Implementation notes
- **The no-value indeterminate markup** — `<span role="status" aria-live="polite">` wrapping an `aria-hidden` `<svg>` (track + head circles) + a visually-hidden "Loading data…" span; or `aria-busy="true"` on the region for the overlay case. **Never** `aria-valuenow` (that's Progress); don't `role=progressbar` a minimal button spinner.
- **The anti-flash timers (inherited from Progress)** — a `useDelay`-style hook returns `null` (renders nothing) until a `setTimeout` passes the `delay` (~200–500ms); if the promise resolves first, never render. A companion **`minDisplayTime`** (~500ms once committed) keeps it visible so it doesn't flash for one frame. Manage the overlapping timers (cleanup to avoid leaks).
- **Reduce-motion substitution** + **`disableShrink` under main-thread load** (§8).
- **In-button width-preservation** — when the label unmounts for the spinner, the button shrinks and the layout reflows; **calculate the button's width on the `onClick`/before the `isLoading` transition and freeze it** (a hard `min-width`/`width`) so it doesn't collapse; pair with **`aria-disabled` (not `disabled`) + JS-suppressed `onClick`** (§6 — the focus-retention rule).
- **The overlay/mask + interaction blocking** — `position:relative` wrapper + an absolute scrim dimming the children; **block interaction only for genuinely blocking ops** (`pointer-events`/`inert` + **`aria-busy` on the masked content**, not just visually dimmed).
- **`currentColor` theming** — the stroke is `currentColor` so it adopts the context (light/dark/brand) with no separate assets.
- **Don't hand-roll** — Polaris/Primer/Fluent/Chakra `Spinner`, Ant `Spin`, or the system's indeterminate `Progress`; skin them.

## 12. Related and alternative components
- **Stands on:** the **anti-flash (delay/min-display) + reduce-motion-substitution + indeterminate-busy contract** inherited from Progress (Spinner is the no-value inline sibling — see progress), and lightly the **live-region pattern** from Toast (the "Loading" announcement — see toast).
- **Composed by:** **Button** (the loading state — the most common use; width-preserving + `aria-disabled` focus retention — see button), and any control/area with a brief indeterminate wait.
- **Alternative to / boundary with:** **Progress** (the value/longer/measurable sibling — same family; faking a value is the Progress anti-pattern; per M3 a spinner doesn't morph into a progress bar — see progress), **Skeleton** (the content-shaped initial-load placeholder, prevents CLS — see skeleton; a spinner gives no shape), the **Toast** that closes the feedback loop (a background spinner resolving → a success/failure Toast — see toast).

(A Foundations loading primitive and one corner of the three-loading-patterns triad (Progress / Spinner / Skeleton) — the minimal, indeterminate, inline, no-value busy indicator, inheriting Progress's anti-flash + reduce-motion substrate and composed by Button's loading state. See progress for the value sibling + the inherited substrate, skeleton for the content-placeholder corner, button for the loading composition (the `aria-disabled` focus rule), toast for the "Loading" live-region touch + the closing-the-loop success toast. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **GIF → CSS `border-radius` → inline SVG** — loading rendering matured to mathematically-precise, themeable SVG (`currentColor`, `stroke-dasharray` control).
2. **The spinner-vs-progress bifurcation** — Material 2 conflated them (indeterminate `CircularProgress`); **Material 3 (May 2025) split the "Loading indicator" out as a distinct primitive** for short waits, recognising indeterminate-busyness and determinate-progress as different semantic/psychological contracts. The practice keeps them distinct in name/contract even where rendering is shared.
3. **The never-unlabeled hardening** — a bare animated SVG (silent to AT) is now a clear failure; `role=status` + a "Loading" name (or `aria-busy` on the region) is table stakes.
4. **`aria-disabled` over `disabled` in loading buttons** (USWDS) — the leading edge: preserve focus + workflow rather than throwing focus to `<body>`.
5. **The anti-flash discipline + reduce-motion substitution + `currentColor` theming** carried over from the perceived-performance and motion-accessibility work.

## 14. Sources cited
(Conservative; the external pass cited Carbon `@carbon/react v1.109.0`, React Spectrum v3.0.0/S2, Fluent v9.74.1, Ant v5/v6, the M3 "Loading indicator" Expressive Update May 2025 — held loosely and flagged unverified.) **Google Material 3** — the "Loading indicator" (separated from progress, May 2025 Expressive Update; the <200ms / 200ms–5s / >5s thresholds; the no-spinner→progress-morph rule) (2024–2026); **IBM Carbon** — `Loading`/`InlineLoading` (the inline-with-text + success/error end state) (2024–2026); **Shopify Polaris** — `Spinner` (2024–2026); **GitHub Primer** — `Spinner` (the `aria-hidden` SVG + `aria-busy` region + don't-over-spin; the subtle-not-removed reduce-motion stance) (2024–2026); **Adobe Spectrum / React Aria** — `ProgressCircle` indeterminate / `staticColor` / force-clockwise RTL / no distinct Spinner (2024–2026); **Microsoft Fluent** — `Spinner` (`labelPosition`, the `delay` as a first-class prop) (2024–2026); **MUI** — `CircularProgress` (`variant="indeterminate"`, **`disableShrink`** for the CPU-jank) (2024–2026); **Ant Design** — `Spin` (the nested-content mask, `delay`, `description`, `fullscreen`) (2024–2026); **Chakra UI** — `Spinner` (track/head, `thickness`) (2024–2026); **Base Web (Uber)** — `Spinner` / the `overrides` API / the in-button spinner (2024); **US Web Design System (USWDS)** — the `aria-disabled`-over-`disabled` loading-button pattern; **WAI-ARIA APG** — no formal spinner pattern (`role=status` / `aria-busy` / the indeterminate `progressbar`); the inherited Progress anti-flash/reduce-motion substrate (see progress) + the Toast live-region pattern (see toast). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.3, 1.4.11, 2.3.3, 2.2.2, 1.1.1.

## 15. Agent-consumable schema

```yaml
identity:
  id: spinner
  name: Spinner
  aliases: [loading, inline-loading, circular-progress, progress-circle, spin, loader, busy-indicator, activity-indicator]
  category: foundations
  status: stable
description: >
  The MINIMAL indeterminate inline busy indicator — a small rotating mark,
  NO value contract (no aria-valuenow), for ~200ms-5s waits in a button/small
  area/dropdown. One corner of the three-loading-patterns triad (Progress/
  Spinner/Skeleton); inherits Progress's anti-flash + reduce-motion +
  indeterminate-busy substrate (the no-value inline sibling); composed by
  Button's loading state. Material 3 (May 2025) fractured it OUT of
  indeterminate CircularProgress into a distinct primitive. NOT a Progress
  bar (value/longer/measurable), NOT a Skeleton (content placeholder/CLS).
anatomy:
  parts:
    - "visual indicator (svg: faint track circle + animated head stroke; currentColor; Base Web/Chakra TrackPath/ActivePath subcomponents)"
    - "accessible wrapper (span role=status / aria-live=polite — the SVG is silent alone)"
    - "optional label/description (Ant description, deprecating tip; visually-hidden in dense layouts)"
    - "overlay/mask (contextual — position:relative wrapper + absolute scrim + centred spinner; Ant Spin embedded/fullscreen)"
api:
  inherits: [progress (anti-flash delay/min-display + reduce-motion substitution + indeterminate-busy contract), toast (live-region Loading announcement)]
  props:
    - {name: size, type: "enum|number", default: M, description: "t-shirt scale (Spectrum) or px/rem (MUI); semantic scale recommended"}
    - {name: color, type: string, default: currentColor, description: "inherits parent text colour; staticColor (white/black, Spectrum) for over-imagery"}
    - {name: thickness, type: "number|string", description: "stroke-width, often tied to size"}
    - {name: label/aria-label, type: "node|string", default: Loading, description: "NEVER omit; replaces legacy tip"}
    - {name: labelPosition, type: enum, values: [before, after, above, below], default: after}
    - {name: delay, type: number, default: 0, description: "anti-flash defer ~200-500ms (Ant/Fluent first-class)"}
    - {name: spinning, type: boolean, description: "overlay/embedded toggle (Ant)"}
  no-value: "NO value/min/max — if you need a value it's a Progress"
  api-divide: "Base Web exhaustive overrides (Svg/TrackPath) vs Spectrum locked-down (only staticColor)"
states:
  runtime: "spinning (the only state — present/not, presentational) + inherited anti-flash delayed/min-display-locked windows; Carbon InlineLoading adds success/error end state"
variants:
  - "bare/inline (inline-flex beside typography; Carbon InlineLoading)"
  - "nested/overlay (Ant Spin mask; fullscreen = page-blocking)"
  - "static-color (over imagery/video; Spectrum staticColor)"
  - "button-loading (the most common)"
  - "size xs-lg; with-label/bare"
accessibility:
  wcag-criteria: ["4.1.3", "1.4.11", "2.3.3", "2.2.2", "1.1.1"]
  announcement: "(1) role=status + visually-hidden 'Loading' (APG-recommended, the practice default for standalone/inline); (2) role=progressbar indeterminate (no valuenow — apt only for true indeterminate progress, NOT a minimal spinner — SRs may nag the missing value); (3) aria-busy=true on the region + aria-hidden SVG (Primer — the practice default for overlay/region)"
  never-unlabeled: "a bare animated SVG is SILENT to AT — must carry an accessible name ('Loading'/contextual)"
  loading-button-focus-trap: "native disabled removes the button from the a11y tree + THROWS FOCUS TO BODY -> use aria-disabled=true (keeps focusable/in order) + JS-suppress onClick (USWDS) — the practice default"
  reduce-motion: "rotation is the only cue -> SUBSTITUTE (slow opacity pulse / static + text ellipsis), never freeze (= crash); Primer: make subtle, don't remove"
  contrast: "indicator >=3:1 non-text contrast (1.4.11); staticColor for over-imagery"
content:
  never-unlabeled: "always an accessible name (visually-hidden if dense)"
  specificity: "'Loading status checks' / 'Processing transaction' > generic 'Loading…' (lowers abandonment)"
  casing: "sentence case ('Updating profile')"
  no-over-spin-label: "single holistic status, don't chain 'Fetching…->Parsing…->Rendering…' (aria-live flood); announce completion for region/longer"
  in-button: "label kept ('Saving…') or replaced, but the accessible name persists"
motion:
  rotation: "continuous 360deg GPU transform:rotate + animated stroke-dasharray/dashoffset (arc grows/shrinks)"
  cpu-jank-trap: "stroke-dasharray is layout/paint-computed -> drops frames/freezes under heavy main-thread load (big JSON/large React tree); MUI disableShrink drops the dash, leaving cheap GPU rotate (expose/default under load)"
  appear: "quick fade (anti-flash governs WHETHER it shows)"
  reduce-motion: "substitute (opacity pulse/static), never freeze"
i18n:
  rtl: "FORCE CLOCKWISE (Spectrum) — do NOT mirror to counter-clockwise (clock/wheel = universal forward-time; counter-clockwise reads as undo/backward); the deliberate exception to auto-mirroring"
  label: "labelPosition flips logically (after -> left in RTL via flex respecting dir); label localizes (short)"
  color: "currentColor is theme/locale-neutral"
implementation:
  - "no-value markup: span role=status aria-live=polite > aria-hidden svg (track+head) + visually-hidden 'Loading'; OR aria-busy=true on the region (overlay); NEVER aria-valuenow; don't role=progressbar a minimal button spinner"
  - "anti-flash: useDelay hook returns null until setTimeout passes delay (~200-500ms, cleared on early resolve) + minDisplayTime (~500ms once committed); cleanup overlapping timers"
  - "reduce-motion substitution + disableShrink under main-thread load"
  - "IN-BUTTON width-preservation: calculate the button width on onClick + freeze (min-width) before isLoading so it doesn't collapse; aria-disabled (not disabled) + JS-suppress onClick"
  - "overlay/mask: position:relative + absolute scrim dimming children; block interaction ONLY for genuinely blocking ops (pointer-events/inert + aria-busy on masked content)"
  - "currentColor theming (adopts context light/dark/brand, no separate assets)"
  - "don't hand-roll — Polaris/Primer/Fluent/Chakra Spinner, Ant Spin, system indeterminate Progress"
composition:
  stands-on: [progress (anti-flash + reduce-motion + indeterminate-busy — the no-value inline sibling), toast (live-region 'Loading' announcement)]
  composed-by: [button (loading state — width-preserving + aria-disabled focus retention), any control/area with a brief indeterminate wait]
  alternative-to: [progress (value/longer/measurable sibling — no spinner->progress morph per M3), skeleton (content-placeholder initial-load/CLS — a spinner gives no shape), toast (closes the loop — background spinner -> success/failure toast)]
notes:
  contested:
    - "separate Spinner primitive (practice; M3 May 2025 corroborates) vs folded into CircularProgress/ProgressCircle (MUI/Spectrum)"
    - "the announcement model (role=status vs progressbar-indeterminate vs aria-busy)"
    - "inline vs overlay + interaction-blocking; the Base-Web-overrides vs Spectrum-locked API divide"
  trap:
    - "an UNLABELED spinner (silent to AT)"
    - "native disabled on a loading button (throws focus to body) -> aria-disabled + JS-suppress"
    - "role=progressbar/aria-valuenow on a minimal spinner (no value)"
    - "spinner for a long/measurable task (-> Progress) or initial content load (-> Skeleton, no shape)"
    - "removing the rotation under reduce-motion (frozen = crash)"
    - "stroke-dasharray jank under main-thread load (-> disableShrink)"
    - "in-button reflow (reserve width); flashing for a <1s op (anti-flash delay); over-spinning (many simultaneous spinners)"
  inherited: "Progress's anti-flash (delay/min-display) + reduce-motion substitution + indeterminate-busy contract; Toast's live-region 'Loading' announcement"
  role-in-family: "a Foundations loading primitive — the minimal indeterminate inline no-value corner of the three-loading-patterns triad (Progress/Spinner/Skeleton); composed by Button's loading state"
  evolution: "GIF->CSS->SVG; spinner-vs-progress bifurcation (M3 'Loading indicator' separated May 2025); never-unlabeled hardening; aria-disabled-over-disabled in loading buttons (USWDS); anti-flash + reduce-motion substitution + currentColor"
  unverified:
    - "external 2026 version numbers; the M3 'Loading indicator' May 2025 separation"
    - "the role=status-vs-progressbar AT announcement specifics — verify against current screen readers"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-spinner/` (16 June 2026), a Foundations loading primitive and one corner of the three-loading-patterns triad (Progress / Spinner / Skeleton) — the minimal, indeterminate, inline, no-value busy indicator. It stands on Progress's anti-flash (delay/min-display) + reduce-motion-substitution + indeterminate-busy substrate (Spinner is the no-value inline sibling) and lightly the Toast "Loading" live-region announcement, and is composed by Button's loading state. The two passes converged almost completely — the no-value contract (the Progress-vs-Spinner boundary), the separate-primitive-vs-`CircularProgress`-variant decision, the three-method accessibility announcement (`role=status` + "Loading" / indeterminate `progressbar` / `aria-busy` on the region) and the never-unlabeled rule, the button-loading composition, the anti-flash + reduce-motion substitution, and inline-vs-overlay placement. The external pass strongly corroborated the separate-primitive recommendation with a concrete platform fact — **Material 3's May 2025 Expressive Update fractured the "Loading indicator" out of indeterminate progress** — and added sharp detail folded in: the time thresholds (<200ms none / 200ms–5s spinner / >5s progress) + the no-spinner→progress-morph rule, **MUI's `disableShrink`** for the CPU main-thread `stroke-dasharray` jank, the **`disabled`-vs-`aria-disabled` focus-thrown-to-`<body>` trap** in loading buttons (USWDS) + the `onClick`-width-preservation calc, `staticColor` for over-imagery, the **RTL force-clockwise** rule (counter-clockwise reads as "undo"), `labelPosition`, the Base-Web-overrides-vs-Spectrum-locked API divide, and Carbon's `InlineLoading` success/error end state. Claude-pass contributions: the framing as the three-loading-patterns triad corner, the no-value contract, and the substrate map. The 2026 version numbers and the M3 May-2025 separation are flagged unverified. Conformant to `components/_schema.md`. The thirtieth brief; Skeleton would complete the three-loading-patterns triad.*

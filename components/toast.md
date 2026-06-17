---
okf_version: "0.1"
type: component-brief
title: Toast
description: The first Feedback brief — the non-interrupting, transient, no-focus-steal counterpart to Dialog, establishing the ARIA live-region announcement pattern the rest of the category reuses. A field-truth study of the no-focus-steal contract, the live-region announcement (role=status/polite vs role=alert/assertive + the pre-existing-region NVDA trap), the auto-dismiss-vs-WCAG-2.2.1 timing tension (pause-on-hover/focus/blur, minimums, actionable-shouldn't-auto-dismiss), the action-in-toast keyboard-reachability problem (hotkey/landmark, the visual-vs-announcement separation), the queue/stack/limit toaster, severity + color-not-sole-carrier, the no-error-toasts POV, and swipe + the button alternative — with the practice's defaults.
tags: [components, feedback]
category: Feedback
status: stable
aliases: [snackbar, notification, flag, flash, message]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Toast

> Toast opens the Feedback category, and it is the **functional opposite of a Dialog**: where a Dialog is modal, focus-trapping, and workflow-halting, a Toast is transient, auto-dismissing, and bound by a strict **no-focus-steal** contract — it delivers a brief status to the user (visually *and* to assistive tech) without making them abandon what they're doing. The whole Overlay arc routed "non-interrupting feedback" here. It inherits **Button** (the optional action + the close) and **Icon** (the severity glyph). As the first Feedback brief it **establishes the ARIA live-region announcement pattern** that Banner/Alert, Inline Message, and Progress reuse. Three realities create all the contention: it announces via a **live region** (not focus); **auto-dismiss collides with WCAG 2.2.1**; and an **action in a toast** (Undo) is a control the keyboard user can't naturally reach on a surface that never takes focus. The defining trajectory is a field-wide retreat from error and actionable toasts (GitHub Primer banned them outright; Polaris bans errors; Apple's HIG won't document a generic toast at all) toward **toasts reserved for low-priority, non-actionable, positive/informational feedback**, with errors in a Banner and actions in a persistent surface.

---

## 1. Framing

A Toast is a **brief, non-interrupting, transient notification** anchored to a screen edge that conveys an asynchronous confirmation or status ("Product saved", "Connection restored") and **auto-dismisses without blocking the page or stealing focus**. It inherits **Button** (action + close — see button) and **Icon** (severity — see icon).

**The three realities that define it:**
- **No focus steal** — it announces to AT via a **live region**, not by moving focus (the Dialog opposite).
- **Auto-dismiss collides with WCAG 2.2.1** (Timing Adjustable) — a notification that vanishes on a timer fights the "enough time to read" rule.
- **An action in a toast** (Undo) sits on a transient, non-focus-stealing, portalled surface the keyboard user can't sequentially tab to before it expires.

**The boundaries** (precise across field leaders):
- **vs. Dialog** — *interruption*: a Dialog traps focus and demands resolution; a Toast never does. A required acknowledgement / destructive confirm is a **Dialog** (see dialog).
- **vs. Banner/Alert** — *persistence + document flow*: a Banner is persistent and in-flow, staying until resolved/dismissed; a Toast floats and vanishes. Persistent errors, connection failures, and corrective-action messages belong in a **Banner** (see banner).
- **vs. Inline Message** — *spatial context*: an Inline Message sits next to the DOM element it describes (field validation); a Toast is viewport-relative and disconnected (see inline-message).
- **vs. Notification Center** — a persistent inbox/log of past notifications, vs. the transient flare.

Why systems disagree: polite-vs-assertive, the auto-dismiss timing, whether errors/actions belong in a toast at all, and the queue model.

## 2. Anatomy and parts
A layered architecture separating global state from per-toast rendering:
- **Provider** (`ToastProvider`/`ToastQueue`) — the app-root global state manager: the queue, timeouts, visibility limit, swipe config.
- **Viewport / region** (`ToastRegion`) — the persistent fixed-position container (portalled to `<body>`) that owns the queue **and the ARIA live region**; semantically often an `<ol>` in a labelled region/landmark. **Must pre-exist in the DOM** (§6).
- **Root** (the individual toast) — the message card; owns its auto-dismiss timer and hover/focus pause.
- **severity glyph** (inherits Icon) — info/success/warning/error; decorative; **color-not-sole-carrier** (distinct shapes, §6).
- **action + close controls** (inherit Button) — an optional safe-to-ignore action (Undo/Retry) + the dismiss control (the non-gesture alternative to swipe); usually restricted to text/ghost/outline variants so they don't overwhelm the card.
- **title/summary** + optional **description/detail** — concise text nodes.
- **progress/timeout indicator** — optional bar (and its paused state).

## 3. Properties / API
The API diverges from declarative UI because a toast is dispatched, not rendered inline — field leaders converge on an **imperative dispatcher** to a root-level queue.

- **Imperative dispatcher (the converged model)** — a global controller/hook/class: `toast()`/`toast.success()`/`toast.error()`/`toast.promise()` (Sonner), `useToastController` (Fluent v9), or `ToastQueue.add()` (React Aria, managing state *outside* the React tree). `.add()` returns a **key** for programmatic `.close(key)` (e.g. cancel a toast when the async op is aborted). Any nested component or background function can fire one without prop-drilling.
- **Declarative alternative** (Radix — `Toast.Root` + `open`/`onOpenChange`) maps to local state but invites overlap/race/no-global-limit, so teams wrap it in an imperative store anyway.
- **Core props:** `duration`/`timeout` (auto-dismiss ms; **min ~5000ms**; `Infinity` for persistent), `placement`/`position`, `type`/`severity` (+ maps to live-region politeness), `action {label, onClick}` (+ `cancel`), `dismissible`/`onDismiss`/`onAutoClose`, `id`/update (promise loading→success/error on one toast), `hotkey` (Radix — the keys to jump focus into the region, e.g. `["F8"]`), `visibleToasts`/limit.

## 4. States and variants
- **Lifecycle states** (Fluent's model): **queued** (held until the visibility limit allows) / **visible** (mounted) / **paused** (hover/focus/blur halts the timer — §6) / **dismissed** (hidden, still mounted for exit anim) / **unmounted**.
- **Variants:**
  - **severity:** info / success / warning / error (+ **loading/promise**).
  - **with-action** (Undo/Retry) / **with-close** / **with-progress**.
  - **snackbar** (single, bottom-center, ≤1 action — Material/Polaris) vs the **stacked corner toaster** (multiple, collapse-by-default/expand-on-hover — Sonner).
  - **persistent** (`Infinity` — errors/actionable) vs auto-dismiss.

## 5. Usage guidance
- **Use a Toast** for **brief, non-critical, non-actionable, positive/informational** feedback the user doesn't need to act on — "Saved", "Copied", "Message sent", "Connection restored". It reassures without interrupting.
- **Don't use a Toast for:**
  - **Critical/blocking info or a required decision** → **Dialog** (see dialog).
  - **Errors / connection failures / corrective-action messages** → a persistent **Banner/Alert** (see banner). *Errors in an auto-dismissing, focus-avoiding toast are a high-risk anti-pattern* — the user looks away and misses a failure.
  - **Field/form validation** → an **Inline Message** (`aria-describedby`, see text-field).
  - **Anything essential or that must be re-read** — a toast is transient and easy to miss (it never takes focus).
- **Decision frameworks:**
  - **Toast vs. Banner:** transient + self-dismissing + corner (Toast) vs. persistent + in-flow + stays-until-resolved (Banner). Importance + persistence, not appearance.
  - **Errors-as-toast? — the practice POV: no.** Polaris bans error toasts; **GitHub Primer deprecated error and actionable toasts entirely** after usability testing with disabled users ("cannot be addressed with a sprinkling of ARIA"); Apple's HIG won't document a generic toast. The practice default: **restrict Toasts to non-actionable positive/informational feedback; route errors to a Banner/Inline and actions to a persistent surface.** General-purpose libs (MUI, Fluent, PrimeReact) ship an error variant but shift the burden (sticky/infinite) to the developer.
  - **Actionable toasts shouldn't auto-dismiss** — if there must be an Undo, give it `Infinity` (or a generous, paused timeout) and a real keyboard route (§6); racing a timer to click Undo is the anti-pattern. If the action matters, it belongs in a persistent Banner.

## 6. Accessibility
The most complex and contested a11y of any feedback component — two hard problems: the live-region announcement and action reachability.

- **The ARIA live-region announcement (the crux, and the category-defining pattern):** the toast announces **without moving focus**, via a live region. **`role="status"` / `aria-live="polite"`** for info/success (waits for a pause — preserves context). **`role="alert"` / `aria-live="assertive"`** for warning/error (interrupts). Default polite; assertive only for genuinely urgent.
- **The pre-existing-region trap (the #1 toast a11y bug):** if a `role="status"` element and its text are injected into the DOM *simultaneously* (the common declarative case), some AT — notably **NVDA** — ignores the update and announces nothing. The region container **must already exist** (empty) before the text changes. Radix mounts an empty `role="status"` at app load and **delays the text injection by one frame** (a `useNextFrame` hook) so the browser registers a distinct mutation. One persistent **shared** region, not one per toast.
- **No focus steal** — the toast does not move focus (the Dialog opposite); the page stays put.
- **Auto-dismiss vs WCAG 2.2.1 (Timing Adjustable):** a static timeout is a violation (reading speeds vary). The timer must **pause on hover, on focus, and on window blur** (a toast firing while you're in another tab/app must not deplete in the background — React Aria pauses the whole queue centrally; Radix broadcasts `blur`/`focus` custom events down to each Root). Give **enough time to read** (≥~5000ms, scaled to content); **error/actionable toasts should not auto-dismiss** (`Infinity`).
- **The action-in-toast keyboard-reachability problem (no field consensus):** the toast portals to the bottom of `<body>` but focus stays where the user was, so there's no sequential tab path to the Undo before the timer expires. The contested strategies:
  - **Radix — an F8 hotkey** jumps focus into the region (needs educating the user via an SR-only `altText`).
  - **React Aria — a focusable landmark** (F6 / Shift+F6 native landmark nav), the toast wrapped as an `alertdialog`.
  - **Carbon — `ActionableNotification`** forces `role="alertdialog"` and **moves focus into it** on mount — guaranteeing reachability but *breaking the non-interrupting contract*.
  - **Primer — banned actionable toasts;** **Apple — prohibits the pattern at the OS level.**
  - The practice default: **don't put actions in toasts** (persistent Banner instead); if unavoidable, the React-Aria focusable-landmark route + not-auto-dismissing.
- **The visual-vs-announcement separation (Radix's sophisticated answer):** an action nested in `role="alert"` is read as one confusing string ("File deleted Undo Close"). Radix sets the **visible toast `aria-live="off"`** and routes a developer-authored descriptive **`altText`** ("Notification: File deleted. Press Ctrl+Z to undo") to a *separate* visually-hidden assertive region — severing the visual DOM from the announcement.
- **Swipe + the close Button** — swipe-to-dismiss needs the close Button as the non-gesture alternative (WCAG 2.5.1/2.5.7 — the Drawer rule).
- **Color-not-sole-carrier** — severity is icon + text, not colour alone (1.4.1).
- **WCAG SCs:** **4.1.3 (Status Messages — the headline)**, 2.2.1 (Timing Adjustable), 1.4.1 (colour not alone), 2.5.1/2.5.7 (swipe alternative), 2.1.1 (keyboard — reach the action), plus the Buttons' SCs.

## 7. Content guidelines
- **Extreme brevity** — Polaris caps at ~**three words** ("Product saved", "Connection restored"); Atlassian truncates aggressively and warns against multi-line wrapping. A toast is glanced at, not read.
- **State the factual outcome** — clinical, direct, no jargon/conversational phrasing; the **severity icon** carries the emotional tone so the text stays scannable.
- **No errors as toast** (the POV) — anything needing detail, bullets, or nuance belongs in an Inline Message or Dialog.
- **The action label** is one clear verb ("Undo", "Retry"); the dismiss is a labelled close control.

## 8. Motion and transition
Slide + fade in from the edge/corner (~150–250ms) — motion establishes the spatial relationship of a surface disconnected from the user's focus point, without reflowing the layout. The **stacked** model collapses by default and **expands on hover** (Sonner: front toast `scale(1)`, next `0.95`, next `0.9`, translated on Y for depth; on hover it computes each `translateY` by summing preceding toast heights into a CSS variable). The **timeout/progress** bar animates down and **pauses on hover/focus** (the visible counterpart of the 2.2.1 pause). Swipe tracks the pointer and snaps back below threshold. Under `prefers-reduced-motion: reduce`, drop slide/scale to a fade or snap. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** — the Viewport is fixed to a screen edge, so **use logical properties** (`inset-inline-end`/`inset-inline-start`, `margin-inline-start`) not `right`/`left` (hardcoded directions fail catastrophically in Arabic/Hebrew); the **entrance/exit motion mirrors** (slide from the *trailing* reading edge in both directions), preserving the spatial metaphor.
- **Text expansion** — toasts are short but expand (+30–50%); **wrap, don't truncate a status**, and the **auto-dismiss duration must scale with the translated reading time** (a fixed ms that suited English is too short for German).
- **Safe-area** — `env(safe-area-inset-*)` so notches/dynamic-islands/keyboards/swipe-bars don't obscure the toast. (See 13-internationalization-and-rtl.)

## 10. Naming
**`Toast`** dominates (Radix, React Aria, Polaris, Fluent v9, Base Web); **`Snackbar`** is Material's bottom-single-action term; **`Notification`** is Carbon's (toast variant); **`Flag`** is Atlassian's (with a `FlagGroup`/`FlagsProvider`); **`Flash`** is Primer's (leans inline/banner); Ant splits **`message`** (centered, simple) and **`notification`** (corner, richer/actionable). **The practice default: `Toast`** managed by a **`Toaster`/`ToastRegion`** (the queue + the live region), with the **`toast()` imperative API**, `Snackbar` as the bottom-single-action alias/variant, and the persistent message routed to **`Banner`/`Alert`**. Aliases to map: `Snackbar`, `Notification`, `Flag`, `Flash`, `message`.

## 11. Implementation notes
- **One `Toaster`/Viewport owns the queue + the pre-existing live region.** Mount a single `<Toaster>` at the app root; it renders a persistent empty ARIA live region (so the pre-existing-region rule holds — §6) and the fixed-position viewport, and manages the queue/limit/stack.
- **The imperative `toast()` store** — a global store the Toaster subscribes to (Sonner); any code fires a toast without context drilling; `toast.promise()` updates one toast id loading→success/error.
- **Duration + pause + actionable rule** — content-scaled default (≥~5000ms), **paused on hover/focus/blur**, `Infinity` for error/actionable; never dismiss while interacted with (2.2.1).
- **The queue/stack/limit** — modern systems stack (max visible ~**3**, the rest queue/collapse) over the older single-FIFO (Material/early Carbon); the **Sonner hover-bridge** is a real trap: when the stack expands, empty gaps form between toasts and the cursor crossing them fires `mouseleave` → premature collapse; fix with an `::after` pseudo-element bridging the gap so the hover stays continuous.
- **Portal + the tab-order mismatch** — the viewport portals to `<body>` to escape `overflow:hidden`/z-index; but portals append **oldest-first** in DOM while the stack renders **newest-on-top** visually, so keyboard tab order disagrees with the visual order. Radix fixes this with **focus-proxy `<span>`s** (before/after the list) that redirect focus to the newest toast, and intercepts `keydown` to **reverse the tab order** to match the visual stack.
- **The keyboard route + the visual-vs-announcement separation** — the hotkey/landmark (§6) and Radix's `aria-live="off"` + `altText` split for actionable toasts.
- **Swipe + close Button** (the non-gesture alternative — 2.5.1/2.5.7); Radix exposes `--radix-toast-swipe-move-x`/`-end-x` for physics-bound gesture tracking.
- **Compose with a Notification Center** — enterprise systems (Fluent, Carbon) pair the transient toast with the **same payload pushed to a persistent Drawer/inbox/page**, so users who miss the ~5s window still get the history — resolving the transient-vs-record conflict.
- **Don't hand-roll** — **Sonner** (the de facto React toast — stacked, promise, the store, the hover-bridge), **Radix `Toast`** (the headless reference — swipe, F8, the pre-existing region + focus proxies + the announcement separation), or **React Aria** (the focusable `ToastRegion` landmark); skin them.

## 12. Related and alternative components
- **Stands on:** Button (the optional action + the close — see button), Icon (the severity glyph — see icon).
- **Alternative to / boundary with:** **Dialog** (the interrupting, focus-stealing, must-act opposite — see dialog), **Banner/Alert** (persistent, in-flow, important — the toast-vs-banner boundary; errors and actions go here; see banner), **Inline Message** (field/section validation — see inline-message), a **Notification Center** (a persistent inbox/log — composed *with* toasts), **Progress/Spinner** (a loading/promise toast shades into progress feedback — see progress and spinner).
- **Establishes for the category:** the **ARIA live-region announcement pattern** (`role=status`/`alert`, the pre-existing region) that Banner/Alert, Inline Message, and Progress reuse.

(The first Feedback brief — the non-interrupting, transient, no-focus-steal counterpart to Dialog, establishing the live-region announcement pattern the rest of the category inherits. See dialog for the interrupting boundary, button for the action/close, icon for the severity glyph, banner/inline-message/progress when briefed for the siblings that reuse the live-region pattern. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **Sonner standardised the modern toast** — the stacked, collapse-by-default/expand-on-hover toaster with an imperative `toast()`/`toast.promise()` store (and the `::after` hover-bridge, the height-summing expansion) became the de facto React pattern.
2. **The live-region + pre-existing-region rule hardened** — one persistent region the toaster injects into, with the one-frame-delay / `useNextFrame` workaround for the NVDA bug; role=status default, alert for urgent.
3. **The auto-dismiss-vs-WCAG correction** — pause-on-hover/focus/blur, content-scaled minimums (≥5s), and error/actionable toasts that don't auto-dismiss became table stakes (2.2.1).
4. **The retreat from error and actionable toasts** — driven by WCAG auditing: **Primer banned them, Polaris bans errors, Apple won't document the pattern**; the opinionated default is toasts for low-priority positive/informational feedback only, errors→Banner, actions→persistent surface.
5. **The Notification-Center composition** emerged as the answer to the transient-vs-record conflict.

## 14. Sources cited
(Conservative; reconcile with external. WAI-ARIA APG has **no formal toast pattern** — the Alert/Alertdialog patterns + live regions are stopgaps; a native `<toast>`/`<popupdialog>` is under Open UI brainstorming — flagged unverified.) **Sonner** (Emil Kowalski — the de facto React toast; stacked/expand-on-hover, the height-sum expansion, the `::after` hover-bridge, `toast.promise()`) (2024–2026); **Radix UI** `Toast` (the headless reference — swipe + `--radix-toast-swipe-*`, the F8 hotkey, the pre-existing region + `useNextFrame`, focus proxies + tab-order reversal, the `aria-live=off`+`altText` separation) (2024–2026); **Adobe Spectrum / React Aria** `Toast`/`ToastRegion`/`ToastQueue` (the focusable-landmark + alertdialog, centralised pause) (2024–2026); **Google Material 3** Snackbar (bottom, single, ≤1 action) (2024–2026); **IBM Carbon** Notification (toast/inline + `ActionableNotification` forcing `alertdialog`+focus, queue→stack) (2024–2026); **Shopify Polaris** `Toast` (bottom-center, ~3-word max, the no-error-toasts POV) (2024–2026); **GitHub Primer** (the inline `Flash`; the deprecation of error/actionable toasts) (2024–2026); **Atlassian** `Flag`/`FlagGroup` (truncation, no multi-line) (2024–2026); **Microsoft Fluent v9** `Toast`/`useToastController`/MessageBar (the lifecycle states) (2024–2026); **Base Web (Uber)** Toast/Snackbar (2024); **Ant Design** `message`/`notification` (2024–2026); **Apple HIG** (the OS-level prohibition of timed toast UI) (2024–2026). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.3, 2.2.1, 1.4.1, 2.5.1, 2.5.7, 2.1.1.

## 15. Agent-consumable schema

```yaml
identity:
  id: toast
  name: Toast
  aliases: [snackbar, notification, flag, flash, message]
  category: feedback
  status: stable
description: >
  A brief NON-INTERRUPTING TRANSIENT notification at a screen edge that
  auto-dismisses and NEVER steals focus — the Dialog opposite — announced via
  an ARIA live region. Opens the Feedback category + establishes the
  live-region pattern. NOT a Dialog (modal/must-act), NOT a Banner/Alert
  (persistent/in-flow — errors + actions go here), NOT an Inline Message
  (field/section), NOT a Notification Center (persistent log).
anatomy:
  layered:
    - "Provider (ToastProvider/ToastQueue): app-root global state — queue, timeouts, limit, swipe config"
    - "Viewport/region (ToastRegion): persistent fixed-position container (portalled to body) owning the queue AND the ARIA live region; <ol> in a labelled region/landmark; MUST PRE-EXIST in the DOM"
    - "Root (the toast): the card; owns its auto-dismiss timer + hover/focus pause"
  parts:
    - "severity glyph (inherits icon; decorative; color-not-sole-carrier — distinct shapes)"
    - "action + close (inherit button; action = safe-to-ignore Undo/Retry; close = non-gesture swipe alternative; text/ghost/outline only)"
    - "title/summary + optional description/detail; optional progress/timeout bar"
api:
  inherits: [button (action + close), icon (severity)]
  dispatcher: "IMPERATIVE (converged) — toast()/.success/.error/.promise (Sonner), useToastController (Fluent), ToastQueue.add()->key + .close(key) (React Aria, state outside React); declarative Radix Toast.Root + open/onOpenChange invites overlap/race (wrap in a store)"
  props:
    - {name: duration/timeout, type: number, description: "auto-dismiss ms; min ~5000; Infinity = persistent (errors/actionable)"}
    - {name: placement/position, type: enum, description: corner/edge}
    - {name: type/severity, type: enum, values: [info, success, warning, error, loading], description: maps to live-region politeness}
    - {name: action, type: "{label,onClick}(+cancel)"}
    - {name: dismissible/onDismiss/onAutoClose, type: "boolean/function"}
    - {name: id/update, type: string, description: "promise loading->success/error on one toast"}
    - {name: hotkey, type: "string[]", description: "Radix — keys to jump focus into the region, e.g. ['F8']"}
    - {name: visibleToasts/limit, type: number, description: "max visible ~3, rest queue/collapse"}
states:
  lifecycle: [queued (held until limit allows), visible, "paused (hover/focus/blur halts timer)", dismissed (hidden, mounted for exit), unmounted]
variants:
  severity: [info, success, warning, error, loading/promise]
  composition: [with-action, with-close, with-progress]
  form: "snackbar (single, bottom-center, <=1 action) vs stacked corner toaster (collapse-default/expand-on-hover)"
  persistence: "persistent (Infinity — errors/actionable) vs auto-dismiss"
accessibility:
  wcag-criteria: ["4.1.3", "2.2.1", "1.4.1", "2.5.1", "2.5.7", "2.1.1"]
  live-region: "role=status/aria-live=polite (info/success) vs role=alert/assertive (warning/error); default polite, assertive only urgent"
  pre-existing-region-trap: "region must already exist EMPTY before text injects — NVDA ignores region+content added together; Radix mounts empty role=status at load + delays text one frame (useNextFrame); ONE shared region not per-toast"
  no-focus-steal: "does NOT move focus (Dialog opposite)"
  auto-dismiss-2.2.1: "static timeout = violation; PAUSE on hover + focus + window blur (React Aria pauses queue centrally; Radix broadcasts blur/focus events); enough time to read (>=~5000ms, content-scaled); error/actionable -> Infinity"
  action-reachability: "portalled toast + focus stays put = no tab path. Strategies (no consensus): Radix F8 hotkey (+SR altText); React Aria focusable landmark F6 + alertdialog; Carbon ActionableNotification forces alertdialog + MOVES focus (breaks contract); Primer BANNED; Apple prohibits at OS level. Practice: no actions in toasts (persistent Banner); if unavoidable, React-Aria landmark + no-auto-dismiss"
  visual-vs-announcement: "action in role=alert reads 'File deleted Undo Close' as one string; Radix sets visible toast aria-live=off + routes descriptive altText ('...Press Ctrl+Z to undo') to a separate hidden assertive region"
  swipe: "swipe-to-dismiss needs the close Button as non-gesture alternative (2.5.1/2.5.7)"
  color: "severity = icon + text, not colour alone (1.4.1)"
content:
  brevity: "extreme — Polaris ~3 words ('Product saved'); Atlassian truncates, no multi-line wrap"
  tone: "factual outcome, clinical/direct, no jargon; severity icon carries the tone"
  no-errors: "errors/detail/bullets -> Inline Message or Dialog"
  action: "one clear verb (Undo/Retry); labelled close"
motion:
  enter: "slide+fade from edge ~150-250ms (spatial cue, no reflow)"
  stack: "Sonner collapse-default (scale 1/0.95/0.9 + Y-translate depth) -> expand-on-hover (translateY = sum of preceding heights via CSS var)"
  progress: "timeout bar animates + PAUSES on hover/focus"
  swipe: "tracks pointer, snaps back below threshold"
  reduce-motion: "fade/snap"
i18n:
  rtl: "Viewport fixed to a screen edge — use LOGICAL props (inset-inline-end/start, margin-inline-start) not right/left (hardcoded fails in ar/he); entrance/exit motion mirrors (slide from trailing reading edge both directions)"
  expansion: "short but +30-50% — WRAP not truncate + auto-dismiss DURATION scales with translated reading time"
  safe-area: "env(safe-area-inset-*) so notches/island/keyboard/swipe-bar don't obscure"
implementation:
  - "ONE Toaster/Viewport owns the queue + a persistent EMPTY live region (pre-existing rule) + fixed-position viewport + the limit/stack"
  - "imperative toast() global store the Toaster subscribes to (no context drilling; toast.promise updates one id loading->success/error)"
  - "duration content-scaled + pause-on-hover/focus/BLUR + Infinity for error/actionable; never dismiss while interacted with"
  - "queue/stack/limit: stack (max ~3, rest queue/collapse) over single-FIFO; SONNER HOVER-BRIDGE — expanding stack leaves gaps -> cursor crossing fires mouseleave -> premature collapse; fix with ::after pseudo-element bridging the gap"
  - "PORTAL TAB-ORDER MISMATCH — portals append oldest-first in DOM but render newest-on-top visually; Radix focus-proxy spans redirect to the newest + intercept keydown to REVERSE tab order to match the visual stack"
  - "keyboard route (hotkey/landmark) + Radix visual-vs-announcement separation (aria-live=off + altText) for actionable toasts"
  - "swipe + close Button (2.5.1/2.5.7); Radix --radix-toast-swipe-move-x/-end-x"
  - "compose with a Notification Center — same payload to a persistent Drawer/inbox so missed toasts have a record"
  - "don't hand-roll — Sonner / Radix Toast / React Aria ToastRegion"
composition:
  stands-on: [button (action + close), icon (severity)]
  alternative-to: [dialog (interrupting/must-act opposite), banner/alert (persistent/in-flow — errors + actions), inline-message (field/section), notification-center (persistent log; composed WITH toasts), progress/spinner (loading toast)]
  establishes: "the live-region announcement pattern (role=status/alert + pre-existing region) for the Feedback category — Banner/Inline-Message/Progress reuse it"
notes:
  contested:
    - "polite-vs-assertive default"
    - "auto-dismiss duration + whether to auto-dismiss at all"
    - "errors-as-toast (Polaris/Primer/Apple say NO; practice: errors persistent)"
    - "actionable toasts (Primer banned; Carbon moves focus breaking the contract; reachability has no consensus)"
    - "queue (single-FIFO) vs stack (max-visible)"
  trap:
    - "live region created WITH its content -> announces nothing (NVDA); must pre-exist + one-frame delay"
    - "auto-dismiss too fast / no pause (2.2.1 fail)"
    - "action in an auto-dismissing toast a keyboard user can't reach"
    - "a region per toast; color-only severity; essential info in a transient toast"
    - "portal DOM order != visual stack order (tab confusion) -> focus proxies + tab reversal"
    - "Sonner expand-on-hover gap collapse -> ::after bridge"
  inherited: "Button action+close; Icon severity"
  role-in-family: "the first Feedback brief — the non-interrupting transient counterpart to Dialog; establishes the live-region pattern the category reuses"
  evolution: "Sonner stacked model + toast() store + hover-bridge; live-region pre-existing-region hardened (useNextFrame/NVDA); auto-dismiss-vs-WCAG correction; retreat from error+actionable toasts (Primer ban/Polaris/Apple); Notification-Center composition"
  unverified:
    - "external 2026 version numbers"
    - "WAI-ARIA APG has no toast pattern; a native <toast>/<popupdialog> is under Open UI brainstorming — verify"
    - "the live-region/NVDA + 2.2.1 specifics — verify against current AT behaviour"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-toast/` (16 June 2026), the first Feedback brief — the non-interrupting, transient, no-focus-steal counterpart to Dialog, establishing the ARIA live-region announcement pattern the rest of the category (Banner/Alert, Inline Message, Progress) inherits. It stands on Button (action + close) and Icon (severity). The two passes converged almost completely — the no-focus-steal contract and the Dialog/Banner/Inline-Message boundaries, the live-region announcement (`role=status`/polite vs `role=alert`/assertive) and the pre-existing-region NVDA trap (mount the empty region first; Radix's one-frame `useNextFrame` delay; one shared region), the auto-dismiss-vs-WCAG-2.2.1 tension (pause on hover/focus/blur, content-scaled ≥5s minimums, error/actionable should not auto-dismiss), the action-in-toast keyboard-reachability problem, the queue/stack/limit toaster, severity + color-not-sole-carrier, the swipe + close-button alternative, and `Toast` (managed by a `Toaster`, imperative `toast()`) as the naming default. External-pass contributions folded in: the **action-in-toast strategy table** (Radix F8 / React Aria F6-landmark+alertdialog / Carbon's focus-moving `ActionableNotification` / Primer's outright ban / Apple's OS-level prohibition), the **Radix visual-vs-announcement separation** (`aria-live="off"` + a descriptive `altText` to a hidden assertive region), the **Sonner stacked/expand-on-hover model** (scale/Y-translate depth, the height-sum expansion, the `::after` hover-bridge for the gap-collapse trap), the **portal tab-order mismatch** (focus proxies + keydown tab-reversal), the imperative-dispatcher detail (`ToastQueue.add()→key`, `useToastController`), the Notification-Center composition, the lifecycle states, and the concrete content limits (Polaris ~3 words) + `env(safe-area-inset-*)`. Claude-pass contributions: the framing as the category-opening live-region establisher, the three-realities framing, and the substrate map. The 2026 version numbers, the no-formal-APG-pattern / native-`<toast>` Open-UI status, and the live-region/NVDA + 2.2.1 specifics are flagged unverified. Conformant to `components/_schema.md`. Opens the Feedback category; Banner/Alert, Inline Message, and Progress reuse the live-region pattern it establishes.*

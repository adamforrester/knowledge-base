# Toast — field-truth study (Claude pass)

## 1. Framing
A Toast is a **brief, non-interrupting, transient notification** that appears at a screen edge, conveys a confirmation or status ("Saved", "Message sent"), and **auto-dismisses** without blocking the page or stealing focus. It opens the Feedback category and is the **opposite of a Dialog**: where a Dialog interrupts, traps focus, and demands resolution, a Toast supplements, never takes focus, and disappears on its own. The whole Overlay arc routed "non-interrupting feedback" here (Dialog/Tooltip/Drawer). It inherits **Button** (the optional action + the close — see button) and **Icon** (the severity glyph — see icon). As the first Feedback brief, it **establishes the ARIA live-region announcement pattern** the rest of the category (Banner/Alert, Inline Message, Progress) will reuse.

Three realities define it and create all the contention:
- **No focus steal** — it announces to AT via a **live region**, not by moving focus (the Dialog opposite).
- **Auto-dismiss collides with WCAG** — a notification that vanishes on a timer fights SC 2.2.1 (Timing Adjustable) and the "enough time to read" rule.
- **An action in a toast** (Undo) is the hard case — a transient, non-focus-stealing surface is a bad place to put a control the user must reach before it disappears.

What it *isn't*: a **Dialog** (modal, focus-trapped, must-act — see dialog), a **Banner/Alert** (persistent, in the page flow, for important/ongoing messages — see banner when briefed), an **Inline Message** (field/section-level validation — see inline-message when briefed), or a **Notification Center** (a persistent log/inbox). Why systems disagree: polite-vs-assertive, the auto-dismiss timing, whether errors/actions belong in a toast at all, and the queue model.

## 2. Anatomy and parts
- **toast viewport / region** — the fixed-position container at a corner that owns the queue **and is the ARIA live region** (must pre-exist in the DOM — §6); often a focusable landmark reachable by a hotkey (§6/§11).
- **toast surface** — the individual notification card.
- **severity icon** — info/success/warning/error glyph (decorative, `aria-hidden`; color-not-sole-carrier — §6).
- **title / message** — a concise string (optional title + body).
- **action button** — an optional single action (Undo, View — a Button).
- **dismiss / close button** — an icon Button ("Dismiss") — the non-gesture alternative to swipe (§6).
- **progress / timeout indicator** — an optional bar showing time-to-dismiss (and paused-on-hover state).

## 3. Properties / API
- **The imperative `toast()` API** (Sonner-style) is the converged shape: `toast("Saved")`, `toast.success(...)`, `toast.error(...)`, `toast.promise(p, {loading, success, error})` — called from anywhere, the toaster renders + queues. The alternative is a declarative provider + `useToast()`.
- **severity / variant** — `info` / `success` / `warning` / `error` (+ `loading` for promise toasts).
- **`duration`** — the auto-dismiss timeout; **`Infinity`/`null` for persistent** (errors/actionable — §5/§6); should scale with content length.
- **`action`** — `{label, onClick}` (a Button); plus an optional `cancel`.
- **`dismissible` / `onDismiss` / `onAutoClose`** — close behaviour + callbacks.
- **`position`** — corner/edge (top-right, bottom-center, …).
- **queue / `visibleToasts` / limit** — max visible, the rest collapse/queue (§11).
- **`id` / update** — update or dedupe an existing toast (e.g. promise loading → success).

## 4. States and variants
- **States:** entering / **showing** / **paused** (hover/focus halts the timeout — §6) / exiting (+ swiping). The toast has no interactive states beyond its action/close.
- **Variants:**
  - **severity:** info / success / warning / error (+ **loading/promise** — resolves to success/error).
  - **with-action** (Undo/View) / **with-close** / **with-progress** (the timeout bar).
  - **snackbar** (single, bottom-center, ≤1 action — Material/Polaris) vs the **stacked corner toaster** (multiple, expand-on-hover — Sonner).
  - **persistent** (`duration: Infinity` — errors/actionable) vs auto-dismiss.

## 5. Usage guidance
- **Use a Toast** for a **brief, non-critical, transient confirmation or status** the user doesn't need to act on — "Saved", "Copied", "Message sent", "Connection restored". It reassures without interrupting.
- **Don't use a Toast for:**
  - **Critical/blocking info or a required decision** → a **Dialog** (modal, focus-stealing — see dialog).
  - **Persistent or important in-context messages** (a system outage, a page-level warning) → a **Banner/Alert** (in the flow, doesn't vanish — see banner).
  - **Form validation / field errors** → an **Inline Message** next to the field (persistent, `aria-describedby` — see text-field, inline-message).
  - **Anything essential or that must be re-read** — a toast is transient and easy to miss (it never takes focus); never put information the task depends on in one.
- **Decision frameworks:**
  - **Toast vs. Banner/Alert:** transient + dismisses itself + corner (Toast) vs. persistent + in-flow + stays until resolved (Banner). Importance + persistence, not appearance.
  - **Errors-as-toast?** A live POV split: Polaris bans error toasts (errors are persistent/inline); the practice default is **errors belong in a persistent surface (Banner/Inline), not an auto-dismissing toast** — if an error *must* toast, it's a persistent `role=alert` toast that doesn't auto-dismiss.
  - **Actionable toasts shouldn't auto-dismiss** — if there's an Undo/action, give it an infinite or generous timeout (and pause-on-hover), or move it to a persistent surface; racing the user against a timer to click Undo is the anti-pattern.

## 6. Accessibility
- **The ARIA live-region announcement (the crux, and the category-defining pattern):** a toast must be announced **without moving focus** — via a live region. **`role="status"` / `aria-live="polite"`** for informational/success (waits for a pause); **`role="alert"` / `aria-live="assertive"`** for errors/critical (interrupts). Default polite; reserve assertive for genuinely urgent.
- **The pre-existing-region trap (the #1 toast a11y bug):** the live-region container **must already exist in the DOM** (empty) before the toast text is injected. AT does **not** announce content added *simultaneously* with the region — so the toaster mounts one persistent live region at app start and injects toasts into it. (And one shared region, not a new one per toast.)
- **No focus steal** — the toast does not move focus (the Dialog opposite); the page stays where it is.
- **Auto-dismiss vs WCAG 2.2.1 (Timing Adjustable):** a timed auto-dismiss must give **enough time to read** (a minimum, scaled to content length — the rough heuristic ~5s + reading time), and must **pause on hover and on keyboard focus** (and not dismiss while hovered/focused). An **error or actionable toast should not auto-dismiss** (`duration: Infinity`). Auto-dismiss without these is a 2.2.1 failure.
- **The action-in-toast keyboard route (the hard problem):** because focus isn't moved to the toast, a keyboard/AT user can't easily reach an Undo button. The solutions: a **hotkey to jump to the toast region** (Radix's **F8**; React Aria exposes the region as a **focusable landmark**), and the discipline that **actionable toasts don't auto-dismiss** (so the action survives long enough to reach). If the action is important, prefer a persistent Banner/Inline message where the control is in the normal tab order.
- **Swipe + button alternative** — swipe-to-dismiss must have the **close Button** as a non-gesture alternative (WCAG 2.5.1/2.5.7 — the Drawer gesture rule).
- **Color-not-sole-carrier** — severity is conveyed by **icon + text**, not colour alone (SC 1.4.1).
- **WCAG SCs:** 4.1.3 (Status Messages — the live region, the headline), 2.2.1 (Timing Adjustable — auto-dismiss + pause), 1.4.1 (colour not alone), 2.5.1/2.5.7 (swipe alternative), 2.1.1 (keyboard — reach the action), plus the action/close Buttons' SCs.

## 7. Content guidelines
- **Concise and scannable** — a short confirmation ("Changes saved"); a toast is glanced at, not read.
- **No errors as toast** (the POV) — errors/validation go to persistent surfaces; if it must toast, it's persistent + `role=alert`.
- **The action label** is a clear verb ("Undo", "View", "Retry") — one action, not many.
- **Title vs message** — most toasts are a single line; a title + body only when the status needs both (and keep the title the announced essence).
- **The dismiss affordance** — a labelled "Dismiss"/close control; pair with (not replace by) swipe.

## 8. Motion and transition
Slide + fade in from the edge/corner (~150–250ms); the stack **reflows** as toasts enter/leave, and (Sonner's model) the stack is **collapsed by default and expands on hover** so multiples don't dominate. Swipe tracks the pointer and dismisses past a threshold. The **timeout/progress** may animate (a shrinking bar), and **pauses on hover/focus** (the visible counterpart of the 2.2.1 pause). Under `prefers-reduced-motion: reduce`, drop the slide/scale to a fade or snap, and keep the progress non-animated. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** — the corner placement and slide direction mirror (a top-right toaster moves to top-left; logical placement); the severity icon and action sit on the mirrored edges.
- **Text expansion** — toasts are short but expand (+30–50%); the surface must **wrap** (not truncate a status) and the **auto-dismiss duration must scale with the (translated) reading time** — a fixed timeout that suited English may be too short for German.
- **Localised** message + action label. (See 13-internationalization-and-rtl.)

## 10. Naming
**`Toast`** is the dominant name (Sonner, Radix, React Aria, Carbon "notification", Fluent, Base Web); **`Snackbar`** is Material's term for the single, bottom, ≤1-action variant; **`Flag`** is Atlassian's; **`Flash`** is Primer's (though Primer's Flash leans inline/banner); Ant splits **`message`** (brief, top-center) and **`notification`** (richer, corner). **The practice default: `Toast`** (the transient corner notification) managed by a **`Toaster`**/`ToastRegion` (the queue + live region), with the **`toast()` imperative API**, `Snackbar` as the bottom-single-action alias/variant, and the persistent message routed to **`Banner`/`Alert`**. Aliases to map: `Snackbar`, `Notification`, `Flag`, `Flash`, `message`.

## 11. Implementation notes
- **One `Toaster`/viewport owns the queue and the live region.** Mount a single `<Toaster>` at the app root; it renders a **persistent, empty ARIA live region** (so the pre-existing-region rule holds — §6) and a fixed-position viewport, and manages the queue/limit/stacking.
- **The imperative `toast()` store** — `toast()` pushes to a global store the `Toaster` subscribes to (Sonner's model), so any code can fire a toast without prop-drilling a context; `toast.promise()` wires loading→success/error on one toast id.
- **Duration + pause + actionable rule** — a default timeout scaled to content, **paused on hover/focus**, **`Infinity` for error/actionable** toasts; never dismiss while interacted with (2.2.1).
- **The keyboard route to the region** — a hotkey (Radix F8) or a focusable landmark (React Aria) so keyboard/AT users can reach an action; pair with not-auto-dismissing actionable toasts.
- **Swipe + the close Button** (the non-gesture alternative — 2.5.1/2.5.7).
- **Polite vs assertive + a single region** — default `role=status`/polite; assertive only for urgent; don't spawn a region per toast (AT chaos) — inject into the one shared region.
- **Don't hand-roll** — **Sonner** (the de facto React toast — stacked, promise, the store), **Radix `Toast`** (the headless reference — swipe, the F8 hotkey, duration/pause), or **React Aria** (the focusable `ToastRegion` landmark); skin them.

## 12. Related and alternative components
- **Stands on:** Button (the optional action + the close — see button), Icon (the severity glyph — see icon).
- **Alternative to / boundary with:** **Dialog** (the interrupting, focus-stealing, must-act opposite — see dialog), **Banner/Alert** (persistent, in-flow, important — the toast-vs-banner boundary; see banner when briefed), **Inline Message** (field/section validation — see inline-message when briefed), a **Notification Center** (a persistent inbox/log of past notifications, vs the transient toast), **Progress/Spinner** (a loading toast shades into progress feedback — see progress/spinner when briefed).
- **Establishes for the category:** the **ARIA live-region announcement pattern** (`role=status`/`alert`, the pre-existing region) that Banner/Alert, Inline Message, and Progress reuse.

(The first Feedback brief — the non-interrupting, transient, no-focus-steal counterpart to Dialog, establishing the live-region announcement pattern the rest of the category inherits. See dialog for the interrupting boundary, button for the action/close, icon for the severity glyph, banner/inline-message/progress when briefed for the siblings that reuse the live-region pattern. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **Sonner standardised the modern toast** — a stacked, collapse-by-default / expand-on-hover toaster with an imperative `toast()`/`toast.promise()` store became the de facto React pattern (over per-component context providers).
2. **The live-region + pre-existing-region rule hardened** — practice settled on one persistent live region the toaster injects into (role=status default, alert for urgent), killing the "announce nothing" bug of regions created with their content.
3. **The auto-dismiss-vs-WCAG correction** — pause-on-hover/focus, content-scaled minimums, and **actionable/error toasts that don't auto-dismiss** became table stakes (2.2.1).
4. **The keyboard-route-to-the-toast** (Radix F8 hotkey / React Aria focusable landmark) emerged as the answer to the action-in-toast reachability problem.
5. **No-error-toasts** gained ground — errors moved to persistent Banner/Inline surfaces (Polaris's long-standing POV).

## 14. Sources cited
(Conservative; reconcile with external.) **Sonner** (Emil Kowalski — the de facto React toast; stacked/expand-on-hover, `toast()`/`toast.promise()`) (2024–2026); **Radix UI** `Toast` (the headless reference — swipe, the F8 hotkey-to-region, duration + pause-on-interaction) (2024–2026); **Adobe Spectrum / React Aria** `Toast`/`ToastRegion` (the focusable-landmark approach) (2024–2026); **Google Material 3** Snackbar (bottom, single, ≤1 action) (2024–2026); **IBM Carbon** Notification (toast / inline / actionable) (2024–2026); **Shopify Polaris** `Toast` (minimal, bottom-center, the no-error-toasts POV) (2024–2026); **GitHub Primer** `Toast` / the inline `Flash` (2024–2026); **Atlassian** `Flag` (2024–2026); **Microsoft Fluent** Toast / MessageBar (2024–2026); **Base Web (Uber)** Toast / Snackbar (2024); **Ant Design** `message` / `notification` (2024–2026); **WAI-ARIA APG** — no formal toast pattern (the Alert pattern + live regions; the ongoing toast-pattern discussion); **Apple HIG** (2024–2026). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.3, 2.2.1, 1.4.1, 2.5.1, 2.5.7, 2.1.1.

## 15. Agent-consumable schema (conform to _schema.md in toast.md)
identity(Toast; aliases Snackbar/Notification/Flag/Flash/message; feedback; stable)/description(a brief NON-INTERRUPTING TRANSIENT notification at a screen edge that auto-dismisses and NEVER steals focus — the Dialog opposite; announced via an ARIA live region; opens the Feedback category + establishes the live-region pattern; NOT a Dialog (modal/must-act), NOT a Banner/Alert (persistent/in-flow), NOT an Inline Message (field/section), NOT a Notification Center (persistent log))/anatomy(toast viewport/region = the fixed-position queue owner AND the ARIA live region (must pre-exist; often a focusable landmark); toast surface; severity icon (aria-hidden, color-not-sole-carrier); title/message; optional action Button; dismiss/close Button (non-gesture alt to swipe); optional progress/timeout indicator)/api(inherits: button (action + close), icon (severity); IMPERATIVE toast() store (Sonner — toast()/.success/.error/.promise(loading,success,error)) vs declarative provider; severity info/success/warning/error(+loading); duration (Infinity/null = persistent for errors/actionable; scale with content); action {label,onClick}(+cancel); dismissible/onDismiss/onAutoClose; position corner/edge; queue/visibleToasts/limit; id/update for promise+dedupe)/states(entering/showing/PAUSED(hover/focus halts timeout)/exiting(+swiping); variants severity info/success/warning/error(+loading/promise), with-action/with-close/with-progress, snackbar(single,bottom,<=1 action) vs stacked corner toaster(expand-on-hover), persistent(Infinity) vs auto-dismiss)/accessibility(LIVE REGION — role=status/aria-live=polite (info/success) vs role=alert/assertive (error/critical); default polite; PRE-EXISTING-REGION TRAP — the region must already exist empty in the DOM before the toast injects (AT won't announce region+content added together) + ONE shared region not per-toast; NO FOCUS STEAL (Dialog opposite); AUTO-DISMISS vs WCAG 2.2.1 — enough time to read (min scaled to content ~5s+reading) + PAUSE-ON-HOVER/FOCUS + error/actionable should NOT auto-dismiss (Infinity); ACTION-IN-TOAST keyboard route — hotkey to region (Radix F8) / focusable landmark (React Aria) + actionable-doesnt-auto-dismiss + prefer persistent Banner if important; swipe + close-button alternative (2.5.1/2.5.7); color-not-sole-carrier (icon+text, 1.4.1); SC 4.1.3/2.2.1/1.4.1/2.5.1/2.5.7/2.1.1)/content(concise/scannable single line; NO errors-as-toast (errors persistent/inline; if must toast -> persistent role=alert); action label a clear verb (one action); title+body only when needed; labelled dismiss)/motion(slide+fade from edge ~150-250ms; stack reflow + collapse-by-default/expand-on-hover (Sonner); swipe tracks + threshold; timeout progress bar PAUSES on hover/focus; reduce-motion fade/snap)/i18n(RTL corner placement + slide direction mirror (logical); text expansion — WRAP not truncate + auto-dismiss DURATION must scale with translated reading time; localise message + action)/implementation(ONE Toaster/viewport owns the queue + a persistent empty live region (pre-existing rule) + fixed-position viewport; imperative toast() global store the Toaster subscribes to (no prop-drilling; toast.promise wires loading->success/error on one id); duration scaled + pause-on-hover/focus + Infinity for error/actionable; keyboard route — hotkey (Radix F8) / focusable landmark (React Aria); swipe + close button; default role=status/polite, assertive only urgent, single shared region; don't hand-roll — Sonner/Radix Toast/React Aria ToastRegion)/composition(stands-on button (action+close), icon (severity); alternative-to dialog (interrupting/must-act opposite), banner/alert (persistent/in-flow), inline-message (field/section), notification-center (persistent log), progress/spinner (loading toast); ESTABLISHES the live-region announcement pattern (role=status/alert + pre-existing region) for the Feedback category — Banner/Inline-Message/Progress reuse it)/notes(contested: polite-vs-assertive default; auto-dismiss duration + whether to auto-dismiss at all; errors-as-toast (Polaris bans; practice: errors persistent); actionable toasts (shouldn't auto-dismiss / reachability); queue stack-vs-collapse. trap: live region created WITH its content (announces nothing) — must pre-exist; auto-dismiss too fast / no pause (2.2.1 fail); action in an auto-dismissing toast the keyboard user can't reach; a region per toast; color-only severity; toast carrying essential info (transient, easy to miss). inherited: Button action+close; Icon severity. role-in-family: the first Feedback brief — the non-interrupting transient counterpart to Dialog; establishes the live-region pattern the category reuses. evolution: Sonner stacked model + toast() store; live-region + pre-existing-region hardened; auto-dismiss-vs-WCAG (pause/minimums/actionable) correction; keyboard-route-to-region; no-error-toasts. unverified: external 2026 version numbers; the live-region/2.2.1 specifics — verify against current AT behaviour.)

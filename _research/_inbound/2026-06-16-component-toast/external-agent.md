# Toast — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/toast.md`; version numbers, the no-formal-APG-pattern / native-`<toast>` Open-UI status, and the live-region/NVDA specifics flagged unverified. The two passes converged almost completely — no substantive disagreement; the external pass is unusually rich on the action-reachability strategies and the implementation traps.*

---

Field-Truth Study: The Feedback Category and the Toast Component Contract

## Identity
Nomenclature varies: "Toast" (Radix, React Aria, Polaris, Fluent v9, Base Web — from the toaster metaphor); "Snackbar" (Material 3 — bottom-edge, single-action, mobile-first); "Notification" (Carbon, toast variant); "Flag" (Atlassian); Ant splits "Message" (centered, simple) and "Notification" (corner, actionable). Underlying contracts are analogous: asynchronous system feedback that doesn't block the workflow.

## Description
The Toast opens the Feedback category — the functional opposite of the Dialog (modal/focus-trapping/halting vs transient/auto-dismissing/no-focus-steal). Boundaries: vs Dialog = interruption (a required acknowledgement/destructive confirm needs a Dialog); vs Banner/Alert = persistence + document flow (Banner is persistent in-flow, used for persistent errors / connection failures / corrective action — Polaris emphasises this); vs Inline Message = spatial context (inline sits near the field; toast is viewport-relative). Defining substance: reliance on ARIA live regions — announcing async updates without shifting focus — and the paradox of embedding interactive actions in a surface a keyboard user can't navigate to.

## Anatomy
Layered: Provider (ToastProvider/ToastQueue — app-root global state, queue, timeouts, swipe, limits); Viewport (ToastRegion — persistent fixed-position node portalled to body, owns the aria-live region / focusable landmark, often an <ol> in a region); Root (individual toast — layout, lifecycle, its auto-dismiss timer + hover/focus events). Sub-components: Severity Glyph (inherits Icon; color-not-sole-carrier, distinct shapes), Action + Close (inherit Button; Action = safe-to-ignore Undo/Retry, Dismiss = non-gesture fallback). Text: Title/Summary + optional Description/Detail.

## API
Diverges from declarative UI — a toast is dispatched, not rendered inline. Imperative dispatcher model (Fluent useToastController, React Aria ToastQueue, PrimeReact service): queue.add()/show()/close(key); add() returns a key for programmatic dismissal if the async op is canceled. React Aria's ToastQueue manages state outside React. Declarative alternative (Radix Toast.Root + open/onOpenChange) maps to local state but risks overlap/race/no-global-limit; developers wrap it in an imperative store. Core props: duration/timeout (min 5000ms consensus), placement/position, type/priority/politeness (maps severity to aria-live assertiveness), hotkey (Radix, e.g. ["F8"] to jump into the viewport).

## States
Fluent v9 documents: queued (in memory until visibility allows), visible, dismissed (hidden, mounted for exit), unmounted. Auto-dismiss vs WCAG 2.2.1 (Timing Adjustable) — static timeout is a violation (reading speeds vary). Pause-and-resume: timer halts on Hover (mouseenter on toast/viewport, resumes on mouseleave), Focus (keyboard focus enters), Blur (tab switch / window minimise / OS focus loss — must not deplete in the background). React Aria pauses all queue timers centrally; Radix listens to window blur/focus at the Viewport and broadcasts CustomEvents to nested Roots. Hard rule: actionable/error toasts should not auto-dismiss or need exponentially longer timeouts.

Stacking/queuing/limits: traditional Queue (FIFO, single toast — Material, early Carbon) — clean but info latency. Modern Stack (Radix, React Aria, Ant) — multiple in the DOM, max-visible limit (default ~3), older ones unmounted/queued/collapsed. Sonner (Emil Kowalski) formalised "stacked + expand-on-hover": absolute positioning, iterative scale (front scale(1), second 0.95, third 0.9) + Y-translate for depth; on hover, expands to a vertical list, computing each translateY via useMemo by summing preceding toast heights into a CSS variable.

## Variants
Placement: Bottom-Center (mobile standard, Material Snackbar, above nav bar/FAB, thumb reach); Top-Right/Bottom-Right (desktop, mimics macOS top-right / Windows bottom-right OS notifications). Safe-area: env(safe-area-inset-*) for notches/islands/keyboards/swipe bars. Severity (Info/Success/Warning/Error) with icon + structural CSS (color-not-sole-carrier). The Error controversy: Polaris — toasts should NEVER carry critical errors (auto-dismiss + no-focus-steal = user misses a failure); errors -> Banner/Inline. GitHub Primer — deprecated actionable + error toasts entirely after moderated usability testing with disabled users. MUI/PrimeReact/Fluent ship an Error variant but shift the sticky/infinite burden to the developer. Practitioner default: Polaris/Primer posture — restrict toasts to positive/informational; force errors into persistent layers.

## Accessibility
ARIA live-region: Info/Success -> role="status" + aria-live="polite" (finishes current speech first). Warning/Error -> role="alert" (implicit assertive, interrupts). The Pre-Existing Region Trap: injecting a role="status" div + its text simultaneously (common in declarative React) makes some AT — notably NVDA — ignore the update. The region must exist in the DOM before the text is modified. Radix renders an empty role="status" at app load, then delays text injection by one frame (a useNextFrame hook) to force a distinct mutation event.

Action-in-Toast Reachability: an Undo button portalled to the bottom of <body> while focus stays in (e.g.) a data table — no sequential tab path before the 5s timer expires. Contested strategies: Radix (F8 hotkey + SR-only altText — high cognitive burden); React Aria (focusable landmark, F6/Shift+F6, toast wrapped in alertdialog — good rotor integration); IBM Carbon (ActionableNotification — forces role="alertdialog" and MOVES focus into the notification on mount — guarantees reachability but breaks the non-interrupting contract); GitHub Primer (complete deprecation — "cannot be addressed with a sprinkling of ARIA" — use Banners); Apple HIG (explicit prohibition — refuses to document a generic toast; timed UI discouraged at OS level for switch/SR users).

Radix Visual-vs-Announcement Separation: an action inside role="alert" is announced as one confusing string ("File deleted Undo Close"). Radix severs the visual DOM from the a11y DOM: the visible toast gets aria-live="off"; a visually hidden element gets aria-live="assertive" + a developer-defined altText ("Notification: File deleted. Press Ctrl+Z to undo").

## Content
Extreme brevity — Polaris max ~3 words ("Product saved", "Connection restored"); Atlassian warns against multi-line wrapping, truncates aggressively. Factual outcome, no jargon/conversational phrasing; the severity icon carries the tone. Detailed/bulleted/nuanced content belongs in Inline Message or Dialog.

## Motion
Slide-in/Fade/Grow establish the spatial relationship without reflow. Swipe-to-dismiss: Radix exposes --radix-toast-swipe-move-x / -end-x for physics-bound gesture tracking (snaps back below threshold). WCAG 2.5.1 (Pointer Gestures) + 2.5.7 (Dragging Movements): swipe can't be the sole mechanism — a persistent Close Button (inherits Button) is the non-gesture alternative.

## i18n
Viewport positioned via fixed coords relative to edges — hardcoded directional props fail in RTL. Use logical properties: inset-inline-end (not right), inset-inline-start (not left), margin-inline-start. Entrance/exit motion must be bi-directionally aware — slide-in from the right in LTR mirrors to slide-in from the left in RTL, preserving the trailing-edge metaphor.

## Implementation
React Portals (createPortal to body / high-z-index root) to escape overflow:hidden / nested modals. Portal DOM-order mismatch: portals append as last child (oldest first, newest last) but the stack renders newest-on-top visually — disorienting for keyboard users. Radix deploys Focus Proxies (invisible <span> before/after the list): tabbing into the proxy redirects focus to the newest toast, and Radix intercepts keydown to reverse the native tab order to match the visual stack. Sonner Gap/Hover Bridging: expand-on-hover creates empty spatial gaps between DOM nodes; the cursor crossing them fires mouseleave -> premature collapse. Sonner injects a CSS :after pseudo-element bridging the gap so pointer hover stays continuous.

## Composition
Action Control (inherits Button) restricted to text/outline/ghost variants to preserve the compact footprint. The Notification Center paradigm (Fluent, Carbon): the Toast is the temporary flare; the same payload is pushed to a persistent aggregated list (Drawer/Sidebar/page), so users who miss the 5s window can access history — resolving transient-feedback vs permanent-record.

## Notes
WAI-ARIA APG lacks a formalised Toast pattern; Open UI / APG GitHub discussions are active and contested; developers use alert/alertdialog as imperfect stopgaps. notes.unverified: a native HTML primitive (hypothetically <popupdialog>/<toast>) is under Open UI conceptual brainstorming. The Paradigm Shift: a definitive retreat from actionable + error toasts (WCAG auditing; GitHub's ban); the opinionated default reserves Toasts for low-priority, non-actionable, positive/informational feedback — intervention/error/workflow modification needs a persistent Banner or an interrupting Dialog.

## Agent-consumable schema (external)

```yaml
component: toast
nomenclature: [Toast, Snackbar, Notification, Flag, Message]
opposite_of: Dialog (modal/focus-trapping vs transient/no-focus-steal)
anatomy: [Provider (queue/state), Viewport/ToastRegion (fixed, portalled, owns live region), Root (timer/lifecycle), SeverityGlyph (Icon), Action+Close (Button), Title, Description]
api:
  model: imperative dispatcher (queue.add() -> key; close(key)) preferred over declarative
  duration: { min: 5000ms, infinite_for: [error, actionable] }
  politeness: { info/success: "status/polite", warning/error: "alert/assertive" }
  hotkey: ["F8"]   # Radix, jump focus into viewport
accessibility:
  live_region_pre_existing: true   # region must exist before text injects (NVDA); Radix useNextFrame one-frame delay
  no_focus_steal: true
  auto_dismiss_2.2.1: pause on hover/focus/blur; actionable/error do not auto-dismiss
  action_reachability: [Radix F8 hotkey, React Aria focusable landmark+alertdialog, Carbon ActionableNotification (moves focus, breaks contract), Primer banned, Apple prohibits]
  visual_vs_announcement: visible toast aria-live=off + hidden assertive altText (Radix)
  swipe: needs non-gesture Close Button (2.5.1/2.5.7)
stacking: { model: stack, max_visible: 3, sonner: "scale+Y-translate, expand-on-hover via height-sum, ::after hover-bridge" }
implementation_traps:
  - pre-existing live region (NVDA)
  - portal DOM-order vs visual-stack mismatch -> focus proxies + tab reversal
  - sonner gap collapse -> ::after bridge
  - errors/actionable in transient toasts (retreat; use Banner)
content: { brevity: "~3 words (Polaris)", no_multiline: "Atlassian" }
i18n: { logical_properties: true, motion: bi-directional }
composition: { notification_center: "transient flare + persistent payload (Fluent/Carbon)" }
notes_unverified: "WAI-ARIA APG has no toast pattern; native <toast>/<popupdialog> under Open UI brainstorming"
```

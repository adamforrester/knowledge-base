---
okf_version: "0.1"
type: component-brief
title: Dialog (Modal)
description: THE focus-trap overlay primitive and the foundational Overlay brief — the counterpart to Menu's roving tabindex and Popover's light-dismiss. A field-truth study of the native <dialog>+showModal() platform-first decision (top layer, ::backdrop, Escape, background inertness — and the four gaps it still leaves: scroll-lock, light-dismiss, initial focus, animation), the focus-trap + initial-focus + focus-return contract (never auto-focus a destructive button; the lost-invoker edge case), role=dialog vs alertdialog, when to disable light-dismiss (data loss) and the native closedby attribute, scroll-lock + scrollbar-width compensation, and the @starting-style/allow-discrete/overlay exit-animation solution — with the practice's defaults.
tags: [components, overlay]
category: Overlay
status: stable
aliases: [modal, modal-dialog, alert-dialog, confirm-dialog]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Dialog (Modal)

> Dialog is the foundational focus-trap overlay primitive — the most aggressive intervention in a UI's flow: when modal, it opens over the page, makes everything behind it **inert**, and confines interaction to the elevated surface until the user resolves it. It is the counterpart the catalogue already named from the other side — Menu established that a menu uses roving tabindex and is *not* a focus trap ("that's Dialog"); Popover (the next brief) will own light-dismiss without trapping. Dialog owns the trap. Two decisions define a from-scratch implementation. First, the **native `<dialog>` + `showModal()` platform-first decision** (exactly like Accordion's native-`<details>`-first): `showModal()` grants the top layer (no z-index wars), the `::backdrop`, free Escape-to-close, focus-in, and background inertness — replacing the legacy `div` + portal + manual focus-trap + recursive `aria-hidden` stack. Native-first is the default — but the platform still leaves four gaps (scroll-lock + scrollbar compensation, light-dismiss/backdrop-click, nuanced initial focus, animation) that the headless libraries exist to fill. Second, the **focus-trap contract**: focus moves in, Tab/Shift+Tab cycle within, Escape closes, focus returns to the invoker.

---

## 1. Framing

A Dialog opens over the page and, when modal, blocks the background until resolved. It stands on **Button** (the footer confirm/cancel + the close-X — see button) and forward-references two overlay siblings: **Popover** (the next brief — light-dismiss, non-modal, anchored, *not* focus-trapped) and **Drawer** (the edge-anchored sheet).

**The defining contract is the focus trap.** On open, focus **moves into** the dialog; Tab/Shift+Tab **cycle within it** (the background is `inert` — unreachable to AT and pointer); Escape closes; on close, focus **returns to the invoker**. This is the explicit contrast with Menu (roving tabindex, Tab closes, *not* trapped) and Popover (light-dismiss, focus *not* trapped). Modality + the trap is what makes a Dialog a Dialog — not its size or its scrim.

What it *isn't*: a **Popover** (light-dismiss, non-modal, anchored to a trigger — see popover), a **Drawer/Sheet** (edge-anchored, often non-modal), a **Toast/Banner/Alert** (non-interrupting, no focus steal — see toast; banner when briefed), or an **inline expander** (Accordion/Disclosure — see accordion). Why systems disagree: native-vs-custom, initial-focus placement, when to disable light-dismiss, scroll-lock mechanics, footer button order, and the exit-animation approach.

## 2. Anatomy and parts

The field has converged on a **composable, slot-based** anatomy (Radix/Ariakit/React Aria) over the monolithic config-object modal — Carbon ships both (`Modal` simple, `ComposedModal` granular):

- **Root** — the state container (open/closed + context); usually no DOM.
- **Trigger** — the invoking control (a Button); carries `aria-haspopup="dialog"` + `aria-expanded` (auto-wired).
- **Portal / top layer** — the mechanism lifting the surface out of local stacking contexts (native top layer via `showModal()`, or a `ReactDOM.createPortal` to `document.body`).
- **backdrop / scrim** — the dimming layer (`::backdrop`); the light-dismiss click target (§5).
- **surface** — the panel; `role="dialog"`/`alertdialog` + `aria-modal`.
- **header** — the **title** (`<h2>`, the accessible name via `aria-labelledby`) + an optional **close button** (icon Button, "Close").
- **body** — the content, an `overflow-y:auto` region distinct from the fixed header/footer (scrolls when tall — §11).
- **footer** — the **action Buttons** (primary + secondary; inherits Button), order locale-sensitive (§9).

The practice default exposes `Dialog.Header`/`Dialog.Body`/`Dialog.Footer` (composable) with a simplified wrapper for the standard case — so split-pane or wizard layouts drop into the body slot without fighting internal CSS.

## 3. Properties / API

- **`open` / `defaultOpen` + `onOpenChange`** — controlled/uncontrolled; `onOpenChange` fires on any close attempt (Escape, backdrop) so external state can sync.
- **trigger composition** — `DialogTrigger`/`asChild` (Radix forwards refs + ARIA onto a real `<button>`; React Aria's `DialogTrigger` clones its child) — auto-wires `aria-expanded`/`aria-controls` so manual ARIA tagging (a frequent regression source) isn't needed.
- **`modal`** — modal (`showModal()`, background inert, focus trapped) vs non-modal/modeless (`show()`, background interactive); default modal (§4).
- **`size`** — sm / md / lg / full-screen (the mobile transform, §4).
- **dismissibility** — `closeOnEscape` (default true) + `closeOnOutsideClick`/`dismissible` (aliased `hideOnInteractOutside`/`preventCloseOnClickOutside`); **off for data-loss/required flows** (§5). **Map to the native `closedby` attribute** where supported (§11).
- **focus** — `initialFocus` (which element gets focus on open — *never* a destructive button), `finalFocus`/`restoreFocus` (return target; default the invoker), `trapFocus` (modal default true).
- **`role`** — `dialog` (default) vs `alertdialog` (confirmations/destructive — §4).
- **title/description wiring** — `aria-labelledby` (title) + `aria-describedby` (body), auto-wired by the headless lib.

## 4. States and variants

- **States:** closed / open / **animating** (the exit state is the historically hard one — §8) / **required** (a standard dialog *dynamically* disabling light-dismiss when it holds unsaved work — a backdrop click then triggers a confirm or a shake rather than closing).
- **Variants:**
  - **`dialog`** (standard) — forms, content, reading; allows light-dismiss; has a close-X.
  - **`alertdialog`** — urgent/destructive confirmations (delete account, revoke access): `role="alertdialog"`, **light-dismiss disabled**, **no close-X** (force an explicit choice), focus on the *safe* action.
  - **modal** vs **non-modal** — background inert vs. interactive.
  - **size** — sm/md/lg/**full-screen**.
  - **dismissible vs required** — close-X + light-dismiss vs. must-choose.
  - **mobile sheet** — below a breakpoint, the centered dialog **morphs into a bottom-sheet / full-screen sheet**; needs viewport-height compensation (`--visual-viewport-height` / dynamic-viewport units) so the software keyboard doesn't bury the footer actions.

## 5. Usage guidance

- **Use a modal Dialog** when the user must make an **immediate, blocking decision** before continuing: a destructive confirmation (→ `alertdialog`), a required form/step, or entering a small discrete set of data that needs context from the page behind it. Modality is justified when continuing without resolving would lose data or cause error.
- **Don't use a modal Dialog for:** non-critical info or transient feedback (→ Toast/Banner — see toast; banner when briefed), a small contextual overflow of actions/info anchored to a control (→ Popover/Menu — see popover, menu), edge-anchored secondary content or navigation (→ Drawer), deeply paginated/scrolling forms (→ a dedicated page route), or content that belongs inline (→ Accordion). **Modal overuse is the anti-pattern** — teams reach for dialogs to avoid proper routing; every modal steals focus and halts the user, so reserve it.
- **Decision frameworks:**
  - **Dialog vs. Popover:** does it **block** the page and demand resolution (modal Dialog, focus-trapped) or **supplement** a trigger and dismiss on outside-click (Popover, non-trapping)? Importance + modality, not size.
  - **Dialog vs. Drawer/Sheet:** centered + interrupting (Dialog) vs. edge-anchored + often-browsable-alongside, sometimes modeless pushing content (Drawer). On mobile a Dialog often *becomes* a bottom-sheet.
  - **Dialog vs. Toast/Alert:** must the user act now (Dialog) or is it passive, non-focus-stealing notification (Toast)?
  - **`alertdialog` vs `dialog`:** a destructive/interrupting confirmation is an `alertdialog`; a form/content modal is a `dialog`.
  - **When to disable light-dismiss:** if dismissing loses unsaved work, turn off backdrop-click (and consider confirm-on-Escape) so the user must choose.

## 6. Accessibility

A non-compliant dialog is among the most destructive a11y failures possible — it can permanently trap a keyboard/AT user or fail to announce that the context changed.

- **Roles:** `role="dialog"` (general) or `role="alertdialog"` (destructive/interrupting — the body is announced **assertively**, bypassing the queue; an alertdialog must contain at least one focusable control). Native `<dialog>` provides `dialog`; set `alertdialog` explicitly.
- **`aria-modal="true"`** on the surface + the background made **`inert`**. `showModal()` makes the background inert automatically; the legacy recursive-`aria-hidden`-the-world hack is superseded by the global `inert` attribute on the app root.
- **Labelling:** `aria-labelledby` → the title (accessible name), `aria-describedby` → the body — so the dialog announces its purpose on open.
- **The focus-trap + initial-focus + return contract (the defining mechanic):**
  - **On open:** focus moves into the dialog — to the **first focusable element**, a designated **`initialFocus`**, or (no interactive content) the **container/`<h2>`** with `tabindex="-1"`. **Never auto-focus a destructive/confirm button** — an `alertdialog` focuses the **Cancel/safe** action, so an accidental Enter/Space doesn't fire the destructive one.
  - **While open (modal):** Tab/Shift+Tab cycle within (React Aria's `FocusScope` is the reference boundary); the inert background is unreachable.
  - **Escape closes.**
  - **On close:** focus **returns to the invoker**; handle the **lost-invoker edge case** — when the invoker is unmounted while the dialog is open (e.g. a Menu item "Delete" that unmounts the Menu and opens an AlertDialog), focus must fall back to the nearest surviving logical trigger, not drop to `<body>` (React Aria keeps a `nodeToRestore` stack).
- **Scroll-lock:** the background must not scroll behind a modal; compensate for scrollbar width to avoid a layout jump (§11).
- **WCAG SCs:** 2.4.3 (focus order — trap + return), 2.1.2 (no keyboard trap — the modal trap is intentional but must be *escapable* via Escape), 4.1.2 (name/role/value), 1.4.13 / 2.4.11 (focus not obscured), 2.4.7 (focus visible), 1.3.1, plus the footer Buttons' SCs.

## 7. Content guidelines

- **Title** — a clear noun phrase or a direct question ("Delete repository?"), mapped to the invoking action; never generic ("Warning", "Are you sure?"). It's the accessible name.
- **Body** — ruthlessly concise (the user is blocked and the background is obscured); state the **consequence**, especially for destructive actions (what's lost, whether it's reversible).
- **Button labels — action-specific, never ambiguous.** The primary button echoes the title's verb ("Delete account", not "OK"/"Yes"/"Confirm"); cancel is explicit ("Cancel"/"Keep account"/"Go back"). A labelled action button is scannable and unambiguous out of context.
- **Destructive-confirm pattern** — `alertdialog`, the title names the action, the body names the consequence, focus lands on the safe choice, the destructive button carries the **danger token** beside a subdued/ghost cancel.
- **Close affordance** — a labelled "Close" icon button (top-trailing) for all *standard* dialogs (Atlassian lints this); **omit it for `alertdialog`/required** flows to force a decision.

## 8. Motion and transition

Entry is easy (opacity + `transform: scale(0.95→1)`, ~150–300ms, backdrop fade); **exit was the long-notorious problem** — CSS can't transition an element to `display:none`, so systems historically delayed unmount with JS transition groups (React Transition Group / Framer Motion). **The platform has now solved it** for top-layer elements with three primitives used together: **`@starting-style`** (the from-state for entry-from-`display:none`), **`transition-behavior: allow-discrete`** (animate discrete props — `display`, `overlay`), and the **`overlay`** property (keep the element in the top layer *during* the exit transition, so it doesn't drop behind other content mid-fade). Animate the `::backdrop` the same way. This retires the JS animation library for dialogs. The mobile sheet slides from the edge. Under `prefers-reduced-motion: reduce`, resolve instantly or use a subtle crossfade. **Platform-state** (per the external pass: `@starting-style`/`allow-discrete` Baseline ≈ Chrome 117+ / Safari 17.2+ / Firefox 129+) — verify; progressive-enhance. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL** mirrors the layout: the close button moves to the top-**leading** (left) edge, and the footer button order mirrors; logical properties handle most of it.
- **The footer button order is itself contested and locale/platform-sensitive:** Windows places confirm-left/cancel-right; macOS/iOS place cancel-left/confirm-right. Pick one system convention and apply it consistently (Carbon: primary always right; the practice default for web favours **primary-right**, matching the western forward-progression model), mirrored under RTL — or flip by detected OS to reduce friction.
- **Text expansion** — titles/body/buttons expand substantially (German/Arabic can run far longer); use **fluid heights**, no fixed widths, and let the **footer wrap from a horizontal row to a stacked column** when labels collide rather than clipping. (See 13-internationalization-and-rtl.)

## 10. Naming

**`Dialog`** (Radix, React Aria, Primer, Fluent, Material — the semantically correct term matching the APG nomenclature and the native element) and **`Modal`** (Carbon, Base Web) split the field; Atlassian hybridises ("Modal Dialog"); **`AlertDialog`** is near-universal for the confirmation/destructive variant (matching `role="alertdialog"`). **The practice default: `Dialog`** (the umbrella, mapping to `role="dialog"` and the native element) with **`AlertDialog`** as the confirmation variant, **`modal` as a prop** (not a separate `Modal` component — "modal" is a behaviour, not a component), and the trigger via `DialogTrigger`/`asChild`. Aliases to map: `Modal`, `ModalDialog`, `AlertDialog`, `ConfirmDialog`, `Sheet` (when it's the mobile/edge variant — but that leans Drawer).

## 11. Implementation notes

- **Native `<dialog>` + `showModal()` first** — the top layer (no z-index management), `::backdrop`, Escape, focus-in, and background inertness for free. Build on it and fill the gaps:
- **Scroll-lock + scrollbar compensation** — `showModal()` does *not* lock background scroll. `overflow:hidden` on the root works but, on OSes with persistent scrollbars (Windows), removing the ~15px scrollbar **shifts the whole page right**. `scrollbar-gutter: stable` is **insufficient** (doesn't fix sticky/fixed elements; adds unwanted gutters where scrollbars are overlaid). The robust fix: measure `window.innerWidth - document.documentElement.clientWidth`, set it as `--scrollbar-width`, apply it as `padding-right` to `<body>` (and fixed elements), then `overflow:hidden`; restore on close. `react-remove-scroll`'s **sidecar pattern** ensures stacked dialogs compute the compensation **once** (no compounding double-gap).
- **Light-dismiss (backdrop click)** — native `<dialog>` doesn't close on backdrop click by default. The new **`closedby` attribute** formalises it at the platform level: `closedby="any"` (Escape + buttons + backdrop), `closedby="closerequest"` (Escape + buttons, **no** backdrop), `closedby="none"` (explicit close only). Map the semantic `dismissible` prop to `closedby` where supported; JS-fallback otherwise. **The backdrop-click trap:** because a native `<dialog>` fills its content box, a click on the `::backdrop` registers as a click on the dialog element — and a user who selects text inside and drags out fires a spurious dismiss on mouseup. Guard it by tracking **`mousedown`** and closing only when the press *originated* on the backdrop (`event.target === event.currentTarget`), not on mouseup after a drag.
- **Initial focus + return** — override native focus to a designated element when needed (never a destructive button); return to the invoker with the lost-invoker fallback (§6).
- **Nested / stacked dialogs are discouraged** (a dialog opening a dialog is a design smell — combine steps or use a wizard) but sometimes required (OAuth, extensions). The native **top layer auto-stacks** — the most-recent `showModal()` sits on top and Escape dismisses only the topmost — which collapses what used to be fragile z-index juggling.
- **The exit animation** — wire `@starting-style` + `allow-discrete` + `overlay` (§8).
- **Don't hand-roll the trap** — Radix `Dialog`/`AlertDialog`, React Aria `Dialog`/`useDialog`/`Modal` (`FocusScope`), or Ariakit handle focus-trap, scroll-lock, `inert`, labelling, and dismissal, increasingly delegating to the native element + top layer; skin them.

## 12. Related and alternative components

- **Stands on:** Button (footer confirm/cancel + the close-X — see button), Icon (the close glyph — see icon).
- **Alternative to / boundary with:** **Popover** (the next brief — light-dismiss, non-modal, anchored, *not* focus-trapped; the importance/modality boundary — see popover), **Drawer/Sheet** (edge-anchored; centered-modal vs edge — see drawer; a modal drawer is a Dialog at the edge, and the mobile bottom-sheet *is* a Drawer), **Toast/Banner/Alert** (non-interrupting, no focus steal — see toast; banner when briefed), **Menu** (roving tabindex, not a trap — see menu), **Accordion/Disclosure** (inline expansion, not an overlay — see accordion).
- **Specialises into:** `AlertDialog` (the confirmation/destructive pattern); the mobile bottom-sheet (shades into Drawer).
- **Composed by:** any flow needing a blocking sub-task — destructive confirms, required forms, focus-demanding wizards.

(The foundational focus-trap overlay primitive, and the trap counterpart to Menu's roving tabindex and Popover's light-dismiss. The first true Overlay primitive defined on its own terms — Menu was the application-command overlay that *uses* this family's machinery; Dialog defines modality + the trap, Popover [next] defines light-dismiss + anchoring, and together they are the substrate Select/Combobox/Menu's positioning + dismissal inherit. See button for the controls, menu for the roving-vs-trap boundary, popover for the light-dismiss sibling, accordion for the platform-first precedent. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **The Z-Index Era → the Portal Era → the Platform-First Era.** Early modals used `position:absolute; z-index:9999` (broke whenever a parent created a stacking context via `transform`/`opacity`/`filter`); the field moved to **portals** (`createPortal` to `document.body`) to escape that, at the cost of manual focus-trap + recursive `aria-hidden` + global Escape listeners; the field is now **gutting portal logic for the native `<dialog>` + top layer**.
2. **`inert` replaced the recursive-`aria-hidden`-the-world hack** for background inertness.
3. **`@starting-style` + `allow-discrete` + `overlay` solved the exit-animation problem** — top-layer elements can finally animate *out* before `display:none`, retiring the JS animation library (cross-brief platform-state — verify).
4. **The `closedby` attribute** is formalising light-dismiss at the platform level (emerging baseline).
5. **The modal-overuse correction** — practice hardened against modals for non-critical info/feedback; toasts, inline messages, popovers, and drawers took the load.

## 14. Sources cited

(Conservative; the external pass cited Radix v1.x, React Aria/Spectrum, Carbon v11/v12, Fluent v9, plus platform baselines `@starting-style`/`allow-discrete` ≈ Chrome 117+/Safari 17.2+/Firefox 129+ and the emerging `closedby` — all held loosely and flagged unverified; `last-audited` is the re-run trigger.)

- **WAI-ARIA APG** — Modal Dialog pattern + Alert Dialog pattern (focus-trap, initial-focus, Escape, `aria-modal`, labelling) (2024–2026).
- **Native HTML `<dialog>`** + `showModal()`/`show()`, the top layer, `::backdrop`, `inert`, `@starting-style`/`transition-behavior: allow-discrete`/`overlay`, the `closedby` attribute (MDN / platform, 2024–2026, current-platform-state).
- **Radix UI** `Dialog`/`AlertDialog` (the headless reference; `asChild`, focus-trap, scroll-lock) (2024–2026).
- **Adobe Spectrum / React Aria** `Dialog`/`Modal`/`DialogTrigger`, `useDialog`, `FocusScope`, the `nodeToRestore` lost-invoker handling (2024–2026).
- **IBM Carbon** `Modal`/`ComposedModal`, the danger modal, responsive 2x-grid sizing, primary-action-right (2024–2026).
- **Ariakit** `Dialog` (`hideOnInteractOutside`, the modeless `modal={false}`) (2024–2026).
- **Shopify Polaris** `Modal`; **GitHub Primer** `Dialog`; **Atlassian** `Modal Dialog` (the close-button lint); **Microsoft Fluent** `Dialog` (v9); **Base Web (Uber)** `Modal`; **Google Material 3** Dialog (basic / full-screen) + bottom sheets; **Apple HIG** sheets / alerts / action sheets (2024–2026).
- `react-remove-scroll` (the scroll-lock sidecar pattern). WCAG 2.2 (W3C Recommendation, Oct 2023) — 2.4.3, 2.1.2, 4.1.2, 1.4.13, 2.4.11, 2.4.7, 1.3.1.

## 15. Agent-consumable schema

```yaml
identity:
  id: dialog
  name: Dialog
  aliases: [modal, modal-dialog, alert-dialog, confirm-dialog]
  category: overlay
  status: stable
description: >
  THE focus-trap overlay primitive — a surface over the page that (when
  modal) makes the background inert until resolved. Native <dialog> +
  showModal() first (top layer, ::backdrop, Escape, background inertness).
  Owns the trap Menu pointed at; NOT a popover (light-dismiss, non-trapping),
  NOT a drawer (edge-anchored), NOT a toast (non-interrupting). Modality +
  the trap define it, not size or scrim.
anatomy:
  parts:
    - "Root (state container; usually no DOM)"
    - "Trigger (a Button; aria-haspopup=dialog + aria-expanded, auto-wired)"
    - "Portal / top layer (showModal() top layer, or createPortal to body)"
    - "backdrop/scrim (::backdrop; light-dismiss click target)"
    - "surface (role=dialog|alertdialog + aria-modal)"
    - "header: <h2> title (aria-labelledby) + close button (icon Button 'Close')"
    - "body (overflow-y:auto, distinct from fixed header/footer)"
    - "footer: action Buttons (primary + secondary; inherits button; locale-ordered)"
api:
  inherits: button   # footer confirm/cancel + close-X
  props:
    - {name: open, type: boolean, description: controlled visibility}
    - {name: defaultOpen, type: boolean, description: uncontrolled initial}
    - {name: onOpenChange, type: function, description: "fires on any close attempt (Escape/backdrop) for state sync"}
    - {name: trigger, type: "DialogTrigger/asChild", description: "auto-wires aria-expanded/controls (avoid manual ARIA — regression source)"}
    - {name: modal, type: boolean, default: true, description: "showModal (inert+trapped) vs show (modeless, interactive bg)"}
    - {name: size, type: enum, values: [sm, md, lg, full], description: surface max-width / mobile transform}
    - {name: closeOnEscape, type: boolean, default: true}
    - {name: dismissible/closeOnOutsideClick, type: boolean, description: "backdrop-click close; OFF for data-loss; aliases hideOnInteractOutside/preventCloseOnClickOutside; map to native closedby"}
    - {name: initialFocus, type: ref, description: "focus target on open — NEVER a destructive button"}
    - {name: finalFocus/restoreFocus, type: ref, default: invoker}
    - {name: role, type: enum, values: [dialog, alertdialog]}
  wiring: "aria-labelledby (title) + aria-describedby (body) auto-wired"
states:
  runtime: [closed, open, "animating (exit is the hard one)", "required (standard dialog dynamically disabling light-dismiss when it holds unsaved work)"]
variants:
  dialog: "standard — forms/content; light-dismiss; close-X"
  alertdialog: "role=alertdialog; destructive/urgent; light-dismiss DISABLED; NO close-X; focus on safe action"
  modal-vs-non-modal: "background inert vs interactive"
  size: [sm, md, lg, full-screen]
  dismissible-vs-required: "close-X + light-dismiss vs must-choose"
  mobile-sheet: "below breakpoint morphs to bottom-sheet/full-screen; needs --visual-viewport-height for the software keyboard"
accessibility:
  wcag-criteria: ["2.4.3", "2.1.2", "4.1.2", "1.4.13", "2.4.11", "2.4.7", "1.3.1"]
  roles: "dialog (general) | alertdialog (destructive — assertive body, needs a focusable control)"
  inertness: "aria-modal=true + background inert (showModal auto; global inert attr replaces recursive aria-hidden hack)"
  labelling: "aria-labelledby title + aria-describedby body"
  focus-trap: "focus moves IN (first focusable / initialFocus / container+tabindex=-1; NEVER a destructive button — alertdialog focuses Cancel); Tab/Shift+Tab cycle within (FocusScope); Escape closes; focus RETURNS to invoker"
  lost-invoker: "if invoker unmounted while open (Menu item -> AlertDialog), fall back to nearest surviving trigger, not <body> (nodeToRestore stack)"
  scroll-lock: "background must not scroll; compensate scrollbar width"
content:
  title: "clear noun/question ('Delete repository?'), mapped to the action; never 'Warning'/'Are you sure?' — it's the accessible name"
  body: "concise; state the consequence (what's lost, reversibility)"
  buttons: "ACTION-SPECIFIC echoing the title verb ('Delete account') NOT OK/Yes/Confirm; explicit Cancel"
  destructive: "alertdialog + danger primary beside subdued/ghost cancel; focus on safe choice"
  close: "labelled 'Close' icon for standard dialogs (Atlassian lints); OMIT for alertdialog/required"
motion:
  entry: "opacity + scale(0.95->1) ~150-300ms + backdrop fade"
  exit: "SOLVED natively: @starting-style (from-state) + transition-behavior: allow-discrete (animate display/overlay) + overlay property (stay in top layer during exit); animate ::backdrop the same; retires the JS animation lib"
  mobile-sheet: "slide from edge"
  reduce-motion: "resolve instantly / subtle crossfade"
  platform-state: "@starting-style/allow-discrete Baseline ~Chrome 117+/Safari 17.2+/Firefox 129+ (verify)"
i18n:
  rtl: "close button to top-leading (left); footer order mirrors"
  footer-order: "contested/locale-sensitive (Windows confirm-left vs macOS cancel-left/confirm-right); pick one (practice default primary-RIGHT, Carbon-aligned), mirror under RTL"
  expansion: "titles/body/buttons expand a lot; fluid heights, no fixed widths; footer WRAPS row->stacked column rather than clipping"
implementation:
  - "native <dialog>+showModal() FIRST = top layer (no z-index) + ::backdrop + Escape + focus-in + background-inert free"
  - "scroll-lock: scrollbar-gutter:stable is INSUFFICIENT; measure window.innerWidth - documentElement.clientWidth -> --scrollbar-width as padding-right on body+fixed els, then overflow:hidden; react-remove-scroll SIDECAR computes once for stacked dialogs (no double-gap)"
  - "light-dismiss: native closedby attr (any | closerequest [no backdrop] | none); map dismissible prop to it; JS-fallback. Backdrop-click TRAP: click on ::backdrop registers as click on the dialog; text-drag-out fires spurious dismiss on mouseup -> track MOUSEDOWN, close only if press originated on backdrop (target===currentTarget)"
  - "initial focus override (never destructive); return to invoker w/ lost-invoker fallback"
  - "nested/stacked dialogs DISCOURAGED but native top layer auto-stacks (most-recent showModal on top; Escape dismisses topmost) — collapses z-index juggling"
  - "exit animation: @starting-style + allow-discrete + overlay (see motion)"
  - "don't hand-roll — Radix/React Aria(FocusScope)/Ariakit, increasingly on the native element"
composition:
  stands-on: [button, icon]
  alternative-to: [popover (light-dismiss boundary), drawer/sheet (edge), toast/banner (non-interrupting), menu (roving, not a trap), accordion (inline)]
  specialises-into: [alertdialog, mobile-bottom-sheet]
  role-in-family: "first true Overlay primitive on its own terms — Dialog=modality+trap, Popover=light-dismiss+anchor; together the substrate select/combobox/menu inherit"
notes:
  contested:
    - "native-vs-custom (native-first, but the 4 gaps keep the headless libs)"
    - "initial-focus placement"
    - "when to disable light-dismiss (data-loss)"
    - "footer button order (Windows vs macOS; practice default primary-right)"
    - "modal vs non-modal"
  trap:
    - "modal overuse (every modal steals focus + halts the user)"
    - "auto-focusing a destructive button"
    - "forgetting focus-return / the lost-invoker -> <body> drop"
    - "scroll-lock scrollbar layout-shift (needs measured padding compensation)"
    - "backdrop-click spurious dismiss on text-drag-out (track mousedown)"
    - "nested dialogs"
  inherited: "Button footer + close-X"
  evolution: "z-index -> portal -> platform-first (native <dialog>+top layer); inert replaced aria-hidden-world; @starting-style/allow-discrete/overlay solved exit animation; closedby formalising light-dismiss; modal-overuse correction"
  unverified:
    - "external-supplied 2026 version numbers (Radix v1.x, Carbon v11/12, Fluent v9, etc.)"
    - "platform-state baselines (@starting-style/allow-discrete ~Chrome 117+/Safari 17.2+/Firefox 129+; closedby emerging) — cross-brief, shared with the overlay family"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-dialog/` (16 June 2026), the foundational focus-trap Overlay primitive — the trap counterpart to Menu's roving tabindex and the modal counterpart to Popover's light-dismiss. The two passes converged almost completely — the native-`<dialog>`+`showModal()`-first decision (top layer, `::backdrop`, Escape, background inertness) and the four gaps it leaves (scroll-lock + scrollbar compensation, light-dismiss/backdrop-click, initial-focus nuance, animation), the focus-trap + initial-focus + focus-return contract (never auto-focus a destructive button; the lost-invoker `<body>`-drop edge case), the `role=dialog`-vs-`alertdialog` boundary, the when-to-disable-light-dismiss (data-loss) decision, scroll-lock + scrollbar-width compensation, the `@starting-style`/`allow-discrete`/`overlay` exit-animation solution, the modal-overuse anti-pattern, action-specific button labels, and `Dialog` (+ `AlertDialog`, `modal` as a prop) as the naming default. External-pass contributions folded in: the native **`closedby`** attribute (`any`/`closerequest`/`none`) formalising light-dismiss, the **mousedown backdrop-click trap** (text-drag-out spurious dismiss), the scrollbar JS measurement + the **`react-remove-scroll` sidecar** (since `scrollbar-gutter: stable` is insufficient), the **top-layer auto-stacking** for the discouraged-but-sometimes-required nested case, the `nodeToRestore` lost-invoker handling, the dynamic **required** state, the mobile-sheet `--visual-viewport-height` keyboard compensation, the footer-button-order Windows-vs-macOS detail, and the concrete platform baselines. Claude-pass contributions: the framing as the first true Overlay primitive defined on its own terms (Dialog=modality+trap, Popover=light-dismiss+anchor), the trap-vs-roving-vs-light-dismiss triangulation across Menu/Popover, and the platform-first-precedent tie to Accordion. The 2026 version numbers and the platform-state baselines (shared with the overlay family) are flagged unverified. Conformant to `components/_schema.md`. The second Overlay brief after Menu; Popover is next, and together they formalise the positioning + dismissal substrate Select/Combobox/Menu already inherit.*

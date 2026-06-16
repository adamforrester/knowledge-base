# Dialog (Modal) — field-truth study (Claude pass)

## 1. Framing
A Dialog is a surface that opens **over** the page, demands attention, and (when modal) makes everything behind it **inert** until the user deals with it. It is THE focus-trap overlay primitive — the counterpart the catalogue already named from the other side: Menu established that a menu uses roving tabindex and is *not* a focus trap ("that's Dialog"). Dialog owns the trap. It stands on **Button** (the footer confirm/cancel + the close control — see button) and forward-references two overlay siblings: **Popover** (the next brief — the light-dismiss, *non-trapping* overlay) and **Drawer** (the edge-anchored sheet).

**The two defining decisions:**
- **The native `<dialog>` + `showModal()` platform-first decision** (the headline, exactly like Accordion's native-`<details>`-first): `showModal()` gives the **top layer** (no z-index wars), the **`::backdrop`** pseudo-element, **free Escape-to-close**, automatic focus-in/return, and **inertness of the background** — replacing the legacy custom `div` + portal + manual focus-trap + `aria-modal` stack. The practice default is **native-first**. But the native element does *not* solve everything — scroll-lock, light-dismiss (backdrop-click-to-close), nuanced initial focus, and animation still need work (§11).
- **The focus-trap contract:** on open, focus **moves into** the dialog; Tab/Shift+Tab **cycle within it** (background inert); Escape closes; on close, focus **returns to the invoker**. This is the explicit contrast with Menu (roving, Tab closes, not trapped) and Popover (light-dismiss, focus not trapped).

What it *isn't*: a **Popover** (light-dismiss, non-modal, anchored — see popover), a **Drawer/Sheet** (edge-anchored, often non-modal), a **Toast/Alert** (non-interrupting, no focus steal — see toast/banner when briefed), or an **inline expander** (Accordion/Disclosure). Why systems disagree: native-vs-custom, initial-focus placement, when to disable light-dismiss, scroll-lock mechanics, and the exit-animation approach.

## 2. Anatomy and parts
- **backdrop / scrim** — the dimming layer behind the surface (native `::backdrop`); click target for light-dismiss (§5).
- **dialog surface** — the centered panel (top layer); `role="dialog"`/`alertdialog`, `aria-modal`, labelled by the title.
- **header** — the **title** (the accessible name via `aria-labelledby`) + an optional **close button** (an icon Button with accessible name "Close").
- **body** — the content, **scrollable** when tall (sticky header/footer, the body scrolls — §11).
- **footer** — the **action Buttons** (confirm/cancel; primary + secondary — inherits Button); right-aligned (or locale-flipped — §9).
- (Optional **description** wired via `aria-describedby`.)

## 3. Properties / API
- **`open` / `defaultOpen` + `onOpenChange`** — controlled/uncontrolled; the trigger composition (`DialogTrigger`/`asChild`, Radix-style) or imperative open.
- **`modal`** — modal (`showModal()`, background inert) vs non-modal/modeless (`show()`); default modal (§4).
- **`size`** — sm / md / lg / full-screen (the mobile transform, §4).
- **dismissibility:** `closeOnEscape` (default true) + `closeOnOutsideClick`/`dismissable` (default true) — **disabled for data-loss/required flows** (§5).
- **focus:** `initialFocus` (which element gets focus on open — *not* a destructive button), `finalFocus`/`restoreFocus` (where focus returns; default the invoker), `trapFocus` (modal default true).
- **`role`** — `dialog` (default) vs `alertdialog` (confirmations/destructive — §4).
- **title/description wiring** — `aria-labelledby` (title) + `aria-describedby` (body/description), auto-wired by the headless lib.

## 4. States and variants
- **States:** closed / open / **animating** (entering/exiting — the exit state is the hard one, §8).
- **Variants:**
  - **`dialog`** (default) — general modal content/forms.
  - **`alertdialog`** — confirmations, destructive actions, interrupting messages: focus the safest action, assertive announcement, minimal/required content (often no close-X, must choose).
  - **modal** vs **non-modal** — background inert vs. background still interactive.
  - **size** — sm/md/lg/**full-screen** (mobile or immersive flows).
  - **dismissible vs required** — has a close-X + light-dismiss vs. must make a choice (no close affordance, light-dismiss off).
  - **mobile sheet** — a Dialog that renders as a bottom-sheet / full-screen sheet on small viewports (the Drawer boundary, §5).

## 5. Usage guidance
- **Use a modal Dialog** when the task **must interrupt** and demands a focused decision/sub-task before continuing: a destructive confirmation, a required form/step, critical information that blocks. Modality is justified when continuing without resolving would lose data or cause error.
- **Don't use a modal Dialog for:** non-critical info or transient feedback (→ Toast/Banner — see toast/banner when briefed), a small contextual overflow of actions or info anchored to a control (→ Popover/Menu — see popover, menu), edge-anchored secondary content or navigation (→ Drawer), or content that belongs inline (→ Accordion/expander, or just the page). **Modal overuse is the anti-pattern** — every modal steals focus and blocks the user; reserve it.
- **Decision frameworks:**
  - **Dialog vs. Popover:** does it **block** the page and demand resolution (modal Dialog, focus-trapped) or **supplement** a trigger and dismiss on outside-click (Popover, non-trapping)? Importance + modality, not size.
  - **Dialog vs. Drawer/Sheet:** centered + interrupting (Dialog) vs. edge-anchored + often-browsable-alongside (Drawer); on mobile a Dialog often *becomes* a bottom-sheet.
  - **Dialog vs. Toast/Alert:** must the user act now (Dialog) or is it passive notification (Toast — no focus steal)?
  - **`alertdialog` vs `dialog`:** a confirmation/destructive interruption is an `alertdialog`; a form/content modal is a `dialog`.
  - **When to disable light-dismiss:** if dismissing loses unsaved work or interrupts a critical flow, turn off backdrop-click (and consider confirm-on-Escape) so the user must choose explicitly.

## 6. Accessibility
- **Roles:** `role="dialog"` (general) or `role="alertdialog"` (confirmations/destructive — the body is the assertive message; the alertdialog must contain at least one focusable control). Native `<dialog>` provides `dialog`; `alertdialog` is set explicitly.
- **`aria-modal="true"`** on the surface (custom path) + the background made **`inert`** so AT and pointer/focus can't reach it. Native `showModal()` handles background inertness automatically; the legacy `aria-hidden`-everything-else hack is superseded by `inert`.
- **Labelling:** `aria-labelledby` → the title (the accessible name) and `aria-describedby` → the body/description so the dialog is announced with its purpose on open.
- **The focus-trap + initial-focus + return contract (the defining a11y mechanic):**
  - **On open:** focus moves into the dialog — to the **first focusable element**, a **designated `initialFocus` element**, or the **dialog container/heading** if there's no obvious control. **Never auto-focus a destructive/confirm button** (an accidental Enter/Space could fire it).
  - **While open (modal):** Tab/Shift+Tab cycle *within* the dialog; the inert background is unreachable.
  - **Escape closes** (native gives this free).
  - **On close:** focus **returns to the invoking element**; handle the **invoker-removed** edge case (fall back to a sensible nearby element / the body landmark).
- **Scroll-lock:** the background must not scroll behind a modal; compensate for the **scrollbar-width** to avoid a layout jump (§11).
- **WCAG SCs:** 2.4.3 (focus order — trap + return), 2.1.2 (no keyboard trap — *escapable* via Escape; the modal trap is intentional but must be exitable), 4.1.2 (name/role/value), 1.4.13 / 2.4.11 (focus not obscured), 2.4.7 (focus visible), 1.3.1, plus the footer Buttons' SCs.

## 7. Content guidelines
- **Title** — a clear noun or a direct question ("Delete 3 files?"), not "Are you sure?"; it's the accessible name, so make it specific.
- **Body** — concise; state the consequence (especially for destructive actions: what's lost, whether it's reversible).
- **Button labels — action-specific, not generic.** "Delete" / "Discard changes" / "Save", not "OK"/"Yes" (a labelled action button is scannable and unambiguous out of context). The destructive action carries the danger token *and* an explicit verb; pair it with a clearly-safe cancel.
- **Destructive-confirm pattern** — `alertdialog`, the title names the action, the body names the consequence, focus lands on the *safe* choice, the destructive button is explicit and danger-styled.
- **Close affordance** — a labelled "Close" icon button (top-trailing); omit it for required choices (force a decision).

## 8. Motion and transition
Entry: the surface scales (~0.95→1) + fades in (~150–200ms) while the backdrop fades; exit reverses. **The long-notorious exit-animation problem** — you can't transition an element to `display:none` (the close just snaps) — is now solved natively with **`@starting-style`** (entry-from styles), **`transition-behavior: allow-discrete`** (animate discrete properties like `display`/`overlay`), and animating the **`overlay`** + **`::backdrop`** so the top-layer element animates out before removal. The mobile bottom-sheet slides up/down from the edge. Under `prefers-reduced-motion: reduce`, drop scale/translate and use a quick opacity fade or snap. (Date these platform features — verify support; progressive-enhance. See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** flips the layout: the close button moves to the top-leading (left) edge, and the **footer action-button order mirrors** (the primary action's side follows the locale's reading direction). Logical properties handle most of it.
- **Footer button order** is itself a contested/locale-sensitive question (primary-first vs primary-last differs by platform convention — macOS vs Windows); pick one system convention and apply it consistently, mirrored under RTL.
- **Text expansion** — titles, body, and especially button labels expand (+30–50%); don't fix dialog or button widths; let the dialog size to content within min/max bounds. (See 13-internationalization-and-rtl.)

## 10. Naming
**`Dialog`** (Radix, React Aria, Primer, Fluent, Material) and **`Modal`** (Carbon, Polaris, Atlassian, Base Web) split the field roughly evenly; **`AlertDialog`** is the near-universal name for the confirmation/destructive variant (matching `role="alertdialog"`). **The practice default: `Dialog`** (the umbrella, mapping to `role="dialog"` and the native element) with **`AlertDialog`** as the confirmation variant, `modal` as a prop (not a separate `Modal` component), and the trigger via `DialogTrigger`/`asChild`. Aliases to map: `Modal`, `ModalDialog`, `AlertDialog`, `ConfirmDialog`, `Sheet` (when it's the mobile/edge variant — but that leans Drawer).

## 11. Implementation notes
- **Native `<dialog>` + `showModal()` first** — it provides the top layer (no z-index management), `::backdrop`, Escape-to-close, focus-in, and background inertness for free. Use it as the base and layer the gaps.
- **What native still doesn't solve (the gaps to fill):**
  - **Scroll-lock** — `showModal()` does *not* lock background scroll; lock it (`overflow:hidden` on the root) **and compensate for the scrollbar width** (pad the root by the removed scrollbar's width, or use `scrollbar-gutter: stable`) to avoid a horizontal layout jump.
  - **Light-dismiss (backdrop click)** — native `<dialog>` does *not* close on backdrop click by default; implement it (detect clicks on the `::backdrop`/outside the surface) and make it **opt-out for data-loss flows**.
  - **Initial focus nuance** — native focuses the first focusable (or the dialog); override to a designated element when needed, and ensure it's never a destructive button.
  - **Focus return edge cases** — return to the invoker; handle the invoker being removed.
  - **Animation** — wire `@starting-style` + `allow-discrete` (above).
- **The `inert` attribute** (custom path) on everything outside the dialog is the modern replacement for the `aria-hidden`-the-world hack.
- **Nested / stacked dialogs are discouraged** — a dialog opening another dialog is a design smell (combine steps, or use a wizard); if unavoidable, the top layer stacks them but focus/return management compounds.
- **Don't hand-roll the trap** — Radix `Dialog`/`AlertDialog`, React Aria `Dialog`/`useDialog`/`Modal`, or Ariakit handle focus-trap, scroll-lock, `inert`, labelling, and dismissal; skin them. (They increasingly delegate to the native element + top layer.)

## 12. Related and alternative components
- **Stands on:** Button (footer confirm/cancel + the close-X — see button), Icon (the close glyph — see icon).
- **Alternative to / boundary with:** **Popover** (the next brief — light-dismiss, non-modal, anchored, *not* focus-trapped; the importance/modality boundary — see popover), **Drawer/Sheet** (edge-anchored; centered-modal vs edge — see drawer when briefed), **Toast/Banner/Alert** (non-interrupting notification, no focus steal — see toast/banner when briefed), **Accordion/Disclosure** (inline expansion, not an overlay — see accordion).
- **Specialises into:** `AlertDialog` (the confirmation/destructive pattern); the mobile bottom-sheet (shades into Drawer).
- **Composed by:** any flow needing a blocking sub-task — destructive confirms, required forms, focus-demanding wizards.

(The foundational focus-trap overlay primitive, and the trap counterpart to Menu's roving tabindex and Popover's light-dismiss. The first true Overlay primitive (Menu was the application-command overlay that *uses* this family's machinery); Dialog defines modality + the trap, Popover [next] defines light-dismiss + anchoring, and together they are the substrate Select/Combobox/Menu's positioning + dismissal inherit. See button for the controls, menu for the roving-vs-trap boundary, popover for the light-dismiss sibling, accordion for the platform-first precedent. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **Native `<dialog>` + `showModal()` adoption** — the top layer (no z-index wars), `::backdrop`, Escape, and background inertness moved into the platform; headless libs increasingly build on it rather than re-implementing the portal + manual trap.
2. **`inert` replaced the `aria-hidden`-the-world hack** for background inertness.
3. **`@starting-style` + `allow-discrete` + `overlay` solved the exit-animation problem** — you can finally animate a top-layer element *out* before `display:none` (cross-brief platform-state — verify).
4. **The modal-overuse correction** — design practice hardened against modals for non-critical info/feedback (toasts, inline messages, popovers, drawers took the load).
5. **`scrollbar-gutter: stable`** simplified the scroll-lock layout-jump compensation.

## 14. Sources cited
(Conservative; reconcile with external.) **WAI-ARIA APG** — Modal Dialog pattern + Alert Dialog pattern (the focus-trap, initial-focus, Escape, `aria-modal`, labelling rules); the **native HTML `<dialog>`** element + `showModal()`/`show()`, the top layer, `::backdrop`, `inert`, `@starting-style`/`transition-behavior: allow-discrete`/`overlay` (MDN / platform, 2024–2026, current-platform-state); **Radix UI** `Dialog`/`AlertDialog` (the headless reference; controlled open, `asChild` trigger, focus-trap, scroll-lock) (2024–2026); **Adobe Spectrum / React Aria** `Dialog`/`Modal`/`DialogTrigger`, `useDialog` (2024–2026); **IBM Carbon** `Modal`/`ComposedModal`, the danger modal (2024–2026); **Shopify Polaris** `Modal` (2024–2026); **GitHub Primer** `Dialog` (2024–2026); **Atlassian** `Modal Dialog` (2024–2026); **Microsoft Fluent** `Dialog` (2024–2026); **Ariakit** `Dialog` (2024–2026); **Base Web (Uber)** `Modal` (2024); **Google Material 3** Dialog (basic / full-screen) + bottom sheets (2024–2026); **Apple HIG** sheets / alerts / action sheets (2024–2026). WCAG 2.2 (Oct 2023) — 2.4.3, 2.1.2, 4.1.2, 1.4.13, 2.4.11, 2.4.7, 1.3.1.

## 15. Agent-consumable schema (conform to _schema.md in dialog.md)
identity(Dialog; aliases Modal/ModalDialog/AlertDialog/ConfirmDialog; overlay; stable)/description(THE focus-trap overlay primitive — a surface over the page that (when modal) makes the background inert until resolved; native <dialog>+showModal() first; NOT a popover (light-dismiss, non-trapping), NOT a drawer (edge-anchored), NOT a toast (non-interrupting); owns the trap Menu pointed at)/anatomy(backdrop/::backdrop scrim; surface role=dialog|alertdialog + aria-modal; header=title (aria-labelledby) + close button (icon Button 'Close'); scrollable body (aria-describedby); footer action Buttons)/api(inherits: button (footer + close); open/defaultOpen+onOpenChange; trigger DialogTrigger/asChild; modal vs non-modal (showModal vs show); size sm/md/lg/full; closeOnEscape(true)/closeOnOutsideClick(true) — OFF for data-loss; initialFocus (NOT a destructive button)/finalFocus-restoreFocus (invoker)/trapFocus; role dialog|alertdialog; aria-labelledby+describedby auto-wired)/states(closed/open/animating (exit is the hard one); variants dialog/alertdialog, modal/non-modal, size sm-md-lg-fullscreen, dismissible/required, mobile-sheet)/accessibility(role=dialog|alertdialog (alertdialog needs a focusable control + assertive body); aria-modal=true + background inert (native showModal auto; inert replaces aria-hidden-world); aria-labelledby title + aria-describedby body; FOCUS-TRAP CONTRACT — focus moves in (first focusable / initialFocus / container, NEVER a destructive button), Tab cycles within, Escape closes, focus RETURNS to invoker (handle invoker-removed); scroll-lock; SC 2.4.3/2.1.2 (escapable trap)/4.1.2/1.4.13/2.4.11/2.4.7/1.3.1)/content(title = clear noun/question not 'Are you sure?'; body states the consequence; buttons ACTION-SPECIFIC ('Delete'/'Discard') not OK/Yes; destructive-confirm = alertdialog + danger button + focus on safe choice; labelled Close, omitted for required choices)/motion(entry scale 0.95->1 + fade ~150-200ms + backdrop fade; EXIT-ANIMATION PROBLEM solved by @starting-style + transition-behavior:allow-discrete + animating overlay/::backdrop; mobile sheet slide; reduce-motion drops scale)/i18n(RTL: close to top-leading + footer button order mirrors; footer-button-order is locale/platform-sensitive — pick one convention; text expansion no fixed widths)/implementation(native <dialog>+showModal() FIRST = top layer + ::backdrop + Escape + focus + background-inert free; what native does NOT solve — scroll-lock (+ scrollbar-width compensation / scrollbar-gutter:stable), light-dismiss/backdrop-click (opt-out for data-loss), initial-focus nuance, focus-return edge, animation; inert on background (custom path); nested/stacked dialogs discouraged; don't hand-roll — Radix/React Aria/Ariakit, increasingly built on the native element)/composition(stands-on button + icon; alternative-to popover (light-dismiss boundary), drawer/sheet (edge), toast/banner (non-interrupting), accordion (inline); specialises-into alertdialog + mobile bottom-sheet; the first true Overlay primitive — Dialog=modality+trap, Popover=light-dismiss+anchor; together the substrate select/combobox/menu inherit)/notes(contested: native-vs-custom (native-first); initial-focus placement; when to disable light-dismiss (data-loss); footer button order; modal vs non-modal. trap: modal overuse (every modal steals focus); auto-focusing a destructive button; forgetting focus-return / scroll-lock scrollbar-jump; nested dialogs. inherited: Button footer + close. evolution: native <dialog>/showModal adoption; inert replaced aria-hidden-world; @starting-style/allow-discrete/overlay solved exit animation; modal-overuse correction; scrollbar-gutter:stable. unverified: external 2026 version numbers; the platform-state features (top layer/::backdrop/@starting-style/allow-discrete/inert/overlay support — cross-brief, shared with the overlay family).)

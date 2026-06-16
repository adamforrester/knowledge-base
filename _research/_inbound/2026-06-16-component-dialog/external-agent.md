# Dialog (Modal) — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/dialog.md`; version numbers and the platform-state baselines flagged unverified. The two passes converged almost completely — no substantive disagreement.*

---

The Dialog (Modal) Component: Field-Truth Architecture and Implementation

## Framing
The Dialog (aliased Modal) is the most aggressive intervention in a UI's flow — the foundational focus-trap overlay primitive. It demands resolution, halts background context, and constrains interaction to the elevated surface. Its defining contract: an uncompromising focus trap. Menu uses roving tabindex and is NOT a trap; Popover uses light-dismiss and doesn't hijack focus scope; Dialog owns the trap (Tab/Shift+Tab cycle within, background inert).

The fundamental decision is the native <dialog> element + .showModal(): the Top Layer (bypasses z-index warfare), the ::backdrop pseudo-element, automatic centering, free Escape, built-in background inertness — vs the legacy custom div+portal+aria-hidden+focus-trap-react stack. Native-first is the default. But native does NOT resolve: complex scroll-locking (scrollbar layout shift), sophisticated initial focus, reliable light-dismiss, and historically the exit animation. So Radix/React Aria/Ariakit wrap/enhance/polyfill the native element. A leading system outputs a managed lifecycle leveraging the Top Layer while smoothing the gaps.

## Anatomy and parts
Composable slot-based architecture (Radix/Ariakit/React Aria); Carbon offers monolithic Modal + ComposedModal. Parts: Root (state container, often no DOM); Trigger (Button; aria-haspopup="dialog" + aria-expanded); Portal (Top Layer or document root); Backdrop/Scrim (::backdrop or fixed div catching light-dismiss); Surface/Content (the <dialog>, role=dialog|alertdialog); Header/Title (<h2>, aria-labelledby); Body (overflow-y:auto, distinct from fixed header/footer); Footer Actions (Buttons); Close Button (icon Button, linted by Atlassian). Practice default: composable sub-components (Dialog.Header/Body/Footer) + a simplified wrapper.

## Properties / API
Controlled (open) / uncontrolled (defaultOpen) + onOpenChange (fires on Escape/backdrop). modal boolean (false = modeless: no backdrop, no trap, page interactive — Ariakit/Fluent). size enum (sm/md/lg/full; Carbon scales on a 2x grid). dismissible (aliased hideOnInteractOutside in Ariakit / preventCloseOnClickOutside in Carbon). Trigger: Radix asChild forwards refs/ARIA to a native button; React Aria DialogTrigger clones its child injecting aria-expanded/controls. Auto-wiring avoids manual-ARIA regressions.

Platform evolution: the HTML closedby attribute formalizes light-dismiss. closedby="any" (Escape + buttons + backdrop); closedby="closerequest" (Escape + buttons, NO backdrop); closedby="none" (explicit only). Map semantic dismissible props to closedby where supported; JS fallback for legacy.

## States and variants
Standard Dialog vs Alert Dialog (Radix/React Aria AlertDialog, Carbon danger modal): standard = forms/reading, light-dismiss, close-X. alertdialog = urgent/destructive (delete account, revoke access), role="alertdialog", light-dismiss DISABLED, NO close-X — forces explicit choice. "Required" state: a standard dialog with unsaved data dynamically disables light-dismiss; a backdrop click triggers a confirm prompt or shake. Sizing + mobile: below a breakpoint the centered dialog morphs into a bottom Sheet / full-screen (Material 3 Expressive, Apple HIG); needs --visual-viewport-height to handle the software keyboard so the footer stays visible.

## Usage guidance
Modal warranted only for an immediate blocking decision before continuing: destructive action (AlertDialog), or small discrete data entry needing page context. Never: primary navigation (Drawer/Popover), deeply paginated/scrolling forms (page route), non-interrupting feedback (Toast/inline Alert). Dialog vs Popover: focus + context (Popover transient, light-dismiss, no trap; Dialog demands completion). Dialog vs Drawer: reference data (Drawer can be modeless, pushing content). The modal-overuse anti-pattern: teams use dialogs to avoid proper routing.

## Accessibility
Focus-trap contract: identify focusable elements; Tab loops last->first, Shift+Tab first->last (React Aria FocusScope). Initial focus: forcefully into the dialog, default first focusable; AlertDialog exception — NEVER on a destructive/confirm action (focus Cancel); no interactive elements -> container/<h2> with tabindex="-1". Focus restoration + lost-invoker: return to the invoker; if it was unmounted while open (Menu "Delete File" unmounts Menu + mounts AlertDialog), focus must not reset to document.body — React Aria keeps a nodeToRestore stack. role=dialog vs alertdialog (assertive announcement). Background hidden via native showModal inertness or global inert on #root (replaces recursive aria-hidden). Accessible name via aria-labelledby (title), aria-describedby (body).

## Content guidelines
Title = clear noun/question ("Delete Repository?"), mapped to the action, not "Warning". Body = concise consequences. Buttons never "Yes"/"No"/"OK" — primary echoes the title verb ("Delete Account"); cancel explicit ("Cancel"/"Keep Account"). Destructive = danger variant primary + subdued/ghost cancel. Atlassian lints (use-modal-dialog-close-button) that non-alert dialogs provide a visible "X".

## Motion and transition
Entry easy (opacity + transform: scale). Exit historically hard (can't transition to display:none) — forced JS transition groups. Solved natively with @starting-style + transition-behavior: allow-discrete + the overlay property (keeps the dialog in the Top Layer during exit so it doesn't drop behind stacked elements mid-fade). Animate ::backdrop the same way. [CSS example provided: dialog transition with display/overlay allow-discrete, @starting-style for dialog[open] and ::backdrop.] Respect prefers-reduced-motion (instant / crossfade).

## Internationalization
Text expansion up to 300% (German/Arabic) — fluid heights, footers wrap row->stacked column. RTL: close button top-right -> top-left; icon inline positions swap. Footer button order contested: Windows = Confirm left / Cancel right; macOS/iOS = Cancel left / Confirm right. Decide: force one brand paradigm (Carbon = primary always right) or flip by detected OS. Web default increasingly primary-right (western forward-progression).

## Naming
Dialog (semantically correct, APG + native) vs Modal (adjective for a behavior). Radix/React Aria/Primer/Fluent/Material = Dialog; Carbon/Base Web = Modal; Atlassian = Modal Dialog. Practice default: Dialog (matches platform), modal as a prop, the interruption variant explicitly AlertDialog.

## Implementation notes
Scroll lock + layout shift: overflow:hidden on body removes the ~15px scrollbar on Windows -> page shifts right. scrollbar-gutter: stable is insufficient (doesn't fix fixed/sticky elements; adds gutters on overlay-scrollbar OSes). Fix: measure window.innerWidth - document.documentElement.clientWidth, apply as --scrollbar-width padding-right on body + fixed els, set overflow:hidden; remove on close. react-remove-scroll's sidecar ensures stacked dialogs compute once (no double-gap). Backdrop click: native <dialog> fills its content box so a ::backdrop click registers on the dialog; text-drag-out fires a click on mouseup -> accidental dismiss. Track mousedown, close only if target===currentTarget. Stacking multiple modals discouraged but needed for OAuth/extensions; native Top Layer auto-stacks (most-recent showModal on top; Escape dismisses topmost).

## Related and alternative components
Popover (light-dismiss, no scrim, no trap — transient contextual). Drawer/Sheet (edge-anchored, often modeless, push not obscure). Menu (roving tabindex + arrows, not a trap). Toast/Alert (background, assertive but never steals focus).

## Field POV evolution
Z-Index Era (z-index:9999, broke on stacking contexts) -> Portal Era (createPortal to body, manual focus-trap + aria-hidden + Escape) -> Platform-First Era (native <dialog> + Top Layer; systems gutting div-portal logic) -> Animation Resolution (@starting-style + discrete transitions remove the last barrier; discard JS animation libs).

## Platform State and Framework Versions
Native <dialog> universally saturated. Top Layer animation (@starting-style + allow-discrete) Baseline: Chrome 117+, Safari 17.2+, Firefox 129+. closedby emerging Baseline (modern Chromium + Safari; JS polyfill for legacy). Systems: Radix UI v1.x, React Aria (Adobe Spectrum), IBM Carbon v11/v12, Microsoft Fluent UI v9, Atlassian, Shopify Polaris, W3C ARIA APG.

## Agent-consumable schema

```yaml
identity:
  name: Dialog
  aliases:
  description: A focus-trapping overlay that halts the primary application flow to demand immediate user interaction or provide critical information.
  role: dialog
anatomy:
  - {name: Root, type: provider}
  - {name: Trigger, type: node, note: 'aria-haspopup="dialog" + aria-expanded'}
  - {name: Portal, type: boundary, note: Top Layer / document root}
  - {name: Backdrop, type: visual, note: '::backdrop or fixed div'}
  - {name: Surface, type: container, note: 'role=dialog|alertdialog'}
  - {name: Header, type: section, note: '<h2> aria-labelledby'}
  - {name: CloseButton, type: control, inherits: Button}
  - {name: Body, type: section, note: 'overflow-y scrollable'}
  - {name: Footer, type: section, note: localized flex-order}
  - {name: FooterActions, type: control, inherits: Button}
api:
  props:
    open: {type: boolean}
    defaultOpen: {type: boolean}
    onOpenChange: {type: function}
    modal: {type: boolean, default: true}
    size: {type: 'enum [sm, md, lg, full]'}
    dismissible: {type: boolean, note: maps to native closedby}
    initialFocus: {type: ref}
states: [open, closed, 'required (disables light-dismiss for unsaved data)']
variants:
  - 'standard: role=dialog, light dismiss, close button'
  - 'alertdialog: role=alertdialog, no light dismiss, no close button, forces resolution'
  - 'sheet: mobile bottom-anchored transform'
accessibility:
  focus_trap: true
  initial_focus: First interactive element (Standard) or Cancel (AlertDialog)
  return_focus: Invoking element (nodeToRestore fallback if unmounted)
  aria: {modal: true, labelledby: Header title ID, describedby: Body ID}
  keyboard: {Escape: closes if dismissible, Tab: cycles, Shift+Tab: cycles backward}
motion:
  entry: scale 0.95->1, opacity 0->1
  exit: scale 1->0.95, opacity 1->0
  css_features: ['@starting-style', 'transition-behavior: allow-discrete', 'overlay property']
implementation:
  platform_first: true
  element: HTML <dialog> + showModal()
  scroll_lock: Calculate --scrollbar-width via JS, padding-right to body, overflow hidden
  backdrop_click: mousedown target check (or closedby="any")
```

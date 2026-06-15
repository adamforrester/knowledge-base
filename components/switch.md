---
okf_version: "0.1"
type: component-brief
title: Switch
description: The control that closes the selection-control decomposition arc — no group. A field-truth study of the immediate-effect contract (the staged-vs-immediate boundary from the switch side), the async/optimistic-update model (optimistic default + a first-class pending/loading lock), the role=switch-vs-checkbox-vs-aria-pressed distinction, the label-side decision, read-only support, and describe-the-setting labels, with the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [toggle, toggle-switch, on-off]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Switch

> Switch closes the boolean/choice arc, and it closes it by *subtracting*. Checkbox set the selection-control decomposition (control + optional group + atomic primitive); Radio made the group mandatory; **Switch removes the group entirely.** A switch is independent by definition — it is never one of a mutually-related set, so there is no `SwitchGroup`, no shared value, no group validation. Both research passes confirmed the no-group refinement without hesitation. What's left to resolve is the substance behind one word — *immediate*: a switch applies its change the instant you flip it, and everything contested about the component (the async model, the ARIA role, the motion, even the label) follows from taking that seriously.

---

## 1. Framing

A Switch is a control for a binary on/off **setting that takes effect immediately** — no save, no submit; the flip *is* the input and the execution command (both agents; the external pass calls it the "immediate effect contract"). That contract is the **topological boundary** with Checkbox: if a Save/Submit button is anywhere in the flow, the change is staged and it's a Checkbox; if the change is live the instant you toggle, it's a Switch. (Stated here from the switch side; the inverse of checkbox §5.)

What it *isn't*: a **staged** binary submitted with a form (Checkbox), an **action or view-mode** with pressed state (ToggleButton, `aria-pressed`), or a **one-of-two exclusive labelled choice** (Radio/Segmented). The switch is **mobile-origin** (the iOS toggle), which is why the platform references matter more than usual and why Apple HIG enforces the immediate-effect boundary hard — famously rejecting App Store submissions that use switches for staged form config (external).

Why systems disagree — and why this earned a dual-agent pass: the **async/optimistic-update problem** (what "immediate" means when the effect is a fallible network call — §3, §11), the **ARIA contract** (`role="switch"` vs checkbox vs `aria-pressed`), whether **read-only** is even coherent for a toggle (§4), the **label side**, and the **on/off affordance**. A telling framing point: data-heavy admin systems like Polaris have historically *debated or rejected* a switch altogether, on the grounds that continuous immediate mutation is incongruous with review-then-commit dashboard workflows (external) — which is itself the strongest statement of the immediate-effect boundary.

## 2. Anatomy and parts

Inherits the Checkbox decomposition (control + atomic primitive, and the nesting POV — see checkbox §2) **minus the group**. Parts: the **track** (the pill/rail), the **thumb** (the sliding knob), the **label**, an optional **description**, optional **track content** (a checkmark or I/O icons for secondary, non-colour state indication), and a **hidden native input** (`<input type="checkbox" role="switch">`) anchoring events, focus, and the a11y tree. The atomic **`Switch.Control`** is the nestable unit — a settings row or list row embeds it and supplies the label + hit target (the canonical iOS settings-row composition).

**The no-group refinement — the arc's final move, and an intentional confirmation, not an omission.** There is no `SwitchGroup`. A "settings panel" of switches (Email / SMS / Push) is a *List of rows* (layout), not a selection group: each switch triggers its own distinct, instant mutation and owns its own independent boolean. Shipping a `SwitchGroup` would actively *invite* the anti-pattern of using switches to compile a multi-select array — which is Checkbox's job (external is emphatic). So: **Checkbox has an optional group, Radio a mandatory one, Switch none** — and that completes the decomposition.

## 3. Properties / API

Inherits the form-field substrate and the checkbox row shape (rich-content label, description, disabled, whole-row hit target, native `checked` naming — see checkbox §3). Switch-specific:

- `checked` + `defaultChecked` / `onChange` — the binary; **`onChange` is expected to apply the effect immediately** (§1). (Material 3 Web's `selected` is the naming outlier; the practice uses native `checked`.)
- `label` + `description` — rich content. **`labelPosition` is the switch divergence:** switches live in settings rows where the **label leads and the control trails** (label left, control at the row's trailing/right edge) — the opposite of checkbox/radio (control leads). The practice exposes `labelPosition` (`leading`/`trailing`) and lands on **label-leading for the settings-row habitat** (control at the trailing edge, where the eye expects the toggle), flipping to **control-leading when a switch sits inline among other form controls** for sibling alignment. (The external pass defaulted the other way — control-leading for sibling consistency — which is equally defensible; the call is context-driven, so the prop is the real answer and the default follows the dominant use.)
- **The async/pending contract — the load-bearing switch-specific API, and where both passes converged after starting apart.** Two field stances: *optimistic-only* (toggle instantly; the host reverts `checked` and toasts on failure — Carbon, Base Web) vs. *explicit locking* (a first-class `loading`/`busy` prop that intercepts input, swaps the thumb for a spinner, and announces pending — Primer's `loading` + `loadingLabel`/`loadingLabelDelay`, Atlassian's `busy`). **The practice ships both: optimistic-by-default** (immediacy is the whole point) **with revert-on-error + a message, *and* a first-class `loading`/`pending` prop** for high-latency or critical-path toggles where an inconsistent intermediate is genuinely harmful and locking is safer. Mandating optimism universally puts too much orchestration burden on consumers; mandating locking kills the immediacy — so expose the choice, default to optimistic.
- **No `indeterminate`** — `role="switch"` doesn't support `aria-checked="mixed"` (it's coerced to false); a switch is uncompromisingly binary (§6). A switch is essentially never `required` (an on/off setting with a default isn't a required field).
- **`isReadOnly`** — supported (§4). **on/off affordance** — `showStateLabel`/icons, off by default (§4, §7).

## 4. States and variants

| State | Switch-specific contract |
| --- | --- |
| on / off | the binary; thumb position + stark track-colour contrast |
| hover / focus-visible / pressed | focus ring on the **track**, never the thumb, ≥3:1; pressed may stretch the thumb along the travel axis |
| disabled | non-interactive, removed from tab order, muted (contrast waived, 1.4.3) |
| **loading / pending** | first-class here — track locked, thumb swapped/overlaid with a spinner, `aria-busy`; the state that exists *because* immediacy meets latency (§3) |
| **error** | an optimistic update failed — revert the thumb, error-colour the track, link a message via `aria-describedby`; this is *outcome* error (the toggle didn't take), not validation error |
| **read-only** | supported — see below |

No indeterminate. **Read-only — adopted, against my first instinct, on the external pass's argument.** It looks paradoxical (an un-toggleable toggle), but enterprise dashboards genuinely need it: users review permission sets and system config they lack authority to change, and dropping those from the tab order (disabling) or swapping to static text destroys data-table consistency and hides the setting from screen readers (Spectrum, Carbon). So the practice **supports `readOnly`**: `aria-readonly="true"`, **focusable and in the tab order**, **full WCAG contrast** (legible, unlike disabled), visually distinct from disabled (e.g. a lock affordance, suppressed hover halo). The no-clean-native-readonly caveat from checkbox/select still applies — implement via `aria-readonly` + prevented toggle.

**Intentional variants:** `size` (small/medium — switches rarely warrant a large); **label-side** (leading/trailing, §3); **on/off affordance** (plain track / inner-track check / I/O icons). The on-affordance is the contested visual: the practice defaults to a **plain track where thumb position + colour carry the state**, adding icons only where state legibility demands — and **never hardcoding "On"/"Off" text adjacent to the label** (§7).

## 5. Usage guidance

- **Use** for a binary on/off **setting that applies immediately** — notifications, dark mode, Wi-Fi, feature flags in a settings panel.
- **Don't use** for: a binary **submitted with a form** (→ Checkbox — the Save-button tell); a **single consent/agree** (→ Checkbox); an **action or toolbar view-toggle** (→ ToggleButton, `aria-pressed`); a **one-of-two exclusive labelled choice** ("Card"/"Bank") or where the "off" state is ambiguous (→ Radio/Segmented); or anything needing a **third/indeterminate** state (→ Checkbox).
- **The progressive-disclosure trap** (external): if toggling the switch *reveals a sub-form that must be filled before the data is valid*, the switch is doing progressive disclosure, not an immediate mutation — that's a Checkbox. This is the most common real misuse.
- **Decision frameworks:**
  - **Switch vs. Checkbox is immediate-vs-staged** — the single most important call, the boundary both prior briefs lean on. If a submit button commits the change, it's a Checkbox. (The external pass's blunt version: *if a submit button is required anywhere in the flow, it's not a switch.*)
  - **Switch vs. ToggleButton is setting-vs-action** — a switch sets *state* (`role=switch`/`aria-checked`); a toggle button performs an *action/mode* (`role=button`/`aria-pressed`), e.g. Bold or Grid/List view. (See button §12.)
  - **Consequential/destructive toggles** — pair with confirmation, or use Checkbox + explicit Save; a switch's immediacy is wrong for costly or hard-to-reverse changes.
  - **Don't switch where the result isn't observable** — immediacy is the contract; if the user can't perceive the effect, reconsider.

## 6. Accessibility

Inherits the substrate (label association, whole-row hit target, focus contrast — see checkbox §6). Switch-specific, and the ARIA role is the headline:

- **`role="switch"` + `aria-checked` (true/false)**, and the distinction from siblings is the whole game: **checkbox** is `role="checkbox"` (announced "checked/unchecked"), **switch** is `role="switch"` (announced **"on/off"**), and a **toggle button** is `role="button"` + `aria-pressed` (announced "pressed"). Putting `aria-pressed` on a switch — a recurring, severe error — corrupts the announcement and violates the spec. Native `<input type="checkbox" role="switch">` is the baseline; `role="switch"` is well-supported in modern AT but newer than checkbox, so verify on the matrix and keep a checkbox fallback as the conservative hedge.
- **State must not be colour-only** — the **thumb position** must distinguish on/off (1.4.1); track colour alone fails colour-blind users. Inner-track icons or a state label help but aren't required if position is clear; hardcoded adjacent "On/Off" text is *not* the fix (it's redundant — §7).
- **Keyboard:** each switch is its **own tab stop** (like checkbox, unlike radio); **Space toggles** (Space is the canonical W3C activation; some systems also accept Enter since the effect is action-like — a defensible addition, Space is the safe default).
- **Announce the immediate effect:** `aria-checked` flips on toggle (announced); for an async effect, `aria-busy` during flight + a polite announcement of the outcome/error so a screen-reader user knows the live change took or failed (4.1.3); and if toggling **changes the page layout** (reveals a sub-form), an `aria-live` region announces the contextual change (external).
- **Implementation traps** (external): the **IA2 quirk** — both `aria-pressed` buttons and `role=switch` map internally to `IA2_ROLE_TOGGLE_BUTTON`, but author to the ARIA spec (`aria-checked` for switches) regardless; and **shadow-DOM label detachment** — wrapping a web-component switch (`<md-switch>`) in a native `<label>` does *not* associate the name with the input inside the shadow DOM, so set `aria-label`/`aria-labelledby` explicitly or ship an unlabelled control.
- **WCAG SCs:** 4.1.2 (role/checked — the switch role doing the work), 1.4.1 (not colour-only), 1.4.11/2.4.13 (focus + the off-state track must be distinguishable from the background), 2.5.8 (target), 4.1.3 (status message for async outcome/error).

## 7. Content guidelines

- **The label names the *setting*, not the state, and not the action** — "Airplane Mode" / "Location Services", **not** "Airplane Mode is On" and **not** "Turn on Airplane Mode". The on/off is carried by the control and the "on/off" announcement; the label is a stable noun/adjective phrase that **does not change on toggle** (a label that flips "Enable"/"Disable" is disorienting — a common bug).
- **Avoid verbs** (they blur "current state" vs "action on click") and **mandate positive framing** (the on state is the affirmative, so "off" never means a double negative).
- **Reject hardcoded adjacent "On"/"Off" text** — it competes with the track state and produces duplicative SR output ("Airplane Mode On, switch, on") — Apple HIG and Carbon both advise against it (external).
- **Error copy** (async failure): say what didn't happen and that it reverted ("Couldn't turn on notifications. Try again."), near the control — a status message more than a validation error.

## 8. Motion and transition

Motion here is **functional, not decorative** — the thumb slide is the literal *receipt* that the immediate action registered (external). The **thumb slides** across the track (~150–200ms, ease-in-out) with a synchronised track-colour crossfade originating from the thumb. For the optimistic-async case, the thumb **snaps optimistically** to the new state and a spinner cross-fades onto its surface for the pending resolution; on failure, the thumb **slides back** (a physical metaphor for rejection) with an error-colour flash and a toast so the reversal isn't mysterious. Under `prefers-reduced-motion: reduce`, **drop the slide and snap** (0ms); a track-colour crossfade may remain if it stays under flashing thresholds. Don't over-spring it — a bouncy switch reads as toy-like in a settings context; and translate the thumb (`transform`), never animate width/layout. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL inverts both the layout and the travel direction:** the label-leading row mirrors (control to the left in RTL), and the **thumb travel flips** — "on" sits at the inline-end, so in LTR on is right and the thumb slides right, in RTL on is left and it slides left, with the track fill originating accordingly. Use logical properties so this is automatic.
- **Text expansion** (German/Russian, up to ~300%) — the row wraps the label rather than crushing the fixed-width track; another reason to **avoid on/off track text** (it doesn't localise/expand cleanly).
- Inherits checkbox i18n otherwise; no text input, so IME is moot. (See 13-internationalization-and-rtl.)

## 10. Naming

The field splits three ways: **`Switch`** (Spectrum/React Aria, Material, Fluent, Base Web, Polaris) vs. **`Toggle`** (Carbon, Atlassian) vs. **`ToggleSwitch`** (Primer). **The practice default is `Switch`** — it maps directly to `role="switch"`, and "Toggle" is an ambiguous verb that collides with toggle *button*, accordion toggling, and generic state swaps. The atomic primitive is **`Switch.Control`**. Aliases to map in docs search: `Toggle`, `ToggleSwitch`, `On/Off`. **Document that there is no `SwitchGroup`** so consumers don't reach for one (a settings list is a List of rows — §2).

## 11. Implementation notes

- **Optimistic update + revert is the core pattern** (with the first-class `loading` prop as the alternative, §3). Toggle the visual state immediately, fire the effect, **revert + message on failure**, show a pending affordance for slow effects.
- **The async race condition is the recurring trap:** user toggles → local state flips → request fires → user toggles again before it resolves → conflicting mutations resolve out of order. The fix: apply `disabled`/`loading` on the first interaction to suppress re-toggle until the promise resolves, **or** use a concurrency primitive (React `useTransition`) to manage an internally-coordinated pending state — the same race discipline as combobox §11.
- **`role="switch"`** on a native `<input type="checkbox">` (or a `<button>`) with `aria-checked`; prefer the styled-native-input approach (checkbox §11); verify `role="switch"` AT support, checkbox fallback as the hedge. Watch the shadow-DOM label-detachment trap (§6).
- **Controlled/uncontrolled** — the checkbox traps apply (controlled `checked` with no `onChange` = frozen thumb). For async, the controlled value is the *server-confirmed source of truth*, with optimistic local state layered over it.
- **No `SwitchGroup`** — compose switches into List/settings-row layouts; `Switch.Control` is the nestable unit when the row owns the label.
- **Auto-wire the label** — generate ids to associate label↔input (`htmlFor`/`aria-labelledby`) so consumers can't ship orphaned, unlabelled switches.

## 12. Related and alternative components

- **Composes with:** Label, Description, status message (async outcome), List / SettingsRow (the canonical host that embeds `Switch.Control`), Form (rarely — switches are usually live settings, not staged form fields).
- **Alternative to:** Checkbox (staged binary — see checkbox), ToggleButton (`aria-pressed` action/mode — see toggle-button), Radio/Segmented (one-of-two exclusive labelled choice).
- **Supersedes:** a Checkbox misused for an immediate-effect setting; two radios used for a binary on/off where the off state is obvious; a `role=button`/`aria-pressed` toggle misused for a state setting.
- **Superseded by:** Checkbox when the change must be staged and submitted.

(Inherits the selection-control decomposition + nesting POV from checkbox, and **closes the arc by removing the group** — checkbox optional, radio mandatory, switch none. See checkbox for the staged-vs-immediate boundary from the other side, button for the switch-vs-toggle-button line; 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **From aesthetic to semantic.** A decade ago switch-vs-checkbox was treated as a styling choice ("iOSification" put sliding thumbs in web forms because they looked modern); the enforcement of `role="switch"` and Apple's App Store rejections forced a rigorous correction — **the immediate-effect contract is now the universal boundary**, not a look.
2. **`role="switch"` matured** from a risky newer role (backed by checkbox fallbacks) to the standard, distinguishing switch from checkbox in AT.
3. **Async moved into the component contract** — components are shifting from "dumb" UI toward orchestrators that handle optimistic updates and pending state internally (Primer's `loading`, Fluent's async triggers), abstracting network orchestration away from app code.
4. **The on/off affordance simplified** — Material dropped its in-thumb icon emphasis; the field trends to position+colour carrying state, hardcoded On/Off text rejected.
5. **Switch firmly separated from ToggleButton** (`role=switch`/`aria-checked` vs `aria-pressed`), where older systems conflated them.

## 14. Sources cited

Conservative dating (the external pass supplied largely 2024–2026 versions — Spectrum 2024.4, Primer React/Rails alpha 2024, Carbon v11/v12 2026, Fluent v9, Base Web v10.x, Material 3 web+Compose, Polaris v12 2025 — held loosely; the Polaris/Material Web-Components migration is the same cross-brief unverified claim flagged on Button/Text Field; `last-audited` is the re-run trigger):

- Adobe Spectrum / React Aria — `Switch`, `useSwitch`, `role="switch"`, `isReadOnly` (Spectrum, 2024).
- IBM Carbon — `Toggle`, read-only support, no-hardcoded-On/Off guidance (Carbon, 2024–2026).
- GitHub Primer — `ToggleSwitch` with first-class `loading` / `loadingLabel` / `loadingLabelDelay` (the async-aware reference) (Primer, 2024).
- Atlassian Design System — `Toggle` with a `busy` async state (Atlassian, 2024).
- Google Material 3 — `Switch` / `<md-switch>` (the `selected` naming outlier; shadow-DOM label trap) + Compose (Material 3, 2024–2026).
- Microsoft Fluent UI v9 — `Switch`, `labelPosition`, async triggers (Fluent, 2024).
- Uber Base Web — toggle via `Checkbox` `STYLE_TYPE='toggle'`, `labelPlacement` (Base Web, 2024).
- Shopify Polaris — the historically-debated/rejected switch (review-then-commit dashboard rationale) (Polaris, 2025).
- Apple Human Interface Guidelines — the canonical toggle; App Store enforcement of the immediate-effect boundary (Apple HIG, 2024).
- WAI-ARIA APG — the Switch pattern (`role="switch"`); the IA2 mapping quirk.
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 4.1.2, 1.4.1, 1.4.11, 2.4.13, 2.5.8, 4.1.3.

## 15. Agent-consumable schema

```yaml
identity:
  id: switch
  name: Switch
  aliases: [toggle, toggle-switch, on-off]
  category: form
  status: stable
description: >
  Control for a binary on/off setting that takes effect IMMEDIATELY (no
  save/submit). Independent — NO group. Closes the selection-control
  decomposition arc: checkbox optional group, radio mandatory, switch
  none. Not a staged binary (checkbox), not an action (toggle-button /
  aria-pressed), not a one-of-two exclusive choice (radio/segmented).
anatomy:
  decomposition:
    inherits: checkbox   # control + atomic primitive + nesting POV (see checkbox §2)
    switch-difference: >
      NO group (the arc's final refinement) — switches are independent,
      immediate; no SwitchGroup, no shared value, no group validation. A
      settings list of switches is a List/section of rows (layout), not a
      selection group; a SwitchGroup would invite the multi-select-array
      anti-pattern reserved for checkbox. Surface: Switch (labelled
      control) + Switch.Control (nestable primitive).
  parts: [track, thumb, label, description, track-content-optional, hidden-native-input, status-message]
api:
  inherits: [text-field, checkbox]   # field substrate + checkbox row shape (rich-content label, description, whole-row hit target, native naming)
  props:
    - {name: checked, type: boolean, required: false, description: the binary; onChange applies the effect IMMEDIATELY; pair defaultChecked (native naming; Material's 'selected' is the outlier)}
    - {name: label, type: node, required: false, description: rich content; names the SETTING not the state; does not change on toggle}
    - {name: description, type: node, required: false}
    - {name: labelPosition, type: enum, values: [leading, trailing], description: "label LEADS in settings rows (control at trailing edge — the switch habitat); control-leading inline in a form for sibling alignment. Default follows context (practice: leading in rows)"}
    - {name: loading/pending, type: boolean, default: false, description: first-class — locks input, swaps thumb for spinner, announces pending (Primer loadingLabel/delay); for high-latency/critical toggles}
    - {name: isReadOnly, type: boolean, default: false, description: SUPPORTED — aria-readonly, focusable, full contrast, distinct from disabled (admin review). No clean native readonly — implement via aria-readonly + prevented toggle}
    - {name: showStateLabel, type: boolean, default: false, description: inner-track check / I/O icons; off by default. NEVER hardcode adjacent On/Off text (redundant)}
  async-contract:
    practice-default: "OPTIMISTIC — toggle immediately (immediacy is the point), revert on error + message, pending affordance for slow effects, guard re-toggle races"
    alternative: "first-class loading/pending lock for high-latency/critical toggles where an inconsistent intermediate is harmful; ship both, default optimistic"
  not-applicable: [indeterminate, required]   # role=switch has no aria-checked=mixed; an on/off setting with a default isn't required
states:
  inherits: checkbox   # rest, hover, focus-visible, pressed, disabled
  switch-specific: [on, off, loading-pending, error-outcome, read-only]
  notes:
    loading-pending: "first-class — immediacy meets latency; track locked, thumb spinner, aria-busy"
    error: "OUTCOME error (the toggle didn't take) — revert thumb + message; not validation error"
    read-only: "SUPPORTED — aria-readonly=true, focusable, full contrast, visually distinct from disabled (lock affordance); admin-review need"
    no-indeterminate: true
variants:
  size: [small, medium]   # switches rarely warrant a large
  label-side: [leading, trailing]
  affordance: [plain-track, inner-track-check, inner-track-io]   # plain default; never colour-only; never hardcoded On/Off text
accessibility:
  inherits: [text-field, checkbox]
  wcag-criteria: ["4.1.2", "1.4.1", "1.4.11", "2.4.13", "2.5.8", "4.1.3"]
  role: "role=switch + aria-checked (announced ON/OFF) — DISTINCT from checkbox (role=checkbox, 'checked') and toggle-button (role=button + aria-pressed, 'pressed'). aria-pressed on a switch CORRUPTS the announcement. Verify role=switch on older AT; checkbox fallback hedge"
  not-colour-only: "thumb POSITION distinguishes on/off (1.4.1) — not track colour alone; hardcoded On/Off text is NOT the fix (redundant)"
  keyboard-model:
    tab: "each switch is its own tab stop (like checkbox, unlike radio)"
    space: "toggles (canonical W3C; Enter optional since the effect is action-like)"
  immediate-effect: "aria-checked flips on toggle (announced); async -> aria-busy + polite outcome/error (4.1.3); layout-changing toggle -> aria-live for the contextual change"
  traps: "IA2 quirk (role=switch + aria-pressed both map to IA2_ROLE_TOGGLE_BUTTON — author to ARIA spec, aria-checked); shadow-DOM label detachment (<md-switch> in <label> doesn't associate — set aria-label/labelledby)"
content:
  label-pattern: "names the SETTING ('Airplane Mode'), a stable noun/adjective — NOT the state, NOT a verb ('Turn on…'), does not flip on toggle; positive framing (on = affirmative)"
  on-off-text-pattern: "REJECT hardcoded adjacent On/Off text (redundant, duplicative SR output); rely on track state + role=switch announcement"
  error-pattern: "async failure: what didn't happen + that it reverted ('Couldn't turn on notifications. Try again.'); status message near the control"
motion:
  thumb-slide: "~150-200ms thumb translate (transform, not width) + synchronised track-colour crossfade — the literal RECEIPT of the immediate action; don't over-spring (toy-like)"
  async: "optimistic snap + spinner cross-fade onto the thumb; on failure slide BACK + error flash + toast"
  reduce-motion: "drop the slide, snap (0ms); track crossfade may remain under flashing thresholds"
i18n:
  inherits: checkbox
  switch-specific: "RTL inverts layout AND thumb travel — on at inline-end (right LTR / left RTL), track fill origin mirrors; avoid on/off track text (doesn't localise/expand); rows wrap label under ~300% expansion"
implementation:
  - "OPTIMISTIC update + revert-on-error is the core pattern; first-class loading/pending prop as the lock alternative"
  - "async race trap: apply disabled/loading on first interaction to suppress re-toggle until resolve, OR useTransition for an internally-coordinated pending state (combobox-style race discipline)"
  - "role=switch on native <input type=checkbox> (or <button>) + aria-checked; styled-native-input; verify AT support, checkbox fallback; watch shadow-DOM label detachment"
  - "controlled value = server-confirmed source of truth, optimistic local state layered over; checkbox controlled/uncontrolled traps apply"
  - "NO SwitchGroup — compose into List/settings rows; Switch.Control is the nestable unit; auto-wire label↔input to prevent orphaned controls"
composition:
  composes-with: [label, description, status-message, list, settings-row, form]
  decomposition-relationship: "Switch.Control composes into settings/list rows; NO SwitchGroup (closes the arc)"
  alternative-to: [checkbox, toggle-button, radio, segmented-control]
  supersedes: ["checkbox misused for an immediate-effect setting", "two radios for an obvious binary on/off", "aria-pressed toggle misused for a state setting"]
  superseded-by: ["checkbox when the change must be staged + submitted"]
notes:
  contested:
    - "async model: optimistic-by-default + revert (practice) vs first-class loading-lock (both shipped; default optimistic)"
    - "read-only: supported (adopted on the external pass's admin-review argument) vs the 'un-toggleable toggle is paradoxical' view"
    - "label side: leading in rows (practice) vs control-leading for sibling alignment (external) — context-driven, prop exposed"
    - "on/off affordance: plain track default; icons only where legibility demands; hardcoded On/Off text rejected"
  inherited: "selection-control decomposition + nesting POV from checkbox; NO group is the switch refinement that CLOSES the arc"
  unverified:
    - "role=switch announcement inside Shadow DOM on older Safari/VoiceOver without explicit aria-labels (Material 3 notes)"
    - "Polaris/Material Web-Components migration; external-supplied 2024-2026 version numbers"
  evolution: "aesthetic -> semantic (immediate-effect contract); role=switch matured; async moved into the component contract; on/off affordance simplified; switch separated from toggle-button"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-component-switch/` (15 June 2026), the third and final boolean/choice control — it **closes the selection-control decomposition arc** (checkbox: optional group; radio: mandatory; switch: none). Both passes confirmed the no-group refinement without hesitation and converged on the immediate-effect contract as the topological boundary with checkbox, `role="switch"` + `aria-checked` distinct from `aria-pressed`, the label-side prop for the settings-row pattern, describe-the-setting (not the state, not a verb) labels with positive framing, no indeterminate, the thumb-slide-as-receipt motion with RTL travel inversion, and `Switch` as the naming default over the ambiguous `Toggle`. The external pass moved two of the Claude pass's calls: it made the case for **supporting read-only** (admin dashboards reviewing settings they can't change — `aria-readonly`, focusable, full contrast, distinct from disabled), which the practice adopts over the initial "rare/awkward" stance; and it argued the **async model** toward a first-class `loading`/pending prop (Primer's `loading`/`loadingLabel`/`loadingLabelDelay`) — reconciled as optimistic-by-default *plus* a first-class lock for high-latency/critical toggles, shipping both. Other external contributions folded in: the Polaris-debated/rejected-switch framing and Apple App Store enforcement, the reject-hardcoded-On/Off-text guidance, the IA2 mapping quirk and shadow-DOM label-detachment traps, the `aria-live`-for-layout-change note, the async race-condition guard (disable/loading on first interaction, or `useTransition`), and the progressive-disclosure misuse. Claude-pass contributions: the no-group framing as the arc's closing move, the optimistic-default position, the thumb-slide-as-receipt motion framing, and the explicit inheritance from checkbox. The Polaris/Material Web-Components migration and the 2024–2026 version numbers are flagged unverified pending `_source-text/` backing. Conformant to `components/_schema.md` (inherits checkbox in the decomposition/api/states/i18n keys). The boolean/choice batch is complete; the selection-control decomposition now has a stated rule with all three variations resolved.*

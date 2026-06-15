# Switch — field-truth study (Claude pass)

## 1. Framing

Switch closes the boolean/choice arc. Checkbox set the selection-control decomposition (control + optional group + atomic primitive); Radio made the group mandatory; **Switch removes the group entirely.** A switch is an *independent* control — it is never one of a mutually-related set, so there is no SwitchGroup, no shared value, no group validation. The surface is just the labelled control (`Switch`) + the atomic primitive (`Switch.Control`) for nesting in settings rows. That's the structural news; the substance is what "immediate" demands.

What a Switch *is*: a control for a binary on/off **setting that takes effect immediately**, with no save/submit step — the user flips it and the system state changes now. What it *isn't*: a **staged** binary that's submitted with a form (Checkbox — the staged-vs-immediate boundary, stated here from the switch side and the inverse of checkbox §5), an **action with on/off pressed state** (ToggleButton, `aria-pressed`), or a **one-of-two exclusive choice** (Radio/Segmented). The tell: if there's a Save button, it's probably a Checkbox; if the change is live the instant you toggle, it's a Switch.

Why systems disagree: the **async/optimistic-update problem** (what "immediate" means when the effect is a fallible network call — §3, §11, the hardest part and the reason this brief is dual-agent), the **ARIA contract** (`role="switch"` vs checkbox vs `aria-pressed`), the **label side** (switches often lead with the label, unlike checkbox/radio), and the **on/off affordance** (text/icons on the track or not).

## 2. Anatomy and parts

Inherits the Checkbox decomposition (control + atomic primitive — see checkbox §2) **minus the group**. Parts: the **track** (the pill/rail), the **thumb** (the sliding knob), the **label**, an optional **description**, and optionally **on/off text or I/O icons** on the track or a state label beside it. The atomic **`Switch.Control`** is the nestable unit — a settings row or list row embeds it, the row supplies the label and hit target (the nesting POV, checkbox §2). There is **no SwitchGroup**: a "settings list" of switches is a layout (a List/section of rows), not a selection group — each switch owns its own independent boolean and there is no shared value or group validation. This is the decomposition's final refinement.

## 3. Properties / API

Inherits the form-field substrate and the checkbox row shape (rich-content label, description, disabled, the whole-row hit target — see checkbox §3), with switch-specific differences:

- `isSelected`/`checked` + `defaultSelected` / `onChange` — the binary; **but `onChange` is expected to perform the effect immediately** (§1). Native naming (`checked`), per the checkbox precedent.
- `label` + `description` — rich content; **label side** is the switch divergence (below).
- **`labelPosition` / label-side** — switches commonly place the **label leading, control trailing** (the settings-row pattern: label left, switch right), the opposite of checkbox/radio (control leads). The practice default: **label-leading in settings/list rows** (the control aligns to the row's trailing edge where the eye expects the toggle), **control-leading only when a switch sits inline in a form among other controls**. Expose `labelPosition` but default to context.
- **The async/pending contract — the load-bearing switch-specific API.** When `onChange` fires a fallible async effect, the component needs a story: an **`isPending`/`isLoading`** state (spinner or in-progress thumb), whether to **optimistically toggle then revert on error** vs. **toggle only on success** (defer), and disabling re-toggle during flight. The practice position: **optimistic by default** (toggle immediately, the whole point of a switch is immediacy), with **revert-on-error + an error message**, a pending affordance for slow effects, and guarding against rapid re-toggle races (§11). Defer (toggle-on-success) only when an inconsistent intermediate state is genuinely harmful.
- **No `indeterminate`** (binary, no mixed); **read-only** is rare and awkward (like checkbox/select, no clean native support — usually `disabled` or static); a switch is essentially never `required` (an on/off setting with a default isn't a required field).
- **on/off affordance** — `showStateLabel` / icons; a contested visual (below), off by default.

## 4. States and variants

| State | Switch-specific contract |
| --- | --- |
| on / off | the binary; thumb at the trailing/leading end; track colour shifts on |
| hover / focus-visible / pressed | as checkbox; focus ring on the control, ≥3:1 |
| disabled | non-interactive, muted |
| **loading / pending** | the async-effect-in-flight state (spinner/animated thumb, `aria-busy`); switch is one of the few controls where this is first-class, because immediacy meets latency (§3) |
| **error** | the effect failed — revert the visual state and surface a message; switch error is *outcome* error (the toggle didn't take), not validation error |
| read-only | rare; no clean native support |

No indeterminate. **Intentional variants:** `size`; **label-side** (leading default in rows / trailing inline); **with/without on-off affordance** (text or I/O icons on the track). No tone/emphasis. The on-affordance is the contested visual axis: iOS uses a plain coloured track; Material historically put an icon in the thumb; some systems show "On/Off" text. The practice default is **a plain track with a clear on-colour and thumb position** (the position + colour carry the state), adding on/off text only where state legibility is critical and space allows — never relying on colour alone (§6).

## 5. Usage guidance

- **Use** for a **binary on/off setting that applies immediately** — notifications on/off, dark mode, Wi-Fi, feature flags in a settings panel.
- **Don't use** for: a binary that's **submitted with a form** (→ Checkbox — if there's a Save button, it's staged); a **single consent/agree** (→ Checkbox); an **action** or a view-toggle in a toolbar (→ ToggleButton, `aria-pressed`); a **one-of-two exclusive choice with two labels** ("Card"/"Bank") (→ Radio/Segmented); or anything needing a **third/indeterminate** state (→ Checkbox).
- **Decision frameworks:**
  - **Switch vs. Checkbox is immediate-vs-staged** — the single most important call, and the boundary both prior briefs lean on. Live effect → Switch; save-on-submit → Checkbox.
  - **Switch vs. ToggleButton is setting-vs-action** — a switch sets a *state* (`role=switch`/`aria-checked`); a toggle button performs/persists an *action or mode* (`role=button`/`aria-pressed`), e.g. Bold in a toolbar. (See button §12.)
  - **Consequential/destructive toggles** — if flipping it is costly or hard to reverse (delete-on-toggle, irreversible billing change), pair with confirmation or use a Checkbox + explicit Save; a switch's immediacy is wrong for high-stakes changes.
  - **Don't use a switch where the result isn't immediately observable** — immediacy is the contract; if the user can't tell it took effect, reconsider.

## 6. Accessibility

Inherits the substrate (label association, the whole-row hit target, focus contrast — see checkbox §6). Switch-specific:

- **`role="switch"` + `aria-checked` (true/false)** is the contract — and the distinction from siblings is the headline: a **checkbox** is `role="checkbox"` (announced "checked/unchecked"), a **switch** is `role="switch"` (announced "on/off"), and a **toggle button** is `role="button"` + `aria-pressed` (announced "pressed"). Native `<input type="checkbox" role="switch">` (or `<button role="switch">`) is the baseline; `role="switch"` is well-supported but verify older AT (it's newer than checkbox) — some teams still back it with a checkbox fallback.
- **State must not be colour-only** — the **thumb position** must distinguish on/off (1.4.1 Use of Color); a switch that signals state by track colour alone fails for colour-blind users. On/off text or icons help but aren't required if position is clear.
- **Keyboard:** each switch is its **own tab stop** (like checkbox, unlike radio); **Space toggles** (Enter optionally toggles too, since the effect is immediate and action-like — a defensible deviation, but Space is the safe default). 
- **The immediate effect should be perceivable to AT** — `aria-checked` flips on toggle (announced); if there's a pending async state, `aria-busy` and a polite announcement of the outcome (or error) so a screen-reader user knows the live change took (or failed).
- **Target size** — the whole row / a ≥24–44px target (2.5.8), as checkbox.
- **WCAG SCs:** 4.1.2 (role/checked — the switch role doing the work), 1.4.1 (not colour-only), 1.4.11/2.4.13 (focus + track/thumb boundary contrast — the off-state track must be distinguishable from the background), 2.5.8 (target), and 4.1.3 (status message for async outcome/error).

## 7. Content guidelines

- **The label names the *setting*, not the state** — "Email notifications", not "Email notifications: On" and not "Turn on email notifications". The on/off is carried by the control, so the label is a stable noun phrase; toggling shouldn't change the label text (a common bug — a label that flips "Enable"/"Disable" is disorienting).
- **Positive framing** — the on state should be the affirmative ("Notifications" on = notifications enabled), so "on" maps to "more/yes" consistently across the product.
- **On/off text, if shown,** is "On"/"Off" (localised), not "Yes"/"No" or "1"/"0".
- **Error copy** (async failure) states what didn't happen and that it was reverted ("Couldn't turn on notifications. Try again."), near the control; SC 3.3.x-adjacent but really a status message.

## 8. Motion and transition

The **thumb slide** is the signature motion — the knob translates across the track (~100–200ms, eased) with a synchronised track-colour crossfade; it is the most physical, most recognisable micro-interaction in the form set, and it *communicates the state change* (position is the affordance, §6). A pending async state may show an in-thumb spinner or a pulsing thumb. Under `prefers-reduced-motion: reduce`, **drop the slide and snap the thumb** (with the colour change) — the state must remain instantly legible. Don't over-spring it; a bouncy switch reads as toy-like in a settings context. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL flips the thumb travel and the label side** — off is at the inline-start, on at the inline-end, so in RTL the thumb travels right-to-left and the on-position mirrors; use logical properties so this is automatic. The label-leading settings-row layout mirrors (label right, control left in RTL).
- **On/off text and labels expand** (German/Russian); the track must accommodate localised on/off text or — better — avoid track text so expansion isn't a layout risk. Label rows wrap with the control holding its row position.
- Inherits checkbox i18n otherwise (no text input, so IME is moot). (See 13-internationalization-and-rtl.)

## 10. Naming

The field splits: **`Switch`** (Spectrum/React Aria, Material, Fluent, Base Web) vs. **`Toggle`** (IBM Carbon, Atlassian) vs. **`ToggleSwitch`** (GitHub Primer). **The practice default is `Switch`** — it matches the ARIA `role="switch"` and the dominant naming, and avoids "Toggle" (which collides with toggle *button*). The atomic primitive: **`Switch.Control`**. Aliases to map: `Toggle`, `ToggleSwitch`, `OnOff`. **There is no `SwitchGroup`** — and that absence is worth documenting so consumers don't reach for one (a settings list is a List of rows).

## 11. Implementation notes

- **Optimistic update + revert is the core implementation pattern.** Toggle the visual state immediately on interaction (immediacy is the contract), fire the async effect, and **revert on failure with an error message**; show a pending affordance for slow effects and **guard against rapid re-toggle races** (an AbortController / request-id, or disable during flight — the same race discipline as combobox §11). The alternative — defer the visual toggle until the server confirms — makes the switch feel laggy and is only right when an inconsistent intermediate is harmful. Make optimistic-vs-deferred an explicit decision, optimistic by default.
- **`role="switch"`** on a native `<input type="checkbox">` (or a `<button>`), with `aria-checked` reflecting state; prefer the styled-native-input approach (checkbox §11). Verify `role="switch"` support on the AT matrix; a checkbox fallback is the conservative hedge for legacy AT.
- **Controlled/uncontrolled** — the checkbox traps apply (controlled `checked` with no `onChange` = frozen). For async, the controlled value is the *source of truth the server confirms*, with optimistic local state layered over it.
- **No SwitchGroup** — don't build one; compose switches into List/settings-row layouts. `Switch.Control` is the nestable unit when the row owns the label.
- **Don't animate `width`/layout** with the thumb — translate the thumb (`transform`) for GPU-friendly motion; reserve the track size.

## 12. Related and alternative components

- **Composes with:** Label, Description, FieldError/status message, List / settings-row (the common host), Form (rarely — switches are usually settings, not form fields), and `Switch.Control` into custom rows.
- **Alternative to:** Checkbox (staged binary — see checkbox), ToggleButton (`aria-pressed` action/mode — see button), Radio/Segmented (one-of-two exclusive with labels).
- **Supersedes:** a Checkbox misused for an immediate-effect setting; two radios used for on/off; a `role=button`/`aria-pressed` toggle misused for a state setting.
- **Superseded by:** Checkbox when the change must be staged and submitted; nothing else for immediate binary settings.

(Inherits the selection-control decomposition + nesting POV from checkbox; closes the arc by removing the group. See checkbox for the staged-vs-immediate boundary from the other side, button for the switch-vs-toggle-button line; 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **`role="switch"` matured** — once a risky newer role backed by checkbox fallbacks, now well-supported and the standard, distinguishing switch from checkbox in AT.
2. **The async/optimistic-update contract is being taken seriously** — as switches increasingly toggle live server state (feature flags, settings sync), the field is converging on optimistic-toggle + revert-on-error + pending, rather than pretending toggles are instant and infallible.
3. **The on/off affordance simplified** — Material dropped the in-thumb icon emphasis it once pushed; the field trends toward position+colour carrying state, on/off text only where legibility demands.
4. **Switch firmly separated from ToggleButton** — `role=switch`/`aria-checked` for settings vs `aria-pressed` for actions is now a clear line, where older systems conflated them.

## 14. Sources cited

(Conservative; reconcile with external pass.) Adobe Spectrum / React Aria `Switch` (`useSwitch`, role=switch) (2024–2025); IBM Carbon `Toggle` (2024); Shopify Polaris (checkbox-as-setting / `Setting toggle`) (2024); GitHub Primer `ToggleSwitch` (with a loading/in-progress state — the async-aware reference) (2024); Atlassian `Toggle` (2024); Google Material 3 Switch (thumb/track, dropped icon emphasis) + Compose (2024); Microsoft Fluent `Switch` (2024); Base Web `Checkbox` with `STYLE_TYPE='toggle'` (2024); Apple HIG toggle (the canonical mobile switch) (2024); WAI-ARIA APG Switch pattern (role=switch); WCAG 2.2 (Oct 2023) — 4.1.2, 1.4.1, 1.4.11, 2.4.13, 2.5.8, 4.1.3.

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
  save/submit). Independent — NO group (closes the selection-control
  decomposition arc: checkbox optional group, radio mandatory, switch no
  group). Not a staged binary (checkbox), not an action (toggle-button /
  aria-pressed), not a one-of-two exclusive choice (radio/segmented).
anatomy:
  decomposition:
    inherits: checkbox   # control + atomic primitive + nesting POV (see checkbox §2)
    switch-difference: >
      NO group — a switch is independent and immediate; there is no
      SwitchGroup, no shared value, no group validation. A settings list
      of switches is a List/section of rows (layout), not a selection
      group. Surface: Switch (labelled control) + Switch.Control (nestable
      primitive). This is the decomposition's final refinement.
  parts: [track, thumb, label, description, on-off-text-or-icons-optional, status-message]
api:
  inherits: [text-field, checkbox]   # field substrate + checkbox row shape (rich-content label, description, whole-row hit target, native naming)
  props:
    - {name: checked, type: boolean, required: false, description: the binary; onChange is expected to apply the effect IMMEDIATELY; pair defaultSelected (native naming per checkbox)}
    - {name: label, type: node, required: false, description: rich content; names the SETTING not the state}
    - {name: description, type: node, required: false}
    - {name: labelPosition, type: enum, values: [leading, trailing], default: leading-in-rows/trailing-inline, description: "label LEADS in settings rows (control at row trailing edge) — opposite of checkbox/radio; control-leading only inline in a form"}
    - {name: isPending/isLoading, type: boolean, default: false, description: async effect in flight; spinner/animated thumb + aria-busy}
    - {name: showStateLabel, type: boolean, default: false, description: on/off text or I/O icons; off by default (position+colour carry state)}
  async-contract:
    practice-default: "OPTIMISTIC — toggle immediately (immediacy is the point), revert on error + show a message, pending affordance for slow effects, guard rapid re-toggle races"
    alternative: "deferred (toggle on success) only when an inconsistent intermediate is harmful"
  not-applicable: [indeterminate, required]   # binary, no mixed; an on/off setting with a default isn't required
states:
  inherits: checkbox   # rest, hover, focus-visible, pressed, disabled, read-only(rare/awkward)
  switch-specific: [on, off, loading-pending, error-outcome]
  notes:
    loading-pending: "first-class here — immediacy meets latency; aria-busy"
    error: "OUTCOME error (the toggle didn't take) — revert visual + message; not validation error"
    no-indeterminate: true
variants:
  size: [small, medium, large]
  label-side: [leading, trailing]
  affordance: [plain-track, with-on-off-text, with-icons]   # plain default; never colour-only
accessibility:
  inherits: [text-field, checkbox]
  wcag-criteria: ["4.1.2", "1.4.1", "1.4.11", "2.4.13", "2.5.8", "4.1.3"]
  role: "role=switch + aria-checked (announced on/off) — DISTINCT from checkbox (role=checkbox, 'checked') and toggle-button (role=button + aria-pressed, 'pressed'); verify role=switch on older AT, checkbox fallback as a hedge"
  not-colour-only: "thumb POSITION must distinguish on/off (1.4.1) — not track colour alone"
  keyboard-model:
    tab: "each switch is its own tab stop (like checkbox, unlike radio)"
    space: "toggles (Enter optional, since the effect is action-like)"
  immediate-effect: "aria-checked flips on toggle (announced); async -> aria-busy + polite outcome/error announcement (4.1.3)"
  target-size: "whole row / >=24-44px (2.5.8)"
content:
  label-pattern: "names the SETTING, a stable noun phrase ('Email notifications') — NOT the state, NOT 'Enable/Disable' that flips on toggle; positive framing (on = affirmative)"
  on-off-text-pattern: "'On'/'Off' (localised) if shown — not Yes/No or 1/0"
  error-pattern: "async failure: what didn't happen + that it reverted ('Couldn't turn on notifications. Try again.'); status message near the control"
motion:
  thumb-slide: "~100-200ms thumb translate + track-colour crossfade — communicates the state change (position is the affordance); don't over-spring (toy-like in settings)"
  reduce-motion: "drop the slide, snap the thumb + colour; state stays instantly legible"
  perf: "translate the thumb (transform), don't animate width/layout"
i18n:
  inherits: checkbox
  switch-specific: "RTL flips thumb travel (off at inline-start, on at inline-end — mirrors) and the label-leading row layout; on/off track text expands — prefer avoiding track text"
implementation:
  - "OPTIMISTIC update + revert-on-error is the core pattern: toggle immediately, fire effect, revert + message on failure, pending affordance, guard re-toggle races (AbortController/request-id or disable in flight)"
  - "role=switch on native <input type=checkbox> (or <button>) + aria-checked; styled-native-input; verify role=switch AT support, checkbox fallback hedge"
  - "controlled value = server-confirmed source of truth, optimistic local state layered over it; checkbox controlled/uncontrolled traps apply"
  - "NO SwitchGroup — compose into List/settings rows; Switch.Control is the nestable unit when the row owns the label"
  - "translate the thumb (transform), not width/layout"
composition:
  composes-with: [label, description, status-message, list, settings-row, form]
  decomposition-relationship: "Switch.Control composes into settings/list rows; NO SwitchGroup (the arc's final refinement)"
  alternative-to: [checkbox, toggle-button, radio, segmented-control]
  supersedes: ["checkbox misused for an immediate-effect setting", "two radios used for on/off", "aria-pressed toggle misused for a state setting"]
  superseded-by: ["checkbox when the change must be staged + submitted"]
notes:
  contested:
    - "async/optimistic-update model (practice: optimistic + revert; deferred only when intermediate is harmful)"
    - "label side (leading in rows / trailing inline)"
    - "on/off affordance (plain track default; text/icons only where legibility demands)"
    - "role=switch maturity vs checkbox fallback for legacy AT"
  inherited: "the selection-control decomposition + nesting POV from checkbox; NO group is the switch refinement (closes the arc)"
  evolution: "role=switch matured; async/optimistic contract taken seriously; on/off affordance simplified; switch firmly separated from toggle-button"
```

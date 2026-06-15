---
okf_version: "0.1"
type: component-brief
title: Toggle Button
description: A Button that carries a persistent binary pressed state. A claude-only brief standing on the Button substrate and the already-settled aria-pressed-vs-role-switch-vs-role-checkbox distinction — it states the setting-vs-action/mode boundary from the toggle side, the persistent-selected vs transient-:active trap, the constant-name + aria-pressed pattern, and the standalone-vs-group (ToggleButtonGroup / Segmented Control) decomposition.
tags: [components, form]
category: Form
status: stable
aliases: [toggle, pressable-button, selectable-button]
last-audited: 2026-06-15
timestamp: 2026-06-15
---

# Toggle Button

> Toggle Button is a Button that remembers. It inherits the entire Button substrate — native `<button>`, the intent/appearance/size model, the press behaviour, icon-only requiring an accessible name (see button) — and adds one thing: a **persistent binary pressed state**. The contested part of that addition, *which* ARIA state to use, was already settled in the Button and Switch briefs (`aria-pressed`, not `role=switch`, not `role=checkbox`); this brief states the boundary from the toggle side and resolves the mechanics that follow — the persistent-vs-transient state trap, the constant-name pattern, and how a lone toggle relates to a group.

---

## 1. Framing

A Toggle Button is an **action or mode that stays on** — a button whose pressed state persists between interactions: Bold in a formatting toolbar, Mute, Pin, Favourite, a filter pill that stays active. It inherits the Button substrate and the only thing it adds is *state that persists* (`aria-pressed`).

What it *isn't*: a one-shot **Button** (fires and forgets, no persistent state); a **Switch** (a *system setting*, `role="switch"`/`aria-checked`, drawn as a track+thumb); or a **Checkbox** (a *staged* form value, `role="checkbox"`, committed on submit). The `aria-pressed` vs `role="switch"` vs `role="checkbox"` distinction is the same one the Button brief calls out (button §6) and the Switch brief draws from the other side (switch §5) — resolved already; this brief inherits it.

It also sits in the selection-control decomposition from the *button* family's side: the Toggle Button is the **atomic unit**, and a set of them is a **ToggleButtonGroup** — which, presented as a connected horizontal control, *is* a Segmented Control (see segmented-control). A lone toggle (Bold) is independent; a single-select group (Grid/List view) carries radiogroup semantics; a multi-select group is a set of independent toggles.

## 2. Anatomy and parts

Inherits Button anatomy (the `<button>`, label and/or icon, leading/trailing visual, focus ring — see button §2). The one structural addition is the **persistent selected/pressed visual** — a filled, inset, or otherwise "on" treatment that must be distinct from both the rest state *and* the transient `:active` press (§4). Icon-only is the common shape (toolbars), so an accessible name is required (the icon-only-button contract — see button §6, icon §5). The atomic Toggle Button composes into a `ToggleButtonGroup` (segmented-control).

## 3. Properties / API

Inherits the Button API (intent / appearance / size, `leadingVisual` / `trailingVisual`, `isDisabled` — see button §3). Toggle-Button-specific:

- **`isSelected` / `pressed` + `defaultSelected` + `onChange`** — the persistent binary, wired to `aria-pressed`. (The transient `:active` press is *not* a prop — it's the Button substrate's existing behaviour; conflating the two is the signature bug, §4.)
- **accessible name — required and constant** (`aria-label="Mute"`); state is carried by `aria-pressed`, not by a label that flips (§6).
- In a group, **selection is owned by the group**, not the individual toggle (single-select = one pressed at a time; multi = independent) — see segmented-control §11.

## 4. States and variants

Inherits Button states (rest / hover / focus-visible / transient-pressed / disabled — see button §4) **plus the persistent `selected` (pressed-on) state**: the visual "on," and the one genuinely new thing here. The defining trap: **`selected` must be visually distinct from the transient `:active` press** — if a persistent toggle looks identical to a momentary button press, users can't tell what's currently on. Use a durable fill/border/inset for `selected`, separate from the brief `:active` feedback. No loading/error of its own beyond Button's.

**Variants:** size and appearance carry over (the `selected` treatment must read against the chosen appearance); icon-only vs. icon+label; standalone vs. grouped. No tone axis beyond Button's.

## 5. Usage guidance

- **Use** for a persistent action/mode, usually icon-based in a command surface: text formatting (Bold / Italic / Underline), Mute, Pin, Favourite, a view or filter toggle that stays active.
- **Don't use** for: a system **setting** conceptually on/off (Wi-Fi, notifications) → **Switch**; a **staged** form value committed on submit → **Checkbox**; a **one-shot** action → **Button**; **navigation** → **Link**; **exactly-one of standard form options** → **Radio** (or **Segmented Control** if the presentation should be compact/toggle-like).
- **Decision frameworks:**
  - **Switch vs. Toggle Button is setting-vs-action/mode, plus visual:** a switch is a labelled *system setting* drawn as a track+thumb; a toggle button is a (usually icon) button that *looks pressed*, living in a toolbar or command surface. (switch §5, button §12.)
  - **Standalone vs. group:** a lone toggle (Bold) is independent; a set where exactly one is active (Grid/List) is a single-select `ToggleButtonGroup` = Segmented Control (radiogroup semantics); a set of independent on/off toggles is a multi-select group.

## 6. Accessibility

Inherits the Button substrate (button §6); Toggle-Button-specific:

- **`role="button"` + `aria-pressed="true|false"`** is the contract — distinct from `role="switch"` + `aria-checked` (a *setting*) and `role="checkbox"` + `aria-checked` (a *staged* value). Putting the wrong one on a toggle is a common AT bug (button §6).
- **Constant accessible name + `aria-pressed`** is the practice default (per APG): the name stays "Mute" and `aria-pressed` conveys on/off — *not* a label that flips "Mute"/"Unmute" with no `aria-pressed`. The flip pattern loses the state semantics and has historically tripped some assistive tech; if a product insists on a state-describing label, it must *still* expose state via `aria-pressed` rather than replace it.
- **Keyboard:** Space **and** Enter activate (it's a button — unlike Switch's Space-only); each standalone toggle is its own tab stop; a single-select group uses the roving radiogroup model (segmented-control §6).
- **Pressed-state perceivability:** the `selected` state must be distinguishable by more than colour — a fill/border/inset (1.4.1) — with ≥3:1 boundary contrast (1.4.11).
- **WCAG SCs:** 4.1.2 (role/pressed), 1.4.1 (not colour-only), 1.4.11 / 2.4.13 (focus + selected-boundary contrast), 2.5.8 (target size), 2.5.3 (Label in Name, where a visible label exists).

## 7. Content guidelines

Icon-only is common, so the accessible name *is* the content: a concise verb or noun naming the action/mode ("Bold", "Mute", "Pin"), held **constant** across state (§6). With a visible label, keep it stable too — don't flip it on toggle. A Tooltip commonly supplies the name for icon-only toggles (with the don't-put-essential-info-only-in-a-tooltip caveat — button §12).

## 8. Motion and transition

The `selected`-state transition (background fill / inset) is a short token-driven change (~100–150ms), and must be visually separable from the transient `:active` feedback (§4). Under `prefers-reduced-motion: reduce`, resolve to an instant state change (button §8). No layout motion. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

Inherits Button i18n (logical-property RTL, mirror directional icons only, no fixed-width labels — see button §9). A toolbar of toggle buttons reorders under RTL via logical layout; the `selected` treatment is direction-neutral.

## 10. Naming

`ToggleButton` is the field default (Adobe Spectrum, Microsoft Fluent, MUI); some systems fold it into Button via a `toggle`/`isSelected` prop, and a few call it `Toggle` (which collides with Switch-as-Toggle and is avoided). **The practice default is `ToggleButton`** (atomic) **+ `ToggleButtonGroup`** (the group, which presented compactly is the Segmented Control — see segmented-control). Aliases to map: `Toggle`, `PressableButton`, `SelectableButton`.

## 11. Implementation notes

- **`aria-pressed` on a real `<button>`**, toggled on activate, inheriting the Button press primitive (button §11). Do **not** use `role="switch"`/`aria-checked` (that's Switch) or `aria-selected` (that's listbox/tab).
- **Controlled/uncontrolled** via `isSelected`/`defaultSelected`; the controlled-without-`onChange` (frozen) trap from text-field applies.
- **Distinguish persistent `selected` from transient `:active`** in both styling and state — the most common Toggle Button implementation bug (§4).
- **In a group**, the group owns selection: single-select = a roving-tabindex radiogroup; multi-select = independent `aria-pressed` buttons inside a `role="group"` (segmented-control §11).

## 12. Related and alternative components

- **Composes with:** Icon (the common content — see icon), Tooltip (icon-only name), ToggleButtonGroup / Segmented Control (the group — see segmented-control), Toolbar (the host).
- **Alternative to:** Button (one-shot vs persistent state — see button), Switch (system setting vs action/mode — see switch), Checkbox (staged value vs immediate action — see checkbox), Radio (standard form options vs a compact toggle group).
- **Supersedes:** a Button hand-wired with ad-hoc "active" styling and no `aria-pressed`; `aria-checked`/`role="switch"` misused for a toolbar mode.
- **Superseded by:** Switch when it is really a system setting; Segmented Control when it is a single-select set presented compactly.

(Inherits the Button substrate; the atomic-vs-group relationship connects to the selection-control decomposition (see checkbox) and is developed in segmented-control. See button for the substrate and the `aria-pressed`/`aria-expanded`/`aria-checked` distinction; switch for the setting-vs-action boundary; 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **`aria-pressed` firmly separated** from `role="switch"` and `aria-checked` — older systems conflated toolbar toggles with switches and checkboxes.
2. **Constant-name + `aria-pressed`** affirmed over the label-flip pattern.
3. **ToggleButton as its own named component** (Spectrum/Fluent/MUI) rather than a Button `toggle` prop, with `ToggleButtonGroup` as the group primitive that feeds the Segmented Control.

## 14. Sources cited

Conservative dating (claude-only run; `last-audited` is the re-run trigger):

- Adobe Spectrum / React Aria — `ToggleButton` / `useToggleButton` (Spectrum, 2024–2025).
- Google Material 3 — icon buttons / toggle buttons (selected state) (Material 3, 2024).
- Microsoft Fluent UI — `ToggleButton` (Fluent, 2024).
- MUI — `ToggleButton` / `ToggleButtonGroup` (the atomic + group reference) (MUI, 2024).
- GitHub Primer, Atlassian, Uber Base Web — button-with-pressed-state patterns (2024).
- Apple Human Interface Guidelines — toggle/selected buttons (Apple HIG, 2024).
- WAI-ARIA APG — Button (toggle) pattern (`aria-pressed`).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 4.1.2, 1.4.1, 1.4.11, 2.4.13, 2.5.3, 2.5.8.

## 15. Agent-consumable schema

```yaml
identity:
  id: toggle-button
  name: Toggle Button
  aliases: [toggle, pressable-button, selectable-button]
  category: form
  status: stable
description: >
  A Button that carries a PERSISTENT binary pressed state (role=button +
  aria-pressed) — an action/mode that stays on. Not a one-shot button (no
  persistent state), not a switch (system setting, role=switch), not a
  checkbox (staged value, role=checkbox). Atomic unit of a
  ToggleButtonGroup / Segmented Control.
anatomy:
  inherits: button   # <button>, label/icon, leading/trailing visual, focus ring (see button §2)
  addition: persistent selected/pressed visual (distinct from rest AND transient :active)
  decomposition: "atomic ToggleButton composes into ToggleButtonGroup (= Segmented Control presented compactly); connects to the selection-control decomposition from the button side"
api:
  inherits: button   # intent/appearance/size, leadingVisual/trailingVisual, isDisabled (see button §3)
  props:
    - {name: isSelected/pressed, type: boolean, required: false, description: persistent binary, wired to aria-pressed; pair defaultSelected/onChange}
    - {name: accessible-name, type: string, required: true (icon-only), description: CONSTANT (aria-label='Mute'); state via aria-pressed, NOT a flipping label}
  note: "the transient :active press is NOT a prop — it's the button substrate; don't conflate with isSelected"
states:
  inherits: button   # rest, hover, focus-visible, transient-pressed, disabled
  toggle-specific: [selected]
  trap: "selected (persistent) MUST be visually distinct from :active (transient) — the signature bug"
variants:
  size: [small, medium, large]
  appearance: [solid, outline, plain]   # selected must read against the appearance
  shape: [icon-only, icon+label]
  grouping: [standalone, grouped]
accessibility:
  inherits: button
  wcag-criteria: ["4.1.2", "1.4.1", "1.4.11", "2.4.13", "2.5.3", "2.5.8"]
  role: "role=button + aria-pressed=true|false — DISTINCT from role=switch+aria-checked (setting) and role=checkbox+aria-checked (staged)"
  name-pattern: "CONSTANT accessible name + aria-pressed (APG) — not a label that flips Mute/Unmute without aria-pressed"
  keyboard-model: "Space AND Enter (it's a button — unlike switch's Space-only); standalone = own tab stop; single-select group = roving radiogroup"
  pressed-perceivability: "selected distinguishable by fill/border/inset, not colour alone (1.4.1); >=3:1 boundary (1.4.11)"
content:
  label-pattern: "concise verb/noun naming the action/mode ('Bold','Mute','Pin'); CONSTANT across state; icon-only name often via Tooltip"
motion:
  selected-transition: "~100-150ms fill/inset, visually separable from transient :active; reduce-motion -> instant"
i18n:
  inherits: button   # logical-prop RTL, mirror directional icons only, no fixed-width labels
implementation:
  - "aria-pressed on a real <button>, toggled on activate (button press primitive); NOT role=switch/aria-checked, NOT aria-selected"
  - "controlled/uncontrolled isSelected/defaultSelected; controlled-without-onChange = frozen"
  - "distinguish persistent selected from transient :active in styling AND state"
  - "in a group: single-select = roving-tabindex radiogroup; multi-select = independent aria-pressed buttons in role=group (see segmented-control)"
composition:
  composes-with: [icon, tooltip, toggle-button-group, segmented-control, toolbar]
  alternative-to: [button, switch, checkbox, radio]
  supersedes: ["button with ad-hoc 'active' styling and no aria-pressed", "role=switch/aria-checked misused for a toolbar mode"]
  superseded-by: ["switch when it is a system setting", "segmented-control when it is a compact single-select set"]
notes:
  inherited: "the Button substrate (button) and the aria-pressed-vs-role-switch-vs-role-checkbox distinction (button §6, switch §6) — not re-derived"
  contested:
    - "constant-name + aria-pressed (practice) vs label-flip pattern"
    - "standalone toggle vs single/multi-select group (group owns selection)"
  evolution: "aria-pressed separated from switch/checkbox; constant-name affirmed; ToggleButton as its own component feeding ToggleButtonGroup/Segmented Control"
```

---

*Provenance: claude-only research run, `_research/_inbound/2026-06-15-component-toggle-button/` (15 June 2026), sanctioned because the component is largely convergent and stands on two already-briefed components: it inherits the Button substrate (button) and the `aria-pressed`-vs-`role=switch`-vs-`role=checkbox` distinction already resolved in the Button (§6) and Switch (§6) briefs. The load-bearing calls: the persistent-state contract (`aria-pressed`), the setting-vs-action/mode boundary with Switch (a switch is a system setting drawn as a track+thumb; a toggle button is a usually-icon button that looks pressed), the persistent-`selected`-vs-transient-`:active` visual trap, the constant-accessible-name + `aria-pressed` pattern over the label-flip, Space-and-Enter activation, and the atomic-vs-group decomposition that hands off to the Segmented Control brief. Paired with the Segmented Control dual-agent run as the close of the toggle-group boundary the form batch repeatedly referenced. The §15 schema is conformant to `components/_schema.md` (inherits button). Flagged as a candidate for a dual-agent second pass only if the constant-name-vs-label-flip a11y question needs adversarial depth.*

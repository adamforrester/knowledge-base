# ToggleButton — Claude pass (claude-only run)

## 1. Framing
ToggleButton is a Button that keeps a **persistent binary pressed state** — it inherits the whole Button substrate (see button) and adds *state that stays on*. What it is: an action/mode that persists (Bold in a toolbar, Mute, Pin, Favourite, a filter pill that stays active). What it isn't: a one-shot Button (no persistent state), a Switch (a *system setting*, `role=switch`/`aria-checked`, visually a track+thumb), or a Checkbox (a *staged* form value, `role=checkbox`). The contested call — `aria-pressed` vs `role=switch` vs `role=checkbox` — is already resolved (button §6, switch §6); this brief states the boundary from the toggle-button side and adds the persistent-state mechanics. It ties to the selection-control decomposition from the button family's side: ToggleButton is the atomic unit; ToggleButtonGroup / Segmented Control is the group (see segmented-control).

## 2. Anatomy and parts
Inherits Button anatomy (the `<button>`, label and/or icon, leading/trailing visual, focus ring — see button §2). The one addition is the **persistent selected/pressed visual** (a filled/inset/"on" background distinct from rest and from the transient `:active` press). Icon-only is the common shape (toolbar), so an accessible name is required (button icon-only / icon §5). The atomic ToggleButton composes into a ToggleButtonGroup (segmented-control).

## 3. Properties / API
Inherits the Button API (intent/appearance/size, leadingVisual/trailingVisual, isDisabled — see button §3). ToggleButton-specific:
- `isSelected`/`pressed` + `defaultSelected` + `onChange` — the persistent binary; wired to `aria-pressed`.
- accessible name — required, **constant** (`aria-label="Mute"`), state carried by `aria-pressed` (§6), not a flipping label.
- In a group, selection is owned by the group (single-select group = one pressed at a time; multi = independent) — see segmented-control.
The transient press (`:active`) is *not* a prop — it's the button substrate's existing behaviour; don't conflate it with `isSelected`.

## 4. States and variants
Inherits Button states (rest/hover/focus-visible/transient-pressed/disabled — see button §4) **plus the persistent `selected` (pressed-on) state** — the visual "on," distinct from the momentary `:active`. No loading/error of its own beyond Button's. Variants: size, appearance (the selected state reads against the chosen appearance), icon-only/icon+label, standalone vs grouped. The trap: designing `selected` to look like `:active` so users can't tell a persistent toggle from a transient press — they must be visually distinct.

## 5. Usage guidance
- **Use** for a persistent action/mode, usually icon-based in a toolbar: text formatting (Bold/Italic/Underline), Mute, Pin, Favourite, a view/filter toggle that stays active.
- **Don't use** for: a system **setting** conceptually on/off (Wi-Fi, notifications) → **Switch**; a **staged** form value → **Checkbox**; a **one-shot** action → **Button**; **navigation** → **Link**; **exactly-one-of-many** standard form options → **Radio** (or **Segmented Control** if compact/toggle-like).
- **Switch vs. ToggleButton** is *setting-vs-action/mode* + visual: a switch is a labelled system setting drawn as a track+thumb; a toggle button is a (usually icon) button that looks pressed, living in a toolbar/command surface. (button §12, switch §5.)
- **Standalone vs group:** a lone toggle (Bold) is independent; a set where exactly one is active (Grid/List view) is a single-select ToggleButtonGroup = Segmented Control (radiogroup semantics); a set of independent toggles is a multi-select group.

## 6. Accessibility
- **`role="button"` + `aria-pressed="true|false"`** — the contract, distinct from `role="switch"`+`aria-checked` (setting) and `role="checkbox"`+`aria-checked` (staged). Conflating them is a common AT bug (button §6).
- **Constant accessible name + `aria-pressed`** is the practice default (APG): the name stays "Mute" and `aria-pressed` conveys on/off — *not* a label that flips "Mute"/"Unmute" with no `aria-pressed` (the flip pattern loses state semantics and historically tripped some AT). If a product insists on a state-describing label, it must still expose state via `aria-pressed`, not replace it.
- **Keyboard:** Space **and** Enter activate (it's a button — unlike switch's Space-only); each toggle is its own tab stop; a single-select group uses the radiogroup roving model (segmented-control).
- **Pressed-state contrast** — the selected state must be distinguishable by more than colour (a fill/border/inset), ≥3:1 for the boundary (1.4.11), and must not rely on colour alone (1.4.1).
- WCAG: 4.1.2 (role/pressed), 1.4.1, 1.4.11/2.4.13 (focus + selected-boundary contrast), 2.5.8 (target), 2.5.3 (Label in Name for the visible-label case). Inherits button §6 otherwise.

## 7. Content guidelines
Icon-only is common → the accessible name is the whole content: a concise verb/noun naming the action/mode ("Bold", "Mute", "Pin"), constant across state (§6). With a visible label, keep it stable too. A Tooltip commonly supplies the name for icon-only toggles (with the don't-tooltip-essential-info caveat — button §12).

## 8. Motion and transition
The selected-state transition (background fill / inset) is a short token-driven change (~100–150ms), distinct from the transient `:active` feedback; reduce-motion resolves to an instant state change (button §8). No layout motion.

## 9. Internationalization
Inherits button i18n (logical-property RTL, mirror directional icons only, no-fixed-width labels — button §9). A toolbar of toggle buttons reorders under RTL via logical layout.

## 10. Naming
`ToggleButton` (Spectrum, Fluent, MUI) is the field default; some systems fold it into Button with a `toggle`/`isSelected` prop or call it `Toggle` (collides with Switch-as-Toggle). Practice default: **`ToggleButton`** (atomic) + **`ToggleButtonGroup`** (the group; ≈ Segmented Control). Aliases: `Toggle`, `PressableButton`, `SelectableButton`.

## 11. Implementation notes
- **`aria-pressed` on a real `<button>`**, toggled on activate; inherits the button press primitive (button §11). Don't use `role=switch`/`aria-checked` (that's Switch) or `aria-selected` (that's listbox/tab).
- **Controlled/uncontrolled** `isSelected`/`defaultSelected` (the button substrate is otherwise stateless); the controlled-without-onChange trap applies.
- **Distinguish persistent `selected` from transient `:active`** in both styling and state — the most common ToggleButton bug.
- **In a group**, the group owns selection (single-select = roving radiogroup; multi = independent `aria-pressed` buttons in a `role=group`) — see segmented-control §11.

## 12. Related and alternative components
- **Composes with:** Icon (the common content), Tooltip (icon-only name), ToggleButtonGroup / Segmented Control (the group), Toolbar (the host).
- **Alternative to:** Button (persistent state vs one-shot), Switch (action/mode vs system setting — see switch), Checkbox (immediate action vs staged value — see checkbox), Radio (compact toggle group vs standard form options).
- **Supersedes:** a Button hand-wired with ad-hoc "active" styling and no `aria-pressed`; `aria-checked`/`role=switch` misused for a toolbar mode.
- **Superseded by:** Switch when it's really a system setting; Segmented Control when it's a single-select set presented compactly.

(Inherits the Button substrate; the atomic-vs-group relationship connects to the selection-control decomposition (checkbox) and is developed in segmented-control. See button for the substrate and the aria-pressed/aria-expanded/aria-checked distinction; switch for the setting-vs-action boundary.)

## 13. Field POV evolution
1. `aria-pressed` firmly separated from `role=switch` and `aria-checked` (older systems conflated toolbar toggles with switches/checkboxes).
2. Constant-name + `aria-pressed` affirmed over the label-flip pattern.
3. ToggleButton increasingly its own named component (Spectrum/Fluent/MUI) rather than a Button `toggle` prop, with ToggleButtonGroup as the group primitive feeding Segmented Control.

## 14. Sources cited
(Conservative.) Adobe Spectrum / React Aria `ToggleButton`/`useToggleButton` (2024–2025); Material 3 icon/toggle buttons (2024); Microsoft Fluent `ToggleButton` (2024); MUI `ToggleButton`/`ToggleButtonGroup` (2024); GitHub Primer, Atlassian, Base Web button-with-pressed (2024); Apple HIG (2024); WAI-ARIA APG Button (toggle) pattern; WCAG 2.2 (Oct 2023) — 4.1.2, 1.4.1, 1.4.11, 2.4.13, 2.5.3, 2.5.8.

## 15. Agent-consumable schema (see toggle-button.md for the conformed block)
identity/description/api(inherits button)/states(inherits button + selected)/variants/accessibility(role=button+aria-pressed)/content/motion/i18n/implementation/composition/notes — persistent-state, constant-name+aria-pressed, setting-vs-action boundary, atomic-vs-group.
